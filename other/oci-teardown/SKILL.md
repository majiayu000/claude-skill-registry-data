---
name: oci-teardown
description: Delete Oracle Cloud Always Free resources safely with the oci CLI — terminate the instance and unwind NSG, subnet, route table, internet gateway and VCN in reverse order. Use for "tear it down", "destroy everything", "clean up my free tier", `oci compute instance terminate`, `oci network vcn delete`, Conflict or "has dependencies" errors, orphaned boot volumes, stopping charges, and verifying nothing billable survived.
---

# OCI teardown

Full procedure: `${CLAUDE_PLUGIN_ROOT}/docs/runbooks/tear-it-all-down.md`.
Configuration and authentication come from the `oci-setup` skill — run it first
if config is missing.

**Destruction is irreversible.** Terminating an instance destroys its boot volume
and everything on it; public IPs are not returned; deleted network resources
cannot be recovered.

## Confirm before deleting anything

1. List exactly what will be deleted, and show the list to the user:

```bash
# Discover the tenancy, target compartment, and managed resources at runtime.
# Never read or write a plugin configuration file.
oci search resource structured-search --query-text \
  "query all resources where (freeformTags.key = 'managed-by' && freeformTags.value = '$MANAGED_BY_TAG')" \
  --query 'data.items[].{name:"display-name",type:"resource-type",state:"lifecycle-state"}' --output table
```

2. Get **explicit confirmation of that specific list** before the first delete. An
   earlier general instruction — "clean up when you're done" — is not standing
   authorization for a deletion later in the session. Ask again, naming resources.
3. Offer a backup first, and wait for an answer:

```bash
ssh -i ~/.ssh/oci_free_tier ubuntu@"$PUBLIC_IP" 'sudo tar czf - /etc /home' \
  > backup-$(date +%F).tar.gz
```

4. Untagged resources will not appear in that search — cross-check the
   tenancy-wide inventory in `${CLAUDE_PLUGIN_ROOT}/docs/staying-free.md` before
   calling it complete.

## Delete in strict reverse dependency order

`instance → NSG → subnet → route table → internet gateway → VCN`

Nothing computes this order for you — that was Terraform's dependency graph. Use
`--wait-for-state TERMINATED` on each step so the next one can succeed. Commands:
`${CLAUDE_PLUGIN_ROOT}/docs/runbooks/tear-it-all-down.md`.

On `Conflict` or `has dependencies`: something is still attached, usually a VNIC
from a not-quite-terminated instance. VNIC cleanup lags instance termination —
wait ~30 seconds and retry. Do not force-delete around it, and do not reorder.

The VCN's default route table, security list, and DHCP options go with the VCN.
They are not deleted separately and cannot be.

## Boot volumes outlive instances

Always terminate with `--preserve-boot-volume false`. A preserved boot volume
outlives the instance and keeps consuming the 200 GB allowance — the most common
source of a mysterious storage charge.

Then hunt orphans from earlier attempts across **every** availability domain:

```bash
for AD in $(oci iam availability-domain list --compartment-id "$OCI_TENANCY_ID" \
            --query 'data[].name' --raw-output | tr -d '[]", '); do
  oci bv boot-volume list --compartment-id "$OCI_COMPARTMENT_ID" --availability-domain "$AD" \
    --query "data[?\"lifecycle-state\"!='TERMINATED'].{name:\"display-name\",gb:\"size-in-gbs\",id:id}" \
    --output table; done
```

Delete each with `oci bv boot-volume delete --boot-volume-id "<id>" --force`.

## Verify — "the delete command ran" proves nothing

Check both that resources are gone and that usage returned to zero:

```bash
oci search resource structured-search --query-text \
  "query all resources where lifeCycleState != 'TERMINATED' && lifeCycleState != 'DELETED'" \
  --query 'data.items[].{name:"display-name",type:"resource-type"}' --output table

AD=$(oci iam availability-domain list --compartment-id "$OCI_TENANCY_ID" \
      --query 'data[0].name' --raw-output)
oci limits resource-availability get --compartment-id "$OCI_TENANCY_ID" --service-name compute \
  --limit-name standard-a1-core-count --availability-domain "$AD" --query 'data.used'
oci limits resource-availability get --compartment-id "$OCI_TENANCY_ID" --service-name block-storage \
  --limit-name total-storage-gb --availability-domain "$AD" --query 'data.used'
```

Both must read `0`. Report the actual numbers, not a claim of success.

`TERMINATED` instances lingering in listings are harmless tombstone records — not
billable, and they age out on their own. A `RUNNING` or `AVAILABLE` anything is a
real leftover; investigate before declaring teardown finished.

## What teardown does not cover

Say so explicitly rather than implying everything is gone. Untouched, possibly
billable:

- IAM users, groups, dynamic groups, policies
- Budgets and alert rules
- Object Storage buckets — deleted separately, and they block compartment cleanup
  (`oci os bucket list --compartment-id "$OCI_COMPARTMENT_ID"`)
- Autonomous Databases — own lifecycle and a retention period
- Custom images and saved console history

## Tidy the config file last

There is no state file, so stale OCIDs from a previous shell are the main way a
later session gets confused — rediscover a deleted `SUBNET_ID`
returns `NotAuthorizedOrNotFound`, which reads like a permissions problem. Delete the exports for what you just removed
(`VCN_ID`, `IGW_ID`, `RT_ID`, `SUBNET_ID`, `NSG_ID`, `INSTANCE_ID`, `PUBLIC_IP`);
leave the profile, tenancy, and compartment values alone.

`oci iam compartment delete` needs a completely empty compartment and is
asynchronous — minutes, not seconds. Only do that, or remove local credentials,
if the user asks.
