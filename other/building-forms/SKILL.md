---
name: flutter-building-forms
description: Builds Flutter forms with model-driven validation using reactive_forms. Use when creating login screens, data entry forms, or any multi-field user input.
tags: [flutter, forms, validation, reactive-forms, form-group, form-control, form-array]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Forms & Validation (Reactive Forms)

## Contents
- [Why Reactive Forms](#why-reactive-forms)
- [Core Concepts](#core-concepts)
- [Validators](#validators)
- [Reactive Widgets](#reactive-widgets)
- [Validation Messages](#validation-messages)
- [Workflow: Implementing a Reactive Form](#workflow-implementing-a-reactive-form)
- [Workflow: Integrating Forms with BLoC](#workflow-integrating-forms-with-bloc)
- [Examples](#examples)

## Why Reactive Forms

**Use `reactive_forms` instead of Flutter's built-in `Form`/`TextFormField`.** It provides:

- **Model-driven approach** — form logic (state, validation) is separated from the UI.
- **Two-way data binding** — `ReactiveTextField` auto-syncs with `FormControl` values.
- **Built-in validators** — `Validators.required`, `Validators.email`, `Validators.minLength`, etc.
- **Async validators** — server-side validation with debounce support.
- **No `TextEditingController` management** — no manual `dispose()` needed.
- **No `GlobalKey<FormState>`** — form state is managed by the `FormGroup` model.
- **FormArray** support — dynamic lists of inputs (add/remove fields at runtime).
- **Group-level validators** — cross-field validation (e.g., password confirmation).

## Core Concepts

| Concept | Description |
|---|---|
| **`FormControl<T>`** | Smallest unit — represents a single input field. Holds value, validation status, touched/dirty state. |
| **`FormGroup`** | Collection of `FormControl` objects. Represents the entire form. Tracks combined validation status. |
| **`FormArray<T>`** | Collection of controls for dynamic lists (e.g., list of phone numbers). Add/remove at runtime. |
| **`ReactiveForm`** | Widget that binds a `FormGroup` to the widget tree. |
| **`ReactiveFormConsumer`** | Rebuilds only the parts of UI that depend on form state (e.g., submit button). |
| **`fb` (FormBuilder)** | Syntactic sugar for concise `FormGroup`/`FormControl` creation. |

### FormControl States

| Property | Meaning |
|---|---|
| `control.valid` | All validators pass |
| `control.invalid` | At least one validator fails |
| `control.touched` | User has focused & unfocused the field |
| `control.dirty` | Value has been changed by the user |
| `control.pending` | Async validation is in progress |
| `control.disabled` | Control is exempt from validation |
| `control.errors` | `Map<String, dynamic>` of current errors |

## Validators

### Predefined Validators

#### FormControl validators
- `Validators.required` — value must not be null/empty
- `Validators.email` — valid email format
- `Validators.number` — numeric value
- `Validators.min(n)` / `Validators.max(n)` — numeric range
- `Validators.minLength(n)` / `Validators.maxLength(n)` — string length
- `Validators.pattern(regex)` — RegExp validation
- `Validators.creditCard` — credit card number
- `Validators.equals(value)` — exact value match
- `Validators.oneOf(list)` — value must be in the list
- `Validators.compose([...])` — all validators must pass (AND)
- `Validators.composeOR([...])` — at least one must pass (OR)

#### FormGroup validators
- `Validators.mustMatch('field1', 'field2')` — cross-field matching (e.g., password confirmation)
- `Validators.compare('field1', 'field2', CompareOption)` — compare two fields

### Custom Validators

Two approaches:

**1. Class-based (reusable):**

```dart
class PhoneValidator extends Validator<dynamic> {
  const PhoneValidator() : super();

  @override
  Map<String, dynamic>? validate(AbstractControl<dynamic> control) {
    final value = control.value as String?;
    if (value == null || value.isEmpty) return null; // Let required handle empty
    final isValid = RegExp(r'^\+?[\d\s-]{10,}$').hasMatch(value);
    return isValid ? null : {'phone': true};
  }
}
```

**2. Function-based (inline):**

```dart
FormControl<String>(
  validators: [
    Validators.delegate((control) {
      final value = control.value as String?;
      if (value != null && value.contains(' ')) {
        return {'noSpaces': true};
      }
      return null;
    }),
  ],
)
```

### Async Validators

For server-side validation (e.g., check if email is unique):

```dart
class UniqueEmailValidator extends AsyncValidator<dynamic> {
  final UserRepository _repo;
  UniqueEmailValidator(this._repo);

  @override
  Future<Map<String, dynamic>?> validate(
    AbstractControl<dynamic> control,
  ) async {
    final email = control.value as String?;
    if (email == null || email.isEmpty) return null;

    final isUnique = await _repo.checkEmailAvailable(email);
    return isUnique ? null : {'unique': true};
  }
}

// Usage with debounce:
FormControl<String>(
  validators: [Validators.required, Validators.email],
  asyncValidators: [UniqueEmailValidator(repo)],
  asyncValidatorsDebounceTime: 500, // ms
)
```

## Reactive Widgets

### Supported Widgets

| Widget | Binds To |
|---|---|
| `ReactiveTextField` | `FormControl<String>` |
| `ReactiveDropdownField` | `FormControl<T>` |
| `ReactiveCheckbox` | `FormControl<bool>` |
| `ReactiveSwitch` | `FormControl<bool>` |
| `ReactiveRadio<T>` | `FormControl<T>` |
| `ReactiveSlider` | `FormControl<double>` |
| `ReactiveCheckboxListTile` | `FormControl<bool>` |
| `ReactiveSwitchListTile` | `FormControl<bool>` |
| `ReactiveRadioListTile<T>` | `FormControl<T>` |
| `ReactiveDatePicker` | `FormControl<DateTime>` |
| `ReactiveTimePicker` | `FormControl<TimeOfDay>` |

### Key Differences from TextFormField

- **No `controller`** — `ReactiveTextField` manages its own internal controller via two-way binding.
- **No `validator` callback** — validation is defined on the `FormControl`.
- **No `onSaved`** — data is always available via `form.value`.
- **Has** `onChanged`, `onTap`, `onEditingComplete`, `onSubmitted`.

## Validation Messages

### Widget-Level

```dart
ReactiveTextField(
  formControlName: 'email',
  validationMessages: {
    ValidationMessage.required: (error) => 'Email is required',
    ValidationMessage.email: (error) => 'Enter a valid email address',
  },
)
```

### Global/Application Level

```dart
ReactiveFormConfig(
  validationMessages: {
    ValidationMessage.required: (error) => 'This field is required',
    ValidationMessage.email: (error) => 'Enter a valid email',
    ValidationMessage.minLength: (error) =>
        'Minimum ${(error as Map)['requiredLength']} characters',
  },
  child: MaterialApp(...),
)
```

**Lookup order:** Widget-level → Global-level.

### When Errors Appear

Validation messages show when a control is **invalid AND touched**. A control becomes touched when:
- User focuses then unfocuses the field
- `control.markAsTouched()` is called programmatically
- `form.markAllAsTouched()` marks all children

Override with `showErrors`:
```dart
ReactiveTextField(
  formControlName: 'email',
  showErrors: (control) => control.invalid && control.dirty,
)
```

## Workflow: Implementing a Reactive Form

- [ ] 1. Add `reactive_forms` to `pubspec.yaml`.
- [ ] 2. Define the `FormGroup` model with `FormControl` fields and validators.
- [ ] 3. Wrap the UI in a `ReactiveForm` widget, passing the `formGroup`.
- [ ] 4. Use `ReactiveTextField` (or other reactive widgets) with `formControlName`.
- [ ] 5. Add `validationMessages` to each reactive widget.
- [ ] 6. Use `ReactiveFormConsumer` to enable/disable the submit button based on `form.valid`.
- [ ] 7. On submit, read data from `form.value` (returns `Map<String, dynamic>`).
- [ ] 8. (Optional) Configure `ReactiveFormConfig` at app level for global error messages.

## Workflow: Integrating Forms with BLoC

Define the `FormGroup` in the widget (not in the Cubit). The Cubit handles business logic only.

- [ ] 1. Create the `FormGroup` in the widget's `State` or as a final field.
- [ ] 2. Use `ReactiveForm` + reactive widgets for the UI.
- [ ] 3. On valid submission, extract `form.value` and pass to the Cubit method.
- [ ] 4. Use `BlocListener` to react to Cubit state changes (success → navigate, error → show snackbar).
- [ ] 5. Use `BlocBuilder` for the submit button loading state.
- [ ] 6. Optionally pre-populate the form from Cubit state using `form.patchValue()`.

## Examples

### Login Form

```dart
class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final form = fb.group({
    'email': ['', Validators.required, Validators.email],
    'password': FormControl<String>(
      validators: [Validators.required, Validators.minLength(8)],
    ),
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: ReactiveForm(
          formGroup: form,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              ReactiveTextField(
                formControlName: 'email',
                keyboardType: TextInputType.emailAddress,
                textInputAction: TextInputAction.next,
                decoration: const InputDecoration(labelText: 'Email'),
                validationMessages: {
                  ValidationMessage.required: (_) => 'Email is required',
                  ValidationMessage.email: (_) => 'Enter a valid email',
                },
                onSubmitted: (_) => form.focus('password'),
              ),
              const SizedBox(height: 16),
              ReactiveTextField(
                formControlName: 'password',
                obscureText: true,
                decoration: const InputDecoration(labelText: 'Password'),
                validationMessages: {
                  ValidationMessage.required: (_) => 'Password is required',
                  ValidationMessage.minLength: (error) =>
                      'At least ${(error as Map)['requiredLength']} characters',
                },
              ),
              const SizedBox(height: 24),
              ReactiveFormConsumer(
                builder: (context, formGroup, child) {
                  return ElevatedButton(
                    onPressed: formGroup.valid ? _onSubmit : null,
                    child: const Text('Login'),
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }

  void _onSubmit() {
    final values = form.value;
    // Pass to cubit: context.read<AuthCubit>().login(
    //   email: values['email'] as String,
    //   password: values['password'] as String,
    // );
  }
}
```

### Registration Form with BLoC

```dart
class RegistrationPage extends StatefulWidget {
  const RegistrationPage({super.key});

  @override
  State<RegistrationPage> createState() => _RegistrationPageState();
}

class _RegistrationPageState extends State<RegistrationPage> {
  final form = FormGroup({
    'name': FormControl<String>(validators: [Validators.required]),
    'email': FormControl<String>(
      validators: [Validators.required, Validators.email],
    ),
    'phone': FormControl<String>(
      validators: [Validators.required, const PhoneValidator()],
    ),
    'password': FormControl<String>(
      validators: [Validators.required, Validators.minLength(8)],
    ),
    'confirmPassword': FormControl<String>(
      validators: [Validators.required],
    ),
  }, validators: [
    Validators.mustMatch('password', 'confirmPassword'),
  ]);

  @override
  Widget build(BuildContext context) {
    return BlocListener<RegistrationCubit, RegistrationState>(
      listener: (context, state) {
        if (state.status == ApiStatus.success) {
          context.go('/home');
        } else if (state.status == ApiStatus.error) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text(state.errorMessage ?? 'Failed')),
          );
        }
      },
      child: ReactiveForm(
        formGroup: form,
        child: Column(
          children: [
            ReactiveTextField(
              formControlName: 'name',
              decoration: const InputDecoration(labelText: 'Full Name'),
              validationMessages: {
                ValidationMessage.required: (_) => 'Name is required',
              },
            ),
            ReactiveTextField(
              formControlName: 'email',
              decoration: const InputDecoration(labelText: 'Email'),
              validationMessages: {
                ValidationMessage.required: (_) => 'Email is required',
                ValidationMessage.email: (_) => 'Enter a valid email',
              },
            ),
            ReactiveTextField(
              formControlName: 'phone',
              decoration: const InputDecoration(labelText: 'Phone'),
              keyboardType: TextInputType.phone,
              validationMessages: {
                ValidationMessage.required: (_) => 'Phone is required',
                'phone': (_) => 'Enter a valid phone number',
              },
            ),
            ReactiveTextField(
              formControlName: 'password',
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Password'),
              validationMessages: {
                ValidationMessage.required: (_) => 'Password is required',
                ValidationMessage.minLength: (e) =>
                    'At least ${(e as Map)['requiredLength']} characters',
              },
            ),
            ReactiveTextField(
              formControlName: 'confirmPassword',
              obscureText: true,
              decoration: const InputDecoration(labelText: 'Confirm Password'),
              validationMessages: {
                ValidationMessage.required: (_) => 'Please confirm password',
                ValidationMessage.mustMatch: (_) => 'Passwords do not match',
              },
            ),
            const SizedBox(height: 24),
            BlocBuilder<RegistrationCubit, RegistrationState>(
              builder: (context, state) {
                return ReactiveFormConsumer(
                  builder: (context, formGroup, child) {
                    final isLoading = state.status == ApiStatus.loading;
                    return ElevatedButton(
                      onPressed: formGroup.valid && !isLoading
                          ? () {
                              form.markAllAsTouched();
                              if (form.valid) {
                                context.read<RegistrationCubit>().register(
                                  name: form.control('name').value,
                                  email: form.control('email').value,
                                  phone: form.control('phone').value,
                                  password: form.control('password').value,
                                );
                              }
                            }
                          : null,
                      child: isLoading
                          ? const CircularProgressIndicator()
                          : const Text('Register'),
                    );
                  },
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

### Dynamic Form with FormArray

```dart
final form = FormGroup({
  'name': FormControl<String>(validators: [Validators.required]),
  'emails': FormArray<String>([
    FormControl<String>(validators: [Validators.email]),
  ]),
});

// Add a new email field dynamically
void addEmail() {
  final array = form.control('emails') as FormArray<String>;
  array.add(FormControl<String>(validators: [Validators.email]));
}

// Remove an email field
void removeEmail(int index) {
  final array = form.control('emails') as FormArray<String>;
  array.removeAt(index);
}

// In the widget tree:
ReactiveFormArray(
  formArrayName: 'emails',
  builder: (context, formArray, child) {
    return Column(
      children: formArray.controls.asMap().entries.map((entry) {
        final index = entry.key;
        return Row(
          children: [
            Expanded(
              child: ReactiveTextField(
                formControlName: index.toString(),
                decoration: InputDecoration(labelText: 'Email ${index + 1}'),
              ),
            ),
            IconButton(
              icon: const Icon(Icons.remove_circle),
              onPressed: () => removeEmail(index),
            ),
          ],
        );
      }).toList(),
    );
  },
)
```

### Pre-populating a Form from API Data

```dart
// In the widget, listen to cubit state and populate form:
BlocListener<ProfileCubit, ProfileState>(
  listener: (context, state) {
    if (state.status == ApiStatus.success && state.user != null) {
      form.patchValue({
        'name': state.user!.name,
        'email': state.user!.email,
        'phone': state.user!.phone,
      });
    }
  },
  child: ReactiveForm(
    formGroup: form,
    child: // ... reactive fields
  ),
)
```

### Focus Flow Between Fields

```dart
ReactiveTextField(
  formControlName: 'name',
  textInputAction: TextInputAction.next,
  onSubmitted: (_) => form.focus('email'),
),
ReactiveTextField(
  formControlName: 'email',
  textInputAction: TextInputAction.next,
  onSubmitted: (_) => form.focus('password'),
),
ReactiveTextField(
  formControlName: 'password',
  obscureText: true,
  textInputAction: TextInputAction.done,
),
```

### Disabling/Enabling Controls

```dart
// Disable a control (exempt from validation, excluded from form.value)
form.control('email').markAsDisabled();

// Re-enable
form.control('email').markAsEnabled();

// Get ALL values including disabled controls
final allValues = form.rawValue;
```

## Anti-patterns

- ❌ Using Flutter's `Form`/`TextFormField` instead of `reactive_forms` (loses model-driven benefits)
- ❌ Putting `FormGroup` definition inside `build()` (recreated every rebuild)
- ❌ Putting form validation logic inside the BLoC/Cubit (keep it in the `FormGroup`)
- ❌ Using `FormArray<FormGroup>` type annotation (use `FormArray()` or `FormArray<Map<String, dynamic>>()`)
- ❌ Calling `form.value` without checking `form.valid` first
- ❌ Forgetting `form.markAllAsTouched()` before submission (errors won't show)
- ❌ Creating `TextEditingController` manually (ReactiveTextField handles it internally)

## Resources

- https://pub.dev/packages/reactive_forms
- https://github.com/joanpablo/reactive_forms
- https://github.com/joanpablo/reactive_forms/wiki
- https://pub.dev/packages/reactive_forms_generator
- https://docs.flutter.dev/cookbook/forms/validation
