---
name: game-mod-api-versioning
description: "Designs stable, versioned mod APIs and compatibility policies. Use when exposing engine hooks, content registration, scripting surfaces, or plugin contracts."
---

# Game Mod Api Versioning

## Use when
A small internal refactor unexpectedly breaks user mods or forces unsafe coupling to internal engine types.

## Workflow
1. Identify public contracts separately from implementation details and define supported extension points with examples.
2. Version data formats and behavioral guarantees independently from internal module versions.
3. Build compatibility fixtures for representative mods and test missing, deprecated, and unsupported capabilities.
4. Publish a deprecation window, capability discovery method, and clear failure diagnostics before removing an API.

## Required output
An API stability matrix, versioning policy, sample mod, and compatibility test suite outline.

## Validation
- Mods depend only on documented public types or functions.
- Breaking changes fail clearly instead of silently changing behavior.
- The policy explains whether old mods are supported, adapted, or rejected.

## Guardrails
Do not expose unsafe memory ownership or internal engine lifetimes as an accidental modding API; isolate untrusted mods.
