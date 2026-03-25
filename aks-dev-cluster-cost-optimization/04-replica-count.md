# Step 4 — Replica Count = 1 for Dev/Test (Max 2)

**Navigation:** [← Step 3 — Pod Requests & Limits](03-pod-requests-limits.md) | [Index](index.md) | [Next: Step 5 — UAT for Performance Testing →](05-uat-for-performance-testing.md)

---

> **Rule:** Set replica count to 1 for Dev and Test environments (max 2 if required).

---

## THE PROBLEM

Production manifests are often copy-pasted into Dev with `replicas: 3` or `replicas: 5`.
In production, multiple replicas serve High Availability and scalability. In Dev:

- **No HA is needed** — developers expect occasional downtime
- **No horizontal scale needed** — no real user traffic
- **Every extra replica consumes node capacity** or triggers new nodes to be provisioned

**The compounding effect:**

```
15 microservices × 3 replicas = 45 pods
15 microservices × 1 replica  = 15 pods

At 200m CPU / 256Mi RAM requested per pod:
  45 pods = 9,000m CPU reserved = needs ~3 Standard_D4s_v5 nodes
  15 pods = 3,000m CPU reserved = needs ~1 Standard_D4s_v5 node

Cost: 3 nodes vs 1 node = 2 saved nodes = $276/month per cluster
Across 15 Dev clusters: 15 × $276 = $4,140/month = $49,680/year
```

---

## THE CONCEPT: Match Reliability to Environment Requirements

```
Production:    replicas: 3+   (HA required — customers using it)
Staging/UAT:   replicas: 2    (mirror production closely for pre-prod testing)
Dev:           replicas: 1    (used by individual developer, HA not needed)
Test (CI/CD):  replicas: 1    (automated tests only, no real users)
```

Setting `replicas: 1` in Dev does not reduce product quality — it matches infrastructure
to actual requirements.

---

## THE MATH

```
BEFORE: 20 Deployments × avg 3 replicas × 200m CPU request = 12,000m = 12 vCPU reserved
AFTER:  20 Deployments × 1 replica × 200m CPU request = 4,000m = 4 vCPU reserved

8 vCPU freed → ~2 fewer Standard_D4s_v5 nodes needed
Savings: 2 × $138/month = $276/month per cluster
```

---

## HOW TO DO IT

### Step 4a: Find All Deployments with Replicas > 1

```bash
# List all deployments and their replica counts, sorted by count
kubectl get deployments --all-namespaces \
  -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name,REPLICAS:.spec.replicas" \
  | sort -k3 -rn

# Show only those with > 1 replica
kubectl get deployments --all-namespaces -o json | jq -r '
  .items[] |
  select(.spec.replicas > 1) |
  .metadata.namespace + "/" + .metadata.name + ": " + (.spec.replicas | tostring) + " replicas"
'
```

### Step 4b: Scale Down to 1 Replica

```bash
# Scale a specific deployment
kubectl scale deployment my-api -n backend --replicas=1

# Scale ALL deployments in a namespace at once
kubectl get deployment -n backend -o name | \
  xargs -I{} kubectl scale {} --replicas=1 -n backend

# Scale all deployments across all user namespaces (Dev cluster only!)
for ns in $(kubectl get ns -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' \
  | grep -v kube-system | grep -v kube-public | grep -v kube-node-lease); do
  kubectl get deployment -n $ns -o name | \
    xargs -I{} kubectl scale {} --replicas=1 -n $ns 2>/dev/null
done

echo "Done. Verify with: kubectl get deployments --all-namespaces"
```

### Step 4c: Prevent Replica Drift via CI/CD Values File

If services are deployed via Helm, create environment-specific override values:

```yaml
# values-dev.yaml (environment override file)
replicaCount: 1       # Override production's replicaCount: 3

autoscaling:
  enabled: true
  minReplicas: 1
  maxReplicas: 2      # Allow brief scale-up to 2 max
  targetCPUUtilizationPercentage: 80

resources:
  requests:
    cpu: 100m         # Dev-specific lighter requests
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

```bash
# Deploy with dev-specific values (they override production values)
helm upgrade my-app ./charts/my-app \
  -f values.yaml \
  -f values-dev.yaml \   # Dev values win for any overlapping keys
  --namespace backend
```

### Step 4d: Add HPA to Allow Temporary Scale-Up When Needed

```yaml
# hpa-dev-app.yaml
# Keeps at 1 replica normally, allows brief scale to 2 for temporary spikes
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
  minReplicas: 1     # Cost-efficient baseline
  maxReplicas: 2     # Cap at 2 per the optimization rule
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 80   # Only scale when CPU > 80%
```

---

## HOW TO CHECK

```bash
# Verify all deployments are at 1 replica
kubectl get deployments --all-namespaces \
  -o custom-columns="NS:.metadata.namespace,NAME:.metadata.name,DESIRED:.spec.replicas,READY:.status.readyReplicas"

# Check pods are healthy
kubectl get pods --all-namespaces | grep -v Running | grep -v Completed
# Should return nothing

# Check node count has reduced as a result
kubectl get nodes
```

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| CI/CD pipeline resets replicas to 3 on next deployment | Update `values-dev.yaml` in the pipeline configuration |
| StatefulSets (e.g., databases) — do NOT blindly set to 1 | Only reduce replicas on stateless Deployments; check with the service owner first for StatefulSets |
| Services with strict PDBs blocking scale-down | Review PDBs before scaling (Step 6 addresses this) |

---

**Navigation:** [← Step 3 — Pod Requests & Limits](03-pod-requests-limits.md) | [Index](index.md) | [Next: Step 5 — UAT for Performance Testing →](05-uat-for-performance-testing.md)
