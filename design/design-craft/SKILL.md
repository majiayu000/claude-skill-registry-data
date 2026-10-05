---
name: design-craft
description: >
  Constraint + process skill for UI that reads "designed", not "AI-generated".
  Mandatory two-pass process (token plan grounded in the subject's world + ONE
  signature element, then self-critique) whose output is the project's root
  DESIGN.md — the design contract re-read on every UI generation. Navigation
  selection matrix, logo rule (vary expression not placement), icon discipline
  (one library, labeled), typography pairing recipe, dominant+accent color,
  copy rules — on top of a non-negotiable usability floor (focus rings,
  empty/loading/error states, WCAG AA, <=200ms). Ships with AVOID-LIST.md
  (versioned AI-tell list) and DESIGN-TEMPLATE.md (DESIGN.md template).
  Triggers: build UI, new component, design review, polish UI, "looks like AI
  made it", design system, style guide, /toh-vibe, /toh-ui, /toh-design.
triggers:
  - /toh-vibe (new projects)
  - /toh-ui (new components)
  - /toh-design (polish)
  - Any UI creation or design review request
---

# Design Craft

Two layers — never confuse them:

| Layer | What | Where decided |
|-------|------|---------------|
| **Creative layer** | Palette, type, nav, signature element — different per project | Root `DESIGN.md`, generated from `DESIGN-TEMPLATE.md` |
| **Usability floor** | Evidence-backed rules that never bend | Bottom of this file |

**Sibling files (same folder):**
- `AVOID-LIST.md` — versioned AI-tell list. Consult during identity generation and every design review.
- `DESIGN-TEMPLATE.md` — template + filled example for the generated per-project root `DESIGN.md`.

**The contract:** root `DESIGN.md` is the project's design identity. **Re-read it before every UI generation** — never work from memory of it. If it doesn't exist and UI is about to be written, generate it first (two-pass process below → template). For UI projects it is the first plan task (design-reviewer authors it before any UI work).

---

## Meta-Rule

> **Defaults are fine when chosen for the brief. Never when inherited.**

Inter, indigo-500, rounded-lg, a 3-card feature row — each is legitimate when the brief calls for it, and slop when it appears because it's the training-data median. Every value in the UI must trace to a DESIGN.md token chosen for THIS project.

---

## Two-Pass Process (mandatory before any UI code)

**Pass A — compact token plan.** Ground it in the subject's actual world — materials, place, era, mood. (A restaurant supply marketplace lives among stainless steel, wet markets, delivery bikes — not "warm and friendly".)

- 4-6 named hex colors incl. **hue-biased neutrals** (never pure gray)
- Display / body / utility typeface roles + weights
- One-sentence layout concept
- **ONE signature element** — the single bold, memorable move (distinctive hero treatment, unusual data display, strong typographic motif). One. Everything else stays quiet.

**Pass B — self-critique.** Ask: *"Would I produce this exact plan for any similar brief?"* If yes → **revise and state what changed.** Check the plan against `AVOID-LIST.md`.

Only after Pass B survives: write the plan into `DESIGN.md` and code — deriving **every** color/type/radius/motion value from it. No raw Tailwind palette colors (`indigo-500`) that bypass the tokens.

---

## Navigation Selection Matrix

| Project type | Navigation pattern |
|---|---|
| Marketing / landing | Visible top bar, 4-7 text links |
| Dashboard / app | Left sidebar with labeled icons |
| Content / docs | Top bar + secondary sidebar / table of contents |
| E-commerce | Top bar + mega menu for categories |
| Peer views (same-level sections) | Tabs |

**Hard rules, all patterns:**
1. **Never a hamburger on desktop** — hiding nav halves discoverability. Visible links at `md`+ always.
2. Nav items are **real links** (`<a>` / `<Link>`), never divs with onClick.
3. **URL reflects state** — views are shareable and back-button-safe.

---

## Logo Rule — vary expression, not placement

- **Top-left, clickable to home — always**, for apps and sites (NNGroup: returning home is ~6x harder with a centered logo).
- Brand variety comes from **wordmark treatment** (typeface, weight, spacing), a **motif**, or an **accent system** — not from moving the logo.
- Centered logo ONLY for editorial/luxury briefs that explicitly call for it, and only with a compensating home affordance (visible "Home" link).

---

## Icon Discipline

- **Exactly ONE library per project**, declared in DESIGN.md: Lucide / Phosphor / Heroicons / Tabler — plus stroke weight and size grid (e.g. 16/20/24).
- Every icon gets a **text label** — except true universals (search, close ×, chevron).
- Icon-only buttons require `aria-label`.
- **Never emoji as UI icons.**
- **"No icons" is a valid choice** — often the stronger one for editorial identities.
- Icon-tile-above-heading cards are the **#1 AI tell** (see AVOID-LIST). Icons support content; they don't headline it.

---

## Typography Pairing Recipe

Formula: **characterful display + complementary body + optional mono/data face.**

- **Inter / Geist are body/utility faces ONLY** — never the personality carrier.
- Use **weight extremes**: pair 100-200 against 800-900 instead of everything at 400-600.
- Hero: **3x+ size jump** from body. Scale ratio **>= 1.25**. Body measure **65-75ch**. `tabular-nums` on any column of numbers.
- Category starting points — **rotate; never converge across projects**:
  - Editorial / food / lifestyle → Fraunces, Newsreader
  - Technical / data → IBM Plex family
  - Startup / product → Cabinet Grotesk, Satoshi
  These are prompts, not defaults. Pick for the brief; if the last project used it, pick differently.
- Thai: IBM Plex Sans Thai / Noto Sans Thai / Anuphan / Sarabun. Next.js: load via `next/font` (self-host, no layout shift) — never a raw Google Fonts `<link>`.

### Type scale (Tailwind)

```
Display / Hero:   text-4xl / text-5xl+  display face   tracking-tight
Page Title:       text-2xl  font-semibold              (24px)
Section Title:    text-lg   font-medium                (18px)
Card Title:       text-base font-medium                (16px)
Body:             text-sm   font-normal                (14px, line-height 1.5-1.6)
Small / Caption:  text-xs   text-muted-foreground      (12px)
```

Rules: headings never `font-normal` · body regular, never bold-everything · max 3 sizes per component · no long ALL-CAPS runs.

---

## Color

- **Dominant + sharp accent** — commit to a dominant character, cut it with one sharp accent. Timid even distribution reads generic.
- **Semantic status colors (good / warn / critical) are separate tokens** from the brand accent — never reuse the accent for status.
- Design **light AND dark token-first**; both stated in DESIGN.md. Dark mode is its own palette, not inverted gray.
- Palette **sourced from the subject's world** or a named cultural aesthetic — name the source in DESIGN.md.
- Neutrals are hue-biased toward the palette, never pure `#808080`. No pure `#000` text. Contrast passes WCAG AA in both modes.
- Wire tokens as CSS custom properties (Tailwind 4 `@theme` / shadcn variables): `--background --foreground --muted-foreground --border --primary --destructive` map to DESIGN.md tokens.
- No gradients on primary buttons — solid reads intentional.

---

## Copy Rules

- **Active voice.** No buzzwords (streamline, empower, supercharge, unleash).
- Buttons say **exactly what happens**: "Save invoice", not "Continue" / "Submit".
- Errors **state the fix**: "Card declined — try another card", never an apology or a stack dump.
- **Declare a case system** in DESIGN.md (e.g. sentence case everywhere) and keep it.
- Real content stance: realistic domain data, no Lorem ipsum, no "Welcome back, User! 👋". Copy follows the project language (Thai = real Thai copy, not stiff translation).

---

## Density & Spacing

Layout reflects the **real work**, not an empty template:

- **Dashboard / admin / data** → dense: tables, stat rows, real data. Not "3 floating cards + giant hero".
- **Marketing / landing** → narrative sections with substance; hero allowed but earns its space.
- **Form / settings** → vertical flow, related fields grouped.
- Mix composition: table / list / stat / section — never `Card → Card → Card`. Don't center everything.

### Spacing scale (Tailwind — use consistently)

```
2  (8px)   inline / icon gap
3  (12px)  gap within a component
4  (16px)  standard gap between elements
6  (24px)  between components / card padding
8  (32px)  between sections
12 (48px)  major page sections
```

Same level = same gap. No random `p-3` here, `p-5` there.

### Border-radius — vary by element, cap declared in DESIGN.md

```
Inputs / small buttons:  rounded-md   (6px)
Cards / dialogs:         rounded-lg / rounded-xl  (8-12px)
Avatars / pills / badge: rounded-full
Cap:                     12px (rounded-xl) for general containers
```

---

## Component Patterns (structural — visual character comes from DESIGN.md tokens)

React 19: ref is a normal prop — no `forwardRef`.

```tsx
// Card — thin border + light shadow; no gradient border, no glassmorphism, no rounded-3xl
<Card className="bg-card border shadow-sm">
  <CardContent className="p-6">{/* ... */}</CardContent>
</Card>

// Buttons — one primary per view; no gradient / 3D
<Button>Save invoice</Button>
<Button variant="outline">Cancel</Button>
<Button variant="destructive">Delete</Button>
<Button variant="ghost" size="icon" aria-label="Settings"><Settings className="size-4" /></Button>

// Form (React 19 Actions) — label above input, inline errors
<form action={formAction} className="space-y-4">
  <div className="space-y-2">
    <Label htmlFor="name">Name</Label>
    <Input id="name" name="name" />
    {state?.errors?.name && <p className="text-sm text-destructive">{state.errors.name}</p>}
  </div>
  <SubmitButton /> {/* useFormStatus() → disabled + pending label */}
</form>

// Table — muted header, hover rows, right-aligned actions; no zebra stripes, no centered content
<TableRow className="hover:bg-muted/50">
  <TableCell>John Smith</TableCell>
  <TableCell><Badge>Active</Badge></TableCell>
  <TableCell className="text-right"><Button variant="ghost" size="sm">Edit</Button></TableCell>
</TableRow>
```

---

## Motion

Motion gives feedback; it is not decoration. Fast (150-200ms), subtle, ease-out.

```tsx
<div className="transition-colors hover:bg-muted" />
<Card className="transition-shadow hover:shadow-md" />
// Framer Motion enter: { opacity: 0, y: 8 } → { opacity: 1, y: 0 }, duration 0.2, easeOut
// List stagger: 0.05 max · press: whileTap={{ scale: 0.98 }}
```

Hover ~150ms · general ~200ms · **cap 200ms** · no bounce/elastic, no dramatic entrances, no animating everything. Respect `prefers-reduced-motion`.

---

## NON-NEGOTIABLE USABILITY FLOOR

The creative layer never overrides these:

| Rule | Detail |
|---|---|
| Logo top-left, clickable to home | Always for apps/sites (NNGroup ~6x evidence) |
| No hamburger on desktop | Visible nav links at `md`+ |
| Icons labeled, one library | `aria-label` on icon-only buttons; never emoji as icons |
| Focus states | `focus-visible:ring-2 ring-ring` on every interactive element |
| Interactions <= 200ms | ease-out; no bounce |
| WCAG AA contrast | Light and dark |
| Empty states | Real sentence + next action — never bare "No data" |
| Loading states | Skeletons matching the real layout — not a centered spinner |
| Error states | Inline: what happened + what to do next |
| Hover / active feedback | Every button/row (`hover:bg-muted`, `active:scale-[0.98]`) |
| Disabled / pending | Submit buttons show working state (`useActionState` / `useFormStatus`) |

---

## Review Checklist

- [ ] Root DESIGN.md exists and was **re-read** for this generation
- [ ] Every color/typeface/radius/motion value traces to a DESIGN.md token
- [ ] Signature element present on the flagship view; everything else quiet
- [ ] Zero AVOID-LIST patterns (scan `AVOID-LIST.md` groups)
- [ ] Nav matches the matrix · logo top-left + clickable · URL reflects state
- [ ] One icon library, labeled · type pairing not Inter-as-display
- [ ] Usability floor: focus/empty/loading/error/hover/pending all present, WCAG AA
- [ ] Final: would a user tell AI made it? → must be **no**. Would two different briefs get this same design? → must be **no**.

---

*Design Craft — one identity per project, chosen on purpose, on top of a floor that never bends.*
