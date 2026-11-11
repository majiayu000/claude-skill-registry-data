---
name: pair-capability-assess-architecture
description: "Assess architecture pattern using resolution cascade (Argument > Adoption > Assessment). Reads architecture guidelines, proposes pattern, writes adoption file, composes /pair-capability-record-decision. Idempotent."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-architecture — Architecture Assessment

Evaluate and decide on the system architecture pattern. Follows the resolution cascade: explicit argument wins, then existing adoption, then full assessment from guidelines.

## Arguments

| Argument  | Required | Description                                                                 |
| --------- | -------- | --------------------------------------------------------------------------- |
| `$choice` | No       | Override: skip assessment, use this architecture directly (e.g. `hexagonal`) |

## Composed Skills

| Skill              | Type       | Required                                          |
| ------------------ | ---------- | ------------------------------------------------- |
| `/pair-capability-record-decision` | Capability | Yes — records architecture decision as ADR |

## Proposal Target

The rendered adoption content is destined for this file — the caller writes it via `/pair-capability-record-decision`:

- **Target**: [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md)
- **Ownership**: Full file (sole owner)

## Adoption File

- **Target**: [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md)
- **Ownership**: Full file (sole owner)

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Confirm the choice with the developer:

   > Architecture override: **$choice**.
   > This will be adopted without full assessment.
   > Confirm?

4. **Check**: Does an adoption file already exist with a different pattern?
   - If yes, warn: "Current adoption is **[existing]**. Override to **$choice**?"
5. **Verify**: Developer confirms. Proceed to Step 2.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md) exist and is it populated (not template)?
2. **Skip**: If not populated or missing, go to Path C.
3. **Act**: Read current adoption. Present:

   > Architecture already adopted: **[pattern name]**.
   > Adoption file is current and valid.

4. **Check**: Does a corresponding decision record exist? (Scan [adoption/tech/adr/](../../../.pair/adoption/tech/adr) for `*architecture*` files.)
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Adoption and decision record consistent. Done — exit skill.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2 (full assessment mode).

### Step 2: Read Guidelines

1. **Act**: Read architecture guidelines:
   - [Architecture README](../../../.pair/knowledge/guidelines/architecture/README.md) — decision tree, complexity matrix, selection criteria
   - [Architectural Patterns](../../../.pair/knowledge/guidelines/architecture/architectural-patterns/README.md) — pattern descriptions and trade-offs
   - [Project Constraints](../../../.pair/knowledge/guidelines/architecture/project-constraints/README.md) — team, platform, deployment constraints
2. **Act**: If PRD exists, read [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) for project context (team size, scale, compliance).
3. **Verify**: Guidelines and project context loaded.

### Step 3: Evaluate Options

1. **Act**: Apply the Architecture Complexity Matrix from guidelines against project constraints:
   - Score each candidate pattern on: Implementation Complexity, Team Skill Required, Maintenance Overhead, Scalability, Best For.
   - Weight criteria based on project type (from PRD or developer input).

2. **Act**: If two or more patterns score within 10% of each other, present top 2 with trade-off analysis:

   > **Top candidates:**
   > 1. **[Pattern A]** — Score: X. Strengths: ... Weaknesses: ...
   > 2. **[Pattern B]** — Score: Y. Strengths: ... Weaknesses: ...
   >
   > Recommendation: **[Pattern A]** because [reason].

3. **Act**: If one pattern clearly wins, present recommendation:

   > **Recommendation: [Pattern]**
   > - Rationale: [evidence from constraints and matrix]
   > - Trade-offs: [key trade-offs acknowledged]

4. **Verify**: Developer approves the choice.

### Step 4: Write Adoption File

1. **Check**: Does [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md) exist?
2. **Act**: Write or update the adoption file with the chosen pattern:
   - Concise, prescriptive statements (what IS adopted, not options)
   - Reference guidelines for detailed rationale
   - Preserve existing content in other sections if file already exists
3. **Verify**: Adoption file written and consistent.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - `$type`: `architectural`
   - `$topic`: `architecture-pattern`
   - `$summary`: "[Pattern] adopted as system architecture"
2. **Verify**: ADR created at `adoption/tech/adr/YYYY-MM-DD-architecture-pattern.md`. Adoption file consistent with ADR.

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:    Architecture
├── Path:      [Argument Override | Adoption Exists | Full Assessment]
├── Decision:  [pattern name]
├── Adoption:  [adoption/tech/architecture.md — written | confirmed | updated]
├── Record:    [ADR path — created | exists | backfilled]
└── Status:    [Complete | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes `/pair-capability-assess-architecture` during Phase 2 (checklist completion). May pass `$choice` if developer pre-selected.
- **Output**: Returns decision summary and adoption file path.
- `/pair-process-bootstrap` includes adoption and ADR changes in the next commit.

When invoked **independently**:

- Full interactive flow. Developer commits changes when satisfied.

## Edge Cases

- **Argument conflicts with adoption**: Warn developer, ask for confirmation. If confirmed, update adoption and create new decision record (supersedes previous).
- **Adoption file partially exists** (e.g. has some sections but missing architecture pattern): Fill gap, preserve existing content.
- **No PRD available**: Proceed with assessment using developer-provided constraints. Warn: "No PRD found — relying on developer input for project context."
- **Decision record already exists for same scope+decision**: Skip writing (no duplicates).

## Graceful Degradation

- If architecture guidelines are not found, use minimal decision framework: ask developer to choose between Modular Monolith, Hexagonal, and Microservices based on team size and scale needs.
- If `/pair-capability-record-decision` is not installed, warn and skip decision recording: "Decision not recorded — /pair-capability-record-decision not installed."
- If adoption directory doesn't exist, create it on first write.

## Notes

- This skill establishes the base pattern for all assess-* skills: resolution cascade + guidelines reference + adoption write + /pair-capability-record-decision composition.
- Architecture decisions are **architectural** type → always produce ADR (never ADL).
- The resolution cascade IS the idempotency mechanism: if adoption exists, assessment is already done.
- Educational content (pattern descriptions, trade-offs, WHY) stays in guidelines. This skill references guidelines for decision matrices and scoring.
