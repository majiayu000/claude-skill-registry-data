---
name: port-from-java
description: Port Java into Rust — class hierarchies onto enums and composition, exceptions onto Result, collections and streams onto Rust equivalents, and the traps (UTF-16 strings, silent integer wraparound, null, equals/hashCode contracts). Use when porting, rewriting, or migrating Java, a JVM service, a Spring or Jakarta application, or a Java library into Rust, when replacing a JVM component with a Rust one behind the same interface, or when the user asks how a Java construct translates to Rust.
---

# Port from Java

## A construct mapping and a boundary, nothing else

This skill maps Java to Rust and owns the Java boundary — a process seam
under end state A, and JNI under B and C. The parity contract, the five
phases, and the anti-patterns are `/port-to-rust`, which runs first and
stays running through the port. It covers Java, not Kotlin and not Scala —
the JVM is shared, the idioms are not.

## The end state, and why Java usually lands on A or B-as-a-service

| End state | In Java terms | JNI |
|---|---|---|
| A. Replacement | A standalone Rust binary or crate replaces a JVM service; the seam is the HTTP or gRPC boundary the system already has | Never appears |
| B. Rust core, JVM artifact is the product | The importable artifact keeps its name and its signatures; the engine underneath becomes Rust | Permanent public surface — signatures, exception classes, native libraries per platform, semver |
| C. Scaffold | The port ends standalone, but the JVM calls the Rust code while the migration is under way | Temporary, and deleted at cut-over |

The end-state decision is `/port-to-rust`. JNI is the most expensive
boundary in this set to write, to test, and to keep safe, and a mistake
in it is a JVM crash rather than an exception — the reason Java usually
lands on A. Prefer a process boundary over JNI unless per-call latency
genuinely forbids it; the mechanics for both are in `BOUNDARY.md`.

## The traps that break parity silently

The body carries these five because each one produces a port that passes a
naive test suite and is wrong; the full table is `MAPPING.md`.

| Trap | What actually differs |
|---|---|
| Integer overflow | Java wraps silently on overflow at every width. Rust panics in debug and wraps in release, so every arithmetic site is a decision: `wrapping_*` to reproduce Java, or checked arithmetic plus a new error path that the source never had |
| Strings are UTF-16 | `String.length()`, `charAt`, and `substring` count UTF-16 code units, so anything outside the basic multilingual plane counts as two. Rust `String` is UTF-8 and slices by byte. Every index arithmetic on a Java string is a decision, and emoji or CJK input is where the difference shows |
| `null` is everywhere and untyped | Any reference may be null, so the port must decide per field whether `Option` reproduces a real absence or papers over a state that should not exist — the second is `/type-driven-design`. Mapping every reference to `Option` produces Rust that is worse than the Java |
| `equals`/`hashCode` contracts | Derived `PartialEq`/`Hash` in Rust compare all fields; a hand-written Java `equals` often compares a subset, and collections branch on it. A port that derives where the source hand-wrote changes set and map behaviour silently |
| Checked versus unchecked exceptions | Checked exceptions are a declared contract and map to `Result` variants. Unchecked ones (`NullPointerException`, `IllegalStateException`, `IndexOutOfBoundsException`) were often *caught anyway* somewhere up the stack; grep for the catch sites before deciding any of them is a panic |

## Mapping, in one line

`MAPPING.md` holds the full table; a row is a starting point, not a
rewrite rule, and the Java corollary is that the port maps behaviour, not
structure — a row that reproduces a class hierarchy has failed even when
it compiles.

## Inheritance is the port, and the answer is usually an enum

A base class with a fixed set of subclasses is a Rust enum with a variant
per subclass, and that translation is where a Java port stops reading like
Java — `/type-driven-design`. A base class with an open set of
implementations is a trait, but only when the implementations genuinely
vary at runtime. Abstract classes carrying state map to a struct field
plus a trait, never to a supertrait with fields, because Rust has none,
and deep hierarchies flatten: three levels of inheritance is usually one
enum and two functions.

## The framework is not the program

Spring, Jakarta, and annotation-driven wiring exist to supply what Java
lacks; Rust supplies it with function arguments and constructors.
Dependency injection becomes explicit construction, usually a single
`App` struct built in `main`. Annotation processors and reflection-driven
mapping become derive macros or explicit code; the most common failed
Java port is reproducing the DI container in Rust, which produces a
trait-object graph nobody can follow, to solve a problem the language does
not have.

## The test suite is the corpus

JUnit cases are characterization input, and Java suites are usually the
richest in this set — mock-heavy, which means the mocks encode assumptions
worth reading. Mockito-based tests do not port; the behaviour they pinned
does. Harness shapes are `/rust-testing`.

## Collections, streams, and the ordering that leaks

`ArrayList` is `Vec`, `HashMap` is `HashMap`, but iteration order differs
between the two and Java code sometimes leaks it into output;
`LinkedHashMap` is `IndexMap`, `TreeMap` is `BTreeMap`. Streams map to
iterators almost directly, and parallel streams map to `rayon` — with the
note that a parallel stream over shared mutable state was already a bug
the port will surface as a compile error.

## Verification

Both sides:

```bash
cargo test --all-features
cargo clippy --all-targets --all-features   # add -- -D warnings only if the target repo has no lint config
mvn test        # or: ./gradlew test — the source still passes while both implementations run
```

Then the differential run over the recorded corpus, reported with its
denominator. The corpus must carry one case per trap: arithmetic at a
wraparound boundary; a string with a character outside the basic
multilingual plane; a null-bearing field; a `HashMap` key with a
hand-written `equals` comparing a subset of fields; an input that
triggered an unchecked exception in the source. A corpus that never
crosses those has not tested the port, it has tested the happy path.
