---
name: explain
description: 'Explains how existing code works in a diagram-rich report on design and weak spots, read-only. Use when the user says "walk me through", "diagram this" or "explain this module". Not for a short sourced answer to a question (use ask).'
argument-hint: '[scope:branch|global|working] [output:<path>] <scope or question — e.g. "src/auth/", "how does the payment flow work", "explain the WebSocket reconnection logic">'
allowed-tools: Agent, Bash(git rev-parse *), Bash(git symbolic-ref *), Bash(git merge-base *), Bash(git diff *), Bash(git ls-files *), Bash(mkdir *), Bash(date *), Read, Write, Glob, Grep, TaskCreate, TaskUpdate, TaskGet, TaskList, TaskStop, AskUserQuestion, WebFetch, WebSearch
---

# Code Explanation Pipeline

## Overview

You orchestrate a deep-dive code analysis that produces a comprehensive, diagram-rich report explaining how a section of code works, why it's designed that way, and what potential issues exist. This is a read-only pipeline — it never modifies source code.

## When to Use

Understanding existing code through a read-only, diagram-rich report on how it works, why it is designed that way, and where it may break.

### When NOT to use

- The user wants a short sourced answer to a question, not a full report — use `ask`.
- The user wants code modified, debugged, or fixed — use `debug` or `build` instead.
- The user wants a hypothesis verified — use `debug certainty:low` instead.
- The user asks a one-line clarifying question answerable without opening files.

## Input

- `$ARGUMENTS` — The scope and optional question. Any combination of:
  - **Path/glob**: `"src/auth/"`, `"src/**/*.py"` — which files to explain
  - **Free-text question**: `"how does the payment flow work"`, `"explain the WebSocket reconnection logic"` — what to focus on
  - **Combined**: `"src/auth/ how does token refresh work"` — narrows both scope and focus

If empty or ambiguous, ask the user via AskUserQuestion. Never guess.

## Scope Parameter

See `<PLUGIN_ROOT>/shared/scope-parameter.md` for the canonical scope modes (`branch`, `global`, `working`) and their git commands. Document any skill-specific overrides or restrictions below this line.

- **Default** (no `scope:`): use path/glob/free-text detection from the argument.
- `global` mode in this skill **requires a focusing question** — if no question tokens are present, ask the user what aspect to explain.
- The `scope:` parameter controls **which files** to analyze. The remaining argument text controls **what to focus on** within those files. They are orthogonal. Example: `scope:branch "how does error handling work"` analyzes only branch-changed files, focused on error handling.

## Output Parameter

Extract `output:<path>` from `$ARGUMENTS` if present. This is where the final report will be written.

**Default** (no `output:` parameter): `<PROJECT_ROOT>/.mz/reports/<YYYY_MM_DD>_explain_<scope_name>.md` (append `_v2`, `_v3` if exists).

Example: `2026_04_20_explain_src_auth_token_refresh.md`

## Constants

- **PROJECT_ROOT**: resolved once in setup with `echo "${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"`; expand `<PROJECT_ROOT>` to it in every command and agent prompt.
- **MAX_RESEARCHERS**: 3 — hard cap on parallel researcher agents
- **LARGE_SCOPE_THRESHOLD**: 10 — file count above which structure and flow analysis split into separate researchers
- **TASK_DIR**: `<PROJECT_ROOT>/.mz/task/` — working artifacts under `<PROJECT_ROOT>/.mz/task/<task_name>/`
- **PLUGIN_ROOT**: `${CLAUDE_PLUGIN_ROOT}`. Skill and phase files write `<PLUGIN_ROOT>/...` because files opened with Read get no variable substitution; expand it to this absolute path before reading a file, running a command, or passing a path to an agent.

## Core Process

### Phase Overview

| #   | Phase             | Reference            | Loop? |
| --- | ----------------- | -------------------- | ----- |
| 0   | Setup             | inline below         | —     |
| 1   | Scope Resolution  | inline below         | —     |
| 2   | Research Dispatch | `phases/research.md` | —     |
| 3   | Report Generation | `phases/report.md`   | —     |

## Red Flags

- You explained without reading the target code end-to-end.
- You output walls of text instead of a diagram for visual concepts.
- Explanation assumed knowledge the user does not have per user memory.

## Verification

Before completing, output a visible block showing: resolved scope file count, researchers dispatched, and the absolute path of the written report. Confirm the report file exists on disk and contains the required mermaid diagrams.

## References

- `${CLAUDE_SKILL_DIR}/references/mermaid-syntax-by-type.md`: syntax skeleton, key tokens and a minimal example for each Mermaid diagram type (flowchart, sequenceDiagram, classDiagram, stateDiagram-v2, erDiagram, mindmap, gitGraph, timeline, C4). Grep it for the diagram type you are writing in Phase 3.

## Phase 0: Setup

### 0.1 Resolve PROJECT_ROOT

Resolve `PROJECT_ROOT` with the command in Constants, before any `cd` or worktree switch, and use it for every `.mz/` path below.

### 0.2 Parse argument

Split `$ARGUMENTS` (after removing `scope:`, `output:` parameters) into:

- **Path-like tokens**: globs, directories, file paths (contains `/`, matches on disk, or has glob characters)
- **Question tokens**: everything else — the user's question or focus area

### 0.3 Derive task name

Task name format: `<YYYY_MM_DD>_explain_<slug>` where `<YYYY_MM_DD>` is today's date (underscores) and slug is a snake_case summary (max 20 chars); on same-day collision append `_v2`, `_v3`. Examples: `2026_04_20_explain_src_auth`, `2026_04_20_explain_payment_flow`.

### 0.4 Create task directory and state

Run `mkdir -p "<PROJECT_ROOT>/.mz/task/<task_name>/"`. Write `state.md` with fields, in order: `schema_version: 2` (first line), Status, Phase, Started, `phase_complete: false`, `what_remains: []`, Researchers dispatched, and Output path.

### 0.5 Create task tracking

Use TaskCreate for each pipeline phase.

## Phase 1: Scope Resolution

Resolve the argument into a concrete file list:

- **`scope:` parameter given**: use the git-derived file list, applying standard exclusions
- **Path-like tokens**: expand by listing the matching files or walking the directory
- **Free-text only (no paths, no `scope:`)**: spawn a `pipeline-researcher` agent (model: **sonnet**) to identify which files match the description. If low confidence or multiple plausible interpretations, ask the user via AskUserQuestion.

**Exclusions**: `.gitignore`, vendored deps, generated/lock files, files > 5000 LOC. Test files are not excluded — they're valuable context.

**If the file list is empty**: report and exit. **If `scope:global` with no focusing question**: ask the user what aspect to explain.

Write `<PROJECT_ROOT>/.mz/task/<task_name>/scope.md` with Mode, file count, Question/focus, and the file list (collapsed by directory if > 30 files). Update state phase to `scope_resolved`.

## Phase 2: Research Dispatch

Dispatch 1-3 `pipeline-researcher` agents based on scope size and external dependency detection. **See `phases/research.md`** for the dispatch decision matrix, researcher prompts, and per-researcher artifact format. Update state phase to `researched`.

## Phase 3: Report Generation

Compile all researcher outputs into a single report with mandatory mermaid diagrams. **See `phases/report.md`** for the report template, diagram requirements, and quality checks. Write the report to the resolved output path. Set `Status: complete`, `phase_complete: true`, `what_remains: []`. Present a summary to the user with the report path.

## Error Handling

- **Ambiguous scope / low confidence scope resolution**: ask the user to clarify. Never guess.
- **Empty file list**: report and exit cleanly.
- **`scope:global` without question**: ask for a focusing question.
- **Researcher fails**: log it, continue with remaining researchers, note the gap in the report.
- **Domain research returns nothing useful / diagram can't be constructed**: note it in the report rather than guessing.

## State Management

After each phase, update `<PROJECT_ROOT>/.mz/task/<task_name>/state.md` with current phase, researchers dispatched/completed, output path, and any issues encountered.

State persists to `.mz/task/<task_name>/state.md` under the project root, `${MZ_MEMORY_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}`, resolved once at the start of the run. Schema is **v2**: line 1 is `schema_version: 2`; line 2 is `Status:` with one of `pending`, `running`, `blocked`, `complete`, `aborted_by_user` or `failed`, lowercase and unquoted; then `Phase`, `Started`, `phase_complete` (boolean) and `what_remains` (YAML list of strings), with skill-specific keys below them. Milestones go in `Phase`; the reason for `blocked` or `failed` goes in `what_remains`. Set `phase_complete: false` on phase entry and `true` once the phase's artifacts are written and its gates pass. Refresh `what_remains` on every phase transition; it is `[]` when `Status` is `complete`. Write the file after every phase and before every gate, and re-read it after compaction. Record decisions worth recalling under a heading that reads exactly `## Decisions`, placed before `## Notes`; mz-memory harvests them only once `Status` is `complete`. Under a heading that reads exactly `## Lessons`, add one line whenever a review finding is accepted and fixed, a step fails, gate feedback corrects a mistake, or an approved approach is reversed, in the form `- (review|failure|correction|change) WHEN <situation> → <what to do> — WHY <cause>`, concrete and under about 40 words; mz-memory harvests lessons whatever the `Status`. Treat a legacy `completed` as `complete`. On reading a `schema_version: 1` or unversioned file, put `schema_version: 2` on line 1 and `Status` on line 2, add the missing keys, and log the upgrade. Leave a file with a higher `schema_version` untouched: ask whether to Restart (archive it), start New (`_v2`) or Abort, and stop if nobody can answer.
