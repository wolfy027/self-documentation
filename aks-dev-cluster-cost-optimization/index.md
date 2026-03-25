# AKS Dev Cluster Cost Optimization — 7-Step Practical Guide

> **Context:** This course covers the 7 optimization steps for Dev AKS clusters,
> targeting significant annual savings through infrastructure right-sizing and lifecycle management.
> Each step explains *why it saves money*, *how it works*, and *exactly how to implement it*.

---

## How to Read This Course

Each optimization step follows this structure:

```
THE PROBLEM   → What waste is happening and why
THE CONCEPT   → The Kubernetes / Azure concept that fixes it
THE MATH      → Exactly how much money it saves
HOW TO DO IT  → Step-by-step CLI commands and YAML
HOW TO CHECK  → How to verify the optimization is working
GOTCHAS       → What to watch out for
```

New to AKS or Kubernetes? Start with [Background Knowledge](00-basics.md) before diving into the steps.

---

## Course Contents

| File | Topic |
|---|---|
| [Background Knowledge](00-basics.md) | AKS & Kubernetes concepts you need to know |
| [Step 1 — Node Pool Consolidation](01-node-pool-consolidation.md) | Reduce idle VMs from multiple pools |
| [Step 2 — SKU Right-Sizing](02-sku-right-sizing.md) | Match VM size to actual workload |
| [Step 3 — Pod Requests & Limits](03-pod-requests-limits.md) | Stop reserving resources you don't use |
| [Step 4 — Replica Count = 1](04-replica-count.md) | Dev doesn't need HA replication |
| [Step 5 — UAT for Performance Testing](05-uat-for-performance-testing.md) | Keep load tests out of Dev |
| [Step 6 — PodDisruptionBudget](06-pod-disruption-budget.md) | Let the autoscaler consolidate nodes |
| [Step 7 — Automated Shutdown](07-automated-shutdown.md) | Stop paying for clusters nobody's using |
| [Cluster Audit Checklist](08-cluster-audit-checklist.md) | End-to-end checklist + expected savings |

---

## Expected Savings Per Step

| Step | Optimization | Monthly Savings (Per Cluster) |
|---|---|---|
| 1 | Node pool consolidation (5 pools → 1) | $800–$1,200 |
| 2 | VM SKU right-sizing (D8s → D2s, util < 20%) | $200–$600 |
| 3 | Pod request right-sizing (fewer nodes needed) | $200–$500 |
| 4 | Replica count 3→1 for 20 deployments | $150–$300 |
| 5 | Cap Dev resources (protects other savings) | $0 direct; enables Step 4 |
| 6 | Fix PDBs (enables autoscaler consolidation) | Unlocks Steps 1–4 savings |
| 7 | Automated shutdown (7pm–7am + weekends) | $200–$400 |
| **Total** | | **$1,550–$3,000/month per cluster** |


---

## Recommended Order of Implementation

Apply from **least to most disruptive**:

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

## Navigation

| | |
|---|---|
| Start here | [Background Knowledge →](00-basics.md) |
| Jump to checklist | [Cluster Audit Checklist →](08-cluster-audit-checklist.md) |
