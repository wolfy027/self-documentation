**Navigation:** [← Chapter 4 — Tracking Costs Inside Databricks](04-databricks-system-tables.md) | [Index](index.md) | [Next: Chapter 6 — Automating Cost Reports →](06-az-cli-automation.md)

> **Rule:** Databricks system tables only cover DBU costs. To see the full picture — VMs, storage, networking — you need Azure Cost Management. The az CLI makes this scriptable, repeatable, and automatable.

---

## THE PROBLEM

`system.billing.usage` gives you precise DBU attribution by cluster, job, and user. It does not know about the Azure infrastructure those clusters run on. Every Databricks workspace creates a managed resource group containing virtual machines, managed disks, network interfaces, and a storage account (DBFS). That infrastructure generates Azure charges that never appear in system tables.

Chapter 2 catalogued those infrastructure cost components. To track them, you need Azure Cost Management — the same service the portal uses when you open Cost Analysis. The portal is useful for exploration, but it is not scriptable. You cannot pipe it into a cron job, feed it into a Slack alert, or combine it with system-table data in a Python script.

The `az` CLI closes that gap. With `az rest` calling the Cost Management Query API, you can query any date range, any scope, any grouping, and get JSON back — all from your terminal. The same command that you run interactively today becomes the foundation of the automated reports in Chapter 6.

---

## THE CONCEPT

### Two approaches

**Primary: `az rest` calling the Cost Management Query API**

`az rest` lets you call any Azure REST endpoint directly. The Cost Management Query API (`Microsoft.CostManagement/query`) accepts a POST body that specifies your date range, granularity, grouping dimensions, and filters. It returns aggregated results — one row per group — rather than raw line items. This is the right tool for cost reporting: you ask for totals and get totals.

The endpoint pattern is:

```
POST https://management.azure.com/{scope}/providers/Microsoft.CostManagement/query?api-version=2023-11-01
```

The scope can be a subscription (`/subscriptions/{id}`) or a resource group (`/subscriptions/{id}/resourceGroups/{name}`). Resource-group scope is faster and more precise when you know which managed RG you care about.

**Alternative: `az consumption usage-detail list`**

This is the older, simpler option. It returns raw usage line items — one row per resource per billing period — with no aggregation. It is slower on large subscriptions, cannot group or aggregate server-side, and is being superseded by the Cost Management Query API. Use it if you need raw line-item exports, but prefer `az rest` for anything that needs a total or a breakdown.

### Prerequisites

- `az` CLI installed — run `az --version` to verify (1.x is too old; 2.x is required)
- **Cost Management Reader** role on the subscription or resource group you are querying
- Authenticated: run `az login` for interactive use, or set up a service principal with `az login --service-principal` for automation
- API version: `2023-11-01` — this is the stable version as of this writing; do not use preview versions in scripts

---

## HOW TO DO IT

The commands below all use shell variables set at the top. Set them once before running any individual command:

```bash
SUBSCRIPTION_ID="<your-subscription-id>"
START_DATE=$(date -d '7 days ago' +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)
```

---

### Command 1: Total Databricks-related spend for the last 7 days, grouped by day

```bash
SUBSCRIPTION_ID="<your-subscription-id>"
START_DATE=$(date -d '7 days ago' +%Y-%m-%d)
END_DATE=$(date +%Y-%m-%d)

az rest \
  --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body "{
    \"type\": \"ActualCost\",
    \"timeframe\": \"Custom\",
    \"timePeriod\": {
      \"from\": \"${START_DATE}\",
      \"to\": \"${END_DATE}\"
    },
    \"dataset\": {
      \"granularity\": \"Daily\",
      \"aggregation\": {
        \"totalCost\": {\"name\": \"Cost\", \"function\": \"Sum\"}
      },
      \"filter\": {
        \"dimensions\": {
          \"name\": \"ServiceName\",
          \"operator\": \"In\",
          \"values\": [\"Azure Databricks\"]
        }
      }
    }
  }"
```

This filters by `ServiceName = "Azure Databricks"`, which matches the Marketplace entries that represent DBU charges. One row per day with the total cost for that day.

Note: `ServiceName = "Azure Databricks"` captures DBU charges billed through the Marketplace. It does not include the underlying infrastructure (VMs, disks, storage) because those resources have different service names — `Virtual Machines`, `Azure Managed Disks`, and so on. To capture infrastructure costs as well, filter by `ResourceGroup` instead of `ServiceName` (see Commands 2 and 3).

---

### Command 2: Break down by meter category to separate DBU from infrastructure

```bash
az rest \
  --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body "{
    \"type\": \"ActualCost\",
    \"timeframe\": \"Custom\",
    \"timePeriod\": {\"from\": \"${START_DATE}\", \"to\": \"${END_DATE}\"},
    \"dataset\": {
      \"granularity\": \"None\",
      \"aggregation\": {
        \"totalCost\": {\"name\": \"Cost\", \"function\": \"Sum\"}
      },
      \"grouping\": [
        {\"type\": \"Dimension\", \"name\": \"ServiceName\"},
        {\"type\": \"Dimension\", \"name\": \"MeterCategory\"}
      ],
      \"filter\": {
        \"dimensions\": {
          \"name\": \"ResourceGroup\",
          \"operator\": \"Contains\",
          \"values\": [\"databricks\"]
        }
      }
    }
  }"
```

This filters to any resource group whose name contains "databricks" (which catches both the customer-managed RG and the managed RG that Databricks creates). It groups the results by `ServiceName` and `MeterCategory`, so each row in the output represents a distinct combination — for example, `Azure Databricks / DBU`, `Virtual Machines / Compute`, `Storage / Blob Storage`.

This is the most useful command for understanding how your Databricks total is split between DBU charges and infrastructure. Run it at the end of each week to confirm the ratio is stable.

---

### Command 3: Filter to a specific workspace's managed resource group

```bash
MANAGED_RG="databricks-rg-<workspace-name>-<suffix>"

az rest \
  --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${MANAGED_RG}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body "{
    \"type\": \"ActualCost\",
    \"timeframe\": \"Custom\",
    \"timePeriod\": {\"from\": \"${START_DATE}\", \"to\": \"${END_DATE}\"},
    \"dataset\": {
      \"granularity\": \"Daily\",
      \"aggregation\": {
        \"totalCost\": {\"name\": \"Cost\", \"function\": \"Sum\"}
      },
      \"grouping\": [
        {\"type\": \"Dimension\", \"name\": \"ResourceType\"}
      ]
    }
  }"
```

This scopes the query directly to the managed resource group for one workspace, which is faster than a subscription-level query and eliminates any ambiguity about which workspace the costs belong to. The `ResourceType` grouping breaks the total down into VM compute, managed disks, and storage — the three main infrastructure components described in Chapter 2.

Find the managed RG name in the Azure portal under the workspace's Overview blade. It follows the pattern `databricks-rg-<workspace-name>-<random-suffix>`.

---

### Command 4: Filter by tag (cost-center or team)

```bash
az rest \
  --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body "{
    \"type\": \"ActualCost\",
    \"timeframe\": \"Custom\",
    \"timePeriod\": {\"from\": \"${START_DATE}\", \"to\": \"${END_DATE}\"},
    \"dataset\": {
      \"granularity\": \"None\",
      \"aggregation\": {
        \"totalCost\": {\"name\": \"Cost\", \"function\": \"Sum\"}
      },
      \"grouping\": [
        {\"type\": \"TagKey\", \"name\": \"team\"}
      ],
      \"filter\": {
        \"tags\": {
          \"name\": \"team\",
          \"operator\": \"In\",
          \"values\": [\"data-engineering\", \"analytics\"]
        }
      }
    }
  }"
```

This filters to resources tagged with `team=data-engineering` or `team=analytics` and groups results by the `team` tag value. This only works if your resources are tagged — see Chapter 3 for the tagging strategy that makes this possible. For Databricks infrastructure costs, the tags need to be on the resource group (since you cannot tag managed-RG resources directly) or propagated via the workspace's custom tags policy.

---

### Command 5: This month vs last month comparison

```bash
THIS_MONTH_START=$(date +%Y-%m-01)
LAST_MONTH_START=$(date -d "$(date +%Y-%m-01) -1 month" +%Y-%m-%d)
LAST_MONTH_END=$(date -d "$(date +%Y-%m-01) -1 day" +%Y-%m-%d)

# This month
az rest --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body "{
    \"type\": \"ActualCost\",
    \"timeframe\": \"Custom\",
    \"timePeriod\": {\"from\": \"${THIS_MONTH_START}\", \"to\": \"${END_DATE}\"},
    \"dataset\": {
      \"granularity\": \"None\",
      \"aggregation\": {\"totalCost\": {\"name\": \"Cost\", \"function\": \"Sum\"}},
      \"filter\": {
        \"dimensions\": {\"name\": \"ResourceGroup\", \"operator\": \"Contains\", \"values\": [\"databricks\"]}
      }
    }
  }"

# Last month
az rest --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body "{
    \"type\": \"ActualCost\",
    \"timeframe\": \"Custom\",
    \"timePeriod\": {\"from\": \"${LAST_MONTH_START}\", \"to\": \"${LAST_MONTH_END}\"},
    \"dataset\": {
      \"granularity\": \"None\",
      \"aggregation\": {\"totalCost\": {\"name\": \"Cost\", \"function\": \"Sum\"}},
      \"filter\": {
        \"dimensions\": {\"name\": \"ResourceGroup\", \"operator\": \"Contains\", \"values\": [\"databricks\"]}
      }
    }
  }"
```

Run both back to back and compare the totals. Because this month is still in progress, the comparison is most meaningful mid-month — divide this month's running total by the number of elapsed days and multiply by the number of days in the month for a projected full-month figure.

---

## OUTPUT FORMATTING

The Cost Management Query API returns JSON with two keys under `properties`: `columns` (an array of column-name/type objects) and `rows` (an array of value arrays). The row values align positionally with the column names.

Pipe through `jq` to make the output readable:

```bash
# Clean table: date, cost, currency
az rest --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body '{ ... }' | \
  jq -r '["Date", "Cost", "Currency"], (.properties.rows[]) | @tsv' | \
  column -t

# Just the total (sum of all rows' first column)
az rest --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body '{ ... }' | \
  jq '.properties.rows | map(.[0]) | add'
```

The column ordering in `.properties.rows` matches the ordering in `.properties.columns`. For Command 1 (daily granularity with a single aggregation), the columns are typically `Cost`, `UsageDate`, `Currency` — in that order. If you add grouping dimensions, they appear as additional columns appended after the cost columns. Inspect `.properties.columns` first if the row layout is unclear:

```bash
az rest --method POST ... | jq '.properties.columns'
```

---

## ALTERNATIVE: `az consumption usage-detail list`

```bash
az consumption usage-detail list \
  --start-date $(date -d '7 days ago' +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d) \
  --query "[?contains(instanceName, 'databricks') || contains(resourceGroup, 'databricks')].{Date:usageStart, Cost:pretaxCost, Meter:meterDetails.meterName, Resource:instanceName}" \
  --output table
```

This returns raw line items — one row per resource per billing period — filtered client-side by `instanceName` or `resourceGroup` containing "databricks". It is simpler to type but significantly slower on large subscriptions because it downloads all line items before filtering. It also cannot aggregate server-side, so you have to sum costs yourself.

Microsoft is phasing this API out in favour of the Cost Management Query API. Use it for quick one-off inspections or if you need raw line-item exports, but do not build automation on it — migrate anything important to `az rest`.

---

## HOW TO CHECK

Run Command 1 and note the total for the date range. Then open the Azure portal, navigate to Cost Management > Cost Analysis, set the same start and end dates, and add a filter for `Service name = Azure Databricks`. The totals should match within a few cents — small discrepancies are normal due to rounding in the portal display.

If the numbers differ by more than a dollar, check that the date ranges are identical. The portal's default view often uses the billing-period timeframe rather than a custom range; make sure you switch it to the same custom range you used in the CLI command.

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| Cost Management data has an 8–24 hour lag | Today's charges may not appear until tomorrow. Build daily reports against yesterday's date (`date -d '1 day ago' +%Y-%m-%d`) to work with complete data. Never alert on today's running total as if it is the final number. |
| Inline JSON body must use escaped quotes | When the `--body` value is an inline shell string, every double quote inside the JSON must be escaped as `\"`. For complex queries with many nested levels, save the body to a file and pass `--body @query.json` instead. |
| Subscription-level scope is slow on large subscriptions | A subscription with hundreds of resource groups processes more data before filtering. Scope queries to the resource group level (`/subscriptions/{id}/resourceGroups/{name}/providers/...`) whenever you know which RG you care about — it is faster and produces less noise. |
| `ServiceName = "Azure Databricks"` only captures DBU charges | Infrastructure costs (VMs, storage, networking) appear under `Virtual Machines`, `Azure Managed Disks`, and other service names. To capture the full Databricks cost, filter by `ResourceGroup` rather than `ServiceName`. |
| `az consumption usage-detail list` is being deprecated | This command is being superseded by the Cost Management Query API. Existing scripts that use it will continue to work until Microsoft removes it, but new automation should use `az rest` with the `Microsoft.CostManagement/query` endpoint. |

---

**Navigation:** [← Chapter 4 — Tracking Costs Inside Databricks](04-databricks-system-tables.md) | [Index](index.md) | [Next: Chapter 6 — Automating Cost Reports →](06-az-cli-automation.md)
