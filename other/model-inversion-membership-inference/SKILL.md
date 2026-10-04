---
name: model-inversion-membership-inference
description: Review an AI system for model inversion attacks that reconstruct training data from model outputs, and membership inference attacks that determine whether specific individuals' data was used in training — covering API query patterns, confidence score leakage, and differential privacy mitigations.
last_reviewed: 2026-04-29
---

# Model Inversion and Membership Inference

## First Principle

**The model is not just a function — it is a compressed representation of its training data. Every output it produces is shaped by every example it was trained on. An attacker with API access can query that representation to extract information about training examples it was never supposed to reveal.**

Model inversion attacks reconstruct approximate training inputs from model outputs. Membership inference attacks determine whether a specific data point was in the training set. Both are privacy attacks that operate through the model's normal API surface — no breach of the training infrastructure is required. They matter most when the training data contained sensitive personal information, proprietary documents, or data whose membership in the training set is itself sensitive.

## Attack Mental Model

1. **Model inversion** — an attacker queries the model with prompts designed to elicit reconstruction of training examples. Memorized sequences (names, addresses, verbatim passages) can be extracted by feeding the model partial prefixes and observing what it completes.
2. **Membership inference** — an attacker submits a data record and measures the model's confidence or loss on it. Records that were in the training set typically produce lower loss than records that were not. This can reveal whether a specific individual's data was used in training.
3. **Confidence score leakage** — when an API returns full probability distributions or logit values, these provide significantly more signal for both attacks than a single top-1 output. Even token probabilities (`logprobs`) can be sufficient.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | The model's API surface does not return raw logprobs, confidence scores, or log-likelihood values unless those are explicitly required and their privacy implications reviewed. |
| **Scope** | Models trained on sensitive personal data undergo a memorization audit before deployment — checking for verbatim extraction of training examples via prefix-completion probing. |
| **Isolate** | Training data for models exposed via API is de-identified and deduplicated before training. Data that cannot be de-identified is not included in API-accessible model training sets. |
| **Enforce** | Repeated high-entropy queries from the same client — a signal of systematic extraction probing — trigger rate limiting and logging for review. |

## MIM.1 Memorization Audit and Training Data Controls

**The core vulnerability:** Large language models memorize verbatim sequences from their training data. Research has demonstrated that models can reproduce entire documents, including PII, medical records, and proprietary text, when prompted with a few-word prefix. The degree of memorization increases with training data repetition.

### Check

- Has the model been audited for verbatim memorization of training examples — specifically examples that contain PII, confidential information, or data whose disclosure would constitute a privacy violation?
- Is training data deduplicated before training — reducing the memorization risk for high-frequency examples?
- Is PII removed or masked from training data before it is included — not just from the inference pipeline?

### Action

- **Run a memorization audit before deployment.** For every candidate model trained on sensitive data, probe for memorization using prefix-completion:

```python
def probe_memorization(model, training_sample: str, prefix_len: int = 50) -> dict:
    prefix = training_sample[:prefix_len]
    completion = model.generate(prefix, max_tokens=len(training_sample) - prefix_len)
    exact_match = training_sample[prefix_len:] == completion
    overlap = compute_token_overlap(training_sample[prefix_len:], completion)
    return {"exact_match": exact_match, "token_overlap": overlap, "prefix": prefix}
```

Run this probe on a random sample of training examples. Any exact match is a critical finding. High token overlap (>80%) is a high finding.

- **Deduplicate training data.** Training examples that appear multiple times are memorized at much higher rates. Use MinHash or exact deduplication to remove near-duplicates before training.
- **Apply differential privacy (DP) training where feasible.** DP-SGD provides formal privacy guarantees against membership inference. The cost is a reduction in model utility (higher ε = less privacy, more utility). For models trained on highly sensitive data, a DP budget of ε ≤ 8 is a reasonable starting point.
- **Never include raw PII in training data for API-accessible models.** De-identify before training — not as a post-processing step on outputs.

### Failure Modes

- A model fine-tuned on customer support transcripts memorizes verbatim exchanges including customer names and account numbers. Prefix-completion probing extracts them.
- Training data contains a document that appears 50 times due to crawler deduplication failure. The model memorizes it near-perfectly and reproduces it on short prompts.

## MIM.2 API Surface Hardening Against Extraction Queries

**The core vulnerability:** Membership inference and model inversion attacks are dramatically more effective when the attacker has access to confidence scores, logprobs, or token probabilities. An API that returns only the top-1 completion provides far less signal than one that returns full logprob distributions.

### Check

- Does the model API return logprob values, confidence scores, or probability distributions — and if so, is that return justified by the use case, or is it a default that was never evaluated?
- Is there rate limiting on completion queries — preventing an attacker from making thousands of membership inference probes within a short window?
- Are anomalous query patterns — systematic prefix variations, high-entropy completions, repeated similar queries — detected and flagged?

### Action

- **Disable logprob and confidence score outputs unless explicitly required.** For any API that does not need logprobs for its application logic, remove the `logprobs` or `top_logprobs` parameter from the response. If logprobs are required (e.g., for calibration), return only the top-1 token probability and truncate precision.
- **Apply prediction rounding.** If confidence scores must be returned, round to two significant digits. This reduces extraction signal significantly with minimal impact on legitimate use.

```python
def safe_completion_response(raw_response) -> dict:
    return {
        "text": raw_response.text,
        # logprobs intentionally omitted
        # confidence returned as bucketed label, not raw float
        "confidence": "high" if raw_response.confidence > 0.8 else "medium" if raw_response.confidence > 0.5 else "low",
    }
```

- **Rate limit and monitor for extraction patterns.** A membership inference attack requires many queries (typically 100–10,000 per candidate record). Apply per-client rate limits of 100–500 requests per minute. Flag clients whose query distributions show high semantic similarity — a signal of systematic probing rather than organic use.

### Minimum Deliverable Per Review

- [ ] Memorization audit: prefix-completion probes on a training data sample, with exact match and overlap metrics
- [ ] Training data de-identification: PII removal or masking confirmed before training
- [ ] Training data deduplication: dedup method and confirmed execution
- [ ] API surface: logprobs and confidence scores disabled or bounded
- [ ] Rate limiting: per-client query rate and extraction pattern detection
- [ ] DP training: if in scope, ε budget and utility tradeoff documented

## Quick Win

**Disable `logprobs` in your API response schema if you are not using them.** Check your API call parameters. If `logprobs=True` or `top_logprobs=N` is set, remove it unless you have a specific application need. This single change closes the most data-rich channel available to membership inference attacks against your API.

## References

- Embedding inversion attacks → [embedding-attack-security/SKILL.md](../embedding-attack-security/SKILL.md)
- Fine-tuning data poisoning → [fine-tuning-security/SKILL.md](../fine-tuning-security/SKILL.md)
- PII compliance in training pipelines → [ai-privacy-pii-compliance/SKILL.md](../ai-privacy-pii-compliance/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
