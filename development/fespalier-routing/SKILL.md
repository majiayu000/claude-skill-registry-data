---
name: fespalier-routing
description: "How a fespalier folder tree becomes URLs and typed routes — static, dynamic ($id), catch-all ($$rest, $$$rest) and (group) folders, _private folders, typed and enum segments, query parameters, sibling order and unreachable routes, not_found.dart, route.dart (caseSensitive, localized paths, nest = false for a sibling with a compound path, linkable = false to keep a folder out of fsp links, remount to start a page again when its URL changes, and deferred to load a page's code on demand on the web), navigator.dart and present.dart for the root navigator, the generated typed routes (.go, .push, .location, locationFor), RouteLink (a typed link that is a real anchor on the web and can preload its page's data), typed extra with extra_codec.dart, and the route manifest with meta.dart. The texts in the route's language, with a $lang folder and a language menu, are fespalier-i18n (since 0.10.0). Notification taps that open routes are fespalier_push (since 0.13.0). Home-screen shortcut and widget taps that open routes are fespalier_launch (since 0.18.0). Load before adding or renaming a route folder, changing a segment's type, writing a link between pages (RouteLink), or when a URL shows not_found.dart instead of its page."
---

# fespalier-routing

> **Verified against fespalier `589cf391` (2026-10-08), release v0.13.0.**
> These skills ship in the fespalier repository, and CI checks them against its code
> on every change. Version-sensitive claims say the release they became true in; if
> your app pins another fespalier, trust that release's code over this page. See
> [Versions](https://github.com/fespalier/fespalier/blob/main/skills/README.md#versions).

The folder **is** the URL. A `page.dart` (or a `redirect.dart`) serves its
folder's path; every other kind decorates it. Start with
[`fespalier`](../fespalier/) if you have not installed or generated anything yet.

## Folders to URLs

| Folder                | Segment                                                           | Example                          |
| --------------------- | ----------------------------------------------------------------- | -------------------------------- |
| `products/`           | static                                                            | `/products`                      |
| `$id/`                | dynamic; typed by the parameters that ask for it                  | `/products/42` (`int id`)        |
| `$$rest/`             | **one or more** remaining segments, a `List`                      | `/docs/a/b` (`docs/$$rest`)      |
| `$$$rest/`            | **zero or more**                                                  | `/files`, `/files/a/b`           |
| `(account)/`          | group: shares a layout/guard/loading, adds **nothing** to the URL | `/profile` (`(account)/profile`) |
| `_components/`, `.x/` | skipped: colocated code, never a route                            |                                  |

- A page-less folder folds into its children's paths (`greet/$name/page.dart`
  is `/greet/:name`). A `(group)` may hold a page: `(marketing)/page.dart` serves
  `/` if nothing else does.
- A page is the **parent** of the routes below it: a deep link to
  `/orders/1/refund/confirm` builds `/orders/1/refund` under it. To make a route a
  sibling of the page above instead, with a compound path, put `const nest = false;` in
  its folder's `route.dart` (0.4.0;
  [`references/route-dart.md`](references/route-dart.md#nest--false-a-sibling-with-a-compound-path)).
- Two pages at one URL are an **error** (`(a)/x` and `(b)/x`). Siblings are tried
  **static, then dynamic, then catch-all**, whatever the folder order; a page
  another route always catches first is an error too, and the fix is to move one
  into or out of its `(group)`.
- `fsp new 'orders/[id]'` (or `:id`) writes `$id` folders; `[...rest]` and
  `[[...rest]]` write the catch-alls. Unquoted `$` is a shell hazard.

## Types come from the parameters

```dart
// data.dart in products/$id/ (and every file that asks for $id)
Future<Product> data(Ref ref, {required int id}) => fetchProduct(id);
```

`required int id` makes `$id` an `int` **everywhere**: the page, the guard, the
typed route, the parsing. `/products/abc` shows the nearest `not_found.dart`,
skips the guards that read segments or query parameters, and never builds the page. A segment is a `String`, `int`,
`double`, `bool` or an app **enum** (read by `name`); a catch-all is a `List` of
those (or `num`/`DateTime`). An **optional nullable** parameter (`int? page`,
`List<String> tags = const []`) is a **query** parameter and never leads to
not-found. Two files that disagree on a type are an error. Everything, with
samples that compile, is in
[`references/segments-and-types.md`](references/segments-and-types.md).

## Typed routes

```dart
ProductRoute(id: 42).go(context);                    // or .push<T>(context), .replace(context)
const SearchRoute(q: 'ap', page: 2).location;        // '/search?q=ap&page=2'
ProductRoute(id: 42).go(context, locale: 'fr');      // localized path, if route.dart has one
NoteRoute(id: 3).go(context, extra: note);           // typed extra
SearchRoute.of(context).copyWith(page: 2).go(context);   // since 0.5.0: the URL as state
```

The class is named after the page class (`ProductPage` becomes `ProductRoute`),
the folder path for a page **function** (`OrdersOrderIdCancelRoute`), or
`const routeName = 'Name';` in `page.dart`. `.location` includes the mount
prefix and is always the canonical spelling. Prefer typed routes over string
paths: a renamed folder then breaks the build, not a link. A string path is allowed,
and since 0.7.0 `fsp` warns about a literal that matches no route
([`references/typed-routes-and-extra.md`](references/typed-routes-and-extra.md#string-paths)).
More in
[`references/typed-routes-and-extra.md`](references/typed-routes-and-extra.md),
which also covers `of` / `maybeOf` / `copyWith` (the URL as state: read the typed
route at the current location, change one query parameter, `null` clears it),
`extra` (for pages, layouts, guards and redirects) and `extra_codec.dart`.

## Links between pages

```dart
RouteLink(
  to: ProductRoute(id: 42),          // or uri: Uri.parse('/products/42')
  preload: Preload.intent,           // none (default) | intent | visible
  onPreload: (context) => ...,       // 0.9.0: what else the page needs, when the preload starts
  method: LinkMethod.go,             // go (default) | push | replace
  builder: (context, follow) => ListTile(title: Text(p.name), onTap: follow),
)
```

`RouteLink` (0.5.0) is a link a browser understands: a real `<a href>` on the web
(status bar, middle click and Ctrl-click open a tab, the `href` carries the mount
prefix and `locale:` spelling), a plain widget elsewhere, and a plain click that goes
through go_router with `method`. **Give `follow` to the child**, or the link shows a
URL and does nothing. It carries no `extra`. `preload:` starts the data of the page it
points at (`fespalier-data`), and since 0.7.0 its code when the page is [deferred](references/route-dart.md#deferred-load-a-pages-code-on-demand); `RouteLinkScope` sets the default for the app. `onPreload:` (since 0.9.0) runs with the link's context when the preload starts, for what the page needs that is
not a provider, such as its image at the size it shows it (`ResponsiveImage.precache`,
[`fespalier-images`](../fespalier-images/SKILL.md)). In debug a
`uri:` that matches no route throws. Detail, the web click path and tests:
[`references/links.md`](references/links.md).

## Opening the app: launches and platform links (since 0.11.0)

An adapter's `launch()` answers an `InboundLaunch(location, source: NavigationSource.notification)` (or
`InboundLaunch.to(route, source: ...)`); `launchRouter(launch, (launch) => GoRouter(...), links: true)` builds the router at
that location over the platform's initial route and marks the first navigation with the source. With `links: true`
(telemetry, or an adapter that has an `onEnter` since 0.16.0) a platform deep link, at cold start or while running, is marked `NavigationSource.link`; an
in-app `go` is not. A launch does not stop later links being marked. Android hands a cold-start link over as the initial route; iOS delivers it after the first frame, as a warm link. `make` receives the launch (null on the web). Never on the web. An adapter's `onEnter` sees it as
`InboundNavigation.source`, and must not block `InboundNavigation.initial`. The generated `AppRoutes.router(launch:)` calls `launchRouter` (`links: true` with telemetry, `links: AppAdapters.handlesEnter` with adapters alone); the generated
main passes it `AppMain.launch`, the adapters' answer, and a `main: manual` app asks `AppAdapters.launch()` itself. With adapters
`AppRoutes.router` passes `onEnter: AppAdapters.handlesEnter ? onEnter : null` (since 0.16.0): go_router gets `AppRoutes.onEnter` only if
an adapter's `onEnter` getter is not null (none of the first-party ones has one; before 0.16.0 any adapter made it pass one, and `onEnter` was a method, which
no longer compiles). Without one go_router keeps its simplest code path, and **any `onEnter` makes go_router parse every navigation
asynchronously and apply its redirect limit to all of them**, so with an adapter that has one `go('/a')` then `push('/b')` in one handler loses the `go`.
An app.dart `router()` must pass `launch: AppMain.launch` on (an `fsp` warning otherwise). Details: `docs/navigation.md`, "Opening the app: launches and platform links".

**Platform links end to end, and a deep-link plugin (since 0.12.0).** There is no deep-link package: Flutter (deep linking is
on by default since 3.27) hands the link to go_router and the router marks it `link`. The steps are `links:` in the pubspec,
`fsp links` (files, and the manifest and entitlements with the opt-in keys), `.well-known` served with no redirect, and a
device check (`adb shell am start -a android.intent.action.VIEW -d <url> <package>`, `xcrun simctl openurl booted <url>`);
a widget test calls `sendPlatformLink(tester, Uri.parse(url))` from `package:fespalier/testing.dart`. `fsp links` warns
(never fails) when `flutter_deeplinking_enabled` is false in the manifest or `FlutterDeepLinkingEnabled` is false in
`ios/Runner/Info.plist`. A plugin such as `app_links` or Branch needs that switch off, and then fespalier sees no platform
link: an adapter of your own answers `launch()` from `getInitialLink()` and forwards warm links with
`navigateFrom(NavigationSource.link, ...)`. Recipe: [`references/links.md`](references/links.md), "Platform links end to end".

**Notification taps (since 0.13.0).** `fespalier_push` is an adapter (`adapters: [fespalier_push]`): the tap that cold-starts the
app is answered in `launch()` and opens the route as the initial location, a tap while the app runs is a `go` (or `push`) in
`attach`, both marked `notification`; the guards still run, and a tap delivered twice (same message id) opens once. The
package depends on no push SDK (Firebase Messaging is a recipe), has no HTTP code, never posts the token (`onToken` is
yours; since 0.14.0 a `PushToken` with a `kind`, a `value` and `properties`, and a revoked one is a `PushTokenRevoked` through `onTokenRevoked`, never a null) and never shows the permission prompt. The app writes a `PushSource`, a `PushRoute` (`linkRoute(hosts:, matches:)`
refuses `//x`, backslashes, foreign hosts) and **one call in `main()` before `AppMain.run()`**:
`FespalierPush.configure(source:, route:, onToken:, onTokenRevoked:)`; unconfigured, it reports once and does nothing. Details and the testing
recipe: [`references/push.md`](references/push.md); the vendor recipes: [`references/push-sources.md`](references/push-sources.md).

**Shortcuts and home-screen widgets (since 0.18.0).** `fespalier_launch` is an adapter (`adapters: [fespalier_launch]`): the shortcut or the widget tap that cold-starts the app is answered in `launch()` and opens the route as the initial location, and a tap while the app runs is a `go` (or `push`) in `attach`, both marked `shortcut` or `widget`; the guards still run. The package depends on neither launcher plugin (quick_actions and home_widget are recipes), sets no shortcut and saves no widget data. The app writes one `LaunchSource` per plugin, a `LaunchRoute` (a `switch` over `ShortcutAction` and `WidgetAction`, with `widgetLinkRoute(schemes:, hosts:, matches:)` for a widget's URI, which refuses anything but an in-app path) and **one call in `main()` before `AppMain.run()`**: `FespalierLaunch.configure(sources:, route:)`; unconfigured, it reports once and does nothing. Details and the testing recipe: [`references/launch.md`](references/launch.md); the plugin recipes: [`references/launch-sources.md`](references/launch-sources.md).

A tap on a **download's** notification works the same way (`adapters: [fespalier_download]`, since 0.15.0, configured with
`FespalierDownload.configure(backend:, store:, route:)` before `AppMain.run()`); the skill is `fespalier-downloads`, "Notification taps".

## Not-found views

A `not_found.dart` at the root is the app-wide one (without it users see a plain
`Nothing at /path`); **any other folder can have one, and the nearest wins**, for two things:

- **Unknown paths.** An unknown URL shows the `not_found.dart` of the deepest folder it is
  under (a `$dynamic` folder matches any value), else the root's. That is
  `AppRoutes.notFound(uri)`, which the router's `errorBuilder` calls.
- **Unparsable segments.** `/teams/a/members/abc` (an `int` id) shows the nearest
  `not_found.dart` above that route; a `(group)`'s counts here, but a group adds nothing to
  the URL, so its own is **never** picked for an unknown URL.

It gets `Uri uri` and the segments of its **own path** as raw `String`s (as the URL spells
them, decoded); **no query and no data**; it shows **without any layout**, so it brings its
own `Scaffold`. Two folders with one URL cannot both have one, a catch-all folder cannot
have one, and under `AppRoutes.mount(at:)` the prefix is skipped when looking for the folder
(a URL outside it gets the root's). `fsp new members --not-found` scaffolds one.

## The other routing files

| Need                                                                         | File and reference                                                                                                                          |
| ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| Paths match in any case, or one folder stays exact                           | `route.dart` with `caseSensitive`: [`references/route-dart.md`](references/route-dart.md)                                                   |
| `/produits` and `/produkte` for `/products`, one route                       | `route.dart` with `paths`, `locationFor`, `locale:`: same reference                                                                         |
| Texts in the URL's language, a language menu (`fespalier_tolgee`, 0.10.0)    | [`fespalier-i18n`](../fespalier-i18n/SKILL.md)                                                                                              |
| A page must start again (fresh state) when its URL changes, not keep it      | `route.dart` with `const remount = Remount.onSegments;` or the pubspec's `remount` (0.6.0): same reference                                  |
| A page's code must be a chunk of its own on the web, loaded on demand        | `route.dart` with `const deferred = true;` or the pubspec's `deferred` (0.7.0): same reference                                              |
| A deep link must not build the page above (`refund` under `refund/confirm`)  | `route.dart` with `const nest = false;` (0.4.0): a sibling with a compound path, same reference                                             |
| A page full-screen above the tab bar, URL still under its parent             | `navigator.dart`: [`references/navigators-and-present.md`](references/navigators-and-present.md)                                            |
| A sheet or dialog page class of your own, with a URL                         | `present.dart`: same reference                                                                                                              |
| Ask before a page goes (unsaved changes), Android back and the iOS swipe too | `leave.dart` (0.11.0): [`references/leaving-a-page.md`](references/leaving-a-page.md)                                                       |
| A route that only forwards (`/old-products/3` to `/products/3`)              | `redirect.dart` (`fespalier-guards`)                                                                                                        |
| Every route's path, groups, layouts, params and your own metadata at runtime | `meta.dart` and `AppManifest`: [`references/manifest-and-meta.md`](references/manifest-and-meta.md)                                         |
| A notification tap that opens a route, cold start and warm                   | `fespalier_push` (0.13.0): [`references/push.md`](references/push.md), [`references/push-sources.md`](references/push-sources.md)           |
| A shortcut or home-screen widget tap that opens a route, cold start and warm | `fespalier_launch` (0.18.0): [`references/launch.md`](references/launch.md), [`references/launch-sources.md`](references/launch-sources.md) |
| A link that shows its URL, opens in a tab, and preloads the page's data      | `RouteLink`, `RouteLinkScope` (0.5.0): [`references/links.md`](references/links.md)                                                         |

## Behaviours worth knowing before you debug

- **`replace` and `push` on the web** (since 0.6.0): `ProductRoute(id: 1).replace(context)` puts
  its location in the address bar and replaces the history entry (over a page that was pushed it
  keeps the stack instead). A `push` stays out of the address bar unless the pubspec has
  `push_updates_url: true` (a reload then builds that URL's own stack). On 0.5.0 use `go` for URL
  state. See `references/typed-routes-and-extra.md`.
- **`pushReplacement`** (since 0.7.0): `ProductRoute(id: 1).pushReplacement<T>(context)` is
  go_router's: a new page key, so a sheet handing over to a full page does not keep the sheet's
  state or transition (over a pushed page `replace` keeps the key; over a page of the declarative stack it is a
  `go`, which keeps it only for the same path template). The replaced page's own future never
  completes, and when it was the only page, neither does this one. Takes `locale:` and, where
  the route has one, `extra:`.
- **Trailing slashes** are dropped by go_router: `/products/` reaches
  `/products`. Nothing to configure.
- **Case** is sensitive by default. `case_sensitive: false` in the pubspec, or a
  `route.dart` per folder (nearest wins), emits `caseSensitive: false`. The
  requested case is **kept** in the router's location; only
  `state.matchedLocation` is spelled by the route.
- **A deferred page** (0.7.0, `const deferred = true;` in a `route.dart`) shows the nearest `loading.dart`
  while its code loads on the web and `error.dart` if that fails; once loaded it builds synchronously.
  Only `page.dart` is deferred, **layouts never are**, and a type (an enum, an `extra` class) declared
  in a deferred page.dart is an error. A test that pumps its own router needs
  `await tester.runAsync(AppRoutes.loadDeferred);` (`pumpRouter` does it).
- **A page keeps its state** when only its parameters change (`/c/1` to `/c/2`):
  go_router keys it by the path template. `remount` (0.6.0) changes that per folder
  or app-wide; the default is `never`.
- **Localized paths** are one `GoRoute` with an alternation, not one route per
  locale, so nested routes, page keys and restoration ids see one route. Read
  the route's `paths` through `RouteInfo`, never `pathParameters` (`_l0`).
  Since 0.10.0 `fespalier_tolgee` reads these spellings (`localeSpelling(AppManifest.all)`,
  `relocate`) and takes the locale from the route (a `$lang` enum segment, or the spellings); the
  texts are [`fespalier-i18n`](../fespalier-i18n/SKILL.md).
- **A page on a tab's first route cannot have a `:segment`** in its own path
  (go_router refuses): give the tab a `tabOptions` `initialLocation`
  (`fespalier-layouts`).
- **`AppRoutes.mount(at: '/x', navigatorKey: hostKey)`** stores its arguments
  statically; pass the host `GoRouter`'s own key whenever a folder uses
  `navigator.dart` or `present.dart`.
- **`fsp routes`** prints every route with its tags; run it before guessing which
  file serves a URL.

If `fsp` complains, look the message up in
[`fespalier-troubleshooting`](../fespalier-troubleshooting/).
