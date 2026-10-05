---
name: researching-market
description: Integrate Phase 0 and Phase 1A outputs into TAM/SAM/SOM sizing, buyer personas, and market entry signals. Run after `analyzing-source-project` and `researching-industry-landscape` (Phase 1B).
compatibility: Designed for Claude Code
metadata:
  stability: stable
  content-hash: sha256:ecc16abb8d05b90eb5b1ca087357cf2090b636b249dfe28b4f4df1070015bcad
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch, Agent
  argument-hint: [market-or-product-category]
---

# Researching Market (Phase 1B)

**Target**: $ARGUMENTS

Phase 1B of the GTM pipeline. Depends on Phase 0 and Phase 1A. Integrates
technical capability and competitive intelligence into strategic market sizing
and buyer analysis.

## Mode Awareness

Read `config/mode.md` before starting:

- `concise` — Top-down TAM estimate, one primary persona, bullet entry signals
- `detailed` — Bottom-up + top-down sizing, 2-3 personas with full profiles, trend projections
- `conservative` — Use published analyst figures, conservative growth rates
- `ambitious` — Build bottom-up case for expansive TAM, highlight adjacencies

## Inputs

- `results/phase-0/capability-profile.md` — Source project capabilities
- `results/phase-1a/competitor-map.md` — Competitive landscape
- `config/targets.md` — Target market segments
- `config/comments_research.md` — Research scope constraints
- `config/mode.md` — Style and approach settings

## Workflow

1. **Read Phase 0 and Phase 1A outputs** — Synthesize capability and competitive signals
2. **Define addressable market** — Scope TAM, SAM, SOM with methodology
3. **Size the market** — Use cited sources; state assumptions explicitly
4. **Build buyer personas** — Role, pain points, budget authority, buying triggers
5. **Assess entry signals** — What evidence suggests this is the right moment to enter?
6. **Identify risks** — Market timing, regulatory, adoption barriers
7. **Validate against criteria** — Check `config/validation_criteria.md` Phase 1B gates

## Output

Write to `results/phase-1b/`:

### `market-analysis.md`

```markdown
# Market Analysis

## Market Sizing

### TAM (Total Addressable Market)
- Estimate: $[X]B
- Methodology: [top-down / bottom-up]
- Source: [URL, year]

### SAM (Serviceable Addressable Market)
- Estimate: $[X]B
- Scope: [geography, segment, use case]

### SOM (Serviceable Obtainable Market — Year 1-3)
- Estimate: $[X]M
- Assumptions: [list]

## Growth Rate
- [X]% CAGR through [year] — Source: [URL]

## Buyer Personas

### Persona: [Name/Role]
- Title: [job title]
- Pain: [primary pain point]
- Budget authority: [Yes/No/Influence]
- Buying trigger: [what prompts purchase decision]

## Market Entry Signals
- [Signal] — Strength: [High/Medium/Low]

## Risks
- [Risk] — Likelihood: [H/M/L] — Mitigation: [approach]
```

## Rules

- Explicitly state all sizing assumptions — no unexplained numbers
- Every market size figure must have a source and year
- Personas must be grounded in target segments from `config/targets.md`
- Integrate Phase 0 capability signals into entry signal rationale
