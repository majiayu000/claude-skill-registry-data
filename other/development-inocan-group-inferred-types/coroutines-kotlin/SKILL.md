---
name: coroutines-kotlin
description: Master Kotlin coroutines with suspend functions, flows, channels, and structured concurrency for building async applications.
---

# Kotlin Coroutines

Master asynchronous programming in Kotlin with coroutines, flows, and structured concurrency.

## Core Concepts

### Basic Coroutine
```kotlin
fun main() = runBlocking {
    launch {
        delay(1000L)
        println("World!")
    }
    println("Hello")
}
```

### Suspend Functions
```kotlin
suspend fun fetchUser(id: String): User {
    delay(1000) // Simulating network call
    return User(id, "John Doe")
}

fun main() = runBlocking {
    val user = fetchUser("123")
    println(user)
}
```

### Async/Await
```kotlin
suspend fun loadData(): Data = coroutineScope {
    val user = async { fetchUser() }
    val posts = async { fetchPosts() }

    Data(user.await(), posts.await())
}
```

### Flow
```kotlin
fun simpleFlow(): Flow<Int> = flow {
    for (i in 1..3) {
        delay(100)
        emit(i)
    }
}

fun main() = runBlocking {
    simpleFlow().collect { value ->
        println(value)
    }
}
```

### Channels
```kotlin
fun main() = runBlocking {
    val channel = Channel<Int>()

    launch {
        for (x in 1..5) channel.send(x * x)
        channel.close()
    }

    for (y in channel) println(y)
}
```

## Best Practices

1. Use structured concurrency
2. Handle exceptions properly
3. Use flows for streams
4. Leverage coroutine scope
5. Use dispatchers appropriately
6. Avoid GlobalScope
7. Test coroutines properly

## Resources
- https://kotlinlang.org/docs/coroutines-overview.html
