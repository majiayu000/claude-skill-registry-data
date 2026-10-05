---
name: speckit-archive-run
description: Archive merged feature specs into project memory with provenance, sweep
  discovery, and gated cleanup
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: archive:commands/archive.md
---

Act as the **Chief Software Architect**, **Documentation Maintainer**, and
**release provenance auditor**.

Your goal is to archive merged feature specifications into durable project
memory while preserving enough provenance to recover raw spec artifacts from git
later. This command also supports Archive Sweep mode, which identifies
previously merged feature specs before a new SpecKit run starts.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding.

## Input Parsing

Parse `$ARGUMENTS` as shell-like tokens. Supported forms:

```text
speckit.archive.run specs/###-feature-name [scope] [provenance] [mode]
speckit.archive.run --sweep --current-target specs/###-current-feature [provenance] [mode]
```

### Positional Input

- First non-option token: feature spec directory path, for example
  `specs/007-invoice-settings`.
- In `--sweep` mode, no positional feature directory is required.

### Scope Modifiers

If none are provided, update all archival artifacts.

- `--spec-only`: update only `.specify/memory/spec.md`
- `--plan-only`: update only `.specify/memory/plan.md`
- `--changelog-only`: update only `.specify/memory/changelog.md`
- `--agent-only`: update only the agent knowledge file
  (`GEMINI.md`, `AGENTS.md`, or `CLAUDE.md`)

### Mode And Safety Options

- `--dry-run`: do not modify files; produce the same eligibility, provenance,
  and cleanup report that an apply run would use.
- `--apply`: apply memory archival edits. This is the default for a single
  feature archive unless `--dry-run` is present.
- `--sweep`: discover previously merged feature specs and report archive and
  cleanup eligibility before any new spec work begins.
- `--apply-cleanup`: after successful archival, remove or move completed spec
  folders out of active `specs/**` only if every cleanup gate passes.
- `--current-target <path>`: active feature spec for the current run. Archive
  Sweep MUST exclude this path from archival and cleanup.

### Provenance Options

Capture these in the archival report when provided:

- `--pr-url <url>`
- `--merge-sha <sha>`
- `--tree-sha <sha>`
- `--ci-url <url>`
- `--argos-url <url>`
- `--metadata-gate <name=pass|fail|warning>`
- `--artifact-manifest <path-or-url>`

If `$ARGUMENTS` is empty, output:

```text
ERROR: No feature spec directory or --sweep mode provided.
Usage: /speckit.archive.run specs/###-feature-name [--dry-run] [--apply-cleanup]
   or: /speckit.archive.run --sweep --current-target specs/###-current-feature --dry-run
```

Then stop without modifying files.

## Mandatory Safety Model

This command MUST NOT create a spec graveyard and MUST NOT destroy provenance.

### Cleanup Is Gated

Never delete, move, or otherwise remove active `specs/**` content unless all of
these are true:

1. The user explicitly supplied `--apply-cleanup`.
2. The target is not the `--current-target`.
3. The feature was already merged, with a recorded PR URL and merge commit or
   tree reference.
4. The archive operation completed successfully in this run or an explicit
   prior archive success record was supplied.
5. The report includes recovery commands for each raw artifact, including:
   `git show <merge-sha>:specs/<feature>/spec.md`
6. The worktree is clean before cleanup begins.
7. The active branch is a safe base branch for this repository, normally
   `main`, unless the project constitution explicitly names another cleanup
   branch.
8. The command will not rewrite git history and will not rely on post-merge CI
   mutating `main`.

If any cleanup gate fails, set `safeToApplyCleanup=false`, set
`dryRunProvenanceOnly=true`, do not remove source files, and explain the failed
gate in the report.

### Current Target Exclusion

Archive Sweep MUST exclude `--current-target` from archival and cleanup in the
same run. If a target path equals the current target, report it under
`excludedCurrentSpec` and take no action against it.

### Screenshot And Artifact Policy

Generated screenshots are review artifacts, not default durable archive
payload. Preserve Argos/CI provenance, artifact manifest links, hashes,
retention classification, redaction status, and expiration risk when available.
Do not require large generated screenshots to be committed into the archive.

## Step 0: Setup And Validation

### 0.1 Resolve Paths

Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` to identify repository paths. This script is mandatory for path
discovery when available. If the script is missing, stop and explain the missing
script unless the user explicitly supplied enough absolute paths to proceed.

Derive absolute paths for:

- `REPO_ROOT`
- `FEATURE_DIR` when not in `--sweep` mode
- `MEMORY_DIR` (`REPO_ROOT / .specify/memory`)
- `TEMPLATES_DIR` (`REPO_ROOT / .specify/templates`)

Feature specs live in `specs/{###-feature-name}/` at repo root. Use absolute
paths in all reports.

### 0.2 Validate Worktree Safety

Record:

- current branch
- `git status --short`
- whether the worktree is clean
- configured remotes
- whether the run is `--dry-run`, `--apply`, or `--apply-cleanup`

This evidence is required even when no cleanup is attempted.

### 0.3 Validate Feature Directory

For a single feature archive, verify `FEATURE_DIR` exists and contains:

- `spec.md` (required)
- `plan.md` (required)

If required files are missing, output a clear error and stop without modifying
files.

### 0.4 Inventory Optional Artifacts

Note whether these exist:

- `tasks.md`
- `research.md`
- `data-model.md`
- non-empty `contracts/`
- non-empty `checklists/`
- `quickstart.md`

### 0.5 Validate Or Bootstrap Memory Directory

If applying archival edits and `.specify/memory` does not exist, create it. If
memory files are missing, bootstrap them from templates when possible. In
`--dry-run`, report what would be bootstrapped without creating files.

### 0.6 Load Constitution

Read `.specify/memory/constitution.md` when present. Constitution MUST rules are
non-negotiable. Any archival content that conflicts with the constitution is a
CRITICAL blocker and must not be merged silently.

### 0.7 Check Extension Hooks

Read `REPO_ROOT/.specify/extensions.yml` when present. For
`hooks.before_archive` and `hooks.after_archive`, list executable enabled hooks.
Do not evaluate non-empty hook conditions; skip conditional hooks and report
that they were skipped.

## Step 1: Archive Sweep Discovery

Run this step when `--sweep` is present. Also run it before a single-feature
archive if the command is being used as a pre-autopilot cleanup pass.

1. Enumerate `specs/*` feature directories.
2. Exclude `--current-target` exactly.
3. Identify completed or merged specs using available local and remote evidence:
   - merged PR URL or PR number
   - merge commit
   - branch deleted/merged marker
   - project memory changelog entry
   - explicit user-provided provenance options
4. For each eligible spec, classify:
   - `eligibleForArchive`
   - `archiveAlreadyRecorded`
   - `eligibleForCleanup`
   - `safeToApplyCleanup`
   - `dryRunProvenanceOnly`
5. Never mutate files in sweep mode unless `--apply` or `--apply-cleanup` is
   explicitly supplied and all gates pass.

If a spec cannot be proven merged, keep it in active specs and report the
missing evidence.

## Step 2: Feature Analysis

For each feature being archived, read and extract:

From `spec.md`:

- user stories and acceptance criteria
- functional requirements
- non-functional requirements
- key entities
- edge cases
- success criteria

From `plan.md`:

- dependencies and versions
- modules/services created
- architecture changes
- configuration changes
- branch name or source metadata
- test strategy

From optional artifacts:

- `data-model.md`: models, relationships, validation rules
- `research.md`: decisions, trade-offs, known issues
- `tasks.md`: completed and total task counts
- `contracts/`: API/CLI contracts
- `checklists/`: quality gates and remaining gaps

## Step 3: Conflict Detection And Gap Analysis

Before merging, check:

- constitution conflicts (CRITICAL)
- requirement ID collisions
- entity redefinitions
- dependency conflicts
- missing implementation evidence
- missing CI/Argos provenance
- missing metadata gate outcomes
- missing recovery commands

If conflicts or gaps exist, list them with recommended resolution. CRITICAL
constitution conflicts block archival edits.

## Step 4: Clarify Once If Needed

Ask at most five questions only when human judgment materially changes scope or
correctness. Skip this step if defaults are clear. Do not ask questions for
basic safety gates; apply the mandatory safety model instead.

## Step 5: Impact Map

Before applying edits, produce an impact map:

```markdown
### Impact Map
| Artifact | Sections Affected | Change Type |
|----------|------------------|-------------|
| `.specify/memory/spec.md` | User Stories, FRs, Entities | Append/Update |
| `.specify/memory/plan.md` | Dependencies, Structure, Testing | Append/Update |
| `.specify/memory/changelog.md` | Merged Features Log | Append |
| `AGENTS.md` | Recent Changes, Gotchas | Append/Update |
| `specs/###-feature-name` | Cleanup Eligibility | Report/Remove only if gated |
```

In `--dry-run`, stop after producing the impact map and archival report unless
the user explicitly asked for a full simulated report.

## Step 6: Archival Edits

Apply edits only when not in `--dry-run`.

### Edit Rules

- Preserve existing document structure and ordering.
- Prefer append/update over restructuring.
- Add `[Source: specs/###-feature-name]` traceability tags.
- Add a revision note with date and reason to each modified artifact.
- Continue the existing requirement ID convention; never reuse or renumber IDs.
- Do not merge content that violates the constitution.

### 6.1 Main Specification

Update `.specify/memory/spec.md` with user stories, requirements, entities,
edge cases, data flow, and success criteria.

### 6.2 Main Plan

Update `.specify/memory/plan.md` with dependencies, project structure,
configuration, routing, and testing strategy. Remove completed items from
future-work sections only when the implementation evidence proves completion.

### 6.3 Agent Knowledge

Update the first existing agent file in this order: `GEMINI.md`, `AGENTS.md`,
`CLAUDE.md`. Record active technologies, project structure, commands, recent
changes, and gotchas extracted from `research.md`.

### 6.4 Changelog

Create or update `.specify/memory/changelog.md` with:

- feature name
- branch
- spec path
- PR URL
- merge commit or tree reference
- CI URL
- Argos URL
- task completion count
- summary of added behavior

### 6.5 Feature Status

In the feature's own `spec.md` and `plan.md`, change `**Status**: Draft` to
`**Status**: Completed` only when archival edits succeeded. Do not change other
status values.

## Step 7: Cleanup Gate

If `--apply-cleanup` is absent, report cleanup recommendations only.

If `--apply-cleanup` is present and every cleanup gate passes:

1. Record recovery commands for raw artifacts.
2. Record archive success and provenance.
3. Remove or move the completed feature directory out of active `specs/**`
   according to project policy.
4. Record the exact cleanup command that was run.

If any gate fails, do not remove files. Report `safeToApplyCleanup=false`.

## Step 8: Archival Report

Output a structured report with absolute paths:

```markdown
# Archival Report

## Mode
- archiveMode: single-feature | sweep
- dryRun: true | false
- applyCleanupRequested: true | false
- dryRunProvenanceOnly: true | false
- safeToApplyCleanup: true | false

## Sweep Summary
| Spec | Eligibility | Cleanup Mode | Reason |
|------|-------------|--------------|--------|

## Excluded Current Spec
`specs/###-current-feature` or `None`

## Provenance
- Source spec path:
- PR URL:
- Merge commit:
- Tree reference:
- CI run URL:
- Argos build/review URL:
- Metadata gates:
- Artifact manifest:
- Screenshot retention:
- Expiration risk:

## Recovery Commands
```text
git show <merge-sha>:specs/<feature>/spec.md
git show <merge-sha>:specs/<feature>/plan.md
git show <merge-sha>:specs/<feature>/tasks.md
```

## Changed Files
| File | Change Summary |
|------|----------------|

## Feature Status

## Constitution Compliance

## Conflicts Resolved

## Outstanding Items

## Cleanup Decision
- cleanupApplied: true | false
- cleanupCommand:
- blockedBy:

## Defaults Applied

## Scoping
```

## Done Criteria

- Feature content is merged into project memory or reported as dry-run only.
- Constitution compliance is verified.
- Archive Sweep excludes the current target.
- Previously merged specs are classified with archive and cleanup eligibility.
- Report includes PR, merge/tree, CI, Argos, metadata gate, artifact manifest,
  and screenshot retention provenance when available.
- Recovery commands are printed for raw spec artifact recovery.
- Cleanup is applied only when every gate passes.
- No git history is rewritten.
- No post-merge CI mutation of `main` is required.
- Source feature spec files are not deleted unless `--apply-cleanup` was
  explicitly requested and safe.