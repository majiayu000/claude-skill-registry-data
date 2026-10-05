---
name: naming
description: >
  Use this whenever a new file/folder is created or renamed in this Vue
  project, when reviewing a module for consistency, or when the right path
  for a file is unclear. Also triggers on "what should I name this?", "is
  this file named correctly?", "audit module naming". Enforces kebab-case
  folders, dot-prefixed `{module}.{name}.{type}.vue|js` files, multi-entity
  rules, singular vs plural for views, and the layered structure
  UI → Store → API.
---

# Naming Skill

Audit or apply the project's file and folder naming conventions.

## Conventions

### Folders

| Location           | Case                | Example                                                 |
| ------------------ | ------------------- | ------------------------------------------------------- |
| Top-level src dirs | kebab-case          | `src/lib/`, `src/modules/`                              |
| Module dirs        | kebab-case          | `modules/home/`, `modules/user-settings/`               |
| Module sub-dirs    | fixed names         | `components/`, `views/`, `stores/`, `router/`, `tests/` |
| Component utils    | `components/utils/` | `components/utils/`                                     |

### Files

| Type      | Pattern                         | Example                   |
| --------- | ------------------------------- | ------------------------- |
| Component | `{module}.{name}.component.vue` | `home.hero.component.vue` |
| View      | `{module}.{name}.view.vue`      | `auth.signin.view.vue`    |
| Store     | `{module}.store.js`             | `tasks.store.js`          |
| Router    | `{module}.router.js`            | `users.router.js`         |
| Unit Test | `{target}.unit.tests.js`        | `home.store.unit.tests.js`  |
| E2E Test  | `{target}.e2e.tests.js`         | `auth.signup.e2e.tests.js`  |
| Service   | `{name}.js`                     | `axios.js`                |
| Helper    | `{name}.js`                     | `tools.js`                |
| Plugin    | `{name}.js`                     | `vuetify.js`              |
| Config    | `{name}.js` or `index.js`       | `development.js`          |

### Multi-entity modules

When a module contains multiple entities (e.g., `billing` with `subscription`), components and views add an entity segment after the module prefix. Stores keep the simple `{module}.store.js` pattern (one store per module).

| Correct | Wrong |
| --- | --- |
| `billing.pricingCard.component.vue` | `PricingCard.component.vue` |
| `billing.plans.view.vue` | `plans.view.vue` |
| `billing.store.js` | `subscription.store.js` |

Pattern (components/views): `{module}.{entity}[.{name}].{type}.{ext}`

### Case conventions in code

| Context             | Convention         | Example                             |
| ------------------- | ------------------ | ----------------------------------- |
| Variable / function | lowerCamelCase     | `useHomeStore`, `paginationRequest` |
| Component name (JS) | PascalCase         | `HomeHeroComponent`                 |
| Store export        | `use{Module}Store` | `useTasksStore`                     |
| Constant / env key  | UPPER_SNAKE_CASE   | `MY_MODULE_KEY`                     |

---

## Rules

1. **Dot-notation prefix**: always prefix with the module name separated by dots
   - `home.hero.component.vue` not `hero.component.vue`
   - `tasks.store.js` not `store.js`

2. **Semantic suffix**: always add the type suffix
   - `.component.vue` for reusable components
   - `.view.vue` for page-level views
   - `.store.js` for Pinia stores
   - `.router.js` for route definitions
   - `.unit.tests.js` for unit tests, `.e2e.tests.js` for E2E tests

3. **Singular vs plural**: follow the module's data semantics
   - List of items → plural: `tasks.view.vue`, `users.view.vue`
   - Single item → singular: `task.view.vue`, `user.view.vue`

4. **Utility sub-components**: place in `components/utils/` and keep the module prefix
   - `components/utils/home.blur.background.component.vue`

5. **Shared code**: files in `src/lib/` use simple kebab-case, no module prefix
   - `src/lib/helpers/tools.js`, `src/lib/plugins/vuetify.js`

---

## Applying names

Derive name as: module prefix (kebab-case) + `.` + semantic name + `.` + type suffix. Place in the correct sub-directory (`components/`, `views/`, `stores/`, `router/`, `tests/`). When auditing, check each file against the tables above and report violations.
