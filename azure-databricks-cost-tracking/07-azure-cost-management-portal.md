**Navigation:** [← Chapter 6 — Automating Cost Reports](06-az-cli-automation.md) | [Index](index.md) | [Next: Unified Cost Tracking Strategy →](08-unified-cost-tracking-strategy.md)

> **Rule:** CLI is for automation; the portal is for humans. Use Azure Cost Management portal for visual analysis, stakeholder sharing, and proactive budget controls that alert before you overspend.

---

## THE PROBLEM

The CLI automation from Chapters 5 and 6 is powerful — but it assumes the person consuming the output can read a terminal. Engineers are fine with that. Managers, finance teams, and non-technical stakeholders are not. They need charts, not JSON.

Beyond presentation, the portal provides two capabilities that are genuinely hard to replicate with the CLI: saved views that any team member can open in two clicks, and budgets that send automatic email alerts when your spend crosses a threshold — before you even look at a dashboard. A cron job that posts to Slack tells you what happened. A budget alert tells you before it happens.

---

## THE CONCEPT

Four portal capabilities cover the full stakeholder surface area:

**Cost Analysis** — ad-hoc visual queries with flexible filters and grouping. You pick a date range, add filters (service, resource group, tag), choose a grouping dimension, and get a chart. No code. The right tool for exploratory questions like "where did that spike come from?" or "how has this month tracked against last month?"

**Custom saved views** — named filter configurations you can return to with one click. Build the views once (DBU costs, infrastructure costs, per-team breakdown), save them, and anyone on the team can open the same view without reconstructing it. Saved views can be shared across the team or kept private.

**Budgets** — monthly spend thresholds with configurable alert conditions. You set an amount, define alert thresholds (e.g., 50%, 80%, 100% of budget), and specify recipients. Azure evaluates actual spend against the budget every 4–8 hours and sends email when a threshold is crossed. You can also alert on forecasted spend, so you know you are on track to overspend before you actually do.

**Dashboards** — pinned charts assembled into a shared view. Pin the charts from your saved Cost Analysis views to a single dashboard, set it as shared, and give your manager the URL. It updates automatically as new cost data arrives.

---

## HOW TO DO IT — Part 1: Cost Analysis Views

### View 1 — DBU costs only

1. Navigate to: **Azure portal > Cost Management + Billing > Cost Management > Cost Analysis**
2. Set scope: your subscription, or narrow to the workspace resource group (faster)
3. Click **Add filter** > **Service name** = `Azure Databricks`
4. Set **Group by**: `Meter`
5. Switch the chart type to **Daily costs** (bar chart) for a trend view across the selected period
6. Click **Save** > enter name `Databricks DBU Costs` > set visibility to **Shared** so teammates can access it

This view shows only Marketplace DBU charges. Because the filter is `ServiceName = "Azure Databricks"`, infrastructure costs (VMs, disks, storage) do not appear here — they have different service names. Use this view for DBU trend analysis and spotting days with unexpectedly high DBU burn.

### View 2 — Infrastructure costs

1. Navigate to: **Cost Management > Cost Analysis** (same entry point)
2. Click **Add filter** > **Resource group** = `databricks-rg-<workspace-name>-<suffix>` (the managed RG that Databricks creates)
3. Set **Group by**: `Resource type`
4. You will see the breakdown across: Virtual machines, Managed disks, Storage accounts, Load balancers, and Network interfaces
5. Click **Save** > name it `Databricks Infrastructure` > set visibility to **Shared**

The managed RG name follows the pattern `databricks-rg-<workspace-name>-<random-suffix>`. Find it under the workspace's Overview blade in the Azure portal, next to "Managed resource group."

Note: DBU charges (Marketplace billing) do not appear when filtering by resource group — they appear under the subscription scope. Use View 1 for DBU and View 2 for infrastructure; combine them in a dashboard for the full picture.

### View 3 — Combined by team tag

1. Start from **Cost Analysis** at subscription scope
2. Remove any resource group filter
3. Click **Add filter** > **Tag** > key: `team`, value: `data-engineering` (or whichever team tag values you defined in Chapter 3)
4. Set **Group by**: `Service name`
5. Save as `Databricks Team: data-engineering` (create one per team)

This view is what you pull up during a chargeback conversation. It shows each team's total Databricks spend split by service name — DBU vs. VMs vs. storage — for the selected period. It only works if your resources are tagged; see Chapter 3 for the tagging strategy that makes this possible.

### Equivalent CLI: create a budget from the terminal

If you want to create the budget without using the portal UI, use `az consumption budget create`. This is also useful for scripting budget creation across multiple workspaces or environments:

```bash
az consumption budget create \
  --budget-name "databricks-monthly" \
  --amount 5000 \
  --category Cost \
  --resource-group <databricks-resource-group> \
  --time-grain Monthly \
  --start-date $(date +%Y-%m-01) \
  --end-date 2027-12-31
```

---

## HOW TO DO IT — Part 2: Budgets

Budgets send email alerts when your spend crosses a threshold. Set them once and they run indefinitely — no cron job required.

### Portal steps

1. Navigate to: **Cost Management > Budgets > + Add**
2. **Scope**: subscription (catches all Databricks charges including Marketplace DBU), or narrow to a specific resource group for infrastructure-only tracking
3. **Budget name**: `databricks-monthly-budget`
4. **Reset period**: Monthly
5. **Amount**: set based on your baseline plus a 20% buffer. If your average monthly spend is $4,000, set $5,000. The 20% buffer gives you room to absorb normal variance without triggering false alerts
6. **Set alert conditions** — add one condition per row:

   | Threshold | Type | Amount (at $5,000 budget) | Action |
   |---|---|---|---|
   | 50% | Actual | $2,500 | Informational — notify team lead |
   | 80% | Actual | $4,000 | Warning — notify team + finance |
   | 100% | Forecasted | $5,000 | Early warning — projected to breach |
   | 100% | Actual | $5,000 | Budget breached — notify all recipients |
   | 120% | Actual | $6,000 | Critical overage — notify finance + escalate |

   The **Forecasted** alert fires before you actually reach 100%, giving you time to act. The **120% Actual** threshold catches runaway spend that blew past the budget despite the earlier alerts — this one should go to finance and trigger an incident response.

7. **Alert recipients**: enter email addresses for each threshold. Add at minimum the data platform lead and the finance contact. Recipients receive email when the threshold is crossed; they do not need Azure portal access to receive the notification.

### CLI version

```bash
# Create budget at resource-group scope
az consumption budget create \
  --budget-name "databricks-monthly" \
  --amount 5000 \
  --category Cost \
  --resource-group <databricks-resource-group> \
  --time-grain Monthly \
  --start-date $(date +%Y-%m-01) \
  --end-date 2027-12-31 \
  --email-recipients "finance@company.com" "dataplatform-lead@company.com" \
  --email-thresholds 50 80 100
```

The `--email-thresholds` flag accepts multiple space-separated percentage values. Actual vs. Forecasted threshold type is not configurable via this flag — use the portal to add a Forecasted condition on top of the CLI-created budget, or use the REST API (`PUT /budgets/{budgetName}`) to set `thresholdType: Forecasted` in the request body.

---

## HOW TO DO IT — Part 3: Action Groups and Alerts

Budgets send email natively, but if you want cost alerts to reach Teams, Slack, PagerDuty, or a webhook, you need an Action Group. Action Groups are Azure Monitor's reusable notification targets — you define them once and attach them to multiple alert rules or budgets.

### Portal steps

1. Navigate to: **Azure Monitor > Alerts > Action groups > + Create**
2. Select your **subscription** and **resource group** (put the action group in the same RG as your workspace for easy cleanup)
3. **Action group name**: `databricks-cost-alerts`
4. **Display name**: `DB Costs` (limited to 12 characters; appears in the email From line)
5. Under **Actions**, click **+ Add action**:
   - Action type: **Email/SMS/Push/Voice**
   - Add each recipient email address
6. To notify Teams or Slack, add a second action:
   - Action type: **Webhook**
   - URI: your Teams incoming webhook URL or Slack webhook URL
   - Tick **Enable the common alert schema** for consistent payload format

### CLI version

```bash
# Create action group
az monitor action-group create \
  --resource-group <rg> \
  --name "databricks-cost-alerts" \
  --short-name "db-costs" \
  --action email lead-alert lead@company.com \
  --action email finance-alert finance@company.com
```

To attach the action group to a budget, go back to **Cost Management > Budgets**, open the budget you created, click **Manage action groups**, and select `databricks-cost-alerts`.

### Anomaly alerts

If your subscription has Cost Management anomaly detection enabled (currently in preview):

1. Navigate to: **Cost Management > Cost alerts > + Add**
2. Select alert type: **Anomaly**
3. Specify scope (subscription or resource group)
4. Enter a notification email address

Anomaly alerts fire when Azure's ML-based detection identifies a spending pattern that deviates significantly from your historical baseline. They are more sensitive to unexpected spikes than threshold-based budget alerts, but are in preview and may not be available in all subscriptions or regions.

---

## HOW TO DO IT — Part 4: Custom Dashboard

A dashboard brings the Cost Analysis saved views together into a single page you can share with a link.

1. Navigate to: **Azure portal > Dashboard > + New dashboard** > **Blank dashboard**
2. **Name**: `Databricks Cost Overview`
3. Pin the following charts to the dashboard (navigate to each saved Cost Analysis view, then click the pin icon in the top-right corner of the chart):
   - `Databricks DBU Costs` — Daily bar chart, last 30 days
   - `Databricks Infrastructure` — Resource type donut chart, current month
   - Budget status gauge: **Cost Management > Budgets** > open `databricks-monthly-budget` > click the pin icon
4. Arrange tiles by dragging them to your preferred layout
5. Click **Share** in the toolbar, select your subscription, and click **Publish**

Publishing generates a URL that anyone with access to the subscription can open. Share it in your team channel or link to it from your team wiki. The charts update automatically as new cost data arrives (subject to the 24–48 hour data lag).

---

## Azure Advisor Recommendations

Azure Advisor scans your resources and surfaces cost optimization suggestions. For Databricks workspaces, the recommendations worth checking regularly are:

- **Underutilized VMs** in the managed RG — if clusters run with low average CPU utilization over 7+ days, Advisor flags the underlying VMs as candidates for right-sizing or shutdown. This typically indicates All-Purpose clusters that are left running between jobs.
- **Reserved instance recommendations** — for predictable All-Purpose compute (BI clusters, always-on dev environments), Advisor calculates the 1-year or 3-year reserved instance savings compared to pay-as-you-go. Savings are typically 40–60%.
- **Right-sizing suggestions for SQL warehouses** — if a SQL warehouse is consistently running at low concurrency, Advisor may recommend a smaller size.

To review these:

1. Navigate to: **Azure Advisor > Recommendations > Cost**
2. Filter by resource group: enter `databricks` in the resource group filter to narrow to Databricks-related resources
3. Expand each recommendation to see the estimated monthly savings and the specific resource involved

Advisor does not have Databricks-specific cluster awareness — it sees the VMs in the managed RG but does not know whether they are running because a job is active or because someone forgot to terminate a cluster. Cross-reference any Advisor VM recommendation against system table data (`system.billing.usage`) to confirm whether the cluster is genuinely idle before acting on it.

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| Budget alerts are not real-time | Budgets are evaluated every 4–8 hours, not continuously. Do not rely on budget alerts as your only signal for runaway spend — a cluster that burns $500/hour could accumulate several thousand dollars before the alert fires. Complement budgets with the daily reporter script from Chapter 6 for faster detection. |
| Azure Marketplace (DBU) costs are invisible when filtering by resource group | DBU charges are billed through the Azure Marketplace and are associated with the subscription scope, not with the managed resource group. A resource group filter will show you infrastructure costs only. To see DBU charges, filter by `Service name = "Azure Databricks"` at subscription scope. |
| Anomaly alerts are in preview | Anomaly alert availability varies by subscription type and Azure region. If the Anomaly option does not appear in Cost alerts, your subscription or region does not yet support it. Check the Azure Updates page for GA announcements. |
| Saved views are private by default | A new saved view is set to Private, meaning only the creator can see it. Change visibility to Shared before distributing the URL — otherwise teammates will see an empty or different view when they open the same link. |
| Cost analysis data has a 24–48 hour lag | "Yesterday" data may not fully appear until this afternoon. If the portal shows lower-than-expected spend for a recent date, it is likely that billing data has not yet propagated. Wait until the following morning and refresh before concluding that costs were genuinely lower. |

---

**Navigation:** [← Chapter 6 — Automating Cost Reports](06-az-cli-automation.md) | [Index](index.md) | [Next: Unified Cost Tracking Strategy →](08-unified-cost-tracking-strategy.md)
