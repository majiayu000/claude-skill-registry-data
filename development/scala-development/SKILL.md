---
name: Scala Development
description: Senior Scala developer using functional programming and Typelevel ecosystem. Use when writing Scala code, implementing Scala features, or working with sbt/bloop projects. Used as a part of the XP skill.
---

# Scala Development

## Principles

- Functional programming techniques
- Avoid `Any`, `null`, `throw`, and unsafe patterns
- Prefer Typelevel ecosystem (cats, cats-effect, fs2)
- Use ADTs for domain modelling
- Errors as values (Either, EitherT, MonadError)

## Compilation Priority

1. **Check for `.bloop` directory first** (`ls -la`)

**If `.bloop` exists — use bloop:**

```bash
bloop compile <module-name>
bloop test <module-name>
bloop test <module-name> -o "*<filename>*"
```

Module name is `root` for non-modular projects.

**If no `.bloop` — use sbt:**

```bash
sbt compile
sbt test
sbt "testOnly *SpecName*"
```

2. **ALWAYS** run `sbt commitCheck` after completing code changes.

## Testing (MUnit)

```scala
class FeatureSpec extends munit.FunSuite:

  test("describes expected behaviour") {
    // Arrange
    val input = createTestData()

    // Act
    val result = functionUnderTest(input)

    // Assert
    assertEquals(result, expected)
  }
```

**Effectful tests (cats-effect):**

```scala
class FeatureSpec extends munit.CatsEffectSuite:

  test("async operation succeeds") {
    for
      result <- asyncOperation()
    yield assertEquals(result, expected)
  }
```

**Assertions:**

- `assertEquals(obtained, expected)`
- `assertNotEquals(obtained, unexpected)`
- `assert(condition)`
- `interceptMessage[ExceptionType]("message") { code }`

## Error Handling Patterns

```scala
// Prefer Either over exceptions
def parse(input: String): Either[ParseError, Value] = ???

// Use EitherT for effectful errors
def fetchAndParse(id: Id): EitherT[IO, AppError, Value] = ???

// MonadError for generic error handling
def process[F[_]: MonadError[*[_], Throwable]](input: Input): F[Output] = ???
```
