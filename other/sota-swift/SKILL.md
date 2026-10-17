---
name: sota-swift
description: State-of-the-art Swift engineering rules (Swift 6 language mode) that Claude applies when writing or auditing Swift on ANY target — server-side services (Vapor, Hummingbird, SwiftNIO), CLIs, libraries, packages and apps. Covers optionals and error handling, value types and API design, Swift 6 data-race safety (Sendable, actors, isolation, cancellation), ARC and retain cycles, unsafe pointers and strict memory safety, security (CryptoKit/swift-crypto, Codable and NSKeyedUnarchiver, SQLKit raw SQL, Process, path traversal, NIOSSL/AsyncHTTPClient TLS), server hardening (auth middleware, cookie defaults, release builds), performance, and SwiftPM supply chain (Package.resolved, plugins and macros, SBOM). Trigger keywords - Swift, SwiftPM, Package.swift, Package.resolved, Vapor, Hummingbird, SwiftNIO, async/await, actor, Sendable, @MainActor, Task, Codable, ARC, weak self, Unsafe pointer, Swift Testing, XCTest, SwiftLint, swift-format, server-side Swift. Use for BOTH building and auditing Swift code.
---

# SOTA Swift (2026)

Expert-level rules for producing and auditing production Swift, on any target. Swift is a
language first and an Apple-platform toolkit second: a Vapor service on Linux, a CLI and an
iOS app share every rule here. **Platform concerns route elsewhere**: app lifecycle, store
review, Keychain, push and offline sync → [`sota-mobile`](../sota-mobile/SKILL.md); containers → [`sota-sandboxing`](../sota-sandboxing/SKILL.md);
telemetry → [`sota-observability`](../sota-observability/SKILL.md).

**Version floor.** swift.org publishes **no end-of-life or support-window policy** for older
Swift releases (searched the swift.org site source, 2026-10-07); the nearest written bar is the
Swift Server Workgroup's graduation criteria — *"Support new GA versions of Swift within 30d"*
and a *"documented support strategy for at least one previous major version"*. So pin the
toolchain you build with, verify the latest release at swift.org, and treat the **language
mode** as the load-bearing line: Swift 6 mode makes data-race safety a compile error.
Feature notes below name the release that introduced each feature.

## BUILD mode

1. Declare the toolchain and language mode in `Package.swift` (`swift-tools-version: 6.x`,
   `swiftLanguageModes:` — `swiftLanguageVersions` is deprecated since 6.1, SE-0441) and pin the
   toolchain for CI ([rules/08](rules/08-tooling-ci-testing.md)).
2. Read the rules files that match the work (index below). Concurrency ([rules/03](rules/03-concurrency.md)) applies to
   any code with `async`, actors or shared state; security ([rules/05](rules/05-security.md)) to anything touching
   input, files, processes, SQL or the network; server code also reads [rules/06](rules/06-server-side.md).
3. Write value types, exhaustive enums and non-optional straight-line code ([rules/01](rules/01-idioms-and-errors.md)); keep the
   public surface small and evolvable ([rules/02](rules/02-api-design.md)).
4. **Self-audit last**: walk each loaded file's Audit checklist against the diff, then the
   router's principle 5 (abuse control, transport, tests, logs) before presenting.

## AUDIT mode

1. Recon: `Package.swift` (tools version, language modes, `unsafeFlags`, plugins, macros,
   binary targets), `Package.resolved`, CI config, the server framework in use.
2. Run what is installed (never install unasked): the compiler in Swift 6 mode with
   `-warnings-as-errors`, SwiftLint, `swift build --sbom-spec` (6.4+), a dependency scanner
   ([rules/09](rules/09-supply-chain.md)), CodeQL's Swift queries where CI has them.
3. Walk every applicable rules file's Audit checklist; each probe below is a grep you can run.
4. Report in the canonical format; severity per the table, chain closure per the [`sota`](../sota/SKILL.md) router.

### Severity conventions (refines the router's [`rules/03`](rules/03-concurrency.md) §1 inside this skill)

| Severity | Swift examples |
|---|---|
| Critical | SQL built with `\(unsafeRaw:)` from request input; `certificateVerification: .none` on a production client; `/bin/sh -c` with interpolated input; `NSKeyedUnarchiver.unarchiveObject(with:)` on untrusted bytes |
| High | data race behind `nonisolated(unsafe)` / `@unchecked Sendable` on reachable state; unauthenticated route group missing its guard middleware; session cookies left at Vapor's `isSecure: false` default; debug build shipped (raw error text to clients); plugin/macro dependency unreviewed on a Linux CI that runs them unsandboxed |
| Medium | `try!`/`!`/`as!` on input-derived values; `Double` for money; unbounded `AsyncStream` buffer; `Task.detached` without reason; ReDoS-prone regex on input |
| Low | `try?` on a write path; `any P` on a hot path; missing `final`; IUO outside two-phase init |

### Finding format

`file:line | rule | severity | effort | fix` — the router's canonical row; expand each
surviving finding to the router's [`rules/03`](rules/03-concurrency.md) §2 evidence block.

## Rules index

| File | Read this when… |
|---|---|
| [rules/01-idioms-and-errors.md](rules/01-idioms-and-errors.md) | Writing any Swift: value types vs classes, enums, optionals and force-unwraps, `throws`/typed throws/`try?`, integer overflow and money, dates and clocks |
| [rules/02-api-design.md](rules/02-api-design.md) | Designing a module or package API: protocols vs generics (`some`/`any`), access control (`public`/`package`), library evolution and `@frozen`, deprecation, SemVer |
| [rules/03-concurrency.md](rules/03-concurrency.md) | Any `async`, actor, `Task`, `Sendable` or shared mutable state: Swift 6 mode, isolation escape hatches, reentrancy, structured concurrency, cancellation and timeouts, streams and backpressure |
| [rules/04-memory-and-unsafe.md](rules/04-memory-and-unsafe.md) | Retain cycles, `weak`/`unowned`, resource ownership (`defer`, `~Copyable`), unsafe pointers, C interop, strict memory safety |
| [rules/05-security.md](rules/05-security.md) | Input, files, processes, SQL, HTTP, crypto, decoding, regex, logs, secrets — the language-level security surface |
| [rules/06-server-side.md](rules/06-server-side.md) | Vapor/Hummingbird/SwiftNIO services: auth middleware order, cookie and session defaults, release vs debug, body limits, error responses, Linux Foundation |
| [rules/07-performance.md](rules/07-performance.md) | Profiling first, allocations, ARC traffic, existentials, copy-on-write, benchmarks in CI |
| [rules/08-tooling-ci-testing.md](rules/08-tooling-ci-testing.md) | Toolchain pinning, warnings-as-errors, SwiftLint/swift-format and every suppression, Swift Testing/XCTest, sanitizers, flaky tests |
| [rules/09-supply-chain.md](rules/09-supply-chain.md) | `Package.resolved`, version requirements, registries and package identity, plugins and macros (build-time code), binary targets, SBOM, vulnerability scanning, adopting a package |

## Top 10 non-negotiables

1. **Swift 6 language mode** for all first-party code; every `nonisolated(unsafe)`,
   `@unchecked Sendable`, `@preconcurrency` and `unowned(unsafe)` carries a comment naming the
   invariant that makes it safe.
2. **No `!`, `try!` or `as!` on values derived from input**; `guard let`/`throw` instead.
3. **Untyped `throws` on public APIs**; typed throws only inside a closed boundary.
4. **Structured concurrency first**; every unstructured `Task` has an owner that cancels it;
   long loops check cancellation.
5. **No retain cycles**: escaping closures stored by `self` capture `[weak self]`.
6. **SQL binds, never interpolates**: no `\(unsafeRaw:)`/`unsafeSQL:` with input; processes
   take an argument array, never `/bin/sh -c`.
7. **TLS verification stays on**; minimum TLS 1.2 set explicitly on NIOSSL clients.
8. **Ship release builds** (`swift build -c release`); production behaviour never depends on a
   debug build's `#if DEBUG` or Vapor's compile-time `isRelease`.
9. **Commit `Package.resolved` and resolve with `--force-resolved-versions` in CI**; review
   plugins and macros as build-time code — on Linux they run unsandboxed.
10. **Warnings are errors in CI**, and every SwiftLint/compiler suppression is visible and
    justified.

## Operating notes

- Swift moves fast; Swift Evolution proposal status (swift.org/swift-evolution) is the primary
  source for whether a feature has shipped. "Accepted" is not "implemented".
- Facts here carry their verification date; re-check before pinning a version or quoting a
  default.
