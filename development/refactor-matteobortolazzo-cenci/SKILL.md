---
name: refactor
description: "Analyze a codebase with specialized agents and propose refactoring tickets."
compatibility: Requires Claude Code subagents, interactive gates, and cenci project configuration.
argument-hint: "[scope: files/dirs/glob] [additional context]"
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Glob, Grep, Task, AskUserQuestion, Bash(git diff --name-only:*), Bash(git log:*), Bash(git remote get-url:*), Bash(wc -l:*), Bash(jq -n:*), Bash(gh api repos/:*)
---

> **Client dispatch**: In Codex, read `codex-runtime` and `refactor/codex.md`, execute that native procedure, and do not continue into the Claude procedure below.

> **Interaction rule**: Every question, confirmation, or approval directed at the user — anywhere in this skill, including error recovery — MUST be asked with the `AskUserQuestion` tool. Never ask in plain text. If an instruction says "ask the user" or "confirm", that means `AskUserQuestion`.

Read the `subagent-safety` reference skill before delegating work to subagents.

## Phase 1: Context Loading

Read `project-core`, resolve neutral configuration, and use the resulting config.
Use root and applicable project `AGENTS.md` as guidance.

> **Progressive disclosure**: Do NOT eagerly read reference docs in this Context section. Read relevant `docs/<topic>.md` files (and any legacy `.claude/rules/lessons-learned.md` if present) when you reach the analysis step that needs them.

### Monorepo Context Loading

If `isMonorepo` is `true` in the resolved config:

1. **Determine affected project(s)**: From the scope and file paths, match against the `projects` array in config to identify which project(s) the analysis affects.
2. **Read per-project AGENTS.md** for stack details and conventions.
3. **Pass project context to subagents**, including applicable AGENTS.md content and on-demand docs.

**Shell rules**: Read the `shell-rules` skill before running any `gh` commands (covers heredoc temp-file pattern).

### Config Existence

Before any other checks, verify neutral-first config resolution succeeded. If not, **stop immediately** and tell the user:
"cenci is not configured for this project. Run `/cenci:configure` first to set up."

### Parse Scope from `$ARGUMENTS`

- **If arguments provided** → use as explicit scope (file paths, directories, globs)
- **If no arguments** → determine scope from recent changes:
  ```bash
  git diff --name-only HEAD~10..HEAD
  ```
  If this returns files, use them as the scope.
- **If no git changes** → ask the user for scope via `AskUserQuestion`:
  > "No scope provided and no recent git changes found. Which files or directories should I analyze?"

**Tip for large or unfamiliar codebases**: Phase 3 fans out 3 parallel analyzer subagents per run. On a first run against an unfamiliar or large codebase, prefer scoping to a single directory or a handful of files before analyzing the whole repo — it keeps that fan-out cheap to validate before committing to a full-repo pass.

## Phase 2: Scope Analysis

<details>
<summary>Phase details</summary>

1. **Gather target file list** from the determined scope:
   - If scope is a glob pattern → expand with Glob tool
   - If scope is a directory → list all source files recursively (exclude `node_modules`, `.git`, `dist`, `build`, `bin`, `obj`, lock files, and auto-generated files)
   - If scope is specific files → use directly
2. **Collect file metadata** for each file:
   - Full path
   - Line count (use `wc -l` via Bash)
   - Language (infer from extension)
   - Whether it's a test file (matches common patterns: `*.test.*`, `*.spec.*`, `*_test.*`, `*_spec.*`, files in `__tests__/`, `tests/`, `test/` directories)
3. **Read project stack info** from the resolved config — framework, testing library, language
4. **Prepare shared context string** for subagents containing:
   - File list with line counts and languages
   - Stack info (framework, testing, language)
   - Project conventions from CLAUDE.md
   - Lessons learned

</details>

## Phase 3: Parallel Analysis

Launch all 3 analyzers as parallel Task tool calls in a **SINGLE message**.

<details>
<summary>Phase details</summary>

1. **Gather shared context ONCE** before launching analyzers — **by path, not by paste**:
   - The file list with metadata (paths, line counts, languages, test-file flags) from Phase 2
   - Stack info and CLAUDE.md conventions (short summaries, not full file dumps)

   Do **not** read full file contents in the main agent. All three analyzers have `Read`/`Grep`/`Glob` and read the files they need themselves — pasting contents would duplicate the scope into the main context plus each of the three Task prompts.

2. **Launch ALL THREE analyzers as three parallel Task tool calls in a SINGLE message:**
   - Task 1: **duplication-analyzer** agent — pass the file path list; it reads and compares code blocks itself
   - Task 2: **security-analyzer** agent — pass the file path list + stack info + CLAUDE.md conventions
   - Task 3: **structure-analyzer** agent — pass the file path list + line counts + test file identification

3. **Wait for all 3 to complete**, then proceed to Phase 4.

**Note on large scopes** (20+ files): tell each analyzer which files to prioritize rather than reading them yourself:
- Files over 200 lines
- Files modified recently (from git log)
- Test files over 300 lines
- Files with common vulnerability patterns (controllers, routes, auth, API handlers)

</details>

## Phase 4: Results Consolidation

<details>
<summary>Phase details</summary>

Parse each agent's structured output and merge findings into a unified list.

### Deduplication

If multiple analyzers flag the same file/location:
- **Security + Duplication** both flag same code → keep as separate findings but note the overlap
- **Structure + Duplication** both flag same large file → merge into a single "Split and deduplicate" finding
- **Identical findings** from different analyzers → keep the one with more detail, discard the other

### Sorting and Grouping

1. **Sort by severity**: Critical → High → Medium → Low
2. **Group by category**: Security → Duplication → Structure
3. **Assign effort estimates** to each finding:
   - **S** (< 1hr): Simple extractions, constant consolidation, renaming
   - **M** (half day): File splits, shared module creation, test reorganization
   - **L** (1+ day): Architectural changes, security overhauls, major refactors

### Numbering

Assign each finding a sequential number (F1, F2, F3...) for easy reference in Phase 5.

</details>

## Phase 5: Present Findings to User

<details>
<summary>Phase details</summary>

Display the consolidated report using markdown formatting.

### Report Format

```
## Refactoring Analysis Report

**Scope**: <files/directories analyzed>
**Files analyzed**: <count>
**Total findings**: <count> (Critical: N, High: N, Medium: N, Low: N)

---

### Security Findings

#### F1. [CRITICAL] <title>
- **Location**: `path/to/file:line`
- **Issue**: <description>
- **Risk**: <what could happen>
- **Suggested fix**: <approach>
- **Effort**: S | M | L

<details>
<summary>Details</summary>
<verbose details, code examples, references>
</details>

#### F2. [HIGH] <title>
...

---

### Duplication Findings

#### F3. [HIGH] <title>
- **Pattern**: <what is duplicated>
- **Locations**: `file1:lines`, `file2:lines`
- **Occurrences**: <count>
- **Suggestion**: <extract to shared function/module/constant>
- **Effort**: S | M | L

---

### Structure Findings

#### F4. [MEDIUM] <title>
- **File**: `path/to/file` (<N> lines)
- **Issue**: <why it needs attention>
- **Suggestion**: <split/reorganize approach>
- **Effort**: S | M | L

---

### Summary
| Category | Critical | High | Medium | Low | Total |
|----------|----------|------|--------|-----|-------|
| Security | N | N | N | N | N |
| Duplication | N | N | N | N | N |
| Structure | N | N | N | N | N |
| **Total** | **N** | **N** | **N** | **N** | **N** |

Estimated total effort: <sum of effort estimates>
```

### No Findings

If all 3 analyzers returned no findings:
> "No refactoring issues found in the analyzed scope. The code looks clean!"

**STOP HERE** if no findings.

### User Decision

After presenting the report, ask the user via `AskUserQuestion`:

> "Which findings should I create tickets for?"

Options:
- **All findings** — Create tickets for everything
- **Critical and High only** — Skip Medium and Low
- **Let me pick individually** — I'll ask about each one
- **None (keep report only)** — Don't create any tickets

If the user selects "None" → skip to Phase 7 (Summary) with no tickets created.

</details>

## Phase 6: Ticket Creation

**Main-agent-only** — requires auth for `gh` commands.

<details>
<summary>Phase details</summary>

### Prerequisites

Read the `shell-rules` skill before running any `gh` commands.

Extract `owner/repo` from `git remote get-url origin`.

### Individual Selection Mode

If the user selected "Let me pick individually":
- For each finding, present it briefly and ask via `AskUserQuestion`:
  > "Create a ticket for F<N>: <title>? (<severity>, <effort>)"
  Options: **Yes** / **No**
- Collect all approved findings, then create tickets for those.

### Ticket Body Template

For each approved finding, use the `Write` tool to author the raw title and body as plain
text (never a heredoc, and never a hand-escaped JSON literal — the title is free text and
must never be interpolated directly into a command line). Refactor has no ticket/PR
identifier in scope, so `F<N>` alone would collide across concurrent runs — scope both
filenames with a `<run-id>` (a run-unique key generated once at skill start, e.g. a
timestamp literal, which is inherently safe under the `shell-rules` scope-key format rule)
in addition to the per-finding `F<N>` suffix:

- `${TMPDIR:-/tmp}/cenci/cenci-refactor-<run-id>-F<N>-title.txt` — content: `refactor: <title>`
- `${TMPDIR:-/tmp}/cenci/cenci-refactor-<run-id>-F<N>-body.md` — content:
  ```
  ## Refactoring: <title>

  ### Category
  <Security | Duplication | Structure>

  ### Severity
  <Critical | High | Medium | Low>

  ### Description
  <finding description>

  ### Affected Files
  - `path/to/file1`
  - `path/to/file2`

  ### Suggested Approach
  <how to fix, with code examples if relevant>

  ### Effort Estimate
  <S | M | L> — <reasoning>

  ---
  *Generated by cenci refactor analysis*
  ```

Build the payload with the `shell-rules` skill's canonical `jq -n --rawfile` snippet, as its
own standalone Bash call:
```bash
jq -n --rawfile title ${TMPDIR:-/tmp}/cenci/cenci-refactor-<run-id>-F<N>-title.txt --rawfile body ${TMPDIR:-/tmp}/cenci/cenci-refactor-<run-id>-F<N>-body.md '{title: ($title | rtrimstr("\n")), body: $body, labels: ["Refined"]}' > ${TMPDIR:-/tmp}/cenci/cenci-refactor-<run-id>-F<N>-payload.json
```

Then create the ticket with a separate standalone Bash call:
```bash
gh api repos/<owner>/<repo>/issues -X POST --input ${TMPDIR:-/tmp}/cenci/cenci-refactor-<run-id>-F<N>-payload.json --jq .number
```
The `--jq .number` output is the new ticket's issue number — proof the API accepted valid
JSON (refine's documented create-time proof; no title re-fetch here, to avoid a
single-call-site `gh issue view` grant).

### Error Recovery

- If `gh` command fails with auth error → stop and tell the user to check authentication
- If ticket creation fails for one finding → report the error, continue with remaining findings
- If all ticket creations fail → report the error pattern and suggest manual creation

</details>

## Phase 7: Summary

<details>
<summary>Phase details</summary>

Present a final summary:

```
## Refactor Analysis Complete

### Tickets Created
| # | Finding | Ticket | Severity | Effort |
|---|---------|--------|----------|--------|
| F1 | <title> | #<id> | Critical | M |
| F2 | <title> | #<id> | High | S |

### Findings Not Ticketed
| # | Finding | Severity | Reason |
|---|---------|----------|--------|
| F3 | <title> | Medium | User skipped |
| F4 | <title> | Low | User skipped |
```

If no tickets were created (user selected "None"):
```
## Refactor Analysis Complete

Report generated with <N> findings. No tickets were created.
Review the findings above and run `/cenci:refactor` again when ready to create tickets.
```

**STOP HERE.** Do not offer to implement any of the refactors.

</details>
