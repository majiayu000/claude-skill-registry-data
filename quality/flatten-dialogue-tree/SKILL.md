---
name: flatten-dialogue-tree
description: "Use when flattening complex branching dialogue trees, validating for dead ends and unreachable nodes, and ensuring localization key coverage."
---

# flatten-dialogue-tree

## 1. Overview

Flattens complex branching dialogue trees into linearized, validated traversal orders. Traces every conversation path to detect dead ends, unreachable nodes, and logic conflicts, ensuring all dialogue leads to valid conclusions. Output: linearized `flattened_dialogue.md` for developer/tester clarity.

## 2. When to Use

- **Scenarios**: Validating branching dialogue trees for dead ends and unreachable nodes, converting hierarchical dialogue structures into linearized traversal orders, ensuring localization key coverage across all dialogue branches.
- **Triggers**: `dialogue tree`, `branching dialogue`, `conversation flow`, `dead end`, `unreachable dialogue`, `dialogue validation`, `dialogue branches`.

## 3. Core Pattern

1. **Node Extraction**: Extract each dialogue node, including its unique ID, Speaker, Text Key (localization), Conditions (reachability), and Choices (outgoing branches).
2. **Branch Mapping**: For every node, record all outgoing branches by mapping the Choice Text, the triggering Condition, and the Target Node.
3. **Linearization (Flattening)**: Convert the hierarchical tree into a linearized traversal order, starting from the entry node and clearly marking mutually exclusive vs. additive branches.
4. **Integrity Validation**: Verify reachability for every node, detect dead ends/terminal integrity, check logic consistency (overlapping conditions), and ensure localization key presence.
5. **Specification Export**: Write the finalized, validated spec to `{TARGET_FOLDER}/docs/flattened_dialogue.md`.

## 4. Interaction Protocol

### Error Handling & Intercepts

- **[Dead-End Intercept]**: If a node has no exit and isn't marked as an end: *"I've detected a dead end at [Node ID]. The conversation will hang here. Should we add an exit choice or mark this as a terminal node?"*
- **[Logic Conflict Intercept]**: If two branches have overlapping conditions: *"I notice a logic conflict at [Node ID]. Branches [A] and [B] both satisfy the same conditions. Should we refine the requirements to make them mutually exclusive?"*

## 5. Quality Gates

- **Terminal Integrity**: Every node either has at least one exit transition or is explicitly marked as a terminal/end node
- **Mutually Exclusive Branches**: Each branch uses distinct conditions; overlapping criteria are refined for clarity
- **Reachable Nodes**: Every dialogue node has at least one valid path from the entry point
- **Localization Coverage**: All branches and text content have corresponding keys in `localization_keys.md`
- **Exit Conditions**: Circular paths include at least one possible exit condition to reach an end state
