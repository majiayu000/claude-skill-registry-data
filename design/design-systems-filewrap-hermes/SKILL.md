---
name: design-systems
description: "Reusable parts so a page never invents a new language."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [web, design, system]
    category: web
    related_skills: [web-design, design-tokens, component-states]
    web_designer_stages: [components, tokens]
---

# Design Systems Skill

A design system is a maintained set of standards for managing design at scale, so the same problem looks and behaves the same everywhere. This skill covers building foundations first, then components, then patterns and templates, with documentation for each part. It does not invent a new visual language per page. Load-on-demand only, loaded by the web-designer coordinator for its stages; never auto-loads; never contacts the user directly — the coordinator is the only router.

## When to Use

- For any site with more than a handful of pages, or any site that will grow.
- When the components stage needs an inventory that reuses parts instead of inventing new ones.
- When the tokens stage needs foundations in place before components are built on them.
- When a second page needs a part that already exists on the first, and the choice is between reusing it and improvising a new one.
- When a site has grown by accretion and the same problem now looks different on different pages.

It is not for a single one-off page with no future, where a full system would cost more than it saves. It is not a pile of components without foundations, patterns, templates or documentation — a component list alone is not a system.

## Prerequisites

- The run is active, the coordinator loaded this skill for its stage(s).
- Foundations exist or are built first: tokens are defined before components that consume them.
- The brief and direction are settled, so the system serves one identity rather than several competing ones.
- The design-tokens skill is available for the foundation layer, and the component-states skill for the component layer.
- The inventory the system records is the components stage record, so the two stages share one list rather than two competing ones.

## How to Run

1. Build foundations first: colour, type, spacing, radius, shadow and motion as tokens.
2. Build components on those foundations, one component at a time, each with a clear purpose.
3. Assemble patterns and templates from the components for repeated page shapes.
4. Document when to use each component and what not to do with it.
5. Reuse a component instead of inventing a new button per page; where no component fits, extend the system deliberately rather than improvising in the build.
6. Record the inventory so a new page can be assembled from existing parts.
7. When a page needs something the system does not have, add it to the system first, then use it — so the next page inherits the addition.
8. Review the inventory at the end of the components stage and remove any part that is unused or duplicated.
9. Check that each pattern and template is assembled from components in the inventory, not from one-off markup.
10. When a component is changed, confirm every page that uses it still reads as the same component.
11. Keep the documentation with the component: a use rule that lives elsewhere is a rule that gets lost.
12. At delivery, confirm the inventory matches the build — nothing in the build that is not in the inventory, and nothing in the inventory that is not used.

## Quick Reference

- Order: foundations, then components, then patterns and templates, then documentation.
- Foundations: colour, type, spacing, radius, shadow, motion.
- Components: reusable, one purpose each, documented with use and misuse.
- Patterns and templates: repeated page shapes assembled from components.
- Rule: reuse instead of inventing a new button per page.
- Addition rule: extend the system first, then use the new part — never improvise in the build.
- Documentation: when to use each component and what not to do with it.
- End check: unused or duplicated parts are removed from the inventory.
- Patterns: assembled from inventory components, not one-off markup.
- Change rule: changing a component keeps every page that uses it consistent.
- Delivery check: inventory matches the build, both ways.

## Procedure

### 1. What it is

A maintained set of standards for managing design at scale — foundations, reusable components, patterns, templates and documentation — so the same problem looks and behaves the same everywhere (definition: NN/g).

### 2. How Hermes applies it

Hermes builds foundations first, then components, then patterns/templates, documents when to use each component and what not to do, and reuses components instead of inventing a new button per page.

### 3. What it returns to the stage

The components stage record in `gateway/web_designer/machine.py` (`STAGE_RECORDS`) requires `inventory`, and the tokens stage record requires `tokens_path`. This skill's work fills both: the inventory lists every component with its purpose, its states, and the tokens it consumes, and the tokens stage records the path to the token set the components are built on. A component in the inventory that invents its own colour, type or spacing instead of consuming a token is not recorded as part of the system. The documentation of when to use each component, and what not to do, is recorded alongside the inventory.

Patterns and templates are recorded with the inventory as the page shapes they assemble, so a new page can be built by naming its template and its components rather than by starting from a blank page. An addition made during the build is recorded in the inventory at the same time it is used, so the inventory stays the single list of what the site is built from.

The inventory is a living list, not a snapshot taken once: every addition, change and removal during the run is recorded in it as it happens. That is what makes the final check possible — inventory against build, both ways — and what lets a later revision trust the inventory as the list of what the site is built from. A system whose inventory lags the build is a system that has stopped describing the site.

### 4. Good looks like

A new page can be assembled from existing parts without inventing a new visual language; a button is the same button everywhere.

A system that a new page can be assembled from is a system that did its job. The assembly is the test, not the inventory list. Where a page still needs a part the system does not have, the part is added to the system first, so the system grows with the site rather than behind it. That growth is what keeps the inventory true.

## Pitfalls

- Inventing a new button per page instead of reusing the one the system already has.
- Building components before foundations, so each component carries its own hardcoded values.
- Shipping a component list with no documentation of when to use each part and what not to do.
- Calling a pile of one-off components a system when there are no patterns, templates or foundations behind them.
- Letting a page drift a component's look for one use case, so the same component stops being the same component.
- Improvising a new part in the build instead of extending the system first, so the next page cannot reuse it.
- Keeping unused or duplicated parts in the inventory, so the list stops describing what the site is built from.
- Assembling a pattern from one-off markup instead of inventory components.
- Changing a component on one page and leaving the other pages on the old version.
- Documentation that lives apart from the component, so it is lost when the component moves.

## Verification

- The inventory lists every component with its purpose and the tokens it consumes; no component carries hardcoded values.
- A new page can be assembled from the inventory without a new visual language.
- The same button, in the same state, is the same everywhere on the site.
- Documentation states when to use each component and what not to do.
- Patterns and templates are recorded with the inventory, and additions made during the build are in the inventory too.
- Unused or duplicated parts have been removed from the inventory.
- Every pattern and template is assembled from inventory components.
- A changed component still reads as the same component on every page that uses it.
- At delivery, the inventory matches the build in both directions.
- The visual judger checks the related rules: consistency of components and foundations is judged there. The skill does the work and the judger checks it; the skill never grades its own output.

## Coordinator wiring

Loaded by stages: components, tokens. Returns: components stage-record key `inventory` and tokens stage-record key `tokens_path`. Judger boundary: visual judger checks the related consistency rules.
