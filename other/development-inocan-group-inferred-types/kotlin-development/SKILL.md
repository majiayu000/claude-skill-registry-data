---
name: Kotlin Development
description: Senior Kotlin developer using http4k and functional patterns. Use when writing Kotlin code, implementing features, or working with Gradle projects. Used as a part of the XP skill.
---

# Kotlin Development

## Principles

- Immutable data structures (`data class`, `copy()`)
- Avoid `null` where possible; use `?` types explicitly
- Prefer `Result4k` for domain errors over exceptions
- Extension functions for domain conversions
- Four-space indentation, 120-char line limit

## Build Commands

```bash
./gradlew :<module>:test           # Run module tests
./gradlew :<module>:run            # Run service locally
./gradlew test                     # Full test suite
```

## Testing (JUnit 5 + Strikt)

```kotlin
class FeatureTest {
    @Test
    fun `describes expected behaviour`() {
        // Arrange
        val input = createTestData()

        // Act
        val result = functionUnderTest(input)

        // Assert
        expectThat(result).isEqualTo(expected)
    }
}
```

**Assertions:**

- `expectThat(obtained).isEqualTo(expected)`
- `expectThat(list).isEmpty()` / `.hasSize(n)`
- `expectThat(result).isA<SuccessType>()`

**Mocking (MockK):**

```kotlin
val mockService = mockk<MyService>()
every { mockService.doThing(any()) } returns expected
verify { mockService.doThing(input) }
```

## http4k Contract Pattern

```kotlin
class MyContract(val service: MyService) {
    fun contractRoutes(): List<ContractRoute> =
        listOf(mySpec to ::myHandler)

    private val requestLens = Body.auto<MyRequest>().toLens()
    private val responseLens = Body.auto<MyResponse>().toLens()

    private val mySpec = "/endpoint" meta {
        tags += Tag("Domain")
        summary = "Description"
        receiving(requestLens to exampleRequest)
        returning(Status.OK, responseLens to exampleResponse)
    } bindContract Method.POST

    private fun myHandler(request: Request): Response {
        val body = requestLens(request)
        val result = service.process(body.toDomain())
        return Response(Status.OK).with(responseLens of result.toApi())
    }
}
```

## Domain Conversion Pattern

```kotlin
data class ApiRequest(val id: Long, val name: String) {
    fun toDomain(): DomainModel = DomainModel(
        id = id,
        name = name
    )
}

fun DomainModel.toApi(): ApiResponse = ApiResponse(
    id = this.id,
    name = this.name
)
```

## Database (kotliquery + JSONB)

```kotlin
object MyStore : TransactionalGeneralStore<MyEntity, MyOperations>(
    dbSessionProvider = Db,
    tableName = "my_table"
) {
    override fun createStore(session: TransactionalSession) =
        MyOperations(session, tableName)
}

class MyOperations(session: TransactionalSession, tableName: String) :
    TransactionalOperations<MyEntity>(
        session = session,
        tableName = tableName,
        getId = { it.id },
        toJson = { it.jsonString() },
        fromJson = { it.to<MyEntity>() }
    ) {

    fun findById(id: UUID): MyEntity? {
        val query = queryOf(
            "SELECT data FROM $tableName WHERE data->>'id' = ?",
            id.toString()
        )
        return session.run(query.map { it.string("data").to<MyEntity>() }.asSingle)
    }
}
```

## Test Factories

```kotlin
// In TestHelpers.kt
fun MyModel.Companion.sample(
    id: UUID = UUID.randomUUID(),
    name: String = "default"
) = MyModel(id = id, name = name)

// Usage
val model = MyModel.sample(name = "custom")
```

## Service Pattern

```kotlin
class MyService(val store: MyStore, val monitor: Monitor) {

    fun process(input: DomainModel): Result<Output, DomainError> {
        monitor.notifyOf("Processing ${input.id}")
        return store.transaction { ops ->
            ops.findById(input.id)
                ?.let { existing -> update(ops, existing, input) }
                ?: create(ops, input)
        }
    }
}
```
