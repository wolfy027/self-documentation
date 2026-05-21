# Decision Matrix — Azure Storage Account Optimization

Full rule set with thresholds, pricing context, and source documentation.
`analyze.py` encodes these rules; this file is the human-readable explanation.

Last updated: May 2026. Pricing snapshot: East US LRS. Verify your region.

---

## 0. Account Modernization

```
IF kind == "Storage"                                # GPv1
→ HIGH: Upgrade to StorageV2 (free, online)
   Why: GPv1 has no lifecycle, no access tiers, no soft delete, no Smart Tier.
        GPv2 is the same or lower price for most workloads.
   Docs: https://learn.microsoft.com/azure/storage/common/storage-account-upgrade
```

---

## 1. Smart Tier (NEW — April 2026 GA)

```
IF kind == "StorageV2"
   AND sku starts with "Standard_ZRS" | "Standard_GZRS" | "Standard_RAGZRS"
   AND is_nfs_v3_enabled == false
   AND access_tier != "Smart"
   AND used_capacity > 0
→ HIGH: Enable Smart Tier
   Why: Auto-tiers Hot↔Cool↔Cold based on access patterns.
        No retrieval, transition, or early-deletion fees within Smart Tier.
        Objects <128 KiB stay on Hot ("SmartHot-small") and skip monitoring fees.
        Customer telemetry showed >50% of capacity auto-shifted to cooler tiers in preview.
   Eligibility limits:
     - Standard GPv2 only (no GPv1, no Premium, no FileStorage, no BlockBlobStorage)
     - ZRS / GZRS / RA-GZRS only (no LRS, no GRS, no RA-GRS)
     - Block blobs only (no page or append blobs)
     - Cannot apply to blobs with an explicit access tier set
   Billing notes:
     - Standard Hot/Cool/Cold capacity rates apply
     - Monthly monitoring fee per 10K objects >128 KiB
     - Moving objects OUT of Smart Tier triggers a Cool-write transaction per object
   Docs: https://learn.microsoft.com/azure/storage/blobs/access-tiers-smart
```

---

## 2. Manual Tier (when Smart Tier is not available)

```
IF transactions_90d == 0
   AND env NOT IN (prod, production, prd)
   AND used_capacity > 0
   AND access_tier != "Archive"
→ HIGH: Move to Archive tier
   Hard rule: Never if any transactions in 90 days.
              Rehydration is up to 15h and costs ~$0.022/GiB.

IF access_tier == "Cool"
   AND transactions_30d == 0
   AND used_capacity > 10 GiB
→ MEDIUM: Move to Cold tier
   Why: Online access, ~55% cheaper than Cool. 90-day minimum retention applies.
   Docs: https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview

IF access_tier == "Hot"
   AND transactions_30d == 0
→ MEDIUM: Move to Cool tier

IF access_tier == "Cool"
   AND transactions_30d > 1,000,000
   AND used_capacity < 100 GiB
→ MEDIUM: Move back to Hot tier
   Why: Cool charges $0.01/10k read ops vs $0.004 for Hot.
        At high read rates the per-op cost exceeds the storage savings.
```

---

## 3. Redundancy

```
IF sku IN (GRS, RA_GRS, GZRS, RA_GZRS)
   AND env IN (dev, test, sandbox, staging, qa, uat)
→ HIGH: Downgrade to Standard_LRS
   Savings: ~$0.010/GiB/mo

IF sku starts with "LRS"
   AND env IN (prod, production, prd)
→ MEDIUM: Flag for durability review (NOT cost)
   LRS survives drive failure but not AZ/region loss.
   Document exception or migrate to ZRS/GRS/GZRS.

IF sku starts with "RAGRS" or "RAGZRS"
→ LOW: If application does not read from -secondary endpoint, downgrade to GRS/GZRS.
```

---

## 4. Lifecycle & Versioning

```
IF lifecycle_policy_present == false
   AND used_capacity > 1 GiB
   AND access_tier != "Smart"
→ HIGH: Add baseline lifecycle policy
   Baseline: Cool@30d / Archive@180d / delete@730d
   Note: "access" requires Last Access Time Tracking enabled.
   Docs: https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview

IF versioning_enabled == true
   AND lifecycle_has_version_rule == false
→ HIGH: Add version-deletion rule
   Why: Each overwrite creates a new version billed at full capacity.
        On write-heavy accounts this commonly produces 3-10x storage inflation.
   Suggested rule: delete non-current versions older than 30-90 days.

IF lifecycle_uses_last_access == true
   AND last_access_time_tracking_enabled == false
→ MEDIUM: Enable Last Access Time Tracking
   Why: Lifecycle rules referencing last-access will silently never fire.
        Enabling LAT is free; first read per blob per day is billed as "Other transactions".

IF blob_soft_delete_days > 14
   AND env IN (dev, test, sandbox, staging, qa, uat)
→ LOW: Reduce to 7 days
   Soft-deleted data counts toward billed capacity.
```

---

## 5. Security Baseline (2026 enforcement)

```
IF min_tls_version NOT IN ("TLS1_2", "TLS1_3")
→ HIGH: Set minimum TLS to 1.2
   Microsoft enforces TLS 1.2 as the floor on Blob endpoints from Feb 2026.
   Docs: https://learn.microsoft.com/azure/storage/common/transport-layer-security-configure-minimum-version

IF allow_blob_public_access == true
→ HIGH: Disable anonymous blob public access at the account level
   Docs: https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-prevent

IF allow_cross_tenant_replication == true
→ MEDIUM: Disable cross-tenant replication
   Default since Dec 2023 is disabled.
   Docs: https://learn.microsoft.com/azure/storage/blobs/object-replication-prevent-cross-tenant-policies

IF public_network_access == "Enabled"
   AND env IN (prod, production, prd)
→ MEDIUM: Use Private Endpoint or service firewall rules

IF key_source == "Microsoft.Keyvault"
   AND transactions_30d > 100,000,000
→ LOW: Review CMK cost
   Standard Key Vault bills per 10k transactions; very high-tx accounts may save
   on flat-fee Managed HSM.
```

---

## 6. Paid Features

```
IF is_sftp_enabled == true
→ HIGH: ~$216/month flat regardless of usage (~$0.30/hr)
   Action: disable when idle, schedule on/off, or consolidate accounts
   Docs: https://learn.microsoft.com/azure/storage/blobs/secure-file-transfer-protocol-support

IF is_nfs_v3_enabled == true
→ INFO: NFS v3 disables soft delete, versioning, snapshots, and some lifecycle flows
   Verify access tier optimization paths still apply.
```

---

## 7. Procurement (Reserved Capacity)

```
IF avg_capacity_90d >= 100 TiB
→ MEDIUM: Evaluate Reserved Capacity
   Units: 100 TiB or 1 PiB / month
   Terms: 1-yr or 3-yr
   Discount: ~18% (1-yr, 100 TiB, Hot LRS) up to ~38% (3-yr, 1 PiB)
   Eligible: Standard GPv2 + Blob Storage accounts; block blobs + ADLS Gen2
   NOT eligible: Premium, GPv1, page blobs, Files (separate SKU), Queue, Table
   Locked to one (region, tier, redundancy) combination — split if you use multiple.
   Docs: https://learn.microsoft.com/azure/storage/blobs/storage-blob-reserved-capacity
```

---

## 8. Orphans

```
IF used_capacity < 1 GiB
   AND transactions_90d == 0
→ MEDIUM: Candidate for deletion — confirm with owner
   Do not auto-delete; placeholder accounts often hold SAS tokens, firewall rules,
   or are referenced by infrastructure.
```

---

## Pricing Reference (East US LRS, May 2026)

| Tier | Storage $/GiB/mo | Read ops $/10k | Min retention | Notes |
|---|---|---|---|---|
| Hot | $0.0184 | $0.0040 | — | Default for new accounts |
| Cool | $0.0100 | $0.0100 | 30 days | Break-even ~2 reads/blob/mo |
| Cold | $0.0045 | $0.0200 | 90 days | Online; ~55% cheaper than Cool |
| Archive | $0.00099 | $0.022/GiB rehydrate | 180 days | Up to 15h rehydration |
| Smart Tier monitoring fee | per 10K objects >128 KiB | — | — | Add-on to underlying tier rates |

| Redundancy | Premium over LRS (approx) |
|---|---|
| ZRS | +~$0.003/GiB/mo |
| GRS / RA-GRS | +~$0.010/GiB/mo (plus write egress) |
| GZRS / RA-GZRS | +~$0.013/GiB/mo (plus write egress) |

| Feature | Cost |
|---|---|
| SFTP enabled | ~$0.30/hr flat ≈ $216/month |
| Private Endpoint | ~$0.01/hr + per-GB data processed |
| Defender for Storage (malware scan) | per-GB scanned; cap recommended |

---

## Sources

- [Access tiers overview](https://learn.microsoft.com/azure/storage/blobs/access-tiers-overview)
- [Smart Tier](https://learn.microsoft.com/azure/storage/blobs/access-tiers-smart)
- [Smart Tier GA blog (April 2026)](https://azure.microsoft.com/en-us/blog/optimize-object-storage-costs-automatically-with-smart-tier-now-generally-available/)
- [Cold tier GA blog](https://azure.microsoft.com/en-us/blog/efficiently-store-data-with-azure-blob-storage-cold-tier-now-generally-available/)
- [Lifecycle management](https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview)
- [Last Access Time Tracking](https://learn.microsoft.com/azure/storage/blobs/lifecycle-management-overview#use-last-access-time)
- [Reserved capacity](https://learn.microsoft.com/azure/storage/blobs/storage-blob-reserved-capacity)
- [TLS enforcement](https://learn.microsoft.com/azure/storage/common/transport-layer-security-configure-minimum-version)
- [Anonymous access](https://learn.microsoft.com/azure/storage/blobs/anonymous-read-access-prevent)
- [Cross-tenant replication](https://learn.microsoft.com/azure/storage/blobs/object-replication-prevent-cross-tenant-policies)
- [SFTP support](https://learn.microsoft.com/azure/storage/blobs/secure-file-transfer-protocol-support)
- [NFS v3 support](https://learn.microsoft.com/azure/storage/blobs/network-file-system-protocol-support)
- [CMK overview](https://learn.microsoft.com/azure/storage/common/customer-managed-keys-overview)
- [Storage redundancy](https://learn.microsoft.com/azure/storage/common/storage-redundancy)
- [Defender for Storage](https://learn.microsoft.com/azure/defender-for-cloud/defender-for-storage-introduction)
- [Soft delete vs versioning](https://learn.microsoft.com/azure/storage/blobs/soft-delete-vs-versioning-options)
