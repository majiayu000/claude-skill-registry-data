---
name: feature-spec
description: Use when planning a new feature, writing a design spec, or when a feature needs upfront design before implementation - provides the standard spec template for this codebase
---

# Feature Spec Writing

## Overview

Write a design spec before implementing any non-trivial feature. The spec lives in `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` and serves as the single source of truth for what gets built.

## When to Write a Spec

- New user-facing feature
- Feature that touches 3+ files
- Feature involving API integration
- Anything with non-obvious edge cases

Skip for: bug fixes, copy changes, simple style tweaks, config changes.

## Spec Template

Every spec follows this structure. Include all sections — mark any as "N/A" if truly not applicable.

```markdown
# Feature Name — Design Spec

## Overview

What are we building and why? 2-3 sentences max.

**Goal:** One sentence on the success metric or purpose.

## UX Flow

Numbered steps showing the user's journey from trigger to outcome.

1. User does X
2. System shows Y
3. User interacts with Z
4. Result: ...

## Data / Constants

Tables for any enums, categories, mappings, or config values the feature needs.
Define these upfront so implementation doesn't guess.

## API

**Endpoint:** `METHOD /path`

**Params:**
- `paramName` (type) — where it comes from

**Response type:**
```ts
type ResponseItem = {
  // full shape with comments on non-obvious fields
};
```

**Base URL:** Which base URL constant to use and any gotchas.

## URL Generation (if navigational)

Full URL pattern with every param's source documented.
Note any existing URL builders to reuse or avoid.

## Component Design

### New component: `ComponentName`

**Internal state:** What state it manages locally.

**Data fetching:** React Query hooks, query keys, caching strategy.

**Renders:** Bullet list of visual elements, top to bottom.

**Accessibility:** ARIA roles, live regions, keyboard navigation.

### Placement

Where it slots into the existing component tree. Reference the parent file and position relative to siblings.

### Model changes

Does this add fields to existing models/form values? If purely navigational/display-only, say so explicitly.

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Empty state | ... |
| Loading state | ... |
| Error state | ... |
| Rapid interaction | ... |
| Missing data | ... |

## GTM Tracking

Event shape with all fields. Use the gtm-tracking skill for conventions.

## Temporary / Experiment Markers

Any badges, flags, or hardcoded values that will be removed later. Document the removal trigger.

## Files to Create/Modify

**New files:**
- `path/to/file.ts` — one-line purpose

**Modified files:**
- `existing-file.tsx` — what changes
```

## Section Guidelines

**Overview**: Lead with WHAT, not HOW. State the goal as a measurable outcome or clear purpose.

**UX Flow**: Think from the user's perspective. Every step should be an observable action or system response. This is the section stakeholders will read first.

**API**: Copy the actual response type from the API if possible. Note any field naming surprises (e.g., `coordinates` is `[lng, lat]` not `[lat, lng]`). Call out which base URL constant to use.

**Component Design**: Focus on decisions that affect implementation — state ownership, data fetching strategy, caching. Don't describe styling in detail (Tailwind classes are self-documenting).

**Edge Cases**: The table format forces you to think about each scenario. If you can't fill in the Behavior column, you haven't designed the feature yet.

**Files to Create/Modify**: This is the implementation contract. Every file listed here maps to a task in the implementation plan.

## Checklist Before Sharing

- [ ] Could someone implement this without asking clarifying questions?
- [ ] Are all data sources (API params, form values, constants) traced to their origin?
- [ ] Does every edge case have a defined behavior?
- [ ] Are file paths concrete, not placeholder?
- [ ] Is the GTM event shape defined (if applicable)?
