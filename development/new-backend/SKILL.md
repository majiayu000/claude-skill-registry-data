---
name: new-backend
description: >-
    Add a pluggable adapter/backend to plainworks the canonical way — a state store, channel
    transport (sse/ws), auth mechanism (oidc/jwt/apikey/BYO), or query wiring — implementing the
    core package's seam, selected via config through an explicit register()/createX({...}), with no
    import-time side effects and the lean default kept in core. Use when integrating a transport, an
    auth style, or a state/query backend.
---

# Adding a backend adapter to plainworks

plainworks' abstraction packages follow a **seam + explicit-registration** pattern: the core package ships the abstraction plus a lean default (in-memory / local), and heavier or alternative backends plug in through an explicitly-created adapter. This mirrors the gokit/rskit backend-split policy, translated to TS. Follow the existing owners exactly — do not invent a new registration mechanism.

## Where adapters live

Match the layer map — the adapter is part of, or sits beside, the core package that owns the seam:

- **State** (`state`, L1) — the **Zustand** store-factory is the blessed default behind the state seam; a secondary adapter (e.g. Jotai) implements the same seam.
- **Channel** (`channel`, L2) — the core owns backoff+jitter, retry ceiling, `minUptime` gating, the lifecycle state machine, and the header-only token-provider seam; `sse` and `ws` are **transport adapters** implementing the wire seam. WebTransport is a seam only, not shipped.
- **Connect / Query** (`connect`, `query`, L2) — Connect-RPC transport and TanStack Query wiring plug into the same event→cache seam.
- **Auth** (`auth`, L3) — a small core (session + header/identity seam, server/client split) with **swappable adapters**: `oidc`, `jwt`, `apikey`, and bring-your-own. New auth styles integrate **without touching the core**.

## The binding rules

1. **Implements the core seam.** The adapter implements the interface the core package owns (the transport seam, the auth-header/identity seam, the state-store seam). It does **not** redefine the abstraction. The seam itself lives in the lowest package that needs it — often `@plainworks/std` — so both sides depend downward only.
2. **Explicit, typed registration — config-driven selection.** The consumer wires an adapter with an explicit `createX({...})` / `register(registry, adapter)` call that captures typed config. **No import-time side effects** (importing the adapter must not dial the network or read env) and **no module-level singleton / global registry**. A registry populated by import order, or a store/client created at module load, is a blocker.
3. **Per-request factories.** Stores, sessions, query clients, and connections are created by a factory (SSR/RSC-safe), never a package-level mutable global.
4. **Core keeps the lean default.** The in-memory / local backend stays in the core package and remains the zero-config default; alternative backends are opt-in and selected via config.
5. **Server/client custody.** Token-holding code (auth server) ships on the server-only `./server` entry and must never be importable from a `"use client"` graph. Auth MUSTs: Authorization Code + PKCE `S256` only; `Secure`+`HttpOnly`+`SameSite=Strict` `__Host-` cookies (BFF default) or in-memory access token (SPA fallback) — never localStorage; header-only tokens; refresh-token rotation for the token-holding fallback. An adapter that exposes a client hook (a `state`/`query` binding) keeps the hook in a `"use client"` module and tests it behaviorally under jsdom with `@testing-library/user-event` + MSW.
6. **Host adapters get their own subpath.** An adapter that needs a host primitive (web storage, cookies, the URL, a form post, `PerformanceObserver`) lives in `src/adapters/<name>.ts` and ships as `@plainworks/<pkg>/<name>`, named after what it does (`state/web-storage`, `auth/form-post`), never after a host (`dom`, `browser`, `node`). It compiles in its own `tsconfig.adapters.json` with the DOM lib, so `.` and `./client` stay DOM-free. See [Choose an entry point](../../../docs/architecture.md#choose-an-entry-point).

Study an existing adapter in the same package for the exact shape before writing a new one. If that shape, or the seam itself, is outdated, redesign it on current best practices rather than copying it. If the new adapter supersedes an existing one, move its consumers and delete the old adapter in the same change (alpha, no backward compatibility; see [Development stage](../../copilot-instructions.md#development-stage-alpha-redesign-over-compatibility)).

The shadcn atoms in `@plainworks/elements` are **not** a backend. They are **vendored** and **locked**, so they have no adapter seam to extend; refresh them with [`update-atoms`](../update-atoms/SKILL.md), and route a deviation through the deviation ladder in the [Vendored atoms](../../copilot-instructions.md#vendored-atoms) baseline.

## Steps

1. **Locate the seam.** Find the interface the core package exports for this concern (transport, auth-header/identity, store). If it lives too high to be implemented downward, move the seam into the lower package (`std`) first — a separate, reviewed change.
2. **Write the adapter test-first.** Failing vitest test (against a fake/harness from `@plainworks/testkit`) → minimal adapter → refactor while green. Cover the failure paths (reconnect, token refresh, cancellation).
3. **Expose an explicit factory.** `createSseTransport({...})` / `createOidcAuth({...})` returning the seam type; typed config; no side effects on import.
4. **Keep the default in core.** Confirm the lean default still works with zero config and the adapter is purely opt-in.
5. **Validate & release.**

```bash
bun run lint
turbo run typecheck build test --filter=@plainworks/<package>
bun run check-boundaries          # adapter imports only downward; seam stays lower
bun run check-versions
bun run changeset
```

## Checklist

- [ ] Implements the core seam; does not redefine the abstraction; seam lives in the lowest package that needs it
- [ ] Explicit `createX({...})` / `register(...)` with typed config; **no import-time side effects, no global registry**
- [ ] Per-request factory — no module-level store/client/session singleton
- [ ] Lean default kept in core and remains the zero-config default
- [ ] Server/client custody correct (auth server out of `"use client"`; header-only tokens; PKCE/cookie MUSTs)
- [ ] Tested test-first with `@plainworks/testkit` doubles, failure paths covered; gates green; Changeset added

Per repo workflow, **create the branch and make edits only** — the maintainer commits and pushes.
