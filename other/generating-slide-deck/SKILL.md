---
name: generating-slide-deck
description: Generate an investor or stakeholder presentation from Phase 5 synthesis; produces a structured slide outline with headlines, talking points, and data citations. Run after `synthesizing-research` (Phase 6).
compatibility: Designed for Claude Code
metadata:
  stability: stable
  content-hash: sha256:b5fd7c159f176dc92aaab3f6c8ec224123bb6e9277404a480c8a1f3072fe682a
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch
  argument-hint: [audience-type]
---

# Generating Slide Deck (Phase 6)

**Target**: $ARGUMENTS

Phase 6 of the GTM pipeline. Depends on Phase 5. Generates a structured
investor or stakeholder presentation from the synthesized GTM research.

## Mode Awareness

Read `config/mode.md` before starting:

- `concise` — 8-10 slides, one data point per slide, minimal text
- `detailed` — 12-15 slides, supporting evidence slides, appendix section
- `conservative` — Data-led narrative, proof-before-vision structure
- `ambitious` — Vision-first narrative, bold claims with supporting data, moonshot framing

## Inputs

- `results/phase-5/synthesis.md` — Integrated GTM narrative (primary source)
- `config/comments_gtm.md` — Audience type, deck length, format preferences
- `config/mode.md` — Style and approach settings

## Slide Structure

Adapt based on audience from `config/comments_gtm.md`:

### Investor Deck (default)

1. Title — Product name + one-liner
2. Problem — Pain point with market evidence
3. Solution — How the product solves it
4. Market Size — TAM/SAM/SOM
5. Product — Key capabilities and differentiators
6. Traction / PMF Evidence — Signals and validation
7. Competitive Landscape — Positioning map
8. GTM Strategy — Channels, ICP, motion
9. Team (placeholder if not available)
10. Ask / Next Steps

### Enterprise Buyer Deck

1. Executive Summary
2. Problem Statement
3. Solution Overview
4. Technical Fit
5. Competitive Differentiation
6. Implementation Path
7. ROI / Business Case
8. Next Steps

### Internal Leadership Deck

1. Opportunity Summary
2. Market Analysis
3. PMF Assessment
4. Recommended GTM Path
5. Resource Requirements
6. Risks and Mitigations
7. Decision Required

## Workflow

1. **Read Phase 5 synthesis** and `config/comments_gtm.md` for audience preference
2. **Select appropriate slide structure** based on audience
3. **Write each slide** with: headline (insight), 3-5 bullets, data citations
4. **Apply mode settings** — concise vs detailed depth, conservative vs ambitious framing
5. **Add appendix slides** for supporting data (detailed mode only)
6. **Validate against criteria** — Check `config/validation_criteria.md` Phase 6 gates

## Output

Write to `results/phase-6/`:

### `slide-deck.md`

```markdown
# [Product Name] — [Audience Type] Deck

---

## Slide 1: [Title]

**Headline**: [Insight-driven headline, not a topic label]

Key points:
- [bullet]
- [bullet]
- [bullet]

Speaker notes: [Optional: key talking point]

---

## Slide 2: [Title]

**Headline**: [Insight-driven headline]

[Data point] — Source: [citation]

Key points:
- [bullet]

---
[Continue for all slides]

---

## Appendix (detailed mode only)

### A1: [Supporting Data Slide Title]
[Data table or extended evidence]
```

## Rules

- Every slide headline must be an insight, not a topic (e.g. "SMB compliance costs $40K/year" not "Market Overview")
- No slide exceeds 5 bullets
- All data slides must cite source inline
- Deck must follow length from `config/comments_gtm.md`; do not exceed it
- Phase 5 synthesis is the single source of truth — do not introduce new claims in the deck
