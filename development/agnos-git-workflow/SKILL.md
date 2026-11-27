---
name: agnos-git-workflow
description: "AGNOS process GIT workflow skill. Handles all git operations mandated by the AGNOS process: 'start-session' creates and checks out a feature branch; 'commit-task' stages and commits changes with the correct AGNOS message format. USE FOR: START SESSION step 8 (branch creation) and DoD commit step (task commit). Validates all artifact IDs before executing any git command."
argument-hint: "start-session <TRI> | commit-task <TASK-ID> [<ADR-ID>] <description>"
---

# AGNOS Git Workflow

Deterministic git operations for the AGNOS process. All artifact IDs are validated before any
git command is executed. <!-- RQ-PLG-005 --> `<skill-folder>` is the folder holding this file;
run every command from the project's root.

## Script Selection

Every validation step below runs a `<validate-ids>` script. Select it from `session.platform`
(read `agnos-process/_sessionstate/session.yaml` first if not already in context):

| `session.platform` | Command |
|---|---|
| `windows` | `powershell -NoProfile -File <skill-folder>/scripts/validate-ids.ps1 -Type <T> -Value <V>` |
| `linux` / `macos` | `bash <skill-folder>/scripts/validate-ids.sh -Type <T> -Value <V>` |

Use `powershell` (Windows PowerShell 5.1), never `pwsh` — PowerShell 7 is not guaranteed to be
installed.

## Sub-Commands

### `start-session <TRI>` — Feature Branch Creation

**When to use**: START SESSION step 8 — at the beginning of every new session.

**Procedure:**

1. Validate `<TRI>` by running `<validate-ids>` (see Script Selection) with `-Type TRI -Value <TRI>`.
   If exit code ≠ 0: report the validation error and STOP. Do NOT proceed.

2. Check whether the branch already exists:
   ```
   git show-ref --quiet refs/heads/feature/<TRI>
   ```
   - **Does NOT exist** (exit code ≠ 0): run `git checkout -b feature/<TRI>` then confirm to the user.
   - **Already exists** (exit code = 0): ask the user how to proceed. Options:
     - (a) Check it out: `git checkout feature/<TRI>`
     - (b) Reset to current HEAD: `git checkout feature/<TRI> && git reset --hard HEAD`
     - (c) Delete and recreate
     - (d) Use a different trigram
   - Wait for explicit confirmation before executing any option.

---

### `commit-task <TASK-ID> [<ADR-ID>] <description>` — Task Commit

**When to use**: DoD commit step — when a task is marked Done.

**Commit message format** (single source of truth for the AGNOS commit-message grammar — do not
restate this elsewhere): `<type>(<TRI>): <ADR-ID>/<TASK-ID> <description>` when an ADR-ID was
given, otherwise `<type>(<TRI>): <TASK-ID> <description>`, where:
- `<type>` is a Conventional-Commits type (`feat` | `fix` | `docs` | `refactor` | `test` |
  `chore` | `perf` | `build` | `ci` | `style`) inferred from the nature of the change — do not
  ask the user unless genuinely ambiguous.
- `<TRI>` is the trigram parsed out of `<TASK-ID>`.
- **During a RECURSIVE SELF-IMPROVEMENT SESSION**: append an `Iteration: <k>/<N>` trailer, e.g.
  `docs(USR): ADR-USR-001/TASK-USR-001 <description>` with trailer `Iteration: 1/5`.
- **When an agent commits**: one single `Co-Authored-By: <Harness>/<Model> <e-mail>` trailer, in place of the tool's
  own attribution, e.g. `Co-Authored-By: Claude Code/Claude Opus 5.5 <noreply@anthropic.com>`. The `<commit-task>`
  script writes it, and the message, from your arguments (step 6). <!-- RQ-HST-030 / DEC-HST-013 -->

**Procedure:**

1. Parse the arguments:
   - First token → TASK-ID
   - If second token matches `ADR-*` → ADR-ID; remaining tokens → description
   - Otherwise → no ADR-ID; all remaining tokens → description

2. Validate TASK-ID using `<validate-ids>` (see Script Selection) with `-Type TASK -Value <TASK-ID>`.
   If exit code ≠ 0: report the error and STOP.

3. If ADR-ID was provided, validate it using `<validate-ids>` with `-Type ADR -Value <ADR-ID>`.
   If exit code ≠ 0: report the error and STOP.

4. Refresh the process index by invoking the `agnos-index` skill. <!-- RQ-IDX-012 -->
   If exit code ≠ 0: report the error or duplicates and STOP. Do NOT commit.

5. Determine `<type>`, then stage the task's files by name with `git add <paths>`, never `git add .`, which would take
   the user's unrelated changes.

6. Never write the message yourself, nor run `git commit` directly: the `<commit-task>` script builds it.
   <!-- RQ-HST-030 / DEC-HST-013 --> Run it with `-DryRun`:

   | `session.platform` | Command |
   |---|---|
   | `windows` | `powershell -NoProfile -File <skill-folder>/scripts/commit-task.ps1 <arguments> -DryRun` |
   | `linux` / `macos` | `bash <skill-folder>/scripts/commit-task.sh <arguments> -DryRun` |

   `<arguments>`: `-Task <TASK-ID> [-Adr <ADR-ID>] -Type <type> -Description "<description>" -Harness "<harness>"
   -Model "<model>" -Email "<e-mail>" [-Iteration <k>/<N>]`. Harness, model and e-mail are yours, as your tool gives
   them; `auto` when the model is chosen dynamically. Then confirm the printed message with the user:
   > "About to commit: `<message>`. Proceed?"
   Wait for confirmation.

7. Run the same command without `-DryRun`: it commits the staged files and prints the hash. Confirm the hash to the
   user. Exit code 1: report its error and STOP.
