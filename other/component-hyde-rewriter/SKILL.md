---
name: component-hyde-rewriter
description: Generate exactly one hypothetical answer-like document from the original query with single-sample HyDE (N=1) for zero-shot semantic retrieval. Use before a vector retriever when query-document wording mismatch is likely; never treat the generated text as factual evidence.
---

# HyDE Rewriter Component

Provide the `rewriter` capability for an Agentic RAG slot.

## Interface

Input `RewriteRequest`:

- `query`: original user query
- optional `temperature`: generation temperature, default `0.0`
- optional `max_tokens`: maximum hypothetical-document tokens, default `8192`

Output `RewriteResult`:

- `rewritten_query`: exactly one hypothetical answer-like document used as the retrieval query

## Execution

Run `scripts/component.py:run(inputs, context)`.

Implement the single-sample HyDE variant (`N=1`). Call the frozen Executor Model supplied through `context.call_model()` exactly once and generate one concise hypothetical document. Do not generate multiple hypotheses or perform embedding aggregation in this Component.

Use the generated text only as the input to a semantic Vector Retriever. Keep the original query for reranking and final answer generation.

The hypothetical document may contain false details. Never add it to the retrieved evidence, never return it as a real document, and never use it directly as the final answer.

Prefer this Component when the original query is short, abstract, or phrased differently from the corpus. Do not select it as the default preprocessing step for exact keyword, identifier, or entity-name retrieval.
