---
name: agentic-iterative-rag
description: Use when a RAG request needs bounded multi-round evidence gathering with Critic-based sufficiency checks before returning an answer.
---

# SIM-RAG-Inspired Iterative RAG

Use this immutable Agentic Skill to run a bounded retrieve-generate-critique
loop. It borrows SIM-RAG's inference architecture, but does not reproduce its
Self-Practicing, Critic training, rationale generation, or experiments.

## Contract

- Bind exactly one retriever, generator, and critic.
- Optionally bind one rewriter and one reranker.
- Keep the user's original query for reranking, generation, and critique.
- Treat rewritten queries as retrieval aids, never as evidence.
- Return an answer only when the Critic approves a direct, non-abstaining answer.
- Require evidence for every fact or reasoning hop needed by the answer.
- Regenerate once with the same evidence when a rejection is clearly about
  answer form only; ambiguous or evidence-related rejections continue retrieval.

## Component selection

- Prefer BM25 for exact names, dates, titles, identifiers, and questions with
  strong lexical overlap with the corpus.
- Prefer Vector retrieval when paraphrases, synonyms, or semantic similarity
  are more important than exact token overlap.
- Use HyDE only with Vector retrieval, and only when a concise hypothetical
  passage is likely to bridge a vocabulary or intent gap. Never treat the HyDE
  passage as evidence.
- Use BGE Reranker when multi-hop reasoning, noisy candidates, or accumulated
  evidence make top-rank precision important.
- Leave optional slots empty when their expected retrieval benefit does not
  justify added model calls, latency, or local model cost.
- Always bind the required Generator and Critic after choosing the retrieval
  path.

## Request options

- `max_iterations` defaults to `3` and must be positive.
- `max_tokens` controls answer generation only.
- `critic_max_tokens` controls critique generation, defaults to `4096`, and
  must be positive.

## Follow-up retrieval

Use at most three concrete missing-evidence issues from the Critic, bounded to
160 characters each. Use bounded feedback only when no usable issue exists.
The trace exposes accumulated and newly added document IDs for every round.

## Answer regeneration

Treat Critic feedback as answer-form-only when it clearly requests a shorter,
more direct, or better-formatted answer and contains no missing-evidence signal.
Regenerate once in that iteration using the original question, bounded Critic
guidance, and the same accumulated evidence. Critique the revised answer again
before returning it. Mixed or unrecognized rejection reasons must continue the
normal retrieval loop.

Record a `regeneration` trace event with the original answer, bounded guidance,
revised answer, and revised Critic result. An approved revision stops with
`critic_approved_after_regeneration`.

## Safe stopping

Stop with `Insufficient evidence to answer reliably.` when the iteration limit
is reached or a rejected round contributes no new evidence. Treat generated
abstentions as rejected even if a model Critic mistakenly approves them.
