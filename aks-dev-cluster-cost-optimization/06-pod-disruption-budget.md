# Step 6 — PodDisruptionBudget with minAvailable: 1

**Navigation:** [← Step 5 — UAT for Performance Testing](05-uat-for-performance-testing.md) | [Index](index.md) | [Next: Step 7 — Automated Shutdown →](07-automated-shutdown.md)

---

> **Rule:** Set PodDisruptionBudget (PDB) with `minAvailable: 1` for all pods.

---

## THE PROBLEM

**PodDisruptionBudgets (PDBs)** control how many pods can be simultaneously unavailable
during **voluntary disruptions** (node drains, cluster autoscaler scale-downs, upgrades).

Without correctly configured PDBs:

**Problem 1: Autoscaler cannot consolidate underutilized nodes**

When the Cluster Autoscaler tries to remove an underutilized node, it drains the pods.
If a pod has `minAvailable: 1` but is the ONLY replica, the autoscaler cannot drain it —
doing so would violate the PDB. The node stays, costs money, even though it's nearly idle.

**Problem 2: No PDB at all = unpredictable drain behavior**

The autoscaler may refuse to drain pods without a PDB (to be safe), OR it may drain too
aggressively. Either way, behavior is inconsistent.

**The correct setup for Dev:**
- `replicas: 1` + `maxUnavailable: 1` → autoscaler CAN drain (pod will be briefly down)
- `replicas: 2` + `minAvailable: 1` → autoscaler CAN drain (keeps 1 pod running)

---

## THE CONCEPT: PDB Controls the Autoscaler's Ability to Consolidate

```
Without PDB (or misconfigured PDB):
  Autoscaler → wants to drain node → unsure → leaves node running → wasted cost

With correct PDB (replicas=1, maxUnavailable=1):
  Autoscaler → checks PDB → "maxUnavailable: 1, OK to evict this single pod"
  → Drains pod → Node removed → Cost saved ✅

With incorrect PDB (replicas=1, minAvailable=1):
  Autoscaler → checks PDB → "must keep 1 available, but this IS the only one"
  → CANNOT drain → Node stays → Cost wasted ❌
```

---

## THE MATH

```
Scenario: 3-node cluster, 2 nodes running at 25% utilization
          (both are candidates for consolidation)

Without proper PDB: Autoscaler cannot drain → both nodes stay → $276/month wasted
With proper PDB:    Autoscaler drains freely → 2 nodes removed → $276/month saved

PDBs are the enabler that lets all other autoscaling optimizations actually work.
```

---

## HOW TO DO IT

### Step 6a: The Three PDB Patterns for Dev

**Pattern A: Single replica deployments (most Dev services)**
```yaml
# replicas: 1 → use maxUnavailable (autoscaler CAN take the pod down briefly)
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
  namespace: backend
spec:
  maxUnavailable: 1    # The pod can be briefly unavailable — acceptable in Dev
  selector:
    matchLabels:
      app: my-app
```

**Pattern B: Two-replica deployments**
```yaml
# replicas: 2 → keep at least 1 running during drain
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-app-pdb
  namespace: backend
spec:
  minAvailable: 1      # Keep 1 running while the other is drained
  selector:
    matchLabels:
      app: my-app
```

**Pattern C: Critical stateful services (use sparingly in Dev)**
```yaml
# replicas: 3 → tolerate losing 1 during maintenance
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: db-pdb
  namespace: database
spec:
  minAvailable: 2      # Keep quorum (2 of 3) running
  selector:
    matchLabels:
      app: my-database
```

### Step 6b: Bulk-Create PDBs for All Deployments in a Namespace

```bash
# Script to create the right PDB for each deployment based on its replica count
kubectl get deployment -n backend -o json | jq -r '.items[] | .metadata.name' | while read depname; do
  REPLICAS=$(kubectl get deployment $depname -n backend -o jsonpath='{.spec.replicas}')

  if [ "$REPLICAS" = "1" ]; then
    PDB_SPEC="maxUnavailable: 1"
  else
    PDB_SPEC="minAvailable: 1"
  fi

  kubectl apply -f - <<EOF
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: ${depname}-pdb
  namespace: backend
spec:
  selector:
    matchLabels:
      app: ${depname}
  ${PDB_SPEC}
EOF
  echo "Created PDB for $depname (replicas: $REPLICAS) using $PDB_SPEC"
done
```

### Step 6c: Find and Fix Blocking PDBs

```bash
# List all PDBs and check if any are blocking with 0 disruptions allowed
kubectl get pdb --all-namespaces

# Problematic output looks like:
# NAMESPACE  NAME         MIN AVAILABLE  MAX UNAVAILABLE  ALLOWED DISRUPTIONS
# backend    my-app-pdb   1              N/A              0          ← BLOCKED

# A PDB with 0 disruptions allowed + replicas=1 = autoscaler is permanently blocked

# Fix: change to maxUnavailable instead of minAvailable
kubectl patch pdb my-app-pdb -n backend --type='merge' -p '
{
  "spec": {
    "minAvailable": null,
    "maxUnavailable": 1
  }
}'
```

### Step 6d: Verify the Autoscaler Is No Longer Blocked

```bash
# Check for PDB-related blocks in autoscaler logs
kubectl logs -n kube-system -l app=cluster-autoscaler | grep -i "pdb\|disruption\|cannot evict"

# Healthy autoscaler logs look like:
# "Scale-down: node aks-nodepool-... removed"

# Blocked autoscaler logs look like:
# "cannot evict pod as it would violate the pod's disruption budget"
```

---

## HOW TO CHECK

```bash
# All PDBs should show ALLOWED DISRUPTIONS >= 1
kubectl get pdb --all-namespaces

# Watch the autoscaler start consolidating nodes after fixing PDBs
kubectl get events -n kube-system | grep ScaleDown
# Should see scale-down events within 5–15 minutes of nodes becoming underutilized

# Node count should drop
kubectl get nodes
```

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| PDB selector doesn't match pod labels → PDB has no effect | Check `kubectl describe pdb <name>` — `Disruptions Allowed` should be ≥ 1, not N/A |
| Deleting a PDB without replacing → autoscaler gets confused | Always replace, never just delete |
| PDB on StatefulSets during upgrades | StatefulSets need careful PDB tuning; consult docs for quorum-sensitive services |

---

**Navigation:** [← Step 5 — UAT for Performance Testing](05-uat-for-performance-testing.md) | [Index](index.md) | [Next: Step 7 — Automated Shutdown →](07-automated-shutdown.md)
