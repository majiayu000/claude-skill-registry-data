---
tags: [flutter, bloc, state-management, cubit]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter BLoC / Cubit Pattern

## Context

Apply when creating or modifying state management using the BLoC/Cubit pattern in Flutter projects.

## Instructions

1. **Cubit vs BLoC**: Use `Cubit` for simple state, `Bloc` for event-driven flows.
2. **State classes**: Use `freezed` with a single state class and an `ApiStatus` enum (`initial`, `loading`, `success`, `error`). Freezed auto-generates `copyWith` and equality.
3. **Naming convention**:
   - Cubit: `FeatureNameCubit` → `FeatureNameState`
   - Bloc: `FeatureNameBloc` → `FeatureNameEvent` / `FeatureNameState`
4. **File structure**:
   ```
   feature_name/
   ├── cubit/
   │   ├── feature_name_cubit.dart
   │   └── feature_name_state.dart
   ├── view/
   │   └── feature_name_page.dart
   └── widgets/
       └── ...
   ```
5. **Never** put business logic in widgets — always delegate to cubit/bloc.
6. **Use** `BlocProvider` at the route level, `BlocBuilder`/`BlocSelector` in widgets.
7. **Error handling**: Emit error states with meaningful messages, catch exceptions in cubit methods.

## Examples

### ApiStatus Enum

```dart
enum ApiStatus { initial, loading, success, error }
```

### State Class

```dart
@freezed
class UserProfileState with _$UserProfileState {
  const factory UserProfileState({
    @Default(ApiStatus.initial) ApiStatus status,
    User? user,
    String? errorMessage,
  }) = _UserProfileState;
}
```

### Cubit

```dart
class UserProfileCubit extends Cubit<UserProfileState> {
  UserProfileCubit(this._repo) : super(const UserProfileState());

  final UserRepository _repo;

  Future<void> loadProfile(String userId) async {
    emit(state.copyWith(status: ApiStatus.loading));
    try {
      final user = await _repo.getUser(userId);
      emit(state.copyWith(status: ApiStatus.success, user: user));
    } catch (e) {
      emit(state.copyWith(
        status: ApiStatus.error,
        errorMessage: e.toString(),
      ));
    }
  }
}
```

### Widget Usage

```dart
BlocBuilder<UserProfileCubit, UserProfileState>(
  builder: (context, state) {
    return switch (state.status) {
      ApiStatus.initial || ApiStatus.loading => const LoadingIndicator(),
      ApiStatus.success => UserProfileView(user: state.user!),
      ApiStatus.error => ErrorView(message: state.errorMessage),
    };
  },
)
```

## Form Management (Reactive Forms)

When using `reactive_forms` with BLoC/Cubit, you can manage the `FormGroup` within the **Cubit** to centralize validation and business logic.

### Implementation Pattern (Cubit-Managed)

1.  **Initialize**: Define and initialize the `FormGroup` as a `late final` property in the Cubit.
2.  **Dispose**: Override the `close()` method in the Cubit to dispose of the form.
3.  **Access**: The widget retrieves the form via `context.read<MyCubit>().form`.
4.  **Action**: Create a method in the Cubit that validates the form and performs the business logic.

```dart
// Cubit
class LoginCubit extends Cubit<LoginState> {
  LoginCubit(this._repo) : super(const LoginState()) {
    // 1. Initialize form
    form = fb.group({
      'email': ['', Validators.required, Validators.email],
      'password': ['', Validators.required],
    });
  }

  final AuthRepository _repo;
  late final FormGroup form;

  // 2. Dispose form
  @override
  Future<void> close() {
    form.dispose();
    return super.close();
  }

  Future<void> login() async {
    if (form.invalid) {
      form.markAllAsTouched();
      return;
    }

    emit(state.copyWith(status: ApiStatus.loading));
    try {
      await _repo.login(
        email: form.control('email').value,
        password: form.control('password').value,
      );
      emit(state.copyWith(status: ApiStatus.success));
    } catch (e) {
      emit(state.copyWith(status: ApiStatus.error, errorMessage: e.toString()));
    }
  }
}

### Implementation Pattern (Bloc-Managed)

For event-driven flows, the form remains in the Bloc, and actions are triggered by events.

```dart
// Bloc
class LoginBloc extends Bloc<LoginEvent, LoginState> {
  LoginBloc(this._repo) : super(const LoginState()) {
    on<LoginSubmitted>(_onSubmitted);
    
    // 1. Initialize form
    form = fb.group({
      'email': ['', Validators.required, Validators.email],
      'password': ['', Validators.required],
    });
  }

  final AuthRepository _repo;
  late final FormGroup form;

  // 2. Dispose form
  @override
  Future<void> close() {
    form.dispose();
    return super.close();
  }

  Future<void> _onSubmitted(LoginSubmitted event, Emitter<LoginState> emit) async {
    if (form.invalid) {
      form.markAllAsTouched();
      return;
    }

    emit(state.copyWith(status: ApiStatus.loading));
    try {
      await _repo.login(
        email: form.control('email').value,
        password: form.control('password').value,
      );
      emit(state.copyWith(status: ApiStatus.success));
    } catch (e) {
      emit(state.copyWith(status: ApiStatus.error, errorMessage: e.toString()));
    }
  }
}
```

// Widget
class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final cubit = context.read<LoginCubit>();
    
    return BlocListener<LoginCubit, LoginState>(
      listener: (context, state) {
        if (state.status == ApiStatus.success) context.pop();
      },
      child: ReactiveForm(
        formGroup: cubit.form, // 3. Access form from cubit
        child: Column(
          children: [
            ReactiveTextField(formControlName: 'email'),
            ReactiveTextField(formControlName: 'password', obscureText: true),
            const SizedBox(height: 20),
            BlocBuilder<LoginCubit, LoginState>(
              builder: (context, state) {
                final isLoading = state.status == ApiStatus.loading;
                return ElevatedButton(
                  onPressed: isLoading ? null : cubit.login, // 4. Call cubit method
                  child: isLoading ? const CircularProgressIndicator() : const Text('Login'),
                );
              },
            ),
          ],
        ),
      ),
    );
  }
}
```

## Anti-patterns

- ❌ Emitting states from widgets directly
- ❌ Using `BlocBuilder` when only one field is needed (use `BlocSelector`)
- ❌ Giant monolithic blocs — split by feature
- ❌ Putting navigation logic inside blocs (use `BlocListener`)

## Resources

- https://bloclibrary.dev/getting-started
- https://bloclibrary.dev/bloc-concepts
- https://bloclibrary.dev/architecture
- https://pub.dev/packages/flutter_bloc
- https://pub.dev/packages/freezed
- https://docs.flutter.dev/data-and-backend/state-mgmt/options
