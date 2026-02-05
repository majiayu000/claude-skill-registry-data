---
name: kotlin-coding-standards
description: Master Kotlin coding standards with null safety, coroutines, and idiomatic patterns. Use when developing JVM/Android applications requiring type-safe async programming.
---

# Kotlin Coding Standards

## Level 1: Quick Reference

### Null Safety Cheat Sheet

```kotlin
// Safe Call (?.) - Returns null if receiver is null
val length = user?.name?.length

// Elvis Operator (?:) - Provides default value
val name = user?.name ?: "Unknown"

// Not-Null Assertion (!!) - Throws NPE if null (avoid!)
val length = user!!.name!!.length

// Safe Cast (as?) - Returns null on cast failure
val employee = person as? Employee
```

### Scope Functions

| Function | Context | Returns | Use Case |
|----------|---------|---------|----------|
| `let` | `it` | Lambda result | Null checks, transforms |
| `apply` | `this` | Receiver | Object configuration |
| `also` | `it` | Receiver | Side effects, logging |
| `run` | `this` | Lambda result | Object config + compute |
| `with` | `this` | Lambda result | Grouping calls |

```kotlin
// let - transform or null check
user?.let { println("Name: ${it.name}") }

// apply - configure object
val user = User().apply {
    name = "Alice"
    email = "alice@example.com"
}
```

### Core Patterns

```kotlin
// Data Classes - auto equals, hashCode, toString, copy
data class User(val id: String, val name: String, val email: String)

// Sealed Classes - restricted hierarchies
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

// Extension Functions - add to existing classes
fun String.isValidEmail(): Boolean =
    android.util.Patterns.EMAIL_ADDRESS.matcher(this).matches()
```

### Essential Checklist

- [ ] Use nullable types (?) instead of !! operator
- [ ] Prefer immutable (val) over mutable (var)
- [ ] Use data classes for DTOs
- [ ] Sealed classes for state management
- [ ] Configure detekt + ktlint
- [ ] Avoid platform types from Java interop

---

## Level 2: Implementation Guide

### 1. Null Safety Patterns

**Smart Casts** - Compiler tracks null checks:

```kotlin
fun processUser(user: User?) {
    if (user != null) {
        // Smart cast to User
        println(user.name)
    }
}

// Early return pattern
fun getUserName(user: User?): String {
    user ?: return "Unknown"
    return user.name  // Smart cast after check
}
```

**Initialization Patterns**:

```kotlin
// lateinit - for non-nullable late init (Android views, DI)
private lateinit var binding: ActivityMainBinding

// Check if initialized
if (::binding.isInitialized) { /* use binding */ }

// lazy - thread-safe initialization on first access
private val database: AppDatabase by lazy {
    Room.databaseBuilder(context, AppDatabase::class.java, "db").build()
}
```

### 2. Coroutines Essentials

**Suspend Functions**:

```kotlin
suspend fun fetchUser(id: String): User {
    return withContext(Dispatchers.IO) {
        apiService.getUser(id)
    }
}
```

**Coroutine Builders**:

```kotlin
// launch - fire and forget
CoroutineScope(Dispatchers.IO).launch {
    val users = apiService.getUsers()
    database.insertAll(users)
}

// async - return deferred result
suspend fun getUserWithDetails(id: String): UserDetails = coroutineScope {
    val user = async { apiService.getUser(id) }
    val posts = async { apiService.getUserPosts(id) }
    UserDetails(user.await(), posts.await())
}
```

**Flow Basics**:

```kotlin
// Cold flow - emits on collection
fun getUsers(): Flow<List<User>> = database.getUsersFlow()

// Transform flows
fun getActiveUsers(): Flow<List<User>> = database.getUsersFlow()
    .map { users -> users.filter { it.isActive } }
    .distinctUntilChanged()

// StateFlow - hot flow with current value
private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
val uiState: StateFlow<UiState> = _uiState.asStateFlow()
```

### 3. Collections & Functional Programming

```kotlin
// Transformation
val names = users.map { it.name }
val pairs = users.flatMap { user -> user.emails.map { user to it } }

// Filtering
val active = users.filter { it.isActive }
val (admins, regular) = users.partition { it.isAdmin }

// Aggregation
val count = users.count { it.isActive }
val total = orders.sumOf { it.amount }

// Grouping
val byRole = users.groupBy { it.role }

// Sequences - lazy evaluation for large collections
val result = users.asSequence()
    .filter { it.isActive }
    .map { it.name.uppercase() }
    .take(10)
    .toList()
```

### 4. Delegation Patterns

```kotlin
// Property delegation - observable
var name: String by Delegates.observable("Unknown") { _, old, new ->
    println("Changed from $old to $new")
}

// Custom delegate
class StringPreference(
    private val prefs: SharedPreferences,
    private val key: String,
    private val default: String
) : ReadWriteProperty<Any?, String> {
    override fun getValue(thisRef: Any?, property: KProperty<*>): String =
        prefs.getString(key, default) ?: default

    override fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
        prefs.edit().putString(key, value).apply()
    }
}

// Class delegation - composition over inheritance
class UserService(logger: Logger) : Logger by logger {
    fun createUser(name: String) {
        log("Creating user: $name")
    }
}
```

### 5. Java Interoperability

```kotlin
// Platform types - make nullability explicit
val safeName: String = javaObject.getName() ?: "Unknown"

// JvmStatic - static methods for Java
companion object {
    @JvmStatic
    fun isBlank(value: String?): Boolean = value.isNullOrBlank()
}

// JvmOverloads - default parameters for Java
class User @JvmOverloads constructor(
    val name: String,
    val email: String = "",
    val age: Int = 0
)

// Checked exceptions
@Throws(IOException::class)
fun readFile(path: String): String = File(path).readText()
```

### 6. Testing Quick Start

```kotlin
@Test
fun `getUser returns user from API`() = runTest {
    // Given
    val userId = "123"
    val expectedUser = User(userId, "Alice")
    coEvery { mockApi.getUser(userId) } returns expectedUser

    // When
    val result = repository.getUser(userId)

    // Then
    assertEquals(expectedUser, result)
    coVerify(exactly = 1) { mockApi.getUser(userId) }
}
```

---

## Level 3: Deep Dive Resources

### Documentation

- [Kotlin Language Reference](https://kotlinlang.org/docs/reference/)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)
- [Kotlin Style Guide](https://kotlinlang.org/docs/coding-conventions.html)

### Tools

- [Detekt](https://detekt.dev/) - Static code analysis
- [ktlint](https://ktlint.github.io/) - Code formatter
- [MockK](https://mockk.io/) - Mocking library
- [Turbine](https://github.com/cashapp/turbine) - Flow testing

### Extended Reference

See [REFERENCE.md](./REFERENCE.md) for:

- Complete coroutine patterns (StateFlow, SharedFlow, structured concurrency)
- Advanced delegation patterns
- Comprehensive testing examples (JUnit 5, MockK, Flow testing)
- Static analysis configuration
- Custom lint rules
- Spring Boot integration patterns

---

*Last updated: 2025-01-01*
