---
name: langchain-rag-security
description: Review a LangChain retrieval augmented generation stack for document poisoning, retriever scope failures, insecure chain composition, weak citation grounding, metadata filter bypass, and leakage from callbacks, memory, or intermediate steps.
last_reviewed: 2026-04-27
---

# LangChain RAG Security

## First Principle

**LangChain's power is composability. Its security risk is the same thing: every component in your chain is a potential trust-boundary violation if the boundary between them is not explicitly defined.**

LangChain makes it easy to connect retrievers, memory, tools, agents, and callbacks into a single flow. That ease of composition is why teams adopt it — and why attackers target it. Each joint in the chain is a trust boundary: retrieved documents entering the prompt, memory state merging with retrieved context, callback handlers logging intermediate steps, agents passing scratchpad content to sub-chains. If you have not defined what is trusted at each boundary, you have not defined a security posture — you have defined a pipeline.

Read the base [rag-security/SKILL.md](../rag-security/SKILL.md) first for the shared control model. This skill narrows the controls to concrete LangChain review points.

## Framework Focus

- `Retriever`, `VectorStoreRetriever`, and hybrid retriever configuration
- `ConversationalRetrievalChain`, `RetrievalQA`, LCEL graphs, and custom chain composition
- Document loaders, text splitters, embeddings, vector stores, rerankers, and callback handlers
- Memory, chat history injection, intermediate steps, and tracing outputs

## Control Lens

| Principle | What It Means Here |
|---|---|
| **Validate** | `Document` objects, metadata filters, callback payloads, memory state, and final prompt inputs are all validated before they influence the model or downstream systems. |
| **Scope** | Retrievers, filters, chain composition, and memory are constrained to the approved source set and tenant context. `k`, score thresholds, and reranker settings are reviewed as security controls, not only performance knobs. |
| **Isolate** | A compromised LangChain component — injected Document, poisoned memory, unsafe callback — cannot pivot through the chain into privileged tools, the vector store, or core data stores. |
| **Enforce** | Server-side filter checks, citation verification, schema validation, and typed chain outputs are the enforcement layer — not model-shaped structure trusted at face value. |

## LC.1 Source Grounding and Hallucination Mitigation

**The LangChain-specific risk:** `chat_history` and conversational memory can silently override retrieved evidence in `ConversationalRetrievalChain`. The chain was designed to blend context — which means prior conversation can become the dominant evidence source, displacing the retrieval the user expects.

### Check

- When `ConversationalRetrievalChain` or equivalent is used, can `chat_history` or memory override retrieved `Document` objects as the primary answer source?
- Do callback handlers expose when the answer used documents outside the configured retriever result set?
- Do intermediate chain steps label whether content came from retrieval, memory, tool output, or model prior?

### Action

- **Trace the citation path through chain composition.** Walk the LCEL graph or chain configuration and identify every point where `Document` object provenance could be lost — prompt templates that flatten documents without preserving `metadata`, rerankers that discard source fields, condensation steps that summarize without attribution.
- **Verify citations against the actual `Document` set.** After chain completion, resolve every emitted citation against the `Document.metadata["source"]` and `Document.metadata["doc_id"]` values actually returned by the retriever for this request. Do not trust citation-shaped text in the model output.
- **Enforce retriever-only mode.** When the configured behavior is documentation-grounded, verify that `chat_history` and memory cannot provide the answer when retrieval fails — require a fallback refusal instead.
- **Audit callback handlers.** Callbacks in LangChain can log intermediate steps, prompts, and retrieved content. Treat callback payloads as sensitive data. Confirm they log only redacted identifiers, not raw document text or raw prompts.

```python
# Server-side citation verification for LangChain
retrieved_sources = {doc.metadata["doc_id"] for doc in retrieved_docs}
for citation in response.citations:
    if citation.doc_id not in retrieved_sources:
        raise CitationHallucinationError(f"Citation {citation.doc_id} not in retrieved set")
```

### Failure Modes

- `chat_history` contains a prior turn where the model stated a fact confidently. In the current turn, retrieval returns weak evidence. The chain uses `chat_history` as primary evidence and the user receives a hallucination dressed as retrieval.
- A custom LCEL step merges tool output and retrieved documents into a single context block. The model cannot distinguish retrieval evidence from tool output, and neither can the citation verifier.
- LangSmith traces capture full prompt text including retrieved chunks containing PII. The trace stream has weaker access controls than the application.

## LC.2 Data Leakage Prevention

**The LangChain-specific risk:** Metadata filters in LangChain vector store integrations are constructed in application code and passed to the backend. If the backend does not enforce them server-side — or if a prompt injection can influence filter construction — the scope boundary fails.

### Check

- Are metadata filters constructed by deterministic application code from the authenticated user context — not derived from or influenced by model output or user-provided text?
- Are filters passed as hard parameters to the vector store backend — not as soft instructions in the query string?
- Do document loaders and splitters preserve `sensitivity`, `tenant_id`, and `doc_class` metadata through chunking?

### Action

- **Construct filters from the session context, not from the query.** The filter must come from `current_user.tenant_id`, `current_user.authorized_doc_classes` — not from anything in the user's message or the model's output.

```python
# Wrong — filter influenced by user input or model
retriever = vectorstore.as_retriever(
    search_kwargs={"filter": {"tenant": query_derived_tenant}}
)

# Right — filter from authenticated session context only
retriever = vectorstore.as_retriever(
    search_kwargs={
        "k": 5,
        "score_threshold": 0.75,
        "filter": {
            "tenant_id": {"$eq": current_user.tenant_id},
            "doc_class": {"$in": current_user.authorized_doc_classes},
            "sensitivity": {"$lte": current_user.clearance_level},
        }
    }
)
```

- **Mask PII before `combine_documents`.** Apply a PII masking function to each `Document.page_content` before it enters the `combine_documents` or equivalent synthesis step. Masking after synthesis is too late — the PII was already in the prompt.
- **Treat LangSmith traces and debugging views as sensitive stores.** Store document IDs and policy outcomes — not raw document content or raw prompt text — in observability outputs by default.

### Minimum Deliverable Per Review

- [ ] LangChain RAG dataflow: loader → splitter → embedder → vector store → retriever → reranker → chain → callback → output
- [ ] Citation verification path: where is it implemented, what is checked, and what is the fallback on failure?
- [ ] Metadata filter construction: source (session context), enforcement point (server-side vs. application-side)
- [ ] Memory and `chat_history` interaction: can either override retrieval as the primary answer source?
- [ ] Callback and trace sensitivity: what fields are logged, what is redacted?

## Quick Win

**Audit your retriever's filter construction.** Open the code that builds your `VectorStoreRetriever` search kwargs. Confirm the `filter` dict is constructed entirely from the authenticated session context — not from user input, not from model output, not from query parameters. If any part of the filter can be influenced by untrusted input, your retrieval scope boundary does not exist.

## References

- Base RAG control model → [rag-security/SKILL.md](../rag-security/SKILL.md)
- Leakage deep-dives → [data-leakage-prevention/SKILL.md](../data-leakage-prevention/SKILL.md)
- Framework notes → [languages-and-frameworks.md](../../references/languages-and-frameworks.md)
