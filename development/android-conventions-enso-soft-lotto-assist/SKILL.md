---
name: android-conventions
description: |
  Defines Android/Kotlin coding conventions for the project. Includes naming
  rules, forbidden patterns, preferred practices, and code style guidelines.
  Use when writing code to ensure consistency. Use when user mentions:
  네이밍, 컨벤션, 코딩 규칙, 스타일 가이드, 금지 패턴, 권장 패턴,
  이름 규칙, 코드 스타일, 컨벤션 확인, 네이밍 규칙.
allowed-tools: Read, Glob, Grep
---

# Android Coding Conventions

프로젝트 코딩 컨벤션 및 스타일 가이드입니다.

## Naming Conventions

### Classes and Interfaces

| Type | Pattern | Example |
|------|---------|---------|
| UseCase | `{Action}{Subject}UseCase` | `GetLottoResultUseCase` |
| Repository Interface | `{Subject}Repository` | `LottoRepository` |
| Repository Impl | `{Subject}RepositoryImpl` | `LottoRepositoryImpl` |
| ViewModel | `{Feature}ViewModel` | `HomeViewModel` |
| Contract | `{Feature}Contract` | `HomeContract` |
| Screen | `{Feature}Screen` | `HomeScreen` |
| Content | `{Feature}Content` | `HomeContent` |
| DataSource | `{Subject}{Type}DataSource` | `LottoRemoteDataSource` |
| DTO | `{Subject}Dto` | `LottoDto` |
| Entity | `{Subject}Entity` | `LottoEntity` |

### Functions

| Type | Pattern | Example |
|------|---------|---------|
| UseCase invoke | `operator fun invoke()` | `suspend operator fun invoke(round: Int)` |
| Event handler | `on{Action}` | `onRefresh()`, `onItemClick()` |
| Private helper | `{action}{Subject}` | `loadData()`, `updateState()` |
| Mapper | `to{Target}()` | `toEntity()`, `toDomain()` |

### Variables

| Type | Pattern | Example |
|------|---------|---------|
| StateFlow | `_uiState` / `uiState` | Private mutable / Public immutable |
| Channel | `_effect` / `effect` | Private / Public |
| Boolean | `is{State}`, `has{Thing}` | `isLoading`, `hasError` |
| Collection | Plural nouns | `items`, `results`, `numbers` |

### Modules

```
feature:{feature-name}    # feature:home, feature:qrscan
core:{core-name}          # core:domain, core:data, core:network
```

## Forbidden Patterns

### 🚫 절대 사용 금지

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| `LiveData` | Deprecated pattern | `StateFlow` |
| `AsyncTask` | Deprecated | Coroutines |
| `GlobalScope` | Memory leak risk | `viewModelScope` |
| `runBlocking` (production) | Blocks thread | `suspend` + coroutines |
| `findViewById` | Old pattern | View Binding or Compose |
| XML layouts (new screens) | Migration to Compose | Jetpack Compose |
| Mutable collections (public) | Immutability violation | Immutable collections |

### Code Examples

```kotlin
// ❌ Don't
val items = mutableListOf<Item>()  // Public mutable
GlobalScope.launch { ... }
runBlocking { ... }

// ✅ Do
val items: List<Item> get() = _items.toList()  // Immutable copy
viewModelScope.launch { ... }
suspend fun doSomething() { ... }
```

## Preferred Patterns

### ✅ 권장 패턴

| Pattern | Usage |
|---------|-------|
| `invoke` operator | UseCase entry point |
| `Result<T>` | Error handling |
| State hoisting | Compose state management |
| Immutable data class | Domain models |
| `suspend` functions | One-shot operations |
| `Flow` | Data streams |
| `Modifier` first optional | Composable parameters |

### Code Examples

```kotlin
// ✅ UseCase with invoke
class GetDataUseCase @Inject constructor(...) {
    suspend operator fun invoke(id: String): Result<Data> = ...
}

// ✅ Result type for errors
suspend fun getData(): Result<Data> = runCatching {
    repository.fetchData()
}

// ✅ Immutable data class
data class LottoResult(
    val round: Int,
    val numbers: List<Int>,  // List is immutable interface
    val bonusNumber: Int
)

// ✅ Modifier as first optional parameter
@Composable
fun MyComponent(
    text: String,                    // Required
    modifier: Modifier = Modifier,   // First optional
    enabled: Boolean = true          // Other optionals
)
```

## Architecture Rules

### Layer Dependencies

```
✅ Allowed:
Presentation → Domain
Data → Domain

❌ Forbidden:
Domain → Data
Domain → Presentation
Presentation → Data (direct)
```

### Module Dependencies

```
✅ Allowed:
feature:* → core:domain
feature:* → core:di
core:data → core:domain
core:data → core:network
core:data → core:database

❌ Forbidden:
core:domain → core:data
core:domain → core:network
feature:home → feature:qrscan (direct)
```

## Code Style

### Imports

```kotlin
// ✅ Explicit imports (preferred)
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.MutableStateFlow

// ⚠️ Star imports (avoid when possible)
import kotlinx.coroutines.flow.*
```

### Formatting

```kotlin
// ✅ Parameter on new line when many
fun createViewModel(
    useCase1: UseCase1,
    useCase2: UseCase2,
    repository: Repository
): ViewModel

// ✅ Chain calls vertically
repository.getData()
    .map { it.toDomain() }
    .catch { emit(emptyList()) }
    .collect { ... }
```

### Comments

```kotlin
// ✅ KDoc for public APIs
/**
 * Fetches lotto result for the given round.
 *
 * @param round The round number to fetch
 * @return Result containing LottoResult or error
 */
suspend fun getLottoResult(round: Int): Result<LottoResult>

// ✅ Explain WHY, not WHAT
// Cache for 5 minutes to reduce API calls during rapid navigation
private val cache = CacheBuilder.newBuilder()
    .expireAfterWrite(5, TimeUnit.MINUTES)
    .build()

// ❌ Don't explain obvious code
// Increment counter by 1
counter++
```

## Korean Market Specifics

### Localization Formats

| Type | Format | Example |
|------|--------|---------|
| Date | `YYYY년 MM월 DD일` | `2024년 01월 15일` |
| Time | `오전/오후 HH:MM` | `오후 08:45` |
| Currency | `₩{amount:,}` | `₩1,000,000,000` |

### Accessibility

- Korean TTS pronunciation 고려
- 문장 길이 ≤ 30자 권장
- 명확한 동작 설명 (`"로또 결과 새로고침"`)

## File Organization

```
feature/home/
├── HomeScreen.kt           # Screen composable
├── HomeViewModel.kt        # ViewModel
├── HomeContract.kt         # UiState, Event, Effect
├── navigation/
│   └── HomeNavigation.kt   # Navigation setup
└── components/
    ├── LottoResultCard.kt  # Reusable component
    └── NumberBall.kt       # Reusable component
```
