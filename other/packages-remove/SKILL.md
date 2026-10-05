---
name: packages_remove
description: Maintains the ansible/roles/packages_remove Ansible role that removes a denylist of packages (and optionally unneeded leaf packages) via dnf, as part of the Linux SOE. Use when checking or fixing which packages should be absent.
---

# packages_remove

Maintains `ansible/roles/packages_remove/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/packages_remove/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/packages_remove/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/packages_remove/policy-<short-desc>` or
  `soe/packages_remove/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/packages_remove/defaults/main.yml`:

- `packages_remove` ships a small default denylist (gofer, katello-agent,
  puppet-agent, `rhn*`, telnet-server) — many more (biosdevname, cloud-init,
  NetworkManager-tui, sssd*, etc.) are present but commented out.
- `packages_remove_exclude` (default: `kernel`, `kernel-core`,
  `microcode_ctl`) is always subtracted from the removal set and also passed
  as dnf's own `exclude`, and any package also present in `packages_install`
  is subtracted too — install and remove lists are cross-checked so the two
  roles can't fight each other.
- `packages_remove_autoremove` (default `false`) — separately runs a
  `dnf autoremove`-equivalent pass for orphaned leaf packages.
- Uses `cacheonly: true, disablerepo: '*'` so removal doesn't need repo
  access.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/packages_remove`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/configure_rhel.yml --tags packages_remove --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`:

```
ansible-playbook ansible/configure_rhel.yml --tags packages_remove
```

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/packages_remove/<short-desc>`, edit `ansible/roles/packages_remove/`, validate
locally (`--syntax-check`, `ansible-lint roles/packages_remove/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[packages_remove] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- Several commented-out defaults (`sssd*`, `NetworkManager-tui`, `tcpdump`)
  would be actively disruptive if uncommented on a domain-joined or
  troubleshooting-dependent host — review each addition against what
  `domain_ad`/`troubleshooting_tools` expect to be present before proposing.

## Wiring into the SOE

This role is in `configure_rhel_domains`'s default value in
`ansible/configure_rhel.yml` (see `.claude/skills/configure_rhel/SKILL.md`)
and has a row in `.claude/skills/soe/SKILL.md`'s domain table, so it runs as
part of both `ansible-playbook ansible/configure_rhel.yml --tags packages_remove ...` and
a full, untagged `ansible-playbook ansible/configure_rhel.yml` run. This repo
no longer uses `ansible/site.yml` as the baseline entrypoint — see
`docs/ARCHITECTURE.md`.
