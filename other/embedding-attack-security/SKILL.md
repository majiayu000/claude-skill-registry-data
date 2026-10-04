---
name: embedding-attack-security
description: Review an embedding pipeline for vector database poisoning, embedding inversion attacks, cross-tenant retrieval leakage, adversarial query perturbations, and semantic similarity abuse that allows attacker-controlled content to dominate retrieval results.
last_reviewed: 2026-04-29
---

# Embedding Attack Security

## First Principle

**A vector database is not a neutral index. It is a ranked-choice system where the attacker's goal is to win the ranking.**

Embeddings translate text into geometric space. Retrieval finds nearest neighbors. This means every security property of your retrieval system — access control, content isolation, trust boundaries — depends on properties of a high-dimensional mathematical space that your application code cannot inspect. An attacker who understands your embedding model can craft inputs that reliably land near any target they choose, making your retrieval system deliver their content in response to legitimate user queries. They do not need to breach your database; they only need to get one document indexed.

## Attack Mental Model

Attackers targeting embedding systems operate across three surfaces:

1. **Vector database poisoning** — inject documents that embed close to high-value query vectors. When a user asks a related question, the poisoned document is retrieved with high similarity. The attack is persistent: a poisoned document remains in the index until explicitly removed.
2. **Embedding inversion** — use the embedding vector itself to recover approximations of the original text. When embeddings are stored or transmitted, they can leak sensitive content even when the source documents are not directly accessible.
3. **Adversarial perturbation** — craft queries or documents whose text appears benign but whose embedding lands in an attacker-controlled position in the vector space. Exploits the gap between human-readable text and the geometric interpretation of that text.

The attack does not require write access to the database. Any pathway that ingests user-supplied or externally sourced content into the vector index is a potential poisoning channel.

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Every document submitted for indexing is inspected for semantic anomalies — embeddings that land unexpectedly close to sensitive query clusters — before it is persisted. |
| **Scope** | Embeddings are generated and stored within strict tenant and data-class boundaries. A query for tenant A cannot retrieve embeddings generated from tenant B's documents, enforced at the datastore, not the application layer. |
| **Isolate** | Embedding vectors are not exposed externally in raw form. Inversion attack surface is minimized by treating embeddings as internal state, not API responses. |
| **Enforce** | Retrieval access controls are enforced as hard metadata filters at the vector store — not as soft instructions to the model or as application-layer post-filters. |

## EAS.1 Vector Database Poisoning Defense

**The core vulnerability:** Once a malicious document is indexed, it participates in every future retrieval that matches its embedding position. Similarity search has no built-in notion of document trustworthiness — a poisoned document retrieved with 0.95 cosine similarity is treated identically to a legitimate document retrieved with the same score.

### Check

- Is there a document ingestion review process that detects content designed to embed close to known sensitive query clusters?
- Is the ingestion pathway for external, user-supplied, or third-party content separated from the ingestion pathway for trusted internal content — with different validation requirements?
- Are large-scale index updates (bulk imports, corpus refreshes) reviewed for statistical embedding distribution shifts before the update is applied?
- Is there an index audit process that can retroactively detect poisoned documents — not just prevent future poisoning?

### Action

- **Separate ingestion tiers by trust level.** Documents ingested from external sources (user uploads, web crawls, vendor feeds) must pass a higher validation bar than internal documents. At minimum: content scanning, metadata completeness check, and embedding proximity analysis before indexing.
- **Run embedding proximity analysis at ingestion time.** Before indexing a new document, compute its embedding and check whether it lands within a defined radius of any high-sensitivity query cluster (support queries, admin commands, financial data queries). Flag documents that score unusually high proximity to sensitive clusters for human review.

```python
# Embedding proximity check at ingestion (pseudocode)
SENSITIVE_CLUSTERS = load_sensitive_query_embeddings()  # pre-computed from audit

def check_ingestion_proximity(document_embedding, threshold=0.92):
    for cluster_name, cluster_embedding in SENSITIVE_CLUSTERS.items():
        similarity = cosine_similarity(document_embedding, cluster_embedding)
        if similarity > threshold:
            raise EmbeddingProximityAlert(
                f"Document embeds within {similarity:.3f} of sensitive cluster '{cluster_name}'"
            )
```

- **Implement index versioning and rollback.** Treat the vector index as a versioned artifact. Before any bulk import or corpus refresh, snapshot the current index state. If anomalous retrieval behavior is detected post-update, roll back to the last known-good snapshot.
- **Run periodic poisoning audits.** On a defined schedule, query the index with a set of known sensitive query vectors and inspect the top-k results for each. Documents appearing in sensitive query results that do not belong there are poisoning candidates.
- **Enforce content provenance in metadata.** Every indexed document must carry: `source`, `ingest_timestamp`, `ingest_tier` (trusted/external), `ingested_by`. This metadata is required for forensic reconstruction when a poisoned document is discovered.

### Failure Modes

- A user-submitted document is indexed without proximity analysis. It was crafted to embed close to "password reset instructions" query vectors. When users ask about account access, the poisoned document is retrieved with high confidence and displayed as authoritative guidance.
- A bulk corpus refresh imports 50,000 documents from an external vendor. The import is not diffed against the prior index state. 200 of the imported documents were poisoned by the vendor's supply chain and embed close to high-sensitivity clusters.
- An attacker splits a poisoning attempt across multiple seemingly innocuous documents. No single document triggers proximity alerts, but together they create a retrieval cluster that dominates results for a targeted query pattern.

## EAS.2 Embedding Inversion and Leakage Prevention

**The core vulnerability:** Embedding vectors are not opaque identifiers. Research has demonstrated that embedding models can be inverted with varying degrees of fidelity — given an embedding vector, it is often possible to recover significant information about the original text. When embeddings are stored in accessible locations, transmitted over APIs, or returned in debug output, they become a data leakage surface.

### Check

- Are raw embedding vectors ever returned in API responses, logs, or debug output — or are they treated as internal state only?
- Are embeddings of PII-containing documents stored separately from embeddings of general documents, with stricter access controls?
- Is the embedding model itself treated as a sensitive asset — or is it accessible in a way that enables white-box inversion attacks?
- Are there access controls on the vector store at the embedding retrieval level, or only at the document retrieval level?

### Action

- **Never return raw embedding vectors in API responses.** Embedding vectors are internal state. If your API returns similarity scores, return normalized scalars, not raw vectors. If an internal service needs vectors for debugging, gate that endpoint behind explicit authorization and log every access.
- **Apply differential metadata to PII-adjacent embeddings.** When documents containing PII must be indexed (after appropriate PII scrubbing), mark their embeddings with a `pii_adjacent: true` metadata field. Apply additional access controls: these embeddings are only retrievable under stricter authorization checks.

```python
# PII-adjacent embedding isolation (pseudocode)
def index_document(doc, user_context):
    embedding = embed(doc.text_after_pii_scrub)
    metadata = {
        "doc_id": doc.id,
        "tenant_id": user_context.tenant,
        "pii_adjacent": doc.contained_pii_before_scrub,
        "sensitivity": doc.sensitivity_class,
        "ingest_tier": user_context.ingest_tier,
    }
    vector_store.upsert(embedding, metadata)
    if doc.contained_pii_before_scrub:
        access_control_store.set(doc.id, required_clearance="pii-authorized")
```

- **Restrict access to the embedding model's weights and architecture.** In self-hosted embedding deployments, treat the model weights as a secrets-tier asset. White-box inversion is significantly more effective than black-box; an attacker with the model weights can perform near-perfect inversion given stored vectors.
- **Apply embedding noise for highly sensitive content.** For documents classified at the highest sensitivity tier, consider adding calibrated noise to embeddings before storage (a form of embedding-space differential privacy). This degrades retrieval precision slightly but substantially increases the cost of inversion. Evaluate the retrieval quality tradeoff for your use case.
- **Audit vector store access logs.** Log every query against the vector store, including the filter parameters applied, the number of results returned, and the requesting identity. High-volume queries with broad or absent filters are inversion attack indicators.

### Minimum Deliverable Per Review

- [ ] Ingestion tier diagram: trusted vs. external pathways and their respective validation gates
- [ ] Embedding proximity check: sensitive cluster definitions, threshold, and review path for flagged documents
- [ ] Index versioning and rollback procedure: snapshot cadence and tested recovery path
- [ ] Embedding leakage inventory: all API surfaces, logs, and debug outputs that could expose raw vectors
- [ ] PII-adjacent embedding policy: separate metadata, access controls, and any noise parameters applied
- [ ] Periodic poisoning audit schedule and findings log

## Quick Win

**Add embedding proximity analysis as a pre-indexing gate for all external content.** Pre-compute embeddings for your 20 highest-sensitivity query patterns. Before indexing any document from an external source, check its cosine similarity against each. Flag anything above 0.90 for human review. This single control blocks the most direct form of vector poisoning — content crafted to hijack retrieval for specific high-value queries — with one function call per ingested document.

## References

- Retrieval boundary enforcement and metadata filters → [rag-security/SKILL.md](../rag-security/SKILL.md)
- PII scrubbing pipelines before indexing → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Indirect prompt injection via retrieved content → [indirect-prompt-injection/SKILL.md](../indirect-prompt-injection/SKILL.md)
- Memory poisoning via retrieval systems → [memory-security/SKILL.md](../memory-security/SKILL.md)
- Severity wording → [severity-and-reporting.md](../../references/severity-and-reporting.md)
- Repeatable attack cases → [test-patterns.md](../../references/test-patterns.md)
