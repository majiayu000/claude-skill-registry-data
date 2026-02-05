---
name: spec-first-sdlc
description: |
  Spec-First, Agent-Implemented Software Development Lifecycle. Use when:
  (1) Starting a new software project that needs structured design-before-code approach,
  (2) User mentions "SDLC", "spec-first", "design docs", or "implementation spec",
  (3) User wants to go from requirements/intent to working code with traceability,
  (4) Project requires documented architectural decisions and review checkpoints,
  (5) User has existing design artifacts and wants to continue from a specific phase.
  Produces: Intent doc → HLD → ADR-Lite → EIS → Code → Validation tests.
---

# Spec-First SDLC

A structured software development lifecycle where specifications drive implementation. Human writes intent; Claude produces design documents, implementation specs, code, and tests—with review gates at each phase.

## Workflow Overview

```
Intent & Constraints (human)
        ↓
High-Level Design (Claude) ←→ Human Review
        ↓
ADR-Lite (Claude) ←→ Human Review
        ↓
Revised HLD (Claude)
        ↓
Executable Implementation Spec (Claude) ←→ Human Review
        ↓
Code Generation (Claude)
        ↓
Validation Tests (Claude)
```

## Phase Details

### Phase 1: Intent and Constraints
**Owner:** Human  
**Output:** `docs/intent-and-constraints.md`

Human provides:
- Problem statement and goals
- Functional requirements
- Non-functional constraints (performance, security, scalability)
- Known boundaries and limitations

### Phase 2: High-Level Design (HLD)
**Owner:** Claude  
**Input:** Intent and constraints document  
**Output:** `docs/high-level-design.md`  
**Template:** See [references/hld-template.md](references/hld-template.md)

Generate HLD covering:
- System architecture and component breakdown
- Data flow and integration points
- Technology choices (with rationale)
- **Open questions section** listing:
  - Ambiguities in requirements
  - Design choice alternatives with default recommendations
  - Areas needing clarification

Wait for human review and agreement before proceeding.

### Phase 3: Architecture Decision Record Lite (ADR-Lite)
**Owner:** Claude  
**Input:** Approved HLD + human feedback  
**Output:** `docs/adr-lite.md`  
**Template:** See [references/adr-template.md](references/adr-template.md)

For each significant decision, document:
- **Decision:** What was decided
- **Alternatives:** Options considered
- **Rationale:** Why this choice (reference constraints from intent doc)
- **Consequences:** Trade-offs and implications

Each ADR entry must explicitly reference:
- The HLD open question it resolves
- Relevant constraints from intent document that influenced the decision

Wait for human review and agreement before proceeding.

### Phase 4: HLD Revision
**Owner:** Claude  
**Input:** Approved ADR-Lite  
**Output:** Updated `docs/high-level-design.md`

Revise HLD to:
- Resolve open questions by referencing ADR-Lite decisions
- Add traceability links (e.g., "See ADR-001")
- Remove ambiguities

### Phase 5: Executable Implementation Specification (EIS)
**Owner:** Claude  
**Input:** Revised HLD + ADR-Lite  
**Output:** `docs/implementation-spec.md`  
**Template:** See [references/eis-template.md](references/eis-template.md)

Specify implementation details:
- **API contracts:** Endpoints, request/response schemas, error semantics, auth
- **State machines:** Key business entity lifecycles with transitions and guards
- **Persistence:** File layouts, database schemas, data models
- **Module boundaries:** Interface contracts between components

Wait for human review and agreement before proceeding.

### Phase 6: Code Generation
**Owner:** Claude  
**Input:** Approved EIS  
**Output:** Source code in `src/`

Implement code that:
- Adheres strictly to EIS contracts
- Includes documentation comments explaining design rationale
- Follows project's coding conventions
- References relevant ADR decisions in comments where appropriate

### Phase 7: Validation
**Owner:** Claude  
**Input:** Implementation + Intent document  
**Output:** Tests in `tests/`

Generate comprehensive tests:
- **State transition tests:** Verify entity lifecycle behaviors
- **Contract tests:** Validate API request/response schemas
- **Negative tests:** Error handling, invalid inputs, edge cases
- **Concurrency tests:** Race conditions, deadlocks (where applicable)

Tests should trace back to original intents and constraints.

## Review Gates

Never proceed to the next phase without explicit human approval. At each gate:
1. Present the deliverable with a summary of key points
2. Highlight decisions or areas that may need discussion
3. Ask: "Ready to proceed to [next phase], or would you like changes?"

## Mid-Workflow Entry

When user provides existing artifacts and wants to continue from a specific phase:

### 1. Identify Entry Point
Determine which phase to start from based on what artifacts exist:
- Has intent doc only → Start at Phase 2 (HLD)
- Has intent + HLD → Start at Phase 3 (ADR-Lite)
- Has intent + HLD + ADR → Start at Phase 4 (HLD Revision) or Phase 5 (EIS)
- Has complete specs → Start at Phase 6 (Code) or Phase 7 (Validation)

### 2. Assess Existing Artifacts
Before generating the next artifact, review provided documents for:
- **Completeness:** Are required sections present?
- **Consistency:** Do artifacts align with each other?
- **Open items:** Are there unresolved questions that block progress?

If gaps or inconsistencies found:
```
"I reviewed [artifact]. Before proceeding to [next phase], I noticed:
- [Gap or inconsistency]
Would you like me to address this first, or proceed with assumptions?"
```

### 3. Establish Traceability
When entering mid-workflow, explicitly map existing artifacts:
- Extract key decisions/constraints from provided docs
- Reference them when generating new artifacts
- Note any assumptions made due to missing context

### 4. Resume Normal Flow
After assessment, continue with standard phase sequence and review gates.

## File Structure

```
project/
├── docs/
│   ├── intent-and-constraints.md
│   ├── high-level-design.md
│   ├── adr-lite.md
│   └── implementation-spec.md
├── src/
│   └── [implementation files]
└── tests/
    └── [test files]
```
