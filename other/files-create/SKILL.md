---
name: files_create
description: Maintains the ansible/roles/files_create Ansible role that creates directories, empty files, and symlinks with specified ownership/mode via ansible.builtin.file, as part of the Linux SOE. Use when checking or fixing the existence/permissions of specific paths.
---

# files_create

Maintains `ansible/roles/files_create/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/files_create/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/files_create/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/files_create/policy-<short-desc>` or
  `soe/files_create/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/files_create/defaults/main.yml`:

This is a low-level, list-driven building block used both directly (a host
sets `files_create` in group_vars/host_vars) and indirectly (e.g. `certificates`
includes `files_remove` internally for its exclusive-mode cleanup). Default
is always an empty list — no-op until something sets it.
- Each entry's `state` (`directory`/`file`/`link`) determines which of three
  registered result variables it contributes to: `create_directories`,
  `create_files`, `create_links`.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/files_create`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

This role is **not** in `ansible/configure_rhel.yml`'s `roles:` list at all
(not even commented out) — it's currently wired in only by the two NFS
composite playbooks, each setting `files_create` itself rather than relying
on this role's (empty) defaults. Pick whichever matches the host:

- **NFS client** — `ansible/nfs_client_setup.yml` creates the mount point
  directory (`nfs_mount_dir`, default `/mnt/remote`).
- **NFS server** — `ansible/nfs_server_setup.yml` creates the export
  directory (`nfs_export_dir`, default `/export`).

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/nfs_client_setup.yml --tags files_create --check --diff
ansible-playbook ansible/nfs_server_setup.yml --tags files_create --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the matching playbook without `--check`:

```
ansible-playbook ansible/nfs_client_setup.yml --tags files_create
ansible-playbook ansible/nfs_server_setup.yml --tags files_create
```

If a host needs `files_create` for something outside these two scenarios,
either add it (uncommented, with its own `vars:`) to
`ansible/configure_rhel.yml`, or write a small dedicated playbook via the
branch + PR workflow below.

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/files_create/<short-desc>`, edit `ansible/roles/files_create/`, validate
locally (`--syntax-check`, `ansible-lint roles/files_create/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[files_create] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Wiring into the SOE

This role has a row in `.claude/skills/soe/SKILL.md`'s domain table but is
**not** part of the general baseline (`ansible/configure_rhel.yml`) — it
only runs as part of `ansible/nfs_client_setup.yml` or
`ansible/nfs_server_setup.yml`. This repo no longer uses `ansible/site.yml`;
see `docs/ARCHITECTURE.md`.
