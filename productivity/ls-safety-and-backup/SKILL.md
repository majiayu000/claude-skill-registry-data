---
name: ls-safety-and-backup
description: "Security and safety (conservative), backup management, temporary file management, firewall management. Use for destructive ops, system config changes, backups, temp files, or when adding services."
metadata:
  version: "1.1"
---

# Safety, Backup, Temp Files, Firewall

Use this skill as an instruction-only safety gate for destructive operations,
system configuration changes, backups, temporary files, and service exposure.
It does not ship shell helpers. When automation is added, implement it as
Python framework tooling that follows `ls/docs/TOOLING_POLICY.md` and
`ls/docs/INPUT_HARDENING_STANDARD.md`.

## Safety Gate

- **Default posture:** Favor data safety, least privilege, and reversible
  changes over convenience.
- **Classify risk before acting:**
  - **CRITICAL:** Data loss, disk operations, credential exposure, user/group
    deletion, broad permission changes, recursive deletion, or changes under
    `/usr`, `/etc`, `/bin`, `/sbin`, or comparable system paths.
  - **HIGH:** Firewall changes, system service changes, package removal,
    privileged installation, or changes that affect every user on the host.
  - **MEDIUM:** Application-level changes, repo-local generated state, or
    service restarts with limited blast radius.
  - **LOW:** Read-only inspection and clearly reversible local edits.
- **Confirm CRITICAL/HIGH work:** State the exact command or edit, likely
  consequences, affected users/services/files, rollback path, and safer manual
  option. Proceed only after explicit confirmation.
- **Prefer dry runs:** Use read-only discovery, `--check`, `--dry-run`,
  `--diff`, or equivalent modes when a tool supports them.

## Backup Workflow

- **Back up first:** Before editing sensitive config or persistent state, copy
  the original to the same directory or a user-approved backup directory using
  `original_filename.YYYYMMDD_HHMMSS.backup`.
- **Preserve metadata:** Keep ownership, mode, timestamps, and symlink behavior
  clear. Use platform tools that preserve metadata when that matters.
- **Handle large files deliberately:** For files larger than 100 MB, warn about
  disk impact and ask whether to back up, snapshot, or skip.
- **Verify rollback:** Before making the change, confirm the backup exists and
  describe the restore command or manual restore step.
- **Respect user choice:** If the user declines a backup for the current
  session, state that residual risk before continuing.

## Temporary Files

- **Use safe locations:** Prefer repo-local ignored temp directories for
  project work, or the platform temp directory for disposable host work.
- **Use unique names:** Include a short task label and timestamp or use the
  platform's secure temp-file creation API.
- **Clean up promptly:** Remove temp files when the operation completes. In
  Python tooling, use `tempfile.TemporaryDirectory()` or `try`/`finally` for
  cleanup.
- **Avoid secrets in temp files:** If unavoidable, restrict permissions,
  minimize lifetime, and delete the file before reporting completion.

## Firewall And Service Exposure

- **Do not assume a firewall tool:** Detect the host policy first. Common
  controls include UFW, firewalld, nftables, cloud security groups, container
  network rules, and reverse proxy ACLs.
- **Default scope is narrow:** Prefer loopback or LAN-only exposure unless the
  user explicitly asks for public internet access.
- **Document every rule:** Record service name, port, protocol, allowed source
  range, reason, and rollback command before applying a change.
- **Validate after change:** Check the service bind address, active firewall
  rule, and connectivity from the intended source only.
- **Rollback ready:** Keep the exact command or control-plane action needed to
  remove the rule.

## Automation Policy

- This skill currently provides guidance only; it has no `scripts/` directory
  and no helper library API.
- Do not invent references to unshipped helpers or missing docs.
- New helpers must be Python, use explicit argument parsing, reject unsafe
  command strings, emit actionable stderr on failure, and avoid shell
  interpolation of untrusted input.
