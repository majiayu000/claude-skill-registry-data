---
name: universal-architecture
description: Apply responsibility-based architecture and enforce import boundaries. Use for code placement, architecture reviews, adapters, CLI entry points, platform sharing, and ESLint boundary rules.
---

# Universal architecture

Read [the portable runtime contract](../superdev-mode/references/portable-runtime.md) before following this workflow.

Apply a responsibility-based architecture without forcing unnecessary packages or abstractions. Detect the active platforms and existing repository conventions before proposing changes.

## Workflow

1. Identify the user's intent: design, placement decision, audit, enforcement, explanation, or implementation.
2. Load the mandatory reference files specified below before analyzing or acting. Do not answer from this summary alone.
3. Inspect the repository when the request concerns existing code. Determine platforms, entry points, workspace packages, aliases, build tools, tests, and current dependency direction.
4. Classify code by responsibility rather than its current directory name.
5. Separate runtime call flow from source-import direction, especially when dependency inversion is used.
6. Preserve existing conventions where they support the boundaries. Do not manufacture a migration solely to match example paths.
7. When implementing or reorganizing JavaScript/TypeScript layer folders, implement matching ESLint import boundaries in the same task. Treat folders without enforcement as incomplete unless the user explicitly declines ESLint or the project cannot use it.
8. For audits, cite concrete files and imports. For implementation, make scoped edits and run proportionate verification.
9. Do not edit when the user asked only for a review, explanation, or diagnosis.

## Mandatory reference loading

The reference files contain the detailed rules intentionally removed from this short file. Use them as required inputs, not optional background reading.

1. **Always read [references/layers.md](references/layers.md)** for every skill activation. It defines layer ownership, ports, adapters, foundations, and placement decisions.
2. **Also read [references/transport.md](references/transport.md)** whenever the request involves HTTP, RPC, GraphQL, IPC, native bridges, webhooks, queues, cron, workers, CLI, authentication, middleware, request validation, or application entry points.
3. **Also read [references/platforms-and-offline.md](references/platforms-and-offline.md)** whenever the request involves web/mobile/desktop flows, cross-platform sharing, deep links, push, payments, files, analytics, configuration, offline behavior, or synchronization.
4. **Also read [references/enforcing-boundaries-with-eslint.md](references/enforcing-boundaries-with-eslint.md)** whenever the request involves ESLint, imports, automated enforcement, dependency inversion, monorepo boundaries, exceptions, rollout, or CI. Read it when an implementation creates or reorganizes JavaScript/TypeScript architecture folders, even if the user did not mention ESLint.
5. **Read all four reference files** for a full architecture design, repository-wide audit, cross-platform refactor, or boundary-enforcement implementation.

If the request expands during the task, load every newly relevant reference before continuing. Resolve these paths relative to this `SKILL.md`. Do not claim a reference is unavailable without checking the skill's `references/` directory.

## Core model

Use six responsibility layers:

1. UI
2. Transport and application entry points
3. Domain
4. Capabilities
5. Vendor and platform adapters
6. Supporting foundations

Representative runtime flow:

```text
UI
→ Transport or application entry point
→ Domain
→ Capability port
→ concrete vendor/platform/persistence adapter
```

Typical source-import direction under dependency inversion:

```text
UI → Transport client and Shared
Server Transport → Domain and Shared
Domain → Capability ports and Shared
Concrete adapters → the ports they implement and Shared
Composition root → consumers plus concrete implementations for wiring
```

Runtime arrows are not automatically source-import arrows. A Capability port must not import its concrete adapter. Put wiring in an explicit composition root and prevent circular package dependencies.

## Non-negotiable boundaries

- UI renders and collects input; it does not own authoritative business rules, persistence, privileged SDKs, or unrestricted OS access.
- Transport parses and translates delivered messages, performs boundary validation and authentication, applies coarse access control, invokes Domain, and maps responses. It does not own product decisions or arbitrary queries.
- Domain owns business rules, invariants, workflows, entity-specific authorization, and business errors. It remains independent of delivery frameworks and concrete infrastructure.
- Capabilities expose small application-owned ports for external or platform operations. They do not leak provider terminology or SDK types.
- Vendor, device, OS, and persistence adapters implement ports and normalize concrete behavior. They do not decide business policy.
- Shared foundations contain only stable, framework-independent contracts and primitives. They must not become a dumping ground.
- Composition roots may import several layers only to construct and inject dependencies. They must not accumulate business logic.
- Split modules that combine responsibilities instead of granting shortcut dependencies.

## Universal placement questions

- Does it display information or collect user input? UI.
- Does it receive, parse, authenticate, validate, or translate a delivered message? Transport.
- Does it decide what the product should do? Domain.
- Does it define a stable operation needed from a service, device, or operating system? Capability.
- Does it use a specific SDK, provider, native API, database, or operating-system API? Adapter or persistence implementation.
- Is it a stable framework-independent contract or primitive? Shared foundation.
- Does it construct the application and connect ports to implementations? Composition root.

## Enforcement policy

Architecture rules should become executable where the language and tooling allow it. For JavaScript/TypeScript implementation work, folder organization and ESLint enforcement are one deliverable.

For JavaScript and TypeScript repositories:

- Inspect the actual package manager, ESLint version, flat/legacy config, paths, aliases, exports, existing plugins, and CI before editing.
- Install an appropriate boundary plugin through the repository's package manager when needed.
- Prefer `eslint-plugin-boundaries` for resolved-file layer classification and dependency policies.
- Use core `no-restricted-imports` for explicit vendor SDK, runtime, alias, or deep-import bans.
- Consider cycle rules and package `exports` as complementary controls.
- Adapt rules to actual paths and installed versions; never paste the reference configuration unchanged.
- Add or update the normal lint script and existing CI lint step so boundary rules run automatically.
- Verify aliases and relative imports cannot bypass enforcement.
- Verify a valid dependency passes and a representative forbidden dependency fails.
- Make CI fail on violations and warnings.

Do not create ESLint configuration for non-JavaScript/TypeScript source. State the limitation and use the language ecosystem's native boundary tooling only when it is within the user's implementation request.

Read the ESLint reference before proposing or editing boundary configuration.

## Output

Report only what serves the request. A full design or audit should include:

1. Detected platforms and entry points
2. Proposed or observed layer map
3. File and package ownership decisions
4. Runtime communication paths
5. Source-import policy
6. Violations or suspicious dependencies with evidence
7. Platform-specific and persistence adapters
8. ESLint enforcement status when applicable
9. Recommended changes in priority order
10. Verification performed or still needed

Prefer concrete repository paths and examples over abstract advice. Keep simple applications simple while preserving the important boundaries.
