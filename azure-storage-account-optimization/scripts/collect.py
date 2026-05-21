"""Collect Azure Storage account snapshots for optimization audit.

Captures inventory, security config, blob-service settings, lifecycle state,
and Azure Monitor metrics in a single pass. Can be run standalone (JSON output)
or imported as a module by report.py.

Prerequisites:
    az login
    pip install azure-identity azure-mgmt-storage azure-monitor-query

Usage:
    python collect.py                                          # active subscription
    python collect.py --subscription <id>                     # specific subscription
    python collect.py --account <name> --resource-group <rg>  # single account
"""

from __future__ import annotations

import argparse
import json
import logging
import subprocess
from dataclasses import asdict, dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional

from azure.identity import AzureCliCredential
from azure.mgmt.storage import StorageManagementClient
from azure.monitor.query import MetricsQueryClient

logging.basicConfig(level=logging.INFO, format='%(levelname)s %(message)s')
log = logging.getLogger('collect')


@dataclass
class Snapshot:
    # Identity
    name: str
    resource_group: str
    subscription_id: str
    location: str
    tags: dict = field(default_factory=dict)

    # Account shape
    kind: str = ''                                # Storage (GPv1) | StorageV2 | BlobStorage | BlockBlobStorage | FileStorage
    sku: str = ''                                 # Standard_LRS | Standard_ZRS | Standard_GRS | ...
    access_tier: Optional[str] = None             # Hot | Cool | Cold | Smart (Apr 2026)
    is_hns_enabled: bool = False                  # ADLS Gen2
    is_sftp_enabled: bool = False                 # ~$216/mo flat
    is_nfs_v3_enabled: bool = False
    is_local_user_enabled: bool = False

    # Security
    min_tls_version: Optional[str] = None
    allow_blob_public_access: Optional[bool] = None
    allow_cross_tenant_replication: Optional[bool] = None
    public_network_access: Optional[str] = None
    key_source: Optional[str] = None              # Microsoft.Storage | Microsoft.Keyvault

    # Blob service
    versioning_enabled: bool = False
    change_feed_enabled: bool = False
    blob_soft_delete_days: Optional[int] = None
    container_soft_delete_days: Optional[int] = None
    last_access_time_tracking_enabled: bool = False

    # Lifecycle
    lifecycle_policy_present: bool = False
    lifecycle_has_version_rule: bool = False
    lifecycle_uses_last_access: bool = False

    # Metrics (Azure Monitor)
    used_capacity_bytes: Optional[float] = None
    avg_capacity_90d_bytes: Optional[float] = None
    transactions_30d: Optional[float] = None
    transactions_90d: Optional[float] = None
    ingress_30d: Optional[float] = None
    egress_30d: Optional[float] = None


def _active_subscription() -> str:
    return subprocess.check_output(
        ['az', 'account', 'show', '--query', 'id', '-o', 'tsv'],
        text=True,
    ).strip()


def _sum_metric(client, resource_id, metric, days):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    try:
        resp = client.query_resource(
            resource_id,
            metric_names=[metric],
            timespan=(start, end),
            granularity=timedelta(days=1),
            aggregations=['Total'],
        )
    except Exception as exc:
        log.debug('Total %s unavailable: %s', metric, exc)
        return None
    if not resp.metrics or not resp.metrics[0].timeseries:
        return None
    data = resp.metrics[0].timeseries[0].data
    total = sum(p.total for p in data if p.total is not None)
    return float(total) if total else None


def _avg_metric(client, resource_id, metric, days):
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=days)
    try:
        resp = client.query_resource(
            resource_id,
            metric_names=[metric],
            timespan=(start, end),
            granularity=timedelta(days=1),
            aggregations=['Average'],
        )
    except Exception as exc:
        log.debug('Average %s unavailable: %s', metric, exc)
        return None
    if not resp.metrics or not resp.metrics[0].timeseries:
        return None
    data = resp.metrics[0].timeseries[0].data
    values = [p.average for p in data if p.average is not None]
    return sum(values) / len(values) if values else None


def _blob_service_props(storage_client, rg, name):
    try:
        return storage_client.blob_services.get_service_properties(rg, name, 'default')
    except Exception:
        return None


def _lifecycle_info(storage_client, rg, name) -> tuple[bool, bool, bool]:
    """Return (present, has_version_delete_rule, uses_last_access_time)."""
    try:
        policy = storage_client.management_policies.get(rg, name, 'default')
    except Exception:
        return False, False, False
    if not policy or not policy.properties or not policy.properties.policy:
        return False, False, False
    try:
        raw = json.dumps(policy.properties.policy.as_dict()).lower()
    except Exception:
        raw = ''
    return True, '"version"' in raw and 'delete' in raw, 'lastaccesstime' in raw


def collect_one(account, sub_id, storage_client, metrics_client) -> Snapshot:
    rg = account.id.split('/')[4]
    name = account.name
    log.info('collecting %s/%s', rg, name)

    bs = _blob_service_props(storage_client, rg, name)
    lc_present, lc_version, lc_last_access = _lifecycle_info(storage_client, rg, name)

    snap = Snapshot(
        name=name,
        resource_group=rg,
        subscription_id=sub_id,
        location=account.location,
        tags=account.tags or {},

        kind=account.kind,
        sku=account.sku.name,
        access_tier=getattr(account, 'access_tier', None),
        is_hns_enabled=bool(getattr(account, 'is_hns_enabled', False)),
        is_sftp_enabled=bool(getattr(account, 'is_sftp_enabled', False)),
        is_nfs_v3_enabled=bool(getattr(account, 'enable_nfs_v3', getattr(account, 'is_nfs_v3_enabled', False))),
        is_local_user_enabled=bool(getattr(account, 'is_local_user_enabled', False)),

        min_tls_version=getattr(account, 'minimum_tls_version', None),
        allow_blob_public_access=getattr(account, 'allow_blob_public_access', None),
        allow_cross_tenant_replication=getattr(account, 'allow_cross_tenant_replication', None),
        public_network_access=getattr(account, 'public_network_access', None),
        key_source=getattr(getattr(account, 'encryption', None), 'key_source', None),

        lifecycle_policy_present=lc_present,
        lifecycle_has_version_rule=lc_version,
        lifecycle_uses_last_access=lc_last_access,
    )

    if bs:
        snap.versioning_enabled = bool(getattr(bs, 'is_versioning_enabled', False))
        cf = getattr(bs, 'change_feed', None)
        snap.change_feed_enabled = bool(getattr(cf, 'enabled', False)) if cf else False
        delete_blob = getattr(bs, 'delete_retention_policy', None)
        if delete_blob and delete_blob.enabled:
            snap.blob_soft_delete_days = delete_blob.days
        container_delete = getattr(bs, 'container_delete_retention_policy', None)
        if container_delete and container_delete.enabled:
            snap.container_soft_delete_days = container_delete.days
        lat = getattr(bs, 'last_access_time_tracking_policy', None)
        snap.last_access_time_tracking_enabled = bool(getattr(lat, 'enable', False)) if lat else False

    snap.used_capacity_bytes = _sum_metric(metrics_client, account.id, 'UsedCapacity', 1)
    snap.avg_capacity_90d_bytes = _avg_metric(metrics_client, account.id, 'UsedCapacity', 90)
    snap.transactions_30d = _sum_metric(metrics_client, account.id, 'Transactions', 30)
    snap.transactions_90d = _sum_metric(metrics_client, account.id, 'Transactions', 90)
    snap.ingress_30d = _sum_metric(metrics_client, account.id, 'Ingress', 30)
    snap.egress_30d = _sum_metric(metrics_client, account.id, 'Egress', 30)

    return snap


def collect(sub_id: str, account_name: Optional[str] = None, resource_group: Optional[str] = None) -> list[Snapshot]:
    cred = AzureCliCredential()
    storage_client = StorageManagementClient(cred, sub_id)
    metrics_client = MetricsQueryClient(cred)

    if account_name and resource_group:
        accounts = [storage_client.storage_accounts.get_properties(resource_group, account_name)]
    elif account_name:
        accounts = [a for a in storage_client.storage_accounts.list() if a.name == account_name]
    else:
        accounts = list(storage_client.storage_accounts.list())

    return [collect_one(a, sub_id, storage_client, metrics_client) for a in accounts]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--subscription', help='Subscription ID (default: az account show)')
    parser.add_argument('--account', help='Single storage account name')
    parser.add_argument('--resource-group', help='Resource group (used with --account)')
    args = parser.parse_args()

    sub_id = args.subscription or _active_subscription()
    log.info('subscription: %s', sub_id)
    snapshots = collect(sub_id, args.account, args.resource_group)
    print(json.dumps([asdict(s) for s in snapshots], indent=2, default=str))


if __name__ == '__main__':
    main()
