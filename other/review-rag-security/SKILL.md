---
name: review-rag-security
description: Audit retrieval-augmented generation pipelines, vector and embedding systems, enterprise search, and agent knowledge stores from ingestion through generated output. Use when reviewing source provenance, poisoning, indirect prompt injection, tenant and document authorization, vector-store isolation, sensitive-data leakage, deletion and freshness, retrieval integrity, citations, or RAG security controls.
---

# Review RAG Security

Assess the complete knowledge path from source admission to retrieved context and downstream use. Verify effective data authorization and provenance outside the model.

Read [methodology](references/methodology.md) before selecting isolation, poisoning, or retrieval-integrity tests.

## Safety boundaries

- Work read-only against production indexes unless the user explicitly authorizes a reversible isolated test.
- Use a disposable namespace or local fixture for poisoned, adversarial, or cross-tenant documents.
- Use synthetic canaries instead of personal, confidential, privileged, copyrighted, or credential data.
- Do not attempt embedding inversion, bulk extraction, destructive reindexing, or unauthorized tenant access.
- Cap query count, retrieval depth, embedding cost, and external requests.
- Stop and preserve evidence if real sensitive data, another tenant's content, or unexpected production mutation appears.

## Workflow

1. **Define the knowledge boundary.** Record users, tenants, data classes, allowed sources, document-level policy, freshness and deletion requirements, expected citations, downstream actions, environment, and authorization.
2. **Fingerprint the pipeline.** Pin application revision, source connectors, parser and chunker, embedding model, index and namespace, metadata schema, retriever and reranker, filters, prompt assembly, generator, caches, guardrails, and corpus snapshot.
3. **Trace the lifecycle.** Map `source -> admission -> parse -> transform -> chunk -> embed -> index -> authorize -> retrieve -> rerank -> prompt -> output -> action or cache`. Mark trust, tenant, identity, and policy boundaries.
4. **Review provenance and admission.** Verify source ownership, allowlisting, authentication, signatures or hashes where used, ingestion identity, malware and content checks, change history, reviewer gates, and rollback.
5. **Review authorization and isolation.** Determine where tenant, user, group, document, and field permissions are enforced. Verify query-time enforcement, cache keys, namespace isolation, service identities, metadata defaults, and fail-closed behavior.
6. **Test controlled cases.** Use synthetic documents to test cross-tenant retrieval, stale or revoked access, deletion propagation, duplicate and conflicting sources, poisoned ranking, indirect instructions, citation mismatch, sensitive canary leakage, and fallback behavior.
7. **Measure retrieval evidence.** Preserve query identity, filters, candidate and final chunk IDs, scores, source versions, assembled context, answer, citations, cache state, and repeated trials.
8. **Trace downstream impact.** Determine whether retrieved content only affects text or can influence a tool, decision, memory, workflow, or privileged user.
9. **Recommend and regress.** Move authorization before context assembly, strengthen provenance and lifecycle controls, isolate untrusted content, and create reproducible fixtures for each confirmed failure.

## Evidence rules

- Assign stable IDs to sources, chunks, queries, identities, trials, and evidence.
- Preserve source and corpus hashes plus parser, chunker, embedding, retriever, and prompt versions.
- Record candidates before filtering and the final context when instrumentation permits.
- Test with the effective requesting identity and record its tenant and groups.
- Repeat rank-sensitive cases and retain all results.
- Separate retrieval failure, generation failure, authorization failure, and provenance failure.
- Require a complete source-to-consequence path and evidence for every finding.

## Output contract

Return:

1. Scope, data classes, authorization, target fingerprint, and limitations.
2. Source inventory, provenance matrix, and lifecycle data-flow diagram.
3. Identity, tenant, document, metadata, cache, and effective-access matrix.
4. Controlled test matrix with fixtures, expected retrieval, actual candidates and context, answer or action, trials, cleanup, and evidence.
5. Findings with affected identities and data, full path, impact, reproducibility, severity, confidence, and framework mapping.
6. Prioritized admission, authorization, isolation, provenance, deletion, monitoring, and regression plan.
7. Unknown, not-tested, out-of-scope, and residual-risk sections.

Write each finding as: `ID | source or tenant | requesting identity | preconditions | source-to-context path | violated control | disclosure or integrity consequence | trials | evidence | severity | confidence | remediation | regression | framework mapping`.

## Quality gate

Do not finalize until:

- Every source, transformation, index, cache, and retrieval identity has an owner or explicit unknown.
- Document authorization is verified at query time, not inferred from ingestion-time controls.
- Cross-tenant, stale-access, deletion, poisoning, indirect-instruction, and citation cases are marked tested, not tested, or not applicable.
- Corpus and component versions make rank-sensitive results reproducible.
- Findings distinguish unauthorized retrieval from undesirable generation.
- Dynamic tests use isolated synthetic fixtures and include cleanup evidence.
- Every remediation includes a regression fixture and expected retrieved chunk set.
