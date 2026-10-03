---
name: retrieval-design
description: Design retrieval for AI features around corpus quality, permissions, chunking, indexing, query strategy, ranking, context assembly, provenance, and retrieval-specific evaluation.
---
# Retrieval Design

Use when a model or agent needs information from documents, code, knowledge bases, records, or other corpora that cannot be assumed to exist reliably in model context.

## Procedure
1. Start from the decision the model must make and the evidence needed to make it. Do not add retrieval merely because a vector database is available.
2. Audit the corpus: ownership, freshness, duplication, authority, access control, sensitive content, document structure, and how updates or deletions propagate into the index.
3. Choose the retrieval unit around meaning and downstream use. Preserve headings, identifiers, timestamps, source metadata, relationships, and other context needed to understand or filter a result. Avoid arbitrary chunk sizes when document structure provides a better boundary.
4. Select indexing and search methods based on the corpus and query distribution. Consider lexical, semantic/vector, structured filters, graph/relationship lookup, or hybrid retrieval rather than assuming embeddings alone are best.
5. Define query construction. Decide whether the user query can be used directly or benefits from normalization, decomposition, expansion, entity extraction, or multiple searches. Preserve the original intent and avoid query rewriting that invents facts.
6. Retrieve enough candidates to protect recall, then rank or rerank for relevance where needed. Apply permission and tenant filters before material can enter model context.
7. Assemble context deliberately: deduplicate, preserve source boundaries and provenance, prioritize authoritative/current evidence, respect context limits, and keep untrusted retrieved text distinguishable from system instructions.
8. Decide what the model should do when evidence conflicts, is stale, is insufficient, or retrieval returns nothing. Citation or source attribution should trace claims back to the actual retrieved evidence when the product requires it.
9. Evaluate retrieval separately from final answer quality. Measure whether relevant evidence is found, ranked highly enough, permission-safe, fresh enough, and included intact before blaming the generator for missing context.
10. Evaluate the assembled system on representative questions, including ambiguous queries, rare facts, conflicting sources, stale documents, permission boundaries, prompt-injection-like content inside documents, and no-answer cases.

## Decision rules
- Retrieval quality begins with corpus quality; indexing cannot repair an untrustworthy source of truth.
- Do not expose material the caller is not authorized to retrieve, even if the model could theoretically ignore it.
- More chunks are not automatically more context. Irrelevant material can reduce answer quality and increase cost.
- Preserve provenance through every transformation so an answer can be audited back to source evidence.
- If deterministic database lookup or structured querying solves the task more reliably, use it instead of semantic retrieval.

## Quality gate
Retrieval is ready when relevant authoritative evidence is found reliably, permissions and freshness are enforced, context assembly preserves provenance and instruction boundaries, no-answer behavior is defined, and retrieval-specific evaluation demonstrates acceptable recall and ranking on the real task distribution.