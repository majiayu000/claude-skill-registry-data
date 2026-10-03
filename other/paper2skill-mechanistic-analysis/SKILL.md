---
name: paper2skill-mechanistic-analysis
description: "Convert mechanistic analysis papers into transferable analytical methodology skills. Extracts the research question, analytical instrument, controlled confounds, and practitioner implications. Use this skill when extracting skills from Category 9 (Mechanistic Analysis) papers — Network Dissection-style interpretability work or any paper whose goal is exploratory understanding of why something works."
---

# Paper2Skill: Mechanistic Analysis Edition

This skill specializes in converting mechanistic analysis papers — those that investigate and explain why systems work — into structured agent skills that teach analytical methodologies and interpretability techniques practitioners can apply.

Mechanistic analysis papers answer questions like: "Why does this work?", "What is the model actually doing?", "Which components matter?", "What is the model learning?"

The extractable knowledge is not an algorithm you implement, but an **analytical approach** — a methodology for answering questions about model internals, combined with practitioner implications from the findings.

## What Counts as Mechanistic Analysis

A **mechanistic analysis paper:**

1. **Asks an exploratory question:** "What is happening inside this model?" or "Why does this technique work?" (Contrast: adversarial robustness papers ask "How to break it?" — that's Category 3.)

2. **Uses a systematic analytical instrument:** A measurement technique, diagnostic tool, or experiment design that lets you peer inside the black box.

3. **Controls for confounds:** Isolates what you're measuring. E.g., "To measure if neurons detect objects, we need to control for that objects also have specific colors."

4. **Reports findings that practitioners can act on:** "When you see X in the model, it means Y is happening."

### Mechanistic Analysis vs. Related Categories

| Category | Asks | Measures | Output Skill Teaches |
|----------|------|----------|---------------------|
| **8 — Field Foundation** | "Is this a new problem worth studying?" | Nothing; defines problem space | The paradigm and vocabulary |
| **3 — Mechanistic Analysis (this one)** | "Why does this work / What's inside?" | Model internals, components, representations | The analytical methodology |
| **2 — Adversarial Analysis** | "How can we break this?" | Failure modes under attack | Attack strategies and defenses |
| **1 — Technique/Algorithm** | "How do we do X better?" | Performance on benchmarks | The algorithm/implementation |

The key distinction: **Mechanistic analysis is exploratory** ("I want to understand"), not adversarial ("I want to break it") or pragmatic ("I want to improve performance").

## Examples of Mechanistic Analysis Papers

- **"Network Dissection: Quantifying Interpretability of Deep Visual Representations"** — Asks: what do individual units in CNNs detect? Methodology: correlation between unit activation and semantic concepts.

- **"Attention is Not Explanation"** — Asks: do attention weights explain what the model is doing? Methodology: perturb attention weights and measure if model behavior changes.

- **"Lottery Ticket Hypothesis"** — Asks: are neural networks overparameterized? Methodology: iteratively prune weights and retrain to find minimal subnetworks.

- **"Theoretically Principled Trade-off between Robustness and Accuracy"** — Asks: why do adversarially robust models lose standard accuracy? Methodology: empirical investigation of loss landscape geometry and data geometry.

- **"Do Differentiable Simulators Give Better Policy Gradients?"** — Asks: do differentiable simulators help RL? Methodology: compare gradient quality, sample efficiency, and final policies vs standard simulators.

## Phase 1: Identifying Mechanistic Analysis Papers

### Assessment Rubric

Does the paper... | Points | Interpretation
---|---|---
Ask "why" or "how" a system works (not "how to improve")? | 1 | Exploratory, not optimization-focused
Use a systematic analytical instrument (measurement, diagnostic, experiment design)? | 1 | Has a replicable methodology
Control for confounds? | 1 | Isolates what's being measured
Report findings practitioners can act on? | 1 | Not just "interesting phenomenon," but actionable insight
Teach a methodology others could apply to new questions? | 1 | The analysis approach generalizes

**Threshold:** Need 4+ points.

## Phase 2: Paper Reading Strategy

### Pass 1: Question & Instrument (3 min)

- What specific question is the paper answering?
- How are they measuring/observing the phenomenon?
- What would a "baseline" (negative control) look like?

Read: intro, abstract, method overview

### Pass 2: Controls & Confounds (5 min)

- What could confound the measurement? (List 3-5 potential confounds)
- How does the paper control for them?
- Are there any unaddressed confounds?

Read: method section in detail

### Pass 3: Core Findings (5 min)

- What are the main empirical results?
- Are they surprising? Why?
- What follows from these findings (implications)?

Read: results, figures, tables

### Pass 4: Practitioner Implications (3 min)

- If I accepted these findings, what would I do differently?
- What diagnostics does this paper enable?
- How would I apply this methodology to a new question?

Read: discussion, implications, conclusion

### Pass 5: Generality (2 min)

- Does the methodology apply only to the specific model/task studied, or could it generalize?
- What would you need to change to apply this to a different system?

Read: limitations, future work

## Phase 3: Extraction Template

```
PAPER: [title]
ARXIV: [verified arXiv ID]
URL: [full verified arXiv URL]

RESEARCH QUESTION:
  Specific, answerable question the paper addresses
  Why is this question interesting/important?

ANALYTICAL INSTRUMENT/METHODOLOGY:
  What measurement technique or experiment design is used?
  How does it work (brief)?
  Why this approach over alternatives?

POTENTIAL CONFOUNDS & CONTROLS:
  What could incorrectly explain the findings?
  How does the paper control for each? (Ablations? Negative controls?)
  Any unaddressed confounds?

CORE FINDINGS:
  Main empirical result (specific, quantitative if applicable)
  Secondary findings (ablations, edge cases)
  Surprising results and why they're unexpected

PRACTITIONER IMPLICATIONS:
  If these findings are true, what should practitioners do differently?
  What diagnostics or tools does this enable?
  When are these findings relevant?
  When would you NOT apply this finding?

METHODOLOGY GENERALITY:
  Does this analytical approach apply beyond the specific domain studied?
  What would you need to change to apply it to a new question/system?
  What similar questions could this methodology answer?

RELATIONSHIP TO PRIORS:
  What did people believe before this paper?
  How does this paper confirm, refute, or nuance that belief?

CODE AVAILABLE: [yes/no, URL]
KEYWORDS: [5-10 analysis/mechanistic keywords]
```

## Phase 4: Writing the Mechanistic Analysis Skill

### Skill Structure

**Title:**
```
# [Phenomenon/Question]: [Outcome — what understanding this enables]
```

Example: "Attention Weights: Are They Explanations or Artifacts?"

**Section 1: The Research Question (2-3 paragraphs)**
- Frame the problem in practical terms
- Why do practitioners care about the answer?
- What do people commonly believe?

Example for "Attention is Not Explanation":
"When a Transformer model attends to certain tokens, we assume those tokens are 'important' for the prediction. Attention weights are widely used to explain model decisions: 'The model paid attention to this word, so that's why it made this prediction.' But is this assumption valid? Or are attention weights a side-effect of training without necessarily reflecting what the model uses for decisions? This question matters because if attention isn't explanation, our interpretability tools are broken."

**Section 2: The Analytical Approach (2-3 paragraphs)**
- Explain the measurement technique or experimental design
- Why is this approach sound?
- What is it measuring?

Example for "Attention is Not Explanation":
"To test if attention weights are explanations, the authors use a perturbation approach: (1) Run the model normally and record predictions and attention weights. (2) Modify attention weights (set them to uniform, reverse them, scramble them). (3) Re-run the forward pass with modified attention but the same input. (4) Compare model predictions before and after. If attention weights are explanations, perturbing them should significantly hurt predictions. If attention is just a side-effect, predictions might not change much."

**Section 3: Controls & Confounds (2 paragraphs)**
- What could confound the measurement?
- How does the paper control for them?

Example:
"A key confound: just because the model can produce predictions without relying on attention weights doesn't prove attention isn't causal — it might just mean the model has redundant pathways. To control for this, the authors compare models with varying attention architectures. If attention isn't explanation in one architecture, but is in another, we've isolated what's happening."

**Section 4: Core Findings (2-3 paragraphs)**
- State the main result clearly
- Include specific numbers/data
- Report any surprising findings

Example:
"Finding 1 (Main): Perturbing attention weights surprisingly little impact on predictions (accuracy drops from 95.2% to 94.8% in BERT on MNLI). By contrast, perturbing random other weights causes much larger accuracy drops. This suggests attention weights are not the bottleneck for prediction.

Finding 2 (Surprising): Even when attention is completely scrambled, many tasks see minimal performance degradation. The model seemingly 'gets' the right answer for different reasons than attention suggests.

Finding 3 (Nuance): For some tasks (e.g., coreference resolution), attention is somewhat more predictive of important tokens than for others (sentiment classification). The finding isn't absolute."

**Section 5: Practitioner Implications (2-3 paragraphs)**
- What should practitioners do differently given these findings?
- When is this relevant?
- When is this NOT relevant?

Example:
"Implications:
- Don't trust attention weight visualizations as explanations. They might be misleading.
- When explaining a specific prediction to humans, attention weights are one piece of signal but not definitive.
- Developing better interpretability tools is important; attention alone won't suffice.
- If you're designing models for interpretability, be skeptical of attention-based designs that assume attention is inherently interpretable.

When this matters: Using pre-trained transformers where you need explanations for stakeholders. When this doesn't matter: Basic classification tasks where you just need good predictions; interpretability is secondary."

**Section 6: Methodology You Can Reuse (2 paragraphs)**
- How would you apply this analytical approach to a new question?
- What is the core insight of the methodology that generalizes?

Example:
"The core analytical pattern: Perturbation-based diagnostics. To test if X is important for Y, (1) measure Y with X present, (2) remove/modify X, (3) remeasure Y, (4) compare. The strength: directly tests causal importance rather than correlation. The limitation: assumes you can modify X without breaking the model (not always true).

To apply this to a new question like 'Are LayerNorm statistics important?' you would: (1) Record model predictions with normal LayerNorm. (2) Modify LayerNorm parameters (e.g., scale them). (3) Re-run inference. (4) Compare predictions. Same methodology, different target."

**Section 7: Limitations & Caveats (1-2 paragraphs)**
- What are the paper's acknowledged limitations?
- What can't this methodology tell us?
- What open questions remain?

Example:
"Limitations: The finding applies to current Transformer architectures. Future architectures might make attention more important. Also, this tests whether attention is sufficient for prediction; it doesn't tell us if attention is necessary (models might have learned to use attention even if not optimal). Finally, perturbation-based analysis is task-dependent — findings on MNLI might not generalize to other tasks."

**Section 8: Related Mechanistic Questions**
- What other questions in this area has this methodology illuminated?
- What natural follow-ups exist?

Example:
"Related questions this methodology illuminates:
- Are intermediate layer representations necessary? (Yes, perturbing them hurts performance)
- Is the feedforward layer more important than attention? (Yes, in some architectures)
- Do different attention heads have different roles? (Yes, some focus on syntax, others on semantics)
- Do all layers need attention? (No; in deep models, some layers don't attend widely)"

**Section 9: When to Apply This Diagnostic**

Create a decision table:

| Scenario | Should I Use This? | Why / Why Not? |
|----------|------------------|---------------|
| Explaining predictions to stakeholders | Yes, but limited | Attention provides some signal, but isn't complete explanation |
| Checking if a component matters | Yes, absolutely | Perturbation testing is the go-to methodology |
| Diagnosing why a model fails | Yes, as first step | Helps identify which components are bottlenecks |
| Comparing two architectures | Yes, with caveats | Results might be architecture-specific |
| Improving interpretability | Partially | Guides design but doesn't solve problem completely |

**Reference:**
```
Paper: https://arxiv.org/abs/XXXX.XXXXX
Code: [URL if available]
Related work: [Paper name, for other mechanistic analyses]
```

---

## Key Rules for Mechanistic Analysis Skills

1. **Methodology > findings.** The paper's specific result matters less than the analytical approach. Teach practitioners how to ask similar questions.

2. **Replicability focus.** Include enough detail that someone could replicate the analysis or apply it to a new question.

3. **Honest about limitations.** Mechanistic analysis often has blind spots. Acknowledge what the methodology can and can't tell you.

4. **Practitioner-focused implications.** Don't just report findings; explain what practitioners should do with them.

5. **Control narrative.** Show what confounds exist and how the paper isolates its claims. This is the core of good analysis.

6. **Generality discussion.** Would this methodology work on other models/tasks? This helps practitioners assess transferability.

## Phase 5: Quality Checks for Mechanistic Analysis Skills

- [ ] **Question clarity:** Is the research question stated as a specific, answerable question (not vague)?
- [ ] **Methodology explainability:** Could someone replicate the analytical approach from the skill description?
- [ ] **Control honesty:** Are potential confounds acknowledged and addressed?
- [ ] **Findings specificity:** Are results quantitative/specific (not hand-wavy)?
- [ ] **Practitioner relevance:** Would a practitioner know when and how to apply this finding?
- [ ] **Generality realistic:** Does the skill honestly assess where the methodology generalizes?
- [ ] **Not just summarizing:** Does it teach the analytical approach, not just list findings?

## Avoiding Common Mistakes

1. **Don't extract as technique papers.** Mechanistic analysis isn't an algorithm to implement — it's a methodology to apply to new questions.

2. **Don't oversimplify to one finding.** The methodology and controls matter more than the specific result.

3. **Don't claim more generality than warranted.** If findings are task-specific, say so explicitly.

4. **Don't miss the confounds.** The controls section is often the most important part; don't skim it.

5. **Don't treat correlation as causation.** Mechanistic papers often use perturbation to test causality; explain why this is more informative than correlation.

## Batch Processing Mechanistic Papers

When triaging mechanistic analysis papers:

1. **Assess methodological novelty:** Is this a new analytical technique or a straightforward application of existing methods?
2. **Check confound handling:** Good mechanistic papers carefully control for alternative explanations. Poor ones don't.
3. **Evaluate practitioner relevance:** Is this finding something a practitioner would want to know?
4. **Coverage balance:** Aim for mix of different analytical approaches (perturbation, feature attribution, probing, causal graphs, etc.).

## Reference

Mechanistic analysis skill extraction adapted from Anthropic's skills guide and interpretability research best practices. Unlike algorithm or infrastructure extraction, mechanistic papers teach diagnostic methodologies and frameworks for understanding system internals. The skill teaches the analytical approach and its implications for practice, not a technique to implement.
