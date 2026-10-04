---
name: speckit-analyze
description: Portfolio-wide audit mode for /speckit-analyze across worktrees
argument-hint: "Optional focus areas for analysis"
compatibility: Requires spec-kit project structure with .specify/ directory
metadata:
  author: github-spec-kit
  source: preset:portfolio-audit
user-invocable: true
disable-model-invocation: false
---

# Speckit Analyze Skill

## Preset Routing (runs BEFORE the stock command body)

This preset is *prepended* to the core `/speckit-analyze` command. Evaluate the routing rules below first; only fall through to the stock command body when neither portfolio mode nor the worktree fallback applies.

### Mode A — Portfolio Audit

**Trigger** — activate portfolio mode if **either** is true:

1. `$ARGUMENTS` contains the token `portfolio` (case-insensitive), or
2. The current branch is **not** a feature branch (e.g. user invoked `/speckit-analyze` from `main`). Detect this by running `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` from repo root: if it errors with "Not on a feature branch" (or equivalent), do **not** abort — switch to this mode instead.

When portfolio mode is active, **skip the entire stock command body** (Steps 1–8 of the per-feature flow) and execute the audit below. The `before_analyze` and `after_analyze` extension-hook scans defined by the stock command still run, bracketing this audit.

#### Portfolio Audit — Behavior (strictly read-only)

1. **Enumerate worktrees.** Run `git worktree list --porcelain` from the primary checkout. Record `(path, branch, head)` for each entry. Treat `<repo>.worktrees/<slug>/` as the canonical worktree layout (per project memory `feedback_worktree_location.md`); also include any worktree paths the user has manually created elsewhere.
2. **Enumerate spec slugs across all worktrees.**
   - For each worktree path, list `specs/*/` excluding the literal `archive` directory.
   - Union by slug (the directory name). A slug may legitimately appear in multiple worktrees; record every location.
3. **Locate the most complete copy of each spec.** For each `(slug, location)`:
   - Check for `spec.md`, `plan.md`, `tasks.md`, `.specify/feature.json`.
   - Prefer the copy in the worktree whose branch name matches the slug; otherwise compute the union of present artifacts across all locations.
   - Record which artifacts are missing and where each present artifact lives.
4. **Enumerate GitHub issues — open AND closed.**
   - Run `gh issue list --state all --limit 300 --json number,title,labels,state`.
   - Closed issues are intentionally included so cleanup gaps are visible.
5. **Match issues → specs**, in priority order:
   1. `source_issue` field in the worktree's `.specify/feature.json` (most authoritative). The file is gitignored per-worktree state, so it is present only in a live worktree for that slug — never under `specs/<slug>/`.
   2. `Closes #N`, `Fixes #N`, or bare `#N` references inside `spec.md` or `plan.md`.
   3. Fuzzy title match as a last resort — flag as **loose** in the report so the user can backfill metadata.
6. **Detect orphans and dead artifacts.**
   - Spec directories containing `tasks.md` but no `spec.md` (e.g. abandoned scaffolds).
   - Worktree branches with no matching `specs/<slug>/` directory anywhere (dead branches).
   - Duplicate spec directories across multiple worktrees.

#### Portfolio Audit — Report (no file writes)

Emit the following Markdown report. Do not write it to disk.

##### Portfolio Audit Report

**Table A — Open issues without any spec**

| Issue | Title | Labels |

**Table B — Closed issues without any spec**

| Issue | Title |

(These are likely missed cleanup.)

**Table C — Specs missing `plan.md` or `tasks.md`**

| Spec slug | Location(s) | spec.md | plan.md | tasks.md |

(Location is the worktree path containing the most complete copy; mark `Y`/`N` for each artifact.)

**Table D — Orphaned / dead artifacts**

| Item | Kind | Notes |

Kinds include: `tasks-only-scaffold`, `dead-worktree-branch`, `duplicate-worktree-copy`.

**Table E — Loose issue↔spec matches**

| Issue | Matched spec | Match reason |

(Matches found only by fuzzy title — add `Closes #N` to `spec.md` to firm these up; `feature.json` is gitignored and cannot be backfilled durably.)

**Metrics**

- Total open issues
- Total closed issues
- Total spec slugs
- Issues without any spec (open + closed)
- Specs missing plan or tasks
- Orphaned / dead artifacts
- Loose matches

#### Portfolio Audit — Next Actions

Suggest concrete follow-ups per table:

- Table A → `/speckit-specify --issue <n>` (or in-worktree if the branch already exists).
- Table B → reopen the issue or create the missing spec if the closure was premature.
- Table C → `/speckit-plan` or `/speckit-tasks` inside the worktree that contains the most complete copy.
- Table D → investigate dead worktree branches manually (`git worktree remove`) or clean up duplicate/stale worktree copies.
- Table E → add `Closes #N` to `spec.md`/`plan.md` (the durable home; `feature.json` is gitignored per-worktree state).

After emitting the report, ask the user: **"Want me to drill into any of these (e.g. start a `/speckit-specify` for an unspec'd issue)?"** Do not apply any changes automatically.

### Mode B — Per-Feature Worktree Fallback (modifies stock Step 1)

If portfolio mode did **not** activate but the prerequisite check is on a feature branch and one or more of `spec.md`/`plan.md`/`tasks.md` is missing in the current checkout, attempt the fallback below **before** aborting:

1. Look up the matching worktree at `<repo>.worktrees/<slug>/specs/<slug>/` (where `<slug>` is the current feature branch).
2. For each artifact missing locally, use the worktree copy if it exists. **Use it even if the worktree copy is stale relative to the current checkout** (e.g. older HEAD).
3. If the worktree copy is older than the local copy of any sibling artifact (compare `git log -1 --format=%ct` of the file paths), record a finding `WORKTREE-STALE` with severity **MEDIUM** in Section 4 of the stock report. The analysis still proceeds.
4. If no worktree copy exists either, fall back to the stock command's abort behavior with the original error message.

This fallback is a pure extension of Step 1 of the stock command. All other stock steps (Load Artifacts → Build Semantic Models → Detection Passes → Severity Assignment → Report → Next Actions → Offer Remediation) run unchanged using whichever artifact paths the fallback resolved.

### Mode C — Stock Per-Feature Analysis (no preset behavior)

If portfolio mode is not active AND no worktree fallback was needed (all artifacts present locally), continue with the stock `/speckit-analyze` command body below as-is.

---


## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Pre-Execution Checks

**Check for extension hooks (before analysis)**:
- Check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.before_analyze` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`). For example, `speckit.git.commit` → `/speckit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Pre-Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Pre-Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}

    Wait for the result of the hook command before proceeding to the Goal.
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This command MUST run only after `/speckit-tasks` has successfully produced a complete `tasks.md`.

## Operating Constraints

**STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up editing commands would be invoked manually).

**Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle. If a principle itself needs to change, that must occur in a separate, explicit constitution update outside `/speckit-analyze`.

## Execution Steps

### 1. Initialize Analysis Context

Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` once from repo root and parse JSON for FEATURE_DIR and AVAILABLE_DOCS. Derive absolute paths:

- SPEC = FEATURE_DIR/spec.md
- PLAN = FEATURE_DIR/plan.md
- TASKS = FEATURE_DIR/tasks.md

Abort with an error message if any required file is missing (instruct the user to run missing prerequisite command).
For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From spec.md:**

- Overview/Context
- Functional Requirements
- Success Criteria (measurable outcomes — e.g., performance, security, availability, user success, business impact)
- User Stories
- Edge Cases (if present)

**From plan.md:**

- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From tasks.md:**

- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**

- Load `.specify/memory/constitution.md` for principle validation

### 3. Build Semantic Models

Create internal representations (do not include raw artifacts in output):

- **Requirements inventory**: For each Functional Requirement (FR-###) and Success Criterion (SC-###), record a stable key. Use the explicit FR-/SC- identifier as the primary key when present, and optionally also derive an imperative-phrase slug for readability (e.g., "User can upload file" → `user-can-upload-file`). Include only Success Criteria items that require buildable work (e.g., load-testing infrastructure, security audit tooling), and exclude post-launch outcome metrics and business KPIs (e.g., "Reduce support tickets by 50%").
- **User story/action inventory**: Discrete user actions with acceptance criteria
- **Task coverage mapping**: Map each task to one or more requirements or stories (inference by keyword / explicit reference patterns like IDs or key phrases)
- **Constitution rule set**: Extract principle names and MUST/SHOULD normative statements

### 4. Detection Passes (Token-Efficient Analysis)

Focus on high-signal findings. Limit to 50 findings total; aggregate remainder in overflow summary.

#### A. Duplication Detection

- Identify near-duplicate requirements
- Mark lower-quality phrasing for consolidation

#### B. Ambiguity Detection

- Flag vague adjectives (fast, scalable, secure, intuitive, robust) lacking measurable criteria
- Flag unresolved placeholders (TODO, TKTK, ???, `<placeholder>`, etc.)

#### C. Underspecification

- Requirements with verbs but missing object or measurable outcome
- User stories missing acceptance criteria alignment
- Tasks referencing files or components not defined in spec/plan

#### D. Constitution Alignment

- Any requirement or plan element conflicting with a MUST principle
- Missing mandated sections or quality gates from constitution

#### E. Coverage Gaps

- Requirements with zero associated tasks
- Tasks with no mapped requirement/story
- Success Criteria requiring buildable work (performance, security, availability) not reflected in tasks

#### F. Inconsistency

- Terminology drift (same concept named differently across files)
- Data entities referenced in plan but absent in spec (or vice versa)
- Task ordering contradictions (e.g., integration tasks before foundational setup tasks without dependency note)
- Conflicting requirements (e.g., one requires Next.js while other specifies Vue)

### 5. Severity Assignment

Use this heuristic to prioritize findings:

- **CRITICAL**: Violates constitution MUST, missing core spec artifact, or requirement with zero coverage that blocks baseline functionality
- **HIGH**: Duplicate or conflicting requirement, ambiguous security/performance attribute, untestable acceptance criterion
- **MEDIUM**: Terminology drift, missing non-functional task coverage, underspecified edge case
- **LOW**: Style/wording improvements, minor redundancy not affecting execution order

### 6. Produce Compact Analysis Report

Output a Markdown report (no file writes) with the following structure:

## Specification Analysis Report

| ID | Category | Severity | Location(s) | Summary | Recommendation |
|----|----------|----------|-------------|---------|----------------|
| A1 | Duplication | HIGH | spec.md:L120-134 | Two similar requirements ... | Merge phrasing; keep clearer version |

(Add one row per finding; generate stable IDs prefixed by category initial.)

**Coverage Summary Table:**

| Requirement Key | Has Task? | Task IDs | Notes |
|-----------------|-----------|----------|-------|

**Constitution Alignment Issues:** (if any)

**Unmapped Tasks:** (if any)

**Metrics:**

- Total Requirements
- Total Tasks
- Coverage % (requirements with >=1 task)
- Ambiguity Count
- Duplication Count
- Critical Issues Count

### 7. Provide Next Actions

At end of report, output a concise Next Actions block:

- If CRITICAL issues exist: Recommend resolving before `/speckit-implement`
- If only LOW/MEDIUM: User may proceed, but provide improvement suggestions
- Provide explicit command suggestions: e.g., "Run /speckit-specify with refinement", "Run /speckit-plan to adjust architecture", "Manually edit tasks.md to add coverage for 'performance-metrics'"

### 8. Offer Remediation

Ask the user: "Would you like me to suggest concrete remediation edits for the top N issues?" (Do NOT apply them automatically.)

### 9. Check for extension hooks

After reporting, check if `.specify/extensions.yml` exists in the project root.
- If it exists, read it and look for entries under the `hooks.after_analyze` key
- If the YAML cannot be parsed or is invalid, skip hook checking silently and continue normally
- Filter out hooks where `enabled` is explicitly `false`. Treat hooks without an `enabled` field as enabled by default.
- For each remaining hook, do **not** attempt to interpret or evaluate hook `condition` expressions:
  - If the hook has no `condition` field, or it is null/empty, treat the hook as executable
  - If the hook defines a non-empty `condition`, skip the hook and leave condition evaluation to the HookExecutor implementation
- When constructing command invocations from hook command names, replace dots (`.`) with hyphens (`-`). For example, `speckit.git.commit` → `/speckit-git-commit`.
- For each executable hook, output the following based on its `optional` flag:
  - **Optional hook** (`optional: true`):
    ```
    ## Extension Hooks

    **Optional Hook**: {extension}
    Command: `/{command}`
    Description: {description}

    Prompt: {prompt}
    To execute: `/{command}`
    ```
  - **Mandatory hook** (`optional: false`):
    ```
    ## Extension Hooks

    **Automatic Hook**: {extension}
    Executing: `/{command}`
    EXECUTE_COMMAND: {command}
    ```
    After emitting the block above you MUST actually invoke the hook and wait for it to finish before continuing. Run it the same way you would run the command yourself in this agent/session (the invocation may differ from the literal `{command}` id shown above, e.g. a skills-mode agent runs it as `/skill:speckit-...` or `$speckit-...`). Emitting the block alone does not run the hook.
- If no hooks are registered or `.specify/extensions.yml` does not exist, skip silently

## Operating Principles

### Context Efficiency

- **Minimal high-signal tokens**: Focus on actionable findings, not exhaustive documentation
- **Progressive disclosure**: Load artifacts incrementally; don't dump all content into analysis
- **Token-efficient output**: Limit findings table to 50 rows; summarize overflow
- **Deterministic results**: Rerunning without changes should produce consistent IDs and counts

### Analysis Guidelines

- **NEVER modify files** (this is read-only analysis)
- **NEVER hallucinate missing sections** (if absent, report them accurately)
- **Prioritize constitution violations** (these are always CRITICAL)
- **Use examples over exhaustive rules** (cite specific instances, not generic patterns)
- **Report zero issues gracefully** (emit success report with coverage statistics)

## Context

$ARGUMENTS
