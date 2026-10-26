---
name: java
description: Use when writing Java (LTS releases such as 21) with Gradle — command-line tools with picocli, records and sealed types for domain models, settlement or allocation algorithms, JUnit 5 tests and runnable distributions. Also use when choosing between picocli and Spring Boot, or when Gradle builds differ between machines.
---

# Java

Default: the current LTS JDK, Gradle with the wrapper (`./gradlew`) and Kotlin DSL, picocli for CLIs (Spring Boot when you need a long-running service), JUnit 5 + AssertJ, `application` plugin for a runnable distribution.

## Setup

1. `gradle init --type java-application --dsl kotlin`, commit the wrapper (`gradlew`, `gradle/wrapper/*`).
2. Set a toolchain in `build.gradle.kts` so Gradle downloads or selects the right JDK regardless of the machine's default:
   ```kotlin
   java { toolchain { languageVersion = JavaLanguageVersion.of(21) } }
   ```
3. Enable `-Xlint:all -Werror` for `compileJava`.

## Modelling with modern Java

- `record` for immutable data (`record Payment(String payer, long amountMinor, Set<String> sharedBy)`).
- `sealed interface` + `switch` pattern matching for closed sets of cases; the compiler checks exhaustiveness.
- `long` minor units or `BigDecimal` with an explicit `RoundingMode` for money; never `double`.

## Example: settling shared expenses

1. Compute each person's balance = paid − owed.
2. Distribute rounding remainders deterministically (e.g. to the people with the largest fractional parts, ties by name) and test that balances sum to exactly zero.
3. Greedy matching of the largest debtor with the largest creditor gives at most n−1 transfers; that is good enough in practice (the true minimum is NP-hard in general).
4. Print transfers in a stable order so output is diffable.

## CLI with picocli

- Annotate a `Callable<Integer>` with `@Command(mixinStandardHelpOptions = true)`; return the exit code.
- Keep parsing in the command class and logic in plain classes.
- Package with `./gradlew installDist` (scripts + jars) or a fat jar if a single file is required.

## Testing

- JUnit 5 `@ParameterizedTest` for tables of inputs; property checks (e.g. with jqwik) for invariants like "balances sum to zero".
- `./gradlew test` should not need network access after the first dependency download.

## Verification loop

1. `./gradlew build` (compiles with lint as errors, runs tests).
2. `./gradlew run --args="--help"` and a real example.
3. Run the distribution from `build/install/` on a machine with only a JRE.

## Pitfalls

- **`equals` on `BigDecimal`** compares scale (`2.0` ≠ `2.00`); use `compareTo` for numeric equality.
- **`Integer` caching:** `==` on boxed integers works only for small values; always use `equals` or unbox.
- **Default charset and locale:** pass `StandardCharsets.UTF_8` and `Locale.ROOT` for files and formatting.
- **Gradle daemons and caches** can hide configuration problems; reproduce CI failures with `--no-daemon --no-build-cache`.
- **Records with mutable components** (lists) are only shallowly immutable; copy with `List.copyOf` in the compact constructor.
