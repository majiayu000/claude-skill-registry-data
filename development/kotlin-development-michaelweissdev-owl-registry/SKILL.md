---
name: kotlin-development
description: >
  Develop, test, and refactor idiomatic Kotlin applications across JVM and Android
  targets. Use when applying Kotlin null safety (?., ?:, let), data classes,
  sealed interfaces with when expressions, Kotlin Coroutines and Flows for async
  concurrency, or writing tests with Kotest and MockK.
compatibility: >
  Agent Skills-compatible coding agents operating on Kotlin 1.9+ / 2.0+ codebases.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "kotlin, coroutines, null-safety, data-classes, sealed-classes, jvm, flow"
  topics: "programming-languages, software-development"
---

# Idiomatic Kotlin Development

Kotlin combines object-oriented and functional paradigms on the JVM with compile-time null safety, extension functions, concise data modeling, and lightweight asynchronous concurrency via **Coroutines**.

## Core Rules

1. **Leverage the null-safety type system**: Never use the non-null assertion operator (`!!`) unless in verified test fixtures. Handle nulls with safe calls (`?.`), the Elvis operator (`?:`), or `let`.
2. **Use Data Classes for value models**: Favor immutable properties (`val`) over mutable variables (`var`).
3. **Model states with Sealed Interfaces**: Combine sealed hierarchies with exhaustive `when` expressions for type-safe state machines.
4. **Practice Structured Concurrency**: Never launch dangling coroutines with `GlobalScope`. Always launch within a defined `CoroutineScope` bound to a lifecycle.
5. **Prefer extension functions over utility classes**: Enhance existing types idiomatically without inheritance (`fun String.toSlug(): String`).
6. **Use Gradle Kotlin DSL (`build.gradle.kts`)**: Maintain type-safe build scripts with version catalogs (`libs.versions.toml`).

---

## 1. Null Safety and Scoping Functions

```kotlin
data class User(val id: String, val email: String?, val profile: Profile?)
data class Profile(val displayName: String?)

// Elvis operator for defaults and early exits
fun getGreeting(user: User): String {
    val name = user.profile?.displayName ?: "Guest"
    return "Hello, $name!"
}

// Scoping: use 'let' for executing logic only when non-null
fun sendNotification(user: User, message: String): Boolean {
    val recipientEmail = user.email ?: return false // Guard clause early exit

    return emailClient.send(to = recipientEmail, text = message)
}
```

---

## 2. Sealed Hierarchies and State Machines

```kotlin
sealed interface NetworkResult<out T> {
    data class Success<T>(val data: T) : NetworkResult<T>
    data class Error(val exception: Throwable, val code: Int) : NetworkResult<Nothing>
    data object Loading : NetworkResult<Nothing>
}

// Exhaustive when expression: compiler ensures every branch is handled
fun <T> handleResult(result: NetworkResult<T>): String = when (result) {
    is NetworkResult.Success -> "Loaded data: ${result.data}"
    is NetworkResult.Error   -> "Error ${result.code}: ${result.exception.message}"
    NetworkResult.Loading    -> "Loading in progress..."
}
```

---

## 3. Asynchronous Concurrency: Coroutines & Flow

```kotlin
import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*

class UserRepository(
    private val api: UserApi,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    // Suspend function runs asynchronously without blocking threads
    suspend fun fetchUserProfile(userId: String): UserProfile = withContext(dispatcher) {
        api.getUser(userId)
    }

    // Reactive cold stream using Flow
    fun observeUserStatus(userId: String): Flow<UserStatus> = flow {
        while (currentCoroutineContext().isActive) {
            val status = api.checkStatus(userId)
            emit(status)
            delay(5000) // Non-blocking delay
        }
    }.flowOn(dispatcher)
}
```

---

## 4. Testing with MockK and Kotest

```kotlin
import io.kotest.core.spec.style.DescribeSpec
import io.kotest.matchers.shouldBe
import io.mockk.*

class UserServiceTest : DescribeSpec({
    val mockRepo = mockk<UserRepository>()
    val service = UserService(mockRepo)

    describe("User profile lookup") {
        it("returns formatted profile on success") {
            coEvery { mockRepo.fetchUserProfile("user-123") } returns UserProfile("Alice", "alice@example.com")

            val result = service.getFormattedName("user-123")
            result shouldBe "Alice (alice@example.com)"

            coVerify(exactly = 1) { mockRepo.fetchUserProfile("user-123") }
        }
    }
})
```

---

## 5. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `val name = user!!.name` | Throws `NullPointerException` if null | Use safe call `user?.name` or elvis `?:` |
| Launching with `GlobalScope.launch` | Unmanaged coroutine leaks memory and runs indefinitely | Use structured scope (`viewModelScope`, `lifecycleScope`, or `coroutineScope`) |
| Mutable properties in data class (`var`) | Breaks hash code stability in sets and map keys | Use immutable `val` and create copies via `.copy()` |
| Creating Java-style `StringUtil` classes | Unidiomatic in Kotlin | Use top-level extension functions |
| Blocking threads inside coroutines (`Thread.sleep`) | Starves the thread pool of other coroutines | Use non-blocking `delay()` |

---

## 6. Verification Checklist

- [ ] Zero usage of `!!` non-null assertions in production source code.
- [ ] Properties in data classes declared with `val` for immutability.
- [ ] Sealed interfaces evaluated with exhaustive `when` (no unnecessary `else`).
- [ ] Coroutine dispatchers injected for testability (`Dispatchers.IO`).
- [ ] Gradle build passes: `./gradlew check` (ktlint / detekt / test).
