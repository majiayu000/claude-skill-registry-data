---
name: add-python-module
description: Add an endpoint, module or setting to the Python AI service (apps/ai) and call it from the API. Use when the user wants new AI, model, retrieval or data-science functionality, or anything written in Python.
---

# Add to the Python service

apps/ai is FastAPI plus a BullMQ worker; only apps/api calls it, through the generated
client in `packages/ai-client`. `docs/python-services.md` describes the service.

1. **Models.** Request and response models in `apps/ai/app/schemas.py`, every field
   constrained (`Field(min_length=…, max_length=…)`, `Literal[...]`). They become
   `apps/ai/openapi.json` and the TypeScript types.
2. **Logic.** A module in `apps/ai/app/` (like `summaries.py` or `documents.py`). Data
   access only through `tenant(org_id)` from `app/db/session.py`; models through Pydantic
   AI, so budgets and `AI_MODEL` apply.
3. **Route.** In `apps/ai/app/main.py`, with `operation_id="<name>"` (the generated
   client's function name) and `CallerDep` (the API's signed token). Errors are
   `AppError("<CODE>", status, params)` with a code from `packages/contracts/src/errors.ts`.
   Blocking work in a plain `def`; I/O in `async def`.
4. **Settings.** A field in `apps/ai/app/settings.py` with `alias="<ENV_NAME>"`, and the
   variable in `.env.example` and `docs/environment.md`.
5. `bun run gen`: regenerates `apps/ai/openapi.json` and `packages/ai-client/src/generated/`.
6. **Call it.** Add a method to `createAiClient` in `packages/ai-client/src/index.ts`
   (wraps the generated function with `unwrap`), then use it from
   `apps/api/src/modules/ai/ai.service.ts` behind a contract procedure (add-feature
   skill). Keep the API's input limits equal to the Pydantic ones; add the pair to
   `apps/api/src/modules/ai/limits.test.ts`.
7. **Tests.** Pure tests in `apps/ai/tests/test_units.py` (run by `bun run test`);
   anything needing Postgres or Redis in `apps/ai/tests/test_service.py`
   (`pytestmark = pytest.mark.integration`, run by `bun run test:integration`).
   `bun run lint` runs ruff and `bun run check-types` runs basedpyright on it.

Background work for the service: the add-job skill (Python section).

Finish with the verify skill, then the `python-reviewer` agent, the `security-reviewer`
agent for a new route (a new entry point), and the `reviewer` agent for the API side.
