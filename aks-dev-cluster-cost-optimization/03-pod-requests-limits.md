# Step 3 — Pod Requests & Limits Tuning

**Navigation:** [← Step 2 — SKU Right-Sizing](02-sku-right-sizing.md) | [Index](index.md) | [Next: Step 4 — Replica Count →](04-replica-count.md)

---

> **Rule:** Assess pod utilization → adjust requests and limits accordingly.

---

## THE PROBLEM

**Resource Requests** are the CPU/memory the scheduler reserves on a node for a pod.
Even if the pod uses zero resources, the reserved amount is unavailable for other pods.

**Why this wastes money:**

```
Node: 4 vCPU, 16 GB RAM

Pod A: requests 2 vCPU, 8 GB  → actual usage: 200m CPU, 512 MB RAM
Pod B: requests 2 vCPU, 8 GB  → actual usage: 300m CPU, 1 GB RAM

Node appears: FULL (4/4 vCPU reserved, 16/16 GB reserved)
Actual usage:  12.5% CPU, 9.4% RAM

→ Kubernetes won't schedule new pods on this "full" node
→ Cluster Autoscaler provisions a new node
→ You're paying for 2 nodes but using 12% of one
```

**Overprovisioned requests are the #1 cause of unnecessary node scaling.**

---

## THE CONCEPT: Requests vs. Limits vs. Actual Usage

```
┌─────────────────────────────────────────────────────────────────┐
│  LIMIT (hard ceiling — pod is throttled/killed if exceeded)     │
│  ─────────────────────────────────────────────────────────────  │
│       REQUEST (reserved on the node — affects scheduling)       │
│       ───────────────────────────────────────────────────       │
│            ACTUAL USAGE (what the pod truly consumes)           │
└─────────────────────────────────────────────────────────────────┘

Ideal: REQUEST ≈ p95 actual usage + 20% headroom
       LIMIT   = 2–4× REQUEST (allows short bursts without hogging the node)
```

**Kubernetes QoS Classes (relevant for understanding eviction behavior):**

| Class | Condition | What It Means |
|---|---|---|
| **Guaranteed** | request == limit for all containers | Safest; evicted last |
| **Burstable** | request < limit | Good for Dev; efficient bin-packing |
| **BestEffort** | No requests or limits at all | Dangerous; evicted first |

For Dev/Test: **Burstable** is the right class. Low requests enable efficient bin-packing;
reasonable limits prevent one pod from consuming the entire node.

---

## THE MATH

```
Pod currently has:  request = 1000m CPU, 2Gi RAM
VPA recommends:     request = 100m CPU,  256Mi RAM

Wasted reserved capacity per pod: 900m CPU, 1.8Gi RAM

With 30 pods showing the same pattern:
  Wasted CPU: 30 × 900m = 27,000m = 27 vCPU
  Wasted RAM: 30 × 1.8Gi = 54 GB

  27 wasted vCPU ≈ 7 Standard_D4s_v5 nodes you don't actually need
  7 nodes × $138/month = $966/month wasted on over-requests alone
```

---

## HOW TO DO IT

### Step 3a: Find Pods with the Highest Over-Request Gap

```bash
# See actual resource usage for all pods
kubectl top pods --all-namespaces --sort-by=cpu

# Compare against what they've requested
kubectl get pods --all-namespaces -o json | jq -r '
  .items[] |
  .metadata.namespace + "/" + .metadata.name + "  →  " +
  "CPU request: " + (.spec.containers[0].resources.requests.cpu // "NONE") +
  ", Memory request: " + (.spec.containers[0].resources.requests.memory // "NONE")
'
```

### Step 3b: Deploy VPA in Off Mode for All Deployments

```bash
# Generate VPA observer objects for all Deployments in a namespace
kubectl get deployment -n backend -o name | while read dep; do
  DEPNAME=$(echo $dep | cut -d/ -f2)
  kubectl apply -f - <<EOF
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: ${DEPNAME}-vpa
  namespace: backend
spec:
  targetRef:
    apiVersion: "apps/v1"
    kind: Deployment
    name: ${DEPNAME}
  updatePolicy:
    updateMode: "Off"
EOF
done

# Wait 24–48 hours for data, then read ALL recommendations at once
kubectl get vpa -n backend -o json | jq -r '
  .items[] |
  "=== " + .metadata.name + " ===" ,
  "  target CPU:    " + (.status.recommendation.containerRecommendations[0].target.cpu // "N/A"),
  "  target Memory: " + (.status.recommendation.containerRecommendations[0].target.memory // "N/A")
'
```

### Step 3c: Update Deployment Resource Requests/Limits

```yaml
# BEFORE (over-provisioned — common copy-paste from production):
resources:
  requests:
    cpu: "1000m"
    memory: "2Gi"
  limits:
    cpu: "2000m"
    memory: "4Gi"

# AFTER (right-sized — VPA recommended 80m CPU, 200Mi RAM):
resources:
  requests:
    cpu: "100m"     # actual p95 usage is 80m + 25% headroom
    memory: "256Mi" # actual p95 usage is 200Mi + ~30% headroom
  limits:
    cpu: "500m"     # Allow bursting to 5× request without blocking scheduling
    memory: "512Mi" # Hard memory cap — pod is OOM-killed if it exceeds this
```

```bash
# Apply patch directly without modifying YAML files:
kubectl patch deployment my-app -n backend --patch '
{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "my-app",
          "resources": {
            "requests": {"cpu": "100m", "memory": "256Mi"},
            "limits":   {"cpu": "500m", "memory": "512Mi"}
          }
        }]
      }
    }
  }
}'
```

### Step 3d: Apply LimitRange — Enforce Sane Defaults for All Future Pods

This ensures new pods deployed without explicit resource specs get sensible defaults
instead of unlimited consumption:

```yaml
# limitrange-dev-defaults.yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-resource-defaults
  namespace: backend
spec:
  limits:
  - type: Container
    default:            # Applied when no limits are specified
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:     # Applied when no requests are specified
      cpu: "100m"
      memory: "128Mi"
    max:                # No container can ever exceed these
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "10m"
      memory: "16Mi"
```

```bash
# Apply to all Dev namespaces at once
for ns in frontend backend database ml-tasks monitoring; do
  kubectl apply -f - <<EOF
apiVersion: v1
kind: LimitRange
metadata:
  name: dev-resource-defaults
  namespace: ${ns}
spec:
  limits:
  - type: Container
    default:
      cpu: "500m"
      memory: "512Mi"
    defaultRequest:
      cpu: "100m"
      memory: "128Mi"
    max:
      cpu: "4"
      memory: "8Gi"
    min:
      cpu: "10m"
      memory: "16Mi"
EOF
done
```

---

## HOW TO CHECK

```bash
# Verify pod resource usage is close to requests (healthy = requests ≈ actual usage)
kubectl top pods -n backend

# Check nodes are now more efficiently utilized
kubectl top nodes
# Target: 40–70% utilization (vs. the 10–20% from over-requests)

# Check for OOM events (if memory limits were set too low)
kubectl get events --all-namespaces | grep -i OOMKilled
kubectl get events --all-namespaces | grep -i oom
```

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| Pod OOM-killed after reducing memory limit | Set limit to at least 1.5× VPA upper bound; watch events for `OOMKilled` |
| CPU throttling after reducing CPU limit | In Dev, set no CPU limit rather than a wrong one — throttling causes latency spikes |
| VPA in Auto mode conflicts with HPA | Never run VPA Auto + HPA on the same CPU/memory metrics — they fight each other |
| JVM apps (Java) show misleading VPA numbers | JVM pre-allocates heap; set memory request = JVM heap size + 200 MB overhead |

---

**Navigation:** [← Step 2 — SKU Right-Sizing](02-sku-right-sizing.md) | [Index](index.md) | [Next: Step 4 — Replica Count →](04-replica-count.md)
