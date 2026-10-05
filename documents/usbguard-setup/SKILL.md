---
name: usbguard_setup
description: Maintains the ansible/roles/usbguard_setup Ansible role that installs USBGuard and enables/starts its service by default with a reject-all policy on RHEL-family systems as part of the Linux SOE. Use when checking or configuring USB device allow/block policy via usbguard. There is NO opt-in gate on service enablement — enforcement is on by default with policy=reject.
---

# usbguard_setup

Maintains `ansible/roles/usbguard_setup/`. See `docs/ARCHITECTURE.md` for
the shared conventions — this is the role with the highest blast radius in
the SOE. **Read this whole file before running remediate on any host with
only physical console access.**

`ansible/roles/usbguard_setup/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/usbguard_setup/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/usbguard_setup/policy-<short-desc>` or
  `soe/usbguard_setup/workload-<short-desc>`), same branch + PR workflow as
  any other role change (see "What to do" above and
  `docs/ARCHITECTURE.md`'s "Contribution workflow"). Don't wait to be
  asked.
- **Not relevant** — say so explicitly (e.g. "checked against
  `docs/POLICY.md` and `docs/WORKLOAD.md` as of `<date>`, nothing affecting
  this domain") rather than silently skipping the check.

This check is informational, not a gate — it runs alongside a normal
audit/remediate, never blocks one; surface the staleness note alongside
the normal output.

## What the role actually does — service enablement is NOT opt-in

Encoded in `ansible/roles/usbguard_setup/defaults/main.yml`:

- `usbguard_setup_policy` (default `reject`): `reject` (default-deny, all
  connected devices blocked), `custom` (use
  `usbguard_setup_config_file`/`_rules_file`/`_ipc_access_file`), or
  `allow` (**disable** USBGuard and allow all USB devices).
- **There is no `soe_usbguard_manage_service`-style opt-in variable in
  this role.** Whenever `usbguard_setup_policy != 'allow'` (i.e. the
  default `reject`, or `custom`), the role installs USBGuard, writes the
  policy config, **enables and starts `usbguard.service`
  unconditionally**. With the default `policy: reject` and default
  `rules.conf` handling below, running this role's remediate path on an
  unconfigured host applies a default-block USB policy and turns on
  enforcement in the same run.
- If `usbguard_setup_rules_file` is unset (the default), the role writes
  an **empty** `/etc/usbguard/rules.conf` — it does **not** run
  `usbguard generate-policy` to seed an allow-list from currently-attached
  devices. Combined with default `policy: reject` and unconditional
  service enablement, the out-of-the-box remediate behavior is: empty
  allow-list + reject-all + service started — which can block *all* USB
  devices including a keyboard/mouse on a host with only physical console
  access.
- `usbguard_setup_exclusive: true` removes unrecognized rules/IPC files
  not in `usbguard_setup_files_known` via `include_role: files_remove` —
  **that role is not vendored in this repository**; it must be resolvable
  separately for `_exclusive: true` to work.
- `policy: allow` takes the opposite path entirely (`disable.yml`):
  disables and stops `usbguard.service` if the package is present, does
  not touch config files.

## What to do

> **This role is off by default** in `ansible/configure_rhel.yml` — every
> role there (active or not) is gated by a single `configure_rhel_domains`
> list variable (`when: "'<name>' in configure_rhel_domains"`), and `usbguard_setup`
> isn't in the default value of that list. Nothing needs editing in the
> playbook itself to turn it on: pass the *full* desired domain list via
> `-e`, e.g.
> `-e '{"configure_rhel_domains": [...the default 20..., "usbguard_setup"]}'`
> (see `.claude/skills/configure_rhel/SKILL.md` for the current default list
> to extend, and why it has to be the full list, not just the addition —
> `-e` replaces the variable's value, it doesn't merge into it). `--tags usbguard_setup`
> alone is **not** enough — the domains list and `--tags`/`--skip-tags` are
> separate, ANDed gates, both verified independently: a role only runs if
> it's in `configure_rhel_domains` *and* matches the requested tags. Some
> roles (this one — check its `defaults/main.yml` and task file) also have
> their own internal enable flag or required variable on top of that, which
> still needs setting the same as before. Flag all of this to the user before
> assuming the commands below will do anything.

**Audit**: `ansible-playbook ansible/configure_rhel.yml --tags usbguard_setup --check --diff`

**Before any remediate run on a host that is not `policy: allow`**:
confirm with the user (a) they have a non-USB or already-reviewed access
path (remote console, iDRAC/iLO, an already-allow-listed keyboard/mouse),
and (b) whether `usbguard_setup_rules_file` should point at a real,
reviewed rules template — since the default is an empty rules file and
this role enables enforcement in the same run, not a separate step:

```
ansible-playbook ansible/configure_rhel.yml --tags usbguard_setup
```

**To explicitly disable enforcement instead** (allow all USB devices,
service off): set `usbguard_setup_policy: allow`.

**Propose a change to the role itself** — especially anything touching
default service enablement or the empty-rules-file default: never commit
directly, and flag it explicitly in the PR body given this role's blast
radius. On a branch named `soe/usbguard_setup/<short-desc>`, edit the
role, validate locally (`--syntax-check`,
`ansible-lint roles/usbguard_setup/`, `--check --diff`), push, and open a
PR titled `[usbguard_setup] <what changed>` — then stop for human review.
See `docs/ARCHITECTURE.md`'s "Contribution workflow".

## Notes — read before touching this role

- **Do not describe this role's service enablement as opt-in or
  safety-gated — it is not, as currently implemented.** If the user
  expects an opt-in gate (e.g. from prior documentation or another SOE
  role's pattern), flag that mismatch explicitly rather than assuming the
  gate exists.
- Always get explicit confirmation of another access path before a
  remediate run with `policy: reject`/`custom` on a host with only
  physical console access — the empty default `rules.conf` plus
  unconditional service start is the exact combination that can lock out
  a physically-connected keyboard/mouse.
- `usbguard_setup_exclusive: true` depends on an external `files_remove`
  role this repo does not vendor — confirm it's resolvable before relying
  on it.
