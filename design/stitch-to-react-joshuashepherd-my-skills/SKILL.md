---
name: stitch-to-react
description: >-
  End-to-end Stitch screen migration: accepts a Stitch project/screen ID, fetches and caches
  HTML/Tailwind wireframes, extracts tokens, archives existing pages, converts to production
  React with shadcn/ui and Layer-5 hooks, and documents the new design layer-by-layer (L1
  tokens → L2 tailwind → L3 primitives → L4 components → L5 layouts). Use for stitch to
  react, HTML to React, wireframe migration, or any Stitch screen conversion in
  movement-leader-websites.
disable-model-invocation: true
---

# Stitch → React (full migration)

One skill. One screen. Fetch from Stitch → convert to React → document the design system layers introduced by **this screen only**.

## Invocation

```
/stitch-to-react {projectId} {screenId} [target-route]
/stitch-to-react projects/c26cbafc-…/screens/abc123 → /
/stitch-to-react homepage          # uses STITCH_ROUTE_INDEX + cache if IDs known
/stitch-to-react list              # browse Stitch projects/screens
/stitch-to-react fetch-only {projectId} {screenId}
```

Run from a **tenant repo root** (`movement-leader-websites/{slug}/`).

| Input | Resolution |
|-------|------------|
| Full resource name `projects/{id}/screens/{id}` | Parse both IDs |
| Two hex/uuid args | projectId + screenId |
| Route slug only | Look up IDs in `docs/build/stitch-migration/STITCH_ROUTE_INDEX.md` or `.stitch/designs/*.meta.json` |
| Cached slug | Reuse `.stitch/designs/{slug}.html` if present (ask refresh vs reuse) |

If IDs or route are ambiguous, ask once — then run to completion.

---

## Critical rules

1. **Archive before replace** — `page.tsx` → `page-old.tsx` (use `-old-2` if needed); never overwrite archives
2. **Design chain order** — L1 tokens → L2 tailwind → L3 primitives → L4 components → L5 layouts. Fix lower layers before upper
3. **Semantic tokens only** — `bg-primary`, `text-muted-foreground`; never wireframe hex, MD3 names, or arbitrary values (`text-[#fff]`, `p-[37px]`)
4. **shadcn/ui L3** — Card, Button, Input, Tabs, Badge, Sheet; never restyle `src/components/ui/*` — fix L1 or L4
5. **Layer 5 hooks only** — no new hooks, services, or API routes; flag gaps if missing
6. **`tenantConfig` for copy** — no hardcoded tenant or Stitch placeholder strings
7. **Server page, client leaves** — `page.tsx` is Server Component; `"use client"` only where hooks/state required
8. **Fetch via curl** — `scripts/fetch-stitch.sh` or MCP `get_screen`; never AI-fetch GCS signed URLs
9. **Lucide icons** — replace Material Symbols / icon fonts with `lucide-react`
10. **Document this screen only** — write L1–L5 docs under `docs/design/stitch-screens/{slug}/`; do not rewrite global layer docs unless this screen introduces net-new tokens

---

## Execution protocol

**Run phases 0–9 sequentially. Do not stop mid-pipeline unless blocked (no Stitch auth, missing route).**

### Phase 0 — Resolve + fetch

1. Resolve `projectId`, `screenId`, target Next.js route, cache slug
2. `get_screen` → `htmlCode.downloadUrl`, `screenshot.downloadUrl`, dimensions, title
3. Cache to `.stitch/designs/{slug}.{html,png,meta.json}` via `scripts/fetch-stitch.sh`
4. Visual audit the PNG — note sections, typography, color mode, spacing rhythm

`fetch-only` stops here.

### Phase 1 — Pre-flight

Read: cached HTML, current `page.tsx` + hooks used, `globals.css`, `tailwind.config.ts`, `tenant.config.ts`, `docs/design/layers/L*.md` (project conventions).

Extract Stitch `<head>` embedded `tailwind.config` — colors, fonts, spacing, radius.

Map required data entities → existing hooks in `src/hooks/simplified/` and `src/hooks/custom/`.

### Phase 2 — Archive

Rename target `page.tsx` → `page-old.tsx`; comment out default export; add archive header with date + screen ID.

Record old hook imports and section components for carry-forward.

### Phase 3 — L1 tokens (extract + apply)

Map Stitch palette → semantic CSS variables in `globals.css` (`:root` + `.dark`).

| Stitch artifact | Target |
|-----------------|--------|
| Backgrounds / surfaces | `--background`, `--card`, `--muted`, `--accent` |
| Text | `--foreground`, `--muted-foreground`, `--primary-foreground` |
| Accents / CTAs | `--primary`, `--secondary`, `--tertiary` |
| Borders / focus | `--border`, `--input`, `--ring` |
| Radius | `--radius` |
| Fonts | `--font-display`, `--font-body` via `layout.tsx` + tailwind |

Rules: map to **existing** semantic names first; add new vars only when Stitch introduces a distinct role; ask before changing site-wide token values; support light + dark if Stitch is dark-first.

**Write** `docs/design/stitch-screens/{slug}/L1_TOKENS.md` — see [reference/design-layer-docs.md](reference/design-layer-docs.md).

### Phase 4 — L2 tailwind (bridge)

Update `tailwind.config.ts` only where this screen needs new utilities: font sizes, spacing extensions (`py-section-gap`), max-width, effect utilities.

All colors reference `hsl(var(--*))` — no hex in config.

**Write** `docs/design/stitch-screens/{slug}/L2_TAILWIND.md`.

### Phase 5 — L3 primitives (map, don't fork)

Inventory which shadcn primitives this screen uses and how Stitch patterns map to them:

| Stitch pattern | Primitive + token classes |
|----------------|---------------------------|
| Primary CTA button | `<Button className="rounded-none px-8 py-4 …">` |
| Ghost / outline | `<Button variant="outline">` |
| Module card | `<Card>` + semantic bg |
| Form fields | `<Input>`, `<Label>`, `<Textarea>` |
| Tabs / accordion | `<Tabs>`, `<Accordion>` |
| Mobile nav | `<Sheet>` |

Do **not** edit `src/components/ui/*`. Document variant/class overrides used in L4.

**Write** `docs/design/stitch-screens/{slug}/L3_PRIMITIVES.md`.

### Phase 6 — Plan L4 decomposition

Break HTML into sections. Produce plan table:

| # | Section | Component path | Primitives | Hook | Server/Client |
|---|---------|----------------|------------|------|---------------|

Present plan if >4 new section files. Identify missing hooks → static manifest stub + flag.

### Phase 7 — Build L4 + L5

**L4** — section components under `src/components/{area}/`:

- Preserve semantic HTML hierarchy; one responsibility per file
- Static class maps for color variants (no `` `bg-${x}` ``)
- Loading / empty / error states in every data component
- `Readonly` prop interfaces; entity types from `@/lib/schemas`
- Preserve `data-stitch-id` as `{/* stitch:id */}` comments when useful

**L5** — compose Server Component `page.tsx`:

```tsx
export default function Page() {
  return (
    <>
      <Hero />
      {tenantConfig.features.chat && <AILabTeaser />}
      …
    </>
  );
}
```

Feature-gate optional sections. One `<h1>` per page.

**Write** `docs/design/stitch-screens/{slug}/L4_COMPONENTS.md` and `L5_LAYOUTS.md` — section order, shell type, route, status.

### Phase 8 — Verify

```bash
pnpm typecheck
```

Run checklist in [reference/conversion-checklist.md](reference/conversion-checklist.md).

Compare rendered page to `.stitch/designs/{slug}.png` — light and dark if applicable.

### Phase 9 — Report + index

1. Write `docs/design/stitch-screens/{slug}/README.md` — stitch IDs, route, date, cache paths, conversion status
2. Update `COMPONENT_CHECKLIST.md` row → `BUILT` or `PARTIAL`
3. Emit session report (below)

---

## React + Tailwind best practices (always)

- Function components; props down / events up; stable list keys
- Derive during render; effects only for sync/subscriptions
- `cn()` for conditional classes; group: layout → box → color → type → state
- No document shell in components (`<html>`, `<head>`, CDN scripts)
- Accessibility: heading hierarchy, `alt` on images, focus-visible (shadcn default), 44px tap targets
- Responsive from Stitch 2560px desktop base — mobile stack at `md`/`lg` breakpoints
- Reuse section components across routes; don't duplicate grids/cards

---

## Session report template

```markdown
## Stitch → React complete

**Screen:** {title} (`projects/…/screens/…`)
**Route:** /path
**Cache:** .stitch/designs/{slug}.html
**Design docs:** docs/design/stitch-screens/{slug}/

### Archived
- page.tsx → page-old.tsx

### Created
- L4: list paths
- L5: page.tsx

### Tokens / tailwind changes
- globals.css: …
- tailwind.config.ts: …

### Data wired
| Component | Hook | Status |

### Flagged
- missing hooks, PARTIAL sections, token questions

### Next
- pnpm dev + visual compare to PNG
- delete page-old.tsx when verified
```

---

## Multi-screen

Convert homepage first (establishes tokens). Subsequent screens reuse L1/L2; document only deltas per screen under `docs/design/stitch-screens/{slug}/`.

Bulk: `list_screens` → fetch all → user picks → run phases 1–9 per screen.

---

## Additional resources

- Layer doc schemas: [reference/design-layer-docs.md](reference/design-layer-docs.md)
- Verification checklist: [reference/conversion-checklist.md](reference/conversion-checklist.md)
- Project layer conventions: `docs/design/layers/L1_TOKENS.md` … `L5_PAGES.md`
