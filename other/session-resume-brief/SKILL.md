---
name: session-resume-brief
description: Reconstructs the current state of a software project after a break by inspecting repository guidance, Git status, recent history, changed files, roadmaps, TODOs, tests, and handoff notes. Use when the user asks to continue a project, resume yesterday’s work, understand what is unfinished, recover context in an unfamiliar repository, or determine the safest next task before editing code.
license: MIT
compatibility: Portable Agent Skill. Can be copied into an Agent Skills-compatible environment with repository file access and read-only command execution.
metadata:
  category: project-planning
  task_type: research
  audience: software-developers
  tags:
    - context-recovery
    - git
    - project-state
    - session-handoff
    - task-planning
  status: draft
  side_effects: command-run
---

# Session Resume Brief

## Purpose

Reconstruct enough reliable project context for a developer or agent to resume work safely after an interruption, a new session, or a period away from the repository.

The skill determines:

- what the project is trying to accomplish
- what changed recently
- what is currently in progress
- which files are modified or untracked
- what has been completed
- what remains unfinished
- which assumptions or decisions must be preserved
- whether the current state is validated
- what the safest next action should be
- which files should be opened first

The result is a compact orientation brief, not a general repository audit and not a new implementation plan.

The skill must favor evidence from the repository over guesses based on filenames, branch names, or incomplete TODO comments.

## When to use this skill

Use this skill when:

- The user asks to continue work on an existing repository.
- The user says “resume this project,” “continue where we left off,” or “what was I working on?”
- A new Codex or agent session needs to recover project context.
- Work was interrupted before completion.
- The repository contains uncommitted changes whose purpose is unclear.
- The current branch appears to contain partially completed implementation work.
- The user returns to a project after several days or weeks.
- A collaborator needs a concise orientation before taking over work.
- The next task should be chosen from the actual repository state.
- The user wants to know which files to inspect before making changes.
- A repository has roadmaps, handoff notes, TODOs, or decision records that need to be reconciled with current code.

Do not use this skill when:

- The user wants a broad architectural review.
- The user asks for a full code review or release-readiness audit.
- The repository has not been started and needs initial project planning.
- The user already supplied a complete and current handoff brief.
- The task is to implement a clearly specified change immediately.
- The user asks only for a Git history summary.
- The user asks to clean, commit, reset, stash, or discard changes.
- The task requires editing files rather than reconstructing context.
- The user asks for a long-term roadmap rather than the immediate project state.

## Operating constraints

- Treat the repository as read-only.
- Do not create, edit, move, delete, stage, commit, stash, reset, or restore files.
- Do not install dependencies.
- Do not run migrations.
- Do not start deployment or publishing workflows.
- Do not modify remote branches, issues, pull requests, or project boards.
- Do not assume uncommitted changes are disposable.
- Do not assume the latest commit represents the current unfinished task.
- Do not mark work complete merely because code exists.
- Separate confirmed facts from likely interpretations.
- Prefer repository-specific instructions over generic conventions.
- Inspect the minimum material necessary to establish reliable context.
- Avoid turning the resume brief into an exhaustive repository audit.

## Inputs to inspect

Inspect available sources in this order, adapting to the repository.

### 1. Repository instructions

Look for:

- `AGENTS.md`
- nested `AGENTS.md` files
- `CLAUDE.md`
- `CODEX.md`
- project instruction files
- `.agents/`
- contribution guidelines
- architecture notes
- coding conventions
- repository-specific skills

Repository instructions establish:

- project purpose
- allowed workflows
- source layout
- validation commands
- important constraints
- files that should not be modified
- expected output conventions

### 2. Immediate Git state

Inspect:

- current branch
- working tree status
- staged files
- modified files
- deleted files
- renamed files
- untracked files
- merge or rebase state
- upstream divergence when available

Useful read-only commands may include:

```bash
git status --short --branch
git diff --stat
git diff --name-status
git diff --cached --stat
git diff --cached --name-status
git branch --show-current
git log --oneline --decorate -n 15
````

Use more detailed diffs only when needed to understand the unfinished task.

### 3. Recent project history

Inspect:

* recent commits
* recent merge commits
* commit messages
* files changed by recent commits
* recent tags or releases
* current branch origin
* branch comparison against the default branch

Possible read-only commands:

```bash
git log --oneline --decorate --graph -n 20
git show --stat --summary HEAD
git diff --stat <default-branch>...HEAD
git log <default-branch>..HEAD --oneline
```

Do not assume `main` or `master` is the default branch. Determine it from repository context when possible.

### 4. Planning and handoff material

Look for:

* `ROADMAP.md`
* `TODO.md`
* `PLAN.md`
* `STATUS.md`
* `HANDOFF.md`
* `NEXT.md`
* `CHANGELOG.md`
* `docs/roadmap/`
* `docs/planning/`
* `docs/decisions/`
* issue exports
* session notes
* implementation checklists
* milestone documents

Treat planning documents as intent, not proof that work is implemented.

### 5. Project metadata

Inspect relevant metadata such as:

* `package.json`
* workspace configuration
* build configuration
* test configuration
* framework configuration
* deployment configuration
* package exports
* scripts
* environment examples
* documentation entry points

Use metadata to determine:

* available validation commands
* project structure
* active packages
* expected build output
* likely development workflow

### 6. Changed implementation files

Inspect the current diff and directly related source files.

Determine:

* what behavior is being added or changed
* whether implementation is partial
* whether public APIs are affected
* whether tests and documentation were updated
* whether temporary debugging code remains
* whether changes align with the current plan

Do not read the entire repository unless the task genuinely requires it.

### 7. Tests and validation evidence

Inspect:

* tests changed with the implementation
* test configuration
* recent test output stored in notes or CI
* build status when available locally
* lint and type-check configuration
* TODOs indicating missing validation

Validation commands may be identified, but should not automatically be run unless they are clearly safe, local, and read-only in effect.

When running validation would:

* modify snapshots
* regenerate files
* update caches tracked by the repository
* write coverage artifacts
* change lockfiles
* start services
* require credentials

report the command without running it.

## Evidence hierarchy

When sources disagree, use this priority order:

1. Current repository instructions
2. Current working tree and diff
3. Current branch history
4. Tests and executable project configuration
5. Current roadmap or handoff notes
6. README and general documentation
7. TODO comments
8. Filename or branch-name inference

A roadmap may say a task is pending while the code already implements it.

A TODO may be stale.

A README may describe the latest released state rather than the current branch.

The current code is strong evidence of implementation, but not proof of correctness or completion.

## State classifications

Classify work using these states.

### Confirmed complete

Use only when:

* implementation exists
* relevant tests or validation exist
* documentation or public API changes are addressed when required
* no clear unfinished markers remain

### Implemented but unvalidated

Use when:

* the main code appears present
* validation has not been run or recorded
* tests are missing, incomplete, or unknown

### In progress

Use when:

* source changes are partial
* TODOs remain within the active implementation
* related files are inconsistent
* tests or documentation indicate unfinished behavior

### Planned but not started

Use when:

* the task appears only in planning material
* no meaningful implementation evidence exists

### Blocked

Use when:

* progress depends on a missing decision, dependency, credential, asset, API, or external response
* the repository records a known blocker
* the current implementation cannot proceed safely

### Abandoned or stale

Use cautiously when:

* the work appears old
* current plans supersede it
* the branch or files no longer align with the active architecture
* repository history clearly indicates replacement

Do not classify work as abandoned from age alone.

### Unknown

Use when available evidence is insufficient or contradictory.

## Workflow

### 1. Establish repository identity

Determine:

* repository name
* project purpose
* primary framework or language
* package or application type
* current branch
* likely default branch
* whether the repository is a monorepo
* relevant subproject or package

If the repository contains multiple applications or packages, identify which area the current changes belong to.

### 2. Read governing instructions

Read repository-level and relevant nested instruction files before interpreting changes.

Record:

* project-specific rules
* required validation
* naming conventions
* protected areas
* source-of-truth documents
* expected planning files
* restrictions on generated files

Do not continue based on generic assumptions when local guidance exists.

### 3. Capture the immediate working state

Inspect the current branch and working tree.

Record:

* clean or dirty status
* staged changes
* unstaged changes
* untracked files
* deleted or renamed files
* current merge, cherry-pick, or rebase state
* branch divergence when available

Group files by likely purpose:

* implementation
* tests
* documentation
* configuration
* generated output
* assets
* temporary files
* unknown

Do not describe every changed line in the final brief. Summarize the task represented by the changes.

### 4. Determine the active workstream

Use the current diff, recent commits, branch name, planning notes, and changed files to identify the main active workstream.

Describe it as an outcome:

Good:

```txt
Add cancellable upload retries and expose retry lifecycle events.
```

Weak:

```txt
Update upload files.
```

If multiple unrelated workstreams exist, list them separately and identify which appears most active.

### 5. Reconstruct recent progress

Inspect a representative recent history.

Determine:

* what was completed recently
* which decisions were made
* which files or APIs changed
* whether current changes build directly on recent commits
* whether a refactor or migration is underway
* whether implementation has diverged from the documented plan

Avoid producing a generic commit log.

Translate history into meaningful progress.

### 6. Compare plans against implementation

Cross-reference planning documents with actual code.

For each relevant task, classify it as:

* confirmed complete
* implemented but unvalidated
* in progress
* planned but not started
* blocked
* stale
* unknown

Report discrepancies such as:

* roadmap says pending, but implementation exists
* checklist says complete, but tests are missing
* README documents behavior not present in code
* code exposes an API not documented in the plan
* tests expect an older contract
* addon compatibility remains unresolved

### 7. Inspect the active diff

Read enough of the changed files to understand:

* the current implementation goal
* completed portions
* incomplete portions
* public contracts affected
* probable next step
* regression risk
* related files that may still need changes

Look for incomplete-work signals:

* TODO or FIXME comments
* placeholder values
* skipped tests
* focused tests such as `.only`
* disabled lint rules
* temporary logging
* unhandled branches
* mock implementations
* duplicated interim code
* stale comments
* incomplete docs
* missing exports
* missing test coverage
* changed types without updated consumers

Do not treat every TODO in the repository as part of the current session.

### 8. Determine validation status

Identify the relevant validation commands from project configuration and instructions.

Examples:

* tests
* targeted tests
* type checking
* linting
* build
* formatting checks
* package validation
* documentation build
* accessibility checks

For each relevant check, classify it as:

* passed with current evidence
* failed with current evidence
* not run
* result unknown
* unsafe to run automatically
* unavailable in the environment

Never claim a check passed because a script exists.

If validation is run, record:

* exact command
* result
* relevant failure
* whether it may have generated files

### 9. Identify blockers and unresolved decisions

Separate blockers from ordinary remaining work.

A blocker may include:

* unclear API contract
* missing design decision
* unavailable external service
* broken dependency
* failing prerequisite test
* missing fixture or asset
* conflicting repository instructions
* incomplete migration dependency
* unknown expected behavior
* credentials not available

For every blocker, state:

* evidence
* impact
* what is needed to unblock it

Do not invent stakeholder decisions.

### 10. Identify the safest next action

Recommend one primary next action.

The action should:

* continue the active workstream
* be supported by evidence
* avoid discarding or overwriting work
* reduce uncertainty
* be small enough to validate
* respect current dependencies
* avoid beginning unrelated improvements

Good next actions:

* complete the missing event-detail type before updating consumers
* add targeted tests for the changed retry state
* reconcile the current diff with the documented API contract
* run the existing targeted test command
* inspect an unresolved failing fixture
* update the addon using the changed public event name

Weak next actions:

* finish the project
* improve the code
* continue implementation
* refactor everything
* update documentation and tests

### 11. Identify files to open first

List no more than five files unless the repository genuinely requires more.

Prioritize:

1. active implementation file
2. directly related test
3. public type or contract
4. current plan or decision record
5. relevant documentation or consumer

For each file, explain why it matters.

### 12. Flag actions that should not happen yet

Explicitly identify tempting but premature work, such as:

* unrelated refactoring
* dependency upgrades
* formatting the entire repository
* committing before validation
* updating release notes before the API stabilizes
* redesigning demos before behavior is complete
* regenerating snapshots before understanding failures
* discarding unknown untracked files
* modifying addons before the core contract is decided

This prevents scope drift during context recovery.

### 13. Produce the resume brief

Keep the result compact enough to use immediately.

The brief should answer:

* Where are we?
* What changed?
* What is unfinished?
* What is validated?
* What is blocked?
* What should happen next?
* Which files should be opened?

Do not include a complete repository inventory.

## Output format

Return:

````md
# Session Resume Brief

## Project context

- **Repository:** ...
- **Purpose:** ...
- **Stack:** ...
- **Current branch:** ...
- **Default branch:** ...
- **Working tree:** Clean | Modified | Conflict state | Unknown
- **Primary workstream:** ...

## Current state

Summarize the active repository state in three to six sentences.

Distinguish:

- confirmed facts
- likely interpretation
- unresolved uncertainty

## Recent progress

- ...
- ...
- ...

Include only progress relevant to the active workstream.

## Work in progress

| Area | State | Evidence | Remaining work |
|---|---|---|---|
| ... | In progress | ... | ... |

## Changed files

| File or group | Status | Purpose | Attention needed |
|---|---|---|---|
| ... | Modified | ... | ... |

Group related files when that improves clarity.

## Validation status

| Check | Status | Evidence or command |
|---|---|---|
| Tests | Passed / Failed / Not run / Unknown | ... |
| Type check | ... | ... |
| Lint | ... | ... |
| Build | ... | ... |

Include only relevant checks.

## Blockers and unresolved decisions

### Blocker or decision

- **Evidence:** ...
- **Impact:** ...
- **Needed next:** ...

If none are evident, state:

```txt
No confirmed blockers found.
````

## Recommended next action

**Do next:** ...

**Why this is next:**

* ...
* ...
* ...

**Completion signal:**

* ...

## Files to open first

1. `path/to/file` — reason
2. `path/to/test` — reason
3. `path/to/contract` — reason

## Do not do yet

* ...
* ...

## Confidence and gaps

* **Confidence:** High | Medium | Low
* **Missing context:** ...
* **Assumptions:** ...

## Resume command

Provide a short, paste-ready instruction for the next Codex action:

```txt
Continue the current work on <specific outcome>.

Start by reading:
- <file>
- <file>

Then:
1. <small concrete action>
2. <validation action>

Preserve:
- <important constraint>

Do not:
- <premature or dangerous action>
```

````

## Resume brief length

Prefer:

- 400–900 words for a normal repository
- under 400 words for a small, clear change
- up to 1,500 words for a monorepo or conflicting project state

Do not make the user read a repository biography before they can resume work.

## Confidence rules

Use **high confidence** when:

- repository instructions are clear
- current diff has one coherent purpose
- recent history aligns with planning material
- validation status is known

Use **medium confidence** when:

- the active workstream is likely but not explicitly documented
- some validation evidence is missing
- planning material is stale
- several related tasks overlap

Use **low confidence** when:

- changed files are unrelated
- commit messages are vague
- the repository lacks guidance
- current work appears partially overwritten
- a merge or rebase state is unclear
- available evidence conflicts materially

Do not hide low confidence behind polished prose.

## Quality bar

The task is complete only when:

- Repository instructions were inspected before interpreting the project.
- The current branch and working tree state are reported.
- Uncommitted changes are treated as potentially valuable work.
- The active workstream is described as an outcome.
- Recent history is translated into progress rather than copied as a commit list.
- Planning documents are checked against actual implementation.
- Completed, in-progress, planned, blocked, and unknown work are distinguished.
- Validation claims are supported by evidence.
- The next action is concrete, narrow, and safe.
- Relevant files to open first are identified.
- Premature actions are explicitly flagged.
- Facts, interpretations, and uncertainties are separated.
- No files or repository state were modified.
- No Git write commands were run.
- The result is concise enough to act on immediately.

## Edge cases

### The working tree is clean

Do not conclude that no work is in progress.

Inspect:

- current branch commits
- branch divergence
- roadmap status
- recent handoff notes
- open implementation tasks

A clean tree only means there are no local uncommitted changes.

### The working tree contains many unrelated changes

Group changes into separate workstreams.

Identify:

- likely active task
- unrelated maintenance
- generated files
- unexplained files
- potential accidental changes

Do not recommend committing or discarding them as one unit.

### The repository is in a merge or rebase state

Report the state prominently.

Inspect:

- conflict files
- current operation
- relevant branch history

Do not resolve conflicts automatically.

The recommended next action should focus on understanding or completing the current Git operation safely.

### There are untracked files

Treat them as potentially intentional.

Inspect names and relevant content when safe.

Do not delete, ignore, or classify them as temporary without evidence.

### The branch name conflicts with the changed files

Prefer the actual diff and recent history.

Report the mismatch as a possible stale branch name.

### The roadmap conflicts with the code

Report both states.

Use implementation evidence to describe what exists, while noting that planning documentation may need reconciliation.

Do not silently “correct” either source.

### Tests exist but were not run

Report them as available but not run.

Do not write:

```txt
Tests should pass.
````

### Tests pass but work remains incomplete

Do not classify the task as complete solely because tests pass.

Check:

* documentation
* types
* exports
* examples
* public API compatibility
* remaining TODOs
* acceptance criteria

### Validation commands may modify files

Do not run them automatically.

Report:

* the command
* likely generated output
* why execution was skipped

### Dependencies are missing

Do not install them.

Report which validation could not run and why.

### The repository is a monorepo

Identify:

* affected workspace
* package-local instructions
* package-local scripts
* cross-package dependencies
* whether changed public contracts affect other packages

Avoid scanning every workspace unless the changes cross boundaries.

### No Git history is available

Use:

* current files
* planning documents
* changelog
* modification context
* handoff notes

Lower confidence and state that recent progression cannot be reconstructed.

### No planning documents exist

Infer the active workstream from the current diff and history.

Mark the interpretation clearly.

Recommend creating a handoff checkpoint later, but do not create one during this read-only task.

### The latest commit is a broad formatting change

Look beyond it for the last meaningful functional changes.

Do not treat formatting churn as the primary project workstream.

### The repository appears complete

Identify the latest confirmed state and whether any validation or release tasks remain.

Do not invent a next feature.

The recommended next action may be:

```txt
Confirm there is no pending work before starting a new workstream.
```

### The project contains sensitive configuration

Do not expose:

* secrets
* tokens
* private keys
* credentials
* private endpoint details
* personal data

Report only that sensitive local configuration exists when relevant.

## Related skills

* `workday-shutdown` — creates a structured end-of-session checkpoint for later recovery.
* `interruption-recovery` — records the exact state of unfinished work during an unexpected stop.
* `next-best-action` — compares several valid tasks and selects the most valuable next task.
* `decision-log-writer` — records architectural or product decisions that must survive across sessions.
* `context-handoff-builder` — creates a handoff for another developer, agent, or team.
* `repo-health-daily-check` — performs a wider repository health inspection after context is recovered.

