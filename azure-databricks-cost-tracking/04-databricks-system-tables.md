**Navigation:** [← Chapter 3 — Tagging for Cost Attribution](03-tagging-for-cost-attribution.md) | [Index](index.md) | [Next: Chapter 5 — Daily Cost Tracking with az CLI →](05-az-cli-daily-usage.md)

> **Rule:** Azure Cost Management shows DBU charges as one Marketplace line item. To drill down to specific clusters, jobs, or users, you need Databricks system tables — the only source of per-entity DBU attribution.

---

## THE PROBLEM

Azure Cost Management shows DBU charges as a single Marketplace line item. The number might be large. It tells you nothing about which clusters consumed the most DBUs, which jobs ran over budget, or which users left clusters running overnight. From Cost Management's perspective, the entire Databricks footprint is one opaque blob.

Databricks system tables solve this. They expose per-record DBU consumption with cluster IDs, job IDs, run names, user identities, and custom tags — everything you need to answer "who spent what and on what." They are the only source of this granularity on Azure.

---

## THE CONCEPT

Two tables in `system.billing` provide everything needed for DBU cost attribution: `system.billing.usage` records every unit of DBU consumption, and `system.billing.list_prices` records the list price for every SKU over time. Joining them gives you a dollar figure for any slice of usage.

### Prerequisites

- Unity Catalog must be enabled on the workspace
- An account admin or metastore admin must run:
  ```sql
  GRANT SELECT ON system.billing.usage TO <principal>;
  ```
- Premium tier is required — Standard tier workspaces do not have system table access

### Table 1: `system.billing.usage`

One row per usage record. Partitioned by `usage_date`.

| Column | Type | Description |
|---|---|---|
| record_id | STRING | Unique record identifier |
| account_id | STRING | Databricks account ID |
| workspace_id | STRING | Workspace where usage occurred |
| sku_name | STRING | e.g., PREMIUM_ALL_PURPOSE_COMPUTE |
| cloud | STRING | AZURE |
| usage_start_time | TIMESTAMP | Start of usage window |
| usage_end_time | TIMESTAMP | End of usage window |
| usage_date | DATE | Date of usage (partition key) |
| usage_unit | STRING | DBU |
| usage_quantity | DECIMAL(38,3) | Number of DBUs consumed |
| custom_tags | MAP\<STRING,STRING\> | Cluster/pool custom tags |
| usage_metadata | STRUCT\<cluster_id:STRING, cluster_name:STRING, notebook_id:STRING, notebook_path:STRING, job_id:STRING, job_run_id:STRING, run_name:STRING, ...\> | Metadata about what generated usage |
| identity_metadata | STRUCT\<run_as:STRING\> | Who ran the workload |
| product_features | STRUCT\<jobs_tier:STRING, sql_tier:STRING, is_serverless:BOOLEAN, ...\> | Additional product context |

### Table 2: `system.billing.list_prices`

One row per SKU per price period. Join to `usage` on `sku_name`, `cloud`, `usage_unit`, and the time range overlap to get the price that was in effect when usage occurred.

| Column | Type | Description |
|---|---|---|
| sku_name | STRING | Matches usage.sku_name |
| cloud | STRING | AZURE |
| currency_code | STRING | USD |
| usage_unit | STRING | DBU |
| pricing | STRUCT\<default:DOUBLE\> | Default list price per DBU |
| price_start_time | TIMESTAMP | When this price became effective |
| price_end_time | TIMESTAMP | When this price was superseded (NULL = current) |

---

## QUERIES

All twelve queries below follow the same JOIN pattern: match on `sku_name`, `cloud`, `usage_unit`, and the price time-range overlap. Always include the `price_start_time`/`price_end_time` filter — omitting it causes row multiplication when a SKU has had multiple prices over time.

---

### Query 1: Daily DBU spend for the last 30 days

Shows total cost and total DBUs per day. Use this to identify spending trends and spot anomalous days at a glance.

```sql
SELECT
  u.usage_date,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2) AS daily_cost_usd,
  SUM(u.usage_quantity)                               AS total_dbus
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
GROUP BY u.usage_date
ORDER BY u.usage_date;
```

Output: one row per day with the total dollar cost and total DBU count. A spike in `daily_cost_usd` without a corresponding spike in `total_dbus` suggests a SKU price change rather than a usage change.

---

### Query 2: Top 10 costliest clusters this month

Ranks all clusters by total cost since the start of the current calendar month. Use this to identify which clusters are driving the most spend and whether they are expected to be that expensive.

```sql
SELECT
  u.usage_metadata.cluster_id                          AS cluster_id,
  u.usage_metadata.cluster_name                        AS cluster_name,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd,
  ROUND(SUM(u.usage_quantity), 1)                      AS total_dbus
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)
GROUP BY u.usage_metadata.cluster_id, u.usage_metadata.cluster_name
ORDER BY total_cost_usd DESC
LIMIT 10;
```

Output: the ten most expensive clusters, sorted by cost descending. A cluster near the top of this list with an unexpected name or ID is a strong signal that something is running that shouldn't be.

---

### Query 3: Spend breakdown by SKU (all-purpose vs jobs vs SQL)

Splits total spend by SKU name to show how costs are distributed across compute types. All-purpose compute is typically the most expensive per DBU; jobs compute is cheaper; SQL compute occupies its own tier.

```sql
SELECT
  u.sku_name,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd,
  ROUND(SUM(u.usage_quantity), 1)                      AS total_dbus,
  COUNT(DISTINCT u.usage_metadata.cluster_id)          AS cluster_count
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)
GROUP BY u.sku_name
ORDER BY total_cost_usd DESC;
```

Output: one row per SKU with total cost, total DBUs, and the number of distinct clusters using that SKU. A high `cluster_count` on `PREMIUM_ALL_PURPOSE_COMPUTE` often indicates interactive dev clusters that could be migrated to the cheaper jobs tier.

---

### Query 4: Spend by job name and ID

Attributes costs to specific scheduled or ad-hoc jobs. Use this to identify which jobs are the most expensive and whether individual job run counts are as expected.

```sql
SELECT
  u.usage_metadata.job_id                              AS job_id,
  u.usage_metadata.run_name                            AS run_name,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd,
  COUNT(DISTINCT u.usage_metadata.job_run_id)          AS run_count
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)
  AND u.usage_metadata.job_id IS NOT NULL
GROUP BY u.usage_metadata.job_id, u.usage_metadata.run_name
ORDER BY total_cost_usd DESC;
```

Output: one row per job (identified by `job_id` and `run_name`) with total cost and how many times it ran. Dividing `total_cost_usd` by `run_count` gives cost-per-run — a useful baseline for detecting regressions when a job suddenly costs much more per execution.

---

### Query 5: Week-over-week comparison

Compares total spend and DBU consumption between the current week and the previous week. Use this in weekly cost reviews to flag meaningful changes before they compound.

```sql
SELECT
  CASE
    WHEN u.usage_date >= DATE_TRUNC('WEEK', CURRENT_DATE)                        THEN 'This Week'
    WHEN u.usage_date >= DATE_TRUNC('WEEK', CURRENT_DATE) - INTERVAL 7 DAYS THEN 'Last Week'
  END                                                    AS week,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)    AS total_cost_usd,
  ROUND(SUM(u.usage_quantity), 1)                        AS total_dbus
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('WEEK', CURRENT_DATE) - INTERVAL 7 DAYS
GROUP BY week
ORDER BY week DESC;
```

Output: two rows — one for this week, one for last week. If the current week's cost is significantly higher mid-week, investigate before the week closes.

---

### Query 6: Anomaly detection — days where spend exceeds 2x the rolling 7-day average

Flags individual days where spending was unusually high relative to recent history. A 2x threshold catches genuine spikes without generating noise from normal day-to-day variation.

```sql
WITH daily AS (
  SELECT
    u.usage_date,
    ROUND(SUM(u.usage_quantity * p.pricing.default), 2) AS daily_cost
  FROM system.billing.usage u
  JOIN system.billing.list_prices p
    ON  u.sku_name     = p.sku_name
    AND u.cloud        = p.cloud
    AND u.usage_unit   = p.usage_unit
    AND u.usage_start_time >= p.price_start_time
    AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
  WHERE u.usage_date >= CURRENT_DATE - INTERVAL 30 DAYS
  GROUP BY u.usage_date
),
windowed AS (
  SELECT
    usage_date,
    daily_cost,
    ROUND(AVG(daily_cost) OVER (
      ORDER BY usage_date
      ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING
    ), 2) AS rolling_7day_avg
  FROM daily
)
SELECT
  usage_date,
  daily_cost,
  rolling_7day_avg,
  CASE
    WHEN rolling_7day_avg IS NULL          THEN 'NO_BASELINE'
    WHEN daily_cost > 2 * rolling_7day_avg THEN 'ANOMALY'
    ELSE 'NORMAL'
  END AS status
FROM windowed
ORDER BY usage_date;
```

Output: one row per day with `daily_cost`, `rolling_7day_avg`, and a `status` of `ANOMALY`, `NORMAL`, or `NO_BASELINE` (the first seven days, where there is not yet a full rolling window). Filter on `status = 'ANOMALY'` to build an alert or a daily digest.

---

### Query 7: Spend by custom tag (team)

Breaks down costs by the `team` custom tag. Use this for chargeback reporting or to show each team its own spend without giving teams access to each other's data.

```sql
SELECT
  u.custom_tags['team']                                AS team,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd,
  ROUND(SUM(u.usage_quantity), 1)                      AS total_dbus,
  COUNT(DISTINCT u.usage_metadata.cluster_id)          AS cluster_count
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)
  AND u.custom_tags['team'] IS NOT NULL
GROUP BY u.custom_tags['team']
ORDER BY total_cost_usd DESC;
```

Output: one row per distinct `team` tag value with total cost, total DBUs, and cluster count. The `IS NOT NULL` filter excludes untagged clusters — run Query 2 alongside this one to check whether untagged clusters represent a significant share of total spend.

---

### Query 8: Cost of every job run for a month

Lists every individual job run with its cost, duration, and cluster. Use this for granular chargeback — each row is one run you can tie to a pipeline execution, a ticket, or an SLA.

```sql
SELECT
  u.usage_metadata.job_id                              AS job_id,
  u.usage_metadata.job_run_id                          AS run_id,
  u.usage_metadata.run_name                            AS run_name,
  u.usage_metadata.cluster_id                          AS cluster_id,
  u.sku_name,
  MIN(u.usage_start_time)                              AS run_start,
  MAX(u.usage_end_time)                                AS run_end,
  ROUND(SUM(u.usage_quantity), 2)                      AS total_dbus,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)
  AND u.usage_metadata.job_id IS NOT NULL
GROUP BY
  u.usage_metadata.job_id,
  u.usage_metadata.job_run_id,
  u.usage_metadata.run_name,
  u.usage_metadata.cluster_id,
  u.sku_name
ORDER BY total_cost_usd DESC;
```

Output: one row per job run per SKU. If a single run uses multiple SKU types (e.g., a DLT pipeline that also triggers a SQL warehouse), it appears as multiple rows — sum by `run_id` to get the full run cost. To look at a specific prior month instead of the current one, replace `DATE_TRUNC('MONTH', CURRENT_DATE)` with a literal like `'2026-02-01'`.

---

### Query 9: Cost per user (who is spending the most?)

Attributes DBU spend to individual users or service principals. Useful for identifying users who leave interactive clusters running overnight.

```sql
SELECT
  u.identity_metadata.run_as                           AS user_or_principal,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd,
  ROUND(SUM(u.usage_quantity), 1)                      AS total_dbus,
  COUNT(DISTINCT u.usage_metadata.cluster_id)          AS cluster_count,
  COUNT(DISTINCT u.usage_date)                         AS active_days
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)
GROUP BY u.identity_metadata.run_as
ORDER BY total_cost_usd DESC;
```

Output: one row per user or service principal. The `run_as` column contains an email for human users or an application ID (GUID) for service principals. Divide `total_cost_usd` by `active_days` to get an average daily spend per user.

---

### Query 10: Hourly cost heatmap (find the expensive hours)

Shows cost by hour-of-day, aggregated across the month. Reveals when clusters are busiest and whether off-hours usage (nights, weekends) is driving waste.

```sql
SELECT
  HOUR(u.usage_start_time)                             AS hour_of_day,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd,
  ROUND(SUM(u.usage_quantity), 1)                      AS total_dbus
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)
GROUP BY HOUR(u.usage_start_time)
ORDER BY hour_of_day;
```

Output: 24 rows (one per hour, 0–23 UTC). High cost in hours 0–6 UTC (evenings/nights in US time zones) often means idle clusters or unscheduled jobs running outside business hours. Cross-reference with Query 2 to find which clusters are responsible.

---

### Query 11: Notebook-level cost attribution

Breaks down cost by notebook path — useful for identifying expensive ad-hoc analyses or runaway notebook executions.

```sql
SELECT
  u.usage_metadata.notebook_path                       AS notebook,
  u.identity_metadata.run_as                           AS user,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd,
  ROUND(SUM(u.usage_quantity), 1)                      AS total_dbus,
  COUNT(DISTINCT u.usage_date)                         AS days_used
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= DATE_TRUNC('MONTH', CURRENT_DATE)
  AND u.usage_metadata.notebook_path IS NOT NULL
GROUP BY u.usage_metadata.notebook_path, u.identity_metadata.run_as
ORDER BY total_cost_usd DESC
LIMIT 20;
```

Output: the 20 most expensive notebook executions this month. The `notebook_path` column is only populated for interactive notebook runs on All-Purpose clusters — job-based notebooks appear under Query 8 instead.

---

### Query 12: Month-over-month cost trend (last 6 months)

Shows monthly totals for the last 6 months, broken down by compute type. Use this in monthly reviews to spot gradual cost creep that daily checks miss.

```sql
SELECT
  DATE_TRUNC('MONTH', u.usage_date)                    AS month,
  CASE
    WHEN u.sku_name LIKE '%ALL_PURPOSE%'  THEN 'All-Purpose'
    WHEN u.sku_name LIKE '%JOBS%'         THEN 'Jobs'
    WHEN u.sku_name LIKE '%SQL%'          THEN 'SQL Warehouse'
    WHEN u.sku_name LIKE '%DLT%'          THEN 'DLT / Lakeflow'
    WHEN u.sku_name LIKE '%SERVERLESS%'   THEN 'Serverless'
    WHEN u.sku_name LIKE '%SERVING%'      THEN 'Model Serving'
    ELSE 'Other'
  END                                                  AS compute_type,
  ROUND(SUM(u.usage_quantity * p.pricing.default), 2)  AS total_cost_usd,
  ROUND(SUM(u.usage_quantity), 1)                      AS total_dbus
FROM system.billing.usage u
JOIN system.billing.list_prices p
  ON  u.sku_name     = p.sku_name
  AND u.cloud        = p.cloud
  AND u.usage_unit   = p.usage_unit
  AND u.usage_start_time >= p.price_start_time
  AND (p.price_end_time IS NULL OR u.usage_start_time < p.price_end_time)
WHERE u.usage_date >= ADD_MONTHS(DATE_TRUNC('MONTH', CURRENT_DATE), -6)
GROUP BY month, compute_type
ORDER BY month, total_cost_usd DESC;
```

Output: one row per month per compute type. Pivot this in a spreadsheet or Databricks dashboard to see which compute type is growing fastest. A steady month-over-month rise in All-Purpose spend is a common sign of clusters that should be converted to Jobs compute.

---

## HOW TO CHECK

Run this first to confirm you have access before running any of the attribution queries:

```sql
-- Run this first to confirm you have access
SELECT COUNT(*) FROM system.billing.usage WHERE usage_date = CURRENT_DATE - INTERVAL 1 DAYS;
-- If you get 0 rows (not an error), your workspace had no usage yesterday — that's normal
-- If you get an error, check Unity Catalog is enabled and you have SELECT grant
```

If the query errors with a permission or table-not-found message, check: (1) Unity Catalog is enabled on the workspace, (2) you have been granted `SELECT` on `system.billing.usage`, and (3) the workspace is on Premium tier.

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| Data freshness lag (~24 hours) | Yesterday's data appears today. Don't panic if rows for the current day are missing or sparse — the table is not real-time. Build daily reports against `CURRENT_DATE - INTERVAL 1 DAYS` to work with complete data. |
| Only covers DBU costs, not Azure infrastructure | `system.billing.usage` accounts for DBUs only. VM compute, managed disks, networking, and storage costs are in Azure Cost Management but not here. Combine both sources for a complete picture — see Chapter 5. |
| Requires Premium tier and Unity Catalog | Standard tier workspaces do not have access to system tables. There is no workaround — if your workspace is on Standard, system tables are unavailable until the tier is upgraded. |
| `custom_tags` is NULL for untagged clusters | The column is only populated if the cluster has custom tags configured. Clusters created without tags will have `NULL` in `custom_tags`, and they will be excluded from tag-based queries. Use Query 2 to catch untagged high-cost clusters. |
| Price JOIN multiplies rows without time-range filter | If you join `usage` to `list_prices` on `sku_name`, `cloud`, and `usage_unit` alone, SKUs that have had multiple prices over time will produce duplicate rows and inflated cost totals. Always include the `price_start_time`/`price_end_time` overlap condition. |
| `identity_metadata.run_as` may be a service principal ID, not an email | When workloads run as service principals, `run_as` contains the service principal's application ID (a GUID), not a human-readable name. Join to `system.iam.service_principals` or `system.iam.users` to resolve IDs to display names. |

---

**Navigation:** [← Chapter 3 — Tagging for Cost Attribution](03-tagging-for-cost-attribution.md) | [Index](index.md) | [Next: Chapter 5 — Daily Cost Tracking with az CLI →](05-az-cli-daily-usage.md)
