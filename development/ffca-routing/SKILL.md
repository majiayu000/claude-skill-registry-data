---
name: ffca-routing
description: >
  Routing and navigation for FFCA monorepos: callback injection, go_router_builder typed routes,
  splitting the routing table, deferred-loaded features, the $extra hydration pattern, and keeping
  features isolated from each other's routes. Use in an FFCA monorepo, a features/ folder whose
  packages are named {feature}_domain, {feature}_data, and {feature}_presentation, when adding
  screens, routes, navigation, deep links, navigation callbacks, or a deferred-loaded feature.
  Triggers on "add a route for this screen", "navigate from one feature to another", "where do
  routes live", "split the router", "lazy load this feature", "pass an object to the next screen",
  "hydrate $extra on deep link", "add a deep link", "wire a navigation callback", and "can this
  feature import the router". If the repo instead uses packages/ with _repository and _api_client
  packages, defer to vgv-ai-flutter-plugin's layered-architecture skill.
allowed-tools: Read Glob Grep Write Edit
effort: high
---

# FFCA Routing

Workflow for wiring navigation in an FFCA monorepo. The patterns and code shapes live in `${CLAUDE_PLUGIN_ROOT}/references/ffca/navigation.md` and in `${CLAUDE_PLUGIN_ROOT}/references/code_templates/presentation_templates.md`. Read them before wiring routes.

## The core constraint

Features are isolated, so a feature cannot know the app's global routing table. It never imports the app's router or another feature's routes. Navigation is a dependency the app layer injects: the app decides *what happens next*, the feature only detects *when* it is needed. Read the intro of `references/ffca/navigation.md`, then follow the pattern that fits the feature's depth.

## Choose the injection pattern

1. **Shallow widget trees: callbacks on the module.** The module constructor takes typed callbacks (`onProductTapped`, `onCheckoutStarted`) and the app supplies them. Read `references/ffca/navigation.md`, section *Simple features: pass callbacks directly*, and adapt the module example in `references/code_templates/presentation_templates.md`.
2. **Deep widget trees: a navigation interface.** Define a plain Dart class in the feature's presentation package holding every navigation action, require it in the module, and provide it to the subtree with `Provider.value`. Deep widgets then call `context.read<CartNavigation>().onProductTapped(id)` with no prop drilling. Read `references/ffca/navigation.md`, section *Deep trees: define a navigation interface*.

Whichever you pick, the callback at the module boundary is the compile-time-safe cross-feature contract.

## Wire routes in the app layer with go_router_builder

Use `go_router` with `go_router_builder`. The app defines `@TypedGoRoute` and `GoRouteData` classes that instantiate feature modules and wire their callbacks to typed route navigation. Adapt the `GoRouteData` template in `references/code_templates/presentation_templates.md`.

Two hard rules from `references/ffca/navigation.md`, section *Recommended: go_router with go_router_builder*:

- No string-based paths. Navigate with generated route classes, `ProductDetailRoute(id: id).go(context)`, never `context.push('/product/123')`. A string path fails at runtime instead of compile time, and it forces the feature to know the app's URL structure.
- Features never import the app router configuration or another feature's route classes.

## Split the routing table, but keep it one library

The app owns the routing table, so every feature lands in the same file and it becomes a merge-conflict magnet. Give each feature's routes their own file, with one constraint that is easy to get wrong.

`go_router_builder` collects every `@TypedGoRoute` it finds in a *library* into a single generated `$appRoutes`. Routes declared in a separate library are left out, **and the failure is quiet**: the build succeeds and the routes simply do not exist. So the per-feature files must be `part` of one library, not separate imports.

```text
apps/my_app/lib/app_router/
  routes.dart            the library: imports, part directives, root route
  favorites_routes.dart  part
  ideas_routes.dart      part
  routes.g.dart          generated part
```

`routes.dart` holds every import and every `part` directive; each feature file starts with `part of 'routes.dart';`. Adding a feature is two lines in the shared file plus a new file nobody else is editing. Read `references/ffca/navigation.md`, section *Splitting the routing table across files*.

## Deferred imports live in the routing table

Because all imports are centralized in `routes.dart`, that is also where each feature gets its `deferred as` prefix, so its code is fetched the first time a route needs it rather than shipping in the initial bundle. Import a subfeature barrel rather than the whole package where one exists, so opening a list screen does not also download the detail screen.

```dart
import 'package:favorites_presentation/favorites_list.dart'
    deferred as favorites_list;
```

Before relying on this, read `references/ffca/project_structure.md`, section *Deferred loading*. A deferred package must not also be reachable from the app through a non-deferred path, or the chunk never splits, silently. This is informational on an iOS/Android-only app, where the AOT snapshot contains the whole program regardless.

## Deep links and the $extra pattern

Every screen must be rebuildable from its URL parameters alone. `$extra` is a volatile optimization that is lost on browser refresh, process death, and cold-start deep links, so the route declares it nullable and the Bloc treats it as optional: emit `Loaded` immediately when it is present, otherwise fetch by id and show loading. Read `references/ffca/navigation.md`, section *Deep links and data hydration*, and adapt the `ProductDetailRoute` template.

## Visual extension points

The same inversion applies to widgets. A feature can declare a slot for a widget it does not own and let the app fill it, exactly as it declares a callback for a destination it does not own. Read `references/ffca/navigation.md`, section *Visual extension points*, then use the `ffca-cross-feature` skill to choose between a slot and a direct import.

## Add-to-app

A module is a self-contained entry point with explicit dependencies, so it can be instantiated directly as the root widget of a `FlutterEngine` instead of inside a `GoRouteData.build()`. The module code is identical; only the callback targets change, from go_router routes to platform channels. Read `references/ffca/project_structure.md`, section *Add-to-app support*.
