---
name: Generate Story
description: Generate a Storybook story file for a React component with baseline, edge, and a11y-focused states. Triggers on 'make a story', 'generate storybook for', 'add stories'. Produces a CSF3 story placed next to the component and matching repo conventions.
---

## Purpose

Ensure every new or touched component has a Storybook entry covering baseline, loading, error, empty, and a11y-relevant states, without the developer re-deriving the skeleton every time.

## When to Invoke

- A new component is added under `frontend/src/components/`.
- A reviewer asks for visual coverage of a touched component.
- Before running `/skill-accessibility-check` or a visual regression sweep.

## When NOT to Invoke

- For page-level components that are covered by end-to-end tests only.
- For pure utility modules with no visual output.
- For components whose props require server-only data with no safe mock.

## Inputs

- **component**: path to the component file.
- **states** (optional): subset of `default,loading,error,empty,long-content,rtl`. Default is all applicable.

## Procedure

1. Read the component file and infer its props interface.
2. Pick up existing story conventions from a sibling `*.stories.tsx` in the same directory (title pattern, decorators, args).
3. Create a CSF3 story with:
   - Typed `Meta<typeof Component>`.
   - One `Story` per requested state.
   - USWDS theme decorator if the component uses USWDS classes.
   - Mock data from the nearest `__factories__` or `test-utils/` directory; generate a factory via `/skill-generate-factory` if none exists.
4. Add a11y-focused variants: long labels, RTL layout (if applicable), focus-visible.
5. Write the file as `<Component>.stories.tsx` next to the component.
6. Run `npm --prefix frontend run storybook:build` smoke check (optional, on request).

## Outputs

- New story file at `frontend/src/components/.../<Component>.stories.tsx`.
- Summary of generated stories and any `TODO` markers where realistic props could not be inferred.

## Safety

- Never fetches real data; stories use synthetic fixtures only.
- Never embeds PII in story args.
- Never overwrites an existing stories file; if present, augments with missing states and notes the diff.
- FedRAMP: stories must never reference production URLs or tokens.

## Examples

**Example 1 — New component.** `OpportunityCard` → default, loading, empty, long-title, with-badge stories.

**Example 2 — Existing file augmentation.** Adds `error` state to an existing `SearchBar.stories.tsx`.

**Example 3 — RTL check.** Generates an RTL decorator story for an i18n-sensitive component.

## Related

- `.cursor/skills/skill-generate-factory/` — for reusable mock data.
- `.cursor/skills/skill-accessibility-check/` — run against the story variants.
- `.cursor/agents/visual-regression.md` — captures baselines from the stories.
