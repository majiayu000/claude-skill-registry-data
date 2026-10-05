---
name: api-linting
description: How OpenAPI specs are linted in this repo. Use when diagnosing a `bundleSpec` failure or understanding what rules the toolchain enforces.
---

# API linting

OpenAPI linting runs as part of gradle's `:assembleSpec` / `:bundleSpec` / `:generate` chain. There is no separate "lint api" step a developer invokes by hand. If those gradle tasks succeed, the spec is good for codegen and publishing.

## What the toolchain actually checks

| Layer                            | Where it runs                              | What it catches                                              |
|----------------------------------|--------------------------------------------|--------------------------------------------------------------|
| Redocly (`@redocly/cli`)         | `assembleSpec` / `bundleSpec`              | Structural errors, unresolved `$ref`s, malformed YAML, invalid OpenAPI 3.0.x. |
| `bundleSpec` ($ref inlining)     | `bundleSpec`                               | Whether every reference can be inlined into a self-contained spec. |
| Codegen rules                    | `generate*`                                | Operation IDs, schema names, response shapes the generator can't translate. |
| Module-specific spectral rules   | Generator pins `@redocly/cli` but does not ship a `.spectral.yml`. Existing modules with custom spectral configs run via `lintExec`. | Style rules for naming, descriptions, etc. |

For a fresh module, **none** of the above require a `.spectral.yml` in the module directory — the defaults are sufficient. Only add one if you need to override a redocly rule for that specific module (rare, document why).

## Running it

```bash
zbb bundleSpec
```

That's the cheapest "is my spec valid?" check. Failures are usually one of:

- **`Can't resolve $ref './node_modules/@…/…'`** — the dependency isn't installed, or the path is wrong, or you're referencing a raw `api.yml` from another module instead of its `dist/module-….yml`.
- **`Required property '…' is missing`** — schema violates OpenAPI 3.0.3.
- **`Operation 'getXxx' must have …`** — codegen-enforced shape (operationId pattern, required success response, etc.).

Read the redocly output verbatim; it points at the offending line and column. Don't paper over it with `redocly bundle … --force` — `--force` ignores unresolved refs, and the generator will then choke trying to consume the broken bundle.

## Rules the redocly+codegen pipeline enforces de-facto

Without any custom `.spectral.yml`, the spec is rejected if it:

- Uses inline schemas in response bodies (codegen emits `InlineResponse200` types — surface as `Gate 2: Type Generation` failures). Every response body must `$ref` a named component.
- Omits `operationId` on any operation. Codegen wraps operations by `operationId`.
- Uses `operationId` containing characters outside `[a-zA-Z0-9]` or not starting with a letter.
- Uses `nullable: true` (OpenAPI 3.0.x specific; the codegen rejects this — use `oneOf: […, { type: 'null' }]` or rethink the type).
- Defines explicit 4xx / 5xx responses (the codegen owns error mapping; declare only the success response).
- Names a parameter or schema starting with `describe` (collides with mocha's BDD globals in test files that import generated types).

The agent audit grep for these is in `@.claude/skills/tool-requirements/SKILL.md` ("Forbidden tokens in api.yml").

## Adding a `.spectral.yml` (only if you need to)

Most modules don't need one. Add it only when:

1. You want to enforce a style rule beyond redocly's defaults (e.g. require examples on all 2xx responses for one specific module).
2. A redocly rule legitimately doesn't fit the API in question and needs to be silenced for *that module only*.

Template:

```yaml
extends:
  - "./node_modules/@zerobias-org/util-spectral-config/rules/.oas3.strict.spectral.yml"

rules:
  # Override or add module-specific rules here, with a comment explaining why
  # operation-description: warn
```

Wire it into the gradle build by referencing it from the module's `build.gradle.kts` config block (if the `zb.typescript-connector` plugin doesn't pick it up automatically — current versions do).

## What the build does NOT enforce automatically

The toolchain catches structural and codegen problems. It does **not** catch:

- Tag consistency across operations (e.g. mismatched `tags:` field across endpoints that conceptually belong together)
- Whether `x-product-operations` covers every operation
- Domain naming (e.g. is `listUsers` really the right operationId for that endpoint?)
- Pagination style choice (page-number vs token vs cursor)

Those are review-level concerns. `@api-reviewer` covers them; the codegen doesn't.

## Common failure shapes

- **`Can't resolve $ref ./node_modules/@zerobias-org/product-…/catalog.yml#/Product`** — `npm view` first. If the version exists, ensure the dep is in `dependencies` of the module's `package.json`. The generator template pins it to `"latest"`; pin to an exact version once you know which one you're using.
- **`InlineResponse200` types appearing in `generated/`** — spec has an inline schema in a response body. Hoist it to `components/schemas/` and `$ref` it.
- **`operationId 'list-users' is invalid`** — must match `^[a-zA-Z][a-zA-Z0-9]*$`. Use `listUsers`.
- **`Tag 'Users' used but not defined globally`** — add it to the spec's top-level `tags:` array.

## CI behavior

CI runs `:gateCheck`, not the build. The committed `gate-stamp.json` carries proof that `bundleSpec` and `generate` succeeded locally. So a spec that lints clean on your machine is also clean in CI; CI doesn't independently re-lint.

## Related

- @.claude/skills/api-spec-core/SKILL.md — what makes a valid OpenAPI 3.0.3 spec
- @.claude/skills/api-critical-12/SKILL.md — the 12 rules a spec must satisfy
- @.claude/skills/api-regeneration/SKILL.md — what `:generate` actually does
- @.claude/skills/build-quality/SKILL.md — lifecycle context
