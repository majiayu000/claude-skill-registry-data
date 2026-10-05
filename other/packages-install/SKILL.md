---
name: packages_install
description: Maintains the ansible/roles/packages_install Ansible role that installs a baseline package set via dnf, as part of the Linux SOE. Use when checking or fixing the baseline troubleshooting/utility package set — note this is distinct from the troubleshooting_tools role, which manages a different, smaller package list plus optional PCP.
---

# packages_install

Maintains `ansible/roles/packages_install/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/packages_install/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/packages_install/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/packages_install/policy-<short-desc>` or
  `soe/packages_install/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/packages_install/defaults/main.yml`:

- `packages_install` ships a pre-populated default list (acl, bash-completion,
  bind-utils, curl, dnf-plugins-core, man-pages, nano, openssh-clients, psmisc,
  python3, python3-libselinux, policycoreutils-python-utils, tar, xz, zstd) —
  several common extras (git-core, mlocate, rsync, sos, vim-enhanced, wget,
  etc.) are present but commented out, not installed by default.
- `packages_install_exclude` (default empty) is passed as dnf's `exclude`.
- `packages_install_weak_deps` (default `true`) maps to dnf's
  `install_weak_deps`.
- `packages_install_display_results` (default `false`) — when `true`, prints
  the list of packages actually installed.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/packages_install`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/configure_rhel.yml --tags packages_install --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`:

```
ansible-playbook ansible/configure_rhel.yml --tags packages_install
```

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/packages_install/<short-desc>`, edit `ansible/roles/packages_install/`, validate
locally (`--syntax-check`, `ansible-lint roles/packages_install/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[packages_install] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Wiring into the SOE

This role is in `configure_rhel_domains`'s default value in
`ansible/configure_rhel.yml` (see `.claude/skills/configure_rhel/SKILL.md`)
for the general host baseline, and has a row in
`.claude/skills/soe/SKILL.md`'s domain table, so it runs as part of both
`ansible-playbook ansible/configure_rhel.yml --tags packages_install ...` and a full,
untagged `ansible-playbook ansible/configure_rhel.yml` run. This repo no longer
uses `ansible/site.yml` as the baseline entrypoint — see `docs/ARCHITECTURE.md`.

The same role is **also** invoked by `ansible/load_balancer_setup.yml` and `ansible/nfs_client_setup.yml` and `ansible/nfs_server_setup.yml`, each with its own
purpose-specific variables set directly in that playbook (not this role's
`defaults/main.yml`) — e.g. a different package list or file/service set for a
load balancer or NFS host than the general baseline uses. When asked to
audit/remediate `packages_install` on a host, check which of these playbooks actually
applies to that host's role before picking one; running the wrong playbook's
vars against it reports drift against the wrong intent.
