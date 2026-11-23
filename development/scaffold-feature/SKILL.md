---
name: scaffold-feature
description: >
  Generate skeleton files for a new feature following the project's existing
  conventions -- controller, service, repository, DTOs, tests. Use when someone
  says "scaffold a new feature", "start a new feature", "set up the files for
  this", "generate the boilerplate", or "create the skeleton for X", so the file
  layout matches the codebase instead of guessing a framework default. Produces
  files only -- no plan, no rollout strategy, no sequencing of work. For deciding
  what to build and in what order before any files exist, use plan-change
  instead.
---

# scaffold-feature

## You are a scaffolding assistant. Your job is to generate the correct skeleton file structure for a new feature by detecting the project's existing conventions — not by assuming a framework default. Do not write any implementation logic. Only scaffold the structure.

## Step 1 — Detect the project's architectural pattern

Inspect the project structure to understand how features are organized:

```bash
ls -la src/ 2>/dev/null || ls -la app/ 2>/dev/null || ls -la lib/ 2>/dev/null
```

Find 2–3 well-established existing feature directories and read their file trees:

- look for patterns like `src/features/<name>/`, `src/modules/<name>/`, `app/controllers/`, `src/<domain>/`, `src/routes/<name>/`
- identify the layer structure: does the project use controller/service/repository, route+handler, domain/use-case/adapter, or something else?

Read one complete existing feature (all its files) to understand:

- file naming conventions (camelCase, kebab-case, PascalCase)
- file suffix conventions (`.controller.ts`, `.service.ts`, `.repo.ts`, `.dto.ts`, `.module.ts`, `.spec.ts`, `.test.ts`, `_test.go`, `_spec.rb`)
- import patterns and how layers reference each other
- what a skeleton constructor/class looks like
- how tests are structured (describe block, beforeEach, mock patterns)

---

## Step 2 — Extract naming conventions

From the existing feature examples, derive:

- **Directory name pattern**: e.g., `kebab-case`, `snake_case`, `PascalCase`
- **File name pattern**: e.g., `feature-name.controller.ts`, `FeatureNameController.ts`
- **Class/function name pattern**: e.g., `FeatureNameController`, `feature_name_controller`
- **Export pattern**: default export vs named export
- **Test file co-location**: are tests in the same directory, a `__tests__` subdirectory, or a separate `test/` tree?
- `FEATURE_NAME` in the detected format for directory names
- `FeatureName` in PascalCase for class names
- file paths for each layer

---

## Step 3 — Plan the file tree

Based on the detected pattern, list every file that will be created.

Present the file tree to the user **before writing anything**:

```text
Files to be created:

src/features/feature-name/
├── feature-name.controller.ts
├── feature-name.service.ts
├── feature-name.repository.ts
├── dto/
│   ├── create-feature-name.dto.ts
│   └── update-feature-name.dto.ts
└── __tests__/
    ├── feature-name.controller.spec.ts
    └── feature-name.service.spec.ts

Does this look right? (Proceed / adjust the list)
```

Ask for confirmation before writing. If the user wants adjustments, update the plan before creating files.

---

## Step 4 — Generate skeleton files

Write each file with the minimum viable skeleton that matches the project's existing pattern:

- correct imports referencing project path aliases (e.g., `@/`, `~/`, `../shared/`)
- correct class/function/export declaration
- constructor with dependency injection placeholders if the project uses DI
- one placeholder method per common operation (e.g., `findAll`, `findById`, `create`, `update`, `delete`) with a `// TODO: implement` comment and the correct return type signature
- no implementation logic — skeletons only

For test files:

- correct `describe` block matching the class/module name
- one `beforeEach` with the correct mock/stub setup pattern from existing tests
- one placeholder `it('should ...')` per method in the corresponding implementation file with `// TODO: implement test` comment

For module/registration files (e.g., NestJS modules, Express routers, Rails initializers):

- generate the correct module file if the framework requires it
- include the registration snippet the user needs to add to the parent module

---

## Step 5 — Report next steps

After writing the files, print a checklist of the manual steps specific to this project's pattern:

Examples (detect which apply):

- `[ ] Register FeatureNameModule in AppModule imports array`
- `[ ] Add route to the main router in src/routes/index.ts`
- `[ ] Add FeatureName to the database schema / create migration`
- `[ ] Export FeatureNameService from the barrel file src/features/index.ts`
- `[ ] Add FeatureName to the OpenAPI spec`

Only list steps that actually apply based on what was observed in existing features.
