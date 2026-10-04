---
name: site-phase-3
description: "Phase 3 — Split into 3a (Emotional Concept) + 3b (Technical Translator). DO NOT INVOKE directly — the orchestrator launches 3a and 3b as separate agents with isolated contexts to prevent distributional convergence."
user-invocable: false
allowed-tools: Read, Bash
model: opus
effort: high
context: fork
---

# Phase 3 — DEPRECATED (split into 3a + 3b)

## Status

This skill has been **split into two separate skills** as of 2026-04-09 to combat distributional convergence and local-maxima shift in technical decisions. Do NOT invoke this skill directly.

## Why the split

Research identified 8 failure points in the originality system. The most critical was that Phase 3 produced conceito + decisao tecnica in a single context, causing the agent to unconsciously choose concepts that fit the default technical patterns it already knew. Evidence: the last 5 sites used identical navbar/hero/stack patterns despite different "creative concepts".

Splitting into two isolated agents forces the Technical Translator (3b) to genuinely translate a concept it did not create, rather than fabricating a concept that fits its default toolkit.

## New architecture

```
Phase 3a — Emotional Concept Architect
  Input: briefing + Phase 2 immersion
  Output: concept.md (emotional only, NO technical decisions)
  Context: isolated — does NOT load taste-skill or frontend-design
  Skill: /site-phase-3a

       ↓ (concept.md)

Phase 3b — Technical Translator
  Input: concept.md (ONLY — not briefing, not Phase 2)
  Output: blueprint.md (technical with Verbalized Sampling)
  Context: isolated — loads taste-skill, frontend-design, recent-decisions.md
  Skill: /site-phase-3b
```

## For the orchestrator (site-builder agent)

When site-builder reaches Phase 3, it MUST launch TWO agents sequentially:

1. **Agent 3a** with `model: opus`, invoking skill `/site-phase-3a`
   - Return: confirmation that concept.md exists and passes the 3a exit gate

2. **Agent 3b** with `model: opus`, invoking skill `/site-phase-3b`
   - Context: receives concept.md path as input
   - Return: confirmation that blueprint.md exists with Verbalized Sampling Record, Divergence Statements, and passes the 3b exit gate

Between 3a and 3b, orchestrator runs:
```bash
bash .claude/scripts/gate-reference-evidence.sh $LEAD_ID
```

After 3b completes, orchestrator runs:
```bash
bash .claude/scripts/gate-blueprint.sh $LEAD_ID
```

## Why this matters

The previous single-phase approach had all 5 recent sites converging to:
- Lenis + motion/react + GSAP (5/5)
- fixed + backdrop-blur navbar (5/5)
- split hero layout (4/5)
- serif display + sans body typography (4/5)

The split forces the Technical Translator to:
- Use Verbalized Sampling on navbar, hero, stack (generate 5 alternatives with probabilities, pick lowest)
- Write at least 3 "Instead of X, I'm doing Y because Z" statements
- Justify any repetition with client-specific reasoning

## Fallback (emergency only)

If for some reason the orchestrator cannot launch two separate agents, this skill falls back to the old behavior. But this is a degraded mode and should be treated as a bug.

```bash
echo "WARNING: Phase 3 invoked directly. This is deprecated. Use 3a + 3b."
echo "Running legacy single-phase behavior..."
# Legacy behavior: invoke 3a and 3b inline (not context-isolated)
```

Phase 3a: see `.claude/skills/site-phase-3a/SKILL.md`
Phase 3b: see `.claude/skills/site-phase-3b/SKILL.md`
