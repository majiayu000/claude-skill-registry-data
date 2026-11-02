---
name: build-llm-seam
description: Use when adding the first LLM call to a service, or when model calls are scattered through it — one module owns every call - model tiers from config, retries, validated structured output, streaming, prompt caching, OTel gen_ai spans with cost, versioned prompt files, PII redaction.
---

# Build the LLM Seam

Every model call in the codebase goes through one module. Call sites say *what* they want (a task, a tier, a prompt name, a schema); the seam decides *how*: which model, how long to wait, when to retry, what to log, what to redact. A vendor swap, a model upgrade or a cost cap is then a one-file change. Provider default: `ai.provider` in the profile (`anthropic`).

## 1. Audit current state

Read `.claude/stack-profile.md` (`languages`, `backend.track`, `ai.provider`, `observability.otel`, `tests`). If absent, detect from lockfiles and manifests per [stack-profile.md](../../core/_shared/stack-profile.md). Then change nothing and look:

```bash
grep -rnE "from ['\"](@anthropic-ai/sdk|openai|@google/genai)|^(import|from) (anthropic|openai)" src | grep -v "platform/llm"   # SDK use outside the seam
grep -rnE "claude-(opus|sonnet|haiku|fable)-|gpt-[0-9]|gemini-[0-9]" src | grep -v "platform/llm"                            # hard-coded model ids
grep -rnE "max_tokens|maxTokens|temperature" src | grep -v "platform/llm"                                                  # per-call knobs
ls src/platform/llm prompts config/llm.models.json 2>/dev/null
grep -rn "ANTHROPIC_API_KEY\|OPENAI_API_KEY" src | grep -v "src/config"                                                      # keys read outside config
```

Report: SDK imports and model ids outside the seam, system prompts built as strings in code, calls without a timeout or `max_tokens`, no usage logging, user text sent as-is.

## 2. Decide what to do

- No seam, no calls yet → full install (steps 4–6).
- Calls scattered → install the seam, then migrate call sites one feature at a time (step 6). The grep in step 1 is the progress meter.
- Seam present → check it against [seam-patterns.md](./seam-patterns.md) rule by rule and apply only the delta.
- Greps clean, `Verify` passes → "already in place".
- The repo is browser-only (no server): stop. A model key must not ship to a browser; add a server first ([backend skills](../../backend/_shared/service-layout.md)).

## 3. Detect track

| Signal | Branch |
|---|---|
| `languages` has `typescript`; Hono or plain Node | [llm-seam-ts.md](../_shared/llm-seam-ts.md) at `src/platform/llm/` |
| `backend.track: nextjs` | Same code at `src/server/llm/` with `import 'server-only'`; call it from Server Actions and route handlers only |
| `backend.track: fastapi` or `languages` has `python` | [llm-seam-py.md](../_shared/llm-seam-py.md) at `src/<pkg>/platform/llm/` |
| `backend.track: go` | Same shape: a `LlmAdapter` interface, one adapter file, the error taxonomy and the retry policy from [seam-patterns.md](./seam-patterns.md); use the official Go SDK in the adapter only. No canonical code here |
| `ai.provider` other than `anthropic` | Write one new adapter implementing `LlmAdapter`; nothing else changes. Map that SDK's errors to `LlmError` |

Model ids and prices differ per provider, so `config/llm.models.json` names the provider it is for.

## 4. Install only what's missing

```bash
pnpm add @anthropic-ai/sdk zod @opentelemetry/api        # TypeScript
uv add anthropic pydantic opentelemetry-api              # Python
```

Add `ANTHROPIC_API_KEY` to the service's validated config (`src/config.ts` or `config.py`, see [config.md](../../backend/_shared/config.md)): required, no default, typed as a secret. Nothing else reads it. Tracing bootstrap is already there when `observability.otel` is true ([observability.md](../../core/_shared/observability.md)); the seam only uses the API.

## 5. Generate the seams

Copy the files from the canonical page, then edit only these:

| File | Edit |
|---|---|
| `config/llm.models.json` | Provider, tier to model id, effort, prices. Verify ids and prices against [stack-versions.md](../_shared/stack-versions.md) and the live pricing page before committing |
| `prompts/<name>.md` | One file per prompt; `version` in the frontmatter; `cache: true` only for a prompt with no variables |
| `src/platform/llm/redact.ts` | Add patterns for identifiers your domain carries (customer numbers, ticket ids). Pattern redaction does not find names |

Defaults: tiers `quality` = `claude-opus-5-5`, `balanced` = `claude-sonnet-5-5`, `fast` = `claude-haiku-5-5`. `claude-fable-5-1` is not a default tier (price, 30-day retention requirement); add it as a fourth tier only after an eval shows the gain.

## 6. Wire it up

1. `main` loads the config once and builds the seam ([composition root](../_shared/llm-seam-ts.md#composition-root)); services receive `llm` as an argument.
2. Move each call site: replace the SDK call with `llm.generate({ task, tier, prompt: { name }, messages, schema, maxTokens, pii })`. Move system text into `prompts/<name>.md`. Put user-supplied and retrieved text in `messages`, never in the prompt file.
3. Ban the SDK outside the seam, so the bug cannot come back. Biome (verified on 2.5.15): `linter.rules.style.noRestrictedImports` with `paths: { "@anthropic-ai/sdk": "…" }`, turned off by an `overrides` entry for `src/platform/llm/**`. Ruff: `[lint.flake8-tidy-imports.banned-api] "anthropic".msg = "…"` plus `per-file-ignores` for `src/app/platform/llm/**` (rule `TID251`). Snippets: [seam-patterns.md](./seam-patterns.md#rule-the-sdk-is-banned-outside-the-seam).
4. Add the grep from step 1 to the task runner as `check:llm-seam`, run in CI.

## 7. Verify

```bash
pnpm typecheck && pnpm vitest run tests/llm.test.ts     # Python: uv run pyright && uv run pytest tests/test_llm.py
grep -rnE "claude-(opus|sonnet|haiku|fable)-|from ['\"]@anthropic-ai/sdk" src | grep -v platform/llm   # expect: no output
```

Expected: type-check clean; the test file shows the fake adapter receiving redacted text, a computed cost, a retry on `overloaded` and no retry on `bad_request`; the grep prints nothing.

With a real key (one paid call, a few cents), call the same cacheable prompt twice within five minutes with a prefix of at least the cache minimum. In your tracing UI the second span shows `gen_ai.usage.cache_read.input_tokens` above zero and a lower `app.llm.cost_usd`. Zero means a silent cache invalidator: see [seam-patterns.md](./seam-patterns.md#rule-cache-the-stable-prefix-and-prove-it).

## References
- [seam-patterns.md](./seam-patterns.md): the rules and why.
- [llm-seam-ts.md](../_shared/llm-seam-ts.md), [llm-seam-py.md](../_shared/llm-seam-py.md): canonical code.
- [llm-security.md](../_shared/llm-security.md): trust boundaries and the OWASP LLM Top 10 map.
- [stack-versions.md](../_shared/stack-versions.md): model ids, prices, SDK lines, verified 2026-10-09.
- [engineering-principles.md](../../core/_shared/engineering-principles.md), [observability.md](../../core/_shared/observability.md), [logging-contract.md](../../core/_shared/logging-contract.md).
