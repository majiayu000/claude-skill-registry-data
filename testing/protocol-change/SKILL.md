---
name: protocol-change
description: Change agent-office's public contracts — AgentEvent fields, inbox/reply/messages HTTP APIs, the IPC contract (AgentOfficeApi, ServerMessage), or the hook's output. Use whenever packages/shared/src/{protocol,desktop-api,ipc-channels}.ts or an /api route's request/response shape changes.
---

# Change a public contract (additive only)

External agents and installed hooks depend on these shapes. See `ARCHITECTURE.md`.

1. **Red** — add a case to `packages/shared/src/index.test.ts` for the new field/shape. The compatibility guard (`{agentId}` alone parses; unknown fields ignored) must stay green.
2. **Green** — add the field as **optional** in the zod schema / type. Never rename, remove, retype, or make a field required.
3. **Core** — if it's agent state: merge logic + tests in `packages/core/src/domain/agent.ts` (`applyEvent` merges only defined fields; add it to the visible fields if it should trigger an upsert).
4. **Adapters** — HTTP route + `packages/adapters/src/http/http-api.test.ts` (400 for invalid input, success path); IPC handler + `packages/desktop/src/main/ipc-api.test.ts` and the preload bridge.
5. **Renderer** — reducer (`web/src/app/state.ts`) and view-model tests, then rendering (`adapters/three/avatar.ts`, `adapters/dom/*`) with `textContent` only.
6. **E2E** — extend the relevant `packages/adapters/test/e2e.*.test.ts`; for IPC, a spec in `packages/desktop/e2e/`.
7. **Docs** — README schema tables and examples.
8. `make check` and `make build test-ui`.

A breaking change is only allowed with an explicit major-version note in the README and the user's agreement.
