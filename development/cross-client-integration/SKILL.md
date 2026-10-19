---
name: cross-client-integration
description: Plan versioned interfaces and independently testable slices across metisa firmware, Android, Apple, and configurator clients.
---

# Cross-Client Integration

## Use when

A feature changes a firmware protocol, mobile app behavior, Windows configurator, planned browser configurator, or planned metisa homepage.

## Procedure

1. Read `project-rules/product-surfaces-and-interfaces.md`, `project-rules/modular-development.md`, and the current workbook.
2. Inventory the actual supplied source directories, build/test commands, protocol/schema, versioning, and (for the homepage) deployment/assets/analytics before proposing architecture.
3. Define the smallest shared contract change first, including versioning, validation bounds, units, defaults, error handling, and compatibility fixtures.
4. Split implementation into independently testable firmware and client slices; declare checkpoint dependencies.
5. Test compatibility with the shared fixtures and document untested hardware/device pairings.
6. For Windows-to-browser migration, create a parity matrix and data migration/rollback plan before replacing behavior.
7. For homepage changes, verify content provenance and avoid unsupported compatibility, safety, certification, or performance claims; keep deploy/release separate from firmware qualification.

## Constraints

- Do not invent mobile/configurator frameworks or protocol details before source and requirements are available.
- Do not claim a client/firmware pairing is supported without a tested compatibility record.
- Do not silently change config-file or wire-protocol formats.
- Hardware end-to-end testing is separate from mocks and compile checks.

## Done when

Each slice has explicit dependencies and tests, shared contracts are versioned, and supported version pairings are documented without overstating evidence.