---
name: sota-llm-engineering
description: >-
  State-of-the-art LLM application engineering rules for BUILDING and AUDITING LLM-powered features. Claude should use this skill whenever it is building, modifying, or reviewing anything that calls a language model — chat features, RAG pipelines, agents and tool use, structured extraction, classification, summarization, embeddings/vector search, evals and regression gates, prompt or context engineering, model selection/routing, fine-tuning decisions, or LLM cost/latency/observability work. Trigger keywords: LLM, AI feature, prompt, system prompt, context window, RAG, retrieval, embeddings, vector DB, rerank, chunking, agent, tool use, MCP, multi-agent, evals, golden set, LLM-as-judge, fine-tuning, model selection, routing, structured output, JSON schema, prompt caching, token budget, counting tokens, instruction file size, tokenizer, hallucination, grounding. Covers build-quality only — for prompt-injection/agent-security use sota-code-security rules/08 and sota-sandboxing rules/05.
---

# SOTA LLM Engineering

## Purpose

One skill, two modes. The `rules/` files define the baseline for
engineering LLM-powered software that is **measured, grounded, bounded, and
observable**. In **BUILD** mode you write LLM features that conform to the
rules by default. In **AUDIT** mode you hunt for violations and report them as
severity-rated findings. The rules are the single source of truth for both.

Framing: an LLM call is a non-deterministic, expensive, latency-heavy RPC to a
dependency that changes underneath you. Everything here follows from that —
you don't ship logic you can't measure (evals), you don't trust output you
didn't validate (structured output, grounding), you don't run loops you can't
stop (budgets), and you don't deploy what you can't trace (observability).

**Scope boundary:** this skill owns build quality. Prompt injection, the
lethal trifecta, tool-call authorization, and model-output-as-untrusted-data
live in `sota-code-security` rules/08; agent sandboxing/isolation lives in
`sota-sandboxing` rules/05; PII/regulatory handling lives in
`sota-privacy-compliance`. Reference them; don't re-derive them.

**Freshness rule:** model names, prices, context limits, and spec revisions in
these files were verified June 2026 and rot fast. When a decision hinges on a
specific model/price/limit, re-verify against provider docs (or the project's
`claude-api`-style reference skill) before encoding it. Write code
version-agnostically: model IDs and parameters in config, never inline.

## BUILD mode — eval-first by default

1. **Write the eval before the feature.** Before any prompt or pipeline work,
   produce a 20+ case golden set with graded criteria (rules/01). A feature
   without an eval is a prototype; treat requests to "just add an LLM call"
   as a request for an eval + a call.
2. **Start at the simplest tier.** Single call → structured output → workflow
   (code-orchestrated, deterministic) → agent. Escalate only when the eval
   shows the simpler tier failing (rules/04 has the decision gates).
3. **Defaults, not options.** Schema-constrained output with validation +
   bounded repair (rules/02); hybrid retrieval with a golden retrieval set
   when RAG is needed (rules/03); stop conditions + token/cost budgets on
   every loop (rules/04); retries with jittered backoff, model IDs in config,
   per-call tracing (rules/05).
4. **Structural over disciplinary.** Prefer designs where the bad variant
   can't be written: typed prompt templates instead of f-string soup,
   versioned prompts in repo, a single gateway module for all model calls
   that enforces tracing/budgets/retries centrally.
5. **When requirements force a deviation** (no eval data yet, latency forbids
   a judge, unbounded agent demanded), implement the rules file's documented
   mitigation and leave a `LLMENG:` comment stating the residual risk.
6. **Finish with the audit checklists.** Run the relevant rules files'
   end-of-file checklists against your own diff before declaring done.

## AUDIT mode — hunting quality violations

Process:

1. **Map the LLM surface**: every call site (grep `messages.create`,
   `responses.create`, `chat.completions`, `interactions.create`,
   `generateContent`/`generate_content`, `invoke`, raw `https://api.`),
   prompt templates, retrieval pipelines, agent loops, eval suites (or their
   absence), and the config/env that selects models.
2. **Sweep by rules file, prioritized**: 01 (evals — absence is the #1
   systemic finding), 04 (unbounded agents), 05 (cost/reliability), 02
   (prompt/output hygiene), 03 (RAG), 06 (data lifecycle).
3. **Check the negatives.** Missing controls are findings: no eval suite, no
   regression gate in CI, no `max_tokens`/iteration cap, no timeout, no
   fallback, no trace of prompt/completion/tokens, no schema on extraction,
   no retrieval metrics, judge never validated against humans.
4. **Trace, don't pattern-match.** Confirm the prompt actually renders what
   you think (run the template), confirm the parser actually handles refusals
   /truncation/`stop_reason`, confirm the "eval" actually gates merges rather
   than decorating a dashboard.
5. **Verify, then report.** State the concrete failure scenario (wrong answer
   shipped, runaway bill, silent regression on model bump). If unverified,
   say so and rate conservatively.

### Severity conventions

| Severity | Criteria | Examples |
|---|---|---|
| **Critical** | User-facing wrongness or unbounded damage with no detection/limit: consequential output (money, health, legal, code-exec) shipped with no eval and no human gate; agent loop with no iteration/cost cap; auto-upgraded model with no regression gate; prompt/completion logs leaking secrets or PII wholesale | `while True:` tool loop, no budget; prod extraction parsed with regex from free text feeding payments; `model="latest"` with zero evals |
| **High** | Silent quality/cost failure likely in normal operation: no eval suite on a shipped LLM feature; parse-and-pray JSON (no schema/validation); RAG with no retrieval eval or no grounding; judge-as-metric never validated; no retry/backoff/fallback on a user-facing path; cache-busting prompt structure tripling spend | `json.loads(response.text)` with no repair/reject path; timestamp interpolated at top of system prompt; recall@k never measured |
| **Medium** | Degraded quality/efficiency or weakened safeguards: golden set <20 cases or stale; eval not in CI; no pairwise/error analysis discipline; missing `stop_reason` handling; unpinned embedding model version; few-shot examples contradicting instructions; no streaming on long user-facing outputs | Eval exists but only run manually; chunking by fixed chars across tables; temperature/params copy-pasted without rationale |
| **Low** | Hygiene/debt: prompts unversioned outside repo; no token-count telemetry; missing batch API on offline workloads; verbose few-shot inflating cost; TODO repair loops | Prompt edited in a dashboard, not git; offline summarizer paying real-time prices |

Adjust one band up/down for context: consequential domain (↑), internal
prototype behind a flag (↓), volume/blast radius (↑ at scale), compensating
human review (↓).

### Finding format

```
[SEVERITY] <title>
File: <path>:<line>
Rule: rules/<NN> §<section>
Failure scenario: <what concretely goes wrong, for whom, at what scale/cost>
Evidence: <code/config/trace anchoring the claim>
Fix: <specific change, referencing the rules/ pattern>
```

Order Critical→Low; lead with an executive summary (counts, worst finding,
systemic themes — "no evals anywhere" is one systemic finding, not twenty).

## Rules index

| File | Topics | Read this when... |
|---|---|---|
| [rules/01-evals.md](rules/01-evals.md) | Eval-first development, golden sets, assertion/rubric/pairwise evals, LLM-as-judge + judge validation, offline vs online, CI regression gates, production sampling into eval sets, error analysis, metric pitfalls (judge bias, contamination, **an arm blind to the treatment — its `+0.00` is structural, not a result**, and **a saturated measure — both arms at the ceiling is a fact about the instrument, never about the system**) | ...building ANY LLM feature (start here), changing a prompt/model, reviewing whether quality claims are real, setting up CI for an LLM repo |
| [rules/02-prompt-context-engineering.md](rules/02-prompt-context-engineering.md) | System prompt structure, instruction placement, self-contained prompts (inline schemas vs. out-of-context references that degrade to fabrication), few-shot selection, context budget management, caching-aware prefix design, prompt versioning/testing, injection-safe template interpolation, structured output (schema/tool-based) + validation/repair, **whole-document rejection as a recall control (salvage the valid remainder and record the drop) and the constant column that means the reader names a key the model never emits**, prompt rot | ...writing or editing prompts/templates, extraction or classification features, diagnosing cost spikes or cache misses, anything that parses model output |
| [rules/03-rag-retrieval.md](rules/03-rag-retrieval.md) | RAG vs long context vs fine-tuning, chunking strategies, embedding selection & versioning, hybrid retrieval (dense+lexical+rerank), query transformation, retrieval evals (recall@k, golden retrieval sets), grounding & citation, freshness/invalidation, index integrity (write-once security metadata, outlier quarantine, expiry filters), poisoning-resistant result shaping, agentic retrieval | ...building search/Q&A over documents, choosing a vector DB/embedding model, "the answers are wrong/stale", evaluating an existing RAG pipeline |
| [rules/04-agents-tools.md](rules/04-agents-tools.md) | Workflow vs agent decision, tool design (descriptions, scope, idempotency, model-actionable errors), context management across turns (compaction, memory), MCP integration & spec status, multi-agent costs, human-in-the-loop gates, stopping conditions & budgets | ...anything with tool calls or loops, designing tool schemas, MCP servers/clients, multi-agent proposals, runaway-cost or stuck-agent debugging |
| [rules/05-production-engineering.md](rules/05-production-engineering.md) | Model selection & routing, capability tiers, fallbacks, provider abstraction caution, latency (streaming, parallel calls, caching), cost engineering (budgets, batch APIs, right-sizing), 429/529 + jittered backoff, LLM observability (trace every call), graceful degradation and an inference kill switch, versioning & rollout (shadow, A/B, pinning vs auto-upgrade), generated-media provenance (C2PA) and likeness consent | ...shipping to production, picking models, cost/latency complaints, retry/fallback design, rollout of a new model or prompt, building dashboards |
| [rules/06-data-lifecycle.md](rules/06-data-lifecycle.md) | Fine-tune vs prompt vs RAG decision, dataset curation hygiene, training-side safety (content filtering, reward hacking, feedback poisoning, label logs), feedback loops (thumbs → eval sets), embedding/index migration, PII in prompts/logs, provider data-retention settings | ...someone proposes fine-tuning, designing feedback capture, migrating embedding models, setting up logging/retention for an LLM app |

## Top-10 non-negotiables

Violations are findings regardless of context; in BUILD mode they are never
acceptable shortcuts:

1. **No LLM feature ships without an eval.** Minimum: a versioned golden set
   with graded criteria, runnable by one command, gating CI. (rules/01)
2. **Every prompt/model/parameter change runs the evals before merge.**
   "It looked better on three examples" is not evidence. (rules/01)
3. **LLM-as-judge is itself validated** against human labels (agreement
   measured, bias checked) before its scores are trusted. (rules/01)
4. **Machine-consumed output is schema-constrained** (structured output API /
   tool call), validated, with a bounded repair-or-reject path — never
   regex/parse-and-pray on free text. (rules/02)
5. **User/retrieved content is data, not instructions**: typed template slots,
   delimited and labeled as untrusted; never f-string-concatenated into the
   instruction stream. (rules/02 + sota-code-security rules/08)
6. **Every agent loop has explicit stopping conditions**: max iterations, max
   tokens/cost, wall-clock timeout — and human gates on consequential
   actions. (rules/04)
7. **RAG answers are grounded or refused**: retrieval quality measured
   (golden retrieval set, recall@k), answers cite sources, and "not in the
   corpus" is an honored outcome. (rules/03)
8. **Every model call is traced**: prompt/completion (with redaction), token
   counts, latency, model ID, cache hits, cost — linked to eval/run IDs.
   (rules/05)
9. **Production model versions are pinned and rolled out deliberately**
   (shadow or A/B with eval gates) — never silent auto-upgrade. (rules/05)
10. **429/529/timeout handling is explicit**: jittered exponential backoff
    honoring `retry-after`, idempotency on retried writes, a degradation
    path when the provider is down. (rules/05)
