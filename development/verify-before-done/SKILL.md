---
name: verify-before-done
description: "Run the verification gauntlet before claiming a task is complete. Executes build, tests, migration check, generated-model drift check, and HANDOFF completeness check. Blocks on any failure. Use when: an agent or the user is about to declare Status=complete, before committing, before opening a PR, or whenever the phrase 'done', 'complete', 'ready to ship', 'finished' is used. Mandatory final step in /tdd-first and recommended final step in /design-first."
user_invocable: true
---

# /verify-before-done — Pre-Completion Verification Gauntlet

When invoked, run every applicable check below. **Do not report completion to the user or to a calling agent until this skill has been executed and passed.** If any check fails, halt and report the specific failure with its output — never claim "verified" based on partial evidence.

## Context — why this skill exists

Implementer agents (and Claude sessions in general) sometimes close a task with `Status: complete` based on *reading* the code they wrote, not *running* it. The project has four automation layers that catch drift (`concept-gate.py`, `architecture-guard.py`, CI `angular-models-drift.yml`, pre-commit hook) — but those only fire on write or commit. This skill is the runtime counterpart: it proves the claim *before* the user or downstream agent accepts it.

## Step 0: Determine scope

Classify the change by files touched (read `git status` + `git diff --stat`):

Roots come from `.claude/project-profile.md`. Read it first; do not infer a path from a project name.

- **Backend only** — every changed file sits under `backend.roots` → Steps 1, 2, 4, 5.5, 6, 7
- **Frontend only** — every changed file sits under `frontend.roots` → Steps 3, 4, 5.5, 6, 7
- **Full-stack** (both) → all steps
- **Migration** — anything under `migration.root` → Steps 1, 2, 5, 5.5, 6, 7
- **Sidecar or auxiliary runtime** — a language runtime outside `backend.roots` and `frontend.roots` → Steps 8, 5.5, 6, 7
- **Docs only** (`.md`, `.claude/`) → Step 6, 7 only

**Step 5.5 (safety-critical review gate) fires on every non-docs-only scope** — it short-circuits to PASS when no safety-critical path is touched, so it is cheap. See Step 5.5 for the path-to-reviewer mapping.

**Step 5.6 (registry structure lint) fires on every scope, docs-only included**, because a registry file under `.claude/registries/` is a docs-only change that can break the registry layout.

## Steps 1 to 4: the scripted runner first, the prose steps as the fallback

When Step 0 selected any of Steps 1 to 4, try `land_contract.py --verify-here` first. It runs the configured verification steps of this checkout against the failing-test baseline on the default branch, and it is the one test run: **the prose Steps 1 to 3 never run beside it**, because two test runs on one LocalDB would collide. It never pushes, merges, resets, cleans or regenerates anything, so Step 4 (drift) stays the prose regenerate-compare-stage step below, whatever the runner says.

1. **Find the script**, the same way `/advance` finds it:

   ```bash
   LANDER=
   S=.claude/scripts/land_contract.py
   if [ -f "$S" ]; then LANDER=$S
   elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then LANDER=$CLAUDE_PLUGIN_ROOT/$S
   else
     # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
     CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
     ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
     REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
     MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
       P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
       [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
     done)
     NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
     LANDER=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
       [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
     done)
   fi
   py -3 "$LANDER" --help
   ```

2. **Read its `--help`.** The last line of the block above prints it. An older script does not know the flag and would exit 2 on it. An empty `LANDER` makes that line fail, which is expected: arm 1 below decides on the empty value.

3. **Pick the arm, first match wins.** Arm 1 is decided before anything is launched; arms 2 to 6 are decided from the locator after the run has ended.

   1. `LANDER` is empty, or the `--help` text does not list `--verify-here` → **launch nothing.** Run Steps 1 to 4 below as written and let them decide. Say "runner not found" (empty `LANDER`) or "runner too old" (no `--verify-here` in `--help`). Never stop here: unlike `/advance`, this skill has a complete fallback.

   Otherwise generate the run id yourself (`verify-<UTC YYYYMMDDTHHMMSSZ>-<six hex digits>`) and launch the runner **in background mode**. The shell caps a foreground call at ten minutes and the suites run 40 to 60 minutes:

   ```bash
   RUN_ID=$(py -3 -c "import datetime, uuid; print('verify-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '-' + uuid.uuid4().hex[:6])")
   py -3 "$LANDER" --verify-here --run-id "$RUN_ID" --json
   ```

   **Wait for that background run to end** (its completion notice arrives on its own; do not poll it, and do not start any prose step meanwhile). **Never read the background task's output** for the result and **never build the report path by hand.** Then ask the read-only locator, which needs no `--contract`, takes no lock and writes nothing:

   ```bash
   py -3 "$LANDER" --verify-here --run-id "$RUN_ID" --status --json
   ```

   It returns `state` (`live`, `report`, `interrupted` or `none`), `run_id`, `report_path` and `report` (the parsed report, or null). Read `state`, then `report.outcome`:

   2. `state` is not `report` → the run ended without a report for this run id (it was cut short, or it refused its arguments). Run Steps 1 to 4 below as written and let them decide. Say so, and point to the background run's own output so the operator can read why.
   3. `outcome` is `no-baseline` → the default branch holds no failing-test baseline, so the runner ran no step (it ends in seconds, without taking the lock). Run Steps 1 to 4 below as written and let them decide. The report lists only the suites that would apply.
   4. `outcome` is `verified` → the runner's reading stands in for Steps 1 to 3, so Steps 1 to 4 pass once Step 4 (drift) has run as written. Skip the prose in Steps 1 to 3 and go on to Step 5.
   5. `outcome` is `verification-not-ready` → Steps 1 to 4 **fail** on the new failures listed in `report.new_failures`. A baseline exists, so the reading is trusted: do not rerun the prose. Halt and report them.
   6. Any other outcome (`environment-failure`, `landing-in-progress`, `landing-not-configured`, `baseline-unreadable`, `base-unreadable`) → the runner decided nothing. Run Steps 1 to 4 below as written, now that the runner has ended, and let them decide. Say which outcome it was; `report.next_command.reason` carries the fix.

Arms 1, 2, 3 and 6 are exactly today's path. A `landing-in-progress` outcome means a contract landing holds the lock: neither side waits for the other.

## Step 1: Backend build

Reached when the runner arms above sent you here, or when the runner was not used.

```bash
dotnet build --nologo --verbosity minimal
```

**Halt conditions:**
- Any error CSxxxx that is NOT "DLL is locked" (the locked-DLL failure is the VS-debugger-attached edge case — ask the user to stop the debugger, then retry).
- Any warning treated as error per project config.

## Step 2: Backend tests

Run the tests for the project(s) whose source changed. Don't run the full suite unless the change is cross-cutting (DI, Program.cs, base classes).

```bash
dotnet test <affected-test-project> --nologo --verbosity minimal --no-build
```

**Halt conditions:**
- Any failed test, including previously-passing ones (regression).
- Any skipped test that was active before the change, unless the user explicitly approved skipping it.

## Step 3: Frontend build + tests

```bash
# From the frontend workspace root (frontend.root-container in the project profile):
npm run build -- --configuration=production
npm run test -- --watch=false --browsers=ChromeHeadless
```

**Halt conditions:**
- Angular compile errors.
- Any spec failure in the projects that changed.
- TypeScript errors in the generated folder (`core/api/generated/`, `core/hub/generated/`) — these indicate model drift, handled by Step 4.

## Step 4: Generated-model drift check

If any `.cs` file in a sentinel path (see `.claude/hooks/sentinel-paths.json`) was edited, verify the generated TypeScript matches:

```bash
# Check drift without running the regenerator
git diff --stat <frontend.roots>/**/generated/
# If there are uncommitted changes here but no regen in flight, run it manually:
tools/regenerate-angular-models.cmd
git diff --stat <frontend.roots>/**/generated/  # should now be clean if auto-regen already ran
```

**Halt conditions:**
- Modified `.cs` file in sentinel path AND stale `.ts` generated file → run the regenerator and stage the diff.
- CI would reject the PR anyway (angular-models-drift.yml) — catch it locally.

## Step 5: Migration safety check

If any `Persistence/Migrations/*.cs` file was created or modified:

1. Open the generated migration in an editor (or `Read` the file) and eyeball it:
   - Does it match the entity change you intended?
   - Does it include a sensible `Down()` for rollback?
   - Are there any `DROP COLUMN` / `ALTER COLUMN` / `DROP INDEX` operations that need a data backfill first?
2. Verify the migration on a disposable copy of the newest backup, never on the dev database:
   ```bash
   tools/db-protection/verify-migration.cmd --from-backup
   ```
   The script restores the newest backup into a throwaway `_MigrationVerify_` copy, applies the pending migrations there with the EF update tool (not the idempotent full-chain script), and removes the copy. It prints the newest migration id in the copy before and after the apply. When the backup already has the newest schema the apply changes nothing, the two ids are equal, and the final line still says "applied cleanly": read the before and after lines. To rehearse a real apply, pass an OLDER backup file as the last argument (`verify-migration.cmd --from-backup <file>`). If the EF tool is missing the script exits 2 before restoring anything: run `dotnet tool restore` once. In a worktree session invoke the script by its path, as above; the worktree-isolation guard blocks `cmd //c`.
   An agent never applies a migration to the dev database. A person does that, in their own terminal, with `tools\db-protection\update-dev-database.cmd` (it backs up first). The hook blocks an agent that tries.
3. Step 5.5 will enforce that `migration-safety-reviewer` was invoked on the current diff — do not bypass it for schema modifications.

**Halt conditions:**
- Migration fails to apply to the disposable copy (syntax, FK, constraint violation).
- Migration drops a column or table without a data migration plan.
- Migration modifies a table with > 1M rows without a plan for online reindex / locking.

## Step 5.5: Safety-critical review gate (hard gate)

This step encodes the **session-context-isolation principle**: code review done inline by the same session that generated the code is biased by the generator's reasoning. For safety-critical paths, an independent reviewer instance (spawned via the `Agent` tool with a cold context) MUST have audited the current diff before verification can PASS.

### Path-to-reviewer mapping

Read `git diff --name-only` (uncommitted + staged) and classify each file:

**Resolve every row against `.claude/project-profile.md` before matching.** The rows name profile
slots, not literal paths. Open the profile, read the slot, and match the diff against the roots it
names. If the profile is missing, say so and halt — do not guess a path from a project name.

> **Why this indirection exists, in one incident.** Until 2026-09-12 the first row read
> `src/ScalpingMachine.Strategy/Execution/**`. That path has never existed in this repository's
> history; the execution engine is under `Services/`. The row had been wrong since the day it was
> written on 2026-08-22, and no run ever failed because of it — a prose rule whose pattern matches
> nothing simply stays quiet, and quiet is indistinguishable from "nothing to review". A hardcoded
> path in a shared skill is a fact nobody owns. A slot has one owner and one place to be wrong.

| Diff touches the roots named by | Required reviewer agent | Rationale |
|---|---|---|
| `safety-critical.roots` — the live-order-flow and broker entries | `trading-safety-reviewer` | Live order flow, broker integration |
| `auth.roots` | `security-auditor` | Credentials, tokens, encryption |
| `migration.root` | `migration-safety-reviewer` | Online schema change risk |
| Any repository class or database query change under `backend.roots` | `sql-performance-reviewer` | Plan / index / N+1 risk |
| Any controller or data-transfer-object change under `backend.roots` | `api-contract-reviewer` | Frontend deserialization drift |
| Any hand edit to generated client code under `frontend.roots` | `api-contract-reviewer` + halt | Generated files must not be hand-edited; investigate before allowing |
| Any file the profile's `review.documents` flags as pipeline-critical | `llm-contract-reviewer` | Tool / schema / training-data alignment |

A slot may name several roots, and a single diff can require multiple reviewers — list them all.

### Gate procedure

1. Compute the required-reviewer set from the diff using the table above.
2. If the set is **empty** → emit `Step 5.5: PASS (no safety-critical paths in diff)` and proceed to Step 6.
3. If the set is **non-empty**, for each required reviewer in the set:
   - Check session history: was this reviewer spawned via the `Agent` tool AFTER the last modification to the files it owns? An inline review in the main session does **NOT** count and never satisfies this gate.
   - If yes → record `<reviewer>: SATISFIED (HANDOFF at <message ref>)`.
   - If no → record `<reviewer>: MISSING`.
4. If any reviewer in the set is `MISSING`:
   - **HALT verification.** Do NOT proceed to Step 6.
   - Emit the list of missing reviewers and the file groups they cover.
   - Tell the caller: *"Spawn the listed reviewer(s) via the `Agent` tool now. After each reviewer returns its HANDOFF, re-invoke `/verify-before-done`. Do NOT review the code inline — the isolation requirement is structural, not stylistic."*
   - Do not auto-spawn the reviewers — the caller (main session) must do it, because the spawn site is part of what makes the review isolated.
5. If every required reviewer is `SATISFIED`, emit `Step 5.5: PASS (<n> reviewers verified)` and proceed.

### What counts as "spawned via Agent tool"

- `Agent` tool call with `subagent_type: <reviewer-name>` returning a fresh HANDOFF block whose `Files reviewed` list overlaps the current diff
- Re-invocation of the same reviewer after a code change is a **new** spawn — do not credit the previous run if any in-scope file changed since
- `SendMessage` to a prior reviewer instance does **NOT** count — that instance still has the generator's context priming its judgment

### What does NOT count

- Inline review prose written by the main session ("I read the diff and it looks fine")
- Build / test PASS (those are Steps 1–3, not review)
- The implementer agent's own self-critique inside its HANDOFF
- A reviewer agent that was spawned but reviewed an earlier diff (the in-scope files changed since)

### Why this is a hard gate (not a recommendation)

The 2026-05-17 eval-runs consolidation contract showed 5 WARN findings from `contract-critic` in a draft the data-architect had marked `verdict: confident`. The generator could not see what an independent reviewer could see. That pattern recurs in code review: the generator's confidence is not evidence of correctness. The gate makes the structural isolation mandatory for the paths where the cost of a missed bug is highest (live money, credentials, schema, query plans, API contracts).

### Escape hatch

For a one-shot human-approved exception, the **user** (not an agent) sets `CLAUDE_VERIFY_REVIEW_GATE=off` in the environment for the session. Agents MUST NOT set or unset this. Document any use in the commit message.

## Step 5.6: Registry structure lint

Run the structure lint of the registries (the three root files and their domain files, `MECHANISMS/*.md`, `VOCABULARY/*.md`, `JOURNAL/*.md`). Find `validate_registries.py` with the standard script lookup block, then run it with the project root:

```bash
VAL=
S=.claude/scripts/validate_registries.py
if [ -f "$S" ]; then VAL=$S
elif [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then VAL=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  VAL=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$VAL" --check-structure --project "$CLAUDE_PROJECT_DIR"
```

If `VAL` comes back empty, say the lint could not run (the plugin's script was not found) and report Step 5.6 as `NOT RUN`; never report it as passed. Otherwise read the exit code:

- **1:** the registries hold a finding (a bodiless entry, a duplicate title, project content in a Universal root, an invalid domain file, a stale digest or a malformed entry) on a project that is on registry layout 2. The verdict is **NOT-READY**: halt, show the printed findings with their file and line, and do not go on to Step 6. A bodiless entry is cleared with the `registry_append.py ... --archive-title-only` line the lint prints, run by the operator; never by hand-editing the registry.
- **0:** the step passes. `advisory:` lines in the output (a dead path reference, a legacy entry, a project that is not yet on registry layout 2) are reported as written, and they do **not** make the verdict NOT-READY.
- **2:** the lint could not run; show its message and report Step 5.6 as `NOT RUN`.

## Step 5.7: Protected database names

The database guard protects the names listed in the project's `.claude/hooks/db-destructive-guard.rules.json`. That file is an ordinary file, so this step checks the OUTCOME: this tree's list must still hold every name the same file holds at the tip of the default branch (a removed, respelled or space-padded name all fail). Only a person shortens the list, by merging a pull request by hand.

Run the **installed plugin's** `protected_names_check.py`, never the copy in the project: a branch that edits the checker must not be the one that judges it. The lookup therefore has no project branch (`CLAUDE_PLUGIN_ROOT`, then what Claude Code recorded for the plugin, then the newest cache folder), and the check runs with `--fetch`, so the default branch is read fresh when the network allows:

```bash
PNC=
S=.claude/scripts/protected_names_check.py
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then PNC=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  PNC=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$PNC" --fetch --project "$CLAUDE_PROJECT_DIR"   # macOS and Linux: python3
```

Standard output is one JSON object (`verdict`, `missing`, `working_ref`, `default_ref`, `fetched`, `reason`); the human text is on standard error. If `PNC` is empty, report Step 5.7 as `NOT RUN` (the plugin's script was not found) and never as passed. Otherwise read the result: it counts only when standard output is exactly one JSON object whose `verdict` agrees with the exit code. Anything else (no JSON, a traceback, exit 1 or 2, a code that disagrees with the verdict) is `unverifiable`, never `names-removed`. Then:

- **0:** `kept` or `first-install`. The step passes. When `fetched` is `false`, say so in one sentence: the local default-branch ref was compared, not a fresh one.
- **10:** `names-removed`. **NOT-READY.** Show the `missing` strings and say: only a person removes a protected database name; restore them, or change only the rules file in its own pull request and merge it by hand. Do not go on to Step 6.
- **11:** `working-malformed` or `reference-malformed`. **NOT-READY.** Show the `reason`. A working file the guard cannot read makes it fail closed; a person repairs the file.
- **12:** `unverifiable` (no `origin`, no default branch, an offline fetch with no local ref, a git failure, or a result that could not be read). This is a disclosed **Not performed** item, not a blocker: the landing gate and the human merge are the blocking points. Say why in one sentence.

Then see whether this tree changes the check itself. A tree whose checker or `land_contract.py` differs from the default branch's is the one case where the judge and the judged meet:

```bash
D=$(git symbolic-ref -q --short refs/remotes/origin/HEAD 2>/dev/null || echo origin/master)
git diff --quiet "$D" -- .claude/scripts/protected_names_check.py .claude/hooks/_protected_names.py .claude/scripts/land_contract.py; [ $? -eq 1 ] && echo "this branch changes the check's own code"
```

If it prints the line, add one sentence to the report: this branch changes the check's own code (the protected-name checker or the landing script), so a person reviews that diff. It never changes the verdict above.

## Step 5.8: The codegraph add-on's settings and hook freshness check

Run this step only when `.claude/settings.json` has a row for `codegraph-first-guard.py` (the project installed the `codegraph` add-on). Otherwise skip it.

The check is `auto_improve_finish_install.py addon --name codegraph --project . --check --json`. It only reads. It finds the script through the plugin install only (`CLAUDE_PLUGIN_ROOT`, then what Claude Code recorded for the plugin, then the newest cache folder); a copy under the project's `.claude/scripts/` is never used, because a stale vendored installer could neither see nor repair a stale hook:

```bash
FIP=
S=.claude/scripts/auto_improve_finish_install.py
if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then FIP=$CLAUDE_PLUGIN_ROOT/$S
else
  # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
  CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
  ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
  REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
  MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
    P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
    [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
  done)
  NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
  FIP=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
    [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
  done)
fi
py -3 "$FIP" addon --name codegraph --project . --check --json   # macOS and Linux: python3
```

**If `FIP` is empty, say so and report "could not check" for this step. Never report READY on it.** A project that holds the add-on but has no plugin install can never reach READY on this step. Then read the exit code:

- `0`: the settings allow `mcp__codegraph__*` and name no single tool, and the answer says `"freshness": "checked"` with no finding. The step passes. **A result with no `freshness` field is from an older installer: report "could not check" (a `freshness` that is missing reads as could not check), NOT READY.** (`"freshness": "not-applicable"` is for another add-on and does not apply to codegraph.)
- `1`: findings. **NOT READY.** `codegraph-wildcard-missing` (no settings layer allows the wildcard) or `codegraph-tool-named` (a layer's `permissions.allow` names one CodeGraph tool; the answer names the entry and the file): run `/auto-improve-codegraph-install` or replace the entry with `mcp__codegraph__*` by hand. The freshness findings: `addon-hook-outdated` (the project's hook is a released copy older than the plugin's; the answer names both versions), `addon-hook-missing` and `addon-row-missing` (a hook file or a settings row the manifest lists is absent): re-run `/auto-improve-codegraph-install`. `addon-row-outdated` (a row is registered but its `if` differs from the manifest's): run `/auto-improve-codegraph-uninstall`, then `/auto-improve-codegraph-install`, because an install never rewrites a row.
- `2`: it could not check (a settings layer is unreadable or malformed, or no separate plugin root was found). **NOT READY.** Say which file the answer names.

`addon-hook-unrecognised` is a note, not a finding: the project's hook is neither the plugin's copy nor a released copy (an edited copy, or one from a newer plugin than the one that ran). It never changes the exit code and never makes this step NOT READY; mention it in one sentence.

## Step 6: HANDOFF completeness check

If the caller is an agent producing a `### HANDOFF` block (see `.claude/HANDOFF_SCHEMA.md`), verify:

- [ ] `Status` is populated (complete / needs-review / blocked)
- [ ] `Files changed` lists absolute paths with one-line description each
- [ ] `Key decisions` explains any non-obvious choice (never "N/A" unless truly nothing notable)
- [ ] `Warnings` lists known-but-unaddressed issues (empty is allowed)
- [ ] `Context for next agent` is populated if `Recommended next` is not `none`
- [ ] `Recommended next` names a specific agent or explicitly says `none`
- [ ] `Suggested input for next agent` is pre-written if `Recommended next` ≠ `none`

A HANDOFF block missing any mandatory field is not a completed task — the implementer gets a second chance to fill it in.

## Step 7: Commit hygiene sanity check

```bash
git status
git diff --stat --cached
```

Check for:

- [ ] No unintended files staged (`.env`, credentials, `*.key`, `*.pem`, connection strings).
- [ ] No generated-client drift under `frontend.roots` (either committed cleanly or regenerated in Step 4).
- [ ] No `.claude/.models-dirty-*` or `.claude/.regen-lock` files accidentally staged.
- [ ] No `bin/`, `obj/`, or build output staged.
- [ ] No `debug-notes*.md` or `.claude/tdd-scratch-*.md` staged (those are local scratch files).

**Halt conditions:**
- Any sensitive file (secrets, keys, connection strings) staged — ask the user to unstage and confirm before proceeding.

## Step 8: Python sidecar smoke check

If any file under `python/scalping_llm/**` changed:

```bash
# Syntax / import check
cd python && py -3 -c "import scalping_llm" && cd ..

# If the sidecar is already running, hit /health
curl -sS http://localhost:8091/health || echo "sidecar not running (acceptable if not required for this change)"

# Run any sidecar tests that exist
cd python && py -3 -m pytest tests/ -q && cd ..
```

**Halt conditions:**
- Import error on the package.
- Any sidecar test fails.

## Step 9: Report verified state

Once all applicable steps pass, emit:

```
### VERIFICATION REPORT
- Scope: <backend|frontend|full-stack|migration|python|docs>
- Steps executed: <list>
- Build: PASS
- Tests: PASS (<n> tests)
- Generated drift: CLEAN
- Migration applied: <yes/no/NA>
- Safety-critical review gate: PASS (<n> isolated reviewers verified | NO SAFETY-CRITICAL PATHS)
- Registry structure lint: PASS (<n> advisory lines) | NOT-READY | NOT RUN
- HANDOFF fields: COMPLETE
- Commit hygiene: CLEAN
- VERDICT: READY
```

Only then may the caller set `Status: complete` in their HANDOFF.

## Step 10: Post-verification commit protocol (auto-fires on VERDICT: READY)

After Step 9 returns `VERDICT: READY`, auto-stage + auto-draft + ASK ONCE before committing. Do **not** commit silently. Do **not** skip this step unless one of the explicit skip conditions below applies.

### Trigger gate

Run this step IFF all of the following are true:
- Step 9 verdict is `READY` (not `BLOCKED`, not partial)
- Working tree has at least 1 modified or untracked file (otherwise nothing to commit — silently skip)
- The user did not say "don't commit", "wait", "hold off", "no commit", or any equivalent phrase since the verification started
- The project's recent commit history is non-empty (this is a `git init`-with-commits repo, not a fresh init)

### Action sequence

1. **Identify scope.** Run `git status --short` and parse the file list. Exclude any of:
   - Sensitive: `.env`, `.env.*`, `*.key`, `*.pem`, `*.pfx`, `appsettings*.json` (with credentials), `secrets*.json`, `credentials.json`
   - Build output: `bin/`, `obj/`, `dist/`, `node_modules/`
   - Local scratch: `.claude/.models-dirty-*`, `.claude/.regen-lock`, `.claude/hooks/*.log*`, `debug-notes-*.md`, `.claude/tdd-scratch-*.md`
   - Generated drift: generated client code under `frontend.roots` only if Step 4 reported drift that was NOT yet regenerated (a CLEAN regen is committable)
   If any excluded file is in the working copy, list it explicitly to the user and ask whether to include it before staging anything else.

2. **Scope-creep check.** If the staged file list exceeds **30 files** OR touches more than **3 top-level project directories**, escalate to the user with the full list before drafting the message. Large commits hide intent; ask the user to confirm or split.

3. **Stage explicitly.** Use `git add <file1> <file2> ...` with the explicit file list. Never `git add -A` / `git add .` / `git add -u`.

   **Changed-file check (once per commit, right after staging).** Ask the plugin's Changed-file check
   whether every staged file is covered by an approved contract. Find the script through the plugin
   only; a copy under the project's `.claude/` is never used, because a file there is trivial to both
   gates and could be forged.

   ```bash
   S=.claude/scripts/concept_changed_check.py
   if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$CLAUDE_PLUGIN_ROOT/$S" ]; then CC=$CLAUDE_PLUGIN_ROOT/$S
   else
     # What Claude Code recorded for this plugin (this project's entry, then the user entry), then the newest cache folder by version number.
     CFG=${CLAUDE_CONFIG_DIR:-$HOME/.claude}
     ME=$(printf %s "$CLAUDE_PROJECT_DIR" | tr 'A-Z\134' 'a-z/' | tr -s /)
     REC=$(tr -d '\r\n' 2>/dev/null < "$CFG/plugins/installed_plugins.json" | grep -o '"agentic-auto-improve@[^"]*" *: *\[[^]]*]' | grep -o '{[^{}]*}' | tr '\134' / | tr -s /)
     MINE=$(printf '%s\n' "$REC" | grep '"scope" *: *"project"' | while IFS= read -r O; do
       P=$(printf %s "$O" | sed -n 's/.*"projectPath" *: *"\([^"]*\)".*/\1/p' | tr 'A-Z' 'a-z' | tr -s /)
       [ -n "$ME" ] && [ "${P%/}" = "${ME%/}" ] && printf '%s\n' "$O"
     done)
     NEWEST=$(ls -d "$CFG"/plugins/cache/*/agentic-auto-improve/*/ 2>/dev/null | sed -n 's|^\(.*/\([0-9][0-9.]*\)/\)$|\2 \1|p' | sort -rV | cut -d' ' -f2-)
     CC=$({ printf '%s\n' "$MINE"; printf '%s\n' "$REC" | grep '"scope" *: *"user"'; } | sed -n 's/.*"installPath" *: *"\([^"]*\)".*/\1/p' | { cat; printf '%s\n' "$NEWEST"; } | while IFS= read -r D; do
       [ -n "$D" ] && [ -f "${D%/}/$S" ] && { printf '%s\n' "${D%/}/$S"; break; }
     done)
   fi
   py -3 "$CC" --staged   # macOS and Linux: python3 "$CC" --staged
   ```

   If `CC` is empty, do not run the last line. Otherwise read its exit code:
   - **2:** refuse the commit. Show the files the check listed and its `/design-first` text, tell the user to run `/design-first` or pin the contract that covers them, and do not go on to the draft.
   - **0:** go on.
   - **3, or `CC` empty:** say in one sentence that the check could not run (git missing, not a git tree, a slow git call, or the plugin's script not found), then go on.

4. **Draft the commit message** matching the project's recent commit style (read the last 3 commit subjects via `git log -3 --format="%s"` to mirror length + tone):
   - **Subject:** ≤ 70 chars, focuses on the *why* (or the named phase/scope), present tense, no trailing period
   - **Body** (only if scope is multi-component or non-obvious): 2–4 sentences explaining the *why* and naming any side-effects, blank line before
   - **Trailer:** `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>` (always, on its own line at the very end)

5. **Show + ask.** Surface to the user:
   - The staged file count + first ~10 file paths (the rest as `... and N more`)
   - The drafted subject line + first 2–3 lines of the body
   - One question: `Commit? (yes / edit / cancel)`

6. **On user response:**
   - `yes` (or any clear go-ahead like "ship", "commit", "go", "do it"): commit via HEREDOC immediately, then run `git status --short` + `git log -1 --oneline` and report the new HEAD hash
   - `edit`: show the full message and accept the user's revision (apply their text verbatim into the HEREDOC), then commit
   - `cancel` / `no` / `wait`: leave the staged file list as-is and tell the user `git reset` will unstage if they want to abandon

7. **Never:**
   - Skip hooks (`--no-verify`) unless the user explicitly asks
   - Amend (`--amend`) unless the user explicitly asks
   - Push (`git push`) unless the user explicitly asks
   - Force-push (`git push --force`) under any circumstance — escalate
   - Commit if the pre-commit hook fails — investigate the hook output and fix the underlying issue (per project rule: failed pre-commit hook means the commit did NOT happen, so `--amend` would corrupt the prior commit)

### Skip conditions (do NOT auto-commit)

- User said any "don't commit" phrase since verification started
- The change is purely a HANDOFF field fix or a stale-cache invalidation that the user would likely want to fold into the next feature commit
- The verification was invoked mid-flight specifically to check state (not to ship) — detect by reading the most recent user message: if it says "check" / "see if" / "what does it look like" / "status" / "smoke", treat as a state-check and skip the commit ask
- The repo is in detached HEAD state, on `main` / `master` directly (not a feature branch), or in mid-rebase (`git status` reports rebase / merge in progress)

### Why this exists

Without this step, every shippable change requires the user to type "commit" twice (once to ask, once to confirm). With this step, the path is one tap (`yes`) once the verification has already proven the change is safe. The ASK-before-commit caveat preserves human review of scope creep — the protocol's purpose is to remove typing, not human judgment.

## Step 11: Tree clean after commit

Run this after Step 10 commits, and also when Step 10 was skipped or declined. A verified change can still leave files behind: journal entries, reviewer memory notes, result records, generated output, and files written by agents during the run.

Run `git status --short` in every tree the work touched and sort each remaining file, using the rules in Step 8 of `/flow`:

- **History needs it:** stage it explicitly and offer it for the commit, or name it as pending if the user declined the commit.
- **History does not need it** (regenerated output, line-ending-only changes, duplicates of committed files): say it can be deleted or restored, and why. Do not delete it without the user's go-ahead.
- **Another session's file:** name it and leave it.

Report the result as one line: `tree clean`, or the list of files still pending with what each needs. Do not report the work as done while files this work wrote are still uncommitted.

## Landing a completed contract: the scripted form

A contract built on a parent branch is not verified by this skill's steps. When every sub-task has a completion record, `/advance` starts `.claude/scripts/land_contract.py` in the background, and that script runs its own scripted gate on the merged head of the parent branch (`master` merged in). It then opens the parent pull request and merges it. Read its Landing Report, never re-run these steps by hand for that merge. Contract: `.claude/concepts/2026-10-05-contract-completion-lands-on-master.md`.

The scripted gate substitutes for two steps here:

- **Step 5 (migration safety)** is not run. It applies migrations to the developer database, and the script never does. A contract touching `migration.root` needs a passing `migration-safety-reviewer` artefact instead, which the script checks.
- **Step 5.5 (safety-critical review gate)** is not judged from session history. The script checks that a completion record of the contract carries a passing review artefact for each reviewer the changed paths require.

Everything else in the gauntlet is a configured verification step in the script (build and tests), read from `master`'s `contractLanding` configuration and compared with the failing-test baseline on `master`. Step 4 (drift) is its `generated-drift` step: it runs the model and GraphQL regenerators' commands and fails when `git status` shows a change afterwards. It runs in a landing only. In the `--verify-here` runner the same step is reported not applicable, because regenerating and staging happen in the operator's tree, so Step 4 stays the prose step there. This skill still governs a contract with no parent branch and every sub-task's own branch.

## Anti-patterns (halt immediately)

- **Reporting done with this work's files still uncommitted** — Step 11 is the check. A green verdict does not make the tree clean.
- **"All green" without running the commands** — the skill requires actual command output, not a summary of what the output would have been.
- **Skipping Step 4 because "I didn't touch generated files"** — if a sentinel `.cs` file changed, the `.ts` drift check is mandatory.
- **Partial verification** — don't run 3 of 8 applicable steps and call it verified. Run them all or report which ones were skipped and why.
- **Claiming "verified" based on the previous CI run** — CI ran before this change. Verify this change's state.
- **Reviewing the diff inline in the main session to satisfy Step 5.5** — the gate exists *because* same-session review is biased. Inline prose never counts; spawn the reviewer via the `Agent` tool.
- **`SendMessage`-ing a prior reviewer instance after a code change to satisfy Step 5.5** — that instance carries the generator's context. Spawn a fresh instance.

## Integration

The canonical places to invoke this skill:

1. **End of `/tdd-first`** — Step 7 already references this skill.
2. **Before any `Status: complete` HANDOFF** — implementer agents should invoke this automatically via the `Skill` tool if the project has the skill available.
3. **Before `git commit`** — either manually, or as part of a pre-commit workflow.
4. **Before `gh pr create`** — PR readiness check.

## When to NOT use this skill

- **Mid-flight exploration** — if you're still iterating, verify-before-done is overkill.
- **Read-only tasks** — research, code review, architecture analysis. Nothing to verify.
- **Documentation-only changes** — Step 6 (HANDOFF) + Step 7 (commit hygiene) are enough.
