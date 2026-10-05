---
name: create-module
description: >
  Use this whenever the user asks to "create a module", "scaffold a feature",
  "add a Vue domain", "new module called X", or starts work on a brand-new
  vertical (views + components + store + router entry + tests). Duplicates
  the canonical `src/modules/tasks` template, applies kebab/Pascal/camel/
  UPPER renames, and wires config-driven values. Module stays self-contained.
---

# Create Module Skill

Create a new module by copying and renaming the `tasks` template module.

## Prerequisites

- The canonical template module `src/modules/tasks` must exist
- You need a name for the new module (kebab-case)

## Steps

### 1. Ask for the module name

Prompt user for the new module name in kebab-case (e.g., `my-feature`, `user-settings`)

### 1b. Crud-only option

On this stack `crud-only` keeps every file and only thins the store test (the Node stack's option of the same name removes files its template carries and this one does not).

Ask: is this module pure CRUD (list/get/create/update/delete, no business logic beyond the standard pass-through actions)? If yes, scaffold crud-only — same files, but the generated store test uses the thin form (step 6b): one test that exercises each action once, no dedicated happy/error-path block per action (see `/feature` Phase 1 §5 — pass-through store actions). If the module will carry any custom logic beyond CRUD, scaffold normally and let `/feature` add tests as that logic lands.

### 2. Derive naming conventions

Follow `/naming` for the full reference. Quick summary from the module name (e.g., `my-feature`):

- **kebab-case**: `my-feature` (folder names, file prefixes, routes)
- **PascalCase**: `MyFeature` (component names in JS/templates)
- **UPPER_SNAKE_CASE**: `MY_FEATURE` (env keys, constants)
- **lowerCamelCase**: `myFeature` (variable names, function names, store exports)

### 3. Duplicate the module

```bash
cp -r src/modules/tasks src/modules/{new-module-name}
```

### 4. Rename references

Search and replace the following tokens across the new module:

- `tasks` → `{new-module-name}` (kebab-case)
- `Tasks` → `{NewModuleName}` (PascalCase)
- `TASKS` → `{NEW_MODULE_NAME}` (UPPER_SNAKE_CASE)
- `task` → `{new-module}` (singular kebab-case, if applicable)
- `Task` → `{NewModule}` (singular PascalCase, if applicable)

Files to check:

- Component names and file names
- Route paths and names
- Store/Pinia modules
- API endpoint names
- Type/interface names
- Config keys
- Test file names and test descriptions

### 5. Apply renames carefully

- Case-sensitive, whole-word matches where possible
- Show plan before applying if many files affected
- Don't rename unrelated code (e.g., "tasks" in comments about other features)

### 6. Config-driven values

Business values (plans, roles, feature flags) should be driven by module config, not hardcoded in stores or components.

Pattern:
- Define in `src/modules/{module}/config/{module}.development.config.js` (and env-specific variants)
- Access via the centralized config service (`import config from '@/lib/services/config'`)

### 6b. Crud-only: trim the store test

If step 1b chose crud-only, replace the copied `{module}.store.unit.tests.js` with the thin form: one `it()` per renamed action that calls it once (mocking `axios` and the config service exactly as the template does) and asserts the resulting state — keep the template's error-path test for any action that changes state after its `await`, instead of the template's per-action `describe` blocks with happy- and error-path cases. Check it with `/verify`'s coverage report — the thin form must still clear `vitest.config.js`'s per-file thresholds; if it doesn't for a given action, keep that action's own test.

### 7. Verify & report

Run `/verify`, then report: module path, renamed tokens, lint/test results, next steps (customize logic, update routes in `src/router`).
