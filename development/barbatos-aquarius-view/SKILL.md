---
name: barbatos-aquarius-view
description: "Views and ViewModels with Barbatos.Wpf.Aquarius (aq: XAML) - Ref/Computed/Watch, aq:Setup ViewModel resolution, aq:Lifecycle hooks (IOnMounted, IOnMountedAsync), Directives.Model/Show/Event, If/Expr, Teleport, Transition, Provide/Inject, Suspense, Slots, Component/KeepAlive. Use when building or debugging a screen with aq:, or when DataContext is null, the ViewModel is never found, OnMounted never fires or fires twice, a value should update by itself, a popup is clipped, state is lost when switching tabs, or content should fade in. For navigation use barbatos-aquarius-router; for validation barbatos-valee-form. Vietnamese prompts too - màn hình mới, DataContext bị null, binding không tự cập nhật, chạy khi màn hình hiện ra, hiệu ứng hiện dần, giữ trạng thái khi chuyển tab, popup bị cắt."
---

# Barbatos.Wpf.Aquarius - Views and ViewModels

Vue 3's Composition API surface (ref/computed/watch, lifecycle hooks, v-model/v-show/v-if/v-on,
Teleport, Transition, provide/inject, Suspense, slots, `<component :is>` + KeepAlive) ported to
plain WPF as thin sugar over CommunityToolkit.Mvvm and WPF's own binding engine - never a
replacement for either. One xmlns, `xmlns:aq="http://schemas.barbatos.co/aquarius/2026/xaml"`,
reaches all four CLR namespaces (`Barbatos.Wpf.Aquarius.Reactivity`, `.Composition`, `.Xaml`,
`.Animation`). Aquarius does not depend on Core and works in any WPF app. Not here: navigation
(`barbatos-aquarius-router`), validation (`barbatos-valee-form`), state shared across screens
(`barbatos-apsu-store`).

## Sources of truth

- Docs: [README](../../../src/Barbatos.Wpf.Aquarius/README.md) -
  [Reactivity](../../../src/Barbatos.Wpf.Aquarius/README.md#reactivity),
  [Lifecycle Hooks](../../../src/Barbatos.Wpf.Aquarius/README.md#lifecycle-hooks),
  [Setup](../../../src/Barbatos.Wpf.Aquarius/README.md#setup),
  [Directives](../../../src/Barbatos.Wpf.Aquarius/README.md#directives),
  [Expr](../../../src/Barbatos.Wpf.Aquarius/README.md#expr---conditional-expressions) - and
  [API-REFERENCE.md](../../../src/Barbatos.Wpf.Aquarius/API-REFERENCE.md).
- Code: `src/Barbatos.Wpf.Aquarius/` - `Reactivity/`, `Composition/` (`Setup.cs`, `Lifecycle.cs`,
  `AquariusServiceCollectionExtensions.cs`), `Xaml/` (`Directives.*.cs`, `Expr*.cs`), `Animation/`.
- Sample: `samples/Barbatos.Wpf.Aquarius.Sample/` - one self-contained View/ViewModel pair per tab.
  `WpfProgram.cs` (`AddAquarius`/`UseAquarius`), `MainWindow.xaml` (parent-bound tab shell),
  `ReactivityDemoViewModel.cs`, `LifecycleDemoView.xaml` + `LifecycleDemoViewModel.cs`,
  `DirectivesDemoView.xaml` + `FocusDirective.cs`, `ExprDemoView.xaml`. Self-sufficient View:
  `samples/Barbatos.Wpf.Samples.Shared/InfoCardView.xaml`; where the naming convention stops:
  `samples/Barbatos.Wpf.Samples.Shared/CrossAssembly/AccountSummaryPresenter.cs`.
- Tests that pin behaviour (`tests/Barbatos.Wpf.Aquarius.UnitTests/`): `SetupTests.cs`,
  `AquariusDependencyInjectionTests.cs`, `LifecycleTests.cs`, `AsyncLifecycleHookTests.cs`,
  `LifecycleLeakTests.cs`, `WatchTests.cs`, `ComputedTests.cs`, `Directives*Tests.cs`,
  `DirectiveExtensibilityTests.cs`, `IfControlTests.cs`, `ExprXamlTests.cs`, `SuspenseTests.cs`.
- [patterns.md](patterns.md) - read when the task involves Teleport (overlays, toolbars, dockable
  panels), Transition/TransitionGroup, Provide/Inject, Slots, or Component + KeepAlive. It holds
  the verified hook sequences, the keep-alive table and the per-pattern pitfalls.

## First: do not reinvent what WPF already has

| Want | Use |
| --- | --- |
| One-way / two-way binding | `{Binding}` - no directive needed |
| Repeat a collection | `ItemsControl` + `DataTemplate` |
| Per-item template supplied by the consumer ("scoped slot") | `ItemsControl.ItemTemplate` - the item *is* the slot props |
| One content area | `ContentControl.Content` |
| Error display for `INotifyDataErrorInfo` | WPF's validation adorner (forms: `barbatos-valee-form`) |
| A condition beyond `Not`/`IsNull`/`IsEqualTo`/a short `Expr` | a `Computed<T>` in the ViewModel |
| State several screens share | an Apsu store (`barbatos-apsu-store`), not `Provide` |

## Wiring a View to its ViewModel - `Setup`

```xml
<UserControl aq:Setup.Enable="True" ... />                            <!-- by naming convention -->
<UserControl aq:Setup.ViewModel="{x:Type vm:SomeViewModel}" ... />   <!-- explicit; wins over Enable -->
```

The default convention (`Setup.Resolver`) works on the **namespace-qualified** name: it strips a
trailing `View` from `Type.FullName` and appends `ViewModel`, so `MyApp.Features.DashboardView`
finds only `MyApp.Features.DashboardViewModel`. It checks the View's assembly first, then every
assembly already loaded. A ViewModel in another assembly is found; one in **another namespace**
(`...Views.X` / `...ViewModels.XViewModel`), with another suffix (`Presenter`), or for a View
whose name does not end in `View` (`MainWindow`, `SettingsPage`) is not - and by default that
failure is silent: `DataContext` stays `null` (or inherited). Fix with `aq:Setup.ViewModel`, or
replace the convention app-wide and make misses loud during development:

```csharp
builder.Services.AddAquarius(options =>
{
    options.ThrowOnUnresolvedViewModels = true;      // -> Setup.ThrowOnUnresolved
    options.ThrowOnUnresolvedExprIdentifiers = true; // -> Expr.ThrowOnUnresolvedIdentifiers
    options.ViewModelResolver = viewType =>          // -> Setup.Resolver (Views -> ViewModels swap)
        viewType.FullName is { } name && name.EndsWith("View", StringComparison.Ordinal)
            ? viewType.Assembly.GetType(name.Replace(".Views.", ".ViewModels.") + "Model")
            : null;
});

var app = builder.Build();
app.Services.UseAquarius();   // Setup.ServiceProvider = container, then applies the options
```

Without Core, call the same two methods on your own `ServiceCollection`/provider, or just assign
`Setup.ServiceProvider`. Rules:

- **Instance source** is `Setup.Resolve(type)`: `Setup.ServiceProvider?.GetService(type)`, else
  `Activator.CreateInstance(type)` - so an unregistered ViewModel needs a public parameterless
  constructor. Register one only when it has constructor dependencies, normally transient (a
  singleton is one instance shared by every copy of that View). `Component` and AquariusRouter's
  `Router` build Views through the same method; never add a second construction path.
- **Resolution happens once, on `Initialized`**, not `Loaded`, so `Lifecycle` always sees the
  resolved `DataContext`. Set it in the View's own XAML root; setting it from code on an element
  that already raised `Initialized` does nothing.
- **Never combine `aq:Setup` on a View with a `DataContext` set at the usage site**
  (`<local:FooView DataContext="{Binding Foo}" />`): one silently replaces the other
  (`InfoCardView.xaml` documents it). Choose per View: self-sufficient (Setup) or parent-bound (no
  Setup, like every tab View in the sample's `MainWindow.xaml`).
- `UseAquarius()` writes both throw switches from the options whenever the container resolves
  `IOptions<AquariusOptions>` - after `AddAquarius`, or after anything else called `AddOptions()`
  (`AddLogging`, any Core `ConfigureXxx`) - overwriting earlier static assignments. Configure them
  in `AddAquarius`, or assign the statics after `UseAquarius()`.
- `AddAquarius` does **not** read configuration, despite `AquariusOptions.SectionName`
  (`"Barbatos:Aquarius"`). To honour appsettings, bind it yourself after `AddAquarius` (the later
  registration wins):
  `builder.Services.AddOptions<AquariusOptions>().Bind(builder.Configuration.GetSection(AquariusOptions.SectionName));`
- Only the default resolver caches per View type; a custom one runs for every View instance.

## Reactivity

Adapted from `ReactivityDemoViewModel.cs`:

```csharp
public Ref<int> Count { get; } = new(0);                // using Barbatos.Wpf.Aquarius.Reactivity;
public Computed<int> Doubled { get; }
public Computed<string> FullName { get; }

[ObservableProperty] private string _firstName = "Ada";
[ObservableProperty] private string _lastName = "Lovelace";

public ReactivityDemoViewModel(Action<string> log)
{
    Doubled = Computed<int>.From(() => Count.Value * 2, Count);
    FullName = Computed<string>.From(
        () => $"{FirstName} {LastName}",
        fullName =>                                   // writable: the setter mutates a dependency
        {
            var parts = fullName.Split(' ', 2);
            FirstName = parts.Length > 0 ? parts[0] : "";
            LastName = parts.Length > 1 ? parts[1] : "";
        },
        this);                                        // `this`: the getter reads [ObservableProperty]s
    Watch.On(Count, (newValue, oldValue) => log($"Count changed {oldValue} -> {newValue}"));
}
```

- Bind through `.Value` (`{Binding Count.Value}`); there is deliberately no implicit conversion.
  `Ref<T>.Value` raises `PropertyChanged` only when the value changes by default equality, so
  mutating a reference value in place (`Items.Value.Add(x)`) notifies nothing.
- **`Computed<T>` dependencies are explicit** - C# has no proxy tracking. Any `PropertyChanged` from
  a listed dependency re-runs the getter (no property-name filter); `Value` notifies only when the
  result changed. The getter runs once inside `From`, so everything it reads must already be
  initialized. Assigning a read-only `Computed<T>` throws `InvalidOperationException`.
- **`Watch.On` takes a `Ref<T>` only** - options `immediate`, `once`, `deep` (also reacts to
  the value's own `CollectionChanged` when it is `INotifyCollectionChanged`), `flush`. The
  overload whose callback has a third parameter registers a cleanup that runs before the next
  invocation and on `Dispose()` (cancel stale async work). To watch an `[ObservableProperty]`,
  use the generated `partial void OnXxxChanged` or `Watch.Effect(effect, this)`. `Watch.Effect`
  always runs once immediately, then on every dependency change.
- **`WatchFlush.Post`** coalesces a burst of changes into one callback that gets the newest value
  and the value from before the burst (`0 -> 1 -> 2 -> 3` is one `(3, 0)`); a burst that ends where
  it started still calls back, with equal arguments.
- **Lifetime**: every dependency's `PropertyChanged` holds the `Computed`/watcher and, through the
  closure, the ViewModel. When a source outlives the ViewModel (a singleton store, an app-wide
  `Ref`), `Dispose()` each `Computed<T>` and `Watch` handle in `IOnUnmounted`, or the ViewModel
  leaks. Sources owned by the same ViewModel need nothing.
- **`NextTick.Run`/`RunAsync` post at `DispatcherPriority.Background`** to the calling thread's
  dispatcher when it is a UI thread (inside a dispatcher operation, or a non-pool STA thread);
  called from a worker they post to the watcher's/element's UI thread, else
  `Application.Current`'s. So `WatchFlush.Post` callbacks and `IOnBeforeUpdate`/`IOnUpdated` run
  on the UI thread even when the `PropertyChanged` behind them was raised on a pool thread
  (`IOnBeforeUpdate` then fires once the UI thread gets to it, not inside the worker's setter).
  Only an app with no `Application` at all, calling from a worker, still queues onto that worker's
  never-pumped dispatcher. Work for a UI thread whose dispatcher has shut down (a window thread
  closing) is dropped, never moved to another thread.
- Use `[ObservableProperty]` for plain state, `Computed<T>` for derived values, `Ref<T>` when the
  value itself is passed around (`Watch.On`, `Component.Is`, `Provide.Value`). They coexist.

## Lifecycle hooks

```xml
<UserControl aq:Lifecycle.Enable="True" ... />
```

```csharp
public sealed partial class LifecycleDemoViewModel : ObservableObject,
    IOnBeforeMount, IOnMounted, IOnUpdated, IOnUnmounted, IOnMountedAsync
```

Eleven sync interfaces in `Barbatos.Wpf.Aquarius.Composition` - `IOnBeforeCreate`, `IOnCreated`,
`IOnBeforeMount`, `IOnMounted`, `IOnBeforeUpdate`, `IOnUpdated`, `IOnBeforeUnmount`,
`IOnUnmounted`, `IOnActivated`, `IOnDeactivated`, `IOnErrorCaptured`
(`bool OnErrorCaptured(Exception)`, `true` = handled) - and eight `Task`-returning twins for all but
`IOnBeforeUpdate`/`IOnUpdated`/`IOnErrorCaptured`. Implement only what you use; never both forms
of one hook. Sequences pinned by `LifecycleTests.cs`/`SetupTests.cs`:

| Moment | Hooks, in order |
| --- | --- |
| Mount (`Loaded`) | `OnBeforeCreate`, `OnCreated`, `OnBeforeMount`, `OnMounted`, `OnActivated` |
| Unmount (one `Unloaded`) | `OnBeforeUnmount`, `OnDeactivated`, `OnUnmounted`, back to back; a real detach (`If`) reports `OnDeactivated` first, via `IsVisibleChanged` |
| Hidden/shown while mounted (`Directives.Show`, `KeepAlive`) | `OnDeactivated` / `OnActivated` only |
| ViewModel property changes | `OnBeforeUpdate` at the first change, one `OnUpdated` per `NextTick` batch |

- The first three fire at `Initialized` when `DataContext` is already there, else at `Loaded` -
  once per `DataContext` object, so a ViewModel swapped in before `Loaded` still gets the full
  sequence. `OnActivated` on mount only if the element is actually visible (a background tab or a
  `Show=false` sibling mounts without it). `*Async` twins fire at the same point and are never
  awaited.
- **Hooks follow the element, not the object.** Every remount of the same instance (an `If`
  toggling, a `TabControl` switch, a Teleport move, an unloaded `KeepAlive`) replays the whole
  create/mount sequence. Make `OnMounted` idempotent, or guard work meant to happen once.
- **WPF raises `Loaded` twice with no `Unloaded` between** (a `TabControl` realizes every tab's
  content, then raises `Loaded` again on selection) and can raise `Unloaded` without `Loaded`.
  Lifecycle, `Directives.Event`/`Use` and Teleport guard both edges; hand-written code must too,
  and must re-hook what it unhooks. A static-event subscription made on every `Loaded` pins the
  whole tree and its ViewModel (`LifecycleLeakTests.cs`).
- **One `aq:Lifecycle.Enable` per ViewModel**, on the View root that owns it. Hooks go to the
  element's effective `DataContext`, inherited included, so a nested element with `Enable` sharing
  that ViewModel fires every hook a second time.
- A `DataContext` replaced while mounted gets no mount hooks - only update tracking moves to it.
  `IOnUpdated` fires for any property of the ViewModel, including ones your own hooks set.
- `IOnErrorCaptured` subscribes to the element's own `Dispatcher.UnhandledException` while
  mounted (on the main UI thread, the event `Application.DispatcherUnhandledException` forwards
  to): app-wide on that thread, not scoped to the View's subtree, so every mounted ViewModel
  implementing it sees every exception there. No `Application` is needed, and an element on a
  second UI thread sees that thread's exceptions. A faulted `*Async` hook is rethrown on the
  element's `Dispatcher` and arrives here - never write `async void OnMounted()`.
- On a `Window`, focus changes (`Activated`/`Deactivated`) also raise `IOnActivated`/`IOnDeactivated`.
- **Loading + `Suspense`**: put `Lifecycle.Enable` and the loading hook on the View that *contains*
  the `aq:Suspense` (as `LifecycleDemoView.xaml` does), never inside its `Child`. The `Child` is out
  of the tree while `IsPending` is true, so a hook living there either never fires (spinner
  forever) or fires again on every resolve (load loop).

## Directives (`Barbatos.Wpf.Aquarius.Xaml`)

| Attached property | Behaviour |
| --- | --- |
| `aq:Directives.Model="{Binding Path}"` | Re-applies the binding `TwoWay` + `UpdateSourceTrigger=PropertyChanged` to `TextBox.Text`, `ToggleButton.IsChecked`, `Selector.SelectedItem` or `RangeBase.Value`, from the first value the binding resolves - `null` included (an empty `SelectedItem`, an unset `string?`). Must be a `Binding`: a plain value, `null` too, throws `InvalidOperationException`, as do `PasswordBox` and every other type; `ClearBinding` is fine. Copies only `Path`, `Converter`, `ConverterParameter`, `ConverterCulture` and the source (`Source`/`RelativeSource`/`ElementName`) - `StringFormat`, `Delay`, `ValidationRules`, `FallbackValue`, `TargetNullValue` are dropped; write a full `{Binding}` when you need them. |
| `Directives.Show` | `true` -> `Visible`, `false` -> `Collapsed`. Stays mounted. |
| `Directives.Event` + `Command` (+ `CommandParameter`) | Any public instance event by name via reflection; an unknown name throws `InvalidOperationException` once both are set. Parameter defaults to the raised `EventArgs`; `CanExecute` is honoured. Suspended on `Unloaded`, re-hooked on `Loaded`. |
| `Directives.Modifiers` | Comma-separated: `stop`/`prevent` (both set `Handled`), `once` (permanent detach), `self` (`OriginalSource` is the element), `left`/`right`/`middle` (mouse button), `enter`/`tab`/`esc`/`space`/`up`/`down`/`left`/`right`/`delete` (key; `delete` also matches Backspace). Filters apply only to the matching `EventArgs` type. No `capture` - use the `Preview{Event}` event. |
| `Directives.Use` (+ `UseValue`, `Argument`, `Modifiers`) | Attaches one custom `Directive` per element (`FrameworkElement` only). |
| `Directives.Class` | Space-separated `Style` resource keys (`TryFindResource`); their `Setter`s, `BasedOn` chain included, are written as local values, later tokens win, dropped tokens are cleared. Unknown key throws. |
| `Directives.Style` | `IDictionary<string, object>`; each key is a dependency-property name on the element's own type, each value must already be that property's type (`Brushes.Red`, not `"Red"`). Unknown name throws. |

- **`stop`/`prevent` and `once` act before the `self`/button/key filters**: `Modifiers="enter,once"`
  detaches on the first key of any kind, and `"enter,stop"` marks every key `Handled`. Combine them
  only when that is what you want; otherwise check the key inside the command.
- `Class`/`Style` beat the element's `Style` setters and triggers, and reverting clears the
  property - a value you also set on that property in XAML is lost. Only `Setter`s apply;
  triggers and event setters in a class `Style` are ignored.
- Custom directive (`FocusDirective.cs`, used in `DirectivesDemoView.xaml`):

  ```csharp
  public sealed class FocusDirective : Directive
  {
      public override void Mounted(FrameworkElement element, DirectiveBinding binding) => element.Focus();
  }
  ```
  ```xml
  <local:FocusDirective x:Key="AutoFocus" />                 <!-- in Resources -->
  <TextBox aq:Directives.Use="{StaticResource AutoFocus}" />
  ```
  `Mounted` runs on `Loaded`, `Updated` when `UseValue`/`Argument`/`Modifiers` change while mounted
  (`DirectiveBinding.Value`/`OldValue`/`Argument`/`Modifiers`), `Unmounted` on `Unloaded`. One
  resource instance serves every element that uses it - keep per-element state on the element.

## Conditional content: `If`, `Expr`, `Comparisons`, `Suspense`

```xml
<aq:If Condition="{aq:Expr 'Count > 0 &amp;&amp; Total &lt;= Budget'}">
    <TextBlock Text="Really detached when false" />
    <aq:If.Else>
        <TextBlock Text="else - nest another aq:If here for else-if" />
    </aq:If.Else>
</aq:If>
```

- `If` genuinely detaches its content (full unmount/remount sequence); `Directives.Show` only hides.
  Use `If` for content that changes rarely; use `Show` for anything toggled often, including any
  periodic/realtime source - each timer tick pays a full unmount/remount, only flips within one
  call stack coalesce (`IfControlTests.cs`). Each branch holds one content object.
- `If.Condition`, `Directives.Show` and `Transition.Show` default to `true`, so an unresolved
  binding or `Expr` **shows** the content ("fails open").
- `Expr` grammar: `> >= < <= == != && || ! + - * /`, parentheses, right-associative `? :`, number
  and string literals, lowercase `true`/`false`/`null`, identifiers as property paths
  (`Order.Total`), `#Name.Path` for an `ElementName` binding. Arithmetic is `double`. `==`/`!=`
  work on any objects (numeric coercion, enum against its name: `Status == "Active"`);
  relational operators need numbers or two `IComparable`s of one type. **`&& || ! ?:` need real
  booleans** - no truthiness; a `null` or number operand throws `InvalidOperationException` at
  evaluation. No `RelativeSource`, method calls, indexers or string concatenation. The result can
  be any type (a ternary feeding `TextBlock.Text` works, see `ExprDemoView.xaml`); one-way only.
- `Expr` in XAML: single quotes delimit the argument; escape `<` as `&lt;`, `&&` as `&amp;&amp;`,
  string quotes as `&quot;`. `Expr.Evaluate(expression, source)` evaluates once from C# by
  reflection and cannot resolve `#` identifiers.
- `Comparisons.Not` (two-way), `IsNull`, `IsEqualTo` via `{x:Static aq:Comparisons.IsNull}`.
  `IsEqualTo` is `Equals(value, ConverterParameter)`, and a literal XAML `ConverterParameter` is a
  string - it never equals an `int` or enum; pass `{x:Static}` or use `Expr`.
- `{x:Static aq:BuildConfiguration.IsDebug}` reads the entry assembly's `DebuggableAttribute` (the
  app's build configuration), not `Debugger.IsAttached`.
- `aq:Suspense IsPending` shows `Fallback` while `true`, `Child` while `false` (default); the
  `Child` is genuinely unmounted while pending - see the Loading + Suspense rule above.

## Teleport, Transition, Provide/Inject, Slots, Component/KeepAlive

Details and verified sequences in [patterns.md](patterns.md). The rules that bite without it:

- **Teleport moves one `UIElement`** into a `Panel` registered with `aq:TeleportHost.RegisterHost`
  (any other host type throws; non-`UIElement` content is never moved). Every move - including the
  first settle into an already-registered host - is a full unmount/remount, so `OnMounted` runs
  twice. `DataContext` does not travel: the content inherits from its new ancestors.
- **`Transition`** ships no animations and skips `Enter` on first render; `TransitionGroup.Enter`
  is enter-only. **`Provide`/`Inject`** is subtree-scoped; lifetime values use constructor injection.
- **Slots** need a `SlotHost` (in practice a subclass, like the sample's `Card`) whose
  `ControlTemplate` reads `{aq:SlotContent name}` / `{aq:SlotProvided name}` - they bind to
  `TemplatedParent`, so they work only inside that template.
- **`Component` alone destroys the outgoing View**; wrap it in `aq:KeepAlive` to cache. `TabControl`
  and `Frame`/`Page` are **not** keep-alive (verified). `KeepAlive` owns its children's
  `Visibility` (never add `Directives.Show` to a cached View), throws if children are added
  directly, and is not supported around `aqr:RouterView`. Register Views it builds as transient.

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| View renders empty, `DataContext` is `null` with `aq:Setup.Enable` | ViewModel in another namespace, another suffix, or the View name does not end in `View`; misses are silent | `aq:Setup.ViewModel="{x:Type ...}"` or `ViewModelResolver`; turn on `ThrowOnUnresolvedViewModels` |
| `MissingMethodException` while the View loads | ViewModel has constructor parameters but is not registered, or `UseAquarius()` never ran | Register it and call `app.Services.UseAquarius()` after `Build()` |
| Parent's `DataContext="{Binding X}"` on a View is ignored, or wipes its ViewModel | The View also uses `aq:Setup` | Keep one: Setup or parent binding |
| `OnMounted` never fires | No `aq:Lifecycle.Enable` on the View root (the `aq-view` template sets it; a hand-written View may not), it sits on an element whose `DataContext` is another object, or the View is a `Suspense` child still pending | Add `Enable` on the View root; move loading out of the `Suspense` child |
| `OnMounted`/data load runs twice | A remount (`If`, tab switch, Teleport settle) or two `Lifecycle.Enable` sharing one ViewModel | Idempotent hook; one `Enable` per ViewModel |
| A `NextTick.Run` callback never runs, only where there is no `Application` object (WPF hosted in WinForms) | Called from a worker with no UI thread to fall back on | Call it on the UI thread |
| Computed value is stale | The getter reads something not passed as a dependency, or the `Computed` was disposed | List every source (or `this`) in `From` |
| ViewModel never garbage-collected | `Watch`/`Computed` on a longer-lived source not disposed; static event subscribed on every `Loaded` | Dispose in `IOnUnmounted`; guard both `Loaded`/`Unloaded` edges |
| `If`/`Show` content always visible | Unresolved binding or `Expr` identifier fails open | `ThrowOnUnresolvedExprIdentifiers = true` in development |
| `Expr: '&&' requires a boolean operand` | A logical operator or `?:` got a number or `null` | Compare explicitly (`Count > 0`, `X != null`) |
| `StringFormat`/validation rules lost on a `Directives.Model` box | `Model` copies only path, converter and source | Write the full `{Binding ..., Mode=TwoWay}` |
| Event command dead after one keypress / every key swallowed | `once`/`stop` act before the key filter | Drop the modifier; check the key in the command |
| `Comparisons.IsEqualTo` always `false` | Literal `ConverterParameter` is a string | `{x:Static}` parameter or `Expr` |
| Tab switch loses typed text / scroll position | `TabControl` and `Frame` destroy content | `aq:KeepAlive` + `aq:Component` (patterns.md) |

## Checklist: adding a View + ViewModel

1. Scaffold `XyzView.xaml` + `XyzView.xaml.cs` (only `InitializeComponent()`) + `XyzViewModel.cs`,
   same folder and namespace: `dotnet new aq-view -n Xyz --namespace MyApp.Features.Xyz`
   (installing and changing the template: `barbatos-templates`).
2. ViewModel: `public sealed partial class XyzViewModel : ObservableObject` (`partial` for the
   `[ObservableProperty]`/`[RelayCommand]` generators); state as `[ObservableProperty]`/`Ref<T>`,
   derived values as `Computed<T>`.
3. Decide: self-sufficient (`aq:Setup.Enable`, as the template generates) or parent-bound (remove
   it and bind `DataContext` at the usage site). Never both.
4. Implementing any `IOn*` hook? The View root needs `aq:Lifecycle.Enable="True"` - the template
   already sets it; add it to a hand-written View, and never a second one inside that View.
5. Constructor dependencies? Register the ViewModel (transient) and make sure `UseAquarius()` runs
   after `Build()`.
6. Dispose `Watch` handles and `Computed<T>` built on longer-lived sources in `IOnUnmounted`.
7. Development builds: `ThrowOnUnresolvedViewModels` and `ThrowOnUnresolvedExprIdentifiers` on.
8. Tests (STA helpers, dispatcher pumping, `GcProbe` leak checks): `barbatos-wpf-testing`.

## Changing Barbatos.Wpf.Aquarius itself

Load `barbatos-package-authoring`. A new control, attached property or directive follows the
`Loaded`-guard and leak/XAML-test rules in `.claude/rules/library-code.md`; tests that call
`UseAquarius` save and restore the `Setup.*` statics; a behaviour pinned by a test (the KeepAlive
table by `KeepAliveTests`) changes together with the README text it backs.

## Related skills

- `barbatos-aquarius-router` - routed Views, `RouterView`, pairing a View with a ViewModel in the
  route table, why `KeepAlive` cannot wrap `RouterView`.
- `barbatos-valee-form` (inputs, validation, error display), `barbatos-apsu-store` (state shared
  across screens), `barbatos-wpf-host` (`WpfApp`, DI, configuration), `barbatos-templates` (`aq-view`).
- `barbatos-wpf-testing` - testing Views, hooks and leaks.
- `barbatos-package-authoring` + `barbatos-docs-sync` - changing Aquarius itself.
