# Step 7 — Automated Shutdown EOD + Weekends, Auto-Startup Mornings

**Navigation:** [← Step 6 — PodDisruptionBudget](06-pod-disruption-budget.md) | [Index](index.md) | [Next: Cluster Audit Checklist →](08-cluster-audit-checklist.md)

---

> **Rule:** Implement automated shutdown at end of day and on weekends. Enable automatic
> startup on weekday mornings, with an option for manual startup when needed.

---

## THE PROBLEM

Dev and Test clusters are used only during business hours. Yet they run 24/7 by default.

```
Business hours: Mon–Fri, 8am–7pm = 11 hours × 5 days = 55 hours/week
Total hours in a week:                                  168 hours

Actual usage: 55 / 168 = 32.7% of the time

You are wasting 67.3% of compute cost every week
on a cluster that nobody is actively using.
```

**Annual waste for a $500/month cluster:**

```
Full-time cost: $500/month × 12 = $6,000/year

With automated shutdown (run only during business hours):
  55 active hours/week = 32.7% of time
  Cost: $500 × 32.7% = $164/month = $1,968/year

Savings: $4,032/year per cluster
```

This single step is often the **largest contributor** to the annual savings target.

---

## THE CONCEPT: AKS Cluster Start/Stop

The AKS **Start/Stop** feature deallocates all node pool VMs while preserving the full
Kubernetes state in etcd.

```
STOP command:
  → All VMs in all node pools are deallocated
  → Compute charges stop immediately
  → Kubernetes objects (Deployments, Services, Secrets, PVCs) preserved in etcd
  → Takes 3–5 minutes

START command:
  → VMs are provisioned again
  → Kubernetes schedules pods back onto nodes
  → Cluster resumes exactly where it left off
  → Takes 3–5 minutes

What you STILL pay while stopped:
  ✅ Managed disks (PVCs retain data — you pay for the storage)
  ✅ Static public IP addresses (if reserved)
  ✅ Log Analytics retention
  ❌ Compute (VMs) → $0 while stopped
  ❌ Control plane (Standard/Premium tier) → $0 while stopped
```

---

## THE MATH

```
Dev cluster (typical):
  System pool:  2× Standard_D2s_v5 → $0.192/hr
  User pool:    2× Standard_D4s_v5 → $0.384/hr
  Total compute: $0.576/hr

Always on:        $0.576 × 24 × 30 = $414/month
Business hours only (55hr/week):
  $0.576 × 55 × 4.33 = $137/month

Savings: $277/month per cluster
Annual: $3,324/year per cluster
```

---

## HOW TO DO IT

### Option A: Manual Commands (Learn This First Before Automating)

```bash
RESOURCE_GROUP="DevClustersRG"
CLUSTER_NAME="dev-cluster-01"

# Stop the cluster (run at end of day)
az aks stop \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME

# Verify it stopped
az aks show \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --query powerState.code \
  --output tsv
# Output: Stopped

# Start the cluster (run in the morning)
az aks start \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME

# Verify it started
az aks show \
  --resource-group $RESOURCE_GROUP \
  --name $CLUSTER_NAME \
  --query powerState.code \
  --output tsv
# Output: Running
```

---

### Option B: Azure Automation Runbooks 

**Step 1: Create an Azure Automation Account**

```bash
# Create the Automation Account
az automation account create \
  --resource-group myOpsRG \
  --name AKSLifecycleAutomation \
  --location eastus \
  --sku Basic

# Enable system-assigned managed identity
az automation account identity assign \
  --resource-group myOpsRG \
  --name AKSLifecycleAutomation \
  --identity SystemAssigned

# Get the managed identity object ID
IDENTITY_ID=$(az automation account show \
  --resource-group myOpsRG \
  --name AKSLifecycleAutomation \
  --query identity.principalId \
  --output tsv)
```

**Step 2: Grant Permission to Manage the Dev Clusters**

```bash
# Grant Contributor role on the resource group containing all Dev clusters
az role assignment create \
  --assignee $IDENTITY_ID \
  --role "Azure Kubernetes Service Contributor Role" \
  --scope "/subscriptions/<sub-id>/resourceGroups/DevClustersRG"
```

**Step 3: Create the Stop Runbook**

```powershell
# Stop-AllDevAKSClusters.ps1
param(
    [string]$ResourceGroupName = "DevClustersRG"
)

Connect-AzAccount -Identity

$clusters = Get-AzAksCluster -ResourceGroupName $ResourceGroupName |
    Where-Object { $_.Tags['Environment'] -eq 'Dev' }

Write-Output "Found $($clusters.Count) Dev AKS cluster(s) to stop"

foreach ($cluster in $clusters) {
    $state = $cluster.PowerState.Code
    Write-Output "Processing: $($cluster.Name) (state: $state)"

    if ($state -eq "Running") {
        Stop-AzAksCluster `
            -ResourceGroupName $ResourceGroupName `
            -Name $cluster.Name `
            -NoWait    # Stop all in parallel
        Write-Output "  ✓ Stop initiated"
    } else {
        Write-Output "  → Already stopped, skipping"
    }
}
```

**Step 4: Create the Start Runbook**

```powershell
# Start-AllDevAKSClusters.ps1
param(
    [string]$ResourceGroupName = "DevClustersRG"
)

Connect-AzAccount -Identity

$clusters = Get-AzAksCluster -ResourceGroupName $ResourceGroupName |
    Where-Object { $_.Tags['Environment'] -eq 'Dev' }

Write-Output "Found $($clusters.Count) Dev AKS cluster(s) to start"

foreach ($cluster in $clusters) {
    $state = $cluster.PowerState.Code
    Write-Output "Processing: $($cluster.Name) (state: $state)"

    if ($state -eq "Stopped") {
        Start-AzAksCluster `
            -ResourceGroupName $ResourceGroupName `
            -Name $cluster.Name `
            -NoWait    # Start all in parallel
        Write-Output "  ✓ Start initiated"
    } else {
        Write-Output "  → Already running, skipping"
    }
}
```

**Step 5: Schedule the Runbooks**

```bash
# Upload and publish the Stop runbook
az automation runbook create \
  --resource-group myOpsRG \
  --automation-account-name AKSLifecycleAutomation \
  --name Stop-AllDevAKSClusters \
  --type PowerShell \
  --location eastus

az automation runbook replace-content \
  --resource-group myOpsRG \
  --automation-account-name AKSLifecycleAutomation \
  --name Stop-AllDevAKSClusters \
  --content @Stop-AllDevAKSClusters.ps1

az automation runbook publish \
  --resource-group myOpsRG \
  --automation-account-name AKSLifecycleAutomation \
  --name Stop-AllDevAKSClusters

# Create schedule: Stop at 7 PM UTC weekdays
az automation schedule create \
  --resource-group myOpsRG \
  --automation-account-name AKSLifecycleAutomation \
  --name Stop-Dev-Evening \
  --frequency Week \
  --interval 1 \
  --start-time "2026-03-23T19:00:00" \
  --time-zone "UTC" \
  --week-days Monday Tuesday Wednesday Thursday Friday

# Create schedule: Start at 7 AM UTC weekdays
az automation schedule create \
  --resource-group myOpsRG \
  --automation-account-name AKSLifecycleAutomation \
  --name Start-Dev-Morning \
  --frequency Week \
  --interval 1 \
  --start-time "2026-03-23T07:00:00" \
  --time-zone "UTC" \
  --week-days Monday Tuesday Wednesday Thursday Friday

# Link runbooks to schedules
az automation job-schedule create \
  --resource-group myOpsRG \
  --automation-account-name AKSLifecycleAutomation \
  --runbook-name Stop-AllDevAKSClusters \
  --schedule-name Stop-Dev-Evening \
  --parameters "{\"ResourceGroupName\": \"DevClustersRG\"}"

az automation job-schedule create \
  --resource-group myOpsRG \
  --automation-account-name AKSLifecycleAutomation \
  --runbook-name Start-AllDevAKSClusters \
  --schedule-name Start-Dev-Morning \
  --parameters "{\"ResourceGroupName\": \"DevClustersRG\"}"
```

---

### Option C: Manual Start Override for Developers (the "when needed" mechanism)

Team members need a way to start their cluster outside of scheduled hours:

```bash
#!/bin/bash
# scripts/start-my-dev-cluster.sh
# Run this when you need the cluster outside of scheduled hours

CLUSTER_NAME="${1:-dev-cluster-01}"
RESOURCE_GROUP="DevClustersRG"

echo "Starting cluster: $CLUSTER_NAME ..."

az aks start \
  --resource-group "$RESOURCE_GROUP" \
  --name "$CLUSTER_NAME"

echo "Waiting for cluster to be ready (this takes 3–5 minutes)..."
az aks wait \
  --resource-group "$RESOURCE_GROUP" \
  --name "$CLUSTER_NAME" \
  --updated \
  --interval 30 \
  --timeout 600

echo "Updating your kubectl config..."
az aks get-credentials \
  --resource-group "$RESOURCE_GROUP" \
  --name "$CLUSTER_NAME" \
  --overwrite-existing

echo "Cluster is ready!"
kubectl get nodes
```

```bash
# Usage:
./scripts/start-my-dev-cluster.sh dev-cluster-team-a
```

> **Important:** Even when a developer manually starts a cluster, the scheduled STOP at 7 PM
> will still shut it down. This is intentional — no cluster runs overnight accidentally.

---

## HOW TO CHECK

```bash
# Check power state of all Dev clusters
az aks list \
  --resource-group DevClustersRG \
  --query "[?tags.Environment=='Dev'].[name, powerState.code]" \
  --output table

# Should show most as "Stopped" outside business hours:
# Name                  PowerState
# ───────────────────────────────
# dev-cluster-team-a    Stopped
# dev-cluster-team-b    Stopped
# dev-cluster-team-c    Stopped

# Verify automation jobs are running successfully
az automation job list \
  --resource-group myOpsRG \
  --automation-account-name AKSLifecycleAutomation \
  --output table

# After 2 weeks: compare week-over-week compute costs in Azure Cost Management
# Look for the characteristic "sawtooth" pattern — cost drops on weekends
```

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| Developer loses terminal session when cluster stops | AKS Stop preserves all K8s objects — only the terminal session is lost. Educate the team. |
| Automated start fails → developers can't work | Set up failure alerts on the Automation Account; provide the manual start script as fallback |
| Cluster state is lost after 12 months stopped | AKS preserves state for up to 12 months. Dev clusters are started daily so this is not a concern. |
| Long-running overnight jobs are interrupted | Use a separate "nightbatch" job cluster, or let the job owner delay the stop for that day |
| NAP-enabled clusters cannot use Stop/Start | Document which clusters use NAP; use `kubectl scale nodepool --node-count 0` instead |

---

**Navigation:** [← Step 6 — PodDisruptionBudget](06-pod-disruption-budget.md) | [Index](index.md) | [Next: Cluster Audit Checklist →](08-cluster-audit-checklist.md)
