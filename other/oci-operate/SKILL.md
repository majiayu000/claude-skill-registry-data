---
name: oci-operate
description: Operate and troubleshoot an existing Oracle Cloud Always Free environment. Use for taking inventory, "what is running in my tenancy", cost checks, "am I still free", checking service limit usage, SSH not working, connection timed out, connection refused, "I can't reach my instance", missing public IP, NSG or security list or route table problems, my IP changed, instance stopped or needs starting, stopping to save OCPU hours, resizing an instance, drift review, orphaned or forgotten billable resources, and guest patching.
---

# OCI operate

Day-two work on an environment that already exists: knowing what you have,
proving it is still free, and fixing SSH. Full procedure:
`${CLAUDE_PLUGIN_ROOT}/docs/runbooks/connect-and-verify.md`. Configuration and
authentication come from the `oci-setup` skill — run it first if config is
missing. Requires an authenticated session first — see the `oci-session` skill.
Use the selected profile from `~/.oci/config` and discover tenancy, compartment,
operator IP, and managed resources at runtime. If a value cannot be discovered,
ask the user rather than guessing or asking them to paste OCIDs. Never invent
OCIDs; query them.

## Take inventory before anything else

Ask the API. There is no state file, so this cannot drift the way
`terraform plan` can — it describes the present, accurately, every time.

```bash
# Everything alive in the tenancy, any resource type
oci search resource structured-search --query-text \
  "query all resources where lifeCycleState != 'TERMINATED' && lifeCycleState != 'DELETED'" \
  --query 'data.items[].{name:"display-name",type:"resource-type",state:"lifecycle-state"}' \
  --output table

# Only what this toolkit created
oci search resource structured-search --query-text \
  "query all resources where (freeformTags.key = 'managed-by' && freeformTags.value = '$MANAGED_BY_TAG')" \
  --output table
```

Run the first query at the start of every session. The gap between the two lists
is the interesting part: anything alive but untagged was created by hand or left
behind, and may be billable. Report the gap; do not delete anything here — that
is `oci-teardown`. `TERMINATED` records linger for a while as tombstones, not
charges.

## Confirm it is still free

Compare what exists against the allowance: **2 OCPUs and 12 GB Arm total, 200 GB
storage total, per tenancy**. Not the 4/24 repeated online. Two 1-OCPU instances
exhaust the allowance exactly as completely as one 2-OCPU instance.

```bash
oci compute instance list --compartment-id "$OCI_COMPARTMENT_ID" --all \
  --query 'data[].{name:"display-name",state:"lifecycle-state",shape:shape,ocpus:"shape-config".ocpus,mem:"shape-config"."memory-in-gbs"}' \
  --output table

# Then read actual usage from the platform rather than trusting arithmetic
AD=$(oci iam availability-domain list --compartment-id "$OCI_TENANCY_ID" \
      --query 'data[0].name' --raw-output)
oci limits resource-availability get --compartment-id "$OCI_TENANCY_ID" \
  --service-name compute --limit-name standard-a1-core-count \
  --availability-domain "$AD" --query 'data.{used:used,available:available}'
```

The `used` value is the truth. Repeat for `standard-a1-memory-count` and, without
`--availability-domain`, for region-scoped limits like `vcn/vcn-count`. A high
`available` means the account is Pay As You Go, not that the headroom is free —
`${CLAUDE_PLUGIN_ROOT}/docs/staying-free.md`. Also confirm the configured region is still the home
region, and that any non-Arm instance is deliberate.

## Diagnose SSH failure in this order

Each step rules out a class of cause. Do not skip ahead, and do not change
anything until the cause is identified.

1. **The operator's public IP changed.** By far the most common cause; home and
   mobile addresses rotate. Compare `curl -s https://checkip.amazonaws.com`
   against `oci network nsg rules list --nsg-id "$NSG_ID"`. Behind a VPN, CGNAT,
   or corporate proxy the address a browser reports is not the address you
   egress from — trust `curl` run from the same machine and shell as the `ssh`.
   Mismatch → update the one rule to the new `/32`.
2. **No public IP.** `oci compute instance list-vnics --instance-id "$INSTANCE_ID"`
   returning `null` for `public-ip` means it launched without one. Assign an
   ephemeral one via the VNIC's private IP.
3. **NSG not attached to the VNIC.** A correct rule on an unattached NSG does
   nothing. Check `data[0]."nsg-ids"` on the VNIC; attach with
   `oci network vnic update --vnic-id ... --nsg-ids`.
4. **Subnet has no internet route.** A subnet quietly using the VCN's *default*
   route table has no `0.0.0.0/0` rule. Read the subnet's `route-table-id`, then
   the route rules, then confirm the internet gateway `is-enabled`.
5. **Subnet security list.** NSGs and security lists are **both** enforced —
   traffic must pass both. Inspect `ingress-security-rules` on the subnet's
   security list, which matters if the default one was ever edited.
6. **Guest-side.** With 1–5 clean, look inside the VM. `oci compute
   console-history capture` then `get-content` needs no network at all; read it
   for cloud-init failures, `sshd` not starting, or a full disk. Oracle Linux
   images ship `firewalld` blocking port 22 even when OCI permits it; Ubuntu
   images generally do not. Then use `nc -vz <host> 22`: **refused** means NSG
   and routing are fine and `sshd` is the problem; **timeout** means traffic
   never arrived. That single distinction is the most useful signal available.
7. **Prove whose network is at fault.** OCI Bastion is free on all tiers and
   reaches the instance over OCI's own network; Cloud Shell runs inside OCI too.
   If SSH works from either but not from the laptop, the problem is the user's
   local network or ISP, not the cloud config.

**Never widen the SSH rule to `0.0.0.0/0` as a diagnostic**, not even
temporarily. It is almost never the cause, and it exposes the box to continuous
automated attack. Refuse, and use step 7 instead.

## Routine operations

```bash
# Stop when idle to conserve monthly OCPU-hours; SOFTSTOP shuts the guest down cleanly
oci compute instance action --instance-id "$INSTANCE_ID" --action SOFTSTOP --wait-for-state STOPPED
oci compute instance action --instance-id "$INSTANCE_ID" --action START --wait-for-state RUNNING
```

A stopped instance burns no compute hours but **still holds its boot volume**
against the 200 GB allowance — stopping is not removing.

Resize with `oci compute instance update --shape-config`, after the pre-flight
check in `${CLAUDE_PLUGIN_ROOT}/docs/staying-free.md`, and never past 2 OCPUs / 12 GB without the user
explicitly accepting the charge. Guest patching is the user's responsibility, not
Oracle's — Oracle maintains the image; nothing patches a running instance for you.

## Reporting

Report state, shape, what falls inside or outside the free allowance, and any
untagged resource found. Truncate OCIDs when showing them for confirmation, and
never write real OCIDs, public IPs, CIDRs, tenancy or account names, keys, or
session tokens into tracked files — those belong in
the current shell only; rediscover them in later sessions.
