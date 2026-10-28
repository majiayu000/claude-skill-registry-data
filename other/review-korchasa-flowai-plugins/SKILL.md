---
name: review
description: >-
  Use when the user asks to review CURRENT uncommitted changes (staged,
  unstaged, branch diff) before committing, or to synthesize JiT tests against
  the diff — QA + lead-engineer verdict on quality, architecture, cleanup. Needs
  a diff, not old commits.
---

<!-- GENERATED FROM framework/atoms/review.md via scripts/generate-skill-composites.ts — DO NOT EDIT BY HAND -->

# Task: Review Changes

## Overview

Act as **QA engineer + lead engineer** simultaneously. Review only the **current changes** (diff from the task branch or unstaged/staged changes) against the original request and plan. Verify task completion AND code quality in a single pass. In the same pass, interleave the JiT subset: synthesize ephemeral **Catching JiTTests** — pass on the parent revision, fail on the diff revision — probing behavioural regressions static review cannot see.

## Context

<context>
The user finished (or nearly finished) a coding task and needs a combined review before committing. Review ONLY this task's changes, NOT the whole project. Two hats: **QA** (request satisfied? anything missing, broken, left dirty?) and **Lead Engineer** (well-designed, readable, safe, consistent with project conventions?).

Input sources: git diff (unstaged / staged / `<base>..HEAD`); the original User Request (chat history); the Plan (task tool or task file via the `tasks` role in AGENTS.md); project conventions (`AGENTS.md`, linter/formatter configs); parent worktree (`git worktree add <parent-sha>` with a session-id'd path, or `git show <parent-sha>:<file>` fallback) — used by the JiT subset to verify pass-on-parent behaviour of synthesized catching tests.
</context>

## Rules & Constraints

<rules>
1. **Scope**: Review ONLY changed/added files. Do NOT audit the whole project (that is `maintenance`'s job).
2. **Diff-first**: Start from `git diff`. Every finding must reference a specific file and line in the diff. **"The diff" ALWAYS means tracked changes PLUS untracked files** — `git diff` omits untracked files entirely, so an untracked-only change set is a full review workload, never an empty diff and never a small one.
3. **Two roles, one pass**: Produce findings under two categories (QA, Code Review) but run them in parallel, not sequentially.
4. **Verification**: Do not assume it works — read files, run project checks (linter, tests, type-checker) if available.
5. **Mandatory**: Use a task management tool (e.g., `todo_write`, `todowrite`) to track the execution steps of this review.
6. **Severity levels**: Tag each finding as `[critical]`, `[warning]`, or `[nit]`. Critical = blocks merge. Warning = should fix. Nit = optional improvement. **`[critical]` is reserved for defects in the CHANGED CODE that are established, not inferred**: a check or test that ran and failed, a surviving catching test, a security hole, a broken contract with a caller or a test, behaviour that contradicts an explicit statement (a requirement, a doc, a docstring, the user's request), or a wrong result on the ordinary input the change exists to handle. **A boundary or rare input whose expected result nothing in the project states is a `[warning]`**, however sure you are of what it should return — an uncommon whitespace character, an empty or huge input, an unusual encoding. Name the input and the result you expect, and let the author decide; your expectation is not a spec. A command that never ran is not a failed check either (step 2a). Stale documentation, a missing doc update, and any other artefact the commit phase repairs are `[warning]` by construction, no matter how consequential they look: escalating one stops the workflow before the step that would fix it.
7. **Output**: Final verdict is **Approve**, **Request Changes**, or **Needs Discussion** with actionable items. **`Approve` is MANDATORY, not merely permitted, when the critical count is zero, no catching test survived, and no applicable blocking gate is unsatisfied** — count the criticals and obey the count. `[warning]` and `[nit]` findings are handed to the author inside an `Approve`; a report that says "0 critical findings" and then withholds approval contradicts itself.
8. **Session Scope**: review session changes only — compare current `git status` to the session-start snapshot; files modified/untracked before the session are out of scope (note them, don't review their content). **No snapshot exists** (review is the session's first work, as in a fresh session or a one-shot invocation) → the ENTIRE uncommitted change set is in scope. Absence of a snapshot NEVER means absence of changes. **Exception**: a file/function/feature the user names explicitly is in scope even if it predates the session.
9. **Catching tests = `[critical]` findings**, processed by the same verdict gate as every other critical. No second gate for the JiT subset.
10. **JiT graceful degradation**: the JiT subset disables itself silently when ANY holds — no `test`/`check` command in AGENTS.md (no guessing); a test module covering the changed symbols is red on the parent (step 2b — a red test the diff cannot reach does not count); pure-deletion diff; diff > ~10 files OR > ~500 LOC. Record the reason in `### Degradation Notes` so the lost signal stays visible. **These four are the only reasons.** A small diff, a simple change, and edge inputs you evaluated by hand on the working tree do not switch the subset off and do not stand in for it: a probe that never ran on the parent cannot tell a regression from intended behaviour.
11. **Ephemeral catching tests**: written under a session-id'd scratch dir, either `.flowai/review-jit/<sid>/` (verify `.gitignore` entry first with `grep -qE '^\.flowai/(\*|$)' .gitignore`; append `.flowai/` if missing) or `$(mktemp -d)/review-jit-<sid>/`. Never tracked by git; deletable on `discard`; session-id MUST be unique so parallel reviews do not collide.
12. **Review never edits the code under review**: report risks; the author fixes. This holds for the whole workflow, not just the JiT subset, and it holds after the verdict too — if a pre-existing test contradicts the diff, that contradiction IS the finding, and patching either side destroys it. Asked to fix during the review, answer that fixing is a separate workflow and keep the verdict as it stands; a verdict that turns into Approve because you repaired the code yourself reports on your own work, not the author's. The only files this workflow writes are the ephemeral catching tests in scratch; they leave scratch only through step 11.
13. **Existing-suite gate**: an `Approve` verdict is FORBIDDEN when pre-existing tests cover the changed area and the only tests run for it were authored in the same diff (step 4b). The gate is discharged — not failed — when the repo-wide search of step 4b finds NO pre-existing coverage for the changed symbols or their callers: a brand-new module with its own tests has nothing older to run, and refusing it forever would make every first test file un-approvable. Record the empty search result; the self-authored tests are then the changed area's only coverage, and that fact goes into the report as a `[warning]`, never as a blocker. A located module that cannot run locally leaves the gate unsatisfied without showing a defect: the verdict is then `Needs Discussion` (step 4b). A missing manifest is not such a reason — the module runs with its own runner.
14. **Decision-level verdict, optional diff (Model B)**: LEAD the report with a plain-language verdict the human accepts WITHOUT reading the diff; offer the diff for optional inspection; never block on the human reading code. Delegate heavy diff reading to a diff-analysis subagent (e.g. `diff-specialist`) where supported; else read inline.
</rules>

## Instructions

<step_by_step>

1. **Empty Diff Guard** — `git diff --stat`, `git diff --cached --stat`, `git status --short`. STOP only when ALL THREE are empty. A `??` entry in `git status --short` IS a change: two empty `git diff --stat` outputs plus one untracked file mean a non-empty review, so proceed. System gitStatus snapshot can be stale (hooks / parallel processes); if live status shows unauthored files clean per snapshot, ask user before staging.

2. **Pre-flight Project Check**
   - **Pick the check/test command**: AGENTS.md/CLAUDE.md declares it → manifest detection (`deno.json` → `deno task check`/`test`; `package.json` → `check`/`lint`/`test` script; `Makefile check` → `make check`; `pyproject.toml` → `pytest`/`ruff check .`; `go.mod` → `go vet ./... && go test ./...`) → else "No automated checks configured" in the report and JiT subset disables (Rule 10). Do NOT guess. **"Declares it" means the instructions record an invocation** — a command line, or a task or script name that a manifest in the repository defines. A section that only names an interface (a "Standard Interface" list saying a `check` command exists) while the sections meant for the actual commands are empty declares nothing; fall through to manifest detection.
   - **The project check needs its manifest.** Do not pick a stack-specific project-wide command when the stack's manifest is absent: no `deno task check` without `deno.json`, no `npm test` without `package.json`, no `make check` without a `Makefile`. This rule chooses the PROJECT CHECK only. It does not stop step 4b from running a located test module with the runner that module is written for — `deno test utils_test.ts`, `python -m pytest tests/test_x.py`, `go test ./pkg` — whether or not a manifest exists.
   - **Leave nothing behind.** Note what is untracked before you run anything; afterwards remove every artefact a run created that was not there before (`deno.lock`, `node_modules/`, `__pycache__/`, `.pytest_cache/`). A leftover gets swept into the commit.
   - **2a (current revision)**: run on working tree. Skip only if no code files changed since the last run of the whole check in this session whose failures were all classified (none, or all on the baseline record). **Classify each failing test before you grade it.** When this session holds a **baseline record** — the file of tests that failed before the change, written by the implement phase — a test on the record is pre-existing: list it under Automated Checks as pre-existing, not as `[critical]`, and do not rerun the suite to confirm it. Without a record, rerun only the failing tests, each one alone, in the parent worktree of step 2b (create it now): failing there too → pre-existing; passing there → the diff broke it. A failure the diff caused is `[critical]`; report it and continue review. **A command that never ran has not failed**: exit 127, `command not found`, or a missing task or script name means the project declares no runnable check. Report it as `[skipped] <command> — not runnable: <error>` under Automated Checks, say "No automated checks configured", disable the JiT subset (Rule 10), and raise no `[critical]` for it.
   - **2b (parent baseline — JiT)**: identify parent (unstaged/staged → `HEAD`; commit-range → `<range-start>^`). Build the parent as a separate tree: `git worktree add
     <SCRATCH>/jit-parent-<sid> <parent-sha>` (full runnable tree); use
     `git show <parent-sha>:<path>` (printed, or written into a scratch dir) ONLY if worktree-add fails. **Never take the diff out of the working tree to reach the parent** — no `git stash` in any form, no `git checkout -- <path>`, `git restore` or `git reset` of the diff's files. A session cut off before the diff is put back leaves the working tree without the author's work. This holds for every look at the parent during the review, not only this step: rerunning one failing test on the parent, comparing lint or type-check output before and after, reading the old version of a file. Run those in the parent worktree from this step (create it then if this step was skipped), and remove it with `git worktree remove` before the review ends — after step 8b has run the probes in it, not before. BEFORE any JiT synthesis, run inside the parent worktree the pre-existing test modules that cover the changed symbols — the modules step 4b locates (locate them now if 4b has not run yet) — each one scoped the way step 4b runs it, and verify they pass. **Not the project's whole suite**: on a real repository the whole suite takes minutes, it already ran on the diff side in 2a, and it is often red on the parent for reasons that have nothing to do with the diff — a red test the diff cannot reach is no reason to switch the JiT subset off. **Two things do NOT satisfy this and are the usual substitutes:** the run of those modules you already did on the DIFF side (it says nothing about the parent), and running only your synthesized JiT probes against the parent (they are not the project's tests). The evidence this step wants is one run of the covering modules whose working directory is the parent tree. No pre-existing module covers the changed symbols → there is nothing to verify, and each probe's own pass on the parent (step 8b (a)) is its baseline. Fallback path OR a covering module red on the parent → "JiT disabled — parent baseline unavailable/red" in Degradation Notes, naming the module; review continues without the JiT subset.

3. **Gather Context**
   - **First**: resolve `SRS`, `SDS`, and `tasks` from AGENTS.md; read the resolved `SRS`/`SDS` files if their content is not already in context. A required role missing → report it and continue only with review steps that do not depend on that role. **AGENTS.md is the FIRST document you open, and no conventional location is probed before it.** The doc layout you have seen most often is one project's convention, not the shape of every project; a speculative `cat <guessed-path> 2>/dev/null` batched alongside the AGENTS.md read is still reading the wrong file first, and discarding its output afterwards does not undo that. Projects that keep their SRS and SDS somewhere else entirely exist, and they are exactly the ones this step is for.
   - Create a review plan in the task management tool.
   - Collect the diff: `git diff` (unstaged), `git diff --cached` (staged), or `git log --oneline <base>..HEAD` + `git diff <base>..HEAD` for branch-based changes.
   - **Untracked files**: `git diff` does NOT show them — read each untracked file from step 1's `git status` and include it in scope.
   - Read the original user request and the plan (task file under the resolved `tasks` role / task list).
   - Note project conventions from linter/formatter configs and patterns visible in the diff and surrounding code.
   - **3d (intent hints — JiT)**: collect intent-author hints for the JiT subset: `git log -1 --pretty=%B <parent-sha>..HEAD` (or commit messages of the range). Optionally `gh pr view --json body` IF `gh` is available AND the branch has a PR; on missing/error proceed silently — PR body is a bonus.
   - **3e (intent inference — JiT)**: derive a list of ≤5 explicit intents for the diff in the form "the author tried to do X; invariants Y should hold". Pull from (a) the task file's DoD items, (b) commit messages from 3d, and (c) the diff hunks. >5 candidates → merge related or drop the least-risky. Skip if the JiT subset is disabled (Rule 10).

   **Parallel Delegation** (after gathering context):
   - **Small diff shortcut**: skip delegation only when the change set is under 50 lines IN TOTAL — `git diff --stat` plus `git diff --cached --stat` plus `wc -l` over every untracked file from step 1. Count the lines before deciding; `git diff --stat` alone reports 0 for an untracked-only change set, and file COUNT is not the threshold (one 173-line file is a large diff, not a small one).
   - Otherwise, delegate **2 independent tasks in parallel** to SEPARATE agent contexts — a subagent or a background task (e.g. `Task`, `Agent`, `task`; on Codex the tool is `spawn_agent` — pass `agent_type="console-expert"` and `fork_turns="none"` (a full-history fork cannot carry an agent type), then collect with `wait_agent`), each returning its result to you. **Batching several tool calls in your own thread is NOT delegation**: the point is to keep the check output out of your context, which only a separate context achieves. **Establish availability by LOOKING, never by assuming**: list the agent directories (`ls .claude/agents/ .cursor/agents/ .opencode/agent/ "${CODEX_HOME:-$HOME/.codex}/agents/" 2>/dev/null`). A file there — `.md` for most hosts, `<name>.toml` under the Codex home — means that agent is installed and dispatchable — dispatch it by name. Running inside a sandbox, a test harness, or an automated run is NOT evidence of missing subagents and is never a reason to skip: decide from the listing, not from where you think you are. **Run the listing BEFORE any inline check, and quote its output in `### Degradation Notes` whenever you claim delegation was unavailable.** The claim is a factual report about this machine, and without the command's output behind it you are stating something you did not check: a review that ran the checks inline and wrote `Parallel delegation unavailable` on top of an installed agent directory reported a fact that was false. Inline is permitted only when the listing came back empty AND no subagent tool is in your toolset — both verified, not assumed. Do not silently call a batch of your own tool calls a delegation. **Speed is not one of the two conditions.** "Faster than spinning up a subagent", "the file is only 181 lines", "I have already read it" — none of these reopen the shortcut, which is decided once, by the line count in step 1, and not revisited per task. The point of delegation is to keep the check output out of YOUR context; doing the work yourself because it is quick spends exactly what the step exists to save. **And it is per task, not per review**: SA1 and SA2 are two dispatches, so delegating one and running the other inline is a partial degradation that must be recorded as such — it is not delegation performed.
     - **SA1**: skip if pre-flight check (step 2a) already ran. Otherwise run the project check command **chosen via the same manifest-detection rule from step 2** (never stack-specific commands without the manifest). Delegate to a console/shell-capable agent (e.g., `console-expert`); return pass/fail + full output.
     - **SA2**: hygiene grep scan on the diff — `TODO`, `FIXME`, `HACK`, `XXX`, `console.log`, `temp_*`, `*.tmp`, `*.bak`, hardcoded-secret patterns. Same delegation; return findings list.
   - **Collect what you dispatched**: many subagent tools dispatch in the background by default and answer with a handle (an agent id plus token/duration counters) instead of the result. When your tool offers a foreground or blocking mode (a `run_in_background: false` parameter or equivalent), set it. If you still get back only a handle, continue that agent by its id — send it a message or resume it and ask for its result. Do NOT feed an agent id to a background-task polling tool: the two id kinds are different, and the poll answers `No task found with ID: <id>` however long you give it. Never write a delegated finding you did not actually receive. **And never end your turn while a dispatch is outstanding.** Sitting idle until a notification arrives is not waiting — the turn closes, the session ends there, and the review produces no verdict, no report and no findings at all: strictly worse than the inline run you were avoiding. Collecting is an action you take, not an event you receive.
   - **Fallback rule**: a delegated task genuinely fails, or is still unfinished when you have exhausted the collection budget → the main agent performs that step inline and says so in `### Degradation Notes`. No hard dependency on delegation success.
   - Continue with steps 4, 6, 7, 8 (main agent review) while delegated tasks run — then collect before writing the report.

4. **QA: Task Completion**
   - Map each requirement/plan item to concrete changes in the diff.
   - Flag requirements with no corresponding changes as `[critical] Missing`.
   - Flag plan items marked "done" but not present in diff as `[critical] Phantom completion`.
   - Check for regressions: do changed files break existing functionality?
   - **Doc drift**: for each changed source path, read the docs that describe it (the Documentation Map in AGENTS.md when present, else the resolved `SRS` / `SDS` / `README`). A doc still describing behaviour the diff removed or changed → `[warning] Doc drift` naming the doc `file:line` and the contradicting hunk. Drift alone is NEVER `[critical]` and never blocks the verdict — the commit phase owns Documentation Sync, so escalating here would stop the workflow before the step that fixes it. Do NOT edit the doc in this review.

4a. **FR Coverage Audit** _(blocking gate — see Requirements Lifecycle in AGENTS.md)_
   - **Applicability first**: this gate encodes a project convention, not a universal rule. It applies ONLY when the project itself declares it — an `SRS` role resolves from AGENTS.md AND that AGENTS.md mandates FR traceability (acceptance references, `[REF:fr:<id>]` code markers). Neither present → skip 4a entirely, record `FR coverage gate not applicable — project declares no requirements lifecycle` in `### Degradation Notes`, and NEVER emit a `missing code marker` / `no acceptance reference` finding. Inventing the convention for a project that does not use it turns every clean diff into `Request Changes`. **The `SRS` role resolves but its file does not exist** → skip 4a the same way: record `FR coverage gate not applicable — <SRS path> does not exist` in `### Degradation Notes`, and NEVER emit a `[critical]` (or any blocking) finding for the missing document or for an acceptance reference it would hold. Creating the requirements document is `init`'s job, not this review's; the commit gate reports the same absence in one line and commits.
   - **FRs in scope**: (a) FR-* in the task file's `implements:`; (b) FR sections added/modified in the diff to `SRS`; (c) `[REF:fr:<id>]` SALP markers touched in the diff.
   - **Per FR**: (1) SRS has `**Acceptance:**` with a runnable ref (test `path::name`, benchmark id, command, or `manual — <reviewer>`); missing/placeholder → `[critical] no acceptance reference`. (2) Run the evidence command (or `deno run -A scripts/check-fr-coverage.ts FR-<ID>`); non-zero / failing / `manual` without reviewer → `[critical] acceptance fails`. (3) FR claimed implemented but no `[REF:fr:<id>]` marker in changed source → `[critical] missing code marker`. (4) DoD `[x]` with no evidence run/cached pass → `[critical] Phantom completion`. (5) Only when the project's AGENTS.md declares the mandatory `**Rationale:**` field (a `Rationale-as-gate` rule or an equivalent sentence): every FR section the diff ADDS or MODIFIES in `SRS` — scope (b) only, never an FR the diff merely cites — carries a non-empty `**Rationale:**` line saying why the requirement exists; missing or empty → `[critical] no rationale`, naming the FR. Report it; do not write the rationale yourself.
   - **Gate**: blocking — verdict cannot be `Approve` while any FR-gate issue remains.

4b. **QA: Existing-Suite Execution** _(blocking gate — Rule 13)_
   - **Locate** the repository's PRE-EXISTING test module(s) covering the changed symbols: grep the WHOLE repository — not just the directory the change lives in — for each changed symbol AND for its direct CALLERS (importers); transitive coverage often never names the changed symbol. Exclude test files added by this diff.
   - **Do these three things before you decide what to run**, and say what each returned: (1) grep the whole repository for the changed symbol and for its importers; (2) read AGENTS.md for a section naming test suites kept outside the default check — contract, integration, e2e, acceptance — and how to run them; (3) open the test-runner config and read the check/test task's `exclude` list and any path it is scoped to. Each one can surface coverage the other two miss, and skipping the last two is how a suite that exists gets reported as absent.
   - **The project's check or test command is NOT this search, and running it does not discharge this step.** Those commands encode what the project runs on every change; this gate asks what covers the symbols YOU changed, and the two differ by design. A suite the check command deliberately excludes — contract tests, integration tests, anything a config `exclude` or a scoped path argument skips — is precisely what this gate exists to reach: it was excluded for cost, not because it stopped being coverage. Before deciding what to run, read AGENTS.md for a section naming where such tests live and how to run them, and check the test-runner config for `exclude` entries and for scoped paths in the check task. If either points at a suite covering your changed symbols, run it. "The project check passed" is not an answer to this step; name the modules you located and the command you ran on each.
   - **RUN** each located module, scoped per AGENTS.md conventions — never a full-suite run. Any failure → `[critical]`; verdict cannot be `Approve`. A pre-existing test that contradicts the diff is a finding under Rule 12, not a file to update. Use the project's scoped test command when it has one; otherwise run the module with the runner it is written for (`deno test <file>`, `python -m pytest <file>`, `go test ./<pkg>`). A missing manifest does not stop this run — the manifest rule of step 2 picks the project check only — and step 2's cleanup applies to whatever the run leaves behind.
   - None found → record "no pre-existing coverage for the changed symbols" (quote the searches that came back empty); Rule 13 is discharged by that record, and the missing prior coverage is reported as a `[warning]`.
   - Module cannot run locally (live service, missing env, its runner not installed) → record module + reason + the command you tried in `### Degradation Notes`; never fabricate a pass. The gate stays unsatisfied, yet nothing in the change has been shown wrong, so the verdict is `Needs Discussion` — not `Request Changes` and not `Approve`: the human decides whether to merge without that run.
   - Self-authored tests NEVER satisfy this gate, regardless of how many pass.

5. **QA: Hygiene** _(use SA2 result if available; else inline)_
   - **Say in the report that the scan ran, including when it found nothing.** A clean scan and a scan that never happened look identical on a page that only lists findings, so a hygiene line is required either way — findings, or `Hygiene: clean (N patterns scanned over the diff)`.
   - SA2 done → dedupe its findings with own Code Review findings and merge.
   - SA2 failed/timed out or skipped (small diff) → scan inline:
   - **Temp artifacts**: the SA2 pattern list from step 3, plus debug `print` output and hardcoded secrets or localhost URLs.
   - **Unfinished markers**: new `TODO`/`FIXME`/`HACK`/`XXX` introduced in this diff (distinguish from pre-existing ones).
   - **Dead code**: commented-out blocks, unused imports/variables/functions added in this diff.
   - **Deleted directories**: diff deletes an entire skill/agent/module directory (not just files) → `[warning] Entire directory deleted — confirm intentional`; ask the user to verify before proceeding.

6. **Code Review: Design & Architecture**
   - **Responsibility**: each changed file/module stays within its stated responsibility? Flag scope creep.
   - **Coupling**: new dependencies (imports, API calls) justified? Flag tight coupling and circular dependencies.
   - **Abstraction**: appropriate level? Flag over-engineering (unnecessary interfaces, premature generalization) and under-engineering (god-functions, duplicated logic).
   - **Risk hypotheses (JiT side-channel)**: while reading each hunk, accumulate ≤3 risk hypotheses per intent (from Step 3e): "if the author, while doing X, had slipped on Y, the code would now fail at Z". Risks MUST be diff-specific — not generic code smells ("null deref") unless the diff directly exposes that risk. Skip if the JiT subset is disabled.

7. **Code Review: Implementation Quality**
   - **Naming**: new identifiers clear and consistent with project conventions?
   - **Error handling**: explicit? Flag swallowed exceptions, missing error paths, generic catch-all handlers.
   - **Edge cases**: boundary conditions handled (null, empty, overflow, concurrent access)? An unhandled boundary whose expected result nothing in the project states is a `[warning]` (Rule 6).
   - **Types & contracts**: precise signatures? Flag `any`, untyped parameters, missing return types (where project conventions require).
   - **Tests**: new/changed behaviors covered? Existing tests updated for changed behavior?
   - **Risk hypotheses (JiT side-channel)**: continue accumulating risks started in Step 6 (see Step 8a for the mutation taxonomy).

8. **Code Review: Readability & Style**
   - **Consistency**: changes follow the project's established patterns (file structure, naming, formatting)?
   - **Comments**: non-obvious decisions explained? Flag misleading or stale comments.
   - **Complexity**: flag functions > 40 lines or cyclomatic complexity spikes introduced in this diff.
   - **Clarity**: flag clarity sacrificed for brevity — nested ternaries, dense one-liners, overly compact expressions. Explicit code is preferred over clever short forms.

8a. **Mutant + Catching Test Synthesis (JiT)** _(skip on pure-deletion diff or JiT-disabled flag)_
   - Generate ≤15 mutants total (≤5 intents × ≤3 risks × 1 mutant per risk), each modelling a concrete diff-specific failure mode. Typical mutations: comparator flip, removed guard, inverted return, off-by-one, swapped args, skipped branch.
   - For each mutant, synthesize ONE ephemeral test that:
     1. Compiles / parses in the project's test language.
     2. Passes on the parent revision.
     3. **Kills** the mutant (fails with the mutation applied; passes on the current diff code iff it preserves the parent behaviour).
   - Write tests to the session-id'd scratch directory (Rule 11). Never colocate next to the file under test in the main test tree.

8b. **Dual-Run + Filter (JiT)** _(skip if Step 8a skipped)_
   - **(a) parent**: run the generated tests against the parent worktree from Step 2b. Any test that FAILS on the parent is an assumption leak — discard it.
   - **(b) diff**: run the surviving tests against the diff revision. Any test that FAILS here is a **Catching JiTTest** — record it for the final report with file:line and the assertion output.
   - **(c) mutant kill-rate** _(optional)_: apply each mutant patch to the diff tree, re-run the matching test, record whether the mutant is killed. SKIP if a single smallest-scope test invocation exceeds 30 s — write `Mutant kill-rate skipped — single test invocation exceeded 30 s threshold (recorded N s)` in Degradation Notes so the lost signal stays visible.
   - **Filter ensemble**, in order:
     1. **Flaky** — rerun each surviving test 3 times; if the result flips, discard.
     2. **Assertion duplicates** — two tests asserting the same thing on the same input.
     3. **Zero-kill** — passed on parent, passed on diff, killed no mutant.

9. **Run Automated Checks** _(collect from step 2 and/or SA1)_
   - Pre-flight 2a ran → use its result, do NOT re-run. SA1 broader check → merge.
   - Neither ran (no check command) → note "No automated checks configured" in the report; do not silently skip.

10. **Review Report** — verdict on first line. Include JiT sections (`Intents`, `Catching Tests`, `Uncovered Risks`, `Degradation Notes`) only when the JiT subset ran (or was disabled — Degradation Notes then explains why). Section order:

   ```
   ## Review: [Approve | Request Changes | Needs Discussion]   <!-- count your [critical] findings BEFORE writing this line; zero criticals with no surviving catching test and no unsatisfied applicable gate => Approve -->
   ### Verdict (plain language) — 2–4 sentences a non-coder acts on, answering ALL four questions explicitly, each in words of its own: (1) is the task complete; (2) is the design sound — say so even with no concern ("the design is sound"); (3) the key risks, or that there are none; (4) the next step. A blocking finding never replaces the design answer: a change can be well designed and still not mergeable. Accept WITHOUT reading the diff. MUST come first.
   ### Intents (≤5)
   ### QA Findings — [severity] file:line — description
   ### Code Review Findings — [severity] file:line — description
   ### Catching Tests (pass on parent, fail on diff) — name, intent #, mutant killed?, failure, file:line
   ### Uncovered Risks — risk + reason no test (non-deterministic / I/O / etc.)
   ### Existing-Suite Check — pre-existing modules (incl. caller tests) + run result, or why not run
   ### Automated Checks — [pass|fail|skipped] command — summary
   ### Degradation Notes — which JiT step was skipped and why
   ### Summary — requirements X/Y; catching tests N; hygiene scan result (findings or `clean`); critical/warning/nit counts
   ### Diff (optional) — offer diff/details for optional inspection; verdict stands without it; never block (Model B). MUST be the report's last section.
   ```

   **This report is the answer of the review.** Step 11 is the only thing that follows it. When you made a scratch directory, the save / discard question is the last line of this answer: name the scratch path, ask, and end your turn. Delete or move nothing before the reply — the end of your turn is not a timeout, and `default for timeout/ambiguous` means an unclear reply, not a missing one.

   **Every later turn of this conversation stays inside the review.** The author's reply to the report — an answer to a question it asked, "go ahead", a request to fix a finding, add tests, fill a missing field, or commit — does not start the next workflow. Reply in words only: what the answer changes in the verdict, or that it changes nothing; which workflow does the requested work (implement for a fix, commit or review-and-commit for a commit), started by name; and that the verdict stands until a fresh review. Edit no file, stage nothing, commit nothing, and do not offer to do any of these yourself — an offer the author accepts ends in the same edit or commit. Committing belongs to the commit workflow, which owns the documentation sync and atomic grouping this review does not run.

   **After the verdict the review is over — including when the author asks you to fix what you found.** A reviewer who repairs the code then reports on their own work, and the finding that made the verdict disappears with the repair, so nobody can check it afterwards. Answer that the fix is the author's to make, or belongs to a separate implement run that the author starts by invoking that workflow by name. A reply in this conversation — "yes", "go ahead", "fix it", "add the tests", an answer to a question your report asked — is not that invocation, however explicit, and does not hand the fix to you. Leave the verdict where it stands. This holds for production files, for tests, for the requirement documents in the diff, AND for pre-existing tests: when a pre-existing test contradicts the diff, the contradiction IS the finding, and editing either side deletes the evidence rather than resolving it. Continuing to run the project's checks or to explain a fix in words is fine; writing the fix is not.

   **Verdict selection** (decide in this order, first match wins): (1) `Request Changes` — ≥1 `[critical]` finding, ≥1 surviving catching test, or an APPLICABLE blocking gate (4a FR coverage where 4a applies at all, 4b existing-suite, Rule 13) still unsatisfied — except a 4b module that could not run locally, which goes to (2). (2) `Needs Discussion` — no blocker, but a design decision genuinely needs the human before merging, or a located pre-existing module could not run locally (step 4b). (3) `Approve` — everything else, and this branch is compulsory once reached. `[warning]` and `[nit]` findings NEVER force `Request Changes` on their own: list them, hand them to the author, approve. An `Approve` carrying warnings is the normal outcome, not a contradiction. Rank findings top-5 by `severity × uniqueness`. No issues AND zero catching tests → "Changes look good. All requirements covered, no issues found, no behavioural regressions detected." (last clause only when JiT actually ran).

11. **Ephemeral Dispose (JiT)** _(skip ONLY when you created no scratch directory)_ — prompt: `save <name>` / `save all` / `discard all`. On `save`: propose destination beside file-under-test, confirm, `git mv`, stage. On `discard all` (default for timeout/ambiguous): delete entire scratch directory, leave no stray files. **A scratch directory you made is yours to remove, and the verdict is not the end of the run while one is still on disk.** This step goes missing in the same way every time: the report reads finished, the catching test has already done its job, and the leftover directory is invisible to you and permanent to everyone else — a run that names its scratch path in the report and then leaves it there without asking has documented the mess rather than cleaned it. Whether you wait for the answer depends on the report's role, stated right after the report template. Removing the parent worktree is a different cleanup and does not cover this.

</step_by_step>

## Verification

<verification>
[ ] Empty diff guard checked before starting.
[ ] Pre-flight project check executed on current revision (or skipped — no code changes since last check); each failing test classified from the baseline record, or by rerunning that test alone on the parent — never by another run of the whole suite.
[ ] Parent baseline (JiT step 2b) executed in `git worktree` (or graceful skip in Degradation Notes).
[ ] Diff collected and reviewed (not the whole project).
[ ] Each requirement/plan item mapped to changes.
[ ] FR Coverage Audit: every FR in scope has runnable Acceptance reference, passing test, code marker, no phantom `[x]`.
[ ] Existing-Suite gate: repo-wide grep, AGENTS.md out-of-check suites, and the runner config's `exclude` / scoped paths all consulted; pre-existing modules (incl. caller tests) located and RUN by name — or reason recorded; the project check command alone does NOT satisfy this; no Approve on self-authored tests alone while pre-existing coverage exists (an empty repo-wide search discharges the gate with a `[warning]`).
[ ] Intents enumerated (≤5) when JiT subset active.
[ ] Risk hypotheses tied to intents (≤3 per intent), diff-specific.
[ ] Hygiene: no temp files, debug output, unfinished markers in diff.
[ ] Design review: responsibility, coupling, abstraction.
[ ] Implementation review: naming, errors, edge cases, types, tests.
[ ] Readability: consistency, comments, complexity.
[ ] Catching tests (if any): passed on parent, failed on diff, stored in the session-id'd scratch dir (outside test tree and git).
[ ] No production code modified by the JiT subset.
[ ] Automated checks executed (or explicitly noted as missing).
[ ] Structured report with severity-tagged findings.
[ ] Verdict on the first line; catching tests pushed verdict to Request Changes when present.
[ ] Report leads with a plain-language decision-level verdict that answers all four questions (task complete, design sound, key risks, next step) and closes with optional, non-blocking diff inspection (Model B).
[ ] Save / discard prompt issued whenever catching tests existed; scratch dir deleted on `discard`.
[ ] Degradation Notes present whenever the JiT subset was disabled, partially skipped, or mutant-probe bypassed.
</verification>
