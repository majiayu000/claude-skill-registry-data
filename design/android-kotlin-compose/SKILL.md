---
name: android-kotlin-compose
description: Android development with Kotlin and Jetpack Compose. Use when user mentions "Compose", "Jetpack Compose", "Material3", "Hilt", "Room", "ViewModel", or needs to build Android UI, implement MVVM architecture, manage Compose state, or integrate Jetpack libraries (Navigation, Room, Hilt, ViewModel). Triggers on Android/Compose/Kotlin development tasks.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(./gradlew:*), Bash(adb:*), WebSearch, WebFetch
---

# Android Kotlin Compose

Expert guidance for Android development using Kotlin and Jetpack Compose with modern architecture patterns.

## When to Use This Skill

Invoke this skill when:

- Building Android UIs with Jetpack Compose
- Implementing MVVM architecture with ViewModels and StateFlow
- Managing state in Compose applications (remember, State hoisting)
- Integrating Jetpack libraries (Navigation, Room, Hilt, ViewModel, WorkManager)
- Designing Material3 interfaces and theming
- User explicitly mentions "Compose", "Kotlin Android", "Jetpack", or related libraries

## Core Principles

1. **Compose-First UI** — Declarative UI with composable functions
2. **Unidirectional Data Flow** — State flows down, events flow up
3. **Single Source of Truth** — ViewModel owns UI state
4. **Separation of Concerns** — UI layer decoupled from data layer

## Quick Reference

### Project Structure (Recommended)

```
app/src/main/java/com/example/app/
├── di/                     # Hilt modules
│   └── AppModule.kt
├── data/
│   ├── local/              # Room database
│   │   ├── dao/
│   │   ├── entity/
│   │   └── AppDatabase.kt
│   ├── remote/             # Network layer
│   │   ├── api/
│   │   └── dto/
│   └── repository/         # Repository implementations
├── domain/
│   ├── model/              # Domain models
│   ├── repository/         # Repository interfaces
│   └── usecase/            # Business logic
├── ui/
│   ├── components/         # Reusable composables
│   ├── theme/              # Material3 theming
│   │   ├── Color.kt
│   │   ├── Type.kt
│   │   └── Theme.kt
│   ├── navigation/         # Navigation graph
│   └── screens/            # Feature screens
│       └── feature/
│           ├── FeatureScreen.kt
│           └── FeatureViewModel.kt
└── App.kt                  # Application class
```

## UI Development Patterns

### Screen Pattern with ViewModel

```kotlin
// FeatureViewModel.kt
@HiltViewModel
class FeatureViewModel @Inject constructor(
    private val repository: FeatureRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(FeatureUiState())
    val uiState: StateFlow<FeatureUiState> = _uiState.asStateFlow()

    fun onAction(action: FeatureAction) {
        when (action) {
            is FeatureAction.LoadData -> loadData()
            is FeatureAction.UpdateItem -> updateItem(action.item)
        }
    }

    private fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            repository.getData()
                .onSuccess { data ->
                    _uiState.update { it.copy(data = data, isLoading = false) }
                }
                .onFailure { error ->
                    _uiState.update { it.copy(error = error.message, isLoading = false) }
                }
        }
    }
}

// FeatureUiState.kt
data class FeatureUiState(
    val data: List<Item> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

sealed interface FeatureAction {
    data object LoadData : FeatureAction
    data class UpdateItem(val item: Item) : FeatureAction
}

// FeatureScreen.kt
@Composable
fun FeatureScreen(
    viewModel: FeatureViewModel = hiltViewModel(),
    onNavigateToDetail: (String) -> Unit
) {
    val uiState by viewModel.uiState.collectAsStateWithLifecycle()

    FeatureContent(
        uiState = uiState,
        onAction = viewModel::onAction,
        onNavigateToDetail = onNavigateToDetail
    )
}

@Composable
private fun FeatureContent(
    uiState: FeatureUiState,
    onAction: (FeatureAction) -> Unit,
    onNavigateToDetail: (String) -> Unit
) {
    // Stateless composable - easy to preview and test
    when {
        uiState.isLoading -> LoadingIndicator()
        uiState.error != null -> ErrorMessage(uiState.error)
        else -> ItemList(
            items = uiState.data,
            onItemClick = { onNavigateToDetail(it.id) }
        )
    }
}
```

### State Hoisting Pattern

```kotlin
// Stateful wrapper
@Composable
fun SearchBar(
    onSearch: (String) -> Unit
) {
    var query by rememberSaveable { mutableStateOf("") }

    SearchBarContent(
        query = query,
        onQueryChange = { query = it },
        onSearch = { onSearch(query) }
    )
}

// Stateless implementation (previewable)
@Composable
private fun SearchBarContent(
    query: String,
    onQueryChange: (String) -> Unit,
    onSearch: () -> Unit
) {
    OutlinedTextField(
        value = query,
        onValueChange = onQueryChange,
        trailingIcon = {
            IconButton(onClick = onSearch) {
                Icon(Icons.Default.Search, contentDescription = "Search")
            }
        }
    )
}
```

### Side Effects

```kotlin
// LaunchedEffect - runs when key changes
LaunchedEffect(userId) {
    viewModel.loadUser(userId)
}

// LaunchedEffect(Unit) - runs once on composition
LaunchedEffect(Unit) {
    viewModel.initialize()
}

// DisposableEffect - cleanup when leaving composition
DisposableEffect(lifecycleOwner) {
    val observer = LifecycleEventObserver { _, event ->
        if (event == Lifecycle.Event.ON_RESUME) {
            viewModel.refresh()
        }
    }
    lifecycleOwner.lifecycle.addObserver(observer)
    onDispose {
        lifecycleOwner.lifecycle.removeObserver(observer)
    }
}

// SideEffect - runs after every successful composition
SideEffect {
    analytics.trackScreen("FeatureScreen")
}

// rememberCoroutineScope - for event handlers
val scope = rememberCoroutineScope()
Button(onClick = {
    scope.launch {
        viewModel.saveData()
    }
}) { Text("Save") }
```

## Navigation

### Type-Safe Navigation (Compose 2.8+)

```kotlin
// Routes.kt
@Serializable
data object Home

@Serializable
data class Detail(val id: String)

@Serializable
data class Settings(val section: String? = null)

// NavGraph.kt
@Composable
fun AppNavGraph(
    navController: NavHostController = rememberNavController()
) {
    NavHost(navController = navController, startDestination = Home) {
        composable<Home> {
            HomeScreen(
                onNavigateToDetail = { id ->
                    navController.navigate(Detail(id))
                }
            )
        }

        composable<Detail> { backStackEntry ->
            val detail: Detail = backStackEntry.toRoute()
            DetailScreen(itemId = detail.id)
        }

        composable<Settings> { backStackEntry ->
            val settings: Settings = backStackEntry.toRoute()
            SettingsScreen(initialSection = settings.section)
        }
    }
}
```

### Navigation with Results

```kotlin
// Returning results to previous screen
composable<SelectItem> {
    SelectItemScreen(
        onItemSelected = { item ->
            navController.previousBackStackEntry
                ?.savedStateHandle
                ?.set("selected_item", item)
            navController.popBackStack()
        }
    )
}

// Receiving results
composable<Home> {
    val savedStateHandle = navController.currentBackStackEntry?.savedStateHandle
    val selectedItem by savedStateHandle
        ?.getStateFlow<Item?>("selected_item", null)
        ?.collectAsStateWithLifecycle() ?: remember { mutableStateOf(null) }

    HomeScreen(selectedItem = selectedItem)
}
```

## Dependency Injection with Hilt

### Module Setup

```kotlin
// AppModule.kt
@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase {
        return Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app_database"
        ).build()
    }

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao {
        return database.userDao()
    }
}

// RepositoryModule.kt
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    @Singleton
    abstract fun bindUserRepository(
        impl: UserRepositoryImpl
    ): UserRepository
}
```

### ViewModel Injection

```kotlin
@HiltViewModel
class UserViewModel @Inject constructor(
    private val userRepository: UserRepository,
    private val savedStateHandle: SavedStateHandle
) : ViewModel() {

    private val userId: String = savedStateHandle.get<String>("userId")
        ?: throw IllegalArgumentException("userId required")
}

// In Composable
@Composable
fun UserScreen(
    viewModel: UserViewModel = hiltViewModel()
) {
    // ViewModel automatically scoped to navigation destination
}
```

## Room Database

### Entity and DAO

```kotlin
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    val name: String,
    val email: String,
    @ColumnInfo(name = "created_at") val createdAt: Long
)

@Dao
interface UserDao {
    @Query("SELECT * FROM users WHERE id = :id")
    fun getUser(id: String): Flow<UserEntity?>

    @Query("SELECT * FROM users ORDER BY name ASC")
    fun getAllUsers(): Flow<List<UserEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertUser(user: UserEntity)

    @Delete
    suspend fun deleteUser(user: UserEntity)

    @Transaction
    @Query("SELECT * FROM users WHERE id = :id")
    fun getUserWithPosts(id: String): Flow<UserWithPosts>
}

@Database(
    entities = [UserEntity::class, PostEntity::class],
    version = 1,
    exportSchema = true
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
    abstract fun postDao(): PostDao
}
```

### Repository Pattern

```kotlin
interface UserRepository {
    fun getUser(id: String): Flow<User?>
    fun getAllUsers(): Flow<List<User>>
    suspend fun saveUser(user: User): Result<Unit>
}

class UserRepositoryImpl @Inject constructor(
    private val userDao: UserDao,
    private val userApi: UserApi,
    @IoDispatcher private val ioDispatcher: CoroutineDispatcher
) : UserRepository {

    override fun getUser(id: String): Flow<User?> {
        return userDao.getUser(id)
            .map { it?.toDomain() }
            .flowOn(ioDispatcher)
    }

    override suspend fun saveUser(user: User): Result<Unit> {
        return withContext(ioDispatcher) {
            runCatching {
                userDao.insertUser(user.toEntity())
            }
        }
    }
}
```

## Material3 Theming

### Theme Setup

```kotlin
// Color.kt
val Purple80 = Color(0xFFD0BCFF)
val PurpleGrey80 = Color(0xFFCCC2DC)
val Purple40 = Color(0xFF6650a4)

// Type.kt
val Typography = Typography(
    headlineLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Bold,
        fontSize = 32.sp,
        lineHeight = 40.sp
    ),
    bodyLarge = TextStyle(
        fontFamily = FontFamily.Default,
        fontWeight = FontWeight.Normal,
        fontSize = 16.sp,
        lineHeight = 24.sp
    )
)

// Theme.kt
private val DarkColorScheme = darkColorScheme(
    primary = Purple80,
    secondary = PurpleGrey80,
    tertiary = Pink80
)

private val LightColorScheme = lightColorScheme(
    primary = Purple40,
    secondary = PurpleGrey40,
    tertiary = Pink40
)

@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    dynamicColor: Boolean = true,
    content: @Composable () -> Unit
) {
    val colorScheme = when {
        dynamicColor && Build.VERSION.SDK_INT >= Build.VERSION_CODES.S -> {
            val context = LocalContext.current
            if (darkTheme) dynamicDarkColorScheme(context)
            else dynamicLightColorScheme(context)
        }
        darkTheme -> DarkColorScheme
        else -> LightColorScheme
    }

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}
```

### Using Theme Values

```kotlin
@Composable
fun ThemedCard() {
    Card(
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.surfaceVariant
        )
    ) {
        Text(
            text = "Title",
            style = MaterialTheme.typography.headlineSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
}
```

## Common Anti-Patterns

### ❌ Avoid

```kotlin
// DON'T: State in composable that survives recomposition incorrectly
@Composable
fun Counter() {
    var count = 0  // Resets on every recomposition!
    Button(onClick = { count++ }) { Text("$count") }
}

// DON'T: Side effects in composition
@Composable
fun BadScreen(viewModel: ViewModel) {
    viewModel.loadData()  // Called on every recomposition!
}

// DON'T: Create objects in composition without remember
@Composable
fun BadList(items: List<Item>) {
    val derivedList = items.filter { it.isActive }  // Recreated every recomposition
}

// DON'T: Collect flow without lifecycle awareness
val state by viewModel.uiState.collectAsState()  // May leak
```

### ✅ Correct

```kotlin
// DO: Use remember for state
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    Button(onClick = { count++ }) { Text("$count") }
}

// DO: Use LaunchedEffect for side effects
@Composable
fun GoodScreen(viewModel: ViewModel) {
    LaunchedEffect(Unit) {
        viewModel.loadData()
    }
}

// DO: Use remember/derivedStateOf for computed values
@Composable
fun GoodList(items: List<Item>) {
    val derivedList by remember(items) {
        derivedStateOf { items.filter { it.isActive } }
    }
}

// DO: Use lifecycle-aware collection
val state by viewModel.uiState.collectAsStateWithLifecycle()
```

## Resources

For detailed patterns and integration guides, see:

- `references/compose-patterns.md` — Advanced composition patterns, performance optimization, custom layouts
- `references/jetpack-integration.md` — Deep integration with Navigation, Room, Hilt, WorkManager
- `references/animations.md` — Complete animation guide: animate*AsState, transitions, AnimatedVisibility, gestures,
  shared elements, Lottie

### When to Consult References

- Complex custom layouts → `compose-patterns.md`
- Multi-module navigation setup → `jetpack-integration.md`
- Database migrations or relations → `jetpack-integration.md`
- Performance profiling → `compose-patterns.md`
- **Animations** (state-based, transitions, gestures, shared elements) → `animations.md`
- Lottie integration → `animations.md`
