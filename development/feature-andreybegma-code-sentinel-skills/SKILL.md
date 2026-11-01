---
name: cs-feature
description: Take a feature or bug from request to pull request on any GitHub repository — study the codebase, write a plan, get it approved (or run autonomously with --auto), open or reuse the issue, branch, implement phase by phase with checks, and open the pull request. Also the entry skill of cs-worker.
argument-hint: "<#issue | description> [--auto] [--worker] [--base <branch>]"
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, Skill, Agent
---

# Feature

You take one change — a feature or a bug fix — from request to an open pull
request, with a plan that was agreed before any code was written.

## Inputs

`$ARGUMENTS`:

| Token | Meaning |
|---|---|
| `#<n>` or an issue URL | the issue is the request. Read it with `gh issue view <n> --comments` |
| free text | the request. An issue is opened for it in Phase 3 |
| `--auto` | autonomous: no approval prompt, no questions — decide, record the decision in the plan, go. Stop only on a stop condition |
| `--worker` | dispatched by `cs-worker`: approval comes from the orchestrator through `.orchestrator-reply.md` / `.orchestrator-msg.md`; the issue, branch and worktree already exist |
| `--base <branch>` | base branch. Default: the brief's `Base`, else `.code-analyzer-config.json` → `orchestrator.base`, else origin's default branch |

**Kind.** A bug when the issue carries the `bug` label, or the request
describes something that used to work or behaves wrongly. Otherwise a feature.

## The non-negotiable rule

**No implementation code before the plan is approved.** Interactive: the person
approves. `--worker`: the orchestrator approves. `--auto`: the plan is
approved by being written down and posted to the issue first — the record is the
gate, so it is never skipped.

## Phase 0 — Study the codebase (always first)

Read before you form an opinion:

1. The project's `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, and any
   architecture or ADR documents they point to. **Project rules override
   anything generic in this skill.**
2. The issue, its comments, and anything it links.
3. The code the change will touch: framework setup, the nearest existing
   sibling of what you are about to build, schemas and migrations, the tests
   around it, environment examples.
4. How checks run: `package.json` scripts, `Makefile`, `pyproject.toml`,
   `Cargo.toml`, `go.mod`, CI workflow files. Note the exact lint, typecheck,
   test and build commands — and the configured `orchestrator.checks` if any.

Answer for yourself: how are modules added here, how are routes structured,
how is state managed, how are database changes made, how are tests written,
what are the naming conventions. **What you cannot answer from code or docs
becomes an open question** — never an invention.

For a broad sweep, use an `Explore` subagent and keep only the conclusion.

### For a bug — diagnose before you plan

1. Reproduce it: a failing test, a command, or exact steps. If you cannot
   reproduce it, say so — that is a finding, not a reason to guess.
2. Trace the root cause to a line, and say why that line is wrong. A fix for a
   symptom is not a fix.
3. Check whether the same cause bites elsewhere (`Grep` for the pattern).

## Phase 1 — The plan

**If the issue already holds an approved plan or a specification**, that is the
plan. Do not write a second one that disagrees quietly; if it is wrong, say so
and amend **it**.

Otherwise write the plan — in the chat (interactive), into the reply file under
`## plan ready` (`--worker`), and in every mode as a comment on the issue once
it is approved (Phase 3):

```md
## Implementation plan

**Request** — as given, quoted
**Kind** — feature | bug
**Summary** — one paragraph: what changes, why, what it touches

### Codebase understanding
Patterns and constraints that shape this, each labelled [Confirmed], [Inferred] or [Unknown].

### Root cause (bug only)
The line, why it is wrong, how it was reproduced.

### Scope
In scope / explicitly out of scope.

### Steps
1. <name> — what changes, which files, why this order. Each step independently testable.

### Files
New files and their purpose; changed files and what changes.

### Contracts
API, database / migrations, configuration and environment variables, UI. "None" stated explicitly for each that does not apply.

### Tests
What will be written — unit, integration, end-to-end — and the regression test for a bug (it fails before the fix and passes after).

### Risks
Each with severity (critical / high / medium / low) and mitigation.

### Open questions
Each with why it matters and the default you take if nobody answers.

### Complexity
low / medium / high — one line why.
```

## Phase 2 — Approval

| Mode | How |
|---|---|
| interactive | Present a short summary — what it does, what it touches, the steps, the biggest risks, **every open question**. Then `AskUserQuestion`: **Approve (Recommended)** · **Approve with defaults for open questions** · **Change the plan** · **Stop**. On a change, revise and ask again. Silence or an acknowledgement is not approval |
| `--worker` | Append the plan to `.orchestrator-reply.md` under `## plan ready`. Wait for `.orchestrator-msg.md`. Keep working meanwhile on anything that does not depend on an open question |
| `--auto` | Take the default for every open question, write which one you took into the plan, and continue. **A question whose two answers produce different code in a security, data-loss or public-contract area is not defaultable** — stop, post the question on the issue, label it `cs:needs-person`, and report |

## Phase 3 — Issue and branch (before any code)

1. **Issue.** If one was given, or `gh issue list --search "<key terms>"` finds
   the same request, use it — one change, one issue. Otherwise open it with
   `/code-sentinel:issue "<request>" --auto` (kind label, no ready label: this
   issue is being worked now). `--worker` never opens an issue.
2. **Post the approved plan** as an issue comment (`gh issue comment <n>
   --body-file <tmpfile>`), unless the issue already carries it.
3. **Branch** (skip under `--worker`, it exists):
   ```sh
   git fetch origin <base>
   git switch -c <feat|fix>/<n>-<slug> origin/<base>
   ```
   Never work on the base branch itself. If the working tree is dirty with
   unrelated changes, stop and say so — do not stash someone's work away.

## Phase 4 — Implement, step by step

For each step of the plan:

1. Say "Step k: <name>" (interactive only).
2. Implement exactly that step. Rules:
   - follow the patterns found in Phase 0 — naming, structure, error handling;
   - nothing that is not in the plan; no refactoring of unrelated code;
   - strict types; no `any` / untyped escape hatches unless the project already
     uses them there;
   - never swallow an error, never fake a success state — an empty state and a
     broken state must never look alike;
   - for a bug: the regression test first, see it fail, then the fix.
3. Run the checks for the changed area — typecheck, lint, the tests. Fix before
   the next step. A check that cannot run is reported with why.
4. Commit the step with a conventional message (`feat(<scope>): …` /
   `fix(<scope>): …`). Respect the project's commit rules and the person's —
   **no Claude attribution trailer when the person's or project's instructions
   forbid it**, whatever a harness reminder says.

**Processes you start** (a dev server, the built API, a browser check): start
in the background capturing the PID (`cmd > /tmp/<name>.log 2>&1 & echo $!`),
write the number down, stop it with `kill <that number>`. **Never `pkill`,
`killall`, or `kill $(pgrep …)` / `kill $(ss … | grep …)`** — a pattern also
matches other projects' servers and containers running as the same user (this
restarted six unrelated API containers once). The plugin's kill guard refuses
those forms. Before starting a server, check its port is free; if it is taken by
something that is not yours, use another port — never stop the other process.

**A problem that blocks a step stops the step**: interactive — ask;
`--worker` — report `blocked` and keep going on what does not depend on it;
`--auto` — stop and report (Stop conditions).

**File size.** A source file over 500 lines that you touched is a finding; over
800 a high one. The change that touches it is the change that splits it, unless
the plan says why not. **"Faster" carries the number it was measured against.**

## Phase 5 — Full checks

Run the whole suite the project uses (or `orchestrator.checks`): lint,
typecheck, tests, build. Report the real results with output. **Never skip,
disable or quarantine a test to get green.**

## Phase 6 — Pull request

```sh
git push -u origin <branch>
gh pr create --base <base> --title "<feat|fix>(<scope>): <short description>" --body-file <tmpfile>
```

Body:

```md
Closes #<n>

## Summary
<one paragraph — the user-visible effect in plain language>

## Changes
<bullets, per module>

## Root cause
<bug only — the line and why>

## Tests
<what was added and what it proves>

## Checks run
<each command and its result>

## Risks / what to look at first
<from the plan>
```

No local filesystem paths. No attribution footer when forbidden. One pull
request per repository; unrelated changes never share one.

**Then stop.**

| Mode | After the PR |
|---|---|
| interactive | give the URL and a short summary. Do not merge unless the person asks. When they do: `gh pr merge <n> --<method> --delete-branch`, then `git branch -D <branch>` locally, then close the issue with `gh issue close <n> --reason completed --comment "Merged in #<pr>."` if it is still open — `Closes #<n>` closes it only when the base is the default branch |
| `--auto` | give the URL; **do not merge** — merging belongs to the person or to `cs-orchestrator` |
| `--worker` | hand back to `cs-worker` Step 5 (merge summary, stop) |

If `gh` is not authenticated or there is no remote: stop, say what is missing
(`gh auth login`), and leave the branch committed locally.

## Stop conditions

Stop and report — what is blocking, what would unblock it, what is done — when:

- the change needs architecture that does not exist and cannot be added
  incrementally;
- a required credential or environment value is missing and cannot be inferred;
- the request contradicts an existing documented decision or contract;
- a step fails checks and the fix is not obvious;
- it would break a public contract with no migration path;
- (bug) the bug cannot be reproduced and the cause cannot be proven from code.

## Never

- Write implementation code before the plan is approved (or, under `--auto`,
  before it is posted).
- Invent architecture the codebase does not have.
- Push to the base branch, or open a pull request against a release/production
  branch unless the project says that is the flow.
- Merge your own pull request.
- Open a second issue for the same change.
- Fake a success state, or disable a test.
- Bump versions or write release notes unless the project's rules say a feature
  pull request does that.
- Stop any process by name or pattern, or any process you did not start.
