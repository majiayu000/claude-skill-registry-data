---
name: direct-setup
description: Add or revise a Direct deterministic development composition around product-owned ports, strict JSON worlds, scenarios, coverage claims, probes, and separate production-safe entries. Use when asked to adopt Direct, build a deterministic UI workbench, replace slow frontend dependencies with fixtures, or repair a Direct setup that leaks into production.
---

# Direct setup

## Inspect the product boundary

1. Read every applicable `AGENTS.md`, the package manifest, build configuration, production entry, feature state, and existing tests.
2. Trace the external dependency that makes the target state slow or nondeterministic.
3. Choose the lowest product-owned semantic port above that dependency and below the behavior under review.
4. State which adapter, service, host, platform, or device behavior the deterministic composition will replace and therefore cannot prove.

Do not simulate a provider SDK or wire protocol when the product can own a smaller domain port. Do not fork product UI or reducers into fixture-only copies.

## Separate production first

1. Define the port in production-safe product code.
2. Move provider, native-module, storage, or service imports into a production adapter.
3. Compose production from a production-only graph.
4. Add Direct as a development dependency and create a distinct Direct graph and output directory. Use a separate entry when both compositions target the same platform; a non-shipping Expo web fixture may instead sit behind an extensionless import with `.native` and `.web` implementations below a shared route tree.

Reject a design that conditionally imports fixtures from a query string, build flag, or runtime environment variable inside the production graph. Keep platform-specific navigation providers below shared routes and screens so route discovery sees one stable module while the bundler selects one composition.

## Define the deterministic surface

1. Define one bounded JSON world with a literal version.
2. Parse it from `unknown`; reject unknown keys, unsupported versions, duplicate identifiers, inconsistent states, and exceeded bounds.
3. Call `defineDirect` with a validated default, stable scenario IDs, and exact `fixture`, `mixed`, or `direct` coverage entries. Authored invalid configuration should fail during startup. Use `tryDefineDirect` for typed configuration assembled dynamically and `parseDirectDefinition` for genuinely unknown configuration.
   Keep each definition within the public discovery bounds of 256 scenarios
   and 256 coverage entries.
4. Implement deterministic adapters for the same product ports. Use logical time for product delays and activity scopes for asynchronous work.
5. Use exact scripts only when request or event order is part of the claim. Keep arbitrary valid interactive behavior stateful in the product adapter.
6. Call `createDirectSession` to own activation, store, clock, activity,
   harness construction, the world-free session manifest, probe observation,
   cancellation, and reverse-order cleanup.

Treat the shared world store as a scenario seed and activity ledger. Let product adapters own mutable repositories or event streams after construction.

A scenario contains initial world, route, and optional logical-runtime state. Product-verifier actions, semantic assertions, and evidence policy do not belong in the scenario catalog.

## Add the development entry

Render the real product interface with deterministic adapters from
`session.harness`. Call `installDirectBrowser({ session })` only in a browser
Direct entry. It atomically publishes the exact session manifest, live probe,
and reset action, installs the fail-closed application-fetch firewall by
default, tracks fetch work in the session activity scope, and registers
cleanup with the session. Configure blocked-request and activity-error
observers as named violations. Pass `firewall: false` only when another
checked boundary owns network containment.

Do not create a product-specific scenario-discovery global. The manifest
already publishes the query keys, default scenario, ordered scenario metadata,
active identity, and coverage contract without exposing worlds, scripts, or
product assertions. Its catalog drift fingerprint covers the query keys,
default scenario, ordered metadata, and exact coverage snapshot. The scenario
route is the expected product route; the product still owns whether its Direct
entry lives at that route or inside one wrapper URL.

Display activation failures. Never fall back from malformed explicit activation to a nearby valid scenario.

## Prove behavior and exclusion

Add focused tests for:

- accepted and rejected worlds;
- scenario and coverage drift;
- session-manifest round trips, active identity, and catalog drift;
- deterministic adapter success, declared failure, cancellation, and cleanup;
- exact-script consumption and remaining work when scripts are used; and
- emitted production output containing a forbidden marker.

Build production and Direct separately. Scan emitted production assets for package names, wire schemas, reserved query keys, fixture and workbench markers, and browser globals. Fail a scan that inspects no executable files.

For native bundles, emit a paired source map for each production platform. Positively require stable path suffixes for the shared screen and state, native composition, and production adapters in every map; reject the Direct package, `.web` composition, fixtures, and workbench sources. Apply the inverse positive selection to a web fixture map. An absence-only scan of an unrelated clean bundle is not proof.

Update the nearest `AGENTS.md`, package README, and command documentation. Run the narrow tests while iterating, then the repository's complete in-scope gate.

## Report the result

Name the selected port, deterministic scenarios, proof modes, commands run, production surfaces scanned, and direct evidence that still remains. Do not describe fixture evidence as proof of a replaced external system.
