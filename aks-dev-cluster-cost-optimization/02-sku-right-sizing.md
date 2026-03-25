# Step 2 — Resource Utilization Review & SKU Right-Sizing

**Navigation:** [← Step 1 — Node Pool Consolidation](01-node-pool-consolidation.md) | [Index](index.md) | [Next: Step 3 — Pod Requests & Limits →](03-pod-requests-limits.md)

---

> **Rule:** Review resource utilization → if utilization is low, suggest switching
> to a more optimized (cheaper) SKU.

---

## THE PROBLEM

When you provision a node, you pay for its full vCPU and RAM — even if your workloads
only use 10% of it. This is **node-level overprovisioning**.

**Common scenario in Dev clusters:**
- `Standard_D8s_v5` nodes (8 vCPU, 32 GB RAM) were chosen for "production parity"
- Actual Dev workloads use 1–2 vCPU and 4–6 GB RAM at peak
- Result: paying 4–8× more than necessary

**VM SKU Pricing Reference (East US, Linux, approximate):**

| VM Size | vCPU | RAM | Price/hr | Price/month |
|---|---|---|---|---|
| Standard_B2s | 2 | 4 GB | ~$0.042 | ~$30 |
| Standard_D2s_v5 | 2 | 8 GB | ~$0.096 | ~$69 |
| Standard_D4s_v5 | 4 | 16 GB | ~$0.192 | ~$138 |
| Standard_D8s_v5 | 8 | 32 GB | ~$0.384 | ~$276 |
| Standard_D16s_v5 | 16 | 64 GB | ~$0.768 | ~$554 |

> 3× `Standard_D8s_v5` → 3× `Standard_D2s_v5` = saving **$621/month per cluster**
> if actual utilization shows < 1.5 vCPU per node.

---

## THE CONCEPT: Measure First, Downsize Second

**Never guess.** Always measure actual utilization before recommending a smaller SKU.

**Key Metric: Node Utilization Ratio**

```
Node Utilization = (Actual CPU Used) / (Allocatable CPU on that node)

Example:
  Node: 8 vCPU — Kubernetes reserves 0.5 vCPU for system = 7.5 allocatable
  Workloads using: 1.2 vCPU actual
  Utilization = 1.2 / 7.5 = 16%   ← massively underutilized
```

**Decision Rule:**
- Utilization < 30% consistently → downsize the SKU
- Utilization 30–70% → SKU is appropriate
- Utilization > 70% → might need to stay or upsize (rare in Dev)

---

## THE MATH

```
BEFORE: 3× Standard_D8s_v5 = 3 × $0.384/hr × 720 hr = $829/month
        (average utilization: 20%)

AFTER:  3× Standard_D2s_v5 = 3 × $0.096/hr × 720 hr = $207/month

Savings: $622/month per cluster (75% reduction)
```

---

## HOW TO DO IT

### Step 2a: Check Node Utilization Right Now

```bash
# Real-time node CPU and memory usage
kubectl top nodes

# Example output:
# NAME                          CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
# aks-nodepool-12345-vmss0      312m         7%     2341Mi          18%
# aks-nodepool-12345-vmss1      198m         4%     1876Mi          14%
# aks-nodepool-12345-vmss2      445m         11%    3102Mi          24%

# 7%, 4%, 11% CPU → SEVERELY underutilized → strong candidate for smaller SKU

# Detailed breakdown on a specific node
kubectl describe node <node-name>
# Scroll to "Allocated resources":
#   Resource    Requests    Limits
#   cpu         950m (23%)  2000m (50%)
#   memory      1900Mi (14%) 4000Mi (31%)
```

### Step 2b: Check Historical Utilization in Azure Portal

1. Open your AKS cluster in the Azure Portal
2. Go to **Monitoring → Insights → Nodes tab**
3. Set time range to **Last 7 days**
4. Look at **CPU Utilization %** and **Memory Working Set %** columns
5. If p95 utilization is below 30%, the node SKU is oversized

### Step 2c: Enable VPA in Off Mode to See What Pods Actually Need

```bash
# Enable VPA add-on
az aks update \
  --resource-group <your-rg> \
  --name <your-cluster> \
  --enable-vpa
```

```yaml
# vpa-observe.yaml
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: my-app-vpa
  namespace: backend
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: my-app            # ← change to your deployment name
  updatePolicy:
    updateMode: "Off"       # Observe only — does NOT change anything
```

```bash
kubectl apply -f vpa-observe.yaml

# After 24–48 hours, read the recommendations
kubectl describe vpa my-app-vpa -n backend

# Output:
# Status:
#   Recommendation:
#     Container Recommendations:
#     - Container Name: my-app
#       Target:           ← USE THESE VALUES to right-size
#         cpu: 80m        ← pod only needs 80 millicores!
#         memory: 210Mi   ← pod only needs 210 MB RAM!
```

### Step 2d: Determine the Right New SKU

```
Step 1: Sum actual needs for all pods (from VPA Target values)
Step 2: Add 20–30% headroom for spikes
Step 3: Add Kubernetes system reservation (~500m CPU, ~1 GB RAM per node)
Step 4: Pick the smallest VM that fits comfortably

Example:
  All pods on a node need: 600m CPU, 3 GB RAM (from VPA data)
  + 25% headroom:          750m CPU, 3.75 GB RAM
  + System reserve:        1250m CPU, 4.75 GB RAM

  Best fit: Standard_D2s_v5 (2 vCPU = 2000m, 8 GB)  ← Fits with headroom
  Previous: Standard_D8s_v5 (8 vCPU = 8000m, 32 GB)
  Savings: 75% reduction in per-node cost
```

### Step 2e: Migrate to the Right-Sized Node Pool

> You cannot change a node pool's VM size in-place. Create a new pool, migrate, delete the old.

```bash
# 1. Create new pool with right-sized VM
az aks nodepool add \
  --resource-group <your-rg> \
  --cluster-name <your-cluster> \
  --name rightsized \
  --node-vm-size Standard_D2s_v5 \    # ← new correct size
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5 \
  --node-count 1

# 2. Cordon the old oversized nodes (stop new scheduling)
kubectl cordon <old-large-node-name>

# 3. Drain pods (they move to the new right-sized pool)
kubectl drain <old-large-node-name> \
  --ignore-daemonsets \
  --delete-emptydir-data \
  --grace-period=60

# 4. Verify everything runs on the new pool
kubectl get pods --all-namespaces -o wide | grep rightsized

# 5. Delete the old pool
az aks nodepool delete \
  --resource-group <your-rg> \
  --cluster-name <your-cluster> \
  --name <old-oversized-pool-name>
```

---

## HOW TO CHECK

```bash
# After migration — node utilization should be healthier (30–60%)
kubectl top nodes

# Check no pods are in Pending state (would mean new node is too small)
kubectl get pods --all-namespaces | grep Pending
# Should return nothing
```

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| New SKU too small → pods go Pending | Start with 1 new node and watch for Pending pods before draining the old pool |
| Memory-intensive apps OOM-killed on smaller nodes | Check memory requests carefully; may need E-series (memory-optimized) |
| SKU not available in target region | Check `az vm list-skus --location <region>` first |
| B-series throttled under sustained load | B-series is fine for burst Dev workloads; avoid for sustained CPU |

---

**Navigation:** [← Step 1 — Node Pool Consolidation](01-node-pool-consolidation.md) | [Index](index.md) | [Next: Step 3 — Pod Requests & Limits →](03-pod-requests-limits.md)
