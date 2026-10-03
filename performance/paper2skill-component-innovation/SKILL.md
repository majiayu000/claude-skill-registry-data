---
name: paper2skill-component-innovation
description: "Convert component innovation papers into drop-in replacement guides. Extracts what was swapped, why, conditions for when it helps, and the performance delta. Use this skill when extracting skills from Category 5 (Component Innovation) papers — BatchNorm-style papers, ResNet skip connections, new loss functions, or any paper proposing one elegant modification with outsized impact."
---

## When to Use This Skill

Use this extraction for papers that:
- Replace or modify a **single component** (a normalization layer, an attention block, a loss function, a data augmentation, an optimizer modification)
- The modification is **expressible in <20 lines of code** (surgical, not architectural redesign)
- Include ablation showing **performance delta with specific numbers** ("+2.5% on ImageNet", "reduces training time by 30%")
- Clearly explain **when the modification helps and when it doesn't** (what properties of the model/task/data matter)
- Positioning is "swap this component" not "redesign the whole system"

**Value signal:** These papers enable *drop-in replacements* with known performance impact. Practitioners can immediately A/B test.

Examples: Batch Normalization, ResNet skip connections, Transformers Without Normalization, RMSprop optimizer, Focal Loss, Mixup data augmentation, Rotary Embeddings

## When NOT to Use This Skill

Skip this category if:
- The change is **not surgical** — modifies multiple interrelated components or requires architectural redesign (use Category 8 instead)
- The modification is **conceptually a new method**, not a component swap (use **paper2skill-component-innovation** only for tweaks to existing patterns)
- **No quantitative ablation** showing the performance impact (must have numbers)
- The paper doesn't explain **conditions of applicability** (just shows one benchmark)
- The component is **too large or complex** to express as a surgical change (>50 lines of code to swap)

---

## Extraction Template

### 1. Component Identification

Clearly name what is being replaced:

```
Component type: [normalization / attention mechanism / loss function / optimizer / data augmentation / activation / regularization]
Old component: [What existed before, or what this improves upon]
New component: [What is being proposed]
Positioned as: [A swap / A modification / A replacement]
```

### 2. Motivation & Problem Statement

Why was the old component insufficient?

```
Problem with the old approach:
- Technical limitation: [E.g., "Batch normalization has reduced expressiveness at test time"]
- Practical pain point: [E.g., "Difficult to train on sequences with variable length"]
- Theoretical gap: [E.g., "Inconsistency between training and inference"]
- Empirical observation: [E.g., "Performance saturates despite better architectures"]

The paper's insight:
[One-sentence explanation of why the new component is better]
```

### 3. The Modification Itself

Show the change as code (must be <20 lines for surgical changes):

```python
# Clear explanation: what specifically changes from old to new
def old_component(x):
    """Original implementation"""
    pass

def new_component(x):
    """Modified implementation — minimal surgical change"""
    pass
```

If code is >20 lines, move to `scripts/` folder and reference it.

### 4. Ablation Results: Performance Delta

Extract exact numbers from ablations:

```
Baseline (old component): [Metric] = X.XX

With new component:
- Test accuracy: +Y.YY percentage points (Z% relative improvement)
- Training time: [faster/slower] by W%
- Convergence speed: [number of steps/epochs to reach accuracy]
- Memory usage: [higher/lower] by V%

Ablation variants tested:
- Without [subcomponent of new approach]: -W.WW (shows each part matters)
- In combination with [related trick]: +Z.ZZ (shows interactions)
```

### 5. Conditions of Applicability

Critical: when does this swap help or hurt?

```
This component swap works best when:
- Model architecture: [transformer / CNN / RNN / specific family]
- Dataset scale: [small / medium / large / ImageNet-scale]
- Task domain: [vision / language / speech / multimodal]
- Training regime: [LR magnitude, batch size, optimization details]
- Data properties: [distribution assumptions, input characteristics]

This swap may hurt or provide no benefit when:
- [Opposite of above conditions]
- [Specific architectural conflicts, e.g., "incompatible with batch norm"]
- [Regime where old component was already optimal]

Surprising findings:
- [Unexpected interaction or limitation discovered in ablations]
```

### 6. Drop-In Replacement Checklist

Practical guidance for practitioners:

```
To swap this component:

1. Replace [old API] with [new API]
   Code pattern: [2-3 line snippet showing the swap]

2. If your code has [specific pattern], adjust [specific way]

3. Verify: [what to measure to confirm the swap worked]

4. Optional tuning: [if performance doesn't match, try]
   - [Hyperparameter A]: suggested range [X-Y]
   - [Hyperparameter B]: suggested range [X-Y]

5. Known issues:
   - [Issue 1]: workaround is [solution]
   - [Issue 2]: usually not a problem unless [condition]
```

### 7. Output Skill Structure

Generate a SKILL.md for the component swap:

```
---
name: [component-type-identifier]
title: [Paper title — action-oriented "Swap X with Y"]
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: [arXiv HTML link]
keywords: [component-type, old-name, new-name, impact-metric, condition-tag]
description: |
  Swap [old component] with [new component] to gain [X% improvement] on [metric]. Works best for [conditions].
  Trigger: When optimizing [model family] on [task type] and want to improve [metric], test this component swap.
---

## What This Skill Does

Replace [old component] with [new component] to improve [outcome metric] by [X%] under [conditions].

## The Swap

[Minimal code showing the surgical change: old vs new]

## Performance Impact

- Improvement: +Y.YY on [metric] (Z% relative)
- Cost: [memory/speed/complexity change, if any]
- Ablation: [subcomponents that matter most]

## When to Use

- Optimizing [model family] on [task type]
- [Other condition where this swap applies]
- When you can verify improvement on your specific benchmark

## When NOT to Use

- If your model has [incompatible property]
- On [different task/domain] where it wasn't tested
- If [specific condition] is true for your setup

## Implementation Checklist

[Swap checklist with verification steps]

## Related Work

This builds on [prior approaches] and relates to [similar swaps].
```

---

## Execution Notes

**For extraction success:**
1. **Identify the component precisely**: "Batch Norm" not "training stability improvements"
2. **Verify it's surgical**: If multiple components change, this is a redesign, not a swap
3. **Extract exact numbers**: "+5.2 percentage points on ImageNet val" not "significant improvement"
4. **Document conditions**: "Works for ResNet, tested on ImageNet, learning rate 0.1" — be specific
5. **Find the ablation**: What happens if you remove subcomponents of the new approach?
6. **Check for interactions**: Does the swap help more/less when combined with other tricks?

**Common pitfalls to avoid:**
- Confusing a component swap with a new method (if it requires redesigning the whole system, skip)
- Missing the conditions (same trick doesn't work in all settings)
- Extracting the improvement without explaining why (missing the "motivation" section)
- Treating a large architectural change as a component swap (>20 lines of code = redesign, not swap)
