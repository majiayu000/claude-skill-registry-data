---
name: implement-state-machine
description: "Use when you need a state machine engine generated with guarded transitions and lifecycle hooks. Triggers: 'implement state machine', 'state transitions'."
---

# implement-state-machine

## 1. Overview
Generates high-integrity state machine engines from formal specs. Ensures explicit terminal states and robust error recovery to prevent undefined behavior in production.

## 2. Core Pattern

1. **Platform Detection**: Analyze config for target language; resolve idioms (Enums vs Classes).
2. **Spec Parsing** (`state_machine_spec.md`): Extract states, transitions (`Source` → `Trigger` → `Target`), guards, lifecycle hooks. Detect composite/nested hierarchies.
3. **State & Transition Definition**: Generate strongly-typed states and `Transition` structure (source, target, trigger, guard, hooks).
4. **Core Engine**: Atomic `Transition(trigger)` method: Match → `OnExit` → Guard → State Change → `OnEnter`.
5. **Composite Integration**: Nested FSM instances in parent contexts; guards/hooks receive `GameState` context.

## 3. Interaction Protocol
- **[Invalid Transition]**: No matching transition for trigger → "Invalid transition for [State] with trigger [Trigger]. Implement error handler or add valid transition?"
- **[Guard Failure]**: Guard evaluates false → "Transition [Source]→[Target] failed: unsatisfied Guard ([Name]). System stays in current state. Refine guard or add fallback?"

**Constraint**: Every state must have at least one exit path or be marked terminal. Recommend fallback transitions for critical systems.

## 4. Red Flags - STOP and Start Over
- **Defined Transitions**: Every trigger has a matching transition or error handler
- **Guard Fallbacks**: Provide fallback transitions when guards evaluate false
- **Correct Hook Order**: Execute OnExit before state change, OnEnter after

## 5. Final Integrity Audit
- [ ] All states from `state_machine_spec.md` as strongly-typed objects/enums
- [ ] Every transition: Exit → Guard → State Change → Enter
- [ ] Nested hierarchies propagate context correctly
- [ ] Terminal states explicitly handled
