---
name: relqis
description: Shared operating rules for using the rlq CLI safely in a Relqis workspace.
---

# Goal

Use `rlq` as the only accounting write interface for a Relqis workspace.

This bundled skill is the runtime entry point for agent behavior in a Relqis
workspace. Workspace-specific choices such as database path, approval rules,
account naming, and use-case policy belong in `AGENTS.md`.

# Scope

- Shared rules across corporation, self-employed, and household bookkeeping workflows.
- Read-first, auditable CLI operation through stable `--json` output.
- Installed reference files under `references/` for detailed runtime guidance.

# Responsibility split

- Bundled skill:
  common Relqis operating model, immutable posted entries, read-first workflow, JSON contract, and period-end safety.
- `AGENTS.md`:
  workspace-specific default database path, use-case choice, approval conditions, account conventions, user-term-to-internal-name mappings, and ask-the-user rules.
- Installed references:
  detailed runtime guidance for operator rules, error recovery, and period-end work.

# Installed references

- `references/README.md`:
  index of the runtime reference set that is installed together with this skill.
- `references/operator-rules.md`:
  detailed execution model, write safety, read-side verification, and approval boundaries.
- `references/error-recovery.md`:
  how to classify CLI failures, when to retry, and when to stop and ask.
- `references/period-end.md`:
  month-close, year-close, carryforward, and export sequencing.
- `references/decision-tables.md`:
  when to stop, what to ask, and which kinds of guessing are not allowed.
- `references/transaction-mapping.md`:
  practical mapping patterns from user input or external data to Relqis operations.

Consult the relevant reference file before acting when the task involves:

- close, reopen, carryforward, export, or other period-end operations
- CLI failures, conflicts, or policy violations
- deciding whether to continue automatically or stop for human confirmation

# Core rules

- Use `rlq` for every accounting state change. Do not edit SQLite tables directly.
- If `AGENTS.md` declares a default database path, treat it as the workspace default and do not require the user to repeat it in every request.
- If `AGENTS.md` contains a vocabulary map such as "現金 -> <workspace account code>", use that only for internal execution. Keep user-facing communication in Japanese accounting terms.
- Prefer `--json` on executable leaf commands.
- Explore with `rlq --help`, `rlq <group> --help`, and `rlq <group> <leaf> --help`.
- There is no dedicated `init` command. If the database file does not exist yet, the first `rlq --database-path PATH ...` command creates it and bootstraps the schema automatically.
- Read first, then write, then verify.
- Manual entry still flows through `PostingRequest` semantics. There is no bypass around posting validation.
- Posted entries are immutable. Use `entry reverse` or `entry void` instead of editing a posted entry.
- Amounts are integer minor units and stay positive. Direction is expressed by `dc_type`.
- When a command accepts `--expected-version`, read the latest version first and pass it explicitly.
- Avoid parallel writers against the same SQLite database.

# Standard workflow

1. Read the relevant workspace policy from `AGENTS.md`.
2. Read the relevant installed reference if the task is specialized.
3. Read the current state with `show`, `list`, or another read-side command.
4. Run at most one state-changing command at a time.
5. Verify the result with another read command.
6. Explain the result to the user in Japanese accounting terms.

# Recommended workflows

## Bootstrap a new database

1. If the parent directory already exists, run a cheap read command such as `rlq --database-path data/company.db fiscal-period list --json`
2. Treat that first command as both connectivity check and schema bootstrap
3. Then continue with normal read-first investigation for the requested work

## Manual entry

1. `rlq entry create ... --json`
2. `rlq entry show ENTRY_ID --json`
3. `rlq entry post ENTRY_ID --expected-version VERSION --posting-date DATE --json`

## Staged posting

1. `rlq postreq preview --input-file FILE --json`
2. `rlq postreq create --input-file FILE --json`
3. `rlq postreq show POSTING_REQUEST_ID --json` or `rlq postreq work --json`
4. `rlq postreq validate --posting-request-id POSTING_REQUEST_ID --entry-id ENTRY_ID --json`
5. `rlq entry show ENTRY_ID --json`
6. `rlq entry post ENTRY_ID --expected-version VERSION --posting-date DATE --json`

## Month close

1. `rlq check close --closing-type month_close ... --json`
2. If the workspace policy requires it, confirm tax review before closing.
3. `rlq close month ... --reason REASON --requested-by OPERATOR --json`

## Year close and carryforward

1. `rlq check close --closing-type year_close ... --json`
2. `rlq close year preview ... --closing-account-id ACCOUNT_ID --reason REASON --json`
3. `rlq close year run ... --closing-account-id ACCOUNT_ID --reason REASON --requested-by OPERATOR --json`
4. `rlq check close --closing-type carryforward ... --json`
5. `rlq carryforward preview ... --reason REASON --json`
6. `rlq carryforward run ... --reason REASON --requested-by OPERATOR --json`

## Export

1. `rlq export-profile show EXPORT_PROFILE_ID --json`
2. `rlq export validate ... --json`
3. `rlq export run ... --requested-by OPERATOR --json`
4. `rlq export show EXPORT_RUN_ID --json`

# Output contract

- Success JSON is written to stdout as `{"success":true,"data":...}`.
- Failure JSON is written to stderr as `{"success":false,"error":{"code":...,"category":...,"message":...}}`.
- Stable exit codes:
  - `0` success
  - `2` invalid request or validation error
  - `3` not found
  - `4` conflict or optimistic concurrency error
  - `5` posting policy or master policy violation
  - `6` period or state transition violation
  - `7` persistence, audit, or other internal failure

# Ask the user before

- Creating or changing master data when mapping is ambiguous.
- Choosing between `reverse` and `void` for a posted entry.
- Running close, reopen, carryforward, or export operations.
- Proceeding when required dimensions cannot be satisfied or policy violations remain.
- Classifying a transaction when business, household, private, or allocation boundaries are unclear.

# User-facing wording

- Prefer user-facing Japanese accounting terms such as "現金", "普通預金", "売上高", "売掛金", "未払金", "月次締め", "年次締め", and "繰越".
- Do not require the user to know internal command names, account codes, export profile IDs, or closing account IDs.
- When a user uses a Japanese accounting term and the workspace has a corresponding internal identifier, translate it internally and continue.
- When the mapping is unknown, inspect existing masters first. If still ambiguous, ask the user using Japanese accounting terms rather than internal identifiers.
