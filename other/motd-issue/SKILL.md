---
name: motd_issue
description: Maintains the ansible/roles/motd_issue Ansible role that deploys /etc/motd (or /etc/motd.d on RHEL 9+) and /etc/issue.d + /etc/issue.net from role-provided templates on RHEL-family systems as part of the Linux SOE. Use when checking or standardizing login banners. Does NOT manage the sshd pre-auth banner.
---

# motd_issue

Maintains `ansible/roles/motd_issue/`. See `docs/ARCHITECTURE.md` for the
shared conventions.

`ansible/roles/motd_issue/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/motd_issue/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/motd_issue/policy-<short-desc>` or
  `soe/motd_issue/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/motd_issue/defaults/main.yml` — both variables
are unset by default, so out of the box this role does nothing:

- `issue_template` (if set) → rendered to **both**
  `/etc/issue.d/zz-ansible.issue` and `/etc/issue.net` (the same template,
  same content, two destinations).
- `motd_template` (if set) → rendered to `/etc/motd.d/zz-ansible.motd` on
  RHEL 9+, or directly to `/etc/motd` on RHEL 8.

## What to do

> **This role is off by default** in `ansible/configure_rhel.yml` — every
> role there (active or not) is gated by a single `configure_rhel_domains`
> list variable (`when: "'<name>' in configure_rhel_domains"`), and `motd_issue`
> isn't in the default value of that list. Nothing needs editing in the
> playbook itself to turn it on: pass the *full* desired domain list via
> `-e`, e.g.
> `-e '{"configure_rhel_domains": [...the default 20..., "motd_issue"]}'`
> (see `.claude/skills/configure_rhel/SKILL.md` for the current default list
> to extend, and why it has to be the full list, not just the addition —
> `-e` replaces the variable's value, it doesn't merge into it). `--tags motd_issue`
> alone is **not** enough — the domains list and `--tags`/`--skip-tags` are
> separate, ANDed gates, both verified independently: a role only runs if
> it's in `configure_rhel_domains` *and* matches the requested tags. Some
> roles (this one — check its `defaults/main.yml` and task file) also have
> their own internal enable flag or required variable on top of that, which
> still needs setting the same as before. Flag all of this to the user before
> assuming the commands below will do anything.

**Audit**: `ansible-playbook ansible/configure_rhel.yml --tags motd_issue --check --diff`

**Remediate**: same command without `--check`, after explicit user
approval.

**Propose a change to the role itself** (e.g. adding the org's approved
banner template): never commit directly. On a branch named
`soe/motd_issue/<short-desc>`, edit the role, validate locally
(`--syntax-check`, `ansible-lint roles/motd_issue/`, `--check --diff`),
push, and open a PR titled `[motd_issue] <what changed>` with the
`--check --diff` output in the body — then stop for human review. See
`docs/ARCHITECTURE.md`'s "Contribution workflow".

## Notes

- **This role does not touch `sshd_config` or the SSH pre-auth banner.**
  If the org needs the SSH pre-auth banner (`Banner` directive) to match
  `/etc/issue.net`, that's a gap in the role today, not something already
  handled — flag it rather than assuming it's covered.
- Neither `motd_template` nor `issue_template` has role-provided
  alternatives shipped in `files/`/`templates/` (unlike `accounts_policy`
  or `audit_setup`) — the org's banner content has to be supplied
  entirely externally (a template path outside this role, or a new file
  added to the role first).
- If the approved banner text is supplied, avoid `\v`/`\r`/`\m`/`\s`
  escape sequences in the issue content — those leak kernel/OS version to
  an unauthenticated user at the pre-auth banner (this is a property of
  `/etc/issue`/`/etc/issue.net` content itself, not something the role
  enforces).
