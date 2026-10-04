---
name: pageindex
description: Vectorless, reasoning-based RAG for long professional documents (financial reports, regulatory filings, legal contracts, technical manuals, medical literature, textbooks). Replaces chunk-embed-vector-search with a hierarchical tree index that an LLM reasons through, so answers trace back to exact pages. Use when similarity search keeps returning plausible-but-wrong passages from a long PDF, when you need page-level citations, or when scoping a document-QA build and deciding between vector RAG and tree-index RAG. SDK is `pip install -U pageindex` (MIT).
---

# PageIndex — Vectorless, Reasoning-Based RAG

**One sentence:** instead of embedding chunks and ranking by cosine similarity, PageIndex builds a table-of-contents-style *tree* for each document and lets an LLM walk that tree — the way a human expert turns to the right chapter — then answers with references to the exact nodes it read.

## Mechanism (two steps)

1. **Index** — generate a hierarchical tree for each document. Upstream says the tree *structure* is extracted from the document layout without an LLM; the index model only summarises/refines nodes, so a basic model is enough.
2. **Retrieve** — an LLM agentically searches that tree. No vector DB, no chunking, retrieval sees conversation history and domain context, not just a query embedding.

| | Vector RAG | PageIndex |
|---|---|---|
| Index | vector index over chunks | tree index over document structure |
| Retrieval | semantic *similarity* | LLM *reasoning* over the tree |
| Result | opaque ranking | traceable to explicit page/node references |
| Context | query embedding only | full conversation + domain context |

## Quickstart (local mode, from the upstream README)

```bash
pip install -U pageindex
```
```python
import os
from pageindex import PageIndexClient

os.environ["OPENAI_API_KEY"] = "<your key>"        # never commit; use env/secret store
client = PageIndexClient(
    index="gpt-5.6-luna",   # model that builds the tree  — a basic model is sufficient
    chat="gpt-5.6-sol",     # model that searches the tree — use the best you can afford
)
doc_id = client.submit_document("report.pdf")["doc_id"]
print(client.chat("What was the 2023 operating margin?", doc_id=doc_id))
```

Model names above are copied from the upstream README as of 2026-09-30 — confirm they exist on *your* provider before running; substitute any compatible model.

## Local vs Cloud

| | Local (open source) | Cloud |
|---|---|---|
| Handles | text-based PDFs | text-based, scanned, image-rich |
| Indexing | on your machine | managed |
| Storage | local directory | cloud |
| Citations | page-level | block-level |
| OCR / image understanding | no | yes |
| MCP server | no | yes (needs a PageIndex API key) |

**Consequence for this repo:** scanned regulatory PDFs (typical for tender documents, older HTA/market-access dossiers) are the *weak* case locally — OCR first (see `ocrmypdf` in the Batch 97 self-hosted list) or use Cloud.

## Vendor-reported numbers (treat as claims, not facts)

- ~$0.001 per page to index locally with the index model named in the README (≈ a little over $1 for a 1,000-page textbook); 9–1,098-page benchmark PDFs indexed in roughly 13 s – 4.5 min.
- 98.7 % on FinanceBench (Mafin 2.5 write-up) vs ~50 % for a vector-RAG baseline. The comparison baseline is the vendor's; a well-tuned hybrid (BM25 + dense + reranker) may close part of that gap.
- Own benchmark: `VectifyAI/PageIndex-OSS-Benchmark`, 62 lookup questions — read before trusting for your domain.

## When to use it vs the other RAG skills here

| Situation | Use |
|---|---|
| One long structured document, need page-cited answers | **`pageindex`** |
| Large mixed corpus of short documents, need semantic recall | `rag-implementation` / `rag-pipeline-architecture` (+ `hybrid-search-implementation`) |
| Deciding build order for a RAG product | `docs/procedures/rag-build-order.md` |
| Millions of documents | PageIndex *File System* (Cloud-only, per upstream) — not covered by the OSS repo |

## Guardrails

- It sends document text to your chosen LLM provider. Do not index confidential, patient or client documents through a third-party API without a data-processing basis; use a local/on-prem model or the vendor's VPC option.
- Tree quality depends on layout: flat OCR text, slide decks and spreadsheets give weak trees.
- Always spot-check 5 answers against the cited pages before relying on a corpus (see `/pageindex-ask`).
