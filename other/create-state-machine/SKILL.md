---
name: create-state-machine
description: "Use when you need a state machine spec designed for complex systems like NPC behavior, quest flows, or UI states. Triggers: 'create state machine', 'design flow', 'fsm design', 'state transition spec', 'behavioral flow architect'."
---

## 1. Overview
Designs high-fidelity state machine specs for complex game systems. Defines clear state boundaries, valid transition triggers, and robust error handling to prevent unreachable states or implementation coupling.

**Scenarios**: NPC decision-making, branching quest/mission flows, UI navigation hierarchies, subsystems requiring strict control over mutually exclusive modes.

## 2. Quick Reference

**Output**: `{TARGET_FOLDER}/docs/state_machine_spec.md`. **Input context**: `events_spec.md`.

Workflow steps:
1. Discovery & Extraction — parse states, triggers, behavioral requirements from user descriptions
2. Gap Analysis — find missing invariants, ambiguous transitions, undefined edge cases
3. Formal Structuring — Overview → Glossary → States → Transitions (Guards/Hooks) → Data Context → Error Handling → Edge Cases
4. Completeness Validation — every non-terminal state has exits, no dead ends, guards are testable booleans, error recovery defined
5. Export — write spec file

Key rules: transitions are atomic (one event → one state change); guards must be deterministic booleans; use hierarchical structures for complex systems.

## 3. Core Pattern

1. **Discovery & Extraction** (`events_spec.md` context): Parse user descriptions to identify states, triggers (events), and behavioral requirements.
2. **Gap Analysis**: Identify missing invariants, ambiguous transitions, or undefined edge cases.
3. **Formal Structuring**: Overview → Glossary → States → Transitions (Guards/Hooks) → Data Context → Error Handling → Edge Cases. Every transition is atomic — a single event triggers one state change with no partial updates.
4. **Completeness Validation**: Non-terminal states have valid exits, no dead ends, guards are testable booleans, error recovery paths defined. Each atomic transition must be independently verifiable.
5. **Export**: Write to `{TARGET_FOLDER}/docs/state_machine_spec.md`. Ensure all transitions remain atomic: one guard evaluated, one hook sequence executed, one state changed.

## 3. Interaction Protocol
- **[Implementation Detail]**: Engine-specific code/timing detected → "I'll translate [Detail] into abstract events (e.g., 'Wait for event X')."
- **[Vague Guard]**: Narrative guard instead of logical → "Guard '[Guard]' is too vague. Use testable boolean like `player.isReady === true`?"

## 4. Quality Gates - STOP
- **Reachable States**: Every reachable non-terminal state has at least one valid exit path; terminal states are explicitly marked
- **Complete Transitions**: All expected inputs have defined transitions
- **Abstract States**: Use conceptual states only
- **Testable Guards**: Express guards as boolean conditions (e.g., `player.isReady === true`) instead of narrative descriptions
- **Controlled Complexity**: Use hierarchical structures to manage complex systems instead of flat state explosions

## 5. Final Integrity Audit
- [ ] All non-terminal states have at least one valid exit transition
- [ ] No unreachable states in the graph
- [ ] Every guard is a deterministic, testable boolean
- [ ] Error recovery paths defined for critical failure modes
- [ ] Spec is language/engine agnostic (no API calls)
