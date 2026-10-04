---
name: super-factory
category: ai_collection
description: Super Factory multi-agent pipeline system — E2E testing, real execution, and contract debugging.
---

# Super Factory

Autonomous Agent development platform with 4-stage pipeline: Research → Planning → Build → Eval.

## When to Use

- Running E2E tests for the Super Factory pipeline
- Executing real LLM-driven pipeline runs
- Debugging agent contract precondition failures
- Adding new agent roles or modifying pipeline YAML
- Setting up API keys for the project

## Project Location

`~/ai_github/super_factory/`

## Quick Commands

```bash
# Run E2E test suite (all mocked)
cd ~/ai_github/super_factory && python3 -m pytest tests/test_e2e_pipeline.py -v

# Run full test suite
cd ~/ai_github/super_factory && python3 -m pytest tests/ -v

# Run real pipeline (requires valid API keys)
cd ~/ai_github/super_factory && python3 scripts/run_real_pipeline.py

# Run CLI pipeline
cd ~/ai_github/super_factory && python3 scripts/run_pipeline.py --pipeline default --context "query=topic"
```

## E2E Testing Pattern

The E2E test suite (`tests/test_e2e_pipeline.py`) validates the full pipeline through the real Orchestrator + PipelineExecutor stack with mocked LLM responses.

### Key Test Classes

| Class | Coverage |
|---|---|
| `TestFullPipelineEndToEnd` | 4-agent happy path, contract precondition blocking, postcondition failure |
| `TestPipelineExecutorIntegration` | Full DAG execution, context passing, failure propagation |
| `TestTraceCollectionEndToEnd` | TraceCollector record/read round-trip, disk persistence |
| `TestHookLifecycleE2E` | PIPELINE_START, STEP_START, AGENT_POST_EXECUTE, PIPELINE_END hooks |

### Mock Response Requirements

Each agent role has specific contract preconditions that mock contexts MUST satisfy:

```python
# Research: query (non-empty) + available_sources + knowledge_sources_consulted
research_context = {"query": "topic", "available_sources": ["url"], "knowledge_sources_consulted": [".wiki/"]}

# Planning: vision (non-empty string) + (research_refs (list) OR knowledge_sources (list))
planning_context = {"vision": "Build something", "research_refs": ["ref.md"]}

# Build: plan (non-empty dict) + task_id (non-empty string)
build_context = {"plan": {"tasks": ["T-1"]}, "task_id": "T-1"}

# Eval: spec_path (non-empty string) + target_output (not None)
eval_context = {"spec_path": "specs/agents/build.yaml", "target_output": build_result}
```

### Contract Debugging Flow

When a test hits "blocked" status:
1. Check which agent's precondition failed (look at log: `Pre-condition failed for <role>`)
2. Read `contracts/<role>.py` to find required fields
3. Ensure the context dict provides all required fields with correct types
4. Common issue: `research_refs` must be a **list**, not a string; `plan` must be a **dict**, not a string

## Real Pipeline Execution

### API Key Setup

```bash
# 1. Extract API key from hermes config or use your own
# 2. Write to .env
cat > ~/ai_github/super_factory/.env << 'EOF'
DASHSCOPE_API_KEY=your-key-here
# or KIMI_API_KEY=...
EOF

# 3. Update agents/config.yaml to use the provider with the valid key
#    default_provider: dashscope  (or kimi)
#    fallback_chain: [dashscope]  (or [kimi])
```

### Pitfalls

- **API keys in .hermes/config.yaml may be truncated or expired** — always test with a simple call first
- **fallback_chain must only include providers with valid API keys** — remove zhipu/kimi/openai if no keys set
- **dotenv load_dotenv() fails in REPL mode** — use manual env loading in scripts
- **PipelineExecutor marks pipeline as "completed" even when ALL steps fail** — check `state.step_results` for individual status, not just `state.status`
- **`claude` CLI auth is broken (HTTP 403) — ALL models return 403** — kimi-k2.5, qwen3-coder-plus, glm-5, glm-5.1 all fail with `Failed to authenticate. API Error: 403 Request not allowed`. Do NOT use `claude` CLI for this project. Use `opencode --model kimi-k2.5 --print 'prompt'` as fallback for code review and patches instead.
- **Critical runtime bugs (as of May 2026)**: `_make_trace()` returns `list[Message]` instead of `list[dict]` causing JSON serialization crash; `_build_messages()` is abstract but unimplemented in domain agents causing `NotImplementedError`; `ModelRouter` lacks exponential backoff/retry. These must be patched before any pipeline run will succeed.

### Execution Script

Use `scripts/run_real_pipeline.py` for real LLM execution. It:
1. Loads .env manually (avoids dotenv REPL issues)
2. Initializes real Orchestrator with live LLM routing
3. Runs default 4-step pipeline with proper context
4. Prints step-by-step results with scores
5. Saves summary to `outputs/pipeline-summary.json`

## Knowledge Base Module

Located at `knowledge/`. Implements Repository Pattern with SQLite backend.

| File | Purpose |
|---|---|
| `models.py` | Entity / Relation / Source data models |
| `repository/base.py` | Abstract KnowledgeRepository interface (CRUD + search + spec) |
| `repository/sqlite.py` | SQLite backend, default `.super_factory/data/knowledge.db` |
| `service.py` | KnowledgeService facade: add/get/search/link/promote_tier |
| `validator.py` | EntityValidator with spec-based validation (K003-K011) |
| `adapter.py` | KnowledgeService → Hook bridge layer |

Key patterns:
- Three-tier entity system: research → finding → knowledge (promote-only, no downgrade)
- Source tracking for citation provenance
- Spec validation before write (K003: must have source; K005: must match type spec)
- Currently keyword-only search (no vector/semantic search yet)
- External kg.db (`~/wiki/kg.db`) not yet integrated

## Memory System Module

Located at `memory/`. File-first JSON persistent storage.

| File | Purpose |
|---|---|
| `types.py` | MemoryEntry frozen dataclass (id, pipeline_id, agent_role, category, content, confidence, tags, created_at, expires_at) |
| `store.py` | MemoryStore: per-entry JSON files + `_index.json`, metadata query, keyword relevance, prune |
| `blocked/` | Blocked pipeline records |
| `skills/` | Agent skill cache |

Key patterns:
- Individual JSON files per entry with index for fast querying
- Thread-safe via threading.Lock
- `query()` filters by pipeline_id/agent_role/category/tags, sorted by created_at desc
- `relevant()` keyword matching with confidence-weighted scoring
- `prune(max_age_days=30)` removes expired + old entries
- No vector/semantic search, no layered memory architecture yet

## Pipeline Architecture

```
Research Agent → Planning Agent → Build Agent → Eval Agent
     ↓                ↓               ↓            ↓
  Contract         Contract        Contract     Contract
  (pre+post)       (pre+post)      (pre+post)   (pre+post)
     ↓                ↓               ↓            ↓
  Scorer          Scorer          Scorer       Scorer
     ↓                ↓               ↓            ↓
  Trace           Trace             Trace        Trace
```

Context flows via `context_map` in pipeline YAML:
- `research.summary` → `planning.research_refs`
- `planning.phases` → `build.plan`
- `build` → `eval.target_output`

## Support Files

- `references/contract-reference.md` — Full contract precondition/postcondition specs for all 4 agents
- `references/audit-log-20260509.md` — Code quality audit findings (2026-05-09): critical runtime bugs, claude CLI auth failure, opencode fallback
- `references/storage-audit-20260512.md` — Knowledge/Memory storage current-state audit (2026-05-12)
- `scripts/run_real_pipeline.py` — Ready-to-run real pipeline execution script