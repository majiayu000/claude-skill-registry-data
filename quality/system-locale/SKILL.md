---
name: system_locale
description: Maintains the ansible/roles/system_locale Ansible role that sets LANG in /etc/locale.conf on RHEL-family systems, restricted to C.UTF-8, en_US.UTF-8, or auto, as part of the Linux SOE. Rebuilds the initramfs and reboots by default when the locale changes. Use when checking or setting the system locale.
---

# system_locale

Maintains `ansible/roles/system_locale/`. See `docs/ARCHITECTURE.md` for
the shared conventions.

`ansible/roles/system_locale/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/system_locale/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/system_locale/policy-<short-desc>` or
  `soe/system_locale/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/system_locale/defaults/main.yml`:

- `system_locale` (default `auto`): **only** `C.UTF-8`, `en_US.UTF-8`, or
  `auto` are accepted — anything else fails the play immediately via an
  explicit `ansible.builtin.fail` task, not an `assert`. `auto` resolves
  to `C.UTF-8` on RHEL 9+ (glibc ships it natively there) or
  `en_US.UTF-8` on RHEL 8.
- Installs `glibc-minimal-langpack`, plus `glibc-langpack-en` if the
  resolved target is `en_US.UTF-8` (either chosen directly, or via `auto`
  on RHEL 8).
- Rewrites `LANG=` in `/etc/locale.conf` via `replace`.
- If that changed, rebuilds the initramfs (`dracut -f --regenerate-all`).
- **If `system_locale_reboot: true` (the default) and the locale changed,
  reboots the host** — same pattern as `boot_parameters`, no separate
  confirmation gate inside the role.

## What to do

**Audit**: `ansible-playbook ansible/configure_rhel.yml --tags system_locale --check --diff`

**Remediate**: same command without `--check`. Because
`system_locale_reboot` defaults to `true`, a remediate run that actually
changes the locale **reboots the host** — get explicit confirmation
first, and consider `-e system_locale_reboot=false` if the user wants the
`/etc/locale.conf` change applied now but the reboot deferred.

**Propose a change to the role itself** (e.g. supporting an additional
locale): never commit directly. On a branch named
`soe/system_locale/<short-desc>`, edit the role, validate locally
(`--syntax-check`, `ansible-lint roles/system_locale/`, `--check --diff`),
push, and open a PR titled `[system_locale] <what changed>` with the
`--check --diff` output in the body — then stop for human review. See
`docs/ARCHITECTURE.md`'s "Contribution workflow".

## Notes

- The role only ever supports exactly three values for `system_locale` —
  it isn't a general-purpose "set any locale" role. Extending it to a
  different language/locale is a role change (new package logic, new
  accepted value), not a variable override.
- Unlike `system_keyboard`, there's no `localectl`-based read here — the
  current locale is read straight from `/etc/locale.conf`.
- If the target locale package isn't installable (bad repo config,
  offline host), the `dnf` task fails loudly rather than silently leaving
  the old locale in place — that's expected, not a role bug to work
  around.
