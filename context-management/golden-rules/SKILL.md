---
name: golden-rules
description: Installs mandatory security, coding, naming, design, testing, error handling, API contract, and performance standards into CLAUDE.md as always-on context for every Claude Code session.
argument-hint: "[--update | --force]"
allowed-tools: Read, Grep, Write, Edit
model: haiku
disable-model-invocation: true
---

# Golden Rules — Always-On Project Standards

Install mandatory security, coding, design, testing, error handling, API contract, and performance standards into this project's CLAUDE.md so they are active for every Claude Code session automatically.

This skill's version: **1.8.0** (also stamped in the marker comment inside the Golden Rules Block below).

## Instructions

1. Use Read to check if `./CLAUDE.md` exists in the current working directory.

2. Use Grep to search `./CLAUDE.md` for the string `## Golden Rules` (if the file exists).
   - **Not found:** proceed to step 3 (fresh install).
   - **Found, no argument given:** check for the version marker comment `<!-- golden-rules vX.Y.Z -->` inside the section.
     - Marker version equals this skill's version: inform the user the Golden Rules are current and stop.
     - Marker is missing or older: inform the user an older install was found and that `/golden-rules --update` will replace it with the current version. Stop without modifying anything.
   - **Found, `--update` given:** if the marker is missing or older than this skill's version, replace the entire existing `## Golden Rules` section (from the `## Golden Rules` header up to the next level-2 (`##`) header, or end of file) with the Golden Rules Block below. If already current, say so and stop.
   - **Found, `--force` given:** replace the existing section unconditionally.

3. If `CLAUDE.md` does not exist, use Write to create it with the Golden Rules Block below as the full content.
   If `CLAUDE.md` exists but lacks the section, use Edit to append the Golden Rules Block to the end of the file.

4. Confirm to the user what was written (installed fresh, updated from vX.Y.Z, or already current) and that the Golden Rules are now active for every Claude Code session in this project.

## Golden Rules Block

Write or append the following content verbatim:

---

## Golden Rules

<!-- golden-rules v1.8.0 — do not remove; used by /golden-rules --update -->

GOLDEN RULES (MANDATORY — ALL WORK IN THIS PROJECT MUST FOLLOW THESE)

1. Security is paramount. Every design, implementation, and review decision must prioritize security. When in doubt, choose the more secure option and document the assumption in docs/assumptions.md.

2. Do not store secrets, passwords, keys, PII, or other sensitive data insecurely.
   - Passwords: Hash with a strong adaptive function (Argon2, bcrypt, scrypt). Never store plaintext or reversibly encrypted passwords.
   - API keys, tokens, secrets: Use environment variables or a secrets manager. Never commit to the repo or log.
   - PII: Encrypt at rest and in transit. Minimize collection and retention. Follow applicable privacy rules.
   - Other sensitive data: Use encryption or hashing as appropriate. Document non-obvious choices in docs/assumptions.md.

3. Always assume the application could be the target of exploitation. Design for untrusted input, defense in depth, least privilege, and secure defaults. Document any accepted risks in docs/assumptions.md.

4. All inputs must be sanitized, length-checked, typed (where the language supports it), and exercised by unit tests. All exceptions must be trapped and handled — never allow an unhandled exception to propagate to the user or crash a process silently.
   - Sanitize: strip, escape, or reject untrusted input before use in queries, templates, file paths, shell commands, or downstream calls.
   - Bound: enforce explicit maximum lengths/sizes on every input (request bodies, headers, query params, file uploads, buffers). In memory-unsafe languages (C, C++, unsafe Rust, cgo), check buffer sizes before every copy/read/write — no `strcpy`, `gets`, `sprintf`, or unbounded `memcpy`. Use `strncpy`/`snprintf`/bounded equivalents.
   - Type: use static types or runtime schema validation (Zod, Pydantic, JSON Schema, or language equivalent) at every boundary.
   - Test: every input handler and parser must have unit tests covering valid input, invalid input, boundary/oversized input, and the exception path. Each Golden Rule above (sanitization, length bounds, exception handling) must be verified by at least one test per handler.
   - Handle: every thrown or returned error must be caught, logged with context, and converted to a meaningful response or recovery action. No empty catch blocks. No bare `except:` or `catch (Throwable)` that hides the failure.

5. AI-generated copy must be free of AI'isms and other telltale signs of machine-written content. This applies to all user-facing text, marketing copy, docs, READMEs, commit messages, and comments produced with AI assistance.
   - Forbidden phrases (non-exhaustive): "delve into", "in today's fast-paced world", "it's important to note", "navigate the landscape", "unleash", "leverage" (as a verb), "tapestry", "embark on a journey", "in the realm of", "game-changer", "revolutionize", "seamlessly", "robust solution", "cutting-edge", "elevate your", "at the end of the day", "boasts", "testament to".
   - Forbidden patterns: gratuitous tricolons ("X, Y, and Z" stacked in every sentence), em-dash sandwiches in every paragraph, "Not only… but also…" constructions, hedging openers like "Certainly!" or "Absolutely!", closing summaries that restate the obvious, emoji bullets in serious copy.
   - Write like a human who has read the codebase: specific, concrete, and grounded in the actual subject. If a sentence would survive deletion without losing information, delete it. Edit AI output before shipping — never paste raw model output into customer-facing surfaces.

CODING & NAMING GUIDELINES (apply unless project explicitly overrides in docs/assumptions.md)

- camelCase for variables, functions, and filenames (see language-specific table below).
- Language-specific naming conventions:

  | Language | Variables/Functions | Files | Classes |
  |----------|-------------------|-------|---------|
  | JavaScript/TypeScript | camelCase | camelCase | PascalCase |
  | Python | snake_case | snake_case | PascalCase |
  | Go | camelCase (unexported) / PascalCase (exported) | snake_case | PascalCase |
  | SQL | snake_case | snake_case | N/A |
  | CSS classes | kebab-case | kebab-case | N/A |

- Strict typing and schema validation (e.g. Zod, Pydantic, or language-equivalent) for all inputs and boundaries.
- No hardcoded API keys, credentials, or secrets — use configuration or secrets management.
- No placeholder or stub code in production paths — write complete, functional code.
- Move task notes to docs/ToDo.md or docs/ — do not leave // TODO in the codebase for project tracking.
- Remove dead code before committing — commented-out code blocks, unused imports, unreachable functions, and orphaned files are not acceptable in production paths.

DESIGN & UX GUIDELINES (apply unless project explicitly overrides)

- Caching: Prefer designs that support caching where appropriate (HTTP cache headers, CDN, app-level) to improve performance.
- Light and dark mode: Support both themes with easy switching (toggle, system preference, or both). Persist user preference.
- Visual design: Prefer minimalist, clean designs. Avoid clutter; use clear hierarchy and whitespace.
- Responsive design: Layouts must be responsive — usable across mobile, tablet, and desktop. Use fluid layouts and touch-friendly targets.
- Accessibility: Choose accessible and pleasant color palettes. WCAG AA contrast minimum. Do not rely on color alone for meaning.

GIT HYGIENE (MANDATORY)

- Never commit or push directly to `main`. All changes must go through a branch and PR, no exceptions.
- Branch from the current release branch (or `main` if no release branch exists). Name branches `feature/`, `fix/`, `hotfix/`, or `claude/` as appropriate.
- If you find yourself on `main` with uncommitted changes, stash or move them to a new branch before committing.
- PRs targeting shared or release branches require at least one approval from a reviewer other than the author. For solo-maintainer repositories, self-merge is permitted — but CI must pass and the author must self-review the diff before merging.

TESTING STANDARDS (MANDATORY)

- Every module with logic must have corresponding tests. No untested business logic in production.
- Name tests descriptively: `test_<unit>_<scenario>_<expected>` or `describe/it` equivalents. A failing test name must explain what broke.
- Test behavior, not implementation. Mock external dependencies; do not mock the unit under test.
- Write the test first when fixing a bug — reproduce it as a failing test, then fix.
- Do not test framework internals, trivial getters/setters, or auto-generated code.
- Integration tests must cover critical paths: auth flows, payment flows, and data persistence boundaries.
- Tests must be deterministic — no flaky tests. Remove or fix any test that fails intermittently.

ERROR HANDLING (MANDATORY)

- Never swallow exceptions silently. Every catch block must log, re-throw, or return a meaningful error.
- Use structured error objects with a machine-readable code, human-readable message, and optional context. No bare string throws.
- Log errors with severity level, timestamp, request/correlation ID, and enough context to reproduce. No PII in logs.
- Distinguish client errors (4xx / validation) from server errors (5xx / unexpected). Return appropriate status codes.
- Fail fast on invalid state. Validate preconditions at function entry; do not let bad data propagate.
- Define and use a project-wide error hierarchy or error code enum. No ad-hoc error strings scattered across the codebase.

API & DATA CONTRACTS (MANDATORY)

- Validate all inputs at system boundaries with schema validation (Zod, Pydantic, JSON Schema, or equivalent). Reject invalid payloads before processing.
- Sanitize all user-supplied strings before use in queries, templates, or downstream calls. Assume all external input is hostile.
- Version APIs explicitly (URL path, header, or query param). Never introduce breaking changes to an existing version.
- Backward compatibility is required for at least one prior version. Deprecate before removing — never drop fields or endpoints without notice.
- Document every public endpoint or contract with request/response schemas. Undocumented APIs are not shippable.
- Use consistent naming across all API surfaces: plural resource nouns, standard HTTP verbs, consistent date/enum formats.

PERFORMANCE BASICS (MANDATORY)

- No N+1 queries. Use eager loading, joins, or batch fetches. Profile queries on realistic data volumes before shipping.
- All list endpoints must support pagination. No unbounded result sets. Default to reasonable page sizes.
- Use async/non-blocking I/O for network calls, file I/O, and any operation that can block the event loop or thread pool.
- Cache expensive computations and frequently-read data. Define TTLs and invalidation strategy — no stale-forever caches.
- Set timeouts on every external call (HTTP, DB, queue). No indefinite waits. Define retry policy with backoff for transient failures.
- Do not optimize prematurely, but do not ship known O(n^2) or worse algorithms on unbounded inputs. Document accepted performance trade-offs in docs/assumptions.md.
- Watch for memory leaks and race conditions. Long-lived processes must release listeners, timers, subscriptions, and connection pools. Concurrent access to shared state must be guarded by locks, atomics, transactions, or message passing — never assume "it works in dev."

LOGGING & OBSERVABILITY (MANDATORY)

- Emit structured logs (JSON or logfmt) with: timestamp, level, message, request/correlation ID, and contextual fields. No `print` / `console.log` for production code paths.
- Log every security-relevant event with enough context to investigate later: failed logins, successful logins from new IPs, password resets, permission changes, MFA challenges, account lockouts, rate-limit trips, CSRF/origin rejections, suspicious input rejections.
- Log every outbound integration event: email sends (provider, message ID, recipient hash, status), SMS sends, payment attempts, webhook deliveries, third-party API failures, retries, and timeouts. Include the upstream response code.
- Never log secrets, passwords, full tokens, full PAN/SSN/keys, or raw PII. Hash, redact, or omit. Log a stable correlation ID instead of the raw subject.
- Emit metrics for: request rate, error rate, p50/p95/p99 latency, queue depth, background job success/failure counts, external dependency latency, and the security/integration events above (auth_failures_total, email_send_failures_total, etc.).
- Wire alerts to the metrics that actually indicate user pain or breach risk. Alerts without an owner and a runbook are noise — remove them.

HEALTH CHECKS & UPTIME MONITORING (MANDATORY)

- Every deployable service must expose a `/healthz` (liveness) and `/readyz` (readiness) HTTP endpoint. Liveness reports "the process is up"; readiness reports "this instance can serve traffic right now" and fails when dependencies are unhealthy.
- Provide a deeper `/health` (or `/status`) endpoint that synthetically checks each critical dependency the service relies on: primary database, cache, queue, object storage, search index, and every third-party API in the request path (e.g. Resend or other email providers, Stripe, auth provider). Each dependency reports `ok` / `degraded` / `fail` with the last check timestamp and latency.
- The dependency check must also verify credential validity where the upstream supports it (e.g. token introspection, low-cost authenticated call) so expired API keys are caught before users hit them.
- Health endpoints must not require authentication for liveness/readiness, but the detailed dependency endpoint must not leak secrets, connection strings, or internal hostnames. Return HTTP 200 when healthy and 503 when not, so external monitors (NodePing, UptimeRobot, Pingdom, CloudFlare health checks) can alert correctly.
- Configure an external uptime monitor (e.g. NodePing) against the public URL and the deep health endpoint, with alerting routed to the on-call channel. A service without an external monitor is unmonitored.

CACHING & CDN (MANDATORY)

- Treat cacheability as a design decision per route. For every public response, set explicit `Cache-Control`, `ETag`/`Last-Modified`, and `Vary` headers — never rely on framework defaults.
- Static assets and immutable content (hashed filenames, versioned URLs, public marketing pages): `Cache-Control: public, max-age=31536000, immutable`. Serve through the CDN.
- Cacheable HTML / API responses: pick a deliberate `s-maxage` for the CDN and a shorter `max-age` for the browser. Use `stale-while-revalidate` for low-risk content.
- Non-cacheable responses (authenticated user pages, dashboards, mutation responses, anything containing PII or per-user data): `Cache-Control: private, no-store` and ensure `Set-Cookie` responses bypass shared caches. Audit any route that returns user-specific data to confirm it is not cached publicly.
- Provide an explicit cache-purge path for content that can change (deploy hook, admin action, or webhook → CDN purge API). Stale-forever caches are a bug.
- If hosted on CloudFlare, follow CloudFlare's published guidance: use Cache Rules (not deprecated Page Rules) for cache behavior, set Tiered Cache where it helps, use Cache Reserve only for content that justifies it, configure Bot Fight Mode / WAF / rate-limiting rules at the edge, set Origin Rules to strip cookies on static paths so they remain cacheable, and use the `CF-Cache-Status` header in monitoring to confirm hit ratio. For SPA/SSR apps, follow CloudFlare's framework-specific guidance (Workers, Pages, or the documented cache-key recipe for the framework in use).

CODE EFFICIENCY & DEPENDENCY HYGIENE (MANDATORY)

- Every line of code must have a clear purpose. No speculative abstractions, no dead branches, no unused exports, no "just in case" features.
- Minimize dependencies. Before adding a new package (npm, pip, cargo, NuGet, gem, go module), justify it: does the value outweigh the size, security surface, and maintenance cost? Prefer the standard library or a small focused implementation.
- Minimize binary and bundle size. Avoid heavyweight libraries when a small utility will do. Watch for dependency explosions — transitive bloat counts.
- Prefer clarity over cleverness. Avoid deep inheritance or abstraction layers that obscure what the runtime is actually doing — assume 80% of effort is debugging, so write code that is easy to step through.

RESOURCE STEWARDSHIP (MANDATORY)

- Treat RAM and CPU cycles as valuable commodities. Don't poll when you can subscribe; don't refresh when nothing changed; don't recompute what you can cache.
- Prefer async / non-blocking calls over sync calls when there is no added complexity penalty. Never block the UI thread on I/O (disk, network, IPC) — move it to a worker.
- Be cache- and allocation-aware in hot paths. Respect locality, batch work, and avoid unnecessary allocations or memory fragmentation, especially in native code (C/C++/Rust).
- Support a degraded or "lean" mode when the application could run on resource-constrained hardware. Failing to start is worse than degraded operation.
- Truthful telemetry: performance metrics must reflect actual system state. Do not smooth, round, or fabricate numbers for UI aesthetics.
- Apply language- and platform-specific best practices. The rules above describe intent; idiomatic implementation is contextual to the stack and the goals of the project.

PLATFORM-SPECIFIC GUIDELINES (MANDATORY)

- Apple platforms (iOS, iPadOS, macOS, watchOS, tvOS, visionOS): Follow the Apple Human Interface Guidelines (HIG) for UX, layout, typography, motion, accessibility, and platform conventions. Prefer native frameworks (SwiftUI, UIKit, AppKit) and idiomatic Swift; respect Apple's review and entitlement rules where relevant.
- Android: Follow Google's Material Design and the Android Developer guidelines for UX, navigation, and architecture (e.g. Architecture Components, Jetpack). Use Kotlin idioms and follow Google's Kotlin / Java style guides.
- Linux applications and scripts: Follow Red Hat's documented best practices (Fedora Packaging Guidelines, RHEL system design guidance, systemd conventions) where they apply. Otherwise follow the most widely accepted conventions for the language and ecosystem — POSIX shell guidelines, the Linux Filesystem Hierarchy Standard, freedesktop.org specs, and the relevant distro packaging norms.
- Windows: Follow Microsoft's official guidance for the target stack — Fluent Design / WinUI for modern UI, Windows App SDK / .NET conventions, and Microsoft Learn documentation for APIs, security, and packaging (MSIX).
- Cross-platform code: When shared UI or behavior spans platforms, branch to honor each host's conventions rather than picking a lowest common denominator. Document any deliberate deviations from a platform's guidelines in `docs/assumptions.md`.

ASSUMPTIONS TRACKING

Any time a non-obvious decision is made, record it in docs/assumptions.md:
- Assumption: one clear sentence
- Why: rationale
- Recorded by: <agent or developer name>
- Date: YYYY-MM-DD

---

## Output Format

Report to the user:
- Whether `CLAUDE.md` was created new or updated (appended).
- That the `## Golden Rules` section is now active.
- That every future Claude Code session in this project directory will load these rules automatically as context.
