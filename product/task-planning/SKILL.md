---
name: task-planning
description: Use when planning a version's build from a design — the plan turn that writes the build's checklist with planBuild, one item per feature the version carries in build order, after a Foundation item when the version needs one.
metadata:
  aep:
    kind: platform
    audience: [design]
---

# Task planning

The plan turn writes the checklist of one build. The platform computed the
**Version scope** section of the instruction: the features that this version
builds, the features that each one needs, the product-wide requirements that it
carries, and the stories that it holds back. You do not add or drop a feature.
You put the items in order, and you write the note of each item.

The coding agent works the checklist top to bottom, one item at a time, and
reads the specs itself. The checklist tells it the order and what the specs do
not say in one place.

## The checklist

Call `planBuild` with all the items:

1. **Foundation** (`"foundation"`), first, when the build has work that no
   single feature owns: the setup of each component that the version builds for
   the first time, and the product-wide requirements that the version carries.
   When the scope has product-wide requirements, Foundation is necessary. A
   version that does not set up a component and has no product-wide
   requirements has no Foundation item.
2. **One item for each feature in the scope** (`"F2"`). Put each feature after
   the features that it needs.
3. With no feature in the scope, one item, `"spec"`, for the whole design.

For each item:

- `components`: the design components that the item changes. A component
  serves a feature when the `stories` of its `design.json` cite stories of that
  feature. Foundation names each component that it sets up.
- `note`: one or two sentences. Write what the coding agent must know before it
  starts the item and cannot read in one file: work that crosses components
  ("the web app calls the API's `GET /greeting`"), an order inside the item, a
  held-back story that the item must not build. Do not repeat `design.json`,
  `openapi.yaml`, the prototype or the feature file.

A later `planBuild` call replaces the checklist. Call it again only to correct
a refusal.

## Gaps

- A story that no component cites is a gap in the design.
- A system that the PRD names and that no design edge reaches is a gap in the
  design. The dependencies of a component are its `design.json`
  `dependencies[]`, and nothing else.
- The platform makes the gate issues (provisioning, external values). You make
  no item for a gate.

Make no item for a gap. Name each gap in your final text, and recommend the
change to the design.

## When the tool refuses

The result names the fix. UNKNOWN_COMPONENT lists the known components.
UNKNOWN_ITEM, MISSING_ITEM, DUPLICATE_ITEM and ITEM_ORDER list the items that
the version carries, in an order that builds. Correct the checklist and call
`planBuild` again.
