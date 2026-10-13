---
name: ai-model-extraction
description: >
  Extract or steal an ML/LLM model's parameters, training data, or system prompt via query
  access — model stealing, membership inference, training-data extraction. Load when testing an
  ML API/endpoint, "model extraction/inversion", data-leakage or IP-theft concerns, exposed
  inference endpoints. Signals: a predict/inference API, embeddings endpoint, fine-tuned model.
domain: ai-ml
type: technique
stability: learning
modes: [bugbounty, defense]
severity: high
owasp_llm: [LLM02:2025-Sensitive-Information-Disclosure, LLM10:2025-Unbounded-Consumption]
cwe: [CWE-200]
tools: []
schema_version: 1
---

# Model extraction & data inference

## When it applies
You have query access to an ML/LLM endpoint and want to show it leaks the model itself, its
training data, or confidential context — IP theft or privacy impact, not just a bad answer.

## Why it works
Query access is more powerful than it looks. Outputs (labels, probabilities, embeddings,
generations) carry information about the model and its data. Enough targeted queries reconstruct a
functional copy, reveal whether a record was in training, or regurgitate memorized secrets.

## Method
1. **Model stealing**: query systematically (esp. if confidence scores/logits are returned) to
   train a surrogate that mimics the target — proves the model can be cloned via the API.
2. **Membership inference**: compare model behaviour (confidence, loss) on candidate records to
   infer whether a specific record was in the training set (privacy impact).
3. **Training-data / secret extraction (LLM)**: prompt for memorized data — PII, keys, or the
   system prompt/hidden context (overlaps `ai-prompt-injection`); look for verbatim regurgitation.
4. **Embedding inversion**: if an embeddings API is exposed, reconstruct approximate input text
   from vectors.
5. **Cost/DoS angle**: unbounded/unthrottled querying is itself a finding (LLM10).

## Gotchas
- Tie it to impact: a stolen surrogate, a confirmed membership leak, or verbatim secret output — not "it answered a lot".
- Respect scope/RoE — extraction requires many queries; get authorization and mind rate/cost limits.
- Defenders: rate-limit, strip logits, add output filtering, and monitor query patterns.

## Verify success
Demonstrated leakage: a working surrogate, a reliable membership inference, or verbatim
training-data/secret extraction.

## References
OWASP LLM Top 10 (2025); "Stealing ML models via prediction APIs" (Tramèr et al.); membership-inference literature.
