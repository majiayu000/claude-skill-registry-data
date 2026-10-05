---
name: code-forge
description: >
  Complete Codex development workflow for turning requirements, feature docs, or
  prompts into working code. Use when the user asks to plan implementation work,
  execute tasks, enforce TDD, review source code, fix bugs, debug failures, verify
  completion, manage worktrees or branch finishing, dispatch parallel agents,
  port a project to another language, check progress, or run an end-to-end build
  flow. Supports complex orchestration across plan -> impl -> review -> fix ->
  verify, plus build, forge smart dispatch, worktree, finish, parallel, port,
  tdd, debug, and status workflows.
  Every workflow here operates on CODE. Do NOT use this suite to review, audit, or
  write documents and prose (PRD, SRS, tech design, feature spec, README, papers) —
  a request like "review this doc" / "review 文档" belongs to spec-forge or
  theory-forge, not to code-forge.
version: 1.0
subcommands:
  - build
  - forge
  - plan
  - impl
  - status
  - review
  - fix
  - debug
  - tdd
  - verify
  - worktree
  - finish
  - parallel
  - port
---

# Code Forge Orchestrator

Code Forge is a development execution workflow suite. This root skill is the
Codex-facing orchestrator: decide which child skill or command workflow to load,
preserve the planning/execution contract, and avoid loading large references
until they are needed.

## Trigger Patterns

Use this skill when the user asks for any of the following:

- End-to-end implementation from spec or prompt: use `commands/build.md`
- Smart natural-language dispatch to a code-forge workflow: use `commands/forge.md`
- Generate an implementation plan from docs, a directory, or a prompt: use `skills/plan/SKILL.md`
- Execute pending feature tasks or resume work: use `skills/impl/SKILL.md`
- Check feature or project progress: use `skills/status/SKILL.md`
- Review **source code** quality, handle code feedback, or post a GitHub PR review: use `skills/review/SKILL.md`
- Debug and fix **code defects** with upstream trace-back: use `skills/fix/SKILL.md`
- Investigate root cause for untracked bugs or failures: use `skills/debug/SKILL.md`
- Enforce Red-Green-Refactor for ad-hoc implementation: use `skills/tdd/SKILL.md`
- Verify work before claiming done, when a command can settle it: use `skills/verify/SKILL.md`
- Create isolated git worktrees: use `skills/worktree/SKILL.md`
- Merge, PR, keep, or discard completed branch work: use `skills/finish/SKILL.md`
- Dispatch independent problems to parallel agents: use `skills/parallel/SKILL.md`
- Port a documentation-driven project to a new language: use `skills/port/SKILL.md`

Also treat slash-like requests as aliases:

| User request | Route |
|---|---|
| `/code-forge:build ...` or `/build ...` | Build |
| `/code-forge:forge ...` or `/forge ...` | Smart dispatch |
| `/code-forge:plan ...` or `/plan ...` | Plan |
| `/code-forge:impl ...` or `/impl ...` | Impl |
| `/code-forge:status ...` or `/status ...` | Status |
| `/code-forge:review ...` or `/review ...` | Review |
| `/code-forge:fix ...` or `/fix ...` | Fix |
| `/code-forge:debug ...` or `/debug ...` | Debug |
| `/code-forge:tdd ...` or `/tdd ...` | TDD |
| `/code-forge:verify` or `/verify` | Verify |
| `/code-forge:worktree ...` or `/worktree ...` | Worktree |
| `/code-forge:finish` or `/finish` | Finish |
| `/code-forge:parallel` or `/parallel` | Parallel |
| `/code-forge:port ...` or `/port ...` | Port |

## Do Not Trigger On

Code Forge acts on code. A request whose target is a **document** is out of scope, even
when it uses a code-forge verb such as "review", "fix", "plan", or "verify":

| Request | Route |
|---|---|
| Review / audit a PRD, SRS, tech design, feature spec | `spec-forge:review`, `spec-forge:audit` |
| Review project docs, README, guides, changelog | `spec-forge:audit` or plain reading |
| Review a theory or academic paper | `theory-forge:*` |
| Write or revise a spec/PRD/design doc | `spec-forge:*` |
| Fix wording, typos, or content inside a document | `spec-forge:*` or a plain edit |
| Verify a fact, a statement, or that a document is accurate | check the source directly |
| Review a plan, proposal, or notes as prose | plain reading — no skill needed |

The trigger is the **object** of the request, not the verb. "Review the auth module" is
code-forge; "review 文档" / "review this design doc" is not. Same for "fix" (a code defect,
not a typo in a spec) and "verify" (something a command can settle, not whether a sentence
is true). When the object is ambiguous, ask one question instead of assuming code.

Weight also matters: `fix` runs a full root-cause + TDD + doc-sync cycle, so a trivial
mechanical edit (rename, format, constant bump) should be made directly rather than routed
here.

The `commands/*.md` files are compatibility command definitions from the
Claude-oriented implementation. In Codex, prefer reading the child
`skills/*/SKILL.md` files directly for single-skill routes. Use `commands/build.md`
and `commands/forge.md` because those are orchestrator workflows, not child skill
directories.

## Progressive Loading

Keep context small.

1. Read this root file first.
2. Read only the child `SKILL.md` or `commands/*.md` file matching the user's request.
3. When a child skill references `skills/shared/execution-entrypoint.md`, read it before acting.
4. Read `skills/shared/configuration.md` when the workflow needs `.code-forge.json` or output/input directory resolution.
5. Read `skills/shared/project-analysis.md` when the workflow needs codebase awareness.
6. Read `skills/shared/design-first.md` before code-writing workflows that must avoid patch-first implementation.
7. Read `skills/shared/multi-repo.md` only when `--repos` or multi-repo work is requested.

The `skills/shared/scripts/` layer (Python 3, stdlib only) absorbs deterministic
bookkeeping so it does not cost tokens or risk hand-merge errors: `cf-config.py`
(config resolution), `cf-state.py` (state.json read/mutate), `cf-status.py`
(dashboard rendering), `cf-verify-plan.py` (plan structure validation), and
`cf-scan.py` (project facts collection). The skills that use them invoke them on
a fast path and keep a manual fallback. See `skills/shared/scripts/README.md`.

Do not bulk-load every child skill. Do not read all shared references just because
the suite is complex.

## Global Rules

- Preserve the user's requested language for user-facing responses.
- Prefer existing project conventions, test frameworks, architecture, and helper APIs.
- Never claim work is done without fresh verification evidence. Use `skills/verify/SKILL.md`.
- Code changes must be design-first and test-disciplined. For ad-hoc work, use `skills/tdd/SKILL.md`.
- For bugs, investigate root cause before fixing. Use `fix` for code-forge tracked features and `debug` for untracked problems.
- Avoid bloat: modify existing abstractions when appropriate instead of adding wrappers, duplicate modules, or parallel implementations.
- Respect dirty worktrees. Do not revert user changes unless explicitly asked.
- Keep code-forge outputs in the configured output directory, default `planning/`, unless `--tmp` or config says otherwise.
- Preserve planning state files and task names because downstream `impl`, `status`, `review`, and `fix` depend on them.
- Ask only necessary questions. If config, docs, state files, or code provide the answer, use them and state the assumption.

## Shared References

Use these references only when relevant:

- `skills/shared/execution-entrypoint.md`: common execution start rules.
- `skills/shared/configuration.md`: `.code-forge.json`, directory hierarchy, and defaults.
- `skills/shared/project-analysis.md`: project scan protocol for codebase-aware workflows.
- `skills/shared/design-first.md`: anti-bloat design discipline before implementation.
- `skills/shared/coding-standards.md`: implementation standards.
- `skills/shared/overview-generation.md`: generated overview structure.
- `skills/shared/multi-repo.md`: multi-repo orchestration.
- `skills/shared/scripts/`: deterministic Python helpers (config, state, status) with a README and per-skill fast-path/fallback wiring.

## Main Workflows

### Build

Read `commands/build.md`.

Use when the user wants an end-to-end pipeline from a feature spec, tech design,
feature name, or plain prompt to working code. The build flow orchestrates:

`requirement understanding -> test cases -> plan -> impl -> review -> verify`

Confirm before moving between major stages when the command workflow requires it.

### Forge Smart Dispatch

Read `commands/forge.md`.

Use when the user gives a natural-language code-forge request and expects routing.
Classify intent, print one routing line, then load the selected skill.

### Plan

Read `skills/plan/SKILL.md`.

Use for turning a spec, feature doc, directory selection, or prompt into a
multi-file implementation plan. Mandatory outputs are:

- `{output_dir}/{feature}/overview.md`
- `{output_dir}/{feature}/plan.md`
- `{output_dir}/{feature}/tasks/*.md`
- `{output_dir}/{feature}/state.json`
- project-level `{output_dir}/overview.md`

Default `output_dir` is `planning/`, unless configuration or `--tmp` changes it.

### Impl

Read `skills/impl/SKILL.md`.

Use for executing pending tasks from a code-forge plan. It depends on `state.json`
and `tasks/*.md`. It supports resume and `--repos` multi-repo execution.

### Status

Read `skills/status/SKILL.md`.

Use for dashboards, progress checks, "what's left", or feature detail.

### Review

Read `skills/review/SKILL.md`.

Use for feature review, project review, feedback response, or GitHub PR review.
Respect review modes such as `--project`, `--feedback`, `--github-pr`, and `--save`.

### Fix

Read `skills/fix/SKILL.md`.

Use for bugs, review batch-fixes, and code-forge tracked issues. It traces root
cause across code, task, plan, and requirements, then applies a TDD fix and syncs
upstream documents where needed.

### Debug

Read `skills/debug/SKILL.md`.

Use for untracked bugs, failures, and root-cause questions. It requires
investigation before fixes.

### TDD

Read `skills/tdd/SKILL.md`.

Use for ad-hoc implementation or implementing test cases outside `impl`. Honor
driven mode from `@test-cases.md`, auto-analysis mode, and standalone mode.

### Verify

Read `skills/verify/SKILL.md`.

Use before claiming completion, fixed status, passing tests, or build success.

### Worktree

Read `skills/worktree/SKILL.md`.

Use when starting feature or hotfix work in an isolated git worktree. Verify the
worktree directory is git-ignored when project-local.

### Finish

Read `skills/finish/SKILL.md`.

Use when branch work is complete and the user wants to merge, create a PR, keep,
or discard the branch/worktree.

### Parallel

Read `skills/parallel/SKILL.md`.

Use only for independent problems that can safely run concurrently. If problems
share files, state, or dependencies, run sequentially.

### Port

Read `skills/port/SKILL.md`.

Use for cross-language or multi-language project ports from documentation and/or
a reference implementation.

## Output Locations

Default locations:

- Configuration: `.code-forge.json`
- Plans: `planning/{feature}/`
- Temporary plans: `.code-forge/tmp/{feature}/`
- Feature overview: `planning/{feature}/overview.md`
- Feature plan: `planning/{feature}/plan.md`
- Tasks: `planning/{feature}/tasks/*.md`
- State: `planning/{feature}/state.json`
- Project overview: `planning/overview.md`
- Worktrees: `.worktrees/{feature}/` or configured/global worktree directory

If `.code-forge.json` changes these directories, follow the configuration and
state the location used.

## Completion Criteria

Before finishing a code-forge task:

- Confirm the requested plan, code change, report, status, or branch action was completed, or explain the blocker.
- Mention the exact files changed or generated.
- For code changes, report the verification command and result.
- For plan/status workflows, report the planning directory and next executable action.
- For review/fix/debug workflows, summarize findings or root cause with concrete file references.
- For build workflows, summarize which stages completed and which stage is next or blocked.
