**Navigation:** [← Background Knowledge](00-basics.md) | [Index](index.md) | [Next: Chapter 2 — The Hidden Azure Costs →](02-azure-infrastructure-costs.md)

> **Rule:** The DBU bill is determined by five independent multipliers stacked together — compute type, tier, VM SKU, node count, and Photon — and any one of them can double your spend without a single line of code changing.

---

## THE PROBLEM

You've enabled a cluster, jobs are running, and the Databricks bill arrives. It's higher than expected — but which knob drove it up? Was it the instance type? The number of nodes? The fact that Photon is on? The tier?

Without a clear map of every parameter that feeds into DBU consumption, you're guessing. This chapter lays out every factor, in order of impact, with real numbers so you can predict and control spend before the bill arrives.

---

## THE CONCEPT

### All Compute Types and Their DBU Rates

Every workload type in Azure Databricks has a fixed DBU rate expressed in dollars per DBU-hour. That rate is multiplied by the number of DBUs consumed per hour (which depends on VM SKU and node count) to produce your hourly spend.

The table below covers every billable compute type as of early 2026, pay-as-you-go, East US region.

| Compute Type | Standard ($/DBU) | Premium ($/DBU) | Notes |
|---|---|---|---|
| All-Purpose Compute | ~$0.40 | ~$0.55 | Interactive notebooks, ad-hoc analysis |
| All-Purpose Compute (Photon) | not available | ~$0.65 | Vectorized engine; Premium only; ~2× DBU/hr vs non-Photon |
| Jobs Compute | ~$0.20 | ~$0.30 | Automated pipelines, scheduled jobs |
| Jobs Compute (Photon) | not available | ~$0.40 | Premium only |
| Jobs Light Compute | not available | ~$0.15 | Lightweight jobs; no Spark; no Photon; Premium only |
| SQL Warehouse Classic | not available | ~$0.22 | Self-managed SQL warehouse; BI workloads; Premium only |
| SQL Warehouse Pro | not available | ~$0.55 | Enhanced SQL; Photon always on; Premium only |
| SQL Warehouse Serverless | not available | ~$0.70 | Bundles VM cost; no separate Stream 2 charges |
| Serverless Compute — Interactive (notebooks) | not available | ~$0.95 | Billed against Interactive Serverless SKU |
| Serverless Compute — Automated (jobs/workflows) | not available | ~$0.55 | Billed against Automated Serverless SKU |
| DLT / Lakeflow Pipelines — Core | not available | ~$0.30 | Basic pipeline; managed Spark |
| DLT / Lakeflow Pipelines — Pro | not available | ~$0.38 | Adds SLAs, schema enforcement |
| DLT / Lakeflow Pipelines — Advanced | not available | ~$0.54 | Adds enhanced observability, data quality |
| Model Serving — CPU | not available | ~$0.65 | 1 concurrent request/hr = 1 DBU/hr |
| Model Serving — GPU (Small, T4) | not available | ~$0.65 | 10.48 DBU/hr per endpoint |
| Model Serving — GPU (XLarge, A100 80GB) | not available | ~$0.65 | 78.60 DBU/hr per endpoint |

> Prices are approximate pay-as-you-go rates. Actual rates vary by region (±5–20%). Pre-purchasing Databricks Commit Units (DBCU) for 1 or 3 years can reduce rates by up to 37%. Always verify at [azure.microsoft.com/pricing/details/databricks](https://azure.microsoft.com/en-us/pricing/details/databricks/).

> **Standard tier retirement:** No new Standard tier workspaces after April 1, 2026. All remaining Standard workspaces are automatically upgraded to Premium on October 1, 2026, increasing DBU costs by ~35–40%.

---

### Cluster Configuration Impact

When you run a classic (non-serverless) cluster, the DBU/hour consumed is not a single fixed number — it is a product of several configuration choices you make when creating the cluster.

#### 1. Node Type (VM SKU)

Each Azure VM instance maps to a fixed DBU/hour consumption rate. This rate is set by Databricks and does not change regardless of what is running on the cluster. Bigger VMs consume more DBUs per hour.

The mapping is proportional to vCPU count within a VM family:

| VM SKU | vCPUs | RAM (GiB) | DBU/hour per node | Common use |
|---|---|---|---|---|
| Standard_DS3_v2 | 4 | 14 | 0.75 | Dev/test, small jobs |
| Standard_DS4_v2 | 8 | 28 | 1.5 | General purpose |
| Standard_DS5_v2 | 16 | 56 | 3.0 | Medium batch workloads |
| Standard_D8s_v3 | 8 | 32 | 1.5 | General purpose (newer gen) |
| Standard_D16s_v3 | 16 | 64 | 3.0 | Larger batch workloads |
| Standard_E8s_v3 | 8 | 64 | 1.5 | Memory-intensive ML/joins |
| Standard_E16s_v3 | 16 | 128 | 3.0 | Large memory workloads |
| Standard_L8s_v3 | 8 | 64 | 1.5 | Storage-optimized |

> The DBU/hour per node is consistent across VM generations within the same vCPU tier. A DS4_v2 (8 vCPU) and a D8s_v3 (8 vCPU) both consume 1.5 DBU/hour per node. Databricks normalizes by vCPU count within the DSv2 and Dsv3 families.

> **Important:** The Azure VM cost (billed separately in Stream 2) varies significantly between SKUs with the same DBU/hour rate. An E8s_v3 and D8s_v3 both consume 1.5 DBU/hr per node, but the E8s_v3 costs more in Azure VM charges due to its larger RAM. Choosing a memory-optimized SKU doesn't change your DBU bill — only your VM bill.

#### 2. Number of Nodes (Driver + Workers)

DBU consumption is strictly additive across nodes. Every node — driver and each worker — accumulates DBU/hour simultaneously while the cluster is running.

```
Total DBU/hour = (1 driver × DBU/hr per node) + (worker_count × DBU/hr per node)
               = (driver_count + worker_count) × DBU/hr per node
               [assuming single-node type for driver and workers]
```

A 10-worker cluster on Standard_DS3_v2 consumes:
```
(1 driver + 10 workers) × 0.75 DBU/hr = 8.25 DBU/hr
```

This is the single largest lever for controlling DBU spend. Halving the node count halves the DBU bill, immediately and exactly.

#### 3. Autoscaling (Min/Max Nodes)

Autoscaling lets the cluster grow and shrink between a minimum and maximum node count based on workload demand.

- At any moment, DBU consumption equals the **current active node count** × DBU/hr per node.
- The cluster scales to min nodes when idle (or terminates entirely if auto-terminate is set).
- The cluster scales toward max nodes when load is high.

The cost risk is **max nodes**: if you set max too high and the workload bursts, the cluster can temporarily reach max nodes and spike DBU consumption. Always set max to a justified upper bound — not "infinity" as a safety margin.

```python
# Example: autoscaling cluster
min_workers = 2
max_workers = 10
dbu_per_node = 0.75  # Standard_DS3_v2

# Best case (idle at min):   (1 + 2)  × 0.75 = 2.25 DBU/hr
# Worst case (full at max):  (1 + 10) × 0.75 = 8.25 DBU/hr
# Monthly cost range at Premium Jobs ($0.30/DBU):
#   Best case:  2.25 × 730 × $0.30 = $493/month
#   Worst case: 8.25 × 730 × $0.30 = $1,808/month
```

#### 4. Spot (Preemptible) vs. On-Demand Workers

Spot VMs (called "Azure Spot" or "low-priority" in Databricks) reduce the **Azure VM cost** (Stream 2) by 60–90% compared to on-demand pricing.

**Spot instances do NOT reduce DBU consumption or DBU charges.**

A Standard_DS3_v2 spot node consumes exactly the same 0.75 DBU/hour as an on-demand Standard_DS3_v2. The DBU bill is identical. Only the Azure VM line item in your Azure subscription changes.

This means spot savings are bounded: for Premium All-Purpose compute, DBU charges typically represent 40–60% of total cluster cost. Even zero VM cost still leaves the full DBU bill intact.

#### 5. Idle Timeout (Auto-Terminate)

Databricks clusters continue consuming DBUs from the moment they start until the moment they terminate — **including all idle time between tasks**.

An All-Purpose cluster waiting for a user to run the next cell is consuming DBUs at the full rate. A Jobs cluster that finishes in 20 minutes but has no auto-terminate set will run until manually stopped, consuming DBUs the entire time.

```
# Idle cost example
cluster_dbu_per_hr = 3.0   # 4-node DS3_v2 cluster
idle_hours_per_day = 6     # cluster left running overnight
dbu_rate = 0.55            # Premium All-Purpose

idle_cost_per_day = cluster_dbu_per_hr × idle_hours_per_day × dbu_rate
                 = 3.0 × 6 × $0.55
                 = $9.90/day idle waste
                 = $217.80/month for doing nothing
```

**Best practice:** Set idle timeout to 10–30 minutes for All-Purpose clusters. Set Jobs clusters to terminate immediately after the job completes (the default for job clusters launched by Databricks Jobs).

#### 6. Photon

Photon is Databricks' vectorized query engine that accelerates SQL and DataFrame operations. Enabling Photon approximately **doubles the DBU consumption rate** for the affected compute.

| Configuration | DBU/hour per node (DS4_v2) | $/DBU (Premium All-Purpose) | Cost/hr per node |
|---|---|---|---|
| Without Photon | 1.5 | $0.55 | $0.825 |
| With Photon | ~3.0 | $0.55 | $1.65 |

> The Photon multiplier is applied by switching to the Photon-enabled SKU, which has a higher DBU/hour rate than the standard SKU for the same VM. The $/DBU rate stays at $0.55 — what changes is that each VM node now burns ~2× the DBUs per hour. The all-in effect is approximately 2× the DBU cost for compute with Photon enabled.

Photon is only available on Premium tier. Photon-accelerated Jobs and All-Purpose clusters are billed at a higher $/DBU rate than their non-Photon counterparts (see the compute type table above), reflecting both the DBU-rate uplift and the $/DBU tier uplift.

Whether Photon pays off depends on query type. Vectorized operations (SQL aggregations, joins, scans) see 2–10× speed improvements. If a Photon-accelerated query runs in 30 minutes instead of 90 minutes, the 2× DBU rate applied to 1/3 the time yields a net ~33% cost reduction despite the higher rate. For non-SQL workloads (Python UDFs, arbitrary ML training loops), Photon provides little acceleration but still charges the higher DBU rate.

---

## THE MATH

### Example 1: Premium Jobs Cluster — Monthly Cost

**Scenario:** 4-node Standard_DS3_v2 cluster running automated Jobs at Premium tier.

```
Configuration:
  VM SKU:        Standard_DS3_v2  → 0.75 DBU/hr per node
  Node count:    1 driver + 3 workers = 4 nodes total
  Tier:          Premium Jobs     → $0.30/DBU
  Runtime:       8 hours/day, 22 working days/month
  Photon:        disabled

Step 1: DBU/hour for the cluster
  4 nodes × 0.75 DBU/hr = 3.0 DBU/hr

Step 2: DBU consumed per month
  3.0 DBU/hr × 8 hr/day × 22 days = 528 DBUs/month

Step 3: DBU cost per month
  528 DBUs × $0.30/DBU = $158.40/month (DBU charges, Stream 1 only)

Note: Azure VM costs (Stream 2) are billed separately.
  Standard_DS3_v2 on-demand East US ≈ $0.19/hr per node
  4 nodes × $0.19/hr × 8 hr/day × 22 days = $133.76/month (VM charges)

Total estimated monthly cost: $158.40 + $133.76 = $292.16/month
```

### Example 2: SQL Warehouse Pro (Medium) — Monthly Cost with Auto-Stop Idle Waste

**Scenario:** SQL Warehouse Pro, size Medium, 1 cluster, used by analysts.

```
Configuration:
  Warehouse type:   SQL Warehouse Pro  → $0.55/DBU
  Size:             Medium             → 4 DBU/hr per cluster
  Clusters:         1 (min=1, max=1)
  Active hours:     10 hr/day of actual query work
  Auto-stop:        10 minutes
  Working days:     22/month

Step 1: Active DBU cost
  4 DBU/hr × 10 hr/day × 22 days = 880 DBU active
  880 DBU × $0.55/DBU = $484.00/month (active queries)

Step 2: Idle waste from auto-stop
  The 10-minute auto-stop means after each query session ends,
  the warehouse idles for up to 10 minutes before terminating.

  Assume 5 query sessions per day (warehouse starts/stops 5×/day):
    5 sessions × 10 min idle × 22 days = 1,100 min = 18.33 hours idle/month
    18.33 hr × 4 DBU/hr × $0.55/DBU = $40.33/month wasted on idle

Step 3: Total DBU cost
  $484.00 + $40.33 = $524.33/month

  At 60-min auto-stop instead of 10-min (worst case):
    5 sessions × 60 min × 22 days = 6,600 min = 110 hours idle
    110 hr × 4 DBU/hr × $0.55/DBU = $242.00/month idle waste
    Total: $484.00 + $242.00 = $726.00/month

  Tighter auto-stop = direct savings. Recommended: 5–10 minutes for SQL
  warehouses used in batch/scheduled BI workloads; 20–30 min for ad-hoc
  analyst sessions where repeated query bursts are expected.

Note: SQL Warehouse Pro is Premium only. Stream 2 (VM charges) apply
      for Classic and Pro warehouses; the VMs (Standard_E8ds_v4 workers)
      are billed directly to your Azure subscription.
      SQL Warehouse Serverless has NO separate VM charges — the $0.70/DBU
      rate bundles the infrastructure cost.
```

---

## SQL Warehouse Sizing Table

SQL Warehouses (Classic, Pro, and Serverless) use the same T-shirt size names. Each size sets the DBU/hour rate **per cluster**. Running multiple clusters (for concurrency) multiplies this by the cluster count.

The DBU/hour values below are for the SQL Serverless SKU as published in the official Microsoft documentation. Classic and Pro warehouses consume the same DBUs per cluster — they differ only in $/DBU rate ($0.22 vs $0.55) and underlying instance family.

| Size | DBU/hr per cluster | Concurrent queries | Typical use case |
|---|---|---|---|
| 2X-Small | 4 | ~10 | Individual analyst, dev/test |
| X-Small | 6 | ~10 | Small team, low-frequency queries |
| Small | 12 | ~10 | Team BI dashboards, moderate load |
| Medium | 24 | ~10 | Department-level BI, heavier ETL/SQL |
| Large | 40 | ~10 | High-concurrency production BI |
| X-Large | 80 | ~10 | Very high concurrency, large joins |
| 2X-Large | 144 | ~10 | Enterprise-scale analytics |
| 3X-Large | 272 | ~10 | Massive parallel workloads |
| 4X-Large | 528 | ~10 | Largest available; significant cost |

> Each cluster handles up to ~10 concurrent queries. When concurrency exceeds this, the warehouse autoscales by adding more clusters of the same size. Each additional cluster adds the full DBU/hr for that size.

```
Example: SQL Pro warehouse, size Medium, autoscaling 1–3 clusters
  At 1 cluster:  24 DBU/hr × $0.55/DBU = $13.20/hr
  At 2 clusters: 48 DBU/hr × $0.55/DBU = $26.40/hr
  At 3 clusters: 72 DBU/hr × $0.55/DBU = $39.60/hr
```

---

## Serverless Pricing Comparison

Serverless compute (SQL Serverless, Serverless Jobs, Serverless Notebooks) carries a higher DBU rate than classic compute. This is because the DBU rate bundles the Azure VM cost that would otherwise appear in Stream 2.

| Dimension | Classic Jobs Compute | SQL Serverless | Serverless Jobs |
|---|---|---|---|
| DBU rate (Premium, East US) | ~$0.30/DBU | ~$0.70/DBU | ~$0.55/DBU |
| Separate Azure VM bill? | Yes | No | No |
| Startup time | 3–8 min | <5 sec | ~30 sec |
| Idle time billing | Billed until terminated | Stops when idle | Stops per job |
| Min billing unit | Per second | Per second | Per second |
| You manage VMs? | Yes (choose SKU, spot/on-demand) | No | No |

### Break-even Analysis

For a 4-node Standard_DS3_v2 Jobs cluster (Premium):

```
Classic approach:
  DBU cost:  3.0 DBU/hr × $0.30/DBU = $0.90/hr
  VM cost:   4 nodes × $0.19/hr = $0.76/hr
  Total:     $1.66/hr

Serverless Jobs approach (comparable capacity):
  Serverless DBU rate: ~$0.55/DBU
  Equivalent capacity ≈ same 3.0 DBU/hr equivalent
  DBU cost:  3.0 DBU/hr × $0.55/DBU = $1.65/hr
  VM cost:   $0 (bundled)
  Total:     $1.65/hr
```

At comparable compute capacity, total cost is similar. Serverless wins on:
- **Operational simplicity** — no cluster management, no VM quota concerns
- **Idle elimination** — no charge between jobs; billing stops when the job ends
- **Speed** — near-instant startup vs. 3–8 min cold-start for classic clusters

Classic compute wins on:
- **Cost predictability** — you know exactly which VMs are running
- **Spot savings** — you can use spot VMs to cut Stream 2 costs by 60–90%
- **Large persistent workloads** — always-on clusters where startup latency doesn't matter

For short jobs (< 30 min) with irregular schedules, Serverless typically wins on total cost because it eliminates idle billing and startup waste. For long-running or always-on clusters, classic with spot workers is usually cheaper.

---

## GOTCHAS

| Gotcha | Impact | Mitigation |
|---|---|---|
| **Photon doubles DBU rate** | Switching from standard to Photon All-Purpose roughly doubles DBU consumption — at the same $0.55/DBU rate, your bill doubles unless the workload finishes in less than half the time | Profile the workload first; Photon accelerates SQL and DataFrame scans most; test with `EXPLAIN` or query profile before enabling in production |
| **Idle clusters still consume DBUs** | An All-Purpose cluster left running overnight at 3.0 DBU/hr × 8 hr × $0.55/DBU = $13.20 wasted per night — $290/month for one idle cluster | Set idle timeout to 10–30 min for all interactive clusters; use job clusters for all automated work (they terminate automatically after the job) |
| **Autoscaling max can spike costs unexpectedly** | A misconfigured max of 50 workers on an All-Purpose cluster ($0.55/DBU) using DS4_v2 (1.5 DBU/hr) can reach 76.5 DBU/hr = $42/hr if all nodes spin up simultaneously | Set max to a conservative upper bound based on actual peak usage; monitor `cluster_activity` or system tables; set budget alerts |
| **Spot savings don't reduce DBUs** | Teams often believe "we use spot — it's cheap" and underestimate the DBU portion, which is unaffected by spot pricing | Always separate Stream 1 (DBU) and Stream 2 (VM) in cost analysis; spot only reduces Stream 2 |
| **SQL Serverless has a minimum charge per query execution** | Even a trivial query that runs in under 1 second incurs a minimum billing unit; with many thousands of small queries, these minimums accumulate | Batch small queries; avoid very-high-frequency polling patterns against SQL Serverless warehouses |
| **DLT has different rates for Core / Pro / Advanced** | Teams creating DLT pipelines default to Advanced without understanding that Core is $0.30/DBU vs Advanced at $0.54/DBU — 80% more expensive per DBU | Choose the minimum DLT tier required: Core for basic pipelines, Pro only when you need SLA enforcement, Advanced only when you need enhanced data quality monitoring |
| **Jobs Light cannot use Spark** | Jobs Light ($0.15/DBU) looks cheap but only supports simple Python/Scala tasks without Spark context; migrating a Spark-based job expecting Light pricing will fail silently or fall back to standard Jobs rates | Verify workload compatibility before switching to Jobs Light; check that the job runs without a SparkSession |
| **SQL Warehouse Pro always runs Photon** | SQL Warehouse Pro includes Photon at no separate multiplier — it is priced into the $0.55/DBU rate; if Photon provides no benefit for your query pattern, Classic at $0.22/DBU is 60% cheaper per DBU | Benchmark the same queries on Classic vs Pro; if runtime is similar, Classic is significantly cheaper |

---

**Navigation:** [← Background Knowledge](00-basics.md) | [Index](index.md) | [Next: Chapter 2 — The Hidden Azure Costs →](02-azure-infrastructure-costs.md)
