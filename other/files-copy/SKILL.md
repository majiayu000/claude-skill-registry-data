---
name: files_copy
description: Maintains the ansible/roles/files_copy Ansible role that copies files/directories (ansible.builtin.copy) and renders templates (ansible.builtin.template) to arbitrary destinations, as part of the Linux SOE. Use when checking or fixing the content of specific deployed config files.
---

# files_copy

Maintains `ansible/roles/files_copy/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/files_copy/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/files_copy/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/files_copy/policy-<short-desc>` or
  `soe/files_copy/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/files_copy/defaults/main.yml`:

This is a low-level, list-driven building block used both directly (a host
sets `files_copy / files_copy_templates` in group_vars/host_vars) and indirectly (e.g. `certificates`
includes `files_remove` internally for its exclusive-mode cleanup). Default
is always an empty list — no-op until something sets it.
- Two independent lists: `files_copy` (static source files) and
  `files_copy_templates` (Jinja2 `.j2` templates rendered on the target).
  Results registered as `copy_files`/`copy_templates` respectively.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/files_copy`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

This role is **not** in `ansible/configure_rhel.yml`'s `roles:` list at all
(not even commented out) — it's currently wired in only by the two
purpose-built composite playbooks below, each setting `files_copy` itself
rather than relying on this role's (empty) defaults. Pick whichever
playbook matches what the host actually is:

- **Load balancer host** — `ansible/load_balancer_setup.yml` copies the
  `keepalived-notify-haproxy` script plus renders the haproxy/keepalived
  config templates.
- **NFS server** — `ansible/nfs_server_setup.yml` writes the
  `/etc/exports.d/ansible.exports` content.

> `ansible/load_balancer_setup.yml`'s `files_copy`/`files_copy_templates`
> entries reference `keepalived-notify-haproxy` and three `.j2` templates
> that **don't currently exist anywhere in this repo** — see that
> playbook's `SKILL.md` for the verified gap. Its `files_copy` tasks fail
> with "could not find src" until those assets are added. This doesn't
> affect the NFS server use above, which uses inline `content:` rather
> than a `src:` file reference.

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/load_balancer_setup.yml --tags files_copy --check --diff
ansible-playbook ansible/nfs_server_setup.yml --tags files_copy --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the matching playbook without `--check`:

```
ansible-playbook ansible/load_balancer_setup.yml --tags files_copy
ansible-playbook ansible/nfs_server_setup.yml --tags files_copy
```

If a host needs `files_copy` for something outside these two scenarios,
either add it (uncommented, with its own `vars:`) to
`ansible/configure_rhel.yml`, or write a small dedicated playbook — same
pattern as `load_balancer_setup.yml`/`nfs_server_setup.yml` — via the
branch + PR workflow below.

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/files_copy/<short-desc>`, edit `ansible/roles/files_copy/`, validate
locally (`--syntax-check`, `ansible-lint roles/files_copy/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[files_copy] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Wiring into the SOE

This role has a row in `.claude/skills/soe/SKILL.md`'s domain table but is
**not** part of the general baseline (`ansible/configure_rhel.yml`) — it
only runs as part of `ansible/load_balancer_setup.yml` or
`ansible/nfs_server_setup.yml`, and only for the specific files each of
those playbooks lists in its own `vars:`. This repo no longer uses
`ansible/site.yml`; see `docs/ARCHITECTURE.md`.
