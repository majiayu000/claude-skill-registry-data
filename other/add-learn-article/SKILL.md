---
name: add-learn-article
description: Write and register a new Learning Hub article (Nuxt Content markdown under content/learn) with valid frontmatter, navigation entry, route list entry, and accurate product details. Use when adding or substantially rewriting a learn guide, reference, or tip.
argument-hint: "<category> <slug> <topic>"
---

# Add a learn article: $ARGUMENTS

1. **File**: `content/learn/<category>/<slug>.md`, where category is one of `theming`, `components`, `tailwind`, `best-practices` (enforced by `content.config.ts`).
2. **Frontmatter** (validated by the `learn` collection schema):
   ```yaml
   ---
   title: "…"
   description: "…" # also used for SEO and cards
   category: theming
   format: guide # guide | reference | tip
   date: "YYYY-MM-DD"
   order: 10 # sort order within the category
   tags: [colors, dark-mode]
   featured: false
   ---
   ```
3. **Writing**: follow the `document-writer` skill (active voice, present tense, task-focused headings). Use MDC components the other articles already use. Code samples must match the current Nuxt UI v4 / Tailwind v4 APIs and this app's export format (`useThemeExport`).
4. **Accuracy**: derive palette, font, shade, and radius lists from `shared/constants/theme.ts` rather than memory. Describe editor controls as they exist in `app/components/editor/`.
5. **Register**:
   - Add an item to `LEARN_CATEGORIES` in `app/utils/navigation/learn.ts`.
   - Add the route to `LEARN_ROUTES` in `shared/constants/routes.ts` (sitemap + prerender; `tests/unit/shared/routes.test.ts` checks nav ↔ routes).
6. **Verify**: `pnpm vitest run tests/unit/shared/routes.test.ts`, then `/run-app` → `/learn/<category>/<slug>` renders, the TOC works, and links resolve.
