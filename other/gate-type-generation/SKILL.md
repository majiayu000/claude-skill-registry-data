---
name: gate-type-generation
description: Gate 2 — `zbb generate` succeeds and writes consumable TypeScript into generated/ and hub-sdk/generated/. Use after Gate 1, before Gate 3 implementation.
---

# Gate 2: Type generation

After Gate 1, `bundleSpec` produced a self-contained spec. Gate 2 runs the codegen and checks the output is shaped how the implementation and tests will need it.

## What to check

```bash
# 1. Regenerate from the spec
zbb generate
# Exit code must be 0.

# 2. Module-side generated/ exists and is populated
test -d generated/api   && ls generated/api/*.ts >/dev/null   || echo "✗ generated/api/ empty"
test -d generated/model && ls generated/model/*.ts >/dev/null || echo "✗ generated/model/ empty"
test -f generated/api/manifest.json                            || echo "✗ generated/api/manifest.json missing"

# 3. hub-sdk-side generated/ exists (used by test/e2e via describeModule<T>)
test -f hub-sdk/generated/api/index.ts                         || echo "✗ hub-sdk/generated/api/index.ts missing"

# 4. No inline-response leakage
grep -rln "InlineResponse\|InlineRequestBody" generated/ hub-sdk/generated/ 2>/dev/null && \
  echo "✗ Inline*Response types present — hoist inline schemas in api.yml"

# 5. Connector interface is present (for connector modules)
grep -E "export interface [A-Z][a-zA-Z]+Connector" generated/api/index.ts || \
  echo "✗ <Class>Connector interface not generated"

# 6. ConnectionProfile / ConnectionState model types present (connectors only)
test -f connectionProfile.yml && grep -q "export interface ConnectionProfile" generated/model/index.ts \
  || echo "  (skip: not a connector or model export shape changed)"

# 7. Module manifest agrees with package.json
jq -r .name package.json
jq -r '.operations | keys[]' generated/api/manifest.json | head
# Should map every operationId from api.yml to <Api>.<method>; missing entries mean spec/operations drifted.

# 8. No leftover stale files (after a forced clean)
git status --short generated/ hub-sdk/generated/ 2>/dev/null
# These directories are gitignored; output should be empty.
```

## Pass criteria

- `zbb generate` exits 0
- `generated/api/`, `generated/model/`, `hub-sdk/generated/api/` all populated
- `generated/api/manifest.json` exists and reflects every operationId
- No `InlineResponse*` / `InlineRequestBody*` types anywhere
- For connectors: a `<Class>Connector` interface exists and `ConnectionProfile` is exported from `generated/model/index.ts`

## On failure

The failing task tells you the cause:

- **`bundleSpec` failed inside `zbb generate`** — go back to Gate 1
- **`generateApi` failed** — codegen rejects a schema or operation. Read the error verbatim; the fix is in `api.yml`, never in `generated/`
- **`buildHubSdk` failed** — same root cause as above; the hub-sdk generator runs on the same bundled spec
- **`InlineResponse*` appears** — a response body has an inline schema. Hoist it:
  ```yaml
  # BEFORE
  '200':
    content:
      application/json:
        schema:
          type: object
          properties: { id: { type: string }, name: { type: string } }

  # AFTER
  '200':
    content:
      application/json:
        schema: { $ref: '#/components/schemas/Foo' }
  ```
- **Stale state** — `zbb clean && zbb generate` to force from cold

## Related

- @.claude/skills/api-regeneration/SKILL.md — what `zbb generate` runs and how to read its output
- @.claude/skills/gate-api-spec/SKILL.md — Gate 1
- @.claude/skills/gate-implementation/SKILL.md — Gate 3 (next)
- @.claude/skills/build-quality/SKILL.md — full lifecycle context
