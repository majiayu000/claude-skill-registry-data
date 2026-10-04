---
name: android-expert
description: House rules and load-bearing patterns for production Android with Jetpack Compose + MVI. Covers the MviViewModel<State,Intent,Effect> contract pattern, DispatcherProvider, collectAsStateWithLifecycle, type-safe Navigation Compose (@Serializable routes) + Navigation3 forward path, Koin DI (not Hilt), strong skipping defaults, edge-to-edge mandate, Material 3 / Expressive + adaptive layouts, Room + DataStore, Turbine + MockK + Robolectric testing scaffold, Baseline Profiles, R8 full mode, composable parameter ordering, module layout, and anti-pattern catalog. **Does not** re-teach elementary Compose (recomposition, remember, LaunchedEffect basics), standard Kotlin/coroutine patterns, or basic Material 3 usage -- assume that baseline. Use when writing or reviewing any Android/Compose code.
---

# Android Expert

Opinion and house-rule reference for **Jetpack Compose + MVI** on modern Android (Kotlin 2.x / K2, Compose BOM, `targetSdk 36+`). **Assumes baseline Compose/Kotlin knowledge** -- this file only covers what's house-specific, load-bearing, or shifts year-to-year.

Non-negotiable defaults:
- **`MviViewModel<State, Intent, Effect>`** with a `*Contract` holder. UDF only; no two-way binding.
- State is a single immutable `data class`; intents and effects are `sealed interface`.
- Always **`collectAsStateWithLifecycle()`**, never `collectAsState()`.
- Type-safe Navigation Compose routes are **`@Serializable data object` / `data class`**. String routes are banned.
- Hoist `modifier: Modifier = Modifier` as the **last** parameter with a default.
- Koin for DI (`koin-compose-viewmodel`), not Hilt.
- One class per file. Full words in names (`connection`, not `conn`). camelCase acronyms (`updateMfa`, not `updateMFA`).

---

## 1. Year-to-year shifts -- get these right

- **Compose Compiler is a Gradle plugin** (`org.jetbrains.kotlin.plugin.compose`). Do NOT add `androidx.compose.compiler:compiler` or set `kotlinCompilerExtensionVersion`. Both are obsolete.
- **Strong skipping is on by default.** `@Stable` / `@Immutable` are almost never needed (see section 8).
- **KSP2 is the default**; KAPT is being phased out.
- **`collectAsState()` -> `collectAsStateWithLifecycle()`.** Plain version keeps collecting while backgrounded.
- **`PredictiveBackHandler` -> `NavigationBackHandler` / Navigation Event API.** Deprecated API splits into `onBackCancelled` / `onBackCompleted` with `NavigationEventState.transitionState`.
- **Edge-to-edge is mandatory** at `targetSdk 36`. `enableEdgeToEdge()` before `setContent { }`. The opt-out manifest flag is ignored.
- **Navigation 3 has shipped** alongside existing `navigation-compose`. Nav2 still maintained -- adopt Nav3 in greenfield only.
- **Material 3 Expressive** (wavy progress, FAB menus, split buttons) ships through `material3`; opt in via `MaterialExpressiveTheme { ... }`.
- **Room 3.0** is KMP-first, KSP-only, coroutines-required. The 2.x line is still production on pure Android.
- **`@Serializable` typed routes** are the only correct way to declare navigation destinations.

---

## 2. Module layout

```kotlin
rootProject.name = "app"
include(":app")
include(":core:common")        // MviViewModel, DispatcherProvider, Analytics, CrashReporter
include(":core:model")         // Domain types: data classes only, no Android deps
include(":core:database")      // Room DAOs + Repositories + Mappers
include(":core:network")       // HTTP client, DTOs
include(":core:preferences")   // DataStore
include(":ui:design")          // Theme, colors, reusable components
include(":feature:home")
include(":feature:detail")
```

Dependency graph: `:app -> :feature:* -> :core:* -> (external libs)`. `:feature:*` may also depend on `:ui:design`.

Rules:
- **Singular nouns** for modules and packages: `:feature:home`, not `:feature:homeFeature`.
- **No `core/util` or `core/helpers`**. `core/common` holds framework primitives. Everything else is domain-grouped.
- **`:core:model` has zero Android dependencies** -- data classes + enums only. Liftable to KMP without changes.
- **No `:data`/`:domain`/`:presentation` layered split.** Domain-driven modularisation: each `core/<domain>` owns entities, DAOs, repositories, and mappers end-to-end.

---

## 3. MVI -- the contract pattern

### 3.1 The `MviViewModel` base class

```kotlin
package com.example.app.core.common

abstract class MviViewModel<State, Intent, Effect>(
    initialState: State,
) : ViewModel() {
    private val _state = MutableStateFlow(initialState)
    val state: StateFlow<State> = _state.asStateFlow()

    private val _effects = Channel<Effect>(Channel.BUFFERED)   // NOT SharedFlow -- buffers while UI rebuilds
    val effects: Flow<Effect> = _effects.receiveAsFlow()

    protected val currentState: State get() = _state.value     // don't call _state.value inside update{}

    fun dispatch(intent: Intent) {
        viewModelScope.launch { handleIntent(intent) }
    }

    protected abstract suspend fun handleIntent(intent: Intent)

    protected fun setState(reduce: State.() -> State) {
        _state.update(reduce)                                  // lock-free, retries on conflict
    }

    protected suspend fun sendEffect(effect: Effect) {
        _effects.send(effect)
    }
}
```

### 3.2 The `*Contract` holder

```kotlin
object ItemListContract {
    data class State(
        val items: List<ItemUiModel> = emptyList(),         // all fields have defaults
        val favorites: List<ItemUiModel> = emptyList(),
        val isLoading: Boolean = true,
        val isRefreshing: Boolean = false,
        val error: UiError? = null,                         // persistent errors as state field
        val searchQuery: String = "",
        val deleteConfirmation: Long? = null,
    )

    sealed interface Intent {                               // sealed interface, not sealed class
        data class Search(val query: String) : Intent
        data class SelectItem(val itemId: Long) : Intent
        data class ConfirmDelete(val itemId: Long) : Intent
        data object DismissDelete : Intent                  // data object, never bare object
        data class ToggleFavorite(val itemId: Long, val isFavorite: Boolean) : Intent
        data object AddItem : Intent
        data object Refresh : Intent
    }

    sealed interface Effect {
        data class NavigateToDetail(val itemId: Long) : Effect
        data class NavigateToAddItem(val prefillLabel: String? = null) : Effect
        data class ShowError(                               // transient messages as effects
            override val message: String? = null,
            @param:StringRes override val messageRes: Int? = null,
            override val messageArgs: List<Any> = emptyList(),
        ) : Effect, LocalizedMessage
    }
}
```

Localised messages use a `LocalizedMessage` interface (`messageRes: Int?` + `messageArgs: List<Any>`) so effects carry a `@StringRes` that resolves at the UI layer. Never stringify at the VM layer.

### 3.3 The ViewModel

```kotlin
class ItemListViewModel(
    private val repository: ItemRepository,
    private val dispatchers: DispatcherProvider,             // injected, not Dispatchers.IO directly
    private val analytics: Analytics,
    private val crashReporter: CrashReporter,
) : MviViewModel<ItemListContract.State, ItemListContract.Intent, ItemListContract.Effect>(
    initialState = ItemListContract.State(),
) {
    init { observeItems() }                                 // long-lived observers start at construction

    private fun observeItems() {
        combine(
            searchQuery.debounce(300).distinctUntilChanged()
                .flatMapLatest { q ->
                    if (q.isBlank()) repository.observeAll() else repository.search(q)
                },
            repository.observeFavorites(),
        ) { items, favorites ->
            items.map { it.toUiModel() } to favorites.map { it.toUiModel() }
        }.onEach { (models, favs) ->
            setState { copy(items = models, favorites = favs, isLoading = false, error = null) }
        }.launchIn(viewModelScope)
    }

    override suspend fun handleIntent(intent: ItemListContract.Intent) {
        when (intent) {                                     // exhaustive when on sealed interface
            is Intent.Search        -> searchQuery.value = intent.query
            is Intent.SelectItem    -> sendEffect(Effect.NavigateToDetail(intent.itemId))
            is Intent.ConfirmDelete -> handleConfirmDelete(intent.itemId)
            // ...
        }
    }

    private suspend fun handleConfirmDelete(itemId: Long) {
        setState { copy(deleteConfirmation = null) }
        try {
            withContext(dispatchers.io) { repository.delete(itemId) }
            sendEffect(Effect.ShowInfo(messageRes = R.string.items_message_deleted))
        } catch (exception: Exception) {
            crashReporter.record(exception)                 // dashboard sees it
            setState { copy(error = UiError(messageRes = R.string.items_message_delete_failed)) }
        }
    }
}
```

### 3.4 The screen composable

```kotlin
@Composable
fun ItemListScreen(
    onNavigateToDetail: (Long) -> Unit,                     // nav callbacks hoisted, no NavController
    onNavigateToAddItem: (String?) -> Unit,
    viewModel: ItemListViewModel = koinViewModel(),
) {
    val state by viewModel.state.collectAsStateWithLifecycle()

    LaunchedEffect(Unit) {                                  // canonical effect collector
        viewModel.effects.collect { effect ->
            when (effect) {
                is Effect.NavigateToDetail -> onNavigateToDetail(effect.itemId)
                is Effect.ShowError -> bannerState.show(effect.resolve(context))
            }
        }
    }

    ItemListContent(state = state, onIntent = viewModel::dispatch, modifier = Modifier.fillMaxSize())
}
```

Split stateful `Screen` from stateless `Content`. `Content(state, onIntent, modifier)` is what previews and tests drive.

### 3.5 Composable parameter ordering (non-negotiable)

```kotlin
@Composable
fun ChoiceButton(
    text: String,                       // 1. required data
    onClick: () -> Unit,                // 2. required callbacks
    isSelected: Boolean = false,        // 3. optional data with defaults
    modifier: Modifier = Modifier,      // 4. modifier ALWAYS last
) { ... }
// content: @Composable () -> Unit comes AFTER modifier as trailing lambda
```

---

## 4. DispatcherProvider

```kotlin
interface DispatcherProvider {
    val main: CoroutineDispatcher       // always Dispatchers.Main.immediate, not .Main
    val io: CoroutineDispatcher
    val default: CoroutineDispatcher
}

class DefaultDispatcherProvider : DispatcherProvider {
    override val main = Dispatchers.Main.immediate
    override val io = Dispatchers.IO
    override val default = Dispatchers.Default
}
```

In tests, supply an object returning `StandardTestDispatcher` / `UnconfinedTestDispatcher` for all three.

---

## 5. Flow patterns -- the idioms you need

```kotlin
// Merge sources into UI state:
combine(searchQuery.debounce(300).distinctUntilChanged(), reachability) { q, reach ->
    buildUiModel(q, reach)
}.onEach { setState { copy(models = it) } }.launchIn(viewModelScope)

// Switch flow on new input (cancels prior):
queryFlow.flatMapLatest { q -> repository.search(q) }

// Read-only derived StateFlow (no VM mutation):
val uiState: StateFlow<UiState> = repository.observe()
    .map { it.toUiState() }
    .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), UiState.Loading)

// Debounce without dropping first emission:
val debouncedKey = merge(keyFlow.take(1), keyFlow.drop(1).debounce(400))
```

`WhileSubscribed(5_000)` is the canonical started strategy -- 5 seconds covers config changes without keeping upstream hot forever. `flowOn` applies **upstream only**.

---

## 6. Navigation

### 6.1 Today: Navigation Compose + type-safe routes

Routes are **always** `@Serializable data object` / `data class`, never strings.

```kotlin
@Serializable data object ItemListRoute
@Serializable data class ItemDetailRoute(val itemId: Long)

fun NavGraphBuilder.itemsNavGraph(navController: NavController) {
    composable<ItemListRoute> {
        ItemListScreen(
            onNavigateToDetail = { navController.navigate(ItemDetailRoute(it)) },
        )
    }
    composable<ItemDetailRoute> { entry ->
        val route = entry.toRoute<ItemDetailRoute>()
        ItemDetailScreen(itemId = route.itemId, onNavigateBack = { navController.popBackStack() })
    }
}
```

- One `XxxNavigation.kt` per feature with routes + `NavGraphBuilder.xxxNavGraph(...)`. `:app` wires them in `AppNavHost`.
- Apply `org.jetbrains.kotlin.plugin.serialization` at every module declaring routes.

### 6.2 Navigation3 (stable, 1.0)

Back stack is a plain `SnapshotStateList<NavKey>` -- `add`, `removeLastOrNull`, `replaceAll` directly.

```kotlin
@Serializable sealed interface HomeRoute : NavKey {
    @Serializable data object Feed : HomeRoute
    @Serializable data class Detail(val id: String) : HomeRoute
}

@Composable
fun AppNavHost() {
    val backStack = rememberNavBackStack(HomeRoute.Feed)
    NavDisplay(
        backStack = backStack,
        onBack = { backStack.removeLastOrNull() },
        entryProvider = entryProvider {
            entry<HomeRoute.Feed> { FeedScreen(onItemClick = { backStack.add(HomeRoute.Detail(it)) }) }
            entry<HomeRoute.Detail> { key -> DetailScreen(id = key.id) }
        },
    )
}
```

Dependencies: `navigation3-runtime`, `navigation3-ui`, `lifecycle-viewmodel-navigation3` (NavEntry-scoped VMs).

**Decision rule**: greenfield -> Nav3 (verify its `minSdk` floor). Existing Nav2 -> do NOT migrate reactively.

---

## 7. DI -- Koin

Koin, not Hilt. Better KMP ergonomics, readable error messages, no codegen overhead.

```kotlin
val commonModule = module {
    single<DispatcherProvider> { DefaultDispatcherProvider() }
    single<Analytics> { FirebaseAnalyticsTracker(FirebaseAnalytics.getInstance(androidContext())) }
}

val databaseModule = module {
    single { Room.databaseBuilder(androidContext(), AppDatabase::class.java, "app.db")
        .fallbackToDestructiveMigration(true).build() }
    single { get<AppDatabase>().itemDao() }
    single { ItemRepository(get()) }
}

val viewModelModule = module {
    viewModel { ItemListViewModel(get(), get(), get(), get()) }
    viewModel { params -> ItemDetailViewModel(params.get(), get(), get()) }  // params.get() is positional
}
```

- `single<Interface> { Impl(get()) }` -- expose interface, not concrete class.
- `androidContext()` instead of injecting `Context`.
- DO NOT pull from `GlobalContext` inside classes. Constructor injection everywhere. The ONE exception: composables use `koinViewModel()` / `koinInject()`.

```kotlin
// Composable injection
@Composable
fun ItemDetailScreen(itemId: Long) {
    val viewModel: ItemDetailViewModel = koinViewModel { parametersOf(itemId) }
}
```

---

## 8. Strong skipping and stability

Strong skipping is on by default. Rules:

1. Skipping is per-parameter. Under strong skipping, unproven stability no longer blocks skipping.
2. `@Stable` / `@Immutable` are mostly unnecessary. Keep only when the type has an expensive `equals()` or is in a dependency the compiler can't reason about.
3. Collection fields in state: use `List<T>` (immutable view) or `ImmutableList<T>`. A `MutableList<T>` field destabilises the enclosing data class.
4. Pass only the slice each composable needs, not whole state objects.
5. Read state as late as possible -- `Modifier.offset { offset.value }` defers to layout phase, skipping composition.
6. `derivedStateOf` for computed scalars, not bare `remember`.

Compiler reports for perf investigation:
```kotlin
composeCompiler {
    reportsDestination  = layout.buildDirectory.dir("compose_compiler")
    metricsDestination  = layout.buildDirectory.dir("compose_compiler")
}
```

---

## 9. Testing -- Turbine + MockK + Robolectric

JUnit 4 + Robolectric + MockK + Turbine + `kotlinx-coroutines-test`. No JUnit 5 on the Android side.

### 9.1 ViewModel test scaffold

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class ItemListViewModelTest {
    private lateinit var testDispatcher: TestDispatcher
    private lateinit var dispatchers: DispatcherProvider

    @Before fun setup() {
        testDispatcher = StandardTestDispatcher()
        dispatchers = object : DispatcherProvider {
            override val main = testDispatcher
            override val io = testDispatcher
            override val default = testDispatcher
        }
        Dispatchers.setMain(testDispatcher)
    }

    @After fun tearDown() {
        Dispatchers.resetMain()
        clearAllMocks(); unmockkAll()
    }

    @Test fun `load emits items then clears loading`() = runTest(testDispatcher) {
        val vm = ItemListViewModel(mockk(relaxed = true), dispatchers, mockk(relaxed = true))
        vm.state.test {
            assertEquals(ItemListContract.State(isLoading = true), awaitItem())
            val loaded = awaitItem()
            assertFalse(loaded.isLoading)
            cancelAndIgnoreRemainingEvents()
        }
    }

    @Test fun `delete emits ShowInfo effect`() = runTest(testDispatcher) {
        val vm = ItemListViewModel(repository, dispatchers, analytics)
        vm.effects.test {
            vm.dispatch(ItemListContract.Intent.ConfirmDelete(itemId = 1L))
            advanceUntilIdle()
            assertTrue(awaitItem() is ItemListContract.Effect.ShowInfo)
            cancelAndIgnoreRemainingEvents()
        }
    }
}
```

Key points: `StandardTestDispatcher()` + `Dispatchers.setMain(testDispatcher)` gives virtual time. Pass the same dispatcher to `runTest`. Fakes over mocks when the collaborator has behaviour.

### 9.2 Compose UI tests

```kotlin
@RunWith(RobolectricTestRunner::class)
@Config(sdk = [34])
class ItemListScreenTest {
    @get:Rule val composeRule = createComposeRule()

    @Test fun `empty state shows CTA`() {
        composeRule.setContent { AppTheme { ItemListContent(state = State(isLoading = false), onIntent = {}) } }
        composeRule.onNodeWithTag("add_item_fab").performClick()
    }
}
```

Drive the stateless `Content`, not the stateful `Screen`. `onNodeWithTag` over `onNodeWithText`. Apply `Modifier.testTag("...")` on every interactive element.

### 9.3 Turbine idioms

```kotlin
flow.test { assertEquals(Loading, awaitItem()); assertEquals(Success(data), awaitItem()); cancelAndIgnoreRemainingEvents() }

turbineScope {
    val a = flowA.testIn(this); val b = flowB.testIn(this)
    assertEquals(1, a.awaitItem()); assertEquals("x", b.awaitItem())
    a.cancel(); b.cancel()
}
```

### 9.4 Screenshot tests

Roborazzi is the current choice. Combine with `ComposablePreviewScanner` to turn every `@Preview` into a snapshot test automatically.

---

## 10. Theming -- Material 3 + extended tokens

```kotlin
data class AppExtendedColors(val cardBorder: Color, val subtleText: Color, val activeElement: Color)
val LocalAppExtendedColors = staticCompositionLocalOf { DarkExtendedColors }

val MaterialTheme.appColors: AppExtendedColors
    @Composable @ReadOnlyComposable get() = LocalAppExtendedColors.current

@Composable
fun AppTheme(darkTheme: Boolean = isSystemInDarkTheme(), content: @Composable () -> Unit) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme
    CompositionLocalProvider(LocalAppExtendedColors provides if (darkTheme) DarkExtendedColors else LightExtendedColors) {
        MaterialTheme(colorScheme = colorScheme, typography = AppTypography, shapes = AppShapes, content = content)
    }
}
```

- Custom tokens in a `data class` via `staticCompositionLocalOf`, exposed as `MaterialTheme.appColors`.
- `@ReadOnlyComposable` on the getter skips composer check.
- Use M3 role map exhaustively. Dynamic color optional per project.
- Expressive: `MaterialExpressiveTheme { ... }` for interior surfaces. Many components still `@ExperimentalMaterial3ExpressiveApi`.

### Adaptive layouts

```kotlin
NavigationSuiteScaffold(
    navigationSuiteItems = { /* items */ },
    layoutType = NavigationSuiteScaffoldDefaults.calculateFromAdaptiveInfo(currentWindowAdaptiveInfo()),
) { content() }
```

Swaps between `NavigationBar` / `NavigationRail` / `PermanentDrawer` by `WindowSizeClass`. For list/detail: `ListDetailPaneScaffold` from `adaptive-layout`.

### Edge-to-edge

```kotlin
override fun onCreate(savedInstanceState: Bundle?) {
    enableEdgeToEdge()  // BEFORE setContent
    super.onCreate(savedInstanceState)
    setContent { AppTheme { App() } }
}
```

Apply `Modifier.safeDrawingPadding()` on root scaffold. Cannot opt out on Android 16.

---

## 11. Data layer

### Room
- `@Entity` + `@Dao` + `Repository` + Mapper per table. Domain types have no Room annotations; entities have no business logic.
- KSP only: `ksp("androidx.room:room-compiler")`.
- Suspend / Flow DAOs only. Blocking DAOs are banned.
- `@TypeConverter`s live next to the entity, not in a global `Converters.kt`.

### DataStore
- Preferences DataStore for settings. Proto DataStore only for real schemas.
- Never `runBlocking` to read -- expose `Flow<Prefs>`.
- Encrypted values use `EncryptedSharedPreferences`, not DataStore.

### Networking
- OkHttp 5 baseline. Ktor 3.4 for KMP.
- Certificate pinning: pin SPKI hashes of **intermediate** certificates (not leaf), plus root CA as backup.

---

## 12. Performance

### Baseline Profiles
- Apply `id("androidx.baselineprofile")` to `:app` and `:baselineprofile`.
- Mark UI ready with `ReportDrawnWhen { uiIsReady }`.
- Add a Startup Profile (first-frame subset) for additional gains.

### R8 full mode
```kotlin
release {
    isMinifyEnabled = true; isShrinkResources = true
    proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
}
```
Remove any legacy `android.enableR8.fullMode=false` from `gradle.properties`.

### Previews
- Always wrap in `AppTheme`. Render the stateless `Content`, not the stateful `Screen`.
- Use `@PreviewLightDark`, `@PreviewScreenSizes`, custom multi-preview annotation.
- `ComposablePreviewScanner` turns previews into screenshot tests.

---

## 13. Gradle -- the `kotlin.compose` plugin is NOT a compiler artifact

In Kotlin 2.x, `alias(libs.plugins.kotlin.compose)` IS the Compose Compiler. Do NOT add `androidx.compose.compiler:compiler` as a dependency or set `kotlinCompilerExtensionVersion`.

Convention plugins go in `build-logic/` included build. `buildSrc` is no longer recommended -- invalidates build cache on every change.

Formatting: `spotless` with ktlint. `./gradlew spotlessApply` before every commit.

---

## 14. Anti-pattern catalog

| # | Anti-pattern | Correct approach |
|---|---|---|
| 1 | `collectAsState()` on anything hot | `collectAsStateWithLifecycle()` always |
| 2 | Suspend function in composable body | `LaunchedEffect` or hoist to VM |
| 3 | `MutableList` in State data class | `List<T>` or `ImmutableList<T>` |
| 4 | `object Foo : Intent` (bare object) | `data object Foo : Intent` |
| 5 | `SharedFlow(replay=0)` for one-shots | `Channel(BUFFERED).receiveAsFlow()` |
| 6 | Hard-coded `Dispatchers.IO` in repo | Inject `DispatcherProvider` |
| 7 | `NavController` inside screen composable | Hoist navigation callbacks to nav graph |
| 8 | Passing `NavBackStackEntry` down | Pull args with `toRoute<Route>()` at entry |
| 9 | `remember {}` for persistence | `rememberSaveable` or hoist to VM |
| 10 | Prophylactic `@Stable`/`@Immutable` | Only after compiler report shows unskippable restarts |
| 11 | Chained `flowOn` calls | One `flowOn` at end of upstream-heavy section |
| 12 | `.value` on StateFlow inside `update {}` | Use the reducer receiver |
| 13 | `ViewModelFactory` | Koin `viewModel { }` IS the factory |
| 14 | `LiveData<Event<T>>` / `SingleLiveEvent` | VM `Channel<Effect>` |
| 15 | `stopKoin()` in production | Koin is app-scoped; never tear down |
| 16 | Strings in code | `stringResource(R.string.foo)`. Effects carry `@StringRes Int` |
| 17 | `core/util` / `core/helpers` | Real domain module or inline next to caller |
| 18 | `@Serializable` route without serialization plugin | Apply `kotlin-serialization` plugin to the module |
| 19 | `material-icons-extended` in release | Pulls 10 MB. Use individual icons from `material-icons-core` |
| 20 | `LazyColumn` items without stable key | Always `key = { it.id }` |

---

## 15. Quick decision tree

> "How do I add a new screen?"

1. `feature/foo/FooContract.kt` -- `State`, `Intent`, `Effect`.
2. `FooViewModel : MviViewModel<...>(State())`. Override `handleIntent`. Observers in `init {}`.
3. Stateless `FooContent(state, onIntent, modifier)` + stateful `FooScreen(onNavigate..., viewModel = koinViewModel())`.
4. Register in `viewModelModule`: `viewModel { FooViewModel(get(), ...) }`.
5. `feature/foo/navigation/FooNavigation.kt` -- `@Serializable data object FooRoute` + `NavGraphBuilder.fooNavGraph(...)`.
6. Wire into `:app`'s `AppNavHost`.
7. Tests: `FooViewModelTest` (MockK + Turbine), `FooScreenTest` (Robolectric + `FooContent`).

> "Where does this code go?"

| Kind | Module |
|---|---|
| Domain type (data class, enum) | `:core:model` |
| Repository + Room DAO + entity | `:core:<domain>` |
| Reusable composable | `:ui:design` |
| Screen, contract, VM | `:feature:<name>` |
| MVI base, dispatchers, analytics | `:core:common` |
| Nav host, DI modules, Application | `:app` |

> "Which effect API?"

| Need | API |
|---|---|
| Collecting a flow | `collectAsStateWithLifecycle()` |
| Suspend work on entry | `LaunchedEffect(key) { }` |
| Non-suspend setup/teardown | `DisposableEffect(key) { onDispose { } }` |
| Computed value from hot state | `derivedStateOf { }` |
| VM effects Channel | `LaunchedEffect(Unit) { vm.effects.collect { } }` |
| Compose state as Flow (rare) | `snapshotFlow { }` |
