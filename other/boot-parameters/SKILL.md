---
name: boot_parameters
description: Maintains the ansible/roles/boot_parameters Ansible role that enables/disables GRUB kernel command-line parameters via grubby, sets the boot timeout and optional bootloader password, and can reboot the host to apply changes, on RHEL-family systems as part of the Linux SOE. Use when checking or changing kernel boot parameters. NOT audit-only — remediation is automatic and can trigger a reboot.
---

# boot_parameters

Maintains `ansible/roles/boot_parameters/`. See `docs/ARCHITECTURE.md` for
the shared conventions. **This role remediates and can reboot the host —
it is not audit-only.**

`ansible/roles/boot_parameters/README.md` documents this role's full
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
git log -1 --format='%cI %h %s' -- ansible/roles/boot_parameters/
```

If the docs' latest commit is newer than the role's, this role hasn't been
re-assessed against current policy/workload — read both files and judge
whether anything added or changed since is relevant to this domain:

- **Relevant** — propose a concrete change on a branch
  (`soe/boot_parameters/policy-<short-desc>` or
  `soe/boot_parameters/workload-<short-desc>`), same branch + PR workflow as
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

Encoded in `ansible/roles/boot_parameters/defaults/main.yml`:

- Installs `grubby`; ensures `/etc/default/grub` exists.
- `boot_parameters_enable` (default `[quiet]`) / `boot_parameters_disable`
  (default `[debug, rhgb]`): checked against `GRUB_CMDLINE_LINUX` in
  `/etc/default/grub` (**not** the running kernel's `/proc/cmdline**), and
  if anything's missing/present-that-shouldn't-be, applies via `grubby
  --update-kernel=ALL --args=... --remove-args=...` for **all** installed
  kernels.
- `boot_parameters_timeout` (default `1`): sets `GRUB_TIMEOUT` via a
  straight `replace`, unconditionally, every run, as long as it's an
  integer ≥ 1.
- `boot_parameters_password` (unset by default): if set, writes a
  `GRUB2_PASSWORD=...` file to `user.cfg` (path depends on BIOS/UEFI and
  RHEL major version); if explicitly set falsy, removes that file.
- Regenerates the boot config with `grub2-mkconfig` whenever the timeout,
  password file, or password removal changed.
- **If `boot_parameters_reboot: true` (the default) and the `grubby`
  command changed anything, reboots the host immediately** — no separate
  confirmation gate inside the role itself.

## What to do

**Audit**: `ansible-playbook ansible/configure_rhel.yml --tags boot_parameters --check --diff`.
The enable/disable checks use `lineinfile` in `check_mode: true` internally
(a self-contained probe, not the outer `--check` flag) so they always
report accurately; the `grubby`/`grub2-mkconfig`/reboot tasks are normal
tasks and will correctly no-op/simulate under the outer `--check`.

**Remediate**: same command without `--check`. Because
`boot_parameters_reboot` defaults to `true`, running this without
`--check` and without first setting `boot_parameters_reboot: false` **can
reboot the target host as soon as any enable/disable parameter changes**
— always get explicit user confirmation before a real remediate run, and
default to `-e boot_parameters_reboot=false` if the user wants the change
applied but the reboot deferred to a manual, reviewed window.

**Propose a change to the role itself**: never commit directly. On a
branch named `soe/boot_parameters/<short-desc>`, edit the role, validate
locally (`--syntax-check`, `ansible-lint roles/boot_parameters/`,
`--check --diff`), push, and open a PR titled
`[boot_parameters] <what changed>` with the `--check --diff` output in the
body — then stop for human review. See `docs/ARCHITECTURE.md`'s
"Contribution workflow".

## Notes — read before touching this role

- This is the highest-blast-radius role in the SOE alongside
  `usbguard_setup`: a bad `boot_parameters_enable`/`_disable` entry can
  leave a host that fails to boot, and the role's default behavior is to
  apply the grubby change **and reboot in the same run** — there is no
  built-in "propose only" mode. Treat `boot_parameters_reboot: true`
  remediate runs the same way you'd treat any other host-impacting change
  requiring explicit approval.
- `GRUB_TIMEOUT` is rewritten every single run regardless of whether it
  already matches — this task has no idempotent "only if different" guard
  beyond the `replace` module's own no-op-if-unchanged behavior, so
  `boot_config`/timeout diffs will show even when nothing meaningfully
  changed if the file didn't already contain a `GRUB_TIMEOUT=` line in the
  expected form.
