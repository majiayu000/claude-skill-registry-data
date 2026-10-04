---
name: haystack-rag-security
description: Review a Haystack retrieval pipeline for router scope failures, insecure document-store access, weak grounding, metadata-filter bypass, and leakage through pipeline components or evaluators.
last_reviewed: 2026-04-27
---

# Haystack RAG Security

## First Principle

**A Haystack pipeline is a directed graph of components. Every edge in that graph is a trust boundary where one component's output becomes the next component's untrusted input — unless you validate it explicitly.**

Haystack's pipeline abstraction makes it easy to wire routers, retrievers, rankers, generators, and evaluators together. The security implication is that data flows between components automatically, and unless you validate at each boundary, a poisoned document entering through a retriever can flow unmodified through a ranker and into a generator's prompt. The router is especially critical: a misconfigured router that routes queries to a broader branch than intended is a retrieval scope failure that no amount of per-component hardening will catch.

Read the base [rag-security/SKILL.md](../rag-security/SKILL.md) first for the shared control model. This skill narrows the controls to concrete Haystack review points.

## Framework Focus

- Pipelines, routers, retrievers, rankers, generators, and evaluators
- Document stores, metadata filters, ingestion, and update paths
- Pipeline component wiring, intermediate outputs, and observability

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Documents, metadata filters, router decisions, retrieved documents, and generator inputs are all checked before they influence a response. |
| **Scope** | Document-store access, pipeline branches, and component access are constrained to the records and sources the current user or tenant is authorized to see. |
| **Isolate** | A poisoned pipeline branch or over-broad router decision cannot silently expose unrelated stores, components, or data domains to the current user. |
| **Enforce** | Document-store filters, pipeline validation, citation checks, and typed component contracts are deterministic controls — not conventions the generator is expected to follow. |

## HS.1 Source Grounding and Pipeline Boundary Review

**The Haystack-specific risk:** Router components can send queries down branches that access different document stores with different trust levels. If the router's branch selection logic is based on semantic similarity or query classification, an attacker can craft queries that steer routing toward a more permissive or less-controlled branch.

### Check

- Does router logic enforce tenant and document-class scope when selecting between branches — or does it route based on semantic content alone?
- After ranking and generation, is there a component that verifies that the generated answer is grounded in documents that were actually retrieved by the authorized retriever?
- When retrieval confidence is weak, does the pipeline fail closed (refusal) or fail open (generator produces an ungrounded answer)?

### Action

- **Audit router branch policies.** For every router component, define an explicit policy that maps branch selection criteria to authorized scope. If the router uses a semantic classifier, verify that the classifier cannot be steered into a broader branch by adversarial query crafting.

```python
# Router policy should be explicit and not purely semantic
class ScopedRouter(Component):
    def run(self, query: str, user_scope: UserScope) -> dict:
        # Scope is determined by user context, not query content
        if user_scope.data_class == "hr":
            return {"hr_retriever": query}
        elif user_scope.data_class == "engineering":
            return {"eng_retriever": query}
        else:
            raise ScopeViolationError(f"Unknown data class: {user_scope.data_class}")
```

- **Post-generation grounding check.** After the generator produces a response, verify that every factual claim can be traced to a document ID from the retrieved set for this pipeline run. Implement this as a pipeline component that follows the generator.
- **Fail-closed on weak retrieval.** Add a confidence gate component before the generator. If the top-k retrieved documents have average relevance below threshold, route to a refusal generator — not the main generator.
- **Evaluator and debugging output security.** Evaluator components and debugging outputs in Haystack can capture full document content and generated responses. Treat these outputs as sensitive data streams with access control and field-level redaction.

### Failure Modes

- A router uses a query classifier that routes "sensitive" queries to the compliance branch. An attacker crafts a query that reads as non-sensitive to the classifier but retrieves compliance data from the targeted branch.
- The ranker reorders retrieved documents and does not preserve the document store filter metadata. A high-scoring document from outside the user's authorized store ranks first and appears in the generator's prompt.
- An evaluator component logs full document content to assess retrieval quality. The evaluator log stream has weaker access control than the document store.

## HS.2 Scoped Retrieval and Store Isolation

**The Haystack-specific risk:** Haystack supports multiple document store backends (Elasticsearch, OpenSearch, Weaviate, Qdrant, etc.). Each has different filter syntax and different server-side enforcement guarantees. A filter that works correctly in one backend may be silently ignored or partially enforced in another.

### Check

- Are document store filters constructed from authenticated session context — not from query content or user-provided text?
- Are the filters passed as backend parameters (server-side enforced) — not as soft filtering in the retriever component code?
- Do ingestion, update, and reindex pipelines preserve provenance and sensitivity metadata in the target document store?

### Action

- **Construct filters from session context only.** The filter parameters passed to the document store must derive exclusively from the authenticated user's session, not from any user-controlled or model-generated input.

```python
# Build filter from session context, not query
filters = {
    "operator": "AND",
    "conditions": [
        {"field": "meta.tenant_id", "operator": "==", "value": current_user.tenant_id},
        {"field": "meta.sensitivity", "operator": "<=", "value": current_user.clearance_level},
        {"field": "meta.doc_class", "operator": "in", "value": current_user.authorized_doc_classes},
    ]
}
retriever = InMemoryBM25Retriever(document_store=store, filters=filters)
```

- **Verify backend-level filter enforcement.** For your specific document store backend, confirm that the filter parameters are enforced at the backend query level — not filtered post-retrieval in Python code. Test this by retrieving with a deliberately wrong `tenant_id` and verifying that documents from other tenants are not returned.
- **Ingestion pipeline metadata preservation.** For every ingestion and update pipeline, verify that `tenant_id`, `sensitivity`, `doc_class`, and `source_id` are written to the document store record, not just to the Python `Document` object. Metadata that exists only in the Python layer is lost at persistence.

### Minimum Deliverable Per Review

- [ ] Haystack pipeline graph with trust level per branch and retriever scope
- [ ] Router branch selection policy — criteria and enforcement point
- [ ] Post-generation grounding check implementation or gap
- [ ] Document store filter construction: source, syntax, and server-side enforcement verification
- [ ] Evaluator and debugging output access control and redaction

## Quick Win

**Test your document store filter enforcement.** Write a retrieval test that queries your document store with a `tenant_id` that belongs to a different tenant. If any documents from the other tenant are returned, your server-side filter enforcement is broken and every tenant's data is visible to every other tenant's queries.

## References

- Base RAG control model → [rag-security/SKILL.md](../rag-security/SKILL.md)
- Leakage deep-dives → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Framework notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
