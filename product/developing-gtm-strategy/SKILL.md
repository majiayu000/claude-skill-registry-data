---
name: developing-gtm-strategy
description: Develop customer segmentation, channel selection, and a 90-day launch plan from Phase 2 PMF assessment. Run after `validating-product-market-fit` (Phase 3).
compatibility: Designed for Claude Code
metadata:
  stability: stable
  content-hash: sha256:aba8abd399d1b9d2af36338ff5fc9da2831dd5773d4e5dc972efa1daf6af3a4c
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch
  argument-hint: [product-name]
---

# Developing GTM Strategy (Phase 3)

**Target**: $ARGUMENTS

Phase 3 of the GTM pipeline. Depends on Phase 2. Builds the actionable GTM
plan: customer segmentation, ICP definition, channel strategy, and launch
milestones.

## Mode Awareness

Read `config/mode.md` before starting:

- `concise` — Top segment, top 2 channels, 90-day milestones (bullet list)
- `detailed` — Full ICP profiles, channel analysis matrix, sequenced roadmap
- `conservative` — Proven channels (inbound, direct sales, partnerships); minimize burn
- `ambitious` — Multi-channel blitz, community-led + product-led hybrid, aggressive land-and-expand

## Inputs

- `results/phase-2/pmf-assessment.md` — PMF score and risk register
- `results/phase-1b/market-analysis.md` — Buyer personas and market sizing
- `results/phase-1a/competitor-map.md` — Competitor channel strategies
- `config/comments_gtm.md` — GTM preferences and constraints
- `config/mode.md` — Style and approach settings

## Workflow

1. **Read Phase 2 PMF output** — Use recommendation and risk register to shape strategy
2. **Define customer segments** — Prioritize 1-3 segments with ICP definitions
3. **Select GTM channels** — Evaluate and rank by reach/cost/fit for each segment
4. **Define positioning** — One-liner, value prop, key proof points per segment
5. **Build 90-day launch plan** — Milestones, owners, success metrics
6. **Validate against criteria** — Check `config/validation_criteria.md` Phase 3 gates

## Output

Write to `results/phase-3/`:

### `gtm-strategy.md`

```markdown
# GTM Strategy

## Target Segments

### Segment 1: [Name]
- ICP: [job title, company size, industry, trigger event]
- Pain: [primary pain]
- Value prop: [one sentence]
- Proof point: [evidence or analogy]

## Channel Strategy

| Channel | Reach | Cost | Fit | Priority |
|---------|-------|------|-----|----------|
| [channel] | H/M/L | H/M/L | H/M/L | 1/2/3 |

## Positioning

### One-Liner
"[Product] is the [category] for [segment] that [differentiator]."

### Key Proof Points
1. [proof point]

## 90-Day Launch Plan

| Week | Milestone | Owner | Success Metric |
|------|-----------|-------|----------------|
| 1-2  | [milestone] | [role] | [metric] |
| 3-6  | [milestone] | [role] | [metric] |
| 7-12 | [milestone] | [role] | [metric] |
```

## Rules

- ICP definitions must be specific enough to identify a named prospect
- Channel priority must account for budget tier from `config/comments_gtm.md`
- Every milestone needs a measurable success metric
- Align positioning against competitor weaknesses from Phase 1A
