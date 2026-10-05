---
name: system_unregister
description: Maintains the ansible/roles/system_unregister Ansible role that unconditionally unregisters a host from Red Hat Insights and Red Hat Subscription Management, as part of the Linux SOE. Use when decommissioning a host or removing it from RHSM/Insights.
---

# system_unregister

Maintains `ansible/roles/system_unregister/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/system_unregister/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/system_unregister/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/system_unregister/policy-<short-desc>` or
  `soe/system_unregister/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/system_unregister/defaults/main.yml`:

- No configuration variables — running this role always attempts to stop
  `rhcd`, unregister `insights-client`, remove Insights state files, run
  `subscription-manager unregister` + `clean`, and remove any RHSM server
  certs under `/etc/containers/certs.d`.
  Each step is conditioned on the relevant package/state actually being
  present (via `package_facts`), so it's safe to run on a host that's already
  partially or fully unregistered.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/system_unregister`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/configure_rhel.yml --tags system_unregister --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`:

```
ansible-playbook ansible/configure_rhel.yml --tags system_unregister
```

Note this only works at all if `system_unregister` has been uncommented in
`ansible/configure_rhel.yml`'s `roles:` list first — see "Wiring into the
SOE" below; by default the tag matches nothing.

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/system_unregister/<short-desc>`, edit `ansible/roles/system_unregister/`, validate
locally (`--syntax-check`, `ansible-lint roles/system_unregister/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[system_unregister] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- This is destructive to the host's ability to get RHEL/Satellite content
  until re-registered via `repository_setup` (or manually) — this is a
  decommissioning action, not something to include in a routine SOE
  compliance run. Confirm the host is actually being decommissioned before
  remediating.

## Wiring into the SOE

This role is **not present at all** in `ansible/configure_rhel.yml`'s
`roles:` list — not even as a commented-out line — nor in any of the other
playbooks (`load_balancer_setup.yml`, `nfs_client_setup.yml`,
`nfs_server_setup.yml`, `update_rhel.yml`, `connect_linux.yml`). This is
deliberate: it acts unconditionally with no guard variable and would
de-register every host it touched, so it must never run as a side effect
of a routine baseline run.

To actually invoke it, add `- system_unregister` directly to
`ansible/configure_rhel.yml`'s `roles:` list yourself before running the
commands above, or write a small dedicated decommissioning playbook —
either way, propose it via the branch + PR workflow, and treat adding it to
`configure_rhel.yml` permanently as a cross-cutting, high-blast-radius
change needing an explicit human decision, same as it was under the old
`ansible/site.yml`. This repo no longer uses `ansible/site.yml`; see
`docs/ARCHITECTURE.md`.
