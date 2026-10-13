---
name: smoke-check
description: "Run the critical path smoke test gate before QA hand-off. Executes the automated test suite, verifies core functionality, and produces a PASS/FAIL report. Supports both game and product projects. A failed smoke check means the build is not ready for QA."
argument-hint: "[sprint | quick | --platform pc|console|mobile|web|api|cli|all]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash, Write, AskUserQuestion
---

## QA policy, facts and authority

Apply `standards/evidence-lifecycle.md`, `standards/notes-adr-sync.md` and existing
collaboration authority. Read actual `workflow/workflow-catalog.yaml`, domain,
current transition and established project QA scope, including initialized
`memory_bank/t1_axioms/qa_context.md` or the existing owning Story/plan/decision.
QA orchestration is optional by default; strict obligations need explicit source,
authority and exact checks/scope. Review mode does not select strict QA. Absent
optional Memory Bank/QA Context with no actual strict selection uses the catalog's
default optional orchestration; disclose absence without requiring initialization.
Unknown applies to unresolved actual required applicability or conflicting policy,
not optional context absence. Resolve that affected scope before dependent claims;
Honor actual user-specified per-effect approval conditions when determining coverage;
do not invent strict obligations or passing results.
Optional orchestration never waives required Story AC, governing DoD, decisions,
evidence or required review. Type tables are starting points; actual owners decide
requirements. Each required check retains PASS/FAIL/NotRun/Blocked/Pending; N/A
needs a governing applicability reason and cannot erase a failure.

Separate sufficiency, actual execution, independence, acceptance and completion.
Files/keywords/counts, planning cases and self-checks prove none of the other facts.
Read relied-on bodies and minimum required direct/indirect dependency closure;
retain full SHA-256/byte sizes, recoverable originals and original-path witnesses.
Disclose reading omissions. Exact bound historical results may be reused only
where selected workflow permits, labeled historical with original runtime/observer,
inputs and scope; never call them this run's execution. Missing required originals
or observations leave affected checks incomplete. Risk acceptance is a separate
scoped record; it cannot change FAIL/NotRun/Blocked/Pending to PASS or completion.

Reuse named paths/effects authority across roles/retries; before new authority show
draft and complete effect set, asking only for material new scope. Review-only
invokes no write entrypoint. Report-only writes its new report, excluding inputs,
indexes, session/sprint/stage state and closure. Existing report paths require a
new revision with prior evidence preserved; index effects need their own covered
scope and historical links. Optional Memory Bank absence uses Story/report/
conversation fallback without initialization, publication or activation.

## User Guide

- When to use: Run the critical path smoke test gate before QA hand-off. Executes the automated test suite, verifies core functionality, and produces a PASS/FAIL report. Supports both game and product projects. A failed smoke check means the build is not ready for QA.
- Inputs: Command arguments: `/smoke-check [sprint | quick | --platform pc|console|mobile|web|api|cli|all]`; project artifacts referenced below; user decisions and approvals before writes.
- Outputs: Primary artifacts, reports, or conversation guidance described below; write files only after user approval.
- Memory-bank writes: Only when Memory Bank is initialized and each named write effect is covered: `memory_bank/t3_archive/qa_evidence_index.md`.
- Next steps: Follow the workflow hand-off or next-step guidance below; recommendations do not auto-run and require explicit user command/approval.

# Smoke Check

This skill is the gate between "implementation done" and "ready for QA
hand-off". It runs the automated test suite, checks for test coverage gaps,
batch-verifies critical paths with the developer, and produces a PASS/FAIL
report.

The rule is simple: **a build that fails smoke check does not go to QA.**
Handing a broken build to QA wastes their time and demoralises the team.

**Output:** `production/qa/smoke-[date].md`

---

## Dual-Domain Parity Contract

| Area | Game branch | Product branch |
|------|-------------|----------------|
| Context reads | Engine from technical preferences, current QA plan, sprint stories, smoke tests, test directories, recent build/test output | Language/framework from technical preferences, current QA plan, API/CLI/workflow/deployment smoke tests, sprint stories, CI/test output, package/deploy config |
| Steps | Run engine tests, verify playable critical path, validate platform/input batches, confirm build ready for QA | Run product test command, verify API/CLI/web/core workflow batches, validate migration/config/deployment/package smoke checks, confirm release candidate ready for QA |
| Outputs | `production/qa/smoke-[date].md` with PASS/FAIL, failed tests, platform batches, manual checks, QA hand-off decision | `production/qa/smoke-[date].md` with PASS/FAIL, contract/CLI/workflow/migration/deployment smoke results, manual checks, QA hand-off decision |
| Next steps | Fix blockers or run `/team-qa`; update regression suite for failures | Fix blockers or run `/team-qa`; run `/test-evidence-review` for contract/migration/package evidence and `/release-checklist` when release-bound |

---

## Parse Arguments

Arguments can be combined: `/smoke-check sprint --platform console`

**Base mode** (first argument, default: `sprint`):
- `sprint` — full smoke check against the current sprint's stories
- `quick` — skip coverage scan (Phase 3) and Batch 3; use for rapid re-checks

**Platform flag** (`--platform`, default: none):

**[游戏专用]** Game platforms:
- `--platform pc` — PC checks (keyboard, mouse, windowed mode)
- `--platform console` — console checks (gamepad, TV safe zones, certification)
- `--platform mobile` — mobile checks (touch, portrait/landscape, battery/thermal)

**[通用产品]** Product platforms:
- `--platform web` — browser checks (page load, navigation, form submission)
- `--platform api` — API checks (health endpoint, auth flow, response schema)
- `--platform cli` — CLI checks (help output, core command, config loading)

**[通用场景]** `--platform all` — all applicable platform variants; per-platform verdict

If `--platform` is provided, Phase 4 adds platform-specific batches and
Phase 5 outputs a per-platform verdict table in addition to the overall verdict.

---

## Phase 1: Detect Test Setup

Before running anything, understand the environment:

1. **Test configuration/capability check**: read actual project test configuration,
   pinned tooling, test roots and documented commands (including configured tests
   outside `tests/`). Verify the configured runner and execution environment are
   already available. `tests/` is a conventional example, not a prerequisite.
   Do not scaffold/stop solely because that directory is absent when valid tests
   live elsewhere. If a required configuration/runner/input is absent, record the
   affected execution as NotRun with its actual missing dependency (Blocked if
   setup prevents it), disclose INCOMPLETE hand-off and suggest the scoped
   `/test-setup` remedy when applicable. Continue independent available checks;
   do not invent observed FAIL/PASS, fetch/install or initialize anything.

2. **CI check**: check whether `.github/workflows/` contains a workflow file
   referencing tests. Note in the report whether CI is configured.

3. **Technology detection**: read actual configured commands/pinned tooling plus
   `standards/technical-preferences.md`. Record Game Engine or Product
   Language/Framework when declared, and bind the actual config/runner/command,
   test roots, relevant inputs and available capability before execution. Language
   examples below apply only when confirmed by that project's real configuration;
   a language name or unknown JavaScript framework cannot select a test command.

4. **Smoke test list**: check whether `production/qa/smoke-tests.md` or
   `tests/smoke/` exists. If a smoke test list is found, load it for use in
   Phase 4. If neither exists, smoke tests will be drawn from the current QA
   plan (Phase 4 fallback).

5. **QA plan check**: resolve the actual current sprint/feature, Story set,
   domain and requested platform/build scope from the user and owning project
   records. Honor an explicitly named plan only after directly reading its body
   and checking that scope. Otherwise glob `production/qa/qa-plan-*.md`, read
   candidate bodies and their referenced scope owners, and select a plan that
   covers this run. A filename, date or newest mtime does not establish a match.
   If multiple matching candidates remain or their scope is ambiguous, present
   their actual existing paths and scope differences with `AskUserQuestion`;
   do not invent a path or silently choose one. Keep plan-dependent claims
   pending until resolved; continue independent available checks.
   Bind the selected original path, full SHA-256, byte size, collection time
   and matched scope for Phase 3, Phase 4, the report and QA hand-off.
   If no usable matching plan exists, disclose the actual absence/mismatch or
   read failure and use available scoped Story/smoke inputs for independent
   checks. Suggest `/qa-plan` for that actual scope without running it. Missing
   optional planning does not invent a strict gate; a plan required by the
   selected workflow remains incomplete. Never fabricate a hand-off plan.

When discovering a plan with the glob above, disclose a truthful empty result and use only the existing independent fallback. Read the actual selected plan completely, wherever located, with its scope owners and exact identity; an empty discovery does not make a workflow-required plan optional. Unresolved branch/scope stays Unknown.

Report findings before proceeding: "Environment: [technology] | Domain: [game/product]. Test directory:
[found / not found]. CI configured: [yes / no]. QA plan: [path / not found]."

---

## Phase 2: Run Automated Tests

Run only the actual configured test command through an available appropriate
shell/runtime verified in Phase 1. The examples below are conditional references:
use one only if the actual project config selects that runner/arguments and the
runner is already available. Respect valid configured roots outside `tests/`.
Never guess a command from language, add unsupported flags, install/fetch a runner
or infer current execution from an artifact filename. Missing required setup or
capability stays NotRun/Blocked and INCOMPLETE for affected hand-off.

**[游戏专用] Godot 4:**
```bash
godot --headless --script tests/gdunit4_runner.gd 2>&1
```
Only if actual configured GDUnit4 uses this alternate runner path and it exists:
```bash
godot --headless -s addons/gdunit4/GdUnitRunner.gd 2>&1
```
If neither path exists, note: "GDUnit4 runner not found — confirm the runner
path for your test framework."

**[游戏专用] Unity:**
Use the configured available Unity editor/CI runner if supported. If it cannot
execute here, record current NotRun and inspect permitted prior result artifacts:
```bash
ls -t test-results/ 2>&1 | head -5
```
If XML/JSON results exist, inspect exact originals and matching build/test/config scope, runtime/observer and result. A latest file/mtime is insufficient; label permitted prior results historical, not current execution. If no artifacts exist: "Unity tests must be run from the
editor or CI pipeline. Supply exact-bound originals for permitted historical reuse; a verbal confirmation does not change current NotRun."

**[游戏专用] Unreal Engine:**
```bash
ls -t Saved/Logs/ 2>&1 | grep -i "test\|automation" | head -5
```
If no matching log found: "UE automation tests must be run via the Session
Frontend or CI pipeline. Current execution remains NotRun; exact-bound originals are needed for permitted historical reuse."

**[通用产品] Python / pytest:**
```bash
pytest -x --tb=short 2>&1
```

**[通用产品] TypeScript / JavaScript:**
If a Vitest config exists (`vitest.config.*`), run:
```bash
npx --no-install vitest run 2>&1
```
If a Jest config exists (`jest.config.*` or `package.json` test script clearly
uses Jest), run:
```bash
npx --no-install jest 2>&1
```
If neither runner is selected by actual configuration, do not guess
`npm test -- --runInBand`. Read the real package test script/runner requirements;
run only its verified configured command when available. Otherwise record
NotRun/Blocked with the missing configuration/capability and retain INCOMPLETE
for required checks.

**[通用产品] Rust / cargo test:**
```bash
cargo test 2>&1
```

**[通用产品] Go / go test:**
```bash
go test ./... 2>&1
```

**Unknown technology / no configured command:**
Inspect actual project configuration independently of the preferences declaration.
A valid configured command may still run when the language label is absent. If
required execution configuration remains unknown/unavailable, record NotRun with
actual missing scope; request the needed project configuration or suggest the
applicable setup skill. Do not guess a language/runner or emit an observed FAIL.

**If the runner is unavailable**, record local execution NotRun with reason.
It is neither observed FAIL nor PASS WITH WARNINGS. Required unexecuted/unavailable/
pending smoke checks make hand-off INCOMPLETE; optional checks remain disclosed
follow-up. Actual documented manual results do not relabel unexecuted automation.
Permitted historical IDE/CI output needs exact original build/test/config input
identity, runtime, observer and recoverable result; label it historical separately.
An unbound verbal "tests passed" cannot satisfy required automation.

Parse runner output and extract:
- Total tests run
- Passing count
- Failing count
- Names of any failing tests (up to 10; if more, note the count)
- Any crash or error output from the runner itself

---

## Phase 3: Check Test Coverage

Draw the story list from, in priority order:
1. The scope-matched QA plan selected in Phase 1 (its Test Summary table lists expected test
   file paths per story)
2. The actual current scope-matched sprint plan from `production/sprints/`,
   verified against the owning Story set rather than newest mtime
3. If the `quick` argument was passed, skip this phase entirely and note:
   "Coverage scan skipped — run `/smoke-check sprint` for full coverage
   analysis."

For each story in scope:

1. Extract the system slug from the story's file path
   (e.g., `production/epics/combat/story-001.md` → `combat`)
2. Read the Story's `Test file:` header or "Test Evidence" section and its
   exact named files first; keep missing required originals visible.
3. Search the actual configured roots and runner-discovered paths from Phase 1
   for additional evidence covering the Story's required ACs. Roots outside
   `tests/` are valid; `tests/unit/[system]/` and `tests/integration/[system]/`
   are conventional examples, not requirements. Filenames locate candidates
   only; read the assertions and exact result binding.

Assign a coverage status to each story:

| Status | Meaning |
|--------|---------|
| **COVERED** | Read behavioral oracle covers actual required AC; execution is separate |
| **MANUAL** | Story type is Visual/Feel or UI; a test evidence document was found |
| **MISSING** | Actual required evidence/test absent for the Game/Product Story |
| **EXPECTED** | Actual owner permits manual/spot-check; required observations still need evidence |
| **UNKNOWN** | Story file missing or unreadable |

Resolve MISSING against actual Story/DoD and selected scope: required gaps make affected hand-off/closure incomplete; optional extra coverage is advisory. Filenames, percentages and keywords cannot establish coverage or execution.

---

## Phase 4: Run Manual Smoke Check

Domain detection drives which batches to use:
- [Game] detected -> present Game smoke batches (Batch 1-3, platform batches pc/console/mobile)
- [Product] detected -> present Product smoke batches (Batch 1-3, platform batches web/api/cli)
- Unknown -> present generic stability checks (never default to game batches)

Draw the smoke test checklist from, in priority order:
1. The selected QA plan's "Smoke Test Scope" section (if its actual scope was verified in Phase 1)
2. `production/qa/smoke-tests.md` (if it exists)
3. `tests/smoke/` directory contents (if it exists)
4. The standard fallback list below (used only when none of the above exist)

Tailor batches 2 and 3 to the actual systems identified from the sprint or QA
plan. Replace bracketed placeholders with real mechanic or workflow names from
the current sprint's stories.

Collect actual results with `AskUserQuestion`. For every applicable item offer PASS / FAIL / NotRun / Blocked / Pending; N/A needs a scope reason. Examples below are prompts, never prefilled results. Record observer, actual steps/time, build/input identity and result. Split batches rather than omit required checks.

**[游戏专用] Game Smoke Batches** *(run when a game engine is detected)*:

**Batch 1 — Core stability (always run):**
```
question: "Smoke check — Batch 1: Core stability. Please verify each:"
options:
  - "Game launches to main menu without crash — PASS"
  - "Game launches to main menu without crash — FAIL"
  - "New game / session starts successfully — PASS"
  - "New game / session starts successfully — FAIL"
  - "Main menu responds to all inputs — PASS"
  - "Main menu responds to all inputs — FAIL"
```

**Batch 2 — Sprint mechanic and regression (always run):**
```
question: "Smoke check — Batch 2: This sprint's changes and regression check:"
options:
  - "[Primary mechanic this sprint] — PASS"
  - "[Primary mechanic this sprint] — FAIL: [describe what broke]"
  - "[Second notable change this sprint, if any] — PASS"
  - "[Second notable change this sprint] — FAIL"
  - "Previous sprint's features still work (no regressions) — PASS"
  - "Previous sprint's features — regression found: [brief description]"
```

**Batch 3 — Data integrity and performance (run unless `quick` argument):**
```
question: "Smoke check — Batch 3: Data integrity and performance:"
options:
  - "Save / load completes without data loss — PASS"
  - "Save / load — FAIL: [describe what broke]"
  - "Save / load — N/A (save system not yet implemented)"
  - "No new frame rate drops or hitches observed — PASS"
  - "Frame rate drops or hitches found — FAIL: [where]"
  - "Performance — not checked in this session"
```

Record actual response plus observation/evidence binding; absent observations remain NotRun/Pending.

**Platform Batches** *(run only if `--platform` argument was provided)*:

**PC platform** (`--platform pc` or `--platform all`):
```
question: "Smoke check — PC Platform: Verify platform-specific behaviour:"
options:
  - "Keyboard controls work correctly across all menus and gameplay — PASS"
  - "Keyboard controls — FAIL: [describe issue]"
  - "Mouse input and cursor visibility correct in all states — PASS"
  - "Mouse input — FAIL: [describe issue]"
  - "Windowed and fullscreen modes function without graphical issues — PASS"
  - "Windowed/fullscreen — FAIL: [describe issue]"
  - "Resolution changes apply correctly — PASS"
  - "Resolution changes — FAIL: [describe issue]"
```

**Console platform** (`--platform console` or `--platform all`):
```
question: "Smoke check — Console Platform: Verify platform-specific behaviour:"
options:
  - "Gamepad input works correctly for all actions — PASS"
  - "Gamepad input — FAIL: [describe issue]"
  - "UI fits within TV safe zone margins (no text clipped) — PASS"
  - "TV safe zone — FAIL: [describe what is clipped]"
  - "No keyboard/mouse-only fallbacks shown to gamepad user — PASS"
  - "Input prompt inconsistency — FAIL: [describe]"
  - "Game boots correctly from cold start (no prior save) — PASS"
  - "Cold start — FAIL: [describe issue]"
```

**Mobile platform** (`--platform mobile` or `--platform all`):
```
question: "Smoke check — Mobile Platform: Verify platform-specific behaviour:"
options:
  - "Touch controls work correctly for all primary actions — PASS"
  - "Touch controls — FAIL: [describe issue]"
  - "Game handles orientation change (portrait ↔ landscape) correctly — PASS"
  - "Orientation change — FAIL: [describe what breaks]"
  - "Background / foreground transitions (home button) handled gracefully — PASS"
  - "Background/foreground — FAIL: [describe issue]"
  - "No visible performance issues on target device (no thermal throttling signs) — PASS"
  - "Mobile performance — FAIL: [describe issue]"
```

---

**[通用产品] Product Smoke Batches** *(run when product stack detected)*:

**Batch 1 — Core Workflow (always run):**
```
question: "Smoke check — Batch 1: Core workflow. Please verify each:"
options:
  - "API: Health endpoint returns 200 — PASS"
  - "API: Health endpoint returns 200 — FAIL: [describe response]"
  - "CLI: --help prints usage without error — PASS"
  - "CLI: --help — FAIL: [describe error]"
  - "Web: Homepage loads without console errors — PASS"
  - "Web: Homepage — FAIL: [describe issue]"
```

**Batch 2 — Integration Health (always run):**
```
question: "Smoke check — Batch 2: Integration checks:"
options:
  - "Auth flow works (login → token → authenticated request) — PASS"
  - "Auth flow — FAIL: [describe where it breaks]"
  - "DB migrations run against fresh instance — PASS"
  - "DB migrations — FAIL: [describe error]"
  - "Core POST/command produces expected result — PASS"
  - "Core POST/command — FAIL: [describe mismatch]"
```

**Batch 3 — Data Integrity (run unless `quick` argument):**
```
question: "Smoke check — Batch 3: Data integrity:"
options:
  - "Seed data / fixtures load without constraint errors — PASS"
  - "Seed data — FAIL: [describe constraint error]"
  - "Core query returns expected results within p95 — PASS"
  - "Core query — FAIL: [describe mismatch or timeout]"
```

**Product Platform Batches** *(run only if `--platform` argument was provided)*:

**Web platform** (`--platform web` or `--platform all`):
```
options:
  - "Core navigation works without 404 — PASS"
  - "Core navigation works without 404 — FAIL: [describe issue]"
  - "Core form submission returns success — PASS"
  - "Core form submission returns success — FAIL: [describe issue]"
  - "Responsive layout on mobile viewport — PASS"
  - "Responsive layout on mobile viewport — FAIL: [describe issue]"
```

**API platform** (`--platform api` or `--platform all`):
```
options:
  - "Core GET endpoint returns expected schema (200) — PASS"
  - "Core GET endpoint returns expected schema (200) — FAIL: [describe issue]"
  - "Core POST endpoint accepts valid payload (201) — PASS"
  - "Core POST endpoint accepts valid payload (201) — FAIL: [describe issue]"
  - "Auth-protected endpoint rejects unauthenticated request (401) — PASS"
  - "Auth-protected endpoint rejects unauthenticated request (401) — FAIL: [describe issue]"
```

**CLI platform** (`--platform cli` or `--platform all`):
```
options:
  - "Core command executes with default flags — PASS"
  - "Core command executes with default flags — FAIL: [describe issue]"
  - "Config file loads correctly (env vars respected) — PASS"
  - "Config file loads correctly (env vars respected) — FAIL: [describe issue]"
  - "--version prints the correct version — PASS"
  - "--version prints the correct version — FAIL: [describe issue]"
```

## Phase 5: Generate Report

Assemble the full smoke check report:

````markdown
## Smoke Check Report
**Date**: [date]
**Sprint**: [sprint name / number, or "Not identified"]
**Technology**: [engine or stack]
**QA Plan**: [verified actual scope-matched path, or "Not found / scope mismatch / candidate choice pending"]
**QA Plan Binding**: [full SHA-256, bytes, collection time and matched scope; unavailable facts stay explicit]
**Argument**: [sprint | quick | blank]

---

### Automated Tests

**Status**: [PASS ([N] tests, [N] passing) | FAIL ([N] failures) |
NOT RUN ([reason])]

[If FAIL, list failing tests:]
- `[test name]` — [brief failure description from runner output]

[If NOT RUN:]
"Current automated execution is NotRun: [reason]. For permitted historical
reuse, provide recoverable original IDE/CI output bound to exact build/test/config
inputs, scope, runtime and observer. Record historical outcome separately; a bare
"yes" or "tests passed" is insufficient and does not change current NotRun.
Required missing execution/evidence yields INCOMPLETE, not an observed FAIL."

---

### Test Coverage

| Story | Type | Test File | Coverage Status |
|-------|------|-----------|----------------|
| [title] | Logic | `tests/unit/[system]/[slug]_test.[ext]` | COVERED |
| [title] | Visual/Feel | `production/qa/evidence/manual/[slug]-screenshots.md` | MANUAL |
| [title] | Logic | — | MISSING ⚠ |
| [title] | Config/Data | — | EXPECTED |

**Summary**: [N] covered, [N] manual, [N] missing, [N] expected.

---

### Manual Smoke Checks

Record the checks that were actually presented for the detected domain.

**[游戏专用] Example rows:**
- [x] Game launches without crash — PASS
- [x] New game starts — PASS
- [x] [Core mechanic] — PASS
- [x] Save / load — PASS

**[通用产品] Example rows:**
- [x] API health endpoint returns 200 — PASS
- [x] CLI `--help` prints usage — PASS
- [x] Web homepage loads without console errors — PASS
- [x] Core workflow produces expected result — PASS
- [x] Database migrations run cleanly — PASS

**[通用场景] Failure row format:**
- [ ] [check name] — FAIL: [user's description]

---

### Missing Test Evidence

Stories that must have test evidence before they can be marked COMPLETE via
`/story-done`:

- **[story title]** (`[path]`) — Logic story has no test file.
  Expected location: `tests/unit/[system]/[story-slug]_test.[ext]`

[If none:] "All Logic and Integration stories have test coverage."

---

### Platform-Specific Results *(only if `--platform` was provided)*

| Platform | Checks Run | Passed | Failed | Platform Verdict |
|----------|-----------|--------|--------|-----------------|
| PC | [N] | [N] | [N] | PASS / FAIL / NotRun / Blocked / Pending |
| Console | [N] | [N] | [N] | PASS / FAIL / NotRun / Blocked / Pending |
| Mobile | [N] | [N] | [N] | PASS / FAIL / NotRun / Blocked / Pending |
| Web | [N] | [N] | [N] | PASS / FAIL / NotRun / Blocked / Pending |
| API | [N] | [N] | [N] | PASS / FAIL / NotRun / Blocked / Pending |
| CLI | [N] | [N] | [N] | PASS / FAIL / NotRun / Blocked / Pending |

Omit rows for platforms that were not requested.

**Platform notes**: [any platform-specific observations not captured in pass/fail]

Any platform with one or more FAIL checks contributes to the overall FAIL verdict.

---

### Verdict: [PASS | PASS WITH WARNINGS | FAIL | INCOMPLETE]

- **FAIL**: an applicable required executed check failed, including automated,
  manual, data/performance and requested platform checks in every batch.
- **INCOMPLETE**: no observed required failure, but required NotRun/Blocked/Pending/
  Unknown, missing evidence or skipped required scope. Preserve each actual status.
- **PASS WITH WARNINGS**: every required smoke check actually passes with adequate
  exact evidence; only optional follow-up remains with owner/due phase.
- **PASS**: every required smoke check passes, with no pending required gaps.
  Unexecuted platform/product qualification never becomes actual runtime PASS.

`quick` proves only its disclosed checked scope. Omitted checks remain NotRun/
unreviewed and cannot satisfy full-smoke/strict obligations by omission.

````

---

## Phase 6: Write and Gate

Present the full report in conversation and reuse existing exact report path/effect authorization. Only for missing or materially new write scope ask:

"May I write this smoke check report to `production/qa/smoke-[date].md`?"

Write only when that exact report effect is covered by existing or newly obtained authorization.

Update the Memory Bank index only when this run enters its separately named, authorized effect after saving the actual report. Initialized Memory Bank alone is insufficient; read-only and report-only scopes exclude indexing. If the intended effect or initialization is unresolved, retain Unknown. Before indexing, read the saved immutable report and exact input/evidence identities; a proposed output or INFO is insufficient. This effect does not initialize Memory Bank.

When initialized and its named index effect is covered, update
`memory_bank/t3_archive/qa_evidence_index.md`:
- Type: `smoke-check`
- Evidence path: `production/qa/smoke-[date].md` (new revision on path collision)
- Verdict: PASS / FAIL / PASS WITH WARNINGS / INCOMPLETE and actual per-check truth
- Dedupe by evidence path for an authorized current pointer, retaining historical
  revision/input links. Report-write approval alone excludes this effect.
- Without Memory Bank use the report/conversation fallback, disclose absent
  optional index and do not initialize or imply governance activation.

After writing, deliver the gate verdict:

**If verdict is FAIL:**

"The smoke check failed. Do not hand off to QA until these failures are
resolved:

[List each failing automated test or smoke check with a one-line description]

Fix the failures and run `/smoke-check` again to re-gate before QA hand-off."

**If verdict is INCOMPLETE:** disclose required unavailable/unexecuted/pending checks and continue independent evidence work. Do not announce qualified hand-off.

**If verdict is PASS WITH WARNINGS:**

"Required smoke checks passed with optional warnings for the exact checked scope.

Advisory items to resolve before running `/story-done` on affected stories:
[list MISSING test evidence entries]

QA hand-off: share the verified actual QA-plan path and input binding selected
in Phase 1 with the qa-tester for that matched scope."

**If verdict is PASS:**

"Required smoke checks passed for the exact checked scope; broader runtime/platform/product qualification remains as actually recorded.

QA hand-off: share the verified actual QA-plan path and input binding selected
in Phase 1 with the qa-tester for that matched scope."

For either passing smoke verdict, if no usable plan is selected, replace the
plan hand-off instruction with the actual unresolved state and scoped `/qa-plan`
recommendation. Do not substitute an undated/synthesized path, write a plan,
auto-run QA or imply that plan-dependent hand-off is ready. The smoke outcome
still covers only its verified checks; required plan gaps remain INCOMPLETE.

---

## Collaborative Protocol

- NotRun is not PASS or observed FAIL; required incomplete checks yield INCOMPLETE.
  Keep current execution and sufficient permitted historical evidence separate.

- **Never auto-fix failures** — report them and state what must be resolved.
  Do not attempt to edit source code or test files.
- **PASS WITH WARNINGS** applies only to exact checked scope with every required check passing; warnings are optional. Each Story still needs required closure evidence.
- **`quick` argument** skips Phase 3 (coverage scan) and Phase 4 Batch 3.
  Use it for rapid re-checks after fixing a specific failure.
- Use `AskUserQuestion` for all manual smoke check verification.
- **Use named report-write authority**: Phase 6 continues under covered existing
  authorization; ask only for missing or materially new report paths/effects. Index/state effects need their own coverage.
