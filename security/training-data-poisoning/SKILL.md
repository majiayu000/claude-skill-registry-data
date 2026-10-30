---
name: training-data-poisoning
description: Detects training and fine-tuning pipelines that ingest external data without
  integrity gating. Use when writing fine-tuning pipelines, dataset ingestion
  scripts, external training data loaders, or code that collects and processes
  data for model training. Also invoke when automating dataset curation from
  web scraping or user-contributed sources.
---

# Training Data Poisoning Security Check (OWASP LLM03:2025)

## What this checks

Protects against malicious or low-quality examples being introduced into training or
fine-tuning datasets. Poisoned data can embed backdoors, degrade accuracy, or skew
model behavior in ways that are difficult to detect after training completes.

## Vulnerable patterns

- Ingesting scraped or user-contributed examples with no content validation
- No deduplication or anomaly detection on training set statistics
- Loading dataset files without verifying provenance or checksums
- Using the same split for training and validation, hiding distribution shift

## Fix immediately

Flag the vulnerable code, explain the risk, and suggest a fix establishing these
properties. Translate to the data-loading and validation libraries of the audited file
— use that stack's documented hashing, schema, and dataframe APIs; do not import a
recipe from a different stack.

1. **Every external dataset file is checksum-verified before use.** A pinned SHA-256 in version control; the loader computes the digest on load and refuses to proceed on mismatch. Pinning a URL or version alone does not help when the bytes behind them change.
2. **Every example passes content validation** before entering the training set: type and length checks, disallowed-pattern filtering for known injection or jailbreak markers, and encoding/Unicode sanity. Invalid examples are dropped, not silently used.
3. **Duplicates are removed before training.** Poisoning attacks often batch the same backdoor trigger across many examples; deduplication by content hash limits the leverage of a single injected payload.
4. **Label distribution is checked and alerts fire on imbalance** above a threshold. A sudden one-class shift is a statistical signature of bulk-inserted poison; it is cheap to catch at ingestion and impossible to reverse after training.
5. **Train and validation splits come from disjoint sources or time windows.** Reusing the same split for both hides distribution shift and lets poisoned examples score well on validation.

## Verification

Confirm the response:

- [ ] For every external dataset load present, files are verified against pinned checksums before use
- [ ] Every training example passes content validation (length limits, disallowed-pattern filtering)
- [ ] Duplicates are removed before training starts
- [ ] For every dataset with categorical labels present, class distribution is checked and alerted on imbalance above a threshold
- [ ] Train and validation splits come from disjoint sources or time windows

## References

- CWE-20 ([Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html))
- CWE-1021 ([Improper Restriction of Rendered UI Layers](https://cwe.mitre.org/data/definitions/1021.html))
- [OWASP LLM03:2025 Training Data Poisoning](https://genai.owasp.org/llmrisk/llm03-training-data-poisoning/)
