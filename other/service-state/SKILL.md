---
name: service_state
description: Maintains the ansible/roles/service_state Ansible role that masks/unmasks, enables/disables, and restarts/reloads systemd units by declarative lists, as part of the Linux SOE. Use when checking or fixing which services should be running, stopped, or masked.
---

# service_state

Maintains `ansible/roles/service_state/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/service_state/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/service_state/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/service_state/policy-<short-desc>` or
  `soe/service_state/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/service_state/defaults/main.yml`:

- Four independent lists, all defaulting empty:
  `service_state_mask`/`_unmask`/`_disable`/`_enable`, plus
  `service_state_restart` (restart by default per entry, or `state: reloaded`
  with an optional `require:` precondition on current state).
- `sshd`/`sshd.service` are hard-excluded from mask and disable/stop
  regardless of what's listed — the role won't let you lock out SSH access to
  itself.
- An item in both `service_state_mask` and `service_state_unmask`, or both
  `service_state_disable` and `service_state_enable`, resolves to
  "unmask"/"enable" winning.
- `service_state_skip_missing` (default `false`) — an enable/start entry for a
  unit that doesn't exist fails the role by default; set `true` to skip it
  instead.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/service_state`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/configure_rhel.yml --tags service_state --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`:

```
ansible-playbook ansible/configure_rhel.yml --tags service_state
```

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/service_state/<short-desc>`, edit `ansible/roles/service_state/`, validate
locally (`--syntax-check`, `ansible-lint roles/service_state/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[service_state] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- Masking a unit prevents even manual `systemctl start` until unmasked —
  confirm the mask list doesn't include anything another role in this repo
  (e.g. `usbguard_setup`, `audit_setup`) depends on being startable.

## Wiring into the SOE

This role is in `configure_rhel_domains`'s default value in
`ansible/configure_rhel.yml` (see `.claude/skills/configure_rhel/SKILL.md`)
for the general host baseline, and has a row in
`.claude/skills/soe/SKILL.md`'s domain table, so it runs as part of both
`ansible-playbook ansible/configure_rhel.yml --tags service_state ...` and a full,
untagged `ansible-playbook ansible/configure_rhel.yml` run. This repo no longer
uses `ansible/site.yml` as the baseline entrypoint — see `docs/ARCHITECTURE.md`.

The same role is **also** invoked by `ansible/load_balancer_setup.yml` and `ansible/nfs_client_setup.yml` and `ansible/nfs_server_setup.yml`, each with its own
purpose-specific variables set directly in that playbook (not this role's
`defaults/main.yml`) — e.g. a different package list or file/service set for a
load balancer or NFS host than the general baseline uses. When asked to
audit/remediate `service_state` on a host, check which of these playbooks actually
applies to that host's role before picking one; running the wrong playbook's
vars against it reports drift against the wrong intent.
