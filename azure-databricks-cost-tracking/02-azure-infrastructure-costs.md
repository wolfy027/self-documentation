**Navigation:** [← Chapter 1 — DBU Cost Parameters](01-dbu-cost-parameters.md) | [Index](index.md) | [Next: Chapter 3 — Tagging for Cost Attribution →](03-tagging-for-cost-attribution.md)

> **Rule:** The DBU bill is only half the story — Azure infrastructure (VMs, storage, networking, disks) can equal or exceed your DBU charges, and it shows up in a completely different section of your Azure bill.

---

## THE PROBLEM

Most people learn to track DBUs and think they have Databricks costs under control. They do not.

Every time a cluster runs, Azure charges you separately for the underlying virtual machines, the managed disks attached to each node, the storage your workspace uses, and the network traffic your jobs generate. These charges appear under **Virtual Machines**, **Storage**, **Networking**, and **Disks** in Cost Management — not under the Databricks line item. They are easy to miss, easy to dismiss as "just infrastructure," and easy to let grow unchecked.

On a modest production workspace, Azure infrastructure costs routinely match or exceed the DBU bill. On data-heavy workloads with cross-region replication or private endpoints, infrastructure can be two to three times the DBU spend.

---

## THE CONCEPT

### Storage Costs

**DBFS root storage** is created automatically inside the managed resource group when you provision a workspace. It is a blob storage account managed by Databricks — you do not control the lifecycle directly. It stores:

- Cluster init scripts and libraries
- Notebook results and temporary outputs
- Internal Databricks metadata

A small workspace with light usage typically accumulates 5–50 GB here. At $0.023/GB/month for ADLS Gen2 LRS, that is $0.12–$1.15/month — negligible on its own, but DBFS root grows over time as old library versions, notebook outputs, and log fragments accumulate. Without periodic cleanup it can reach hundreds of GB.

**User ADLS Gen2 for Delta tables** is where the real storage bill lives.

| Data volume | Monthly storage cost |
|-------------|----------------------|
| 100 GB      | $2.30                |
| 500 GB      | $11.50               |
| 1 TB        | $23.60               |
| 5 TB        | $118.00              |
| 10 TB       | $236.00              |

At $0.023/GB/month, 1 TB of Delta tables costs $23.60/month. This does not include transaction costs.

**Transaction costs** are charged per 10,000 operations and add up faster than most people expect:

| Operation | Rate per 10,000 | 100M ops/month cost |
|-----------|-----------------|---------------------|
| Write      | $0.065          | $650                |
| List       | $0.065          | $650                |
| Read       | $0.005          | $50                 |

A pipeline doing 100M reads/month adds $50 to the bill. A pipeline doing 10M writes/month adds $65. Delta's frequent small-file activity (compaction, OPTIMIZE, VACUUM) generates list and write operations continuously — this is often the largest storage line item on busy workspaces.

**Log storage** applies if diagnostic settings are enabled. Sending cluster logs, audit events, and Spark application logs to a storage account or Log Analytics adds to both storage volume and transaction counts.

---

### Networking Costs

**VNet injection** is required for production workspaces. When Databricks deploys clusters into your VNet, it provisions resources in the managed resource group: network interfaces, network security groups, and (depending on configuration) load balancers. These carry their own charges.

**Data egress pricing** by destination:

| Traffic path                        | Rate per GB |
|-------------------------------------|-------------|
| Same region, same AZ                | $0.00       |
| Same region, different AZ           | $0.01       |
| Cross-region within US              | $0.02       |
| Outbound to internet (first 10 TB)  | $0.087      |

Jobs that read from or write to resources in a different Azure region pay cross-region egress on every byte. A pipeline moving 1 TB/day cross-region costs $20/day — $600/month — in egress alone, before a single DBU is counted.

**Private endpoints** charge $0.01/hr regardless of cluster state. A single private endpoint for your ADLS account costs approximately $7.20/month plus $0.01/GB processed. The always-on cost applies even when no clusters are running.

**NAT gateway**, if configured for outbound internet access from VNet-injected clusters, costs $0.045/hr plus $0.045/GB processed. At continuous operation: $0.045 × 730hr = **$32.85/month** before any data processing charges.

**Standard Load Balancers** are provisioned in the managed resource group for VNet-injected workspaces. At $0.025/hr, a load balancer running continuously costs $18.25/month.

---

### Compute VM Costs

This is the most important thing to understand: **you pay Azure for the VM and Databricks for the DBU — both charges apply simultaneously for every node-hour a cluster runs.**

A single Standard_DS3_v2 driver node running for an hour costs you:
- $0.19 to Azure (VM)
- $0.225 to Databricks (0.75 DBU × $0.30/DBU for Jobs tier)
- **$0.415 total per node-hour**

Common VM SKUs, hourly and monthly (730 hr) pay-as-you-go cost:

| SKU                  | vCPU | RAM (GB) | $/hr   | $/month (730 hr) | DBU/hr |
|----------------------|------|----------|--------|------------------|--------|
| Standard_DS3_v2      | 4    | 14       | $0.19  | $138.70          | 0.75   |
| Standard_DS4_v2      | 8    | 28       | $0.38  | $277.40          | 1.5    |
| Standard_DS5_v2      | 16   | 56       | $0.76  | $554.80          | 3.0    |
| Standard_D8s_v3      | 8    | 32       | $0.38  | $277.40          | 1.5    |
| Standard_E4s_v3      | 4    | 32       | $0.25  | $182.50          | 0.75   |
| Standard_E8s_v3      | 8    | 64       | $0.50  | $365.00          | 1.5    |

**Spot instances** (Azure Spot VMs) reduce the VM cost by 60–80%. A DS3_v2 spot VM costs roughly $0.038–$0.076/hr instead of $0.19/hr. The DBU rate is **not discounted** — Databricks charges the same DBU rate whether the VM is on-demand or spot. Spot pricing is only visible on the Azure VM line in Cost Management; the Databricks bill is identical either way.

---

### Disk Costs

Every cluster node has an OS disk and, depending on workload, one or more data/shuffle disks. These are billed as managed disks from the moment the cluster starts until it terminates — even if the node is idle.

**OS disk per node** is typically a P10 Premium SSD (128 GB):

| Disk tier | Size  | Monthly cost |
|-----------|-------|--------------|
| P10       | 128 GB | $19.71       |
| E10       | 128 GB | $11.52       |
| P20       | 512 GB | $73.22       |
| P30       | 1 TB   | $135.17      |

A 4-node cluster with P10 OS disks adds $78.84/month in disk charges for a cluster that runs full-time.

**Shuffle and spill disks** are provisioned automatically when Spark needs to spill intermediate data to disk during wide transformations (joins, aggregations, sorts). The size and tier depend on the instance type and workspace configuration. On memory-intensive workloads, shuffle spill can result in large Premium SSD disks being attached during a job and remaining attached until the cluster is terminated.

Disk costs accumulate even when a cluster is sitting idle. A cluster left running overnight with no active jobs continues to accrue disk charges for every attached disk.

---

### Other Costs

**Azure Key Vault** is required for Databricks secret-backed scopes. Key Vault charges $0.03 per 10,000 operations. A workspace with heavy secret usage (hundreds of job runs, each fetching multiple secrets) can generate meaningful Key Vault operation counts, but this is typically a minor line item unless secret fetching is in a tight loop.

**Azure Monitor / Log Analytics**, if used for cluster diagnostics, audit logging, or Spark metrics, charges $2.30/GB ingested. A busy workspace emitting detailed Spark event logs can ingest tens of gigabytes per month. At $2.30/GB, 20 GB/month of log ingestion costs $46/month — often more than the ADLS storage for the actual data.

---

## THE MATH

A worked example: a single 4-node Standard_DS3_v2 Jobs cluster running 8 hours/day, 22 days/month (176 hours total).

```
VMs:         4 nodes × $0.19/hr × 176 hr        = $133.76
OS Disks:    4 nodes × P10 ($19.71/month)        = $78.84
Storage:     500 GB ADLS Gen2 ($11.50)
             + 50M reads ($25.00) + 10M writes ($6.50) = $43.00
DBFS root:   20 GB × $0.023                     = $0.46
Egress:      50 GB cross-region × $0.02/GB      = $1.00
Load balancer: $0.025/hr × 176 hr               = $4.40
─────────────────────────────────────────────────────────
Total Azure infra:                               $261.46/month

Plus DBU charges (Chapter 1, Premium Jobs):     $158.40/month
─────────────────────────────────────────────────────────
GRAND TOTAL (this cluster):                     $419.86/month
DBU as % of total:                               37.7%
Azure infra as % of total:                       62.3%
```

The Azure infrastructure is **62% of the grand total** in this scenario. It is not a rounding error.

For the same cluster running as an All-Purpose (interactive) workload at $0.55/DBU:

| Workload tier             | Azure infra | DBU cost | Grand total |
|---------------------------|-------------|----------|-------------|
| Jobs (Premium, $0.30/DBU) | $261.46     | $158.40  | **$419.86** |
| All-Purpose (Premium, $0.55/DBU) | $261.46 | $290.40 | **$551.86** |

Note: disk charges above assume disks are attached for the full month. If the cluster is fully terminated between sessions, disk cost is prorated to the hours the cluster ran.

---

## COST COMPOSITION BY WORKLOAD TYPE

```
Monthly cost composition (illustrative — 4-node DS3_v2, 176 hr)

Jobs cluster (Premium, $0.30/DBU):
  DBU    [==========]  $158  (38%)
  Infra  [================]  $261  (62%)
         Total: ~$420

SQL Serverless warehouse (equivalent capacity):
  DBU    [==========================]  100%  (VM bundled into DBU rate)
  Infra  []                             0%   (no separate VM/disk charges)
         Total: DBU charges only

All-Purpose cluster (heavy, Premium, $0.55/DBU):
  DBU    [==============]  $290  (45%)
  Infra  [=================]  $357  (55%)  ← higher networking/disk if longer runs
         Total: ~$647

Breakdown of the Infra bar (Jobs cluster, for reference):
  VM     [=========]   $134  (51% of infra)
  Disk   [=====]        $79  (30% of infra)
  Stor   [===]          $43  (17% of infra)
  Net    [=]             $6  ( 2% of infra)
```

Infrastructure share of total spend grows as:
- Clusters run longer (disk cost amortized; VM cost linear)
- Dataset size increases (storage)
- Jobs move data across regions (egress)
- Private endpoints or NAT gateways are added (always-on networking)

SQL Serverless eliminates the infrastructure portion entirely by bundling VM costs into the DBU rate. For short, sporadic jobs the higher DBU rate ($0.70/DBU vs $0.30/DBU) is often offset by zero idle billing and zero disk cost.

---

## GOTCHAS

| Gotcha | Why it matters |
|--------|----------------|
| Managed RG VMs are not the DBU charge — you pay both | A common misconception is that the DBU covers the VM. It does not. Azure bills VM hours; Databricks bills DBU hours. These are independent charges on the same invoice period. |
| Cross-region egress adds up silently | If your Databricks workspace is in East US and your reporting database is in West US, every byte of query result pays $0.02/GB egress. 1 TB/day = $600/month in egress alone. |
| DBFS root grows over time | Old library versions, failed job outputs, and notebook results accumulate in DBFS root. Storage is cheap per GB, but unchecked growth can reach hundreds of GB over months. |
| Spot instance preemption causes job reruns | When a spot VM is preempted mid-job, Databricks retries. The retry runs DBUs from scratch. The discount on VM cost can be erased by 1–2 full job reruns. |
| Private endpoints charge 24/7 even when clusters are off | A private endpoint for ADLS costs ~$7.20/month in hourly charges regardless of whether any cluster is running. Multiple private endpoints multiply this cost. |
| Disk costs accumulate on idle clusters | Managed disks remain attached to cluster nodes until the cluster terminates. A cluster left running over a weekend with no active jobs still accrues P10 disk charges for every node. |
| Azure Monitor log ingestion is expensive at scale | $2.30/GB ingested means verbose Spark application logging for a 10-node cluster can cost more per month than the ADLS storage holding the actual Delta tables. |

---

**Navigation:** [← Chapter 1 — DBU Cost Parameters](01-dbu-cost-parameters.md) | [Index](index.md) | [Next: Chapter 3 — Tagging for Cost Attribution →](03-tagging-for-cost-attribution.md)
