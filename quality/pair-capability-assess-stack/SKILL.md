---
name: pair-capability-assess-stack
description: "Assess tech stack using resolution cascade (Argument > Adoption > Assessment). Lifecycle-spanning: bootstrap (full eval), implementation (add dependency), review (detect unlisted). Version tracking. Composes /pair-capability-record-decision. Idempotent."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-stack — Tech Stack Assessment

Evaluate and decide on the technology stack: languages, frameworks, runtime, database, and libraries — all with version tracking. Follows the resolution cascade and operates across the entire project lifecycle.

## Arguments

| Argument  | Required | Description                                                                              |
| --------- | -------- | ---------------------------------------------------------------------------------------- |
| `$choice` | No       | Technology to assess (e.g. `zod@3.22`, `node@20`, `react@18.2`). Format: `name@version`. |
| `$mode`   | No       | Lifecycle mode: `bootstrap`, `implementation`, `review`. Auto-detected if omitted.       |

## Composed Skills

| Skill              | Type       | Required                                     |
| ------------------ | ---------- | -------------------------------------------- |
| `/pair-capability-record-decision` | Capability | Yes — records stack decision as ADL (or ADR) |

## Proposal Target

The rendered adoption content is destined for this file — the caller writes it via `/pair-capability-record-decision`:

- **Target**: [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — **core sections only**
- **Ownership**: Core sections only — see [Section Ownership](#section-ownership) below for the full table (Testing owned by /pair-capability-assess-testing, AI by /pair-capability-assess-ai).

## Adoption File

- **Target**: [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) — **core sections only**
- **Ownership**: Core sections (language, framework, runtime, database, monorepo, bundling, release, linting, git hooks, CLI tooling, markdown/docs)
- **Shared file**: /pair-capability-assess-testing owns Testing section, /pair-capability-assess-ai owns AI section

## Lifecycle Modes

### Bootstrap Mode

Full stack evaluation. Used when no tech stack is defined yet. Evaluates language, framework, runtime, database, key libraries. Produces the initial `tech-stack.md` with all core sections and versions.

### Implementation Mode

Add or update a single dependency. Used when `/pair-process-implement` detects a new dependency or developer wants to add a library. Validates compatibility with existing stack, adds to `tech-stack.md` with version, records decision.

### Review Mode

Detect and evaluate unlisted dependencies. Used when `/pair-process-review` finds a dependency in code that isn't in `tech-stack.md`. Presents approve/reject options to developer. If approved, adds to stack and records decision.

## Algorithm

### Step 0: Detect Lifecycle Mode

1. **Check**: Is `$mode` provided?
2. **Skip**: If provided, use it. Proceed to Step 1.
3. **Act**: Auto-detect mode:
   - `$choice` provided AND [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) has populated core sections → `implementation` (adding to existing stack)
   - `$choice` provided AND tech-stack.md missing or empty → `bootstrap` (initial setup with override)
   - No `$choice` AND tech-stack.md missing or empty → `bootstrap` (full assessment)
   - No `$choice` AND tech-stack.md populated → check caller context
     - Called by `/pair-process-review` → `review`
     - Otherwise → confirm existing adoption (Path B of cascade)
4. **Verify**: Mode is set.

### Step 1: Resolution Cascade

#### Path A — Argument Override (implementation or bootstrap with $choice)

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act** (implementation mode): Validate compatibility:
   - Parse `$choice` as `name@version`.
   - Check existing [tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) for conflicts:
     - Version incompatibility (e.g. library needs Node 20, stack has Node 18)
     - Duplicate entry (same library already listed)
     - Category conflict (e.g. two ORMs)
   - If conflict detected, warn developer:

     > **Compatibility issue**: `$choice` conflicts with existing stack.
     > - Conflict: [description]
     > - Options: (a) resolve conflict and proceed, (b) reject addition

4. **Act** (bootstrap mode with choice): Confirm the choice and proceed to Step 3.
5. **Verify**: Choice validated. Proceed to Step 3.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) exist with populated core sections?
2. **Skip**: If not populated or missing, go to Path C.
3. **Act**: Read current adoption. Present summary:

   > Tech stack already adopted. Core sections populated.
   > [Summary of key technologies with versions]

4. **Check**: Does a corresponding decision record exist?
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Adoption and decision record consistent. Done — exit skill.

#### Path C — Full Assessment (bootstrap mode)

1. **Act**: Proceed to Step 2 (full assessment).

### Step 2: Read Guidelines (bootstrap mode only)

1. **Act**: Read technology guidelines:
   - [Technology Stack Standards](../../../.pair/knowledge/guidelines/technical-standards/technology-stack/stack-standards.md) — stack requirements
   - [Framework Selection](../../../.pair/knowledge/guidelines/technical-standards/technology-stack/framework-selection.md) — evaluation criteria
   - [Tech Decisions](../../../.pair/knowledge/guidelines/technical-standards/technology-stack/tech-decisions.md) — decision frameworks
   - [Conventions](../../../.pair/knowledge/guidelines/technical-standards/technology-stack/conventions.md) — naming and coding conventions
2. **Act**: Read project context:
   - [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — project type, scale, constraints
   - [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md) — architecture pattern (stack must support it)
3. **Verify**: Guidelines and context loaded.

### Step 3: Evaluate and Decide

#### Bootstrap Mode (full evaluation)

1. **Act**: For each core category, evaluate options:
   - **Language**: Primary development language
   - **Framework**: Web/CLI/application framework
   - **Runtime**: Execution environment with version
   - **Database**: If applicable, persistence layer
   - **Package manager**: Dependency management
   - **Monorepo tooling**: If applicable
   - **Core libraries**: Essential libraries (CLI parsing, formatting, etc.)
   - **Bundling**: Build and packaging tools
   - **Linting/formatting**: Code quality tools with versions
   - **Release management**: Versioning and changelog tools

2. **Act**: For each category, use guideline evaluation criteria:
   - Compatibility with chosen language and architecture
   - Community health and maintenance status
   - Team familiarity and learning curve
   - License compatibility

3. **Act**: Present full stack recommendation with versions:

   > **Tech Stack Recommendation:**
>
   > | Category | Technology | Version | Rationale |
   > |----------|-----------|---------|-----------|
   > | Language | [name] | [vX.Y] | [reason] |
   > | ... | ... | ... | ... |

1. **Verify**: Developer approves the full stack.

#### Implementation Mode (add single entry)

1. **Act**: Confirm the addition:

   > Adding to tech stack: **$choice**
   > - Category: [auto-detected or ask]
   > - Compatible: [yes/no — details]
   > - Rationale: [developer provides or auto-inferred]

2. **Verify**: Developer approves.

#### Review Mode (unlisted dependency detected)

1. **Act**: Present finding to developer:

   > **Unlisted dependency detected**: `[name@version]`
   > Found in: [file(s)]
   > Not listed in tech-stack.md.
   >
   > Options:
   > 1. **Approve** — add to tech stack with version + record decision
   > 2. **Reject** — flag for removal from implementation

2. **Act**: If approved → treat as implementation mode addition.
3. **Act**: If rejected → report back to caller (e.g. /pair-process-review marks as CHANGES-REQUESTED).
4. **Verify**: Developer decision captured.

### Step 4: Write Adoption File

1. **Check**: Does [adoption/tech/tech-stack.md](../../../.pair/adoption/tech/tech-stack.md) exist?
2. **Act** (bootstrap mode): Write full tech-stack.md with all core sections. Include version for every entry.
3. **Act** (implementation/review mode): Add or update **only the affected entry** in the appropriate section. Preserve all other content, including sections owned by /pair-capability-assess-testing and /pair-capability-assess-ai.
4. **Verify**: Adoption file written. All entries have versions. Section ownership respected.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - **Bootstrap**: `$type: non-architectural`, `$topic: tech-stack-initial`, `$summary: "Initial tech stack adopted: [key technologies]"`
   - **Implementation**: `$type: non-architectural`, `$topic: stack-add-[name]`, `$summary: "[name]@[version] added to tech stack — [rationale]"`
   - **Review approve**: `$type: non-architectural`, `$topic: stack-approve-[name]`, `$summary: "[name]@[version] approved during review — added to tech stack"`
2. **Verify**: Decision record created. Adoption file consistent with record.

## Version Tracking Policy

- Every entry in tech-stack.md **MUST** include a version: `[tool] v[X.Y.Z]` or `[tool]@[X.Y.Z]`.
- **Major.minor required**, patch optional.
- Version updates go through /pair-capability-assess-stack: check compatibility with existing stack, update adoption, write decision record.
- Version format in adoption file: human-readable prose (e.g. "vitest v3.2.4 is adopted").

## Section Ownership

| Section                     | Owner            | Other Skills                        |
| --------------------------- | ---------------- | ----------------------------------- |
| Core (language, framework, runtime, DB) | `/pair-capability-assess-stack`  | Read-only for others          |
| Monorepo, bundling, release | `/pair-capability-assess-stack`  | Read-only for others                |
| Linting, formatting, hooks  | `/pair-capability-assess-stack`  | Read-only for others                |
| CLI tooling, markdown/docs  | `/pair-capability-assess-stack`  | Read-only for others                |
| **Testing**                 | `/pair-capability-assess-testing`| /pair-capability-assess-stack reads, never writes   |
| **AI**                      | `/pair-capability-assess-ai`     | /pair-capability-assess-stack reads, never writes   |

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:    Tech Stack
├── Mode:      [Bootstrap | Implementation | Review]
├── Path:      [Argument Override | Adoption Exists | Full Assessment]
├── Decision:  [technology@version — or full stack summary]
├── Adoption:  [tech-stack.md — written | confirmed | updated | entry added]
├── Record:    [ADL path — created | exists | backfilled]
└── Status:    [Complete | Confirmed existing | Approved | Rejected]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes `/pair-capability-assess-stack` during Phase 2 with `$mode: bootstrap`. May pass `$choice` for pre-selected stack.
- **Output**: Returns decision summary and adoption file path.
- `/pair-process-bootstrap` includes adoption and ADL changes in the next commit.

When composed by `/pair-process-implement`:

- **Input**: `/pair-process-implement` detects new import/dependency → invokes `/pair-capability-assess-stack` with `$choice: [name@version]`, `$mode: implementation`.
- **Output**: Returns validation result (approved/rejected) and adoption file path.
- If rejected (incompatible) → `/pair-process-implement` HALTs.

When composed by `/pair-process-review`:

- **Input**: `/pair-process-review` detects unlisted dependency → invokes `/pair-capability-assess-stack` with `$choice: [name@version]`, `$mode: review`.
- **Output**: Returns developer decision (approve/reject).
- If rejected → `/pair-process-review` includes as CHANGES-REQUESTED finding.

When invoked **independently**:

- Full interactive flow. Mode auto-detected. Developer commits changes.

## Edge Cases

- **Argument conflicts with adoption**: Warn developer with details, ask for confirmation.
- **Version conflict**: Library requires runtime version different from adopted → warn, propose resolution (upgrade runtime or reject library).
- **Duplicate entry**: Same library already in stack → check if version differs. If same, skip. If different, treat as version update.
- **Multiple skills writing same file**: Section ownership prevents conflicts. Each skill writes only its sections.
- **tech-stack.md exists but missing core sections**: Fill gaps, preserve existing content.
- **Decision record already exists for same scope+decision**: Skip writing (no duplicates).

## Graceful Degradation

- If technology guidelines are not found, use minimal assessment: ask developer for stack choices directly.
- If `/pair-capability-record-decision` is not installed, warn and skip decision recording.
- If architecture.md doesn't exist, warn: "No architecture adopted — stack compatibility cannot be verified against architecture."
- If tech-stack.md doesn't exist (bootstrap mode), create it. If implementation/review mode, HALT: "No tech stack defined — run /pair-capability-assess-stack in bootstrap mode first."

## Notes

- **Lifecycle-spanning**: unlike other assess-* skills (primarily bootstrap), /pair-capability-assess-stack is used throughout bootstrap, implementation, and review.
- **Tech stack as registry**: `tech-stack.md` is the registry of approved technologies. Only listed technologies are approved. Unlisted technologies detected during review trigger /pair-capability-assess-stack evaluation.
- Stack decisions are typically **non-architectural** → produce ADL. Exception: if a stack choice fundamentally changes the architecture (e.g. switching from monolith to microservices runtime), use ADR.
- **Section ownership** prevents parallel write conflicts: each assess-* skill owns its sections, preserves others.
- Educational content (technology descriptions, ecosystem overview, WHY) stays in guidelines. This skill references guidelines for evaluation criteria and comparison matrices.
