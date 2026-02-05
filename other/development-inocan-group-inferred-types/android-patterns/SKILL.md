---
name: android-patterns
description: |
  Provides Android coding patterns for Kotlin 2.0 and Jetpack Compose projects.
  Includes MVI architecture, Clean Architecture layers, Compose best practices,
  and Coroutines/Flow patterns. Use when writing Android code, implementing
  features, reviewing code, or learning patterns. Use when user mentions:
  MVI 패턴, 클린 아키텍처, 컴포즈 패턴, 코루틴, Flow, 상태 관리, 아키텍처,
  ViewModel 패턴, 레이어 구조, 패턴 설명.
---

# Android Coding Patterns

Kotlin 2.0 + Jetpack Compose 프로젝트를 위한 코딩 패턴 가이드입니다.

## Architecture: Clean Architecture + MVI

### Layer Overview

| Layer | Responsibility | Dependencies |
|-------|---------------|--------------|
| **Domain** | Business logic, UseCases | None (pure Kotlin) |
| **Data** | Repository impl, DataSources | Domain |
| **Presentation** | ViewModel, UI State, Compose | Domain |

```
┌─────────────────────────────────────────┐
│            Presentation                 │
│  (ViewModel, Compose UI, Contract)      │
└─────────────────┬───────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────┐
│              Domain                     │
│  (UseCases, Models, Repository I/F)     │
└─────────────────┬───────────────────────┘
                  │ depends on
┌─────────────────▼───────────────────────┐
│               Data                      │
│  (Repository Impl, DataSources, DTOs)   │
└─────────────────────────────────────────┘
```

## Quick References

### MVI Pattern

State, Event, Effect로 구성된 단방향 데이터 흐름 패턴.

```kotlin
// Contract 기본 구조
data class UiState(val isLoading: Boolean = false, val data: List<Item> = emptyList())
sealed interface Event { data class LoadData(val id: String) : Event }
sealed interface Effect { data class ShowToast(val message: String) : Effect }
```

**상세 가이드:** [patterns/mvi-pattern.md](patterns/mvi-pattern.md)

### Compose Patterns

상태 호이스팅, Modifier 규칙, Recomposition 최적화.

```kotlin
// State Hoisting 기본
@Composable
fun Counter(count: Int, onIncrement: () -> Unit) {
    Button(onClick = onIncrement) { Text("$count") }
}
```

**상세 가이드:** [patterns/compose-patterns.md](patterns/compose-patterns.md)

### Clean Architecture

레이어별 구현 가이드 및 의존성 규칙.

```kotlin
// UseCase 기본 구조
class GetLottoResultUseCase @Inject constructor(
    private val repository: LottoRepository
) {
    suspend operator fun invoke(roundNumber: Int): Result<LottoResult> =
        repository.getLottoResult(roundNumber)
}
```

**상세 가이드:** [patterns/clean-architecture.md](patterns/clean-architecture.md)

### Coroutines & Flow

비동기 처리 및 반응형 스트림 패턴.

```kotlin
// StateFlow 기본
private val _uiState = MutableStateFlow(UiState())
val uiState: StateFlow<UiState> = _uiState.asStateFlow()
```

**상세 가이드:** [patterns/coroutines-flow.md](patterns/coroutines-flow.md)

## Code Templates

### ViewModel Template

```kotlin
@HiltViewModel
class FeatureViewModel @Inject constructor(
    private val useCase: SomeUseCase
) : ViewModel() {
    private val _uiState = MutableStateFlow(UiState())
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    private val _effect = Channel<Effect>()
    val effect = _effect.receiveAsFlow()

    fun onEvent(event: Event) {
        when (event) {
            is Event.Load -> loadData()
        }
    }

    private fun loadData() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true) }
            useCase().fold(
                onSuccess = { data -> _uiState.update { it.copy(isLoading = false, data = data) } },
                onFailure = { _effect.send(Effect.ShowError(it.message)) }
            )
        }
    }
}
```

### UseCase Template

```kotlin
class GetDataUseCase @Inject constructor(
    private val repository: DataRepository
) {
    suspend operator fun invoke(param: String): Result<Data> =
        repository.getData(param)
}
```

### Repository Template

```kotlin
// Domain layer - Interface
interface DataRepository {
    suspend fun getData(param: String): Result<Data>
}

// Data layer - Implementation
class DataRepositoryImpl @Inject constructor(
    private val remoteDataSource: RemoteDataSource,
    private val localDataSource: LocalDataSource
) : DataRepository {
    override suspend fun getData(param: String): Result<Data> =
        runCatching { remoteDataSource.fetchData(param).toDomain() }
}
```

## Module Structure

```
app/                    # Application entry
core/
├── domain/            # Pure Kotlin
├── data/              # Repository impl
├── network/           # Retrofit
├── database/          # Room
└── di/                # Hilt modules
feature/
├── home/              # Feature module
└── qrscan/            # Feature module
```
