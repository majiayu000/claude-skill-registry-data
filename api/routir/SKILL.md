---
name: routir
description: Use RoutIR — call a running endpoint with the client, stand up a local server that mixes locally-hosted services with services proxied from a remote master server, and extend RoutIR with new bi-encoders, rerankers, and document collections by writing a small config (and optionally one Python file referenced via `file_imports`). No checkout of the routir source is required.
---

# RoutIR skill

RoutIR is an HTTP/gRPC service that hosts retrieval engines (dense, sparse,
rerankers, fusion, query expanders) behind a uniform API and composes them
into multi-stage pipelines with a small DSL. This skill covers the five
things you actually do with it:

1. Call a running RoutIR endpoint with the client.
2. Stand up your own RoutIR server, optionally importing services from a
   master server so users can pipeline local + remote engines together.
3. Wrap a bi-encoder retrieval index.
4. Wrap a cross-encoder reranker.
5. Serve document collections (single- or multi-view).

**Run everything through `uvx`.** This project forbids bare `pip`,
`python`, `pytest`, `ruff`. Every command below uses `uvx` so the deps land
in a throwaway venv instead of your conda environment.

The full reference for extending RoutIR with Python lives in
[`examples/CLAUDE.md`](examples/CLAUDE.md); pipeline / DSL / config reference
in the project [`CLAUDE.md`](CLAUDE.md). This skill is the operational
overview — read those when you need depth.

---

## 1. Use the client (and the pipeline DSL)

`routir.client.Client` is the sync facade (auto-uses gRPC when the server
advertises it, falls back to REST). `AsyncClient` is the async version with
the same surface.

```python
from routir.client import Client

with Client(endpoint="http://compute01:5000", api_key="…optional…") as c:
    print(c.avail())                          # what's available
    print(c.transport)                        # "grpc" or "rest"

    # search a single hosted index
    r = c.search(service="qwen3-neuclir", query="…", limit=20)
    # r["scores"] -> {doc_id: float}

    # score a list of passages against a query
    r = c.score(service="my-reranker", query="…", passages=["p1", "p2", …])
    # r["scores"] -> [float, float, …]   (one per passage)

    # fetch document content
    r = c.content(collection="neuclir", id="doc-id-123", view="asr")
    # r["text"] or r["bytes"]

    # run a composed pipeline (the main entry point)
    r = c.pipeline(
        pipeline="{dense%1000, bm25%1000}RRF%100 >> rerank@asr%20",
        query="…",
        collection="neuclir",                 # needed when a stage reranks
        runtime_kwargs={"rerank": {"some_engine_kwarg": 0.5}},  # optional
    )
```

**Endpoint scheme rules:** `http(s)://…` → REST; `grpc(s)://…` → gRPC;
bare `host:port` is treated as `http://` and may auto-upgrade to gRPC if
the server advertises `grpc_port` via `/avail`. Pass
`transport="rest"` to force REST.

### Pipeline DSL — quick reference

| DSL form                                | Meaning                                                                       |
| --------------------------------------- | ----------------------------------------------------------------------------- |
| `svc%N`                                 | Call `svc`, keep top *N*.                                                     |
| `A%1000 >> B%20`                        | Sequential: A retrieves 1000, B reranks down to 20. B gets role `rerank`.     |
| `{A%K, B%K}Merger%N`                    | Parallel: A and B run concurrently; `Merger.fuse_batch` fuses to top *N*.     |
| `Expander{A%K, B%K}Merger%N`            | Expander makes sub-queries; each runs A and B in parallel; all fused.         |
| `svc[alias]%N`                          | Name a stage so `runtime_kwargs` can target it by alias.                      |
| `svc@view%N`                            | Pick a named view of the collection at rerank time (multi-modal).             |

**Built-in mergers:** `RRF` (reciprocal rank fusion) and `ScoreFusion` are
always available. You only need to write your own fusion engine if you need
something neither covers.

**Aliases:** `pipeline_aliases` in the server config let you give a long
pipeline a short name (`"ragtime2": "{zho%100, rus%100, …}ScoreFusion"`);
the alias is then usable everywhere a service name is. The call-site `%N`
re-caps the alias's outer-most stage.

**Bound the result set.** `/pipeline` ignores a top-level `limit`; the
result-set size is whatever the final `%N` produced. If your pipeline has
no `%N`, you'll get the full inner result.

`scripts/query.py` is the canonical batch-query script that writes the
[JSONL run format documented in `CLAUDE.md`](CLAUDE.md#search-results-output-format).
Copy it when scripting evaluations.

---

## 2. Stand up a local server (and import a master server)

Minimal `my-config.json`:

```json
{
    "services": [
        { "name": "my-bm25", "engine": "PyseriniBM25",
          "config": {"index_path": "/path/to/bm25-index"},
          "cache": 1024, "cache_ttl": 600,
          "batch_size": 16, "max_wait_time": 0.05 }
    ],
    "collections": [
        { "name": "my-corpus", "doc_path": "/data/corpus.jsonl" }
    ],
    "server_imports": [
        "http://master-host:5000"
    ],
    "file_imports": [
        "./my_extension.py"
    ]
}
```

**`server_imports` is the master-import mechanism.** At startup the local
server queries `/avail` on every entry and registers a `Relay`-backed local
proxy for every remote search / score / content service it doesn't already
host. After that, your users can write pipelines that freely mix local and
remote services as if they were all on one box:

```text
{my-bm25%1000, remote-qwen3%1000}RRF%100 >> remote-cross-encoder%20
```

Notes that bite people:

- **Local services win on name collision.** Remote services with a name
  already registered locally are skipped, not overridden.
- **Each entry can be a dict** with `endpoint`, `grpc_endpoint`, `api_key`,
  `transport`, etc., not just a bare URL — handy when the master is gRPC.
- **Cache relayed content.** Reranking against a remote collection
  re-fetches every doc per query without a cache. Set
  `"relay_content_cache": 4096` (and `relay_content_cache_ttl`) at the
  top level of the config, or wire a Redis URL.

**Serve it:**

```bash
# REST only, port 5000
uvx --with "routir[dense] @ ." \
    routir my-config.json --port 5000

# REST + gRPC; add --with for every runtime dep your engines need
uvx --with transformers --with torch --with "routir[dense,grpc] @ ." \
    routir my-config.json --port 5000 --grpc --grpc-port 50051

# With auth (prefer env over --api_key; CLI args show up in ps)
ROUTIR_API_KEY=sekret uvx --with "routir @ ." routir my-config.json --port 5000
```

**Verify it works**:

```bash
curl http://localhost:5000/avail        # lists search/score/fuse/collection
curl http://localhost:5000/ping         # always unauthenticated; for liveness
```

`/avail` is also what `server_imports` uses for discovery — if your
service doesn't appear there, no one else will see it either.

**Per-service knobs in `services[]`** that you'll routinely tune:

| key                | what it does                                                                                       |
| ------------------ | -------------------------------------------------------------------------------------------------- |
| `cache`            | LRU capacity for this service's results. `-1` (default) disables.                                  |
| `cache_ttl`        | TTL in seconds. Applies to LRU and Redis.                                                          |
| `cache_key_fields` | Request fields that go into the cache key. Default `["query", "limit"]`; add `"subset"` etc. when they affect results. |
| `cache_redis_url`  | Use Redis instead of in-memory LRU.                                                                |
| `batch_size`       | Max requests batched into one engine call. Default 32.                                             |
| `max_wait_time`    | Max seconds to wait for a batch to fill. Default 0.05; raise for throughput, lower for latency.   |
| `scoring_disabled` | Set to `true` to refuse to register `/score` for an engine that *can* score, when you only want search. |

---

## 3. Wrap a bi-encoder with an index

**Default path: write zero Python.** RoutIR ships `Qwen3` and
`SentenceTransformerEngine` and they cover the majority of dense models
purely through config. Reach for a custom engine only when neither fits.

### 3a. Zero-code: external query encoder via OpenAI-compatible API (preferred)

This is the right answer almost always — it keeps the query encoder on its
own GPU/process (vLLM, llama.cpp, sglang, …), so RoutIR doesn't have to
share VRAM with it and you can scale the encoder independently.

Run your query encoder as an OpenAI-compatible `/v1/embeddings` server
(vLLM, llama.cpp, sglang, TEI — any of them) and point RoutIR at it:

```json
{
    "services": [
        {
            "name": "qwen3-neuclir",
            "engine": "Qwen3",
            "cache": 1024, "cache_ttl": 600,
            "batch_size": 32, "max_wait_time": 0.05,
            "config": {
                "index_path": "/path/to/faiss-index",
                "embedding_base_url": "http://gpu-host:8000/v1/",
                "embedding_model_name": "Qwen/Qwen3-Embedding-8B",
                "api_key": "…or set OPENAI_API_KEY env…",
                "k_scale": 5
            }
        }
    ]
}
```

Likewise `SentenceTransformerEngine` covers ME5-Instruct, ArcticEmbed, BGE-M3,
Jina-v3, etc. by setting `embedding_model_name`, `instruction`,
`prompt_name_query`, `task_query`, `normalize_embeddings`. The full key list
is on the class in `src/routir/models/st.py`.

**`index_path`** is a directory with `index.faiss` + `index.ids` (one doc id
per line, in the same order as FAISS vectors). The `hfds:<org/repo>` prefix
auto-downloads from Hugging Face Datasets at startup
(e.g. `"index_path": "hfds:routir/neuclir-qwen3-8b-faiss-PQ2048x4fs"`).

### 3b. Run the query encoder in-process (less ideal)

If you must (e.g. small model, no spare encoder host, sharing VRAM is fine),
either drop `embedding_base_url` from the configs above — both engines fall
back to local `transformers`/`sentence-transformers` — or write a tiny
custom engine if neither fits. The cost is real: the query encoder now
contends with everything else this RoutIR process is doing.

If you do need to write your own, use `file_imports` to ship one `.py`
without touching the routir checkout:

```python
# my_extension.py
from typing import Dict, List
import faiss, numpy as np
from routir.models.abstract import Engine

class MyBiencoderEngine(Engine):
    def __init__(self, name=None, config=None, **kwargs):
        super().__init__(name, config, **kwargs)
        self.encoder = load_my_query_encoder(config["model"])
        self.index = faiss.read_index(f"{config['index_path']}/index.faiss")
        with open(f"{config['index_path']}/index.ids") as f:
            self.doc_ids = [ln.strip() for ln in f]

    async def search_batch(self, queries: List[str], limit=1000, **kwargs) -> List[Dict[str, float]]:
        if isinstance(limit, int):
            limit = [limit] * len(queries)
        q_emb = self.encoder.encode(queries)                    # (N, d)
        scores, idx = self.index.search(q_emb.astype(np.float32),
                                        k=max(limit) * 2)
        return [
            dict(list(zip([self.doc_ids[i] for i in idx[qi]], scores[qi].tolist()))[:k])
            for qi, k in enumerate(limit)
        ]
```

```json
{
    "file_imports": ["./my_extension.py"],
    "services": [{
        "name": "my-dense",
        "engine": "MyBiencoderEngine",
        "config": {"model": "org/name", "index_path": "/path/to/index"},
        "batch_size": 16, "max_wait_time": 0.05
    }]
}
```

The class **name** in `engine:` must match the Python class name exactly —
that's how lookup works. There is no registration boilerplate.

If your engine can also score query-passage pairs cheaply (true for dense
models — it's just `q @ p.T`), implement `score_batch` on the same class
too and a `/score` endpoint registers automatically. See `Qwen3.score_batch`
for the canonical implementation.

**Building the FAISS index** is out of scope here — produce
`index.faiss` + `index.ids` any way you like and point `index_path` at the
directory.

---

## 4. Wrap a reranker as a scorer

A reranker is an `Engine` that implements `score_batch`. The input shape is
intentionally flat-with-strides and trips everyone up the first time, so
read this section before you write the method.

### The contract

```python
async def score_batch(
    self,
    queries: List[str],                  # N queries
    passages: List[str],                 # flattened over ALL queries
    candidate_length: List[int] = None,  # passages-per-query strides
    **kwargs,
) -> List[List[float]]:                  # one score list per query
```

- `passages` is **not** grouped per query — it's one flat list across the
  whole batch. `candidate_length[i]` says how many *consecutive* passages
  belong to `queries[i]`. So `sum(candidate_length) == len(passages)` and
  `len(candidate_length) == len(queries)`.
- The return value **is** grouped: one list of floats per query, in
  passage order, higher = more relevant.
- `candidate_length=None` defaults to `[len(passages)]` (all passages
  belong to a single query).

### The canonical implementation skeleton — copy this

```python
# my_reranker.py — ship via file_imports
from typing import List
from routir.models.abstract import Engine

class MyReranker:
    """Sync model wrapper. Knows nothing about RoutIR or async."""
    def __init__(self, model_path: str, batch_size: int = 32):
        self.model = load_my_model(model_path)
        self.batch_size = batch_size

    def score(self, pairs):
        # pairs: List[Tuple[str, str]] of (query, passage)
        # return: List[float] of the same length, higher = more relevant
        out = []
        for i in range(0, len(pairs), self.batch_size):
            out.extend(self.model.predict(pairs[i:i + self.batch_size]))
        return out


class MyRerankerEngine(Engine):
    """RoutIR adapter. Implements score_batch ONLY."""

    def __init__(self, name=None, config=None, **kwargs):
        super().__init__(name, config, **kwargs)
        self.model = MyReranker(
            model_path=config.get("model", "org/reranker"),
            batch_size=config.get("batch_size", 32),
        )

    async def score_batch(self, queries, passages, candidate_length=None, **kwargs):
        if candidate_length is None:
            candidate_length = [len(passages)]
        assert len(candidate_length) == len(queries)
        assert sum(candidate_length) == len(passages)

        # 1) expand queries so each passage has its query alongside it
        expanded = [queries[i] for i, n in enumerate(candidate_length) for _ in range(n)]
        pairs = list(zip(expanded, passages))

        # 2) score all pairs at once (sync call inside async is fine for GPU work)
        flat = self.model.score(pairs)

        # 3) regroup back into per-query lists, in original passage order
        out, cursor = [], 0
        for n in candidate_length:
            out.append(flat[cursor:cursor + n])
            cursor += n
        return out
```

Config:

```json
{
    "file_imports": ["./my_reranker.py"],
    "services": [{
        "name": "my-reranker",
        "engine": "MyRerankerEngine",
        "config": {"model": "org/reranker", "batch_size": 32},
        "cache": 1024, "cache_ttl": 600,
        "batch_size": 16, "max_wait_time": 0.05
    }]
}
```

Smoke test:

```bash
curl -X POST http://localhost:5000/score -H 'Content-Type: application/json' \
  -d '{"service":"my-reranker","query":"q","passages":["p1","p2","p3"]}'
# -> {"scores": [...], ...}
```

In a pipeline, the reranker is the second stage:

```text
my-bm25%1000 >> my-reranker%20
```

The pipeline runs `my-bm25` to get 1000 candidates, fetches each candidate's
text from the collection's `/content` endpoint, then calls your
`score_batch(queries, flattened_passages, candidate_length)` and keeps the
top 20.

### Gotchas

- **Don't override `score`** (the singular one). The base class implements
  it as a one-element call to `score_batch`. Overriding both is a known
  legacy footgun.
- **Return floats in the original passage order.** The pipeline pairs your
  output back to candidate ids positionally — don't sort inside
  `score_batch`.
- **Fallbacks beat crashes.** If a single pair errors, return `0.5` (or any
  neutral score) for it rather than blowing up the whole batch.
- **Truncate to your model's context.** Long passages will OOM or get
  silently clipped by tokenizers.
- **Bytes/multimodal rerankers** (keyframes, audio): set
  `accepts_view_kind = "bytes"` as a class attribute. Then `passages` is
  `List[List[bytes]]` (one inner list per doc, possibly empty / multi-blob).
  REST `/score` refuses bytes engines — reach them via pipeline DSL or gRPC
  `Score`. See `examples/CLAUDE.md` for the full multimodal contract.
- **If candidates aren't supplied by the pipeline** (i.e. you're hitting
  `/score` standalone or the engine should run its own first-stage), look at
  the `Reranker` base class in `src/routir/models/abstract.py` — it
  implements `search_batch` for you via an `upstream_service` +
  `text_service`. Most users only need `score_batch` and the pipeline
  supplies candidates.

---

## 5. Serve a document collection (single- and multi-view)

Collections power `/content` and feed text/bytes to reranker stages. Every
collection has one or more named **views**; a view picks a backend (JSONL,
tar, local files) and a modality (`text` or `bytes`).

### Single text view (the common case)

Either form works. The "legacy" form is still fully supported and is the
shortest path.

```json
{
    "collections": [
        { "name": "my-corpus", "doc_path": "/data/corpus.jsonl",
          "id_field": "docid", "content_field": "text" }
    ]
}
```

Equivalent modern form (use this for anything non-trivial):

```json
{
    "collections": [{
        "name": "my-corpus",
        "views": {
            "text": {
                "kind": "text",
                "source": {
                    "source": "text_jsonl",
                    "doc_path": "/data/corpus.jsonl",
                    "id_field": "docid",
                    "content_fields": ["title", "body"],
                    "sep": "\n"
                }
            }
        }
    }]
}
```

JSONL access is O(1): RoutIR builds a `.offsetmap` sidecar on first open.
Random access then uses byte offsets.

### Multi-view

```json
{
    "collections": [{
        "name": "multivent",
        "default_view": "asr",
        "views": {
            "asr": {
                "kind": "text",
                "source": {"source": "text_jsonl",
                           "doc_path": "/data/mv.jsonl",
                           "id_field": "chunk_id",
                           "content_fields": "asr_transcript"}
            },
            "keyframe": {
                "kind": "bytes",
                "source": {
                    "source": "tar",
                    "tar_template": "/data/mv/shard_{shard:06d}.tar",
                    "shard_resolver": {
                        "kind": "manifest",
                        "path": "/data/mv/catalog.csv",
                        "id_column": "chunk_id",
                        "shard_column": "shard_index"
                    },
                    "matcher": {"kind": "glob", "pattern": "{id}.kf_uni5s.t*.jpg"},
                    "mime": "image/jpeg",
                    "cache_dir": "/expscratch/me/routir/.cache"
                }
            }
        }
    }]
}
```

Pipeline stages pick a view with `@view`:

```text
{asr-search%1000, kf-search%1000}RRF%200 >> kf-reranker@keyframe%20
```

The `kf-reranker` stage gets the `keyframe` view's bytes; `asr-reranker`
(if you added one) would `@asr` and receive strings.

`default_view` is used when a stage omits `@view`. Required to be set
explicitly when there are multiple views; auto-elected when there's only one.

### View backends

| `source:`     | Kind   | Use for                                              |
| ------------- | ------ | ---------------------------------------------------- |
| `text_jsonl`  | text   | One JSONL file (optionally gzipped). The default.    |
| `local_path`  | bytes  | One-or-many files per id (`path_template` or `path_glob`). |
| `tar`         | bytes  | Sharded `.tar` archives with a member-name matcher.  |

For tar collections, the **shard resolver** decides which tar holds a given
id: `manifest` (CSV/TSV `id,shard`), `modulo` (hash-based), or `substring`
(slice of the id is the shard token).

### Sidecar caches and warmup — important on shared filesystems

`tar` and `text_jsonl` backends build sidecar indexes
(`.taridx`, `.offsetmap`) on first access. Scanning 50–500 K members in a
tar on a cold request will stall.

- **Always set `cache_dir`** per view when the dataset mount is read-only
  (most shared FS). Point at an in-tree `./.cache/` by convention.
- **Pre-build sidecars off the login node** with
  `scripts/warmup_slurm.sh <config.json> [view]`. One sbatch job per
  *view* — never per shard. See [`CLAUDE.md`](CLAUDE.md#warming-up-sidecar-caches)
  for the rule and the exact command.

### Caching `/content`

`CollectionConfig.cache` is 256 entries by default and keys on
`(view, id)` — bytes views especially need this. Crank it up for hot
corpora; set to `0` to disable.

For `server_imports`ed remote collections, enable `relay_content_cache` at
the top level of the config; otherwise every reranked candidate triggers a
remote fetch.

---

## Where to look when this skill isn't enough

- **DSL grammar and execution model**: `src/routir/pipeline/parser.py` and
  `src/routir/pipeline/pipeline.py`. The grammar at the top of `parser.py`
  is short and authoritative.
- **Engine contract**: `src/routir/models/abstract.py` — the docstrings
  on `search_batch`, `score_batch`, `decompose_query_batch`, `fuse_batch`
  are the source of truth.
- **Reference engine implementations**: `src/routir/models/` (built-ins)
  and `examples/*_extension.py` (file-imports pattern).
- **Config schema**: `src/routir/config/config.py` — every JSON field
  the server accepts is a Pydantic field with a docstring.
- **Detailed extension how-to**: [`examples/CLAUDE.md`](examples/CLAUDE.md).
- **Project conventions and warmup**: [`CLAUDE.md`](CLAUDE.md).
