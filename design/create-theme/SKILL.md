---
name: create-theme
description: Step-by-step workflow for creating a new theme. Use when asked to "create a theme", "make a new theme", or any request to author a new theme for Baan.
---

# Theme Creation Workflow

Follow this workflow when creating a new theme for the blog system.

## Required Reference

**Always read `docs/theme/ai-agent-built-guide.md` first** — it is the authoritative reference for creating themes with AI agents.

Additional references:
- `docs/theme/README.md` — Overview of both theme types
- `docs/theme/admin-generated-guide.md` — Admin UI AI-generated themes (different system)

## Step 1: Research Existing Themes

Investigate ALL builtin themes in `themes/` directory:

| Theme | Key Characteristics |
|-------|-------------------|
| `default` | Clean, minimal, Inter font, sidebar with categories/tags |
| `geek` | Terminal-ish, JetBrains Mono, text-only, no images |
| `news` | WSJ-inspired, Merriweather, editorial grid, right sidebar |
| `the-publish` | Dark, Obsidian-style, left tree nav + right sidebar |
| `terminal` | Dark terminal, JetBrains Mono, no images |
| `monograph` | Minimal B&W, ultra-thin header, right TOC with scroll progress |

For each: check concept, color scheme, layout approach, and unique features.

## Step 2: Differentiation Analysis

Identify how the new theme differs from existing ones. Must be clearly distinct — not a minor variation of an existing theme.

## Step 3: Approach Decision

| Approach | When to Use |
|----------|-------------|
| Config-Driven (config.json only) | Minor visual changes |
| Full Custom (TSX components) | **Always for builtin themes** |

If adding as a builtin theme, **full custom is mandatory**.

## Step 4: Present Proposal to User

Before implementing, present:
- Design concept and visual direction
- Color palette (primary, accent, background)
- Layout approach (grid, list, magazine, etc.)
- Key differentiating features
- Font choice (specified as a `font` object in `theme.json` — see "Font Declaration" below)

**Ask for reference URLs.** Request 1–3 URLs of real sites that match the intended look and feel. Reference URLs dramatically improve implementation quality — typography decisions, spacing rhythms, and interaction patterns are much clearer from a live example than from a text description alone.

```
Before I implement, could you share 1–3 reference sites
that match the visual direction you have in mind?
```

**Wait for user approval (and reference URLs) before proceeding.**

## Step 5: Implement

### Theme Directory Structure

```
themes/my-theme/
├── theme.json              # Metadata: name, displayName, font, ai
├── config.ts               # Theme configuration
├── prompts/                # Theme Provenance (required)
│   ├── concept.md          # Design concept & principles
│   └── generation.md       # Optional: generation prompt
├── styles/theme.css         # CSS variables (:root)
├── components/
│   ├── layout/Layout.tsx    # Main layout
│   └── post/
│       ├── PostCard.tsx     # Article card
│       └── PostContent.tsx  # Article body
└── templates/
    └── home-template.tsx    # Home page template
```

### Required Files

1. **`theme.json`**: include `name`, `displayName`, `font` (see "Font Declaration" below), and `ai` field
2. **`config.ts`**: **Required — build fails without it** (`Module not found: Can't resolve '@/themes/my-theme/config'`)
3. **`prompts/concept.md`**: required — documents the theme's design concept and principles. Write in **English**.
4. **Components**: Follow existing theme directory conventions
5. **CSS**: Define theme variables in `styles/theme.css`
6. **Public CSS**: `cp themes/my-theme/styles/theme.css public/themes/my-theme/styles/`

### theme.json `ai` field

Every theme must record its provenance:

```json
{
  "name": "my-theme",
  "displayName": "My Theme",
  "font": {
    "source": "google",
    "import": "Inter",
    "subsets": ["latin", "latin-ext"]
  },
  "ai": {
    "agent": "Claude Code",
    "skills": ["create-theme"],
    "generatedAt": "YYYY-MM-DD"
  }
}
```

### Font Declaration

Each theme owns its font entirely. Declare it inline in `theme.json` — the prebuild script collects every theme's spec, deduplicates identical ones, and emits `lib/generated/theme-fonts.ts` with static `next/font/google` imports. **Never edit `lib/theme/fonts.ts` to add a font.**

```json
"font": {
  "source": "google",                    // only "google" today
  "import": "Source_Serif_4",            // exact named export from next/font/google
  "subsets": ["latin", "latin-ext"],
  "weight": ["400", "600", "700"],       // required for non-variable Google fonts
  "style": ["normal", "italic"]          // optional
}
```

Two themes with identical specs share a single font instance. Different `weight` / `subsets` on the same import yield separate instances — each theme keeps exactly what it requested.

If a custom skill was used, include its name in `skills[]` and bundle the skill file at `prompts/skills/<skill-name>.md`. Both built-in and custom skill names can coexist in the array.

### Markdown Coverage Contract (read before writing PostContent)

**This is the single most important typography decision when creating a theme.**
See `.claude/rules/theme-system.md` → "Markdown Coverage Contract" for the
authoritative spec. In short:

#### Approach A — Prose-backed (recommended default)

PostContent wraps `contentHtml` with Tailwind Typography's `prose` class:

```tsx
<div
    className="prose prose-lg max-w-none prose-headings:font-semibold prose-a:text-accent ..."
    dangerouslySetInnerHTML={{ __html: contentHtml }}
/>
```

Tailwind Typography covers every markdown element out of the box (h1-h6, p, list,
table, blockquote, code, pre, img, hr, strong, em, del, mark, task list, etc.).
The theme only tweaks colors via `prose-*` utilities. **Almost every existing
builtin theme (default / geek / news / monograph / terminal / the-publish) uses this.**

Choose this unless you have a strong reason not to.

#### Approach B — Fully custom (for distinctive typography)

PostContent wraps with a custom class and the theme writes every selector itself:

```tsx
<div
    className="my-theme-prose"
    dangerouslySetInnerHTML={{ __html: contentHtml }}
/>
```

**No fallback exists.** If any selector from Category A (structural blocks,
inline, media, footnotes) is missing, that element renders as unstyled flow
text — the same regression that broke Slate's tables during its redesign.

If you pick Approach B, **every element in `.claude/rules/theme-system.md`
Category A must be explicitly styled**. Before committing, render
`docs/theme/markdown-coverage-sample.md` under the new theme and visually
audit every numbered section.

#### How to decide

| Scenario | Approach |
|----------|----------|
| Theme is a palette / font variant on a clean sans body | A |
| Theme uses Tailwind Typography's h2/h3/list/table styles as a baseline | A |
| Theme has a cohesive editorial voice that differs from `prose` (serif body + mono labels + custom list markers + rule-separated sections) | B, with the coverage sample verified |
| Theme is a dark terminal / brutalist / art-directed design where `prose` utilities feel wrong | B |

Never pick B "for flexibility". Pick B because the design genuinely conflicts with `prose`'s defaults.

### prompts/concept.md template

```markdown
# <Theme Name> — Theme Concept

## Overview
<1-2 sentence positioning statement>

## Design Principles
- ...

## Target Users
...

## Layout
...

## Typography
<font choice + rationale>

## Color Palette
<light/dark approach, key CSS variables>

## Component Notes
<any theme-specific behavior>
```

Minimal `config.ts`:
```typescript
export const themeConfig = {
    pagination: {
        activeColor: "#111111",
        hoverColor: "#f5f5f5",
    },
};
export type ThemeConfig = typeof themeConfig;
```

### After Implementation

```bash
npm run build  # Always verify build passes before finishing
```

### Verification against the Markdown Coverage Contract

**Mandatory for Approach B themes. Recommended for Approach A themes.**

1. Publish `docs/theme/markdown-coverage-sample.md` as an article (temporary — can be
   deleted after verification) or view it directly in the admin preview.
2. Switch the active theme to the one under test.
3. Walk through every numbered section (1–13) and visually confirm:
   - Headings are clearly differentiated by size (h1 > h2 > h3 > …)
   - Task list checkboxes render with custom styling (not bare browser boxes)
   - GFM tables have borders, alignment works, headers stand out
   - Footnote reference arrows (`↩`) are styled — not a raw underlined char
   - Callouts carry the pipeline's default inline colors (blue / yellow / red)
     OR your theme's overridden palette
   - Syntax-highlighted code blocks have token colors (from `.hljs-*` in globals)
   - Embedded Mermaid / YouTube / LinkCard render correctly without theme work
4. If anything flows as unstyled inline text, a selector is missing — add to `theme.css`.

## Pitfalls Learned from Real Implementations

### 1. Client Components with DOM scanning must handle client-side navigation

Next.js App Router keeps Layout mounted across page navigations. A `useEffect(fn, [])` only runs once, so DOM queries (e.g., scanning `<article>` for headings) silently return stale results after navigating to another post.

**Fix**: import `usePathname` and use it as a dependency. Also use `requestAnimationFrame` to wait one frame for the new DOM to render.

```typescript
import { usePathname } from "next/navigation";

const pathname = usePathname();

useEffect(() => {
    setHeadings([]);  // reset first
    const raf = requestAnimationFrame(() => {
        const article = document.querySelector("article");
        // ... scan headings
    });
    return () => cancelAnimationFrame(raf);
}, [pathname]);  // re-run on every route change
```

### 2. Header and content grid must use the same column template

To align header nav with the content column, use the **identical** grid template in both:

```tsx
// Layout.tsx content area
<div className="grid grid-cols-1 lg:grid-cols-[1fr_640px_200px] gap-0 lg:gap-8">

// SiteHeader.tsx — same template
<div className="grid grid-cols-1 lg:grid-cols-[1fr_640px_200px] gap-0 lg:gap-8 items-center">
```

### 3. HeaderNavigation adds `px-3` when navStyle is passed

When a `navStyle` prop is provided, `HeaderNavigation` applies `px-3 py-1.5` to each link (the default size class). The first item's left padding makes it appear offset from content below it.

**Fix**: add `[&_a]:pl-0` to the className:

```tsx
<HeaderNavigation
    className="flex items-center gap-6 text-sm [&_a]:pl-0"
    navStyle={navigationStyle}
/>
```

### 4. Use `lg` breakpoint, not `xl`, for sidebar visibility

The Admin Customizer preview panel occupies ~350px on the left. At a typical 1440px screen, the preview iframe is ~1090px — below the `xl` breakpoint (1280px) but above `lg` (1024px). Using `xl:` makes the sidebar invisible in the preview.

**Rule**: use `lg:` for layout breakpoints in themes.

## Critical Rules

- **Never modify builtin themes** (default, geek, news, the-publish, default_geek, terminal)
- **Never hardcode theme names** in lib/theme-loader.ts or lib/theme-fonts.ts
- New theme must work with auto-detection (theme.json required)
- **`config.ts` is mandatory** — omitting it breaks the build
- Use existing fonts when possible (new font = 2 lines in theme-fonts.ts)
- **Always run `npm run build`** to verify before finishing
