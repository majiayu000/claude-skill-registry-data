---
name: dotnet-conventions
description: "Use when writing or reviewing C#/.NET: async/await with cancellation, injection and service lifetimes, the type and visibility prohibitions, authorisation, disposal, nullability, EF Core, tests."
---

# dotnet-conventions

Step 6 of the pipeline (`WORKFLOW.md`). Frames the writing and review of C#/.NET code. Every rule below
holds in a repo with **nothing installed** (`CONVENTIONS.md`, rule A). **Special status**:
like `go-conventions`, no production experience behind this file yet — content comes from the Roslyn
analyzers (`Microsoft.CodeAnalysis.NetAnalyzers`, enabled by default since .NET 5), Meziantou.Analyzer and an
org catalogue for the stack, not from real review feedback. A solid base to be confronted with the first real
.NET project, not proven doctrine — which is why `theoden` reads it in a question register rather than as
settled house law.

**Relation to an org skill catalogue.** Where a company ships its own versioned catalogue for this stack, it
is the authority on **its** house style — its authorisation attribute, its allowed-package list, its
deployment targets — and overrides this block wherever the two differ. Several rules below are deliberately
strict prohibitions; they come from a real house style and are stated as such, because "allowed but rare" is
not a reviewable rule.

**An applied override is recorded, not hidden.** Write the code the governing rule actually requires, and
leave one short neutral trace addressed to whoever can decide (a line in the PR description, the task summary
or an ADR): which rule was overridden, by what, and that it is a resolved case. Never phrase it as "a conflict
between mentis and the house rules" to a non-technical stakeholder — that framing reads as broken even when
the case is a normal, resolved one, and has already caused a real project to get abandoned and restarted over
nothing. Raise one specific, named question to the decider only when no rule anywhere actually resolves the
case.

## When
As soon as C#/.NET code is written or modified, during `code` (6) or `tdd` (5).

## Steps

**Read only the sections the task actually touches.** The rules live one file per section under
`references/`; loading all twelve for a change that renames a field is waste, and a section read is a
section that has to be applied. If you are reviewing a whole diff, pick the rows whose trigger the diff
meets, not the whole table.

| § | Covers | Read it when | File |
|---|---|---|---|
| 1 | Async, cancellation, threading | an `async` method, a token or any concurrency is written | [`01-async-cancellation.md`](./references/01-async-cancellation.md) |
| 2 | Dependencies and logging | a dependency is injected or registered, a lifetime is chosen, config is read, or something is logged | [`02-dependencies-logging.md`](./references/02-dependencies-logging.md) |
| 3 | Authorisation | an endpoint, a hub method or a message consumer is added or modified | [`03-authorisation.md`](./references/03-authorisation.md) |
| 4 | Types and visibility: the prohibitions | a type is declared or a member's visibility is chosen | [`04-types-and-visibility.md`](./references/04-types-and-visibility.md) |
| 5 | Disposal, nullability, enumeration | a disposable is created, a null is silenced, or a sequence is enumerated or counted | [`05-disposal-nullability-enumeration.md`](./references/05-disposal-nullability-enumeration.md) |
| 6 | Data access and portability | an EF Core query or migration, the middleware order, a path, a clock or a culture | [`06-data-access-portability.md`](./references/06-data-access-portability.md) |
| 7 | Language idioms | new code has a choice of form (preferences, not prohibitions) | [`07-language-idioms.md`](./references/07-language-idioms.md) |
| 8 | Resilience and throttling | an outbound client, a retry, a timeout, or a limit on our own API | [`08-resilience-throttling.md`](./references/08-resilience-throttling.md) |
| 9 | What only breaks at publish | the project targets a trimmed, single-file or AOT publish, or reflection is written in one that might | [`09-publish-time-failures.md`](./references/09-publish-time-failures.md) |
| 10 | Testing | a test project, a fixture, a double, an HTTP-level or database-backed test is written | [`10-testing.md`](./references/10-testing.md) |
| 11 | Build hygiene: shared build files, central package versions | a project file, a shared build file or a package reference changes | [`11-build-hygiene.md`](./references/11-build-hygiene.md) |
| 12 | Web API shape: minimal APIs, typed results, status codes, error handler | an HTTP endpoint, its result type or error response is added or changed | [`12-web-api-shape.md`](./references/12-web-api-shape.md) |

## Output / checkpoint
Code compliant with the sections above, and a build with no new
`Microsoft.CodeAnalysis.NetAnalyzers`/Meziantou warning introduced by the diff. Checked by `gate` (7) and
`review` (8).

## Guardrails
**Most rules named in this block are off by default.** The .NET 10 rule pages list CA2007, CA2000, CA1063,
CA1851, CA1008, CA1515 and CA1812 as not enabled by default, and CA1822 as a suggestion only: a clean build
proves nothing about them until the project's analysis mode or editor configuration turns them on.

**Analyser configuration is a requirement, not advice.** Detect what the project has configured on the first
edit and write code that already passes it, rather than introducing findings someone else clears; its
baseline is not a licence to add to the baseline. Then **build what you touched and iterate to zero new
warnings before reporting the work done** — the second half is the one that gets skipped, and an unbuilt
claim is exactly what the pipeline's default-is-failure guarantee exists to catch (`WORKFLOW.md` §3).

No comments in the code produced. This block hasn't been confronted with a real production .NET project yet;
if a rule here diverges from a real observed need, fix this block rather than treating it as settled. The
Framework Design Guidelines (public API naming) only apply to shared library code, not to internal
application code — **and the analyser set is scoped to say so**, in the project's editor configuration
rather than file by file: those naming rules fire hardest on the test project, where nothing is a public
API and where underscored test names are the readable convention, so a solution that has not scoped them
starts by rewriting every test name. Under `AnalysisMode All` the same applies to the localisation rule on literal strings (CA1303, noise in an application with one language) and the never-instantiated rule on container-built classes (CA1812, §4.47). Existing threading, existing `var`, existing nested classes stay
until migrated — these rules govern **new** code, and a mass rewrite is its own decision
(`skills/simplify`, not this block). Where
an org catalogue is installed and disagrees, **it wins**.

## Origin
Ideas taken from the `Microsoft.CodeAnalysis.NetAnalyzers` Roslyn analyzers, Meziantou.Analyzer, the EF Core
documentation, the community-documented captive-dependency pattern, and an org skill catalogue for this
stack, extracted and de-identified. The full provenance, the source stamps and the refresh log are in
[`references/origin.md`](./references/origin.md). Read it when checking whether a rule is still current, not
when applying one.
