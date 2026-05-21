# Prompt Templates — Azure Storage Account Optimization

Copy-paste prompts for invoking this skill in any agent (Claude Code, Copilot CLI, Codex, etc.). The skill is **read-only** — it never modifies Azure resources, so these prompts are safe to run against production.

Before running anything, the user must be logged in:
```bash
az login
az account show --query '{id:id, name:name}'   # confirm active subscription
```

---

## 1. Audit the whole active subscription (most common)

**Prompt:**
```
Audit all Azure storage accounts in my active subscription and give me a markdown report.
```

**What the agent should do:**
1. Run `az account show --query id -o tsv` to confirm the active subscription
2. Run `python scripts/collect.py | python scripts/report.py > report.md`
3. Show the path to `report.md` (and optionally summarize the top findings)

---

## 2. Audit a specific subscription

**Prompt:**
```
Audit all storage accounts in subscription <SUBSCRIPTION_ID> and produce a markdown report.
```

**Example:**
```
Audit all storage accounts in subscription 7c1b9e3a-1234-5678-9abc-def012345678
and produce a markdown report.
```

**What the agent should do:**
```bash
python scripts/collect.py --subscription <SUBSCRIPTION_ID> | python scripts/report.py > report.md
```

---

## 3. Audit a single storage account

**Prompt:**
```
Optimize storage account <ACCOUNT_NAME> in resource group <RESOURCE_GROUP>.
Produce a markdown report with status and recommendations.
```

**Example:**
```
Optimize storage account stproddata01 in resource group rg-data-prod.
Produce a markdown report with status and recommendations.
```

**What the agent should do:**
```bash
python scripts/collect.py --account stproddata01 --resource-group rg-data-prod \
  | python scripts/report.py > report.md
```

---

## 4. Re-run report from a cached inventory

Use this when the inventory was already collected and you want to re-render the report (e.g., after a rules update) without re-querying Azure.

**Prompt:**
```
Regenerate the storage audit report from inventory.json (no re-collect).
```

**What the agent should do:**
```bash
python scripts/report.py inventory.json > report.md
```

---

## 5. Compare two subscriptions side-by-side

**Prompt:**
```
Collect storage inventory for subscriptions <SUB_A> and <SUB_B>, then produce
two separate markdown reports.
```

**What the agent should do:**
```bash
python scripts/collect.py --subscription <SUB_A> | python scripts/report.py > report-suba.md
python scripts/collect.py --subscription <SUB_B> | python scripts/report.py > report-subb.md
```

---

## 6. Filter for a specific finding category

The skill always emits the full report, but the user can grep it. Useful follow-ups after the report is generated:

```
From report.md, list only the HIGH severity recommendations.
From report.md, sum the estimated monthly savings by team tag.
From report.md, list every account eligible for Smart Tier opt-in.
```

The agent should grep/parse `report.md` directly — no re-running of the scripts needed.

---

## Prompt Anatomy

A good prompt for this skill contains, in order:

1. **Action verb** — "audit", "optimize", "analyze", "report on"
2. **Scope** — "all storage accounts", "this single account", "subscription X"
3. **Output** — "markdown report" (the only artifact this skill produces)

Optional modifiers:
- **Subscription**: `in subscription <id>` (otherwise defaults to active)
- **Resource group**: `in resource group <name>` (for single-account scope)
- **Skip collect**: `from inventory.json` (use cached data)

---

## What the Report Will Contain

The agent should set the user's expectations to:

1. **Subscription summary** — account count, total capacity, total savings estimate, severity breakdown
2. **Issues by category** — Tier / Redundancy / Lifecycle / Security / Governance / Feature / Procurement / Orphan
3. **Top 10 savings opportunities** — ranked by dollars
4. **Per-account detail** (grouped by team/owner tag) — full config, usage, data protection, security, paid features, and ranked recommendations with `docs:` links to Microsoft Learn
5. **Methodology** footer

The report is self-contained — the user can hand it to engineering owners as a punch list without needing access to the agent.

---

## Safety Notes

- **No write permissions needed.** Run with `Reader` + `Monitoring Reader` Azure RBAC roles.
- **No resource modifications.** All API calls are list/get/query. No `update`, `create`, or `delete` operations exist.
- **Cost of running:** Azure Monitor `query_resource` calls are negligible (a few cents per audit at most for thousands of metric points).
- **Time to run:** ~1-3 seconds per account; full subscription audits with 50-100 accounts typically complete in 1-3 minutes.

---

## Anti-Patterns (prompts to avoid)

| Don't say | Why | Better |
|---|---|---|
| "Apply the optimizations to my storage accounts" | Skill is read-only by design — it will not apply changes | "Audit storage accounts and produce a report; I'll review and apply changes manually" |
| "Migrate account X to Cool tier" | Outside skill scope — use `az storage account update` directly | "Tell me whether account X should be on Cool tier" |
| "Show me only the savings, don't include status" | Skill produces a single comprehensive report; filtering happens after | Run the report, then `grep "est. \\\$" report.md` |
| "Run continuously every hour" | One-shot skill, not a daemon | Schedule via cron or GitLab/GitHub Actions calling the same scripts |
