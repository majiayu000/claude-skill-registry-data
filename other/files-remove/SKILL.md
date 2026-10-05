---
name: files_remove
description: Maintains the ansible/roles/files_remove Ansible role that removes files/directories by exact path or shell glob, as part of the Linux SOE. Use when checking or fixing which files/directories should be absent — including internally by other roles such as certificates for exclusive-mode cleanup.
---

# files_remove

Maintains `ansible/roles/files_remove/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/files_remove/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/files_remove/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/files_remove/policy-<short-desc>` or
  `soe/files_remove/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/files_remove/defaults/main.yml`:

This is a low-level, list-driven building block used both directly (a host
sets `files_remove` in group_vars/host_vars) and indirectly (e.g. `certificates`
includes `files_remove` internally for its exclusive-mode cleanup). Default
is always an empty list — no-op until something sets it.
- Supports globbing on the last path element; directories are removed
  recursively. `files_remove_recursive` (default `false`) additionally does a
  recursive `find` for the given patterns — the role's own comment warns this
  makes a pattern like `/etc/*.old` also match `/etc/x/y.old`.
  `files_remove_exclude` protects specific paths from a glob/recursive match.
  Result registered as `remove_files`.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/files_remove`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

This role is **not referenced by any playbook in `ansible/`** right now —
not `configure_rhel.yml` (not even commented out), not
`load_balancer_setup.yml`/`nfs_client_setup.yml`/`nfs_server_setup.yml`/
`update_rhel.yml`. There is currently no `ansible-playbook` command that will
invoke `files_remove` in this repo. Before running it, either:

1. **Add it to an existing playbook** — most often
   `ansible/configure_rhel.yml`'s `roles:` list (uncomment-style, with a
   `vars:` entry for `files_remove` set to what's actually needed), if what's wanted is
   a permanent, repeatable part of the host baseline; or
2. **Write a small ad hoc playbook** for the one-off task, same shape as
   `ansible/load_balancer_setup.yml`/`ansible/nfs_client_setup.yml` (a
   `vars:` block plus a `roles: [files_remove]` list), if it's a one-time or
   host-class-specific job that doesn't belong in the general baseline.

Either way, propose it via the branch + PR workflow below rather than running
an untracked local playbook against a real host. Once wired in, audit/remediate
the same way as any other role — `--tags files_remove` against whichever playbook now
contains it, `--check --diff` first:

```
ansible-playbook ansible/<playbook>.yml --tags files_remove --check --diff   # audit
ansible-playbook ansible/<playbook>.yml --tags files_remove                  # remediate
```

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/files_remove/<short-desc>`, edit `ansible/roles/files_remove/`, validate
locally (`--syntax-check`, `ansible-lint roles/files_remove/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[files_remove] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- The role's own defaults file carries an explicit warning: a typo or
  unexpected glob expansion here can remove unintended files/directories
  across every managed host with no confirmation prompt. Always review the
  literal expanded pattern (not just the pattern string) in the
  `--check --diff` output before remediating, and be especially careful with
  `files_remove_recursive: true`.

## Wiring into the SOE

This role has a row in `.claude/skills/soe/SKILL.md`'s domain table, but (see
"What to do" above) is not currently included in any playbook in this repo —
neither the general baseline (`ansible/configure_rhel.yml`) nor any of the
composite playbooks. This repo no longer uses `ansible/site.yml`; see
`docs/ARCHITECTURE.md`.
