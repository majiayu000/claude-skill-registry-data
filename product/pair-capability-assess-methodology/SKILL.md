---
name: pair-capability-assess-methodology
description: "Assess development methodology using resolution cascade (Argument > Adoption > Assessment). Reads methodology guidelines, proposes Scrum/Kanban/Lean/etc., writes way-of-working.md methodology section, composes /pair-capability-record-decision. Idempotent."
version: 0.4.1
author: Foomakers
---

# /pair-capability-assess-methodology — Methodology Assessment

Evaluate and decide on the development methodology: Scrum, Kanban, Lean, Waterfall, SAFe, LeSS, or hybrid. Follows the resolution cascade.

## Arguments

| Argument  | Required | Description                                                                     |
| --------- | -------- | ------------------------------------------------------------------------------- |
| `$choice` | No       | Override: skip assessment, use this methodology directly (e.g. `kanban`, `scrum`) |

## Composed Skills

| Skill              | Type       | Required                                            |
| ------------------ | ---------- | --------------------------------------------------- |
| `/pair-capability-record-decision` | Capability | Yes — records methodology decision as ADL           |

## Proposal Target

The rendered adoption content is destined for this section — the caller writes it via `/pair-capability-record-decision`:

- **Target**: [adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — **methodology section**
- **Ownership**: Methodology section (shared file — /pair-capability-assess-pm owns PM tool section)

## Adoption File

- **Target**: [adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) — **methodology section**
- **Ownership**: Methodology section (shared file — /pair-capability-assess-pm owns PM tool section)

## Algorithm

### Step 1: Resolution Cascade

#### Path A — Argument Override

1. **Check**: Is `$choice` provided?
2. **Skip**: If not provided, go to Path B.
3. **Act**: Confirm the choice. Check for conflicts with existing adoption.
4. **Verify**: Developer confirms. Proceed to Step 3.

#### Path B — Adoption Exists

1. **Check**: Does [adoption/tech/way-of-working.md](../../../.pair/adoption/tech/way-of-working.md) exist and contain a methodology reference (e.g. "Kanban", "Scrum", or similar)?
2. **Skip**: If no methodology defined, go to Path C.
3. **Act**: Read current adoption. Confirm it's valid.
4. **Check**: Does a corresponding decision record exist?
5. **Act**: If decision record missing, compose `/pair-capability-record-decision` to backfill.
6. **Verify**: Done — exit skill.

#### Path C — Full Assessment

1. **Act**: Proceed to Step 2.

### Step 2: Read Guidelines

1. **Act**: Read methodology guidelines:
   - [Methodology README](../../../.pair/knowledge/guidelines/collaboration/methodology/README.md) — decision framework, comparison matrix, decision tree, cost-benefit analysis
   - Individual methodology files as needed for detail:
     - [Kanban](../../../.pair/knowledge/guidelines/collaboration/methodology/kanban.md)
     - [Scrum](../../../.pair/knowledge/guidelines/collaboration/methodology/scrum.md)
     - [Lean](../../../.pair/knowledge/guidelines/collaboration/methodology/lean.md)
     - [Waterfall](../../../.pair/knowledge/guidelines/collaboration/methodology/waterfall.md)
     - [SAFe](../../../.pair/knowledge/guidelines/collaboration/methodology/safe.md)
     - [LeSS](../../../.pair/knowledge/guidelines/collaboration/methodology/less.md)
2. **Act**: Read project context:
   - [adoption/product/PRD.md](../../../.pair/adoption/product/PRD.md) — team size, timeline, requirements stability
   - [adoption/tech/architecture.md](../../../.pair/adoption/tech/architecture.md) — system complexity
3. **Verify**: Guidelines and context loaded.

### Step 3: Evaluate Options

1. **Act**: Apply the Methodology Comparison Matrix from guidelines:
   - Score each methodology on: Requirements Stability, Change Tolerance, Team Size/Complexity, Time to Market, Predictability Needs, Quality Focus, Learning/Innovation.
   - Weight criteria based on project type.

2. **Act**: Apply the Methodology Selection Decision Tree for quick validation.

3. **Act**: Present recommendation:

   > **Methodology Recommendation: [Name]**
   > - Score: [weighted total]
   > - Rationale: [evidence from project context and matrix]
   > - Key ceremonies: [list main ceremonies/practices]
   > - Trade-offs: [acknowledged limitations]

4. **Act**: If two methodologies score within 10%, present both with trade-off analysis.

5. **Verify**: Developer approves.

### Step 4: Write Adoption File

1. **Act**: Write or update **methodology-related content** in [way-of-working.md](../../../.pair/adoption/tech/way-of-working.md):
   - Methodology name and key practices
   - Development cycle description (iterations, flow, etc.)
   - Preserve all other sections (quality gates, PM tool, etc.)
2. **Verify**: Methodology section written. Other sections preserved.

### Step 5: Record Decision

1. **Act**: Compose `/pair-capability-record-decision`:
   - `$type`: `non-architectural`
   - `$topic`: `methodology-choice`
   - `$summary`: "[Methodology] adopted for development workflow"
2. **Verify**: ADL created. Adoption consistent.

## Output Format

```text
ASSESSMENT COMPLETE:
├── Domain:    Methodology
├── Path:      [Argument Override | Adoption Exists | Full Assessment]
├── Decision:  [methodology name]
├── Adoption:  [way-of-working.md methodology section — written | confirmed | updated]
├── Record:    [ADL path — created | exists | backfilled]
└── Status:    [Complete | Confirmed existing]
```

## Composition Interface

When composed by `/pair-process-bootstrap`:

- **Input**: `/pair-process-bootstrap` invokes during Phase 2.
- **Output**: Returns decision summary and adoption file path.

When invoked **independently**:

- Full interactive flow. Developer commits changes.

## Edge Cases

- **way-of-working.md exists but no methodology section**: Add methodology content, preserve all other sections.
- **Team uses hybrid approach**: Document the hybrid: which elements from which methodology, how they combine.
- **Methodology change mid-project**: Update adoption, create new decision record referencing the old one.

## Graceful Degradation

- If methodology guidelines not found, use minimal assessment: ask developer for methodology preference based on team size and requirements stability.
- If `/pair-capability-record-decision` not installed, warn and skip recording.
- If way-of-working.md doesn't exist, create it with methodology section. Warn: "Created way-of-working.md — other sections should be populated."

## Notes

- Methodology decisions are **non-architectural** → produce ADL.
- **Section ownership**: this skill writes ONLY methodology-related content in way-of-working.md. /pair-capability-assess-pm owns PM tool section. Quality gates section is managed by /pair-process-bootstrap.
- Educational content (methodology descriptions, ceremonies, WHY each works) stays in guidelines.
