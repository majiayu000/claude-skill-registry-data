---
name: reverse-document
description: "Use when existing implementation needs a design or architecture document reconstructed from evidence."
---

<!-- codex-studio-delegation: governed -->
Resolve every role through `../../../.codex/docs/plugin-agent-delegation.md`;
do not require a repository-local `.codex/agents/` or `.codex/agent-packs/` tree.
Before default delegation, run `python3 ../../../tools/codex_studio/agent_delegation.py resolve --project-root <project-root> --role <role>` and use only its returned role contract.

## Codex Interaction Contract

- Ask one decision question per turn and wait for the answer before asking another.
- Use `request_user_input` for structured choices when it is available; otherwise ask the same concise question directly.
- Use Codex custom agents by role and profile when delegation is useful.
- Treat any approved write as one complete proposed changeset. Before writing, present every target path and material edit together; do not add unlisted files or behavior.
- A new path, expanded scope, or material change requires a revised complete proposed changeset and fresh approval.

## Documentation Changeset Boundary

Analyze read-only, then show the evidence summary and artifact outline before drafting. Present the draft and complete proposed changeset before writing the selected document path.

# Reverse Documentation

This skill analyzes existing implementation (code, prototypes, systems) and generates
appropriate design or architecture documentation. Use this when:
- You built a feature without writing a design doc first
- You inherited a codebase without documentation
- You prototyped a mechanic and need to formalize it
- You need to document "why" behind existing code

---

## Workflow

## Phase 1: Parse Arguments

**Format**: `$reverse-document <type> <path>`

**Type options**:
- `design` → Generate a game design document (GDD section)
- `architecture` → Generate an Architecture Decision Record (ADR)
- `concept` → Generate a concept document from prototype

**Path**: Directory or file to analyze
- `src/gameplay/combat/` → All combat-related code
- `src/core/event-system.cpp` → Specific file
- `prototypes/stealth-mech/` → Prototype directory

**Examples**:
```bash
$reverse-document design src/gameplay/magic-system
$reverse-document architecture src/core/entity-component
$reverse-document concept prototypes/vehicle-combat
```

## Phase 2: Analyze Implementation

**Read and understand the code/prototype**:

**For design docs (GDD):**
- Identify mechanics, rules, formulas
- Extract gameplay values (damage, cooldowns, ranges)
- Find state machines, ability systems, progression
- Detect edge cases handled in code
- Map dependencies (what systems interact?)

**For architecture docs (ADR):**
- Identify patterns (ECS, singleton, observer, etc.)
- Understand technical decisions (threading, serialization, etc.)
- Map dependencies and coupling
- Assess performance characteristics
- Find constraints and trade-offs

**For concept docs (prototype analysis):**
- Identify core mechanic
- Extract emergent gameplay patterns
- Note what worked vs what didn't
- Find technical feasibility insights
- Document player fantasy / feel

## Phase 3: Ask Clarifying Questions

Do not merely describe the code; identify unresolved intent such as resource purpose, pillar status, scaling intent, architecture trade-offs, or emergent prototype behavior.

Ask the first unresolved intent question and wait for the answer. Record that answer. Then ask the next unresolved intent question and wait again. Continue sequentially until every material uncertainty is resolved or explicitly marked unknown. Never batch multiple intent decisions into one prompt.

## Phase 4: Present Findings

Before drafting, show what you discovered:

```
I've analyzed [path]/. Here's what I found:

MECHANICS IMPLEMENTED:
- [mechanic-a] with [property] (e.g. timing windows, cooldowns)
- [mechanic-b] (e.g. interaction between two states)
- [resource] system (depletes on [action], regens on [condition])
- [state] system (builds up, triggers [effect])

FORMULAS DISCOVERED:
- [Output] = [formula using discovered variables]
- [Secondary output] = [formula]

UNRESOLVED INTENT QUEUE:
- [Resource] system purpose
- [Mechanic] pillar status
- [Value] scaling intent

Next question (one only): [first unresolved intent question]
```

Wait for the answer, update the queue, and return to Phase 3 for the next single question before drafting.

## Phase 5: Draft Document Using Template

Based on type, use appropriate template:

| Type | Template | Output Path |
|------|----------|-------------|
| `design` | `../../../.codex/docs/templates/design-doc-from-implementation.md` | `design/gdd/[system-name].md` |
| `architecture` | `../../../.codex/docs/templates/architecture-doc-from-code.md` | `docs/architecture/[decision-name].md` |
| `concept` | `../../../.codex/docs/templates/concept-doc-from-prototype.md` | `prototypes/[name]/CONCEPT.md` or `design/concepts/[name].md` |

**Draft structure**:
- Capture **what exists** (mechanics, patterns, implementation)
- Document **why it exists** (intent clarified with user)
- Identify **what's missing** (edge cases not handled, gaps in design)
- Flag **follow-up work** (balance tuning, missing features)

## Phase 6: Show Draft and Request Approval

**Collaborative protocol**:
```
I've drafted the [system-name] design doc based on your code and clarifications.

[Show key sections: Overview, Mechanics, Formulas, Design Intent]

ADDITIONS I MADE:
- Documented [mechanic] as "[intent]" per your clarification
- Added edge cases not in code (e.g., what if [resource] hits 0 mid-[action]?)
- Flagged balance concern: [scaling type] scaling at [boundary condition]

SECTIONS MARKED AS INCOMPLETE:
- "[System] interaction with [other-system]" (not fully implemented yet)
- "[Variant or feature]" (only [subset] implemented so far)

Proposed complete changeset: `design/gdd/[system-name].md`. Approve this draft and exact path?
```

Wait for approval. User may request changes before writing.

## Phase 7: Write Document with Metadata

When approved, write the file with special markers:

```markdown
---
status: reverse-documented
source: [path/]
date: [today]
verified-by: [User name]
---

# [System Name] Design

> **Note**: This document was reverse-engineered from the existing implementation.
> It captures current behavior and clarified design intent. Some sections may be
> incomplete where implementation is partial or intent was unclear.

[Rest of document...]
```

## Phase 8: Flag Follow-Up Work

After writing, suggest next steps:

```
✅ Written to design/gdd/combat-system.md

FOLLOW-UP RECOMMENDED:
1. Run $balance-check on combat formulas (exponential scaling concern)
2. Create ADR for stamina system architecture decision
3. Implement missing edge cases:
   - Stamina depletion mid-combo behavior
   - Stagger state during dodge
4. Extend design doc when weapon variety is implemented

Next decision (one only): Should I prepare the `$balance-check` handoff first?
```

---

## Template Selection Logic

| If analyzing... | Use template... | Because... |
|----------------|-----------------|------------|
| `src/gameplay/*` | `../../../.codex/docs/templates/design-doc-from-implementation.md` | Gameplay mechanics → GDD |
| `src/core/*`, `src/ai/*` | `../../../.codex/docs/templates/architecture-doc-from-code.md` | Core systems → ADR |
| `prototypes/*` | `../../../.codex/docs/templates/concept-doc-from-prototype.md` | Experiments → concept doc |
| `src/networking/*` | `../../../.codex/docs/templates/architecture-doc-from-code.md` | Technical systems → ADR |
| `src/ui/*` | `../../../.codex/docs/templates/design-doc-from-implementation.md` | UI/UX → design spec |

---

## Example Session: Sequential Intent Clarification

```text
User: $reverse-document design src/gameplay/[system]

Agent: I found three unresolved intent areas. First question: Is the resource system primarily for pacing or strategic management?

User: Pacing; it should prevent repeated high-power actions.

Agent: Recorded. Next question: Is the central mechanic a core pillar or a supporting feature?

User: Core pillar.

Agent: Recorded. Next question: Should the current exponential scaling remain, or should the document mark it for tuning?

User: Mark it for linear tuning.

Agent: All material intent questions are resolved. Here is the draft and its one complete proposed changeset.
```

---

## Collaborative Protocol

This skill follows the collaborative design principle:

1. **Analyze First**: Read code, understand implementation
2. **Question Intent**: Ask about "why", not just "what"
3. **Present Findings**: Show discoveries, highlight unclear areas
4. **User Clarifies**: Separate intent from accidents
5. **Draft Document**: Create doc based on reality + intent
6. **Show Draft**: Display key sections, explain additions
7. **Get Approval**: Present `[filepath]` and the full draft as one complete proposed changeset. On approval: Verdict: **COMPLETE** — document generated. On decline: Verdict: **BLOCKED** — user declined write.
8. **Flag Follow-Up**: Suggest related work, don't auto-execute

**Never assume intent. Always ask before documenting "why".**
