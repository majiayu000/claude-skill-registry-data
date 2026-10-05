---
name: researching-industry-landscape
description: Map competitive intelligence and industry landscape; produce a competitor map and whitespace analysis. Run alongside `analyzing-source-project` at the start of the GTM pipeline (Phase 1A).
compatibility: Designed for Claude Code
metadata:
  stability: stable
  content-hash: sha256:63b5d0505a4eb7efa5c9bab7a80fa3542178874fb2ed02ba3d4887d8146e5bf9
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Agent
  argument-hint: [industry-or-product-category]
---

# Researching Industry Landscape (Phase 1A)

**Target**: $ARGUMENTS

Phase 1A of the GTM pipeline. Runs in parallel with Phase 0. Produces competitive
intelligence that feeds Phase 1B (researching-market).

## Mode Awareness

Read `config/mode.md` before starting:

- `concise` — Top 5 competitors, one-line summary per player, key whitespace only
- `detailed` — Full competitor profiles, market map, trend analysis
- `conservative` — Focus on established market leaders and proven segments
- `ambitious` — Identify emerging players, disruption vectors, underserved niches

## Inputs

- `config/targets.md` — Target markets to scope the competitive search
- `config/comments_research.md` — Research constraints (geography, verticals, depth)
- `config/mode.md` — Style and approach settings

## Workflow

1. **Define search scope** from `config/targets.md` and `config/comments_research.md`
2. **Identify competitors** — Direct, adjacent, and indirect players (target 6-10)
3. **Profile each competitor** — Positioning, pricing, target segment, key features
4. **Assess competitive dynamics** — Who wins and why? Who is losing ground?
5. **Map whitespace** — Where are underserved segments or capability gaps?
6. **Identify trends** — Regulatory, technological, or behavioral shifts shaping the landscape
7. **Validate against criteria** — Check `config/validation_criteria.md` Phase 1A gates

## Output

Write to `results/phase-1a/`:

### `competitor-map.md`

```markdown
# Industry Landscape

## Competitor Profiles

### [Competitor Name]
- URL: [url]
- Positioning: [one-liner]
- Target segment: [segment]
- Pricing tier: [free/freemium/paid/enterprise]
- Strengths: [list]
- Weaknesses: [list]
- Source: [URL cited]

## Competitive Dynamics
[Who leads, who is disrupting, key battlegrounds]

## Whitespace Opportunities
1. [Opportunity] — Evidence: [sources]

## Trends Shaping the Landscape
- [Trend] — Impact: [High/Medium/Low]
```

## Rules

- Use public sources only; cite every claim with URL
- Cover direct competitors before adjacent ones
- Whitespace must be specific — not "SMB market" but "SMB fintech compliance tooling"
- Cross-reference competitor weaknesses against Phase 0 capabilities once available
