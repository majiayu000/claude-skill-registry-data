---
name: world-operator
description: Provides comprehensive context about the Codako game engine's world operator, actor/character/rule types, stage helpers, and simulation logic. Use when modifying world-operator.ts, stage-helpers.ts, types.ts, or any game simulation, rule evaluation, or world state management code.
---

# World Operator & Game Engine Context

## When to Use This Skill

Activate this skill when working on:
- The WorldOperator (`frontend/src/editor/utils/world-operator.ts`)
- Stage helpers (`frontend/src/editor/utils/stage-helpers.ts`)
- Core domain types (`frontend/src/types.ts`)
- Rule evaluation, conditions, or actions
- Actor/character behavior
- World state mutations or history/undo
- The recording flow (programming by demonstration)
- Animation frames or debug data

## Key Files

| File | Purpose |
|------|---------|
| `frontend/src/types.ts` | All domain model types |
| `frontend/src/editor/utils/world-operator.ts` | Simulation engine |
| `frontend/src/editor/utils/stage-helpers.ts` | Position, transform, and comparison helpers |
| `frontend/src/editor/utils/frame-accumulator.ts` | Animation frame tracking |
| `frontend/src/editor/utils/world-constants.ts` | FLOW_BEHAVIORS and CONTAINER_TYPES |

## Core Concepts

### Domain Model Hierarchy

```
Character (template)
  ├── rules: RuleTreeItem[]      # Behavior tree
  ├── spritesheet.appearances    # Sprites
  └── variables                  # Variable definitions

Actor (instance of Character)
  ├── characterId                # Reference to template
  ├── position: {x, y}           # Grid coordinates
  ├── appearance                 # Current sprite ID
  ├── variableValues             # Instance variable overrides
  └── transform                  # Rotation/flip

Stage (2D grid)
  ├── actors: {[id]: Actor}
  ├── width, height
  └── wrapX, wrapY               # Edge wrapping

World (complete state)
  ├── stages: {[id]: Stage}
  ├── globals                    # Global variables
  ├── input: {keys, clicks}      # Current frame input
  ├── evaluatedRuleDetails       # Debug: detailed rule evaluation results
  ├── evaluatedTickFrames        # Debug: animation frames
  └── history: HistoryItem[]     # Undo stack (max 20)
```

### Rule Structure

A **Rule** defines a before→after pattern transformation:

```typescript
Rule = {
  mainActorId: string           // "Owner" actor, always at (0,0) in rule space
  actors: {[id]: Actor}         // "Before" pattern - positions relative to mainActor
  conditions: RuleCondition[]   // Additional constraints
  actions: RuleAction[]         // Transformations to apply
  extent: RuleExtent            // Bounding box {xmin, xmax, ymin, ymax, ignored}
}
```

### Rule Tree (Control Flow)

Rules are organized hierarchically:

- **RuleTreeEventItem** (`group-event`): Filters by input
  - `event: "key"` with `code` - Specific key press
  - `event: "click"` - Actor was clicked
  - `event: "idle"` - Always fires

- **RuleTreeFlowItem** (`group-flow`): Controls iteration
  - `behavior: "first"` - Stop after first match
  - `behavior: "all"` - Execute all matches
  - `behavior: "random"` - Shuffle, then first match
  - `behavior: "loop"` - Repeat N times

### Conditions and Actions

**RuleCondition**: Comparison between two RuleValues
```typescript
{ left: RuleValue, comparator: VariableComparator, right: RuleValue, enabled: boolean }
```

**RuleValue** variants:
- `{ constant: string }` - Literal value
- `{ actorId, variableId }` - Actor's variable/appearance/transform
- `{ globalId }` - Global variable

**RuleAction** types:
- `move` - Change position (delta or offset)
- `appearance` - Change sprite
- `transform` - Rotate/flip
- `variable` - Modify actor variable (add/set/subtract)
- `delete` - Remove actor
- `create` - Spawn new actor
- `global` - Modify global variable

## WorldOperator API

```typescript
WorldOperator(previousWorld, characters) → {
  tick(),        // Advance simulation one step
  untick(),      // Revert to previous state
  resetForRule() // Set up for rule preview
}
```

### tick() Flow

1. **Snapshot** previous state to history
2. **Clone** globals and actors for mutation
3. **Update** special globals (keypress, click)
4. **Evaluate** each actor's rules via `ActorOperator`
5. **Return** new immutable world state

### Pattern Matching (checkRuleScenario)

For each grid cell in rule.extent:
1. Find stage actors at that position (wrapping-aware)
2. Find rule actors covering that position
3. Unless "ignored", actor counts must match
4. Stage actors must match rule actors (same character + conditions)
5. Verify all referenced actors found
6. Validate action offsets are valid positions

Returns `{ruleActorId → stageActor}` mapping, or `false`.

## Debug Data

### evaluatedRuleDetails
```typescript
{ [actorId]: { [ruleId]: EvaluatedRuleDetails } }
```
Tracks detailed evaluation results for each rule per actor. Includes:
- Overall pass/fail status
- Per-square matching results (with failure reasons)
- Per-condition evaluation results (with resolved values)
- Actor mappings (which stage actor matched which rule actor)

Used by inspector to show rule state circles and condition status dots. See `granular-rule-tracking.md` for full details.

### evaluatedTickFrames
```typescript
Frame[] where Frame = { actors: {[id]: FrameActor}, id: number }
FrameActor = Actor & { deleted?, actionIdx?, animationStyle? }
```
Animation frames within a tick. Stage container animates through these.

## Important Patterns

1. **Immutable Updates**: Uses `updeep` (imported as `u`) for state updates
2. **Relative Positioning**: Rule positions are relative to mainActor at (0,0)
3. **Deep Clone**: Always clone before mutating (`deepClone` from utils)
4. **Wrapping**: Use `wrappedPosition()` for stage edge handling
5. **History**: Only saved when at least one rule fires

## See Also

- `architecture-reference.md` - Detailed architecture diagrams, data flow, and code examples
- `granular-rule-tracking.md` - Documentation for the granular rule evaluation tracking system (square/condition-level feedback)
