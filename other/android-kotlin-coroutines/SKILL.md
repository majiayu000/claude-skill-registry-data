---
name: android-kotlin-coroutines
description: Android development with Kotlin Coroutines and Flow. Use when user mentions "coroutines", "suspend", "Flow", "StateFlow", "SharedFlow", "viewModelScope", "lifecycleScope", or needs to implement async programming, handle structured concurrency, integrate coroutines with Retrofit/Room/WorkManager, or write coroutine tests. Triggers on Android concurrency, async, or Flow tasks.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(./gradlew:*), Bash(adb:*), WebSearch, WebFetch
---

# Android Kotlin Coroutines

Expert guidance for Android development using Kotlin Coroutines and Flow for asynchronous programming with structured
concurrency.

## When to Use This Skill

Invoke this skill when:

- Implementing asynchronous operations in Android
- Managing concurrent operations with structured concurrency
- Using Flow for reactive data streams (StateFlow, SharedFlow, callbackFlow)
- Integrating coroutines with Retrofit, Room, or WorkManager
- Handling cancellation and error propagation
- Writing coroutine-based unit tests
- User explicitly mentions "coroutines", "async", "Flow", "suspend", or related patterns

## Core Principles

1. **Structured Concurrency** — Coroutines bound to lifecycle prevent leaks
2. **Suspend over Callbacks** — Transform callback APIs to suspend functions
3. **Main-Safety** — Suspend functions safe to call from main thread
4. **Flow for Streams** — Use Flow for multiple values over time

## Quick Reference

### Essential Dependencies

```kotlin
// build.gradle.kts (app)
dependencies {
    // Coroutines core
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.8.0")

    // Lifecycle-aware scopes
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.7.0")
    implementation("androidx.lifecycle:lifecycle-viewmodel-ktx:2.7.0")

    // Flow integration with Compose
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.7.0")

    // Testing
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.8.0")
    testImplementation("app.cash.turbine:turbine:1.0.0")
}
```

## Coroutine Scopes in Android

### ViewModel Scope

```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val repository: UserRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(UserUiState())
    val uiState: StateFlow<UserUiState> = _uiState.asStateFlow()

    init {
        loadUser()
    }

    private fun loadUser() {
        // Automatically cancelled when ViewModel is cleared
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }

            repository.getUser()
                .onSuccess { user ->
                    _uiState.update { it.copy(user = user, isLoading = false) }
                }
                .onFailure { error ->
                    _uiState.update { it.copy(error = error.message, isLoading = false) }
                }
        }
    }

    fun refresh() {
        viewModelScope.launch {
            repository.sync()
        }
    }
}
```

### Lifecycle Scope

```kotlin
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Cancelled when Activity is destroyed
        lifecycleScope.launch {
            viewModel.events.collect { event ->
                handleEvent(event)
            }
        }

        // Only runs when at least STARTED
        lifecycleScope.launch {
            repeatOnLifecycle(Lifecycle.State.STARTED) {
                viewModel.uiState.collect { state ->
                    updateUI(state)
                }
            }
        }
    }
}

// In Compose - preferred approach
@Composable
fun UserScreen(viewModel: UserViewModel = hiltViewModel()) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    UserContent(uiState = uiState)
}
```

### Custom Scopes with SupervisorJob

```kotlin
class SearchManager(
    private val searchApi: SearchApi,
    private val dispatcher: CoroutineDispatcher = Dispatchers.IO
) {
    // SupervisorJob: child failure doesn't cancel siblings
    private val scope = CoroutineScope(SupervisorJob() + dispatcher)

    fun search(query: String): Flow<SearchResult> = flow {
        val results = searchApi.search(query)
        emit(results)
    }.flowOn(dispatcher)

    fun cancel() {
        scope.cancel()
    }
}
```

## Suspend Functions

### Basic Patterns

```kotlin
// Main-safe suspend function (moves work off main thread internally)
suspend fun fetchUser(id: String): User = withContext(Dispatchers.IO) {
    api.getUser(id)
}

// Parallel decomposition
suspend fun fetchUserWithPosts(id: String): UserWithPosts = coroutineScope {
    val userDeferred = async { api.getUser(id) }
    val postsDeferred = async { api.getPosts(userId = id) }

    UserWithPosts(
        user = userDeferred.await(),
        posts = postsDeferred.await()
    )
}

// Timeout
suspend fun fetchWithTimeout(id: String): User? {
    return withTimeoutOrNull(5000L) {
        api.getUser(id)
    }
}
```

### Converting Callbacks to Suspend

```kotlin
// suspendCancellableCoroutine for one-shot callbacks
suspend fun Location.awaitLastLocation(): Location = suspendCancellableCoroutine { cont ->
    val client = LocationServices.getFusedLocationProviderClient(context)

    client.lastLocation
        .addOnSuccessListener { location ->
            cont.resume(location)
        }
        .addOnFailureListener { e ->
            cont.resumeWithException(e)
        }

    cont.invokeOnCancellation {
        // Cleanup if coroutine is cancelled
    }
}

// For Firebase/Firestore
suspend fun DocumentReference.awaitGet(): DocumentSnapshot = suspendCancellableCoroutine { cont ->
    get()
        .addOnSuccessListener { cont.resume(it) }
        .addOnFailureListener { cont.resumeWithException(it) }
}
```

## Flow Patterns

### StateFlow for UI State

```kotlin
@HiltViewModel
class ProductListViewModel @Inject constructor(
    private val repository: ProductRepository
) : ViewModel() {

    private val _searchQuery = MutableStateFlow("")

    // Derived state from search query
    val products: StateFlow<ProductsUiState> = _searchQuery
        .debounce(300)
        .flatMapLatest { query ->
            repository.searchProducts(query)
                .map { ProductsUiState.Success(it) }
                .catch { emit(ProductsUiState.Error(it.message)) }
        }
        .stateIn(
            scope = viewModelScope,
            started = SharingStarted.WhileSubscribed(5000),
            initialValue = ProductsUiState.Loading
        )

    fun updateSearch(query: String) {
        _searchQuery.value = query
    }
}

sealed interface ProductsUiState {
    data object Loading : ProductsUiState
    data class Success(val products: List<Product>) : ProductsUiState
    data class Error(val message: String?) : ProductsUiState
}
```

### SharedFlow for Events

```kotlin
@HiltViewModel
class CheckoutViewModel @Inject constructor(
    private val orderRepository: OrderRepository
) : ViewModel() {

    // Events that should not be replayed
    private val _events = MutableSharedFlow<CheckoutEvent>()
    val events: SharedFlow<CheckoutEvent> = _events.asSharedFlow()

    fun placeOrder(order: Order) {
        viewModelScope.launch {
            orderRepository.placeOrder(order)
                .onSuccess { orderId ->
                    _events.emit(CheckoutEvent.OrderSuccess(orderId))
                }
                .onFailure { e ->
                    _events.emit(CheckoutEvent.OrderFailed(e.message ?: "Unknown error"))
                }
        }
    }
}

sealed interface CheckoutEvent {
    data class OrderSuccess(val orderId: String) : CheckoutEvent
    data class OrderFailed(val message: String) : CheckoutEvent
}

// Collecting in Compose
@Composable
fun CheckoutScreen(
    viewModel: CheckoutViewModel = hiltViewModel(),
    onNavigateToConfirmation: (String) -> Unit
) {
    val snackbarHostState = remember { SnackbarHostState() }

    LaunchedEffect(Unit) {
        viewModel.events.collect { event ->
            when (event) {
                is CheckoutEvent.OrderSuccess -> onNavigateToConfirmation(event.orderId)
                is CheckoutEvent.OrderFailed -> snackbarHostState.showSnackbar(event.message)
            }
        }
    }

    // Screen content
}
```

### callbackFlow for Continuous Streams

```kotlin
// Location updates as Flow
fun LocationClient.locationUpdates(
    request: LocationRequest
): Flow<Location> = callbackFlow {
    val callback = object : LocationCallback() {
        override fun onLocationResult(result: LocationResult) {
            result.lastLocation?.let { trySend(it) }
        }
    }

    requestLocationUpdates(request, callback, Looper.getMainLooper())

    awaitClose {
        removeLocationUpdates(callback)
    }
}

// Firebase Realtime Database listener
fun DatabaseReference.valueEvents(): Flow<DataSnapshot> = callbackFlow {
    val listener = object : ValueEventListener {
        override fun onDataChange(snapshot: DataSnapshot) {
            trySend(snapshot)
        }
        override fun onCancelled(error: DatabaseError) {
            close(error.toException())
        }
    }

    addValueEventListener(listener)
    awaitClose { removeEventListener(listener) }
}
```

### Flow Operators

```kotlin
// Combining flows
val userWithSettings: Flow<UserWithSettings> = combine(
    userFlow,
    settingsFlow
) { user, settings ->
    UserWithSettings(user, settings)
}

// Retry with exponential backoff
fun <T> Flow<T>.retryWithBackoff(
    maxRetries: Int = 3,
    initialDelay: Long = 1000
): Flow<T> = retryWhen { cause, attempt ->
    if (attempt < maxRetries && cause is IOException) {
        delay(initialDelay * (2.0.pow(attempt.toInt())).toLong())
        true
    } else {
        false
    }
}

// Throttle/sample
val throttledClicks = clickFlow
    .sample(300) // Emit at most once per 300ms
```

## Error Handling

### Try-Catch in Coroutines

```kotlin
viewModelScope.launch {
    try {
        val user = repository.getUser(id)
        _uiState.update { it.copy(user = user) }
    } catch (e: CancellationException) {
        throw e // Always rethrow cancellation
    } catch (e: Exception) {
        _uiState.update { it.copy(error = e.message) }
    }
}
```

### Result Pattern

```kotlin
class UserRepository @Inject constructor(
    private val api: UserApi,
    @IoDispatcher private val dispatcher: CoroutineDispatcher
) {
    suspend fun getUser(id: String): Result<User> = withContext(dispatcher) {
        runCatching {
            api.getUser(id)
        }
    }
}

// Usage
viewModelScope.launch {
    repository.getUser(id)
        .onSuccess { user -> _uiState.update { it.copy(user = user) } }
        .onFailure { e -> _uiState.update { it.copy(error = e.message) } }
}
```

### CoroutineExceptionHandler

```kotlin
// Global handler for uncaught exceptions
val handler = CoroutineExceptionHandler { _, exception ->
    Timber.e(exception, "Uncaught exception")
    analytics.trackError(exception)
}

val scope = CoroutineScope(SupervisorJob() + Dispatchers.Main + handler)
```

## Dispatcher Injection

```kotlin
// Qualifiers
@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class IoDispatcher

@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class MainDispatcher

@Qualifier
@Retention(AnnotationRetention.BINARY)
annotation class DefaultDispatcher

// Hilt module
@Module
@InstallIn(SingletonComponent::class)
object DispatcherModule {
    @Provides
    @IoDispatcher
    fun provideIoDispatcher(): CoroutineDispatcher = Dispatchers.IO

    @Provides
    @MainDispatcher
    fun provideMainDispatcher(): CoroutineDispatcher = Dispatchers.Main

    @Provides
    @DefaultDispatcher
    fun provideDefaultDispatcher(): CoroutineDispatcher = Dispatchers.Default
}

// Repository using injected dispatcher
class DataRepository @Inject constructor(
    private val api: DataApi,
    @IoDispatcher private val ioDispatcher: CoroutineDispatcher
) {
    suspend fun fetchData(): List<Data> = withContext(ioDispatcher) {
        api.getData()
    }
}
```

## Common Anti-Patterns

### ❌ Avoid

```kotlin
// DON'T: GlobalScope - no structured concurrency
GlobalScope.launch {
    repository.sync()
}

// DON'T: Blocking the main thread
runBlocking {
    api.fetchData()  // Blocks main thread!
}

// DON'T: Swallowing CancellationException
try {
    suspendFunction()
} catch (e: Exception) {  // Catches CancellationException!
    log(e)
}

// DON'T: Using flow { } for single values
fun getUser(): Flow<User> = flow {
    emit(api.getUser())  // Use suspend function instead
}

// DON'T: Collecting in ViewModel init without proper scope
init {
    repository.dataFlow.collect { data ->  // Suspends forever in init
        _uiState.value = data
    }
}
```

### ✅ Correct

```kotlin
// DO: Use viewModelScope
viewModelScope.launch {
    repository.sync()
}

// DO: Use suspendCancellableCoroutine properly
suspend fun fetch() = withContext(Dispatchers.IO) {
    api.fetchData()
}

// DO: Rethrow CancellationException
try {
    suspendFunction()
} catch (e: CancellationException) {
    throw e
} catch (e: Exception) {
    log(e)
}

// DO: Use suspend for single values
suspend fun getUser(): User = api.getUser()

// DO: Launch collection properly
init {
    viewModelScope.launch {
        repository.dataFlow.collect { data ->
            _uiState.value = data
        }
    }
}
```

## Resources

For detailed patterns and integration guides, see:

- `references/flow-patterns.md` — Advanced Flow operations, hot/cold flows, sharing strategies
- `references/testing-coroutines.md` — Unit testing with Turbine, TestDispatcher, runTest
- `references/integrations.md` — Retrofit, Room, WorkManager, Firebase integration patterns

### When to Consult References

- Complex Flow transformations → `flow-patterns.md`
- Testing suspend functions and Flows → `testing-coroutines.md`
- Retrofit/Room integration setup → `integrations.md`
- WorkManager with coroutines → `integrations.md`
