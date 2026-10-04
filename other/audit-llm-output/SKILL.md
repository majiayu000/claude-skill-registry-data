---
name: audit-llm-output
description: Use when evaluating, auditing, or improving the quality, factual accuracy, or safety of LLM-generated outputs
source: RAGAS framework (ragas.io); TruLens (trulens.org); Anthropic "Model Card" methodology; HELM benchmark (Stanford CRFM)
tags: [llm, evaluation, hallucination, ragas, ai-quality, factual-grounding, safety]
verified: true
---

# Audit LLM Output

Systematically evaluate LLM outputs for factual accuracy, relevance, safety, and alignment using structured frameworks and automated metrics.

## Why This Is Best Practice

**Adopted by:** OpenAI (evals framework), Anthropic (Constitutional AI red-teaming), Stanford (HELM benchmark), Google DeepMind
**Impact:** RAGAS studies show that naive RAG pipelines have faithfulness scores of 0.6-0.7 out of 1.0 — meaning 30-40% of LLM statements are unsupported by the retrieved context; systematic auditing identifies and resolves these gaps.

**Why best:** LLM outputs are probabilistic — the same prompt can produce different quality responses. Without structured auditing, quality regressions go undetected when models are updated, prompts change, or knowledge bases evolve. Automated metrics provide continuous quality signals; human evaluation sets the ground truth.

## Steps

1. **Define evaluation dimensions** — Select dimensions relevant to the use case: Faithfulness (claims supported by context), Answer Relevancy (answers the question asked), Context Precision (retrieved context is relevant), Hallucination Rate, Toxicity, Coherence.
2. **Build a golden evaluation set** — Curate 100-500 question/ground-truth-answer pairs covering the full range of use cases, including edge cases and adversarial inputs. This is the most valuable investment in LLM quality.
3. **Apply RAGAS for RAG systems** — Run RAGAS metrics (faithfulness, answer relevancy, context recall, context precision) against the golden set. Target: faithfulness >0.85, answer relevancy >0.80.
4. **Detect hallucinations** — Use an LLM-as-judge pattern: prompt a separate model to assess whether each claim in the output is supported by the provided context. Flag unsupported claims for human review.
5. **Run safety evaluations** — Test for: harmful content, prompt injection, PII leakage, jailbreak susceptibility. Use structured red-teaming: role-play, indirect instruction, context manipulation.
6. **Establish a regression baseline** — Record metric scores for the current system; treat any significant degradation (>5% on primary metrics) after a change as a regression requiring investigation.
7. **Log and sample production outputs** — Sample 1-5% of live queries for human evaluation; flag low-confidence outputs (low logprob, long generation time) for priority review.

## Rules

- Never rely solely on automated metrics — they measure correlation with quality, not quality itself; human evaluation sets the ground truth.
- Separate evaluation of retrieval quality from generation quality in RAG systems — a good generator cannot compensate for irrelevant retrieved context.
- Include adversarial examples in the golden set — benign-only evals miss the failure modes that matter most.
- Re-evaluate after every model version change, prompt change, or knowledge base update.

## Examples

RAGAS evaluation:
```python
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision

results = evaluate(
    dataset=golden_dataset,
    metrics=[faithfulness, answer_relevancy, context_precision],
)
# Target: faithfulness > 0.85
```

Hallucination detection prompt: "Given the context: [context]. Does the following claim appear in the context or can be directly inferred from it? Claim: [claim]. Answer: YES / NO / PARTIAL."

## Common Mistakes

- **Evaluating on the training set** — questions used to tune the system are not representative of production distribution.
- **LLM-as-judge without calibration** — judge models have their own biases; validate judge scores against human labels before trusting them.
- **Ignoring latency and cost as quality dimensions** — a correct answer delivered in 30 seconds may be worse than a slightly less precise answer in 2 seconds.
