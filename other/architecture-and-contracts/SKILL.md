---
name: architecture-and-contracts
description: Use when .forge/prd.md exists and the system needs a structural design before task breakdown, when modules will be implemented in parallel and need interface contracts to prevent integration failures, or when non-obvious technical decisions need to be recorded for future reference.
---

# Architecture and Contracts

## Overview

Read `.forge/prd.md` and produce three artifacts: a system architecture document, precise interface contracts per module boundary, and ADRs for non-obvious decisions. Contracts must be specific enough that two engineers can implement different modules independently and integrate without surprises.

## When to Use

- `.forge/prd.md` exists and is complete
- System has 2+ modules that need to interact
- Team will work in parallel — contracts prevent integration failures
- Non-obvious tech decisions need to be recorded with rationale

## When NOT to Use

- PRD doesn't exist yet — run `spec-driven-development` first
- Trivial change touching only one module — skip straight to `tdd`
- Architecture already exists and contracts are current — just update the affected contract

## Common Rationalizations

| Thought | Reality |
|---------|---------|
| "We don't need contracts for a small feature" | Contracts protect parallel workers — without them, work diverges |
| "I'll define interfaces as I implement" | Interfaces defined during implementation encode accidents as decisions |
| "ADRs are bureaucratic overhead" | ADRs are the only record of why — without them, decisions get relitigated |
| "The architecture is obvious from the PRD" | Make the obvious explicit — it's where disagreements hide |
| "I can keep the architecture in my head" | You can. Your parallel workers can't. |

## Red Flags

- Contracts written at function level instead of module boundary level
- Input/output types described in prose instead of typed schemas
- "Error handling: TBD" in any contract
- Architecture document names files and line numbers (these rot)
- ADR is missing a "Decision" section — only has "Context"
- `.forge/contracts/` has no files after this skill runs

## Core Process

### Step 1: Read the PRD

Read `.forge/prd.md`. Identify: module list, interaction points, data flows, NFRs that impose architectural constraints.

### Step 2: Explore existing architecture

If a codebase exists, explore it. Understand current patterns, tech stack, existing module boundaries. The architecture must fit the existing system unless the PRD explicitly calls for a rewrite.

### Step 3: Design the system

Produce a system overview:
- Component diagram (text-based: boxes and arrows)
- Tech stack decisions with rationale
- Data flow for the primary user journey
- Where each module from the PRD sits in the system

### Step 4: Write interface contracts

For each module boundary identified in the PRD, write a contract file at `.forge/contracts/<module-name>.md`. See [contract-templates.md](../../references/contract-templates.md).

Each contract must define:
- **Provides**: what this module exposes to callers
- **Consumes**: what this module depends on
- **Input types**: typed schemas for every input
- **Output types**: typed schemas for every output
- **Error types**: named error cases with conditions
- **Invariants**: guarantees the module always maintains
- **Not responsible for**: explicit out-of-scope list

### Step 5: Write ADRs

For each non-obvious decision made in steps 3-4, write an ADR at `.forge/adr/NNN-<slug>.md`. Use the format in [contract-templates.md](../../references/contract-templates.md).

**Required fields:**
- `forge:meta` header with `last_reviewed_at` set equal to `generated_at` on creation.
- Body header lines: `Status:` (Accepted on creation), `Superseded by:` (blank), `Supersedes:` (blank unless this ADR replaces a previous one).
- Review log: one initial line `<date> — Created.`

When this skill re-runs and the user identifies a decision that has been superseded:
1. Write the new ADR (`ADR-N+1`) with `Supersedes: ADR-N`.
2. Update the old ADR's body: `Status: Superseded by ADR-N+1`, `Superseded by: ADR-N+1`, bump `last_reviewed_at` to now-UTC, append a review-log line.

### Step 5b: Address pending feedback

Before re-writing architecture or contracts on a re-run, read `.forge/feedback/*.md`. For every entry where `status: PENDING` AND `target_artifact` is one of this skill's outputs (`architecture.md`, `contracts/*.md`, `adr/*.md`):

1. Address the recommended change in the regenerated artifact.
2. Update the feedback entry in place: `status: RESOLVED`, `resolved_at: <now UTC>`, `resolved_by: <commit short sha or "manual">`. Append a brief note describing what changed.

If a feedback entry's recommendation is rejected (the team decides the current artifact is correct), mark it `status: DEFERRED` with a reason in the body. Do not delete feedback entries — they are historical record.

### Step 6: Cost modeling

Include a cost model section in the architecture:
- Per-unit cost breakdown (what does one transaction/request/user cost?)
- Margin analysis per pricing tier (if applicable)
- Cost scaling curve (how costs grow with 10x, 100x users)
- Third-party API costs at projected volume

### Step 7: Write architecture.md

Write `.forge/architecture.md` with system overview, component diagram, tech stack table, cost model section, and a table of all contracts with their module names and file paths. Prepend a `forge:meta` header (`generated_by: architecture-and-contracts`, `generated_at: <ISO 8601 UTC with Z>`, `depends_on: [.forge/prd.md]` — paths only, never hashes, `generated_from: {.forge/prd.md: <upstream content_hash AT generation time>}`, `content_hash: <sha256 first 8 of THIS file's body>`). Same header convention on every file under `.forge/contracts/` and `.forge/adr/` (co-output: each carries the same `depends_on` + `generated_from` set). See [forge-dependency-graph](../../references/forge-dependency-graph.md).

### Step 8: Expansion documents (optional)

When the user requests deeper analysis, generate supplementary docs:
- `docs/architecture/scalability-analysis.md`
- `docs/architecture/microservices-design.md`
- `docs/planning/testing-strategy.md`
- `docs/planning/feature-priority-matrix.md`

These are deeper dives on specific sections. Generate only when explicitly requested.

## Verification

- [ ] `.forge/prd.md` read in full
- [ ] On re-run: all PENDING feedback entries targeting architecture.md / contracts/ / adr/ addressed AND marked RESOLVED with `resolved_at` + `resolved_by`
- [ ] Every module from the PRD has a contract in `.forge/contracts/`
- [ ] Every contract has input types, output types, error types, and invariants
- [ ] No contract says "TBD" in any required field
- [ ] Architecture document uses component names, not file paths
- [ ] At least one ADR written (even "use existing patterns" is a decision)
- [ ] Every ADR has `last_reviewed_at` set on creation (== `generated_at`)
- [ ] Superseded ADRs have `Status: Superseded by ADR-NNN` AND `Superseded by:` field filled
- [ ] Cost model section included with per-unit costs and scaling curve
- [ ] `.forge/architecture.md` written with component diagram
- [ ] Contract table in architecture.md lists all contract files

## Fit-Check

Before declaring done, emit one of:

- A short list of specific fit issues observed (e.g., "Only 2 modules being changed but 6 contracts emitted — overscoped; consider skipping for single-module work next time" / "Cost model section assumed multi-tenant SaaS pricing; this is an internal admin tool with no cost dimension").
- The explicit line: **"No fit issues observed for this use case."**

Silence is not allowed. See [docs/skill-anatomy.md#fit-check](../../docs/skill-anatomy.md#fit-check-the-meta-honesty-step).
