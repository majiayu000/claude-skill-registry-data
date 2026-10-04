---
name: awesome-design-md
description: |
  Primary design skill — the default for ALL design tasks across every project.
  Loaded automatically whenever a design, UI, UX, or visual task is requested.
  After any design deliverable is produced, this skill runs a mandatory review pass
  before marking the work complete.
  Sources 59 curated design system references from the design-refs/ subdirectory,
  covering the world's best product design (Stripe, Linear, Figma, Airbnb, Notion, etc.).
triggers:
  - design
  - ui design
  - ux design
  - visual design
  - redesign
  - design system
  - make it look like
  - inspired by
  - apply design
  - design review
  - review design
  - ui/ux
scope: global
dept: all
priority: implementation
aliases:
  - design-md
  - design-reference
  - design-task
author: voltagent + community
provenance: skill-seekers + custom
---

# Awesome Design MD

Primary design execution skill — loaded by default for every design task.

## Workflow

Every design task follows this two-phase workflow:

### Phase 1 — Execute

1. **Understand the request** — identify the product domain, audience, and key interaction patterns
2. **Select reference design(s)** — search `design-refs/` for the closest match (or fuse two)
3. **Apply design tokens** — extract colors, typography, spacing, motion, and component patterns from the reference
4. **Implement** — produce UI code, design tokens, or component specs using the reference as the north star
5. **Annotate** — document design decisions, token mappings, and deviations from the reference

### Phase 2 — Review Pass (MANDATORY)

**Never mark design work complete without running this pass.**

The review pass checks:
- **Visual fidelity** — do the implemented components match the reference's aesthetic?
- **Token adherence** — are CSS variables / design tokens correctly mapped?
- **Typography consistency** — font family, scale, weight, and tracking match reference?
- **Spacing & rhythm** — do margins, padding, and gap values follow the reference system?
- **Component completeness** — are all states covered (default, hover, active, disabled, error)?
- **Accessibility** — contrast ratios, focus states, and semantic HTML
- **Responsive behavior** — does the design scale gracefully across breakpoints?

Review findings → document as a numbered list of fixes. Apply fixes before declaring done.

### Delegation

If the design task spans multiple domains, delegate sub-tasks to specialized agents:
- `frontend` skill → implement UI components
- `figma` skill → produce Figma assets or import design to Figma
- `huashu-design` skill → HTML prototypes, app mockups, design philosophy exploration, animation/MP4/GIF export
- `design-review` skill → external design audit (optional deep pass)
- `copywriting` skill → product copy and microcopy within the design

Always delegate AFTER Phase 1 execution, not instead of it.

## Reference Library: design-refs/

59 design systems are available. Search by product domain or keyword:

| File | Domain / Aesthetic |
|------|--------------------|
| airbnb.md | Travel marketplace, warm coral accent, photography-driven, rounded UI |
| airtable.md | Collaborative spreadsheet, colorful, blocks-based |
| apple.md | Premium hardware/software, minimal, typography-first |
| bmw.md | Luxury automotive, dark, precision engineering |
| cal.md | Calendar/scheduling, clean, time-focused |
| claude.md | AI chat, conversational, readable, warm |
| clay.md | Sales/pipeline, dark luxury, gradient accents |
| clickhouse.md | Data/analytics, technical, monospace, high-density |
| cohere.md | AI/ML platform, minimal, developer-friendly |
| coinbase.md | Crypto exchange, clean, trust-forward |
| composio.md | AI integrations, tool-focused, developer aesthetic |
| cursor.md | AI IDE, minimal dark, coding-first |
| elevenlabs.md | Audio/AI, futuristic, sound-wave motifs |
| expo.md | React Native dev, approachable, friendly |
| ferrari.md | Luxury automotive, deep red, precision |
| figma.md | Design tool, grid-focused, minimal chrome |
| framer.md | No-code web builder, kinetic, modern |
| hashicorp.md | Infrastructure tooling, developer, minimal |
| ibm.md | Enterprise software, systematic, IBM Plex |
| intercom.md | Customer messaging, friendly, conversational |
| kraken.md | Crypto exchange, bold, dark |
| lamborghini.md | Super-luxury automotive, angular, aggressive |
| linear.app.md | Project management, minimal, keyboard-first |
| lovable.md | AI app builder, friendly, accessible |
| mintlify.md | Documentation, clean, developer-focused |
| miro.md | Whiteboard/collaboration, infinite canvas |
| mistral.ai.md | AI/ML platform, elegant, European minimal |
| mongodb.md | Database, technical, leaf-green brand |
| notion.md | All-in-one workspace, block-based, versatile |
| nvidia.md | GPU/AI hardware, futuristic, dark |
| ollama.md | Local AI, developer, terminal-forward |
| opencode.ai.md | AI code platform, developer, minimal |
| pinterest.md | Visual discovery, grid, masonry, inspirational |
| posthog.md | Product analytics, clean, data-forward |
| raycast.md | Productivity tool, spotlight-style, fast |
| renault.md | Automotive, electric, modern European |
| replicate.md | AI model hosting, developer, minimal |
| resend.md | Email API, developer, clean |
| revolut.md | Fintech, dark, premium, card-forward |
| runwayml.md | Video/AI, creative, dark cinematic |
| sanity.md | CMS, developer-friendly, structured |
| semrush.md | SEO/marketing, data-dense, professional |
| sentry.md | Error monitoring, technical, dark |
| spacex.md | Aerospace, futuristic, stark |
| spotify.md | Music streaming, dark, green brand, card-based |
| stripe.md | Payments, clean, confident, trust-forward |
| supabase.md | Backend-as-a-service, developer, open-source |
| superhuman.md | Email client, speed-obsessed, keyboard-first |
| tesla.md | EV/tech, minimal, large type, dark |
| together.ai.md | AI compute, developer, modern |
| uber.md | Mobility/logistics, map-centric, card UI |
| vercel.md | Deployment platform, minimal, monochrome |
| voltagent.md | AI agent platform, clean, technical |
| warp.md | Terminal, retro-futuristic, opinionated |
| webflow.md | No-code web, visual, responsive-first |
| wise.md | Global finance, clean, multi-currency |
| x.ai.md | AI (x.ai Grok), bold, modern |
| zapier.md | Automation, workflow, connector-focused |

## Usage Example

```
User: Build a checkout page inspired by Stripe
→ Load design-refs/stripe.md
→ Extract: colors (#6366f1, #0f172a), typography (Inter, specific scale),
  spacing (4px base unit), shadows, border-radius, component states
→ Implement checkout page using these tokens
→ Run Phase 2 Review: token check, state check, accessibility check
→ If issues found: fix before marking done
```

## Design Token Extraction

When applying a reference, extract into this structure:

```markdown
## Applied Design Tokens (from [reference].md)

### Colors
- Primary: [hex] — usage: [where]
- Background: [hex]
- Text: [hex]
- Accent: [hex]
- Border: [hex]

### Typography
- Font family: [name] with [fallback]
- Heading: [size] / [weight] / [tracking]
- Body: [size] / [weight] / [line-height]
- Mono: [font] for [purpose]

### Spacing
- Base unit: [n]px
- Component padding: [values]
- Section gaps: [values]

### Motion
- Duration: [ms]
- Easing: [function]
- Motion principle: [description]

### Components
- Button: [styles per state]
- Input: [styles per state]
- Card: [shadow, radius, border]
```

## Design Review Checklist

Used in Phase 2 after any implementation:

```
[ ] Visual hierarchy matches reference
[ ] Color palette applied correctly (primary, secondary, accent, surface)
[ ] Typography scale and weight consistent with reference
[ ] Spacing system follows base unit
[ ] All interactive states implemented (default, hover, active, disabled, focus, error)
[ ] Border radius consistent
[ ] Shadows match reference intensity
[ ] No placeholder or TODOs left in UI
[ ] Accessible contrast (WCAG AA minimum)
[ ] Focus indicators visible
[ ] Responsive at mobile / tablet / desktop
[ ] Design tokens documented in the output
[ ] Any deviations from reference documented and justified
```

## Notes

- When the user's project already has a design system, use it as the **primary**
  and layer the reference design on top — don't replace existing tokens wholesale.
- For ambiguous requests, pick the most relevant reference and note the choice in
  the output. You may fuse two references with a clear justification.
- This skill replaces generic "design" prompts with structured, reference-driven work.