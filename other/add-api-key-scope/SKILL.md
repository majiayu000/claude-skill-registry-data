---
name: add-api-key-scope
description: Let workspace API keys call a procedure, with a new or existing scope. Use when the user wants third parties or scripts to reach a feature over the REST API (/api/v1) with an API key.
argument-hint: <resource:read|write>
---

# Add an API-key scope

A key may call only procedures whose contract names a scope it has; every other
procedure is for signed-in people. docs/auth.md, "API keys", has the model.

1. **Should keys reach it?** Only data a third party should read or change. Never
   account settings, members, billing, keys or webhooks management: those stay
   scope-less.
2. **The scope.** Reuse one in `API_KEY_SCOPES` (`packages/contracts/src/api/scopes.ts`)
   or add `<resource>:read` / `<resource>:write` there. Its description,
   `workspace.apiKeys.scopes.<scope>`, goes in every `packages/i18n/messages/*.json`: the
   settings page lists it.
3. **The procedure.** `base.meta({ apiKeyScope: "<scope>" })` on it in the contract
   (`packages/contracts/src/api/<area>.ts`), like the todo procedures. It needs a REST
   route (`.route({ method, path })`) to be reachable at `/api/v1`.
4. `bun run gen`: the OpenAPI document shows the scope.
5. **Test** in `apps/api/test/api-keys.integration.test.ts`: a key with the scope gets
   the data of its own workspace only, one without it gets `FORBIDDEN`.

## Done when

`bun run check-types`, `bun run test` and `bun run test:integration` pass, the
regenerated `apps/api/openapi.json` is in the change, and the `security-reviewer` agent
reports nothing blocking.
