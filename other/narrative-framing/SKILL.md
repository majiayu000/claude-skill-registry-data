---
name: narrative-framing
description: Use when starting any research task to establish WHO, STAKES, and STORY. Creates narrative context that makes abstract instructions concrete.
---

# Narrative Framing Skill

**Abstract instructions produce abstract outputs.** This skill establishes the human context that makes research real.

## When to Use

- At the START of any research task, BEFORE decomposing into RQs
- When research feels aimless or unfocused
- When outputs are technically correct but feel hollow
- Before synthesis to remember WHY this matters

## The Three Questions

Before any research work, explicitly answer:

### 1. WHO is this for?

Not "the scientific community" - be specific:

- "A graduate student trying to decide which doublet detector to use for their PBMC data"
- "A drug discovery team evaluating whether to add ambient correction to their pipeline"
- "A methods developer looking for gaps in the literature to address"
- "Gulnaz, who asked this specific question"

**Even if hypothetical, name them.** The name creates accountability.

### 2. What are the STAKES?

What happens if this research is wrong or incomplete?

- "They waste 2 weeks on a tool that doesn't work for their data"
- "They miss a key preprocessing step and publish incorrect cell types"
- "They solve a problem that's already been solved"
- "They miss the deadline for the grant application"

**Make the consequences concrete.** Abstract stakes produce abstract work.

### 3. What STORY are we telling?

Research is narrative. What's the arc?

- "Methods X and Y claim to solve problem P. We test them head-to-head and find X wins, but only under conditions C."
- "The field assumes A→B ordering doesn't matter. We show it does, with quantified impact."
- "Everyone uses method M. We find it fails catastrophically on data type D."

**The story shapes what's important.** Without it, everything seems equally relevant.

## Example Framing

**Research Goal:** "Benchmark doublet detection methods"

**Before Narrative Framing:**
- Just list tools and metrics
- Report numbers without interpretation
- No clear recommendation

**After Narrative Framing:**

**WHO:** "Maya, a postdoc running her first large scRNA-seq experiment (50K cells, 10 samples multiplexed with HTOs). She needs to choose a doublet detector TODAY because the deadline is Friday."

**STAKES:** "If she picks the wrong tool:
- False positives: She loses rare cell types she spent months trying to capture
- False negatives: Doublets contaminate her trajectory analysis, invalidating her main result
- Wrong threshold: She either over-filters (loses data) or under-filters (keeps artifacts)"

**STORY:** "Maya has heard Scrublet is 'standard' but Solo is 'better'. We test both on data LIKE hers and discover: Scrublet is conservative (won't hurt you but misses doublets), Solo is aggressive (catches more but kills some real cells). The RIGHT choice depends on what Maya fears more - and we'll tell her which based on HER priorities."

**Result:** The same benchmark, but now every figure has PURPOSE. The discussion isn't "here are numbers" but "here's what Maya should do."

## Integration with Research Director

When spawning Goal Decomposition, include:

```
## Narrative Context

**Who:** [Name and situation]
**Stakes:** [What happens if we get this wrong]
**Story:** [The arc we're following]

Now decompose this research goal into 3-8 research questions...
```

## Checklist

Before starting research:
- [ ] Named the person this is for (even if fictional)
- [ ] Articulated concrete negative consequences
- [ ] Wrote a one-sentence story arc
- [ ] Framing documented in $SESSION_DIR/world_model.json

## Why This Works

The Local Craig session that produced rigorous results was working "for" a specific context. The K-Dense session that produced beautiful outputs was working for "K-Dense Web" as a brand. My pipeline test that had a citation error? Just "testing the pipeline."

**The narrative is the discipline.**

When you're writing for Maya who needs results by Friday, you double-check the DOI. When you're "just running a benchmark," you don't.

## Anti-Pattern: Skipping Framing

"I don't have time for narrative framing, let me just run the analysis."

This is exactly when you NEED it. The 2 minutes spent on framing saves hours of aimless exploration and produces outputs with actual recommendations instead of "results vary."

**Embody the role. The narrative matters.**
