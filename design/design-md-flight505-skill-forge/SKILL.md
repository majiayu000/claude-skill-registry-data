---
name: design-md
description: Drop-in DESIGN.md design-system files for 71 popular brands (Claude, Linear, Stripe, Vercel, Apple, Figma, Tesla…). Use when the user wants to match a brand's look and feel, asks to "apply a design system", says "make it look like <brand>", mentions DESIGN.md, or needs design tokens (colors, typography, components) extracted from a known site.
---

# DESIGN.md Library

**A curated vault of 71 DESIGN.md files** — plain-text design system documents inspired by real brand websites. Drop one into a project and Claude will generate UI that matches the brand's look and feel.

## What is DESIGN.md?

DESIGN.md is a [Google Stitch](https://stitch.withgoogle.com/docs/design-md/overview/) format: a single markdown file that captures a brand's visual design system in a way AI coding agents can read and apply directly. No Figma exports, no JSON schemas, no tooling — just markdown.

Each file follows the Stitch format with these sections:

1. Visual Theme & Atmosphere
2. Color Palette & Roles (semantic name + hex + functional role)
3. Typography Rules (font families, full hierarchy table)
4. Component Stylings (buttons, cards, inputs, nav, with states)
5. Layout Principles (spacing scale, grid, whitespace philosophy)
6. Depth & Elevation (shadow system, surface hierarchy)
7. Do's and Don'ts (guardrails and anti-patterns)
8. Responsive Behavior (breakpoints, touch targets)
9. Agent Prompt Guide (quick color reference, ready-to-use prompts)

## When to Activate

Trigger this skill when the user:

- Names a brand and asks for its look: _"make it look like Linear"_, _"use Stripe's design system"_, _"apply the Claude design"_
- Asks for a design system by domain: _"I need a design for an AI product site — something like Cohere or Mistral"_
- Mentions DESIGN.md directly: _"drop in a DESIGN.md"_, _"what DESIGN.md files do you have?"_
- Wants brand-accurate tokens: _"give me Stripe's color palette"_, _"what's Vercel's type scale?"_
- Asks to list or browse available designs: _"what design systems are available?"_, _"show me the catalog"_

If the user asks for something that isn't in the catalog, say so honestly — don't invent tokens. Suggest the closest match or point them at `scripts/update-templates.sh` to refresh from upstream.

## How to Use

### Browse the catalog

Read `references/catalog.md` for a flat alphabetical list of all 71 brands with one-line hooks, or `references/categories.md` to see them grouped (AI & LLM, Developer Tools, Fintech, Automotive, etc.).

### Apply a template

Use the apply script — it validates the brand name, copies the template into the user's cwd as `DESIGN.md`, and prints an activation hint.

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/apply.sh" <brand>
# e.g.
bash "${CLAUDE_SKILL_DIR}/scripts/apply.sh" claude
bash "${CLAUDE_SKILL_DIR}/scripts/apply.sh" linear.app
bash "${CLAUDE_SKILL_DIR}/scripts/apply.sh" stripe
```

The brand slug is the lowercase name used in the catalog (e.g. `claude`, `linear.app`, `mistral.ai`, `opencode.ai`, `together.ai`, `theverge`, `x.ai`).

The script writes `./DESIGN.md` into the current working directory. If a `DESIGN.md` already exists, it aborts unless `--force` is passed:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/apply.sh" stripe --force
```

### List all available brands

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/list.sh"
bash "${CLAUDE_SKILL_DIR}/scripts/list.sh" --category ai     # filter by category
bash "${CLAUDE_SKILL_DIR}/scripts/list.sh" --search dark     # search descriptions
```

### After applying

Once `DESIGN.md` is in the project root, tell Claude to use it. Claude reads the file automatically when generating UI in that project — you shouldn't need to paste the tokens inline. Example prompts:

- _"Build a landing page following DESIGN.md"_
- _"Create a pricing card using our DESIGN.md tokens"_
- _"Refactor this component to match DESIGN.md"_

DESIGN.md is complementary to [AGENTS.md](https://agents.md/). If both exist in a project: AGENTS.md tells Claude how to build the project, DESIGN.md tells Claude how it should look.

## Composition with other tools

- **Image generation**: if the project also has the `nano-banana` plugin installed, you can ask Claude to generate brand-matched images using the DESIGN.md as the style reference. No explicit wiring needed — just ask.
- **html-artifacts**: separate concern. html-artifacts creates quick dashboards/forms for in-terminal work; it doesn't compose with DESIGN.md unless you explicitly ask it to.

## Updating the templates

The source of truth is the [`getdesign` npm package](https://www.npmjs.com/package/getdesign), which bundles the 71 templates from [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md).

To refresh all templates from the latest upstream release:

```bash
bash "${CLAUDE_SKILL_DIR}/scripts/update-templates.sh"
```

This pulls the newest `getdesign@latest` via `npm pack`, extracts `package/templates/*.md` + `manifest.json`, and replaces the local copy atomically. Run this monthly or when you hear about new brands.

## File Layout

```
design-md/
├── SKILL.md                          # This file
├── references/
│   ├── catalog.md                    # Flat alphabetical list (Tier 1 lookup)
│   ├── categories.md                 # Grouped by category (Tier 2 browsing)
│   └── templates/                    # 71 DESIGN.md files + manifest.json
│       ├── manifest.json             # Brand metadata (descriptions, hashes, commit)
│       ├── claude.md                 # Each file: ~300 lines of design-system spec
│       ├── stripe.md
│       ├── linear.app.md
│       └── ... (63 more)
├── scripts/
│   ├── apply.sh                      # Copy template → cwd/DESIGN.md
│   ├── list.sh                       # Show catalog
│   └── update-templates.sh           # Sync from getdesign npm package
└── commands/
    ├── apply.md                      # /design-md:apply <brand>
    └── list.md                       # /design-md:list
```

## Rules

1. **Don't invent tokens.** If a user asks for a brand not in the catalog, tell them and suggest the closest match. Never fabricate hex codes, font names, or component specs.
2. **Don't overwrite without permission.** The apply script refuses to clobber an existing `DESIGN.md` unless `--force` is passed.
3. **Brand slugs are canonical.** Use what the manifest says — `linear.app`, `mistral.ai`, `opencode.ai`, `together.ai`, `x.ai`, `theverge` (no dot). Don't guess.
4. **Credit the source.** DESIGN.md files are extracted from publicly visible CSS. Attribution: VoltAgent/awesome-design-md (MIT). The design tokens represent the source brands' public visual identity.
5. **This skill supersedes `showroom`.** The old showroom skill bundled product-showcase prompts inline; DESIGN.md is the durable replacement and composes with nano-banana for image generation.

---

**Source:** [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT License)
**Upstream CLI:** [`getdesign`](https://www.npmjs.com/package/getdesign) — bundled inside that package as `package/templates/*.md`
**Format spec:** [Google Stitch DESIGN.md](https://stitch.withgoogle.com/docs/design-md/format/)
