---
license: Apache-2.0
name: helm-liang-2022
description: Holistic evaluation framework for language models measuring accuracy, calibration, robustness, and fairness
category: Research & Academic
tags:
  - benchmarks
  - llm-evaluation
  - holistic
  - metrics
  - language-models
---

# SKILL.md — Holistic AI Evaluation (HELM Framework)

license: Apache-2.0
```yaml
name: holistic-ai-evaluation-helm
version: 1.0.0
description: >
  Rigorous, multi-dimensional evaluation of AI/language model systems.
  Draws from Stanford CRFM's Holistic Evaluation of Language Models (HELM) —
  the first systematic attempt to treat LLM evaluation as a multi-dimensional
  measurement science rather than a single-number leaderboard sport.
activation_triggers:
  - "evaluate a model"
  - "benchmark comparison"
  - "which model is better"
  - "accuracy vs fairness"
  - "prompt sensitivity"
  - "evaluation methodology"
  - "model selection criteria"
  - "measuring AI performance"
  - "calibration"
  - "bias evaluation"
  - "how do we know if this works"
  - "production readiness assessment"
  - "agent routing / model routing decisions"
```

---

## When to Use This Skill

Load this skill when you encounter:

- **Model selection decisions** — choosing between models for a task, system, or deployment
- **Evaluation design** — designing tests, benchmarks, or acceptance criteria for AI components
- **Suspiciously clean results** — someone reports a single accuracy number as sufficient evidence
- **Prompt engineering disputes** — disagreements about whether a formatting choice "counts"
- **Production monitoring** — defining what to measure once a model is deployed
- **Fairness/bias questions** — any claim that a model treats groups equitably (or doesn't)
- **Confidence/calibration questions** — when a model's stated confidence will drive downstream decisions
- **Agent orchestration design** — routing tasks to models or skills without specifying adaptation procedure
- **Scaling law arguments** — claims that "bigger model = better" without qualification

**The core diagnostic question this skill answers**: *Are you measuring what actually matters, or measuring what's easy to measure?*

---

## Core Mental Models

### 1. Taxonomy Before Benchmark
You cannot evaluate comprehensively without first stating *what you're trying to evaluate*. The taxonomy makes incompleteness **visible** — you can point to what's missing. Jumping straight to measurement without taxonomy is how you end up with benchmarks that answer questions nobody asked and miss questions everyone cares about.

> Before choosing a metric, ask: "What is the full space of things we care about? Which slice of that space does this metric cover?"

### 2. Single-Metric Optimization Is a Category Error
For complex AI systems, accuracy, robustness, fairness, calibration, bias, toxicity, and efficiency are **simultaneously relevant** and **partially orthogonal**. HELM finds these relationships are scenario-dependent:
- Accuracy and robustness: often correlated
- Accuracy and calibration: sometimes *anti-correlated* (HellaSwag)
- Accuracy and bias: paradoxically opposed (BBQ — the most accurate models show worst social bias in ambiguous contexts)

No model dominates on all metrics. Optimizing for one trades off others, usually invisibly.

### 3. Adaptation Procedure Is a First-Class Variable
The same model on the same task can swing **30–80% accuracy** depending solely on prompt formatting. Multiple-choice framing, number of in-context examples, stop sequences, and phrasing are not implementation details — they define what you're actually measuring. A model comparison without controlled adaptation is not a model comparison; it's a prompt comparison with a confound.

### 4. Scale Predicts Within Families, Not Across Them
Scaling laws hold *within* a model family (more parameters → better) but break across families. A 52B instruction-tuned model outperforms a 530B base model. Perplexity on a training corpus does not predict downstream task accuracy. The key confound is **training procedure** (instruction tuning, RLHF, fine-tuning objective) — not parameter count alone.

### 5. Benchmarks Are Social Artifacts, Not Neutral Instruments
Benchmarks encode values. They create incentives. They shape what gets built by defining what "better" means. A benchmark that measures only accuracy on English text encodes a value judgment that non-English users and calibration don't matter. This is not a technical observation — it's sociological. The choice of what to measure is always a normative act.

---

## Decision Frameworks

### Designing an Evaluation

| If you're doing this... | Then consider... |
|---|---|
| Selecting metrics for a new benchmark | Start with an explicit taxonomy of scenarios × metrics before selecting any subset |
| Comparing two models | Verify adaptation procedure is held constant; a prompt difference invalidates the comparison |
| Reporting a single accuracy number | Ask: what are the calibration, robustness, fairness, and toxicity numbers? Why are those not reported? |
| Claiming "Model A is better than Model B" | Better *on what scenario, for what domain, under what metric*? The unqualified claim is almost always underdetermined |
| Evaluating for production deployment | Accuracy is necessary but insufficient — add calibration (are confidence scores trustworthy?), robustness (dialect/perturbation), and at minimum one fairness metric |

### Model Selection for Agent Systems

| If your system does this... | Then check for this... |
|---|---|
| Routes tasks to models by capability | Whether capability was measured under the same adaptation procedure you'll use in production |
| Uses model confidence to gate decisions | Whether that model's confidence is calibrated on your scenario type |
| Serves diverse user populations | Whether fairness/performance was measured across demographic or dialect groups |
| Spans multiple domains (medical + legal + news) | Whether the model was benchmarked domain-specifically — "summarization" performance varies by domain |
| Scales to larger models for "better" results | Whether the larger model is from the same family — cross-family scaling is not guaranteed |

### Diagnosing Evaluation Failures

| Symptom | Likely failure mode | Reference |
|---|---|---|
| Model performs well in testing, fails in production | Adaptation sensitivity — prompts differ between test and prod | `helm-adaptation-sensitivity-problem.md` |
| Fair accuracy metrics, but user complaints of bias | Accuracy-bias paradox — accuracy and bias can be anti-correlated | `helm-fairness-bias-evaluation-methodology.md` |
| High confidence predictions that are often wrong | Calibration failure — accuracy ≠ reliability of uncertainty | `helm-calibration-uncertainty-quantification.md` |
| Benchmark scores don't predict real-world ranking | Benchmark-to-deployment gap, possible contamination | `helm-failure-modes-evaluation-collapse.md` |
| "Bigger model is always better" assumption | Cross-family scaling confusion | `helm-scale-vs-training-procedure-tradeoff.md` |
| Different teams getting incomparable results | Standardization failure — no shared adaptation protocol | `helm-standardization-comparability.md` |

---

## Reference Documents

Load these on demand when deeper treatment is needed:

| File | When to Load |
|---|---|
| `references/helm-taxonomy-first-design.md` | Designing a new evaluation, benchmark, or test suite from scratch; someone jumps to metrics without taxonomy |
| `references/helm-multi-metric-evaluation-framework.md` | Any situation involving metric selection, single-number reporting, or the question of "what should we measure?" |
| `references/helm-adaptation-sensitivity-problem.md` | Prompt engineering decisions that affect evaluation; comparing models across teams; production-to-test gaps |
| `references/helm-scale-vs-training-procedure-tradeoff.md` | Model selection involving scaling arguments; comparing models across families; instruction-tuned vs. base model choices |
| `references/helm-failure-modes-evaluation-collapse.md` | Evaluations that seem too clean; contamination concerns; understanding why historical benchmarks became unreliable |
| `references/helm-standardization-comparability.md` | Multi-team environments; reproducing published results; designing shared evaluation protocols |
| `references/helm-calibration-uncertainty-quantification.md` | Any downstream use of model confidence scores; risk-sensitive applications; human-in-the-loop systems |
| `references/helm-fairness-bias-evaluation-methodology.md` | Equity/fairness requirements; serving diverse populations; understanding the fairness vs. bias distinction |
| `references/helm-benchmark-as-social-artifact.md` | Evaluating the evaluations themselves; understanding incentive effects; making normative choices about what to measure |

---

## Anti-Patterns

These are the failure modes HELM specifically identifies and warns against:

**1. The Accuracy Sufficiency Fallacy**
Treating accuracy as a complete description of model quality. Accuracy can be high while calibration, robustness, fairness, and toxicity are all failing simultaneously. "97% accuracy" without the other dimensions is incomplete information, not a clean result.

**2. Uncontrolled Adaptation Comparison**
Comparing Model A (with 5-shot chain-of-thought prompting) to Model B (with 0-shot direct prompting) and attributing differences to the model. The prompting convention is not a detail — it's half the measurement.

**3. Cross-Family Scaling Extrapolation**
Assuming the scaling laws observed within GPT-3 variants generalize to comparing GPT-3 variants against instruction-tuned models from a different family. They don't.

**4. Task-Without-Domain Decomposition**
Treating "summarization" as a single, uniform task. HELM's findings show domain (medical vs. news vs. legal) affects performance as much as task type. Routing all summarization to one model without domain-awareness ignores this.

**5. Benchmark Laundering**
Selecting benchmarks post-hoc to make a preferred model look better. The taxonomy-first approach exists specifically to prevent this — you must commit to what you're measuring before you see results.

**6. Conflating Fairness and Bias**
Treating "the model doesn't show bias" and "the model treats groups fairly" as equivalent claims. HELM distinguishes these carefully: a model can have low measured bias on explicit stereotype tests while still producing disparate performance outcomes across demographic groups.

**7. Black-Box Confidence**
Using model-generated confidence scores downstream without verifying calibration on your specific scenario type. Calibration is not a global model property — it varies by task and domain.

**8. Coverage Blindness**
Evaluating on the scenarios you have data for and assuming coverage of what matters. HELM's explicit taxonomy exists to reveal the gap between "scenarios we evaluated" and "scenarios that exist." The gap is almost always large.

---

## Shibboleths

*How to tell if someone has actually internalized HELM vs. just read a summary:*

**They've internalized it if they...**

- Immediately ask "what's the adaptation procedure?" when shown a model comparison, before looking at the numbers
- Distinguish between "Model A has better accuracy than Model B" and "Model A dominates Model B" — and know that the latter requires checking all metric dimensions
- Treat prompt formatting choices as *confounds to be controlled for*, not implementation details
- Know the BBQ paradox by heart: the most accurate models show *worse* social bias in ambiguous contexts — and can explain why this is counterintuitive
- Can name at least three metrics that accuracy doesn't tell you about (calibration, toxicity, robustness, fairness, efficiency...)
- When asked "which model should we use?", respond with "for what task, in what domain, for which users, measured how?" before engaging with the substance
- Describe a benchmark as encoding values and creating incentives — not as a neutral measuring instrument
- When someone says "we tested it and it works," ask "works on what distribution of inputs, for which subpopulations, and how did you control for prompt sensitivity?"

**They've only read the summary if they...**

- Cite "seven metric categories" without being able to name them or explain their relationships
- Treat the taxonomy as an organizational convenience rather than an epistemological commitment
- Think "holistic evaluation" means "many benchmarks" rather than "explicit prior taxonomy + acknowledged gaps"
- Can describe HELM's findings but apply them only to model evaluation, not to their own evaluation choices
- Believe calibration matters only for probabilistic outputs, not for all model deployments
- Treat the adaptation sensitivity finding as a prompting tip ("use few-shot examples") rather than a measurement validity challenge

---

*Load reference documents on demand. Start with `helm-taxonomy-first-design.md` if the core question is evaluation design. Start with `helm-multi-metric-evaluation-framework.md` if the core question is metric selection. Start with `helm-failure-modes-evaluation-collapse.md` if something has already gone wrong.*