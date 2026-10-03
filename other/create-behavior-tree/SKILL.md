---
name: create-behavior-tree
description: "Use when you need a Behavior Tree spec designed for NPC/AI decision-making. Triggers: 'create behavior tree', 'design npc ai', 'ai logic design', 'npc brain structure', 'decision making hierarchy'."
---

## 1. Overview
Generates formal BT specs for NPC/AI decision-making. Translates agent motivations into hierarchical decision trees. Output: `behavior_tree_spec.md` — discrete actions, conditional checks, prioritized decision hierarchies.

**Scenarios**: NPC/enemy/allies AI behavior, hierarchical trees from qualitative descriptions, reusable AI capabilities for multiple agent types.

## 2. Quick Reference

**Output**: `{TARGET_FOLDER}/docs/behavior_tree_spec.md`.

BT node types:
- **Selector** — tries children in priority order; succeeds on first child success
- **Sequence** — executes children left-to-right; fails on first child failure
- **Decorator** — modifies a single child's behavior (Inverter, Repeat, UntilFailure, etc.)
- **Action** — leaf node that performs a task (succeed/fail)
- **Condition** — leaf node that checks a predicate (true/false)

Workflow: Role & Goal Discovery → Capability Extraction (Actions/Conditions) → Behavior Mapping → Tree Construction & Validation → Export. Use `- ` indentation only (no Unicode tree chars). Every branch reaches a terminal node.

## 3. Workflow

1. **Role & Goal Discovery**: Identify AI Role (Guard, Merchant), Type (Hostile/Friendly/Neutral), primary motivations.
2. **Capability Extraction**: Define available Actions and Conditions without assuming implementation details — these become leaf nodes in the tree.
3. **Behavior Mapping**: Translate natural language rules into prioritized BT node hierarchy (Selectors, Sequences, Decorators). Each node has a single responsibility; compose complex behavior by arranging simple nodes into a tree structure.
4. **Tree Construction & Validation**: Strict formatting using `- ` indentation only (avoid Unicode tree chars or nested code blocks). Every branch leads to an action or valid exit. Validate that each subtree reaches a terminal node.
5. **Export**: Write to `{TARGET_FOLDER}/docs/behavior_tree_spec.md`.

## 3. Intercepts
- **[Implementation Detail]**: Engine-specific code detected → "Translating [Detail] to behavioral description (e.g., 'Play animation')."
- **[Vague Logic]**: Ambiguous rules → "Logic for [Behavior] too vague. Use concrete conditions like `is_in_range` or `has_line_of_sight`?"

## 4. Quality Gates
- **Behavioral Descriptions**: All nodes use abstract behavioral descriptions exclusively
- **Testable Conditions**: Every condition is concrete and verifiable (e.g., `is_in_range`, `has_line_of_sight`)
- **Complete Branches**: Every branch leads to a terminal action or valid exit
- **Progressive Logic**: Each decision advances the tree forward without repeating checks
- **Hierarchical Structure**: Use proper Selector/Sequence nesting instead of flat lists
