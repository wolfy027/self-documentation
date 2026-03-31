**Navigation:** [← Chapter 7 — Azure Cost Management Portal](07-azure-cost-management-portal.md) | [Index](index.md) | [Index →](index.md)

> **Rule:** A cost tracking strategy is only as good as its cadence. Pick the right tool for each job, automate the daily checks, and review on a fixed schedule — or costs silently compound.

---

## THE PROBLEM

You have now learned system tables, the az CLI, portal budgets, Cost Management exports, and tagging. Each tool is useful in isolation. The problem is that using them ad hoc — pulling a system table query when something seems off, opening the portal when finance asks a question, running the CLI script when you remember — produces fragmented tracking. You end up with gaps, duplicate effort, and no clear owner for each cost signal.

Without a clear strategy for what to use when, two failure modes emerge. Over-tracking: you run every query and check every tool daily, spending more time on cost monitoring than it saves. Under-tracking: you rely on whichever tool is most convenient and miss cost spikes that only the other tool would have caught.

This chapter assembles the tools from the previous seven chapters into a single coherent strategy — a decision matrix for which tool covers which need, an implementation checklist with exact commands, a monitoring cadence that minimizes time while maintaining coverage, and a validation script to confirm the setup is healthy.

---

## DECISION MATRIX — WHAT TO USE WHEN

| Need | Best Tool | Why |
|---|---|---|
| DBU deep-dive by cluster/job/user | Databricks system tables (Chapter 4) | Most granular DBU data, custom tags, full SQL flexibility |
| Daily all-in cost check (DBU + infra) | az CLI daily reporter script (Chapter 6) | Covers both billing streams, automatable, no portal needed |
| Visual trend analysis for stakeholders | Azure Cost Management portal (Chapter 7) | Charts, shareable views, non-technical friendly |
| Proactive spend control | Azure budgets + alerts (Chapter 7) | Automatic threshold notifications before overspend |
| Automated daily/weekly reports | Cost Management exports + script (Chapter 6) | Hands-off, scheduled delivery to storage |
| Per-team/project attribution | Tags + system tables or Cost Management (Chapter 3+4) | Tags flow to both billing systems |
| Forensic investigation of a cost spike | System tables (DBU) + az CLI (infra) together | Drill to specific cluster, day, meter |
| Finance / chargeback reporting | Cost Management portal with tag filters | Exportable tables, budget vs. actual |

The overlap is intentional. System tables and the az CLI both surface DBU data, but in different shapes: system tables let you slice by job, user, or custom tag; the CLI reporter gives you the dollar figure without needing a Databricks notebook. Use both — they answer different questions.

---

## IMPLEMENTATION CHECKLIST

Work through the phases in order. Each phase builds on the previous one. The checkbox format is intentional — track your progress and return here after changes.

```
PHASE 1: FOUNDATION (Day 1)
□ Apply ARM tags to all Databricks workspaces (environment, team, cost-center)
  az resource tag --tags environment=production team=<team> cost-center=<code> \
    --resource-group <rg> --name <ws> --resource-type Microsoft.Databricks/workspaces
□ Create cluster policies enforcing mandatory custom tags (Chapter 3)
□ Verify tags propagate — wait 24h, then run:
  az resource show --resource-group <rg> --name <ws> \
    --resource-type Microsoft.Databricks/workspaces --query tags

PHASE 2: DATABRICKS-SIDE TRACKING (Day 2–3)
□ Verify Unity Catalog is enabled and you have system table access:
  SELECT COUNT(*) FROM system.billing.usage WHERE usage_date = CURRENT_DATE - INTERVAL 1 DAYS;
□ Run and save all 7 SQL queries from Chapter 4 as Databricks SQL named queries
□ Set up a Databricks SQL alert on Query 6 (anomaly detection) with email notification

PHASE 3: AZURE-SIDE TRACKING (Day 3–5)
□ Set up daily Cost Management export to storage account:
  az costmanagement export create --name databricks-daily-export ...
□ Download and configure databricks-cost-reporter.sh (Chapter 6)
□ Schedule reporter via cron or Azure Automation
□ Set WEBHOOK_URL to post daily summaries to Teams/Slack

PHASE 4: BUDGETS & ALERTS (Day 5–7)
□ Create monthly budget for each Databricks resource group:
  az consumption budget create --budget-name databricks-monthly --amount <X> ...
□ Set alert thresholds at 50%, 80%, 100%, 120%
□ Create action group with email + webhook targets
□ Test alert: temporarily lower budget below current MTD spend, verify email arrives, then reset

PHASE 5: DASHBOARDS & REVIEW (Day 7–10)
□ Create "Databricks Cost Overview" dashboard in Azure portal
□ Pin: DBU daily trend, infrastructure cost by type, budget status gauge
□ Share dashboard with team and finance stakeholders
□ Block recurring calendar time for weekly and monthly reviews
```

The test step in Phase 4 is the one most teams skip — and then discover their alert is misconfigured the first time they actually need it. Lower the budget below current MTD spend for five minutes, confirm the email arrives, then set it back to the real value. This takes ten minutes and eliminates an entire class of false confidence.

---

## MONITORING CADENCE

| Frequency | Action | Tool | Time |
|---|---|---|---|
| Daily | Check automated reporter output or Teams/Slack notification | Reporter script | 2 min |
| Weekly | Review anomaly query (Query 6) and top-10 clusters (Query 2) | Databricks SQL | 15 min |
| Monthly | Full budget reconciliation, compare actual vs plan | Azure Cost Management portal | 30 min |
| Monthly | Review Azure Advisor cost recommendations | Azure Advisor | 10 min |
| Quarterly | Audit: are tags applied? exports running? budgets set? | Validation script (below) | 15 min |

The daily check is passive — the reporter script runs via cron and posts to Teams or Slack. You are not opening a tool; you are reading a message that arrives in a channel you already check. If no message arrives, that itself is a signal (the script failed, or the export is broken). Keep the 2-minute estimate realistic by setting the channel notification to be skimmable: one line per metric, not a wall of JSON.

The quarterly audit exists because tracking infrastructure drifts. Cluster policies get modified, tags get removed when resources are recreated, budgets get stale as spend patterns change. Run the validation script below and treat any failure as a maintenance ticket.

---

## VALIDATION SCRIPT

Run this script quarterly (or after any infrastructure change) to confirm the cost tracking setup is intact. It checks tags, exports, and budgets — the three components most likely to silently break.

```bash
#!/usr/bin/env bash
# databricks-cost-tracking-audit.sh — Check cost tracking setup health

set -euo pipefail

SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID:?Set AZURE_SUBSCRIPTION_ID}"
WORKSPACE_NAME="${DATABRICKS_WORKSPACE_NAME:?Set DATABRICKS_WORKSPACE_NAME}"
WORKSPACE_RG="${DATABRICKS_RESOURCE_GROUP:?Set DATABRICKS_RESOURCE_GROUP}"
PASS=0
FAIL=0

check() {
  local name="$1"
  local result="$2"
  if [[ "$result" == "PASS" ]]; then
    echo "  ✓ PASS  $name"
    ((PASS++))
  else
    echo "  ✗ FAIL  $name  →  $result"
    ((FAIL++))
  fi
}

echo "=== Databricks Cost Tracking Audit ==="
echo "Workspace: ${WORKSPACE_NAME} (${WORKSPACE_RG})"
echo ""

# Check 1: Workspace tags
REQUIRED_TAGS="team environment cost-center"
WORKSPACE_TAGS=$(az resource show \
  --resource-group "${WORKSPACE_RG}" \
  --name "${WORKSPACE_NAME}" \
  --resource-type Microsoft.Databricks/workspaces \
  --query "tags" -o json 2>/dev/null || echo "{}")

for tag in $REQUIRED_TAGS; do
  val=$(echo "$WORKSPACE_TAGS" | jq -r --arg t "$tag" '.[$t] // empty')
  if [[ -n "$val" ]]; then
    check "Workspace tag '${tag}'" "PASS"
  else
    check "Workspace tag '${tag}'" "Tag not set on workspace"
  fi
done

# Check 2: Cost Management export exists
EXPORT_COUNT=$(az costmanagement export list \
  --scope "subscriptions/${SUBSCRIPTION_ID}" \
  --query "length(value[?contains(name, 'databricks')])" \
  -o tsv 2>/dev/null || echo "0")

if [[ "$EXPORT_COUNT" -gt 0 ]]; then
  check "Cost Management export configured" "PASS"
else
  check "Cost Management export configured" "No export named *databricks* found"
fi

# Check 3: Budget exists
BUDGET_COUNT=$(az consumption budget list \
  --scope "subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${WORKSPACE_RG}" \
  --query "length(@)" \
  -o tsv 2>/dev/null || echo "0")

if [[ "$BUDGET_COUNT" -gt 0 ]]; then
  check "Budget configured for workspace RG" "PASS"
else
  check "Budget configured for workspace RG" "No budget found for ${WORKSPACE_RG}"
fi

echo ""
echo "─────────────────────────────────────────"
echo "  Results: ${PASS} passed, ${FAIL} failed"
if [[ "$FAIL" -gt 0 ]]; then
  echo "  → Review failed checks and re-run."
  exit 1
else
  echo "  → Cost tracking setup looks healthy!"
fi
```

Save this as `databricks-cost-tracking-audit.sh`, make it executable (`chmod +x`), and add it to your quarterly ops checklist. The script exits with code 1 if any check fails, so it works in CI if you want to gate deployments on a healthy tracking setup.

---

## WHAT THIS COURSE DID NOT COVER

This course focused on tracking — observability over spend, not reducing it. Three areas are the natural next step once tracking is in place:

**Cost optimization** — right-sizing clusters for actual workload, enabling autoscaling with appropriate min/max bounds, switching interactive clusters to spot (preemptible) instances, and evaluating reserved instances for predictable All-Purpose compute. None of these actions are safe to take without first understanding your usage patterns, which is why tracking comes first.

**Multi-workspace account-level cost aggregation** — this course covered a single workspace. Large organizations run dozens of workspaces across business units and environments. Databricks account-level billing provides cross-workspace rollups in `system.billing.usage` at the account level (not workspace level), and Azure Cost Management can be scoped to a management group to aggregate across subscriptions. Both require additional access and setup beyond what was covered here.

**Third-party cost management tools** — CloudHealth, Overcast, Spot.io, and similar platforms provide multi-cloud cost management with more opinionated dashboards and optimization recommendations than the native Azure tools. They are worth evaluating once you have baseline tracking in place and a clear picture of where Azure-native tooling falls short for your team.

These are not gaps — they are the next layer. The foundation built in this course (tags, system tables, CLI automation, budgets, exports, portal views) is the prerequisite for all of them.

---

**Navigation:** [← Chapter 7 — Azure Cost Management Portal](07-azure-cost-management-portal.md) | [Index](index.md) | [Index →](index.md)
