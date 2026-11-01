---
name: barbatos-valee-form
description: "Forms and validation with Barbatos.Wpf.AquariusValee - Form.FromModel over DataAnnotations or ad-hoc DefineField, Field<T>, HandleSubmit, DependsOn/PropertyRange cross-field and async rules, and aqv: markup (Valee.Field/PasswordField/Mask/Numeric, SafeMessageConverter). Use when a form needs required, email or phone checks, password confirmation, a username-taken check while typing, digits-only or masked input, a number clamped to a range, or a server error on a field - or when an error never shows, the submit button stays disabled, or a message stays in the old language. For View/ViewModel wiring use barbatos-aquarius-view. Vietnamese prompts too - form nhập liệu, validate, bắt buộc nhập, sai định dạng email, xác nhận mật khẩu, chỉ cho nhập số, thông báo lỗi, lỗi không đổi ngôn ngữ."
---

# Forms and validation with Barbatos.Wpf.AquariusValee

vee-validate's `useField`/`useForm` ported to WPF: `Field<T>` holds one value and its validation
state, `Form` aggregates fields and drives submit, `System.ComponentModel.DataAnnotations` is the
schema language, and errors reach the screen through `INotifyDataErrorInfo`. It is **not** a DI
feature (there is no `AddXxx`/`UseXxx` - a ViewModel constructs and owns its `Form`), it does not
localize anything itself, and it does not use WPF's `Binding.ValidationRules`.

Namespaces `Barbatos.Wpf.AquariusValee.Validation` (`Form`, `Field<T>`, metas, rule delegates),
`.Rules` (extra attributes) and `.Xaml` (`Valee` attached properties, converters) all map to
`xmlns:aqv="http://schemas.barbatos.co/aquariusvalee/2026/xaml"`.

## Sources of truth

- [README](../../../src/Barbatos.Wpf.AquariusValee/README.md) (concepts, rationale) and
  [API-REFERENCE](../../../src/Barbatos.Wpf.AquariusValee/API-REFERENCE.md) (signatures). The
  behaviour itself is in [`Validation/Field.cs`](../../../src/Barbatos.Wpf.AquariusValee/Validation/Field.cs)
  and [`Validation/Form.cs`](../../../src/Barbatos.Wpf.AquariusValee/Validation/Form.cs) - read them
  before trusting a doc sentence.
- Sample [`samples/Barbatos.Wpf.AquariusValee.Sample`](../../../samples/Barbatos.Wpf.AquariusValee.Sample):
  `Views/Login` (ad-hoc + `SetFieldError`), `Views/Signup` (both modes side by side),
  `Views/ProfileEdit` (schema + `Valee.Numeric` bounds from `[Range]`), `Views/CustomRules`
  (standalone fields, async rule, dynamic range, eagerly localized messages), `Views/Showcase`
  (`FieldTemplateSelector`, `Valee.Mask`, `[PropertyRange]`), `MainWindow.xaml.cs` (language switch).
- Scaffolds: `dotnet new aqv-form` ([item template](../../../templates/Barbatos.Wpf.AquariusValee/item-templates/valee-form),
  schema mode) and `dotnet new barbatos-wpf-app --IncludeValee true` (`SignUpViewModel.cs`, ad-hoc).
- [`tests/Barbatos.Wpf.AquariusValee.UnitTests`](../../../tests/Barbatos.Wpf.AquariusValee.UnitTests)
  pins it, one class per area (`FormTests`, `FieldTests`, `CrossFieldDependencyTests`, ...).
- [reference.md](reference.md) - read when choosing an attribute, wiring `Valee.Mask`/`Valee.Numeric`,
  building a template-driven form, or checking what `Form.FromModel` reads from a model.

## Choose the mode first - they are not interchangeable

| | Schema: `Form.FromModel(model)` | Ad-hoc: `form.DefineField(...)` | Standalone: `new Field<T>(...)` |
| --- | --- | --- | --- |
| Rules come from | attributes on the model's properties | attributes or delegates per call | same as ad-hoc |
| `[Compare]`, `[PropertyRange]`, `IValidatableObject` | work | do not | do not |
| `AddRule(ValidationAttribute)` | **silently ignored** | works | works |
| `AddRule(ValidationRule<T>)` / async overload | works | works | works |
| Values end up in | the model instance, live (`GetModel<TModel>()`) | `GetValues()` and the typed fields | the field |
| `HandleSubmit`, focus-first-invalid | yes | yes | no `Form`, so no |

Schema mode (adapted from `Views/Signup/SignupModel.cs` and `SignupViewModel.cs`):

```csharp
public sealed class SignupModel
{
    [Required(ErrorMessage = "Validation.Required")]
    [EmailAddress(ErrorMessage = "Validation.InvalidEmail")]
    public string Email { get; set; } = "";

    [Required, MinLength(8)]
    public string Password { get; set; } = "";

    [Required, Compare(nameof(Password))]
    public string ConfirmPassword { get; set; } = "";
}

SchemaForm = Form.FromModel(new SignupModel());
SchemaEmail = (Field<string>)SchemaForm.Fields["Email"];
```

Ad-hoc mode (from `Views/Login/LoginViewModel.cs`):

```csharp
public Form LoginForm { get; } = new();

Email = LoginForm.DefineField("Email", "",
    new RequiredAttribute { ErrorMessage = "Validation.Required" },
    new EmailAddressAttribute { ErrorMessage = "Validation.InvalidEmail" });
```

- `FromModel` makes a field of **every** public instance property with a getter and a setter of
  any accessibility, `private`/`init` included (indexers skipped), so non-input state on the model
  also counts toward `Meta.Valid` and `GetValues()`. Cast `Fields["Name"]` to `Field<TProperty>` with the property's exact type.
- Attributes that read a sibling property need a real model: ad-hoc fields validate with
  `new ValidationContext(this)` (the `Field<T>` itself), so `[Compare]` finds no sibling and fails
  every pass, and `[PropertyRange]` throws `InvalidOperationException`.
- `DefineField` overloads take no rules or one kind (`params ValidationAttribute[]`,
  `ValidationRule<T>[]` or `AsyncValidationRule<T>[]`); layer other kinds with `AddRule` (chainable).
  A `ValidationRule<T>` returns `null` for valid, otherwise the message.
- Every `Field<T>` constructor runs one **silent** pass with its rules, so `Meta.Valid` is right
  from the start without showing errors. `AddRule` rules miss that pass (`Meta.Valid` ignores them
  until the next one), and an async rule given to the constructor is called once, at construction.

## Submitting

```csharp
LogInCommand = LoginForm.HandleSubmit(async values =>
{
    await Task.Delay(TimeSpan.FromSeconds(1));
    if ((string)values["Password"]! != "correct-password")
    {
        LoginForm.SetFieldError("Password", "Login.InvalidCredentials");   // server-driven
        return;
    }
});
```

`HandleSubmit(onValid, onInvalid = null)` returns an `IAsyncRelayCommand` that, as vee-validate:
(1) touches **every** field, (2) sets `IsSubmitting` and increments `SubmitCount`, (3) runs
`ValidateAllAsync()` (forced pass on every field, then `IValidatableObject` for a schema form),
(4) calls `onValid(GetValues())`, or `onInvalid(GetValues(), GetErrors())` plus `SubmitInvalid`
with `GetFirstInvalidField()`, (5) clears `IsSubmitting` in a `finally` - even when `onValid` throws.

- **`CanExecute` is gated only on `!IsSubmitting`, never on `Meta.Valid`.** Submitting an empty
  form is what touches every field and surfaces every error. Do not bind the button's `IsEnabled`
  to validity; show progress with `IsSubmitting`.
- `Form.SetFieldError(name, message)` shows a server error immediately (`ArgumentException` for an
  unknown name; `null` clears). It marks the field validated, so the user's next edit re-runs the
  rules and replaces it.
- `aqv:Valee.Form` subscribes to `SubmitInvalid` and focuses + `BringIntoView()`s the control
  bound to the first invalid field. Without it, subscribe to the headless event yourself.
  `ValidateAllAsync()` alone never raises it.
- `ResetForm()` restores initial values and clears touched/validated/errors and `SubmitCount`;
  after a save, `field.Reset(savedValue)` rebases the initial value so `Dirty` tracks the saved one.

## Field and form state

`FieldMeta` has `Touched` (blur or submit only), `Validated` (a pass that writes errors has
run), `Valid` (written by every pass, default `true`), `Pending` (async rule in flight) and `Dirty`
(live comparison with the initial value); setters are `internal`. Full table and `FormMeta` aggregation
in [reference.md](reference.md#field-and-form-state-in-detail). Which pass may write visible errors
(the internal `ValidationWriteMode`):

| Pass | Writes `Errors`? |
| --- | --- |
| Constructor, `Reset` | never (silent) - updates `Meta.Valid` only |
| `HandleChange` / `Value` setter (`OnChange`), a `DependsOn` source changing | only if already `Validated` |
| `HandleBlur` (`OnBlur`), `ValidateAsync()`, submit, `RevalidateValidatedAsync()` | always |

So typing into a pristine field shows nothing until the first blur or submit; afterwards errors
update per keystroke. That is the intended vee-validate behaviour, not a bug.

- Triggers per field: `Email.Triggers = ValidateTrigger.OnBlur;` (`None`, `OnChange`, `OnBlur`,
  `Default = OnChange | OnBlur`). `HandleBlur()` always sets `Touched`.
- Every failing rule adds its message (no bailing), except that the BCL runs `[Required]` first and
  short-circuits the other attributes: `[Required, MinLength(3)]` on `""` reports one message.
  Delegate rules still run on the empty value.
- `Valid` defaults to `true`; pair it with `Dirty`/`Touched` before any "looks good" UI.

## Cross-field validation - three mechanisms

**Ad-hoc: `DependsOn` + a closure** (`Views/Signup/SignupViewModel.cs`):

```csharp
AdHocConfirmPassword.AddRule(value => value == AdHocPassword.Value ? null : "Signup.PasswordMismatch");
AdHocConfirmPassword.DependsOn(AdHocPassword);
```

Call it once per source for bounds driven by other fields (`Views/CustomRules`: two rules reading
`MinPrice.Value`/`MaxPrice.Value`, then `Price.DependsOn(MinPrice)` and `Price.DependsOn(MaxPrice)`);
`[Range]` cannot, its arguments are constants. `DependsOn` returns an `IDisposable`, re-validates
validated-only (no error appears on an untouched field), and uses `Watch.On`, which reacts only to
the source's value - never `Errors`/`Meta` - so mutual dependencies cannot loop.

**Schema, one sibling: `[Compare(nameof(Password))]`.** Right verdict whenever the confirm field
validates, but **no automatic re-validation** when `Password` changes - add
`ConfirmPassword.DependsOn(Password)` (the `aqv-form` template does), or fixing the password leaves
a stale "don't match" error.

**Schema, dynamic bounds: `[PropertyRange(nameof(MinPrice), nameof(MaxPrice))]`.** It implements
`IDependsOnProperties`, so `FromModel` wires `DependsOn` itself once all fields exist (any custom
attribute can opt in the same way). The message is `ErrorMessage` formatted with display name, min
and max (`"The {0} field must be between {1} and {2}."`); a placeholder-free key works like any
key but loses the live bounds. Localized text **with** bounds needs a resx resource
(`ErrorMessageResourceType`/`ErrorMessageResourceName` - the resource string is the template,
`RulesTests`) or ad-hoc `DependsOn` when the text must come from an app localizer.

**Model-level: `IValidatableObject`** on a schema model runs only in `ValidateAllAsync`/submit (and
`RevalidateValidatedAsync`), never per keystroke. Each result must name its members -
`new ValidationResult("You must accept the terms.", [nameof(AcceptedTerms)])` - and the message is
appended to each named field; a result with no member names, or naming a non-field, is dropped.
It runs whether or not the properties' own attributes pass (an empty `[Required]` field does not
hold it back), after any class-level `ValidationAttribute` (`[CustomValidation]` on the class) -
a failing class-level attribute skips `Validate`, as in the BCL. `Form` does not call
`Validator.TryValidateObject`: its `validateAllProperties: false` still re-checks every
`[Required]` and stops there (`FormFromModelTests`). So `Validate` sees values its property
attributes reject - `""`, `null`, out of range - and must not assume they passed: skip a
comparison whose operand is empty rather than dereference it, or the submit throws.

## Async rules

Adapted from `Views/CustomRules/CustomRulesViewModel.cs`, plus the optional `try`/`catch`
explained below:

```csharp
Username.AddRule(async (value, cancellationToken) =>
{
    if (string.IsNullOrWhiteSpace(value))
        return null;                                   // rules run in order and never bail - guard

    try
    {
        var available = await availabilityService.IsAvailableAsync(value, cancellationToken);
        return available ? null : "Validation.UsernameTaken";
    }
    catch (HttpRequestException)
    {
        return "Validation.UsernameCheckFailed";      // a failure shown as a message - see below
    }
});
```

- **Forward the token.** Every new pass cancels the previous pass's token and the latest pass wins
  (`AsyncValidationRaceTests`); forwarding turns a superseded call into cancelled work, not just a
  discarded result. There is no debounce: start the rule with
  `await Task.Delay(300, cancellationToken)` if each keystroke should not hit the server.
- **A throwing rule is safe, but it is not a message** (`FieldRuleExceptionTests`). The pass
  writes nothing (`Errors`/`Meta.Valid` keep the previous pass's values) and `Meta.Pending` is
  lowered. The exception propagates from `ValidateAsync`/`ValidateAllAsync`/
  `RevalidateValidatedAsync` and the `HandleSubmit` command (`IsSubmitting` still clears, neither
  callback runs); a pass nobody awaits - typing, blur, `DependsOn`, the silent constructor/`Reset`
  pass - rethrows it on the starting UI thread's `Dispatcher`, i.e. `Application.DispatcherUnhandledException`
  (a pass started off a UI thread - a pool thread, or one neither STA nor inside a dispatcher
  operation - leaves it on the task, for `UnobservedTaskException`).
  Catch inside the rule, as above, when a failed check should read as an error under the field.
- **Only Valee's own cancellation is swallowed**: a superseded pass ends quietly whatever it
  throws. An `OperationCanceledException` in a live pass - an `HttpClient` timeout's
  `TaskCanceledException` - is a failure like any other, so do not filter on the exception type
  to tell the two apart; `cancellationToken.IsCancellationRequested` is the supersession signal.
- Show progress with `{Binding Username.Meta.Pending}` or `Form.Meta.Pending`. Add the rule with
  `AddRule` after construction, as the sample does, so the constructor's silent pass never calls
  the service (a later `Reset`/`ResetForm` silent pass still does).
- `Field<T>.Dispose()` cancels in-flight work, clears `Pending` and stops every `DependsOn`;
  `Form.Dispose()` disposes all fields. Dispose when the owning ViewModel goes away mid-check.

## XAML

```xml
<StackPanel aqv:Valee.Form="{Binding LoginForm}">
    <TextBox aqv:Valee.Field="{Binding Email}" />          <!-- or aqv:Valee.For="Email" -->
    <TextBlock Text="{Binding Email.ErrorMessage}" Foreground="Red" />
    <PasswordBox aqv:Valee.PasswordField="{Binding Password}" />
    <TextBlock Text="{Binding Password.ErrorMessage}" Foreground="Red" />
    <Button Content="Log in" Command="{Binding LogInCommand}" />
</StackPanel>
```

- **`Valee.Field`** (value: any `IField`) binds `TextBox.Text`, `ToggleButton.IsChecked`,
  `Selector.SelectedItem` or `RangeBase.Value` TwoWay with `UpdateSourceTrigger=PropertyChanged`
  (WPF's `TextBox.Text` default is `LostFocus`), and wires `LostFocus` to `HandleBlur`. It throws
  `InvalidOperationException` on a `PasswordBox`, an unsupported element, or a non-`IField` value.
  Inside a `DataTemplate` whose item is the field, use `aqv:Valee.Field="{Binding}"`.
- **`Valee.PasswordField`** (`PasswordBox` only, value `Field<string>`) pushes `PasswordChanged`
  into the field and never binds `Password`. So: no native adorner - always add an error
  `TextBlock` - and it is one-way: `Reset`, `ResetForm` and `SetFieldValue` do not clear the box.
- **`Valee.Form`** on a container enables `Valee.For` and focus-first-invalid, and suppresses the
  native adorner on that element only (`Form` is itself `INotifyDataErrorInfo`; the whole panel
  would turn red). `Validation.HasError` there still works for a form-level banner.
- **`Valee.For="Email"`** finds the ancestor `Valee.Form` by a visual-tree walk at `Loaded`, with
  no retry: the `Form` must be non-null by then (build it in the ViewModel constructor). A missing form or
  field name is an `InvalidOperationException` posted to the dispatcher. `Popup` content has no
  visual path to the panel - use `Valee.Field` there.
- Error display is native: a `TextBlock` on `ErrorMessage` plus WPF's red adorner from
  `Field<T>`'s `INotifyDataErrorInfo`. No error control ships; do not write one.

Input helpers (`TextBox` only; details in [reference.md](reference.md)):
`aqv:Valee.Mask=">AAA-0000"` shapes typing but does not validate - pair it with `PatternAttribute`.
A positional mask fits fixed layouts only; Showcase hand-rolls international phone input instead
(`Views/Showcase/InputMask.cs`). `aqv:Valee.Numeric="Integer"` (or `Decimal`) filters keystrokes
and clamps **on `LostFocus` only** to `aqv:Valee.Minimum`/`aqv:Valee.Maximum`, else to a numeric
`[Range]` on the field when bound through `Valee.Field`/`Valee.For` - keep the `[Range]`, clamping
corrects but does not validate. `FieldTemplateSelector` renders a whole form from
`ItemsSource="{Binding Form.Fields.Values}"`.

## Localized messages

Valee takes no localization dependency; literal messages are fine. To localize, pick per message:

| Message | Store as | After a language switch |
| --- | --- | --- |
| fixed text | a lookup key in `ErrorMessage`, `SetFieldError` or a rule's return value | resolved by a converter when the binding re-reads |
| text with runtime values (`{0} is taken`, "at least {MinPrice}") | text resolved eagerly in the rule | `await form.RevalidateValidatedAsync()` |

BCL default messages ("The {0} field is required.") are English whatever the culture - .NET ships
no satellite resources for DataAnnotations - so every attribute a user can trip needs a key or a
resource of its own. The resx route (`ErrorMessageResourceType`/`ErrorMessageResourceName`) works
on Valee's `Rules` attributes as on BCL ones; never combine it with `ErrorMessage` (the BCL throws).

Wrap the localizing converter in `SafeMessageConverter` (its XAML content property) so an unknown
key or literal prose shows as written instead of blank - it returns the input when the inner
converter returns null/empty or throws:

```xml
<aqv:SafeMessageConverter x:Key="LocalizeConverter">
    <i18n:LocalizeConverter />
</aqv:SafeMessageConverter>
<TextBlock Text="{Binding Email.ErrorMessage, Converter={StaticResource LocalizeConverter}}" />
```

**"The error stays in the old language after switching"** has three causes:

1. **Eager text.** A rule that returned resolved text (and BCL default messages, which are
   formatted when the rule runs) captured the old language. Call `RevalidateValidatedAsync()` after
   changing culture: it re-runs only `Meta.Validated` fields (no new errors on pristine ones) and
   re-applies `IValidatableObject` messages for them. For standalone fields, call `ValidateAsync()`
   on each `Meta.Validated` field (`CustomRulesViewModel.RefreshLocalizedMessagesAsync`).
2. **Key + converter, but the binding never re-read.** A converter runs when `ErrorMessage`
   changes, and a culture switch does not change it. The sample rebuilds each tab's View against
   the same ViewModel (`MainWindow.xaml.cs`), so form state survives; anything that makes the
   binding re-evaluate works.
3. **A key spliced into another message.** `{0}` is formatted with the raw `[Display(Name)]` when the
   rule runs, so a key there renders as the key. Keep key messages placeholder-free (the Showcase
   `[PropertyRange]` message drops `{0}` for this reason).

## Rules: prefer the BCL

BCL `ValidationAttribute` first, then `Barbatos.Wpf.AquariusValee.Rules`, then
`[CustomValidation]`/`IValidatableObject` (schema) or a `ValidationRule<T>` (ad-hoc). Valee adds
attributes only for confirmed BCL gaps - `Pattern` (`RegexOptions`, anchored, timeout fails),
`PropertyRange`, `Alpha*` (`AsciiOnly`), `Digits`/`NumericString`/`IntegerString`, and loose
`OneOf`/`NotOneOf` (prefer the strict BCL `AllowedValues`/`DeniedValues`). No `ExactLength`: use
`[Length(n, n)]`. Semantics, including which skip `""` or non-strings, are in
[reference.md](reference.md#attribute-catalogue). Optional `[Url]`/`[EmailAddress]`/`[Phone]`
strings must be `string?` defaulting to `null`: those accept `null` but fail `""`.

## Hard rules

- **Create and mutate forms on the UI thread.** `Field<T>` and `Form` are not thread-safe (a
  worker's change races the UI's keystrokes over the same pass state), raise every notification on
  the calling thread, and a pass started off the UI thread leaves a rule's exception on its task
  instead of `DispatcherUnhandledException`. Build the `Form` in the ViewModel constructor and
  never touch a field or form after `ConfigureAwait(false)` in `onValid`. `Form.Meta` bindings no
  longer freeze when a worker does touch one: Aquarius `NextTick`, which `FormMeta` coalesces its
  notification through, posts from a worker to `Application.Current`'s dispatcher (earlier
  versions posted to the worker's own, which nothing pumps). With no `Application` - a test or
  console host - it still falls back to that worker's dispatcher.
- Never gate submit on `Meta.Valid`; never `AddRule(attribute)` on a `FromModel` field; always
  `DependsOn` a `[Compare]` source; build the `Form` before the View loads; never put
  `[DataType(...)]` beside `[Phone]`/`[CreditCard]`/`[EmailAddress]`/`[Url]`/`[EnumDataType]`
  (they are `DataTypeAttribute`s already; `FromModel` throws a `TargetInvocationException` wrapping
  `AmbiguousMatchException`).
- Lifetimes: `DependsOn` subscribes to the source, so a dependent field stays reachable from a
  longer-lived source (a store, a singleton ViewModel) until disposed. `Valee` remembers the last
  control bound to each field (for focus-first-invalid) only through a weak reference, so a `Form`
  that outlives its View does not keep the closed View alive (`ValeeFieldLeakTests`).

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| Nothing shows while typing in a fresh field | validated-only passes before the first blur/submit | by design; it appears after blur or submit |
| No error even after blur | plain `{Binding X.Value}` (no blur hook, `LostFocus` timing), `Triggers` without `OnBlur`, or a rule that throws (the pass writes nothing) | use `Valee.Field`/`Valee.For`; check `Triggers`; catch inside the rule and return a message |
| Error area blank though `Meta.Valid` is false | field not validated yet (silent pass), or a localizing converter returned null for an unknown key | blur/submit; wrap the converter in `SafeMessageConverter` |
| Raw key such as `Validation.Required` on screen | key missing from the locale files, or no converter on that binding | register the key / add the converter |
| Message stays in the old language | eager text, an unrefreshed binding, or a key in `{0}` | see [Localized messages](#localized-messages) |
| Submit button disabled on an empty form | `IsEnabled` bound to `Meta.Valid` | rely on `HandleSubmit`'s `CanExecute` |
| "Passwords don't match" persists after fixing the password | `[Compare]` not wired for re-validation | `ConfirmPassword.DependsOn(Password)` |
| `[Compare]` in `DefineField` always fails; `AddRule(attribute)` on a schema field does nothing | each works only in the other mode | `DependsOn` + closure; put the attribute on the model |
| Optional URL/email field invalid from the start, or again after clearing it | `""` default / the box writes `""` when cleared | `string?` with `null` default / a rule that returns `null` for `""` |
| `IValidatableObject` message never appears | no member names, a failing class-level attribute, or only per-keystroke validation ran | name members; it runs on submit/`ValidateAllAsync` once class-level attributes pass |
| Unhandled exception (`DispatcherUnhandledException`) while typing or on blur; submit throws | a rule threw or timed out - rethrown from a pass nobody awaits, propagated from an awaited one | catch inside the rule and return a message |
| "checking..." never clears, `Form.Meta.Pending` stuck | a rule that never completes (ignores the token and awaits forever) | forward the token; give the call a timeout |
| `Form.Meta` never raises `PropertyChanged` in a test or a host with no `Application` | the form was mutated on a worker thread: with no `Application.Current`, `NextTick` falls back to that thread's own dispatcher, which nothing pumps | mutate on the UI (STA) thread and pump its dispatcher |
| Unhandled `InvalidOperationException` mentioning `Valee.For` | `Form` null at `Loaded`, misspelt field name, or element inside a `Popup` | construct the form in the constructor; fix the name; use `Valee.Field` |
| `PasswordBox` keeps its dots after `ResetForm()` | `Valee.PasswordField` is one-way | clear `PasswordBox.Password` in the View |
| `TargetInvocationException` (inner `AmbiguousMatchException`) / `InvalidOperationException` from `Form.FromModel` | two `DataTypeAttribute`s on a property / an `IDependsOnProperties` name that does not exist | drop the explicit `[DataType]` / use `nameof` |
| Numeric box ignores `[Range]` | box bound without `Valee.Field`/`Valee.For`, a non-numeric `[Range]` overload, or the `RangeAttribute` added with `AddRule` (only the constructor/`DefineField` copies its bounds) | bind with `Valee.Field`; pass the `[Range]` to `DefineField` or set `Valee.Minimum`/`Valee.Maximum` |
| Letters typed into a number box: no `ErrorMessage`, `Value` keeps the old number | text the binding cannot convert never reaches a `Field<int>`, so no rule runs | `Valee.Numeric`, or a `Field<string>` with `[IntegerString]` parsed on submit |
| Numeric box rejects `,` or the value stops updating | separator comes from `FrameworkElement.Language` (default `en-US`) | set `Language` on the box or window |
| Service called with the initial value at startup | async rule passed to the constructor runs in the silent pass | `AddRule` after construction and guard empty input |

## Checklist: adding a form to an app

1. Pick the mode; build the `Form` and typed `Field<T>` properties in the ViewModel constructor on
   the UI thread (`dotnet new aqv-form` scaffolds the schema shape).
2. Rules: BCL first, Valee `Rules` second, delegates last; `string?` for optional formatted strings.
3. Cross-field: `DependsOn`, `[Compare]` + `DependsOn`, or `[PropertyRange]`; name members in
   `IValidatableObject` results. Async rules forward the token, guard empty input, and catch
   the failures that should show as a message.
4. `HandleSubmit`, server errors via `SetFieldError`, no validity gate on the button.
5. View: `aqv:Valee.Form` on the container, `Valee.Field`/`For`/`PasswordField`, an error
   `TextBlock` per field (mandatory for `PasswordBox`), `SafeMessageConverter` when localized.
6. Language switch: rebind key-based messages, `RevalidateValidatedAsync()` for eager text.
7. Dispose forms that die while async checks or cross-lifetime `DependsOn` are live.

## Changing Barbatos.Wpf.AquariusValee itself

Load `barbatos-package-authoring` too. A new rule attribute goes in `Rules/` (namespace
`Barbatos.Wpf.AquariusValee.Rules`, already mapped to `aqv:`) and follows the shipped ones:
`public sealed class XxxAttribute : ValidationAttribute`,
`[AttributeUsage(AttributeTargets.Property | AttributeTargets.Field | AttributeTargets.Parameter, AllowMultiple = false)]`,
the default message passed to the base constructor (`: base("The {0} field ...")` - never
assigned to `ErrorMessage`, which would make the BCL reject `ErrorMessageResourceName`), and
`IsValid` returning `true` for `null` (and normally for `""`) so `[Required]` alone owns emptiness. A cross-field rule
implements `IDependsOnProperties`. Add its row to [reference.md](reference.md#valee-rules-attributes),
tests for null, empty, non-string and failing values, and README/API-REFERENCE entries
(`barbatos-docs-sync`). A new attached property follows the control rules in
`.claude/rules/library-code.md`.

## Related skills

- `barbatos-aquarius-view` - the View/ViewModel the form lives in (`aq:Setup.Enable`, reactivity).
- `barbatos-aquarius-router` - a form screen as a route, or a leave guard on unsaved `Meta.Dirty`.
- `barbatos-wpf-testing` - STA helpers and per-TFM runs for Valee tests.
- `barbatos-package-authoring`, `barbatos-docs-sync`, `barbatos-templates` - changing Valee itself.
  It depends on Aquarius (`Watch.On`, `NextTick`) and `CommunityToolkit.Mvvm`, never on Core; a
  change also updates README (and its menu), API-REFERENCE, the sample and both templates. Test one
  TFM at a time: `dotnet test tests/Barbatos.Wpf.AquariusValee.UnitTests -f net8.0-windows`.
