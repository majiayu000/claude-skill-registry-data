---
name: gate-api-spec
description: Gate 1 — api.yml + connectionProfile.yml + connectionState.yml are well-formed and will bundle. Use after API design, before invoking `zbb generate`.
---

# Gate 1: API specification

The spec must satisfy three things:

1. **It bundles** — `zbb bundleSpec` exits 0 (every `$ref` resolves, no syntax errors).
2. **It encodes the right shape** — direct response objects, camelCase, no envelopes, no error responses declared, no `nullable`.
3. **It refers to the right packages** — `@zerobias-org/product-*` for product info, `@zerobias-com/types-core` for shared schemas.

Gate 2 (type generation) will catch anything Gate 1 missed, but most of the work is cheaper to catch here.

## What to check

Run from inside the module directory:

```bash
# 1. Bundling — the load-bearing check
zbb bundleSpec
# Exit code must be 0.

# 2. Forbidden tokens in api.yml
grep -E "describe[A-Z]"                     api.yml   # describeFoo collides with mocha BDD globals
grep -E "'40[0-9]'|'50[0-9]'"               api.yml   # No 4xx/5xx response declarations
grep -E "^\s*[a-z]+_[a-z]"                  api.yml   # No snake_case property names
grep "nullable:"                             api.yml   # Not supported by the codegen
grep -E "name: (apiKey|token|baseUrl|organizationId|region)" api.yml
                                                      # Connection context belongs in ConnectionProfile, not on operations
# Each grep must print nothing.

# 3. Response shapes — no envelope/wrapper responses
yq '.paths.*.*.responses.*.content.*.schema | select(has("properties"))' api.yml
# Should print business object schemas only, never response wrappers
# (status, data, meta, response, result, caller, token, etc.).

# 4. operationId hygiene (codegen contract: ^[a-z][a-zA-Z0-9]*$)
yq '.paths.*.*.operationId' api.yml | grep -vE '^- "?[a-z][a-zA-Z0-9]*"?$'
# Should print nothing.

# 5. Every operation references a 200/201 response with a $ref schema
yq '.paths.*.* | select(has("responses")) | .responses."200".content."application/json".schema' api.yml
# Should print $ref entries, not inline schemas.

# 6. Connector-only: connectionProfile.yml exists and is non-empty
if [ -f connectionProfile.yml ]; then
  yq '.type' connectionProfile.yml | grep -q 'object' || echo "✗ connectionProfile.yml shape"
fi

# 7. Optional: connectionState.yml extends baseConnectionState when present
if [ -f connectionState.yml ]; then
  grep -q "baseConnectionState\|expiresIn:" connectionState.yml || \
    echo "✗ connectionState.yml must extend baseConnectionState or declare expiresIn"
fi
```

## Schema-context separation (heads-up, not a hard fail)

A schema used both as a direct response *and* as a nested property of another schema can confuse the codegen and the API consumer (large summary types embedded everywhere). When found, consider a `<Name>Summary` for the nested case.

```bash
nested=$(yq '.components.schemas[] | .. | select(type == "string" and test("#/components/schemas/")) \
            | capture("#/components/schemas/(?<schema>.+)").schema' api.yml | sort -u)
endpoints=$(yq '.paths.*.*.responses.*.content.*.schema["$ref"]' api.yml | grep -o '[^/]*$' | sort -u)

comm -12 <(echo "$nested") <(echo "$endpoints") | while read schema; do
  prop_count=$(yq ".components.schemas.${schema}.properties | length" api.yml)
  if [ "${prop_count:-0}" -gt 10 ]; then
    echo "warn: '${schema}' used in nested + direct contexts (${prop_count} properties) — consider ${schema}Summary"
  fi
done
```

## Pass criteria

- `bundleSpec` exits 0
- All forbidden-token greps return empty
- Every response schema is a `$ref`, never inline
- Every operation has a 2xx response (200 or 201)
- `connectionProfile.yml` is well-formed (if module is a connector)
- `connectionState.yml`, if present, extends `baseConnectionState.yml` (or declares its own `expiresIn`)

## On failure

Fix the spec, do **not** patch around it in `generated/` (which is gitignored and overwritten on next `zbb generate`). Common shapes:

- `Can't resolve $ref './node_modules/@…/…'` — dependency missing or version not published; fix `package.json` and rerun
- `Inline schema in response 'getFoo' 200` — hoist to `components/schemas/` and `$ref` it
- `operationId 'list_users' is invalid` — rename to `listUsers`
- `Response 401 / 404 / 500 declared` — remove; the codegen owns error mapping

## Related

- @.claude/skills/api-spec-core/SKILL.md — base OpenAPI rules
- @.claude/skills/api-critical-12/SKILL.md — the 12 codegen-blocking rules
- @.claude/skills/api-linting/SKILL.md — what bundleSpec/redocly check
- @.claude/skills/api-regeneration/SKILL.md — what to run after fixing
- @.claude/skills/connection-profile/SKILL.md — connectionProfile/State shape
