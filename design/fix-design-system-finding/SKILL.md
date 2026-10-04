---
name: fix-design-system-finding
description: Fix a specific design-system integration finding in a Figma screen or component, including missing shared components, local overrides, and unbound tokens.
---

# Fix One Design-System Finding

Use this skill after `audit-design-system` has already identified a concrete issue.

This skill is intentionally narrow:
- one finding at a time
- one offending node or local cluster at a time
- minimal read scope
- minimal write scope

Load these capabilities first:
- Figma MCP read access for the normal inspection tools
- a `figma-use`-style helper before any `use_figma` write call, when your environment requires one

Use [apply-design-system](../apply-design-system/SKILL.md) instead when the task is a broader screen-wide reconnect, multiple sections need coordinated changes, or the user explicitly wants a full pass across the frame.

## Expected Input

Prefer one of these:
- a single JSON finding from `audit-design-system`
- the full review JSON plus the specific finding to address
- a paraphrased issue plus a Figma URL or `fileKey` and `nodeId`

If the finding came from `audit-design-system`, extract the target from:
- `code_location.absolute_file_path = /figma/<fileKey>/nodes/<nodeId>`

Treat the review result as the scope contract. Do not silently widen from one finding into a full cleanup pass.

## Scope Rule

Stay pinned to the selected finding until one of these is true:
- `fixed`: the targeted issue is corrected
- `blocked`: the fix requires missing library assets, inaccessible components, or broader product decisions
- `needs-follow-up`: the targeted node is improved, but a separate adjacent issue remains and should be reviewed independently

If the user pastes multiple findings, either address the one they selected or pick the highest-priority finding and say that is the one being fixed now.

## Required Workflow

### 1. Normalize the Finding

Extract and restate:
- `fileKey`
- offending `nodeId`
- finding title
- why the reviewer flagged it

If the review output does not identify a specific node, stop and ask for either the raw finding JSON or a direct Figma node.

### 2. Run A Local Compatibility Check When Replacement Choice Is Ambiguous

Before backing anything up or editing the canvas, decide whether a clean fix is actually possible.

Run a local compatibility check when:
- the finding implies a DS swap but does not identify the exact component
- more than one library component looks plausible
- override behavior or sizing is unclear
- the user explicitly wants extra research before writing

Do not continue into writes until the compatibility check returns one of:
- `safe-to-apply`
- `blocked`
- `needs-human-choice`

The compatibility check should answer:
- which exact component or variant is the leading candidate
- whether text, icon, state, and size overrides are supported
- whether the replacement can preserve the node's layout contract

If the result is `blocked`, stop and report the blocker.

If the result is `needs-human-choice`, stop and ask the minimal clarifying question instead of guessing.

### 3. Gather Only the Evidence Needed

Before writing, inspect the target with the smallest useful set of reads:
1. `get_screenshot` for the offending node or closest enclosing section
2. `get_metadata` for structural context
3. `get_variable_defs` when the finding mentions tokens, raw values, color, spacing, or typography
4. `get_code_connect_map` when the finding suggests an existing mapped component
5. `search_design_system` only if you still need to locate the replacement primitive

Do not re-review the whole board unless the finding clearly points to a repeated pattern and the repeated pattern is required to choose the fix.

### 4. Classify the Fix

Choose exactly one remediation mode:
- `swap-instance`: replace an ad-hoc or wrong instance with the correct library component or variant
- `compose-from-primitives`: rebuild the local custom wrapper from published library parts
- `bind-tokens`: replace raw values with variables or styles
- `align-variant`: move an existing instance to the correct variant or property state
- `blocked`: no valid library-backed fix is currently possible

If more than one mode seems plausible, prefer the smallest change that satisfies the original finding.

### 5. Back Up Only the Affected Area

Before destructive edits, duplicate only the offending node or the smallest enclosing local section.

Name the backup clearly, for example:
- `Backup - Fix finding 1`
- `Backup - Custom nav`

Make the backup in its own write call and return the created node ID.

### 6. Apply the Fix Incrementally

Do not rebuild the whole screen.

Work in small steps:
1. inspect current node IDs and component linkage
2. import or locate the needed library component or variable
3. replace, compose, or retokenize only the targeted area
4. return all created and mutated node IDs

Prefer `swapComponent()` when it preserves the node's position and valid overrides.

Prefer rebuilding beside the original when:
- the current node is a local wrapper with mixed custom structure
- the review finding points at a custom composition, not a single primitive
- you need visual comparison before replacing the original

If the first validation pass shows that the recommended component regresses layout, text visibility, icon behavior, or width contract, stop. Report `blocked` or `needs-follow-up` instead of continuing to force the same primitive into place.

### 7. Validate the Finding, Not the Entire Screen

After the write:
1. screenshot the changed node or its immediate section
2. confirm the specific review complaint is no longer true
3. confirm the result is library-backed or token-bound when that was the goal
4. confirm spacing and text overrides still make sense

Only expand validation beyond the local section if the fix touched a global pattern such as navigation.

## Decision Heuristics

- If the finding says a primitive was recreated as a frame, bias toward `swap-instance`.
- If the finding says repeated local wrappers should collapse into a shared pattern, fix one representative node unless the task explicitly asks to roll the fix across all siblings.
- If the finding is about raw values beside tokenized peers, bias toward `bind-tokens`.
- If the finding is about a locally edited instance with the wrong size or state, bias toward `align-variant`.
- If the library lacks the required component family or the import fails, mark it `blocked` instead of improvising a fake connection.
- If a DS component exists but cannot preserve the node's text/icon/sizing contract, mark it `blocked` or `needs-human-choice` instead of forcing the swap.

## Writing Rules

- Keep the write scope tightly aligned to the selected finding.
- No write before a `safe-to-apply` compatibility outcome when replacement choice is ambiguous.
- Do not claim the whole screen is "on system" after fixing one finding.
- Prefer exact component keys and variable IDs over names.
- Do not continue into unrelated cleanup just because you noticed more drift.
- If a broader refactor is obviously needed, finish the targeted fix or report the blocker, then recommend `apply-design-system` for the next pass.

## Deliverable Format

When closing the task, report:
- `Finding fixed`: what changed and on which node
- `Validation`: how you confirmed the original issue is resolved
- `Blocked` or `Follow-up`: only if the finding could not be fully resolved

Keep the report tied to the single finding. Avoid screen-wide summaries unless the user asks for them.
