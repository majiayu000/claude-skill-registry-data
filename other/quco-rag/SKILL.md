---
name: quco-rag
title: "QuCo-RAG: Quantifying Uncertainty for Dynamic RAG"
version: 0.0.2
engine: skillxiv-v0.0.2-claude-opus-4.6
license: MIT
url: https://arxiv.org/abs/2512.19134
keywords: [rag, retrieval, uncertainty, hallucination, calibration]
description: "Replace unreliable model-internal confidence signals with objective corpus statistics to decide when RAG retrieval is necessary. Pre-evaluates entity rarity in training data and verifies entity co-occurrence at runtime, triggering retrieval only when hallucination risk is high—improving reliability without per-model tuning."
---

## Overview

QuCo-RAG addresses a critical flaw in dynamic RAG systems: relying on LLM confidence scores for retrieval decisions when models are notoriously poorly calibrated. This framework shifts to objective, corpus-based evidence that's reliably indicative of hallucination risk.

## Core Technique

The key innovation is grounding retrieval decisions in pre-training corpus statistics rather than model outputs.

**Pre-Generation Entity Assessment:**
Before generation, identify knowledge gaps by checking entity rarity in training data.

```python
# Entity rarity assessment using corpus statistics
import infini_gram  # Trillion-token corpus query tool

class CorpusBasedUncertainty:
    def __init__(self, corpus_client):
        self.corpus = corpus_client  # Infini-gram for fast queries

    def assess_pre_generation(self, input_question):
        """
        Identify entities in question appearing rarely in training corpus.
        High rarity → high hallucination risk → retrieve.
        """
        entities = extract_entities(input_question)
        high_risk_entities = []

        for entity in entities:
            # Query corpus for entity frequency
            frequency = self.corpus.query_frequency(entity)

            # Low frequency = long-tail knowledge gap
            if frequency < RARITY_THRESHOLD:
                high_risk_entities.append(entity)
                return True  # Trigger retrieval

        return False  # Confident in internal knowledge
```

**Runtime Verification via Co-occurrence:**
After generation, verify factual claims by checking entity co-occurrence in corpus.

```python
def verify_runtime_factuality(generated_text, corpus_client):
    """
    Extract factual claims and verify via corpus co-occurrence.
    Zero co-occurrence = hallucination risk.
    """
    claims = extract_factual_claims(generated_text)
    hallucination_risk = False

    for claim in claims:
        subject, predicate, obj = parse_claim(claim)

        # Check if entities co-occur in corpus
        cooccurrence = corpus_client.query_cooccurrence(
            entities=[subject, obj],
            context=predicate
        )

        if cooccurrence == 0:
            # No corpus evidence for relationship
            hallucination_risk = True
            break

    return hallucination_risk
```

**Binary Retrieval Decision:**
Unlike continuous confidence scores with unclear thresholds, decisions are binary and principled.

```python
def dynamic_rag_decision(question, generated_text, corpus_client):
    """
    Make discrete retrieval decision based on corpus evidence,
    not subjective confidence scores.
    """
    pre_gen_risk = assess_rarity(question, corpus_client)
    runtime_risk = verify_factuality(generated_text, corpus_client)

    should_retrieve = pre_gen_risk or runtime_risk
    return should_retrieve
```

## When to Use This Technique

Use QuCo-RAG when:
- Reducing hallucinations in RAG systems
- Model calibration is unknown or unreliable
- Corpus statistics are available (via Infini-gram or similar)
- Retrieval cost justifies verification overhead

## When NOT to Use This Technique

Avoid this approach if:
- Training corpus is unavailable or unreliable
- Entity rarity is poor indicator in your domain
- Retrieval latency cannot tolerate verification queries
- Model calibration is already well-tuned

## Implementation Notes

The framework requires:
- Access to trillion-token corpus with fast query capability (Infini-gram)
- Entity and claim extraction pipelines
- Entity frequency and co-occurrence query infrastructure
- Integration with existing RAG systems at generation time

## Key Performance

- Bypasses unreliable model-internal signals
- Transfers effectively across different language models
- More principled than continuous confidence thresholding

## References

- Pre-training corpus statistics for uncertainty quantification
- Entity rarity as indicator of knowledge gaps
- Entity co-occurrence verification for factual grounding
- Binary retrieval decisions based on objective evidence
