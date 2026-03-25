# Step 5 — Use UAT for Performance Testing, Not Dev/Test

**Navigation:** [← Step 4 — Replica Count](04-replica-count.md) | [Index](index.md) | [Next: Step 6 — PodDisruptionBudget →](06-pod-disruption-budget.md)

---

> **Rule:** For performance testing with high load, use UAT; more than one replica is
> not required for Dev/Test.

---

## THE PROBLEM

Load tests are resource-hungry by design. Running them in Dev causes:

1. **Artificial and expensive node scaling** — Cluster Autoscaler adds nodes for the test,
   then removes them shortly after. You pay for nodes that ran for 1–2 hours.
2. **Disruption for developers** — the load test consumes all available CPU/RAM, making
   the shared Dev cluster unusable for others during the test window.
3. **Corrupts your baseline cost data** — Dev cluster costs spike during tests, making
   it impossible to accurately measure optimization progress.
4. **Misleading right-sizing decisions** — if you analyze node needs after a load test,
   you'll over-provision based on test peaks rather than real Dev usage.

---

## THE CONCEPT: Environment Segmentation by Purpose

```
DEV     → Individual developer work, code iteration
          Resources: Small (1–2 nodes), ephemeral
          No SLA. Can be down.

TEST    → Automated integration tests, CI/CD validation
          Resources: Small, runs briefly per pipeline trigger
          No SLA. Expected to start/stop.

UAT     → User acceptance testing, performance testing
          Resources: Production-like (enough to simulate real load)
          Soft SLA. Should be stable during test windows.

PROD    → Real user traffic
          Resources: Full HA, autoscaling, monitoring
          Hard SLA. Zero tolerance for downtime.
```

UAT already has production-like resources — making it the right place for load testing.
Performance test results are also **more accurate in UAT** because the environment more
closely mirrors production.

---

## THE MATH

```
Load test scenario: 2-hour test that scales Dev cluster from 2 to 8 nodes

6 extra nodes × Standard_D4s_v5 ($0.192/hr) × 2 hr = $2.30 per test run
20 test runs/month: $2.30 × 20 = $46/month wasted per cluster
```

---

## HOW TO DO IT

### Step 5a: Cap Dev Namespace Resources to Make Load Tests Structurally Impossible

Apply tight ResourceQuotas so a load test cannot spin up enough workers to be meaningful:

```yaml
# resource-quota-dev-cap.yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: dev-hard-cap
  namespace: backend
spec:
  hard:
    requests.cpu: "2"          # Max 2 vCPU — load test workers would exhaust this instantly
    requests.memory: "4Gi"     # Max 4 GB RAM across the entire namespace
    pods: "10"                 # Max 10 pods — prevents spinning up 50 load test workers
```

When a load test tries to add 50 worker pods, it gets rejected:
```
Error: pods "load-test-worker-6" is forbidden: exceeded quota: dev-hard-cap
```
This is the right outcome — it naturally redirects the engineer to use UAT.

### Step 5b: Size UAT to Handle Load Tests with Autoscaling

```bash
# UAT cluster: small normally, scales up during load test windows, scales back down after
az aks nodepool update \
  --resource-group <uat-rg> \
  --cluster-name <uat-cluster> \
  --name userpool \
  --enable-cluster-autoscaler \
  --min-count 2 \          # Stays at 2 nodes normally
  --max-count 10           # Scales up for load tests, scales back down after

# Tune autoscaler to scale down quickly after tests complete
az aks update \
  --resource-group <uat-rg> \
  --name <uat-cluster> \
  --cluster-autoscaler-profile \
    scale-down-unneeded-time=10m \
    scale-down-delay-after-add=5m
```

### Step 5c: Document and Communicate the Policy

```markdown
## Performance Testing Policy

ALL load tests, stress tests, and performance benchmarks MUST be run
in the UAT environment — not in Dev or Test clusters.

Why:
  Dev clusters are sized for developer iteration (1–2 nodes).
  Load tests cause the Cluster Autoscaler to spin up extra nodes,
  increasing costs and disrupting other developers on the shared cluster.

How to run a load test in UAT:
  1. Deploy your app to UAT: helm upgrade ... -f values-uat.yaml
  2. Run your load test (k6, Locust, JMeter, etc.)
  3. UAT autoscales during the test and scales back down within ~15 minutes
  4. Clean up: helm uninstall <your-release> -n <namespace>

Need an exception?
  Contact the platform team. Temporary Dev quota increases can be arranged
  for a time-boxed window.
```

---

## HOW TO CHECK

```bash
# Dev cluster node count should stay flat — no spikes from load tests
watch kubectl get nodes

# If nodes are scaling up unexpectedly, check what caused it
kubectl get events -n kube-system | grep -i "ScaleUp"

# Check if any namespace is near its quota limit
kubectl describe resourcequota dev-hard-cap -n backend
```

---

## GOTCHAS

| Risk | Mitigation |
|---|---|
| Engineers bypass policy by manually scaling quotas | Apply RBAC to prevent namespace quota modifications without platform team approval |
| UAT not sized appropriately → load test results are wrong | UAT node pool should match production node SKU; difference in count is OK since autoscaler handles it |
| CI/CD integration tests mistaken for load tests | Keep CI/CD test runs short (<5 min); true load tests run for 30+ min — easy to distinguish |

---

**Navigation:** [← Step 4 — Replica Count](04-replica-count.md) | [Index](index.md) | [Next: Step 6 — PodDisruptionBudget →](06-pod-disruption-budget.md)
