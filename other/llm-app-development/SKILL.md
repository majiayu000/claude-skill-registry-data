---
name: llm-app-development
description: >
  Build LLM applications: RAG, embeddings, agents, structured outputs, evaluations, fine-tuning, and local inference.
license: MIT
compatibility: "Varies by task. Common: Python 3.10+, Node.js 18+. Optional: GPU for local inference"
metadata:
  source: iuliandita/skills
  date_added: "2026-04-02"
  effort: high
  argument_hint: "[task description or architecture question]"
---

# LLM Application Development

Build, review, and architect applications that use AI models - from single-API calls to
multi-agent systems with RAG pipelines. The goal is production-grade AI apps that are reliable,
cost-effective, and don't hallucinate their way into an incident.

**Target versions**: October 2026 snapshot. Read `references/target-versions.md` before
pinning model IDs (Claude/OpenAI/DeepSeek families), SDKs, runtimes, vector stores, or evaluation tools.
Unfamiliar model names or versions are not evidence of fabrication: verify them against primary
provider docs, installed binaries (`--version`/`--help`), and package sources before rejecting them.

## When to use

- Integrating LLM APIs (Anthropic, OpenAI, etc.) into applications
- Building RAG pipelines (chunking, embedding, retrieval, generation)
- Designing agent systems (tool use, loops, state, multi-agent)
- Choosing between fine-tuning, RAG, and prompt engineering
- Setting up vector stores for semantic search
- Implementing structured output and tool use / function calling
- Building evaluation and testing harnesses for AI features
- Optimizing token costs, latency, and model routing
- Setting up local inference with Ollama or vLLM
- Adding safety guardrails (content filtering, PII handling, output validation)

## When NOT to use

- Building MCP servers or tools (use **mcp** - it handles the protocol layer)
- Writing or refining individual prompts (use **prompt-generator**)
- General database configuration, schema design, or migrations (use **databases**)
- Security auditing AI application code (use **security-audit**)
- Reviewing code quality unrelated to AI/ML patterns (use **code-review**)
- Building AI-powered HTTP APIs (use **backend-api** for the API layer; return here for the LLM integration within it)
- Reviewing AI-generated application code for slop, hallucinated APIs, or over-abstraction (use **code-simplification**)

## AI Self-Check

AI tools consistently produce the same mistakes when generating AI application code.
**Before returning any generated AI/ML code, verify against this list:**

- [ ] API keys loaded from environment variables, never hardcoded
- [ ] Streaming responses handled with proper error boundaries and cleanup
- [ ] Token limits respected - input truncation or chunking for long contexts
- [ ] Structured output uses native schema enforcement (Anthropic `output_config.format` or
  strict tools, OpenAI Responses `text.format` or Chat Completions `response_format`), with
  application validation for constraints the provider cannot enforce
- [ ] Tool use / function calling validates tool results before passing back to the model
- [ ] Retry logic uses exponential backoff with jitter, not fixed delays
- [ ] Rate limit errors (429) handled distinctly from server errors (5xx)
- [ ] Vector store queries include a relevance threshold - don't blindly pass low-similarity
  results to the model
- [ ] Embedding model matches between indexing and querying (mixing models = garbage results)
- [ ] Prompt templates use parameterized injection, not string concatenation
- [ ] Model responses validated before use (check for refusals, empty content, malformed JSON)
- [ ] Cost estimation done before batch operations (token count * price * volume)
- [ ] No synchronous LLM calls in request handlers - always async with timeouts
- [ ] PII stripped or masked before sending to external model APIs
- [ ] Sampling settings are intentional only where the selected model supports them; use
  effort and native schemas on models that reject temperature or other sampling controls
- [ ] **Provider drift checked**: Responses/Agents/SDK examples use current provider surfaces, not deprecated patterns - specifically verify no use of `openai.beta.assistants.create` (Assistants API, superseded by Responses/Agents API) or other Assistants-era surfaces
- [ ] **RAG evidence bounded**: retrieval thresholds, citations, and empty-result behavior are defined before generation
- [ ] **Pipeline delivered end to end**: a requested RAG or agent build ships ingestion and chunking, the embedding adapter, indexing, retrieval, and the generation handler as runnable code, not a schema plus a retrieval query with the rest left as TODO
- [ ] Cross-cutting agent hygiene applied - see `references/agent-hygiene.md`

## Performance

- Batch embeddings and eval runs; avoid one request per row when the provider offers batch or bulk APIs.
- Cache deterministic retrieval, tool metadata, and prompt templates, but never cache tenant-specific model outputs without a data-retention decision.
- Track token, latency, and retry budgets separately for interactive, background, and eval traffic.

## Best Practices

- Keep model, tool, retrieval, and safety decisions configurable per environment; avoid hardcoding preview model names in application logic.
- Treat model output as untrusted input: validate structure, refusal states, tool arguments, and downstream side effects.

## Workflow

Copy this checklist and track progress:
- [ ] Step 1: Architecture pattern chosen
- [ ] Step 2: Lightest sufficient abstraction chosen
- [ ] Step 3: Implemented, AI Self-Check passes
- [ ] Step 4: Evals pass (on failure, fix the cause and return to Step 3)

### Step 1: Determine the architecture pattern

| Need | Pattern | Start with |
|------|---------|------------|
| Single model call | Direct API integration | Provider SDK |
| Knowledge-grounded answers | RAG pipeline | Vector store + retrieval |
| Multi-step reasoning | Agent with tools | LangGraph, OpenAI Agents SDK, or custom loop |
| Multiple specialized models | Model routing / chain | Custom router or Vercel AI SDK |
| Offline / air-gapped | Local inference | Ollama or vLLM |
| Existing data enrichment | Batch processing | Provider batch APIs |

### Step 2: Choose the right abstraction level

Pick the lightest tool that solves the problem:

1. **Raw SDK** - direct Anthropic/OpenAI SDK calls. Best for simple integrations, maximum
   control, minimum dependencies. Start here unless you have a specific reason not to.
2. **Vercel AI SDK** - unified provider interface with streaming primitives. Good for
   TypeScript apps that need provider-agnostic code or React/Next.js streaming UI.
3. **LangChain / LlamaIndex** - orchestration frameworks. Use when you need complex chains,
   built-in document loaders, or 300+ pre-built integrations. Don't use for simple API calls -
   the abstraction overhead isn't worth it.
4. **LangGraph / OpenAI Agents SDK** - stateful agent frameworks. Use when you need cycles,
   persistence, human-in-the-loop, or multi-agent coordination.

### Step 3: Implement

Follow the domain-specific sections below. Read the appropriate reference file for detailed
patterns and code examples.

### Step 4: Evaluate and validate

Every AI feature needs evaluation. Not "run it once and eyeball the output" - structured evals
with datasets, metrics, and regression detection.

Start with the project's existing evals and representative success, failure, and boundary
cases for the changed behavior. Prefer deterministic assertions where they prove the contract;
add paid judge or cost checks only when they answer a material question. Preserve required CI
gates, track regressions, and expand the dataset when failures expose missing coverage. A small
prompt fix does not require a new framework or an arbitrary minimum case count. If a case
fails, fix the cause and return to Step 3; repeat until the required cases pass.

Read `references/evaluation.md` for promptfoo setup, assertion types, CI integration (GitHub
Actions example), RAG-specific evals, agent evals, and red teaming patterns.

## LLM Integration Patterns

### Streaming

Stream user-facing responses. For background processing, stream when progress, incremental
persistence, early error detection, or timeout avoidance matters; otherwise buffer the result.

```python
# Anthropic streaming (Python)
import anthropic

client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-sonnet-5-5",
    max_tokens=4096,  # covers adaptive thinking plus the reply
    messages=[{"role": "user", "content": prompt}],
) as stream:
    for text in stream.text_stream:
        yield text
```

### Structured output

Use native provider mechanisms, not regex parsing of free-text responses.

- **Anthropic**: `tool_use` with JSON schema (add `strict: true` to guarantee validation), or `output_config: { format: { type: "json_schema", ... } }`
- **OpenAI**: Responses `text.format: { type: "json_schema", ... }`, or Chat Completions `response_format: { type: "json_schema", json_schema: {...} }` where supported
- **Vercel AI SDK**: `generateText()` with `output: Output.object({ schema })` and a Zod schema

### Tool use / function calling

Define tools with tight schemas. Validate tool results before feeding them back.

```python
tools = [{
    "name": "search_docs",
    "description": "Search internal documentation",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "maxLength": 200},
            "limit": {"type": "integer", "minimum": 1, "maximum": 50}
        },
        "required": ["query"]
    }
}]
```

Read `references/llm-patterns.md` for multi-turn tool use, parallel tool calls, error
recovery, and provider-specific gotchas.

## RAG Architecture

The quality of a RAG system depends more on retrieval quality than model quality.
A mediocre model with great retrieval beats a frontier model with bad retrieval.

### Chunking strategy

| Strategy | When to use | Chunk size |
|----------|------------|------------|
| Fixed-size with overlap | Default starting point | 512-1024 tokens, 10-20% overlap |
| Semantic (sentence/paragraph) | Well-structured documents | Varies by content |
| Recursive character | Mixed content types | 1000 chars, 200 overlap |
| Document-aware (markdown headers, code blocks) | Structured docs, code | Section-based |
| Parent-child | Need both precision and context | Small retrieval, large context |

### Embedding model selection

Use the same model for indexing and querying. Mixing models produces meaningless similarity
scores.

Read `references/rag-patterns.md` section 4 for the embedding model comparison.

### Retrieval patterns

1. **Vector search alone** - fast, good for semantic similarity, bad for exact keyword matches
2. **Hybrid search** (vector + BM25/keyword) - best default. Qdrant, Weaviate, and Pinecone
   support this natively. pgvector + `tsvector` for PostgreSQL.
3. **Reranking** - retrieve more candidates (top-50), rerank with a cross-encoder or Cohere
   Rerank, return top-5. Adds latency but significantly improves relevance.
4. **Query expansion** - rephrase the user query using an LLM before retrieval. Helps when
   user queries are vague or use different terminology than the source docs.

Pick a vector store from the selection table in `references/rag-patterns.md` section 5.

### Minimal RAG example (Python + pgvector)

```python
from anthropic import Anthropic
import psycopg

client = Anthropic()

def search(query: str, limit: int = 5) -> list[dict]:
    embedding = get_embedding(query)  # same model used at index time
    with psycopg.connect(DB_URL) as conn:
        rows = conn.execute(
            "SELECT content, 1 - (embedding <=> %s::vector) AS score "
            "FROM documents WHERE 1 - (embedding <=> %s::vector) > 0.7 "
            "ORDER BY embedding <=> %s::vector LIMIT %s",
            [embedding, embedding, embedding, limit],
        ).fetchall()
    return [{"content": r[0], "score": r[1]} for r in rows]

def ask(question: str) -> str:
    context = search(question)
    if not context:
        return "No relevant documents found."
    response = client.messages.create(
        model="claude-sonnet-5-5",
        max_tokens=4096,
        messages=[{"role": "user", "content": (
            f"Answer based on these documents:\n\n"
            + "\n---\n".join(d["content"] for d in context)
            + f"\n\nQuestion: {question}"
        )}],
    )
    if response.stop_reason != "end_turn":  # max_tokens can be spent on thinking; refusal has no answer
        raise RuntimeError(f"incomplete answer: {response.stop_reason}")
    # Thinking blocks can precede the text; select by type, not position.
    return "".join(b.text for b in response.content if b.type == "text")
```

Key patterns: relevance threshold (0.7), same embedding model for index/query, context passed as user message prefix.
`get_embedding` and the indexing loop are the pieces most often left out of a "build a RAG pipeline"
answer; a delivered pipeline includes both (sections 3 and 4 of `references/rag-patterns.md`).

Read `references/rag-patterns.md` for indexing pipelines, metadata filtering, multi-index
strategies, and production RAG architecture.

## Agent Systems

### The agent loop

Every agent system is fundamentally: observe -> think -> act -> repeat. The differences are in
how you manage state, handle failures, and know when to stop.

```
while not done:
    observation = get_context(state)
    action = model.decide(observation, tools)
    if action.type == "final_answer":
        done = True
    else:
        result = execute_tool(action)
        state.add(result)
```

### Framework selection

| Framework | Best for | Key feature |
|-----------|----------|-------------|
| Custom loop | Simple agents, maximum control | No dependencies |
| LangGraph | Complex state machines, cycles, persistence | Graph-based, checkpointing |
| OpenAI Agents SDK | OpenAI-native, multi-agent handoffs | Sessions, tracing |
| Claude Agent SDK | Claude-native agentic loops in code | Programmatic SDK for building custom agents with Claude; use when you need fine-grained control over Claude agent behavior in your own application |
| Vercel AI SDK | TypeScript agents with UI streaming | ToolLoopAgent, React hooks |

### Common pitfalls

1. **Infinite loops** - always set a max iteration count. Agents will happily loop forever.
2. **Tool explosion** - more than 10-15 tools degrades model performance. Group related
   operations into fewer, more capable tools.
3. **Missing error handling** - tool failures are normal. The agent needs to recover, not crash.
4. **No cost ceiling** - a runaway agent can burn through API budget. Set per-request token
   and cost limits.
5. **Stale context** - long-running agents accumulate context. Summarize or prune periodically.

### Minimal safe agent loop

Every agent loop needs an iteration cap, a cost gate, and a tool-error policy. Retry transient
errors with backoff, abort on permanent errors, and pass failed tool results back with an error
marker so the model can choose the next step instead of silently losing state.

Read `references/agent-patterns.md` for multi-agent architectures, human-in-the-loop patterns,
memory management, and production agent deployment.

## Fine-Tuning vs RAG vs Prompt Engineering

Pick the cheapest approach that meets your quality bar:

| Approach | Cost | Lead time | Best for |
|----------|------|-----------|----------|
| **Prompt engineering** | Lowest | Hours | Formatting, tone, simple tasks |
| **Few-shot examples** | Low | Hours | Pattern matching, classification |
| **RAG** | Medium | Days | Knowledge-grounded, dynamic data |
| **Fine-tuning** | High | Days-weeks | Style/behavior, latency-critical, domain specialization |

**Fine-tune when**: prompt engineering can't capture the behavior, you need consistent
style/format across thousands of outputs, or you need lower latency than RAG provides.

**Don't fine-tune when**: your data changes frequently (use RAG), you have fewer than 100
high-quality examples, or prompt engineering already works (you're just cargo-culting).

Read `references/fine-tuning.md` for data preparation, PEFT/LoRA patterns, evaluation during
training, and when to use full fine-tuning vs parameter-efficient methods.

## Local Inference

### Local serving choices

| Tool | Best for | GPU required |
|------|----------|-------------|
| Ollama | Dev, prototyping, Mac (MLX) | No (CPU/MLX), optional GPU |
| vLLM | Production serving, high throughput | Yes |
| llama.cpp / llama-cpp-python | Minimal deps, quantized models, CPU-only | No (CPU), optional GPU |
| TGI (HF Text Generation Inference) | HF model hub integration | Yes |

CPU-only llama.cpp is viable for dense models that fit in RAM and MoE models with low active
params. Pass server API keys with `--api-key-file <path>`, never `--api-key <value>`, which
leaks into `/proc/<pid>/cmdline`.

Read `references/local-inference.md` for CPU-only fit and gotchas, the llama.cpp build per CPU
generation, SHA-pinned model download, systemd-per-model deployment, NUMA tuning, mlock
budgeting, benchmark methodology, and production serving configuration.

## Cost Optimization

### Token budgeting

Know your costs before you scale:

```
cost_per_request = (input_tokens * input_price + output_tokens * output_price) / 1_000_000
monthly_cost = cost_per_request * requests_per_day * 30
```

### Strategies (ordered by impact)

1. **Model routing** - use cheaper models for easy tasks, frontier models for hard ones.
   Route by task complexity, not by default.
2. **Caching** - cache identical or semantically similar requests. Anthropic prompt caching
   bills cache reads at a fraction of the base input price; the ratio varies by model.
3. **Prompt optimization** - shorter prompts cost less. Cut examples, compress instructions.
4. **Batch APIs** - Anthropic and OpenAI offer 50% discounts for async batch processing.
5. **Output length limits** - set `max_tokens` to what you actually need, not 4096 "just in case."
6. **Context pruning** - for multi-turn conversations, summarize history instead of sending
   the full transcript.

## Safety and Guardrails

Input validation (prompt injection), output validation (schema + content policy), PII handling
(strip before external API calls), rate limiting (per-user + per-IP), content filtering, and
audit logging (redact PII). These are non-negotiable for production AI apps.

Read `references/safety.md` for prompt injection defense patterns, output validation schemas,
PII detection setup, and content policy implementation.

## Production Checklist

- [ ] API keys in environment variables or secret manager (never in code)
- [ ] Timeouts set on all LLM calls (model inference can hang)
- [ ] Rate limiting on AI-powered endpoints
- [ ] Cost monitoring and alerting (daily spend, per-request cost tracking)
- [ ] Structured logging of prompts, responses, latency, token usage
- [ ] Evaluation suite running in CI (regression detection)
- [ ] Model fallback chain configured (primary -> secondary -> error response)
- [ ] Input validation and prompt injection defense
- [ ] Output validation before returning to users
- [ ] Max token limits set per request type
- [ ] Health checks on model endpoints (especially self-hosted)
- [ ] A/B testing infrastructure for prompt and model changes

## Reference Files

- `references/llm-patterns.md` - multi-turn tool use, parallel tool calls, error recovery, provider gotchas
- `references/rag-patterns.md` - indexing pipelines, metadata filtering, multi-index, production architecture
- `references/agent-patterns.md` - multi-agent, human-in-the-loop, memory management, production deployment
- `references/evaluation.md` - promptfoo setup, assertion types, CI integration, RAG/agent evals, red teaming
- `references/fine-tuning.md` - data prep, PEFT/LoRA, training evaluation, full vs parameter-efficient methods
- `references/local-inference.md` - quantization, model selection, GPU memory, production serving config
- `references/safety.md` - prompt injection defense, output validation, PII handling, content filtering, audit logging
- `references/target-versions.md` - October 2026 snapshot: Claude/OpenAI/DeepSeek model families, AI SDKs, runtimes, vector stores, and eval tools

## Output Contract

See `references/output-contract.md` for the full contract.

- **Skill name:** LLM-APP-DEVELOPMENT
- **Deliverable bucket:** `audits`
- **Mode:** conditional. When invoked to **analyze, review, audit, or improve** existing repo content, apply the reporting size and evidence rules in `references/output-contract.md` and write the deliverable to `docs/local/audits/llm-app-development/<YYYY-MM-DD>-<slug>.md`. When invoked to **answer a question, teach a concept, build a new artifact, or generate content**, respond freely without the contract.
- **Severity scale:** `P0 | P1 | P2 | P3 | info` (see shared contract; only used in audit/review mode).

## Related Skills

- **mcp** - handles MCP server development (the protocol/tooling layer). This skill handles
  the application layer - how to build apps that call models, retrieve context, and orchestrate
  agents. If building an MCP server, use mcp. If building an app that uses AI, use this skill.
- **prompt-generator** - for crafting and refining individual prompts. This skill covers prompt
  template management and patterns within applications; prompt-generator handles one-off prompt
  creation and iteration.
- **databases** - for general database operations. This skill covers vector store integration
  for RAG; databases handles engine configuration, schema design, and traditional DB operations.
- **security-audit** - for security review of AI application code. This skill provides
  guardrail patterns; security-audit provides the audit methodology.
- **code-review** - for reviewing AI application code quality beyond AI-specific patterns.
- **backend-api** - for the HTTP API layer wrapping AI features. Use backend-api for contract design, auth, and route structure; use this skill for the LLM integration within those handlers.
- **code-simplification** - for auditing AI-generated application code for hallucinated APIs, over-abstraction, and slop patterns introduced by AI generation tools.
- **testing** - for non-AI test infrastructure: unit/integration test harnesses and CI coverage gates. This skill covers model evaluation; testing covers the surrounding test harness.

## Rules

1. **Start with the simplest approach.** Direct SDK calls before frameworks. Prompt engineering
   before fine-tuning. Single agent before multi-agent. Complexity is a cost.
2. **Set token limits explicitly.** `max_tokens` on every call. Unbounded generation wastes
   money and risks timeouts.
3. **Cap agent iterations.** Set a max loop count. Runaway agents burn budget and produce
   garbage. 10-20 iterations is a reasonable default.
