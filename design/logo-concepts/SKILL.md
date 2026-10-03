---
skill_id: logo-concepts
name: Logo Concepts — editable SVG logo directions you can ship
description: "Generate logo directions — \"give me logo concepts for\", \"logo ideas for\", \"design a logo for\". Emits 3 to 5 distinct directions as real editable SVG vector code, not raster mockups."
version: 1.0.0
category: design
office: cpo
lead_agent: ui-ux-designer
everyday_skill: true
triggers:
  - "give me logo concepts for"
  - "logo ideas for"
  - "design a logo for"
collaborates_with:
  - ui-ux-designer
  - brand-guardian      # keep concepts inside the brand kit if one exists
references:
  wraps_skills: .claude/skills/brand/SKILL.md · .claude/skills/ui-styling/SKILL.md · .claude/skills/banner-design/SKILL.md
  adr_moat_framing: documents/ADRs/ADR-007-behavioral-moat-framing-doctrine.md
  adr_confidence: documents/ADRs/ADR-010-confidence-tag-technical-educator-rubric.md
confidence_default: 🟡 MEDIUM
---

# Logo Concepts

> **Does:** generates clean, **editable SVG** logo directions you can refine and ship.
> **Solves:** paying for five logo rounds before seeing anything usable.
> **Triggers on:** *"give me logo concepts for [name]"*

## How Maxim does this

Routes to the `brand` + `ui-styling` + `banner-design` depth and emits **3–5 distinct SVG directions** (real vector code you can edit — not a flat raster). If a **Brand Kit** is set, concepts stay inside your locked colors/fonts; if not, it proposes a palette and says so.

## Behavioral overlay

- **Frameworks (cited per ADR-007):** **Gestalt principles** (closure, figure-ground) · **Color Psychology** · **Golden Ratio / visual balance** · **Pre-attentive attributes** (does it read at 16px?).
- **Confidence tag (ADR-010):** default **🟡 MEDIUM** — a logo is subjective; this gives you strong, editable *directions* to pursue, not a finished mark. Each concept names the idea it expresses so you choose on strategy, not taste.
- **No-fabrication:** it won't claim trademark-clearance or originality — that's your designer/lawyer's call, and it says so.

## Output

3–5 editable SVG concepts · the idea behind each · the one or two worth developing · usage notes (favicon / dark-bg legibility).
