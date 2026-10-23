---
name: jqwik-testing
description: "Authors property-based tests for the JVM (Java + Kotlin) using jqwik - wires `@Property` test methods, `@ForAll` parameter annotations, `Arbitraries.integers/strings/etc` generators, custom `@Provide` arbitraries, and the JUnit 5 platform integration. Use when a JVM project needs PBT - alternative to JUnit-QuickCheck and Vavr's property-checking; tightly integrates with JUnit 5 so property tests run alongside conventional unit tests in the same Maven / Gradle pipeline."
---

# jqwik-testing

## Overview

jqwik is a JVM property-based testing library for Java and Kotlin that
integrates with JUnit 5, so property tests run alongside conventional
unit tests in the same Maven / Gradle pipeline ([jqwik-home][jh]).

[jh]: https://jqwik.net/

## When to use

- A JVM project (Java / Kotlin / Scala) tests via JUnit 5 and
  needs PBT alongside the existing unit tests.
- The team finds JUnit-QuickCheck or Vavr's PBT awkward; jqwik's
  JUnit 5 integration is more idiomatic.
- Properties hold for parsers / encoders / round-trip transforms.

## Step 1 - Install

Maven:

```xml
<dependency>
  <groupId>net.jqwik</groupId>
  <artifactId>jqwik</artifactId>
  <version>1.9.3</version>
  <scope>test</scope>
</dependency>
```

The artifact pulls in the JUnit 5 platform dependency transitively.
Version note: [references/jqwik-reference.md](references/jqwik-reference.md).

Gradle:

```gradle
testImplementation 'net.jqwik:jqwik:1.9.3'

test {
    useJUnitPlatform()
}
```

## Step 2 - Basic property

Per [jqwik-home][jh]:

```java
import net.jqwik.api.*;

class CartProperties {

    @Property
    boolean addingItemIncreasesCount(@ForAll int qty) {
        Cart cart = new Cart();
        cart.addItem(new Item("BOOK-001", qty));
        return cart.itemCount() == qty;
    }
}
```

The `@Property` annotation marks a property test (JUnit 5 hooks in
via the platform). `@ForAll` on a parameter means "jqwik generates
values for this." The method returns `boolean` (or `void` with
assertions).

By default jqwik runs each property with **1000 generated cases**
(more than Hypothesis's 100 or proptest's 256).

## Step 3 - Constrained generators

```java
@Property
boolean validQtyStaysInRange(@ForAll @IntRange(min = 1, max = 100) int qty) {
    Cart cart = new Cart();
    cart.addItem(new Item("BOOK-001", qty));
    return cart.itemCount() >= 1 && cart.itemCount() <= 100;
}
```

Constraint annotations live in `net.jqwik.api.constraints.*`
(`@IntRange`, `@LongRange`, `@StringLength`, `@Size`, `@NotEmpty`,
`@Email`, `@Positive`, ...). Full table:
[references/jqwik-reference.md](references/jqwik-reference.md).

## Step 4 - Custom arbitraries via `@Provide`

```java
class UserProperties {

    @Property
    boolean userJsonRoundTrip(@ForAll("validUser") User u) {
        String json = mapper.writeValueAsString(u);
        User back = mapper.readValue(json, User.class);
        return u.equals(back);
    }

    @Provide
    Arbitrary<User> validUser() {
        Arbitrary<Long> id = Arbitraries.longs().between(1, 1_000_000);
        Arbitrary<String> email = Arbitraries.strings()
            .alpha().ofMinLength(3).ofMaxLength(10)
            .map(s -> s + "@example.com");
        Arbitrary<Integer> age = Arbitraries.integers().between(18, 100);
        return Combinators.combine(id, email, age).as(User::new);
    }
}
```

The `@Provide` method returns an `Arbitrary<T>`; its name (or
the method name when omitted) is referenced from `@ForAll("...")`.

`Combinators.combine(...)` is the canonical way to assemble a
multi-field arbitrary; `.as(...)` constructs the target object
from the parts.

## Step 5 - Arbitraries catalog

Per [jqwik-home][jh], the `Arbitraries` API provides built-in
generators:

```java
Arbitraries.integers().between(0, 100);            // bounded int
Arbitraries.strings().alpha().ofLength(8);         // fixed-length alpha string
Arbitraries.of(Status.ACTIVE, Status.SUSPENDED);   // enum-like
Arbitraries.integers().list().ofMinSize(1).ofMaxSize(100);   // List<Integer>
```

Half-bounded generators, sets, maps, and `subsetOf`:
[references/jqwik-reference.md](references/jqwik-reference.md).

## Step 6 - Statistics + classification

```java
@Property
@Statistics
boolean evenAndOddDistribution(@ForAll int n) {
    Statistics.label("evenness").collect(n % 2 == 0 ? "even" : "odd");
    return true;
}
```

Statistics output reports the distribution of generated cases - 
useful for verifying the strategy generates the intended mix.

## Step 7 - Configuration

```java
@Property(tries = 5000, shrinking = ShrinkingMode.FULL, edgeCases = EdgeCasesMode.MIXIN)
boolean expensiveProperty(@ForAll long n) {
    // ...
}
```

| Field            | Default | Use                                                |
|------------------|--------:|----------------------------------------------------|
| `tries`          |   1000  | More for higher confidence.                        |
| `shrinking`      |   FULL  | `FULL` (default) / `BOUNDED` / `OFF`.              |
| `edgeCases`      |  MIXIN  | Mix in edge cases (0, MAX, MIN, ε, etc.) by default. |
| `seed`           |  random | Fixed seed for CI determinism.                     |
| `maxDiscardRatio`|   5     | Cap on `assume()` rejection ratio.                 |

For CI determinism:

```java
@Property(seed = "42")
boolean reproducibleProperty(@ForAll int n) { /* ... */ }
```

Or globally via `jqwik.config.properties`:

```properties
defaultSeed = 42
defaultTries = 1000
```

## Step 8 - CI integration

```bash
mvn test                  # runs JUnit 5 tests including @Property
gradle test               # same
```

No additional config beyond JUnit 5 platform.

## References

- [references/jqwik-reference.md](references/jqwik-reference.md) - constraint
  annotations, Arbitraries catalog, anti-patterns, limitations, version note.
- [jh][jh] - jqwik overview: `@Property`, `@ForAll`, `@Provide`,
  Arbitraries API, JUnit 5 integration.
- `hypothesis-testing`,
  `fast-check-testing`,
  `proptest-testing`,
  `quickcheck-testing` - 
  per-language siblings.
