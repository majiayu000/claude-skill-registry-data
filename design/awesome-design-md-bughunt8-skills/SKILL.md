---
name: awesome-design-md
description: Curated collection of 73 production-grade DESIGN.md files extracted from real developer-focused websites. Drop any DESIGN.md into your project root and instruct your AI coding agent to build UI that matches the target brand's design language — covering typography, color, layout, components, motion, and anti-patterns.
---

# Awesome DESIGN.md — AI UI Design Reference Skill

## Overview

This skill provides **73 ready-to-use DESIGN.md files** sourced from real, production websites across AI platforms, developer tools, fintech, automotive, and more. Each file encodes a site's full design language — color tokens, typography rules, component states, layout principles, motion specs, and explicit anti-patterns — in plain Markdown that any AI coding agent can read directly.

**Source:** [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)

---

## What is DESIGN.md?

[DESIGN.md](https://stitch.withgoogle.com/docs/design-md/overview/) is a concept introduced by Google Stitch. It is a plain-text design system document that AI agents read to generate visually consistent UI.

| File | Who reads it | What it defines |
|------|-------------|-----------------|
| `AGENTS.md` | Coding agents | How to build the project |
| `DESIGN.md` | Design agents | How the project should look and feel |

It is just a Markdown file — no Figma exports, no JSON schemas, no special tooling. Drop it into your project root and any AI coding agent (Cursor, Copilot, Claude, Gemini CLI) or Google Stitch instantly understands how your UI should look.

---

## How to Use This Skill

1. **Browse the catalog below** and pick the brand whose aesthetic you want to replicate or draw inspiration from.
2. **Copy the corresponding `DESIGN.md`** from `design-md/<brand>/DESIGN.md` into your project root (or reference it directly from this skill path).
3. **Tell your AI agent** to use it:
   - *"Use the DESIGN.md in this project to style all components."*
   - *"Build a landing page that follows the DESIGN.md system."*
   - *"Generate a dashboard UI consistent with the DESIGN.md."*
4. The agent will read the file and apply the design tokens, typography, color palette, and component rules automatically.

### Mixing Styles
You can also use multiple DESIGN.md files as reference points:
- *"Use the Stripe DESIGN.md for color and typography, but adopt Linear's spacing and layout philosophy."*

---

## What Each DESIGN.md Contains

Every file follows the [Stitch DESIGN.md specification](https://stitch.withgoogle.com/docs/design-md/specification/) with extended sections:

| # | Section | What it captures |
|---|---------|-----------------|
| 1 | Visual Theme & Atmosphere | Mood, density, design philosophy |
| 2 | Color Palette & Roles | Semantic name + hex code + functional role |
| 3 | Typography Rules | Font families, full hierarchy table |
| 4 | Component Stylings | Buttons, cards, inputs, navigation with states |
| 5 | Layout Principles | Spacing scale, grid, whitespace philosophy |
| 6 | Depth & Elevation | Shadow system, surface hierarchy |
| 7 | Do's and Don'ts | Design guardrails and anti-patterns |
| 8 | Responsive Behavior | Breakpoints, touch targets, collapsing strategy |
| 9 | Agent Prompt Guide | Quick color reference, ready-to-use prompts |

---

## Catalog

### AI & LLM Platforms

| Brand | Path | Description |
|-------|------|-------------|
| **Claude** | `design-md/claude/DESIGN.md` | Anthropic's AI assistant. Warm terracotta accent, clean editorial layout |
| **Cohere** | `design-md/cohere/DESIGN.md` | Enterprise AI platform. Vibrant gradients, data-rich dashboard aesthetic |
| **ElevenLabs** | `design-md/elevenlabs/DESIGN.md` | AI voice platform. Dark cinematic UI, audio-waveform aesthetics |
| **Minimax** | `design-md/minimax/DESIGN.md` | AI model provider. Bold dark interface with neon accents |
| **Mistral AI** | `design-md/mistral.ai/DESIGN.md` | Open-weight LLM provider. French-engineered minimalism, purple-toned |
| **Ollama** | `design-md/ollama/DESIGN.md` | Run LLMs locally. Terminal-first, monochrome simplicity |
| **OpenCode AI** | `design-md/opencode.ai/DESIGN.md` | AI coding platform. Developer-centric dark theme |
| **Replicate** | `design-md/replicate/DESIGN.md` | Run ML models via API. Clean white canvas, code-forward |
| **Runway** | `design-md/runwayml/DESIGN.md` | AI creative-tools platform. Cinematic dark heroes, paper-white reading bands |
| **Together AI** | `design-md/together.ai/DESIGN.md` | Open-source AI infrastructure. Technical, blueprint-style design |
| **VoltAgent** | `design-md/voltagent/DESIGN.md` | AI agent framework. Void-black canvas, emerald accent, terminal-native |
| **xAI** | `design-md/x.ai/DESIGN.md` | Elon Musk's AI lab. Stark monochrome, futuristic minimalism |

### Developer Tools & IDEs

| Brand | Path | Description |
|-------|------|-------------|
| **Cursor** | `design-md/cursor/DESIGN.md` | AI-first code editor. Sleek dark interface, gradient accents |
| **Expo** | `design-md/expo/DESIGN.md` | React Native platform. Dark theme, tight letter-spacing, code-centric |
| **Lovable** | `design-md/lovable/DESIGN.md` | AI full-stack builder. Playful gradients, friendly dev aesthetic |
| **Raycast** | `design-md/raycast/DESIGN.md` | Productivity launcher. Sleek dark chrome, vibrant gradient accents |
| **Superhuman** | `design-md/superhuman/DESIGN.md` | Fast email client. Premium dark UI, keyboard-first, purple glow |
| **Vercel** | `design-md/vercel/DESIGN.md` | Frontend deployment platform. Black and white precision, Geist font |
| **Warp** | `design-md/warp/DESIGN.md` | Modern terminal. Dark IDE-like interface, block-based command UI |

### Backend, Database & DevOps

| Brand | Path | Description |
|-------|------|-------------|
| **ClickHouse** | `design-md/clickhouse/DESIGN.md` | Fast analytics database. Yellow-accented, technical documentation style |
| **Composio** | `design-md/composio/DESIGN.md` | Tool integration platform. Modern dark with colorful integration icons |
| **HashiCorp** | `design-md/hashicorp/DESIGN.md` | Infrastructure automation. Enterprise-clean, black and white |
| **MongoDB** | `design-md/mongodb/DESIGN.md` | Document database. Green leaf branding, developer documentation focus |
| **PostHog** | `design-md/posthog/DESIGN.md` | Product analytics. Playful hedgehog branding, developer-friendly dark UI |
| **Sanity** | `design-md/sanity/DESIGN.md` | Headless content platform. 112px display type, IBM Plex Mono, coral-red CTA |
| **Sentry** | `design-md/sentry/DESIGN.md` | Error monitoring. Dark dashboard, data-dense, pink-purple accent |
| **Supabase** | `design-md/supabase/DESIGN.md` | Open-source Firebase alternative. Dark emerald theme, code-first |

### Productivity & SaaS

| Brand | Path | Description |
|-------|------|-------------|
| **Cal.com** | `design-md/cal/DESIGN.md` | Open-source scheduling. Clean neutral UI, developer-oriented simplicity |
| **Intercom** | `design-md/intercom/DESIGN.md` | Customer messaging. Friendly blue palette, conversational UI patterns |
| **Linear** | `design-md/linear.app/DESIGN.md` | Project management for engineers. Ultra-minimal, precise, purple accent |
| **Mintlify** | `design-md/mintlify/DESIGN.md` | Documentation platform. Clean, green-accented, reading-optimized |
| **Notion** | `design-md/notion/DESIGN.md` | All-in-one workspace. Warm minimalism, serif headings, soft surfaces |
| **Resend** | `design-md/resend/DESIGN.md` | Email API for developers. Minimal dark theme, monospace accents |
| **Slack** | `design-md/slack/DESIGN.md` | Team messaging platform. Aubergine sidebar, friendly multi-color palette |
| **Zapier** | `design-md/zapier/DESIGN.md` | Automation platform. Warm orange, friendly illustration-driven |

### Design & Creative Tools

| Brand | Path | Description |
|-------|------|-------------|
| **Airtable** | `design-md/airtable/DESIGN.md` | Spreadsheet-database hybrid. Colorful, friendly, structured data aesthetic |
| **Clay** | `design-md/clay/DESIGN.md` | Creative agency. Organic shapes, soft gradients, art-directed layout |
| **Figma** | `design-md/figma/DESIGN.md` | Collaborative design tool. Vibrant multi-color, playful yet professional |
| **Framer** | `design-md/framer/DESIGN.md` | Website builder. Bold black and blue, motion-first, design-forward |
| **Miro** | `design-md/miro/DESIGN.md` | Visual collaboration. Bright yellow accent, infinite canvas aesthetic |
| **Webflow** | `design-md/webflow/DESIGN.md` | Visual web builder. Blue-accented, polished marketing site aesthetic |

### Fintech & Crypto

| Brand | Path | Description |
|-------|------|-------------|
| **Binance** | `design-md/binance/DESIGN.md` | Crypto exchange. Bold Binance Yellow on monochrome, trading-floor urgency |
| **Coinbase** | `design-md/coinbase/DESIGN.md` | Crypto exchange. Clean blue identity, trust-focused, institutional feel |
| **Kraken** | `design-md/kraken/DESIGN.md` | Crypto trading platform. Purple-accented dark UI, data-dense dashboards |
| **Mastercard** | `design-md/mastercard/DESIGN.md` | Global payments network. Warm cream canvas, orbital pill shapes |
| **Revolut** | `design-md/revolut/DESIGN.md` | Digital banking. Sleek dark interface, gradient cards, fintech precision |
| **Stripe** | `design-md/stripe/DESIGN.md` | Payment infrastructure. Signature purple gradients, weight-300 elegance |
| **Wise** | `design-md/wise/DESIGN.md` | International money transfer. Bright green accent, friendly and clear |

### E-commerce & Retail

| Brand | Path | Description |
|-------|------|-------------|
| **Airbnb** | `design-md/airbnb/DESIGN.md` | Travel marketplace. Warm coral accent, photography-driven, rounded UI |
| **Meta** | `design-md/meta/DESIGN.md` | Tech retail store. Photography-first, binary light/dark surfaces, Meta Blue CTAs |
| **Nike** | `design-md/nike/DESIGN.md` | Athletic retail. Monochrome UI, massive uppercase Futura, full-bleed photography |
| **Shopify** | `design-md/shopify/DESIGN.md` | E-commerce platform. Dark-first cinematic, neon green accent |
| **Starbucks** | `design-md/starbucks/DESIGN.md` | Coffee retail. Four-tier earth-green system, warm cream canvas, SoDoSans typography |

### Media & Consumer Tech

| Brand | Path | Description |
|-------|------|-------------|
| **Apple** | `design-md/apple/DESIGN.md` | Consumer electronics. Premium white space, SF Pro, cinematic imagery |
| **HP** | `design-md/hp/DESIGN.md` | PC and printer maker. Pure white canvas, HP Electric Blue, geometric Forma DJR Micro |
| **IBM** | `design-md/ibm/DESIGN.md` | Enterprise technology. Carbon design system, structured blue palette |
| **NVIDIA** | `design-md/nvidia/DESIGN.md` | GPU computing. Green-black energy, technical power aesthetic |
| **Pinterest** | `design-md/pinterest/DESIGN.md` | Visual discovery platform. Red accent, masonry grid, image-first |
| **PlayStation** | `design-md/playstation/DESIGN.md` | Gaming console retail. Three-surface channel layout, cyan hover-scale |
| **SpaceX** | `design-md/spacex/DESIGN.md` | Space technology. Stark black and white, full-bleed imagery, futuristic |
| **Spotify** | `design-md/spotify/DESIGN.md` | Music streaming. Vibrant green on dark, bold type, album-art-driven |
| **The Verge** | `design-md/theverge/DESIGN.md` | Tech editorial media. Acid-mint and ultraviolet accents, Manuka display type |
| **Uber** | `design-md/uber/DESIGN.md` | Mobility platform. Bold black and white, tight type, urban energy |
| **Vodafone** | `design-md/vodafone/DESIGN.md` | Global telecom brand. Monumental uppercase display, Vodafone Red chapter bands |
| **WIRED** | `design-md/wired/DESIGN.md` | Tech magazine. Paper-white broadsheet density, custom serif, ink-blue links |

### Automotive

| Brand | Path | Description |
|-------|------|-------------|
| **BMW** | `design-md/bmw/DESIGN.md` | Luxury automotive. Dark premium surfaces, precise German engineering aesthetic |
| **BMW M** | `design-md/bmw-m/DESIGN.md` | Performance automotive. Motorsport-inspired contrast, M color accents |
| **Bugatti** | `design-md/bugatti/DESIGN.md` | Luxury hypercar. Cinema-black canvas, monochrome austerity, monumental display type |
| **Ferrari** | `design-md/ferrari/DESIGN.md` | Luxury automotive. Chiaroscuro black-white editorial, Ferrari Red with extreme sparseness |
| **Lamborghini** | `design-md/lamborghini/DESIGN.md` | Luxury automotive. True black cathedral, gold accent, LamboType custom Neo-Grotesk |
| **Renault** | `design-md/renault/DESIGN.md` | French automotive. Vivid aurora gradients, NouvelR proprietary typeface |
| **Tesla** | `design-md/tesla/DESIGN.md` | Electric vehicles. Radical subtraction, cinematic full-viewport photography |

### Retro Web

| Brand | Path | Description |
|-------|------|-------------|
| **Dell (1996)** | `design-md/dell-1996/DESIGN.md` | Catalog-era enterprise web. Flat color-block ribbon cards, chunky Helvetica-Black |
| **Nintendo.com (2001)** | `design-md/nintendo-2001/DESIGN.md` | Y2K console chrome web. Brushed-periwinkle beveled metal panels, halftone nav |

---

## Example Agent Prompts

After dropping a DESIGN.md into your project root:

```
"Build a SaaS landing page following this project's DESIGN.md."
"Create a dashboard layout consistent with the DESIGN.md color palette and typography."
"Generate a pricing page that uses the component styles defined in DESIGN.md."
"Redesign this component to match the motion and interaction patterns in DESIGN.md."
```

For direct reference without copying:
```
"Use skills/design/awesome-design-md/design-md/stripe/DESIGN.md as the design system for this project."
```

---

## Tips

- **For SaaS / dashboards:** Start with Linear, Vercel, Supabase, or Notion.
- **For dark developer tools:** Try Cursor, Warp, Raycast, or Sentry.
- **For premium/luxury UI:** Ferrari, Apple, Stripe, or Bugatti.
- **For fintech apps:** Revolut, Stripe, or Wise.
- **For editorial/media sites:** The Verge, WIRED, or Sanity.
- **For retro/nostalgic projects:** Dell (1996) or Nintendo.com (2001).
