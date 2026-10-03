---
name: paper2skill-systematic-empiricism
description: "Convert systematic empiricism papers into ranked practitioner checklists. Extracts implementation tricks, hyperparameter findings, and design choice ablations with conditions of applicability. Use this skill when extracting skills from Category 4 (Systematic Empiricism) papers — '37 PPO details'-style papers, hyperparameter studies, or ablation-heavy guides that systematize scattered knowledge."
---

## When to Use This Skill

Use this extraction for papers that:
- Systematically test 10+ implementation tricks, hyperparameters, or design choices
- Provide quantitative ablation results with before/after impact numbers
- Identify which decisions matter most vs. which don't ("trick A: +5%, trick B: +0.5%")
- Explain conditions when each trick helps or hurts (dataset size, model scale, task type)
- Are motivated by "we need clear guidance for practitioners" or "let's settle debates in the community"

**Value signal:** These papers unlock *immediate executable knowledge*. The output is already a recipe.

Examples: "The 37 Implementation Details of PPO", "Regularization Matters in Policy Optimization", "An Empirical Study of Training End-to-End Vision-and-Language Transformers"

## When NOT to Use This Skill

Skip this category if:
- Paper proposes a novel component or new method (use **paper2skill-component-innovation** instead)
- Paper focuses on a single insight or observation (use **paper2skill-insight-driven** instead)
- Ablations are shallow or lack quantitative impact measurements
- Paper doesn't explain conditions of applicability (just lists tricks without "when to use")
- No clear ranking of impact (can't distinguish between high/low value changes)

---

## Extraction Template

### 1. Pain Point & Motivation
Start here: What problem does this paper solve for practitioners?

```
Pain point: [E.g., "PPO implementations vary wildly; unclear which tricks are essential vs. nice-to-have"]
Community impact: [E.g., "Reproducibility issues, wasted compute on low-impact tricks"]
Paper's claim: [E.g., "Systematic ablation identifies the 10 high-impact tricks that matter for convergence"]
```

### 2. Ranked Findings: What Matters Most

Extract the quantitative impact ranking. Order by effect size (largest first).

```
High-impact tricks (>3% improvement):
- Trick A: +X% when [condition]
  - Complexity: [trivial/moderate/high]
  - Applicable to: [when does it help]

Medium-impact tricks (1-3% improvement):
- Trick B: +Y% when [condition]

Low-impact tricks (<1% improvement):
- Trick C: +Z% but conditional on [specific setup]
- Trick D: No clear benefit, may hurt in [specific cases]

Surprising findings:
- Conventional wisdom was wrong about: [what assumption failed]
```

### 3. Decision Checklist for Practitioners

Create a ranked checklist practitioners should follow first-to-last:

```
Checklist (prioritized by impact and cost):
☐ Step 1: [High-impact, low-cost trick] — Essential, do this first
  Condition: Only if [dataset/model/task property]

☐ Step 2: [High-impact, moderate-cost trick]
  Condition: Only if [additional property]

☐ Skip: [Low-impact trick] — Not worth it unless [very specific case]
```

### 4. Conditions of Applicability

For each trick, extract when it helps and when it doesn't:

```
Trick X works best when:
- Model scale: [small/medium/large]
- Dataset size: [tiny/standard/large]
- Task type: [specific domains or task properties]
- Optimization regime: [early/late training, learning rate magnitude]

Trick X fails or becomes negative when:
- [Specific condition that breaks it]
- [Data regime where it hurt performance]
```

### 5. Implementation Recipe (if applicable)

For tricks that need code, show the minimal implementation:

```python
# 1-2 sentence explanation of what this does
def apply_trick_x(model, hyperparams):
    # Minimal implementation showing exactly what changes
    return modified_config
```

Store larger implementations in `scripts/` folder.

### 6. Output Skill Structure

Generate a SKILL.md that converts the findings into a practitioner resource:

```
---
name: [category-derived-name]
title: [Paper title — converted to action-oriented title]
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: [arXiv HTML link]
keywords: [domain, trick-type, impact-level, conditions-tag, community-need]
description: |
  [Outcome-focused]: Practitioners can [achieve X] by [applying Y ranked tricks] under [conditions Z].
  Trigger: When [specific implementation challenge], reference this ranked checklist.
---

## What This Skill Does

[High-impact outcome]: Using the ranked tricks from [paper] can improve [metric] by [cumulative %] while reducing [cost/complexity].

[Checklist preview]: Start with [top 3 high-impact tricks], then optionally add [medium-impact tricks] if [conditions].

## Ranked Trick Checklist

[Full checklist with conditions for each]

## When to Use

- Optimizing [specific model/task] and want to prioritize implementation effort
- Reproducing baselines with confidence that you're using high-impact changes
- Deciding between competing design choices: reference the ablation results

## When NOT to Use

- If your model/task has radically different properties (e.g., paper tested on vision, you're doing language)
- When exploring novel architectures (tricks are typically tuned for specific model families)
```

---

## Execution Notes

**For extraction success:**
1. Find the main ablation table or figure showing impact rankings
2. Extract exact numbers: "+X%" or "improves by Y points on [metric]"
3. Always note the conditions: "works best when [property], fails when [opposite]"
4. Identify surprising findings (conventional wisdom vs. empirical results)
5. Prioritize by effect size + implementation cost (high impact + low cost = top of checklist)

**Common pitfalls to avoid:**
- Extracting tricks without their quantitative impact (not actionable)
- Missing conditional clauses ("trick works for ResNets but not Vision Transformers")
- Listing tricks without a clear ranking or decision heuristic
- Ignoring statistical significance or confidence intervals
