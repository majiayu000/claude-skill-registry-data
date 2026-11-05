---
name: plan
description: Master build roadmap for ConvoPilot. Claude should load this when user asks what to build next, starts a coding session, or needs to know the build order.
---

# ConvoPilot Master Build Plan

## Architecture → Features Map

| Layer | ConvoPilot Feature | Status |
|---|---|---|
| 1. Ingestion | F1: Test Ingestion | **Done** |
| 2. Understanding & Orchestration | F2: Spec Builder + F3: Flow Analyzer | F2 **Done**, F3 not started |
| 3. Knowledge / RAG | F3: Flow Analyzer (Weaviate) | Not started |
| 4. Simulation | F4: Conversation Runner | Not started |
| 5. Agent Integration | F5: Agent Client | Not started |
| 6. Evaluation | F7: Tool Call Validator + F8: Conv Evaluator + F9: Semantic Evaluator | Not started |
| 7. Regression & Drift | F11: Drift Detector | Not started |
| 8. Human Review | F13: Review Queue | Not started |
| 9. Observability | F6: Transcript Store + F12: Langfuse + F14: Reports | Not started |
| 10. Storage & Platform | DB models, LLM layer, schemas, routes | **Done** |

---

## Build Order (dependency-aware)

```
F1 ✅ → F2 ✅ → F6 → F5 → F4 → F7 → F8 → F9 → F3 → F13 → F11 → F12 → F10 → F14
                 ↑         ↑    ↑         ↑    ↑
              simple    no deps  needs   needs  needs
              CRUD              F5+F6   F4     transcript
```

---

## What Exists (built in this project)

| Component | Location | What it does |
|---|---|---|
| FastAPI app | `main.py` | CORS, request-ID middleware, router registration |
| DB models (7 tables) | `db/models.py` | TestCaseSpec, ConversationSpec, TestRunSession, ConversationTurn, ToolCallEvent, EvaluationResult, ReviewCase |
| DB session | `db/session.py` | Async MySQL, auto-table-creation, pool_size=5 |
| LLM interface | `llm/interfaces.py` | Abstract LLMInterface, LLMMessage, LLMResponse |
| LLM providers | `llm/providers/claude.py`, `gemini.py` | ClaudeProvider, GeminiProvider |
| LLM factory | `llm/factory.py` | get_llm_provider() → Claude or Gemini |
| F1 Ingestion | `services/ingestion/service.py` | ingest_text, ingest_openapi, ingest_yaml, get/list |
| F2 Spec Builder | `services/interpretation/service.py` | LLM → structured spec (intent, flow, tools, criteria) |
| Schemas | `schemas/test_cases.py` | IngestRequest, StructuredSpec, TestCaseResponse |
| Routes | `routes/test_cases.py` | POST /ingest, GET /{id}, GET / |
| Tests | `tests/test_main.py`, `test_models.py`, `test_llm.py` | 45 tests passing |

---

## Feature Build Specs

### Next: F6 — Transcript Store
- **What:** Persist every conversation turn + tool call to MySQL
- **LLD:** Section 2.1 (Transcript Store), Section 4.1 (ConversationTurn, ToolCallEvent)
- **Models:** Already exist in db/models.py — ConversationTurn, ToolCallEvent, TestRunSession
- **New files:**
  - `services/tracing/__init__.py`
  - `services/tracing/service.py` — TranscriptService
  - `schemas/simulation.py` — response models for runs/transcripts
  - `routes/simulation.py` — GET /simulation/runs/{run_id}
  - `tests/test_tracing.py`
- **Pattern:** Follow services/ingestion/service.py exactly
- **Reference:** None needed — straightforward CRUD

### Then: F5 — Agent Client
- **What:** Adapter layer to call agents (Bolna, HTTP, webhook)
- **LLD:** Section 2.1 (Agent Client), Section 3.5 (Bolna API)
- **Models:** NormalizedAgentResponse (canonical type), AgentConfig
- **New files:**
  - `services/agent_client/__init__.py`
  - `services/agent_client/service.py` — AgentClientService
  - `services/agent_client/http_adapter.py` — HTTP/webhook adapter
  - `services/agent_client/bolna_adapter.py` — Bolna API adapter (agents, calls, executions)
  - `routes/agents.py` — GET /agents/bolna
  - `tests/test_agent_client.py`
- **Pattern:** Adapter pattern — one interface, multiple implementations
- **Reference:** Bolna API docs (docs.bolna.ai)

### Then: F4 — Conversation Runner
- **What:** Multi-turn simulation engine (text mode first, voice later)
- **LLD:** Section 2.1 (Conversation Runner), LLD testing engine structure
- **Models:** TestRunSession (state machine), ConversationSpec
- **New files:**
  - `services/simulation/__init__.py`
  - `services/simulation/service.py` — ConversationRunnerService
  - `services/simulation/persona.py` — LLM-driven persona generation
  - `routes/simulation.py` — POST /simulation/run (extend from F6)
  - `tests/test_simulation.py`
- **Pattern:** State machine (pending→running→awaiting_evaluation→evaluated→completed)
- **Reference:** Text mode runs the multi-turn loop in-process; voice mode hands the persona to the Bolna "ConvoPilot Caller" agent and pulls the transcript + recording from the executions API

### Then: F7 — Tool Call Validator
- **What:** Intercept + validate tool calls during simulation
- **LLD:** Section 2.1 (Tool Call Validator), Section 10.5 (tool metrics)
- **Models:** ToolCallEvent, ExpectedToolCall from ConversationSpec
- **New files:**
  - `services/tool_calls/__init__.py`
  - `services/tool_calls/service.py` — ToolCallValidatorService
  - `tests/test_tool_calls.py`
- **Pattern:** Called per-turn inside F4's loop
- **Checks:** tool_was_called, tool_not_called, argument matching

### Then: F8 — Conversation Evaluator
- **What:** LLM-as-judge + DeepEval for conversation correctness
- **LLD:** Section 2.1 (Conversation Evaluator), Section 10.1-10.2, Section 10.6 (verdict formula)
- **Models:** EvaluationResult, MetricResult
- **New files:**
  - `services/evaluation/__init__.py`
  - `services/evaluation/conversation.py` — ConversationEvaluatorService
  - `services/evaluation/deepeval_runner.py` — DeepEval integration
  - `schemas/evaluation.py` — evaluation response models
  - `routes/evaluation.py` — GET /evaluation/{run_id}, GET /evaluation/{run_id}/deepeval
  - `tests/test_evaluation.py`
- **Verdict formula:** weighted avg of 7 metrics (flow_adherence 25%, slot_coverage 20%, outcome_completion 15%, intent_recognition 15%, response_relevance 10%, hallucination_score 10%, tone_appropriateness 5%)
- **Metrics:** TP/FP/TN/FN, precision, recall, F1

### Then: F9 — Semantic Evaluator
- **What:** Intent, tone, hallucination + RAGAS grounding
- **LLD:** Section 2.1 (Semantic Evaluator), Section 10.1 F9 metrics, Section 10.3 (RAGAS)
- **New files:**
  - `services/evaluation/semantic.py` — SemanticEvaluatorService
  - `services/evaluation/ragas_runner.py` — RAGAS integration
  - `routes/evaluation.py` — GET /evaluation/{run_id}/ragas (extend)
  - `tests/test_semantic_eval.py`
- **Reference:** RAGAS library docs for faithfulness, answer_relevancy, context_precision

### Then: F3 — Flow Analyzer (RAG)
- **What:** Semantic flow graph from use case description using Weaviate RAG
- **LLD:** Section 2.1 (Flow Analyzer)
- **New files:**
  - `services/understanding/__init__.py`
  - `services/understanding/service.py` — FlowAnalyzerService
  - `services/understanding/weaviate_client.py` — Weaviate integration
  - `tests/test_understanding.py`
- **Requires:** WEAVIATE_URL + WEAVIATE_API_KEY secrets
- **Reference:** None — Weaviate client SDK docs

### P1: F13 → F11 → F12 → F10

- **F13 (Review Queue):** Simple state machine — pending_review → in_review → approved/overridden. Triggered when confidence_score < 0.70
- **F11 (Drift Detector):** Compare current vs baseline EvaluationResult. Uses the F8 classification metrics
- **F12 (Langfuse Client):** Wrap langfuse SDK with try/except. Never block execution
- **F10 (STT/TTS Recommender):** LLM + knowledge base → ranked providers. Standalone

### P2: F14 — Reports + Frontend Wiring

- Backend: aggregate run results → structured JSON
- Frontend: replace mock data in all 15 pages with real API calls
- Start with TestCases.tsx (already has api.ts client ready)

---

## Consistency Rules (when pulling from repos)

When code comes from reference repos, always:
1. Rename classes to `<Name>Service` pattern
2. Replace sync code with async
3. Replace direct SDK imports with our `llm/interfaces.py`
4. Replace their DB patterns with our SQLAlchemy async (flush, not commit)
5. Remove framework-specific deps (test mocks, rollbar, etc.)
6. Run `/consistency` after pulling to catch drift

---

## Workflow Per Feature

```
/plan                    ← load this roadmap (you're reading it now)
/go build F<n>           ← refine prompt + TDD build
/verify                  ← 3 agents check the work
/consistency             ← ensure it matches the rest of the codebase
/learn                   ← save lessons for future sessions
git add + commit + push  ← you run these manually
```

---

## System Limits (from LLD Section 3.6)

| Limit | Value |
|---|---|
| Max turns per conversation | 20 (configurable) |
| Agent response timeout | 10s per turn |
| LLM evaluator timeout | 30s |
| LLM API retries | 3 (backoff: 1s→2s→4s) |
| Max requirement text | 50 KB |
| Max OpenAPI spec | 500 KB |
| Max tool call output | 100 KB |
| Review queue page size | 20 default / 100 max |
