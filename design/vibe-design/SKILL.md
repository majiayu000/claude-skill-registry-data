---
name: vibe-design
description: >
  Frontend design workflow that produces non-generic, editorial-quality UI.
  Immediately invokes the frontend-design skill for aesthetic direction before
  any code is written. Enforces a written design contract that is re-read before
  every single component — not once and forgotten. Creates separate files per
  page and component, never monolithic output. Reads DESIGN.md if present for
  exact brand tokens. Derives the design from the product's domain × audience ×
  emotion (ANTI_GENERIC.md) — killing BOTH the SaaS-generic look AND the
  anti-generic cliché (warm-cream+terracotta, the Fraunces/DM-Sans reflex,
  dark-as-premium, SaaS layouts on non-SaaS products). Reads SITE_TYPE_PLAYBOOK.md
  for domain-specific design worlds well beyond software.
  Triggers on "design:" prefix, "style this", "make this look better",
  "redesign this page", "the UI needs work", "can you polish",
  "do a design pass", "it looks too plain", "it looks generic",
  "it looks like a saas dashboard", "make separate pages".
  Two review modes: "design: critique" judges the design + preview and writes
  vibe/design/critique.md (MUST-FIX / CONSIDER / NIT) without changing anything;
  "design: fix [must|must+consider|all]" applies those notes, regenerates the preview,
  and re-critiques. Used at the design gate before the design is signed off.
  Always use when the goal is visual — aesthetics, layout, feel, interactions.
  Never use for logic, data, tests, or spec changes.
---

# Vibe Design Skill

Handles all visual styling for a vibe project.
Invokes frontend-design first. Commits to a design contract.
Re-reads that contract before every component. Creates separate files.

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

**The separation of concerns:**
- **vibe agent** — spec compliance, data flow, logic, tests, docs
- **vibe-design** — aesthetics, layout, feel, interactions, visual polish

---

## CRITICAL: How this skill works

The reason AI design tools produce generic output is that they commit to a
direction once and then forget it during implementation.

This skill works differently:
1. **frontend-design is invoked first** — before reading any project files
2. **A design contract is written** — specific, named, irreversible choices
3. **The contract is re-read before every single component** — not once, every time
4. **Each page gets its own file** — never one monolithic output

If you find yourself about to write a white card with shadow-md — stop.
Re-read the design contract. If the contract says "no cards" — no cards.

---

## Step 1 — Invoke frontend-design IMMEDIATELY

Before reading project files. Before understanding the request.
Before doing anything else.

**Invoke the first-party `frontend-design` skill now** — via the Skill tool
(`frontend-design`, or the plugin-qualified `frontend-design:frontend-design`),
not by reading a file path. It ships as a skill/plugin in the current ecosystem;
a hardcoded `~/.claude/skills/...` path does not resolve under a plugin install.

This is not optional. This is not "if installed." This is the first action.

**Defer aesthetic direction to frontend-design** — it owns the typography,
colour, motion, and anti-generic principles. This skill (vibe-design) layers the
vibe-specific mechanics on top: persisting a design contract, re-reading it
before every component, one file per page/component, and grounding in
SPEC/CODEBASE. Do not re-derive aesthetic rules here that frontend-design already
provides; `references/ANTI_GENERIC.md` and `SITE_TYPE_PLAYBOOK.md` are
supplementary reminders, not the source of truth.

If the `frontend-design` skill is genuinely unavailable in the session — proceed
using `references/ANTI_GENERIC.md`, but note the output quality will be lower.

**After reading frontend-design — internalise this:**
> "I will DERIVE the design from this product's domain × audience × emotion
>  (ANTI_GENERIC.md), not stamp on a house style.
>  I will not produce a SaaS dashboard — and I will not reach for the
>  anti-generic cliché either (warm-cream + terracotta, the Fraunces/DM-Sans
>  reflex, dark-as-premium, a 140px editorial hero on everything).
>  I will pick the archetype that fits THIS domain, derive the palette and
>  typography from it, and be able to justify every choice from the audience.
>  Every component will reflect that derived direction."

---

## Step 2 — Read project context and DESIGN.md

Read in this order:

**First — check for DESIGN.md (highest priority):**
```bash
ls DESIGN.md 2>/dev/null && echo "DESIGN.MD EXISTS" || echo "NO DESIGN.MD"
cat DESIGN.md 2>/dev/null
```

If DESIGN.md exists — its tokens are the law. Exact hex values. Exact font names.
Exact shadow formulas. Do not approximate. Do not substitute.
DESIGN.md overrides DESIGN_SYSTEM.md where they conflict.

**Then read project files:**
1. `vibe/CODEBASE.md` — stack, component library, file paths
2. `vibe/SPEC.md` — UI specification, screens, components
3. `vibe/DESIGN_SYSTEM.md` — existing tokens
4. `CLAUDE.md` — code style, naming conventions

Extract:
- Styling approach: Tailwind / CSS Modules / styled-components / vanilla CSS
- Framework: React / Vue / Next.js / vanilla — determines animation library
- Platform: mobile-first or desktop
- Pages and screens that need design work

---

## Step 3 — Write the design contract

This is the most important step. Do not rush it.

Read `references/ANTI_GENERIC.md` in full — do the domain × audience × emotion
derivation and pick the archetype.
Read `references/SITE_TYPE_PLAYBOOK.md` — find the matching domain / design world
(software is only a few entries — most products aren't SaaS).

Then write the design contract. This is a concrete, named document.

```
═══════════════════════════════════════════════════════════
DESIGN CONTRACT — [Project name] — [date]
═══════════════════════════════════════════════════════════

DERIVATION (fill first — everything below traces to this):
  Domain:   [what world — e.g. children's education, private banking, taqueria]
  Audience: [who + what they find credible/delightful]
  Emotion:  [the one feeling in 3 seconds]
  Archetype: [from ANTI_GENERIC.md — e.g. Playful / Swiss / Luxe / Crafted …]
  Theme:    [light | dark] — with the reason it fits this domain
            (do NOT pick dark for "premium"; do NOT default to warm cream)

ONE FITTING BOLD CHOICE: [Name it — bold AND right for this audience]
  (bold ≠ random; a private bank being loud is wrong, not brave)

TYPOGRAPHY CONTRACT: (chosen for the archetype/emotion — justify, don't reflex)
  Display font: [exact name — for THIS archetype; not the Fraunces/DM-Sans reflex]
  Body font: [exact name — NOT Inter/system-ui]
  Mono font: [exact name, if used]
  Why these: [one line tying the pairing to the emotion]
  Display size: [fits the archetype — Luxe may be small+airy, not 140px]
  Weight contrast: [display weight vs caption weight — the gap is the design]

COLOUR CONTRACT: (DERIVED via ANTI_GENERIC.md Steps A–D)
  Theme + neutrals: [near-white/near-black hexes in the hue's TEMPERATURE —
                     cool brand → cool neutrals, not warm cream by default]
  Brand hue: [one specific, slightly-unexpected shade — NOT the category default
              (not SaaS blue, not eco green, not reflex terracotta)]
  Brand appears on: [list exactly where] · Brand does NOT appear on: [rest]
  (Playful/Maximalist archetypes may use multiple saturated hues — say so.)

MOTION CONTRACT:
  Library: [CSS + View Transitions (default) | Framer Motion | GSAP — only if needed]
  Energy: [matches archetype — Luxe slow/few · Playful springy · Swiss minimal]
  Hero / sections / interactions: [specific approaches] · reduced-motion honoured

FILE STRUCTURE:
  [Every file to be created — one page per file, one component family per file]

BANNED FOR THIS PROJECT:
  Enemy 1 (SaaS generic): Inter display · blue/indigo/violet primary · white
    shadow-md cards · centered hero · 3-col icon grid · gray-100 sections
  Enemy 2 (anti-generic cliché): warm-cream + terracotta as default · the
    Fraunces/DM-Sans reflex · dark-as-premium · 140px editorial hero on a
    non-editorial product · SaaS layout on a non-SaaS domain
  [add project-specific bans]
═══════════════════════════════════════════════════════════
```

**Save the contract:**
```bash
mkdir -p vibe/design
# Write contract to file — this gets re-read before every component
```

Save as `vibe/design/CONTRACT.md`.

**Present to user:**
> "Design contract written.
> Bold choice: [state it clearly]
> This will look like: [one sentence description]
> Files to create: [N files — list them]
> Proceeding."

Wait for approval only if 3+ components. Otherwise proceed immediately.

---

## Step 3.5 — Write the reviewable preview (a click-through prototype)

A contract is a document. A person cannot judge a *look and feel* by reading one —
they judge it by seeing it. Before building any production files, render the
direction as a single self-contained prototype the reviewer can click through:

Write **`vibe/design/preview.html`** — ONE standalone file:
- **All CSS + the design tokens inlined verbatim** from the contract (no external
  stylesheet, no build step; a normal Google-Fonts `<link>` is fine). It opens
  directly in a browser.
- **Every primary screen of THIS product**, each a realistic, fully-laid-out mock
  populated with plausible sample content — real-looking copy and data, never lorem
  or blank boxes.
- **Navigation between the screens** — a top nav / tab bar / clickable links wired
  with a little inline `<script>` that shows/hides each screen — so the reviewer
  follows the actual product FLOW end to end, not one static frame.
- **The states that matter**: empty, loading, a populated list, a detail view, an
  error — wherever they carry weight for this product.
- **One compact style reference** (palette swatches, type scale, buttons, inputs,
  and the contract's signature element) on a single screen, so the tokens are
  visible in isolation too.

This is a **preview only — never imported by app code**, and it is the one place a
single all-in-one HTML file is correct (Step 4's "one file per page" rule governs
production files, not this artifact). A person approves the design by clicking
through this prototype; keep it current on every design refine. Downstream
orchestrators may gate the build on this file — a design gate that shows only a
Markdown contract has nothing a human can actually approve.

**Present to user:**
> "Preview written: vibe/design/preview.html — open it to click through
> [N] screens ([list]). Approve the direction here before I build production files."

---


**At a design gate, stop here.** When `design:` runs as the design gate (vibe-new-app
Step 10C, `vibe-mode: run`, or a caller that asks for the Step 3.5 checkpoint), end after
the contract, tokens and preview: the sign-off is on this, and the production UI files
(Steps 4-7) are built afterwards by the build's UI tasks from the approved contract. In
manual mode the person approves here in chat and you continue as usual.

## Step 4 — Establish file structure BEFORE writing any code

**Rule: one file per page, one file per component family. Always.**

Never put multiple pages in one production file.
Never create a single wireframe.html or index.html with everything.
(The sole exception is `vibe/design/preview.html` from Step 3.5 — the reviewable
prototype, which is not production code.)

If the user asks for a wireframe.html — respond:
> "I create separate files per page for maintainability and because
> vibe-design produces production files, not wireframes.
> File structure: [list from contract]. Starting with [first page]."

Create the structure:
```bash
mkdir -p src/pages src/components src/lib src/styles

# Create animation tokens file FIRST — everything imports from here
# Write src/lib/animations.ts (or CSS keyframes) with motion tokens whose ENERGY
# matches the contract's archetype (Luxe slow/few · Playful springy · Swiss minimal).
# Prefer CSS transitions + View Transitions; use a motion library only if the
# contract's Motion section calls for one. Always gate on prefers-reduced-motion.

# Create CSS tokens file with values from the contract
# Write src/styles/tokens.css with all CSS custom properties

# Announce
echo "Structure created. Building [N] files:"
echo "[list all files from contract]"
echo "Starting with [first file]."
```

---

## Step 5 — Implement — one file at a time

### MANDATORY before each file: Re-read the design contract

```bash
cat vibe/design/CONTRACT.md
```

Then ask: does my plan for this component implement the bold choice?
State out loud:
> "Building [filename]. Bold choice implementation: [how this component shows it].
> Using [display font] at [size]. Brand colour on [what, if anything]."

If you cannot answer how this component implements the bold choice — redesign
the approach until you can.

### Write the implementation

For each component:
1. Implement the design
2. Cover all states: default, hover, active, focus, disabled, loading, empty
3. Mobile-first if project is mobile-first

### Per-component self-check (mandatory before moving to next file):

- [ ] Bold choice is visible and intentional in this component
- [ ] Display font used for headlines — NOT Inter, NOT system fonts
- [ ] Brand colour appears only where the contract specifies
- [ ] Animation imported from `src/lib/animations.ts` — not inline
- [ ] No pattern from the BANNED LIST is present
- [ ] This component could not be mistaken for a generic SaaS dashboard

If any check fails — fix before moving to the next file.

### Stack-specific guidance

**React + Tailwind + Framer Motion:**
```typescript
// Tokens in tailwind.config.js, not hardcoded
// All animations from src/lib/animations.ts
// next/font for font loading
// motion.div with variants from animations.ts
```

**React + CSS Modules + Framer Motion:**
```typescript
// CSS custom properties in tokens.css
// BEM class names in .module.css
// Framer Motion for all transitions
```

**Vue 3:**
```typescript
// CSS custom properties globally
// Vue Transition + CSS @keyframes
// IntersectionObserver for scroll reveals
// No Framer Motion (React only)
```

**Vanilla HTML + CSS + JS:**
```javascript
// CSS custom properties at :root
// IntersectionObserver for scroll triggers
// CSS @keyframes with animation-delay for stagger
// No dependencies required
```

---

## Step 6 — Full consistency check after all files

After all files written:

**Screenshot verification (do this first — actually look, don't self-report):**
Render the built UI and inspect it visually rather than checking boxes from
memory. Run the app (`preview_start` / dev server) or open the page in the
browser, take a screenshot of each page at desktop and mobile widths, and judge
the *rendered image* against the contract and the checks below. This is the
"screenshot test" from `references/ANTI_GENERIC.md` — run it for real. Iterate on
what the screenshot reveals (spacing, hierarchy, the bold choice actually
landing), not on what the code says it should look like.

**Accessibility:** if the session has `design:accessibility-review`, run it
(contrast ratios, keyboard nav, focus states, `prefers-reduced-motion`); else
spot-check contrast on text/brand-colour pairs and confirm focus-visible states.

**Derivation held:**
- [ ] The design still reads as THIS domain/audience (domain test) — not re-skinnable
- [ ] Palette was derived (theme + hue + temperature-matched neutrals), not fallen
      back to warm cream or dark-for-premium
- [ ] Fonts fit the archetype — not the reflex Fraunces/DM-Sans pairing

**Typography:**
- [ ] Display + body fonts are the contract's — everywhere; display ≠ body
- [ ] No Inter/system-ui as display unless the contract genuinely chose it
- [ ] Weight contrast (heavy display vs light caption) is visible

**Colour:**
- [ ] One brand hue, only where the contract specifies (or the multi-hue set a
      Playful/Maximalist contract declared)
- [ ] Neutrals match the brand's temperature; theme matches the contract
- [ ] Brand hue is not the category default (SaaS blue / eco green / reflex terracotta)

**Motion:**
- [ ] Motion energy matches the archetype; `prefers-reduced-motion` handled

**Layout:**
- [ ] The fitting bold choice is visible; structure fits the domain (not a SaaS
      scroll-journey forced onto a non-SaaS product)
- [ ] No unintended SaaS defaults (centered hero / 3-col icon grid / shadow-md cards)
      unless the contract chose them

**Files:**
- [ ] Every page is a separate file
- [ ] No monolithic output

---

## Step 7 — Update docs and commit

Update `vibe/DESIGN_SYSTEM.md` with the design contract as the direction section.
Update `vibe/TASKS.md` with what was built.

```bash
git add src/ vibe/
git commit -m "design([scope]): [bold choice] — [files created]"
```

Signal done:
```
✅ Design complete — [scope]
   [One sentence: what it looks like]
   Bold choice: [restate]
   Files: [N files created — list them]
   Contract: vibe/design/CONTRACT.md
```

---

## Mode: `design: critique` — judge the design, change nothing

Run this after `design:` (and before the design is signed off at the design gate).

1. Invoke the **frontend-design** skill for the lens. Read `DESIGN.md` (if any),
   `vibe/design/CONTRACT.md`, `vibe/DESIGN_SYSTEM.md` and `vibe/design/preview.html`.
2. Judge the design against the frontend-design principles and `references/ANTI_GENERIC.md`:
   is it distinctive or a default dashboard; type hierarchy and pairing; palette; spacing
   and rhythm; one real signature element; empty / loading / error states;
   responsiveness; contrast and accessibility.
3. Judge `preview.html` **as a click-through prototype**: does it render the product's
   primary screens (not just one) with navigation between them and realistic sample
   content, so the *flow* can be reviewed? A single-screen or style-tile-only preview is a
   MUST-FIX.
4. Write `vibe/design/critique.md` with exactly three sections, headed exactly like this so
   tools can count them:
   ```
   # Design critique — [project] — [date]

   ## MUST-FIX ([N])
   - **[short title].** [specific, actionable note — cite the token/component/file:line]

   ## CONSIDER ([N])
   - ...

   ## NIT ([N])
   - ...
   ```
5. **Do not edit the design, the preview, or any code.** End with the three counts.

## Mode: `design: fix [must|must+consider|all]` — apply the critique

1. Invoke frontend-design. Read `vibe/design/critique.md` and the design files above.
2. Apply the notes in scope (`must` = MUST-FIX only; `must+consider`; `all`) to
   `DESIGN.md` / `vibe/design/CONTRACT.md` / `vibe/DESIGN_SYSTEM.md` — the smallest change
   that resolves each note, following its intent. Keep the direction's tokens and
   signature coherent; **do not invent an unrelated new look.**
3. **Regenerate `vibe/design/preview.html`** so every change is visible in the rendered
   preview (Step 3.5 rules).
4. Re-run `design: critique` and rewrite `vibe/design/critique.md` with the new counts.
5. Do not build app features or start a build. Commit: `design(critique): apply [scope] notes`.

At the design gate in autonomous mode, vibe-new-app / `vibe-mode: run` run
`design:` → `design: critique` → one `design: fix must` pass, then record the gate
(vibe-mode `references/HEADLESS.md` §3).

---

## Non-negotiable rules

**frontend-design is read in Step 1. No exceptions.**

**The design contract is written before any code. No exceptions.**

**The contract is re-read before each file. No exceptions.**

**One file per page. One file per component family. No exceptions.**

**Generic is failure.** A SaaS dashboard means the skill failed.
Not played it safe — failed. Retry from Step 3.
