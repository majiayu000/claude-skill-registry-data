---
name: explain
description: "Generate project explanation docs in docs/explain/ covering architecture, flows, syntax, system APIs, infra, and testing, or explain a code diff, commit, branch, or PR directly in the conversation with --diff."
argument-hint: "[--diff [--staged | --unpushed | target] | --all | --architecture | --flows | --syntax | --system | --infra | --test] [topic]"
effort: medium
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Explain

Generate project explanation documents in `docs/explain/`. Each aspect of the project gets its own file. An `overview.md` acts as the index (opened first); a `preliminary.md` carries the shared project context every other doc assumes. The exception is `--diff`, which explains a change directly in the conversation and never writes files.

## Flags

| Flag | What it covers |
|------|----------------|
| `--architecture` | Components, data flow, layering. Pros/cons of the current design **and** at least one alternative structuring with its tradeoffs. Include ASCII diagrams (component maps, layer stacks, sequence diagrams, ER, state machines) wherever they make the structure easier to grasp than prose. |
| `--flows` | End-to-end walkthroughs of real code paths: take a concrete input (user action, API request, CLI invocation, scheduled job, etc.), trace it from entry point through the stack to final state change or response. Annotate the actual code inline — explain what each step does and any non-obvious syntax as it appears. |
| `--syntax` | Non-obvious language features actually used in the project **and not already explained inline in `flows.md`**. Skip basics like `for` loops. Where the language offers multiple ways to do the same thing, list them with pros/cons. |
| `--system` | System-level APIs in use (filesystem, networking, process, IPC, OS-specific). For each, list alternatives with pros/cons. |
| `--infra` | Build, CI/CD, deploy, release pipelines. Include how to run each piece locally (scripts, commands, env setup). |
| `--test` | Testing infrastructure: frameworks, test types, fixtures, how to run. |
| `--all` | All six aspects above, dispatched to parallel sub-agents. |
| `--diff [target]` | Explain a code change directly in the conversation. `target` may be a commit, revision range, branch comparison, PR number, or PR URL. With no target or scope flag, explain current tracked worktree changes against `HEAD` plus any untracked files. This is a standalone, read-only mode: do not generate `docs/explain/` files or modify anything. |
| `--staged` | Scope to files returned by `git diff --cached --name-only`. Combines with any aspect flag or with `--diff`. |
| `--unpushed` | Scope to files changed across unpushed commits (`git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD`). Combines with any aspect flag or with `--diff`. |
| _topic_ | A positional word after an aspect flag narrows the focus (e.g. `--architecture database` = architecture of the database layer only, `--flows login` = just the login flow). |

## Usage

```
/explain --all                      # Full project explanation
/explain --diff                     # Explain current worktree changes in this conversation
/explain --diff --staged            # Explain staged changes in this conversation
/explain --diff HEAD~2..HEAD        # Explain a revision range in this conversation
/explain --diff 123                 # Explain PR #123 in this conversation
/explain --architecture             # Just architecture
/explain --architecture database    # Architecture, focused on the database
/explain --flows                    # End-to-end walkthroughs of representative code paths
/explain --flows login              # Walk through just the login flow
/explain --staged --architecture    # Architecture needed to understand staged changes
/explain --unpushed --architecture  # Architecture needed to understand unpushed changes
/explain --staged --all             # All aspects, scoped to staged files
/explain --infra                    # CI/CD + local setup
```

## Workflow

### 1. Parse arguments
- If `--diff` is present, enter the conversational diff mode below. It is standalone: do not combine it with an aspect flag or `--all`.
- For `--diff`, accept at most one of `--staged`, `--unpushed`, or an explicit target. A target can be a commit, revision range, branch comparison, PR number, or PR URL.
- Collect requested aspect flags. `--all` expands to all six.
- Check for `--staged` / `--unpushed`.
- Capture any positional topic filter that follows an aspect flag, and pass it to that aspect's sub-agent only.
- If neither `--diff`, an aspect flag, nor `--all` was given, ask the user which mode or aspect(s) to cover before proceeding.

### 2. Handle `--diff` in the conversation and stop

`--diff` is strictly read-only. Do not create, edit, or overwrite files; do not run formatters or generators; and do not dispatch write-capable sub-agents. Inspect the change and surrounding code with read-only tools, give the explanation in the current conversation, and stop before step 3.

Resolve the change in this order:

| Input | Change to inspect |
|-------|-------------------|
| Diff already supplied by the user | The supplied diff and any repository context available locally |
| `--staged` | `git diff --cached` |
| `--unpushed` | The full unpushed range used by the document modes |
| PR number or URL | PR metadata and patch; for GitHub, use `gh pr view` and `gh pr diff` |
| Commit | The commit patch and metadata, using read-only git commands |
| Revision range or branch comparison | The diff for that exact range or merge-base comparison |
| No target | `git status --short` plus tracked worktree changes against `HEAD`; inspect untracked files separately because `git diff HEAD` omits them |

If the target is genuinely ambiguous, ask one concise question rather than guessing. If the resolved diff is empty, say which scope was checked and stop.

Treat the diff as a map, not as sufficient context. Read the changed functions plus the callers, callees, tests, types, configuration, and docs needed to explain the existing system and the behavioral change. Reconstruct the relevant before-and-after flow. State uncertain motivation as an inference rather than fact.

Return one coherent chat response with these sections:

1. **Summary** — lead with the change's purpose and observable effect in one or two sentences.
2. **Background (skip if familiar)** — first give the minimum beginner context, then narrow to the existing components, data flow, and constraints directly involved in the change.
3. **Intuition** — explain the central idea before implementation details. Use a concrete example or toy data. Add a small diagram or table only when it materially improves understanding.
4. **Code walkthrough** — group changes by behavior or concept in the order a reader needs, not raw file order. Cite real files and line numbers, distinguish changed code from surrounding context, and connect each edit to the behavior it enables.
5. **Check your understanding** — ask five medium-difficulty multiple-choice questions that test the substance of the change without gotchas. Do not reveal the answers until the user responds; then grade each answer and explain why it is right or wrong.

Do not dump the whole diff or reproduce long functions. Quote only the snippets needed to anchor an explanation. This is an explanation, not a code review: do not turn it into a findings list unless the user also asked for review.

### 3. Determine document scope

| Mode | Scope |
|------|-------|
| `--staged` set | Output of `git diff --cached --name-only` |
| `--unpushed` set | Output of `git diff --name-only $(git rev-list HEAD --not --remotes \| tail -1)^..HEAD` |
| neither set | Whole project (respect `.gitignore`, skip `node_modules/`, `build/`, `dist/`, lockfiles, binaries) |

Empty scope: if `--staged` is set but nothing is staged, tell the user to stage files first or drop `--staged`. Do not proceed. Likewise, if `--unpushed` is set but nothing is unpushed — or there is no remote/upstream so the range can't be determined reliably (or it walks back to the root commit) — tell the user and do not proceed.

### 4. Write `preliminary.md` first
Before dispatching aspect sub-agents, write `docs/explain/preliminary.md`. Keep it tight — just enough shared context that a new reader can follow the other docs:
- Project name and purpose
- Primary language(s) and major frameworks
- Top-level directory layout
- Entry points (main binary, app root, server entry)

Every aspect sub-agent should be told to assume readers have read `preliminary.md` and link to it rather than restate its content.

### 5. Run aspect sub-agents in parallel
For each requested aspect, dispatch one sub-agent, launching each batch together as runtime capacity allows.

**The sub-agent must be able to write files.** Its deliverable is a markdown file it creates itself, so dispatch a general-purpose agent, never a read-only one (Claude Code's `Explore`, or any harness's read-only agent profile). A read-only agent either fails outright ("I'm in read-only mode") or flails improvising via `Bash` heredocs, which can stall it. Read-only agents suit tasks whose deliverable is a returned message, not a file.

**Assign delegation separately from write access.** Default aspect writers do their own research and writing; disable delegation tools where supported and include: *"Do not dispatch sub-agents or launch other agent CLIs; research and write this document yourself."* When an aspect benefits from coordinated research, replace that line with the named subtasks, maximum descendant count, and stopping condition. Include those descendants in the overall allocation; the aspect writer owns the final document.

Each sub-agent prompt must include:
- The aspect name (e.g. "architecture")
- The exact scope (list of staged files, or "whole project" with `.gitignore` honored)
- The topic filter, if any
- The target output path (`docs/explain/<aspect>.md`) — give the absolute path
- The per-aspect rubric (see below) copied into the prompt
- The file format template (see Output)
- Instructions to link to siblings using the "See also" block
- An explicit "use the `Write` tool to create the file" instruction
- The worker restriction or explicit coordination assignment from above

### 6. Write `overview.md`
After sub-agents return, write `docs/explain/overview.md` as the entry index: short intro, link to `preliminary.md`, one link per generated aspect file with a one-line summary. In the final chat response, tell the user to open `overview.md` first.

## File output for document modes

All output for aspect modes goes to `docs/explain/`. Existing files there are overwritten — this is generated content, not hand-written. `--diff` never writes any of these files.

```
docs/explain/
├── overview.md        # Index; open this first
├── preliminary.md     # Project context needed to read the rest
├── architecture.md    # If --architecture or --all
├── flows.md           # If --flows or --all
├── syntax.md          # If --syntax or --all
├── system.md          # If --system or --all
├── infra.md           # If --infra or --all
└── test.md            # If --test or --all
```

### File format (per-aspect)

```markdown
# [Aspect Title]

**Scope:** [whole project | staged files: path/a, path/b, …]
**Topic filter:** [none | database | …]
**See also:** [overview](overview.md) · [preliminary](preliminary.md) · [architecture](architecture.md) · [flows](flows.md) · [syntax](syntax.md) · [system](system.md) · [infra](infra.md) · [test](test.md)

[Body following the per-aspect rubric]
```

Only link to siblings that were actually generated in this run.

### Per-aspect rubrics

**architecture.md**
- Component/module map with data flow and boundaries
- Major design decisions, each with pros/cons
- For each major decision: at least one alternative structuring, with its pros/cons
- Reference real files/functions, not vague labels
- **Include ASCII diagrams** wherever they make the structure easier to grasp than prose. Pick whichever fits the thing being explained:
  - Component / module maps (boxes and arrows) — show which modules depend on which and what crosses each boundary
  - Layer stacks — show the vertical slicing (e.g. HTTP handler → service → repository → DB)
  - Sequence diagrams — show request/response ordering between components
  - Entity-relationship diagrams — show the shape of persistent data models
  - State machines — show lifecycles of domain objects (e.g. order: draft → paid → shipped → delivered)
  - Directory trees — show where things live when the layout is non-obvious
- Keep diagrams small and readable in a monospace font. Label arrows with what flows along them (data, calls, events). If a diagram needs more than ~25 lines, split it.

**flows.md**
- Pick 2–4 representative end-to-end code paths. Typical choices: the main user action, a representative API/RPC request, a CLI entry point, a scheduled or background job. Adjust for what the project actually does.
- Write each flow as a **linear guided tour** in execution order. A reader scrolling top-to-bottom should be able to follow the code path without jumping back.
- For each flow, use this structure:
  1. **Developer-facing setup** — the code the developer writes to install / invoke the feature (e.g. `ShortcutRecorderView($shortcut)`, `router.post("/login", loginHandler)`, `cron.schedule("0 3 * * *", reindex)`). One code block, no more than ~10 lines. This is the mental anchor — the API surface that triggers the flow.
  2. **End-user interaction** — what the end user does that drives the flow (clicks a field, submits a form, waits for the scheduled time). 1–2 sentences.
  3. **Walkthrough** — for EACH function that executes, in the order it executes, produce one section containing, in this order:
     - **Location header** — `#### <FunctionName>  —  <file>:<line>`
     - **Where we are** — a tiny locator: the file + layer/component this function lives in, and how control got here from the previous function. 1–3 lines or a ≤6-line mini-diagram showing the hop. This should NOT restate the full architecture — just the slice relevant to this step.
     - **The function code, in its entirety** — paste the full body from the source file, no edits, no elisions. If a function is genuinely too long (>~60 lines), split it at natural seams and walk the halves as separate steps, noting that you've done so.
     - **What it does** — prose or bullets explaining the control flow of THIS function, referencing its own lines (not the rest of the stack).
     - **Non-obvious syntax** — language features used inside this function that a reader might not immediately grasp (weak captures, decorators/attributes, macros, C interop, closure-return semantics, etc.). Only call out what actually appears here; skip basics.
     - **What happens next** — one line naming the next function in the trace and why control transfers (direct call, callback, event dispatch, async completion).
  4. **Terminal state** — after the last function's section, one short paragraph or bullet list describing what has visibly changed (DB row written, `@Binding` updated, response body sent, beep suppressed). This is the "and we're done" marker.
- Optionally, a single short ASCII sequence diagram at the end of the flow showing the whole hop chain at a glance. Do NOT put it at the start — it belongs as a recap.
- Do NOT precede the walkthrough with a separate Trigger / Entry point / Trace / Outcome summary. Those facts belong inline in steps 1, 2, the first walkthrough section, and step 4 respectively. Duplicating them up front is what makes flows hard to follow.
- If `--syntax` also runs this session, call out in a one-line note at the top of the file that language-feature coverage here is inline — `syntax.md` covers features not already annotated in a flow.

**syntax.md**
- Notable language features the project uses (macros, operators, type-system quirks, idioms) **that aren't already annotated inline in `flows.md`**
- For each: what it does, why it's used here, alternatives the language offers, pros/cons
- Omit anything a general programmer already knows
- If `flows.md` was also generated this session, open with a one-line pointer to it so readers know the annotated-code view lives there.

**system.md**
- System APIs in use (OS, filesystem, network, process, IPC, hardware)
- For each: what it does in this project, why this one, alternatives with pros/cons

**infra.md**
- Build system, CI/CD pipelines, release flow, deployment targets
- For each pipeline/script: what it does, where it lives, exact command(s) to run it locally, prerequisites, env vars

**test.md**
- Test frameworks in use; unit/integration/e2e split
- Directory layout, fixtures, mocks
- Exact commands to run the full suite and a single test

### overview.md format

```markdown
# Explanation Overview

Start here. Read [preliminary](preliminary.md) next for the shared context the
other docs assume.

**Scope:** [whole project | staged files: …]

## Aspects
- [Architecture](architecture.md) — one-line summary
- [Flows](flows.md) — one-line summary
- [Syntax](syntax.md) — one-line summary
- [System APIs](system.md) — one-line summary
- [Infrastructure](infra.md) — one-line summary
- [Testing](test.md) — one-line summary
```

Only include bullets for aspects actually generated this run.

## Examples

### `/explain --diff`
Read the current tracked worktree diff against `HEAD` and inspect untracked files separately. Explore the surrounding code needed to explain the change, then respond in the conversation with background, intuition, a concept-grouped code walkthrough, and five multiple-choice questions. Do not write any files.

### `/explain --diff 123`
Use GitHub CLI read-only commands to inspect PR #123 and its surrounding repository context. Explain it with the same conversational structure and leave the working tree untouched.

### `/explain --all`
Writes `preliminary.md`, dispatches six parallel sub-agents (one per aspect), writes `overview.md` last. Final chat message lists the files and tells the user to open `overview.md` first.

### `/explain --flows`
Whole-project scope. Picks 2–4 representative code paths (user action, API request, CLI/job) and traces each end-to-end in `flows.md` with inline-annotated code. Use `--flows login` to focus on a single flow.

### `/explain --staged --architecture`
`git diff --cached --name-only` → staged files. Write a focused `preliminary.md` covering the surrounding modules. Dispatch one sub-agent to produce `architecture.md` limited to what is needed to understand the staged change. Write `overview.md` linking only to `preliminary.md` and `architecture.md`.

### `/explain --architecture database`
Whole-project scope. Write `preliminary.md`. Dispatch one architecture sub-agent with topic filter `database`. `architecture.md` covers the database layer's structure, decisions, and alternatives only. `overview.md` links to the two generated files.

## Troubleshooting

### No staged files
"No staged files found. Stage files with `git add` first, or drop `--staged` to cover the whole project." Do not fall back to the whole project silently.

### No diff found
For `--diff`, name the checked target or scope and say that it contains no changes. Do not fall back to a broader scope and do not generate documentation files.

### Aspect not applicable to the project
E.g. `--infra` on a project with no CI/CD. Generate the file anyway with a clear "No CI/CD configured. Build runs manually via `…`" note, and still link to it from `overview.md`. Silent omission leaves the user wondering.

### Project too large for one sub-agent
The sub-agent can split by top-level directory and run its own parallel reads. If output is still incomplete, re-run the specific aspect flag (with a topic filter if helpful) rather than `--all`.

### Docs went stale after code changes
`docs/explain/` is regenerated, not incrementally updated. Re-run the relevant flags; existing files are overwritten.

## Notes
- Group by aspect, not by file. Within an aspect, cite real files/functions.
- Do not restate `preliminary.md` content inside aspect docs — link to it.
- Only link to sibling files that exist in this run; don't produce broken links.
