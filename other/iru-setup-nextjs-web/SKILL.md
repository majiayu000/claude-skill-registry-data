---
name: iru-setup-nextjs-web
description: >-
  Scaffold a new Next.js web application with `npx create-next-app@<latest>` driven entirely by explicit flags
  (TypeScript, App or Pages Router, ESLint, Tailwind or CSS Modules, `src/`, `@/*` alias, package manager, React
  Compiler off, Cache Components on or off, AGENTS.md — saved create-next-app preferences can never leak in), or
  bring an existing Next.js app up to this catalog's toolchain, then post-process it — `0.1.0-dev.0` version, the
  shared npm script names the workflows skill calls (`lint` = ESLint flat config with `eslint-config-next` since
  `next lint` is gone, `format`/`format:check` = Prettier, `typecheck` = `next typegen && tsc --noEmit`, `test`/
  `coverage` = Vitest + React Testing Library + jsdom with an 80% v8 threshold and lcov at `coverage/lcov.info`,
  `test:e2e` = Playwright against the production build, `build`, `start`, `docs` = TypeDoc), `output: 'export'`
  with `basePath` from `PAGES_BASE_PATH` for GitHub Pages or a server build (`output: 'standalone'` plus a
  non-root multi-stage `Dockerfile` with a health-check route when the image is distributed), a tested sample
  feature that follows the `iru-nextjs-code-one-task` references (async Server Component page with a
  `server-only` data layer, Client Component leaf, Server Action with Zod validation and an auth stub, Route
  Handlers, metadata, `loading`/`error`/`not-found`, all adapted to static export or the Pages Router), per the
  catalog's UI contract a `.ui-quality.yml` at the repository root and — with `e2e: playwright` — a Playwright
  component-testing project against a standalone Vite component gallery (Playwright's built-in `mount()` fixture,
  `next/link`/`next/navigation`/`next/image` stand-ins), `@axe-core/playwright`, the shared
  `e2e/support/ui-screenshots.ts` helper, and specs capturing `.ui-screenshots/component/LikeButton/` and
  `.ui-screenshots/screen/Home/` across left-to-right/right-to-left × light/dark with an accessibility check, and
  `sonar-project.properties` when Sonar is enabled. Invoke as `/iru-setup-nextjs-web`. Accepts pre-resolved inputs
  via `args` (`key: value` lines) — `app-name`, `description`, `license`, `developer-name`, `developer-email`,
  `organization-url`, `open-source`, `sonar` (+ `sonar-organization`/`sonar-project-key`/`sonar-host-url`),
  `router` (`app`/`pages`), `output` (`server`/`static`), `cache-components` (`yes`/`no`), `styling`
  (`tailwind`/`css-modules`), `e2e` (`playwright`/`none`), `distribution` (`none`/`internal`), `docs-tool`
  (`typedoc`/`none`), `agents-md` (`yes`/`no`), `package-manager` (`npm`/`pnpm`/`yarn`), `node-version`,
  `visibility`, `ci`, `accessibility` (`enforce`/`report`/`off`/`none`, default `enforce`), `mode` (`new`/`existing`),
  `on-existing` (`ask`/`keep`/`update`/`replace`) — and asks
  whatever `args` didn't resolve. Announces whether it is scaffolding from scratch or updating an existing app and,
  for every artifact it owns that already exists, asks Update / Keep as is / Replace (or Stop). Use whenever a
  repository needs a Next.js app bootstrapped with its full test/lint/e2e/deploy toolchain from this house
  template, instead of running `create-next-app` and wiring the rest by hand.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(npx *) Bash(npm *) Bash(pnpm *) Bash(yarn *) Bash(node *) Bash(docker *) Bash(curl *) Bash(git *) Bash(gh repo view *) Bash(mktemp *) Bash(mv *) Bash(cp *) Bash(rm *) Bash(mkdir *) Bash(ls *) Bash(find *) Bash(grep *) Bash(cat *) Bash(test *) Bash(command -v *) Bash(head *) Bash(date *)
---

# Setup Next.js Web

Scaffold a Next.js + TypeScript application with `create-next-app`, then layer on this catalog's standard
toolchain: Vitest + React Testing Library + jsdom (v8 coverage, 80% thresholds, lcov), ESLint flat config with
`eslint-config-next` + Prettier, `next typegen && tsc --noEmit` type checking, Playwright against the production
build, TypeDoc, a GitHub Pages–ready static export or a container-ready server build, and a sample feature that is
the living example of the `iru-nextjs-code-one-task` references. Every template below was generated and run in
throwaway scaffolds (`create-next-app` 16.4.0, Next.js 16.4.0, React 19.3, Node 24, npm 11, Vitest 5.0.4,
Playwright 1.63, TypeDoc 0.28) in five combinations — App Router server (previous caching model, with Docker),
App Router server with Cache Components, App Router static export, Pages Router server (with Docker), and Pages
Router static export. The gotchas called out inline are observed behavior.

The templates live in `reference/` next to this file, each introduced by a `File: \`<path>\` — when: <tags>` line
(write it only when every tag applies):

- `reference/config-templates.md` — `next.config.ts`, Vitest, ESLint, Prettier, Playwright, TypeDoc, Sonar,
  `Dockerfile`, `.dockerignore`.
- `reference/app-router-samples.md` — the App Router sample feature, its unit tests, and its Playwright specs, plus
  the route table each variant must produce.
- `reference/pages-router-samples.md` — the same feature for `router: pages`.

## Step 0 — Resolve inputs

This skill runs stand-alone (`/iru-setup-nextjs-web`) or driven by `iru-setup-typescript-repository` (flavor
`nextjs`), which resolves inputs once and passes them through `args` as `key: value` lines, e.g.:

```
app-name: bookshelf
description: A web catalogue of books.
license: Apache License 2.0
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/jane
open-source: yes
sonar: cloud
sonar-organization: jane-github
sonar-project-key: jane_bookshelf
sonar-host-url: https://sonarcloud.io
output: server
e2e: playwright
distribution: internal
package-manager: npm
node-version: 24
visibility: public
ci: yes
accessibility: enforce
mode: new
```

Parse any such lines now; every key found is resolved and its question in Step 2 is skipped. If `args` is absent
or not in this format, treat everything as unset.

Recognized keys:

| Key | Values | Default when not asked |
|---|---|---|
| `app-name`, `description`, `license`, `developer-name`, `developer-email`, `organization-url` | free text | asked (Step 2) |
| `open-source` | `yes`/`no` | asked |
| `sonar` (+ `sonar-organization`, `sonar-project-key`, `sonar-host-url`) | `cloud`/`self-hosted`/`none` | asked |
| `router` | `app`/`pages` | `app` |
| `output` | `server`/`static` | asked |
| `cache-components` | `yes`/`no` | `no` (asked only for `router: app` + `output: server`) |
| `styling` | `tailwind`/`css-modules` | `tailwind` |
| `e2e` | `playwright`/`none` | `playwright` |
| `distribution` | `none`/`internal` | asked for `output: server`; always `none` for `static` |
| `docs-tool` | `typedoc`/`none` | asked (TypeDoc recommended) |
| `agents-md` | `yes`/`no` | `yes` |
| `package-manager` | `npm`/`pnpm`/`yarn` | lockfile present, else `npm` |
| `node-version` | Node major | `24` (current LTS) — the `Dockerfile`'s `NODE_VERSION` |
| `visibility` | `public`/`private`/`internal` | resolved only if the Sonar question is asked |
| `ci` | `yes`/`no` | `yes` (only consulted for the Sonar recommendation) |
| `accessibility` | `enforce`/`report`/`off`/`none` | asked with `e2e: playwright`, else `enforce` — the UI tests' automated accessibility level written to `.ui-quality.yml` |
| `mode` | `new`/`existing` | derived in Step 1 |
| `on-existing` | `ask`/`keep`/`update`/`replace` | `ask` |

The orchestrator forwards `router`, `cache-components`, and `styling` only when they reached it through its own
`args`; their defaults above are therefore what most runs use, and Step 2 asks only `cache-components` (and only
when it matters). `pages` (GitHub Pages yes/no) is not a key of this skill: a static export is always built
Pages-ready (`basePath` from `PAGES_BASE_PATH`), and whether it gets deployed is the workflows skill's decision.

Contradictions are resolved, not obeyed, and reported in Step 10:

- `output: static` + `cache-components: yes` → `no`: a static export has no server to stream dynamic holes, and
  every route must prerender as `○`/`●`.
- `output: static` + `distribution: internal` → `none`: there is no server to containerize; the export is the
  artifact.
- `router: pages` + `cache-components: yes` → `no`: Cache Components is an App Router feature.

`mode: existing` marks the run as an update, but never means "update silently": Step 1 still asks per artifact
unless `on-existing` says otherwise.

**Accessibility level `none` and assistive-technology templates.** `accessibility` takes `enforce`, `report`, `off` or
`none` (UI contract §8; the stand-alone question gains a fourth option, **None — opt out entirely**, e.g. a mandated
non-compliant design). With `none`: write `accessibility: none` to `.ui-quality.yml`, do not install or configure the
accessibility test tooling (axe-core in the Playwright tests and `eslint-plugin-jsx-a11y`), and omit the accessibility-specific attributes from the generated templates.
With `enforce`, `report` or `off`: include the assistive-technology attributes from the contract's §8 platform
subsections in every generated template — semantic landmarks, accessible names on icon-only buttons, `alt` on images (`next/image`), `rem`/relative font sizes, `prefers-reduced-motion` guards, visible focus — and, for `enforce`/`report` only, the automated checks. In
`mode: existing`, a prior `.ui-quality.yml` follows this skill's existing Update / Keep / Replace prompt and its
`accessibility` value is never silently flipped (**Update** sets it only when `args` supplied it).

## Step 1 — Survey the repository

- If `mode` wasn't supplied, derive it: `package.json` with `next` in `dependencies` at the repository root ⇒
  `existing`, otherwise `new`. A `package.json` **without** `next` is a different project — stop and ask whether
  to scaffold into a subdirectory instead.
- Survey every artifact this skill owns: `package.json` (the Next.js app itself — `src/app` or `src/pages`),
  `next.config.*`, `vitest.config.*`/`vitest.setup.ts` (or a `jest.config.*` — another runner),
  `eslint.config.*` (or `biome.json`), `.prettierrc*`/`.prettierignore`, `playwright.config.*` + `e2e/`,
  `typedoc.json`, `sonar-project.properties`, `Dockerfile`/`.dockerignore`, the UI-contract files
  (`.ui-quality.yml` at the repository root, `e2e/support/ui-screenshots.ts`, `playwright/`, `e2e/components/`), and
  the sample feature (`src/lib/books.ts` and its routes).
- For an existing app, detect what it already is instead of asking: router (`src/app`/`app` ⇒ `app`,
  `src/pages`/`pages` only ⇒ `pages`), `output` (`'export'` ⇒ `static`, else `server`), `cacheComponents: true` ⇒
  `cache-components: yes`, styling (`tailwindcss` dependency ⇒ `tailwind`), `src/` or root layout, import alias
  from `tsconfig.json` `paths`. Use those as resolved values and never change them as a side effect (Step 2 only
  confirms them in one line). An app without `src/` keeps its layout — adjust every template path (`src/app/...` →
  `app/...`) and the Vitest `include`/coverage globs accordingly.
- Announce the mode before asking anything else:
  - **Nothing owned exists**: "Scaffolding the Next.js app **from scratch**."
  - **Anything owned exists** (or `mode: existing`): "**Updating an existing setup** — found: <list with paths>."
    Then resolve one action per existing artifact:
    - **`on-existing` is `keep`/`update`/`replace`**: apply it to every artifact without asking (still print the
      list).
    - **Otherwise**: ask with `AskUserQuestion`, up to 4 artifacts per call, naming any concrete contradiction with
      this run's choices (e.g. "`next.config.ts` has no `output: 'export'` but you chose `output: static`", "the
      `lint` script still runs `next lint`, which Next.js 16 removed", "a `sonar-project.properties` exists but
      you chose `sonar: none`"):
      - **Update (Recommended)** — merge: add what's missing and correct outdated parts using the templates
        (missing scripts/devDependencies, the coverage `include`/`exclude` and thresholds, the `server-only` and
        `next/navigation` mocks, `globalIgnores`, the Chromium-only production-build `webServer`), keeping
        everything else. The user sees a diff; customizations survive, but a customized part this skill owns may be
        rewritten.
      - **Keep as is** — leave it untouched and skip the commands that only serve it. It may stay out of date or
        disagree with this run's choices — Step 10 lists each mismatch.
      - **Replace** — regenerate from the template; customizations in it are lost (recoverable only from git). For
        `package.json` this means re-running `create-next-app` over the app, which overwrites `src/app/layout.tsx`,
        `page.tsx`, `globals.css` — say so and never recommend it. For a `jest.config.*`, Replace means switching to
        Vitest (Step 5); Keep stays on Jest and skips Step 5 (recommend Keep — the gate skills support both).
      - **Stop** (first batch only) — end without changing anything; report that and end here.
    - Defer the `sonar-project.properties` question until Step 2 resolves `sonar` (with `sonar: none`,
      Update/Replace mean removing it), and the `Dockerfile` question until `distribution` is resolved.
    - The **sample feature** is only written on a scaffold-from-scratch run (or when the user explicitly asks for
      it on an update): never drop sample routes into an existing app's URL space.
- Placement (only when Step 3 will scaffold). `create-next-app` refuses a non-empty target directory unless
  every entry is on its own allow-list (verified in 16.4: `.git`, `.gitignore`, `.gitattributes`, `.claude`,
  `.idea`, `.vscode`, `.zed`, `.cursor`, `.yarn`, `LICENSE`, `docs`, `mkdocs.yml`, `.npmignore`, `*.iml`, `.DS_Store`,
  `Thumbs.db`, plus log files) — a `README.md`, `CLAUDE.md`, `.github/`, or `CHANGELOG.md` makes it print "The
  directory … contains files that could conflict" and exit.
  - **Only allow-listed entries**: scaffold into `.` directly. If a `.gitignore` exists, copy it aside first —
    the generated one replaces it — and merge the two afterwards (keep every existing line, append the template's
    missing ones).
  - **Anything else present**: ask with `AskUserQuestion` — **Scaffold into the repository root** (Recommended
    for a repository that exists for this app) or **Scaffold into a subdirectory named `<app-name>`**. For the
    root, scaffold into a temporary directory (`mktemp -d`) with `--skip-install`, then move every generated entry
    into the root **except** ones that already exist there (merge `.gitignore` as above; keep the existing
    `README.md`/`CLAUDE.md` — `iru-setup-readme` owns the README; when `agents-md: yes` and a `CLAUDE.md` exists,
    append one `@AGENTS.md` line to it instead of replacing it), delete the temporary directory, and run the
    package manager's install in the root.

## Step 2 — Collect identity and options

Use every value Step 0 or Step 1 already resolved; when an existing `package.json` supplies an identity value,
confirm it in one line instead of asking.

- **app-name** — the `package.json` `name` (lowercase, URL-safe; also the container image name the workflows
  skill derives). Default: the target directory's basename.
- **app-title** — not a key: the human-readable name used in metadata and TypeDoc (`<App title>` in the
  templates). Derive it from `app-name` (`bookshelf-web` → "Bookshelf Web") and confirm in one line.
- **description**, **developer name**, **developer email**, **organization URL** — for `package.json`
  (`description`, `author`).
- **license** (`AskUserQuestion`, same choices as every setup skill): Apache License 2.0 (recommended), MIT License,
  No license (proprietary), Other (ask its name). Remind in Step 10 to add a `LICENSE` file if missing.
- **open-source** — Yes / No.
- **sonar** — "Configure SonarCloud / SonarQube for this project?" Same rule as `iru-setup-react-web`: resolve
  `visibility` only now if missing (`gh repo view --json visibility -q .visibility`, lowercased; otherwise ask
  Public/Private; `internal` counts as private; flag open source + private as contradictory). Recommend `cloud`
  only for a public open-source repository (SonarCloud is free only for those), otherwise `none` with
  `self-hosted` as the second option; with `ci: no` recommend `none` (no CI would send reports) and, if Sonar is
  still chosen, say so in Step 10. `cloud` asks `sonar-organization` (suggest `<owner>-github` from
  `git remote get-url origin`), `sonar-project-key` (suggest `<owner>_<repo>`), host `https://sonarcloud.io`;
  `self-hosted` asks the host URL, the project key, and an organization only if that server uses them.
- **output** (`AskUserQuestion`):
  - **Server** (Recommended unless the site is purely static content) — `next build` + `next start`; Server
    Actions, Route Handlers, ISR, request-time rendering all available.
  - **Static export** — `output: 'export'` to `out/`, hostable on GitHub Pages or any file host; no Server
    Actions, no request-time APIs, no dynamic Route Handlers, no proxy/middleware, no ISR, no image optimization —
    every route must prerender (`○`/`●`). The sample feature is adapted accordingly (Step 7).
- **cache-components** (only `router: app` + `output: server`; `AskUserQuestion`): **No — previous model**
  (Recommended: nothing is cached unless asked, route segment config works, every guide and library assumes it)
  or **Yes — Cache Components** (`'use cache'` + `cacheLife`/`cacheTag`, Partial Prerendering by default; every
  request-time read must sit under `<Suspense>` or `next build` fails). Name the consequence for later tasks:
  `iru-nextjs-code-one-task` applies the `16-prev` or `16-cc` profile from this choice.
- **distribution** (only `output: server`): **None** (the app is deployed by your own pipeline from the repository)
  or **Internal** (a container image pushed to GHCR by the release workflow — this step writes `output:
  'standalone'`, a `Dockerfile`, a `.dockerignore`, and a health-check route). There is no `store` value.
- **docs-tool**: **TypeDoc** (Recommended — `npm run docs` writes `docs/api`, which the workflows skill merges
  under the Antora site; also lets `iru-typescript-tsdoc` verify instead of running audit-only) or **None**.

- **accessibility** (only with `e2e: playwright`; `AskUserQuestion`): "Support accessibility and assistive technologies?" — **Enforce (Recommended)** (axe violations fail the UI tests) / **Report only** (listed, never failing) /
  **Off** (not run; the coding defaults still apply).

Do not ask `router`, `styling`, `e2e`, `agents-md`, or `package-manager` unless the user brings them up — their
defaults (`app`, `tailwind`, `playwright`, `yes`, detected/`npm`) are the house template.

## Step 3 — Scaffold with `create-next-app`

Resolve the version live (`npm view create-next-app version`; it is released in lockstep with `next`) and pass
**every** choice as an explicit flag, including the negative ones:

```bash
npx --yes create-next-app@<version> <target> \
  --ts --eslint --src-dir --import-alias "@/*" \
  <--app | --no-app> \
  <--tailwind | --no-tailwind> \
  <--cache-components | --no-cache-components> \
  --no-react-compiler \
  <--agents-md | --no-agents-md> \
  --no-agent-feedback \
  <--use-npm | --use-pnpm | --use-yarn> \
  --disable-git --yes [--skip-install]
```

| Choice | Flag |
|---|---|
| `router: app` / `pages` | `--app` / `--no-app` |
| `styling: tailwind` / `css-modules` | `--tailwind` / `--no-tailwind` (the starter then uses `page.module.css`) |
| `cache-components: yes` / `no` | `--cache-components` / `--no-cache-components` |
| `agents-md: yes` / `no` | `--agents-md` / `--no-agents-md` |
| `package-manager` | `--use-npm` / `--use-pnpm` / `--use-yarn` |

Why every flag is explicit (verified against `create-next-app` 16.4.0's own source and `--help`):

- **`--yes` fills every unprovided option from the user's saved preferences, else from built-in defaults — and the
  built-in default for Cache Components is ON** (`cacheComponents: true` in its defaults object). A bare
  `create-next-app --yes` therefore produces a Cache Components project. The CLI honors an explicit
  `--no-<option>` over both (it checks `argv` for `--no-cache-components`, `--no-tailwind`, `--no-app`,
  `--no-src-dir`, `--no-react-compiler`, `--no-agents-md`, `--no-eslint`, `--no-linter`, `--no-import-alias`), so
  passing every flag makes saved preferences irrelevant. `--yes` is kept only so a flag added by a future release
  never blocks on a prompt.
- **Never pass `--reset-preferences`**: it deletes the user's saved preferences (a global file outside the
  repository) and then exits without scaffolding.
- `--disable-git`: the repository is the user's; `create-next-app` must not `git init` or commit.
- `--no-agent-feedback`: skips the opt-in feedback prompt added in 16.4.
- Turbopack is the default bundler — don't pass `--webpack`/`--rspack`. `--turbopack` is no longer in `--help`.
- `--ts`, `--eslint`, `--src-dir`, `--import-alias "@/*"` are house constants. Biome (`--biome`) is supported by the
  gate skills but not by this template.

Non-interactive as written (verified with stdin closed). What 16.4.0 generates for `--app --tailwind --src-dir`:
`src/app/{layout.tsx,page.tsx,globals.css,favicon.ico}`, `public/*.svg`, `next.config.ts` (with a `turbopack.rules`
block wiring `@tailwindcss/turbopack` for `*.css` — new in 16.4, replacing `postcss.config.mjs`),
`eslint.config.mjs` (flat config), `tsconfig.json` (strict, `"@/*": ["./src/*"]`, includes `.next/types`),
`AGENTS.md` (no `CLAUDE.md` in 16.4, despite older docs), a `.gitignore`, and `package.json` with `next`/`react`
pinned exactly, `eslint` `^9`, and **`@types/node` `^20`**. `--no-app` writes `src/pages/{_app,_document,index}.tsx`,
`src/pages/api/hello.ts`, and `src/styles/`. It also runs `next typegen` after installing.

`npm` 11.19+ prints `install-scripts … not yet covered by allowScripts: unrs-resolver` during the install — that
package (an `eslint-config-next` dependency) ships a prebuilt binary and works without its postinstall; mention it,
don't act on it.

## Step 4 — Identity, version, `next.config.ts`, starter cleanup

1. `package.json`: set `name` (Step 2), `description`, `author` (`"<name> <<email>> (<url>)"`), `license` (SPDX id,
   or `"UNLICENSED"` for proprietary), and **`version: "0.1.0-dev.0"`** — the `x.y.z-dev.N` development version
   `iru-typescript-bump-version` and the workflows skill's `sync.yml` maintain. Keep `"private": true` (an app is
   never published to npm).
2. `next.config.ts`: write the variant from `reference/config-templates.md` for the resolved `output`/
   `distribution`, **merging in every key `create-next-app` wrote** — the Tailwind `turbopack.rules` block,
   `cacheComponents: true` + `partialPrefetching: true` (Cache Components), and `reactStrictMode: true` (Pages
   Router). For `output: static` the template reads `basePath` from **`PAGES_BASE_PATH`** (empty when unset — the
   workflows skill's Pages deploy job sets it from `actions/configure-pages`), sets `images: { unoptimized: true }`
   and `trailingSlash: true`, and exposes the base path as `NEXT_PUBLIC_BASE_PATH`. Verified: with
   `PAGES_BASE_PATH=/my-repo npm run build`, `out/index.html` links `/my-repo/books/` and loads
   `/my-repo/_next/static/...`.
3. Root layout (`router: app`): replace the starter's `metadata` export with site-wide defaults and give the layout
   one-line TSDoc (TypeDoc's strict run flags both otherwise); keep its fonts and classes as generated:

   ```tsx
   /** Absolute origin used to resolve Open Graph and canonical URLs. */
   const siteUrl = process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000";

   /** Site-wide metadata defaults; pages override `title` and `description`. */
   export const metadata: Metadata = {
     metadataBase: new URL(siteUrl),
     title: { default: "<App title>", template: "%s | <App title>" },
     description: "<description>",
     openGraph: { siteName: "<App title>", type: "website" },
   };
   ```

   and prefix `export default function RootLayout` with `/** Root layout: the \`<html>\`/\`<body>\` shell around
   every page. */`.
4. Starter cleanup (scaffold-from-scratch only): the starter `src/app/page.tsx` (or `src/pages/index.tsx`) is
   replaced by the sample in Step 7; delete `src/app/page.module.css` (`styling: css-modules`),
   `src/pages/api/hello.ts` and `src/styles/Home.module.css` (Pages Router). Keep `public/` and `globals.css`.
5. Runtime dependencies for the sample (latest via `npm view <pkg> version`; fallbacks verified 2026-10-13):
   `router: app` → `server-only` (`0.0.1`); `router: app` + `output: server` → also `zod` (`4.6.7`). The Pages
   Router samples need neither (`server-only` breaks modules shared with `pages/`).

## Step 5 — Unit tests: Vitest + React Testing Library + jsdom

Dev dependencies — latest via `npm view <pkg> version`, fallbacks observed 2026-10-13:

| Package | Fallback | Note |
|---|---|---|
| `vitest`, `@vitest/coverage-v8` | `5.0.4` | same version for both |
| `vite` | `8.3.4` | declared explicitly; otherwise only present as a peer of the plugin |
| `@vitejs/plugin-react` | `6.1.2` | |
| `jsdom` | `30.1.2` | |
| `@testing-library/react` / `dom` / `jest-dom` / `user-event` | `16.3.3` / `10.4.2` / `7.0.1` / `14.6.8` | |
| `@types/node` | `^24` (the Node LTS major) | **required**: see below |

**Critical gotcha, verified**: Vitest 5 declares `peerDependencies["@types/node"]: "^22.0.0 || >=24.0.0"`, and
`create-next-app` scaffolds `@types/node@^20` — installing Vitest 5 alone fails with npm `ERESOLVE`. Install
`@types/node@^<node-version>` (24 by default) **in the same command** as Vitest. Don't fall back to Vitest 4 to
dodge it.

```bash
npm install -D @types/node@^24 vitest@<v> @vitest/coverage-v8@<v> vite@<v> @vitejs/plugin-react@<v> jsdom@<v> \
  @testing-library/react@<v> @testing-library/dom@<v> @testing-library/jest-dom@<v> @testing-library/user-event@<v>
```

Write `vitest.config.mts` and `vitest.setup.ts` from `reference/config-templates.md`. Notes that matter:

- `.mts` keeps the config ESM regardless of `package.json` `"type"` (Next.js projects must not set
  `"type": "commonjs"`). `resolve: { tsconfigPaths: true }` resolves `@/*` natively on Vite 8 — no plugin.
- `include: ["src/**/*.test.{ts,tsx}"]` keeps Playwright's `e2e/*.spec.ts` out of Vitest (Playwright's `test()`
  fails inside Vitest).
- The setup file mocks `server-only` (the real module throws outside a React Server environment) and the
  `next/navigation` client hooks, keeping the real `notFound()`/`redirect()` so tests can assert their `digest`.
- Server-side tests (data layer, Server Actions, Route Handlers) start with `// @vitest-environment node`.
  `connection()`, `cookies()`, `headers()`, `revalidatePath()`/`updateTag()` and `cacheLife()`/`cacheTag()` throw
  outside a request — verified: `connection` was called outside a request scope — so each test mocks exactly the
  `next/server`/`next/headers`/`next/cache` functions its module imports.
- Coverage: `include: ["src/**/*.{ts,tsx}"]` (so untested files show up at 0% instead of disappearing), excluding
  tests, `*.d.ts`, and the framework wiring jsdom can't render (`src/app/layout.tsx` with `next/font` and
  `<html>`, `src/pages/_app.tsx`, `src/pages/_document.tsx`); reporters `text`, `lcov` (`coverage/lcov.info` for
  Sonar/CI) and `json-summary` (`coverage/coverage-summary.json`, which `iru-typescript-coverage` reads first);
  thresholds 80% for lines/branches/functions/statements so `npm run coverage` itself fails below the gate.

Scripts: `"test": "vitest run"`, `"coverage": "vitest run --coverage"`.

## Step 6 — Lint and format

`next lint` was removed in Next.js 16 and `next build` no longer lints: linting is the ESLint CLI over the flat
config. Keep the scaffold's `eslint` (`^9`; `eslint-config-next` 16.4 peers on `eslint >=9`) and
`eslint-config-next` (pinned to the `next` version), add Prettier and `eslint-config-prettier`
(fallbacks `3.9.10` / `10.1.8`):

```bash
npm install -D prettier@<v> eslint-config-prettier@<v>
```

Write `eslint.config.mjs`, `.prettierrc.json`, and `.prettierignore` from `reference/config-templates.md`. The
ESLint config keeps `eslint-config-next/core-web-vitals` + `/typescript` and the scaffold's `globalIgnores`, adds
`eslint-config-prettier/flat` last, and ignores coverage/Playwright/TypeDoc output. `.prettierignore` lists
`AGENTS.md`/`CLAUDE.md`: `next dev` rewrites its agent-rules block there, so formatting it only produces churn.

Scripts: `"lint": "eslint --max-warnings=0"`, `"format": "prettier --write ."`, `"format:check": "prettier
--check ."`, `"typecheck": "next typegen && tsc --noEmit"`.

`typecheck` must run `next typegen` first: App Router code uses the global `PageProps`/`LayoutProps`/`RouteContext`
helpers generated into `.next/types`, and a clean checkout fails `tsc` with `TS2304: Cannot find name
'LayoutProps'` without it. The scaffold's single `tsconfig.json` includes `**/*.ts`, `**/*.tsx`, `**/*.mts`, so
`e2e/`, `playwright.config.ts`, and `vitest.config.mts` are type-checked too — no project references needed
(unlike the Vite template).

Run `npx prettier --write .` once after Step 7 so the generated files match `.prettierrc.json`.

## Step 7 — Sample feature and Playwright

Write the sample files from `reference/app-router-samples.md` (`router: app`) or
`reference/pages-router-samples.md` (`router: pages`) whose `when:` tags match the run. What the App Router sample
demonstrates, per variant:

| Piece | `server` | `static` |
|---|---|---|
| `src/lib/books.ts` | `server-only` data layer returning DTOs; `16-cc`: `'use cache'` + `cacheLife("hours")` + `cacheTag` | same (previous model), read at build time |
| `src/lib/session.ts` | auth stub (`React.cache`, demo user — replace before shipping) | — |
| `src/app/books/actions.ts` + `add-book-form.tsx` | Server Action: authenticate → Zod `safeParse` → write → `revalidatePath` (prev) / `updateTag` (cc); `useActionState` form | — (static export has no Server Actions) |
| `src/components/like-button.tsx` | Client Component leaf | same |
| `src/app/books/page.tsx`, `[id]/page.tsx` | async Server Components, `metadata`/`generateMetadata`, `generateStaticParams`, `notFound()` | same, plus `dynamicParams = false` |
| `loading.tsx`, `error.tsx` (`retry` prop, stable since 16.3), `not-found.tsx` | yes | yes |
| Route Handlers | `GET /api/books/[id]` (`RouteContext`, 401/400/404) and `GET /api/health` (`connection()`, `no-store`) | `GET /books.json` with `dynamic = "force-static"` |

Every source file has a colocated `*.test.ts(x)` exercising it — async Server Components are called as functions
and their result rendered, Server Actions are called with `FormData` including the anonymous and invalid cases,
Route Handlers are called with `new Request(...)` and a `RouteContext`. The suite reaches 100% lines and ≥94%
branches in every verified variant.

### Playwright (`e2e: playwright`)

Add `@playwright/test` (latest; fallback `1.64.0`) and, for `output: static`, `serve` (fallback `14.2.6`) as dev
dependencies. Write `playwright.config.ts` and `e2e/books.spec.ts` from the templates. Don't run
`npm init playwright` — its template (three browsers, `tests/` against an external site, no `webServer`) needs more
undoing than writing the file.

- The `webServer` runs the **production** build on port 3100: `npm run build && npm run start -- --port 3100`
  for `server`, `npm run build && npm run start -- --listen 3100` for `static` (where `"start": "serve out"`).
  `reuseExistingServer: !process.env.CI` — under `CI` it never attaches to a dev server.
- `output: server` + `distribution: internal`: `next start` prints `⚠ "next start" does not work with "output:
  standalone" configuration. Use "node .next/standalone/server.js" instead.` — verified harmless (the server
  starts and every spec passes); the container runs `node server.js` itself.
- Specs locate by role/name, never a bare `getByRole("alert")` (Next injects a route announcer with that role).
- Install the browser so the suite can run: `npx playwright install --with-deps chromium` (on Linux without root,
  `npx playwright install chromium`). Each Playwright release pins its own Chromium build — a newer
  `@playwright/test` with only an older browser cached fails with `Executable doesn't exist at
  …/chromium_headless_shell-<rev>`; that is an environment gap to report, not a test failure.

Scripts: `"test:e2e": "playwright test"`; for `output: static` also `"start": "serve out"`.

### UI contract

The catalog's UI contract (repeated in `iru-nextjs-code-one-task/reference/ui-contract.md`) makes every component
and screen test capture its states into `<repo root>/.ui-screenshots/<kind>/<Id>/<state>--<direction>--<theme>.png`
and run axe at the level `.ui-quality.yml` sets. Write `.ui-quality.yml` at the repository root on every run
(also with `e2e: none` — the coding skills read it); an existing one follows Step 1's decision (**Update** sets only
`accessibility` when `args` supplied it and adds missing keys). With `e2e: playwright`, also write everything under
"UI contract" in `reference/config-templates.md`:

- dev dependencies `@axe-core/playwright` (fallback `4.14.0`), `vite` (the major Vitest already uses), and
  `@tailwindcss/vite` for `styling: tailwind` (`@vitejs/plugin-react` is already there from Step 5);
- `e2e/support/ui-screenshots.ts` from this skill's `reference/ui-screenshots.ts`;
- the component gallery (`playwright/vite.config.ts`, `playwright/gallery/{index.html,main.tsx,next-stubs.tsx,
  next-image.tsx}`) — Playwright's component testing is a plain project whose `baseURL` is a gallery page driven by
  the built-in `mount()` fixture (`@playwright/test` ≥ 1.62; `@playwright/experimental-ct-react` is frozen), and
  Next.js has no Vite server to host it, so it gets its own on port 3200; only Client Components (and synchronous,
  `server-only`-free presentational components) can be storied;
- the `components` project + gallery `webServer` entry in `playwright.config.ts`;
- `src/components/like-button.story.tsx`, `e2e/components/like-button.spec.ts`, and `e2e/home.spec.ts` (a screen
  capture of `/`, deterministic unlike the book list the Server Action spec mutates).

`playwright/` is excluded from ESLint/Prettier (`reference/config-templates.md`'s lint templates) and type-checked
by `tsc --noEmit` through the default `**/*.tsx` include (the gallery's `/// <reference types="vite/client" />`
covers `import.meta.glob`). The sample book list stays a small server-rendered list: it is bounded seed data, so the
contract's server pagination isn't needed there. Verified: `CI=1 npm run test:e2e` writes
`component/LikeButton/default--{ltr,rtl}--{light,dark}.png` and `screen/Home/default--…` with axe clean in both
themes.

Append Playwright's output to `.gitignore` if missing (`/test-results/`, `/playwright-report/`, `/blob-report/`,
`/playwright/.cache/`), `.ui-screenshots/` (with the comment `# UI test screenshots, regenerated on every UI test
run`), plus `/docs/api/` (TypeDoc) and `.integration-test.lock/` (the lock
`iru-nextjs-code-one-task-group` takes before `next build`/Playwright). `iru-setup-typescript-gitignore` maintains
the full file when the orchestrator runs it.

## Step 8 — TypeDoc, Sonar, container image

- **`docs-tool: typedoc`**: install `typedoc` (fallback `0.28.20`), write `typedoc.json`, add
  `"docs": "next typegen && typedoc"` (output `docs/api`, the path the workflows skill merges under the Antora
  site). Verified: `npm run docs` builds, and the gate's strict run
  (`npx typedoc --emit none --treatWarningsAsErrors --validation.notDocumented true --disableGit
  --disableSources`) exits 0 on every variant — the samples document every exported symbol, property, and union
  member for exactly that reason.
- **`sonar` ≠ `none`**: write `sonar-project.properties` from the template (placeholders from Step 2; tests are
  colocated, so `sonar.tests=src` + `sonar.test.inclusions`). With `sonar: none` write nothing and say so.
- **`distribution: internal`** (server only): `output: 'standalone'` is already in `next.config.ts` (Step 4); write
  `Dockerfile` and `.dockerignore` from the template with `NODE_VERSION` = `node-version`. Multi-stage
  (`deps` → `builder` → `runner` on `node:<node-version>-slim`), the standalone server plus `public/` and
  `.next/static`, owned by and running as the image's non-root `node` user, `HEALTHCHECK` calling
  `/api/health` with Node's built-in `fetch` (no `curl` in the slim image). The image name the release workflow
  pushes is the `package.json` `name` without scope, lowercased — keep `name` valid for that.

## Step 9 — Scripts and full verification

`package.json` `scripts` end up as (replace `npm run` with the chosen package manager's runner everywhere):

| Script | Command |
|---|---|
| `dev` | `next dev` (scaffold) |
| `build` | `next build` (scaffold) |
| `start` | `next start` (`server`) / `serve out` (`static`) |
| `lint` | `eslint --max-warnings=0` |
| `format` | `prettier --write .` |
| `format:check` | `prettier --check .` |
| `typecheck` | `next typegen && tsc --noEmit` |
| `test` | `vitest run` |
| `coverage` | `vitest run --coverage` |
| `test:e2e` | `playwright test` (`e2e: playwright`) |
| `docs` | `next typegen && typedoc` (`docs-tool: typedoc`) |

These are the names `iru-setup-typescript-github-workflows` calls for the `nextjs` flavor and the gate skills
(`iru-typescript-test` with its `e2e` selector, `iru-typescript-coverage`, `iru-typescript-code-quality`,
`iru-typescript-tsdoc`) detect. Never rename them.

Run, in order, and fix anything red before reporting success:

```bash
npm run lint && npm run format:check && npm run typecheck && npm run test && npm run coverage && npm run build
```

Then:

- **Route table**: compare `next build`'s table with the variant's expected table in the samples reference
  (e.g. `server` + `prev`: `○ /`, `○ /books`, `● /books/1`, `● /books/2`, `ƒ /api/books/[id]`, `ƒ /api/health`;
  Cache Components adds `◐ /books/[id]` and Revalidate `1h` / Expire `1d` columns; `static`: only `○`/`●`). A
  mismatch is a finding, not something to paper over.
- **`e2e: playwright`**: `CI=1 npm run test:e2e` (its `webServer` runs the production build itself).
- **`distribution: internal`**: if `docker info` succeeds, `docker build -t <app-name>:verify .`, run it on a free
  port, wait for `docker inspect -f '{{.State.Health.Status}}'` to report `healthy`, `curl` `/api/health` and
  `/books`, confirm `docker exec <container> id` is not root, then remove the container and image. Without a
  Docker daemon, report the image as **unverified** — never as built.
- **`docs-tool: typedoc`**: `npm run docs`.

## Step 10 — Report

Start with the mode from Step 1 (**scaffolded from scratch** or **updated an existing setup**), then the app name,
location (root or subdirectory), license, `create-next-app`/`next` versions used, and per owned artifact the action
taken — **created / updated / replaced / kept as is / removed** — with every mismatch a kept artifact has with this
run's choices.

State the resolved options and where each came from (`args`, detected, asked, default): `router`, `output`,
`cache-components` (and therefore the coding profile `16-prev`/`16-cc` later tasks will use), `styling`, `e2e`,
`distribution`, `docs-tool`, `package-manager`, `node-version`, `open-source`, `sonar` (+ `visibility` and its
source), and every contradiction Step 0 resolved (e.g. "`cache-components: yes` ignored: static export").

Report each verification command and its result: lint, format check, typecheck, unit tests (count), coverage
(lines/branches, `coverage/lcov.info`), build with the route table, Playwright (count, or why it couldn't run —
e.g. a missing browser build) with the screenshot count under `.ui-screenshots/` and any accessibility violation
rule ids, TypeDoc, Docker build/health/non-root (or "unverified: no Docker daemon"). Also report `.ui-quality.yml`
with its action (**created / updated / replaced / kept as is**) and the `accessibility` level written.

Finish with **Warn explicitly**:

- Review every generated file before committing — `package.json` `author`/`description`/`license`, metadata
  title/description, Sonar keys.
- **`src/lib/session.ts` is a stub that treats every caller as signed in.** Replace it with real authentication
  before deploying anything with Server Actions or authenticated Route Handlers; the actions and handlers already
  handle a `null` session.
- The in-memory book store resets on every server restart and is per-instance — it exists to prove the stack;
  replace or delete the sample feature (`src/lib/books.ts`, `src/app/books/`, `src/app/api/books/`, `e2e/`).
- `output: static`: the app is built for GitHub Pages with `basePath` from `PAGES_BASE_PATH`; `next/image` `src`
  strings and raw `public/` URLs need `process.env.NEXT_PUBLIC_BASE_PATH` prefixed manually. Server Actions,
  request-time APIs, middleware/proxy, and ISR will fail the build if added later.
- `distribution: internal`: multi-instance deployments need the same `NEXT_SERVER_ACTIONS_ENCRYPTION_KEY` at build
  time on every instance; set `NEXT_PUBLIC_SITE_URL` at build time for correct Open Graph URLs.
- `sonar: cloud`/`self-hosted`: a `SONAR_TOKEN` secret and a matching project must exist before CI analysis works.
- Playwright browsers were installed locally; CI needs `npx playwright install --with-deps chromium` (the workflows
  skill's template does it).
- If a license was chosen and no `LICENSE` exists, suggest `iru-check-license`.

## Verification notes

Exercised in `$TMPDIR/iru-verify/ts-setup/nextjs/` on 2026-10-13 with `create-next-app` 16.4.0 / `next` 16.4.0 /
React 19.3.0, Node 24.20, npm 11.19, Vitest 5.0.4, `@vitest/coverage-v8` 5.0.4, Vite 8.3.4, jsdom 30.1.2, ESLint 9
+ `eslint-config-next` 16.4.0, Prettier 3.9.10, TypeDoc 0.28.20, Zod 4.6.7, Docker 29.8:

| Variant | lint / format / typecheck / test / coverage / build | Playwright | Docker |
|---|---|---|---|
| App, server, previous model, Tailwind, `internal`, TypeDoc, Sonar | all pass; 25 tests, 100% lines / 94% branches; table as documented | 5/5 | built, `healthy`, runs as `node` (uid 1000), `/books/999` → 404 |
| App, server, Cache Components, Tailwind | all pass; table shows `◐ /books/[id]`, `1h`/`1d` | 5/5 (Server Action + `updateTag` read-your-own-writes) | n/a |
| App, static export, CSS Modules, TypeDoc, Sonar | all pass; only `○`/`●`; `PAGES_BASE_PATH=/my-repo` prefixes links and assets | 4/4 (`serve out`) | n/a |
| Pages, server, CSS Modules, `internal` | all pass; `● /books` with `1m` revalidate | 3/3 (404 status asserted) | built, `healthy` |
| Pages, static export, Tailwind | all pass | 2/2 | n/a |

Playwright ran on **1.63.0** because only that release's Chromium build was cached locally (1.64.0 needs
`chromium_headless_shell-1248`, which was not downloaded); the configs and specs are version-independent. Not
verified: `pnpm`/`yarn` (scaffold flags and the `Dockerfile` variants), `styling: css-modules` with the Docker
image, `create-next-app --biome`, Next.js 15 or older (this skill always scaffolds the latest), and anything on a
Linux CI runner (the workflows skill covers that).
