# Step 1 — Node Pool Consolidation

**Navigation:** [← Background Knowledge](00-basics.md) | [Index](index.md) | [Next: Step 2 — SKU Right-Sizing →](02-sku-right-sizing.md)

---

> **Rule:** If the node pool count exceeds 3 → review the use case, recommend moving
> to shared node pools where possible, enable autoscaling, set the minimum data node count
> to 1 for Dev and Test, use namespace-level isolation if required.

---

## THE PROBLEM

Every node pool in AKS is a separate Virtual Machine Scale Set (VMSS). Each pool has:

- A **minimum node count** — VMs that run 24/7 regardless of workload
- **System overhead** — each node reserves ~1 vCPU and ~1.5 GB RAM for Kubernetes itself
- **Fixed costs** — even idle nodes cost money

When a cluster has 5, 6, or 7 node pools each with a minimum of 2 nodes, you end up paying
for 10–14 VMs that are mostly idle in a Dev environment.

**Typical Waste Pattern:**

```
Node Pool 1 (frontend):    min=2 nodes × Standard_D4s_v5 = 2 VMs running 24/7
Node Pool 2 (backend):     min=2 nodes × Standard_D4s_v5 = 2 VMs running 24/7
Node Pool 3 (database):    min=2 nodes × Standard_D4s_v5 = 2 VMs running 24/7
Node Pool 4 (ml-tasks):    min=2 nodes × Standard_D4s_v5 = 2 VMs running 24/7
Node Pool 5 (monitoring):  min=2 nodes × Standard_D4s_v5 = 2 VMs running 24/7

Total: 10 VMs always on → ~$1,382/month
```

In a Dev environment, all 10 VMs are at ~15% utilization. You're paying for 10 VMs but
effectively using the equivalent of 1.5 VMs worth of compute.

---

## THE CONCEPT: Shared Node Pools + Namespace Isolation

Instead of separate node pools per team/workload, use **one shared node pool** and separate
workloads using **Kubernetes Namespaces**.

```
BEFORE (5 separate pools):                AFTER (1 shared pool):

[ frontend pool ] ← 2 VMs               [ shared-user pool ] ← 1 VM (autoscaled)
[ backend pool  ] ← 2 VMs               │
[ db pool       ] ← 2 VMs               ├── namespace: frontend
[ ml pool       ] ← 2 VMs               ├── namespace: backend
[ monitoring    ] ← 2 VMs               ├── namespace: database
                                         ├── namespace: ml-tasks
Total: 10 VMs minimum                    └── namespace: monitoring

                                         Total: 1 VM minimum (scales as needed)
```

**Namespace isolation** gives each team their own virtual space with:
- Separate ResourceQuotas (CPU/memory caps per team)
- Separate RBAC (access control)
- Cost tracking per namespace (via AKS Cost Analysis or Kubecost)
- Network policies for traffic isolation between namespaces

Namespace isolation is "soft" — pods from different namespaces share the same physical nodes.
This is intentional: it enables **bin-packing** (filling nodes efficiently), which reduces the
total number of nodes needed and therefore total cost.

---

## THE MATH

```
BEFORE: 5 pools × 2 VMs minimum × Standard_D4s_v5 ($0.192/hr)
      = 10 VMs × $0.192 × 24 hr × 30 days
      = $1,382/month

AFTER:  1 shared pool × 1 VM minimum (autoscaler handles the rest)
      = 1 VM × $0.192 × 24 hr × 30 days
      = $138/month (base) + burst during business hours

Dev clusters rarely need more than 2–3 nodes at peak during business hours.
Even accounting for burst: ~$350/month vs. $1,382/month.

Savings: ~$1,032/month (~75% reduction)
```

---

## HOW TO DO IT

### Step 1a: Audit Your Current Node Pools

```bash
# List all node pools with their min/max counts and VM sizes
az aks nodepool list \
  --resource-group <your-rg> \
  --cluster-name <your-cluster> \
  --output table

# Example output:
# Name       OsType    VmSize            Count    MinCount    MaxCount    Mode
# system     Linux     Standard_D2s_v5   2        2           2           System
# frontend   Linux     Standard_D4s_v5   2        2           4           User
# backend    Linux     Standard_D4s_v5   2        2           4           User
# database   Linux     Standard_D4s_v5   2        2           4           User
# mltasks    Linux     Standard_D4s_v5   2        2           4           User
```

### Step 1b: Check What's Actually Running in Each Pool

```bash
# See which pods are on which nodes (understand if pools are truly necessary)
kubectl get pods --all-namespaces -o wide

# Get current node utilization
kubectl top nodes

# See what labels/taints force pods to specific pools
kubectl get nodes --show-labels
kubectl describe node <node-name> | grep -A5 Taints
```

### Step 1c: Create a Single Shared User Node Pool

```bash
# Create the consolidated shared pool with autoscaling
az aks nodepool add \
  --resource-group <your-rg> \
  --cluster-name <your-cluster> \
  --name shareduser \
  --mode User \
  --node-vm-size Standard_D4s_v5 \
  --enable-cluster-autoscaler \
  --min-count 1 \      # Only 1 node minimum for Dev/Test!
  --max-count 5 \      # Allows burst up to 5 nodes when needed
  --node-count 1
```

### Step 1d: Create Namespaces for Each Team/Workload

```bash
# Create namespaces for each logical grouping
kubectl create namespace frontend
kubectl create namespace backend
kubectl create namespace database
kubectl create namespace ml-tasks
kubectl create namespace monitoring

# Label namespaces for cost tracking and policy targeting
kubectl label namespace frontend team=frontend environment=dev
kubectl label namespace backend team=backend environment=dev
kubectl label namespace database team=dba environment=dev
```

### Step 1e: Apply ResourceQuotas to Each Namespace

```yaml
# resource-quota-frontend.yaml
# Prevents any one team from consuming all shared resources
apiVersion: v1
kind: ResourceQuota
metadata:
  name: frontend-quota
  namespace: frontend
spec:
  hard:
    requests.cpu: "4"        # Max 4 CPU cores for this namespace
    requests.memory: "8Gi"   # Max 8 GB RAM
    limits.cpu: "8"
    limits.memory: "16Gi"
    pods: "20"               # Max 20 pods
```

```bash
# Apply the quota
kubectl apply -f resource-quota-frontend.yaml

# Verify
kubectl describe resourcequota frontend-quota -n frontend
```

### Step 1f: Enable Cluster Autoscaler with Aggressive Dev Settings

```bash
# Enable on shared pool (if not already done in Step 1c)
az aks nodepool update \
  --resource-group <your-rg> \
  --cluster-name <your-cluster> \
  --name shareduser \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5

# Tune autoscaler to be more aggressive about scaling down in Dev
# (Dev has no SLA, so fast scale-down is fine)
az aks update \
  --resource-group <your-rg> \
  --name <your-cluster> \
  --cluster-autoscaler-profile \
    scale-down-unneeded-time=5m \          # Remove unneeded nodes after 5 min (default: 10m)
    scale-down-delay-after-add=5m \
    scale-down-utilization-threshold=0.4   # Remove node if utilization < 40%
```

### Step 1g: Drain and Delete Old Node Pools (After Migration)

```bash
# ONLY after verifying all workloads run fine on the shared pool

# Cordon the old pool (prevent new pods scheduling there)
kubectl cordon <old-node-name>

# Drain pods gracefully (they reschedule to the new shared pool)
kubectl drain <old-node-name> \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=60

# Delete the old node pool
az aks nodepool delete \
  --resource-group <your-rg> \
  --cluster-name <your-cluster> \
  --name frontend \
  --no-wait

# Repeat for each pool being removed
```

---

## HOW TO CHECK

```bash
# Verify node count dropped
kubectl get nodes

# Verify pods still running in their namespaces
kubectl get pods --all-namespaces | grep -v Running | grep -v Completed

# Check autoscaler is working
kubectl get events -n kube-system | grep -i autoscal

# Check cluster autoscaler logs
kubectl logs -n kube-system -l app=cluster-autoscaler --tail=50
```

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| Some pools exist for a reason (GPU, Windows, Spot) | Keep specialized pools; only consolidate general-purpose ones |
| Pods with `nodeSelector` targeting old pools | Update pod specs to remove old selectors before deleting the pool |
| System pool cannot be consolidated | Always keep the System pool separate — it runs kube-system pods |
| Resource contention between teams on shared pool | Set ResourceQuotas per namespace to cap each team's allocation |

---

**Navigation:** [← Background Knowledge](00-basics.md) | [Index](index.md) | [Next: Step 2 — SKU Right-Sizing →](02-sku-right-sizing.md)
