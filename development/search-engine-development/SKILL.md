---
name: search-engine-development
description: "Use when building a search system over an application, document collection, or structured dataset without a public-web crawler as its main purpose to define corpus scope, tokenization, ranking goals, freshness, and access rules before indexing. Trigger for analyzers, inverted indexes, query execution, ranking, or search relevance work."
---

# Search Engine Development

## Overview

This skill applies when building a search system over an application, document collection, or structured dataset without a public-web crawler as its main purpose. Its intended outcome is to define corpus scope, tokenization, ranking goals, freshness, and access rules before indexing.

## When to Use

### Preserved source section: When to Use

Use for local, enterprise, or application search over an authorized corpus. For discovering and crawling public web pages, use `web-search-engine-development` instead.

## Scope

**Does:** Follow the task boundary stated under When to Use and Instructions.

**Does not:** See the preserved source boundaries below and under Stop Conditions.

### Source boundary statements from: Procedure

2. **Build a transparent ingestion path.** Normalize documents with provenance, stable identifiers, timestamps, and deletion/update handling. Do not index data outside the user's authorized scope.

### Source boundary statements from: Output and Acceptance

Report corpus boundaries, analyzer and ranking choices, access checks, freshness guarantees, evaluation results, and scaling limits. Accept only when results are relevant on the declared test set and unauthorized or deleted content cannot leak through stale indexes.

## Inputs

**Required:** See the preserved source input guidance below.

**Optional:** Not specified in source skill.

**Prerequisites:** Not specified in source skill.

### Preserved source section: Inputs

- Authorized data sources, document types, update frequency, and retention rules.
- Query language, language/locale needs, ranking goals, latency, and scale.
- Access-control model, privacy restrictions, and relevance judgments or evaluation data.

## Instructions

### Preserved source section: Procedure

1. **Define relevance.** Specify what counts as a useful result, representative queries, ranking signals, and a baseline metric before tuning.
2. **Build a transparent ingestion path.** Normalize documents with provenance, stable identifiers, timestamps, and deletion/update handling. Do not index data outside the user's authorized scope.
3. **Implement a baseline index.** Start with a simple inverted index and deterministic analyzer. Document tokenization, stemming, stop words, and Unicode normalization.
4. **Make queries safe and explainable.** Parse the supported query syntax, bound expansion and result size, enforce access controls before results are returned, and expose enough scoring detail to debug relevance.
5. **Test lifecycle and privacy.** Cover insert, update, delete, stale index entries, permission changes, empty queries, malformed input, and sensitive terms in logs.
6. **Evaluate with judgments.** Use held-out queries or human relevance labels, measure precision/recall or task-specific outcomes, and avoid tuning against the same small set indefinitely.
7. **Measure operations.** Track index size, freshness lag, latency percentiles, and failure/rebuild behavior under a representative workload.

## Decision Rules

The following source conditional guidance is preserved verbatim; no unstated action is inferred.

### Source conditional guidance from: Output and Acceptance

Report corpus boundaries, analyzer and ranking choices, access checks, freshness guarantees, evaluation results, and scaling limits. Accept only when results are relevant on the declared test set and unauthorized or deleted content cannot leak through stale indexes.

## Output Format

### Preserved source section: Output and Acceptance

Report corpus boundaries, analyzer and ranking choices, access checks, freshness guarantees, evaluation results, and scaling limits. Accept only when results are relevant on the declared test set and unauthorized or deleted content cannot leak through stale indexes.

## Validation Checklist

- [ ] Verify the source-defined success criteria above.

## Edge Cases and Recovery

### Source edge/failure guidance from: Procedure

5. **Test lifecycle and privacy.** Cover insert, update, delete, stale index entries, permission changes, empty queries, malformed input, and sensitive terms in logs.
7. **Measure operations.** Track index size, freshness lag, latency percentiles, and failure/rebuild behavior under a representative workload.

## Stop Conditions

### Source stop-related guidance from: Procedure

3. **Implement a baseline index.** Start with a simple inverted index and deterministic analyzer. Document tokenization, stemming, stop words, and Unicode normalization.

## Examples

Not specified in source skill. The original provided no input/output example, and none has been invented.

## Success Criteria

### Acceptance criteria from source: Output and Acceptance

Report corpus boundaries, analyzer and ranking choices, access checks, freshness guarantees, evaluation results, and scaling limits. Accept only when results are relevant on the declared test set and unauthorized or deleted content cannot leak through stale indexes.
