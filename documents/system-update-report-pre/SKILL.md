---
name: system_update_report_pre
description: Maintains the ansible/roles/system_update_report_pre Ansible role that reports (without applying) pending dnf updates, optionally emailing/PDF-reporting the list, as part of the Linux SOE. Use when asked what updates are pending without installing them — see system_update for the role that actually applies updates.
---

# system_update_report_pre

Maintains `ansible/roles/system_update_report_pre/`. See `docs/ARCHITECTURE.md` for the shared
conventions (role layout, audit vs. remediate via `--check --diff`, safety
rules, branch + PR contribution workflow).

`ansible/roles/system_update_report_pre/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/system_update_report_pre/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/system_update_report_pre/policy-<short-desc>` or
  `soe/system_update_report_pre/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/system_update_report_pre/defaults/main.yml`:

- Read-only by construction — it lists what `dnf update` *would* install,
  it never runs the update itself, so this role behaves the same under
  `--check` and without it.
- `system_update_report_pre_display_updates`/`_email_report`/`_pdf` mirror
  `system_update`'s equivalent flags (all default `false`) but describe
  pending, not applied, updates — same PDF caveat: generated on the control
  host, needs `enscript`/`ghostscript` there.

This role is sourced from the myllynen/rhel-ansible-roles import
(see `git log -- ansible/roles/system_update_report_pre`) rather than hand-authored for this
repo. Unlike the original reference domains (e.g. `timesync`, `usbguard_setup`),
it applies state declaratively via standard Ansible modules and does **not**
add its own `assert`-based drift checks on top — an audit here is exactly
what `--check --diff` reports from the underlying modules, nothing more.

## What to do

**Audit** (read-only, safe to run any time):

```
ansible-playbook ansible/update_rhel.yml --tags system_update_report_pre --check --diff
```

Summarize the diff output and any failed tasks in plain language. Since this
role never changes anything, `--check` is mostly cosmetic here — the same
command without `--check` reports the same pending-update list, it's just
no longer the convention this repo's other roles use, so keep using
`--check --diff` for consistency:

```
ansible-playbook ansible/update_rhel.yml --tags system_update_report_pre
```

**Propose a change to the role itself**: never edit and commit directly. On a
branch named `soe/system_update_report_pre/<short-desc>`, edit `ansible/roles/system_update_report_pre/`, validate
locally (`--syntax-check`, `ansible-lint roles/system_update_report_pre/`, and
`--check --diff` against a real/test host if available), then push and open a
PR titled `[system_update_report_pre] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Wiring into the SOE

This role has a row in `.claude/skills/soe/SKILL.md`'s domain table. It
runs as part of `ansible/update_rhel.yml` (active, uncommented, alongside
`system_update` which stays commented — see that role's `SKILL.md`), not
the general host baseline: it's absent from `ansible/configure_rhel.yml`
entirely. This repo no longer uses `ansible/site.yml`; see
`docs/ARCHITECTURE.md`.
