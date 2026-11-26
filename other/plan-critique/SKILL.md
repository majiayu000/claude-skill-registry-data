---
name: plan-critique
allowed-tools: >-
  Read, Glob, Grep, Write, Edit, AskUserQuestion, LSP, mcp__ide__getDiagnostics, Bash(git status:*),
  Bash(git log:*), Bash(git diff:*), Bash(echo $PPID), Bash(echo $COPILOT_AGENT_SESSION_ID), Bash(kill -0:*),
  Bash(find:*), Bash(rm:*), Bash(mkdir:*)
description: >-
  Critique the user's plan from plan.md and write critique.md. Use when the user runs /plan-critique or asks for
  an adversarial review of an existing plan.
disable-model-invocation: true
model: opus
effort: high
license: MIT
---

On Codex, invoke skills with `$skill-name` (for example, `$plan-create`). Use that form when giving Codex
commands; other clients use `/skill-name`.

This skill helps the user perform an iterative review of the execution plan.
Critique the plan, code, architecture, system design, and design patterns.

## Working agreement

Read the working agreement at [working-agreement.md](../plan-create/working-agreement.md) before step 1 and follow it
for the whole run. If it cannot be found, tell the user it is missing and apply the rules listed below.

## Critique methodology

1. Be adversarial. Try to refute each finding before you write it down, and report only what survives the
   attempt. A finding you could not refute is worth more than three you did not test.
2. Grade confidence per finding. Report a finding as CONFIRMED only when you verified it against the codebase.
   Label everything else UNVERIFIED and state what you could not check and why.
3. Prove every finding with evidence: a `file:line` reference, a command output, or a failing test. Never assert
   a plausible but unverified conclusion, and never present a guess as a fact.
4. Cite `plan.md` line numbers only from the copy you read in this run. Re-read `plan.md` before writing the
   critique and check that each line reference points at the text you describe. Merging a critique into the plan
   shifts every line below the merge point, so numbers carried over from an earlier iteration are wrong.
5. Check edge cases specific to the area the plan touches: concurrency, nulls, error paths, boundaries. A generic
   "find bugs" pass over the plan is not enough.
6. Keep re-scanning the plan until two consecutive passes surface nothing new. Stop at that point, not before.
7. Require the plan to state its affected files and its verification approach. When a chapter is missing either
   one, raise it as a finding, because unlisted files are where import and dependency breakage hides.
8. Do not edit project code or `plan.md` during this phase. This phase writes `critique.md` only. The user
   decides what moves into the plan.

## Grading findings

Grade each finding from 1 to 10 across six aspects:

| Factor | 1-3 (Low) | 4-7 (Medium) | 8-10 (High) |
| --- | --- | --- | --- |
| Confidence | Weak guess; re-review required | Plausible, unverified; re-review | Verified (file:line / output) |
| Priority | Cosmetic or minor cleanup | Causes rework if deferred | Fix at start of execution |
| Complexity | Fast model, low effort | Standard model, moderate effort | Max model/effort; split task |
| Blast radius | Single file or local function | Multiple modules or callers | Cross-cutting, API, or schema |
| Ambiguity | Deterministic from codebase | Minor edge-case choice | Requires user design decision |
| Verification | Existing unit test covers it | Needs new test or mock setup | Hard to test or manual check |

Grading rules:

- Confidence 1-7: run adversarial re-review before assigning the final score and `CONFIRMED` / `UNVERIFIED` label.
- Priority 8-10: address at the beginning of the execution phase.
- Complexity 8-10: rate by model + effort needed; consider splitting into smaller sub-tasks.
- Blast radius 8-10: call out affected callers, contracts, or migrations explicitly.
- Ambiguity 8-10: flag for user input instead of assuming a resolution.
- Verification 8-10: specify concrete manual or integration checks when unit tests cannot cover it.

## Critique steps

1. Resolve `plansFolder` from config:
   Check the active agent's config file first (`.codex/plan-critique-config.json` for Codex,
   `.claude/plan-critique-config.json` for Claude Code,
   `.gemini/plan-critique-config.json` for Agy/Gemini, or `.copilot/plan-critique-config.json` for Copilot CLI),
   falling back to reading the other agent configs. If no config exists or `plansFolder` is not set or is empty:
   Respond with "No plans folder configured. Run `/plan-create` first to set up."
2. Get the active session id:
   - On Copilot CLI (or when `COPILOT_AGENT_SESSION_ID` is set): read `COPILOT_AGENT_SESSION_ID` via
     `echo $COPILOT_AGENT_SESSION_ID` (macOS/Linux) or `$env:COPILOT_AGENT_SESSION_ID` (Windows); if empty, use the
     literal value `default`. Store as `sessionId`.
   - Otherwise (Codex, Claude Code / Agy): run `echo $PPID` and store as `sessionId`.
3. Clean up stale sessions in `[plansFolder]/.sessions/` (non-blocking, never abort because of cleanup):
   - For numeric PID filenames, check `kill -0 [PID] 2>/dev/null` and delete if the process is no longer running.
   - For non-PID session files (e.g. `default` or UUIDs), delete files not modified in the last 7 days.
4. Read the current session's plan from `[plansFolder]/.sessions/[sessionId]` if it exists. Store as `sessionPlan`.
5. Scan `[plansFolder]/` for subdirectories (each subdirectory is a plan). Exclude `archived/` and `.sessions/`
   folders and any files, only list plan directories.
   If no plan folders exist: Respond with "No plans found. Create one with `/plan-create`".
6. Select the plan to critique:
   - If `sessionPlan` exists and matches a plan folder, auto-select it. Inform the user:
     "Using current session plan: [sessionPlan]"
   - Else if only one plan exists, auto-select it and inform user.
   - Otherwise, ask the user to select a plan from the list.
     Example:
     ```
     Available plans:
     1. add-user-authentication
     2. refactor-database-layer
     3. implement-caching

     Which plan would you like to critique? [1-3]
     ```
7. Update the session file `[plansFolder]/.sessions/[sessionId]` with the selected plan slug (create if needed).
8. Read the plan file at `[plansFolder]/[selected-plan]/plan.md`
9. Resolve project instructions and check for errors:
   - Check the active agent's native instructions file first (`AGENTS.md` for Codex, `GEMINI.md` for Agy,
     `.github/copilot-instructions.md` for Copilot, `CLAUDE.md` for Claude Code), falling back to `AGENTS.md` then
     `CLAUDE.md`.
   - If `plan.md` is empty: Respond with "Plan file is empty. Edit `[plansFolder]/[selected-plan]/plan.md`"
   - If no project instructions file exists in the project root:
     Respond with "Create a project instructions file (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, or
     `.github/copilot-instructions.md`) in the root of your project."
10. Detect project languages and verify LSP / language server availability:
    - Detect the main project languages with Glob: e.g. `tsconfig.json`, `*.ts`, or `*.tsx` for TypeScript,
      `composer.json` or `*.php` for PHP, `go.mod`, `pyproject.toml`, `pom.xml`, etc.
    - Probe code intelligence: pick a source file referenced by the plan (or any project source file) and request
      go-to-definition or hover on a known symbol using the `LSP` tool or active language server.
    - If the probe succeeds, code intelligence is available. Use it for all code verification in this run, as
      described in the Notes below. Do not substitute Grep for checks LSP / the language server can answer.
    - If the probe fails or no language server is available for the detected language, inform the user:
      "No LSP / language server support detected for [language]. The critique will fall back to Grep, which is
      less accurate. Enable an LSP plugin (for example `/plugins` -> `typescript-lsp` or `php-lsp`), configure
      a language server with `/lsp`, or use https://github.com/github/awesome-copilot/tree/main/skills/lsp-setup."
    - Do not block the critique. Proceed with the Grep fallback and record in the critique Summary that no
      language server / LSP was available, so the user knows symbol verification relied on Grep.
11. Read the existing "Iteration: [number]" at `[plansFolder]/[selected-plan]/critique.md` (if it exists) and
    determine the current iteration number. If no critique exists, this is iteration 1.
12. If the plan references files that are in the `[plansFolder]/[selected-plan]/` folder, review those as well and
    add them to the context of the critique.
13. Perform a thorough critique of the plan considering:
    - Clarity: Are requirements specific and unambiguous?
    - Completeness: Are all necessary steps included?
    - Order: Are dependencies between steps correctly sequenced?
    - Feasibility: Can each step be executed given the current codebase?
    - Risk: Are there potential side effects or breaking changes?
    - Standards: Does it comply with the project instructions?
    - Scope: Is scope reasonable? Any unnecessary additions?
    - Testability: How is success verified? Does each chapter name the test to write or the command to run?
    - Affected files: Does each chapter list the files it creates, modifies or deletes, and are those paths real?
    - Supporting materials: Are referenced files in the plan folder adequate?
14. Evaluate whether the plan can be split into independent tasks. If the plan contains multiple features
    or changes that can be executed separately, strongly recommend splitting it into separate plans.
    Why this matters:
    - Reduces complexity during execution
    - Limits the context window needed for each plan
    - Makes critique iterations more focused and actionable
    - Allows independent tasks to proceed without blocking each other

    Example: A plan with "Add user authentication", "Refactor database layer", and "Add caching" should
    be split into three separate plans if these can be implemented independently.

    When suggesting a split, be specific about which sections should become their own plan.
15. Write the critique to `[plansFolder]/[selected-plan]/critique.md`.
    When writing the critique, follow the original chapters from `plan.md`.
    The goal is to be able to easily override `plan.md` if the user chooses to merge `critique.md` with `plan.md`.

    Use the format in [critique-format.md](critique-format.md).

Notes:

- When critiquing, always analyze codebase structure (existing files, directories, patterns), the project
  instructions, the `README.md` file, dependencies (`package.json`, `requirements.txt`, etc.), git state if
  relevant, whether referenced files/APIs actually exist, and supporting files in the plan folder.
- When doing the writeup of the critique, in the "Description" area make use of the line numbers from `plan.md`
  and reference them so that the user can easily find what text to replace or update.
- Use code intelligence to verify the plan against the actual codebase. Always use LSP / the language server when
  step 10 confirmed it is available; use Grep only as a fallback when step 10 found no support:
  - Verify types exist: use LSP go-to-definition; fallback is Grep for `class`, `interface`, `type`, or
    `struct` definitions
  - Check method/function existence: use LSP go-to-definition; fallback is Grep for `function`/`def`/`fn`
    declarations in the target file
  - Find usages/references: use LSP find-references; fallback is Grep for the symbol name across the codebase
  - Review diagnostics: use `mcp__ide__getDiagnostics` when available, otherwise use LSP / language server
    hover/diagnostics for files referenced in the plan
  - Verify file paths exist with Glob before referencing them in the critique
- If the active agent ignores `model` frontmatter, select a high-capability model with `/model`.
- Add the found issues/observations list in the beginning of `critique.md` as a Table of contents.
- Always follow the chapters from `plan.md` as a structure for critique.
- Be direct and constructive in feedback and suggest multiple solutions when appropriate.
- Each critique iteration completely overwrites the previous `critique.md` file.
- Discard addressed issues: If an issue from the previous critique has been fixed in `plan.md`, do not include it.
- Only include current issues: The critique should reflect the current state of `plan.md`.
- New unrelated observations: If new issues appear that don't fit under existing `plan.md` chapters, add them as
  new chapters at the bottom of the critique.
- Increment iteration number: Always increment from the previous critique's iteration number.
