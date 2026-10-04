---
name: ffca-feature
description: >
  Scaffold and extend FFCA features: the three-package domain, data, and presentation structure,
  models, repositories, Commands and Queries, DTOs, mappers, Cubits, and Modules. Use in an FFCA
  monorepo, a features/ folder whose packages are named {feature}_domain, {feature}_data, and
  {feature}_presentation, when creating a new feature, a headless feature, a presentation-only
  feature, or a screen, or when adding a layer, repository, Command, Query, DTO, mapper, or Cubit to
  an existing feature. Triggers on "add a feature package", "create a new feature", "scaffold the
  profile feature", "add a headless feature", "add a repository to this feature", "add a use case",
  "add a Command", "map this DTO to a domain model", "add a Cubit for this screen", and "wire up the
  feature Module". If the repo instead uses packages/ with _repository and _api_client packages,
  defer to vgv-ai-flutter-plugin's layered-architecture skill.
allowed-tools: Read Glob Grep Write Edit mcp__plugin_vgv-ffca-plugin_very-good-cli__create mcp__plugin_vgv-ffca-plugin_very-good-cli__packages_get
effort: high
---

# FFCA Feature

Workflow for building a feature in an FFCA monorepo. Conventions and code shapes are not restated here: read the cited sections of `${CLAUDE_PLUGIN_ROOT}/references/ffca/` and adapt the templates in `${CLAUDE_PLUGIN_ROOT}/references/code_templates/`.

## Before you start

1. Confirm the repo is FFCA-shaped (a `features/` folder with `{feature}_{layer}` packages). If not, stop and use the layered-architecture skill.
2. Read `references/ffca/overview.md`, section *Feature layers*, for the layer model, and `references/ffca/project_structure.md`, section *Naming conventions*, for package names (the hook validates them).
3. Check for a pre-generated API client first. If the backend ships one OpenAPI/Swagger definition, read `references/ffca/faq.md`, section *What if the backend has one large OpenAPI or Swagger definition for every endpoint?* The client belongs in `shared/`, and each feature's data layer consumes it.

## Build order: domain, then data, then presentation

Scaffold each package with the Very Good CLI (`dart_package` for domain and data, `flutter_package` for presentation), then fill it in. Build in dependency order so each layer compiles against the one below it.

### 1. Domain (`{feature}_domain`, Dart package)

Read `references/ffca/domain.md` and adapt `references/code_templates/domain_templates.md`:

- Models in `models/`: plain Dart with value equality. Do not suffix them with `Model` or `Entity`.
- Repository interfaces in `repositories/`: `abstract interface class`, one per feature, named for the feature's own aggregate. A feature's domain never defines another feature's repository.
- Commands and Queries in `use_cases/`: add one only when you combine multiple repositories or repeat the same work across Blocs. A pass-through to a single repository does not need a class at all. Name them `{Verb}{Thing}Command` and `{Get,Watch}{Thing}Query`, and use `execute` for commands, `get` or `watch` for queries. Do not call these "use cases" in names or docs; the folder keeps that name, the classes do not. See section *Business rules* and `references/ffca/faq.md`, section *Should we use callable classes for Commands and Queries?*
- Add the primary barrel `{feature}_domain.dart`.

### 2. Data (`{feature}_data`, Dart package)

Read `references/ffca/data.md` and adapt `references/code_templates/data_templates.md`:

- Data sources in `data_sources/`, each with a `dtos/` subfolder. A DTO never escapes the package.
- Mappers in `mappers/`. Prefer a `Converter<Dto, Domain>` subclass, which keeps the mapping in one named, testable place; extension methods such as `toDomain()` and generators like `auto_mappr` are also fine. One converter per source and per direction, so a feature reading from a database and an API has a `DbToDomain...` and an `ApiToDomain...`.
- Repository implementations in `repositories/` that fulfil the domain interface and apply the mapping as data comes out of the source.
- Add the primary barrel `{feature}_data.dart`.

### 3. Presentation (`{feature}_presentation`, Flutter package)

Read `references/ffca/presentation.md` and adapt `references/code_templates/presentation_templates.md`:

- Per screen: a `{screen}/bloc/` Cubit with sealed states (Initial, Loading, Loaded, Error), a `{screen}/views/` screen that switches on state, and a `{screen}/{screen}_module.dart` that wires dependencies and exposes navigation callbacks.
- The module constructs its dependencies with `Provider`. Read `references/ffca/presentation.md`, section *The module*: standardizing on one DI package is deliberate, so that every module in every feature reads the same way.
- Add subfeature barrels per independent entry point plus the primary barrel `{feature}_presentation.dart`. Read `references/ffca/presentation.md`, section *Subfeature barrel files*, for why this matters to deferred imports.
- For navigation wiring, use the `ffca-routing` skill.

## Feature shapes other than all three layers

- **Headless feature**: domain plus data, no UI. Read `references/ffca/overview.md`, section *Headless features*. When a screen is needed later, add a `{feature}_presentation` package with no change to the existing packages. If the data layer is backend-specific, name it `{feature}_data_{backend}`, for example `auth_data_firebase`.
- **Presentation-only feature**: a presentation package and nothing else, existing to compose other features' domains into a screen. Read `references/ffca/overview.md`, section *Presentation-only features*. The layout and naming do not change: it sits at `features/{name}/{name}_presentation` like any other presentation package, and the absence of siblings is the signal. Nothing needs declaring.

## Reserving a slot for a widget you do not own

When a screen needs to display something owned by another feature, the module can declare a slot the app fills, instead of importing that feature. Give the parameter a nullable `Widget` type, default it to nothing, and name it for its position (`trailingAction`), never for the widget you expect (`cartBadgeBuilder` leaks the other feature straight back in). More than two slots on one module means the composition belongs in an app-owned shell. Read `references/ffca/presentation.md`, section *Or let the app place it*, and use the `ffca-cross-feature` skill to choose between a slot and a direct import.

## Pubspecs and dependencies

When you add dependencies between packages, follow `references/ffca/project_structure.md`, section *Dependency rules*. The pubspec hook blocks edits that violate a layer rule and tells you the fix, so set the direction correctly the first time: data depends on its own domain, presentation depends on domains and never on a data layer, neither depends on an app.

If the app defers this feature's import, read `references/ffca/project_structure.md`, section *Deferred loading*, before adding a dependency on another feature's presentation package. An eager edge from a deferred package silently cancels the code splitting downstream.

## Tests

Every package gets tests. This skill does not cover test mechanics: delegate `blocTest`, `mocktail`, and golden details to the vgv-ai-flutter-plugin testing skill. Cover each repository implementation, each Command and Query, and each Cubit (success, failure, edge cases). A module whose slots default to nothing stays golden-testable without the other feature's repositories in the widget tree.
