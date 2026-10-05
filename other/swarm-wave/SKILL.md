---
name: swarm-wave
description: "Orchestrate multi-agent development sprints with wave-based parallelism. Use when the user wants to plan a swarm sprint, partition work into file-disjoint waves, map file contention across open issues, run a post-wave quality gate with review agents, manage agent backpressure, run a parallel research wave, or coordinate multiple concurrent agents on a shared codebase. Works with or without beads: sources waves from the beads backlog, from a ROADMAP.md, or from a manually supplied work list. Trigger phrases: 'swarm sprint', 'wave plan', 'launch wave', 'execute wave', 'post-wave gate', 'contention map', 'research wave', 'parallel agents', 'multi-agent sprint', 'agent wave', 'swarm orchestration', 'swarm from ROADMAP', 'wave plan without beads', 'swarm with manual list'."
argument-hint: "[workflow] [wave-number|topic]"
user-invocable: true
paths:
  - "SWARM-*.md"
  - ".beads/**"
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Agent
  - Skill
---

# Swarm Wave

Orchestrate multi-agent development sprints using the swarm wave pattern: group
file-disjoint work into waves, launch parallel task agents per wave, enforce a
blocking quality gate before committing, and track sprint state in `SWARM-NN.md`
files.

File isolation is the primary safety mechanism — agents within a wave each own
distinct files, preventing merge conflicts without relying on worktrees.

This skill does not create beads issues (use `/backlog-groomer`), write
retrospectives (use `/retrospective`), or gate sprint closure (the
`sprint-review` agent handles that). It orchestrates the execution phase
between backlog grooming and sprint close.

## SWARM Files

Sprint state is tracked in `SWARM-NN.md` files in the project root (NN =
sprint number). These are gitignored — they are ephemeral working documents,
not committed artifacts.

Structure:

```markdown
# SWARM-NN — Sprint Theme

Waves: N | Issues: N | Started: YYYY-MM-DD

## Wave 1 — [Theme]

Status: pending | running | gate-pending | gate-passed | committed
Issues: id1, id2, id3

### Agent Assignments

- Agent A: [file1, file2] -> issue-id
- Agent B: [file3] -> issue-id
- Research: [topic]

### Item Status

| Item        | State                              |
| ----------- | ---------------------------------- |
| id1         | pending / claimed / done / carried |
| id2         | pending / claimed / done / carried |

## Wave 2 — [Theme]
...
```

**Item Status is the run-state table.** When beads is available, `bd` is the
source of truth (claim/close) and this table mirrors it for at-a-glance status.
When beads is **unavailable** (ROADMAP or manual source), this table *is* the
source of truth: the orchestrator owns all writes to it — `pending` at plan
time, `claimed` when an agent launches, `done` when the agent reports complete,
`carried` when an item is deferred to a later wave. `Item` is a beads id when
beads is used, otherwise a short slug for the work item.

## Workflows

Determine which workflow the user needs based on their request. If ambiguous,
default to workflow 1 (Plan a swarm sprint) when the user mentions planning or
starting a sprint, workflow 2 (Execute a wave) when a SWARM plan already exists,
and workflow 3 (Post-wave gate) when a wave has completed and needs review.

### 1. Plan a swarm sprint

Plan which issues go in which wave, optimizing for file-disjoint parallelism.

**Steps:**

1. **Determine the work source (Tier A — require-or-fallback).** Beads is
   available iff a `.beads/` directory exists **and** `command -v bd` succeeds;
   this component is **Tier A** per CLAUDE.md `### Beads-availability
   convention`. Select the wave source by precedence — **beads wins when both
   beads and a `ROADMAP.md` exist**:

   - **Beads available** — run `bd ready` and `bd list --status open` to load
     the candidate issue set.
   - **No beads, `ROADMAP.md` present** — interpret it as the work source
     following `references/roadmap-interpretation.md` (read it in its own
     idiom; never reformat it). If that interpretation declines the ROADMAP
     (it is not a parallelizable work plan), fall through to the manual path.
   - **No beads and no usable ROADMAP** — **manual path**: ask the user for the
     work items and their file scopes, reusing the workflow 4 (Map file
     contention) step-1 prompt (item titles + descriptions + the files each
     touches).

   Downstream steps operate on the resulting item list regardless of source.
   Issue creation and `bd` claim/close are beads-only; for a beadless source
   the `SWARM-NN.md` Item Status table is the run-state equivalent (see
   `## SWARM Files`).
2. Read the project structure to understand the codebase layout. Use Glob for
   key source directories and Read for `package.json` and relevant config files.
   This builds the mental model for file contention analysis.
3. Build the file contention map using the procedure from workflow 4 (Map file
   contention). Identify HIGH contention files (3+ issues touching the same
   file). See `references/file-contention-and-clustering.md` for threshold rules.
4. Cluster issues into waves. Apply these rules in order:
   - 4a. Issues sharing HIGH contention files must go into separate waves.
   - 4b. Within a wave, each agent owns 1-3 files; no file appears in more
     than one agent's scope.
   - 4c. P0/P1 issues form earlier waves. P2 fills remaining slots. P3/P4 go
     to later waves. See `references/file-contention-and-clustering.md` for
     priority ordering.
   - 4d. Wave size: 4-6 task agents per wave. Check RAM constraints in
     `references/agent-concurrency-limits.md` and reduce if needed.
   - 4e. Each wave gets one background research agent slot if research
     questions exist for the sprint.
   - 4f. Issues that block other issues (check with `bd blocked`) must go in
     an earlier wave than their dependents.
   - 4g. **Single owner per issue.** When an issue's scope spans files that
     would otherwise be split across multiple agents, assign the whole issue
     to one agent — issue narrative coherence beats wave-level file balance.
     Precedent: RETRO-10 (Sprint 10's `vp-beads-0e9.6`, which spanned skill
     code, `CLAUDE.md`, and `MEMORY.md`). See
     `references/file-contention-and-clustering.md` "Single owner per issue"
     for the trade-off.
5. Draft the wave execution plan in the SWARM file format shown above. Include
   per-agent file ownership and the research topic for each wave.
6. Write the plan to `SWARM-NN.md` in the project root. **Collision detection:**
   pick the next free `SWARM-NN` (glob existing `SWARM-*.md`, including
   `-suffix` variants, and choose the lowest unused number) rather than
   overwriting an active plan; append if deliberately replanning the same
   sprint mid-flight. **If any `SWARM-*.md` is git-tracked, warn the user** —
   these are ephemeral run-state and should be gitignored (a tracked SWARM file
   usually means `.gitignore` is missing the entry).
7. Present the plan to the user. **No wave execution begins without explicit
   approval.** After approval, suggest: "Run `/swarm-wave execute-wave 1` to
   start Wave 1."

**Note:** GitHub-mirrored beads sync via `bd github sync` runs *post-wave* (or
post-sprint), not as part of swarm-wave — the bd v1.0.0 Integration Charter
(`gastownhall/beads@5d524cf7:docs/INTEGRATION_CHARTER.md`) explicitly punts
cross-tracker orchestration out of bd's scope, and swarm-wave follows the same
boundary.

### 2. Execute a wave

Launch parallel task agents for a specific wave. Takes the wave number as
argument.

**Steps:**

1. Read the active `SWARM-NN.md` file. Find the wave matching the requested
   wave number. Verify status is `pending` — if `committed`, report it is
   done; if `gate-pending` or `gate-passed`, redirect to workflow 3
   (Post-wave gate).
2. Run `git status` — if there are uncommitted changes, stop and report.
   Stale staged files get swept into agent commits.
3. Run the backpressure sequence from
   `references/agent-concurrency-limits.md` — Phase 1 (kill orphans),
   Phase 2 (GC cooldown — skip for waves with fewer than 5 agents), and
   Phase 3 (pressure check). If memory pressure is HIGH, reduce agent
   count and note the reduction. If CRITICAL, stop and report.
4. Claim all wave issues: run `bd update <id> --claim` for each issue ID in
   the wave. Report the claimed IDs. **Beadless source:** set each item's row
   in the wave's `### Item Status` table to `claimed` instead (the orchestrator
   owns these writes).
5. Update the wave status to `running` in the SWARM file.
6. Launch task agents in parallel. For each agent slot in the wave plan,
   use the Agent tool with a prompt built from the canonical template in
   `references/command-patterns.md`. Key elements:

   - Issue title and ID (from `bd show <id>`)
   - Exhaustive file scope list (files this agent may modify — never globs)
   - Isolation constraint: "Do not modify any file outside your scope list."
   - Validation: "Run `npm run check` before finishing."
   - Completion: "Run `bd close <id>` when the issue is done." (Beadless
     source: omit this line — the agent reports completion in its final
     message and the orchestrator marks the Item Status row `done`.)

   If a background research agent is planned for this wave, include it in
   the same parallel launch batch. Research agents write findings to a
   separate file and do not modify source files.

   All agent launches go in a single response (parallel execution).
7. Wait for all agents to complete. As each agent reports done, log it.
8. Verify closures: run `bd list --status in_progress` to check for unclosed
   issues. Any issue still `in_progress` means the agent did not complete —
   note it for the user (carry forward or retry in the next wave). **Beadless
   source:** the equivalent check is the wave's `### Item Status` table — any
   row still `claimed` (not `done`) is the unclosed-item signal; mark deferred
   items `carried`.
9. Update wave status to `gate-pending` in the SWARM file.
10. Suggest: "Wave N agents complete. Run `/swarm-wave post-wave-gate N` to
    run the quality gate."

### 3. Post-wave gate

Run the blocking quality gate after a wave completes. Takes the wave number
as argument.

This is a **hard blocking gate** — no commit happens until all steps pass.
See `references/wave-planning-checklist.md` for the full gate sequence and
`references/review-gate-protocol.md` for reviewer details.

**Steps:**

1. Read the active SWARM file. Find the wave. Verify status is
   `gate-pending` or `gate-passed`.
2. Launch two review agents and `npm run check` in parallel (Agent tool
   calls + Bash in a single response):
   - **Code reviewer**: reads all files modified by the wave (derive from
     the file ownership map in the SWARM file). Reviews for correctness,
     edge cases, error handling, type safety.
   - **Domain reviewer**: specialized by wave theme. See
     `references/review-gate-protocol.md` for the domain specialization
     table. If the wave theme is unclear, use a second code reviewer.
   - **`npm run check`**: via Bash (not an agent — fast and synchronous).
     Capture pass/fail.
3. Wait for both review agents and the check to complete. Read findings.
4. Tally the gate:
   - `npm run check` must pass (P0 — gate fails immediately on check errors).
   - Code reviewer confidence must be 80+.
   - Domain reviewer confidence must be 60+ (80+ for security-adjacent).
     See `references/review-gate-protocol.md` for threshold details and
     severity handling.
5. If the gate passes:
   - 5a. Run tests sequentially (workspace-first, root-last if applicable).
   - 5b. If tests pass: commit all wave changes with
     `git commit --no-gpg-sign -m "feat: wave N — [theme] (N issues)"`.
   - 5c. Close any remaining wave issues with `bd close`.
   - 5d. Update wave status to `committed` in the SWARM file.
   - 5e. Report: "Wave N passed gate and committed. N issues closed."
   - 5f. **If this is the final wave**: offer the retrospective handoff.
     "All waves committed. Run `/retrospective` to generate the sprint
     retro?" If the user confirms, invoke `/retrospective` via the Skill
     tool.
6. If the gate fails:
   - 6a. List specific failures (check errors, review concerns).
   - 6b. For `npm run check` failures: fix inline (mechanical fixes).
   - 6c. For HIGH-severity review findings: launch a targeted fix agent
     scoped to the specific concern and affected files. After the fix
     agent completes, re-gate from step 1. **If fix iterations exceed 2
     within a single wave, halt and escalate to the user instead of
     launching a third fix agent.** Scope is per-wave: a wave with
     multiple HIGH findings dispatches one fix agent that addresses all
     of them, and the count increments once per re-gate cycle (not once
     per finding). The iteration count covers fix-agent dispatches
     only — inline orchestrator fixes (step 6b) do not consume
     iteration budget, while user-directed MEDIUM fix-agent dispatches
     (step 6d) DO consume the same budget as HIGH-driven dispatches
     (same dispatch path). This is a preventive cap — Sprint 10 ran one
     fix iteration per wave; the budget exists to bound runaway gate
     failures in future runs where reviewers and fix agents disagree.
   - 6d. For MEDIUM/LOW findings: present to the user — accept risk and
     commit, or fix first. See `references/review-gate-protocol.md` for
     the severity handling table.
   - 6e. Never commit with an open HIGH-severity concern.

### 4. Map file contention

Standalone utility: build a file-to-issue matrix to identify contention
before planning waves. Also called inline by workflow 1 (Plan a swarm
sprint).

**Steps:**

1. Run `bd ready` to get all open issues. If beads is unavailable, ask the
   user to provide issue titles and descriptions — the same manual path
   workflow 1 (Plan a swarm sprint) Tier A falls back to.
2. For each issue, identify which files it is likely to touch:
   - 2a. Read the issue description (`bd show <id>`) — look for explicit
     file mentions.
   - 2b. Grep/Glob: search for function names, class names, or keywords
     mentioned in the description against the codebase. Map matches to
     files.
3. Build the file-to-issue matrix:

   ```
   File                      Issues           Contention
   src/foo.ts                id1, id2, id3    HIGH (3)
   src/bar.ts                id1, id2         MEDIUM (2)
   src/baz.ts                id3              LOW (1)
   ```

   HIGH = 3+ issues. MEDIUM = 2 issues. LOW = 1 issue.
4. For HIGH contention files with 500+ lines, run a section-level analysis:
   Grep for function or class boundaries to identify which sections each
   issue touches. If issues touch different sections, they may be compatible
   in the same wave — assign explicit line-range ownership. See
   `references/file-contention-and-clustering.md` for the two-tier
   contention model.
5. Present the map to the user. For HIGH contention files, recommend
   strategies from `references/file-contention-and-clustering.md` (sequence,
   split, refactor, consolidate).

### 5. Research wave

Orchestrate parallel research agents. Takes a topic or domain as argument.
Delegates issue creation to `/backlog-groomer` — this workflow only handles
the parallelism and deduplication.

**Steps:**

1. Identify the research domain from the user's request. Classify by intent:
   `explore`, `deepen`, `validate`, `audit`, or `bm-enrichment`. See
   `references/command-patterns.md` for the intent-matching table.
2. Determine agent count based on intent and RAM. Hard caps: 3-15 write
   agents, up to 37 for read-only audit. See
   `references/agent-concurrency-limits.md` for the ceiling table.
3. Design agent prompts. Each agent gets a distinct sub-question or domain
   slice — no two agents investigate the same question. Research agents
   write findings to separate files (one per agent). Research agents do not
   modify source files.
4. Launch all research agents in parallel (single response, multiple Agent
   tool calls).
5. Wait for all agents to complete. Read all findings files.
6. **Dedup pass.** Read all findings side by side. Identify duplicate or
   overlapping findings across agents. Produce a merged summary.
7. **Validate against code.** For each significant finding, use Grep/Glob
   to verify the claim holds in the actual codebase. Flag findings that do
   not match reality — research agents have a 15-20% false positive rate.
8. Present the merged, validated findings to the user. Suggest: "Run
   `/backlog-groomer workflow 5 (Create issues from findings)` to turn
   these into issues." Keep the findings cap at roughly 15 beads — more
   suggests the research scope was too broad.

## Guidelines

- **File isolation is non-negotiable.** Every agent in a wave must have an
  explicit, exhaustive list of files it may modify. Agents that wander
  outside their scope create the same conflict problems as shared-file
  agents. When in doubt, give an agent a narrower scope and create a
  follow-up issue for the remaining work.
- **The gate is a hard block.** The post-wave gate (workflow 3 (Post-wave
  gate)) must fully pass before the next wave launches. Never commit wave work that has not
  passed the gate. "Fix it later" is how parallel agent work produces
  cascading failures.
- **Beads is preferred, not required (Tier A).** swarm-wave needs a *work
  source*, not beads specifically (per CLAUDE.md `### Beads-availability
  convention`). Use beads when available; otherwise source waves from a
  `ROADMAP.md` (workflow 1 (Plan a swarm sprint)) or a manual list, and use the
  `SWARM-NN.md` Item Status table as run-state in place of `bd` claim/close.
  Guard every `bd` command so a beadless run never errors. Only stop when no
  work source can be obtained at all.
- **SWARM files are ephemeral.** `SWARM-NN.md` files are working documents,
  not committed artifacts. They should be gitignored.
- **No mutations without approval.** Wave plans require explicit user
  approval before the first agent launches. HIGH-severity gate failures are
  described to the user before fix agents launch. `/retrospective` is only
  invoked via the Skill tool after explicit user confirmation.
- **Agent prompts must be complete.** Each task agent needs: issue title,
  file scope, isolation constraint, validation command, and `bd close`
  instruction. See `references/command-patterns.md` for the canonical
  template. An incomplete prompt is a gate failure waiting to happen.
- **Research agents are read-only for source files.** Research agents may
  write findings files and may write to Basic Memory (using their own
  tool budgets). They must not modify source files.
- **Sequential tests, parallel reviews.** Reviews run in parallel (two
  agents). Tests run sequentially after the gate passes. This is a
  correctness requirement, not a performance trade-off.
- **RAM ceilings are hard caps.** The ceilings in
  `references/agent-concurrency-limits.md` come from empirical sprint
  data. Exceeding them produces OOM failures. When in doubt, run fewer
  agents.
- **Cross-skill boundaries.** swarm-wave does not own UPSTREAM, SYNERGY, or
  RETRO files. When a wave surfaces upstream friction, suggest
  `/upstream-tracker workflow 1 (Log a new entry)`. When the sprint closes,
  hand off to `/retrospective`. Do not replicate logic that belongs in
  other skills.
