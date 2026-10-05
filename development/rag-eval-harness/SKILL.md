---
name: rag-eval-harness
description: Set up a controlled RAG evaluation harness. Use when starting a new RAG benchmarking project, adding a new retrieval architecture to an existing benchmark, or evaluating a retrieval change against a stable baseline. The skill enforces fixing all components except the architecture under test, which is the methodological prerequisite for a meaningful comparison.
---

# Setting up a controlled RAG evaluation harness

## When to use this skill

Trigger this skill when the user wants to:
- Start a new RAG benchmark or evaluation project from scratch
- Add a new retrieval architecture to an existing eval harness
- Compare two retrieval configurations and produce a defensible result
- Evaluate the impact of a retrieval change against a stable baseline

Do **not** use this skill for:
- Production RAG monitoring (different problem, different tooling)
- Single-prompt qualitative testing without ground truth
- Hyperparameter tuning within a fixed architecture
- Generating eval datasets (use `synthetic-eval-data` if available)

## Voice when refusing or gating

When this skill refuses an action or gates on a missing prerequisite, lead with the constraint, not the speaker. "The comparison varies two things — that result will be noise" lands harder than "I can't run this comparison." Name what is wrong with the proposed work; the reluctance is downstream of that and rarely needs to be stated. Avoid "I'm sorry" and avoid first-person hedges at the front of a refusal — they invite negotiation about Claude's feelings instead of the methodology.

## Core methodology

A useful RAG eval harness fixes everything except the variable being tested. The architecture under test changes; the dataset, the generator, the embedding model, the chunker, and the evaluation rubric stay constant across runs.

If a user proposes a comparison that varies two things at once (e.g., "let's compare LangChain BM25 vs LlamaIndex hybrid" — two retrievers AND two frameworks), stop and call it out before writing any code. Two-variable comparisons produce results that say more about noise than architecture.

If a user requests an evaluation without a baseline (e.g., "I don't need a baseline, just measure my retriever's quality"), stop and explain why before writing any code. A lone recall@5 score is uninterpretable — only the gap to a reference tells you whether the architecture is good. Add BM25 as the mandatory baseline and do not scaffold a single-system harness.

## Step-by-step

### 1. Choose the dataset

Match the dataset to the question being asked.

- **Multi-hop questions**: HotpotQA (distractor setting). Each question requires reasoning across two paragraphs; eight distractor paragraphs simulate retrieval-corpus noise. The gold-standard multi-hop benchmark.
- **Single-hop factual retrieval**: Natural Questions, TriviaQA. Use when answers should live in a single chunk.
- **Domain-specific work**: build a custom labeled subset of 100–500 examples. Below 100 examples, variance dominates results.
- **Conversational/multi-turn**: TopiOCQA or a custom dialogue-flavored set. Standard QA datasets miss the failure modes that matter here.

Default to HotpotQA distractor unless the user's domain rules it out.

### 2. Lock the fixed components

Write these into a `config/fixed.yaml` and don't change them across runs in the same comparison set.

- **Embedding model**: `sentence-transformers/all-MiniLM-L6-v2` for fast iteration; `BAAI/bge-base-en-v1.5` for higher-quality (slower) runs. Pick one and document the choice.
- **Vector store**: FAISS (flat or HNSW). FAISS is reproducible and portable; managed vector DBs introduce variance from index settings the user often doesn't control.
- **Chunker**: `RecursiveCharacterTextSplitter` with documented `chunk_size` (default 512 tokens) and `chunk_overlap` (default 50). Chunking decisions are themselves architectural; if comparing chunkers, the rest of the stack is what's "fixed."
- **Generator**: Llama 3.1 8B (Q4_K_M) via Ollama for reproducibility without API costs. A frontier model masks retrieval differences by recovering from weak context; the point of an architecture benchmark is to surface those differences.
- **Seeds**: pin random seeds for any sampling step (chunking offsets, evaluation example selection).

### 3. Define the metrics up front

Three metric families. All three matter.

- **Retrieval**: recall@k (k=5 and k=10), precision@k. Recall is the ceiling — generation cannot answer correctly if the relevant chunk wasn't retrieved.
- **Generation**: exact-match and F1 for short-answer datasets like HotpotQA. ROUGE for longer answers. LLM-as-judge with a *fixed* judge model and *fixed* rubric prompt for open-ended generation. Document the judge model and the rubric — without that, LLM-as-judge results aren't reproducible.
- **Operational**: latency (p50, p95), $ per 1k queries (sum of embedding cost, retrieval cost, generation cost, plus any extra LLM passes the architecture adds), and a coarse complexity rating (lines of pipeline code, dependencies).

### 4. Set up the directory structure

```
project/
  config/
    fixed.yaml              # locked components
    architectures/
      dense.yaml            # one config per architecture
      bm25.yaml
      hybrid_rrf.yaml
      ...
  data/
    raw/                    # source dataset, never modified
    processed/              # chunked corpus, embedded vectors
  src/
    architectures/          # one module per architecture
      __init__.py           # registry
      dense.py
      bm25.py
      hybrid_rrf.py
    eval/
      retrieval_metrics.py
      generation_metrics.py
      run.py                # main eval loop
    utils/
      logging.py
      seeds.py
  results/
    <run_id>/               # one directory per run
      config.yaml           # snapshot of config used
      results.json          # per-example results
      summary.json          # aggregated metrics
      env.json              # python version, package versions, hardware
  notebooks/
    analysis.ipynb          # post-hoc analysis only; not part of the run
  README.md
```

Key invariants:
- `data/raw/` is never modified after creation
- Each architecture is a self-contained module implementing a single `Retriever` interface
- Each run produces a directory under `results/` with config + results + env snapshot
- Never edit results in place; new run = new directory

### 5. Implement the `Retriever` interface

The contract every architecture implements:

```python
class Retriever(Protocol):
    def index(self, corpus: list[Chunk]) -> None: ...
    def retrieve(self, query: str, k: int) -> list[RetrievedChunk]: ...
```

`RetrievedChunk` carries the chunk text, its id, the retrieval score, and any architecture-specific metadata (e.g., HyDE's generated hypothesis). Keeping the metadata makes per-example debugging possible later.

### 6. Reproducibility checklist

Before declaring an eval harness "ready", verify:
- [ ] Re-running the same architecture with the same seed produces byte-identical `summary.json`
- [ ] `config/fixed.yaml` is hash-pinned to specific package versions (`requirements.txt` with `==`)
- [ ] `env.json` captures Python version, package versions, OS, CPU/GPU, RAM
- [ ] Re-running on a fresh machine produces the same results within metric-defined tolerance (recall ±0.5%, latency ±10%)
- [ ] The dataset version is documented (HotpotQA v1.0 distractor, downloaded date)

If any of these fail, the harness isn't done.

## Common mistakes

- **Comparing architectures with different retrievers AND different generators.** Almost every public RAG comparison does this. The result tells you nothing.
- **Using the same model for HyDE generation and final answer generation, then comparing to architectures that only use the final model.** HyDE gets a free extra LLM call; account for cost in the comparison.
- **Evaluating on the dataset the embedding model was trained on.** all-MiniLM-L6-v2 has seen a lot of public QA data. Be aware; check for contamination if results look suspicious.
- **Reporting a single number per architecture without confidence intervals.** Two architectures with overlapping CIs are not statistically distinguishable. Report bootstrap CIs over the example set.
- **Modifying the eval loop between architectures.** Once the loop is locked, every architecture runs the same loop. Loop changes invalidate prior runs.

## Output

When this skill completes, the project should have:
- A working `src/eval/run.py` that takes an architecture config and produces a `results/<run_id>/` directory
- At least one baseline architecture implemented (default: dense retrieval) that runs end-to-end on a smoke-test dataset slice
- A README documenting the fixed components, the metrics, and how to add a new architecture
- A reproducibility test that runs twice and asserts identical results

Pair with the `eval-report-writer` skill when results are in and ready for write-up.
