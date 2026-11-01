---
name: barbatos-aquarius-router
description: "Navigation with Barbatos.Wpf.AquariusRouter (Vue Router port) - RouteRecord tables, IOnBeforeRouteLeave/IOnBeforeRouteUpdate and BeforeEach guards, RouterView, RouterLink, RouteTo, modal routes via RouteRecord.Window + RouterWindows, RouteSearchIndex. Use when moving between screens, back/forward, a nav bar or nested outlet, login-only screens, an unsaved-changes prompt, a 404 page, a deep link or toast click opening a screen, an in-app search box, or a dialog that is a route - or when an edit is silently lost on switching records, an outlet stays blank, or a link throws 'No route matches'. For the View/ViewModel itself use barbatos-aquarius-view. Vietnamese prompts too - điều hướng, chuyển màn hình, thanh nav, quay lại, chặn khi chưa đăng nhập, cảnh báo chưa lưu, tìm kiếm trong app."
---

# Navigation with Barbatos.Wpf.AquariusRouter

A port of Vue Router onto Aquarius: a `RouteRecord` table, a `Router` that runs a full guard
pipeline before committing, `RouterView` outlets, `RouterLink` triggers. `Router` never touches
`Window` or `Application` (only `RouterWindows` opens windows), so the whole pipeline runs headless
in tests. It is **not** a browser router: no URL history, scroll behaviour, transitions on
`RouterView`, or route-level keep-alive. Switching Views *inside* one screen is `aq:Component`
(`barbatos-aquarius-view`).

Every namespace (`.Matching`, `.Routing`, `.Searching`, `.Xaml`) maps to
`xmlns:aqr="http://schemas.barbatos.co/aquariusrouter/2026/xaml"`.

## Sources of truth

- Concepts and rationale: [README](../../../src/Barbatos.Wpf.AquariusRouter/README.md)
  ([Dialog windows](../../../src/Barbatos.Wpf.AquariusRouter/README.md#dialog-windows),
  [The Full Pipeline Order](../../../src/Barbatos.Wpf.AquariusRouter/README.md#the-full-pipeline-order));
  signatures: [API-REFERENCE](../../../src/Barbatos.Wpf.AquariusRouter/API-REFERENCE.md).
- The code beats the docs. `RunGuardPipeline`/`NavigateWithRedirect` in
  [`Routing/Router.cs`](../../../src/Barbatos.Wpf.AquariusRouter/Routing/Router.cs) are the
  pipeline; [`Matching/RouteMatcher.cs`](../../../src/Barbatos.Wpf.AquariusRouter/Matching/RouteMatcher.cs)
  is resolution, index children, aliases and registration-time validation;
  [`Xaml/RouterWindows.cs`](../../../src/Barbatos.Wpf.AquariusRouter/Xaml/RouterWindows.cs) is
  modal-route open/close.
- Sample [`samples/Barbatos.Wpf.AquariusRouter.Sample`](../../../samples/Barbatos.Wpf.AquariusRouter.Sample):
  `WpfProgram.cs` (wiring), `Routing/AppRoutes.cs` (every guard placement, index child, alias,
  redirect, catch-all, modal children), `Routing/AppNavigationGuards*.cs`, `Routing/LoginRedirect.cs`,
  `MainWindow.xaml` (nav bar, `IsActive` trigger, named outlet, search box), `Views/Dialog/`.
- Tests in [`tests/Barbatos.Wpf.AquariusRouter.UnitTests`](../../../tests/Barbatos.Wpf.AquariusRouter.UnitTests):
  `RouterNavigationGuardOrderTests` (the order contract), `RouterRedirectAndFailureTests`,
  `DefaultChildRouteTests`, `RouteRecordViewModel*Tests`, `RouterModalRouteTests`,
  `RouterDialogWindowTests`, `RouterLinkTests`, `RouterLeakTests`, `RouteMatcherTests`.
- [reference.md](reference.md) - read when you need the full `RouteRecord` member table, path
  syntax and ranking, exact `RouteLocationRaw` resolution (name param seeding, relative targets),
  history, the `RouterLink` active-state algorithm, search ranking/folding, or what holds a View
  alive.

## Wiring

From the sample's `WpfProgram.cs`:

```csharp
builder.Services.AddSingleton<AuthState>();
builder.Services.AddAquarius();
builder.Services.AddAquariusRouter(sp => AppRoutes.Build(sp.GetRequiredService<AuthState>()));

builder.Services.AddTransient<InspectorWindow>();     // a modal-route Window
builder.Services.AddTransient<DashboardViewModel>();  // routed ViewModel with ctor dependencies
builder.ConfigureAppNavigationGuards();               // global guards, via IWpfInitializeService

var app = builder.Build();
app.Services.UseAquarius();         // Setup.ServiceProvider = this container
app.Services.UseAquariusRouter();   // Router.Current = the Router singleton (also returned)
```

Then once, at startup (`MainWindow.OnSourceInitialized` in the sample):
`await Router.Current!.Start("/");`

- `routes` is a **factory**, called once when `Router` is first resolved, so a per-route
  `BeforeEnter` can close over a DI service. Optional second argument:
  `options => options.PathOptions = new PathParserOptions { Strict = true }` - set it in code;
  nothing in the package binds `RouterOptions` from configuration (its `SectionName` is only a
  name). For a settings file, add
  `builder.Services.Configure<RouterOptions>(builder.Configuration.GetSection(RouterOptions.SectionName))`
  after `AddAquariusRouter`. Without DI: `new Router(routes)` + `Router.Current = router`.
- `Router` and `IRouterHistory` go in with `TryAddSingleton`: register your own first to win.
- **Routed Views and ViewModels are transient.** `Router` resolves a fresh instance on every
  genuine (re-)entry through `Setup.Resolve` (container first, `Activator.CreateInstance`
  fallback); a singleton fights that and is never released. Register only types with
  constructor dependencies - parameterless ones need nothing.
- `Start(initial)` is `Push` that replaces the seed history entry. There is no default top-level
  route and no ambient URL. A cold-start protocol URI `myapp://users/42?ref=mail#detail` is
  `Start(RouteLocationRaw.Parse($"/{uri.Host}{uri.PathAndQuery}{uri.Fragment}"))` - `System.Uri`
  reads `users` as the host, so `PathAndQuery` alone is `/42?ref=mail`; for the empty-authority
  form `myapp:///users/42` it is `uri.PathAndQuery + uri.Fragment`. A `FullPath` the app stored
  itself (e.g. in a toast's `Arguments`) is `RouteLocationRaw.Parse(text)`.
- Register global guards from an `IWpfInitializeService` (sample: `AppNavigationGuardsInitializer`).
  `BeforeEach`/`BeforeResolve`/`AfterEach` return an `IDisposable`; dispose it when the
  registering object is shorter-lived than the router.

## The route table

Keep it in one place - `Routing/AppRoutes.cs`, the `router/index.ts` of the app:

```csharp
new RouteRecord
{
    Path = "/settings", Name = "settings", View = typeof(SettingsShellView),
    Meta = new Dictionary<string, object?> { ["requiresAuth"] = true, ["requiresPremium"] = true },
    Children =
    [
        new RouteRecord { Path = "", Name = "settings-profile", View = typeof(SettingsProfileView) },
        new RouteRecord { Path = "security", Name = "settings-security", View = typeof(SettingsSecurityView) },
    ],
},
new RouteRecord { Path = "/old-home", Redirect = _ => "/" },
new RouteRecord { Path = "/:pathMatch(.*)*", Name = "not-found", View = typeof(NotFoundView) },
```

- **Top-level paths start with `/`**, or registration throws `ArgumentException`. Children are
  relative unless they start with `/`.
- **`Path = ""` is the index child.** Targeting the parent by path *or by name* descends to it,
  keeping the location at `/settings`. It has no path of its own (`/settings/profile` is not it) -
  reach it by name (`ShortcutRouting.cs` does). Without an index child `/settings`
  renders the shell with an empty inner outlet. The alternative, `Redirect = _ => "/settings/security"`
  on the parent, changes the location and resolves before any guard.
- **Name every navigable record.** `{aqr:RouteTo Name=...}`, `RouteSearchResult.To` and a modal
  window's [X] all navigate by name. A second record with the same name takes over the name;
  the first stays reachable by path. A record with no `Name`, View or `Redirect` is a pure
  grouping record: its children match, its own path never does (it falls to the catch-all or
  throws `No route matches`).
- `Meta` merges root-to-leaf on every resolve (child wins), so one flag on a parent protects the
  subtree through a single global `BeforeEach`. The catch-all ranks last wherever declared.
- `Alias` paths resolve to the **same** record (shared `Instances`), by path only, without its
  children. `View`+`Views`, `ViewModel`+`ViewModels`, or a ViewModel for an outlet with no View
  throw `InvalidOperationException` at registration.
- `RouteRecord` is a reference type on purpose - identity is what makes a route "the same route"
  across navigations. Never make it a `record`, never share one table between two routers, and
  compare locations with `RouteLocation.IsSameLocation`, not `==`.

## Pairing a View with its ViewModel

| Situation | Use |
| --- | --- |
| You own the View, names follow `Ns.FooView` -> `Ns.FooViewModel` | `aq:Setup.Enable="True"` in the View |
| You own the View, namespace or name differs | `aq:Setup.ViewModel="{x:Type ...}"` |
| You own neither (both ship in libraries) | `RouteRecord.ViewModel` / `ViewModels` (sample: `/accounts/:id`) |

- **A routed View must resolve its own `DataContext`.** `Router` runs route hooks against the
  View's `DataContext` right after constructing it, before it is in any tree - an inherited
  `DataContext` is not there yet, so no enter hook or enter guard fires (and later leave/update
  guards hit whatever outer ViewModel it inherits once mounted).
- The convention matches the namespace-qualified name; another assembly is fine (if loaded),
  another namespace or suffix is not, and failure leaves `DataContext` null silently. Make it
  loud with `AddAquarius(o => o.ThrowOnUnresolvedViewModels = true)` - `UseAquarius()` overwrites
  a hand-set `Setup.ThrowOnUnresolved` with that option.
- `RouteRecord.ViewModel` is assigned after construction and **overrides** the View's own
  `aq:Setup`. The paired ViewModel gets every route hook and guard, but Aquarius mount hooks
  (`IOnMounted`, `IOnBeforeUnmount`, ...) only if the View itself sets `aq:Lifecycle.Enable` - if
  you cannot edit the View, load from `IOnRouteEnter`.

## Navigating from code

```csharp
await router.Push("/users/42");                                   // literal path
await router.Push(new RouteLocationRaw { Name = "user", Params = new Dictionary<string, object?> { ["id"] = "42" } });
await router.Push(RouteLocationRaw.Parse("/search?q=hello#results")); // a serialized FullPath
await router.Replace("/login");                                   // no new history entry
await router.Back();                                              // Go(-1); Forward() = Go(1)
```

- A string is **always a literal `Path`**. `"/x?y=1"` is not split - a `/:param` route can
  swallow `x?y=1` as its value, otherwise it falls to the catch-all or throws. Use `Query`, or `RouteLocationRaw.Parse` for anything that was a `FullPath` (history,
  a stored redirect target, a protocol URI).
- `Path` ignores `Params`; build from parts with `Name` + `Params`. `Params` is
  `IReadOnlyDictionary<string, object?>` and `Query` is `IReadOnlyDictionary<string, string?>` -
  write `new Dictionary<string, object?> { ... }` / `new Dictionary<string, string?> { ... }`;
  target-typed `new() { ... }` does not compile against an interface.
  By name, required params the current location already has carry over (from `/users/7/...`,
  `{ Name = "user-overview" }` stays on user 7).
- Results: `null` on success, else a `NavigationFailure`. An unmatched path or unknown name is
  **not** a failure - `Resolve` throws `InvalidOperationException` out of `Push`.
- Same location again returns `Duplicated` without running guards; `Force = true` re-runs the
  pipeline as an *update* (same instance). `Go`/`Back`/`Forward` run the guards but skip steps 1-2
  below; out of range is a silent `null` with no `AfterEach`.
- **Navigate on the UI thread.** `Push` constructs Views synchronously. Marshal callbacks from
  thread-pool timers or `Task.Run` through the Dispatcher first. `INotificationService.Activated`
  and `IPushNotificationService.RouteRequested` already arrive on the UI thread, so a toast
  handler can `Push` directly; so are input-system actions, global hotkeys included, in a normal
  startup, which is why the sample's `ShortcutRouting` pushes directly.

## Guards

| Interface (on the View's `DataContext`) | Fires | Can cancel |
| --- | --- | --- |
| `IOnBeforeRouteLeave` | its record leaves the matched chain | yes |
| `IOnRouteUpdate` then `IOnBeforeRouteUpdate` | its record stays matched across a param/query change | update guard only |
| `IOnRouteEnter` then `IOnBeforeRouteEnter` | its record is newly entered (fresh instance) | enter guard only |

Guards are always async and return `NavigationGuardResult.Continue`, `.Cancel` or
`.Redirect(raw)`; a `bool` converts implicitly. Unlike Vue Router, `IOnBeforeRouteEnter` runs on
the real instance - `to.Params` is right there, no `next(vm => ...)`.

**Pipeline order** (`Router.NavigateWithRedirect` + `RunGuardPipeline`; pinned by
`RouterNavigationGuardOrderTests`):

1. Static `Redirect` on the resolved leaf - followed again while the new leaf redirects; each hop
   counts toward the 30-hop redirect limit.
2. Duplicate check -> `Duplicated` unless `Force`.
3. `IOnBeforeRouteLeave`, deepest child first.
4. Global `BeforeEach`, registration order.
5. Every updating record's `IOnRouteUpdate`, **then** every `IOnBeforeRouteUpdate`, root first.
6. Per-route `BeforeEnter` on entering records, root first.
7. Entering Views constructed (their `aq:Setup` resolves `DataContext`), then every
   `IOnRouteEnter`, then every `IOnBeforeRouteEnter`, root first.
8. Global `BeforeResolve`.
9. Leaving records' `Instances` cleared; history pushed (replaced for `Replace` or the first
   navigation); `CurrentRoute` swapped; every `RouterView` reacts.
10. `AfterEach(to, from, failure)` for every outcome - success, `Aborted`, `Cancelled`,
    `Duplicated` - except a redirect in progress.

- A guard's `Cancel` -> `Aborted` (4); a newer navigation started meanwhile -> `Cancelled` (8),
  checked at the end of every stage; `Duplicated` is 16. Real flags, so
  `NavigationFailures.IsNavigationFailure(f, NavigationFailureType.Aborted | NavigationFailureType.Cancelled)` tests both.
- A guard's `Redirect` restarts at the new target. Static and guard redirects share one limit of
  30 chained hops per navigation; past it `Push` throws `InvalidOperationException` ("Infinite
  redirect loop detected...") and commits nothing - unlike Vue Router, which only counts guard
  redirects.
- A guard that **throws** is not a failure: the exception leaves `Push` as-is (`RouterLink`
  rethrows it on the Dispatcher). Like a refusal it commits nothing and releases any View built in
  step 7, so a retry constructs fresh ones. Still say no with `Cancel`/`Redirect`: a throw reaches
  the caller as an error, not as a `NavigationFailure`.
- Data hooks (`IOnRouteEnter`/`IOnRouteUpdate`) run before their stage's guards and before every
  later stage, and are never rolled back. Do not start subscriptions or timers there - an
  entering instance can be discarded unmounted; use the Aquarius mount hooks.

**Where to put a check** (the sample shows each): protection by `Meta` + one global `BeforeEach`
(`/preferences`, `/settings` - one guard checks `requiresAuth` and `requiresPremium`); a rule
owned by the route, `BeforeEnter` (`/admin`); a rule owned by the screen, `IOnBeforeRouteEnter`
(`DashboardViewModel`); unsaved changes, leave + update guards. Redirect to login with the
intended target in the query (`LoginRedirect.To(to)`), and push it back with
`RouteLocationRaw.Parse`.

### Unsaved changes - leave and update

`/users/1/settings` -> `/users/2/settings` is an **update** (same record, same instance), not a
leave, so a leave guard alone lets the edit vanish. And because step 5 runs `IOnRouteUpdate`
first, a ViewModel whose `IOnRouteUpdate` reloads state destroys the edit before its own update
guard can see it. Load inside the guard, after the decision - the sample's
`UserSettingsViewModel` does exactly this:

```csharp
public sealed partial class UserSettingsViewModel : ObservableObject,
    IOnRouteEnter, IOnBeforeRouteLeave, IOnBeforeRouteUpdate   // deliberately no IOnRouteUpdate
{
    public void OnRouteEnter(RouteLocation to, RouteLocation from) => Load((string)to.Params["id"]!);

    public Task<NavigationGuardResult> OnBeforeRouteLeave(RouteLocation to, RouteLocation from) =>
        Task.FromResult<NavigationGuardResult>(!IsDirty || ConfirmDiscard());

    public Task<NavigationGuardResult> OnBeforeRouteUpdate(RouteLocation to, RouteLocation from)
    {
        if (IsDirty && !ConfirmDiscard())
            return Task.FromResult(NavigationGuardResult.Cancel);

        Load((string)to.Params["id"]!);   // Load/IsDirty/ConfirmDiscard are the app's own
        return Task.FromResult(NavigationGuardResult.Continue);
    }
}
```

Steps 6-8 can still refuse after that `Load`; where they might, reload once the navigation
commits instead. A ViewModel with nothing to protect implements `IOnRouteUpdate` to refresh on a
param change - without it a reused screen shows the previous record's data.

## XAML surface

```xml
<aqr:RouterView />                          <!-- default outlet; Content is managed - never set it -->
<aqr:RouterView OutletName="sidebar" />     <!-- fed by RouteRecord.Views["sidebar"] -->

<Button aqr:RouterLink.To="/about" Content="About" />
<Button aqr:RouterLink.To="{aqr:RouteTo Name=user, Params='id=2'}" Content="User 2" />
<Button aqr:RouterLink.To="{Binding SettingsTarget}" aqr:RouterLink.Replace="True" />
```

- A nested outlet is just `<aqr:RouterView />` inside a routed View; depth comes from walking
  ancestor `RouterView`s at `Loaded`, skipping records without Views.
- `RouterLink.To` takes a `string` or `RouteLocationRaw`, only on `ButtonBase` or `Hyperlink`
  (anything else throws).
- `RouterLink.IsActive` (the target or one of its descendants is current, so a link to a parent
  stays active on any child) and `IsExactActive` (exact, params included) are read-only - style with
  `<DataTrigger Binding="{Binding (aqr:RouterLink.IsActive), RelativeSource={RelativeSource Self}}" Value="True">`
  (`MainWindow.xaml`).
- `{aqr:RouteTo}` is evaluated **once** at parse: `Params`/`Query` are `;`-separated `key=value`,
  a comma inside a value makes a repeatable param's list; `Name` + `Path` together or neither
  throws. For a target that changes, bind `To` to a ViewModel `RouteLocationRaw` property
  (`UserLayoutViewModel.SettingsTarget`).
- Which router: explicit `Router` on the control, then inherited `RouterScope.Router`, then (outlets
  only) the ancestor outlet's, then `Router.Current` - so `RouterView.Router` never reaches links;
  use `RouterScope`. See [reference.md](reference.md#router-resolution-and-routerlink).

## Dialog windows - two shapes

**Modal route - the default.** The dialog is a route, so links, `Push`, shortcuts, search and deep
links all reach it with nothing extra:

```csharp
new RouteRecord
{
    Path = "/dashboard", Name = "dashboard", View = typeof(DashboardView),
    Children =
    [
        new RouteRecord { Path = "inspector", Name = "inspector", Window = typeof(InspectorWindow),
            Views = new Dictionary<string, Type> { ["inspector"] = typeof(InspectorOverviewView) } },
    ],
}
```

`aqr:RouterWindows.Enable="True"` once on the main `Window`; the dialog hosts
`<aqr:RouterView OutletName="inspector" />` and ordinary `RouterLink`s (it gets `RouterScope.Router`
automatically).

- Declare it as a **child** of the route that stays visible behind it - that parent keeps
  rendering in the main window.
- Prefer a named outlet: a plain `View` is also claimed by any main-window outlet that reaches
  that depth. The sample's plain `View` works only because `DashboardView` has no nested outlet.
- Register the `Window` **transient** - a closed WPF `Window` cannot be shown again. It is
  resolved through `Setup.Resolve`, owned by the main window, and opened with `Show()`: modal in
  routing terms only, the main window stays usable.
- One history: `Back` closes it; leaving the record closes it; closing the host closes all.
  Sibling records naming the same `Window` type share one window and swap its outlet.
- [X] (or `Close()`) becomes a navigation: `Push` to the parent by name (a new entry, current
  params kept), or `Back` if the parent has no name. The window goes once it commits and stays
  open if a guard refuses, throws, or a newer navigation supersedes it - so an unsaved-changes
  leave guard on a modal ViewModel works. An async guard keeps the window up until it decides. A
  throw is rethrown on the Dispatcher, as for a `RouterLink` click.
- **Name the parent.** Unnamed, [X] is `Back`, a no-op when the app started on the modal route:
  the window still closes, but the route stays on the modal record and re-pushing it is
  `Duplicated`.
- Your own `Window.Closing` handler on the dialog runs on every attempt, and again when a later
  commit closes the window - put once-only work in `Closed`. If it cancels, no navigation starts -
  provided it runs before `RouterWindows`' (attach it in XAML or the constructor, or cancel in an
  `OnClosing` override before the base call). An owner closing or app shutdown cannot be vetoed:
  the dialog goes, its guards are asked once.

**Independent stack** - a window that is a second application surface: a second `Router` with its
**own** route table, set once with `aqr:RouterScope.Router` on the `Window` (inheritance stops at
the window boundary, so it cannot drive the main router). Call `Start` on it. A container
resolves one `Router` per type, so expose the second through a holder type (README: `InspectorRouter`),
and scope it to the dialog: the last routed View - and through it the closed dialog - stays
alive until that router navigates elsewhere (`RouterDialogWindowTests`).

## Rules that bite

- `RouterView.Content` and `RouteRecord.Instances` belong to the router - never assign them.
- `Router` never disposes Views or ViewModels; it drops them. Release resources in Aquarius
  unmount hooks, and dispose any `Watch.On(router.CurrentRoute, ...)` there - an app-lifetime
  router pins every watcher.
- Never wrap `<aqr:RouterView>` in `<aq:KeepAlive>`: the router owns routed View lifetimes so
  guards run against the mounted instance. Keep-alive inside one screen is `aq:Component` +
  `aq:KeepAlive`. Nor in a `Transition`: it is driven by its boolean `Show`, not by a content
  swap - animate inside the routed View instead.

## Symptom -> cause -> fix

| Symptom | Cause | Fix |
| --- | --- | --- |
| Edit lost switching `/users/1` -> `/users/2`, no prompt | Update, not leave; or `IOnRouteUpdate` reloads before the update guard | [Unsaved changes](#unsaved-changes---leave-and-update) pattern |
| Reused screen shows the previous record's data | Same record = same instance, only update hooks run | Implement `IOnRouteUpdate` (or load in the update guard) |
| Routed screen blank, no hooks fire | `DataContext` null: convention missed, or the View relies on an inherited one | `aq:Setup.ViewModel` or `RouteRecord.ViewModel`; `ThrowOnUnresolvedViewModels` to surface it |
| `/settings` shows the shell, inner outlet empty | No index child | Add a `Path = ""` child, or `Redirect` on the parent |
| `InvalidOperationException` "No route matches path" from `Push`/a click | No catch-all, a pure grouping path, or a `?query` inside a string | Catch-all; `Query` or `RouteLocationRaw.Parse` |
| Clicking the current link does nothing; `AfterEach` logs `Duplicated` | Same location | `Force = true` to re-run as an update |
| Dispatcher exception "No Router is available" | `UseAquariusRouter`/`Router.Current` not set before the window loaded | Call `UseAquariusRouter()` right after `Build()` |
| Every outlet empty, no error | `Start` never called - `CurrentRoute` is still `RouteLocation.Start` | `await router.Start("/")` once at startup |
| `InvalidOperationException` "Infinite redirect loop" | A guard redirects to a target it also redirects, or static `Redirect`s form a cycle (30 hops in all) | Exempt the target (`/login`) from the guard; break the static cycle |
| Link inside a dialog navigates the main window | No `RouterScope.Router` on the dialog (or only `RouterView.Router` set) | `aqr:RouterScope.Router` on the `Window` |
| Dialog outlet shows the top-level route's View | `RouterView` in a window without `RouterWindows`/`RouterScope` is depth 0 | Modal route, or an independent stack |
| Modal dialog opens once, then throws on the next open | `Window` registered singleton | `AddTransient<TWindow>()` |
| Dialog stays open after [X] | A leave guard refused (or is still awaiting) the navigation away, or your own `Closing` handler cancelled | Intended - the route still claims the window; answer the guard |
| Dialog closed, but its link does nothing (`Duplicated`) | Parent record unnamed and no earlier history entry, so [X]'s `Back` went nowhere | Give the modal route's parent a `Name` |
| `RouteSearchResult.To` throws, or pushing it throws "Missing required param" | Record has no `Name`, or needs a param the current location lacks | Name it; only make param-free routes searchable |
| A left screen is never collected, or memory grows per navigation | Singleton View/ViewModel, or an undisposed `CurrentRoute` watch | Transient registrations; dispose watches |
| `InvalidOperationException` about thread/STA during `Push` | Navigating from a background callback | Marshal through the Dispatcher |

## Checklist - adding a screen

1. Add the `RouteRecord` to `AppRoutes` with a `Name`; nest it under the layout that hosts its
   outlet.
2. The View resolves its own `DataContext` (`aq:Setup.Enable`/`Setup.ViewModel`) or the record
   pairs one (`RouteRecord.ViewModel`).
3. `AddTransient` the ViewModel only if it has constructor dependencies.
4. Read params in `IOnRouteEnter`; add `IOnRouteUpdate` if the record can be reused across param
   changes; leave + update guards if it edits data.
5. Protect it with `Meta` and the existing global `BeforeEach`, not a new guard per screen.
6. Nav entry: `aqr:RouterLink.To` + the `IsActive` trigger; `RouteSearchEntry` items if searchable.
   A dialog: `Window` + named outlet on a child record, transient window registration.

Changing the library itself: `barbatos-package-authoring`; keep the README "The Full Pipeline
Order" list, `RouterNavigationGuardOrderTests` and `Router`'s remarks in step; tests per TFM via
`barbatos-wpf-testing`; both docs via `barbatos-docs-sync`.

## Out of scope - do not add

Route-level keep-alive or `KeepAlive`/`Transition` around `RouterView` (above); a `RouterLink`
"open in a window" property (the window belongs on the record); a shipped search-box control
(`RouteSearchIndex` is the engine only); HTML5/hash history, scroll behaviour, Vue Router's
`props` binding, data loaders.

## Changing Barbatos.Wpf.AquariusRouter itself

Load `barbatos-package-authoring`. `Router` never touches `Window` or `Application`, so keep new
pipeline logic headless; a new XAML control follows the `Loaded`-guard and leak/XAML-test rules in
`.claude/rules/library-code.md`; tests that call `UseAquariusRouter` save and restore
`Router.Current`; a change to the guard order changes `RouterNavigationGuardOrderTests` and the
README pipeline table together.

## Related skills

`barbatos-aquarius-view` (the routed View/ViewModel, `aq:Setup`, lifecycle hooks, `aq:Component`),
`barbatos-wpf-host` (`WpfAppBuilder`, `IWpfInitializeService`, toast activation, global hotkeys),
`barbatos-valee-form` (the form inside a guarded screen), `barbatos-templates` (the
`barbatos-wpf-app` router scaffold), `barbatos-wpf-testing`, `barbatos-package-authoring`,
`barbatos-docs-sync`.
