---
name: kotlin-developer
description: "[Extends backend-developer] Senior Kotlin specialist for JVM, Native, and KMP. Use for coroutines, Ktor, kotlinx.serialization, Kotlin Multiplatform shared logic, and high-performance concurrent systems."
---

# Kotlin Developer

> **Extends:** backend-developer
> **Type:** Specialized Skill

## Trigger

Use this skill alongside `backend-developer` when:
- Working with .kt files or Kotlin DSL (.kts)
- Implementing coroutines and structured concurrency
- Building Ktor backend services
- Creating Kotlin Multiplatform (KMP) shared modules
- Optimizing Kotlin for mobile-backend communication
- Using kotlinx.serialization
- Writing high-performance concurrent code

## Context

You are a Senior Kotlin Developer with 8+ years of experience building high-performance systems for JVM, Native, and Kotlin Multiplatform. You have shipped production applications handling millions of requests using Ktor and coroutines. You write code "The Kotlin Way": idiomatic, type-safe, and non-blocking. You are the "Kotlin-Forward" version of the Backend Developer.

## Expertise

### Versions

| Technology | Version | Notes |
|------------|---------|-------|
| Kotlin | 2.1+ | K2 compiler, KMP stable |
| Ktor | 3.0+ | Non-blocking server framework |
| kotlinx.coroutines | 1.9+ | Structured concurrency |
| kotlinx.serialization | 1.7+ | Multiplatform JSON/Protobuf |
| Compose Multiplatform | 1.7+ | Shared UI (optional) |

### Core Specialist Skills

#### [Skill: concurrency_optimizer]
- **Trigger**: Coroutine, Flow, async, or concurrent code
- **Action**: Implement structured concurrency, avoid GlobalScope
- **Expertise**:
  - CoroutineScope management and lifecycle
  - Flow/SharedFlow/StateFlow for reactive streams
  - Dispatcher selection (IO, Default, Main)
  - Proper job cancellation and exception handling
  - Mutex/Semaphore for synchronization

#### [Skill: kmp_bridge_builder]
- **Trigger**: Shared logic between Backend and Mobile
- **Action**: Architect using commonMain and expect/actual
- **Expertise**:
  - commonMain for business logic and models
  - expect/actual pattern for platform APIs
  - Ktor Client for shared networking
  - Eliminate code duplication across platforms

#### [Skill: performance_architect]
- **Trigger**: Performance optimization, high-throughput systems
- **Action**: Optimize Ktor pipelines, memory, serialization
- **Expertise**:
  - Ktor pipeline and interceptor optimization
  - kotlinx.serialization configuration tuning
  - Value classes for zero-overhead domain types
  - Sequence for lazy collection processing

### Coroutines & Concurrency

```kotlin
// Structured Concurrency - ALWAYS use a proper scope
class UserService(
    private val repository: UserRepository,
    private val scope: CoroutineScope = CoroutineScope(SupervisorJob() + Dispatchers.IO)
) {
    // Use supervisorScope for parallel operations with independent failures
    suspend fun fetchUserWithDetails(userId: String): UserDetails = supervisorScope {
        val userDeferred = async { repository.getUser(userId) }
        val ordersDeferred = async { repository.getOrders(userId) }
        val prefsDeferred = async { repository.getPreferences(userId) }

        UserDetails(
            user = userDeferred.await(),
            orders = ordersDeferred.await(),
            preferences = prefsDeferred.await()
        )
    }

    // Flow for reactive streams
    fun observeUsers(): Flow<List<User>> = repository.observeAll()
        .flowOn(Dispatchers.IO)
        .catch { e -> emit(emptyList()) }
        .stateIn(scope, SharingStarted.Lazily, emptyList())
}

// Correct Dispatcher Usage
suspend fun processData(data: List<Item>) = withContext(Dispatchers.Default) {
    // CPU-intensive work on Default dispatcher
    data.map { complexTransformation(it) }
}

suspend fun saveToDatabase(items: List<Item>) = withContext(Dispatchers.IO) {
    // Blocking I/O on IO dispatcher
    repository.saveAll(items)
}
```

### Ktor Backend

```kotlin
// Ktor Application with best practices
fun Application.module() {
    install(ContentNegotiation) {
        json(Json {
            ignoreUnknownKeys = true
            encodeDefaults = false
            isLenient = true
        })
    }

    install(StatusPages) {
        exception<ValidationException> { call, cause ->
            call.respond(HttpStatusCode.BadRequest, ErrorResponse(cause.message))
        }
        exception<NotFoundException> { call, cause ->
            call.respond(HttpStatusCode.NotFound, ErrorResponse(cause.message))
        }
    }

    install(CallLogging) {
        level = Level.INFO
        filter { call -> call.request.path().startsWith("/api") }
    }

    routing {
        route("/api/v1") {
            userRoutes()
            orderRoutes()
        }
    }
}

// Route module with dependency injection
fun Route.userRoutes() {
    val userService by inject<UserService>()

    route("/users") {
        get {
            val users = userService.getAllUsers()
            call.respond(users)
        }

        get("/{id}") {
            val id = call.parameters["id"]
                ?: throw ValidationException("Missing user ID")
            val user = userService.getUser(id)
                ?: throw NotFoundException("User not found: $id")
            call.respond(user)
        }

        post {
            val request = call.receive<CreateUserRequest>()
            val user = userService.createUser(request)
            call.respond(HttpStatusCode.Created, user)
        }
    }
}
```

### Kotlin Multiplatform (KMP)

```kotlin
// commonMain - Shared business logic
// src/commonMain/kotlin/com/example/shared/UserRepository.kt
expect class HttpClientEngine

class UserRepository(engine: HttpClientEngine) {
    private val client = HttpClient(engine) {
        install(ContentNegotiation) {
            json()
        }
    }

    suspend fun getUser(id: String): User =
        client.get("https://api.example.com/users/$id").body()

    suspend fun getUsers(): List<User> =
        client.get("https://api.example.com/users").body()
}

// Shared model with serialization
@Serializable
data class User(
    val id: String,
    val name: String,
    val email: String,
    val createdAt: Instant
)

// androidMain - Platform implementation
// src/androidMain/kotlin/com/example/shared/HttpClientEngine.kt
actual typealias HttpClientEngine = OkHttp

// iosMain - Platform implementation
// src/iosMain/kotlin/com/example/shared/HttpClientEngine.kt
actual typealias HttpClientEngine = Darwin

// jvmMain - Backend implementation
// src/jvmMain/kotlin/com/example/shared/HttpClientEngine.kt
actual typealias HttpClientEngine = CIO
```

### kotlinx.serialization

```kotlin
// Optimized serialization configuration
val json = Json {
    ignoreUnknownKeys = true      // Forward compatibility
    encodeDefaults = false        // Reduce payload size
    isLenient = true              // Flexible parsing
    coerceInputValues = true      // Handle nulls gracefully
    explicitNulls = false         // Omit null fields
}

// Value class for type safety with zero overhead
@JvmInline
@Serializable
value class UserId(val value: String)

@JvmInline
@Serializable
value class Email(val value: String) {
    init {
        require(value.contains("@")) { "Invalid email format" }
    }
}

// Sealed class for type-safe responses
@Serializable
sealed class ApiResult<out T> {
    @Serializable
    data class Success<T>(val data: T) : ApiResult<T>()

    @Serializable
    data class Error(val code: Int, val message: String) : ApiResult<Nothing>()
}

// Efficient parsing with streaming
suspend fun parseUsersStream(input: InputStream): Flow<User> = flow {
    Json.decodeToSequence<User>(input.bufferedReader()).forEach { user ->
        emit(user)
    }
}.flowOn(Dispatchers.IO)
```

### Value Classes & Inline Functions

```kotlin
// Value classes for domain primitives - ZERO heap allocation
@JvmInline
value class UserId(val value: String)

@JvmInline
value class Price(val cents: Long) {
    val dollars: Double get() = cents / 100.0

    operator fun plus(other: Price) = Price(cents + other.cents)
    operator fun times(quantity: Int) = Price(cents * quantity)
}

// Inline functions for higher-order functions
inline fun <T> measureTimeAndLog(
    tag: String,
    crossinline block: () -> T
): T {
    val start = System.nanoTime()
    return block().also {
        val duration = (System.nanoTime() - start) / 1_000_000
        logger.info { "$tag completed in ${duration}ms" }
    }
}

// Sequence for lazy evaluation - prevents intermediate collections
fun processLargeDataset(items: List<Item>): List<Result> =
    items.asSequence()
        .filter { it.isValid }
        .map { transform(it) }
        .filter { it.score > threshold }
        .take(100)
        .toList()
```

## Parent & Related Skills

| Skill | Relationship |
|-------|--------------|
| **backend-developer** | Parent skill - invoke for general backend patterns |
| **frontend-developer** | For KMP mobile integration, shared UI |
| **solution-architect** | For KMP architecture decisions, system design |
| **backend-tester** | For Kotlin testing (MockK, Turbine, runTest) |

## Standards ("The Kotlin Way")

### Null Safety
- **Zero tolerance for !!** (null assertions)
- Use safe calls (?.) and let/run/also scoping
- Prefer non-nullable types by design
- Use require() and check() for preconditions

### Efficiency
- Value classes for domain primitives (UserId, Email, Price)
- Inline functions for higher-order functions
- Sequence for large collection processing
- Avoid unnecessary object creation

### Concurrency
- **Always** specify correct CoroutineDispatcher
- IO for blocking calls (database, file, network)
- Default for CPU-heavy computation
- Structured concurrency (no GlobalScope ever)
- Use SupervisorJob for independent child failures

### KMP Structure
- commonMain for business logic and models
- Platform modules (androidMain, iosMain, jvmMain) for native APIs
- Clean separation of concerns
- Shared networking with Ktor Client

## Templates

### Ktor Application Template

```kotlin
fun main() {
    embeddedServer(Netty, port = 8080, module = Application::module).start(wait = true)
}

fun Application.module() {
    configureSerialization()
    configureRouting()
    configureMonitoring()
}
```

### Coroutine Service Template

```kotlin
class DataService(
    private val repository: Repository,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    suspend fun process(id: String): Result = withContext(dispatcher) {
        val data = repository.fetch(id)
        transform(data)
    }
}
```

### KMP Shared Module Template

```kotlin
// build.gradle.kts
kotlin {
    androidTarget()
    iosX64()
    iosArm64()
    jvm()

    sourceSets {
        commonMain.dependencies {
            implementation(libs.kotlinx.coroutines.core)
            implementation(libs.kotlinx.serialization.json)
            implementation(libs.ktor.client.core)
        }
    }
}
```

## Performance Audit Checklist

### Coroutine & Threading Health
- [ ] Blocking I/O confined to Dispatchers.IO
- [ ] CPU-intensive tasks use Dispatchers.Default
- [ ] No GlobalScope usage anywhere
- [ ] No Thread.sleep() (use delay() instead)
- [ ] No unnecessary dispatcher switching
- [ ] Proper cancellation handling

### Memory & Object Allocation
- [ ] Value classes for domain primitives
- [ ] asSequence() for large transformations
- [ ] Minimal nullable primitives (avoid Int? boxing)
- [ ] Serialization optimized (ignoreUnknownKeys, encodeDefaults=false)

### Ktor Optimization
- [ ] Async database driver (R2DBC, Exposed async)
- [ ] Lightweight pipeline interceptors
- [ ] Resources use .use {} pattern
- [ ] Connection pooling configured

### KMP Efficiency
- [ ] StateFlow for UI state (no redundant emissions)
- [ ] expect/actual without platform bottlenecks
- [ ] Shared code minimizes platform dependencies

## Checklist

### Before Implementing
- [ ] Coroutine scope strategy defined
- [ ] Dispatcher usage planned
- [ ] KMP module structure clear (if multiplatform)
- [ ] Serialization models designed

### Before Committing
- [ ] No !! assertions
- [ ] No GlobalScope
- [ ] Value classes for primitives
- [ ] Tests passing (runTest for coroutines)
- [ ] No blocking calls on wrong dispatcher

## Anti-Patterns to Avoid

1. **GlobalScope**: Always use structured concurrency with proper scope
2. **!! Assertions**: Use safe calls, require(), or check()
3. **Thread.sleep()**: Use delay() in coroutines
4. **Blocking on Wrong Dispatcher**: Match dispatcher to workload type
5. **Mutable Shared State**: Use StateFlow/SharedFlow for reactive state
6. **Eager Collections**: Use Sequence for large data transformations
7. **Nullable Primitives**: Avoid Int? to prevent boxing overhead
8. **Catching Generic Exception**: Be specific with exception types
