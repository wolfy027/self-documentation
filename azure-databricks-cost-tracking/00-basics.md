**Navigation:** [← Course Index](index.md) | [Index](index.md) | [Next: Chapter 1 — DBU Cost Parameters →](01-dbu-cost-parameters.md)

> **Key insight:** Every Azure Databricks workspace produces two completely separate bills — DBU charges billed by Databricks through Azure Marketplace, and infrastructure charges billed by Azure for the VMs and resources in your managed resource group — and you need different tools to find each one.

---

## What is a DBU

A **Databricks Unit (DBU)** is the metering unit Databricks uses to charge for compute. It represents a normalized unit of processing capacity, billed per second of cluster or warehouse runtime.

**How it maps to compute time:**

- A cluster consumes DBUs continuously from the moment it starts until it terminates — including idle time between tasks.
- The number of DBUs consumed per hour is fixed by Databricks for each instance type and workload tier.
- Multi-node clusters accumulate DBUs from every node: `(driver DBUs/hr) + (worker count × worker DBUs/hr)`.
- DBU consumption is metered per second, so a cluster running for 90 seconds costs 1.5x the per-second rate.

**Analogy to vCPU-hours:**

A DBU is to Databricks what a vCPU-hour is to Azure VMs. Just as Azure charges you per vCPU-hour based on the VM SKU, Databricks charges you per DBU based on the workload type and compute tier. The key difference: a DBU abstracts both CPU and memory capacity into a single unit, letting Databricks apply pricing tier multipliers independently of the underlying VM cost.

```
Example: 4-node All-Purpose Premium cluster on Standard_DS3_v2

  Each node = 0.75 DBU/hr
  4 nodes × 0.75 DBU/hr = 3 DBU/hr total
  3 hours runtime → 9 DBUs consumed
  At $0.55/DBU (Premium All-Purpose, East US) → $4.95 in DBU charges

  NOTE: The Azure VM cost (Standard_DS3_v2 × 4 nodes × 3 hrs) is billed
        separately in Stream 2 — it does NOT appear in this $4.95 figure.
```

---

## Pricing Tiers

Azure Databricks workspaces are provisioned as either **Standard** or **Premium**. The tier is set at workspace creation and determines which features are available and the per-DBU price for every workload type.

### Feature Comparison

| Feature | Standard | Premium |
|---|---|---|
| Notebooks, Jobs, Workflows | Yes | Yes |
| Delta Lake, Spark | Yes | Yes |
| Photon acceleration | No | Yes |
| Unity Catalog | No | Yes |
| Role-based access control (RBAC) | Workspace-level only | Account-level + table-level |
| Cluster policies | No | Yes |
| Audit logs | No | Yes |
| IP access lists | No | Yes |
| SCIM provisioning / SSO | No | Yes |
| Credential passthrough | No | Yes |
| Customer-managed keys (CMK) | No | Yes |
| Databricks SQL / SQL Warehouse | No | Yes |
| Delta Live Tables / Lakeflow Pipelines | No | Yes |
| Serverless compute | No | Yes |
| Model Serving | No | Yes |

### DBU Price Comparison (Pay-As-You-Go, East US region)

| Workload / SKU | Standard ($/DBU) | Premium ($/DBU) | Notes |
|---|---|---|---|
| All-Purpose Compute | ~$0.40 | ~$0.55 | Interactive notebooks, ad-hoc analysis |
| All-Purpose Compute (Photon) | not available | ~$0.65 | Vectorized engine; Premium only |
| Jobs Compute | ~$0.20 | ~$0.30 | Automated pipelines, scheduled jobs |
| Jobs Light | not available | ~$0.15 | Lightweight jobs, no Spark; Premium only |
| SQL Warehouse Classic | not available | ~$0.22 | BI queries on shared compute |
| SQL Warehouse Serverless | not available | ~$0.70 | Bundles infra cost; no separate VM bill |
| DLT Core | not available | ~$0.30 | Delta Live Tables; Premium only |
| DLT Pro | not available | ~$0.38 | DLT with SLAs; Premium only |
| DLT Advanced | not available | ~$0.54 | DLT with enhanced observability; Premium only |
| Model Serving (CPU) | not available | ~$0.65 | Real-time inference endpoints |

> Prices are approximate pay-as-you-go rates as of early 2026. Actual rates vary by region (±5–20%). Pre-purchasing Databricks Commit Units (DBCU) for 1 or 3 years can save up to 37%. Always verify current rates at [azure.microsoft.com/pricing/details/databricks](https://azure.microsoft.com/en-us/pricing/details/databricks/).

### Standard Tier Retirement

> **Warning — Standard tier is being retired:**
>
> - **After April 1, 2026:** No new Standard tier workspaces can be created in any Azure subscription.
> - **October 1, 2026:** All remaining Standard tier workspaces are automatically upgraded to Premium.
>
> Automatic upgrade to Premium means an immediate DBU cost increase of approximately 35–40% for All-Purpose and Jobs workloads. Workspaces not proactively migrated before October 1, 2026 will be converted without opt-out. Plan the migration now.

---

## Two Billing Streams

Every Azure Databricks workspace generates charges across two completely separate billing paths. This is the most important structural concept for cost tracking: conflating the two streams is the primary reason teams underestimate total Databricks spend by 30–60%.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      AZURE DATABRICKS WORKSPACE                             │
│                                                                             │
│   You run a notebook, job, SQL query, pipeline, or model serving request    │
└──────────────────────────────┬──────────────────────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               │                               │
               ▼                               ▼
┌──────────────────────────┐     ┌─────────────────────────────┐
│  STREAM 1: DBU CHARGES   │     │  STREAM 2: AZURE INFRA      │
│                          │     │                             │
│  Billed by:              │     │  Billed by:                 │
│  Databricks, Inc.        │     │  Microsoft Azure            │
│  via Azure Marketplace   │     │  (standard resource costs)  │
│                          │     │                             │
│  Workload types:         │     │  Resource types:            │
│  · All-Purpose Compute   │     │  · VMs (cluster nodes)      │
│  · Jobs Compute          │     │  · Managed disks            │
│  · Jobs Light            │     │  · Storage accounts (DBFS)  │
│  · SQL Warehouse Classic │     │  · VNet / subnets           │
│  · SQL Warehouse Serverless     │  · Network Security Groups  │
│  · Model Serving         │     │  · Public IP addresses      │
│  · DLT / Lakeflow        │     │  · Load balancers           │
│  · Serverless Jobs       │     │  · Key Vault                │
│  · Serverless Notebooks  │     │  · Log Analytics workspace  │
│                          │     │  · Networking / egress      │
│  Appears in Cost Mgmt:   │     │                             │
│  Marketplace / SaaS      │     │  Appears in Cost Mgmt:      │
│  charges (NOT in any     │     │  Resource group costs —     │
│  resource group)         │     │  filter by managed RG       │
│                          │     │                             │
│  Tracked via:            │     │  Tracked via:               │
│  system.billing.usage    │     │  Azure Cost Management API  │
│  system.billing.         │     │  az costmanagement query    │
│    list_prices           │     │  az consumption usage list  │
│  (Databricks SQL)        │     │  (Azure CLI / portal)       │
└──────────────────────────┘     └─────────────────────────────┘

  EXCEPTION: Serverless workloads (SQL Serverless, Serverless Jobs,
  Serverless Notebooks) bundle infrastructure into the DBU price.
  For those SKUs, Stream 2 has no separate VM charges — only Stream 1.
```

**Tracking each stream:**

| Stream | Tool | Where to query |
|---|---|---|
| DBU charges | `system.billing.usage` | Databricks SQL Editor in any workspace |
| DBU rates | `system.billing.list_prices` | Databricks SQL Editor in any workspace |
| Azure infra | Azure Cost Management (portal) | Portal → Cost Management + Billing → Cost Analysis |
| Azure infra | `az costmanagement query` | Azure CLI |

---

## The Managed Resource Group

When you deploy an Azure Databricks workspace, Azure automatically provisions a second resource group alongside your workspace resource group. This is the **managed resource group** — a locked container that Databricks controls and uses to run your clusters.

### What it is

The managed resource group is an Azure-managed resource group that Databricks owns on your behalf. It holds the infrastructure required to operate the workspace. You have read access but cannot modify or delete its contents.

### Naming convention

```
databricks-rg-<workspace-name>-<random-suffix>
```

Example — workspace named `analytics-prod`:

```
databricks-rg-analytics-prod-xqz8m7wnkd4eo
```

The suffix is generated at workspace creation and cannot be changed after the fact. You can specify a custom managed resource group name at deployment time using ARM templates, Terraform, or the Databricks REST API — but the Azure portal does not expose this option.

```bash
# Terraform: control the managed resource group name at workspace creation
resource "azurerm_databricks_workspace" "example" {
  name                        = "analytics-prod"
  resource_group_name         = azurerm_resource_group.main.name
  location                    = azurerm_resource_group.main.location
  sku                         = "premium"
  managed_resource_group_name = "databricks-mrg-analytics-prod"
}
```

### Resources inside the managed resource group

**Always present (created at workspace provisioning):**

| Resource type | Purpose |
|---|---|
| Storage account | DBFS root (`dbfs:/`) — workspace default storage, also holds cluster logs and job output |
| Network Security Group (NSG) | Controls inbound/outbound traffic to cluster nodes |
| Virtual Network (VNet) + subnets | Default network for cluster nodes (present in default deployment; not created here in VNet-injected workspaces — existing subnets are used instead) |

**Created dynamically when clusters start, destroyed when clusters terminate:**

| Resource type | Purpose |
|---|---|
| Virtual Machines | Driver and worker nodes for each active cluster |
| Managed disks | OS disk + data/shuffle disks per VM |
| Network interfaces (NICs) | One per VM |
| Public IP addresses | One per VM (when public network access is not disabled) |
| Load balancer | Driver node reachability |

**Present when specific features are enabled:**

| Resource type | Condition |
|---|---|
| VNet + subnets | Standard (non-injected) deployment only |
| Customer VNet references | VNet injection — existing VNet/subnets used; no new VNet created in managed RG |
| Azure Key Vault | Customer-managed keys (CMK) enabled |
| Log Analytics workspace | Diagnostic logging / Azure Monitor integration enabled |

### Why you cannot modify or delete resources in it

Azure applies a **deny assignment** to the managed resource group at workspace creation. This is a system-level lock that blocks all write, delete, and action operations from any principal — including subscription owners — except the Databricks control plane service principal.

Practical consequences:

- Attempting to delete a VM will return a 403 error.
- Attempting to modify an NSG rule or VNet config will be rejected.
- You cannot delete the managed resource group while the workspace exists.
- Modifying resources through workarounds risks corrupting cluster provisioning.

The deny assignment exists so Databricks can guarantee infrastructure state. Clusters are ephemeral by design: Databricks starts VMs when a cluster is created and deletes them on termination. Any external modification could leave orphaned resources or break cluster bring-up.

**Billing implication:** Because VMs and disks are created and destroyed with each cluster, your Stream 2 infrastructure costs fluctuate directly with cluster activity. A workspace with zero running clusters still incurs a continuous storage account cost for DBFS root.

```bash
# List all resources in the managed resource group
az resource list \
  --resource-group "databricks-rg-<workspace-name>-<suffix>" \
  --output table

# Inspect the deny assignment (confirm the lock)
az lock list \
  --resource-group "databricks-rg-<workspace-name>-<suffix>" \
  --output table
```

---

## How to Find Your Costs in the Portal

DBU charges and infrastructure charges surface in different views inside Azure Cost Management. You must check both to get an accurate total.

### Step 1 — Find DBU charges (Stream 1)

DBU charges are billed through Azure Marketplace as a SaaS charge. They are not attached to any resource group — filtering by resource group will not show them.

1. Open the **Azure portal** and navigate to **Cost Management + Billing**.
2. Select your subscription scope, then open **Cost analysis**.
3. Add a filter: **Publisher type** = `Marketplace`.
   - Alternatively: **Service name** = `Azure Databricks`.
4. Set your date range. Group by **Meter category** or **Meter** to see individual workload types.
5. DBU line items appear as charges from publisher **Databricks, Inc.** with meter names such as:
   - `Premium All Purpose Compute DBU`
   - `Premium Jobs Compute DBU`
   - `Premium SQL Compute DBU`
   - `Premium Serverless SQL Compute DBU`
   - `Standard All Purpose Compute DBU`

> If you filter by resource group here, DBU charges disappear entirely — this is expected. They exist only in the Marketplace / SaaS billing channel.

### Step 2 — Find infrastructure charges (Stream 2)

Infrastructure charges are standard Azure resource charges and appear in resource group cost views.

1. In **Cost Management + Billing** → **Cost analysis** (same subscription scope).
2. Add a filter: **Resource group** = `databricks-rg-<your-workspace-name>-<suffix>`.
3. Group by **Service name** or **Resource type** to break down the costs.
4. Expected line items:
   - `Virtual Machines` — cluster driver and worker node compute
   - `Storage` — DBFS root storage account
   - `Managed Disks` — OS and data disks per node
   - `Bandwidth` — data egress / network transfer
   - `Azure Key Vault` — if CMK is enabled
   - `Log Analytics` — if diagnostic logging is enabled

### Step 3 — Combine both for total workspace cost

To see total Databricks spend (DBU + infrastructure) in one view:

1. In **Cost analysis**, set scope to your subscription.
2. Remove resource group filters. Group by **Resource group**.
3. Your workspace resource group shows Marketplace DBU charges; your managed resource group shows infrastructure charges.
4. Sum both groups to get total Databricks cost for that workspace.

Alternatively, apply a shared tag (e.g., `project: databricks`) to both the workspace resource group and managed resource group, then filter Cost Analysis by that tag. This requires tagging to be configured — see [Chapter 3 — Tagging for Cost Attribution](03-tagging-for-cost-attribution.md).

### Quick reference

| Cost type | Where it appears | Filter |
|---|---|---|
| DBU charges (all workload types) | Marketplace / SaaS charges | Publisher type = Marketplace, Service = Azure Databricks |
| VM compute (cluster nodes) | Managed resource group | RG = `databricks-rg-*` → Service = Virtual Machines |
| Managed disks | Managed resource group | RG = `databricks-rg-*` → Service = Storage |
| DBFS root storage | Managed resource group | RG = `databricks-rg-*` → Service = Storage |
| Networking (egress, IPs) | Managed resource group | RG = `databricks-rg-*` → Service = Networking |
| User storage (ADLS Gen2) | Your workspace resource group | Your RG → Service = Storage |
| Key Vault, Log Analytics | Your workspace resource group | Your RG → Service = Security / Monitor |

---

**Navigation:** [← Course Index](index.md) | [Index](index.md) | [Next: Chapter 1 — DBU Cost Parameters →](01-dbu-cost-parameters.md)
