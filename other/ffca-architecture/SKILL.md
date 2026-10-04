---
name: ffca-architecture
description: >
  Feature-First Clean Architecture (FFCA) orientation for Flutter monorepos: where code lives, layer
  boundaries, dependency rules, naming, and package organization. Use when working in an FFCA
  monorepo, a features/ folder whose packages are named {feature}_domain, {feature}_data, and
  {feature}_presentation, or when the user asks about Feature-First Clean Architecture, monorepo
  structure, layer dependencies, or package organization. Triggers on "where should this code live",
  "which package does this belong in", "is this dependency allowed", "can presentation import data",
  "can domain depend on Flutter", "what goes in {feature}_domain", "how should I name this package",
  and "explain the FFCA layers". If the repo instead uses packages/ with _repository and _api_client
  packages, defer to vgv-ai-flutter-plugin's layered-architecture skill.
allowed-tools: Read Glob Grep
effort: high
---

# FFCA Architecture

Orientation skill for Feature-First Clean Architecture (FFCA) monorepos. It tells you how to navigate the structure and which rules apply. It does not restate the conventions: those live in `${CLAUDE_PLUGIN_ROOT}/references/ffca/`. Every step below names the file and section to read.

## Confirm you are in an FFCA repo

The detection signal is a `features/` folder whose packages follow the `{feature}_domain`, `{feature}_data`, or `{feature}_presentation` naming. If the repo uses the standard VGV layered structure (`packages/` with `_repository`/`_api_client`), this is not an FFCA repo: defer to the layered-architecture skill instead.

## Workflow: deciding where code lives

1. Read `references/ffca/overview.md`, section *The structure*, to place the work in one of the three top-level folders: `apps/`, `features/`, `shared/`.
2. To decide between a feature and a shared package, apply the two-question decision rule in `references/ffca/overview.md`, section *Shared libraries* (a business capability an app composes goes to `features/`; something you could publish to pub.dev and a stranger would use unchanged goes to `shared/`). Use its component table to settle edge cases.
3. To decide which layers a feature needs, read `references/ffca/overview.md`, sections *Headless features* and *Presentation-only features*. A feature with no screens stays domain plus data and can grow a presentation package later with no structural change. A feature that only composes other features' domains into a screen has a presentation package and nothing else.
4. Before naming any package, read `references/ffca/project_structure.md`, section *Naming conventions*. The names are mechanically validated by the hook, so they are not optional.
5. To place a file inside a package, read `references/ffca/project_structure.md`, section *Layer subfolders*, for the per-layer folder map (`models/`, `repositories/`, `use_cases/`, `data_sources/`, `dtos/`, `mappers/`, and the per-screen `bloc/`, `views/`, module layout).

## Vocabulary: Command and Query, not use case

The classes in `use_cases/` are named **Command** (mutates, `execute`) and **Query** (reads, `get` or `watch`). Use those words when you talk about them and when you name them. The folder keeps the conventional `use_cases/` name so the layout matches other clean architecture projects, but the term "use case" is not used for the classes. Read `references/ffca/domain.md`, section *Business rules*.

## Before you wire dependencies

Read `references/ffca/project_structure.md`, section *Dependency rules*, before adding a dependency on another workspace package to a pubspec. That section's table is the whole policy, and it is what `scripts/validate_layers.dart` implements. The hook enforces it on every pubspec edit and blocks the edit on a violation, so confirm the direction first:

- apps depend on features and shared
- shared depends only on external packages
- the domain layer imports other domains and shared, nothing else
- the data layer imports its own domain, other domains, and shared
- the presentation layer imports domains and other presentation packages, never a data layer

Two absences carry as much weight as the rows: no presentation package depends on any `_data` package, its own included, and no shared package depends on a feature.

## Deferred loading constrains the graph

An app can load a feature on demand with a `deferred as` import, which is what splits web bundles and backs Android deferred components. This only works if the deferred package is not *also* reachable from the app through a non-deferred path. If `product_presentation` imports `cart_presentation` eagerly, deferring `cart` from the router achieves nothing.

The failure is silent: nothing breaks, no analyzer warning fires, and the bundle just stops splitting. Treat it as a rule, not a review note. Read `references/ffca/project_structure.md`, section *Deferred loading*. On an app shipping only to iOS and Android the AOT snapshot contains the whole program anyway, so this is informational there.

## Anti-patterns to reject

These are the violations the architecture exists to prevent. Read the cited sections for the rationale:

- Presentation importing a data layer. Depend on the domain and go through its repository interface. See `references/ffca/project_structure.md`, section *Dependency rules*.
- A shared package depending on a feature. See `references/ffca/overview.md`, section *Shared libraries*.
- Business logic living in `shared/`. Volatile, app-specific logic belongs in a feature domain. See the component table in the same section.
- A widget in `ui_kit` that needs a repository. It cannot compile there, because shared packages depend on external packages only. Split it: the presentational view goes to `ui_kit`, the stateful part stays in its feature. See `references/ffca/presentation.md`, section *Where the widget should live*.

## Where to go next

- Creating or extending a feature: use the `ffca-feature` skill.
- Routes, navigation, or deep links: use the `ffca-routing` skill.
- One feature needing another's data or widgets: use the `ffca-cross-feature` skill.
- Checking the whole repo's health: use the `ffca-audit` skill.

For a worked example of the whole structure, see the [mealify reference implementation](https://github.com/VGVentures/mealify_feature_first).
