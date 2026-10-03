---
name: authz-schema-sync
description: Sync packages/authz-rpc with lightbridge-authz's authz.cstack schema and regenerate the TypeScript client. Use whenever a task mentions a new or changed RPC procedure, cratestack, authz.cstack, generated/ types being missing or stale, a codegen version bump, or a type error naming a procedure or input the console calls.
---

# Syncing the authz RPC schema

`packages/authz-rpc/generated/` is **gitignored** and **cratestack-generated**. Never hand-edit it,
and never assume a warm local tree proves anything about CI.

Backend source of truth: `lightbridge-authz`'s `schema/authz.cstack` on **its `main` branch**.

## The sequence

### 1. Copy the schema from lightbridge-authz `main`

```sh
# From a lightbridge-authz checkout, read main directly — do not trust a feature branch
git -C /Users/selast/dev/gis/lightbridge-authz show origin/main:schema/authz.cstack \
  > packages/authz-rpc/schema/authz.cstack
```

If the procedure you need is not in `origin/main` yet, **stop**: the console cannot ship against a
schema the backend has not merged. Say so and take the dependency.

### 2. Wipe and regenerate — wipe is not optional

```sh
rm -rf packages/authz-rpc/generated
pnpm --filter @lightbridge/authz-rpc codegen
```

The generator does not remove files for symbols that disappeared. Regenerating over a populated
directory leaves orphans that still typecheck locally and do not exist in CI.

### 3. Fix the `Create*Input` helpers

The TypeScript codegen keeps `@readonly` fields **required** on `Create*Input`, unlike the Rust
side. Every `build*Input` helper in `apps/console/src/containers/build-create-*.ts` exists to paper
over exactly that. After a schema change, re-check them — a new `@readonly` field is a new required
property the console must supply or the build breaks.

### 4. Typecheck the whole workspace, not just the package

```sh
pnpm -r typecheck
pnpm --filter @lightbridge/authz-rpc test
pnpm --filter console test
pnpm --filter console build:web
```

## The CI trap this skill exists for

`generated/` is gitignored **and** `postinstall` runs `codegen:all`, which means:

- A **warm** local tree keeps working after a generator version bump, because the old output is
  still on disk.
- **CI is always cold**, so it regenerates with the new generator and breaks.

**After any bump of `@cratestack/cli` or `@cratestack/api`/`@cratestack/cbor`, you must
`rm -rf packages/authz-rpc/generated`, regenerate, and run the real build.** A green
`pnpm -r typecheck` on a warm tree proves nothing about that bump.

The same applies to `packages/api-rest` (Hey API / OpenAPI): also generated, also do-not-hand-edit.

## Pitfalls

- **`pnpm install` runs codegen via `postinstall`.** If `generated/` is missing after a fresh clone
  and typecheck fails, run `pnpm --filter @lightbridge/authz-rpc codegen` before debugging anything
  else.
- **A version bump must move `@cratestack/cli`, `@cratestack/api` and `@cratestack/cbor`
  together.** They are pinned to the same version on purpose.
- **`normalize-generated-specifiers.mjs` runs after the generator** and is part of the script — do
  not invoke `cratestack generate-typescript` alone.
- **Do not commit `generated/`** to "fix CI". The gitignore is deliberate; the fix is making the
  cold path work.
- **A procedure existing in the schema does not mean the console may call it.** Check the gate
  (`docs/knowledge/authorization-and-permissions.md`) and add the permission to
  `apps/console/src/shared/permissions.ts` if the screen needs one.
