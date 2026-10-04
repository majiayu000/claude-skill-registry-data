---
name: design-steal
description: |
  Steal a specific company's design language for a component or page. Fetches any of 55
  DESIGN.md files from VoltAgent/awesome-design-md (Spotify, Apple, Linear, Stripe, etc),
  extracts the relevant patterns, and adapts them to ZAO OS's navy/gold palette while
  preserving the source's aesthetic DNA. Use when asked to "make it look like Spotify",
  "steal Linear's style", "design like Apple", or "use [company]'s design for this".
---

# Design Steal

Fetch a company's design system, extract the patterns that matter, build the component with their aesthetic DNA adapted to ZAO OS.

## Usage

- `/design-steal spotify` — fetch Spotify's design system, show what to steal
- `/design-steal linear for the governance page` — apply Linear's precision to a specific page
- `/design-steal apple airbnb` — compare two systems, pick the best patterns from each

## Available Design Systems (55)

### By Vibe

| Vibe | Companies |
|------|-----------|
| **Music / Audio** | spotify, elevenlabs, runwayml |
| **Premium Dark** | apple, bmw, spacex, nvidia, superhuman, uber |
| **Developer Precision** | linear, cursor, vercel, raycast, resend, warp, supabase |
| **Friendly / Warm** | airbnb, notion, zapier, airtable, intercom |
| **Crypto / Fintech** | coinbase, kraken, revolut, wise |
| **Bold / Playful** | figma, framer, miro, lovable, posthog |
| **AI / Technical** | claude, cohere, minimax, mistral, ollama, replicate, together, voltagent, xai |
| **Enterprise Clean** | ibm, hashicorp, mongodb, stripe, sanity |
| **Content / Design** | clay, pinterest, webflow, mintlify, cal |

## Workflow

### Step 1: Fetch the Design System

```bash
# Single company
curl -s https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/{company}/DESIGN.md

# Company name mapping (use lowercase, dots become dots):
# linear → linear.app
# together → together.ai
# mistral → mistral.ai
# opencode → opencode.ai
# xai → x.ai
```

Use WebFetch to get the full DESIGN.md content. Read it completely — don't summarize.

### Step 2: Read ZAO's DESIGN.md

Read `/DESIGN.md` at project root. This is the ground truth for ZAO OS.

### Step 3: Extract What to Steal

Present a table to the user:

```markdown
## Stealing from [Company]

| Pattern | Their Value | ZAO Adaptation | Impact |
|---------|------------|----------------|--------|
| Border radius | 16px (rounded) | Keep our 8px (sharper) | Low — skip |
| Card hover | scale(1.02) + shadow | Add to track cards | High — steal |
| Typography weight | 510 (signature) | Try 500 on headings | Medium — test |
| Button style | pill 9999px | Already using pills | None — we have it |
| Spacing rhythm | 8px base | Match our 4px base | Adapt to 4px |
```

Categorize each pattern as:
- **STEAL** — directly adopt, adapting colors to navy/gold
- **ADAPT** — take the concept but modify for our context
- **SKIP** — doesn't fit ZAO's aesthetic or we already have it

### Step 4: Build It

Apply the stolen patterns to the target component or page. Rules:

1. **Colors stay ZAO** — navy (#0a1628) background, gold (#f5a623) accent. NEVER use the source company's brand colors.
2. **Font stays Inter** — don't import other companies' proprietary fonts.
3. **Steal the STRUCTURE, not the skin** — layout patterns, spacing rhythm, hover behaviors, animation timing, component architecture.
4. **Reference DESIGN.md** — every stolen pattern should be consistent with or explicitly override values in `/DESIGN.md`.

### Step 5: Update DESIGN.md (if patterns are reusable)

If the stolen pattern is good enough to become a ZAO OS standard, add it to `/DESIGN.md` under the appropriate section.

## Examples

### "Make the music player look like Spotify"

Steal: content-first darkness (album art as hero), pill-shaped play button, heavy card shadows, compressed type scale, white-on-dark text hierarchy.

Adapt: Green (#1ed760) → Gold (#f5a623), Black (#121212) → Navy (#0a1628), CircularSp → Inter.

Skip: Spotify's proprietary font, their specific shadow values (too heavy for our navy palette).

### "Make governance look like Linear"

Steal: ultra-minimal card borders (rgba white 0.05), weight-510 emphasis, negative letter-spacing on headers, achromatic UI with single accent color, luminance-based depth.

Adapt: Purple (#5e6ad2) → Gold (#f5a623), Black (#08090a) → Navy (#0a1628).

Skip: Berkeley Mono (we use system monospace), their specific OpenType features.

### "Make onboarding feel like Airbnb"

Steal: warm photography-driven layout, generous whitespace, rounded 12px cards, friendly button copy, progress indicators.

Adapt: Coral (#FF5A5F) → Gold (#f5a623), White backgrounds → Navy, their serif headings → Inter semibold.

Skip: Light theme patterns, their specific illustration style.

## Source Repo

- **Repo:** [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
- **License:** MIT
- **Count:** 55 design systems
- **Format:** Single DESIGN.md per company
- **Research:** Doc 282 in `research/dev-workflows/282-awesome-design-md-system/`

## Rules

- ALWAYS read ZAO's DESIGN.md first — it's the ground truth
- NEVER use another company's brand colors in production code
- NEVER import proprietary fonts — stick with Inter
- ALWAYS present the steal/adapt/skip table before building
- ALWAYS show before/after if modifying an existing component
- If stealing from 2+ companies, show which patterns come from which source
