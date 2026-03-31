**Navigation:** [← Chapter 5 — Daily Cost Tracking with az CLI](05-az-cli-daily-usage.md) | [Index](index.md) | [Next: Chapter 7 — Azure Cost Management Portal →](07-azure-cost-management-portal.md)

> **Rule:** Manual cost checks don't scale. Automate the daily summary so cost spikes surface immediately instead of going unnoticed for days.

---

## THE PROBLEM

Running the Chapter 5 queries manually is better than nothing, but it depends on a human remembering to do it. Engineers get busy, queries get skipped, and a cluster that was accidentally left running goes unnoticed until the monthly bill arrives. A $50/day accident becomes a $1,500 surprise.

Automation removes the human dependency. The same query that you ran interactively yesterday runs at 8am every weekday, produces a formatted report, and optionally posts an alert to Teams or Slack — whether or not anyone remembered to check.

---

## THE CONCEPT

### Two automation layers

**Layer 1: Azure Cost Management exports**

Azure has a built-in export mechanism that delivers a CSV of your cost data to a Blob storage container on a recurring schedule. No code required — you configure it once via the CLI or portal and it runs indefinitely. The CSV lands in storage, where downstream processes (Power BI, Azure Data Factory, custom scripts) can pick it up.

This is the right choice when you need a durable, auditable record of cost data, or when another system will consume the data rather than a human reading a report.

**Layer 2: Custom reporter script**

A short bash script wraps the `az rest` query from Chapter 5, formats the output into a readable summary, and can post to a webhook. This gives you more control over format, filtering, and routing than a raw CSV export. It also lets you add logic — for example, comparing yesterday's spend against a rolling 7-day average and flagging anomalies.

Use Layer 1 when you need persistence and downstream integration. Use Layer 2 when you need humans to see a formatted daily summary immediately.

---

## HOW TO DO IT — Part 1: Scheduled Exports

Create a daily export that delivers a cost CSV to a Blob storage container. The export covers the current month's accumulated costs and runs on the same schedule every day.

```bash
SUBSCRIPTION_ID="<your-subscription-id>"
STORAGE_ACCOUNT_ID="/subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-name>"

az costmanagement export create \
  --name "databricks-daily-export" \
  --scope "subscriptions/${SUBSCRIPTION_ID}" \
  --type ActualCost \
  --timeframe MonthToDate \
  --recurrence Daily \
  --recurrence-period from="$(date +%Y-%m-%d)T00:00:00Z" to="2027-12-31T00:00:00Z" \
  --schedule-status Active \
  --storage-account-id "${STORAGE_ACCOUNT_ID}" \
  --storage-container "cost-exports" \
  --storage-directory "databricks"
```

List existing exports to confirm the new export was created:

```bash
az costmanagement export list \
  --scope "subscriptions/${SUBSCRIPTION_ID}" \
  --output table
```

Run an export immediately without waiting for the schedule — useful for testing the configuration before the first scheduled run:

```bash
az costmanagement export execute \
  --name "databricks-daily-export" \
  --scope "subscriptions/${SUBSCRIPTION_ID}"
```

Confirm the CSV landed in storage (allow a few minutes after triggering the run):

```bash
az storage blob list \
  --account-name <storage-name> \
  --container-name "cost-exports" \
  --prefix "databricks/" \
  --query "[].{Name:name, Modified:properties.lastModified, Size:properties.contentLength}" \
  --output table
```

---

## HOW TO DO IT — Part 2: Daily Reporter Script

This script queries yesterday's Databricks costs, breaks them down by service, compares against the 7-day average, and optionally posts a notification to a Teams or Slack webhook.

Save it as `databricks-cost-reporter.sh`, make it executable (`chmod +x databricks-cost-reporter.sh`), and run it manually once before scheduling it to confirm the output looks correct.

```bash
#!/usr/bin/env bash
# databricks-cost-reporter.sh — Daily Databricks cost summary
# Usage: ./databricks-cost-reporter.sh
# Set WEBHOOK_URL env var to post to Teams/Slack

set -euo pipefail

SUBSCRIPTION_ID="${AZURE_SUBSCRIPTION_ID:?Set AZURE_SUBSCRIPTION_ID}"
YESTERDAY=$(date -d 'yesterday' +%Y-%m-%d)
WEEK_AGO=$(date -d '8 days ago' +%Y-%m-%d)

# Query yesterday's costs grouped by ServiceName
RESPONSE=$(az rest \
  --method POST \
  --url "https://management.azure.com/subscriptions/${SUBSCRIPTION_ID}/providers/Microsoft.CostManagement/query?api-version=2023-11-01" \
  --headers "Content-Type=application/json" \
  --body "{
    \"type\": \"ActualCost\",
    \"timeframe\": \"Custom\",
    \"timePeriod\": {\"from\": \"${YESTERDAY}\", \"to\": \"${YESTERDAY}\"},
    \"dataset\": {
      \"granularity\": \"None\",
      \"aggregation\": {\"totalCost\": {\"name\": \"Cost\", \"function\": \"Sum\"}},
      \"grouping\": [{\"type\": \"Dimension\", \"name\": \"ServiceName\"}],
      \"filter\": {
        \"dimensions\": {
          \"name\": \"ResourceGroup\",
          \"operator\": \"Contains\",
          \"values\": [\"databricks\"]
        }
      }
    }
  }")

# Extract costs by service
DBU_COST=$(echo "$RESPONSE" | jq -r '.properties.rows[] | select(.[0] == "Azure Databricks") | .[1]' 2>/dev/null || echo "0")
VM_COST=$(echo "$RESPONSE"  | jq -r '.properties.rows[] | select(.[0] == "Virtual Machines") | .[1]' 2>/dev/null || echo "0")
STOR_COST=$(echo "$RESPONSE" | jq -r '.properties.rows[] | select(.[0] == "Storage") | .[1]' 2>/dev/null || echo "0")
NET_COST=$(echo "$RESPONSE"  | jq -r '.properties.rows[] | select(.[0] == "Bandwidth") | .[1]' 2>/dev/null || echo "0")
TOTAL=$(echo "$DBU_COST + $VM_COST + $STOR_COST + $NET_COST" | bc)

# Print report
echo "╔══════════════════════════════════════════════════╗"
echo "║   Databricks Daily Cost Report: ${YESTERDAY}   ║"
echo "╠══════════════════════════════════════════════════╣"
printf "  DBU Charges (Marketplace):  \$%8.2f\n" "$DBU_COST"
printf "  VM Compute:                 \$%8.2f\n" "$VM_COST"
printf "  Storage:                    \$%8.2f\n" "$STOR_COST"
printf "  Networking:                 \$%8.2f\n" "$NET_COST"
echo "  ──────────────────────────────────────────────"
printf "  TOTAL:                       \$%8.2f\n" "$TOTAL"
echo "╚══════════════════════════════════════════════════╝"

# Post to webhook if configured
if [[ -n "${WEBHOOK_URL:-}" ]]; then
  PAYLOAD="{\"text\": \"Databricks cost ${YESTERDAY}: \$${TOTAL} (DBU: \$${DBU_COST}, VMs: \$${VM_COST}, Storage: \$${STOR_COST})\"}"
  curl -s -X POST -H "Content-Type: application/json" -d "$PAYLOAD" "$WEBHOOK_URL" > /dev/null
  echo "  → Notification sent to webhook"
fi
```

The `WEEK_AGO` variable is defined here for use if you extend the script to query the 7-day rolling average and compare it against `TOTAL` before deciding whether to post an alert. The pattern: query the same endpoint for the window `${WEEK_AGO}` to `${YESTERDAY}` with `granularity: Daily`, sum all rows, divide by 7, compare to `TOTAL`, and add a warning line if `TOTAL` exceeds the average by more than 20%.

---

## HOW TO DO IT — Part 3: Notification Integration

Send the daily summary to a Teams channel or Slack workspace without modifying the reporter script — pipe its output to a webhook separately, or set the `WEBHOOK_URL` environment variable when scheduling.

### Microsoft Teams webhook

Create an incoming webhook in Teams (channel settings → Connectors → Incoming Webhook), then:

```bash
SUMMARY="Databricks cost $(date -d 'yesterday' +%Y-%m-%d): see today's report"
WEBHOOK_URL="https://outlook.office.com/webhook/<your-webhook-id>"

curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{
    \"@type\": \"MessageCard\",
    \"@context\": \"http://schema.org/extensions\",
    \"summary\": \"Databricks Daily Cost Report\",
    \"sections\": [{
      \"activityTitle\": \"Databricks Daily Cost Report\",
      \"activityText\": \"$SUMMARY\"
    }]
  }" \
  "$WEBHOOK_URL"
```

### Slack webhook

Create an incoming webhook in Slack (App settings → Incoming Webhooks), then:

```bash
SUMMARY="Databricks cost $(date -d 'yesterday' +%Y-%m-%d): \$${TOTAL}"
SLACK_WEBHOOK="https://hooks.slack.com/services/<your-webhook-path>"

curl -s -X POST \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$SUMMARY\"}" \
  "$SLACK_WEBHOOK"
```

Both examples work standalone or from inside the reporter script. The `WEBHOOK_URL` variable in the script (line 144) uses the same `curl` pattern — set it to either a Teams or Slack webhook URL.

---

## HOW TO DO IT — Part 4: Schedule the Script

### Cron (local or VM-based)

Add an entry to crontab to run the script at 8am on weekdays. The export and query APIs both have a 24–48h lag, so running in the morning gives yesterday's data enough time to finalize.

```bash
# Add to crontab: crontab -e
0 8 * * 1-5 AZURE_SUBSCRIPTION_ID=<sub-id> WEBHOOK_URL=<url> /path/to/databricks-cost-reporter.sh >> /var/log/databricks-costs.log 2>&1
```

This logs all output (stdout and stderr) to `/var/log/databricks-costs.log`. Check that file if the script stops producing output — the most common failure modes are expired credentials and network timeouts, both of which produce error output that only shows up in the log.

### Azure Automation (cloud-based, no cron needed)

If you do not have a persistent VM to run cron jobs from, Azure Automation provides a managed, cloud-based scheduler:

- Create an **Azure Automation Account** in the same subscription you are querying
- Import the script as a **PowerShell or Python Runbook** (the bash script requires a Linux Hybrid Runbook Worker; alternatively, port the `az rest` call to PowerShell's `Invoke-AzRestMethod`)
- Attach a **Daily schedule** trigger to the Runbook
- Assign a **System-assigned Managed Identity** to the Automation Account and grant it **Cost Management Reader** on the subscription — this eliminates stored credentials entirely

Azure Automation is more operationally complex to set up than cron, but it removes the dependency on a persistent server and handles authentication via Managed Identity rather than stored service principal secrets.

---

## HOW TO CHECK

Verify that the export ran and the script is producing output:

```bash
# Check when the export last ran (and when it will run next)
az costmanagement export list \
  --scope "subscriptions/${SUBSCRIPTION_ID}" \
  --query "[?name=='databricks-daily-export'].{Name:name, LastRun:properties.nextRunTimeEstimate}" \
  --output table

# Check that today's CSV landed in storage
az storage blob list \
  --account-name <storage-name> \
  --container-name "cost-exports" \
  --prefix "databricks/$(date +%Y/%m)/" \
  --output table
```

For the reporter script, run it manually first with a recent date and compare the output total against the Chapter 5 Command 1 query for the same date. They should match within rounding. If the script outputs `0` for all line items, inspect the raw `RESPONSE` variable by temporarily adding `echo "$RESPONSE" | jq .` to the script — the most common cause is a ResourceGroup filter that does not match any of your actual resource group names.

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| Cost Management exports have a 24–48h lag | The export for "today" contains yesterday's finalized data, not live charges. Schedule the export and reporter script to run in the morning so that yesterday's data has had time to fully propagate before the report runs. |
| Storage account must be in the same subscription as the export scope | If the storage account is in a different subscription, the export creation will succeed but the write will fail at runtime. Grant the Cost Management export principal **Storage Blob Data Contributor** on the storage account explicitly, or co-locate the storage account in the same subscription. |
| Webhook message size limit | Teams limits incoming webhook messages to 28 KB; Slack's limit varies by plan. Keep the report payload to a short text summary — do not serialize the full API response into the webhook body. |
| Export storage costs money | Each exported CSV is a storage write plus subsequent reads by downstream consumers. For most teams this is negligible (well under $1/month), but it is nonzero — worth knowing before you create ten exports across ten subscriptions. |
| The `databricks` ResourceGroup filter may miss your workspace RG | The filter `"operator": "Contains", "values": ["databricks"]` catches managed RGs (e.g. `databricks-rg-<workspace>-<suffix>`) but will miss a customer-managed workspace RG named something like `platform-prod` or `data-services`. Run `az group list --query "[?contains(name, 'databricks')]"` to see what the filter actually matches, and adjust the filter values to include any non-standard RG names. |

---

**Navigation:** [← Chapter 5 — Daily Cost Tracking with az CLI](05-az-cli-daily-usage.md) | [Index](index.md) | [Next: Chapter 7 — Azure Cost Management Portal →](07-azure-cost-management-portal.md)
