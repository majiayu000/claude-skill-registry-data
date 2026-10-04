---
name: frontend-design
description: "Design skill for external, non-YURI, non-Kagami surfaces. Use when building client work, external products, public-facing sites, or any UI that is NOT YURI HUD or Kagami. Enforces high-end intentional design systems, prevents AI slop. For YURI/Kagami surfaces, use design-master instead."
triggers:
  - "build a UI"
  - "design a landing page"
  - "fix UX"
  - "create a page"
  - "build a website"
  - "make it look professional"
  - "no AI slop"
  - "production design"
  - "web design"
  - "design principles"
  - "client site"
  - "external product"
  - "public page"
routing_note: "EXTERNAL SURFACES ONLY. Do NOT use for YURI HUD or Kagami — those route to design-master. This skill is for: client work, external products, non-YURI public pages, or any surface outside the YURI OS ecosystem."
scope: harness
invocation: ability
---

# Frontend Design — External Surfaces

Use this skill to act as Creative Director for external, non-YURI UI/UX tasks.

## Scope
**In scope:** Client sites, external products, public landing pages, any UI outside YURI OS.
**Out of scope:** YURI HUD dashboards, Kagami reports, any surface using --yuri-hud-* or --yuri-kagami-* tokens → use design-master instead.

## Load Order (External Work)
1. Define industry keywords and brand tone for this project
2. Establish CSS variables for colors, typography, spacing
3. Pick distinctive font pairing (no Inter/DM Sans by default — use something with personality)
4. Select 3-7 references from frontier atlas or Design Radar (not YURI internal packs)
5. Reference: `03_RESOURCES/References/design-packs/frontier-design-intelligence/00-start-here.md`
6. Reference: `03_RESOURCES/References/design-packs/framer-university-resource-atlas/00-start-here.md` for motion/Framer work

## Core Principles
- **Anti-Generic Mandate**: Refuse default choices. No Inter/Arial default. No generic SaaS hero.
- **Reference First**: Pick 3-7 sources before layout, typography, or motion decisions.
- **Motion Integration**: CSS animations or framer-motion for micro-interactions.
- **Verification**: Browser/screenshot check at desktop and mobile before declaring done.

## Design System Phase (before any component work)
Define explicitly:
- Industry keywords and brand tone
- Color variables with roles
- Typography scale + font pairing
- Spacing system
- Reference set (named, with rationale)

## Session Notes

### 2026-06-13
- session: 116m | peak ctx: 0% | compacts: 0
- tools: Bash×947, Read×345, Edit×171, StructuredOutput×82, Write×63, TodoWrite×25, ToolSearch×8, Workflow×6, Agent×3, ScheduleWakeup×2, TaskStop×1, PushNotification×1, AskUserQuestion×1
- corrections: rick i have a fun little task for you. I will be giving you the task of going through trending repos on github, scanning them, compare yuri to those, see what we can adopt and rebuild better in yuri u
- errors: none

### 2026-05-21
- session: 10m | peak ctx: 0% | compacts: 0
- tools: Read×24, Glob×1
- corrections: none
- errors: none

### 2026-05-20
- Scoped to external/non-YURI surfaces only (v2 re-scoping)
- YURI/Kagami work now exclusively routes to design-master
