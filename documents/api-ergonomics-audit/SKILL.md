---
name: api-ergonomics-audit
description: >
  Use this when auditing the consumer-facing surface of a new or extended SDK
  client — constructor shape, quickstart length, doc discoverability, runnable
  example coverage, sentinel/exception exposure, parameter ordering convention,
  sibling-package consistency. Feeds api-ergonomics-devil's NEEDS-FIX findings
  at design and impl exits.
  Triggers: quickstart, ergonomics, examples, boilerplate, consumer experience, sentinel error, exception class, ctx-first, kw-only.
version: 1.1.0
last-evolved-in-run: v0.6.0-rc.0-sanitization
status: stable
tags: [ergonomics, sdk, api-design]
cross_language_ok: true
---

<!-- Cross-language: body is language-neutral; cross-references name language-pack siblings (`go-api-ergonomics-patterns`, `python-api-ergonomics-patterns`, `python-doctest-patterns`, `go-example-function-patterns`). The leakage scripts honor `cross_language_ok: true`. -->


# api-ergonomics-audit (v1.1.0)

## Scope

Defines the language-neutral consumer-experience checklist used by the api-ergonomics-devil agents (`sdk-api-ergonomics-devil-go`, `sdk-api-ergonomics-devil-python`) at design and impl exits. Language-specific realizations of "what good looks like" live in `go-api-ergonomics-patterns` and `python-api-ergonomics-patterns`.

## Rationale

An SDK succeeds or fails on the first ten minutes of a new integrator's experience. Every extra line in "hello world", every missing example in the docs, every undocumented failure mode that surfaces as a string-matched error, and every parameter naming inconsistency costs hundreds of future-user hours. This skill is a checklist the design-phase devil evaluates against; because it is SHOULD-priority (not MUST), findings are NEEDS-FIX rather than BLOCKER unless combined with a MUST-violation.

## Activation signals

- Phase 1 design exit — any new exported package gets the audit.
- Phase 2 review wave — api-ergonomics-devil scheduled.
- TPRD §11 "Usage examples" section is empty or thin.
- No runnable example functions in the new package.
- Quickstart in README exceeds ~10 lines.
- Design proposes a method that returns multiple distinct error types.

## The 8-point checklist (language-neutral)

1. **Quickstart ≤5 lines** (excluding imports + error handling). "Hello world" is **construct → use → close**. If it takes more, either Config has too many required fields (consider defaults) or the constructor has the wrong shape.
2. **Constructor shape matches sibling packages** in the same SDK. Don't ship a different shape for every client.
3. **Cancellation primitive is the FIRST parameter** (or first-class) on every I/O method. Convention per language adapter — see realizations.
4. **Every exported symbol has documentation** starting with the symbol name. The first sentence is the symbol's purpose.
5. **At least one runnable example per exported package.** Renders in the language's package documentation viewer.
6. **Failure modes are exposed as discriminable types.** Sentinel error or exception class per failure mode — discoverable through the language's typed-error mechanism, not string matching.
7. **No forced caller boilerplate.** If every call needs a multi-line wrapper to be useful, the API is wrong.
8. **Consistency with sibling packages** in the same SDK. Pick one of `Close` vs `Shutdown`, one of `Duration` vs seconds-as-int, etc., and stick to it.

## Severity ladder for findings

- **BLOCKER** — cancellation primitive not first/scoped, multi-error returns, panic on documented valid input, surprising zero-value-config that silently misconfigures
- **HIGH** — missing runnable example, missing exception/sentinel for documented failure mode, quickstart >5 lines
- **MEDIUM** — sibling-package inconsistency, missing default factory, field-naming drift
- **LOW** — doc phrasing, ordering of options, package-doc thinness

## Audit output format

Per `agents/sdk-api-ergonomics-devil-go.md` and `agents/sdk-api-ergonomics-devil-python.md`: re-write the quickstart by hand from the README; if the result is >5 lines OR needs unfamiliar primitives, mark NEEDS-FIX with a finding ID like `IM-401`. Every finding carries a suggested fix. Verdicts land in `runs/<id>/impl/reviews/api-ergonomics-devil-<lang>.md`. Review-fix loop per `review-fix-protocol`.

## Greenfield vs retrofit

In Mode A (new package), fix every HIGH+ finding before Phase 2 exit — the cost of shipping a bad API is lifetime-of-the-SDK. In Mode B/C, fix HIGH+ where the change is source-compatible; if it requires a major bump, defer to the next major release and record in `docs/PROPOSED-API-CHANGES.md`.

## Language realizations

- `go-api-ergonomics-patterns` — Go realization (5-line quickstart shape, runnable example functions with deterministic-output blocks, sentinel discoverability, cancellation-first parameter ordering, doc-comments starting with the symbol name, compile-time interface checks).
- `python-api-ergonomics-patterns` — Python realization (async-context-manager quickstart, doctest example blocks, exception class hierarchy, frozen-dataclass keyword-only constructor, async enter/exit shutdown protocol, Protocol-typed ports, type-marker file).

## Cross-references

- `go-sdk-config-struct-pattern` / `python-sdk-config-pattern` — constructor shape (drives quickstart length)
- `go-example-function-patterns` / `python-doctest-patterns` — runnable-example authoring conventions
- `go-error-handling-patterns` / `python-exception-patterns` — discriminable failure modes
- `sdk-semver-governance` — ergonomics-driven API rewrite triggers semver bumps
- shared-core `spec-driven-development` — TPRD §11 "Usage" section is where the quickstart lands first
