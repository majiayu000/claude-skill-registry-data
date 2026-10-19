---
name: rag-evaluation
description: Evaluate retrieval-augmented generation systems component by component - build a query set with labelled relevant passages, compute retrieval metrics (recall@k, precision@k, hit rate, MRR, nDCG@k), then score generation for groundedness (faithfulness to retrieved context), answer correctness, citation accuracy and appropriate abstention, and diagnose whether failures come from chunking, embeddings, retrieval, reranking, context assembly or the generator. Includes a tested stdlib script for retrieval metrics and notes on access-control and prompt-injection tests. Use when building, tuning or regression-testing a RAG pipeline, comparing chunkers, embedding models, rerankers or prompts, or when users report wrong or unsupported answers. Not for generic LLM benchmarking (llm-evaluation), dataset cleaning (dataset-quality), search relevance in Elasticsearch itself (elasticsearch-search), or serving the models (local-llm-deployment).
compatibility: Python 3.10+. The bundled script uses only the standard library. LLM-judged groundedness needs a judge model; sending corpus text or user queries to a hosted judge requires the user's authorization.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "rag, retrieval, evaluation, ndcg, recall, groundedness, faithfulness, chunking"
  topics: "machine-learning, search, quality"
---

# RAG Evaluation

A RAG answer can be wrong for four different reasons: the right passage was never indexed or was chunked badly, retrieval did not surface it, the context was assembled badly, or the generator ignored or contradicted what it was given. One end-to-end "answer quality" score cannot tell you which. Evaluate retrieval and generation separately, then end to end.

## Scope and boundaries

- This skill: query sets, retrieval metrics, groundedness and answer scoring, failure attribution, regression testing of RAG.
- `llm-evaluation`: general eval design, judge calibration, statistics (apply those principles here; this skill does not repeat them). `dataset-quality`: clean the corpus/query set, leakage. `elasticsearch-search`: tuning the search engine, analyzers, BM25/kNN. `redis-caching`: semantic caching. `local-llm-deployment`: hosting the embedding or generation model.

## Non-negotiable rules

1. **Evaluate on queries that look like real user queries**, not only on LLM-generated questions that copy the passage's wording (these inflate lexical and embedding retrieval scores). Mix real or human-written queries with synthetic ones and report them separately.
2. **Label relevance at the passage/chunk-independent level** (document id plus span or section) so changing the chunker does not invalidate the gold labels. Chunk-id gold labels break every time chunking changes.
3. **Separate retrieval metrics from generation metrics** and report both, with confidence intervals (see `llm-evaluation`).
4. **Never send private corpus text or user queries to a third-party judge or embedding API without authorization.** State what leaves the machine.
5. **Include security tests as first-class cases**: documents the user must not see (access-control leakage), and retrieved text that contains instructions (indirect prompt injection). A RAG pipeline that retrieves across tenants or obeys instructions in documents fails regardless of accuracy.
6. **No fabricated numbers.** Label scenarios as designed vs executed.

## Workflow

### 1. Define the answerable space
List question types: single-fact lookup, multi-hop (needs several passages), aggregation/comparison, procedural, unanswerable (corpus has no answer), ambiguous, and out-of-scope. Decide the expected behaviour for each, especially refusal or "not in the documents".

### 2. Build the query set
- 100+ queries is a practical floor to see differences of a few points; more for slices. Stratify by type above.
- Each query: text, gold relevant documents/sections (graded 0-3 if you will use nDCG), a reference answer or key facts, and an `answerable` flag.
- Synthetic generation (LLM writes questions from passages) is useful for coverage but biased toward the passage vocabulary: filter for answerability, have a human review a sample, and keep a human-written subset as the headline.
- Keep a frozen test portion; do not tune chunking and prompts on it.

### 3. Retrieval metrics
Compute per query, then macro-average (queries with no relevant document are excluded or evaluated separately as unanswerable).

| Metric | Definition (k = cutoff) | Reads as |
|---|---|---|
| Recall@k | relevant docs in top k / all relevant docs | Did we get what is needed into the context? Primary for RAG, since the generator can ignore extras but cannot invent missing evidence |
| Precision@k | distinct relevant in top k / k | Noise in the context |
| Hit rate@k | 1 if any relevant in top k | Coarse success |
| MRR | mean of 1/rank of the first relevant doc | How early the first good hit appears |
| nDCG@k | DCG@k / ideal DCG@k with DCG = sum rel_i / log2(i+1) | Graded relevance and rank order; bounded 0..1 |
| MAP | mean over queries of average precision | Whole-ranking quality for multi-relevant queries (not in bundled script) |

nDCG has gain-formula variants (linear rel_i versus 2^rel_i - 1); state which one, since scores differ between libraries. The bundled script uses linear gain with log2(i+1) discounts and 1-based positions. For RAG choose k to match what you will actually pass to the generator (context budget), and also report recall at the retrieval stage before reranking to locate the loss.

```bash
python3 -I scripts/retrieval_metrics.py runs.jsonl --k 5 10
```
Input line: `{"query_id": "q1", "relevant": {"d1": 1, "d7": 2}, "retrieved": ["d3", "d1", "d9"]}`. Verified on a small hand-computed fixture (recall@3 0.75, nDCG@3 0.6199 for the two-query example in references/metrics-notes.md). See [scripts/retrieval_metrics.py](scripts/retrieval_metrics.py).

### 4. Generation metrics
Score on the **retrieved** context actually given to the model, and separately with gold context to isolate the generator.

- **Groundedness / faithfulness**: is every claim in the answer supported by the provided context? Procedure: split the answer into atomic claims, check each against the context (NLI model or LLM judge with a rubric), score = supported / total. Unsupported but true claims still count as ungrounded: they come from model memory and will fail when the corpus differs.
- **Answer correctness**: matches the reference facts (key-fact recall, exact match for short answers, or calibrated judge).
- **Answer relevance / completeness**: does it address the question and include required parts.
- **Citation accuracy**: do cited sources exist, are they in the retrieved set, and do they actually support the attached claim? Check programmatically that cited ids were retrieved, then judge support.
- **Abstention**: for unanswerable queries, does the system say it does not know instead of guessing? Report abstention precision and recall (it should not refuse answerable questions).
- Operational: latency per stage, token cost, context length used.

Frameworks such as Ragas, TruLens or DeepEval package these metrics with LLM judges; their metric names and definitions change between versions, so read the definition in the installed version, pin it, and calibrate the judge as in `llm-evaluation` instead of trusting a number by name.

### 5. Attribute failures
For each failed query, walk the pipeline in order and record the first broken stage:

| Check | If it fails |
|---|---|
| Is the answer in the corpus at all (ingestion, parsing, OCR, table extraction)? | Fix ingestion before anything else |
| Is the gold passage in a chunk intact (not split across a boundary or stripped of heading)? | Chunking: size, overlap, structure-aware splits, contextual headers |
| Retrieved in top-N candidates? | Embedding model, query rewriting, hybrid (lexical + vector) retrieval, metadata filters |
| In final top-k after reranking? | Reranker, k cutoff, diversity |
| Present in the prompt (not truncated, not buried)? | Context assembly, ordering, budget |
| Generator answered from it correctly (gold-context run)? | Prompt, model, instruction following |

Aggregate the first-failure stage counts; fix the largest bucket and re-measure. Change one component at a time; keep an experiment table (config, recall@k, nDCG, groundedness, correctness, latency).

### 6. Security and robustness cases
- **Access control**: queries as user A that would match only documents of user B must retrieve nothing from B; assert at the retrieval layer (filters applied before ranking), not just in the answer text.
- **Indirect prompt injection**: plant a document containing "ignore previous instructions and ..." in a test corpus; the system must treat it as data. Failure is a pass/fail case in the regression suite.
- **Sensitive data**: confirm PII or secrets in documents are not surfaced to users without entitlement.
- **Stale or conflicting sources**: documents with different versions; check the answer cites the current one.

### 7. Regression
Run retrieval metrics on every change to chunking, embeddings, index settings or reranker (cheap, deterministic given fixed index). Run the generation suite on prompt/model changes. Gate on recall@k and groundedness floors plus the security cases; investigate drops by slice.

## Worked example

A support-docs assistant answers incorrectly on 22 of 100 test queries. Retrieval run with k=5: recall@5 = 0.71, nDCG@5 = 0.58, MRR = 0.64. Failure attribution over the 22: 3 not in corpus (PDF tables dropped by the parser), 9 relevant passage not in top-50 candidates (queries use product nicknames; docs use official names), 4 retrieved in top-50 but cut by the reranker at k=5, 6 generator errors with gold context.
Action in order of size: add synonym/alias expansion and hybrid retrieval (9), then fix the table parsing (3), raise rerank k to 8 (4); revisit the prompt last (6). After the first change recall@5 = 0.80 (illustrative figures, not an executed run). Report with intervals and re-run the security suite.

## Anti-patterns

- One end-to-end score with no component breakdown.
- Gold labels tied to chunk ids; evaluating only on synthetic questions that echo the passage.
- Optimising precision when the failure is missing evidence (recall).
- Judge-only groundedness without human calibration; counting "true but not in context" as grounded.
- Tuning chunk size on the same queries you report.
- Ignoring unanswerable queries, so hallucination under missing evidence is never measured.
- Skipping ACL and injection tests because the demo corpus is public.
- Comparing nDCG across tools without checking the gain formula and tie handling.

## Verification checklist

- [ ] Query set stratified, with answerable flag; human-written subset reported separately
- [ ] Gold labels at document/section level, chunker-independent
- [ ] Recall@k, nDCG@k, MRR reported with k matching the generator context; gain formula stated
- [ ] Groundedness, correctness, citation accuracy and abstention scored; judge calibrated
- [ ] Failures attributed to a pipeline stage; one change per experiment
- [ ] ACL leakage and indirect injection tests included
- [ ] No corpus or query text sent to third parties without authorization
- [ ] Frozen test portion kept; results labelled executed vs designed

## References

- [scripts/retrieval_metrics.py](scripts/retrieval_metrics.py)
- [references/metrics-notes.md](references/metrics-notes.md) - worked metric arithmetic and variants
- [references/scenarios.md](references/scenarios.md)
- [references/sources.md](references/sources.md)
