---
name: ipv6_setup
description: Maintains the ansible/roles/ipv6_setup Ansible role that enables/disables IPv6 via sysctl, the ipv6.disable grubby boot parameter, and NetworkManager/ifcfg connection files, and reboots on change, as part of the Linux SOE. Use when checking or fixing IPv6 enablement.
---

# ipv6_setup

Maintains `ansible/roles/ipv6_setup/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/ipv6_setup/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/ipv6_setup/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/ipv6_setup/policy-<short-desc>` or
  `soe/ipv6_setup/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/ipv6_setup/defaults/main.yml`:

- `ipv6_setup_enable` (default `true`) drives all three layers: sysctl
  (`net.ipv6.conf.{all,default,lo}.disable_ipv6` written to
  `/etc/sysctl.d/50-ipv6.conf`), the `ipv6.disable` grubby kernel argument
  (removed via `grubby --remove-args` when found, regardless of the target
  state — i.e. this role actively edits boot parameters, unlike
  `boot_parameters` which is audit-only), and (if
  `ipv6_setup_configure_nm: true`, the default) `IPV6INIT`/`method=` in any
  ifcfg/NetworkManager connection files found.
- `ipv6_setup_loopback_persist` (default `false`) — when disabling IPv6, keeps
  it enabled on loopback unless this stays false.
- Installs `grubby` first if missing (needed before repos may be configured,
  per the role's own comment).
- Reboots automatically whenever any of the boot-param, sysctl, ifcfg, or
  NM-connection tasks report changed — there is no separate opt-out flag for
  this reboot (unlike `boot_parameters_reboot`/`system_locale_reboot`
  elsewhere in this repo).

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/ipv6_setup`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/configure_rhel.yml --tags ipv6_setup --check --diff
```

Summarize the diff output and any failed tasks in plain language.

**Remediate** (modifies the system — only after the user explicitly asks):
first summarize what will change from the `--check --diff` output, then run
the same command without `--check`:

```
ansible-playbook ansible/configure_rhel.yml --tags ipv6_setup
```

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/ipv6_setup/<short-desc>`, edit `ansible/roles/ipv6_setup/`, validate
locally (`--syntax-check`, `ansible-lint roles/ipv6_setup/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[ipv6_setup] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- Unlike `boot_parameters` (audit-only by design because a bad edit can leave
  a host unbootable), this role directly edits the boot command line **and**
  reboots by default. Get explicit confirmation before a real remediate run —
  there's no `-e` flag here to suppress the reboot.

## Wiring into the SOE

This role is in `configure_rhel_domains`'s default value in
`ansible/configure_rhel.yml` (see `.claude/skills/configure_rhel/SKILL.md`)
and has a row in `.claude/skills/soe/SKILL.md`'s domain table, so it runs as
part of both `ansible-playbook ansible/configure_rhel.yml --tags ipv6_setup ...` and
a full, untagged `ansible-playbook ansible/configure_rhel.yml` run. This repo
no longer uses `ansible/site.yml` as the baseline entrypoint — see
`docs/ARCHITECTURE.md`.
