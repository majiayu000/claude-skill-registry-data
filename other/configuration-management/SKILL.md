---
name: configuration-management
description: >-
  Use when adding, renaming or reading an environment variable, extending the typed config layer, or
  diagnosing a build that fails at boot with a schema error. Triggers include "add an env var",
  reading a NEXT_PUBLIC_* or REACT_APP_* value, an ESLint no-restricted-syntax error naming
  process.env, a Zod validation error thrown during a build, and edits to .env, .env.example or
  .env.production.
---

# Configuration management

## Profile keys consumed

- `make.format`
- `make.lint_eslint`
- `make.lint_tsc`
- `architecture.source_root`

## Overview

Environment variables are read once, through a typed and validated config module, and never from
`process.env` at the point of use. Validation runs at module load, so a missing or malformed value
fails the build immediately instead of degrading silently in production.

## When to use

- Adding, renaming or removing an environment variable.
- Reading configuration from application code, a component, or a hook.
- ESLint rejects a `process.env` member expression.
- A build or dev server dies at boot with a schema error naming one variable.
- Reviewing whether a value belongs in the build-time layer or the runtime layer.
- Not for: secrets management, CI workflow `env:` blocks, or Docker Compose variables that never
  reach application code.

## Applicability by repository shape

- **React SPA shape** (feature modules under the source root, a bootable app, an aggregate CI
  target): partial — the layer lives under the source root (`architecture.source_root`) at
  `config/env/` (dependency-free `raw-env.ts` for the paint path plus Zod-validated `env.ts`, frozen
  at construction), the ban is scoped to non-React `.ts` files under the source root and runs under
  the target mapped by `make.lint_eslint`; a dedicated env-sync target asserts `.env` and
  `.env.example` declare the same keys, and `config/runtime/` under the same source root carries
  values an operator can change without a rebuild.
- **Next.js app shape** (routed pages, no aggregate duplication gate): yes — `src/config/env.ts` is
  the single reader, enforced by `no-restricted-syntax` under the target mapped by
  `make.lint_eslint`, over layered `.env`, `.env.production` and `.env.example`.
- **Component-library shape** (Storybook-first, no bootable app, published package): no — components
  read `process.env` directly; no barrel exists.

The env-sync target has no logical key in the profile; in the React SPA shape it is the repository's
own `.env`/`.env.example` key-parity check:

```bash # profile-example
make check-env-sync   # asserts .env and .env.example declare the same keys
```

## Core pattern

```ts
// Correct — the validated module is the only source. This is the Next.js shape's barrel, which
// exports the parsed object directly; the React SPA shape's `config/env/` under the source root
// exports a frozen singleton read through accessors instead.
import { env } from '@/config/env';

const apiUrl = env.NEXT_PUBLIC_GRAPHQL_API_URL;

// Rejected by ESLint everywhere except the config module itself.
const bad = process.env.NEXT_PUBLIC_GRAPHQL_API_URL;
```

The rule matches both spellings — `MemberExpression[object.name='process'][property.name='env']` for
`process.env.X` and `[property.value='env']` for the computed `process['env']` — because a
dotted-only selector is trivially sidestepped. The config module, tests, and stories are the only
exemptions.

## Procedure

1. Declare the variable in `.env.example` with a comment saying what it is for.
2. Add it to the schema with a type that actually validates: a URL check, a coerced number, an enum,
   or a non-empty string — not a bare string.
3. Set the value in every layered file that needs it (`.env` for development, the production overlay
   for the deployed build).
4. Read it from the config module at every call site.
5. Run the formatter mapped by `make.format`, then the gates mapped by `make.lint_eslint` and
   `make.lint_tsc` — skip either with a recorded note when it maps to `null`.

## Validation is a deployment blocker

Parsing happens at module load, before any application code runs, and a failure throws with the
variable name and the reason. Treat that as correct behaviour: a bad configuration is not a runtime
condition to handle, and defaulting past it ships a silent no-op — a placeholder analytics id, or a
development endpoint in production.

Two invariants worth keeping when the schema grows: endpoints that carry credentials or trace
headers should be required to be encrypted, accepting cleartext only for loopback hosts; and in a
statically exported build, public variables are inlined only for **literal** member expressions, so
a dynamic read (`process.env[name]`) inlines `undefined` in the browser bundle.

## Common mistakes

- Reading `process.env` "just this once" in a component — refactor the read into the config module
  rather than reaching for a lint suppression, which these repository shapes forbid.
- Typing everything as `z.string()` — the schema then validates nothing.
- Adding the variable to the schema but not to `.env.example` — the next contributor's build fails
  at boot with no template to copy from.
- Committing a local override file — those are ignored on purpose; personal values belong there,
  shared defaults in the tracked layer.
