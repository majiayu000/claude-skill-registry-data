---
name: update_rhel
description: Runs ansible/update_rhel.yml to report pending dnf updates on a RHEL-family host, and optionally apply them, as part of the Linux SOE. Use when asked what updates are pending, or to patch/update a host — as distinct from the general host baseline (configure_rhel.yml), which does not touch package updates at all.
---

# update_rhel

Runs `ansible/update_rhel.yml`, a purpose-built playbook pairing the
`system_update_report_pre` role (active by default) with the
`system_update` role (commented out by default). See
`docs/ARCHITECTURE.md` for the six-playbook layout this fits into, and
each role's own `SKILL.md` for full detail — `system_update_report_pre`
and `system_update`.

## Policy & workload awareness

This playbook doesn't own an `ansible/roles/<name>/` directory of its
own — it reuses `system_update_report_pre`, `system_update`, each of which already carries its own
policy/workload staleness check in its own `SKILL.md` (see
`docs/ARCHITECTURE.md`'s "Policy & workload awareness"). What's specific to
*this* playbook is the `update_rhel.yml`-specific variables set directly
there rather than in any role's own `defaults/main.yml` — check whether
those need updating too:

```
git log -1 --format='%cI %h %s' -- docs/POLICY.md docs/WORKLOAD.md
git log -1 --format='%cI %h %s' -- ansible/update_rhel.yml
```

If the docs are newer than the playbook file, re-read both docs with this
specific workload in mind (not just the general-baseline case each
underlying role's own check considers) before assuming nothing needs to
change.

## What the playbook actually does

Encoded directly in `ansible/update_rhel.yml`'s `vars:` block:

- `system_update_reboot_policy` (default `when_needed`, checked via `dnf
  needs-restarting`) and `system_update_display_updates: true` — these
  configure `system_update`, but since that role is commented out of the
  `roles:` list by default, they currently have no effect until it's
  uncommented.
- `system_update_report_pre_display_updates: true` — configures the
  active role, so its output actually is displayed by default.
- `roles:` lists `system_update_report_pre` active, `system_update`
  commented out (`#- system_update`) directly below it.

By default, running this playbook **only reports** what dnf would update —
it never actually updates anything, because the one role that applies
updates is commented out. This is deliberate (see `system_update`'s
`SKILL.md`) — the same behavior the old `site.yml` achieved by leaving
`system_update` off its `roles:` list entirely, just implemented here as a
commented-out line in a dedicated playbook instead.

## What to do

**Report pending updates** (safe, read-only by construction — no `--check`
needed, though it's harmless to include for consistency):

```
ansible-playbook ansible/update_rhel.yml
```

Summarize the reported package list in plain language.

**Apply updates** (modifies the system, can reboot the host — only after
the user explicitly asks, and only after uncommenting `system_update` in
`ansible/update_rhel.yml`'s `roles:` list):

```
ansible-playbook ansible/update_rhel.yml --tags system_update --check --diff   # audit first
ansible-playbook ansible/update_rhel.yml --tags system_update                  # then apply
```

Confirm `system_update_reboot_policy` with the user before applying —
`when_needed`/`when_updated`/`always` can all reboot the host as part of
this run; `never` will not.

**Propose a change to this playbook**: never edit and commit directly. On a
branch named `soe/update_rhel/<short-desc>`, edit `ansible/update_rhel.yml`,
validate locally (`--syntax-check`, `--check --diff` against a real/test
host if available), then push and open a PR titled
`[update_rhel] <what changed>` with the `--check --diff` output in the
body. Then stop — a human reviews and merges; see `docs/ARCHITECTURE.md`'s
"Contribution workflow". Don't uncomment `system_update` permanently in
this playbook without an explicit decision from a human operator —
fleet-wide auto-patching needs a deliberate choice, not a default.

## Notes

- Under `--check`, `system_update`'s `dnf update *` doesn't perform the
  update, so `needs-restarting`-based reboot-policy evaluation during an
  audit reflects pre-update state — `--check --diff` here previews *what*
  would update, not reliably *whether* a reboot would follow. See that
  role's own `SKILL.md`.
- `system_update_report_pre` and `system_update` both support emailing
  and/or PDF-reporting the update list (`_email_report`, `_pdf`) — the PDF
  option needs `enscript`/`ghostscript` on the **control host**, not the
  target, and both default `false` here.
