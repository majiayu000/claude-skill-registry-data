---
name: thalarch-kotlin-migration
description: "Semantics-preserving Java→Kotlin and Kotlin/tooling migration workflow for staged conversions where behavior, interop, nullability, framework semantics, serialization, persistence, and public API compatibility must not drift."
license: Apache-2.0
metadata:
  upstream: https://github.com/Kotlin/kotlin-agent-skills/tree/main/skills/kotlin-tooling-java-to-kotlin
  upstream-author: JetBrains
  modification-notice: Modified for Thalarch; see THIRD_PARTY_NOTICES.md.
---

# Thalarch Kotlin Migration

Migration is not transliteration. The first goal is preserved behavior and contracts; idiomatic
Kotlin comes only after the faithful baseline is understood and verified.

When an installed official Kotlin/JetBrains migration skill exactly matches the task, prefer that
skill for platform-specific facts and use this skill as the acceptance/verification envelope.

## 1. Detect before converting

For every file/package in scope, inspect imports, annotations, build plugins, and call sites to
detect the frameworks/contracts that can change conversion semantics.

Examples include:

- Spring / dependency injection / proxy annotations;
- JPA/Hibernate;
- Jackson/serialization;
- Dagger/Hilt/Guice;
- Retrofit/OkHttp;
- RxJava/coroutines;
- JUnit/Mockito/test frameworks;
- Lombok/generated members;
- Java reflection/service loading;
- public Java callers;
- Android/Compose/KMP source sets.

Load only the matching framework/platform guidance. Do not bulk-load unrelated migration rules.

## 2. Freeze migration invariants

Before editing, write the invariants that must survive:

1. **Behavior** — same externally observable results, exceptions, side effects, ordering.
2. **API/interoperability** — Java/Kotlin callers still see compatible signatures where required.
3. **Nullability/mutability** — platform/null contracts and collection mutation semantics stay
   intentional.
4. **Framework semantics** — annotations, proxyability, constructor/lifecycle requirements,
   serialization/persistence behavior remain valid.
5. **Identity/data semantics** — equality/hashCode, default values, numeric conversions, wire and
   persisted representations do not silently change.

Add domain-specific invariants when concurrency, transactions, ABI/binary compatibility, or
platform targets matter.

## 3. Staged conversion

Convert in explicit stages so semantic drift can be isolated.

### Stage A — faithful baseline

Translate structure and control flow as directly as practical. Do not simultaneously redesign the
architecture or “Kotlinize” every pattern.

### Stage B — nullability and ownership audit

Classify each Java platform type and nullable value from actual declarations, annotations, call
sites, and framework contracts. Replace routine `!!` with explicit boundary contracts or nullable
flows only when evidence supports the change.

Choose `val` vs `var` from real mutation behavior, not preference.

### Stage C — collections and type system

Preserve mutability, ordering, duplicate behavior, variance, numeric semantics, and public generic
contracts. Java `List`/`Map` does not automatically mean immutable Kotlin collection behavior.

### Stage D — idiomatic transformations

Only now consider properties, expression bodies, scope/collection functions, sealed/data/value
classes, extension functions, lambdas/SAM conversion, string templates, and coroutine/Flow idioms.

Every transformation must preserve the frozen invariants.

## 4. Framework-aware hazards

Review as applicable:

- Kotlin annotation use-site targets (`field:`, `get:`, `param:` etc.);
- proxy/open/no-arg requirements;
- generated Lombok API replaced by explicit Kotlin API;
- Jackson constructor/default/null behavior;
- JPA entity identity and proxy semantics;
- `@JvmStatic`, `@JvmField`, `@JvmOverloads`, `@Throws` only when real Java/framework callers need
  them;
- checked exception expectations at Java boundaries;
- wildcard/variance changes visible to Java callers;
- SAM overload ambiguity;
- reflection depending on field/getter/method names;
- Android parcelization/serialization/lifecycle behavior;
- KMP source-set/platform API leakage.

## 5. Batch order

For multi-file migration:

1. enumerate files in scope;
2. map dependencies/callers;
3. prefer leaf/internal dependencies before higher-level consumers when that reduces broken
   intermediate states;
4. migrate one bounded batch at a time;
5. compile/test after each batch;
6. run integration/public API checks after the full boundary is converted.

Do not parallelize two conversions that independently redefine the same public interface.

## 6. Git/history

Preserve file history when practical, but do not create commits merely because a migration recipe
suggests it unless the user authorized commit actions.

When Git history matters, use moves/renames rather than delete-and-recreate where the repository's
workflow supports it. External commit/push behavior remains governed by `thalarch-git`.

## 7. Verification

For each migrated batch:

- compile the affected target/source set;
- run existing targeted tests;
- run Java-call-site/interoperability tests when relevant;
- inspect generated/framework metadata when annotation placement matters;
- compare public API/wire/persistence behavior when required;
- run device/platform target evidence for Android/KMP behavior that compilation cannot prove.

A successful syntax conversion is not a successful migration.

## 8. Modernization after migration

Do not bundle broad architectural modernization into the conversion by default.

After the behavior-preserving migration is green, additional idiomatic refactors can be proposed or
performed if they are within scope, each with its own proof.

## Completion report

Report:

- files/batches converted;
- frameworks detected;
- invariants checked;
- compile/test/runtime evidence;
- API/interoperability changes intentionally made;
- items that remain `UNVERIFIED`.
