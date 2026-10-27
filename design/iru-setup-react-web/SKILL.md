---
name: iru-setup-react-web
description: "Invoked as /iru-setup-react-web with optional key: value args, usually by iru-setup-typescript-repository. Scaffolds a Vite + React + TypeScript web app and adds Vitest, ESLint or Oxlint, Prettier, Stylelint, Playwright e2e and component UI tests with accessibility checks, optional Storybook and Sonar."
model: sonnet
---

# Setup React Web

Scaffold a React + TypeScript web application with Vite, then layer on this catalog's standard
test/coverage/lint/format/e2e toolchain: Vitest (unit tests, `jsdom`, v8 coverage with lcov),
`@testing-library/react`, ESLint 10 flat config (or the Vite template's own Oxlint, kept by choice) with
`eslint-plugin-react-hooks`, Prettier, Stylelint 17 for CSS, Playwright for a smoke end-to-end test, an
optional Storybook setup, and `sonar-project.properties` when Sonar is enabled. Every step below was proven
against the actual current tooling (Vite 8 / `create-vite` 9.2.1, ESLint 10, Vitest 5, Playwright 1.63,
Stylelint 17, Storybook 10) in a throwaway scaffold — the gotchas called out inline are real, observed
behavior, not speculation.

## Step 0 — Resolve inputs

This skill can be invoked stand-alone (`/iru-setup-react-web`) or driven by another orchestrating skill (e.g.
a future `iru-setup-repository` front door), which resolves these same inputs itself and passes them through
`args` as `key: value` lines, one per line, e.g.:

```
app-name: my-app
description: A React web application.
license: MIT License
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/jane
open-source: yes
sonar: cloud
sonar-organization: example-github
sonar-project-key: example_my-app
sonar-host-url: https://sonarcloud.io
keep-oxlint: no
storybook: no
visibility: public
ci: yes
accessibility: enforce
on-existing: ask
mode: new
```

Parse any such lines from `args` now. Every field found here is resolved — skip asking about it in Step 2.
Only fields genuinely missing from `args` still need a question. If `args` is absent or doesn't look like
this format, treat everything as unset and ask normally.

Recognized keys: `app-name`, `description`, `license`, `developer-name`, `developer-email`,
`organization-url`, `open-source` (`yes`/`no`), `sonar` (`cloud`/`self-hosted`/`none`, plus
`sonar-organization`/`sonar-project-key`/`sonar-host-url` only when `sonar` is `cloud` or `self-hosted`),
`keep-oxlint` (`yes` keeps the Vite template's Oxlint script alongside ESLint, `no` replaces it), `storybook`
(`yes`/`no`), `visibility` (`public`/`private`/`internal` — the GitHub repository's visibility, used only to key
Step 2's Sonar recommendation), `ci` (`yes`/`no` — whether the run invoking this skill generates GitHub Actions
workflows at all; only consulted by Step 2's Sonar question), `accessibility` (`enforce`/`report`/`off`/`none`, default
`enforce` — the automated accessibility level of the UI tests, written to `.ui-quality.yml` in Step 6b),
`on-existing` (`ask`/`keep`/`update`/`replace`,
default `ask` — how Step 1 treats each pre-existing artifact; meant for scripted runs), and `mode`
(`new`/`existing`). There is no `publish`/`distribution` key for this skill.

`mode: existing` marks this run as an **update** of an established repository, but it never means "update
silently": Step 1 still warns and asks per pre-existing artifact unless `on-existing` says otherwise.

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (axe-core and `eslint-plugin-jsx-a11y`), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — semantic landmarks (`header`/`nav`/`main`), accessible names on icon-only buttons, `alt` on images, `rem`/relative font sizes, `prefers-reduced-motion` guards, visible focus — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

## Step 1 — Survey the repository

- If `mode` wasn't supplied via `args`, don't ask it as an isolated question — derive it from whether
  `package.json` already exists at the repository root (absent ⇒ `new`, present ⇒ `existing`).
- Survey every artifact this skill owns: `package.json` (the Vite scaffold), `vitest.config.ts` (or a
  `jest.config.*` — another unit-test setup), `src/test/setup.ts`/`src/App.test.tsx`, an ESLint or Oxlint config
  (`eslint.config.js`, `.oxlintrc.json`), `.prettierrc`/`.prettierignore` (or a `prettier` key), a Stylelint config,
  `playwright.config.ts`/`e2e/`, the UI-contract files (`e2e/support/ui-screenshots.ts`, `playwright/gallery/`,
  `src/App.story.tsx`, `e2e/components/`), `.ui-quality.yml` at the repository root, `.storybook/`,
  `tsconfig.e2e.json` (and its reference in `tsconfig.json`), and `sonar-project.properties`.
- Announce the mode before asking anything else:
  - **Nothing owned exists**: "Scaffolding the React web app **from scratch**." Continue with the placement check
    below.
  - **Anything owned exists** (or `mode: existing`): "**Updating an existing setup** — found: <list with paths>."
    Warn that each one will be handled individually, then resolve one action per existing artifact:
    - **`on-existing` is `keep`/`update`/`replace`**: apply it to every artifact without asking (still print the
      warning).
    - **Otherwise**: ask with `AskUserQuestion`, batching up to 4 artifacts per call (one question each), naming
      any concrete contradiction with this run's choices in the question (e.g. "your `eslint.config.js` has no
      `react-hooks` rules", "a `sonar-project.properties` exists but you chose `sonar: none`"):
      - **Update (Recommended)** — merge: add what's missing and correct outdated parts using this skill's
        template as reference (missing scripts/devDependencies, ignores, the `e2e/**` Vitest exclude, the
        Chromium-only Playwright project, the `tsconfig.e2e.json` reference), keeping everything this skill
        doesn't own. The user reviews a diff; customizations survive, but a customized part this skill owns may be
        rewritten.
      - **Keep as is** — leave it untouched (and skip the install/fix commands that only serve it). Nothing
        customized changes, but it may stay out of date or disagree with this run's choices — Step 10 lists each
        mismatch.
      - **Replace** — regenerate from this skill's template; every customization in it is lost (recoverable only
        from git history). For `package.json` this means re-running `npm create vite@latest` over the existing
        app, which overwrites the template's own files (`src/App.tsx`, `index.html`, …) — say so and never
        recommend it. For a `jest.config.*`, Replace means switching the unit tests to Vitest (Step 4); Keep stays
        on Jest and skips Step 4 entirely (recommend Keep here).
      - **Stop** (first batch only) — end this skill now without changing anything; report this and end here.
    - Defer the `sonar-project.properties` question until Step 2 resolves `sonar`: with `sonar: none`,
      Update/Replace mean removing the file and Keep leaves it as a reported mismatch.
- Steps 3–9 consult these decisions: an absent artifact is created; **Update** merges and shows the diff;
  **Keep as is** skips that artifact (e.g. a kept linter config also skips the `keep-oxlint` question in Step 2,
  using whichever linter exists); **Replace** overwrites it. Step 3's `create-vite` scaffold runs only when there
  is no `package.json` yet or the user chose Replace for it.
- Placement (only when Step 3 will scaffold): check whether the repository root is otherwise empty (ignoring
  dotfiles like `.git`, `.gitignore`, a `LICENSE`, or a `CLAUDE.md`/`README.md`):
  - **Empty**: scaffold `npm create vite@latest . -- --template react-ts` directly into
    the repository root (verified — `create-vite` accepts `.` as the target and infers the `package.json`
    `name` from the current directory's basename when no other name is given). Use the resolved `app-name`
    (Step 2) to override that inferred name afterward if it differs.
  - **Not empty** (e.g. docs or CI files already present but no app scaffolded): ask
    the user with `AskUserQuestion` whether to scaffold into the repository root anyway (accepting that
    `create-vite` scaffolds alongside existing files — it does not require an empty directory, only warns if
    files would be overwritten) or into a subdirectory named after `app-name`.

## Step 2 — Collect identity and options

For any field Step 0 already resolved from `args`, use that value directly. For everything else, ask the
user directly (plain conversation for free text; `AskUserQuestion` for the bounded choices below):

When an existing `package.json` (or app config such as `app.json`/`angular.json`) already supplies an identity
value Step 0 didn't — typical in `mode: existing`, where orchestrators omit identity keys — use it as resolved and
confirm it in one line instead of asking.

- **app-name** — only asked when scaffolding into a subdirectory (Step 1); when scaffolding into the
  repository root, default to the root directory's own basename and only ask if the user wants a different
  `package.json` name.
- **description** — one line, used in `package.json`.
- **Developer name**, **developer email**, **organizationUrl** — for `package.json`'s `author` field.

Then, unless Step 0 already resolved it, ask about the **license** with `AskUserQuestion` (same choices as
every other setup skill in this catalog, for consistency):

- Apache License 2.0 (recommended)
- MIT License
- No license (proprietary / all rights reserved)
- Other — ask for the license's display name directly afterward

If a license is chosen, remind the user in the final report to add a matching `LICENSE` file if one doesn't
exist yet — `iru-check-license` can verify/backfill source headers against it.

Then resolve `open-source` and `sonar` — skip either one Step 0 already resolved:

- **open-source** — is this repository open source? Yes / No.
- **sonar** — "Configure SonarCloud / SonarQube for this project?" The recommendation keys on both `open-source`
  and `visibility`. If `visibility` wasn't supplied via `args`, resolve it only now (only when this question is
  actually asked): `gh repo view --json visibility -q .visibility` when the repository has a GitHub remote
  (lowercase the result and tell the user), otherwise ask **Public** / **Private** (Public recommended when open
  source); `internal` counts as private. If `open-source: yes` but `visibility` is `private`/`internal`, warn about
  the contradiction and ask which is right. Recommend **SonarCloud** (`cloud`) only when the repository is public
  **and** open source; otherwise state that SonarCloud is free only for public open-source projects (per its
  current pricing — a private project needs a paid plan) and recommend **None** (`none`), offering **self-hosted
  SonarQube** as the second option. If `ci: no` was supplied via `args`, say plainly that no CI workflow would send
  reports — analysis would only run when someone runs the scanner manually with a token — and recommend **None**;
  if the user still picks `cloud`/`self-hosted`, write `sonar-project.properties` anyway and say so in Step 10:
  - `cloud` — ask for `sonar.organization` (suggest `<owner>-github`, the owner parsed from
    `git remote get-url origin`), `sonar.projectKey` (suggest `<owner>_<repo>`), and confirm
    `sonar.host.url` defaults to `https://sonarcloud.io`.
  - `self-hosted` — ask for `sonar.host.url` directly, plus `sonar.organization` only if that server has
    organizations enabled, and `sonar.projectKey`.
  - `none` — Step 8 is skipped entirely; no `sonar-project.properties` is written.

Then, unless Step 0 already resolved `keep-oxlint`, ask **once** with `AskUserQuestion` (this is the one
question this skill is required to ask about the lint toolchain, per the current `create-vite` template
shipping Oxlint by default — verified: `npm create vite@latest <name> -- --template react-ts` today
generates `.oxlintrc.json` and a `"lint": "oxlint"` script, not ESLint):

- **Replace Oxlint with ESLint** (recommended — matches this catalog's ESLint-based `iru-typescript-*` gate
  skills, which understand ESLint rule ids, not Oxlint's) — Step 5 removes `.oxlintrc.json`, the `oxlint`
  devDependency, and the `oxlint` script, replacing them with the ESLint flat config below.
- **Keep Oxlint alongside ESLint** — Step 5 adds the ESLint flat config *in addition to* Oxlint, keeping both
  `"lint:oxlint": "oxlint"` and `"lint": "eslint . --max-warnings=0 && stylelint ..."` as separate scripts
  (`iru-typescript-code-quality` already expects this combination when both are configured).

Finally, ask **storybook** (`yes`/`no`, default **No** — it's a heavier, optional add-on) unless Step 0
already resolved it, and — in the same `AskUserQuestion` call — **accessibility** unless Step 0 resolved it:
"Support accessibility and assistive technologies?" — **Enforce (Recommended)** (axe violations fail the UI tests) /
**Report only** (listed, never failing) / **Off** (not run; the coding defaults still apply).

## Step 3 — Scaffold the Vite React app

Run (per Step 1's placement decision):

```bash
npm create vite@latest . -- --template react-ts
```

or, scaffolding into a subdirectory:

```bash
npm create vite@latest <app-name> -- --template react-ts
```

Verified non-interactive as-is — no extra flags (`--yes`, `--no-interactive`) are needed or accepted by the
current `create-vite`; it scaffolds and exits cleanly without prompting as long as `--template react-ts` is
given. This generates (as of `create-vite@9.2.1`, Vite 8, React 19, TypeScript ~6.0):

- `package.json`, `index.html`, `src/` (`App.tsx`, `App.css`, `main.tsx`, `index.css`, `assets/`), `public/`
- `vite.config.ts` (`@vitejs/plugin-react`)
- `tsconfig.json` — **project references only**: `{"files": [], "references": [...]}`, pointing at
  `tsconfig.app.json` (`include: ["src"]`) and `tsconfig.node.json` (`include: ["vite.config.ts"]`). Neither
  referenced project's `noEmit`/strictness applies unless invoked through `tsc -b` (build mode) — see the
  critical gotcha in Step 9.
- `.oxlintrc.json` + `"lint": "oxlint"` in `package.json`'s scripts (this is the template's own linter —
  handled per the `keep-oxlint` choice in Step 5)
- A default `.gitignore` (`node_modules`, `dist`, `dist-ssr`, `*.local`, editor dirs) — leave as-is; nothing
  to add yet (Playwright's own init in Step 6 appends its entries; Storybook, if added in Step 7, appends its
  own `storybook-static` entry as part of its installer).

If `npm install` wasn't already triggered, run it now:

```bash
npm install
```

## Step 4 — Add unit testing (Vitest + Testing Library + jsdom)

Look up current versions at run time (`npm view <package> version`); fall back to the versions verified
below if the registry is unreachable (observed 2026-09-16 — record whatever `npm view` returns as the
actual versions used in the report):

| Package | Fallback version |
|---|---|
| `vitest` | `5.0.1` |
| `@vitest/coverage-v8` | `5.0.1` |
| `@testing-library/react` | `16.3.3` |
| `@testing-library/jest-dom` | `7.0.1` |
| `jsdom` | `30.0.1` |

```bash
npm install -D vitest@<version> @vitest/coverage-v8@<version> @testing-library/react@<version> \
  @testing-library/jest-dom@<version> jsdom@<version>
```

Write `src/test/setup.ts`:

```ts
import '@testing-library/jest-dom/vitest'
```

Write `vitest.config.ts` at the repository root:

```ts
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    // Vitest's default `include` glob also matches Playwright's `e2e/**/*.spec.ts` files (Step 6), which
    // then fail when Vitest tries to run them (Playwright's `test()`/`test.describe()` API isn't Vitest's).
    // Verified: without this exclude, `npm run test`/`npm run coverage` fail with "You are calling test()
    // from an async test.describe() block. Only sync ones are supported." once e2e/ exists.
    exclude: ['e2e/**', 'node_modules/**', 'dist/**'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov'],
      reportsDirectory: 'coverage',
      exclude: ['e2e/**', 'dist/**', '**/*.config.*', 'src/main.tsx'],
    },
  },
})
```

Replace the template's placeholder test with a real one — write `src/App.test.tsx` (adjust the matched text
to whatever the scaffolded `src/App.tsx` actually renders; the current template's heading is "Get started",
not the older "Vite + React"):

```tsx
import { describe, expect, it } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

describe('App', () => {
  it('renders the app shell', () => {
    render(<App />)
    expect(screen.getByText(/get started/i)).toBeInTheDocument()
  })
})
```

Add to `package.json`'s `scripts`: `"test": "vitest run"`, `"coverage": "vitest run --coverage"`.

Verified: `npm run coverage` produces `coverage/lcov.info` plus an HTML report (`coverage/lcov-report/`) —
exclude `coverage/` from Prettier/Stylelint (Step 5) and from `.gitignore` if not already covered by `dist`.

## Step 5 — Add linting and formatting

### ESLint (or Oxlint — per the `keep-oxlint` choice from Step 2)

Look up current versions; fall back to those verified below:

| Package | Fallback version |
|---|---|
| `eslint` | `10.10.0` |
| `@eslint/js` | `10.0.1` |
| `typescript-eslint` | `8.70.0` |
| `eslint-config-prettier` | `10.1.8` |
| `eslint-plugin-react-hooks` | `7.1.1` |
| `eslint-plugin-react-refresh` | `0.5.7` |
| `globals` | `17.12.0` |

```bash
npm install -D eslint@<version> @eslint/js@<version> typescript-eslint@<version> \
  eslint-config-prettier@<version> eslint-plugin-react-hooks@<version> \
  eslint-plugin-react-refresh@<version> globals@<version>
```

Write `eslint.config.js`:

```js
import js from '@eslint/js'
import reactHooks from 'eslint-plugin-react-hooks'
import reactRefresh from 'eslint-plugin-react-refresh'
import eslintConfigPrettier from 'eslint-config-prettier'
import globals from 'globals'
import tseslint from 'typescript-eslint'

export default tseslint.config(
  { ignores: ['dist', 'coverage', 'e2e/**', 'playwright/**', 'playwright-report', 'storybook-static'] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      ecmaVersion: 2023,
      globals: globals.browser,
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': ['warn', { allowConstantExport: true }],
    },
  },
  eslintConfigPrettier,
)
```

**If `keep-oxlint: no`** (replace): delete `.oxlintrc.json`, remove the `oxlint` devDependency
(`npm uninstall oxlint`), and set `package.json`'s `"lint"` script to
`"eslint . --max-warnings=0 && stylelint \"src/**/*.css\""` (Stylelint appended below).

**If `keep-oxlint: yes`** (keep alongside): leave `.oxlintrc.json` and the `oxlint` devDependency as-is, add
`"lint:oxlint": "oxlint"`, and set `"lint"` to
`"eslint . --max-warnings=0 && oxlint && stylelint \"src/**/*.css\""`.

Verified clean (`npx eslint .` exits 0) against the untouched scaffold from Step 3 once these rules are in
place — no template code needs changing to satisfy them.

### Prettier

Look up the current version (fallback `3.9.7`):

```bash
npm install -D prettier@<version>
```

Write `.prettierrc`:

```json
{
  "semi": false,
  "singleQuote": true,
  "printWidth": 100
}
```

Write `.prettierignore`:

```
coverage
dist
e2e/**
playwright/**
playwright-report
storybook-static
```

Add scripts: `"format": "prettier --check ."`, and run `npx prettier --write .` once now so the scaffolded
files (which are **not** pre-formatted to this config — the template ships with semicolons, this config
turns them off) pass `format` immediately instead of failing on the first CI run.

### Stylelint (CSS)

Look up current versions (fallback `stylelint@17.15.0`, `stylelint-config-standard@40.0.0`):

```bash
npm install -D stylelint@<version> stylelint-config-standard@<version>
```

Write `.stylelintrc.json`:

```json
{
  "extends": ["stylelint-config-standard"],
  "ignoreFiles": ["dist/**", "coverage/**", "storybook-static/**"]
}
```

**Critical gotcha, verified**: `stylelint-config-standard` 40's modern-notation rules
(`color-function-notation`, `alpha-value-notation`, `media-feature-range-notation`,
`color-function-alias-notation`) flag the Vite template's own `src/App.css`/`src/index.css` out of the box
(53 errors observed on a completely untouched scaffold — old-style `rgba(0,0,0,.1)`, `@media (min-width:
...)`, etc.). Always run once right after writing the config, before reporting success:

```bash
npx stylelint "src/**/*.css" --fix
```

This autofixes every one of the observed violations with no manual changes needed. Re-run
`npx stylelint "src/**/*.css"` afterward to confirm zero remaining errors before moving on — if any remain
(a rule `--fix` can't auto-resolve), report them rather than silently leaving the lint script red for the
user's first run.

Finally, run `npx prettier --write .` again (Stylelint's `--fix` reformats the CSS files it touched, which
can disagree with Prettier's own formatting) and confirm `npm run format` passes.

## Step 6 — Add Playwright end-to-end tests

Look up the current version (fallback `1.63.0` for both `@playwright/test`/`playwright`):

```bash
npm init playwright@latest -- --quiet --lang ts --no-browsers
```

Verified non-interactive flags for the *current* `create-playwright` CLI (1.17.x) — **`--gha=false` is not
valid** (it errors `unknown option '--gha=false'`; `--gha` is a bare boolean flag, not `key=value` — omit it
entirely to skip generating a GitHub Actions workflow, since this catalog's own
`iru-setup-typescript-github-workflows` skill covers CI). `--lang ts` (not `TypeScript`) is accepted as-is.
`--no-browsers` skips downloading browser binaries here — Step 6's verification sub-task installs Chromium
separately, and so should a real run of this skill (see below).

This installs `@playwright/test`, writes `playwright.config.ts`, and scaffolds a `tests/` directory with a
placeholder test that hits `https://playwright.dev/` — none of which match this skill's target shape. Fix
both:

1. **Rename `tests/` to `e2e/`** and delete the placeholder `tests/example.spec.ts` (or its `e2e/` copy after
   the rename).
2. **Edit `playwright.config.ts`**:
   - `testDir: './e2e'` (was `'./tests'`).
   - Set `use.baseURL: 'http://localhost:4173'` (Vite's `preview` default port).
   - Add a `webServer` block so `npm run e2e` builds and serves the app itself rather than requiring a
     server already running:
     ```ts
     webServer: {
       command: 'npm run build && npm run preview',
       url: 'http://localhost:4173',
       reuseExistingServer: !process.env.CI,
     },
     ```
   - Trim the `projects` array to Chromium only — the default template lists `chromium`, `firefox`, and
     `webkit`, but only Chromium is what gets installed below (and by this skill's own verification
     sub-task); leaving the other two in place makes `npm run e2e` report 2 failures out of the box with
     "Executable doesn't exist" until the user separately runs `npx playwright install firefox webkit`:
     ```ts
     /* Chromium only by default — this is what `npx playwright install --with-deps chromium` provisions
        in CI. Add `firefox`/`webkit` projects (and install those browsers) if cross-browser coverage is
        needed. */
     projects: [
       {
         name: 'chromium',
         use: { ...devices['Desktop Chrome'] },
       },
     ],
     ```

Write `e2e/smoke.spec.ts` — a real smoke test against the scaffolded app rather than an external site:

```ts
import { expect, test } from '@playwright/test'

test('home page renders the app shell', async ({ page }) => {
  await page.goto('/')
  await expect(page.getByRole('heading', { name: /get started/i })).toBeVisible()
})
```

Add to `package.json`'s `scripts`: `"e2e": "playwright test"`.

Install the Chromium browser binary now so the smoke test can actually run:

```bash
npx playwright install --with-deps chromium
```

Verified: on macOS this succeeds without sudo (`--with-deps` is effectively a no-op for system packages on
macOS). On Linux, `--with-deps` needs `sudo`/root to install OS packages via `apt`; if it fails for that
reason, fall back to `npx playwright install chromium` (browser binary only, no OS deps) and note in the
report that CI images (e.g. `mcr.microsoft.com/playwright` or the official GitHub Actions runners, which
already have the OS deps) won't hit this at all.

Run `npm run e2e` and confirm the smoke test passes before reporting success.

Playwright's own installer appends `/test-results/`, `/playwright-report/`, `/blob-report/`,
`/playwright/.cache/`, `/playwright/.auth/` to `.gitignore` automatically — no extra `.gitignore` edit
needed here.

## Step 6b — UI contract: component gallery, screenshots and accessibility

The catalog's UI contract (repeated in `iru-typescript-code-one-task/reference/ui-contract.md`) makes every
component and screen test capture its states into `<repo root>/.ui-screenshots/<kind>/<Id>/<state>--<direction>--<theme>.png`
and run an automated accessibility check at the level `.ui-quality.yml` sets. This step makes the scaffold ready for
it. Component tests use Playwright's built-in `mount()` fixture (since `@playwright/test` 1.62 — the old
`@playwright/experimental-ct-react` package is frozen at 1.62 and no longer updated): a `components` project whose
`baseURL` is a gallery page served by Vite's own dev server. Verified on Vite 8 / React 19 / Playwright 1.64.1 /
`@axe-core/playwright` 4.14.0: both specs below pass and produce the eight captures.

1. **`.ui-quality.yml`** at the repository root (not the app subdirectory), exactly this shape, with `accessibility`
   from Step 0/2:

   ```yaml
   # .ui-quality.yml — at the repository root; written by the iru-setup-* scaffolds, read by the coding and test skills.
   accessibility: enforce      # enforce: violations fail the UI tests | report: listed, never failing | off: not run | none: opted out entirely
   directions: [ltr, rtl]      # screenshot matrix directions
   themes: [light, dark]       # screenshot matrix themes
   ```

   An existing file follows Step 1's decision: **Update** sets only `accessibility` (when `args` supplied it) and adds
   missing keys, keeping the user's `directions`/`themes`; **Keep as is** leaves it (report a mismatch with this
   run's `accessibility`); **Replace** rewrites it.

2. **Dependency** — look up the current version (fallback `4.14.0`): `npm install -D @axe-core/playwright@<version>`.
   Confirm `@playwright/test` is ≥ 1.62 (Step 6's install); otherwise `mount()` doesn't exist.

3. **The shared helper** — write `e2e/support/ui-screenshots.ts` with exactly the content of this skill's
   `reference/ui-screenshots.ts` (screenshot directory from `UI_SCREENSHOTS_DIR` else `<repo root>/.ui-screenshots`,
   `.ui-quality.yml` reader, contract file names, `captureUiMatrix`, `checkAccessibility`). `e2e/**` is already
   excluded from ESLint/Prettier/Vitest (Steps 4–5).

4. **The gallery** — `playwright/gallery/index.html`:

   ```html
   <!doctype html>
   <html lang="en">
     <head>
       <meta charset="UTF-8" />
       <meta name="viewport" content="width=device-width, initial-scale=1.0" />
       <title>Component gallery</title>
     </head>
     <body>
       <main id="root"></main>
       <script type="module" src="./main.tsx"></script>
     </body>
   </html>
   ```

   and `playwright/gallery/main.tsx`:

   ```tsx
   // Component gallery for Playwright's built-in `mount()` fixture: renders one `*.story.tsx` export into #root.
   import { StrictMode, type ComponentType } from 'react'
   import { flushSync } from 'react-dom'
   import { createRoot, type Root } from 'react-dom/client'
   import '../../src/index.css'

   type StoryModule = Record<string, ComponentType<Record<string, unknown>>>
   const stories = import.meta.glob<StoryModule>('../../src/**/*.story.tsx')
   const idOf = (file: string): string => file.replace(/^(\.\.\/)+src\//, '').replace(/\.story\.tsx$/, '')

   async function resolve(storyId: string): Promise<ComponentType<Record<string, unknown>> | undefined> {
     const sep = storyId.lastIndexOf('/')
     const [storyPath, exportName] = [storyId.slice(0, sep), storyId.slice(sep + 1)]
     const file = Object.keys(stories).find((f) => idOf(f) === storyPath || idOf(f).endsWith(`/${storyPath}`))
     return file ? (await stories[file]())[exportName] : undefined
   }

   const rootElement = document.getElementById('root') as HTMLElement
   let root: Root | undefined

   interface MountParams {
     readonly story: string
     readonly props?: Record<string, unknown>
   }

   Object.assign(window, {
     mount: async ({ story, props }: MountParams): Promise<void> => {
       const Story = await resolve(story)
       if (!Story) throw new Error(`Unknown story: ${story}`)
       root ??= createRoot(rootElement) // reused, so update() reconciles and keeps state
       flushSync(() =>
         root?.render(
           <StrictMode>
             <Story {...props} />
           </StrictMode>,
         ),
       )
     },
     unmount: async (): Promise<void> => {
       root?.unmount()
       root = undefined
     },
   })
   ```

   `vite build` ignores it (it only builds `index.html`'s graph). ESLint and Prettier ignore `playwright/**` (Step 5's
   templates); it is type-checked by `tsconfig.e2e.json` (Step 9).

5. **A story for the sample screen** — `src/App.story.tsx` (Vite's template exports `App` as default):

   ```tsx
   import App from './App'

   /** The app shell as first rendered. */
   export const Default = () => <App />
   ```

   and `react-refresh/only-export-components` is fine with it (a story file has no fast-refresh boundary to keep).

6. **`playwright.config.ts`** — add the `components` project in front of the Chromium one, give the Chromium
   project `testIgnore: 'components/**'` and its own `baseURL`, and turn `webServer` into an array (the gallery's
   dev server, then the existing preview server):

   ```ts
   projects: [
     {
       name: 'components',
       testDir: './e2e/components',
       use: {
         ...devices['Desktop Chrome'],
         baseURL: 'http://localhost:5173/playwright/gallery/index.html',
         serviceWorkers: 'block',
         reuseContext: true,
       },
     },
     {
       name: 'chromium',
       testIgnore: 'components/**',
       use: { ...devices['Desktop Chrome'], baseURL: 'http://localhost:4173' },
     },
   ],
   webServer: [
     {
       command: 'npm run dev -- --port 5173 --strictPort',
       url: 'http://localhost:5173/playwright/gallery/index.html',
       reuseExistingServer: !process.env.CI,
     },
     {
       command: 'npm run build && npm run preview -- --port 4173 --strictPort',
       url: 'http://localhost:4173',
       reuseExistingServer: !process.env.CI,
     },
   ],
   ```

7. **The sample screen spec** — `e2e/components/App.spec.ts` (behaviour once, then the matrix with axe in every
   cell):

   ```ts
   import { expect, test } from '@playwright/test'
   import { captureUiMatrix } from '../support/ui-screenshots'

   test('App counts clicks', async ({ mount }) => {
     const app = await mount('App/Default')
     await app.getByRole('button', { name: /count is 0/i }).click()
     await expect(app.getByRole('button', { name: /count is 1/i })).toBeVisible()
   })

   test('App default state across the matrix', async ({ page, mount }, testInfo) => {
     await captureUiMatrix(page, { kind: 'screen', id: 'App', state: 'default' }, () => mount('App/Default'), {
       accessibility: { testInfo, include: '#root' },
     })
   })
   ```

   Keep `e2e/smoke.spec.ts` (Step 6) as the flow-level smoke test against the built app.

8. **Make the template pass its own checks.** Verified on `create-vite` 9.2.1:
   - **Contrast** — the template's light-theme `--accent: #aa3bff` on its counter button fails axe's
     `color-contrast` (3.82:1, needs 4.5:1). In `src/index.css` change the light value to `--accent: #7e22ce` (the
     dark-theme `#c084fc` passes). With `accessibility: enforce` the spec fails until this is done.
   - **Logical properties** — `src/App.css` uses physical edges, so right-to-left captures don't mirror. Replace
     `text-align: left` → `text-align: start`, `border-right` → `border-inline-end` (both occurrences),
     `left: 0` → `inset-inline-start: 0`, `right: 0` → `inset-inline-end: 0`, `border-left-color` →
     `border-inline-start-color`, `border-right-color` → `border-inline-end-color`; then
     `grep -nE '(^|[ :;-])(left|right)\b' src/*.css` should list nothing, and re-run Stylelint/Prettier (Step 5).

9. **`eslint-plugin-jsx-a11y` is not added**: its latest release (6.10.2) declares `eslint` peers only up to `^9`,
   so it can't install next to this skill's ESLint 10 without `--legacy-peer-deps`. Axe in the UI tests is the
   automated check; say so in Step 10. If the user later pins ESLint 9, `jsxA11y.flatConfigs.recommended` is the
   flat config to add.

Run `npm run e2e` again — both projects (`components` and `chromium`) must pass, and
`.ui-screenshots/screen/App/` must hold `default--ltr--light.png`, `default--ltr--dark.png`,
`default--rtl--light.png` and `default--rtl--dark.png`. `.ui-screenshots/` belongs in `.gitignore` —
`iru-setup-typescript-gitignore` adds it; when this skill runs standalone, append it (with the comment
`# UI test screenshots (.ui-screenshots/), regenerated on every UI test run`) yourself.

## Step 7 — Optional Storybook

Only run this step if `storybook: yes` was resolved in Step 2.

Look up the current version (fallback `10.6.0` for `storybook`/`@storybook/react-vite`):

```bash
npm create storybook@latest -- --yes --no-dev --type react --builder vite --disable-telemetry \
  --package-manager npm
```

Verified non-interactive: `--yes` answers every prompt, `--no-dev` skips launching the dev server after
install, `--disable-telemetry` avoids the telemetry prompt. This installs `storybook` plus a cluster of
addons (`@storybook/addon-a11y`, `@storybook/addon-docs`, `@storybook/addon-vitest`, `@chromatic-com/storybook`,
`@storybook/addon-mcp`), scaffolds `.storybook/` (`main.ts`, `preview.tsx`), and adds `"storybook": "storybook
dev -p 6006"` / `"build-storybook": "storybook build"` scripts.

**Important, verified interaction**: `@storybook/addon-vitest`'s installer *rewrites* `vitest.config.ts` from
Step 4 into a multi-`projects` config — it keeps the existing `jsdom` unit-test setup as one project
(`extends: true`) and adds a second `storybook` project that runs stories as browser-mode tests via
`@vitest/browser-playwright` (which needs its own Playwright browser install, separate from Step 6's
`e2e/`). This means:

- `npm run test`/`npm run coverage` (still `vitest run [--coverage]` with no `--project` filter) now execute
  **both** projects — the unit project plus the browser-mode Storybook project — which is slower and needs
  Playwright browsers installed for Storybook's own use, not just Step 6's `e2e/` smoke test.
- If that combined run isn't wanted (e.g. the unit-only `coverage` gate should stay fast and
  browser-install-free), scope the scripts explicitly instead: `"test": "vitest run --project=unit"`,
  `"coverage": "vitest run --project=unit --coverage"`, and add a separate `"test:storybook": "vitest run
  --project=storybook"` script the user can opt into.
- Re-run `npm run format`/`npm run lint` after this step — the addon-vitest installer's rewritten
  `vitest.config.ts` is not Prettier-formatted to this project's `.prettierrc`.

Because this step substantially reshapes the test config, treat it as genuinely optional (default **No** in
Step 2) and call out in the report exactly what it changed, including whichever of the two script-scoping
options above was applied.

## Step 8 — `sonar-project.properties`

Only run this step if `sonar` resolved to `cloud` or `self-hosted` in Step 2. Write
`sonar-project.properties` at the repository root:

```properties
sonar.organization=<sonar-organization>
sonar.projectKey=<sonar-project-key>
sonar.host.url=<sonar-host-url>
sonar.sources=src
sonar.tests=src
sonar.test.inclusions=**/*.test.tsx,**/*.test.ts
sonar.exclusions=**/e2e/**,**/dist/**
sonar.javascript.lcov.reportPaths=coverage/lcov.info
```

**Placeholder resolution:**

| Placeholder | Resolved from |
|---|---|
| `<sonar-organization>` | Step 2's `sonar-organization` answer (omit the whole line if `sonar: self-hosted` and the server has no organizations enabled) |
| `<sonar-project-key>` | Step 2's `sonar-project-key` answer |
| `<sonar-host-url>` | Step 2's `sonar-host-url` answer (`https://sonarcloud.io` for `cloud`) |

`sonar.tests=src` (not a separate `test/` directory) because tests are colocated with source
(`src/App.test.tsx` next to `src/App.tsx`) — `sonar.test.inclusions` is what actually tells Sonar which of
the files under `sonar.sources` are tests rather than production code. `sonar.exclusions` keeps `e2e/` (a
different test type, reported separately if at all) and the build output out of the main scan.

If `sonar: none`, skip this step entirely and note in the report that Sonar was deliberately not wired up.

## Step 9 — Wire up npm scripts and final `tsconfig` fix

By this point `package.json`'s `scripts` should read (module-manager-agnostic — every command below is
`npm run <script>`):

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "test": "vitest run",
    "coverage": "vitest run --coverage",
    "lint": "eslint . --max-warnings=0 && stylelint \"src/**/*.css\"",
    "format": "prettier --check .",
    "typecheck": "tsc -b",
    "e2e": "playwright test"
  }
}
```

(Adjust `lint` per the `keep-oxlint` choice from Step 5, and `test`/`coverage` per Storybook's project-scoping
note in Step 7 if Storybook was added.)

**Critical gotcha, verified — do this unconditionally**: the scaffolded root `tsconfig.json` is
project-references-only (`{"files": [], "references": [...]}`). Running `tsc --noEmit` directly at the root
**silently exits 0 without checking anything** — `files: []` means there is nothing in the root project
itself to check, and plain `tsc` does not follow `references` the way `tsc -b` (build mode) does. Verified by
injecting a real type error into `src/App.tsx`: `npx tsc --noEmit` at the root reported nothing and exited 0,
while `npx tsc -b` correctly caught it. **Always use `"typecheck": "tsc -b"`, never `"typecheck": "tsc
--noEmit"`, for this template's `tsconfig.json` shape.**

A second, related gotcha: neither `tsconfig.app.json` (`include: ["src"]`) nor `tsconfig.node.json`
(`include: ["vite.config.ts"]`) covers `e2e/` or `playwright.config.ts` from Step 6 — `tsc -b` silently skips
type-checking them too. Add a third referenced project. Write `tsconfig.e2e.json`:

```json
{
  "compilerOptions": {
    "tsBuildInfoFile": "./node_modules/.tmp/tsconfig.e2e.tsbuildinfo",
    "target": "es2023",
    "lib": ["ES2023", "DOM", "DOM.Iterable"],
    "types": ["node", "vite/client"],
    "skipLibCheck": true,
    "module": "preserve",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "noEmit": true,
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["e2e", "playwright.config.ts", "playwright/gallery"]
}
```

`DOM`, `vite/client`, `jsx` and `bundler` resolution are there for Step 6b's files: the gallery is browser code
using `import.meta.glob`, specs import story types from `src/`, and with `nodenext` every relative import in a spec
would need an explicit `.js` extension (verified: `TS2835` on `'./support/ui-screenshots'`). Verified with `tsc -b` on TypeScript 6.0 — the e2e project, gallery and stories all
type-check.

And add it as a third reference in `tsconfig.json`:

```json
{
  "files": [],
  "references": [
    { "path": "./tsconfig.app.json" },
    { "path": "./tsconfig.node.json" },
    { "path": "./tsconfig.e2e.json" }
  ]
}
```

Verified: without this third project, injecting the same kind of type error into `e2e/smoke.spec.ts` was
*not* caught by `tsc -b`, `npm run build`, or `npm run e2e` (Playwright's own TS transform strips types
without checking them) — the error would only ever surface in an editor. With `tsconfig.e2e.json` referenced,
`tsc -b` catches it as expected.

Run the full sequence once, in order, before reporting success — this is exactly what Step 9.2 of this
skill's own verification exercised:

```bash
npm run typecheck && npm run lint && npm run format && npm run test && npm run coverage \
  && npm run build && npm run e2e
```

## Step 10 — Report

Start by repeating the mode announced in Step 1 (**scaffolded from scratch** or **updated an existing setup**).
Summarize what was generated: the app name and location (repository root or subdirectory), the license chosen (or
"none"), and, per owned artifact, the action actually taken — **created / updated / replaced / kept as is /
removed**. For every kept artifact, list each mismatch with this run's choices (e.g. a `sonar-project.properties`
left after `sonar: none`, a Playwright config still listing Firefox/WebKit).

State explicitly what was included versus omitted, and why:

- **`open-source`**: yes/no, as resolved in Step 2.
- **Linter**: ESLint only (Oxlint removed) or ESLint + Oxlint kept alongside, per the `keep-oxlint` choice —
  name which `package.json` scripts run which tool.
- **`sonar`**: `cloud`/`self-hosted`/`none` — if `cloud`/`self-hosted`, `sonar-project.properties` was
  written with the resolved organization/project key/host URL; if `none`, note that this is expected when
  the repository isn't public and open source (SonarCloud is free only for public open-source projects) unless
  the user explicitly chose it. State the `visibility` used and where it came from (`args`, `gh`, or the user);
  if `ci: no` was supplied and Sonar was still configured, say no CI step sends reports.
- **`storybook`**: yes/no — if yes, call out the `vitest.config.ts` project-split from Step 7 and which
  script-scoping option (combined vs. `--project=unit`/`--project=storybook`) was applied.
- **UI contract** (Step 6b): `.ui-quality.yml` with its action (**created / updated / replaced / kept as is**) and
  the `accessibility` level written; the helper, gallery, story and spec files written; the screenshot count
  produced by the verification run; the template contrast/logical-property fixes applied; and that
  `eslint-plugin-jsx-a11y` was deliberately not added (ESLint 10 peer range).

Then report each verification command actually run and its result (typecheck, lint, format, unit test,
coverage — including the `coverage/lcov.info` path — build, e2e), and explicitly flag the two `tsconfig`
gotchas from Step 9 (`tsc -b` vs. `tsc --noEmit`; the `tsconfig.e2e.json` third project) as something to
preserve if the user or another tool later "simplifies" the TypeScript config.

Finish with an explicit **Warn explicitly** block:

- **Review every generated file before committing** — `package.json`'s `author`/`description`, the license
  text, and the Sonar organization/project key (if set) should all be double-checked.
- **`sonar: cloud`/`self-hosted`** was chosen: a `SONAR_TOKEN` repository secret and an actual
  SonarCloud/SonarQube project matching `sonar.projectKey` still need to exist before a CI-run Sonar scan
  (typically via `iru-setup-typescript-github-workflows`) will succeed.
- **Playwright's browser binaries** were installed locally for verification (`npx playwright install
  --with-deps chromium`) — CI will need the same step (or a Playwright-provided Docker image) before `npm run
  e2e` can run there; on Linux runners without root, use `npx playwright install chromium` (binary only) if
  `--with-deps` fails.
- If a license was chosen and no `LICENSE` file exists yet, suggest `iru-check-license` to generate one and
  backfill source headers.
- If Storybook was added, remind the user that `npm run storybook` starts a dev server on port 6006 and
  `npm run build-storybook` produces `storybook-static/` — neither is wired into this skill's own `build`
  script, by design. `iru-setup-typescript-github-workflows` (with `docs-tool: storybook`) runs
  `npm run build-storybook` by that exact name in `build.yml` and merges `storybook-static/` under the Antora
  site, so keep the installer's script name as-is rather than renaming/aliasing it to `docs`.
