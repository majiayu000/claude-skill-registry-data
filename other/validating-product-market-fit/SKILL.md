---
name: validating-product-market-fit
description: Score product-market fit from Phase 1B market analysis; produce PMF score, evidence matrix, and risk register. Run after `researching-market` (Phase 2).
compatibility: Designed for Claude Code
metadata:
  stability: stable
  content-hash: sha256:36d5115fa26dc55eac0465fab8e4ac6ae9e168105cc6a9e5f3135bdf0c9eac87
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch
  argument-hint: [product-name-or-hypothesis]
---

# Validating Product-Market Fit (Phase 2)

**Target**: $ARGUMENTS

Phase 2 of the GTM pipeline. Depends on Phase 1B. Scores PMF across multiple
dimensions using evidence from prior phases.

## Mode Awareness

Read `config/mode.md` before starting:

- `concise` — Overall PMF score + top 3 evidence points + top 2 risks
- `detailed` — Full per-dimension scoring, evidence matrix, risk register with mitigations
- `conservative` — Weight negative evidence heavily; set high evidence bar
- `ambitious` — Weight leading indicators and analogous market signals; accept proxy evidence

## Inputs

- `results/phase-1b/market-analysis.md` — Market sizing and buyer personas
- `results/phase-0/capability-profile.md` — Technical capabilities
- `results/phase-1a/competitor-map.md` — Competitive context
- `config/validation_criteria.md` — Phase 2 quality gates
- `config/mode.md` — Style and approach settings

## PMF Scoring Dimensions

Score each dimension 1-10, then compute weighted average:

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Problem severity | 25% | How painful is the problem for buyers? |
| Solution fit | 25% | How well does the product solve it? |
| Market timing | 20% | Is the market ready? |
| Competitive moat | 15% | Can differentiation be sustained? |
| Distribution path | 15% | Is there a clear route to customers? |

## Workflow

1. **Read all Phase 0, 1A, 1B outputs**
2. **Score each dimension** with evidence justification
3. **Compute weighted PMF score** (0-10)
4. **Identify PMF risks** — What would invalidate each dimension?
5. **Propose mitigations** for top risks
6. **Validate against criteria** — Check `config/validation_criteria.md` Phase 2 gates

## Output

Write to `results/phase-2/`:

### `pmf-assessment.md`

```markdown
# Product-Market Fit Assessment

## PMF Score: [X.X] / 10

## Dimension Scores

| Dimension | Score | Evidence |
|-----------|-------|----------|
| Problem severity | [X]/10 | [evidence] |
| Solution fit | [X]/10 | [evidence] |
| Market timing | [X]/10 | [evidence] |
| Competitive moat | [X]/10 | [evidence] |
| Distribution path | [X]/10 | [evidence] |

## Evidence For PMF
- [evidence point] — Source: [phase output or URL]

## Evidence Against PMF
- [counter-evidence] — Source: [phase output or URL]

## PMF Risk Register

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [risk] | H/M/L | H/M/L | [approach] |

## Recommendation
[Proceed to GTM / Iterate on product / Pivot hypothesis]
```

## Rules

- Both supporting and contradicting evidence are mandatory
- Score deflation is preferable to inflation — honest assessment protects GTM investment
- Mitigation suggestions must be actionable, not generic
