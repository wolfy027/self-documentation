---
name: azure-storage-account-optimization
description: Use when auditing Azure storage accounts for cost waste, tier mismatches, redundancy overprovisioning, missing lifecycle policies, Smart Tier opt-in, TLS/public-access security baseline, paid-feature overspend (SFTP), versioning storage inflation, reserved-capacity opportunities, or identifying orphaned accounts. Triggers on requests to optimize storage costs, review storage account configuration, or run a subscription-wide storage audit. Requires az login before use.
---

# Azure Storage Account Optimization

Produces a single comprehensive **markdown status + recommendations report** for one storage account or every account in a subscription. Covers tier (incl. Smart Tier — April 2026 GA), redundancy, lifecycle, versioning, Last Access Time, security baseline (TLS 1.2, anonymous access, cross-tenant replication), paid features (SFTP, NFS v3), reserved-capacity opportunities, and orphan detection. Requires only `az login` — no service principal or managed identity. Platform-neutral (agentskills.io spec).

## Read-Only Guarantee

**This skill never modifies Azure resources.** All SDK calls are read-only:

| Operation | API | Type |
|---|---|---|
| List/get storage accounts | `storage_accounts.list()`, `.get_properties()` | read |
| Read blob service settings | `blob_services.get_service_properties()` | read |
| Read lifecycle policy | `management_policies.get()` | read |
| Read metrics | `MetricsQueryClient.query_resource()` | read |
| Resolve subscription | `az account show --query id -o tsv` | read |

No `create_or_update`, `update`, `delete`, or `begin_*` calls exist in the scripts. The skill produces a markdown report containing **recommendations only** — applying any change is left to the user, who can review the report and execute changes via Portal, CLI, IaC, or another tool of their choosing. Safe to run against production subscriptions with a read-only Azure RBAC role (e.g. `Reader` or `Storage Account Contributor` with no changes).

## Prerequisites

```bash
az login
pip install azure-identity azure-mgmt-storage azure-monitor-query
```

The minimum Azure RBAC role needed is **`Reader`** on the subscription, plus **`Monitoring Reader`** for the metrics queries. No write permissions required.

Confirm the active subscription before collecting:
```bash
az account show --query '{id:id, name:name}' -o json
```

## How to Invoke This Skill

| Intent | Prompt to use |
|---|---|
| All accounts, default subscription | "Audit all storage accounts" |
| All accounts, specific subscription | "Audit all storage accounts in subscription `<sub-id>`" |
| Single account | "Optimize storage account `<name>` in resource group `<rg>`" |
| From pre-collected JSON | "Build the report from this inventory: `<path>`" |

Full prompt templates (with anatomy, anti-patterns, and end-user phrasing): **`prompt.md`**

If the subscription or account is ambiguous, run `az account show` and confirm before collecting.

## The Workflow (one markdown out)

The agent's job is to produce **one file**: `report.md`. The pipeline is two scripts:

```
collect.py  →  inventory.json  →  report.py  →  report.md
```

`report.py` imports `analyze.py` internally and renders the comprehensive report — no separate JSON intermediate is needed unless you want to cache the inventory.

### Recommended one-shot

```bash
# All accounts in the active subscription
python scripts/collect.py | python scripts/report.py > report.md

# Specific subscription
python scripts/collect.py --subscription <sub-id> | python scripts/report.py > report.md

# Single account
python scripts/collect.py --account <name> --resource-group <rg> | python scripts/report.py > report.md
```

### Two-step (cache inventory)

```bash
python scripts/collect.py > inventory.json     # collect once
python scripts/report.py inventory.json > report.md
# re-run report only after rule/threshold changes — no Azure calls needed
```

`analyze.py` can still be run standalone if a downstream system wants raw recommendations JSON instead of the markdown.

## What's in the Report

1. **Subscription summary** — account count, total capacity, recommendation count by severity, estimated monthly savings
2. **Issues by category** — Tier / Redundancy / Lifecycle / Security / Governance / Feature / Procurement / Orphan
3. **Top 10 savings opportunities** — ranked by dollars
4. **Per-account detail** (grouped by team/owner tag):
   - Configuration (kind, SKU, tier, HNS, tags)
   - Usage (capacity, 90d-avg capacity, 30d/90d transactions, ingress/egress)
   - Data protection (lifecycle, versioning, change feed, soft delete, last-access tracking)
   - Security (TLS, public access, cross-tenant, key source)
   - Paid features (SFTP, NFS v3, local users)
   - Recommendations sorted high → medium → low → info with savings estimates
5. **Methodology** footer

## Decision Matrix (summary)

| Category | Rule | Severity |
|---|---|---|
| Account | GPv1 (`kind=Storage`) → upgrade to GPv2 (free) | HIGH |
| **Tier (new)** | GPv2 + ZRS/GZRS/RA-GZRS + not Smart → **Enable Smart Tier** (Apr 2026 GA) | HIGH |
| Tier | 0 txn 90d, non-prod → Archive | HIGH |
| Tier | Cool + 0 txn 30d + >10 GiB → Cold | MEDIUM |
| Tier | Hot + 0 txn 30d → Cool | MEDIUM |
| Tier | Cool with high read rate → back to Hot | MEDIUM |
| Redundancy | GRS/RA-GRS/GZRS in dev/test → LRS | HIGH |
| Redundancy | RA-* without secondary reads → drop RA prefix | LOW |
| Lifecycle | No policy + >1 GiB → add baseline policy | HIGH |
| Lifecycle | Versioning ON + no version-delete rule → add rule | HIGH |
| Lifecycle | Lifecycle uses last-access + LAT disabled → enable LAT | MEDIUM |
| Security | min_tls != TLS1_2 → set TLS 1.2 (Feb 2026 enforcement) | HIGH |
| Security | `allow_blob_public_access=true` → disable | HIGH |
| Security | `allow_cross_tenant_replication=true` → disable | MEDIUM |
| Security | Public network access + prod → use Private Endpoint | MEDIUM |
| Security | CMK with >100M tx/30d → review vs Managed HSM | LOW |
| Feature | SFTP enabled → flat ~$216/mo, review | HIGH |
| Feature | NFS v3 → feature compatibility note | INFO |
| Procurement | Avg capacity ≥ 100 TiB over 90d → reserved capacity | MEDIUM |
| Orphan | <1 GiB used + 0 txn 90d → deletion candidate | MEDIUM |

**Hard rule:** Never recommend Archive when any transactions exist in the last 90 days — rehydration (up to 15h, ~$0.022/GiB) wipes the savings.

Full thresholds, pricing, and source links: `references/decision_matrix.md`

## Files

```
azure-storage-account-optimization/
├── SKILL.md                          this file (agentskills.io spec)
├── prompt.md                         copy-paste prompt templates for invoking the skill
├── scripts/
│   ├── collect.py                    inventory + metrics from Azure Monitor (read-only)
│   ├── analyze.py                    decision-matrix module (also CLI for raw JSON)
│   └── report.py                     comprehensive markdown report (primary entry point)
└── references/
    └── decision_matrix.md            full rules + pricing context + source links
```

## Installation per Platform

| Agent | How to install |
|---|---|
| **Claude Code** | Symlink or copy this folder into `~/.claude/skills/`, or load directly from workspace |
| **GitHub Copilot CLI** | Place under a plugin path Copilot auto-discovers (e.g. `.github/copilot/skills/` in the repo, or the user-level skills directory) |
| **Codex** | Symlink or copy into `~/.agents/skills/` |
| **Any agentskills.io agent** | Point the agent at this folder; YAML frontmatter is the canonical metadata |
