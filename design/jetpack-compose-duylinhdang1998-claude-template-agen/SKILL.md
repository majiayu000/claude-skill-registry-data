---
name: jetpack-compose
description: Modern Android UI development with Jetpack Compose from Google's Android team. Use when building declarative Android UIs, creating Compose screens and components, implementing Material Design 3, handling navigation with Compose Navigation, managing state with remember/mutableStateOf, or building responsive layouts. Triggers on Jetpack Compose, Compose UI, Android UI, Material3, composable functions, or Android declarative UI.
---

# Jetpack Compose - Modern Android UI

**Purpose**: Build native Android UIs with declarative Jetpack Compose framework

**Agent**: Google Android Lead
**Use When**: Building Android UI, migrating from XML layouts, or creating custom composables

---

## Compose Basics

```kotlin
@Composable
fun Greeting(name: String) {
    Text(text = "Hello, $name!")
}

// Preview
@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    Greeting("Android")
}

// Column/Row/Box (like flexbox)
@Composable
fun UserCard(user: User) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Image(
                painter = painterResource(R.drawable.avatar),
                contentDescription = null,
                modifier = Modifier.size(48.dp)
            )
            Spacer(modifier = Modifier.width(16.dp))
            Column {
                Text(text = user.name, style = MaterialTheme.typography.titleMedium)
                Text(text = user.email, style = MaterialTheme.typography.bodySmall)
            }
        }
    }
}
```

---

## State Management

```kotlin
// remember state
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }

    Column {
        Text("Count: $count")
        Button(onClick = { count++ }) {
            Text("Increment")
        }
    }
}

// ViewModel state
@Composable
fun UserListScreen(viewModel: UserViewModel = viewModel()) {
    val users by viewModel.users.collectAsState()
    val isLoading by viewModel.isLoading.collectAsState()

    if (isLoading) {
        CircularProgressIndicator()
    } else {
        LazyColumn {
            items(users) { user ->
                UserItem(user = user)
            }
        }
    }
}

// State hoisting
@Composable
fun SearchBar(
    query: String,
    onQueryChange: (String) -> Unit
) {
    TextField(
        value = query,
        onValueChange = onQueryChange,
        label = { Text("Search") }
    )
}

@Composable
fun SearchScreen() {
    var query by remember { mutableStateOf("") }

    Column {
        SearchBar(query = query, onQueryChange = { query = it })
        SearchResults(query = query)
    }
}
```

---

## Lists

```kotlin
@Composable
fun UserList(users: List<User>) {
    LazyColumn {
        items(users) { user ->
            UserItem(user = user)
        }

        // Or with key
        items(users, key = { it.id }) { user ->
            UserItem(user = user)
        }
    }
}

// Grid
@Composable
fun PhotoGrid(photos: List<Photo>) {
    LazyVerticalGrid(
        columns = GridCells.Fixed(3),
        contentPadding = PaddingValues(8.dp)
    ) {
        items(photos) { photo ->
            PhotoItem(photo = photo)
        }
    }
}
```

---

## Navigation

```kotlin
@Composable
fun AppNavigation() {
    val navController = rememberNavController()

    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            HomeScreen(
                onNavigateToDetail = { userId ->
                    navController.navigate("detail/$userId")
                }
            )
        }

        composable(
            route = "detail/{userId}",
            arguments = listOf(navArgument("userId") { type = NavType.IntType })
        ) { backStackEntry ->
            val userId = backStackEntry.arguments?.getInt("userId")
            DetailScreen(userId = userId)
        }
    }
}
```

---

## Side Effects

```kotlin
@Composable
fun UserScreen(userId: Int, viewModel: UserViewModel = viewModel()) {
    // LaunchedEffect - run on composition
    LaunchedEffect(userId) {
        viewModel.loadUser(userId)
    }

    // DisposableEffect - cleanup
    DisposableEffect(Unit) {
        val listener = viewModel.addListener()
        onDispose {
            listener.remove()
        }
    }

    // rememberCoroutineScope - launch coroutines
    val scope = rememberCoroutineScope()

    Button(onClick = {
        scope.launch {
            viewModel.refreshData()
        }
    }) {
        Text("Refresh")
    }
}
```

---

## Theming

```kotlin
@Composable
fun MyAppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit
) {
    val colors = if (darkTheme) {
        darkColorScheme()
    } else {
        lightColorScheme()
    }

    MaterialTheme(
        colorScheme = colors,
        typography = Typography,
        content = content
    )
}

// Usage
@Composable
fun App() {
    MyAppTheme {
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = MaterialTheme.colorScheme.background
        ) {
            MainScreen()
        }
    }
}
```

---

## Best Practices

- Composables should be pure functions
- Hoist state when shared between composables
- Use keys in lists for recomposition optimization
- Avoid side effects in composition (use `LaunchedEffect`)
- Remember expensive computations with `remember`
- Use `derivedStateOf` for computed state
- Keep composables small and focused
- Preview composables for fast iteration

---

**Remember**: Compose is declarative. UI = f(state). No XML, no findViewById.

**Created**: 2026-02-04
**Maintained By**: Google Android Lead
