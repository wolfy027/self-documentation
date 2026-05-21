"""Render a comprehensive Azure Storage Account audit report (Markdown).

Reads an inventory JSON (from collect.py), applies the decision matrix via analyze.py,
and produces a single markdown report covering:
    - Subscription summary
    - Top savings opportunities
    - Per-account status (current configuration)
    - Per-account recommendations (sorted by severity then savings)

This is the primary user-facing entry point. The user runs collect → report and
consumes report.md as the only artifact they need.

Usage:
    python collect.py | python report.py > report.md
    python collect.py > inventory.json && python report.py inventory.json > report.md
"""

from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from dataclasses import asdict
from datetime import datetime, timezone

from analyze import GiB, analyze

SEVERITY_ORDER = {'high': 0, 'medium': 1, 'low': 2, 'info': 3}
SEVERITY_BADGE = {'high': 'HIGH', 'medium': 'MEDIUM', 'low': 'LOW', 'info': 'INFO'}
CATEGORY_LABEL = {
    'account': 'Account',
    'tier': 'Tier',
    'redundancy': 'Redundancy',
    'lifecycle': 'Lifecycle',
    'governance': 'Governance',
    'security': 'Security',
    'feature': 'Feature',
    'procurement': 'Procurement',
    'orphan': 'Orphan',
}


def _fmt_capacity(bytes_val):
    if not bytes_val:
        return '—'
    gib = bytes_val / GiB
    if gib >= 1024:
        return f'{gib / 1024:,.2f} TiB'
    if gib >= 1:
        return f'{gib:,.2f} GiB'
    return f'{bytes_val / (1024 * 1024):,.1f} MiB'


def _fmt_metric(val):
    if val is None:
        return '—'
    if val >= 1_000_000:
        return f'{val / 1_000_000:,.1f}M'
    if val >= 1_000:
        return f'{val / 1_000:,.1f}K'
    return f'{val:,.0f}'


def _check(flag):
    if flag is True:
        return 'yes'
    if flag is False:
        return 'no'
    return '—'


def _team(account_or_rec) -> str:
    tags = account_or_rec.get('tags') or {}
    return tags.get('team') or tags.get('owner') or tags.get('cost_center') or 'untagged'


def _account_status_block(account: dict) -> list[str]:
    name = account['name']
    rg = account['resource_group']
    loc = account.get('location', '—')
    lines = [f'### `{name}`  in  `{rg}`  ({loc})', '']

    tier = account.get('access_tier') or '—'
    smart_note = '  **(Smart Tier enabled)**' if tier.lower() == 'smart' else ''

    lines += [
        '**Configuration**',
        '',
        f'| Field | Value |',
        f'|---|---|',
        f'| Kind | `{account.get("kind") or "—"}` |',
        f'| SKU | `{account.get("sku") or "—"}` |',
        f'| Default tier | `{tier}`{smart_note} |',
        f'| ADLS Gen2 (HNS) | {_check(account.get("is_hns_enabled"))} |',
        f'| Tags | {", ".join(f"{k}={v}" for k, v in (account.get("tags") or {}).items()) or "—"} |',
        '',
        '**Usage (last 30 / 90 days)**',
        '',
        f'| Metric | Value |',
        f'|---|---|',
        f'| Used capacity | {_fmt_capacity(account.get("used_capacity_bytes"))} |',
        f'| Avg capacity (90d) | {_fmt_capacity(account.get("avg_capacity_90d_bytes"))} |',
        f'| Transactions (30d / 90d) | {_fmt_metric(account.get("transactions_30d"))} / {_fmt_metric(account.get("transactions_90d"))} |',
        f'| Ingress (30d) | {_fmt_capacity(account.get("ingress_30d"))} |',
        f'| Egress (30d) | {_fmt_capacity(account.get("egress_30d"))} |',
        '',
        '**Data protection & lifecycle**',
        '',
        f'| Setting | Value |',
        f'|---|---|',
        f'| Lifecycle policy | {_check(account.get("lifecycle_policy_present"))} |',
        f'| → version-delete rule | {_check(account.get("lifecycle_has_version_rule"))} |',
        f'| → uses last-access time | {_check(account.get("lifecycle_uses_last_access"))} |',
        f'| Last-access tracking | {_check(account.get("last_access_time_tracking_enabled"))} |',
        f'| Versioning | {_check(account.get("versioning_enabled"))} |',
        f'| Change feed | {_check(account.get("change_feed_enabled"))} |',
        f'| Blob soft delete (days) | {account.get("blob_soft_delete_days") or "—"} |',
        f'| Container soft delete (days) | {account.get("container_soft_delete_days") or "—"} |',
        '',
        '**Security**',
        '',
        f'| Setting | Value |',
        f'|---|---|',
        f'| Min TLS version | `{account.get("min_tls_version") or "—"}` |',
        f'| Public network access | `{account.get("public_network_access") or "—"}` |',
        f'| Anonymous blob access allowed | {_check(account.get("allow_blob_public_access"))} |',
        f'| Cross-tenant replication allowed | {_check(account.get("allow_cross_tenant_replication"))} |',
        f'| Key source | `{account.get("key_source") or "—"}` |',
        '',
        '**Paid features**',
        '',
        f'| Feature | Value |',
        f'|---|---|',
        f'| SFTP enabled (~$216/mo flat) | {_check(account.get("is_sftp_enabled"))} |',
        f'| NFS v3 enabled | {_check(account.get("is_nfs_v3_enabled"))} |',
        f'| Local users enabled | {_check(account.get("is_local_user_enabled"))} |',
        '',
    ]
    return lines


def _account_recs_block(recs: list[dict]) -> list[str]:
    if not recs:
        return ['**Recommendations:** none — account looks well-configured.', '']
    lines = ['**Recommendations**', '']
    sorted_recs = sorted(
        recs,
        key=lambda r: (
            SEVERITY_ORDER.get(r['severity'], 9),
            -(r.get('estimated_monthly_savings_usd') or 0),
        ),
    )
    for r in sorted_recs:
        sev = SEVERITY_BADGE.get(r['severity'], r['severity'].upper())
        cat = CATEGORY_LABEL.get(r['category'], r['category'].title())
        savings = r.get('estimated_monthly_savings_usd')
        savings_str = f'  — est. **${savings:,.2f}/mo**' if savings else ''
        lines.append(f'- **[{sev}][{cat}]** {r["action"]}{savings_str}')
        lines.append(f'  _{r["reason"]}_')
        if r.get('docs'):
            lines.append(f'  Reference: <{r["docs"]}>')
    lines.append('')
    return lines


def _render_summary(inventory, all_recs, sub_id):
    total_capacity = sum(a.get('used_capacity_bytes') or 0 for a in inventory)
    total_savings = sum(r.get('estimated_monthly_savings_usd') or 0 for r in all_recs)
    severity_counts = Counter(r['severity'] for r in all_recs)
    category_counts = Counter(r['category'] for r in all_recs)
    accounts_with_recs = len({(r['account'], r['resource_group']) for r in all_recs})

    lines = [
        f'# Azure Storage Account Audit',
        '',
        f'_Subscription: `{sub_id}` · Generated {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}_',
        '',
        '## Subscription Summary',
        '',
        f'| Metric | Value |',
        f'|---|---|',
        f'| Storage accounts | {len(inventory)} |',
        f'| Total used capacity | {_fmt_capacity(total_capacity)} |',
        f'| Accounts with recommendations | {accounts_with_recs} / {len(inventory)} |',
        f'| Total recommendations | {len(all_recs)} |',
        f'| → high severity | {severity_counts.get("high", 0)} |',
        f'| → medium severity | {severity_counts.get("medium", 0)} |',
        f'| → low / info | {severity_counts.get("low", 0) + severity_counts.get("info", 0)} |',
        f'| **Estimated monthly savings** | **${total_savings:,.2f}** |',
        '',
    ]

    if category_counts:
        lines += [
            '### Issues by Category',
            '',
            '| Category | Count |',
            '|---|---|',
        ]
        for cat in sorted(category_counts, key=lambda c: -category_counts[c]):
            lines.append(f'| {CATEGORY_LABEL.get(cat, cat.title())} | {category_counts[cat]} |')
        lines.append('')

    # Top 10 savings opportunities
    by_savings = sorted(
        [r for r in all_recs if r.get('estimated_monthly_savings_usd')],
        key=lambda r: -r['estimated_monthly_savings_usd'],
    )[:10]
    if by_savings:
        lines += [
            '### Top 10 Savings Opportunities',
            '',
            '| # | Account | Action | Est. $/mo |',
            '|---|---|---|---|',
        ]
        for i, r in enumerate(by_savings, 1):
            lines.append(f'| {i} | `{r["account"]}` | {r["action"]} | ${r["estimated_monthly_savings_usd"]:,.2f} |')
        lines.append('')

    return lines


def render(inventory: list[dict]) -> str:
    sub_id = inventory[0].get('subscription_id', '—') if inventory else '—'
    by_account: dict[tuple[str, str], list[dict]] = defaultdict(list)
    all_recs: list[dict] = []
    for account in inventory:
        recs = [asdict(r) for r in analyze(account)]
        for r in recs:
            key = (r['account'], r['resource_group'])
            by_account[key].append(r)
        all_recs.extend(recs)

    lines = _render_summary(inventory, all_recs, sub_id)

    # Group accounts by team tag for the detail section
    by_team: dict[str, list[dict]] = defaultdict(list)
    for account in inventory:
        by_team[_team(account)].append(account)

    lines += ['## Per-Account Detail', '']
    for team in sorted(by_team):
        team_accounts = sorted(by_team[team], key=lambda a: (a['resource_group'], a['name']))
        lines += [f'---', '', f'## Team / Owner: `{team}`', '']
        for account in team_accounts:
            lines += _account_status_block(account)
            recs = by_account.get((account['name'], account['resource_group']), [])
            lines += _account_recs_block(recs)

    lines += [
        '---',
        '',
        '## Methodology',
        '',
        '- Data collected via `AzureCliCredential` (requires `az login`) from Azure Resource Manager and Azure Monitor.',
        '- Savings estimates use approximate East US LRS rates; actual savings vary by region, redundancy, and access pattern.',
        '- Smart Tier (April 2026 GA) is preferred over manual tiering for eligible GPv2 + ZRS/GZRS/RA-GZRS accounts.',
        '- Full rule set and pricing context: `references/decision_matrix.md`',
        '',
    ]
    return '\n'.join(lines)


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fh:
            inventory = json.load(fh)
    else:
        inventory = json.load(sys.stdin)
    print(render(inventory))


if __name__ == '__main__':
    main()
