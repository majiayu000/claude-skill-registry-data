---
name: thalarch-router
description: >
  Chooses the smallest compatible process, language, domain, platform, visual, cognitive, and
  installed-skill stack for a task. Use before complex work and after project discovery. Combines
  autonomous skill intelligence with task, stack, risk, evidence, source-grounding, context,
  no-regression, memory/experience, teacher/eval, and in-flight doubt routing instead of requiring
  the user to manually name the best skills.
---

# Thalarch Router

Use `thalarch-skill-intelligence` before loading heavy instructions.

## Decision

1. Inspect the skill inventory exposed by the current host session.
2. Shortlist skills by description without opening every full `SKILL.md`.
3. Identify the task's primary goal/failure type.
4. Detect the actual language/runtime/toolchain/framework from repository evidence.
5. Estimate risk: low / medium / high.
6. Identify evidence needed for completion.
7. Decide whether stale/large context requires `thalarch-context`.
8. Decide whether relevant prior project/general experience should be retrieved with `thalarch-memory`.
9. Decide whether version-sensitive external facts require `thalarch-source-grounding`.
10. Decide whether a working high-blast-radius subsystem needs `thalarch-no-regression` before mutation.
11. Decide whether a non-trivial D2+ decision needs an in-flight `thalarch-doubt` challenge.
12. Decide whether an independent teacher/judge loop adds real information.
13. Select the smallest compatible process + language + domain + platform stack.
14. Prefer project-local and current official platform/vendor skills when they are more specific
    than a generic Thalarch or community skill.
15. Remove redundant or conflicting skills instead of stacking everything.
16. Re-run selection after preflight when new stack/version/root-cause evidence changes the route.
17. For image inputs/outputs, classify inspect/generate/edit/vector/capture/compare/annotate/optimize.

## Core process routing

- small safe edit → `thalarch-code-craft` + lightweight review;
- isolated bug/regression → `thalarch-debug` + language overlay + `thalarch-test` + review;
- working subsystem + risky targeted improvement → `thalarch-no-regression` + relevant domain/language
  skills + targeted test/review;
- broken feature/module with several dependent surfaces → bounded scope/trace/diagnose workflow
  using codebase intelligence + debug + relevant language/domain skills;
- feature → `thalarch-spec` + language overlay + `thalarch-test` + review;
- architecture/system design → `thalarch-spec` + `thalarch-codebase-intel` +
  `thalarch-architecture` + relevant language/domain + deep review;
- behavior-preserving refactor → `thalarch-refactor` + language overlay + test + review;
- performance → `thalarch-performance` + language overlay + performance review;
- API/service boundary → language overlay + `thalarch-api` + security/data skills as relevant;
- database/ORM/migration → language overlay + `thalarch-data-sql` + test/review;
- dependency/toolchain change → `thalarch-dependency` + affected language/domain + compatibility verification;
- production service/job/queue/external integration telemetry → `thalarch-observability` + relevant
  language/security/performance skills;
- security → `thalarch-security` + relevant language/domain + review council;
- CI → `thalarch-ci` + language/toolchain overlay + security when relevant;
- Git/publication → `thalarch-git` + review + remote-state verification.

`thalarch-code-craft` is the default universal coding overlay for meaningful mutation/review unless
a stronger project-specific coding skill already covers the same concern without losing Thalarch's
scope and verification invariants.

## Cognitive routing

Do not load cognitive skills mechanically on every task.

- relevant verified prior experience may change the first hypothesis → `thalarch-memory`;
- repeatedly revisited repository with an authorized durable local knowledge sink →
  `thalarch-project-brain` + `thalarch-memory`;
- verified non-trivial task produced a reusable lesson → `thalarch-compound` + `thalarch-experience`;
- prompt/skill/router/agent behavior is being tuned against a stable evaluator →
  `thalarch-teacher` + `thalarch-autoresearch`;
- high-value implementation benefits from independent artifact feedback before final verification →
  `thalarch-teacher`, but reuse an existing independent reviewer/verifier when it already covers the need.

Memory retrieval happens before broad rediscovery only when relevance is plausible. Retrieved memory
remains `MEMORY` trust until current evidence revalidates load-bearing claims.

Durable storage is never implied by retrieval. Persist project/general memory only through an
authorized sink and the `thalarch-memory` evidence/privacy/generalization gates.

A generic Thalarch rule must not self-modify from one successful task. Use frozen evaluation,
holdout/counterexamples, `thalarch-autoresearch`, and independent teacher/verifier evidence before
promoting general behavior.

## Epistemic process overlays

These are not loaded mechanically on every task.

### Context hygiene

Add `thalarch-context` when:

- the repository/task area is unfamiliar;
- a large amount of source/log/docs/memory would otherwise enter the main context;
- the task switches modules/features;
- a long session/compaction risks stale assumptions;
- outputs start ignoring current project conventions or referencing unsupported facts.

### Source grounding

Add `thalarch-source-grounding` when a load-bearing decision depends on:

- framework/library/runtime version behavior;
- exact external API/signature/configuration;
- deprecation/migration guidance;
- browser/platform compatibility;
- current official vendor recommendations.

Pure local logic does not need documentation ceremony merely because a dependency exists nearby.

### No-regression contract

Add `thalarch-no-regression` when the target subsystem currently works and the task risks breaking
adjacent behavior, especially cache, playback, persistence, sync, migration, concurrency, retries,
networking, or stateful UI.

Use it to separate the suspected problem from must-preserve behavior and to force `AUDIT ONLY` when
the suspected defect is still `UNKNOWN`/weak inference. A similar fix from another repository is a
research lead, not proof of a local bug.

### In-flight doubt

Add `thalarch-doubt` for D2+ decisions when at least one is true:

- branching/state semantics change materially;
- a service/module/data boundary changes;
- correctness relies on concurrency/idempotency/ordering/lifecycle/ownership;
- the codebase is unfamiliar and a mistaken premise would propagate;
- the decision is difficult to reverse or high-blast-radius;
- the leading answer is confident but not strongly disconfirmed.

A good failing regression/invariant test can serve as executable disconfirmation for the specific
behavioral claim. Do not spawn reviewers for mechanical edits.

## Language detection and routing

Use source files plus build manifests. Do not infer from repository name alone.

- Java (`.java`, Maven/Gradle JVM Java source) → `thalarch-java`;
- Kotlin (`.kt`, `.kts`, Kotlin Gradle plugins) → `thalarch-kotlin`;
- Python (`.py`, `pyproject.toml`, Python package metadata) → `thalarch-python`;
- TypeScript/JavaScript (`.ts`, `.tsx`, `.js`, `.jsx`, package scripts) → `thalarch-typescript`;
- Go (`.go`, `go.mod`) → `thalarch-go`;
- Rust (`.rs`, `Cargo.toml`) → `thalarch-rust`.

When the current host exposes a matching language specialist/subagent, use it for substantial
language-specific implementation or review. If that named specialist is unavailable, use the
canonical language skill in the strongest compatible host-native context instead of inventing an
agent name.

If an installed project-local or official language/framework skill is more specific, use it with or
instead of the generic language overlay as judged by `thalarch-skill-intelligence`.

For mixed-language changes, choose the minimum set that covers the changed boundary. Use separate
specialists for independent implementation surfaces and an explicit integration stage for the
shared contract.

If no dedicated language skill exists, use `thalarch-code-craft`, project-native conventions, and
current primary documentation for version-sensitive APIs.

## JVM specialization

Add only when evidence proves the surface:

- Java/Kotlin shared-state, threads, executors, futures, virtual threads, proxy async, locks or
  thread-safety → `thalarch-jvm-concurrency` plus the language skill;
- Kotlin + JPA/Hibernate/Spring Data entity/repository/fetch/transaction work →
  `thalarch-kotlin-jpa`, while preferring an available official Kotlin JPA skill for exact facts;
- Java → Kotlin or Kotlin/tooling conversion where semantic compatibility matters →
  `thalarch-kotlin-migration`, plus the most specific installed official Kotlin migration skill;
- ordinary Java/JVM JPA work → language skill + `thalarch-data-sql`, and an installed focused JPA
  skill when it adds current framework-specific evidence;
- major JDK/framework migration → `thalarch-dependency` + `thalarch-java` +
  `thalarch-source-grounding` and a focused installed migration skill when compatible.

Do not activate every JVM skill for every JVM repository.

## Platform routing

When installed and relevant, automatically consider current official/vendor platform skills exposed
by the host — for example Kotlin/JetBrains tooling, Android, browser/Chrome tooling, Firebase,
Modern Web, cloud/vendor SDKs, or other curated integrations. Do not require the user to remember
their names.

Platform skills supply current platform expertise; Thalarch supplies scope, causal debugging,
source grounding, review, evidence, memory discipline, and cold verification.

## Android routing

Kotlin/Java Android work normally combines the language layer with `thalarch-android` and the
smallest specialist stack that matches the proven surface:

- Media3/ExoPlayer/session/service/Android Auto/queue/cache/preload/recovery/audio processors →
  `thalarch-media3`;
- Compose product UI/redesign/settings/media surfaces → `thalarch-compose-ui`, with
  `thalarch-design-system` when substantial visual-system extraction is useful;
- fuzzy automatic provider/catalog/media identity matching → `thalarch-entity-matching`;
- locale resources/translated UI/RTL/placeholders → `thalarch-localization`;
- memory/cache/hot-path work → `thalarch-performance`, and `thalarch-no-regression` when the current
  subsystem is working;
- Room pagination/query shape → `thalarch-data-sql` plus the Android paging playbook;
- deprecated AndroidX/Compose/Media3 APIs → `thalarch-source-grounding` plus the Android deprecation
  playbook.

For Android runtime/device behavior require runtime/device evidence appropriate to the claim.
For visually consequential Compose work require actual rendered pixels/interaction evidence rather
than source-only confidence.

Do not activate every Android specialist for every Android task.

## Web / visual routing

- full website, open art direction → design system + `thalarch-web-design` + best installed frontend
  design/platform skill + language overlay + browser QA + design review;
- screenshot/mockup/reference matching is central → add `thalarch-image-to-code`;
- redesign existing product → spec + existing-system audit + UI/web design + best installed redesign
  skill + browser/device QA + visual review;
- new raster image → `thalarch-image` + `thalarch-imagegen` + `thalarch-visual-qa`;
- precise image edit → `thalarch-image` + `thalarch-imagegen` + `thalarch-visual-qa`;
- inspect/compare image → `thalarch-image` + `thalarch-visual-qa`;
- exact logo/icon/diagram → `thalarch-image` + deterministic vector/code path + `thalarch-visual-qa`;
- UI with generated artwork → UI/web stack + `thalarch-imagegen` + runtime QA + visual QA.

Do not force image-first generation when visual reference creation is not actually useful.

## Risk signals

Raise risk for auth/security/privacy, shared concurrency, persistence/schema migration,
network/protocol parsing, public API/ABI/wire compatibility, build/release/signing/toolchain,
broad refactor, user data, hard-to-reproduce runtime behavior, cross-language/service interfaces,
unsafe/FFI/native code, unmeasured hot paths, architecture boundary changes, exact brand
preservation, “change only X” image edits, production assets with exact text/transparency/dimensions,
and durable memory containing sensitive/stale/high-impact project knowledge.

For working high-blast-radius systems, the risk response is not automatically “more refactoring”;
it is usually a narrower preservation contract plus stronger evidence.

## Output

Return a compact routing decision:

`Mode: <...>`
`Languages/stack: <detected evidence>`
`Risk: <...>`
`Skills: <ordered minimal stack>`
`Agents: <only specialists actually available and needed>`
`Memory: <retrieval/persistence decision when relevant>`
`Evidence required: <...>`
`Deferred/rejected: <only close alternatives when useful>`
