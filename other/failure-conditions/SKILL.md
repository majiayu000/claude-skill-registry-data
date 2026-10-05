---
name: failure-conditions
description: Conditions that fail a /create-module or /add-operation task on contact. Use when scoping work, reviewing a PR, or refusing a request that violates a hard rule.
---

# Immediate failure conditions

A task fails on the spot if any of these are true. The fix is always the same: don't do the thing.

## Spec / codegen

1. **`describe*` operationId** — collides with mocha's BDD global. Rename to `get*`/`list*`/etc.
2. **4xx / 5xx response declared in `api.yml`** — the framework owns error mapping. Declare only 200/201.
3. **`nullable: true` anywhere in the spec** — codegen rejects it. Use `oneOf: […, { type: 'null' }]` or rethink the type.
4. **`Inline*Response*` / `Inline*RequestBody*` types in `generated/`** — `api.yml` has an inline schema in a request/response body. Hoist it to `components/schemas/` and `$ref` it.
5. **Schema used as a direct endpoint response *and* as a nested property of another schema, and it has 10+ properties** — generated types will balloon. Create a `<Name>Summary` for the nested case.
6. **Spec edit without re-running `zbb generate`** — implementation will compile against stale types. Always `zbb generate` after a spec change.

## Source code

7. **`Promise<any>` in any `src/` signature** — use the generated types from `../generated/api/*` and `../generated/model/*`.
8. **`process.env` access in `src/`** — credentials and config flow through `ConnectionProfile`. The only place that may read `process.env` is `test/e2e/constants.ts`.
9. **Relative imports missing `.js` extension** — ESM under `module: NodeNext` rejects them.

## Tests

10. **`jest.mock`, `sinon`, `fetch-mock`, or `msw` anywhere** — nock is the only mocking library. `import nock from 'nock'` (default import).
11. **`test/integration/` directory** — that layout is gone. e2e tests live in `test/e2e/` and use `describeModule<T>` from `@zerobias-org/module-test-client`.
12. **Hardcoded test values (IDs, orgs, repos) in `test/e2e/` or `test/unit/`** — every env-driven value lives in `test/e2e/constants.ts` with a sensible default, and tests skip when empty.
13. **`process.env` outside `test/e2e/constants.ts`** — same rule as for `src/`, with the one designated exception.
14. **`dotenv` import anywhere** — `zbb env set` and `zbb secret create` manage env state. The dependency is gone.
15. **Skipped *unit* tests** — `it.skip()` / `describe.skip()` to dodge a problem is forbidden. Fix the impl or the mock. Suite-level `this.skip()` is reserved for e2e tests when a required env constant is empty.
16. **`test/e2e/*.test.ts` without `CoreError.deserialize` as the third arg to `describeModule`** — without it, errors thrown across the wire arrive as plain objects instead of `NotFoundError` etc.

## Build / packaging

17. **`npm-shrinkwrap.json` in the module directory** — delete it. CI runs `npm ci` against `package-lock.json`.
18. **`gate-stamp.json` missing or stale at commit time** — CI's only check is `zbb gateCheck` against the committed stamp. Run `zbb gate --slot local` and commit the result.
19. **Module package not in `@zerobias-org/` scope** — module packages don't move. Products are `@zerobias-org/product-*`; modules are `@zerobias-org/module-*`.
20. **`package.json` missing `"type": "module"`** — the module is ESM. The generator sets this; never remove it.

## Workflow scope

21. **Editing files outside the target module path** — one module at a time. `package/<vendor>/[<suite>/]<service>/` and `gate-stamp.json` are the only paths a module-scoped commit may touch.
22. **Re-running the generator on an existing module to "fix" something** — the generator throws when the destination exists, and rightly so. Edit the files in place.

## Lifecycle

23. **Tests written but not run** — `zbb test` and `zbb testDirect` must exit 0; for connectors, `zbb testDocker` too. The stamp is the proof.
24. **Build not run from cold before claiming completion** — `zbb gate --slot local` re-runs from cold. Anything green only in a warm daemon is suspect.

## Signals you (or a user) shouldn't have to send

If you find yourself having to say any of these to an agent, the agent failed:

- "Now write tests"
- "Did you regenerate after editing the spec?"
- "Run `zbb lint`"
- "Commit the gate stamp"
- "Move that ID out of the test file"
- "Drop dotenv"

The right shape of a completion message is: "Gates 1–6 green. `gate-stamp.json` written and staged. PR-ready."

## Gate ordering

Gates run in sequence. Don't skip ahead:

```
Gate 1: API spec       → assembleSpec / bundleSpec
Gate 2: Type gen       → generate*
Gate 3: Implementation → compile + lint
Gate 4: Test creation  → unit + e2e files present
Gate 5: Test execution → zbb test / testDirect / testDocker
Gate 6: Build + stamp  → zbb gate, gate-stamp.json committed
```

A failure at any gate is final until fixed. Gate N+1 doesn't run.

## Related

- @.claude/skills/gate-api-spec/SKILL.md … @.claude/skills/gate-build/SKILL.md — checklists per gate
- @.claude/skills/completion-checklist/SKILL.md — the positive form of this file
- @.claude/skills/production-readiness/SKILL.md — extra checks before publish
