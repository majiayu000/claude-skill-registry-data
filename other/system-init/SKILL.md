---
name: system_init
description: Maintains the ansible/roles/system_init Ansible role that performs optional post-install cleanup actions (reboot and/or syslog message), as part of the Linux SOE. Use when asked about post-installation initialization steps — the role's own README states it is by no means mandatory.
---

# system_init

Maintains `ansible/roles/system_init/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/system_init/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/system_init/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/system_init/policy-<short-desc>` or
  `soe/system_init/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/system_init/defaults/main.yml`:

- `system_init_final_actions` (default: `[reboot, syslog]`) — `localhost`
  is excluded from the reboot action regardless of this list (per the role's
  own default comment).

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/system_init`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/configure_rhel.yml --tags system_init --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`:

```
ansible-playbook ansible/configure_rhel.yml --tags system_init
```

> **Behavior change from the old `ansible/site.yml`:** this role is now
> **active by default** in `ansible/configure_rhel.yml`'s `roles:` list —
> unlike the old baseline playbook, which deliberately excluded it (see
> "Wiring into the SOE" below). A full, untagged
> `ansible-playbook ansible/configure_rhel.yml` run now reboots the host
> as a side effect, because `reboot` is in `system_init_final_actions`'
> default list. Flag this loudly before anyone runs the full baseline
> playbook without `--tags` against a host they don't expect to reboot.

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/system_init/<short-desc>`, edit `ansible/roles/system_init/`, validate
locally (`--syntax-check`, `ansible-lint roles/system_init/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[system_init] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- Because `reboot` is in the default action list, running this role for the
  first time on a host reboots it — confirm before including it in a
  remediate run, same as any other reboot-by-default role in this repo
  (`boot_parameters`... no, `boot_parameters` is audit-only; think
  `system_locale`, `ipv6_setup`, `multipath_setup`).

## Wiring into the SOE

This role is in `configure_rhel_domains`'s **default** value in
`ansible/configure_rhel.yml` (see `.claude/skills/configure_rhel/SKILL.md`)
— this is the opposite of its old status under `ansible/site.yml`, where
it was deliberately excluded from the default `roles:` list (see the
"excluded from the default run" table this repo used to keep in
`.claude/skills/soe/SKILL.md`) because it acts unconditionally with no
guard variable and reboots the host. That exclusion doesn't apply to
`configure_rhel.yml`: a plain, untagged
`ansible-playbook ansible/configure_rhel.yml` run now **does** reboot the
host via this role. If a host needs `configure_rhel.yml`'s baseline
without the reboot, either run with `--tags` excluding `system_init`
(`--skip-tags system_init`), pass a `configure_rhel_domains` list that
leaves `system_init` out, or override `system_init_final_actions` to
drop `reboot` for that host/group. Don't assume this role is a safe no-op
the way it was when `site.yml` was the entrypoint. This repo no longer
uses `ansible/site.yml`; see `docs/ARCHITECTURE.md`.
