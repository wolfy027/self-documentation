# Putting It All Together — The Cluster Audit Checklist

**Navigation:** [← Step 7 — Automated Shutdown](07-automated-shutdown.md) | [Index](index.md)

---

Use this checklist when analyzing each Dev cluster. Work through the steps sequentially
for each cluster — applying in order from least to most disruptive.

---

## Phase 1: Data Collection (Day 1–2)

```bash
# Set your cluster details
CLUSTER="<your-assigned-cluster>"
RG="<resource-group>"

# Get credentials
az aks get-credentials --resource-group $RG --name $CLUSTER --overwrite-existing

echo "=== Node Pool Count and Config ==="
az aks nodepool list --cluster-name $CLUSTER --resource-group $RG \
  --query "[].{Pool:name, VMSize:vmSize, Count:count, Min:minCount, Max:maxCount, Mode:mode}" \
  --output table

echo "=== Current Node Utilization ==="
kubectl top nodes

echo "=== Replica Counts (sorted highest first) ==="
kubectl get deployments --all-namespaces \
  -o custom-columns="NS:.metadata.namespace,NAME:.metadata.name,REPLICAS:.spec.replicas" \
  | sort -k3 -rn

echo "=== Existing PDBs ==="
kubectl get pdb --all-namespaces

echo "=== Existing ResourceQuotas ==="
kubectl get resourcequota --all-namespaces

echo "=== Existing LimitRanges ==="
kubectl get limitrange --all-namespaces

echo "=== Cluster Power State ==="
az aks show --resource-group $RG --name $CLUSTER --query powerState.code --output tsv
```

---

## Phase 2: Decision Table — Fill This In Per Cluster

| # | Check | Finding | Action Needed? |
|---|---|---|---|
| 1 | Node pool count > 3? | e.g., 5 pools | Yes → consolidate → [Step 1](01-node-pool-consolidation.md) |
| 1 | Any pool min-count > 1? | e.g., min=2 on user pool | Yes → set min-count=1 → [Step 1](01-node-pool-consolidation.md) |
| 2 | Any VM larger than D4s with util < 30%? | e.g., D8s at 8% util | Yes → downsize → [Step 2](02-sku-right-sizing.md) |
| 3 | Any pods with requests >> VPA recommendation? | e.g., 10× over-requested | Yes → right-size → [Step 3](03-pod-requests-limits.md) |
| 3 | LimitRanges in place? | No | Yes → add defaults → [Step 3](03-pod-requests-limits.md) |
| 4 | Any deployment with replicas > 1? | e.g., 12 deployments at 3 | Yes → set to 1 → [Step 4](04-replica-count.md) |
| 5 | ResourceQuotas limiting heavy resource use? | No | Yes → add caps → [Step 5](05-uat-for-performance-testing.md) |
| 6 | PDBs configured correctly for replica count? | Some blocking (0 disruptions) | Yes → fix → [Step 6](06-pod-disruption-budget.md) |
| 7 | Cluster enrolled in automated stop/start? | No | Yes → add to automation → [Step 7](07-automated-shutdown.md) |

---

## Phase 3: Apply Changes (Day 3–5, in this order)

Apply from least to most disruptive:

```
1. Apply LimitRanges             → non-disruptive (affects only new pods)
2. Apply ResourceQuotas          → non-disruptive (blocks new resources over cap)
3. Scale replicas down to 1      → rolling restart (brief, acceptable in Dev)
4. Fix PDBs                      → non-disruptive
5. Enable/tune Cluster Autoscaler → non-disruptive
6. Enroll in stop/start automation → test manually first
7. Consolidate node pools        → requires pod migration — save for last
8. Resize VM SKU                 → requires new pool creation — save for last
```

---

## Phase 4: Expected Savings Per Step

| Step | Optimization | Expected Monthly Savings (Per Cluster) |
|---|---|---|
| 1 | Node pool consolidation (5 pools → 1) | $800–1,200 |
| 2 | VM SKU right-sizing (D8s → D2s, util < 20%) | $200–600 |
| 3 | Pod request right-sizing (fewer nodes needed) | $200–500 |
| 4 | Replica count 3→1 for 20 deployments | $150–300 |
| 5 | Cap Dev resources (protects other savings) | $0 direct; enables Step 4 |
| 6 | Fix PDBs (enables autoscaler consolidation) | Unlocks Steps 1–4 savings |
| 7 | Automated shutdown (7pm–7am + weekends) | $200–400 |
| **Total** | | **$1,550–3,000/month per cluster** |

---

## Phase 5: Validate After 2 Weeks

```bash
# Node count should have decreased
kubectl get nodes

# No pods in Pending state (right-sizing didn't break anything)
kubectl get pods --all-namespaces | grep -v Running | grep -v Completed

# Autoscaler is active and making decisions
kubectl logs -n kube-system -l app=cluster-autoscaler --tail=20

# Check cost trend in Azure Cost Management
# Compare: week before optimization vs. week after
az consumption usage list \
  --scope "/subscriptions/<sub-id>/resourceGroups/$RG" \
  --start-date $(date -d '2 weeks ago' +%Y-%m-%d) \
  --end-date $(date +%Y-%m-%d) \
  --output table
```

---

## Quick-Reference: What to Run on a New Cluster

```bash
#!/bin/bash
# audit-cluster.sh — paste this into any cluster to get a full snapshot

echo "=============================="
echo " AKS Cost Optimization Audit"
echo "=============================="

echo ""
echo "--- NODE POOLS ---"
az aks nodepool list \
  --cluster-name $CLUSTER --resource-group $RG \
  --query "[].{Pool:name,VM:vmSize,Count:count,Min:minCount,Max:maxCount,Mode:mode}" \
  --output table

echo ""
echo "--- NODE UTILIZATION ---"
kubectl top nodes 2>/dev/null || echo "(metrics-server not available)"

echo ""
echo "--- DEPLOYMENTS WITH REPLICAS > 1 ---"
kubectl get deployments --all-namespaces -o json | jq -r '
  .items[] | select(.spec.replicas > 1) |
  .metadata.namespace + "/" + .metadata.name + " → " + (.spec.replicas|tostring) + " replicas"
'

echo ""
echo "--- PDB STATUS ---"
kubectl get pdb --all-namespaces 2>/dev/null

echo ""
echo "--- RESOURCE QUOTAS ---"
kubectl get resourcequota --all-namespaces 2>/dev/null || echo "(none)"

echo ""
echo "--- LIMIT RANGES ---"
kubectl get limitrange --all-namespaces 2>/dev/null || echo "(none)"

echo ""
echo "--- CLUSTER POWER STATE ---"
az aks show --resource-group $RG --name $CLUSTER \
  --query "{Name:name, State:powerState.code}" --output table
```

---

**Navigation:** [← Step 7 — Automated Shutdown](07-automated-shutdown.md) | [Index](index.md)
