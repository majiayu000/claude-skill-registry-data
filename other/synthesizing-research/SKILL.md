---
name: synthesizing-research
description: Synthesize all prior research into a unified GTM narrative. Run after `analyzing-contradictions` to prepare for slide deck generation (Phase 5).
compatibility: Designed for Claude Code
metadata:
  stability: stable
  content-hash: sha256:a8c1dc87f705a039a21f114e8b7f28a7f8518948388e7ed17f573ff5949b2160
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch
  argument-hint: [optional-synthesis-focus]
---

# Synthesizing Research (Phase 5)

**Target**: $ARGUMENTS

Phase 5 of the GTM pipeline. Depends on all prior phases (0-4). Produces a
unified GTM narrative integrating technical, market, and strategic findings.
This output drives Phase 6 slide deck generation.

## Mode Awareness

Read `config/mode.md` before starting:

- `concise` — Executive summary (1 page), key findings table, single recommended path
- `detailed` — Full integrated narrative, alternative scenarios, confidence annotations
- `conservative` — Lead with validated evidence; clearly separate confirmed from inferred
- `ambitious` — Lead with opportunity thesis; build the bull case narrative

## Inputs

- `results/phase-0/capability-profile.md`
- `results/phase-1a/competitor-map.md`
- `results/phase-1b/market-analysis.md`
- `results/phase-2/pmf-assessment.md`
- `results/phase-3/gtm-strategy.md`
- `results/phase-4/contradiction-analysis.md`
- `config/comments_gtm.md` — GTM preferences for framing
- `config/mode.md` — Style and approach settings

## Workflow

1. **Read all prior phase outputs** including contradiction resolutions from Phase 4
2. **Construct the narrative arc**: Source capability → Market opportunity → PMF evidence → GTM path
3. **Resolve outstanding contradictions** from Phase 4 into final recommendations
4. **Assign confidence ratings** to all major claims (High/Medium/Low)
5. **Identify the single recommended GTM path** and articulate why
6. **Document alternatives** with tradeoffs for decision-maker context
7. **Validate against criteria** — Check `config/validation_criteria.md` Phase 5 gates

## Output

Write to `results/phase-5/`:

### `synthesis.md`

```markdown
# GTM Research Synthesis

## Executive Summary
[3-5 sentence narrative: what we found, what it means, what we recommend]

## Key Findings by Phase

| Phase | Key Finding | Confidence |
|-------|-------------|------------|
| 0 — Source | [finding] | High/Medium/Low |
| 1A — Landscape | [finding] | High/Medium/Low |
| 1B — Market | [finding] | High/Medium/Low |
| 2 — PMF | [finding] | High/Medium/Low |
| 3 — GTM | [finding] | High/Medium/Low |
| 4 — Gaps | [finding] | High/Medium/Low |

## Integrated GTM Narrative

### The Opportunity
[Market context and timing rationale]

### The Fit
[How product capabilities match market needs]

### The Path
[Recommended GTM motion and why]

## Recommended GTM Path
[Specific, actionable recommendation with first 3 steps]

## Alternative Paths
### Alternative 1: [Name]
- Tradeoff: [upside vs downside]

## Confidence Assessment
- Claims with High confidence: [N]
- Claims with Medium confidence: [N]
- Claims with Low confidence: [N] — [action needed]
```

## Rules

- Low-confidence claims must be explicitly flagged — do not bury uncertainty
- Contradiction resolutions from Phase 4 must be reflected in the narrative
- The recommended path must be specific enough to act on within 30 days
- Reference phase output files by path for traceability
