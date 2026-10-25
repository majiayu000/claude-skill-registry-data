---
name: ls-system-changes-backup
description: "Security and safety (conservative), backup management, temporary file management, firewall management. Use for backup confidence reports, isolated recovery exercises, destructive ops, system config changes, backups, temp files, or when adding services."
metadata:
  version: "1.2"
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
  option. Proceed only with explicit authorization covering the named targets,
  destructive scope, consequences, and recovery strategy. Reuse an applicable
  current request or existing grant; routine implementation choices within that
  scope do not require another confirmation. Ask when authority is missing or
  materially exceeded, while retaining native permissions, authentication,
  revocation, and any exact-command or lifetime restrictions on the grant.
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

## Backup and recovery confidence

Use this guided review when someone asks whether their backups are working or
whether they could recover important data. It works with their chosen backup
product; do not install a product, start a backup, or restore data just to produce
this report. Read the existing product's status and records within the approved
scope. Keep credentials, filenames containing personal data, and raw logs private.

1. Confirm the protected data, intended recovery outcome, acceptable data age,
   and review interval with the user or their existing policy. Inventory scope
   and exclusions before claiming completeness. If no age policy exists, report
   the evidence's age and mark its freshness as unchecked rather than inventing
   a threshold.
2. Report three separate observations, each with its timestamp, protected scope,
   evidence source, result, and age against the selected policy:
   - **Latest backup:** the latest attempt and its outcome, plus the latest
     successful recovery point. A later failed attempt must remain visible.
   - **Latest verification:** what the product checked (such as archive integrity
     or readability), which recovery point it checked, and any omissions.
   - **Recovery exercises:** the latest attempt and its outcome, plus the most
     recent successful exercise with its date and tested scope. For each, show
     what was restored, where it was tested, which recovery point was used, and
     which operational acceptance checks passed. A later failed or partial
     exercise must not hide an older successful restore or refresh its age.
3. Label each observation `passed`, `failed`, `missing`, or `unknown`; report
   freshness separately as `current`, `outdated`, or `unchecked`. A recent copy
   does not refresh an old verification or restore exercise. A passed integrity
   check does not demonstrate recovery. Missing evidence is not a pass.
4. Explain the resulting confidence in plain language: for example, "Yesterday's
   backup succeeded; archive integrity was checked last month; recovery has not
   been demonstrated." Give the next useful action and the specific unproven
   steps. A partial restore proves only its tested scope, not complete recovery.

A compact report can use this format without including raw private evidence:

```text
Protected scope: <approved data and recovery outcome>
Latest attempt: <time, outcome>; latest successful backup: <time or unknown>
Verification: <time, recovery point, checks, outcome, omissions>
Latest recovery attempt: <time, recovery point, scope, acceptance result>
Latest successful exercise: <time, recovery point, proven scope or none>
Freshness: <policy and separate assessment for each observation>
Unproven or blocked: <missing access, exclusions, failed or untested steps>
Next action: <smallest useful verification or isolated exercise>
```

## Guided recovery exercise

Prepare the exercise before asking to execute any consequential operation.
Choose a separate scratch destination or isolated test environment with enough
capacity; never overwrite the originals, active service data, or the only backup.
Review the selected recovery point, access requirements, encryption-key access,
expected contents, restore command from the backup product's verified procedure,
and acceptance checks. Keep outbound integrations disabled so restored services
cannot send messages or change production state. Preserve existing authority;
a backup review alone does not authorize service interruption or destructive work.

Restore only within the approved scope. Check representative content and
integrity, permissions and ownership where relevant, then test the intended
application behavior without changing the source. Record elapsed time, recovery
point age, tested scope, failures, and remaining steps. Report a failed or
incomplete exercise accurately. Clean up only exercise-owned resources after
results are retained and cleanup is authorized; do not remove recovery evidence
or the backup itself.

For machine, account, or environment recovery, load the common operation policy's
"Complete recovery" procedure. Independent access to recovery credentials and a
clean-host restore are required before claiming complete disaster recovery. This
guided report does not certify an untested product or replace that procedure.
