---
name: vibe-design-md
description: >
  Generates a DESIGN.md file for any website URL or fetches a pre-built one
  from the awesome-design-md collection (55+ sites). DESIGN.md captures the
  complete design system of a real product — exact hex/oklch values, font
  families, spacing scales, shadow formulas, component states, do's and don'ts
  — in a format vibe-design reads to produce pixel-accurate matching UI.
  Three modes: (A) fetch a pre-built DESIGN.md from the catalog by site name
  (instant, exact tokens); (B) generate one from any URL by reading the site's
  rendered CSS and visual language (~2 min); (C) INGEST a design the user already
  made — a mockup/screenshot image (PNG/JPG), a prototype HTML/CSS file, or a
  written description — and extract it into DESIGN.md, so a look designed
  elsewhere (e.g. in the Claude desktop app) satisfies the pipeline's design gate
  without redoing it.
  Output always saved to project root as DESIGN.md.
  Triggers on "design-md:", "generate a design system for", "extract design
  tokens from", "make it look like [brand]", "get the design system for",
  "fetch DESIGN.md for", "create DESIGN.md from", "ingest this mockup/design",
  "turn this prototype/screenshot into DESIGN.md", "here's the design I made".
  After output: vibe-design reads DESIGN.md automatically in Step 2.
---

# Vibe Design MD Skill

Captures the visual language of any real website into a DESIGN.md file.
vibe-design reads this file at session start to produce UI that matches
the target product's aesthetic — exact tokens, not approximations.

> **Autonomous / headless mode.** At startup resolve the settings with
> `python3 ~/.claude/skills/vibe-mode/scripts/vibe_state.py mode`. If `vibe_mode` is
> `autonomous`, every "wait", "ask", "confirm" and approval step in this skill follows
> vibe-mode's `references/HEADLESS.md` §2 instead: take the recommended option, accept your
> own draft after one self-check, log each choice to `vibe/DECISIONS.md`, never ask the
> user, and stop — writing `vibe/.run_state.json` — only when a person is genuinely required.

Two modes. Same output. Always `DESIGN.md` in the project root.

---

## Mode A — Catalog fetch (instant)

**When:** User names a site that exists in the catalog
**How:** Download the pre-built DESIGN.md from awesome-design-md
**Accuracy:** High — tokens extracted directly from real CSS
**Time:** ~5 seconds

**Triggers:**
```
design-md: stripe
design-md: linear
design-md: notion
make it look like Vercel
get the design system for Supabase
```

Read `references/CATALOG.md` to check if the site is in the collection.
If found → fetch and save.
If not found → offer Mode B or suggest closest match from catalog.

---

## Mode B — URL generation (any site)

**When:** User provides a URL not in the catalog
**How:** Fetch the site, extract design tokens from CSS and visual inspection
**Accuracy:** Good — based on computed styles and visual analysis
**Time:** ~2 minutes

**Triggers:**
```
design-md: https://linear.app
design-md: https://resend.com
extract design tokens from https://raycast.com
```

---

## Mode C — Ingest a design the user already made (image / prototype / description)

**When:** the user brings their own design — a mockup/screenshot **image** (PNG/JPG),
a **prototype HTML/CSS** file, or a **written description** of the look (often
produced in Claude desktop, then dropped into the project root).
**How:** analyze the provided artifact and extract its design language into DESIGN.md.
This is what lets a design done elsewhere satisfy the pipeline's design gate — the
user should never be asked to re-do a design they already have.
**Accuracy:** high for HTML (computed/authored values) and images (read the image
directly — palette, type feel, spacing, layout, mood); prose fills the rest.

**Triggers:**
```
design-md: ingest mockup.png
design-md: use this prototype (prototype.html)
"here's the design I made — turn it into DESIGN.md"
[a design image or prototype file dropped in the project root]
```

---

## Step 0 — Parse the request

Determine mode:

```
A provided image / prototype file / "here's my design" → Mode C (ingest artifact)
Input contains "http" or "https"                        → Mode B (URL generation)
Input contains a known site name                        → Mode A (catalog fetch)
Input is ambiguous                                      → check CATALOG.md, then ask
```

**If ambiguous — ask once, concisely:**
> "Is this [site name] in the catalog (instant), a URL I should visit and extract,
>  or a design file/mockup you've already made that I should ingest?"

---

## Step 1A — Catalog fetch (Mode A)

Read `references/CATALOG.md` to find the exact slug and fetch URL.

```bash
# Fetch from awesome-design-md
curl -fsSL "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/[SLUG]/DESIGN.md" \
  -o DESIGN.md

# Verify download succeeded
if [ -f DESIGN.md ] && [ -s DESIGN.md ]; then
  echo "✅ DESIGN.md downloaded — $(wc -l < DESIGN.md) lines"
  head -20 DESIGN.md
else
  echo "❌ Download failed — falling back to Mode B"
fi
```

If download succeeds → jump to Step 3.
If download fails → fall back to Mode B automatically, tell user.

---

## Step 1B — URL rendering and CSS extraction (Mode B)

**Prefer a real browser over `curl`.** Most catalog-worthy sites (Linear,
Vercel, Notion, Stripe, …) are JS-rendered and/or use CSS-in-JS or Tailwind —
raw HTML shows none of the actual colours, fonts, or spacing. Load the page in
the browser (`navigate` to the URL), then read **computed styles** and a
screenshot, which reflect what users actually see:

1. **Screenshot** the page (desktop, and mobile if responsive) — judge palette,
   density, hierarchy, and layout from the rendered image.
2. **Computed styles** via the page-inspection tools / a small `javascript_tool`
   snippet: read `getComputedStyle` on `body`, headings, buttons, and links for
   real colours, `font-family`, font sizes, radius, and shadows; collect any
   `:root { --var }` custom properties.
3. **Fonts** — the actually-applied `font-family` stacks (not just `<link>` tags).
4. **Meta** — title / og:description / brand name for the DESIGN.md header.

**Fallback only if no browser tool is available in the session:**
```bash
curl -fsSL "[URL]" -o /tmp/design_target.html 2>/dev/null && wc -c /tmp/design_target.html
```
Then extract font `<link>`s, `:root` custom properties, and inline colours from
the static HTML — and warn the user:
> "No browser was available, so I read static HTML only — for a JS-rendered site
> the computed colours/fonts may be incomplete. Share a screenshot or the site's
> style-guide URL for higher accuracy."
Flag every inferred value explicitly.

---

## Step 1C — Ingest a provided design artifact (Mode C)

Extract the design language from whatever the user brought:

- **Image mockup / screenshot (PNG/JPG):** read the image directly (it's multimodal —
  actually look at it). Extract: the palette (sample the real colours — background,
  text, primary/accent, borders; give hex/OKLCH), the type feel (serif/sans/mono,
  weight contrast, display vs body; name the closest real families), spacing/rhythm,
  radius and shadow character, layout structure, and the overall mood/archetype
  (per vibe-design ANTI_GENERIC.md). Where a value can't be read exactly from the
  image, infer and mark it "(from mockup — verify)".
- **Prototype HTML/CSS file:** read the file; pull authored/`getComputedStyle` values —
  CSS custom properties, font stacks, colours, spacing, radii, shadows. Highest fidelity.
- **Written design description (prose):** map the described intent onto the DESIGN.md
  fields; fill unstated specifics with archetype-appropriate defaults and mark them
  "(inferred from description)".

Do NOT overwrite an existing DESIGN.md silently — if one exists, diff and confirm.
The goal is to faithfully capture *the user's* design, not to redesign it.

---

## Step 2 — Generate the DESIGN.md

Read `references/DESIGN_MD_FORMAT.md` for the exact 9-section structure.

Fill each section from extracted data. Be precise — exact values, not descriptions.

**Section 1 — Visual Theme & Atmosphere**
2-3 sentences: what does this design feel like? What's the mood, density, philosophy?
Example: "Linear uses extreme restraint — near-monochrome surfaces, tight typography,
and generous whitespace to create a sense of precision and focus. Every element
earns its place. Nothing is decorative."

**Section 2 — Color Palette & Roles**
Every colour with: semantic name, exact hex (and oklch if extractable), functional role.
```markdown
| Token | Hex | OKLCH | Role |
|-------|-----|-------|------|
| --color-bg | #FFFFFF | oklch(100% 0 0) | Page background |
| --color-text | #0F0F0F | oklch(6% 0 0) | Primary text |
| --color-brand | #5E6AD2 | oklch(50% 0.12 265) | Linear purple — CTAs, links, active states |
| --color-surface | #F7F8F9 | oklch(97% 0.005 240) | Card and sidebar backgrounds |
| --color-border | #E5E7EB | oklch(91% 0.006 240) | Dividers, input borders |
```

Minimum 6 colours. Include the brand accent even if subtle.

**Section 3 — Typography Rules**
Font families (exact names as they appear in CSS/font links).
Full hierarchy table:
```markdown
| Role | Font | Size | Weight | Line height | Tracking |
|------|------|------|--------|------------|---------|
| Display | [font] | [px/rem] | [number] | [value] | [em] |
| H1 | [font] | [px] | [number] | [value] | [em] |
| H2 | [font] | [px] | [number] | [value] | [em] |
| Body | [font] | [px] | [number] | [value] | [em] |
| Caption | [font] | [px] | [number] | [value] | [em] |
| Mono | [font] | [px] | [number] | [value] | [em] |
```

**Section 4 — Component Styling**
Buttons, cards, inputs, navigation — with exact values for all states.
```markdown
### Button (Primary)
- Background: [colour token]
- Text: [colour token]
- Border radius: [px]
- Padding: [px × px]
- Font: [weight, size]
- Hover: background [value], transition [duration ease]
- Active: background [value], scale [value]
- Disabled: opacity [value]
- Focus: outline [colour] [width] offset [value]
```

**Section 5 — Layout Principles**
Spacing scale (e.g. 4px base, multiples), max-widths, grid, whitespace philosophy.

**Section 6 — Depth & Elevation**
Shadow system with exact `box-shadow` values for each elevation level.
```
Level 0 — flat: no shadow
Level 1 — card: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)
Level 2 — dropdown: 0 4px 16px rgba(0,0,0,0.12), 0 1px 4px rgba(0,0,0,0.06)
Level 3 — modal: 0 20px 60px rgba(0,0,0,0.16), 0 4px 16px rgba(0,0,0,0.08)
```

**Section 7 — Do's and Don'ts**
5-8 specific guardrails for this design language.
Example for Linear:
```
✅ DO: Use weight contrast (300 vs 600) for hierarchy, not size alone
✅ DO: Keep interactive elements subtle — hover should feel discovered, not announced
❌ DON'T: Use colour to convey information (colourblind-safe by design)
❌ DON'T: Add decorative elements — if it doesn't help users, remove it
❌ DON'T: Use more than 2 font weights in any single view
```

**Section 8 — Responsive Behaviour**
Key breakpoints, how navigation collapses, touch target sizes, what changes on mobile.

**Section 9 — Agent Prompt Guide**
3 ready-to-use prompts for common UI tasks in this style.
```
"Build a dashboard sidebar using the Linear DESIGN.md.
 Navigation items: text-only, no icons, active state uses --color-brand background at 8% opacity."

"Create a data table using Linear tokens.
 Headers: --color-text-secondary, 12px, weight 500, uppercase, tracking 0.04em.
 Rows: 1px --color-border bottom, hover --color-surface background."

"Design an empty state using Linear's minimalist approach.
 Short headline, one-line description, single CTA. No illustrations."
```

---

## Step 3 — Save and validate

```bash
# Save to project root
# (already there from curl in Mode A, or write from generation in Mode B)

# Validate it has content
LINES=$(wc -l < DESIGN.md)
SECTIONS=$(grep -c "^## " DESIGN.md)

echo "DESIGN.md: $LINES lines, $SECTIONS sections"

if [ $SECTIONS -lt 7 ]; then
  echo "⚠️ Missing sections — expected 9, found $SECTIONS"
fi
```

---

## Step 4 — Tell the user

```
✅ DESIGN.md ready — [Site name]
   [Mode A: "Downloaded from awesome-design-md catalog" /
    Mode B: "Generated from [URL]"]

Design language:
  [One sentence from Section 1]

Key tokens:
  Brand: [colour name + hex]
  Type: [display font] + [body font]
  Surface: [bg colour]

How to use:
  vibe-design reads DESIGN.md automatically.
  Trigger a design pass: design: [what to style]

[If Mode B — inferred values:]
  ⚠️ [N] values were inferred (marked with * in DESIGN.md).
  Verify against the live site before production use.
```

---

## Step 5 — Offer to update DESIGN_SYSTEM.md

If `vibe/DESIGN_SYSTEM.md` exists:
> "DESIGN.md is ready. Should I also update vibe/DESIGN_SYSTEM.md to use
> these tokens as the project's design system? This would make all future
> design passes use [site name]'s visual language by default."

Wait for answer. If yes — update DESIGN_SYSTEM.md with the key tokens.
If no — leave as is. DESIGN.md will still be read by vibe-design.

---

## Absolute rules

**Never fabricate token values.**
If a colour can't be extracted, write `[EXTRACT FROM SITE]` as the value.
Inferred values are marked with `*` and flagged in the Step 4 summary.

**DESIGN.md always goes in the project root.**
Not in vibe/, not in src/. Root only.
vibe-design checks `./DESIGN.md` — nowhere else.

**Mode B accuracy is honest.**
JS-rendered sites will have incomplete token extraction.
Always flag what was inferred vs extracted.
Never present an inferred value as definitive.

**One DESIGN.md per project at a time.**
If DESIGN.md already exists, show a diff of what would change:
> "DESIGN.md already exists ([current site name]).
> Replace with [new site]? Or save as DESIGN_[site].md for reference?"
Wait for answer.
