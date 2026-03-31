# Azure Databricks Cost Tracking & Management

> **Context:** This course covers how to understand, track, and manage all costs
> associated with Azure Databricks — both the Databricks DBU charges and the
> often-overlooked Azure infrastructure charges (storage, networking, VMs, disks).
> Each chapter explains *what the cost is*, *how to find it*, and *exactly how to track it*.

---

## How to Read This Course

Each chapter follows this structure (adapted to the topic):

```
THE PROBLEM   → What cost is hidden or misunderstood and why
THE CONCEPT   → The billing mechanism or tracking tool that addresses it
THE MATH      → Quantified cost examples with real numbers
HOW TO DO IT  → Step-by-step CLI commands, SQL queries, or portal steps
HOW TO CHECK  → How to verify your tracking is working
GOTCHAS       → Common pitfalls and mitigations
```

New to Databricks billing? Start with [Background Knowledge](00-basics.md) before diving into the chapters.

---

## Course Contents

| File | Topic |
|---|---|
| [Background Knowledge](00-basics.md) | DBUs, pricing tiers, billing streams, managed resource group anatomy |
| [Chapter 1 — DBU Cost Parameters](01-dbu-cost-parameters.md) | Every compute type, DBU rates, SKU multipliers, cluster config impact |
| [Chapter 2 — The Hidden Azure Costs](02-azure-infrastructure-costs.md) | Storage, networking, VMs, disks — everything outside the DBU bill |
| [Chapter 3 — Tagging for Cost Attribution](03-tagging-for-cost-attribution.md) | Workspace/cluster/job tags and how they flow to Cost Management |
| [Chapter 4 — Tracking Costs Inside Databricks](04-databricks-system-tables.md) | system.billing.usage, list_prices, ready-to-use SQL queries |
| [Chapter 5 — Daily Cost Tracking with az CLI](05-az-cli-daily-usage.md) | Manual commands for querying Azure Cost Management |
| [Chapter 6 — Automating Cost Reports](06-az-cli-automation.md) | Scheduled exports, daily reporter scripts, notifications |
| [Chapter 7 — Azure Cost Management Portal](07-azure-cost-management-portal.md) | Cost analysis views, budgets, alerts, dashboards |
| [Unified Cost Tracking Strategy](08-unified-cost-tracking-strategy.md) | Decision matrix, implementation checklist, monitoring cadence |

---

## Cost Categories Overview

| Category | Billed By | Where It Appears | Tracking Tool |
|---|---|---|---|
| DBU charges (All-Purpose, Jobs, SQL Warehouse, Serverless, etc.) | Databricks via Azure Marketplace | Marketplace/SaaS charges | Databricks system tables + az CLI |
| VM compute (cluster nodes) | Azure | Managed resource group | az CLI + Cost Management portal |
| Storage (DBFS root, ADLS Gen2, Delta tables) | Azure | Storage account charges | az CLI + Cost Management portal |
| Networking (egress, private endpoints, NAT, VNet) | Azure | Network resource charges | az CLI + Cost Management portal |
| Disks (OS, data, shuffle/spill) | Azure | Managed disk charges | az CLI + Cost Management portal |
| Other (Key Vault, Log Analytics) | Azure | Individual resource charges | az CLI + Cost Management portal |

---

## Recommended Reading Order

```
1. Background Knowledge (00)  → understand the billing model first
2. DBU Cost Parameters (01)   → learn what drives the Databricks bill
3. Hidden Azure Costs (02)    → learn what drives the Azure infra bill
4. Tagging (03)               → set up attribution before tracking
5. System Tables (04)         → track DBU costs inside Databricks
6. az CLI Manual (05)         → track all costs from the command line
7. az CLI Automation (06)     → automate daily cost reports
8. Portal (07)                → visual dashboards, budgets, alerts
9. Unified Strategy (08)      → bring it all together
```

---

## Navigation

| | |
|---|---|
| Start here | [Background Knowledge →](00-basics.md) |
| Jump to strategy | [Unified Cost Tracking Strategy →](08-unified-cost-tracking-strategy.md) |
