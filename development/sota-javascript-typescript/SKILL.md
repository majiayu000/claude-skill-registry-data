---
name: sota-javascript-typescript
description: State-of-the-art JavaScript and TypeScript engineering (2026) for both writing and auditing code. Covers strict TypeScript configuration and type design, language idioms and pitfalls, async patterns, Node.js backends, JS/TS-specific security (XSS, prototype pollution, supply chain, injection), frontend/React and Node performance, and testing/tooling. Use whenever building, reviewing, refactoring, or security-auditing code involving JavaScript, TypeScript, Node, npm, React, frontend code, tsconfig, package.json, vitest, or any .ts/.tsx/.js/.mjs files.
---

# SOTA JavaScript / TypeScript Engineering

## Purpose

This skill encodes 2026 state-of-the-art for JS/TS so generated code is strict, secure, and fast by default — and so audits of existing code find the bug classes that actually bite: untyped boundaries, floating promises, XSS sinks, prototype pollution, supply-chain gaps, event-loop blocking, and leak-prone listeners. It has two operating modes; pick one explicitly at the start of a task.

Baseline assumptions (mid-2026): TypeScript ≥5.9 strict (6.0 = last JS-based compiler; 7.0 Go-native since July 2026, shipped as the regular `typescript` package **with no compiler API** — typescript-eslint, including the non-negotiable `no-floating-promises`, and Volar-based frameworks (Vue/Angular/Astro/Svelte) still need the 6.0 API, so install `typescript` as `npm:@typescript/typescript6` beside 7.0 until they support 7: rules/01), ESM-first, Node LTS ≥22 (run the line marked Active LTS at github.com/nodejs/Release; 26 is scheduled for LTS on 2026-10-28 and ships Temporal by default), ES2024+ available, React 19.2-era with Server Components and React Compiler (stable since 1.0) where relevant, latest stable Vitest + flat-config ESLint (the default since v9).

## BUILD mode (writing or modifying code)

1. **Read the relevant rules files first** (index below) for the area you're touching. Don't generate from memory what a rules file specifies.
2. **Defaults unless the codebase dictates otherwise**: strict tsconfig (rules/01), ESM, `unknown` over `any`, discriminated unions for state, zod/valibot parse at every untrusted boundary, `??`/`?.` discipline, AbortController on cancellable ops, pino logging in services, Web APIs over deps.
3. **Match the host codebase** for style, framework, and structure — but do not replicate its security bugs or `any`-sprawl into new code. New code meets the bar even in old repos.
4. **Boundary rule**: every input from outside the type system (HTTP, env, JSON.parse, storage, postMessage, DB without typed client) is parsed with a schema before use. No `as T` on external data.
5. **Finish the job**: new code compiles under `tsc --noEmit`, passes lint, and ships with behavior-level tests (rules/07). Handle the error path of every async call — no floating promises.
6. When a requirement conflicts with a rule (e.g., legacy CJS, jest), follow the codebase and note the deviation; don't silently half-apply both.

## AUDIT mode (reviewing existing code)

Scope first (frontend? Node service? library?), then read the matching rules files and run their audit checklists — each ends with grep/eslint hunt patterns. Validate findings: confirm attacker-controlled data actually reaches the sink, confirm the perf issue is on a hot path. No speculative findings.

**Severity conventions:**
- **CRITICAL** — remotely exploitable now: untrusted input reaching eval/innerHTML/exec/SQL, auth bypass, secrets exfiltratable via XSS.
- **HIGH** — exploitable with conditions, or guaranteed-corruption bug class: missing boundary validation, prototype-pollution-prone merge of request data, floating promises dropping errors, tokens in localStorage, unbounded request bodies, float money math, sync crypto blocking the loop.
- **MEDIUM** — weakened posture or latent defect: missing strict tsconfig flags, no graceful shutdown, missing CSP/timeouts, `||` vs `??` on falsy-valid values, index keys on mutable lists, unbounded caches, missing supply-chain controls.
- **LOW** — hygiene/debt: dead deps, `hasOwnProperty`, console.log in services, snapshot sprawl, missing memoization on profiled-hot paths.

**Finding format:**
```
[SEVERITY] Title (CWE-xxx if security)
File: path/to/file.ts:42
Issue: what is wrong, in one or two sentences
Evidence: the offending snippet
Impact: what an attacker/user/operator experiences
Fix: concrete change (code if short)
```

Order the report CRITICAL→LOW, deduplicate repeated patterns into one finding with a file list, and end with the top 3 systemic recommendations (e.g., "enable noUncheckedIndexedAccess", "adopt MSW", "add zod to route boundaries").

## Rules index

| File | Read this when... |
|---|---|
| [rules/01-typescript-config-and-types.md](rules/01-typescript-config-and-types.md) | touching tsconfig (**TS ≥6.0 `types: []` / `rootDir` defaults; TS 7.0 has no compiler API — the `typescript6` alias for typed lint**; `.ts` import specifiers under Node type stripping); designing types/interfaces; seeing `any`/casts; modeling state; validating input shape; setting up a library or monorepo; deciding zod-vs-types questions |
| [rules/02-language-idioms.md](rules/02-language-idioms.md) | writing any JS/TS logic: equality, `??`/`?.`, array methods, immutability, Map/Set, **in-band sentinels (absence encoded as `-1`/`0`/`""`)** — **`-1` lies where `NaN` poisons**, error classes and Result types, generators, dates (Temporal), money/number precision |
| [rules/03-async-patterns.md](rules/03-async-patterns.md) | anything with promises/async: combinator choice, floating promises, AbortController/timeouts, event-loop ordering, top-level await, workers, streams, async race conditions |
| [rules/04-node-backend.md](rules/04-node-backend.md) | building/auditing Node services: runtime choice (**Node Permission Model: scoped `--allow-*`, symlinks escape it, no network scope before v25**), dropping deps for built-ins, env config, **dev servers, `--inspect` and an unset `NODE_ENV` in production**, HTTP hardening (timeouts/body limits), graceful shutdown, **request context kept out of module scope (`AsyncLocalStorage.run`, not `enterWith`)**, process error policy (**unlistened `'error'` events, Express 4 async handlers**), pino; **`require(esm)` vs dual publishing, and top-level `await` in a library entry (`ERR_REQUIRE_ASYNC_MODULE`)**; **`node:crypto` AEAD traps** (`update()` before `final()`, missing `authTagLength`), **TLS/`ssh2` verification opt-outs**, server-side **headless browsers** (`goto` as SSRF, string `evaluate`) |
| [rules/05-security.md](rules/05-security.md) | any security-relevant code or audit: XSS sinks (incl. **string-to-code DOM APIs**: `setAttribute('on…')`, script text, Lit `unsafe*`), CSP, **server-side template engines** (raw output, template/view-name injection), prototype pollution, invisible/bidi characters in source, NoSQL operator injection, Ajv and `cors` config, npm supply chain (install/build-time hooks per package manager, credential-free install job), ReDoS, token storage/JWT, **app-set cookie defaults per framework**, **dynamic code evaluation (`Function`, `node:vm`, dispatch tables)**, postMessage and **Web Worker scripts/messages**, **frozen security objects and attacker-chosen global keys** (child_process injection and SSRF moved to rules/08); **escape hatches into raw memory**: native addons, `node:ffi` and `Buffer.allocUnsafe`; **pnpm cooldown that fails open** unless `minimumReleaseAge` is written, `trustPolicy: no-downgrade` |
| [rules/06-performance.md](rules/06-performance.md) | bundle size, React re-renders/keys/RSC, virtualization, debounce/throttle, memory leaks, Node event-loop blocking, profiling before optimizing |
| [rules/07-testing-and-tooling.md](rules/07-testing-and-tooling.md) | writing tests or setting up tooling: vitest, testing-library behavior testing, MSW, Playwright, ESLint flat + typescript-eslint strict, knip, publint/attw, **tarball review (`npm pack --dry-run`, `files` over `.npmignore`)**, CI gates. **Test *strategy* — suite shape, TDD, doubles, test data, flake policy — lives in `sota-testing`; load it for any build that writes logic. This file owns JS/TS runner mechanics only.** |
| [rules/08-process-and-outbound.md](rules/08-process-and-outbound.md) | server code that spawns processes or fetches a caller-influenced URL: `child_process` (`execFile` array form, `shell: true`), SSRF with the connect-time `lookup` check, **credentials that follow a redirect**, and its browser counterpart: **client-side `fetch`/XHR/`EventSource` to a page-supplied URL** (split out of rules/05, section names unchanged) |
| [rules/09-browser-platform-security.md](rules/09-browser-platform-security.md) | browser code with more reach than a page: **service workers** (same-origin script, narrow scope, stable URL, kill switch; AppCache retired), **DOM clobbering** (named elements shadowing globals; DOMPurify `SANITIZE_NAMED_PROPS`, Sanitizer API keys), **browser extensions** (no remote code, isolated world, sender checks, least permissions, `storage` access level), **client-side storage** (`sessionStorage` over `localStorage`, non-extractable `CryptoKey` for IndexedDB, read-back as untrusted input; Web SQL removed) |

For a full audit, read 01→09 in order; security-focused audits prioritize 05, 08, 09, 01, 03, 04.

## Top 10 non-negotiables

1. **`strict: true` + `noUncheckedIndexedAccess`** in every tsconfig; no `any`, no `@ts-ignore` — `unknown` + narrowing, `@ts-expect-error` with reason.
2. **Parse, don't cast, at boundaries**: zod/valibot on every HTTP body/query, env var, JSON.parse, webhook, postMessage payload. Types inside, schemas at the edge.
3. **No floating promises**: every promise awaited or explicitly `.catch`-handled; `@typescript-eslint/no-floating-promises` as error. `allSettled` for independent work; bounded concurrency.
4. **Discriminated unions for state**, exhaustive `switch` with `never` default — no boolean-soup interfaces with optional data/error pairs.
5. **`===` always; `??`/`?.` over `||`/`&&`** for null-handling; immutable updates (`toSorted`, `structuredClone`, spread) on shared data.
6. **Errors are `Error` subclasses with `cause`**; never throw strings; never swallow with empty catch; Node policy = log fatally then exit on uncaught.
7. **XSS sinks are forbidden by default**: no `innerHTML`/`dangerouslySetInnerHTML` with non-constant input unless DOMPurify-sanitized at render; no eval family ever; CSP on HTML responses.
8. **No secrets in localStorage; no shell interpolation**: httpOnly cookies for tokens; `execFile`/`spawn` array-args, never `exec` with template strings; parameterized SQL.
9. **Supply chain controlled**: committed lockfile + `npm ci`, install scripts disabled/allowlisted, update cooldown, minimal deps — prefer platform built-ins (fetch, node:test, crypto.randomUUID).
10. **AbortController + timeouts on all I/O**; never block the event loop (>50ms CPU → worker; no `*Sync` in request paths); listeners and intervals always cleaned up.
