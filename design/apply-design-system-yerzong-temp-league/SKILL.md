---
name: apply-design-system
description: Review an existing design and connect it to design system components.
---

# Connect A Design To A Design System

Use this skill for an existing Figma design that should reuse a published design system instead of detached layers, local wrappers, or one-off components.

This skill supports two entry modes:
- `review-then-apply`: the user wants a broad pass, but the exact offending sections are not yet identified
- `apply-known-scope`: the user already knows which sections or clusters should be brought onto the design system

Load these capabilities first:
- Figma MCP read access for tools such as `get_metadata`, `get_screenshot`, and `search_design_system`
- a `figma-use`-style helper before any `use_figma` call, when your environment requires one
- a screen-building companion workflow, when available, if you are reconnecting a full screen or page

Do not use this skill as the default follow-up to a single `audit-design-system` finding. For one targeted issue, use [fix-design-system-finding](../fix-design-system-finding/SKILL.md) so the write scope stays narrow.

## Core Rule

Do not treat a section as "connected" just because it contains a few design-system buttons or icons.

This skill is for multi-section reconciliation. If the task can be satisfied by fixing one specific reviewed node, the narrower finding-fix skill is the better choice.

Classify each section into exactly one bucket:
- `already-connected`: the section itself is a library instance or a composition the user explicitly accepts as already canonical
- `exact-swap`: a published library component or variant can replace the section directly
- `compose-from-primitives`: no single library component exists, but the section can be rebuilt from published library primitives
- `blocked`: the library does not expose the needed components, imports fail, or the section is intentionally bespoke

## Required Workflow

### 1. Determine Scope First

Before gathering replacement candidates, decide whether the screen needs an initial audit.

If scope is not already identified:
1. Run [audit-design-system](../audit-design-system/SKILL.md) or perform an equivalent internal audit pass.
2. Collapse the review output into section-sized work packages instead of treating every micro-finding as a separate rewrite task.
3. If the review produces only one narrow finding, switch to [fix-design-system-finding](../fix-design-system-finding/SKILL.md) instead of continuing here.

If scope is already identified, continue directly.

Do not skip component discovery just because a review already exists. Review identifies drift; this skill still has to choose the actual replacement primitives and variants.

### 2. Capture the Current State

Before writing:
1. Get the target frame metadata with `get_metadata`.
2. Get a screenshot with `get_screenshot`.
3. If you need `get_design_context` and Figma asks the Code Connect question, ask the user exactly as instructed by the tool before proceeding.

For this skill, prefer `get_metadata` plus `use_figma` for structure discovery. `get_design_context` is optional unless it unlocks missing context.

### 3. Back Up the Target Screen

Before destructive edits, duplicate the frame or page and place the backup to the right.

Name it clearly, for example:
- `Backup - Start`
- `Backup - Mobile dashboard`

Do this in its own `use_figma` call and return the created node ID.

### 4. Inventory the Existing Screen

Inspect the target frame before searching the library.

Use `use_figma` to gather:
- top-level section instances
- each section's `mainComponent`
- whether that component is local, remote, or missing
- nested published components already used inside each local wrapper
- exposed text and variant properties when present

Prefer exact keys over names. Names are only hints.

Useful read-only inventory pattern:

```js
(async () => {
  try {
    await figma.setCurrentPageAsync(figma.root.children.find(p => p.id === "PAGE_ID"));
    const frame = await figma.getNodeByIdAsync("FRAME_ID");
    const sections = frame.findAll(n => n.type === "INSTANCE").map(inst => {
      const mc = inst.mainComponent;
      const cs = mc?.parent?.type === "COMPONENT_SET" ? mc.parent : null;
      return {
        instanceId: inst.id,
        instanceName: inst.name,
        componentName: mc?.name ?? null,
        componentKey: mc?.key ?? null,
        componentSetName: cs?.name ?? null,
        componentSetKey: cs?.key ?? null,
      };
    });
    figma.closePlugin(JSON.stringify({ createdNodeIds: [], mutatedNodeIds: [], sections }));
  } catch (e) {
    figma.closePluginWithFailure(e.message);
  }
})()
```

### 5. Build a Component Map From the Design System

Prefer authoritative sources in this order:
1. Existing screens in the same library or workfile that already use the system
2. Known library pages inspected directly with `use_figma`
3. `search_design_system` as a fallback only

When using `search_design_system`, remember:
- results may include unrelated team or community libraries
- broad queries are useful for discovery, but do not trust them without verifying the actual file or page
- once the right library is known, prefer direct inspection of that file over repeated search calls

For each candidate, capture:
- component or component-set key
- exact variant name
- whether the section is a one-to-one swap or a composition
- text property keys or nested instance properties needed for overrides

Do not default blindly to the library's primary or default variant.

Before choosing a variant, inspect the original node for:
- semantic cues from the name, copy, and usage context
- visual cues such as fills, strokes, effects, corner radius, and typography treatment
- existing variant-like traits already visible in the screen, such as primary vs secondary button treatment

Then compare those cues against the available component-set variants and choose the closest match. If the family is correct but the variant match is ambiguous, call that out instead of silently using the default variant.

### 6. Decide Section Strategy

Use these heuristics:

- `exact-swap` if a library component matches the section's job and structure closely enough that `swapComponent()` or a direct replacement preserves intent.
- `compose-from-primitives` if the section is really a container around library pieces such as avatar, badge, buttons, metrics, or nav items.
- `blocked` if the design system lacks the composite, the library is not published, imports fail, or the section should remain bespoke.

Common patterns:
- Header summary blocks are often `compose-from-primitives`, not one component.
- Alerts and metrics often have strong `exact-swap` candidates.
- Appointment or patient cards often require composition unless the system explicitly ships those domain cards.
- Bottom nav bars are frequently custom containers built from nav-item primitives.

### 7. Update One Section At A Time

Never rewrite the entire screen in one script.

For each section:
1. Read the current node IDs.
2. Import or locate the library component.
3. Match the closest variant to the original section before swapping or rebuilding.
4. Detect whether the parent uses auto-layout.
5. Create or swap only that section.
6. Return all mutated node IDs.
7. Validate with `get_screenshot`.

Prefer `swapComponent()` when the existing node is already an instance of a compatible family and you want to preserve overrides.

Prefer rebuilding beside the original when:
- the old section is a local wrapper around mixed content
- you need to compare the result visually before replacing the original
- you are composing from multiple primitives

When the parent is not auto-layout, treat replacement as a layout-risk operation.

For non-auto-layout parents:
- preserve `x` and `y` explicitly
- preserve width and height explicitly when the replacement should occupy the same footprint
- do not assume the new instance will inherit the old node's position or size
- warn the user that absolute-positioned or grouped parents can cause drift after swaps or rebuilds
- suggest converting the parent to auto-layout only when the user wants structural cleanup, not as the default move

### 8. Handle Import Failures Explicitly

If `importComponentSetByKeyAsync()` or `importComponentByKeyAsync()` fails or times out:
1. Stop.
2. Do not continue making unrelated edits and pretend the section is connected.
3. Check whether exact component keys already exist elsewhere in the target file.
4. If the library file is accessible, verify the exact component key there.
5. Try importing the exact component key instead of the component-set key.
6. If imports still fail, mark the section `blocked` and report the blocker clearly.

Treat these as real blockers:
- published key exists in the library but import times out
- `search_design_system` finds the family, but the target file cannot import it
- only nested primitives can be imported, not the intended composite

### 9. Validate What Actually Changed

After each section:
- screenshot the changed section, not only the full frame
- confirm placeholder text is gone
- confirm the instance is really linked to a library component
- confirm spacing did not regress

At the end, validate the full screen screenshot as well.

## Writing Rules

- Work incrementally and preserve a backup.
- Prefer direct library inspection over noisy search results.
- Prefer exact component keys over names.
- Match the variant to the original visual treatment, not just the correct component family.
- Preserve position and size explicitly when replacing content inside non-auto-layout parents.
- Use imperative evidence in the report: node names, keys, component families, and whether the final node is local or library-backed.
- Do not claim full reconnection when the result is still a local shell around a few shared children.
- If a section must remain bespoke, say so and explain why.

## Deliverable Format

When closing the task, report:
- `Swapped`: sections replaced directly with library instances
- `Composed`: sections rebuilt from library primitives
- `Already connected`: sections that were already valid
- `Blocked`: sections that could not be connected, with the concrete reason

If everything is blocked, say that plainly and include the exact failure mode instead of a vague summary.
