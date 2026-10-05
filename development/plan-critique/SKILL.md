---
name: plan-critique
allowed-tools: >-
  Read, Glob, Grep, Write, Edit, AskUserQuestion, LSP, mcp__ide__getDiagnostics, Bash(git status:*),
  Bash(git log:*), Bash(git diff:*), Bash(echo $PPID), Bash(kill -0:*), Bash(rm:*), Bash(mkdir:*)
description: Critique the user's plan from plan.md
disable-model-invocation: true
model: opus
effort: high
---

You are performing an iterative review of the user's execution plan.
Critique the plan, code, architecture, system design, and design patterns.

Fixed rules:

Read the working agreement at [working-agreement.md](../../../working-agreement.md) before step 1 and follow it for
the whole run. If that path does not resolve, look for `working-agreement.md` in the project root, then in
`.gemini/`. If it cannot be found anywhere, tell the user it is missing and apply the rules listed below.

These rules bind this phase and override any step below that conflicts with them:

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
9. Be brief. No filler, no preamble, no emojis, no em dashes, no bold or italic text.

To do this, follow these steps precisely:

1. Read `.gemini/plan-critique-config.json`, get `plansFolder` path from settings.
   If that file does not exist, read `.claude/plan-critique-config.json` instead.
   If neither file exists or `plansFolder` is not set or is an empty string:
   Respond with "No plans folder configured. Run `/plan-create` first to set up."
2. Get the session process ID by running: `echo $PPID`. Store this as `sessionPID`.
3. Clean up stale sessions: Scan `[plansFolder]/.sessions/` for files. For each file named with a PID, check if that
   process is still running via `kill -0 [PID] 2>/dev/null`. If the command fails (process not running), delete that
   session file. This is non-blocking cleanup.
4. Read the current session's plan from `[plansFolder]/.sessions/[sessionPID]` if it exists. Store as `sessionPlan`.
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
7. Update the session file `[plansFolder]/.sessions/[sessionPID]` with the selected plan slug (create if needed).
8. Read the plan file at `[plansFolder]/[selected-plan]/plan.md`
9. Check for errors:
   - If `plan.md` is empty: Respond with "Plan file is empty. Edit `[plansFolder]/[selected-plan]/plan.md`"
   - If none of `GEMINI.md`, `AGENTS.md`, or `CLAUDE.md` exist in project root:
     Respond with "Create a `GEMINI.md`, `AGENTS.md`, or `CLAUDE.md` file in the root of your project."
10. Detect project languages and verify LSP availability. LSP is the required tool for code verification in
    this phase, so this check is mandatory:
    - Detect the main project languages with Glob: `tsconfig.json`, `*.ts`, or `*.tsx` for TypeScript,
      `composer.json` or `*.php` for PHP, and the equivalent markers for any other language the plan touches.
    - Probe LSP: pick a source file referenced by the plan (or any project source file) and request
      go-to-definition or hover on a known symbol using the LSP tool.
    - If the probe succeeds, LSP is available. Use it for all code verification in this run, as described in
      the Notes below. Do not substitute Grep for checks LSP can answer.
    - If the probe fails or the LSP tool is not available for the detected language, inform the user before
      continuing:
      "No LSP support detected for [language]. The critique will fall back to Grep, which is less accurate.
      To enable code intelligence, install the LSP plugin for your language (for example `typescript-lsp` or
      `php-lsp` from claude-plugins-official, check with the `/plugins` command), or use an LSP setup skill
      such as https://github.com/github/awesome-copilot/tree/main/skills/lsp-setup to install and configure a
      language server."
    - Do not block the critique. Proceed with the Grep fallback and record in the critique Summary that LSP
      was unavailable, so the user knows symbol verification relied on Grep.
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
    - Standards: Does it comply with `CLAUDE.md` project standards?
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
    The goal is to be able to easily override the `plan.md` if the user chooses to merge `critique.md` with `plan.md`

    Use the format in [critique-format.md](critique-format.md).

Notes:

- When critiquing, always analyze codebase structure (existing files, directories, patterns), project standards
  from `CLAUDE.md`, the `README.md` file, dependencies (`package.json`, `requirements.txt`, etc.), git state if
  relevant, whether referenced files/APIs actually exist, and supporting files in the plan folder.
- When doing the writeup of the critique, in the "Description" area make use of the line numbers from `plan.md`
  and reference them so that the user can easily find what text to replace or update.
- Use code intelligence to verify the plan against the actual codebase. Always use LSP when step 10 confirmed
  it is available; use Grep only as a fallback when step 10 found no LSP support:
  - Verify types exist: use LSP go-to-definition; fallback is Grep for `class`, `interface`, `type`, or
    `struct` definitions
  - Check method/function existence: use LSP go-to-definition; fallback is Grep for `function`/`def`/`fn`
    declarations in the target file
  - Find usages/references: use LSP find-references; fallback is Grep for the symbol name across the codebase
  - Review diagnostics: use `mcp__ide__getDiagnostics` to pull current errors/warnings from the IDE for files
    referenced in the plan
  - Verify file paths exist with Glob before referencing them in the critique
- Add the found issues/observations list in the beginning of the critique.md file as a Table of contents
- Always follow the chapters from plan.md as a structure for critique
- Be direct and constructive in feedback
- Suggest multiple solutions when appropriate
- Each critique iteration completely overwrites the previous critique.md file.
- Discard addressed issues: If an issue from the previous critique has been fixed in plan.md, do not include it.
- Only include current issues: The critique should reflect the current state of plan.md.
- New unrelated observations: If new issues appear that don't fit under existing `plan.md` chapters, add them as
  new chapters at the bottom of the critique
- Increment iteration number: Always increment from the previous critique's iteration number
