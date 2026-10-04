---
name: code-organization
description: Enforce frontend code organization — bulletproof-react ownership-first placement, the allowed-folder law (a folder holds only the kind of thing its name promises), kebab-case file naming with PascalCase / UI* identifiers, type-only files, classes-only / no-static-or-free-functions outside React, path-alias imports, semantic (no-data-testid) selectors, and hardcoded value / string extraction to `.env` and i18n. Use when placing, moving, renaming, or splitting components, hooks, repositories, stores, or modules; reviewing structure; fixing dependency-cruiser, ESLint, type-file, or duplication CI failures that stem from structural or naming issues; or extracting hardcoded configuration.
---

# Code Organization Skill

## Profile keys consumed

- `architecture.source_root`
- `architecture.modules`
- `architecture.component_prefix`
- `architecture.path_aliases`
- `framework.ui`
- `framework.state`
- `framework.di`
- `framework.i18n`
- `make.ci`
- `make.lint_deps`
- `make.lint_eslint`
- `make.lint_tsc`
- `make.lint_dup`
- `make.lint_metrics`
- `make.format`
- `make.test_unit_client`
- `make.test_integration`
- `quality.depcruise_violations`
- `quality.eslint_errors`
- `quality.eslint_warnings`
- `quality.tsc_errors`
- `quality.jscpd_clones`
- `quality.metrics_enforced`

## Core Principle

> **Place code by ownership first, then by kind — a feature owns its code,
> and a folder holds ONLY the kind of thing its name promises.**

This is the fundamental, stack-generic law of code organization in a
bulletproof-react layout. It holds in every feature-module under
`architecture.source_root`, regardless of the UI framework or state
manager. Prefer the existing module and feature structure over new
top-level abstractions. See
[DIRECTORY-STRUCTURE.md](reference/DIRECTORY-STRUCTURE.md) for the full
folder-by-folder placement reference.

## Context (Input)

- Creating new components / hooks / repositories / stores and determining
  the correct directory
- Moving files to their proper owner
- Reviewing code for organizational compliance
- Fixing organizational issues from code reviews (the
  `code-quality-reviewer` agent flags these)
- Ensuring file and identifier names match their responsibility
- **Refactoring code structure** (moving, renaming, splitting components,
  hooks, or modules)
- **Fixing CI failures** that stem from structural / naming issues
  (dependency-cruiser, ESLint, type-file, duplication gates)
- **Extracting hardcoded config values** to `.env` and user-facing
  **strings** to feature i18n

## Task (Function)

Enforce strict code organization principles: bulletproof-react
ownership-first placement, the allowed-folder law, kebab-case file naming
with PascalCase / `architecture.component_prefix` identifiers, type-only
files, classes-only / no-static outside React, path-alias imports, and
semantic (no-`data-testid`) selectors.

Source paths follow the profile: feature code lives under
`<architecture.source_root>/modules/<module>/features/<feature>/` where
`<module>` is one of `architecture.modules`; reusable UI lives under
`<architecture.source_root>/components/<component_prefix lowercased>-*`.
See [DIRECTORY-STRUCTURE.md](reference/DIRECTORY-STRUCTURE.md) for the
complete tree.

## Directory Type Classification

Folders MUST hold only the kind of thing their name promises. The
allowed-folder sets are enforced by `dependency-cruiser`
(`module-allowed-folders`, `feature-allowed-folders`,
`tests-top-level-allowed-folders`); anything else fails `make.lint_deps`.

### Top-level `<architecture.source_root>/`

| Directory     | Contains ONLY                                       | Example                                 |
| ------------- | --------------------------------------------------- | --------------------------------------- |
| `modules/`    | Feature-modules (domain-owned workflows)            | `modules/catalog/`                      |
| `components/` | Reusable UI building blocks (`<component_prefix>*`) | `components/ui-button/`                 |
| `services/`   | Singleton infrastructure services                   | `services/https-client/`                |
| `stores/`     | Shared cross-module state                           | `stores/session-store.ts`               |
| `config/`     | DI container config, tokens, app config             | `config/dependency-injection-config.ts` |
| `routes/`     | Route definitions                                   | `routes/app-routes.tsx`                 |
| `providers/`  | React context providers                             | `providers/theme-provider.tsx`          |
| `utils/`      | Shared cross-cutting utilities (specific names)     | `utils/format-currency.ts`              |

### Module root — `module-allowed-folders`

A module directory may contain ONLY: `config`, `features`, `hooks`,
`lib`, `store`, `types`, `utils`. Shared module code goes in `lib/` or
`utils/` — never `helpers/`.

### Feature root — `feature-allowed-folders`

A feature directory may contain ONLY: `assets`, `components`, `hooks`,
`i18n`, `repositories`, `routes`, `types`, `utils`. Data access is
`repositories/`; the store stays at module level. Do not add `api/`,
`helpers/`, or a feature-level `store/`.

| Folder          | Contains ONLY                                   | Example                                 |
| --------------- | ----------------------------------------------- | --------------------------------------- |
| `components/`   | React components (feature UI)                   | `components/form-section/inert-box.tsx` |
| `hooks/`        | Hooks (`use-*` or `index`)                      | `hooks/use-login-switcher.ts`           |
| `repositories/` | Data-access classes (consumed via `index` only) | `repositories/login-repository.ts`      |
| `routes/`       | Route components / definitions                  | `routes/sign-in-route.tsx`              |
| `types/`        | Type-only files                                 | `types/login-form/fields.ts`            |
| `utils/`        | Instance-method helper classes (specific names) | `utils/normalize-auth-error.ts`         |
| `i18n/`         | `en.json` / `uk.json`                           | `i18n/en.json`                          |
| `assets/`       | Static assets                                   | `assets/logo.svg`                       |

### Directory Creation Guardrails

- **NEVER create new directories autonomously** — the allowed-folder sets
  above are closed lists enforced by `dependency-cruiser`. When in doubt,
  use an existing folder.
- Do not invent ad-hoc catch-all directories. The following are
  **explicitly forbidden** (and rejected by `make.lint_deps`):
  - `helpers/`, `misc/`, `common/`, `manager/` — vague catch-all
    anti-patterns; use `lib/` or `utils/` with a specific file name
  - `api/` at feature level — data access is `repositories/`
  - feature-level `store/` — module state stays at module level
  - any folder with uppercase letters (`no-uppercase-paths`)
- A genuinely new shared folder needs **demand from multiple callers**
  and explicit user approval — never add one speculatively.

## Frontend Naming Patterns

> **Files and folders are lowercase kebab-case; exported identifiers carry
> their role in the name.**

All path-shape rules are enforced by `dependency-cruiser`
(`no-uppercase-paths`, `src-module-name-kebab-case`,
`src-feature-name-kebab-case`, `feature-hooks-file-convention`). Violations
fail `make.lint_deps`.

### By Kind and Type

| Kind                  | File pattern                       | Identifier                            | Example                                      |
| --------------------- | ---------------------------------- | ------------------------------------- | -------------------------------------------- |
| Reusable UI component | `<prefix-lower>-<kebab>/index.tsx` | PascalCase `<component_prefix><Name>` | `ui-button/index.tsx` → `UIButton`           |
| Feature component     | `<kebab>.tsx`                      | PascalCase                            | `inert-box.tsx` → `InertBox`                 |
| Hook                  | `use-<kebab>.ts(x)` or `index.*`   | `use<Name>`                           | `use-login-switcher.ts` → `useLoginSwitcher` |
| Repository            | `<kebab>-repository.ts`            | class `<Name>Repository`              | `login-repository.ts` → `LoginRepository`    |
| Store / reactive var  | `<kebab>.ts`                       | class + module singleton              | `auth-var.ts` → `AuthStateVar`               |
| Selectors             | `<kebab>-selectors.ts`             | class singleton                       | `auth-store-selectors.ts`                    |
| Helper / util         | `<specific-kebab>.ts`              | class with instance methods           | `normalize-auth-error.ts`                    |
| Type-only file        | `types/<area>/<kebab>.ts`          | `interface` / `type` only             | `types/ui-form/submit-controls.ts`           |
| i18n                  | `i18n/{en,uk}.json`                | —                                     | `i18n/en.json`                               |
| Test                  | mirror subject + environment       | —                                     | `normalize-auth-error.test.ts`               |

- Module names under `modules/` are lowercase kebab-case (`back-to-main`,
  not `BackToMain`); feature names under `features/` are too (`auth`, not
  `Auth`).
- Reusable component identifiers are prefixed with
  `architecture.component_prefix` (default `UI`), but their files and
  folders stay kebab-case (`ui-button/index.tsx` exporting `UIButton`).
- Hook identifiers are `useSomething`; hook files are `use-something.ts`.
- Helpers get specific names, never `helper`, `misc`, or `utils`
  catch-alls.

### Directory Structure by Layer

```text
<architecture.source_root>/
├── modules/
│   └── <module>/                  ← one per architecture.modules entry
│       ├── config/
│       ├── features/
│       │   └── <feature>/
│       │       ├── assets/
│       │       ├── components/    ← feature UI
│       │       ├── hooks/         ← use-* / index
│       │       ├── i18n/          ← en.json, uk.json
│       │       ├── repositories/  ← data access (via index)
│       │       ├── routes/
│       │       ├── types/         ← type-only files
│       │       └── utils/
│       ├── hooks/
│       ├── lib/
│       ├── store/                 ← module state + composition root
│       ├── types/
│       └── utils/
├── components/                    ← reusable <component_prefix>* UI
├── services/                      ← singleton services (HTTP client, …)
├── stores/
├── config/                        ← DI config + tokens
├── routes/
├── providers/
└── utils/
```

`<module>` is each entry of `architecture.modules`; `<feature>` is any
feature directory under that module.

## Verification Checklist

When creating or reviewing a file, verify:

1. ✅ **Kind Matches Folder** (a folder holds ONLY its declared kind)
   - Example: a hook in `hooks/use-*.ts`, NOT in `components/`
2. ✅ **Name Follows the Pattern** for its kind (kebab file, role-carrying
   identifier)
3. ✅ **Path Is Lowercase Kebab-Case** (no uppercase anywhere under
   `architecture.source_root` or `tests/`)
4. ✅ **Name Reflects Actual Responsibility**
5. ✅ **Correct Owner** (feature-owned by default; shared only on real
   multi-caller demand)
6. ✅ **Reusable Components Have NO Feature Dependency** (no feature i18n,
   store, repository types, or route state in `components/`)
7. ✅ **Identifiers Are Specific** (not vague)
   - ✅ `normalizeAuthError`, `useLoginSwitcher` (specific)
   - ❌ `helper`, `doStuff`, `useData` (too vague)
8. ✅ **Type-Only Files Hold Only Types** (no runtime); logic files hold
   no `interface` / `type`
9. ✅ **No "Helper" / "Util" Catch-Alls** (extract specific
   responsibilities into named classes)
10. ✅ **No Free Functions / `static` in non-React `.ts`** (instance
    methods on a class instead)
11. ✅ **New Folders Are From the Allowed Set**, not agent-invented — must
    be explicitly approved by the user

## Frontend Best Practices

### Required Patterns

- ✅ **Classes + instance methods for non-React `src/**/*.ts`** — no
  `static` members, no standalone (free) functions. Behavioral
  collaborators are `@injectable()` classes; render-path primitives are
  instance classes exported as a module singleton. Enforced by an ESLint
  `no-restricted-syntax` gate (`make.lint_eslint`). Exempt: `*.tsx`
  components and `use-*` hooks.
- ✅ **Type-only files** — types live in dedicated `types/` folders;
  logic files never declare `interface` / `type`. Enforced by ESLint plus
  `dependency-cruiser` (`type-files-imported-as-type-only`,
  `type-files-no-runtime-imports`).
- ✅ **Container-free render path** — only the composition root touches
  the `framework.di` container, behind a dynamic `import()`, so the paint
  path stays light.
- ✅ **Semantic selectors** — source ships **no `data-testid`**; locate by
  role / label / text, falling back to a stable `id` only when no semantic
  query fits. Enforced by ESLint (`make.lint_eslint`).
- ✅ **Path aliases** — `@/` for cross-folder imports and a feature-scoped
  alias for deep within-feature imports (`architecture.path_aliases`);
  avoid `../../../` chains.
- ✅ **`framework.ui` styling** — Material UI v7 + Emotion (`sx`,
  `styled()`, theme); reusable components prefixed
  `architecture.component_prefix`.
- ✅ **DRY** — no copy-paste clones at or above the jscpd threshold
  (`make.lint_dup`); extract a shared component, hook, or constant rather
  than duplicating (see the `complexity-management` skill for the split).

### Anti-Patterns (Forbidden)

These are enforced by `dependency-cruiser` and the ESLint
`no-restricted-syntax` gates under `architecture.source_root`; treat the
rules as binding.

- ❌ **`helpers/` / `misc/` / `common/` / `manager/` folders** or
  `helper` / `util` / `misc` file names — extract specific
  responsibilities into named classes in `lib/` or `utils/`
- ❌ **Free functions or `static` members in non-React `.ts`** — use
  instance methods on an injectable class (or module-singleton class)
- ❌ **`data-testid` anywhere under `architecture.source_root`** — expose a
  stable `id` or query by role / label / text
- ❌ **`interface` / `type` in logic files**, and **runtime (`const` /
  `function` / `class`) in type-only files**
- ❌ **Deep relative import chains** (`../../../X`) across folders — use an
  alias from `architecture.path_aliases`
- ❌ **Business / user-facing strings hardcoded in JSX** — move them to
  feature `i18n/{en,uk}.json`
- ❌ **Feature UI importing the module store, repositories, or
  `services/` directly** — route through a hook
  (`no-components-to-store`, `no-components-to-repositories`,
  `no-feature-ui-to-services`)
- ❌ **Repositories reached by anything but their `index`**, or features
  calling the HTTP client directly (`no-repository-internal-imports`,
  `no-feature-direct-http-client`)
- ❌ **Cross-module / cross-feature imports that bypass public exports**
  (`no-cross-module-imports`, `no-cross-feature-imports`)
- ❌ **Uppercase letters in any path** under `architecture.source_root` or
  `tests/` (`no-uppercase-paths`)
- ❌ **Suppression directives** (`eslint-disable`, `@ts-ignore`,
  `// dependency-cruiser-disable`) — fix the structure instead

## Factory & DI Pattern (Maintainability & Flexibility)

> **Avoid hardcoded `new ClassName(...)` of collaborators in production
> code — resolve them through the DI container (`framework.di`).**

### Behavioral Collaborators → DI

Services, repositories, mappers, factories, and error handlers are
`@injectable()` classes registered against a token and resolved by token
or constructor `@inject`:

```typescript
// ❌ BAD: hand-wired collaborators at the call site
const repo = new LoginRepository(new HttpsClient(), new AuthErrorFactory());

// ✅ GOOD: resolved through the container by token
const repo = container.resolve<LoginRepository>(TOKENS.LoginRepository);
```

Resolution by token is the **preferred** way to obtain a collaborator
outside its own construction — substitution in tests happens by swapping
the container binding, not by monkey-patching a module.

### Render-Path Primitives → Module Singleton

State primitives that must stay container-free (for the
`framework.di`-free paint path / Lighthouse budget) are instance classes
exported as a module singleton, so call sites stay `X.method(...)` without
pulling DI into the chunk:

```typescript
// reactive state, dependency-free; no container in the paint path
class AuthStateVar {
  public get(): AuthState {
    /* read */
  }
  public set(partial: Partial<AuthState>): void {
    /* merge + notify */
  }
}
const authStateVar = new AuthStateVar();
export default authStateVar;
```

### When DI Registration Is REQUIRED

1. Collaborators with injected dependencies (HTTP client, config, factories)
2. Anything that must be substituted in tests (mockability)
3. Objects constructed from external input (responses, DTOs)
4. A token with **multiple** implementations (register the chosen one)

### When Direct Construction Is ACCEPTABLE

- Inside factory classes and the composition root (that is their purpose)
- In test code (Faker builders favor simplicity over abstraction)
- For framework-required patterns (`throw new ValidationError(...)`)
- Render-path module singletons (`export default new X()`)

### Factory Naming Convention

- `<ObjectName>Factory` creates `<ObjectName>` instances
- Location: same feature area as the object being created
- Example: `AuthErrorFactory` creates auth error objects

## Type Safety: Typed Files Over Loose Shapes

> **Known shapes get a named `interface` / `type` in a dedicated type-only
> file — not an inline anonymous object repeated across files, and never
> `any`.**

Loose shapes lose IDE support and let drift through. Name the shape once,
import it via `import type`.

### Loose vs Typed Comparison

| Pattern         | Bad (loose)                                 | Good (typed)                                     |
| --------------- | ------------------------------------------- | ------------------------------------------------ |
| Component props | inline `{ label: string; onChange: ... }`   | `LoginFormFields` interface in `types/`          |
| API value       | `const data: any = await repo.fetch()`      | `const data: LoginResponse = await repo.fetch()` |
| Known map       | `Record<string, unknown>` for a fixed shape | a named `interface`                              |
| Re-declared DTO | the same shape typed in two files           | one `type` re-exported from `types/`             |

### Benefits of Named Types

- ✅ IDE autocompletion and safe refactoring
- ✅ `make.lint_tsc` catches drift (`quality.tsc_errors` = 0)
- ✅ Self-documenting boundaries
- ✅ Single source of truth (import the type, don't restate it)

### When Loose Shapes ARE Acceptable

- Genuinely dynamic, one-shot internal data inside a single function
- Framework integration points that hand back `unknown`
- A `toJSON`-style serialization output

## Cross-Cutting Concerns Pattern

> **Hooks own data and side effects; components render props and
> translated UI. Feature components reach state and data through hooks —
> never by importing the store, repositories, or services directly.**

### Anti-Pattern: Container Logic Inside a Component

```tsx
// ❌ WRONG: one component fetches, maps errors, owns form state, and renders
export function ProfileForm() {
  const repo = container.resolve<ProfileRepository>(TOKENS.ProfileRepository);
  const [state, setState] = useState(/* form state */);
  // fetch, error mapping, validation, AND layout all here — violates the boundary
  return <form>{/* … */}</form>;
}
```

### Correct Pattern: Hook Owns Data, Component Renders

```text
<source_root>/modules/<module>/features/<feature>/
  hooks/use-profile-form.ts        ← data + side effects + state
  components/profile-form.tsx       ← renders props + translated UI
  components/profile-form-fields.tsx ← renders fields
```

```tsx
// ✅ CORRECT: the hook owns data; the component renders what it returns
export function ProfileForm() {
  const { fields, onSubmit, isSubmitting } = useProfileForm();
  return <ProfileFormFields fields={fields} onSubmit={onSubmit} busy={isSubmitting} />;
}
```

The hook is the only place that resolves repositories or store actions;
the component stays a pure render of translated props.

## Common Issues and Fixes

### Issue 1: File in the Wrong Folder

```bash
❌ WRONG:
<source_root>/components/login-card.tsx        # imports feature i18n + repo types

✅ CORRECT:
<source_root>/modules/<module>/features/<feature>/components/login-card.tsx

# Fix: move it back to its feature; keep it feature-owned until ≥2 modules
# use it without feature-specific props, copy, or state.
mv <source_root>/components/login-card.tsx \
   <source_root>/modules/<module>/features/<feature>/components/login-card.tsx
# Update imports/aliases everywhere
```

### Issue 2: Uppercase or Non-Kebab Path

```text
❌ WRONG: src/modules/BackToMain/Features/Auth/
✅ CORRECT: src/modules/back-to-main/features/auth/
```

`no-uppercase-paths`, `src-module-name-kebab-case`, and
`src-feature-name-kebab-case` fail `make.lint_deps` on uppercase or
PascalCase path segments.

### Issue 3: Vague Util Names

```text
❌ WRONG:
<source_root>/modules/<module>/features/<feature>/utils/utils.ts

✅ CORRECT:
<source_root>/modules/<module>/features/<feature>/utils/normalize-auth-error.ts
<source_root>/modules/<module>/features/<feature>/utils/map-validation-errors.ts
```

Name utilities by the transformation or decision they perform.

### Issue 4: Helper Class / Free Function

```typescript
// ❌ WRONG: free functions in a non-React .ts file (and a catch-all name)
export function validateEmail() {}
export function formatName() {}

// ✅ CORRECT: instance methods on specific classes
//   EmailValidator (utils/email-validator.ts)
//   NameFormatter  (utils/name-formatter.ts)
class EmailValidator {
  public validate(value: string): boolean {
    /* … */
  }
}
```

### Issue 5: Type Declared in a Logic File

```typescript
// ❌ WRONG: a logic file declaring its own prop type
// File: components/submit-controls.tsx
interface SubmitControlsProps { busy: boolean }

// ✅ CORRECT: the type moves to the feature's types/ folder
// File: types/ui-form/submit-controls.ts
export interface SubmitControlsProps { busy: boolean }
// File: components/submit-controls.tsx
import type { SubmitControlsProps } from '@/.../types/ui-form/submit-controls';
```

## Decision Tree: Where Does It Belong?

```text
What does the file DO?

├─ Renders UI reused across modules? → components/<prefix-lower>-*/
├─ Renders feature UI? → modules/<module>/features/<feature>/components/
├─ Owns data / side effects / state for components? → a hook (hooks/use-*.ts)
├─ Talks to the API? → features/<feature>/repositories/ (consumed via index)
├─ Holds module state? → modules/<module>/store/ (+ composition root)
├─ Declares a type only? → a types/ folder (import type)
├─ Pure transformation / decision? → instance method in utils/ or lib/
├─ A user-facing string? → i18n/{en,uk}.json
└─ Something else? → confirm against the allowed-folder set before adding a folder!
```

## Verification Commands

```bash
# Placement, naming, and import boundaries:
#   run the target mapped by make.lint_deps (dependency-cruiser)
#   must report quality.depcruise_violations (= 0) violations

# Convention gates (no-static / no-free-function / no-data-testid / type-file):
#   run the target mapped by make.lint_eslint
#   quality.eslint_errors (= 0) and quality.eslint_warnings (= 0)

# Types: run the target mapped by make.lint_tsc — quality.tsc_errors (= 0)
# DRY:   run the target mapped by make.lint_dup — quality.jscpd_clones (= 0)
# Complexity: run the target mapped by make.lint_metrics (quality.metrics_enforced)
# Format first: run the target mapped by make.format before make.lint_eslint

# Find organizational smells (generic tooling)
grep -rn "data-testid" <architecture.source_root>/                 # forbidden in source
grep -rEn "/(helpers|misc|common|manager)/" <architecture.source_root>/  # catch-all folders
grep -rEn "\.\./\.\./\.\." <architecture.source_root>/             # deep relative chains
```

If a `make.*` entry is `null`, the capability is absent — note the skip
and fall back to the remaining checks instead of inventing a target.

## DI Registration: No Redundant Wiring

Applies when `framework.di` is set (e.g. tsyringe; adapt the mechanics for
another container — the rule itself is generic).

> **Register each `@injectable()` class once against a token, then resolve
> it by token or constructor `@inject`. Do not register the same class
> twice, and do not reach for the container outside the composition root.**

### Rule

A class with constructor-injectable dependencies is registered **once** in
the DI config against a token in the tokens file, then obtained via
`container.resolve<Type>(TOKENS.X)` or `@inject(TOKENS.X)`. The render-path
store stays container-free: only the composition root imports the
container, behind a dynamic `import()` (`dependency-cruiser`
`no-di-config-import-outside-composition-root`).

### When Explicit Registration IS Required

- A token has **multiple implementations** (register the chosen one)
- A class needs a constructor argument the container cannot resolve
  (a config value, an env-backed primitive) — register it with an explicit
  value
- The implementation lives **outside** the autowired source

### When Wiring is REDUNDANT (don't add it)

- A class with only constructor-injectable deps and a single token —
  register once, resolve by token; do **not** also `new` it at call sites
- A render-path primitive that is already a module singleton — do not also
  bind it into the container

### Verification

```bash
# Confirm no call site imports the DI config outside the composition root:
#   run the target mapped by make.lint_deps
#   (no-di-config-import-outside-composition-root must report 0)
```

## Constraints (Never Do This)

**NEVER**:

- Place a file in the wrong folder (violates "a folder holds ONLY its
  declared kind")
- Let a reusable `components/` UI depend on feature i18n, store,
  repositories, or route state
- Use vague identifiers (`helper`, `doStuff`, `useData` — be specific!)
- Create `helpers/` / `misc/` / `common/` / `manager/` catch-alls
- Use uppercase in any path under `architecture.source_root` or `tests/`
- Declare `interface` / `type` in a logic file, or runtime in a type file
- Use `data-testid` in source — expose a stable `id` or query by
  role / label / text
- Use free functions or `static` members in non-React `.ts`
- Import the module store, repositories, or `services/` from feature UI —
  route through a hook
- Reach a repository by anything but its `index`, or call the HTTP client
  from a feature directly
- Use deep relative chains across folders instead of a path alias
- Hardcode user-facing strings in JSX instead of feature i18n
- Add suppression directives (`eslint-disable`, `@ts-ignore`,
  dependency-cruiser disables) instead of fixing structure
- Lower any `quality.*` threshold or edit `.dependency-cruiser.js` /
  `eslint.config.mjs` to make misplaced code pass

**ALWAYS**:

- Verify "a folder holds ONLY its declared kind"
- Keep code feature-owned by default; promote to shared only on real
  multi-caller demand
- Use specific, role-carrying identifiers and kebab-case paths
- Keep types in dedicated type-only files, imported via `import type`
- Use instance methods on classes instead of free functions / `static`
- Route feature data and state through hooks
- Use `@/` and feature-scoped aliases instead of deep relative chains
- Move user-facing strings to feature i18n
- Use DI to obtain collaborators in production code

## Hardcoded Configuration & Strings → `.env` / i18n Extraction

> **Configurable values (ports, URLs, language defaults, schema versions,
> feature flags) belong in `.env`; user-facing strings belong in feature
> i18n — not inline in code or JSX.**

### When to Extract to `.env`

Extract to `.env` (exposed to the client as `REACT_APP_*`, read through
app config and inlined at build time by `framework.bundler`) when the
value is an environment tunable:

- **Ports / hosts**: dev / prod / mock server ports and URLs
- **Language defaults**: main and fallback language
- **Schema / contract versions**: pinned external schema version
- **Feature flags and timeouts**: client-side toggles, request timeouts

### When to Extract to i18n

Every user-facing string (`framework.i18n`) → feature
`i18n/{en,uk}.json`, used via `t('key')`. Never inline a label, button
text, or message in JSX.

### When NOT to Extract

Keep inline / in code when the value is:

- **A design token**: spacing, colors, radii — they live in the theme
- **Protocol / spec-defined**: HTTP status codes, ARIA role names
- **A domain invariant**: validation rules that are part of the model
- **A test fixture / golden text / mock sentinel** (see the Faker-builders
  convention)

### Extraction Pattern — Config (3-Step)

**Step 1**: Add the variable to `.env` (and `.env.test`)

```dotenv
# .env
REACT_APP_REQUEST_TIMEOUT_MS=8000
```

**Step 2**: Read it through app config (not `process.env` scattered in
components)

```typescript
// config — single read point, typed
public get requestTimeoutMs(): number {
  return Number(import.meta.env.REACT_APP_REQUEST_TIMEOUT_MS);
}
```

**Step 3**: Inject the config value where it is used, instead of a literal.

### Extraction Pattern — Strings (i18n)

**Step 1**: Add the key to `i18n/en.json` and `i18n/uk.json`.
**Step 2**: Replace the literal with `t('feature.key')`.
**Step 3**: Re-run localization generation if your build composes module
i18n.

### Verification After Extraction

Run, in order:

1. Target mapped by `make.format`, then `make.lint_eslint` —
   `quality.eslint_errors` / `quality.eslint_warnings` stay `0`
2. Target mapped by `make.lint_tsc` — `quality.tsc_errors` (= 0)
3. Target mapped by `make.test_unit_client` — update mocks / props
4. Target mapped by `make.ci` — full validation

## CI Integration: When CI Fails

When the target mapped by `make.ci` fails, consult this skill if the
failure involves:

| CI Failure Indicator                                   | Code Organization Fix                                                           |
| ------------------------------------------------------ | ------------------------------------------------------------------------------- |
| `dependency-cruiser` violation                         | Check folder placement / allowed folders / cross-module & cross-feature imports |
| ESLint `no-restricted-syntax` (static / free function) | Refactor to an instance method on an injectable class                           |
| ESLint `data-testid` finding                           | Query by role / label / text; fall back to a stable `id`                        |
| Type-file ESLint / dep-cruiser violation               | Move runtime out of type files; import types via `import type`                  |
| jscpd clone over threshold                             | Deduplicate the block (extract a component / hook / constant)                   |
| `make.lint_tsc` error after a move                     | Update imports and aliases everywhere                                           |
| `make.lint_metrics` violation after a split            | Extract a hook / helper (see the `complexity-management` skill)                 |
| Test failure after a file move                         | Move the mirrored test file too (mirror source ownership)                       |

Thresholds come from the profile only: `quality.depcruise_violations`,
`quality.eslint_errors`, `quality.eslint_warnings`, `quality.tsc_errors`,
and `quality.jscpd_clones` are fixed ceilings of `0`, and
`quality.metrics_enforced` stays `true`. Ceilings are fixed and floors are
**raise-only**: a profile may tighten them, never relax them — fix the
code, never the threshold.

### Refactoring Checklist (Before Running CI)

When moving, renaming, or restructuring files:

- [ ] File in the correct folder for its kind (see Decision Tree above)
- [ ] Path is lowercase kebab-case; identifier carries its role
- [ ] All imports updated to aliases under `architecture.source_root` and
      `tests/`
- [ ] Reusable UI carries no feature dependency
- [ ] Types live in a `types/` folder, imported via `import type`
- [ ] Test file moved to mirror source ownership; environment matches
- [ ] User-facing strings moved to feature i18n; config to `.env`
- [ ] Targets mapped by `make.lint_deps`, `make.lint_eslint`,
      `make.lint_tsc`, and `make.test_integration` pass

```yaml # profile-example
# Upstream reference profile values this skill reads:
architecture:
  source_root: src
  modules: [catalog, checkout]
  component_prefix: UI
  path_aliases: ["@/", "@feature/"]
framework:
  ui: mui-v7
  state: zustand
  di: tsyringe
  i18n: react-i18next
make:
  ci: ci
  lint_deps: lint-deps
  lint_eslint: lint-eslint
  lint_tsc: lint-tsc
  lint_dup: lint-dup
  lint_metrics: lint-metrics
  format: format
  test_unit_client: test-unit-client
  test_integration: test-integration
quality:
  depcruise_violations: 0
  eslint_errors: 0
  eslint_warnings: 0
  tsc_errors: 0
  jscpd_clones: 0
  metrics_enforced: true
```

## Related Skills

- [architecture](../architecture/SKILL.md) — layering, repository / hook
  boundaries, and `dependency-cruiser` rule resolution; use it together
  with this skill when a move crosses a layer boundary
- [complexity-management](../complexity-management/SKILL.md) — refactoring
  often requires reorganization; consult both when a file or component
  exceeds the metrics gate
- [code-review](../code-review/SKILL.md) — references this skill for
  organization verification during PR reviews
- [ci-workflow](../ci-workflow/SKILL.md) — apply code-organization
  principles when fixing CI failures that stem from structural issues
- [frontend-component-development](../frontend-component-development/SKILL.md)
  — component / hook authoring conventions that this placement guidance
  enforces
- [quality-standards](../quality-standards/SKILL.md) — maintains the
  overall quality thresholds these gates protect

Before applying this skill, confirm the active task against
[../AI-AGENT-GUIDE.md](../AI-AGENT-GUIDE.md) and
[../SKILL-DECISION-GUIDE.md](../SKILL-DECISION-GUIDE.md) so every relevant
skill is consulted and no verdict is silently skipped.

## Related Documentation

See [DIRECTORY-STRUCTURE.md](reference/DIRECTORY-STRUCTURE.md) for the
complete folder-by-folder placement reference, file naming conventions,
and step-by-step placement guides.

---

**Remember**: Structure reflects intent. Feature-owned placement and
truthful folder names make the architecture self-documenting.
