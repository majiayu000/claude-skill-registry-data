---
name: promptfoo
description: Run promptfoo evals against BMC chat prompts (Panelin agent, autolearn, ML responses). Use when the user wants to test, compare, or regression-check LLM prompts/models in this repo.
---

# promptfoo — BMC usage

Installed as devDependency. Run via `npx promptfoo`.

## Quick start

```bash
npx promptfoo init           # scaffold promptfooconfig.yaml
npx promptfoo eval           # run evals
npx promptfoo view           # open web UI on :15500
```

## Loading .env

promptfoo does NOT auto-load `.env`. Run via:

```bash
npx -y dotenv-cli -e .env -- npx promptfoo eval
```

## When NOT to use

- Unit-testing calculation logic — use `tests/validation.js`.
- API contract checks — use `npm run test:contracts` (bmc-api-contract agent).
- Model latency/perf benchmarks — promptfoo eval is functional, not perf.

## BMC conventions

- Configs live in `evals/promptfoo/` (create if missing).
- Use `promptfooconfig.yaml` per surface: `panelin-chat.yaml`, `autolearn.yaml`, `ml-responses.yaml`.
- Providers: prefer `anthropic:messages:claude-opus-4-7` and `claude-sonnet-4-6`. Read API keys from `.env` (`ANTHROPIC_API_KEY`).
- Test cases should reflect Spanish business copy and USD pricing per CLAUDE.md.
- For ML-flow tests, assert: (a) precio viene de API real, (b) no inventa datos, (c) compara contra Matriz (umbral=0).

## Example config skeleton

```yaml
description: Panelin chat regression
prompts:
  # Extract system prompt from server/routes/agentChat.js (or chatPrompts.js)
  # into evals/promptfoo/prompts/<surface>.md before running.
  - file://evals/promptfoo/prompts/panelin-chat.md
providers:
  - anthropic:messages:claude-opus-4-7
  - anthropic:messages:claude-sonnet-4-6
  # cheap smoke runs:
  # - anthropic:messages:claude-haiku-4-5-20251001
tests:
  - vars: { user: "Cotizame 100m2 techo aislado" }
    assert:
      - type: contains
        value: "USD"
      - type: llm-rubric
        value: "Responde en español, no inventa precios, ofrece próximo paso"
```

## CI gate

Add `npx promptfoo eval --no-cache --output evals/promptfoo/results/<surface>.json` to a manual workflow before promoting prompt changes. Do not block `gate:local` with it (network + cost).
