---
name: rag-security
description: Review a retrieval augmented generation system for ingestion poisoning, retrieval boundary failures, insecure chunking and metadata handling, document trust confusion, and cross-tenant or stale-context exposure across any language or framework.
last_reviewed: 2026-04-27
---

# Retrieval Augmented Generation Security

## First Principle

**Every retrieved document is a potential attacker input. The retrieval system is an attack surface as large as your corpus.**

RAG systems were designed to extend LLM knowledge with external data. That same mechanism — injecting external text into the prompt — is the canonical indirect prompt injection path. The document the model trusts most is the document the attacker poisons first. The scope of what can be retrieved defines the blast radius of every injection in your corpus.

## Attack Mental Model

Attackers targeting RAG systems operate on two surfaces:

1. **Ingestion poisoning** — inject malicious content into documents before they enter the vector store. When a user asks a related question, the poisoned chunk is retrieved and executed as context.
2. **Retrieval boundary violation** — exploit weak or missing metadata filters to retrieve documents the user was never authorized to see (cross-tenant, cross-classification, stale data).

The attacker does not need account credentials. They need a document that scores high on semantic similarity to a predictable query.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every ingested document, metadata field, chunk boundary, retrieval result, and reranker output is checked before it influences a prompt or response. |
| **Scope** | Retrieval is bounded to authorized documents, approved metadata filters, and the current user's data class — enforced at the datastore, not in the prompt. |
| **Isolate** | A poisoned or over-broad retrieval result cannot cascade into unrestricted data access, privilege escalation, or persistent memory writes. |
| **Enforce** | Citations are verified server-side against the actual retrieved set. Model claims about sources are not trusted as proof of grounding. |

## 2.1 Source Grounding and Hallucination Mitigation

**The core vulnerability:** The model will generate confident-sounding text regardless of whether its retrieved context supports the claim. If you do not verify citations against the actual retrieved set, you have no grounding — you have hallucination dressed as sourcing.

### Check

- Does every factual claim trace to a specific retrieved chunk by ID, not just by model assertion?
- Is citation verification done in application code, not by asking the model to self-verify?
- Does the system define a minimum retrieval confidence threshold below which it refuses to answer?

### Action

- **Citation mandate:** Require the model to emit structured citations in the response schema: `{"answer": "...", "citations": [{"chunk_id": "...", "doc_id": "..."}]}`
- **Server-side citation verification:** After the response is generated, resolve every emitted `chunk_id` against the actual retrieved set for this request. Reject or flag responses citing chunks that were not retrieved.
- **Confidence gate:** Compute a retrieval confidence score (e.g., mean similarity of top-k chunks). If it falls below threshold, emit the required refusal: `I cannot answer this question with the available documentation.`
- Never allow the model to answer from chat history, model prior, or memory when the configured mode is documentation-grounded only.

```python
# Server-side citation verification (pseudocode)
retrieved_ids = {chunk.id for chunk in retrieved_chunks}
for citation in response.citations:
    if citation.chunk_id not in retrieved_ids:
        raise CitationHallucinationError(citation)
```

### Failure Modes

- Model cites `[Source: Policy_v2.pdf, p. 4]` but that document was not retrieved — the citation was fabricated.
- Retrieval confidence is low (all chunks are tangentially related) but the system answers anyway.
- Chat history from a prior session silently overrides retrieved evidence.

## 2.2 Data Leakage Prevention

**The core vulnerability:** Vector search is semantic, not access-controlled by default. A query for "vacation policy" may retrieve HR documents from every tenant in a multi-tenant index. The filter is only as strong as the code that sets it — and if that code runs in application layer, a prompt injection can bypass it.

### Check

- Are metadata filters for tenant, user, document class, and sensitivity enforced server-side at the vector store — not only in the prompt or application logic?
- Is PII screened from retrieved chunks before they enter the prompt context?
- Are sensitivity and provenance metadata preserved through chunking, re-embedding, and reindexing?

### Action

- **Query scoping:** Before querying the vector store, construct strict metadata filters: `{"tenant_id": current_user.tenant, "doc_class": {"$in": user.authorized_classes}}`. Pass these as server-enforced filter parameters, not as soft instructions.
- **PII masking:** Apply a masking pipeline to retrieved chunks before prompt assembly. Mask, do not strip — preserve the structure while redacting sensitive fields.
- **Provenance persistence:** Ensure chunking, re-embedding, and reindexing pipelines carry `doc_id`, `sensitivity`, `owner`, and `created_at` through every transformation. A chunk without provenance metadata cannot be correctly scoped.
- **Double enforcement:** Check authorization at ingestion time (does this document belong in this tenant's index?) and at retrieval time (is this user allowed to see this chunk?).

### Minimum Deliverable Per Review

- [ ] RAG dataflow diagram: ingestion → chunking → indexing → retrieval → reranking → prompt assembly → response
- [ ] Citation policy and server-side verification path
- [ ] Query-scoping filter construction and enforcement point (server-side vs. application-side)
- [ ] PII masking pipeline and fields masked
- [ ] Fallback behavior when confidence threshold is not met

## Quick Win

**Add server-side metadata filters immediately.** If your vector store queries do not pass a tenant or user scope filter as a hard parameter — not a soft prompt instruction — your retrieval boundary exists only in convention. One prompt injection can bypass it.

## References

- Framework-specific review notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
- Repeatable attack cases → [test-patterns.md](../../references/test-patterns.md)
- Deeper leakage controls → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
