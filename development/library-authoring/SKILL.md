---
name: library-authoring
description: Conventions for a published package/library — semver discipline, changelog, public API stability, dependency footprint. Use when building or reviewing a project meant to be imported by other code, not a deployed app or service.
---

# Library authoring

A library's consumers can't fix a break the way an app's own team can — they're on
a different release schedule, often don't read your source, and only see what the
package registry and changelog tell them. Treat the published surface as a
contract.

## Semantic versioning, actually enforced

- Patch (`x.y.Z`): bug fixes only, no API change, no new exported symbol.
- Minor (`x.Y.z`): additive — new exported function/type/optional parameter, old
  callers keep working unmodified.
- Major (`X.y.z`): anything that breaks an existing caller — removed/renamed
  export, changed function signature, changed default behavior, dropped runtime/
  language-version support.
- A build tool or lint pass that infers version bumps from commit messages
  (changesets, conventional-commits + semantic-release) removes the "I forgot this
  was breaking" failure mode — worth adopting once a project has any external
  consumer.

## Changelog

- Every published version gets a changelog entry, written for the consumer deciding
  whether to upgrade — not a copy of commit messages. Keep a Changelog format
  (Added/Changed/Deprecated/Removed/Fixed/Security sections) is a reasonable
  default.
- A breaking change's entry says what broke and the concrete migration step, not
  just "BREAKING: refactored X."

## Public API surface

- Export only what's meant to be used by consumers. An internal helper that's
  merely *reachable* (not re-exported, not documented) isn't part of the contract —
  but if it's actually exported, it is, whether or not that was intended.
- Prefer additive changes (new optional parameter, new export) over modifying an
  existing signature — see `api-design` skill's versioning section; a library's
  exported functions are exactly the "API" that skill describes.
- Deprecate before removing: mark the old symbol deprecated (with a note pointing
  to its replacement) for at least one minor version before deleting it in a major.
- Widen accepted input types/narrow returned types cautiously — loosening what you
  accept is usually safe in a minor, tightening what you return usually isn't
  (a consumer may depend on the wider type).

## Dependency footprint

- Every dependency a library adds is forced onto every consumer's tree, including
  transitively — prefer zero/minimal runtime dependencies over convenience, more
  aggressively than you would in an application.
- Peer dependencies (not bundled deps) for anything the host app is expected to
  already provide a single shared instance of (framework runtimes, UI libraries) —
  bundling your own copy causes duplicate-instance bugs for the consumer.
- Pin dependency versions loosely enough that a consumer's own version doesn't
  conflict with yours (`^`/`~` ranges, not exact pins) unless there's a specific
  compatibility reason not to.

## Documentation

- The package's entry point (README or top-level doc comment) shows a minimal
  working example before anything else — a consumer evaluating whether to adopt it
  shouldn't have to read the whole API reference first.
- Document the minimum supported language/runtime version explicitly, and treat
  dropping it as a breaking (major) change.
