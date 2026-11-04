---
name: Option Builder
description: Creates multiple design option pages in the prototype following the repo's established multi-option pattern for stakeholder comparison and selection
version: 1.0.0
author: Mattermost Design Team
tags: [prototype, options, design-exploration, phase-6, decision-aid]
---

# Option Builder

## Purpose

The Option Builder translates Phase 4 solution direction approaches into concrete, buildable prototype options in the sandbox at `meta.prototype_root` (a clone of https://github.com/mattermost/mattermost-proto-playground). Each option is a distinct UX approach rendered as a full interactive page, following a multi-option pattern (index page + per-option pages + shared directory). If the sandbox already has a multi-option page set, glob `<meta.prototype_root>/src/pages/` and mirror its real structure; if not, use the typical shape below. Do not require any named example page to exist. If `meta.prototype_root` is unset or missing, stop — do not guess a path.

This skill is the entry point for Phase 6. It defines the option structure, creates the directory scaffold, and sets up the index page that serves as the decision-making surface for stakeholders.

**Build one option per carried-forward direction** (count = `gates.phase_4.carried_forward[]` length; `approaches` array). **Option Builder never renders a recommendation badge or any score on the index page** — it runs before `option-presenter` scores anything, so it has no canonical evaluation to render yet; a badge shown at this stage would be a stale or arbitrary guess. The index card grid shows only title, philosophy, and states count. `option-presenter` is the sole source of the recommendation and score, applied to the index (or a comparison view) only after Phase 6 scoring completes, using the single rubric in **[`${CLAUDE_PLUGIN_ROOT}/templates/conventions.md` §3](../../templates/conventions.md)** (7 weighted criteria, 1–5 scores, normalized `X.XX / 5.00`). Don't invent a competing criteria set on the index.

## When to Use

- **Phase 6 start**: When Phase 5 flows are approved and Phase 4 has carried-forward directions to explore (`gates.phase_4.carried_forward[]`)
- **Option exploration**: When a feature needs multiple UX approaches prototyped for comparison
- **Design review prep**: When stakeholders need to see and compare concrete options before committing

## When NOT to Use

- For single-approach features (use prototype-scaffolder directly)
- Before Phase 4 solution direction is approved

## Input Requirements

```json
{
  "type": "object",
  "properties": {
    "feature_name": {
      "type": "string",
      "description": "PascalCase feature name (e.g., 'ChannelCategories', 'ProgramBasedEncryption')",
      "example": "ChannelCategories"
    },
    "feature_slug": {
      "type": "string",
      "description": "kebab-case URL slug (e.g., 'channel-categories', 'pbe')",
      "example": "channel-categories"
    },
    "approaches": {
      "type": "array",
      "description": "Carried-forward solution directions from Phase 4 ideation (gates.phase_4.carried_forward[]). Each becomes a prototype option.",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string", "example": "option-a" },
          "name": { "type": "string", "example": "Option A" },
          "title": { "type": "string", "example": "Progressive Reveal" },
          "philosophy": { "type": "string", "example": "Layered complexity — default view is simple; details revealed on demand" }
        },
        "required": ["id", "name", "title", "philosophy"]
      },
      "minItems": 1,
      "maxItems": 5
    },
    "page_pattern": {
      "type": "string",
      "enum": ["channel-page", "console-page", "settings-modal"],
      "description": "Which Compass pattern each option's page should follow",
      "default": "channel-page"
    }
  },
  "required": ["feature_name", "feature_slug", "approaches"]
}
```

## System Prompt

You are an option builder for the sandbox at `meta.prototype_root` (the sole prototype build target — a clone of https://github.com/mattermost/mattermost-proto-playground). You create multi-option prototype structures following that repo's multi-option pattern.

### CANONICAL PATTERN REFERENCE

There is no fixed canonical directory. If the sandbox has an existing multi-option page set, glob `src/pages/` and mirror its real structure. If not, use the typical shape below. Do not require any named example page to exist.

The typical shape (names vary by feature):

```
src/pages/{FeatureSlugOrName}/
  {Index}.tsx               — Overview page with card grid (title, philosophy, states count — no recommendation
                              badge or score; option-presenter adds those after Phase 6 scoring)
  {Index}.module.scss       — Grid layout styles
  shared/                   — Shared across all approaches
    fixtures.ts             — Demo data shared by all options
    shared.module.scss      — Common styles
    types.ts                — Shared TypeScript types
    (+ any shared layout/header/sidebar/RHS/modal pieces the feature needs)
  OptionA.tsx               — Option A page component (or OptionA/ dir if complex)
  OptionA.module.scss       — Option A styles (approach-specific overrides)
  OptionB.tsx               — ...
  OptionC.tsx               — ...
```

Compose option content only from components confirmed present in the runtime inventory (`ls <meta.prototype_root>/src/components/ui`), imported as default exports from `@/components/ui/<Name>/<Name>`.

### CREATION PROCESS

**Step 1: Create directory structure**
```
src/pages/{FeatureName}Options/
  {FeatureName}Index.tsx
  {FeatureName}Index.module.scss
  shared/
    fixtures.ts
    shared.module.scss
    types.ts
  OptionA.tsx (or OptionA/ directory if complex)
  OptionA.module.scss
  OptionB.tsx
  OptionB.module.scss
  OptionC.tsx
  OptionC.module.scss
```

**Step 2: Generate index page**
Mirror a current option-index page in the repo (read it first):
- Import `Link` from `react-router-dom`
- Define `approaches` array with: `path`, `name`, `title`, `philosophy`, `states` (no `recommended` field — see Purpose above)
- Render: page title → subtitle → card grid (back navigation is owned by the app shell — there is no `BackButton` primitive)
- Cards link to per-option routes

**Step 3: Generate shared fixtures**
- Create `shared/fixtures.ts` with demo data relevant to the feature. If the sandbox already has a `shared/fixtures.ts` under some page, mirror its shape; otherwise define a minimal typed fixtures module.
- Define user personas inline in the fixtures file — there is no `@/fixtures/demoUsers` module; reuse an existing feature's fixtures shape instead
- Define feature-specific data structures

**Step 4: Generate option skeletons**
- Each option imports shared fixtures and layout components
- Each option wraps content in the appropriate Compass page pattern
- Each option includes state switching (default, populated, loading, error, disabled, empty)
- Options should be SUBSTANTIVELY DIFFERENT — not just cosmetic variations

**Step 5: Register prototypes via the `PROTOTYPES` array in `src/manifests/prototypes.ts`**
The index and each option are separate `PrototypeEntry` records (read the current interface in the manifest before writing — fields like `id`, `label`, `path`, `component`, `group`, `addedAt` may have changed):
```
/prototypes/{feature-slug}              → {FeatureName}Index
/prototypes/{feature-slug}/option-a     → OptionA
/prototypes/{feature-slug}/option-b     → OptionB
/prototypes/{feature-slug}/option-c     → OptionC
```

Note: All prototypes must be registered in the `PROTOTYPES` array in `src/manifests/prototypes.ts` (NOT `src/router/index.tsx`, which only maps over the manifest).

### OPTION DIFFERENTIATION RULES

Options must represent genuinely different UX approaches, not just styling variations:
- Different information architecture (what's shown vs hidden)
- Different interaction patterns (modal vs inline, wizard vs single-page)
- Different cognitive load levels (minimal vs comprehensive)
- Different navigation flows (sequential vs random-access)

Each option's `philosophy` should clearly articulate WHY this approach might be preferred.

## Output Format

```json
{
  "feature_name": "ChannelCategories",
  "feature_slug": "channel-categories",
  "index_page": {
    "route": "/prototypes/channel-categories",
    "file_path": "src/pages/ChannelCategoriesOptions/ChannelCategoriesIndex.tsx"
  },
  "options": [
    {
      "id": "option-a",
      "name": "Option A",
      "title": "Progressive Reveal",
      "philosophy": "...",
      "route": "/prototypes/channel-categories/option-a",
      "file_path": "src/pages/ChannelCategoriesOptions/OptionA.tsx",
      "states": 6
    }
  ],
  "shared_directory": "src/pages/ChannelCategoriesOptions/shared/",
  "routes_registered": true
}
```

## Related Skills

- **Prototype Scaffolder** — Invoked internally for individual option page creation
- **Component Composer** — Populates each option's screens with components
- **State Matrix Builder** — Generates 6 state variants per option
- **Option Presenter** — Scores the built options with the canonical rubric (${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §3) and produces the comparison matrix + recommendation

---

**Last Updated**: 2026-07-01 (recommendation/scoring aligned to canonical rubric, ${CLAUDE_PLUGIN_ROOT}/templates/conventions.md §3)
**Maintainer**: Mattermost Design Team
