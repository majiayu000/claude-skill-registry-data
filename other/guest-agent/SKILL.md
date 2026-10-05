---
name: guest_agent
description: Maintains the ansible/roles/guest_agent Ansible role that detects the hypervisor a system runs under (Azure/Hyper-V, KVM/QEMU, Nutanix AHV, VMware) via Ansible facts and installs/enables the matching guest agent while removing others, as part of the Linux SOE. Use when checking guest-agent presence or state on a virtual machine.
---

# guest_agent

Maintains `ansible/roles/guest_agent/` (note: the role directory and role
name are `guest_agent`, not `vm_guest_agent`). See `docs/ARCHITECTURE.md`
for the shared conventions. Unlike most domains, this role branches on
detected virtualization facts rather than checking one fixed baseline.

`ansible/roles/guest_agent/README.md` documents this role's full
configuration surface (every `defaults/main.yml` variable, with its
original inline comments, rendered as a single reference). Read it
before proposing or explaining how to configure this role — it
reflects the role's actual current defaults even if a variable summary
elsewhere in this file has drifted out of sync with the role.

## Policy & workload awareness

`docs/POLICY.md` and `docs/WORKLOAD.md` capture org-wide policy items and
the workloads this SOE actually hosts — either can gain a new or changed
item that this role should reflect. Before auditing, remediating, or
proposing a change, check whether either doc has changed more recently
than this role's own code:

```
git log -1 --format='%cI %h %s' -- docs/POLICY.md docs/WORKLOAD.md
git log -1 --format='%cI %h %s' -- ansible/roles/guest_agent/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/guest_agent/policy-<short-desc>` or
  `soe/guest_agent/workload-<short-desc>`), same branch + PR workflow as
  any other role change (see "What to do" above and
  `docs/ARCHITECTURE.md`'s "Contribution workflow"). Don't wait to be
  asked.
- **Not relevant** — say so explicitly (e.g. "checked against
  `docs/POLICY.md` and `docs/WORKLOAD.md` as of `<date>`, nothing affecting
  this domain") rather than silently skipping the check.

This check is informational, not a gate — it runs alongside a normal
audit/remediate, never blocks one; surface the staleness note alongside
the normal output.

## What the role actually does

Encoded in `ansible/roles/guest_agent/defaults/main.yml`:

- `guest_agent_enable` (default `true`): if `false`, all recognized guest
  agent packages (`hyperv*`, `open-vm-tools`, `qemu-guest-agent`,
  `spice-vdagent`, `WALinuxAgent`) are removed regardless of platform.
- `guest_agent_remove_firmware` (default `true`): on a detected VM guest,
  removes firmware packages (`*firmware*` families, `linux-firmware*` on
  RHEL 9+) that VMs typically don't need — VMs using device passthrough
  may need to set this `false`.

Detection uses `ansible_facts.virtualization_role`,
`ansible_facts.virtualization_type`, and `ansible_facts.system_vendor`
(not `systemd-detect-virt` output text) — the role gathers these facts
itself if not already present:

- `virtualization_type == 'kvm'` (and `system_vendor != 'Nutanix'`) →
  `qemu-guest-agent` package + `qemu-guest-agent.service`
- `virtualization_type == 'VMware'` → `open-vm-tools` package +
  `vmtoolsd.service`
- `virtualization_type == 'VirtualPC'` (Azure/Hyper-V) → installs
  `hyperv-daemons` **and** `WALinuxAgent`, but only enables/starts
  `waagent.service` (there is no separate `hypervkvpd.service` handling)
- `system_vendor == 'Nutanix'` with `virtualization_type == 'kvm'` → all
  known agent packages removed, **no agent installed** — Nutanix AHV
  guests are treated as "remove everything," not mapped to an agent
- Any other `virtualization_type`, or `virtualization_role != 'guest'`
  (bare metal, or an unrecognized platform) → all known agent packages
  removed, no agent installed; the role doesn't emit an `[INFO]` message
  for this case, it just silently converges to "no agent"

All package/service tasks use `cacheonly: true, disablerepo: '*'` for
removals (fast, no repo hit) but a normal `dnf install` for the agent
itself.

## What to do

**Audit**: `ansible-playbook ansible/configure_rhel.yml --tags guest_agent --check --diff`

**Remediate**: same command without `--check`, after explicit user
approval.

**Propose a change to the role itself** (e.g. adding a new
hypervisor/vendor mapping): never commit directly. On a branch named
`soe/guest_agent/<short-desc>`, edit the role, validate locally
(`--syntax-check`, `ansible-lint roles/guest_agent/`, `--check --diff`),
push, and open a PR titled `[guest_agent] <what changed>` with the
`--check --diff` output in the body — then stop for human review. See
`docs/ARCHITECTURE.md`'s "Contribution workflow".

## Notes

- Nutanix AHV guests report `virtualization_type: kvm` at the hypervisor
  level, which is why the role checks `system_vendor == 'Nutanix'` first
  to distinguish them from plain KVM/QEMU — get this fact-gathering order
  right if extending the mapping, or Nutanix guests will get
  `qemu-guest-agent` installed instead of having all agents removed.
- If detected virtualization facts don't match what the user says the
  host actually is (e.g. facts say bare metal but the user says it's a
  VM), ask rather than forcing `guest_agent_enable`/manually picking a
  package — installing the wrong guest agent is wasted and can mask a
  fact-gathering problem worth investigating on its own.
