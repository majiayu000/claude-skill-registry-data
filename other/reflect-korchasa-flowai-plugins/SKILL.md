---
name: reflect
description: >-
  Use when the user asks to reflect on the CURRENT session or one transcript
  file they name, analyze the agent's own process, audit context use, or extract
  lessons from how a task was done. Not for multi-session history — use
  reflect-by-history.
---

# Task: Reflect on Process, Technical Decisions, Context & Knowledge Gaps

## Overview

Analyze the task execution (either current history or a provided transcript) to identify errors in the **agent's process and logic**, weaknesses in **technical decisions**, inefficiencies in **context usage**, and **useful discoveries not captured in project instructions**.
Focus on *how* the agent attempted to solve the problem, *whether the chosen technical approach was sound*, *what information it used or missed*, and *what new knowledge was gained but not persisted*.

## Context

<context>
The goal is to perform a "Root Cause Analysis" of the agent's behavior, evaluate the quality of its technical decisions, audit its information gathering, AND identify useful knowledge discovered during work that is missing from project instructions.

### Behavioral Errors
- **Logic Loops**: Repeating the same failing action.
- **False Assumptions**: Assuming a state without verifying.
- **Ignoring Feedback**: Ignoring tool error messages.
- **Process Violations**: Skipping required steps (like reading docs or verifying).
- **Hallucinations**: Inventing facts or file contents.

### Technical Decision Errors
- **Overcomplexity**: Solution more complex than necessary (extra abstractions, unnecessary indirection, premature generalization).
- **Wrong Abstraction Level**: Solving at the wrong layer (e.g., app-level fix for an infra problem, or vice versa).
- **Ignoring Existing Patterns**: Not following established project conventions, reinventing what already exists in the codebase.
- **Poor Error Handling**: Missing error paths, swallowing exceptions, unclear failure modes.
- **Fragile Design**: Solution tightly coupled, hard to test, or brittle to future changes.
- **Performance Anti-patterns**: O(n^2) where O(n) is trivial, unnecessary I/O, missing caching for repeated operations.
- **Security Gaps**: Unsanitized input, hardcoded secrets, excessive permissions.
- **Wrong Tool/Library Choice**: Using a dependency where stdlib suffices, or picking a deprecated/unmaintained library.
- **Unrequested Fallbacks**: Adding fallback/default behavior the user never asked for (e.g., silent retries, default values masking errors, graceful degradation where fail-fast was expected).

### Context Inefficiencies
- **Missing Context**: Information the agent needed but never obtained.
- **Redundant Context**: Information the agent loaded but never used.

### Automation Opportunities
Repeating manual actions that could be codified:
- **Manual Multi-Step Workflows**: Sequence of actions performed manually that recurs across tasks (candidate for a skill or command).
- **Ad-hoc Decisions**: Choices made without a documented rule, leading to inconsistency (candidate for a rule).
- **Unchecked Invariants**: Conditions verified manually that a hook or CI step could enforce automatically (candidate for a hook).

### Target Artifact Taxonomy
When proposing a fix, classify *where* it belongs:
- **Project Docs** (AGENTS.md, README, SRS, SDS) — persistent project-wide context, conventions, stack info.
- **Rule** (glob-triggered IDE rule) — formatting, style, or behavioral constraint scoped to specific files.
- **Skill** (multi-step workflow) — repeatable procedure the agent can follow.
- **Command** (one-shot action) — single-purpose shortcut wrapping multiple steps.
- **Hook** (automated check) — deterministic validation triggered by file save or pre-commit.
- **Code Comment** — inline explanation of non-obvious logic in source code.

### Undocumented Discoveries
**Universally useful** knowledge gained during task execution that exists only in the conversation and is not persisted in project docs/rules/instructions. Only facts relevant to most future tasks qualify — discard one-off or task-specific details:
- **Implicit Conventions**: Patterns, naming rules, or constraints discovered empirically (e.g., "API returns 429 after 10 req/s", "field X must be set before Y").
- **Environment Quirks**: Non-obvious tooling behavior, version-specific bugs, platform differences found by trial and error.
- **Architectural Insights**: Discovered dependencies, data flows, or coupling between components not documented anywhere.
- **Workarounds & Gotchas**: Solutions to problems that required non-obvious steps (e.g., "must restart service after config change", "header X is required but undocumented").
- **Domain Knowledge**: Business rules, edge cases, or valid/invalid states clarified during the session.
</context>

## Rules & Constraints

<rules>
1. **Evidence-Based**: Base all observations on the actual conversation history, tool outputs, AND session history (if available).
2. **Specific References**: When suggesting improvements, cite the specific file (e.g., a rules or commands file in the project's IDE configuration directory) or the command name.
3. **Constructive**: Focus on actionable improvements (additions, clarifications, removals).
4. **Do not make changes to the agent's instructions or rules**. Only suggest improvements.
5. **Mandatory**: The agent MUST use a task management tool (e.g., `todo_write`, `todowrite`, `Task`) to track the execution steps.
6. **Pattern Validation**: Before proposing a fix for an issue found in the current session, check session history to determine whether it is a **recurring pattern** or an **isolated incident**. Prioritize systemic fixes for recurring patterns over one-off corrections. This ranks NEW rules; a wrong fact in an existing instruction file is corrected even when it bit once (see step 13, Proportionality).
7. **Rescue is read-only (FR-DOC-RESCUE)**: when surfacing a decision passage for task capture (step 2b), reflect MUST recommend `/flowai:plan` and MUST NOT write under the `tasks` role resolved from AGENTS.md, MUST NOT draft or offer to write the task file itself. Clean separation: detection lives here, recording lives in `plan`.
</rules>

## Instructions

<step_by_step>
1. **Initialize**
   - Use a task management tool (e.g., `todo_write`, `todowrite`) to create a plan for the reflection process.

2. **Identify Source**
   - If the user points to a transcript file, read it using available file reading tools.
   - Otherwise, review the current conversation history.

2b. **Surface Decisions for Task Capture (FR-DOC-RESCUE)** — execute IMMEDIATELY after step 2, BEFORE the main reflection analysis. This is a STANDALONE output, separated from the rest of the report.
   - Scan the source for **decision passages**: ≥2 weighed alternatives + explicit reasoning ("picked X over Y because …", "rejected Z due to …"). Headings like `## Decision` / `## Solution` with bulleted alternatives are strong signals.
   - If any decisions are found, emit ONE chat block immediately (not buffered into the final report), titled `### Decisions for Task Capture`. For each decision use this template (literal text + substituted fields):
     - `**Decision detected:** <≤8-word title>`
     - `**Recommended action:** invoke \`/flowai:plan <title>\` — that skill writes the task file as a persistent canonical record of the decision.`
     - `**Alternatives weighed:** <bullet list, 1 line each>`
     - `**Chosen:** <chosen alternative + 1-sentence rationale>`
   - The literal token `/flowai:plan` MUST appear on the Recommended action line — that is the user's invocation signal. After emitting, this finding is DONE; do not revisit it later in steps 12 or 14.
   - FORBIDDEN: writing under the resolved `tasks` role; drafting the full task body in chat as if preparing to save it; offering "shall I create the task?" / "Хотите, чтобы я создал…?" / equivalent; listing "create task file" under step 12's Corrective Actions. Reflect detects + recommends; `/flowai:plan` writes — clean separation.
   - If no decision passages exist in the source, skip silently — do NOT fabricate one. Continue to step 3.

3. **Load Session History**
   - Look for session history files (e.g., `session-history/` directory, previous transcripts, or logs).
   - If session history exists, read all available session transcripts.
   - Build a summary of recurring issues: for each error type, note how many sessions it appeared in, the pattern signature, and whether the root cause was the same.
   - This data will be used in later steps to distinguish recurring patterns from isolated incidents.

4. **Analyze Execution Flow**
   - Map out the agent's "Thought -> Action -> Result" loop.
   - Identify where the chain broke:
     - Did the Thought match the Goal?
     - Did the Action match the Thought?
     - Did the Agent interpret the Result correctly?

5. **Detect Logic Patterns**
   - **Looping**: Is the agent retrying without changing strategy?
   - **Blindness**: Is the agent ignoring "File not found" or linter errors?
   - **Stubbornness**: Is the agent forcing a solution that doesn't fit?

6. **Evaluate Technical Decisions**
   Review the actual code/changes produced by the agent:
   - **Complexity Check**: Is the solution proportional to the problem? Could it be simpler?
   - **Pattern Conformance**: Does it follow existing project patterns (naming, structure, error handling)? Or does it introduce inconsistencies?
   - **Abstraction Fit**: Is the problem solved at the right layer? Is there unnecessary indirection or missing encapsulation?
   - **Error Handling**: Are failure modes explicit and handled? Are errors swallowed or masked?
   - **Robustness**: Is the solution fragile to edge cases, concurrency, or future changes?
   - **Performance**: Are there obvious inefficiencies (quadratic loops, redundant I/O, missing caching)?
   - **Security**: Is input validated? Are secrets/permissions handled correctly?
   - **Dependency Choice**: Are dependencies justified? Could stdlib or existing project code suffice?
   - **Unrequested Fallbacks**: Did the agent add fallback/default behavior not asked for (silent retries, default values masking errors, graceful degradation where fail-fast was expected)?

7. **Analyze Context: Missing Information**
   Identify what the agent *should have* read/checked but didn't:
   - **Unread docs**: Project docs (README, AGENTS.md, design docs) relevant to the task but never opened.
   - **Unread source**: Related source files (imports, callers, interfaces) that would have prevented errors.
   - **Unused skills/rules**: Available skills or rules that were relevant but not consulted.
   - **Skipped verification**: Test results, linter output, or runtime checks that would have caught issues earlier.
   - **Unasked questions**: Ambiguities the agent resolved by guessing instead of asking the user.
   - **Stale instructions**: Anything the project instructions told the agent that the repository contradicted — a command or task that does not exist, a path that moved, a convention the code does not follow. Compare the commands the instructions name with the ones the project's manifest defines.

8. **Analyze Context: Redundant Information**
   Identify what the agent loaded but *didn't need*:
   - **Read-but-unused files**: Files opened via file reading tools but never referenced in the solution.
   - **Over-reading**: Large files read entirely when only a small fragment (function, config key) was needed.
   - **Repeated reads**: The same unchanged file read multiple times, wasting context window.
   - **Irrelevant tool output**: Command outputs (e.g., verbose logs, full `git diff`) that added noise without value.
   - **Off-task files**: Files from unrelated domains or previous tasks still in context.

9. **Extract Undocumented Discoveries**
   Scan the session for useful knowledge that was learned but not persisted:
   - Review tool outputs, error messages, and user clarifications for **facts not present in any project file**.
   - For each discovery, check whether it is already documented in project docs (AGENTS.md, README, SRS, SDS, rules, code comments).
   - A discovery qualifies if ALL three conditions are met:
     (a) it was essential to solving the task or avoiding an error,
     (b) a future agent starting a new session would not have access to it,
     (c) it is **universally useful** — applicable to most future tasks in this project, not just the current one.
   - **Discard** task-specific, one-off, or narrow facts that won't help in other contexts (e.g., "file X had a typo on line 42", "user prefers blue buttons").
   - **Keep** knowledge that affects how the project is built, run, tested, or deployed in general (e.g., "API requires header X for all endpoints", "tests must run sequentially due to shared DB state", "config changes require service restart").

10. **Identify Automation Opportunities**
   Scan the session for repeating manual work that could be codified:
   - **Repeated workflows**: Was a multi-step sequence performed manually that is likely to recur? → suggest a skill or command.
   - **Ad-hoc decisions**: Were formatting, naming, or structural choices made without a documented rule? → suggest a rule.
   - **Manual checks**: Were invariants verified by the agent manually (e.g., "check that file has frontmatter") that a hook could enforce? → suggest a hook.
   - Only include items that would save effort across multiple future tasks.

11. **Cross-Session Pattern Analysis**
   If session history was loaded in step 3:
   - For each issue found in steps 4-10, check if a **similar issue** appeared in previous sessions.
   - Classify each issue as:
     - **Recurring** (appeared in 2+ sessions with similar root cause) — requires a systemic fix (rule, hook, skill, or architectural change).
     - **Isolated** (appeared only in the current session) — may be a one-off; propose a targeted fix but note the lower priority.
   - For recurring patterns, include: frequency (N sessions out of M total), pattern signature, and why it keeps happening.
   - Recurring patterns MUST be prioritized above isolated issues in the report.

12. **Formulate Report**
   - **Process Summary**: What went wrong in the *process*?
   - **Technical Summary**: What was wrong with the *technical approach*?
   - **Root Cause**: Why did the agent make this mistake? (e.g., "Assumed file existed", "Didn't check existing patterns").
   - **Cross-Session Patterns**: Which issues are recurring across sessions? Include frequency and evidence from multiple sessions.
   - **Context Gaps**: What missing information led to errors or wasted effort?
   - **Context Waste**: What unnecessary information consumed context budget?
   - **Undocumented Discoveries**: What useful knowledge was gained but not captured in project files?
   - **Automation Opportunities**: What manual work could be codified as a skill, rule, or hook?
   - **Corrective Actions**: Numbered list. Each item is a **self-contained narrative** — a reader must understand the full problem, its cause, and the proposed solution without reading any other document or transcript.

   **Sections per item** (all required):
   - **What happened**: Full story with quoted tool calls/errors. A reader who never saw the transcript must get the complete picture.
   - **Impact**: Measurable cost — tokens/lines wasted, time lost, errors/regressions introduced, downstream effects. Every action gets a number, including a process failure: "1 production edit, 0 tests run, 0 verification commands, 1 correctness claim without evidence" is measurable; "possible correctness risk" is not.
   - **Root cause**: Why the agent made this mistake. What knowledge/rule/context was missing.
   - **Proposed fix**: (a) **Where** — exact file path + section. (b) **Draft content** — the literal text to paste and nothing else: the rule sentence, the code comment, the hook body. A sentence ABOUT the change is not draft content — "consider adding a pre-commit hook" names an intention, the hook's own config is the artefact. If you cannot write the artefact, the fix is not ready — and a finding without a ready fix is NOT a corrective action: move it to **Process Summary** or **Technical Summary** and drop it from this list. Never keep it here with a verdict in the fix slot ("No new rule is warranted", "the existing rule already covers this"): every item in this list carries all five sections, or it is not in this list. Same when the rule already exists and the agent broke it anyway — then the item is a rule that did not fire, and its Where + Draft is the sentence that makes it bind (a precondition, a gate, a checklist line), not a restatement. Observed 2026-09-06 (`reflect-context`): action 2 read "No new rule is warranted" as its fix and gave no measurable Impact; the interviewed agent named this sentence as the one that left room. (c) **Why this works** — how it addresses the root cause.
   - **Recurrence risk**: HIGH/MEDIUM/LOW + specific trigger scenarios + frequency.

   **Quality bar**: Remove the title — a reader should still understand what happened, why it matters, and what to do. If any section would make a reader ask "what does this mean?" — expand it.

   **Anti-patterns**: one-line sections (`Impact: 500 lines wasted` — wasted how?); bare step references (`What happened: steps 5-7`); actionless fixes (`Fix: check similar code` — what artifact enforces this?); vague locations (`Where: AGENTS.md` — which section?); drafts that describe the change instead of being it (`Draft: consider adding a hook that runs the suite`, `the existing rule should be more prominent`). The bar is per finding, not per report: one finding carrying a suggestion in its draft slot spoils the section, however complete the other four are.

   **Example:**

   1. **[Discovery] Adding a field to SettingsSnapshot requires synchronized updates across ~10 files**

      **What happened**: Agent added `allowedHosts` field to `BotVersionSettingsSnapshot` interface in `types/mod.ts`. `deno check` passed (structural typing). But `deno test --no-run` (step 34) revealed 7 type errors: `parseSettingsJson()` in `parser.ts` lacked a default, `flattenBot()` in `script.js` omitted the field, reducers `APPLY_BOT_UPDATE` and `SET_CURRENT_BOT_FIELDS` in `store.ts` didn't handle it, `handleCreateBot()` + `handleUpdateBot()` in `frontend_handler.ts` missed it. Agent then spent ~20 min chasing errors one-by-one through the dependency graph.

      **Impact**: 20+ min on cascading fixes. 7 type errors discovered late, each requiring a separate read-edit-check cycle. The coupling is invisible — nothing documents which files must be updated together.

      **Root cause**: `SettingsSnapshot` is consumed by ~10 functions across 7 files, but no checklist or code comment lists these dependencies. Every developer rediscovers the graph from scratch.

      **Proposed fix**:
      - **Where**: `types/mod.ts`, JSDoc on `BotVersionSettingsSnapshot` (line ~25).
      - **Draft content**: `/** When adding a field: update (1) parseSettingsJson() in parser.ts — backward-compat default, (2) flattenBot() in script.js, (3) saveCurrentBot() in script.js, (4) APPLY_BOT_UPDATE in store.ts, (5) SET_CURRENT_BOT_FIELDS in store.ts, (6) applyUpdate() in chat_handler.ts, (7) handleCreateBot()+handleUpdateBot() in frontend_handler.ts, (8) all test files constructing SettingsSnapshot. Run deno test --no-run after. */`
      - **Why this works**: Checklist at the interface definition — agents/developers see it before making changes, eliminating trial-and-error discovery.

      **Recurrence risk**: HIGH — triggers on every new settings field (next: FR-29 `state`). ~20 min saved per occurrence.

13. **Self-Criticism**
   Before presenting the report, critically examine your own analysis:
   - **Validity**: Re-examine each finding — is it backed by concrete evidence from the transcript/history, or is it speculative? Remove or downgrade findings that rely on assumptions rather than observed behavior.
   - **False Positives**: Are any flagged issues actually acceptable or intentional? (e.g., reading a related file to understand patterns is not "redundant context"; updating a test after changing behavior is not always "modifying tests instead of code").
   - **Proportionality**: Is each proposed fix proportional to the problem severity? A minor one-off issue does not warrant a new rule or hook — flag disproportionate recommendations and simplify them. This limits NEW rules only. A line in an existing instruction file that the session proved wrong is corrected on its first sighting, however rarely it bites: fixing a fact is not adding a rule.
   - **Blind Spots**: What categories of problems might you have missed entirely? Consider whether you focused too narrowly on one error type and overlooked others (e.g., security, performance, missing docs).
   - **Severity Calibration**: Are severity labels (HIGH/MEDIUM/LOW, recurring/isolated) accurate? Re-check the evidence — a pattern that appeared in 2 sessions with different root causes is not truly recurring.
   - **Revise**: Based on the above, update the report — remove weak findings, strengthen valid ones, adjust severity, add any newly discovered issues from blind-spot analysis. Explicitly note what changed and why.

14. **Report Findings**
   - Present the revised report from steps 12–13.
   - Clearly mark which findings were adjusted during self-criticism and why.
   - List the proposed actionable items.
   - Ask the user if they want to apply these changes immediately.
   - **Exception**: Decision rescue items emitted in step 2b are already done — they are STANDALONE recommendations for the user to run `/flowai:plan` separately. Do not re-list them here; do not offer to write the task file yourself.

</step_by_step>
