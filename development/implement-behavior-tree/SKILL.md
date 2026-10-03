---
name: implement-behavior-tree
description: "Use when you have a behavior tree spec (behavior_tree_spec.md) and need to generate the BT execution engine, node types, and AI factories."
---

## 1. Overview
Generates high-performance BT engine for NPC/AI decision-making. Focuses on correct mathematical definitions for composite nodes and multi-tick async operations via strict `Running` state handling.

## 2. Core Pattern

1. **Platform Detection**: Scan config for target language/platform.
2. **Core Nodes**: Generate `Node` interface (with `tick()` method) + `Status` enum (`Success`/`Failure`/`Running`).
3. **Composite & Leaf Nodes**: `SelectorNode` (short-circuiting), `SequenceNode` (progress tracking), `ConditionNode`, `ActionNode`.
4. **Context & Factory**: `BTContext` object for entity/game state + specialized factory functions.
5. **Tree Definitions (MANDATORY)**: Read `behavior_tree_spec.md` Section 3. For EACH tree:
    * Generate `<TreeName>Tree.ts` or `<EnemyType>AI.ts`
    * Create exact node hierarchy (Selector → Sequence → Condition/Action)
    * Implement all conditions/actions from Section 2 as concrete classes
    * Condition/action nodes read/write ECS exclusively through BTContext
6. **Enemy AI Factories (MANDATORY)**: For each enemy tier in spec:
    * Accept entity ID + optional config → return root node
    * Accept `BTContext` for per-entity state
    * Export from single file (e.g., `src/ai/enemyFactories.ts`)
    * Include factories for each tier (e.g., `createSwarmMeleeAI()`, `createEliteRangedAI()`)

## 3. Interaction Protocol
- **[Running Status]**: Node missing `Running` state support → "Node needs async/multi-tick capability. Adding `Running` state?"
- **[Broken Composite]**: Selector/Sequence deviates from definition → "[Node Type] must follow its logical definition. Refactor?"

**Guidance**: All composites must follow mathematical definitions using Status enum transitions. Prioritize Running status for multi-tick async actions.

## 4. Red Flags
- **Running State Support**: All nodes handle Running status for multi-tick async actions
- **Correct Composite Definitions**: Selectors short-circuit on success, Sequences track progress
- **Clean State Management**: Nodes clean up global state modifications

## 5. Final Integrity Audit
- [ ] Composite nodes (Selector, Sequence) follow mathematical definitions
- [ ] Leaf nodes interact with BTContext (no direct ECS access)
- [ ] `Running` status handled for multi-tick async actions
- [ ] **All tree hierarchies from Section 3 implemented as concrete definitions**
- [ ] **All condition/action nodes from Section 2 as concrete classes**
- [ ] **Enemy AI factories for each enemy tier**
- [ ] **`src/ai/` not empty — contains all tree defs and factories**
