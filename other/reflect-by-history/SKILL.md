---
name: reflect-by-history
description: >-
  Use when the user asks to review PAST sessions, find recurring patterns across
  sessions, or improve project primitives (rules, skills, hooks, docs) from
  historical IDE transcripts. Do NOT trigger on current-session self-review —
  use reflect instead.
---

# Task: Reflect on Previous Session History

Analyze **previous** IDE session transcripts (not the current session) to identify recurring behavioral patterns, systemic issues, and propose improvements to project primitives (rules, skills, hooks, project docs).

Unlike `reflect` (which analyzes the current session), this skill works with historical data across multiple past sessions to find cross-session patterns.

## Session History Locations

Session history for all three IDEs is stored **only at user level** (home directory). None of them create project-local session stores — do not look for `.claude/projects/`, `.cursor/projects/`, or `.opencode/` inside the project root; those paths do not exist.

### Claude Code

JSONL files at user level:

- **Sessions**: `~/.claude/projects/{project-path-with-dashes}/*.jsonl` — each file is one session. The dir name is the absolute project path with `/` replaced by `-` (e.g. `/Users/alice/www/foo` → `-Users-alice-www-foo`).
- **Global index**: `~/.claude/history.jsonl` (one line per prompt: text, timestamp, project path, session ID).

JSONL format — each line is a JSON object with `type` field:
- `type: "user"` — user messages (`message.content` has the text)
- `type: "assistant"` — agent responses (may contain `tool_use` in `message.content[]`)
- `type: "progress"` — hook/tool progress events
- `type: "ai-title"` — session title (`aiTitle` field)
- `type: "queue-operation"` — internal queue events (skip)
- `type: "file-history-snapshot"` — file backup metadata (skip)

### Cursor

- **SQLite (primary)**: `~/Library/Application Support/Cursor/User/workspaceStorage/<hash>/state.vscdb` (macOS). The `<hash>` dir corresponds to one workspace; the chat/agent history is inside the `ItemTable` rows keyed by `workbench.panel.aichat.view.aichat.chatdata` (and similar).

### OpenCode

- **SQLite**: `~/.local/share/opencode/opencode.db`
- **Session artifacts**: `~/.local/share/opencode/storage/`, `~/.local/share/opencode/tool-output/`

## Discovery Strategy

0. **Explicit path override**: If the user's request names a concrete directory or file path for session history (e.g., "analyze sessions in `./foo/bar/`", "look at `<path>`", "use the history at `<dir>`"), use **that path verbatim** and skip IDE detection. An explicit user-supplied path wins over every default location — do not fall back to `~/.claude/projects/` "just in case". Report which path you used.
1. Determine current IDE by checking project markers (`.claude/`, `.cursor/`, `.opencode/`) and/or environment (`CLAUDECODE=1`).
2. Compute the per-IDE session path from the project's absolute path (Claude Code: replace `/` with `-`; Cursor: look up the workspaceStorage hash).
3. List session files under that user-level path and sort by mtime (newest first).
4. **Filter out current session**: exclude the JSONL file for the currently running session (it is still being written and is not "previous" history). If only the current session is found, report "No previous session history found" and stop.
5. **No history**: if no session files are found at all, clearly report "No session history found" and tell the user the exact path checked. Do not fabricate or hallucinate analysis results.

## Scope Determination

Pick **exactly one** scope bucket from the table below based on the user's request. Use the listed exact session count — do **not** inflate the scope because "the volume is small" or because more sessions "are available". If the history has fewer files than the target, take all of them; never exceed the target.

| User Request phrasing | Scope | Exact session count |
|---|---|---|
| "Find recurring issues" / "patterns" / "deep analysis" | Deep | **Last 20** (or all if fewer) |
| "recently" / "last few" / "what went wrong" | Recent | **Last 5** |
| "last session" / "previous session" / "review latest" | Single | **Last 1** |
| "How has X improved?" / "trend of X" | Trend | All sessions mentioning X |
| Unspecified — no phrasing cue | Default | **Last 10** |

State the chosen bucket, the exact count, and the user phrasing that triggered it. Example: *"Scope: Recent — last 5 sessions (user said 'last few')"*.

## Analysis Focus

For each session, extract:

1. **Task summary** — what was requested (from `ai-title` and first user message)
2. **Tool usage** — which tools were called, how many times, in what order
3. **Errors & retries** — failed tool calls, repeated attempts, error messages
4. **Primitive usage** — which skills/commands were invoked, which rules were triggered
5. **Time patterns** — session duration (calculated from first/last message timestamps), idle gaps, bursts of activity

### Cross-Session Pattern Detection

Compare across sessions to find:

- **Recurring errors** — same error type or message appearing in 2+ sessions
- **Repeated manual workflows** — same sequence of actions performed manually across sessions (candidate for a skill or command)
- **Ad-hoc decisions** — choices made inconsistently without a rule (candidate for a rule)
- **Unchecked invariants** — conditions verified manually that could be automated (candidate for a hook)
- **Underused primitives** — available skills/commands that could have been used but weren't
- **Missing knowledge** — information discovered in sessions but not captured in project docs

## Target Artifact Taxonomy

When proposing a fix, classify *where* it belongs:

- **Rule** (glob-triggered IDE rule) — formatting, style, or behavioral constraint scoped to specific files
- **Skill** (multi-step workflow) — repeatable procedure the agent can follow
- **Command** (one-shot action) — single-purpose shortcut wrapping multiple steps
- **Hook** (automated check) — deterministic validation triggered by file save or pre-commit
- **Project Docs** (AGENTS.md, CLAUDE.md, README) — persistent project-wide context, conventions
- **Code Change** — fix in the codebase itself (e.g., shared test helper, better abstractions)

## Instructions

1. **Initialize**
   - Add tasks to the todo list for tracking progress.

2. **Locate History**
   - Detect the IDE (Claude Code, Cursor, OpenCode).
   - Find session history files using the paths from "Session History Locations" above.
   - List and sort sessions by date.

3. **Determine Scope**
   - Based on user request, decide how many sessions to analyze (see "Scope Determination" table).
   - Communicate the chosen scope and reasoning to the user.

4. **Read & Parse Sessions**
   - Read each session JSONL file.
   - For each session, extract: title, user requests, tool calls, errors, outcomes.
   - Skip `queue-operation`, `file-history-snapshot`, and `progress` type entries (unless they contain hook errors).

5. **Analyze Individual Sessions**
   - For each session, identify: behavioral errors, technical decisions, context usage, outcomes.
   - Note any undocumented discoveries or ad-hoc decisions.

6. **Cross-Session Pattern Analysis**
   - Compare findings across sessions.
   - For each issue, classify as:
     - **Recurring** (2+ sessions, similar root cause) → requires systemic fix
     - **Isolated** (1 session only) → note but lower priority
   - For recurring patterns: count frequency, describe pattern signature, explain why it keeps happening.

7. **Formulate Report**
   Present findings in this structure:

   - **Scope**: N sessions analyzed, date range, reasoning for scope choice
   - **Recurring Patterns**: Issues found in 2+ sessions, with frequency and evidence
   - **Isolated Issues**: Notable one-off problems (lower priority)
   - **Primitive Usage Summary**: Which primitives were used/underused across sessions
   - **Corrective Actions**: Numbered list. Each item is a **self-contained narrative** — a reader must understand the full problem, its cause, and the proposed solution without reading any session transcript. Use the section structure below.

   **Section structure per item:**

   ```
   N. **[Recurring|Isolated] <clear problem title> (N/M sessions)**

      **What happened**: Full story across sessions. For each session where the issue appeared:
      what was the task, what actions did the agent take, what went wrong? Quote error messages
      and tool calls. A reader who never saw the sessions must get the complete picture.

      **Impact**: Measurable cost per occurrence and total. How many steps/tokens were wasted
      each time? What errors or regressions were introduced? What is the cumulative cost across
      all affected sessions?

      **Root cause**: Why does this keep happening (recurring) or why did it happen (isolated)?
      What knowledge, rule, or automation is missing? Why haven't previous fixes resolved it?

      **Proposed fix**:
      - **Where**: Exact file path and section (e.g., `CLAUDE.md` § "TDD Flow", after rule 4;
        or new file `test/helpers.ts`).
      - **Draft content**: The actual text to add — a rule, code, hook config, or skill
        description. Ready to paste. In a quote block or code block.
      - **Why this works**: How this fix addresses the root cause. Why will the agent behave
        differently with this artifact in place?

      **Recurrence risk**: HIGH/MEDIUM/LOW. What specific scenarios trigger this issue?
      How often do they occur? For isolated issues — under what conditions should this be
      escalated to a systemic fix?
   ```

   **Quality bar**: If you remove the title, a reader should still understand what happened, why it matters, and what to do about it. If any section would make a reader ask "what does this mean?" or "why?" — expand it.

   **Per-action completion gate (check before presenting)**: walk every corrective action on its own and reject it unless it carries ALL of: a per-session narrative (task, actions, what went wrong — for each session listed); a quantified Impact (steps, time, errors, and the total); an exact destination (`Where`); and complete paste-ready draft content. Do not infer one action's compliance from another's: the action that matches the example above tends to get the full treatment while the rest slide into a date list, a generic risk, and a fix described in prose (observed 2026-09-05 — one action out of three met the bar). When the evidence cannot support a field, say so in that field instead of generalising.

   **Anti-patterns (avoid):**
   - One-line sections: `Impact: 4-6 wasted steps` — doing what? With what consequence?
   - Bare session references: `Evidence: sessions 2026-03-15, 2026-03-20` — describe what happened in each session.
   - Actionless fixes: `Fix: add rule "mock before import"` — what is the full rule text? Where exactly to add it?
   - Vague locations: `Where: CLAUDE.md` — which section? After which existing rule?

   **Examples (desired detail level):**

   1. **[Recurring] JWT mock ordering breaks on every refactor (3/4 sessions)**

      **What happened**: In three out of four analyzed sessions, the agent hit the same `TypeError: jwtVerifier is not a function` when working with test files. **Session 2026-03-15**: agent refactored imports in `auth.test.ts`, moved the `import { authenticate } from './auth'` line above the mock setup call. Test failed at line 12 with `TypeError: jwtVerifier is not a function`. Agent spent 3 steps trying different import orders before discovering the cause. **Session 2026-03-20**: identical error in `user.test.ts:8` after restructuring test setup. Agent spent 4 steps reordering imports. **Session 2026-03-28**: same error in `admin.test.ts:15`, resolved in 6 steps by trial-and-error. In all three cases the root cause was identical: the module under test captures the JWT verifier at import time, so `setupMockJwt()` must be called *before* the `import` statement, not after.

      **Impact**: 13 wasted agent steps across 3 sessions (3 + 4 + 6). Each occurrence adds ~5 minutes of trial-and-error debugging with identical symptoms. The pattern is invisible — nothing in project docs or code explains the import-time binding behavior of the JWT module.

      **Root cause**: The `auth` module calls `getJwtVerifier()` at module load time and caches the result. If the mock is set up after import, the module already holds a reference to the real (undefined) verifier. No rule or code comment documents this constraint. The agent rediscovers it from scratch each session.

      **Proposed fix**:
      - **Where**: (1) `CLAUDE.md` § "Test Rules", after "No stubs or mocks for internal code." (2) New file `test/helpers.ts`.
      - **Draft content**:
        Rule text: _"In test files for JWT-authenticated modules, call `setupMockJwt()` from `test/helpers.ts` BEFORE importing the module under test. The auth module captures the JWT verifier at import time — mocking after import has no effect."_
        Helper file `test/helpers.ts`:
        ```typescript
        export function setupMockJwt() {
          globalThis.jwtVerifier = (token: string) => ({ sub: "test-user", exp: Date.now() + 3600 });
        }
        ```
      - **Why this works**: The rule explains the *why* (import-time binding), so the agent understands the constraint rather than memorizing a procedure. The shared helper eliminates copy-paste mock setup across test files.

      **Recurrence risk**: HIGH — triggers on every refactor that touches import order in test files. Without the fix, each occurrence costs ~5 minutes and 4-6 agent steps.

   2. **[Isolated] Agent wrote custom auth check instead of using existing middleware**

      **What happened**: In session 2026-03-25, the user asked to "just add a quick admin check to the dashboard endpoint." The agent wrote a custom `checkAdmin()` function directly in `dashboard_handler.ts` that reads the user role from the request and returns 403 if not admin. However, the project already has a `requireRole('admin')` middleware in `src/middleware/auth.ts:34` that does exactly this — including proper error formatting, audit logging, and role hierarchy support. The agent never read the `src/middleware/` directory in this session, likely because the user's framing ("just add a quick check") implied a small inline solution.

      **Impact**: The custom `checkAdmin()` duplicates existing functionality but lacks audit logging and role hierarchy support that the middleware provides. This creates a security inconsistency — the dashboard endpoint silently bypasses the audit trail that all other admin endpoints use.

      **Root cause**: One-off skip — in all other analyzed sessions, the agent read `src/middleware/` before adding auth logic. The user's urgency framing ("just add a quick check") likely biased the agent toward an inline solution.

      **Proposed fix**:
      - **Where**: No systemic action needed yet.
      - **Draft content**: N/A — replace the custom `checkAdmin()` in `dashboard_handler.ts` with `app.use('/dashboard', requireRole('admin'))` and delete the custom function. This is a one-time code fix, not a rule.
      - **Why this works**: Restores consistency with the existing middleware pattern.

      **Recurrence risk**: LOW — occurred in 1/4 sessions. **Escalation trigger**: if the same skip appears in 2+ future sessions, add a rule to `CLAUDE.md` § "Core Project Rules": _"Before adding auth/validation logic, read `src/middleware/` for existing patterns. Do not write inline auth checks."_

8. **Self-Criticism**
   Before presenting the report, critically examine your own cross-session analysis:
   - **Validity**: Re-examine each finding — is it backed by concrete evidence from multiple sessions, or did you over-generalize from superficially similar events? A TypeError in two sessions is not a "recurring pattern" if the root causes differ.
   - **False Positives**: Are any flagged patterns actually acceptable behavior? (e.g., reading a related file to understand existing conventions is not "redundant"; updating tests after intentional behavior change is not always "modifying tests instead of code").
   - **Proportionality**: Is each proposed systemic fix proportional to the pattern's frequency and impact? A pattern seen in 2 out of 10 sessions may not warrant a new hook — consider lighter interventions (a doc note, a rule) first.
   - **Blind Spots**: Did you focus too narrowly on one pattern type and miss others? Consider whether the sessions contain unremarked security issues, performance problems, or missing documentation.
   - **Severity Calibration**: Are recurring/isolated classifications accurate? Re-check that "recurring" patterns share the same root cause across sessions, not just similar symptoms.
   - **Revise**: Based on the above, update the report — remove weak findings, strengthen valid ones, reclassify patterns, adjust severity. Explicitly note what changed and why.

9. **Present & Confirm**
   - Present the revised report from steps 7–8.
   - Clearly mark which findings were adjusted during self-criticism and why.
   - Ask the user if they want to apply any of the proposed changes.
