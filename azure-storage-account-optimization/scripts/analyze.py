"""Apply optimization rules to collected storage account inventory.

Module + CLI. Encodes the full decision matrix (see references/decision_matrix.md).
Imported by report.py; can also be run standalone to produce raw recommendations JSON.

Usage:
    python analyze.py inventory.json             # from file
    python collect.py | python analyze.py        # piped
"""

from __future__ import annotations

import json
import sys
from dataclasses import asdict, dataclass, field
from typing import Optional

GiB = 1_073_741_824
TiB = 1024 * GiB

# East US LRS approximate rates ($/GiB/mo storage; $/10k ops where noted).
# See references/decision_matrix.md — adjust if your region differs significantly.
RATES = {
    'hot':     0.0184,
    'cool':    0.0100,
    'cold':    0.0045,
    'archive': 0.00099,
    'geo_premium_per_gib': 0.010,   # GRS/GZRS premium over LRS (approx)
    'sftp_monthly_flat':   216.0,   # ~$0.30/hr * 720h
    'reservation_discount_1yr': 0.18,  # 100 TiB / 1yr / Hot LRS ~18%
    'reservation_discount_3yr': 0.38,  # 1 PiB  / 3yr / Hot LRS ~38%
}

PROD_ENVS = {'prod', 'production', 'prd'}
NONPROD_ENVS = {'dev', 'test', 'sandbox', 'staging', 'qa', 'uat'}
GEO_SKUS = ('STANDARD_GRS', 'STANDARD_RAGRS', 'STANDARD_GZRS', 'STANDARD_RAGZRS')
SMART_ELIGIBLE_SKUS = ('STANDARD_ZRS', 'STANDARD_GZRS', 'STANDARD_RAGZRS')


@dataclass
class Recommendation:
    account: str
    resource_group: str
    subscription_id: str
    category: str   # tier | redundancy | lifecycle | security | governance | feature | account | procurement | orphan
    severity: str   # high | medium | low | info
    action: str
    reason: str
    estimated_monthly_savings_usd: Optional[float] = None
    docs: Optional[str] = None
    tags: dict = field(default_factory=dict)


def _gib(val: Optional[float]) -> float:
    return (val or 0) / GiB


def _env(tags: dict) -> str:
    return (tags.get('env') or tags.get('environment') or '').lower()


def analyze(account: dict) -> list[Recommendation]:
    recs: list[Recommendation] = []
    name = account['name']
    rg = account['resource_group']
    sub = account.get('subscription_id', '')
    tags = account.get('tags') or {}
    env = _env(tags)

    kind = (account.get('kind') or '')
    kind_lower = kind.lower()
    sku = (account.get('sku') or '').upper()
    tier = (account.get('access_tier') or '').lower()
    txn_30 = account.get('transactions_30d') or 0
    txn_90 = account.get('transactions_90d') or 0
    used_gib = _gib(account.get('used_capacity_bytes'))
    avg_90d_gib = _gib(account.get('avg_capacity_90d_bytes'))
    lifecycle = account.get('lifecycle_policy_present', False)
    is_smart_eligible = (
        kind_lower == 'storagev2'
        and any(sku.startswith(s) for s in SMART_ELIGIBLE_SKUS)
        and not account.get('is_nfs_v3_enabled', False)
    )
    smart_enabled = tier == 'smart'

    def add(category, severity, action, reason, savings=None, docs=None):
        recs.append(Recommendation(
            account=name, resource_group=rg, subscription_id=sub,
            category=category, severity=severity, action=action, reason=reason,
            estimated_monthly_savings_usd=savings, docs=docs, tags=tags,
        ))

    # =========================================================================
    # ACCOUNT MODERNIZATION
    # =========================================================================
    if kind_lower == 'storage':
        add('account', 'high',
            'Upgrade GPv1 → GPv2 (free)',
            'GPv1 is legacy — GPv2 unlocks lifecycle management, access tiers, soft delete, '
            'and is the same or lower price for most workloads',
            docs='https://learn.microsoft.com/azure/storage/common/storage-account-upgrade')

    # =========================================================================
    # SMART TIER (April 2026 GA) — preferred over manual tiering when eligible
    # =========================================================================
    if is_smart_eligible and not smart_enabled and used_gib > 0:
        # Conservative: Smart Tier shifts ~30% of capacity from Hot to Cool/Cold over 90d.
        # Savings ≈ 30% of used_gib * (hot_rate - blended_cool_cold_rate)
        savings = used_gib * 0.30 * (RATES['hot'] - (RATES['cool'] + RATES['cold']) / 2)
        add('tier', 'high',
            'Enable Smart Tier (April 2026 GA)',
            f'{kind} + {sku} eligible — auto-tiers Hot↔Cool↔Cold based on access patterns. '
            'No retrieval, transition, or early-deletion fees within Smart Tier',
            savings,
            docs='https://learn.microsoft.com/azure/storage/blobs/access-tiers-smart')

    # =========================================================================
    # MANUAL TIER (skip if Smart Tier already recommended/enabled)
    # =========================================================================
    if not smart_enabled and not is_smart_eligible:
        # Archive — strictly for zero-access non-prod
        if txn_90 == 0 and env not in PROD_ENVS and used_gib > 0 and tier != 'archive':
            savings = used_gib * (RATES['hot'] - RATES['archive']) if tier == 'hot' else used_gib * 0.005
            add('tier', 'high',
                'Move to Archive tier',
                f'Zero transactions in 90 days, env={env or "untagged"}. '
                'Hard rule: only if no reads expected — rehydration takes up to 15h',
                savings,
                docs='https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview')
        # Cold — between Cool and Archive, online access
        elif tier == 'cool' and txn_30 == 0 and used_gib > 10:
            savings = used_gib * (RATES['cool'] - RATES['cold'])
            add('tier', 'medium',
                'Move to Cold tier',
                f'Cool tier with no transactions in 30 days, {used_gib:.0f} GiB — '
                'Cold is online and ~55% cheaper than Cool (90-day minimum retention)',
                savings,
                docs='https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview')
        # Hot → Cool
        elif tier == 'hot' and txn_30 == 0 and used_gib > 0:
            savings = used_gib * (RATES['hot'] - RATES['cool'])
            add('tier', 'medium',
                'Move to Cool tier',
                'Hot tier with zero transactions in 30 days',
                savings,
                docs='https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview')
        # Cool → Hot (read-heavy Cool is more expensive than Hot)
        elif tier == 'cool' and txn_30 > 1_000_000 and used_gib < 100:
            add('tier', 'medium',
                'Move back to Hot tier',
                f'Cool tier with {txn_30:,.0f} transactions/30d — per-operation cost in Cool '
                'likely exceeds the storage savings vs Hot',
                docs='https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview')

    # =========================================================================
    # REDUNDANCY
    # =========================================================================
    if any(sku.startswith(s) for s in GEO_SKUS) and env in NONPROD_ENVS:
        savings = used_gib * RATES['geo_premium_per_gib']
        add('redundancy', 'high',
            f'Downgrade {sku} → Standard_LRS',
            f'Geo-redundant storage unnecessary for env={env}',
            savings,
            docs='https://learn.microsoft.com/azure/storage/common/storage-redundancy')
    elif sku.startswith('STANDARD_LRS') and env in PROD_ENVS:
        add('redundancy', 'medium',
            'Review durability posture',
            'LRS in production — survives drive failure but not AZ or region loss. '
            'Document exception or migrate to ZRS/GRS',
            docs='https://learn.microsoft.com/azure/storage/common/storage-redundancy')
    if sku.startswith(('STANDARD_RAGRS', 'STANDARD_RAGZRS')):
        add('redundancy', 'low',
            f'Downgrade {sku} → {sku.replace("RAGRS", "GRS").replace("RAGZRS", "GZRS")} '
            'if secondary endpoint unused',
            'Read-access secondary only useful if application reads from -secondary endpoint',
            docs='https://learn.microsoft.com/azure/storage/common/storage-redundancy')

    # =========================================================================
    # LIFECYCLE & VERSIONING
    # =========================================================================
    if not lifecycle and used_gib > 1.0 and not smart_enabled:
        add('lifecycle', 'high',
            'Add lifecycle management policy',
            f'No lifecycle policy on {used_gib:.1f} GiB — recommend Cool@30d / Archive@180d / delete@730d baseline',
            used_gib * 0.005,
            docs='https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview')

    if account.get('versioning_enabled') and not account.get('lifecycle_has_version_rule'):
        add('governance', 'high',
            'Add lifecycle rule deleting old non-current versions',
            'Versioning is enabled but no version-expiration rule — '
            'versions accumulate at full capacity (typically 3-10x storage on write-heavy accounts)',
            used_gib * 0.01,
            docs='https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-policy-configure')

    if account.get('lifecycle_uses_last_access') and not account.get('last_access_time_tracking_enabled'):
        add('lifecycle', 'medium',
            'Enable Last Access Time tracking',
            'Lifecycle policy references last-access time but tracking is disabled — '
            'these rules will never fire',
            docs='https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview#use-last-access-time')

    soft_blob = account.get('blob_soft_delete_days') or 0
    if soft_blob > 14 and env in NONPROD_ENVS:
        add('governance', 'low',
            'Reduce blob soft-delete retention to 7 days',
            f'{soft_blob}-day retention in {env} inflates billed capacity for deleted data',
            docs='https://learn.microsoft.com/azure/storage/blobs/soft-delete-blob-overview')

    # =========================================================================
    # SECURITY BASELINE (Feb 2026 enforcement)
    # =========================================================================
    tls = (account.get('min_tls_version') or '').upper()
    if tls and tls not in ('TLS1_2', 'TLS1_3'):
        add('security', 'high',
            'Set minimum TLS to 1.2',
            f'Current: {tls} — Microsoft enforces TLS 1.2 as the floor for Blob endpoints from Feb 2026',
            docs='https://learn.microsoft.com/azure/storage/common/transport-layer-security-configure-minimum-version')
    elif not tls:
        add('security', 'medium',
            'Set minimum TLS to 1.2',
            'Minimum TLS version not set — defaults to TLS 1.0 on older accounts',
            docs='https://learn.microsoft.com/azure/storage/common/transport-layer-security-configure-minimum-version')

    if account.get('allow_blob_public_access') is True:
        add('security', 'high',
            'Disable anonymous blob public access',
            'allow_blob_public_access=true — disable at account level unless explicitly serving public content',
            docs='https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-prevent')

    if account.get('allow_cross_tenant_replication') is True:
        add('security', 'medium',
            'Disable cross-tenant replication',
            'Default since Dec 2023 is disabled — restrict object replication to your tenant unless explicitly needed',
            docs='https://learn.microsoft.com/azure/storage/blobs/object-replication-prevent-cross-tenant-policies')

    if account.get('public_network_access') == 'Enabled' and env in PROD_ENVS:
        add('security', 'medium',
            'Restrict public network access via Private Endpoint or service firewall',
            'Public network access enabled on production account — prefer Private Link or selected networks',
            docs='https://learn.microsoft.com/azure/storage/common/storage-network-security')

    if account.get('key_source') == 'Microsoft.Keyvault' and (txn_30 or 0) > 100_000_000:
        add('security', 'low',
            'Review CMK cost on high-tx account',
            f'CMK enabled with {txn_30:,.0f} transactions/30d — Key Vault unwrap calls billed per 10k tx; '
            'consider Managed HSM (flat hourly fee) for very high throughput',
            docs='https://learn.microsoft.com/azure/storage/common/customer-managed-keys-overview')

    # =========================================================================
    # PAID FEATURES
    # =========================================================================
    if account.get('is_sftp_enabled'):
        add('feature', 'high',
            'SFTP enabled — flat ~$216/mo per account',
            'is_sftp_enabled=true incurs ~$0.30/hr regardless of usage. '
            'Disable when idle, schedule on/off, or consolidate accounts',
            RATES['sftp_monthly_flat'],
            docs='https://learn.microsoft.com/azure/storage/blobs/secure-file-transfer-protocol-support')

    if account.get('is_nfs_v3_enabled'):
        add('feature', 'info',
            'NFS v3 enabled — feature compatibility note',
            'NFS v3 disables several blob features (soft delete, versioning, snapshots, lifecycle on some flows). '
            'Verify access tier optimization paths still apply',
            docs='https://learn.microsoft.com/azure/storage/blobs/network-file-system-protocol-support')

    # =========================================================================
    # RESERVED CAPACITY (procurement)
    # =========================================================================
    avg_tib = avg_90d_gib / 1024
    if avg_tib >= 100:
        # ~18% on 1yr, ~38% on 3yr at 100 TiB / Hot LRS — use conservative blended 20%
        savings_1yr = avg_90d_gib * RATES['hot'] * RATES['reservation_discount_1yr']
        add('procurement', 'medium',
            f'Evaluate Reserved Capacity ({avg_tib:.0f} TiB sustained over 90 days)',
            f'Sustained capacity qualifies for 1-yr (~18%) or 3-yr (~38%) blob reservations. '
            f'Eligible: Standard GPv2/Blob accounts, block blobs/ADLS Gen2',
            savings_1yr,
            docs='https://learn.microsoft.com/azure/storage/blobs/storage-blob-reserved-capacity')

    # =========================================================================
    # ORPHAN
    # =========================================================================
    if used_gib < 1.0 and txn_90 == 0:
        add('orphan', 'medium',
            'Orphan candidate — confirm deletion with owner',
            f'{used_gib:.3f} GiB used, zero transactions in 90 days')

    return recs


def main() -> None:
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as fh:
            inventory = json.load(fh)
    else:
        inventory = json.load(sys.stdin)

    all_recs = [asdict(r) for account in inventory for r in analyze(account)]
    severity_order = {'high': 0, 'medium': 1, 'low': 2, 'info': 3}
    all_recs.sort(
        key=lambda r: (
            severity_order.get(r['severity'], 9),
            -(r.get('estimated_monthly_savings_usd') or 0),
        ),
    )
    print(json.dumps(all_recs, indent=2))


if __name__ == '__main__':
    main()
