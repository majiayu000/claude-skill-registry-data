---
name: frontend-component-development
description: Build or change React components, hooks, forms, and feature UI through the profile — reusable components carry the configured prefix, styling uses the configured UI library (MUI v7 + Emotion) and theme tokens, selectors stay semantic (no data-testid), and accessibility is non-negotiable. Use when building or changing a React component, hook, form, or feature view, when adding shared UI, or when wiring presentation to state, routing, i18n, or DI.
---

# Frontend Component Development Skill

## Profile keys consumed

- `architecture.source_root`, `architecture.modules`, `architecture.component_prefix`, `architecture.path_aliases`
- `framework.ui`, `framework.state`, `framework.di`, `framework.router`, `framework.i18n`, `framework.bundler`, `framework.package_manager`
- `make.format`, `make.lint`, `make.lint_eslint`, `make.lint_tsc`, `make.lint_metrics`, `make.lint_dup`, `make.test_unit_client`, `make.test_visual`, `make.storybook_build`, `make.ci`
- `quality.eslint_errors`, `quality.eslint_warnings`, `quality.tsc_errors`, `quality.jscpd_clones`, `quality.metrics_enforced`, `quality.visual_diffs`
- `capabilities.visual_testing`, `capabilities.storybook`, `capabilities.figma`, `capabilities.accessibility_audit`

## Context (Input)

- A story needs a new React component, hook, form, or feature view, or an existing one changed.
- Profile loaded from `.claude/react-sdlc.yml` (run `/fe-sdlc-setup` if missing) — the `make`
  map is the only sanctioned command surface; the `architecture.*` and `framework.*` keys are
  the only source of truth for where code lands and how it is built.
- This skill is the build-time companion to the `react-implementer` agent: when dispatched by
  `/fe-sdlc-implement`, that agent follows these rules; invoked directly, follow them yourself.

## Task (Function)

Turn the story's acceptance criteria into working, tested, accessible UI that lands in the
correct module under `architecture.source_root`, styles through the configured UI library, keeps
copy translated, and passes every mapped quality lane unchanged.

**Success Criteria**: the new/changed UI satisfies the story's acceptance criteria; the targets
mapped by `make.format`, `make.lint_eslint`, `make.lint_tsc`, `make.lint_metrics`,
`make.lint_dup`, and `make.test_unit_client` exit `0`; and — for any visible layout change — the
target mapped by `make.test_visual` reports `quality.visual_diffs` (= 0) diffs.

## Stack (from the profile)

Read the stack from the profile, never assume it. Build with the configured bundler
(`framework.bundler`) and the project package manager (`framework.package_manager`); style with
the configured UI library (`framework.ui` — MUI v7 + Emotion in the reference repository); read
state from `framework.state`, resolve non-React collaborators through `framework.di`, route
through `framework.router`, and translate through `framework.i18n`. A `framework.*` key that is
`null`/absent means that capability is not present in this repo — skip the related step with an
explicit note rather than improvising a substitute.

## Workflow

1. **Locate the boundary.** Find the owning module or shared-component boundary from
   `architecture.modules` and `architecture.source_root`. Reusable, module-agnostic UI is shared;
   feature-specific UI stays in its owning feature. See
   [code-organization](../code-organization/SKILL.md) and [architecture](../architecture/SKILL.md).
2. **Read the neighbours.** Read nearby components, hooks, i18n files, and tests before writing —
   match their conventions, do not invent new ones.
3. **Test first.** Add or update a Testing Library test before the behavior change (TDD); run it
   via `make.test_unit_client` to see it fail for the right reason. See
   [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md).
4. **Implement.** Write the minimal component/hook/form to pass, styling through `framework.ui`
   and theme tokens, keeping side effects out of presentational components.
5. **Translate.** Add user-facing copy to the locale files for `framework.i18n` (e.g. `en.json`
   and `uk.json`) in the same change — never hardcode strings in JSX.
6. **Verify.** Run the formatter, focused unit tests, lint, and (for visible changes) the visual
   lane. See [Verification](#verification).

## Component placement & naming

Place by responsibility, name by the profile. Feature-owned UI lives under the module the story
names; reusable, cross-module UI is shared and carries `architecture.component_prefix`.

| What you are building | Where it lands | Naming |
| --- | --- | --- |
| Reusable, module-agnostic component | the shared components root under `architecture.source_root` | folder kebab-case with the configured prefix; exported symbol uses `architecture.component_prefix` (e.g. prefix `UI` → folder `ui-button/`, symbol `UIButton`) |
| Feature-specific component | `components/` inside the owning feature under that module | feature-local name, no shared prefix |
| Hook | `hooks/` inside the owning feature (or shared hooks root) | `use-*` file, `useX` symbol |
| Form / validations | the feature's `components/` + `utils/` (validators) | colocated with the feature |
| Data access (queries/mutations) | the feature's `repositories/` | never `api/`/`helpers/`/`store/` at feature root |

Reference feature shape (only create the folders the feature needs):

```text # profile-example
<source_root>/modules/<module>/features/<feature>/
  assets/ components/ hooks/ i18n/ repositories/ routes/ types/ utils/ index.ts
```

Import cross-feature with the configured aliases (`architecture.path_aliases` — e.g. `@/…` and a
feature-scoped `@<feature>/…`); use a relative import only within the same folder. Never reach
through deep `../../../` chains. Module and feature folder names are lowercase kebab-case.

## MUI + Emotion conventions

- Prefer the UI library's components and theme tokens (spacing, palette, typography) before
  hardcoded CSS values; reach for `framework.ui` primitives before custom markup.
- Keep Emotion styles stable and scoped: move large or reused static `sx` objects / `styled`
  definitions outside render so they are not reallocated per render.
- Use the library's icon set for standard actions (e.g. `@mui/icons-material`); every icon-only
  control carries an accessible name.
- Extract a shared style fragment, constant, or base-object-plus-overrides rather than copy-paste
  — the duplication lane (`make.lint_dup`, `quality.jscpd_clones` = 0) fails on copied blocks.
  See [complexity-management](../complexity-management/SKILL.md).

## State, DI, and the classes-only / no-static rule

- Read and update state through `framework.state`; keep data fetching and mutation side effects
  out of presentational components — push them into hooks or the feature's `repositories/`.
- Register non-React collaborators (services, repositories, mappers, factories, error handlers)
  through `framework.di` as injectable classes resolved via the container, not reached for.
- **Outside React components**, logic files under `<source_root>/**/*.ts` must use **instance
  methods on classes** — no `static` members and no standalone (free) functions. React components
  (`*.tsx`) and hooks (`use-*.ts` / `use-*.tsx`) are exempt — they are functions by definition.
  Satisfy this by refactoring to instance methods, never with a suppression directive.

## Type-only files & semantic selectors

- Keep types in dedicated type-only files / `types/` folders; logic files declare no `interface`
  or `type`. A component's prop types move to its feature/area `types/` folder and are imported
  back with `import type`.
- Locate elements by user-facing semantics — `getByRole`, `getByLabelText`, `getByText` — falling
  back to a stable `id` only when no semantic query fits. The source ships **no `data-testid`**;
  adding one to make a selector resolve is forbidden. Fix the component's semantics instead.

## Localization (i18n)

Feature translations live beside the feature (e.g. `i18n/en.json` + `i18n/uk.json` for
`framework.i18n`). Add every locale's key together in the same change, keep keys grouped by
feature and screen, and preserve the naming style of nearby keys. Never hardcode user-facing
strings in JSX.

## Accessibility-first (non-negotiable)

Accessibility is a hard requirement, not a polish pass. For every component:

- Use semantic roles and an accessible name for every interactive control (labels, `aria-*`
  only where semantics do not already convey it).
- Keep keyboard operability and a visible focus state; manage focus on mount/route change where
  it matters.
- Keep color contrast and tap targets within WCAG AA; announce async state changes politely.

Route deeper audits and any flagged finding to
[frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) and
[accessibility-audit](../accessibility-audit/SKILL.md). When `capabilities.accessibility_audit`
is false, run the manual a11y checks above and record `SKIPPED: accessibility-audit
(capabilities.accessibility_audit=false)` rather than assuming the gate passed.

## Design-handoff gate (Figma)

When `capabilities.figma` is true and the story references a Figma node, reconcile the
implementation against the design (spacing, color, typography, states) via
[figma-design-check](../figma-design-check/SKILL.md) before declaring the component done.

`SKIPPED: figma-design-check` when `capabilities.figma` is false (no design source wired) — note
the skip and build to the story's written acceptance criteria instead; never block on an absent
capability.

## Storybook

When `capabilities.storybook` is true, add or update a story (CSF3) for new shared UI and keep
the target mapped by `make.storybook_build` green. `SKIPPED: storybook` when
`capabilities.storybook` is false or `make.storybook_build` is `null`.

## Verification

Run through the profile `make` map (the targets wrap the containerized toolchain and the
package-manager-managed dependencies — never invoke the bundler, `tsc`, ESLint, or the test
runner directly on the host):

```bash # profile-example
make format              # mutating preflight (Prettier + qlty) — runs first, alone
make test-unit-client    # focused Testing Library run (jsdom)
make lint                # eslint + tsc + markdown + jscpd + metrics + deps (read-only)
```

For visible layout changes, also run the visual lane when `capabilities.visual_testing` is true:

```bash # profile-example
make test-visual         # capabilities.visual_testing — quality.visual_diffs (= 0)
```

`SKIPPED: make.test_visual` when `capabilities.visual_testing` is false or `make.test_visual` is
`null`. The full gated suite (`make.ci`, mutation, Lighthouse) is re-enforced by the CI and QA
stages — see [ci-workflow](../ci-workflow/SKILL.md); do not weaken it here.

## Line length disclosure

Before presenting changes, check changed text files for lines longer than 100 characters. If any
exist, report each `path:line` and the measured character count. Treat this as disclosure, not
failure, unless a project gate (`make.lint_eslint` / `make.lint_metrics`) actually fails on it.

## Constraints (Parameters)

**DO NOT**:

- Hardcode the stack — read the bundler, package manager, UI library, state, DI, router, and i18n
  from `framework.*`; read placement from `architecture.*`. Never assume a specific tool by name.
- Hardcode user-facing strings in JSX, or add a key to one locale without the others.
- Add a `data-testid` (or any test-only hook) to make a selector resolve — fix the semantics.
- Use `static` members or free functions in non-React `<source_root>/**/*.ts` logic — use
  instance methods on injectable classes.
- Declare an `interface` / `type` in a logic file, or place data fetching in a presentational
  component.
- Copy-paste a style/markup block past the duplication threshold (`quality.jscpd_clones` = 0) —
  extract a shared fragment instead.
- Lower or edit any quality config (`quality.*`, ESLint, `tsc`, the metrics policy, the
  duplication config, the visual baseline tolerance) to make a violation pass.
- Add any suppression directive (`eslint-disable`, `@ts-ignore`, `@ts-expect-error`,
  jscpd/dependency-cruiser ignores) — fix the root cause.
- Run quality tools outside the mapped `make` targets, or invoke them on the host.

**ALWAYS**:

- Place feature UI in its owning module and shared UI under the prefix from
  `architecture.component_prefix`.
- Style through `framework.ui` and theme tokens before custom CSS; keep Emotion styles stable.
- Give every interactive control an accessible name, keyboard operability, and a focus state.
- Write the failing Testing Library test first and locate elements by semantic queries.
- Import cross-feature via `architecture.path_aliases`; relative only within a folder.

## Format (Output)

**Required final state**: the targets mapped by `make.format`, `make.lint_eslint`,
`make.lint_tsc`, `make.lint_metrics`, `make.lint_dup`, and `make.test_unit_client` exit `0`; the
visual lane (when enabled) reports `quality.visual_diffs` (= 0); locale keys exist for every
language; no suppression added and no threshold changed.

## Verification Checklist

- [ ] Component/hook/form landed in the correct module under `architecture.source_root`
- [ ] Shared UI carries `architecture.component_prefix`; cross-feature imports use the aliases
- [ ] Styled through `framework.ui` + theme tokens; Emotion styles stable and scoped
- [ ] State read via `framework.state`; non-React collaborators resolved through `framework.di`
- [ ] No `static` / free functions in non-React logic; types in type-only files
- [ ] Elements located by semantic queries; no `data-testid` introduced
- [ ] Accessible names, keyboard operability, focus state, AA contrast verified
- [ ] All locale files updated together; no hardcoded JSX strings
- [ ] `make.format`, `make.test_unit_client`, and `make.lint` exit `0`; visual lane clean (or noted skip)
- [ ] No quality threshold decreased, no suppression added

## Related Guides

Before applying this skill, confirm the active task against
[../AI-AGENT-GUIDE.md](../AI-AGENT-GUIDE.md) and
[../SKILL-DECISION-GUIDE.md](../SKILL-DECISION-GUIDE.md) so every relevant skill is consulted and
each verdict is recorded.

## Related Skills

- [code-organization](../code-organization/SKILL.md) — where a component, hook, or repository belongs and how it is named
- [architecture](../architecture/SKILL.md) — module boundaries, layering, and dependency-cruiser rules
- [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) — Testing Library, Playwright, visual, and mutation tests
- [frontend-quality-workflow](../frontend-quality-workflow/SKILL.md) — format, ESLint, TypeScript, markdown, and metrics gates
- [complexity-management](../complexity-management/SKILL.md) — reduce complexity and resolve duplication
- [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) — Lighthouse, web-vitals, and accessibility recovery
- [accessibility-audit](../accessibility-audit/SKILL.md) — deeper a11y audit and remediation
- [figma-design-check](../figma-design-check/SKILL.md) — reconcile the implementation against the Figma design
- [ci-workflow](../ci-workflow/SKILL.md) — drive the full mapped CI suite to green before commit
