---
name: flutter-guide
description: |
  Flutter/BLoC Clean Architecture patterns, review checklists, and testing guides.
  Background knowledge for flutter-dev, flutter-reviewer, flutter-tester.
  Not user-invocable.
user-invocable: false
---

# Flutter Guide — Clean Architecture + BLoC

## Reference Guide

| Topic | Reference | Use When |
|-------|-----------|----------|
| Clean Architecture | `references/clean-architecture.md` | Layer rules, dependency direction |
| BLoC Patterns | `references/bloc-patterns.md` | @freezed events/states, handlers, transformers |
| UI Guidelines | `references/ui-guidelines.md` | AppColors, AppTextStyles, SVGImage |
| Review Checklist | `references/review-checklist.md` | Code review, quality checks |
| Mocking Guide | `references/mocking-guide.md` | Mocktail, MockBloc, ProviderContainer |
| Test Patterns | `references/test-patterns.md` | UseCase tests, BLoC tests, widget tests |

## Project Structure

```
lib/
├── core/          # AppError, extensions, DI (GetIt)
├── data/
│   ├── mapper/    # Entity <-> Model mappers
│   ├── network/   # API client, models (@JsonSerializable), interceptors
│   ├── repository/ # Repository implementations
│   └── services/
├── domain/
│   ├── entity/    # Domain entities (@freezed)
│   ├── repository/ # Abstract interfaces
│   ├── services/
│   └── usecases/
├── presentation/
│   ├── {feature}/
│   │   ├── bloc.dart       # FeatureBloc
│   │   ├── events.dart     # @freezed events
│   │   ├── states.dart     # @freezed states
│   │   └── view/           # Pages + widgets
│   └── common/
└── resources/     # Colors, text styles, localization
```

## Dependency Rule

`Presentation -> Domain <- Data` — Domain depends on NOTHING.

## Critical Rules

### 1. MANDATORY: @freezed for Events and States

```dart
@freezed
class FeatureEvent with _$FeatureEvent {
  const factory FeatureEvent.started() = _Started;
  const factory FeatureEvent.loadData({required int id}) = _LoadData;
}

@freezed
class FeatureState with _$FeatureState {
  const factory FeatureState.initial() = _Initial;
  const factory FeatureState.loading() = _Loading;
  const factory FeatureState.loaded(Data data) = _Loaded;
  const factory FeatureState.error(AppError error) = _Error;
}
```

### 2. BLoC Individual Event Handlers

```dart
class FeatureBloc extends Bloc<FeatureEvent, FeatureState> {
  FeatureBloc() : super(const FeatureState.initial()) {
    on<_Started>(_onStarted);
    on<_LoadData>(_onLoadData);
  }

  Future<void> _onLoadData(_LoadData event, Emitter<FeatureState> emit) async {
    emit(const FeatureState.loading());
    final result = await _repository.getData(event.id);
    result.fold(
      (error) => emit(FeatureState.error(error)),
      (data) => emit(FeatureState.loaded(data)),
    );
  }
}
```

NEVER use `event.when()` or `state.when()` in BLoC handlers.
NEVER use a single handler for all events.

### 3. Either for Error Handling

```dart
abstract class UserRepository {
  Future<Either<AppError, User>> getUser(int id);
}
```

### 4. Type-Safe Models

```dart
// Domain Entity
@freezed
class UserEntity with _$UserEntity {
  const factory UserEntity({
    required String id,
    required String name,
    required UserRole role,
  }) = _UserEntity;
}

// API Model
@freezed
@JsonSerializable()
class UserApiModel with _$UserApiModel {
  const factory UserApiModel({...}) = _UserApiModel;
  factory UserApiModel.fromJson(Map<String, dynamic> json) =>
      _$UserApiModelFromJson(json);
}

// Mapper
extension UserApiMapper on UserApiModel {
  UserEntity toDomain() => UserEntity(id: id, name: name, role: UserRole.fromString(role));
}
```

## Dart 3.x: Use Modern Features

- **Sealed classes** for exhaustive state matching (alternative to @freezed unions)
- **Pattern matching** in switch expressions
- **Records** for lightweight multiple return values
- **Null safety** everywhere, no `!` operator without justification

## Performance Rules

- **const constructors** everywhere possible
- **Keys** on list items (`ValueKey(item.id)`)
- **ListView.builder** for large lists
- **buildWhen** in BlocBuilder for granular rebuilds
- **CachedNetworkImage** with `memCacheWidth`/`memCacheHeight`
- Extract expensive subtrees into separate const widgets
- No expensive operations in `build()` methods

## Anti-Patterns (FORBIDDEN)

| Pattern | Reason |
|---------|--------|
| `Map<String, dynamic>` for data | No type safety |
| `event.when()` in BLoC handlers | Use individual handlers |
| `state.when()` in BLoC handlers | Only for UI |
| Single handler for all events | Hard to maintain |
| Hardcoded strings in UI | Use AppLocalization |
| `SvgPicture.asset()` | Use SVGImage() |
| Redundant comments | Code must be self-documenting |
| `dynamic` type | No type safety |

## UI Patterns

```dart
// BlocBuilder with buildWhen
BlocBuilder<FeatureBloc, FeatureState>(
  buildWhen: (previous, current) => previous != current,
  builder: (context, state) {
    return state.when(
      initial: () => const SizedBox.shrink(),
      loading: () => const LoadingWidget(),
      loaded: (data) => DataWidget(data: data),
      error: (error) => ErrorWidget(error: error),
    );
  },
)

// BlocListener for side effects
BlocListener<FeatureBloc, FeatureState>(
  listenWhen: (previous, current) => current is _Error,
  listener: (context, state) {
    if (state is _Error) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.error.message)),
      );
    }
  },
)
```

## Code Generation

```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

## Testing Summary

- **BLoC tests** (MANDATORY): `bloc_test` with `blocTest<>()`, seed, expect, verify
- **Flow tests** (MANDATORY): after create -> list updated, after delete -> item removed
- **Widget tests**: BlocProvider + MockBloc
- **Coverage**: 80%+ with `flutter test --coverage`

## Review Summary

1. Architecture compliance (correct layer, inward dependencies)
2. Type safety (no dynamic, no Map<String, dynamic>)
3. BLoC patterns (individual handlers, no event.when(), no state.when())
4. @freezed on all events/states
5. UI standards (AppColors, AppTextStyles, AppLocalization, const)
6. No redundant comments
