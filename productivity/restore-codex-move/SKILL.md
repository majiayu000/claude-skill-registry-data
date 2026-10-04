---
name: restore-codex-move
description: Inspect, verify, transactionally restore, and audit a Codex migration package on a new computer. Use when the user has transferred Codex “行李”, a codex-move ZIP or age-encrypted package, and asks to receive, import, unpack, restore, or complete a move on macOS, Windows, or Linux.
---

# Restore Codex Move

Verify first, show an exact plan, obtain confirmation, restore transactionally, and produce an auditable report.

## Workflow

1. Read [migration-policy.md](references/migration-policy.md). Select exactly one complete interaction contract from the user's language:
   - Simplified Chinese → [zh-CN](references/user-interaction-zh.md)
   - English → [en-US](../../locales/en-US/restore.md)
   - Japanese → [ja-JP](../../locales/ja-JP/restore.md)
   - Traditional Chinese → [zh-Hant](../../locales/zh-Hant/restore.md)
   Read the selected contract completely and use its prompts, confirmation gates, error translations, and result states. Do not mix locales.
2. Confirm the exact package path. Obtain the separately carried SHA-256 and, for `.age`, the identity file.
3. Resolve Python 3.11 or newer and `age` when decrypting.
4. Inspect without changing the destination:

   ```bash
   python3 "<skill-directory>/scripts/restore_codex_move.py" \
     "/absolute/path/codex-move.zip" --expected-sha256 "<sha256>"
   ```

5. Summarize verification, source/destination OS, actions, deferred categories, conflicts, encryption, transaction guarantees, and remaining authorization/toolchain work.
6. Ask for explicit confirmation before `--apply`. Also require explicit confirmation for:
   - `--include-history`;
   - `--include-automations` (files still go to quarantine);
   - `--apply-review-config`;
   - cross-OS history or review config overrides.
7. Prefer a cold restore. If feasible, give the user the final command with `--require-codex-stopped` to run after quitting Codex. Otherwise apply atomically and require an immediate restart:

   ```bash
   python3 "<skill-directory>/scripts/restore_codex_move.py" \
     "/absolute/path/codex-move.zip" --expected-sha256 "<sha256>" --apply
   ```

8. Report the backup, quarantine, review, and restore-report paths. Never claim success unless `verification.ok` is true.
9. Restart Codex, sign in again, confirm memory discovery, invoke one restored Skill, parse the restored config, and review the report.
10. Use the report's managed-plugin list to reinstall through supported plugin management and reauthorize connectors. Review MCP/Hooks and quarantined automations before activation. Recreate missing secrets outside the migration package.
11. Transfer or clone projects separately; reconcile paths, architecture, package managers, runtimes, Git hooks, and OS permissions.

If the user returns after restarting and asks to “验收刚才的恢复” with a restore-report path, read that report and perform steps 9–11 only. Do not inspect or apply the package again.

## Conflict and activation policy

- Identical files: skip.
- Changed non-memory files: back up, then replace.
- Changed memory files: preserve the destination and import the incoming version under `memories/imports/<package-id>/`.
- Destination-only files: preserve.
- Portable preferences: deep-merge into current config and back up the original.
- MCP/Hooks/review config: always save a redacted review copy; merge only with explicit flags.
- Automations: always restore under `move-quarantine`; never activate automatically.
- Managed plugins/connectors: reinstall and reauthorize; never copy caches or credentials.

## Non-negotiable safety

- Never restore auth, secrets, keychains/keyrings, raw config, caches, logs, databases, UI state, or source absolute paths.
- Reject unsupported schemas, unsafe paths, duplicates, case collisions, undeclared members, excessive sizes, hash mismatches, and symlinked ancestors.
- Stage and hash every write before commit; back up conflicts; roll back committed files if the transaction fails.
- Never delete destination-only data or destructively mirror directories.
- Treat memory restoration as one-time local migration, not continuous synchronization.
- Do not promise historical conversations will reappear in the UI.

## Communication contract

- Follow the exact localized contract selected in workflow step 1. Infer the locale from the user's current language; if the user explicitly requests a locale, that request wins.
- Never expose raw script JSON as the user-facing answer. Translate plan actions and preserve exact paths, hashes, package IDs, backup paths, and report paths.
- Announce inspection, staging, backup, commit, verification, and report phases. For long operations, update every 30–60 seconds without invented percentages.
- Require the localized confirmation phrase defined by the selected product contract before `--apply`; require separate confirmation for history, automations, review-config merge, and cross-OS overrides.
- End in exactly one state: verified-success, success-with-follow-up, safely-refused-without-write, failed-and-rolled-back, or rollback-incomplete.
- Never say “fully restored” before restart and post-restore acceptance checks.

## Resources

- Run [restore_codex_move.py](scripts/restore_codex_move.py).
- Read [migration-policy.md](references/migration-policy.md) for supported/deferred state.
- Read [package-format.md](references/package-format.md) when diagnosing schemas or recovery.
- Read exactly one user-facing contract for each run: [zh-CN](references/user-interaction-zh.md), [en-US](../../locales/en-US/restore.md), [ja-JP](../../locales/ja-JP/restore.md), or [zh-Hant](../../locales/zh-Hant/restore.md).
