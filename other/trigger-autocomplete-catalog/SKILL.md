---
name: trigger-autocomplete-catalog
description: Use when adding webhook events to make sure integrations properly register the webhook events they carry
---

# Trigger Autocomplete Catalog

Use this whenever a provider has webhook/event triggers.

The trigger catalog is owned by `@relayfile/adapter-core` and generated from
adapter sources. It does **not** live in this (cloud) repo's `packages/core` -
that's a different package.

- **To check coverage** (is a provider already in the catalog?), import it from
  the installed package - no checkout needed:
  `import("@relayfile/adapter-core/triggers")` exposes
  `KNOWN_TRIGGER_CATALOG` and `ADAPTERS_WITHOUT_KNOWN_TRIGGERS`.
- **To add events**, edit the provider's adapter source. That's the same
  `@relayfile/adapter-<provider>` package you already work in when wiring a
  provider (the relayfile-adapters checkout from the persona's adapter-package
  steps). Declaring events is one more edit in that package - no separate
  location to track.

## Goal

Ensure persona trigger autocomplete and deploy-time lint include the provider via `KNOWN_TRIGGER_CATALOG`.

## Scope

Only providers that actually emit webhook/event triggers belong in the catalog.
Pure storage / polling providers with no event source (e.g. s3, gcs, postgres)
legitimately remain in `adapters-without-known-triggers.generated.json` - do not
fabricate events for them.

## Required outcomes

- Provider appears in `KNOWN_TRIGGER_CATALOG` (regenerated `catalog.generated.ts`).
- Provider is absent from `adapters-without-known-triggers.generated.json` for missing trigger metadata.
- Event names are verbatim provider event names used at runtime (match the
  adapter webhook-normalizer's `eventType` and/or the events the cloud
  `nango-integrations/<provider>-relay` syncs subscribe to).

## Implementation options (in the adapter package)

1. Add `supportedEvents(): string[]` to the adapter class, or
2. Add a `<provider>.mapping.yaml` with a top-level `webhooks:` block whose keys
   are the event names (mirror `packages/granola/granola.mapping.yaml`). The
   generator only reads the keys.

## Validation (in your relayfile-adapters checkout)

```bash
# Build ALL workspaces first. The generator imports each adapter's
# supportedEvents(); if dependencies/dist are missing, those providers fail to
# import and are silently dropped from the catalog into the gap list. A core-only
# build is NOT enough.
npm ci
npm run build
node --import tsx packages/core/src/cli.ts triggers generate --repo-root .
node --import tsx packages/core/src/cli.ts triggers check --repo-root .
npm run build --workspace=packages/core
node --import tsx --test packages/core/tests/triggers/catalog-generator.test.ts
```

After the change merges, publish `@relayfile/adapter-core` (the `Publish Package`
workflow, e.g. `package=core`, `version=patch`). Publishing is what makes the
catalog change take effect - the trigger-autocomplete / deploy-time lint tooling
reads it via its `@relayfile/adapter-core` dependency. Cloud's
`packages/core` also depends on `@relayfile/adapter-core` and has tests that
import `KNOWN_TRIGGER_CATALOG`; normally no cloud `package.json` edit is
required because the dependency is a caret range that accepts new patch
releases. Bump Cloud's dependency only when the catalog fix requires a new
minor/major adapter-core version or Cloud needs to pin a specific published
version for CI.

## Notes

- Reference `relayfile-adapters#115` when closing missing-provider autocomplete gaps.
- If a provider intentionally has no event source, document why it remains in the `without-known-triggers` list.
