---
name: inventorying-api-surface
description: Use when documenting public interfaces, planning API changes, evaluating backward compatibility, or understanding what a module exposes to consumers
---

## Announce at start: "Using codebase-analyzer to inventory the API surface."

## Overview

Catalog every public interface: exported functions, classes, types, REST/GraphQL endpoints, and their contracts. This skill finds implicit ENTRY POINTS (how you get in: undocumented endpoints, conditionally exposed routes, IPC channels, WebSocket message types, CLI argument schemas, environment variable contracts, plugin hooks). For implicit BEHAVIORAL ASSUMPTIONS (how code expects to be used), use `detect-hidden-contracts`.

## Process

1. Find public exports (export, module.exports, pub fn, def with __all__)
2. Map REST/GraphQL/RPC endpoints if applicable
3. Document function signatures and type contracts
4. Find breaking change risks (widely-used public APIs)
5. Find undocumented public APIs
6. Categorize by stability: stable, experimental, deprecated, internal-but-exported
7. Map implicit entry points beyond HTTP (see Implicit Entry Points below)
8. Trace API-to-data-flow: verify every endpoint touches data, detect endpoint chains

## API-to-Data-Flow Mapping

Every endpoint should be traceable to a data mutation or query. Endpoints that don't touch data are either proxies, health checks, or dead endpoints.

**Chain detection**: if endpoint A's response shape matches endpoint B's request body, they are designed to be chained. That reveals intended workflows the codebase expects but may never document. Look for:
- Response schemas that mirror request schemas on other endpoints
- IDs returned from create endpoints that feed directly into detail endpoints
- Pagination cursors that flow into subsequent calls
- Field names that are identical across request/response boundaries

## Implicit Entry Points

Not just HTTP: the implicit API is often larger than the explicit one. Check for:
- **IPC channels**: `ipcMain.handle`, `ipcRenderer.send`, Electron/Node child_process message protocols
- **WebSocket message types**: JSON message discriminators (`type` field), subscription channels
- **CLI argument schemas**: argparse/click/ commander definitions, each flag is an API contract
- **Environment variable contracts**: `process.env.X` reads that control behavior without being documented as config
- **Plugin hooks**: extension points, event emitters, middleware registration functions, lifecycle callbacks

## SECURITY_SIGNAL

Undocumented endpoints are a security surface. Specifically flag:
- Admin routes without visible authentication middleware
- API versions that expose more fields than documented (field leakage across versions)
- CORS misconfigurations (wildcard origins on non-GET endpoints)
- Endpoints reachable but not in any route index or OpenAPI spec
- Environment variables that bypass auth or change security behavior

## Diagnostic Reasoning

1. **Start from routes, not controllers.** Route definitions reveal the intended API surface. Controllers may have methods that are never routed — these are dead endpoints or upcoming features. The route table is the source of truth; everything else is speculation.

2. **Trace exports through re-export chains.** A function exported from `utils.js` but re-exported through `index.js` is public. The same function without a re-export is internal. The re-export graph determines what consumers can actually reach — the original export site does not.

3. **Check for versioned APIs.** If `/v1/` and `/v2/` exist, the difference between them reveals what changed and why. Removed endpoints between versions = deprecated capabilities. Added endpoints = new features that may not be documented yet. The delta IS the migration guide.

4. **Map middleware chains per route.** Middleware that runs BEFORE a route determines who can access it. Routes without auth middleware = publicly accessible. Routes with role-based middleware = permission-gated. The middleware chain IS the access control policy.

5. **Find the shadow API.** Framework-specific patterns often expose more than explicit routes: GraphQL schemas, WebSocket message handlers, gRPC service definitions, event bus subscriptions. Each is an API surface that standard route-scanning misses. Look for framework-specific registries, not just HTTP verbs.

6. **Correlate env var reads with behavior branches.** `process.env.FEATURE_X` without a default means the feature is opt-in. With a default, it is opt-out. Either way, the env var is an implicit API contract — it changes behavior without touching code, and consumers may depend on it without knowing.

## Trigger Signals

- **HIGH confidence**: APIs exposed conditionally behind feature flags -> `map-feature-gates`
- **HIGH confidence**: Internal APIs exposed without documentation -> `classify-repo-artifacts`
- **MEDIUM confidence**: Versioned APIs with deprecation patterns -> refactoring candidate
- **LOW confidence**: Well-documented, stable API surface -> no deep dive needed

## Adversarial Lens

The documented API is what they WANT you to see. The undocumented API is what EXISTS. Look for: endpoints that respond but aren't in any docs, admin routes accessible without auth, API versions that expose more data than the latest. The gap between docs and reality is where secrets hide.

## Red Flags

- Only checking explicit exports, missing re-exports
- Not checking REST/GraphQL endpoints if they exist
- Ignoring type-level API (exported interfaces, types)
- Missing implicit entry points (IPC, env vars, CLI args, WebSocket types)
- Not tracing data flow through endpoints

## Output Contract

Write `docs/analysis/api-surface.md` using standard contract.
Include: exported symbols, endpoints, stability categories, undocumented APIs, implicit entry points, data-flow chains, security signals.
