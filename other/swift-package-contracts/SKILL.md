---
name: swift-package-contracts
description: Design or review reusable Swift packages and SDKs. Use when public boundaries, compatibility, consumer tests, binaries, or versioned releases matter.
license: MIT
metadata:
  author: "coryparrry"
  version: "0.1.0"
  last-updated: "2026-08-30"
  last-reviewed: "2026-08-30"
  apple-docs-reviewed: "2026-08-30"
---

# Swift Package Contracts

Treat packages as consumer contracts proved outside implementation modules and bound to release evidence.

## Contract

Record tools/language modes and Swift settings, products and every target kind, explicitly supported platforms/floors, delivery form, host needs, exact baseline, and version policy including pre-1.0. Contracts include names, declarations, protocols, constraints, Codable forms, availability, resources, behavior, isolation, and `Sendable`. Do not mistake SwiftPM's implicit platform defaults for an intentionally supported test matrix.

Route detail to [package boundaries](references/package-boundaries.md), [public contracts](references/public-contracts.md), or [verification and release](references/verification-and-release.md).

## Invariants

- Products are consumer-visible; targets are build-graph units. Distinguish regular, executable, test, binary, system-library, plugin, macro, and other supported target kinds instead of assuming each target compiles source or tests. Export supported modules only, normally leave linkage unspecified, narrow dependencies, and keep implementation types out of signatures. Treat name/floor changes as migrations; build conditional graphs on real platforms.
- Classify source, binary, wire, behavioral, and concurrency impact. Additive overloads, requirements, conformances, constraints, defaults, or isolation can break clients; compile old call sites.
- For durable data, use explicit keys, define missing/unknown/renamed fields, and test historical old/new fixtures. A current round trip does not prove compatibility.
- `Sendable`, actors, `async`, callback isolation, cancellation, and completion are API. Prefer checked conformance; require a synchronization proof for public `@unchecked Sendable`.

## Evidence and release

Use package tests for internals. A same-package test without `@testable` is still not necessarily public-client proof because modern `testTarget` declarations enable package access by default; set `packageAccess: false` where supported or, preferably, compile a truly external consumer. Make that external fixture resolve the reviewed Git tag/commit or packaged artifact—not a sibling path—and exercise import/availability/calls. Use app-hosted tests for bundle/lifecycle/entitlement/permission/platform behavior, and artifact tests for slices, resources, linkage, checksum, and provenance. Workspaces/caches can mask breaks; `swift test` cannot prove host behavior.

Against a released tag or commit, compare manifest, API, client compilation, schemas, concurrency, and every distributed form. Match semantic version to impact and document migrations.

Complete with explicit boundaries/impact, external proof, required schema/concurrency/host evidence, source provenance, and named unverified combinations.

Apple sources are recorded in [apple-documentation.md](references/apple-documentation.md).

## Review

- Last updated: 2026-08-30
- Last reviewed: 2026-08-30
- Apple documentation reviewed: 2026-08-30

PackageDescription products, targets, platforms, dependencies, resources, binary targets and checksums, plus Swift availability, Codable, and Sendable guidance were reviewed with Xcode MCP `DocumentationSearch`; see [Apple documentation evidence](references/apple-documentation.md).
