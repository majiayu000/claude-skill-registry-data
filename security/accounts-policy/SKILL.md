---
name: accounts_policy
description: Maintains the ansible/roles/accounts_policy Ansible role that deploys local account, login, PAM, and password-quality configuration (login.defs, pwquality.conf, faillock.conf, limits.conf, authselect profile) on RHEL-family systems as part of the Linux SOE. Use when checking or changing local account/authentication policy.
---

# accounts_policy

Maintains `ansible/roles/accounts_policy/`. See `docs/ARCHITECTURE.md` for
the shared conventions (role layout, `--check --diff`, safety rules).

`ansible/roles/accounts_policy/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/accounts_policy/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/accounts_policy/policy-<short-desc>` or
  `soe/accounts_policy/workload-<short-desc>`), same branch + PR workflow as
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

This role does **not** assert individual policy values (e.g. it never
checks "is `PASS_MAX_DAYS` 90?"). It deploys whole config files from
role-provided templates/files, each independently optional — any variable
left unset in `defaults/main.yml` means that file is left untouched:

- `useradd_defaults_file` → `/etc/default/useradd`
- `login_defs_config_file` → `/etc/login.defs`
- `login_access_config_file` → `/etc/security/access.conf`
- `faillock_config_file` → `/etc/security/faillock.conf`
- `pwhistory_config_file` → `/etc/security/pwhistory.conf`
- `pwquality_config_file` → `/etc/security/pwquality.conf`
- `limits_config_file` → `/etc/security/limits.conf`
- `user_resource_limits` (list) → `/etc/security/limits.d/95-ansible.conf`
- `system_auth_profile` (+ `system_auth_profile_parameters`) → installs
  `authselect`, optionally copies a `custom/*` profile to
  `/etc/authselect/custom`, and runs `authselect select -f <profile>
  <parameters>` if the currently-selected profile doesn't match
- `system_auth_pam_d_su_file` → `/etc/pam.d/su`

Each variable's docstring in `defaults/main.yml` lists the role-provided
template alternatives (e.g. `login_defs_config_file` can be
`login.defs_cis_rhel89.j2`, `login.defs_rhel_rhel8.j2`, etc. — pick per
RHEL major version and compliance target). Nothing is configured out of
the box: every one of these is unset by default.

## What to do

> **This role is off by default** in `ansible/configure_rhel.yml` — every
> role there (active or not) is gated by a single `configure_rhel_domains`
> list variable (`when: "'<name>' in configure_rhel_domains"`), and `accounts_policy`
> isn't in the default value of that list. Nothing needs editing in the
> playbook itself to turn it on: pass the *full* desired domain list via
> `-e`, e.g.
> `-e '{"configure_rhel_domains": [...the default 20..., "accounts_policy"]}'`
> (see `.claude/skills/configure_rhel/SKILL.md` for the current default list
> to extend, and why it has to be the full list, not just the addition —
> `-e` replaces the variable's value, it doesn't merge into it). `--tags accounts_policy`
> alone is **not** enough — the domains list and `--tags`/`--skip-tags` are
> separate, ANDed gates, both verified independently: a role only runs if
> it's in `configure_rhel_domains` *and* matches the requested tags. Some
> roles (this one — check its `defaults/main.yml` and task file) also have
> their own internal enable flag or required variable on top of that, which
> still needs setting the same as before. Flag all of this to the user before
> assuming the commands below will do anything.

**Audit**: `ansible-playbook ansible/configure_rhel.yml --tags accounts_policy --check --diff`.
Note: the `authselect current`/`authselect check` steps are
`command` tasks — they run under `--check` (marked `check_mode: false`) so
drift there is still visible, but the `authselect select` task itself is a
normal `command` and is skipped under `--check`, so a check run won't show
its own diff.

**Remediate**: same command without `--check`, only after explicit user
approval and after confirming which template/profile variables are
actually set — an unset variable is a no-op, not a "use defaults" signal.

**Propose a change to the role itself**: never commit directly. On a
branch named `soe/accounts_policy/<short-desc>`, edit the role, validate
locally (`--syntax-check`, `ansible-lint roles/accounts_policy/`,
`--check --diff`), push, and open a PR titled
`[accounts_policy] <what changed>` with the `--check --diff` output in the
body — then stop for human review. See `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- This role has no built-in drift detection for password aging, empty
  passwords, duplicate UIDs, or `NOPASSWD:ALL` sudoers entries — none of
  that is checked or reported. If that kind of auditing is needed, it has
  to be added to the role first (propose via the branch/PR workflow), not
  assumed to already happen.
- `system_auth_profile_parameters` is a raw string appended to `authselect
  select`, e.g. `with-mkhomedir with-pamaccess` — get this right, a typo'd
  parameter is silently accepted by `authselect` in some cases.
- Sudoers edits made manually (not by this role — this role doesn't touch
  sudoers at all) should always go through `visudo -c`.
