---
name: llamaindex-rag-security
description: Review a LlamaIndex retrieval augmented generation stack for ingestion poisoning, node metadata loss, retriever scope failures, insecure query-engine composition, weak source attribution, and leakage through storage, memory, or observability layers.
last_reviewed: 2026-04-27
---

# LlamaIndex RAG Security

## First Principle

**LlamaIndex's `Node` is the unit of retrieval — and it is also the unit of trust. If node metadata is lost during parsing or chunking, you lose the ability to scope retrieval, verify citations, and enforce access control.**

LlamaIndex abstracts documents into `Node` objects that carry both content and metadata through the pipeline. Security in a LlamaIndex stack depends on whether that metadata survives: if `source_id`, `tenant_id`, `sensitivity`, and `doc_class` are dropped at any parsing, chunking, or transformation step, every downstream control that depends on metadata — retrieval scoping, citation verification, masking decisions — fails silently. The node is the trust anchor. Guard its metadata as carefully as its content.

Read the base [rag-security/SKILL.md](../rag-security/SKILL.md) first for the shared control model. This skill narrows the controls to concrete LlamaIndex review points.

## Framework Focus

- Readers, parsers, node creation, embeddings, index construction, and storage context
- `RetrieverQueryEngine`, router query engines, agents, response synthesizers, and postprocessors
- Metadata filters, node references, citation support, memory, and observability paths

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | Parsed nodes, metadata fields, storage context contents, retriever output, postprocessor changes, and synthesized response inputs are all validated before they influence the model or downstream systems. |
| **Scope** | Node metadata filters enforce tenant, user, and document-class scope at the index — not only in application logic. Router query engines cannot broaden scope beyond what the user is authorized to access. |
| **Isolate** | A poisoned node, a mis-scoped router decision, or a memory leakage cannot cascade from the LlamaIndex pipeline into unrestricted data access or core system compromise. |
| **Enforce** | Metadata validation, citation mapping against actual retrieved nodes, deletion verification, and schema-validated response handling are deterministic code controls — not model-layer promises. |

## LI.1 Source Grounding and Hallucination Mitigation

**The LlamaIndex-specific risk:** Response synthesizers can condense multiple nodes into a single answer, stripping the per-node provenance that citation verification requires. Router query engines can silently route to a broader engine than intended when confidence is low.

### Check

- Does node metadata — `node_id`, `source_id`, `doc_id`, page references — survive every parsing, chunking, postprocessing, and synthesis step?
- After response synthesis or condensation, are citations still verifiable against the exact nodes the retriever selected?
- Can router query engines route to broader or less-restricted engines without explicit policy authorization?

### Action

- **Metadata survival audit.** Trace a representative document through the full pipeline: `Reader` → `NodeParser` → `VectorStoreIndex` → `Retriever` → `Postprocessor` → `ResponseSynthesizer`. At each step, verify that `source_id`, `tenant_id`, `sensitivity`, and `doc_class` are present in `node.metadata`. A step that drops these fields breaks every downstream security control.
- **Server-side citation verification.** After synthesis, resolve every node reference in the response against the set of `node_ids` actually selected by the retriever for this request. Reject responses that cite nodes outside the retrieved set.

```python
retrieved_node_ids = {node.node_id for node in retrieved_nodes}
for citation in response.source_nodes:
    if citation.node.node_id not in retrieved_node_ids:
        raise CitationHallucinationError(citation)
```

- **Router policy enforcement.** For router query engines, define an explicit policy that maps query types to authorized engines. The router must not fall back to a broader engine silently — require an explicit fallback with a logged policy decision.
- **Refusal when grounding fails.** If postprocessors filter out too many nodes (low relevance, wrong scope, contradictory), the required output is a documented refusal — not speculative synthesis from the remaining fragments.

### Failure Modes

- `SimpleNodeParser` strips custom metadata during chunking. Downstream retrieval scoping silently fails because the `tenant_id` field is gone.
- A `RouterQueryEngine` routes to a "catch-all" engine when confidence is low. That engine has access to the full index, not the user's scoped sub-index.
- A `TreeSummarize` synthesizer compresses 10 nodes into one summary, losing per-node citation mapping. The model then cites specific pages it did not actually retrieve.

## LI.2 Data Leakage Prevention

**The LlamaIndex-specific risk:** LlamaIndex's storage context — `VectorStore`, `DocStore`, `IndexStore` — can share a backend across multiple users or tenants if not explicitly partitioned. Deletion and reindexing workflows may not remove nodes from all layers simultaneously, leaving zombie entries retrievable after they should have been purged.

### Check

- Are metadata filters enforced at the vector store query level — not only in application code — for tenant, document class, and sensitivity boundaries?
- When a document is deleted or updated, is the deletion applied to the vector store, the doc store, the index store, and all derived caches consistently?
- Are sensitive node metadata fields masked before nodes enter synthesis, agent tools, or observability integrations?

### Action

- **Vector store query filter construction.** Build metadata filters from the authenticated session context:

```python
filters = MetadataFilters(filters=[
    MetadataFilter(key="tenant_id", value=current_user.tenant_id, operator=FilterOperator.EQ),
    MetadataFilter(key="sensitivity", value=current_user.clearance_level, operator=FilterOperator.LTE),
    MetadataFilter(key="doc_class", value=current_user.authorized_doc_classes, operator=FilterOperator.IN),
])
retriever = index.as_retriever(filters=filters)
```

- **Deletion consistency audit.** For every delete and refresh workflow, verify that: the source document is removed from the `VectorStore` (embedding deleted), the `DocStore` (text deleted), the `IndexStore` (node references deleted), and any caching layer (embedding cache invalidated). Test this by attempting retrieval of a deleted document after deletion. If retrieval returns content, the deletion is incomplete.
- **Mask before synthesis.** Apply PII masking to `node.text` before nodes are passed to the `ResponseSynthesizer`. After synthesis, the PII is in the model's context and potentially in the response.
- **Storage context and observability access control.** Treat `StorageContext` backends and any observability integration (e.g., Arize, LlamaTrace) as sensitive data stores. Apply access control, retention limits, and field-level redaction equivalent to the application's data classification requirements.

### Minimum Deliverable Per Review

- [ ] LlamaIndex pipeline map: reader → parser → node creation → index → retriever → postprocessor → synthesizer → response
- [ ] Metadata survival check: which fields are present at each stage, which steps could drop them
- [ ] Citation verification implementation and fallback on failure
- [ ] Vector store filter construction: source (session context), enforcement point
- [ ] Deletion consistency: all storage layers covered
- [ ] Masking point: where PII masking is applied relative to synthesis

## Quick Win

**Run a metadata survival test.** Ingest a test document with known custom metadata (`tenant_id`, `sensitivity`, `doc_class`). Retrieve a chunk from it. Print `chunk.node.metadata`. If any of your security-critical fields are missing, you have found the leak in your metadata pipeline. Fix it before building any other control.

## References

- Base RAG control model → [rag-security/SKILL.md](../rag-security/SKILL.md)
- Leakage deep-dives → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Framework notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
