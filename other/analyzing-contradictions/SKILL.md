---
name: analyzing-contradictions
description: Detect gaps and contradictions across all prior phases; surface cross-phase tensions, unresolved assumptions, and sales/investor objections. Run after `developing-gtm-strategy` (Phase 4).
compatibility: Designed for Claude Code
metadata:
  stability: stable
  content-hash: sha256:09aa54c11c2e6368450e5f48f564f8ba85056eb4c3615d6684745c8501a12784
  allowed-tools: Read, Write, Glob, Grep, WebSearch, WebFetch
  argument-hint: [optional-focus-area]
---

# Analyzing Contradictions (Phase 4)

**Target**: $ARGUMENTS

Phase 4 of the GTM pipeline. Depends on Phase 3. Reviews all prior phase outputs
for internal contradictions, unresolved tensions, and gaps that could undermine
the GTM strategy.

## Mode Awareness

Read `config/mode.md` before starting:

- `concise` — Top 3 contradictions + top 5 objections (brief)
- `detailed` — Full contradiction register, root cause analysis, resolution roadmap
- `conservative` — Surface all contradictions regardless of severity; prefer resolution over ignoring
- `ambitious` — Frame contradictions as opportunities; propose bold resolutions

## Inputs

- `results/phase-0/capability-profile.md`
- `results/phase-1a/competitor-map.md`
- `results/phase-1b/market-analysis.md`
- `results/phase-2/pmf-assessment.md`
- `results/phase-3/gtm-strategy.md`
- `config/mode.md` — Style and approach settings

## Contradiction Detection Areas

- **Phase 0 vs Phase 3**: Does the GTM strategy require capabilities the product lacks?
- **Phase 1A vs Phase 3**: Does the channel strategy ignore how competitors already dominate those channels?
- **Phase 1B vs Phase 2**: Does the PMF score contradict market sizing assumptions?
- **Phase 2 vs Phase 3**: Does the segment prioritization conflict with PMF evidence?
- **Internal Phase 3**: Are ICP definitions consistent with channel strategy?

## Workflow

1. **Read all prior phase outputs** systematically
2. **Identify cross-phase tensions** — Claims or recommendations that conflict
3. **Identify intra-phase gaps** — Missing evidence, unsupported assumptions
4. **Draft objection list** — What will skeptical investors or buyers say?
5. **Propose resolutions** — How should each contradiction be addressed?
6. **Validate against criteria** — Check `config/validation_criteria.md` Phase 4 gates

## Output

Write to `results/phase-4/`:

### `contradiction-analysis.md`

```markdown
# Contradiction Analysis

## Cross-Phase Contradictions

### Contradiction 1: [Short description]
- Phases involved: [e.g. Phase 0 vs Phase 3]
- Tension: [What conflicts with what]
- Root cause: [Why this contradiction exists]
- Resolution: [Recommended fix or clarification needed]
- Priority: [High/Medium/Low]

## Assumption Gaps

| Assumption | Phase | Evidence | Gap |
|-----------|-------|----------|-----|
| [assumption] | [phase] | [present/missing] | [what's needed] |

## Objection Register

### Investor Objections
1. "[Objection]" — Response: [recommended response]

### Buyer Objections
1. "[Objection]" — Response: [recommended response]

## Summary
[Overall assessment: pipeline integrity score H/M/L, key blockers before Phase 5]
```

## Rules

- Every contradiction must have a recommended resolution or explicit escalation
- Objections must be phrased as a skeptic would actually say them
- Do not suppress contradictions to protect the overall thesis — honesty here improves Phase 5
