# Background Knowledge — AKS & Kubernetes Concepts

**Navigation:** [Index](index.md) | [Next: Step 1 — Node Pool Consolidation →](01-node-pool-consolidation.md)

---

This file explains the core concepts you need to understand before working through the
optimization steps. If you're already familiar with AKS and Kubernetes resource management,
skip to [Step 1](01-node-pool-consolidation.md).

---

## What is AKS?

**Azure Kubernetes Service (AKS)** is Microsoft Azure's managed Kubernetes offering.
It handles the Kubernetes control plane (the management layer) for you — you only pay for
and manage the **worker nodes** (the VMs that run your actual workloads).

```
AKS Cluster
├── Control Plane (managed by Azure — free on Basic tier)
│   ├── API Server
│   ├── etcd (cluster state database)
│   └── Scheduler / Controller Manager
│
└── Node Pools (your VMs — you pay for these)
    ├── System Pool (runs kube-system pods)
    └── User Pool(s) (runs your application pods)
```

---

## Node Pools and VMSS

A **node pool** is a group of VMs (Virtual Machines) in AKS. Each pool uses an
**Azure Virtual Machine Scale Set (VMSS)** — a group of identically sized VMs that
scale together.

Key facts:
- Every node pool has a **minimum node count** — VMs that run 24/7 regardless of load
- Each node reserves ~0.5 vCPU and ~1 GB RAM for Kubernetes system overhead
- You pay for all VMs in a pool, even if they're idle

**VM SKU** (Stock-Keeping Unit) is the Azure VM type. Common ones in AKS:

| SKU | vCPU | RAM | ~Price/hr | ~Price/month |
|---|---|---|---|---|
| Standard_B2s | 2 | 4 GB | $0.042 | $30 |
| Standard_D2s_v5 | 2 | 8 GB | $0.096 | $69 |
| Standard_D4s_v5 | 4 | 16 GB | $0.192 | $138 |
| Standard_D8s_v5 | 8 | 32 GB | $0.384 | $276 |

---

## Kubernetes Namespaces

A **namespace** is a virtual partition inside a Kubernetes cluster. Think of it like a
folder — it groups related resources and lets you apply policies (quotas, access control)
to a specific team or workload.

```bash
# Create a namespace
kubectl create namespace backend

# List all namespaces
kubectl get namespaces

# Run commands scoped to a namespace
kubectl get pods -n backend
kubectl get deployments -n backend
```

Namespaces provide **soft isolation** — pods from different namespaces can share the
same physical nodes. This enables efficient bin-packing (filling nodes to capacity).

---

## Pods and Deployments

A **Pod** is the smallest deployable unit in Kubernetes — it wraps one or more containers.

A **Deployment** manages a set of identical pods. It ensures the desired number of
replicas is always running and handles rolling updates.

```yaml
# Minimal deployment example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
  namespace: backend
spec:
  replicas: 1         # How many pod copies to run
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: my-app
        image: my-image:latest
        resources:
          requests:
            cpu: "100m"
            memory: "128Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
```

---

## Resource Requests and Limits

Every container in Kubernetes can (and should) specify:

- **`requests`** — the CPU/memory the Kubernetes scheduler reserves on a node for this
  container. This affects which nodes the pod can be placed on.
- **`limits`** — the maximum CPU/memory the container can use. If it exceeds the memory
  limit, it is killed (OOMKilled). If it exceeds the CPU limit, it is throttled.

```
CPU units:
  "1"    = 1 vCPU core
  "500m" = 500 millicores = 0.5 vCPU
  "100m" = 100 millicores = 0.1 vCPU

Memory units:
  "1Gi"  = 1 gibibyte = 1,073,741,824 bytes
  "512Mi" = 512 mebibytes
  "128Mi" = 128 mebibytes
```

**Why requests matter for cost:** The scheduler treats reserved resources as used,
even if the actual usage is much lower. Over-requesting causes artificial node fullness,
triggering the cluster autoscaler to add new (costly) nodes unnecessarily.

---

## Cluster Autoscaler

The **Cluster Autoscaler** automatically adjusts the number of nodes in a pool:

- **Scale UP:** When pods cannot be scheduled (insufficient resources), it adds nodes
- **Scale DOWN:** When nodes are underutilized for a sustained period (configurable),
  it drains and removes them

```bash
# Enable cluster autoscaler on a node pool
az aks nodepool update \
  --resource-group <rg> \
  --cluster-name <cluster> \
  --name <pool-name> \
  --enable-cluster-autoscaler \
  --min-count 1 \
  --max-count 5
```

**Key autoscaler settings for Dev clusters:**

| Setting | Default | Dev Recommendation | Meaning |
|---|---|---|---|
| `scale-down-unneeded-time` | 10m | 5m | How long a node must be unneeded before removal |
| `scale-down-utilization-threshold` | 0.5 | 0.4 | Remove nodes below this utilization |
| `scale-down-delay-after-add` | 10m | 5m | Wait after scale-up before considering scale-down |

---

## HPA — Horizontal Pod Autoscaler

**HPA** automatically adjusts the number of pod replicas based on metrics (CPU, memory,
custom). In Dev, HPA is useful to allow brief scale-up from 1 to 2 replicas during spikes,
while staying at the efficient minimum at rest.

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: my-app-hpa
  namespace: backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: my-app
  minReplicas: 1     # Always stay at 1 in Dev
  maxReplicas: 2     # Allow brief burst to 2
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80
```

---

## VPA — Vertical Pod Autoscaler

**VPA** observes actual pod resource usage over time and recommends (or automatically
applies) better `requests` and `limits` values.

Modes:
- **`Off`** — Observe only; outputs recommendations, changes nothing (use this first)
- **`Auto`** — Automatically updates pods with recommended values (use with caution)

```bash
# Enable VPA add-on in AKS
az aks update --resource-group <rg> --name <cluster> --enable-vpa

# Read VPA recommendations after 24-48 hours of observation
kubectl describe vpa my-app-vpa -n backend
```

> **Warning:** Never run VPA in `Auto` mode on the same deployment as HPA using CPU/memory
> metrics — they will conflict with each other.

---

## ResourceQuota

A **ResourceQuota** sets hard limits on the total resources a namespace can consume.
It prevents any one team or test run from consuming all shared cluster resources.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: backend-quota
  namespace: backend
spec:
  hard:
    requests.cpu: "4"        # Max 4 CPU cores reserved across all pods
    requests.memory: "8Gi"   # Max 8 GB RAM reserved
    limits.cpu: "8"
    limits.memory: "16Gi"
    pods: "20"               # Max 20 pods in this namespace
```

---

## LimitRange

A **LimitRange** sets default `requests` and `limits` for containers in a namespace
that don't specify them. It also enforces min/max bounds.

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-defaults
  namespace: backend
spec:
  limits:
  - type: Container
    default:            # Applied when no limits specified
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:     # Applied when no requests specified
      cpu: "100m"
      memory: "128Mi"
    max:                # Hard ceiling — container cannot request more
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "10m"
      memory: "16Mi"
```

---

## PodDisruptionBudget (PDB)

A **PDB** controls how many pods of a deployment can be simultaneously unavailable
during **voluntary disruptions** (node drains, cluster autoscaler scale-downs, upgrades).

Two modes:
- **`minAvailable: N`** — at least N pods must stay running. If only N exist, nothing can be drained.
- **`maxUnavailable: N`** — at most N pods may be unavailable at once. Allows draining even single-replica deployments.

**The critical insight for Dev:** With `replicas: 1` and `minAvailable: 1`, the autoscaler
can never drain the pod — the node stays running forever. Use `maxUnavailable: 1` instead.

---

## AKS Cluster Start/Stop

AKS supports stopping and starting the entire cluster:

```bash
# Stop all node VMs — compute charges stop immediately
az aks stop --resource-group <rg> --name <cluster>

# Start them back up — Kubernetes state is preserved in etcd
az aks start --resource-group <rg> --name <cluster>
```

What's preserved while stopped: all Kubernetes objects (Deployments, Services, Secrets, PVCs)
What stops billing: VM compute costs
What still bills: Managed disks (PVCs), static IPs, Log Analytics retention

---

**Navigation:** [Index](index.md) | [Next: Step 1 — Node Pool Consolidation →](01-node-pool-consolidation.md)
