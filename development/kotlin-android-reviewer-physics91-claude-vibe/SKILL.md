---
name: kotlin-android-reviewer
description: |
  WHEN: Android Kotlin code review, Jetpack Compose patterns, Coroutines/Flow checks, ViewModel structure analysis
  WHAT: Compose best practices + Coroutines patterns + State management + Memory leak detection + Performance optimization
  WHEN NOT: KMP shared code → kotlin-multiplatform-reviewer, Backend → kotlin-spring-reviewer
---

# Kotlin Android Reviewer Skill

## Purpose
Reviews Android Kotlin code for Jetpack Compose, Coroutines, Flow, and ViewModel best practices.

## When to Use
- Android Kotlin project code review
- "Compose pattern", "Coroutines", "Flow", "ViewModel" mentions
- Android performance, memory leak inspection
- Projects with Android plugin in `build.gradle.kts`

## Project Detection
- `com.android.application` or `com.android.library` in build.gradle
- `AndroidManifest.xml` exists
- `src/main/java` or `src/main/kotlin` directories

## Workflow

### Step 1: Analyze Project
```
**Kotlin**: 1.9.x
**Compose**: 1.5.x
**minSdk**: 24
**targetSdk**: 34
**Architecture**: MVVM + Clean Architecture
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full Android pattern check (recommended)
- Jetpack Compose UI patterns
- Coroutines/Flow usage
- ViewModel/State management
- Memory leaks/Performance
multiSelect: true
```

## Detection Rules

### Jetpack Compose Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Side-effect in Composable | Use LaunchedEffect/SideEffect | HIGH |
| Object creation without remember | Use remember { } | HIGH |
| Missing State hoisting | Hoist state to parent | MEDIUM |
| Missing derivedStateOf | Use for derived state | LOW |
| LazyColumn without key | Add key parameter | HIGH |

```kotlin
// BAD: Object creation without remember
@Composable
fun MyScreen() {
    val list = mutableListOf<String>()  // New every recomposition
}

// GOOD: Use remember
@Composable
fun MyScreen() {
    val list = remember { mutableListOf<String>() }
}

// BAD: Direct suspend call in Composable
@Composable
fun MyScreen(viewModel: MyViewModel) {
    viewModel.loadData()  // Side-effect!
}

// GOOD: Use LaunchedEffect
@Composable
fun MyScreen(viewModel: MyViewModel) {
    LaunchedEffect(Unit) {
        viewModel.loadData()
    }
}
```

### Coroutines Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| GlobalScope usage | Use viewModelScope/lifecycleScope | CRITICAL |
| Missing Dispatcher | Specify Dispatchers.IO/Default | MEDIUM |
| Missing exception handling | try-catch or CoroutineExceptionHandler | HIGH |
| runBlocking abuse | Convert to suspend function | HIGH |

```kotlin
// BAD: GlobalScope
GlobalScope.launch {
    repository.fetchData()
}

// GOOD: viewModelScope
viewModelScope.launch {
    repository.fetchData()
}

// BAD: Network on Main
viewModelScope.launch {
    val result = api.getData()  // NetworkOnMainThreadException
}

// GOOD: IO Dispatcher
viewModelScope.launch {
    val result = withContext(Dispatchers.IO) {
        api.getData()
    }
}
```

### Flow Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Direct collect in Composable | Use collectAsState | HIGH |
| SharedFlow without replay | Set appropriate replay value | MEDIUM |
| Nullable StateFlow initial | Provide meaningful initial value | MEDIUM |

```kotlin
// BAD: Direct collect in Composable
@Composable
fun MyScreen(viewModel: MyViewModel) {
    var data by remember { mutableStateOf<Data?>(null) }
    LaunchedEffect(Unit) {
        viewModel.dataFlow.collect { data = it }
    }
}

// GOOD: collectAsState
@Composable
fun MyScreen(viewModel: MyViewModel) {
    val data by viewModel.dataFlow.collectAsState()
}

// BAD: Nullable StateFlow initial
private val _state = MutableStateFlow<UiState?>(null)

// GOOD: Sealed class with clear initial state
private val _state = MutableStateFlow<UiState>(UiState.Loading)
```

### ViewModel Patterns
| Check | Issue | Severity |
|-------|-------|----------|
| Direct Context reference | Memory leak risk | CRITICAL |
| View reference | Memory leak risk | CRITICAL |
| Missing SavedStateHandle | Process death handling | MEDIUM |
| Bidirectional data flow | Use UiState + Event pattern | MEDIUM |

```kotlin
// BAD: Activity Context reference
class MyViewModel(private val context: Context) : ViewModel()

// GOOD: Application Context with Hilt
class MyViewModel(
    @ApplicationContext private val context: Context
) : ViewModel()

// BAD: Bidirectional binding
class MyViewModel : ViewModel() {
    var name = MutableLiveData<String>()
}

// GOOD: Unidirectional + sealed class
class MyViewModel : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    fun onNameChanged(name: String) {
        _uiState.update { it.copy(name = name) }
    }
}
```

### Memory Leak Detection
| Check | Problem | Solution |
|-------|---------|----------|
| Inner class with outer reference | Activity leak | WeakReference or static |
| Unremoved Listener | Memory leak | Remove in onDestroy |
| Uncancelled Coroutine Job | Job leak | Structured concurrency |
| Unreleased Bitmap | OOM risk | recycle() or Coil/Glide |

## Response Template
```
## Android Kotlin Code Review Results

**Project**: [name]
**Kotlin**: 1.9.x | **Compose**: 1.5.x
**Files Analyzed**: X

### Jetpack Compose
| Status | File | Issue |
|--------|------|-------|
| HIGH | ui/HomeScreen.kt | Object creation without remember (line 45) |
| MEDIUM | ui/ProfileScreen.kt | State hoisting recommended |

### Coroutines/Flow
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | data/Repository.kt | GlobalScope usage (line 23) |
| HIGH | viewmodel/MainViewModel.kt | Missing exception handling |

### ViewModel/State
| Status | File | Issue |
|--------|------|-------|
| HIGH | viewmodel/DetailViewModel.kt | Activity Context reference |

### Recommended Actions
1. [ ] GlobalScope → viewModelScope
2. [ ] Add remember { }
3. [ ] Apply UiState sealed class pattern
```

## Best Practices
1. **Compose**: Prefer Stateless Composable, State hoisting
2. **Coroutines**: Structured concurrency, appropriate Dispatcher
3. **Flow**: Distinguish Hot/Cold Flow, StateFlow for UI state
4. **ViewModel**: Unidirectional data flow, avoid Context
5. **Testing**: Turbine for Flow, Compose test rules

## Integration
- `code-reviewer` skill: General Kotlin code quality
- `kotlin-multiplatform-reviewer` skill: KMP shared code
- `test-generator` skill: Android test generation

## Notes
- Based on Compose 1.0+
- Kotlin 1.9+, Coroutines 1.7+ recommended
- Supports Hilt/Dagger DI patterns
