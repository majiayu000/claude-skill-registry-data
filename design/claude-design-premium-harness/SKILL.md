---
name: claude-design-premium-harness
description: Premium design system harness for Claude Design Web that maintains context, tokens, and component fidelity across sessions
triggers:
  - set up claude design premium for my project
  - bind my design system to claude design web
  - scaffold a design system showcase with claude design premium
  - audit this UI against my design system tokens
  - run design system guardian on this component
  - assemble the full design system specimen
  - create a framework handoff for this design
  - bootstrap claude design premium in builder mode
---

# Claude Design Premium Harness

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Claude Design Premium is a **context harness and skill pack** for Claude Design Web that prevents design system amnesia. It binds your tokens, components, voice, and constraints into persistent artifacts (`BOUND_DS.json`, `DESIGN.md`) so Claude respects your system across sessions without re-briefing.

**Zero npm dependencies.** Scripts run inside Claude Design's canvas runtime. 13 skills cover setup, guardian checks, audits (a11y, mobile, copy, Tailwind), showcase assembly, and framework handoff.

## What It Does

- **Binds your design system** via `BOUND_DS.json` (tokens, components, manifest paths)
- **Enforces fidelity** with `design-system-guardian` that checks every UI task against your system
- **Assembles a living specimen** (`design-system.dc.html`) from your `DESIGN.md`
- **Runs targeted audits** before handoff: accessibility, mobile-first, text integrity, visual originality, Tailwind alignment
- **Supports two modes**: **Builder** (you maintain the DS) and **Consumer** (you use a published bundle)

## Installation

### 1. Download and Upload

```bash
# Download ZIP from GitHub
curl -L https://github.com/oalanicolas/claude-design-premium/archive/refs/heads/main.zip -o cdp.zip
unzip cdp.zip
```

Then upload the ZIP to your Claude Design Web project, or clone the repo directly if working locally.

### 2. Promote Harness Files

In Claude Design Web chat:

```text
Copy all files from the claude-design-premium-main folder to the project root.
Keep existing _ds/ or root manifest files.
```

This moves:
- `CLAUDE.md` (skill router)
- `skills/` (13 `.md` files)
- `scripts/` (bootstrap `.mjs` files)
- `pages/` (starter `.dc.html` files)
- `README.md`, `PLAYBOOK.md`, `LIMITATIONS.md`

### 3. Bootstrap

Open a **new tab** in the same project and send:

```text
GO
```

The `harness-auto-setup` skill runs `scripts/bootstrap-harness.mjs`, detects builder or consumer mode, writes `BOUND_DS.json`, scaffolds `design-system.dc.html`, and generates `.cdp/showcase-brief.json`.

## Key Configuration Files

### `DESIGN.md`

Your **canonical brief**: voice, surfaces, constraints. Claude reads this before every UI task.

**Builder mode** (root):

```markdown
# Design System Brief

## Voice & Tone
CDP:UNCONFIGURED — Replace with your brand voice rules

## Surfaces
- Dashboard (dense, data-first)
- Landing (spacious, conversion-focused)
- Settings (utility, clarity over beauty)

## Constraints
- Mobile-first grid, 4px base unit
- Tailwind utilities only, no arbitrary values unless documented
- WCAG AA minimum

## Token Reference
See `_ds_manifest.json` → colors, spacing, typography
```

**Consumer mode** (`_ds/<bundle>/DESIGN.md`):

```markdown
# Design System: Acme SaaS Kit

## Voice
Professional, warm, no jargon. Active voice. Sentence case everywhere.

## Components
Dashboard cards, metric tiles, action sheets (see `_ds/acme/components/`)

## Tokens
`_ds/acme/_ds_manifest.json`
```

### `BOUND_DS.json`

Written by bootstrap. Machine-readable binding.

```json
{
  "mode": "builder",
  "design_md_path": "DESIGN.md",
  "manifest_path": "_ds_manifest.json",
  "components_dir": "components/",
  "tokens": {
    "colors": { "primary": "#3b82f6", "surface": "#ffffff" },
    "spacing": { "xs": "0.25rem", "sm": "0.5rem" }
  },
  "timestamp": "2026-06-18T22:14:04Z"
}
```

### `.cdp/showcase-brief.json`

Inventory for the design system specimen:

```json
{
  "sections": [
    { "id": "colors", "title": "Color Palette", "components": [] },
    { "id": "typography", "title": "Typography Scale", "components": [] },
    { "id": "buttons", "title": "Buttons", "components": ["primary", "secondary", "ghost"] }
  ],
  "meta": { "generated": "2026-06-18T22:14:04Z", "mode": "builder" }
}
```

## Core Skills

### `harness-auto-setup`

**Trigger:** First open or `GO` command.

Runs `scripts/bootstrap-harness.mjs`:
1. Detects mode (builder if `_ds_manifest.json` at root, consumer if `_ds/<bundle>/` exists)
2. Writes `BOUND_DS.json`
3. Scaffolds `design-system.dc.html`
4. Generates `.cdp/showcase-brief.json`

**User prompt:**

```text
GO
```

### `design-system-guardian`

**Trigger:** Any UI creation task (dashboard, landing page, component mockup).

Checks:
- Token usage (colors, spacing, typography from `BOUND_DS.json`)
- Component existence (manifest `components/` array)
- Voice alignment (`DESIGN.md` tone rules)

**Example (in Claude Design Web):**

```text
Create a settings page for user preferences using our design system.
```

Guardian intercepts, validates tokens, suggests fixes:

```text
✓ Tokens aligned
✗ "Toggle Switch" not in manifest — use "Checkbox" or add to components/
✓ Copy matches DESIGN.md voice
```

### `assemble-design-system-showcase`

**Trigger:** After bootstrap, to complete the specimen.

Reads `.cdp/showcase-brief.json`, builds out each section in `design-system.dc.html`.

**User prompt:**

```text
Assemble the full design-system showcase from the brief.
```

Produces a live, navigable specimen with:
- Token swatches
- Component examples with states
- Spacing/typography scales
- Real copy samples

### Audit Skills

All run before handoff. Invoked via `CLAUDE.md` routing.

| Skill | What It Checks |
|-------|----------------|
| `ui-audit` | Hierarchy, layout, spacing consistency |
| `visual-originality-audit` | Generic template patterns, stock photo drift |
| `text-integrity-audit` | Copy vs `DESIGN.md` voice rules |
| `mobile-first-audit` | Responsive behavior, touch targets |
| `accessibility-audit` | WCAG AA contrast, keyboard nav, ARIA |
| `tailwind-audit` | Utility/token alignment, arbitrary value usage |

**Example prompt:**

```text
Run a mobile-first audit on this dashboard.
```

Claude applies `skills/mobile-first-audit.md`, reports breakpoint issues, touch target sizes.

### `framework-handoff`

**Trigger:** Ready to export to React, Vue, Svelte, etc.

Generates notes mapping `.dc.html` to framework code.

**User prompt:**

```text
Create a framework handoff for this landing page in React + Tailwind.
```

Output:

```markdown
## Framework Handoff: Landing Page → React

### Components
- `Hero.jsx` — token: `text-primary`, spacing: `py-16`
- `FeatureGrid.jsx` — 3-col responsive, `gap-6` (token: `spacing.md`)

### Tailwind Config
Extend `tailwind.config.js`:
```js
module.exports = {
  theme: {
    extend: {
      colors: { primary: '#3b82f6', surface: '#ffffff' }
    }
  }
}
```

### Missing in Manifest
- Icon component (suggest adding `_ds_manifest.json` → `components: ["Icon"]`)
```

## Real Usage Patterns

### Pattern 1: Bootstrap a New Builder Project

You're the DS maintainer. Tokens and components are in this repo.

```bash
# Local validation (optional)
node scripts/bootstrap-harness.mjs
node scripts/context-signals.mjs
```

In Claude Design Web:

```text
GO
```

Then configure `DESIGN.md`:

```markdown
# Design System Brief

## Voice
Clear, confident, no marketing fluff. Active voice. Sentence case.

## Surfaces
- Dashboard: dense, data-forward
- Landing: spacious, conversion-focused

## Constraints
- Mobile-first, 4px base unit
- Tailwind utilities only
- WCAG AA minimum

## Token Reference
`_ds_manifest.json` → colors, spacing, typography
```

Assemble specimen:

```text
Assemble the full design-system showcase from the brief.
```

### Pattern 2: Consumer Mode (Published Bundle)

Your app uses a published DS bundle in `_ds/acme/`.

Upload harness ZIP, promote files:

```text
Copy all files from the claude-design-premium folder to the project root.
```

New tab:

```text
GO
```

Bootstrap detects `_ds/acme/_ds_manifest.json`, sets mode to `consumer`, binds to `_ds/acme/DESIGN.md`.

Build a screen:

```text
Create a user settings page using the Acme design system.
```

Guardian checks `_ds/acme/components/`, validates tokens, enforces voice from `_ds/acme/DESIGN.md`.

### Pattern 3: Audit Before Handoff

You've designed a dashboard. Run all audits:

```text
Run a full audit pass on this dashboard: UI, mobile, accessibility, and Tailwind alignment.
```

Claude invokes:
1. `ui-audit.md` → hierarchy, spacing
2. `mobile-first-audit.md` → responsive, touch targets
3. `accessibility-audit.md` → contrast, ARIA
4. `tailwind-audit.md` → utility usage

Reports issues, you iterate, then:

```text
Create a framework handoff for React + Tailwind.
```

### Pattern 4: Maintain the Specimen

Your DS evolves. Update `_ds_manifest.json` (new components), then:

```text
Update the design-system showcase with the new Button variants.
```

Claude reads updated manifest, rebuilds relevant sections in `design-system.dc.html`.

## Bootstrap Scripts (Node.js, Optional Local Use)

Scripts in `scripts/` are **Node.js modules** that run inside Claude Design's canvas when Claude reads and applies them. You can also run them locally for validation.

### `scripts/bootstrap-harness.mjs`

```javascript
import fs from 'fs';
import path from 'path';

// Detects mode, writes BOUND_DS.json, scaffolds showcase
const mode = fs.existsSync('_ds_manifest.json') ? 'builder' : 
             fs.existsSync('_ds') ? 'consumer' : 'unknown';

const binding = {
  mode,
  design_md_path: mode === 'builder' ? 'DESIGN.md' : '_ds/*/DESIGN.md',
  manifest_path: mode === 'builder' ? '_ds_manifest.json' : '_ds/*/_ds_manifest.json',
  timestamp: new Date().toISOString()
};

fs.writeFileSync('BOUND_DS.json', JSON.stringify(binding, null, 2));
console.log('✓ BOUND_DS.json written');
```

Run locally:

```bash
node scripts/bootstrap-harness.mjs
# Output: ✓ BOUND_DS.json written
```

Override mode:

```bash
node scripts/bootstrap-harness.mjs --mode builder
```

### `scripts/context-signals.mjs`

Validates setup: checks for `CLAUDE.md`, `DESIGN.md`, `BOUND_DS.json`.

```bash
node scripts/context-signals.mjs
# Output:
# ✓ CLAUDE.md exists
# ✓ BOUND_DS.json valid
# ✗ DESIGN.md contains CDP:UNCONFIGURED placeholders
```

### `scripts/test-builder-bootstrap.mjs`

Simulates full bootstrap in builder mode, writes test files.

```bash
node scripts/test-builder-bootstrap.mjs
# Creates .cdp/test-run/ with mock BOUND_DS.json, showcase-brief.json
```

## Environment Variables

No API keys required. All logic runs inside Claude Design Web's canvas or locally via Node.js.

If you integrate external APIs (e.g., Figma token sync), reference:

```javascript
const figmaToken = process.env.FIGMA_ACCESS_TOKEN;
```

Do **not** hardcode secrets in `DESIGN.md` or scripts.

## Common Issues

### "CDP:UNCONFIGURED" in Specimen

**Cause:** `DESIGN.md` still has placeholders.

**Fix:** Edit `DESIGN.md`, replace placeholders with your voice, surfaces, constraints. Then:

```text
Reassemble the design-system showcase.
```

### Guardian Rejects Valid Component

**Cause:** Component not in `_ds_manifest.json` `components` array.

**Fix (builder mode):** Add to manifest:

```json
{
  "components": ["Button", "Card", "Toggle"]
}
```

**Fix (consumer mode):** Request bundle maintainer to publish update.

### "Mode detection failed"

**Cause:** No `_ds_manifest.json` at root and no `_ds/<bundle>/` folder.

**Fix:** Create a minimal manifest:

```json
{
  "name": "my-system",
  "version": "1.0.0",
  "tokens": {},
  "components": []
}
```

Or place a published bundle in `_ds/<name>/`.

### Showcase Scaffold Empty

**Cause:** Bootstrap ran, but `assemble-design-system-showcase` didn't.

**Fix:**

```text
Assemble the full design-system showcase from the brief.
```

## CLI Commands (Local Validation)

```bash
# Bootstrap (detect mode, write BOUND_DS.json)
node scripts/bootstrap-harness.mjs

# Validate setup
node scripts/context-signals.mjs

# Test builder bootstrap
node scripts/test-builder-bootstrap.mjs

# Override mode
node scripts/bootstrap-harness.mjs --mode consumer
```

## File Structure

```
project-root/
├── CLAUDE.md                    # Skill router
├── DESIGN.md                    # Your voice, surfaces, constraints
├── BOUND_DS.json                # Machine-readable binding (generated)
├── _ds_manifest.json            # Builder mode: tokens, components
├── _ds/                         # Consumer mode: published bundles
│   └── acme/
│       ├── DESIGN.md
│       ├── _ds_manifest.json
│       └── components/
├── skills/                      # 13 .md skill files
│   ├── harness-auto-setup.md
│   ├── design-system-guardian.md
│   ├── ui-audit.md
│   └── ...
├── scripts/                     # Bootstrap .mjs
│   ├── bootstrap-harness.mjs
│   ├── context-signals.mjs
│   └── test-builder-bootstrap.mjs
├── pages/
│   ├── intro.dc.html
│   └── design-system.dc.html    # Scaffold → full specimen
└── .cdp/
    └── showcase-brief.json      # Section inventory
```

## Integration with Claude Design Web

All skills are invoked **via natural language** in Claude Design Web. The `CLAUDE.md` router maps user intent to skill files.

**Example routing (from `CLAUDE.md`):**

- "create a dashboard" → `design-system-guardian.md`
- "audit for accessibility" → `accessibility-audit.md`
- "assemble showcase" → `assemble-design-system-showcase.md`

No manual skill selection. Paste your prompt; Claude applies the right skill.

## Best Practices

1. **Configure `DESIGN.md` immediately** after bootstrap — remove all `CDP:UNCONFIGURED` placeholders.
2. **Run audits before handoff** — full pass (UI, mobile, a11y, Tailwind) catches issues early.
3. **Keep `_ds_manifest.json` updated** (builder mode) — guardian can't enforce components it doesn't know.
4. **Assemble the specimen once**, then update sections as the system evolves.
5. **Use framework handoff** when ready for code — don't skip this step or engineers guess token mappings.

## Further Reading

- [PLAYBOOK.md](PLAYBOOK.md) — Session flows for dashboard, landing, settings pages
- [LIMITATIONS.md](LIMITATIONS.md) — What this harness does and doesn't guarantee
- [docs/script-pipeline.md](docs/script-pipeline.md) — Deep dive on bootstrap scripts
- [docs/canvas-runtime.md](docs/canvas-runtime.md) — How `.dc.html` runs inside Claude Design Web
- [docs/validation-method.md](docs/validation-method.md) — Verify your setup

---

**License:** MIT  
**Community project** — not affiliated with or endorsed by Anthropic. Claude Design Web is Anthropic's product.
