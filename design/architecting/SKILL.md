---
name: superpowers-sage:architecting
description: >
  Define architecture for a Sage/Acorn feature — architecture decision records,
  component boundaries, data flow, dependency mapping, pre-implementation design,
  trade-off analysis, Acorn architecture patterns, ADR, design before building
user-invocable: true
argument-hint: "[feature or scope description]"
---

# Architecting (Compatibility Mode)

This skill remains available to avoid breaking existing workflows. It now orchestrates the new split flow:

1. `superpowers-sage:architecture-discovery`
2. `superpowers-sage:plan-generator`

**Announce at start:** "I'm using architecting compatibility mode and will run architecture-discovery then plan-generator."

## Input

$ARGUMENTS

## HARD GATE

Do not implement code in this skill. If implementation is requested, complete the split planning flow first.

## Procedure

### 0) Design system gate

Before starting architecture discovery, check whether the visual foundation exists:

1. Does `resources/css/design-tokens.css` exist **and** contain real tokens (not a placeholder)?
2. Does a kitchensink route/view exist (e.g., `resources/views/kitchensink.blade.php` or `/kitchensink` is accessible)?

**If both are present:** proceed to Step 1 normally.

**If either is missing or unvalidated:**

```
⚠ Design system foundation not found.

Architecture for multi-block features should follow a validated design system.
Tokens, UI atoms, and layout components must exist before defining block schemas.

Recommendation: run /sage-design-system first.
  → It will create design-tokens.css, ui/ + layout/ Blade components, and validate with a kitchensink page.
  → Return to /architecting after the kitchensink screenshot is confirmed.

Proceed anyway? (only if this feature has no visual blocks / is purely backend)
```

Wait for explicit user confirmation before skipping the design system gate.

### 1) Run architecture discovery

- Invoke `superpowers-sage:architecture-discovery` with the same arguments.
- Wait for explicit user approval of the written architecture spec.

### 2) Run plan generation

- Invoke `superpowers-sage:plan-generator` with the approved spec path.
- Ensure output plan includes strategy, dependencies, and per-component execution ordering.

### 3) Transition to execution

After plan generation, offer:

1. `subagent-driven-development` for parallel task execution in this session
2. `superpowers-sage:building` for direct implementation from plan files

## Verification

- Confirm both files exist before claiming completion:
  - `docs/superpowers/specs/YYYY-MM-DD-<topic>-architecture.md`
  - `docs/plans/YYYY-MM-DD-<topic>/plan.md`
- Confirm the user approved the architecture spec before invoking `superpowers-sage:plan-generator`.

## Failure modes

- If architecture approval is missing: stop and return to `superpowers-sage:architecture-discovery` review loop.
- If plan generation cannot parse the spec: ask for spec corrections and re-run `superpowers-sage:plan-generator`.
