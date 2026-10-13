---
name: swap-llm
description: Change which language model the AI service uses (Anthropic, OpenAI, another provider, a local model, or an LLM gateway such as LiteLLM), or add a fallback. Use when the user decides on a different or cheaper model, or a gateway. Not for debugging; when something fails, use the debug skill.
disable-model-invocation: true
---

# Swap the model

- **Seam:** a Pydantic AI model name. `create_model(name, fallback)` in
  `apps/ai/app/assistant.py` builds the assistant's model (a `FallbackModel` when a
  fallback is set); `create_summaries` in `apps/ai/app/documents.py` uses the same
  setting for document summaries.
- **Today:** `local:extractive` locally (quotes the best passage, no model or key;
  refused in production by `apps/ai/app/settings.py`).
- **Env:** `AI_MODEL`, `AI_FALLBACK_MODEL`, and the provider's own key, which Pydantic AI
  reads from the environment (e.g. `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`). Budgets:
  `AI_MONTHLY_TOKENS_PER_ORG`, `AI_TOKENS_PER_RUN`. Unset `AI_MODEL` turns the assistant
  off.

## Swap

1. Any provider Pydantic AI supports: set `AI_MODEL` (e.g. `anthropic:claude-sonnet-5`,
   `openai:gpt-5`) and its key: locally `bun run env:set`, deployed in
   the ai service's SOPS Secret (rotate-secrets skill). No code.
2. A gateway with an OpenAI-compatible API (LiteLLM and most routers):
   `AI_MODEL=openai:<model the gateway serves>`, with `OPENAI_BASE_URL` and
   `OPENAI_API_KEY` pointing at the gateway. No code.
3. Something Pydantic AI doesn't support: add a branch in `create_model` returning a
   `pydantic_ai.models.Model`, like `_local_extractive()`.
4. Measure before switching production: `bun run --cwd apps/ai evals` against the
   new model (CI runs them nightly with the `EVAL_MODEL` variable).

## Tests

`apps/ai/tests/test_units.py` and `apps/ai/tests/test_service.py` run on
`local:extractive`; `apps/ai/tests/test_evals.py` checks the evals themselves.

## Finish

1. The verify skill.
2. Ask the `reviewer` agent to review the change, and the `security-reviewer` agent: a
   new implementation brings its own credentials and sends data somewhere new. If you
   wrote a migration, the `migration-reviewer` agent too. The change is in apps/ai, so the
   `python-reviewer` agent as well.
3. Update the seam's row in the README's "Scaling path" table if what's "Now" changed.
