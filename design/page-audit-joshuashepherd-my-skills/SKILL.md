---
name: page-audit
description: Holistic audit of any movemental.com page — UI, content, architecture, UX, and conversion — writes a markdown report and a standalone fix prompt.
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash, Agent, Write
---

# Page Audit

Audit a page of movemental.com: **$ARGUMENTS**

You are acting as a **senior collaborator** — someone who deeply understands the project's design system, content strategy, and technical architecture. You are not running a checklist mechanically. You are looking at this page the way a thoughtful human teammate would.

---

## Before Starting

Read these files to establish full project context:

### Design & Architecture
1. `docs/design/DESIGN.md` — The Digital Curator design spec (canonical)
2. `docs/build/prompts/stitch-to-react-migration.md` — Stitch→React migration rules and translation table
3. `src/app/globals.css` — Design tokens: `@theme inline`, `:root`, `@layer base`
4. `src/components/primitives/index.ts` — Primitive component inventory

### Project Context
5. `CLAUDE.md` — Project conventions, tech stack, architecture, constraints
6. `src/app/(site)/layout.tsx` — Site chrome (SiteNav + SiteFooter)

### Then read the actual page
7. Find and read: `src/app/(site)/<route>/page.tsx` and any sibling layout/loading/error files
8. Read every component imported by the page (follow imports at least 2 levels deep)
9. If the page has a Stitch source, read: `docs/build/stitch/<screen-name>/code.html`

---

## The Six Lenses

Evaluate the page through each lens. For every issue, note severity (**CRITICAL** / **HIGH** / **MEDIUM** / **LOW**).

### Lens 1: First Impression & User Experience
- [ ] **Clarity of purpose** — Within 3 seconds, can someone tell what this page is for?
- [ ] **Visual hierarchy** — Clear reading order via Eyebrow → Display → Prose → CTA pattern?
- [ ] **Scroll motivation** — Does each section earn its place?
- [ ] **Tonal rhythm** — Sections alternate tonal layers (default → section → elevated → midnight)?
- [ ] **Mobile experience** — Works on a phone? No cramped layouts?
- [ ] **Dead ends** — Can a user get stuck? Is there always a clear next action?

### Lens 2: Design System Compliance (DESIGN.md)
- [ ] **Semantic tokens only** — No hardcoded hex, `bg-white`, `bg-black`, `text-gray-*`, `bg-blue-*`
- [ ] **No decorative borders** — Section separation via tonal stacking, not `border-b`
- [ ] **No decorative shadows** — Only `shadow-ambient` or tonal stacking (Ghost Lift)
- [ ] **Typography** — Inter only, display headings with tight tracking, eyebrows uppercase
- [ ] **Primitives used** — Section, Container, Display, Eyebrow, Prose, SurfaceCard, FeatureSplit
- [ ] **Icons** — Lucide React only, consistent sizing, `aria-hidden` on decorative
- [ ] **Images** — `next/image` with alt text, explicit dimensions or `fill`
- [ ] **Primary is a light-switch** — `#0053db` for actions only, not large backgrounds
- [ ] **Never pure black** — `text-foreground` (#2a3439) or `bg-inverse-surface` (#101820)

### Lens 3: Stitch Fidelity
- [ ] **Content match** — Does the React page faithfully represent its Stitch source HTML?
- [ ] **Section coverage** — Are all Stitch sections translated? Nothing dropped?
- [ ] **Copy accuracy** — Headlines, body text, and data match the Stitch design?
- [ ] **Token translation** — All Stitch hex values translated per migration prompt §7 table?

### Lens 4: Information Architecture
- [ ] **Internal linking** — Links to related pages (services, contact, evidence)?
- [ ] **CTAs** — Clear, specific, appropriate for the page's funnel position?
- [ ] **SEO basics** — `<Metadata>` export with title and description, single h1, semantic HTML
- [ ] **URL structure** — Clean, descriptive route

### Lens 5: Conversion Architecture
- [ ] **Next step clarity** — Obvious what to do after reading?
- [ ] **Value proposition** — Clear why this matters, not just what it is?
- [ ] **Trust signals** — Social proof, credentials, evidence links where appropriate?

### Lens 6: Technical Architecture
- [ ] **Server Components** — No `"use client"` in page.tsx or layout.tsx
- [ ] **Layer compliance** — UI uses primitives/hooks, not raw fetch
- [ ] **Type safety** — Props typed, no `any`
- [ ] **Import hygiene** — No circular imports, clean tree
- [ ] **Tailwind v4** — Canonical classes (`aspect-4/5` not `aspect-[4/5]`, `bg-linear-to-*` not `bg-gradient-to-*`)

---

## Output: Write Two Files

### File 1: Audit Report → `reports/page-audits/<route-slug>-audit.md`

```markdown
# Page Audit: [Page Name] (`/route`)

**Audited:** [date]
**Readiness: SHIP / NEEDS WORK / BLOCKED**

## Executive Summary
[2-3 sentences]

## Scorecard
| Lens | Status | Notes |
|------|--------|-------|

Scores: STRONG / GOOD / NEEDS WORK / WEAK / BROKEN

## Detailed Findings
### [Lens Name]
#### What's Working
#### Issues
| # | Severity | Issue | Recommendation | File |
|---|----------|-------|----------------|------|

## The Collaborator Take
[3-5 paragraphs — honest, specific, constructive]

## Priority Actions
1. **[CRITICAL]** [Action] — [Why]
2. **[HIGH]** [Action] — [Why]
```

### File 2: Fix Prompt → `docs/build/prompts/page-fixes/<route-slug>-fixes.md`

Standalone prompt copy-pasteable into a fresh Claude Code session:

```markdown
# Fix: [Page Name] (`/route`)

## Context
You are working in the `movemental` repo — Next.js 16 + Tailwind v4 + shadcn/ui.
- pnpm only
- Semantic tokens only (DESIGN.md)
- No borders for sectioning — tonal stacking
- Inter font only
- Primary #0053db for actions only
- Primitives: Section, Container, Display, Eyebrow, Prose, SurfaceCard

## Changes
### Change 1: [Title]
**Why:** [rationale]
**File:** `[path]`
**Current:** [code]
**Replace with:** [code]

## Validation
1. `pnpm typecheck` — zero errors
2. `pnpm build` — completes clean
3. Visual verify at localhost:3000/[route]
```

---

## Rules

1. **Read the actual code.** Never guess based on route name.
2. **Compare against Stitch source** when available in `docs/build/stitch/`.
3. **File:line references for every issue.**
4. **Don't just flag — recommend** specific fixes.
5. **The Collaborator Take is mandatory.**
6. **Always write both files.**
7. This is a light-primary site with regional Midnight sections — not a dark-mode site.
