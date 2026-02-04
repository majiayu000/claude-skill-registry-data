---
name: lcp-openai-serve
description: Develop apps/openai-serve (Go). Keep OpenAI gateway behavior correct and avoid logging prompts/outputs.
metadata:
  short-description: Work on the OpenAI-compatible gateway
---

You are working on the OpenAI-compatible HTTP gateway in `apps/openai-serve/`.

## Scope

- Module: `apps/openai-serve/`
- Runtime contract: `apps/openai-serve/README.md`

## Development principles

These are the consolidated rules that previously lived in `apps/openai-serve/AGENTS.md`:

1. Design for robustness. Keep modules aligned with SRP.
2. Use a ubiquitous language. Keep terminology consistent across code and docs.
3. Test-first. Prefer TDD when changing behavior.
4. Run golangci-lint v2. When changing code, run `make lint` and fix findings.
5. Use `cmp.Diff` in tests. Compare expected vs actual with `github.com/google/go-cmp/cmp.Diff`.
6. Make logging diagnosable. Logging level MUST be configurable (for example via env vars).
7. Prefer lnd libraries. Use lnd-provided APIs/libraries before re-implementing.

## Non-negotiables

- Logging is sensitive: do not log raw prompts (`messages[].content`) or raw model outputs.
- Keep behavior stable and explicit: JSON decoding is strict, unsupported fields must be rejected as documented.

## Workflow

1. Read `apps/openai-serve/README.md` before changing behavior.
2. When adding config/env vars, document them in `apps/openai-serve/README.md` and keep defaults sane.
3. When changing request/response structures, update tests and ensure the documented constraints still hold.

## Validation (run from `apps/openai-serve/`)

- `make test`
- `make lint`
- `make fmt`
