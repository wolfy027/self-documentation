**Navigation:** [← Chapter 2 — The Hidden Azure Costs](02-azure-infrastructure-costs.md) | [Index](index.md) | [Next: Chapter 4 — Tracking Costs Inside Databricks →](04-databricks-system-tables.md)

> **Rule:** Tag before you track. Without tags, every cost report is a single undifferentiated blob — you can't tell which team, project, or environment is spending what.

---

## THE PROBLEM

Azure Cost Management shows you a "Databricks" line item. Possibly a large one. It does not tell you which team generated it, which project drove it, or whether it came from dev clusters someone forgot to terminate or from production pipelines doing real work.

Cluster-level attribution is invisible without tags. You cannot answer "which team spent the most this month?" by looking at Cost Management alone. You cannot do chargeback to individual cost centers. You cannot compare environment costs (dev vs. staging vs. production) or track whether a new project is staying within its budget.

Tags are the bridge between "Databricks spent $X" and "team A spent $Y on project Z in production."

---

## THE CONCEPT

Databricks tagging operates at three distinct layers, and each layer propagates differently into Azure Cost Management and the Databricks system tables. Understanding this propagation is essential — applying tags in the wrong layer is the most common reason cost reports still come back undifferentiated.

### Tag propagation rules

| Tag Source | Appears in system.billing.usage? | Appears in Azure Cost Management? | Notes |
|---|---|---|---|
| Workspace ARM tags | No | Yes (on all managed RG resources) | Apply at workspace level via portal/CLI/Terraform |
| Cluster custom tags | Yes (custom_tags column) | Partial (only some Azure resources) | Set per-cluster in JSON config or cluster policy |
| Job tags | Yes (usage_metadata) | No | Only visible in system tables |
| Default tags (ClusterId, Creator, JobId, RunName) | Yes | No | Auto-applied by Databricks |

The key insight: **workspace ARM tags are the only reliable way to get tags into Azure Cost Management**. Cluster custom tags reach system tables but do not reliably propagate to all Azure-managed resources (VMs, disks, NICs) in the managed resource group. If your finance team pulls reports from Cost Management, workspace ARM tags are what they will see.

### Default tags Databricks auto-applies

Databricks automatically applies the following tags to clusters without any configuration:

- `ClusterId` — unique cluster identifier
- `Creator` — email of the user who created the cluster
- `JobId` — ID of the job (for job clusters only)
- `RunName` — name of the job run
- `ClusterName` — display name of the cluster

These default tags are visible in `system.billing.usage` in the `custom_tags` column. They are not visible in Azure Cost Management. They are useful for per-cluster attribution inside Databricks but cannot substitute for workspace ARM tags when you need cost data in Azure tooling.

---

## HOW TO DO IT

### Layer 1: Workspace ARM tags via az CLI

Apply tags to the Databricks workspace resource itself. These tags propagate to the managed resource group and to Azure Cost Management.

```bash
az resource tag \
  --tags environment=production team=data-engineering cost-center=DE-001 \
  --resource-group <resource-group-name> \
  --name <workspace-name> \
  --resource-type Microsoft.Databricks/workspaces
```

Replace `<resource-group-name>` and `<workspace-name>` with your values. The `--tags` flag accepts space-separated `key=value` pairs. This command overwrites all existing tags — use `az resource tag --is-incremental` to merge instead of replace.

---

### Layer 2: Cluster tags via Databricks REST API

Apply custom tags to an existing cluster. These tags appear in `system.billing.usage` under the `custom_tags` column.

```bash
curl -X POST https://<workspace-url>/api/2.0/clusters/edit \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "cluster_id": "<cluster-id>",
    "custom_tags": [
      {"key": "team", "value": "data-engineering"},
      {"key": "project", "value": "etl-pipeline"},
      {"key": "cost-center", "value": "DE-001"},
      {"key": "environment", "value": "production"}
    ]
  }'
```

Replace `<workspace-url>` (e.g. `adb-1234567890123456.7.azuredatabricks.net`), `<token>` (a personal access token or service principal token), and `<cluster-id>` with your values.

Alternatively, set tags in the Databricks UI under **Cluster > Advanced Options > Tags**, or by including them directly in the cluster JSON configuration:

```json
{
  "cluster_name": "etl-production",
  "spark_version": "14.3.x-scala2.12",
  "node_type_id": "Standard_DS3_v2",
  "custom_tags": {
    "team": "data-engineering",
    "project": "etl-pipeline",
    "cost-center": "DE-001",
    "environment": "production"
  }
}
```

---

### Layer 3: Cluster policy enforcing mandatory tags

Cluster policies prevent clusters from being created without required tags. This is the enforcement mechanism — without it, tags are opt-in and will be inconsistently applied.

Create or update a cluster policy with tag constraints:

```json
{
  "custom_tags.team": {
    "type": "allowlist",
    "values": ["data-engineering", "data-science", "analytics", "platform"],
    "defaultValue": "platform"
  },
  "custom_tags.environment": {
    "type": "allowlist",
    "values": ["dev", "staging", "production"]
  },
  "custom_tags.cost-center": {
    "type": "regex",
    "pattern": "^[A-Z]{2,4}-[0-9]{3,4}$"
  }
}
```

- `allowlist` restricts the tag to a fixed set of values
- `regex` enforces a format (here: 2–4 uppercase letters, hyphen, 3–4 digits)
- Adding `"defaultValue"` pre-fills the field for the user

Apply the policy via the Databricks UI under **Admin Console > Cluster Policies**, or via the REST API (`POST /api/2.0/policies/clusters/create`).

---

### Layer 4: Job tags via Databricks jobs API

Job tags appear in `system.billing.usage` under `usage_metadata`. They do not appear in Azure Cost Management.

```bash
curl -X POST https://<workspace-url>/api/2.1/jobs/update \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": <job-id>,
    "new_settings": {
      "tags": {
        "team": "data-engineering",
        "project": "daily-etl",
        "cost-center": "DE-001"
      }
    }
  }'
```

Replace `<job-id>` with the numeric job ID (no quotes). Job tags are particularly useful for attributing serverless compute costs, where there is no persistent cluster to tag.

---

## HOW TO CHECK

### Check workspace ARM tags

```bash
az resource show \
  --resource-group <resource-group-name> \
  --name <workspace-name> \
  --resource-type Microsoft.Databricks/workspaces \
  --query tags \
  --output table
```

This returns the tags currently applied to the workspace resource. If the output is empty or missing expected keys, the tags were not applied (or were overwritten).

### Check cluster and job tags in system tables

Run this query in Databricks SQL against `system.billing.usage`:

```sql
SELECT DISTINCT custom_tags
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 7 DAYS
  AND custom_tags IS NOT NULL
LIMIT 20;
```

This shows the tag maps that have appeared in recent billing records. If `custom_tags` is consistently `NULL` or missing expected keys, the clusters generating those records do not have custom tags set.

To check job tag propagation:

```sql
SELECT
  usage_metadata.job_id,
  usage_metadata.run_name,
  custom_tags,
  SUM(usage_quantity) AS total_dbus
FROM system.billing.usage
WHERE usage_date >= CURRENT_DATE - INTERVAL 7 DAYS
  AND usage_metadata.job_id IS NOT NULL
GROUP BY 1, 2, 3
ORDER BY total_dbus DESC
LIMIT 20;
```

---

## RECOMMENDED TAG SCHEMA

A practical starting point. Apply consistently across all workspaces and clusters from day one — retrofitting tags after the fact is significantly more effort.

| Tag Key | Example Values | Applied At | Why |
|---|---|---|---|
| team | data-engineering, analytics, platform | Workspace + Cluster | Team-level chargeback |
| environment | dev, staging, production | Workspace + Cluster | Separate env costs |
| cost-center | DE-001, AN-002 | Workspace + Cluster | Finance allocation |
| project | etl-pipeline, ml-training | Cluster + Job | Project-level tracking |
| owner | jane.smith@company.com | Cluster | Accountability |

Apply `team`, `environment`, and `cost-center` at the workspace level (ARM tags) for Cost Management visibility, and repeat them at the cluster level for system table granularity. `project` and `owner` are cluster-level — they change too frequently to be workspace-level tags.

---

## GOTCHAS

| Risk | Mitigation |
|------|------------|
| Cluster custom tags don't propagate to Azure Cost Management automatically | Workspace ARM tags are the only reliable way to get tags into Cost Management. Always tag at the workspace level for any reporting that goes to finance. |
| Tag keys are case-sensitive in system.billing.usage | "Team" and "team" are different keys. Enforce casing via cluster policy regex or allowlist; document the canonical casing in your tagging standard. |
| Removing workspace ARM tags doesn't remove them from already-created VMs in the managed resource group | Existing VMs keep the old tags until the cluster terminates and the VMs are deallocated. Historical cost data in Cost Management will continue to show old tag values for past periods. |
| Azure has a maximum of 50 tags per resource | Workspace and managed RG resources share this limit. Treat it as ~45 usable tags in practice. Consolidate tags that serve the same purpose rather than creating tag proliferation. |
| Cluster policies only enforce tags on new clusters | Existing clusters are not retroactively enforced when a policy is applied. Audit existing clusters and update their tags manually or via the REST API after introducing a policy. |
| Cluster tags take effect only after the cluster is restarted | Editing custom tags on a running cluster does not update billing records until the cluster is terminated and restarted. Tags on running clusters reflect the state at cluster start time. |

---

**Navigation:** [← Chapter 2 — The Hidden Azure Costs](02-azure-infrastructure-costs.md) | [Index](index.md) | [Next: Chapter 4 — Tracking Costs Inside Databricks →](04-databricks-system-tables.md)
