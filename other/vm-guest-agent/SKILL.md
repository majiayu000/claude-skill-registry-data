---
name: vm_guest_agent
description: Maintains the ansible/roles/guest_agent Ansible role (this skill is named vm_guest_agent, but the actual role directory is guest_agent — see the note in the file body) that detects the hypervisor a system runs under and installs/enables the matching guest agent (qemu-guest-agent, open-vm-tools, hyperv-daemons/WALinuxAgent) as part of the Linux SOE, removing guest-agent packages on bare metal or unrecognized/Nutanix virtualization instead. Use when checking guest-agent presence or state on a virtual machine.
---

# vm_guest_agent

Maintains `ansible/roles/guest_agent/` (see the naming-mismatch note under
"What to do" below — this skill is named `vm_guest_agent`, but the actual
role directory, and the tag that works against every playbook in this
repo, are both `guest_agent`). See `docs/ARCHITECTURE.md` for the shared
conventions. Unlike most domains, this role branches on detected
virtualization type rather than checking one fixed baseline.

`ansible/roles/guest_agent/README.md` documents this role's full
configuration surface (every `defaults/main.yml` variable, with its
original inline comments, rendered as a single reference). Read it before
proposing or explaining how to configure this role — it reflects the
role's actual current defaults even if a variable summary elsewhere in
this file has drifted out of sync with the role.

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

## Baseline

`guest_agent_enable` (default `true`) is the only real on/off switch —
there is no per-hypervisor mapping variable to override; which package/
service applies is resolved entirely inside `tasks/main.yml` from
`ansible_facts.virtualization_type`/`virtualization_role`/`system_vendor`,
not from anything in `defaults/main.yml`. `guest_agent_remove_firmware`
(default `true`) separately controls whether VM firmware packages
(`*firmware*` families) get removed on guest hosts.

Actual behavior by detected virtualization (verified directly against
`tasks/main.yml`, not assumed):

- `virtualization_role != "guest"` (bare metal, or `guest_agent_enable:
  false`) → **actively removes** `hyperv*`, `open-vm-tools`,
  `qemu-guest-agent`, `spice-vdagent`, `WALinuxAgent` if present. This is
  enforcement, not a passive `[INFO]` report — a host that used to be a VM
  and is now bare metal gets cleaned up on the next run.
- `system_vendor == "Nutanix"` (AHV) → all guest-agent packages are
  **removed**, none installed. Nutanix AHV doesn't use any of the
  packages this role manages, so this is deliberate, not an oversight.
- `virtualization_type == "kvm"` (and not Nutanix) → installs
  `qemu-guest-agent`, enables + starts `qemu-guest-agent.service`; removes
  the other platforms' packages first.
- `virtualization_type == "VirtualPC"` (Hyper-V/Azure) → installs
  `hyperv-daemons` **and** `WALinuxAgent`, enables + starts
  `waagent.service`; removes the other platforms' packages first.
- `virtualization_type == "VMware"` → installs `open-vm-tools`, enables +
  starts `vmtoolsd.service`; removes the other platforms' packages first.
- Any other guest type (not `kvm`/`VirtualPC`/`VMware`, not Nutanix) →
  removes all known guest packages, installs nothing — there's no generic
  fallback agent, unlike what a naive reading of "detects and installs
  the matching agent" might suggest.

## What to do

> **Known naming mismatch** (pre-existing, not introduced by this change):
> the actual role directory and the tag used by `configure_rhel.yml`'s
> `roles:` list are both `guest_agent`, not `vm_guest_agent` — see
> `.claude/skills/guest_agent/SKILL.md` and the note in
> `.claude/skills/soe/SKILL.md`'s domain table ("role dir is `guest_agent`,
> not `vm_guest_agent`"). `--tags vm_guest_agent` will report "did not
> match any tags" against every playbook in this repo. Use `--tags
> guest_agent` (see that skill) until this mismatch is resolved, or flag it
> to a human operator as something worth fixing via the branch + PR
> workflow.

**Audit**: `ansible-playbook ansible/configure_rhel.yml --tags guest_agent --check --diff`

**Remediate**: same command without `--check`, after explicit user
approval.

**Propose a change to the role itself** (e.g. adding a new hypervisor to
the `agent_packages`/`agent_services` dicts in `tasks/main.yml`): never
commit directly. On a branch named `soe/guest_agent/<short-desc>` (the
role's real name — see the naming-mismatch note above), edit
`ansible/roles/guest_agent/`, validate locally (`--syntax-check`,
`ansible-lint roles/guest_agent/`, `--check --diff`), push, and open a PR
titled `[guest_agent] <what changed>` with the `--check --diff` output in
the body — then stop for human review. See `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- The per-hypervisor package/service mapping is hardcoded in
  `tasks/main.yml` (`agent_packages`/`agent_services` dicts), not exposed
  as a `defaults/main.yml` variable — there's nothing to override via
  `-e` or group_vars for a new hypervisor type, only a role code change.
- If `ansible_facts.virtualization_type` is something not covered by the
  role's dicts (`kvm`, `VirtualPC`, `VMware`) but the user says the host
  is a VM, ask rather than assuming — on an uncovered guest type the role
  removes every known guest package and installs nothing, which could
  surprise someone expecting *some* agent to end up installed.
