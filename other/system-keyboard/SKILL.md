---
name: system_keyboard
description: Maintains the ansible/roles/system_keyboard Ansible role that sets the console keymap and console font (via /etc/vconsole.conf, localectl, setfont, and an initramfs rebuild) on RHEL-family systems as part of the Linux SOE. Use when checking or setting the virtual console keymap/font. Does not manage X11 keyboard layout — there is no X11 handling in this role.
---

# system_keyboard

Maintains `ansible/roles/system_keyboard/`. See `docs/ARCHITECTURE.md` for
the shared conventions.

`ansible/roles/system_keyboard/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/system_keyboard/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/system_keyboard/policy-<short-desc>` or
  `soe/system_keyboard/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/system_keyboard/defaults/main.yml`:

- `system_keyboard` (default `us`): checked against `/etc/vconsole.conf`'s
  `KEYMAP=` line via a `check_mode: true` `lineinfile` probe; if not
  already set, applies via `localectl set-keymap`.
- `system_font` (default `eurlatgr`): same pattern for `FONT=`, but
  applied by directly rewriting the line with `replace` (not
  `localectl`) and then running `setfont` to apply it live.
- Installs `kbd` and `kbd-misc` first.
- If the package install, keymap change, or font change did anything,
  rebuilds the initramfs with `dracut -f --regenerate-all`.

## What to do

> **This role is off by default** in `ansible/configure_rhel.yml` — every
> role there (active or not) is gated by a single `configure_rhel_domains`
> list variable (`when: "'<name>' in configure_rhel_domains"`), and `system_keyboard`
> isn't in the default value of that list. Nothing needs editing in the
> playbook itself to turn it on: pass the *full* desired domain list via
> `-e`, e.g.
> `-e '{"configure_rhel_domains": [...the default 20..., "system_keyboard"]}'`
> (see `.claude/skills/configure_rhel/SKILL.md` for the current default list
> to extend, and why it has to be the full list, not just the addition —
> `-e` replaces the variable's value, it doesn't merge into it). `--tags system_keyboard`
> alone is **not** enough — the domains list and `--tags`/`--skip-tags` are
> separate, ANDed gates, both verified independently: a role only runs if
> it's in `configure_rhel_domains` *and* matches the requested tags. Some
> roles (this one — check its `defaults/main.yml` and task file) also have
> their own internal enable flag or required variable on top of that, which
> still needs setting the same as before. Flag all of this to the user before
> assuming the commands below will do anything.

**Audit**: `ansible-playbook ansible/configure_rhel.yml --tags system_keyboard --check --diff`.
The keymap/font check tasks use `lineinfile` in `check_mode: true`
internally (a self-contained probe), so they report accurately regardless
of the outer `--check` flag — but the `localectl`, `setfont`, and `dracut`
tasks are normal `command` tasks and are skipped entirely under the outer
`--check`, so an audit run won't show their effect, only whether they'd
run.

**Remediate**: same command without `--check`, after explicit user
approval. A `dracut -f --regenerate-all` full initramfs rebuild is
comparatively slow and runs whenever the package install, keymap, or font
task reports changed — factor that into how disruptive a remediate run is
expected to be.

**Propose a change to the role itself**: never commit directly. On a
branch named `soe/system_keyboard/<short-desc>`, edit the role, validate
locally (`--syntax-check`, `ansible-lint roles/system_keyboard/`,
`--check --diff`), push, and open a PR titled
`[system_keyboard] <what changed>` with the `--check --diff` output in the
body — then stop for human review. See `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes

- There is no X11 keyboard layout management in this role at all — it is
  virtual-console only. Most SOE targets are headless servers, which is
  presumably why, but don't describe this role as covering X11 layout.
- `system_font` is applied via a hand-written `replace` on
  `/etc/vconsole.conf`, not `localectl set-font`/an equivalent — if a
  future systemd/`localectl` adds first-class font management, this task
  is the one to revisit.
