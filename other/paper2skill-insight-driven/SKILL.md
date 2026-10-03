---
name: paper2skill-insight-driven
description: "Convert insight-driven papers into minimal reproducible recipes built around a single non-obvious observation. Extracts the key insight, why the problem seemed hard, and the minimal implementation. Use this skill when extracting skills from Category 6 (Insight-Driven) papers — 'Learning to See in the Dark'-style papers where one clever observation unlocks a seemingly hard problem."
---

## When to Use This Skill

Use this extraction for papers that:
- Introduce **one non-obvious observation or insight** that dramatically changes how the problem is solved
- The insight **simplifies or reframes** a previously hard problem
- The core result can be reproduced with a **minimal recipe** (often <50 lines, sometimes just a different way of looking at the problem)
- The paper's positioning is "we discovered that [X]" not "we built a new method [Y]"
- Results show **dramatic improvements** suggesting the insight unlocks something fundamental

**Value signal:** These papers teach *conceptual breakthroughs*. Often the smallest papers with the biggest impact.

Examples: "Learning to See in the Dark" (image denoise by reversing the camera sensor pipeline), "Live Repetition Counting" (count using just motion history), "Prompt Injection Attacks" (security observation that changes how to think about LLM safety)

## When NOT to Use This Skill

Skip this category if:
- The paper introduces **a complex new method** with multiple moving parts (use **paper2skill-component-innovation** for single changes)
- It's **primarily an empirical study** of existing methods (use **paper2skill-systematic-empiricism** instead)
- The breakthrough is **a new architecture or component swap** better framed as component innovation
- The insight requires **significant domain knowledge** but isn't clearly articulated as an "aha moment"
- The paper doesn't clearly explain **why the problem was hard before** and **why the insight makes it easy**

---

## Extraction Template

### 1. The Core Insight (One Sentence)

This is the centerpiece. Extract the single non-obvious observation:

```
The insight: [One-sentence statement of the observation, e.g., "Raw sensor noise follows a predictable distribution — use it as a prior for image reconstruction"]

Alternative phrasings of the same insight:
- [Formulation view]: [How to think of it as a math problem]
- [Data view]: [How to think of it as a data property]
- [Algorithmic view]: [How to think of it as an algorithm]
```

### 2. Why Was This Hard Before?

Explain the previous conceptual barrier:

```
Conventional approach:
- [People tried X to solve the problem]
- [Why X seemed reasonable at the time]
- [What fundamental assumption limited X]

The hidden assumption:
- [What everyone was getting wrong]
- [Why it wasn't obvious]
- [Why the insight contradicts conventional wisdom]

Why nobody discovered this before:
- [Could be: too simple, required new data, required asking a different question]
```

### 3. How Does the Insight Reframe the Problem?

Show the conceptual shift:

```
Before the insight:
- Problem seemed to require: [complex approach, new architecture, lots of labeled data, ...]
- Bottleneck was: [what made it hard]
- Complexity was at: [where the problem was hard]

After the insight:
- Problem reduces to: [simplified formulation]
- Bottleneck moves to: [if any remaining]
- New framing enables: [why this is now tractable]

Shift type:
- [Observation-driven]: "We measured X and found Y" → changes the prior
- [Formulation-driven]: "Rewrite the problem as X instead of Y" → simplifies math
- [Perspective-shift]: "View this as X problem not Y problem" → unlocks solution
```

### 4. The Minimal Recipe

Distill the implementation to its core:

```python
# 2-3 sentence explanation of what this does and why it works given the insight
def insight_driven_approach(inputs):
    """
    Minimal implementation showing exactly how the insight translates to code.
    This should feel almost trivially simple once the insight clicks.
    """
    pass
```

For larger recipes, show the key steps:

```
Recipe steps:
1. [Step using the insight]
   Why: [Because of the insight]
   Code: [2-3 lines or reference to scripts/]

2. [Step that follows naturally]
   Result: [What you get at this point]

3. [Final step]
   Check: [How to verify it worked]
```

### 5. Empirical Validation

Extract the core results showing the insight works:

```
Metric: [What they measured]
Baseline (old approach): [Value and description]
With insight-driven approach: [Value and description]
Improvement: [X% or Y percentage points]

Key ablation:
- Remove [core element of insight]: [Degradation in performance]
  → Confirms the insight is doing the work

Surprising finding:
- [Something unexpected that validates the insight is fundamental]
```

### 6. Type of Insight (Classification)

Identify what kind of insight this is:

```
This is an [observation/formulation/perspective] insight because:
- [Characteristics of this type]

Related insights of the same type:
- [Other papers that make similar moves]
```

**Insight types:**
- **Observation-driven**: "We measured X and discovered property Y" (e.g., "camera noise is Poisson-distributed")
- **Formulation-driven**: "Reframe the math differently" (e.g., "use stochastic gradient descent as sampling from posterior")
- **Perspective-shift**: "View this as a different kind of problem" (e.g., "counting as optical flow, not classification")
- **Data property**: "The structure of the data itself holds the solution" (e.g., "image patches appear multiple times in a single image")
- **Inverse transformation**: "Reverse a process to undo its effects" (e.g., "inverse tone mapping for low-light image recovery")

### 7. Output Skill Structure

Generate a SKILL.md that conveys the insight:

```
---
name: [insight-identifier-short]
title: [Paper title — action-oriented "Unlock X using insight Y"]
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: [arXiv HTML link]
keywords: [problem-domain, insight-type, key-observation, outcome, breakthrough]
description: |
  A single insight reframes [hard problem] as [simple problem]: [the insight in one sentence].
  Trigger: When facing [problem type], apply this insight to enable [outcome] without [previous complexity].
---

## The Breakthrough Insight

**The observation**: [One sentence]

**Why this matters**: Conventional approaches required [complexity], but the insight reveals [simplification].

## Why Was This Hard?

[Explain the previous conceptual barrier and hidden assumptions]

## How the Insight Reframes the Problem

[Show the conceptual shift: what changed, why the problem is now tractable]

## Minimal Recipe

[Core implementation showing the insight in action]

[Optional code or pseudocode, <20 lines]

## Results

[Core empirical validation: metric improvement, ablation showing insight does the work]

## When to Use This Insight

- When [problem type] seems to require [old complex approach]
- To replace [previous method] with [insight-based method]
- When you need [property the insight enables]

## When This Insight Doesn't Apply

- If [property] is not true for your problem
- When [condition] changes the assumptions
- For [different domain or setup]

## Insight Type

This is a [observation/formulation/perspective]-driven insight.

[Other related insights or papers making similar moves]
```

---

## Execution Notes

**For extraction success:**
1. **Find the singular insight**: Read the abstract and introduction. What is the *one* thing the paper discovered?
2. **Verify it reframes the problem**: Does understanding this insight make the solution obvious?
3. **Extract the "aha moment"**: What assumption was wrong? What changed?
4. **Keep the implementation minimal**: If the code is complex, you may have misidentified the insight (it might be a full method instead)
5. **Validate through ablation**: Remove the core insight and performance drops → confirms it's doing the work
6. **Classify the insight type**: Observation? Formulation shift? Perspective change?

**Common pitfalls to avoid:**
- Confusing "new method" with "single insight" (if multiple components, it's not insight-driven)
- Extracting a complex derivation as the "recipe" (should be simple once the insight clicks)
- Missing the conceptual shift (just listing the technical details, not the breakthrough)
- Not explaining *why* the problem was hard before (diminishes the insight value)
- Treating a well-executed paper as insight-driven when it's actually systematic empiricism
