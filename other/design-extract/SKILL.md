---
name: design-extract
version: 1.0.0
description: "Extract a website's design system (colors, typography, spacing, buttons) and populate the brand guide. Trigger with /design-extract or when the user mentions 'extract design,' 'pull brand from website,' 'design tokens from site,' 'scrape brand colors,' or 'extract visual identity.' Requires Node 20+ and installs designlang globally if not present."
---

# Design Extract

Extract a live website's design system and write the results into `brain/brand-guide/brand-guide.md`.

Uses [designlang](https://github.com/Manavarya09/design-extract) — a headless-browser tool that reads the design system off the live DOM and emits structured tokens.

---

## Prerequisites

- Node 20+
- `designlang` CLI (installed automatically if missing)

---

## Workflow

### Step 1: Get the URL

Ask the user:

> What website URL should I extract the design system from?

If they already provided a URL in their message, confirm it.

Optional follow-ups:
- "Should I extract dark mode too?" (adds `--dark` flag)
- "Any pages behind auth I should include?" (adds `--cookie` flag)

### Step 2: Install designlang if needed

Check if designlang is available:

```bash
command -v designlang || npm list -g designlang 2>/dev/null
```

If not installed, use npx to avoid global install permission issues:

```bash
npx -y designlang <url> ...
```

Alternatively, if the user prefers a global install:

```bash
npm i -g designlang
```

### Step 3: Run extraction

Run designlang's `brand` subcommand against the URL. This generates a full editorial brand-guidelines document (13 chapters, print-ready) along with design tokens:

```bash
designlang brand <url> --out ./design-extract-output --name brand --verbose
```

If the `brand` subcommand fails or produces insufficient output, fall back to the default extraction:

```bash
designlang <url> --out ./design-extract-output --name brand --full --verbose
```

Flags to consider based on user input:
- `--dark` — if they want dark mode tokens
- `--depth 2` — if they want to crawl beyond the homepage
- `--cookie "name=value"` — if pages require auth

### Step 4: Parse the output

Read the generated files from `./design-extract-output/`:

1. **`brand-design-language.md`** — the full 19-section design system doc
2. **`brand-design-tokens.json`** — W3C DTCG tokens (colors, typography, spacing)
3. **`brand-voice.json`** — tone, CTA verb inventory (pass to tone-mapping if present)

Extract and organize:
- **Colors:** core palette, accent colors, semantic colors (success, error, warning), gradients
- **Typography:** font families, weights, sizes, line heights, font sources
- **Spacing:** base unit, scale tokens
- **Buttons:** primary/secondary styles, border radius, padding, hover states
- **Design principles:** inferred from patterns (dark-first vs light, density, whitespace approach)

### Step 5: Review with user

Present the extracted design system in a summary table format:

```
Extracted from: [url]

Colors:
  Primary Background    #1a1a2e
  Card Background       #16213e
  Primary Text          #ffffff
  Body Text             #a8b2d1
  Primary Accent        #0f3460    (buttons, CTAs)
  Secondary Accent      #e94560    (highlights)

Typography:
  Headings    Inter         700    fallback: system-ui
  Body        Inter         400    fallback: system-ui
  Code        JetBrains Mono 400   fallback: monospace

Spacing: 4px base unit (4, 8, 12, 16, 24, 32, 48, 64)

Buttons:
  Primary     #0f3460 bg, #fff text, 8px radius
  Secondary   transparent bg, #0f3460 border
```

Ask: "Does this look right? Anything to adjust before I write the brand guide?"

### Step 6: Write brand-guide.md

Write the extracted values into `brain/brand-guide/brand-guide.md`, replacing `[FILL IN]` placeholders with real values. Preserve the template structure exactly — only replace placeholders.

If the extraction found values not covered by the template (gradients, shadows, z-index), add them as new sections at the bottom following the same formatting conventions.

### Step 7: Clean up

Remove the `design-extract-output/` directory:

```bash
rm -rf ./design-extract-output
```

Tell the user:

> Brand guide updated at `brain/brand-guide/brand-guide.md`. All visual skills (brand-design, web-design, hubspot-email, etc.) will now use these values.

If `brand-voice.json` contained tone/voice data, mention:

> I also found voice/tone data. Run `/tone-mapping` to build a full voice profile.

---

## Rules

- Never overwrite existing brand-guide values without confirming with the user
- If the brand guide already has values filled in, show a diff of what would change and ask
- If designlang fails (site blocks headless browsers, JS-heavy SPA that doesn't render), tell the user and offer manual entry as fallback
- Keep the design-extract-output directory until the user confirms the brand guide looks good, then clean up
- If the site has both light and dark modes, extract both and present both, letting the user pick which is primary
