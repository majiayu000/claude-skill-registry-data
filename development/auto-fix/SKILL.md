---
name: auto-fix
description: >-
  CRITICAL: ONLY activate this skill when the user explicitly triggers the `/fix` or `/auto-fix` slash command.
  DO NOT auto-trigger or invoke this skill for general coding, debugging, refactoring, or problem-solving tasks.
  When invoked via `/fix` or `/auto-fix`, executes a systematic 9-stage TDD bug-fixing workflow with interactive selection, plan freezing, ponytail minimal fix, subagent regression verification, and automated git commit-push.
argument-hint: "<problem description>"
---

# Auto-Fix Workflow

Systematic, test-driven bug-fixing workflow enforcing targeted test runs, plan immutability, surgical minimal code changes via `ponytail`, independent subagent regression review, and atomic git commit & push.

---

## 0. Invocation Guard

Check the initiating user prompt:
- If this turn was **NOT** explicitly initiated by `/fix` or `/auto-fix` (e.g. `/fix <description>` or `/auto-fix <description>`), **ABORT** this workflow immediately and proceed with normal conversational or coding behavior without applying auto-fix constraints.
- Do **NOT** auto-trigger for general troubleshooting, bug reports, or when words like "fix", "bug", or "issue" appear in casual conversation.
- Do **NOT** persist across subsequent turns unless the user explicitly invokes `/fix` or `/auto-fix` again.

---

## Core Invariant: Run Necessary Tests Only

Across ALL testing stages:
- **Never run full-workspace or monolithic test suites.** Blind execution of entire project test suites wastes time and catches unrelated flakiness.
- **Target only the specific file or pattern**: Execute only the isolated reproduction test or affected module tests (e.g. `npm test -- path/to/target.test.mjs`, `pytest tests/test_module.py::test_case`, `go test ./pkg/... -run TestName`).

---

## Stage 1: Triage & Code Analysis

1. Trace execution paths and inspect all relevant files, callers, and data flows.
2. Identify the root cause behind the reported symptom.

### Handling "No Problem Found" or Ambiguity
If the code appears to work as designed, the issue cannot be reproduced, or the description is under-specified:
- **Do NOT fabricate a problem or jump to speculative changes.**
- Explain what was inspected and why the current implementation appears correct.
- Invoke `ask_question` to let the user triage:
  1. *Provide additional reproduction details* (error payload, stack trace, environment specifics) -> Loop back to Stage 1.
  2. *Write expected behavior test anyway* -> Construct a test asserting the user's expected behavior. If it passes, it proves the code already works as expected and workflow halts cleanly. If it fails, it isolates the problem and advances to Stage 2.
  3. *Close / Working as Intended* -> Exit cleanly without modifying codebase files.

---

## Stage 2: Build Reproduction Test (Red Phase)

1. Write an isolated test that triggers the bug and asserts the expected behavior.
2. Execute the test using `run_command` (running **necessary tests only**).
3. Confirm the test **FAILS** with the expected error before touching any production code.

---

## Stage 3: Explain & Multi-Fix Comparison

1. Provide a concise explanation of the root cause.
2. If more than one clean way to fix the problem exists:
   - Outline the viable options (e.g. boundary guard, handler refactor, configuration adjustment).
   - Compare tradeoffs: blast radius, complexity, maintainability, and line impact.
   - Give an explicit recommendation based on minimalism and safety.

---

## Stage 4: Interactive User Decision

Use the `ask_question` tool to solicit the user's decision:
- List each viable fix option (prefixing your recommendation with `(Recommended)`).
- Include an explicit option: `"Abort: Cancel fix"`.
- Block execution until the user selects an option.
- **Abort Handling**: If the user selects "Abort", **preserve all reproduction test files intact** (do not delete or clean them up) for future inspection, and halt immediately.

---

## Stage 5: Formulate Surgical Implementation Plan (Plan Freeze & Artifact)

Before making any modifications to production code:
1. Formulate a step-by-step surgical implementation plan for the chosen fix:
   - Target files, functions, and line ranges.
   - Planned minimal diff (exact replacement snippet).
   - Targeted verification test command.
2. **CREATE PLAN ARTIFACT (MANDATORY)**:
   - Write the complete plan as an artifact file at `<Artifact Directory>/auto_fix_plan.md` using `write_file` with `ArtifactMetadata`:
     - `Summary`: "Frozen surgical implementation plan for auto-fix"
     - `UserFacing`: `true`
     - `RequestFeedback`: `false`
   - Inside the artifact, detail:
     - Root cause summary
     - Target files & line numbers
     - Full proposed replacement diff
     - Verification command
     - Lock banner: `> [!IMPORTANT]\n> This plan is FROZEN and IMMUTABLE. Stages 6–8 must strictly adhere to this specification.`
3. **VISIBLE CHAT NOTIFICATION**:
   - In chat, present a clickable link to the newly created artifact and summarize the target scope:
     ```markdown
     ### 📋 Stage 5: Frozen Implementation Plan (🔒 LOCKED)
     The implementation plan has been generated as a dedicated artifact:
     👉 [auto_fix_plan.md](file:///<absolute-path-to-artifact>)

     - **Target File(s)**: `path/to/file`
     - **Planned Scope**: Minimal surgical fix applying `ponytail`
     - **Verification Command**: `<command to run necessary reproduction test only>`
     - **Status**: 🔒 Frozen — no changes to this plan are permitted during Stages 6–9.
     ```
4. **PLAN FREEZE**: Once written to the artifact, this plan is **strictly locked and immutable**. Stages 6 through 9 must strictly execute against this artifact and are forbidden from altering scope, expanding diffs, or introducing ad-hoc redesigns.

---

## Stage 6: Execute Plan & Deliver Minimal Fix (Applying `ponytail`)

Carry out the Stage 5 plan step-by-step applying the **`ponytail`** skill principles:
1. **The Ponytail Ladder**:
   - Reuse existing codebase helpers > Standard Library > Native platform features > Minimum lines.
   - Zero boilerplate, zero unrequested abstractions, zero speculative generality.
   - Fix root cause over symptom: fix once where all callers route through.
   - Shortest working diff wins.
2. Apply the minimal modifications to the target files.
3. Re-run the Stage 2 reproduction test (running **only that necessary test**).
4. Verify the test transitions from **RED** to **GREEN**.

### Controlled Plan Invalidation & Revision Protocol
If the planned diff fails to make the test pass or hits a technical blocker during implementation:
- **Zero Silent Deviation**: Never quietly edit unrelated files or expand scope without logging.
- **Case A: Minor Tactical Amendment** (same strategy, e.g. missing null guard, type cast, or import):
  1. Append an amendment entry to `<Artifact Directory>/auto_fix_plan.md`:
     ```markdown
     ### 📝 Amendment #1: <brief description>
     - **Reason**: <why adjustment was necessary to pass test>
     - **Adjusted Diff**: <new minimal replacement snippet>
     ```
  2. Note in chat: `> ℹ️ Plan Amendment #1: [brief reason]`
  3. Apply the amendment and re-verify the Stage 2 reproduction test.
- **Case B: Major Strategic Invalidation** (approach is fundamentally unviable):
  1. **Halt immediately.** Do not touch further files.
  2. Explain the fundamental roadblock clearly.
  3. Call `ask_question` with options:
     - Pivot to Alternative Strategy (describe approach)
     - Abort fix workflow
  4. If user approves pivot, update `auto_fix_plan.md` with the new plan and resume Stage 6. If user aborts, preserve tests and halt.

---

## Stage 7: Multi-Dimensional Post-Fix Review

Conduct three independent verification checks:

### 1. Issue Resolution Proof
Confirm the Stage 2 reproduction test passes consistently.

### 2. Regression Subagent Review
Invoke a subagent using `invoke_subagent`:
- `TypeName: "self"`
- `Role: "Regression Tester & Verifier"`
- Prompt the subagent to:
  a) Inspect the `git diff` of the changes.
  b) Analyze potential edge cases, boundary conditions, and direct callers affected by the modified lines.
  c) Write complementary regression test cases covering only the affected function/module.
  d) Run **only the necessary tests** (the new regression tests and direct unit tests of the touched module).
  e) Report any discovered regressions, unexpected side effects, or verify all green.

### 3. Simplicity / YAGNI Audit
Evaluate the final diff against Ponytail rules:
- Were any unnecessary abstractions, interfaces, or unused parameters added?
- Could this fix be safely expressed in fewer lines?

---

## Stage 8: Consolidated Status Report & Plan Compliance Audit

Present a clear, structured report to the user:
1. **Root Cause & Fix Summary**: What was broken and the chosen resolution.
2. **TDD Proof**: Reproduction test output transitioning from RED to GREEN.
3. **Regression Audit Results**: Findings from the subagent and pass status of edge-case tests.
4. **Simplicity Rating**: Confirmation of minimal diff and zero over-engineering.
5. **Plan vs. Reality Audit**:
   - Compare the final code changes delivered in Stage 6 and any follow-up actions taken in Stage 7 against the frozen artifact: [`auto_fix_plan.md`](file:///<path-to-artifact>) and any logged amendments.
   - Include a plan compliance checklist:
     - Target files matched artifact plan? (Yes / No)
     - Diff scope matched artifact plan + logged amendments without extra modifications? (Yes / No)
     - Any amendments logged and justified? (Yes / None needed / Unlogged divergence)
     - Verification test command matched artifact plan? (Yes / No)
   - Explicitly certify whether the implementation complied 100% with the frozen plan (or approved amended plan), or detail any deviations made and the reasons why.

---

## Stage 9: Automated Git Commit & Push (Applying `git-commit-push`)

Upon completing the Stage 8 report, automatically commit and push the verified changes following the **`git-commit-push`** skill protocol:

1. **Git Worktree Verification**:
   - Check if inside a git worktree (`git rev-parse --is-inside-work-tree`). If not a git repository, skip this stage cleanly.

2. **Pre-Flight Fast Leak & Size Scan**:
   - Ensure no secrets or sensitive files (`.env*`, `*.key`, `*.pem`, `token.txt`, `credentials.json`) are untracked or modified.
   - Ensure no large files (> 5MB) were added.

3. **Surgical Staging**:
   - Stage ONLY the files modified by the fix, the reproduction test file(s), and newly created regression test file(s):
     ```bash
     git add <modified_files> <test_files>
     ```
   - Do NOT run blind `git add .` to avoid staging unrelated workspace changes.

4. **Conventional Commit Message**:
   - Synthesize a Conventional Commit message from the root cause and fix:
     ```text
     fix(<scope>): <imperative summary under 72 chars>

     - Root cause: <concise summary>
     - Fix: <brief summary of minimal fix>
     - Tests: reproduction and subagent regression tests verified
     ```

5. **Atomic Commit & Push**:
   - Execute commit and push in one compound command with upstream fallback:
     - **PowerShell**:
       ```powershell
       git commit -m "<message>"; if ($LASTEXITCODE -eq 0) { git push; if ($LASTEXITCODE -ne 0) { git push -u origin (git rev-parse --abbrev-ref HEAD) } }
       ```
     - **Bash / POSIX**:
       ```bash
       git commit -m "<message>" && (git push || git push -u origin $(git rev-parse --abbrev-ref HEAD))
       ```

6. **Summary Output**:
   - Output the concise 3-line commit summary:
     - **Commit**: `<hash>` — `<message title>`
     - **Branch**: `<branch>` (pushed to remote)
     - **Files**: List of committed files
