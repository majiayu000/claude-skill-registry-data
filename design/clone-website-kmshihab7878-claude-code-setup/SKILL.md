---
name: clone-website
description: Reverse-engineer and clone any website pixel-perfectly — extracts assets, CSS, and content section-by-section and dispatches parallel builder agents in worktrees. Triggers on "clone", "replicate", "rebuild", "reverse-engineer", "copy site", "pixel-perfect clone". Provide the target URL as an argument.
argument-hint: "<url>"
user-invocable: true
---

# Clone Website

Reverse-engineer and rebuild `$ARGUMENTS` as a pixel-accurate clone. This is not
an inspect-then-build pass: inspect each section, write an auditable component
spec, then dispatch or build from that spec.

## Pre-Flight

1. Playwright MCP is required. Test the target URL with `browser_navigate`; stop
   if browser access fails.
2. Read `TARGET.md` for URL and scope. If it is missing, create a public-safe
   target file using the project template or a minimal local template.
3. Verify the base project builds before cloning sections.
4. Ensure these output directories exist: `docs/research/`,
   `docs/research/components/`, `docs/design-references/`, and `scripts/`.

## Non-Negotiables

- Extract real content, assets, styles, layout, and behaviors from the live site.
- Do not approximate CSS when computed values can be inspected.
- Do not build a single monolithic section when the interaction or layout is
  complex; split into smaller component specs.
- Do not dispatch builders without a spec file.
- Do not skip responsive, hover, click, scroll, and stateful behavior checks.
- Do not use private data, credentials, session records, local absolute paths,
  or proprietary assets that the user is not authorized to clone.
- Every build increment must compile; builders verify `npx tsc --noEmit`, and
  final assembly verifies `npm run build`.

## Core Workflow

1. **Reconnaissance:** capture desktop/mobile screenshots, global styles,
   assets, UI patterns, interactions, and page topology.
2. **Foundation:** configure fonts, global CSS tokens, types, icons, and global
   assets before section work starts.
3. **Component specs:** for each section, capture screenshot, DOM structure,
   computed CSS, behavior states, assets, text, responsive rules, and complexity.
4. **Build/dispatch:** use focused builders for small components or subparts;
   keep spec payloads under the complexity budget.
5. **Merge:** integrate completed work, resolve conflicts, and build after each
   merge.
6. **Assembly:** wire sections into the page and implement page-level behavior.
7. **Visual QA:** compare original and clone at desktop and mobile sizes; test
   scroll, click, hover, animations, and responsive behavior.
8. **Report:** summarize sections, components, specs, assets, build status,
   visual QA, and known gaps.

## Reference Map

Read `references/clone-workflows-reference.md` when you need the detailed
playbook for:

- Playwright MCP tool mappings
- exact reconnaissance sweeps
- asset discovery JavaScript
- per-component computed-style extraction script
- component spec template
- builder dispatch and merge rules
- pre-dispatch checklist
- anti-patterns
- completion report fields
- template project guidance

## Completion Standard

The clone is complete only when:

- all sections have spec files and implemented components
- all real assets are downloaded or intentionally substituted with documented
  rationale
- desktop and mobile screenshots are compared against the source
- interactions and responsive states match the inspected behavior
- `npm run build` passes
- the final report lists known gaps honestly
