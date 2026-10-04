---
name: oci-provision
description: Create Always Free Oracle Cloud infrastructure with the oci CLI — pre-flight the free allowance, then create VCN, internet gateway, route table, subnet, NSG and SSH rules, and launch a VM.Standard.A1.Flex Arm instance. Use for "launch an instance", "spin up a free VM", "create the network", `oci compute instance launch`, `oci network vcn create`, shape-config sizing, image discovery, Out of host capacity retries, and anything that risks becoming billable.
---

# OCI provision

Translate the user's infrastructure request into a bounded plan before creating
anything. Show requested resources, sizing, region, and free-tier usage; ask for
confirmation when the request is ambiguous or could bill. Create resources only
after the free allowance has been checked. Procedures:
`${CLAUDE_PLUGIN_ROOT}/docs/runbooks/create-the-network.md` and
`${CLAUDE_PLUGIN_ROOT}/docs/runbooks/launch-an-instance.md`. Read
`${CLAUDE_PLUGIN_ROOT}/docs/staying-free.md` first. Configuration and
authentication come from the `oci-setup` skill — run it first if config is
missing. Requires an authenticated session — see the `oci-session` skill.

## Resolve runtime context

Discover tenancy, compartment, home region, operator CIDR, and SSH key at runtime.
If any value cannot be discovered, ask the user rather than guessing or asking
them to paste an OCID.

```bash
# Discover OCI_TENANCY_ID, OCI_COMPARTMENT_ID, OPERATOR_CIDR, and
# SSH_PUBLIC_KEY_FILE before creating anything. Do not persist them.
RESOURCE_PREFIX="af"
MANAGED_BY_TAG="oracle-cloud-cli-ops"
```

Never substitute a placeholder, a guessed OCID, or a default CIDR — that creates
a real resource in the wrong place, or opens a rule to the wrong network.

Take a tagged inventory snapshot before the first create. Repeat it after all
creates and compare the snapshots for the final report:

```bash
oci search resource structured-search --query-text \
  "query all resources where (freeformTags.key = 'managed-by' && freeformTags.value = '$MANAGED_BY_TAG')" \
  --query 'data.items[].{id:identifier,name:"display-name",type:"resource-type",state:"lifecycle-state"}' \
  --output table
```

## Pre-flight check — mandatory, every launch

Moving off Terraform deleted the `variables.tf` validation that rejected an
oversized shape before any API call; this check is the only guardrail left. Show
the user the numbers and refuse to launch if it fails.

1. Intended sizing must fit **2 OCPUs / 12 GB RAM / 200 GB total storage**.
2. **Add existing tenancy usage.** The allowance is per tenancy, not per
   instance: two 1-OCPU instances exhaust it as thoroughly as one 2-OCPU
   instance, and each extra launch looks individually harmless.

```bash
oci compute instance list --compartment-id "$OCI_COMPARTMENT_ID" --all \
  --query "data[?\"lifecycle-state\"=='RUNNING'].{name:\"display-name\",shape:shape,ocpus:\"shape-config\".ocpus,mem:\"shape-config\".\"memory-in-gbs\"}" --output table
```

3. Confirm the configured region equals the home region, both discovered at
   runtime — never hardcoded. Free compute exists **only** in the home region.

```bash
HOME_REGION=$(oci iam region-subscription list \
  --query 'data[?"is-home-region"]."region-name" | [0]' --raw-output)
CURRENT=$(grep -A8 "^\[$OCI_CLI_PROFILE\]" ~/.oci/config | grep '^region' | cut -d= -f2 | tr -d ' ')
[ "$HOME_REGION" = "$CURRENT" ] || echo "STOP: $CURRENT is not home region $HOME_REGION"
```

## Network, in dependency order

`VCN → internet gateway → route table → subnet → NSG → NSG rules`

Each step needs the OCID of the one before, so create them one at a time with
`--wait-for-state AVAILABLE`. Nothing here bills. Flags are in
`${CLAUDE_PLUGIN_ROOT}/docs/runbooks/create-the-network.md`: `--cidr-blocks`
(JSON array) on the VCN,
`--is-enabled true` on the gateway, `--route-table-id` on the subnet or it
silently gets no internet route.

**Never create an SSH ingress rule with `"source":"0.0.0.0/0"`.** Require
`$OPERATOR_CIDR` as a `/32`, refreshed with
`export OPERATOR_CIDR="$(curl -s https://checkip.amazonaws.com)/32"` if the user's
IP may have rotated. Leave 80/443 closed until something listens on them.

## Launching compute

- `--shape-config "{\"ocpus\":2,\"memoryInGBs\":12}"` is **required** for `.Flex`
  shapes. Omitted, you inherit shape defaults that can exceed the allowance.
- Discover the image at runtime: `oci compute image list ... --shape
  "VM.Standard.A1.Flex" --sort-by TIMECREATED --sort-order DESC`. `--shape` filters
  out x86 images. Never paste an image OCID from a blog — region-specific, and
  deprecated over time.
- `--ssh-authorized-keys-file "$SSH_PUBLIC_KEY_FILE"` takes the **public** key. A
  private or wrong key makes the instance permanently unreachable — no password
  login, no reset.
- `--wait-for-state RUNNING` on every create; without it the command returns
  before provisioning is known to have succeeded.
- Tag everything: `--freeform-tags "{\"managed-by\":\"$MANAGED_BY_TAG\"}"`.
- Apply the same tag to every created resource wherever the OCI command supports
  freeform tags. Never create a managed resource without the tag.

## Out of host capacity is normal

`Out of host capacity` on A1 is contested free capacity, not a mistake. Retry the
same launch against each availability domain from
`oci iam availability-domain list`, then retry later or drop to 1 OCPU / 6 GB.
**Never resolve it by switching to a non-A1 shape** — that is the billable "fix".

## Verify, then persist

Verify the launched shape against what was requested — do not assume the API
honoured it:

```bash
oci compute instance get --instance-id "$INSTANCE_ID" --query 'data.{state:"lifecycle-state",
  shape:shape, ocpus:"shape-config".ocpus, memory:"shape-config"."memory-in-gbs", region:region}'
```

Wrong shape, OCPUs, memory or region: terminate immediately, billing is hourly.

```bash
oci compute instance terminate --instance-id "$INSTANCE_ID" \
  --preserve-boot-volume false --force --wait-for-state TERMINATED
```

Keep returned OCIDs only in the current shell. The final report must come from
the post-create tagged snapshot, not intended commands: list each new resource's
truncated OCID, name, type, lifecycle state, region, and free-tier status, plus
anything skipped, failed, or already present.

Report what was created, the verified shape, and the home region, then point at
`${CLAUDE_PLUGIN_ROOT}/docs/staying-free.md` for the budget alert.
