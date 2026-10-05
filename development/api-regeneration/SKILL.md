---
name: api-regeneration
description: Regenerate TypeScript types after editing api.yml / connectionProfile.yml / connectionState.yml. Use whenever a spec file changes.
---

# Regenerating after spec edits

After any change to `api.yml`, `connectionProfile.yml`, or `connectionState.yml`, the generated TypeScript under `generated/` and `hub-sdk/generated/` is stale. Code that imports `../generated/model/index.js` will compile against the previous shape until you regenerate.

## Command

From the module directory:

```bash
zbb generate
```

That single task chains through `syncMeta → assembleSpec → bundleSpec → generate*`, rewriting:

- `generated/api/` — connector interface, tag APIs, operation wrappers, `manifest.json`
- `generated/model/` — `ConnectionProfile`, `ConnectionState`, resource types, enums
- `hub-sdk/generated/` — the typed client e2e tests import

You do not need to clean first — gradle's input-aware caching invalidates the right outputs. If gradle reports `UP-TO-DATE` after a spec edit, the spec file may not be staged for the task; run `zbb clean && zbb generate` to force.

## When to run

- After any commit-worthy change to `api.yml` (paths, components, security, examples)
- After editing `connectionProfile.yml` or `connectionState.yml`
- After updating a `$ref` target version (e.g. bumping `@zerobias-org/product-…`)
- Before invoking `:compile` or `:test` — both depend on `:generate` indirectly, so they'll trigger it themselves, but running `:generate` directly is faster for catching codegen errors early

You do **not** need to run it:

- While iterating on `api.yml` — finish the edit pass, then regenerate once
- For source-only edits in `src/` or `test/`
- To "just check" — gradle's daemon already knows what's stale

## What to look for in the output

```
> Task :<…>:syncMeta
> Task :<…>:assembleSpec
> Task :<…>:bundleSpec
> Task :<…>:generate
```

If `bundleSpec` fails with `Can't resolve $ref`:

- Inspect the offending reference; it's usually a path that needs a published dependency (e.g. `./node_modules/@zerobias-org/product-foo/catalog.yml#/Product`)
- Confirm `npm view @zerobias-org/product-foo version` returns something; if not, the dep needs publishing
- For module interface refs, use the bundled spec in the package's `dist/`, not the raw `api.yml`:
  ```yaml
  # CORRECT
  $ref: ./node_modules/@zerobias-com/interface-foo/dist/interface-foo.yml#/paths/...
  ```

If `generate` fails:

- Surface the codegen error verbatim — it usually points at a schema with conflicting types or an `operationId` that doesn't match `^[a-z][a-zA-Z0-9]+$`
- Don't hand-edit `generated/` to "fix" the error; that directory is gitignored and overwritten every run

## What it does NOT do

`:generate` doesn't run `:compile`, `:test`, or `:lint`. Those run on demand or as part of `:build` / `:gate`. Run them separately when you need them:

```bash
zbb compile              # tsc against src/, test/, generated/
zbb test --slot local    # mocha in-process
zbb build                # full lifecycle
```

## Common pitfalls

- **Editing `generated/` directly** — overwritten on next `:generate`. Make the change in `api.yml` instead.
- **Cleaning `hub-sdk/generated/` by hand** — same story. Gradle owns it.
- **Skipping `:generate` after spec edit** — `:test` will still pass against stale types and you'll get a confusing runtime error later. Always regenerate before testing a spec change.
- **Multiple `:generate` invocations** — fine; gradle caches. The cost is small.
- **CI failures with "spec drift"** — locally the daemon was warm and skipped a step. CI runs from cold; reproduce with `zbb clean && zbb build`.

## Related

- @.claude/skills/api-spec-core/SKILL.md — what makes a valid `api.yml`
- @.claude/skills/connection-profile/SKILL.md — `connectionProfile.yml` / `connectionState.yml` shape
- @.claude/skills/tool-requirements/SKILL.md — zbb command reference
- @.claude/skills/build-quality/SKILL.md — full lifecycle checkpoints
