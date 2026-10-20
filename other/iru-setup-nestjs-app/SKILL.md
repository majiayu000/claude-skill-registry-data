---
name: iru-setup-nestjs-app
description: >-
  Scaffold a new NestJS 12 service with the Nest CLI (`nest new` for ESM + Vitest, the default, or the application
  schematic with `--type=cjs` for CommonJS + Jest), generated in a temporary directory and copied into the
  repository without overwriting anything, or bring an existing NestJS app up to this catalog's toolchain, then
  post-process it — `0.1.0-dev.0` version, the shared npm script names the workflows skill calls (`lint` = Oxlint
  `--type-aware`, `format`/`format:check` = Prettier, `typecheck` = `tsc --noEmit`, `test` = unit suite, `coverage`
  = unit coverage with an 80% threshold, `*.module.ts`/`main.ts`/generated code excluded, lcov at
  `coverage/lcov.info`, `test:e2e`, `build`, `start`, `docs` = Compodoc or TypeDoc), `ConfigModule` validated by a
  Zod schema, a global `ValidationPipe` registered as `APP_PIPE`, a shared `configureApp()` (security headers,
  shutdown hooks) used by `main.ts` and the e2e tests, `@nestjs/terminus` liveness/readiness endpoints, a tested
  sample feature module that follows the `iru-nestjs-code-one-task` references, optional persistence (`orm`
  TypeORM / Prisma 7 with a driver adapter / Mongoose 9 / Drizzle, with migrations) with Testcontainers-backed e2e
  tests, a multi-stage non-root `Dockerfile` with a health check, `.env.example`, and `sonar-project.properties`
  when Sonar is enabled. Invoke as `/iru-setup-nestjs-app`. Accepts pre-resolved inputs via `args` (`key: value`
  lines) — `app-name`, `description`, `license`, `developer-name`, `developer-email`, `organization-url`,
  `open-source` (`yes`/`no`), `sonar` (`cloud`/`self-hosted`/`none`, plus `sonar-organization`/`sonar-project-key`/
  `sonar-host-url`), `orm` (`none`/`typeorm`/`prisma`/`mongoose`/`drizzle`), `database` (`postgresql`/`mysql`/
  `mongodb`, only when `orm` is not `none`), `distribution` (`none`/`internal` — `internal` means the workflows
  push the image to GHCR; the `Dockerfile` is written either way), `package-manager` (`npm`/`pnpm`/`yarn`),
  `node-version` (the `Dockerfile` base image's Node major, default `24`), `visibility` (`public`/`private`/
  `internal`), `ci` (`yes`/`no`), `mode` (`new`/`existing`), `on-existing` (`ask`/`keep`/`update`/`replace`),
  `module-system` (`esm`/`cjs`), `http` (`express`/`fastify`), and `docs-tool` (`compodoc`/`typedoc`/`none`) — so
  an orchestrating skill (`iru-setup-typescript-repository`) can supply them without re-prompting; invoked
  stand-alone it asks whatever `args` didn't resolve. Announces whether it is scaffolding from scratch or updating
  an existing app; for every artifact it owns that already exists, warns and asks Update (merge, keep
  customizations) / Keep as is / Replace (regenerate from the template), explaining each option's consequences.
  Use whenever a repository needs a NestJS backend service bootstrapped with its full test/lint/e2e/container
  toolchain from this house template, instead of running `nest new` and wiring the rest by hand.
model: sonnet
allowed-tools: Read Write Edit AskUserQuestion Bash(npx *) Bash(npm *) Bash(pnpm *) Bash(yarn *) Bash(node *) Bash(docker *) Bash(curl *) Bash(git *) Bash(gh repo view *) Bash(mktemp *) Bash(rsync *) Bash(mv *) Bash(cp *) Bash(rm *) Bash(mkdir *) Bash(ls *) Bash(find *) Bash(grep *) Bash(cat *) Bash(test *) Bash(command -v *) Bash(head *) Bash(date *) Bash(sleep *)
---

# Setup NestJS App

Scaffold a NestJS 12 service with the Nest CLI, then layer on this catalog's standard toolchain and a small,
real, tested application skeleton: validated configuration, global validation, shared bootstrap setup, health
checks, one sample feature module, optional persistence with migrations, Testcontainers e2e tests, a production
container image, and Sonar configuration. Everything in this skill and its `reference/` files was proven against
the actual current tooling (`@nestjs/cli` 12.0.8, Nest 12.1.3, TypeScript 6.0, Vitest 4.1, Jest 30, Oxlint 1.x,
Prisma 7.10, TypeORM 1.1, Mongoose 9.11, Drizzle 0.45, Testcontainers 12.2, Compodoc 2.0, Node 24.20, npm 11.19,
Docker 29) in throwaway scaffolds — the gotchas called out inline are observed behavior, not speculation.

The generated code is the **first exemplar** of the conventions `iru-nestjs-code-one-task` enforces (its
`reference/` files: feature folders, controller → service → repository, class DTOs imported as values,
`APP_PIPE`, `configureApp()`, `getOrThrow`, `forRootAsync`, migrations instead of `synchronize`, unit specs next to
the source, e2e specs in `test/`), and every npm script name is the one `iru-setup-typescript-github-workflows`
calls and the `iru-typescript-test`/`-coverage`/`-code-quality`/`-tsdoc` gate skills detect.

## Reference files — read only what this run needs

| Read | When |
|---|---|
| `reference/app-templates.md` | **Always.** Config files (Vitest *and* Jest forms), the CommonJS conversion rules, every source/test file of the no-ORM app, and the Fastify deltas. |
| `reference/orm-prisma.md` / `orm-typeorm.md` / `orm-mongoose.md` / `orm-drizzle.md` | Only the one matching `orm`, when `orm` ≠ `none`. |
| `reference/docker-and-sonar.md` | **Always** (the `Dockerfile` and `.env.example` are always written); its Sonar section only when `sonar` ≠ `none`. |

## Step 0 — Resolve inputs

This skill can be invoked stand-alone (`/iru-setup-nestjs-app`) or driven by `iru-setup-typescript-repository`,
which resolves the shared inputs once and passes them through `args` as `key: value` lines, one per line, e.g.:

```
app-name: orders-service
description: Order management API.
license: Apache License 2.0
developer-name: Jane Doe
developer-email: jane@example.com
organization-url: https://github.com/example-org
open-source: yes
sonar: cloud
sonar-organization: example-org-github
sonar-project-key: example-org_orders-service
sonar-host-url: https://sonarcloud.io
orm: prisma
database: postgresql
distribution: internal
package-manager: npm
node-version: 24
visibility: public
ci: yes
mode: new
on-existing: ask
module-system: esm
http: express
docs-tool: compodoc
```

Parse any such lines from `args` now. Every field found here is resolved — skip asking about it in Step 2. Only
fields genuinely missing from `args` still need a question. If `args` is absent or doesn't look like this format,
treat everything as unset and ask normally.

Recognized keys (exact names):

- Identity: `app-name` (the `package.json` `name`, lowercase kebab-case; also the image name), `description`,
  `license`, `developer-name`, `developer-email`, `organization-url`.
- Shared pipeline vocabulary: `open-source` (`yes`/`no`), `sonar` (`cloud`/`self-hosted`/`none`) plus, only when
  `cloud`/`self-hosted`, `sonar-organization`/`sonar-project-key`/`sonar-host-url`; `visibility`
  (`public`/`private`/`internal` — only keys the Sonar recommendation); `ci` (`yes`/`no` — only consulted by the
  Sonar question); `mode` (`new`/`existing`); `on-existing` (`ask`/`keep`/`update`/`replace`, default `ask` — one
  answer for every pre-existing artifact, for scripted runs); `distribution` (`none`/`internal`, default `none` —
  `internal` = the workflows build and push the image to GHCR; the `Dockerfile` is written in both cases so the
  image can always be built); `package-manager` (`npm`/`pnpm`/`yarn`, default `npm`); `node-version` (Node major for
  the `Dockerfile` base image, default `24`, the active LTS).
- NestJS-specific: `module-system` (`esm`/`cjs`, default `esm` — Nest 12's default), `http` (`express`/`fastify`,
  default `express`), `orm` (`none`/`typeorm`/`prisma`/`mongoose`/`drizzle`, default `none`), `database`
  (`postgresql`/`mysql`/`mongodb` — only when `orm` ≠ `none`; `mongoose` implies `mongodb`; TypeORM/Prisma/Drizzle
  take `postgresql` (verified) or `mysql` (documented, not verified)), `docs-tool` (`compodoc`/`typedoc`/`none`,
  default `compodoc` — the orchestrator detects the choice from disk afterwards, so it needn't send it).

There is no `publish`/`storybook`/`pages`/`ci-tests` key for this skill — ignore them if sent.

`mode: existing` marks this run as an **update** of an established repository, but it never means "update
silently": Step 1 still warns and asks per pre-existing artifact unless `on-existing` says otherwise.

## Step 1 — Survey the repository

- If `mode` wasn't supplied via `args`, derive it: a `package.json` at the repository root ⇒ `existing`, else
  `new`. Don't ask it as a question.
- If a `package.json` exists, classify it: `@nestjs/core` in `dependencies` ⇒ an **existing NestJS app** (no CLI
  scaffold — Steps 4+ merge into it; read its `"type"` to fix `module-system`, `@nestjs/platform-fastify` to fix
  `http`, and its ORM packages to fix `orm`, telling the user when that disagrees with `args`); anything else ⇒ a
  **non-Nest project** at the root — ask whether to scaffold into a subdirectory named `app-name` or stop (never
  merge a Nest app into another project's `package.json`).
- Survey every artifact this skill owns: `package.json` (scripts, version, devDependencies), `nest-cli.json`,
  `tsconfig.json`/`tsconfig.build.json`, unit/e2e test configs (`vitest.config.ts`/`vitest.config.e2e.ts` or
  `jest.config.ts`/`test/jest-e2e.json`), `.oxlintrc.json` (or an ESLint config on older Nest projects),
  `.prettierrc`/`.prettierignore`, `src/main.ts`, `src/app.module.ts`, `src/app.setup.ts`, `src/config/`,
  `src/health/`, the sample feature (`src/books/`), ORM files (`prisma/` + `prisma.config.ts`,
  `src/database/`, `drizzle.config.ts` + `drizzle/`), `test/app.factory.ts`/`test/global-setup.ts`, `Dockerfile`,
  `.dockerignore`, `.env.example`, `typedoc.json`, and `sonar-project.properties`.
- Announce the mode before asking anything else:
  - **Nothing owned exists**: "Scaffolding the NestJS service **from scratch**."
  - **Anything owned exists** (or `mode: existing`): "**Updating an existing setup** — found: <list with paths>."
    Warn that each one will be handled individually, then resolve one action per existing artifact:
    - **`on-existing` is `keep`/`update`/`replace`**: apply it to every artifact without asking (still print the
      warning).
    - **Otherwise**: ask with `AskUserQuestion`, batching up to 4 artifacts per call (one question each), naming
      any concrete contradiction with this run's choices in the question (e.g. "`package.json` has no
      `format:check`/`coverage` script — the CI workflow calls both", "`src/main.ts` registers
      `app.useGlobalPipes()` — e2e tests won't see it", "`vitest.config.ts` has no coverage threshold", "a
      `sonar-project.properties` exists but you chose `sonar: none`"):
      - **Update (Recommended)** — merge: add what's missing and correct outdated parts using the templates as
        reference (missing scripts/devDependencies, coverage exclusions and threshold, the `docs` exclude in
        `tsconfig.json`, `ignorePatterns`, `.prettierignore` entries, `configureApp()`/`APP_PIPE` wiring), keeping
        everything this skill doesn't own. Show the diff; customizations survive, but a customized part this skill
        owns may be rewritten.
      - **Keep as is** — leave it untouched (and skip the commands that only serve it). It may stay out of date
        or disagree with this run's choices — Step 13 lists each mismatch.
      - **Replace** — regenerate from the template; every customization in it is lost (recoverable only from git
        history). For application source (`src/main.ts`, `src/app.module.ts`, an existing feature) recommend
        **Keep as is** instead and say why: it is real code once the project exists.
      - **Stop** (first batch only) — end this skill now without changing anything; report this and end here.
    - Never add the sample feature (`src/books/`) to an **existing** app unless the user asks — on the update path
      it would be dead code. Ask once: "Add the `books` sample feature as a reference?" (default **No**).
    - Defer the `sonar-project.properties` question until Step 2 resolves `sonar`: with `sonar: none`,
      Update/Replace mean removing the file and Keep leaves it as a reported mismatch.
- Placement (only when Step 4 will scaffold): the repository root, unless it holds another project's
  `package.json` (above) — other files (docs, CI, `README.md`, `LICENSE`, `.git`) are fine, because Step 4
  generates into a temporary directory and copies without overwriting.

## Step 2 — Collect identity and options

For any field Step 0 resolved, use it directly. When an existing `package.json` supplies an identity value Step 0
didn't (typical with `mode: existing`), use it and confirm it in one line instead of asking. Otherwise ask (plain
conversation for free text, `AskUserQuestion` for bounded choices):

- **app-name** — default: the repository directory's basename, lowercased, kebab-cased.
- **description** — one line for `package.json`.
- **developer name / email / organization URL** — `package.json`'s `author`.
- **license** (`AskUserQuestion`, same choices as every setup skill here): Apache License 2.0 (recommended) — SPDX
  `Apache-2.0` / MIT License — `MIT` / No license — `UNLICENSED` / Other (ask for the SPDX id). Remind in Step 13 to
  add a `LICENSE` file if missing.
- **open-source** — Yes / No.
- **sonar** — "Configure SonarCloud / SonarQube for this project?" Resolve `visibility` only now if absent (`gh repo
  view --json visibility -q .visibility` when there is a GitHub remote — lowercase it and tell the user — else ask
  Public/Private; `internal` counts as private; warn if `open-source: yes` contradicts a private visibility).
  Recommend **SonarCloud** only for a public **and** open-source repository; otherwise say SonarCloud is free only
  for public open-source projects and recommend **None**, offering self-hosted SonarQube second. With `ci: no`
  from `args`, say no CI workflow would send reports and recommend **None**. `cloud` → ask `sonar.organization`
  (suggest `<owner>-github`), `sonar.projectKey` (suggest `<owner>_<repo>`), confirm `https://sonarcloud.io`;
  `self-hosted` → ask the host URL, the organization only if the server has them, and the project key.
- **module-system** (`AskUserQuestion`, only when unresolved and not fixed by an existing app): **ESM with Vitest
  (Recommended — Nest 12's default)** / **CommonJS with Jest** (pick it for an organization standardized on Jest or
  a deployment target that can't load ESM). Explain that relative imports carry `.js` under ESM.
- **http**: **Express (Recommended)** / **Fastify** (faster, but Express-only middleware recipes don't apply).
- **orm** (only when unresolved): **None** (in-memory sample repository) / **Prisma** / **TypeORM** / **Other**
  (Mongoose or Drizzle, follow-up question). Then **database** when `orm` ≠ `none` and unresolved:
  **PostgreSQL (Recommended)** / **MySQL**; `mongoose` ⇒ `mongodb` without asking.
- **distribution**: **None** (image built in CI, not pushed) / **Internal** (pushed to GHCR by `release.yml`).
- **docs-tool**: **Compodoc (Recommended — understands modules, controllers, routes)** / **TypeDoc** / **None**.

## Step 3 — Resolve versions

Resolve every version live — never invent one. The fallbacks are what this skill was verified with (observed
2026-10-13); record in Step 13 which were used.

| Package | Command | Fallback |
|---|---|---|
| `@nestjs/cli` | `npm view @nestjs/cli version` | `12.0.8` |
| `@nestjs/config` / `@nestjs/terminus` | `npm view <pkg> version` | `12.0.1` / `12.1.0` |
| `zod` / `class-validator` / `class-transformer` | `npm view <pkg> version` | `4.6.7` / `0.15.1` / `0.5.1` |
| `@compodoc/compodoc` / `typedoc` | `npm view <pkg> version` | `2.0.0` / `0.28.20` |
| `testcontainers` + `@testcontainers/<db>` | `npm view testcontainers version` (same version for the module) | `12.2.1` |
| `prisma` / `@prisma/client` / `@prisma/adapter-pg` | `npm view @prisma/client version` — **use this for all three**: `prisma`'s own `latest` tag is a Prisma 8 RC | `7.10.0` |
| `@nestjs/typeorm` / `typeorm` | `npm view <pkg> version` | `12.0.2` / `1.1.2` |
| `@nestjs/mongoose` / `mongoose` | `npm view <pkg> version` | `12.0.0` / `9.11.2` |
| `drizzle-orm` / `drizzle-kit` / `@nestjs/drizzle` | `npm view <pkg> version` (the `latest` tag; `1.0.0` is still `rc`) | `0.45.4` / `0.31.11` / `0.0.2` |
| `pg` / `@types/pg` / `dotenv` | `npm view <pkg> version` | `8.23.1` / `8.23.1` / `17.x` |

Don't upgrade the scaffold's own pins (`typescript ~6.0`, `vitest`/`vite`, `jest`/`ts-jest`, `oxlint`,
`@types/node`): the CLI chose a mutually compatible set, and TypeScript 7 (npm's `latest`) is not supported by it.

## Step 4 — Scaffold with the Nest CLI (new apps only)

Skip for an existing NestJS app. Otherwise generate in a **temporary directory** — the Nest schematics refuse to
write into a directory that already holds any of their files (verified: `nest new .` next to an existing
`README.md` fails with `A merge conflicted on path "/README.md"`) — then copy without overwriting:

```bash
SCAFFOLD_DIR="$(mktemp -d)"
cd "$SCAFFOLD_DIR"
# module-system: esm (Vitest)
npx -y @nestjs/cli@<cli-version> new <app-name> --skip-git --skip-install --package-manager <package-manager> --no-observe --strict
# module-system: cjs (Jest) — `nest new` offers CommonJS only as an interactive prompt; the application schematic
# takes it as a flag (verified with CLI 12.0.8):
npx -y @nestjs/cli@<cli-version> g application <app-name> --type=cjs
cd -
rsync -a --ignore-existing --exclude README.md "$SCAFFOLD_DIR/<app-name>/" <target>/
rm -rf "$SCAFFOLD_DIR"
```

- `--no-observe` skips the `@nestjs/observe` prompt (non-interactive runs skip it anyway); `--skip-git` because
  the repository already exists; `--skip-install` because Step 5 installs once, with everything. `--strict` is
  already the default — kept for explicitness.
- `README.md` is excluded: `iru-setup-readme` owns it. `<target>` is the repository root or the `app-name`
  subdirectory (Step 1). Without `rsync`, copy the tree with `cp -Rn` (no-clobber).
- The scaffold gives: `package.json`, `nest-cli.json`, `tsconfig.json`, `tsconfig.build.json`, `.oxlintrc.json`,
  `.prettierrc`, `.gitattributes`, `src/{main,app.module,app.controller,app.service}.ts`,
  `src/app.controller.spec.ts`, `test/app.e2e-spec.ts`, and `vitest.config.ts` + `vitest.config.e2e.ts` (ESM) or
  `jest.config.ts` + `test/jest-e2e.json` (CJS).
- Delete the "Hello World" placeholders (`src/app.controller.ts`, `src/app.service.ts`,
  `src/app.controller.spec.ts`, `test/app.e2e-spec.ts`) — the health and sample feature replace them.

## Step 5 — `package.json`, dependencies, and scripts

Edit `package.json` (by hand or `npm pkg set`), keeping everything the scaffold added that isn't listed here:

- `name` = `app-name`, `version` = `0.1.0-dev.0` (the `x.y.z-dev.N` convention `iru-typescript-bump-version`
  maintains), `description`, `author` (`{name, email, url}`), `license` (SPDX id), `"private": true` (a service is
  never published to npm), `"engines": {"node": ">=24"}` (`">=24.9"` for CommonJS: Jest needs it to load the
  ESM-only Nest 12 packages).
- Remove the `deploy` script and the `@nestjs/mau` devDependency (`nest deploy` targets Nest's commercial cloud;
  this catalog distributes a container image instead) — say so in Step 13.
- Scripts — exactly these names (the workflows and gates call them):

| Script | ESM (Vitest) | CommonJS (Jest) |
|---|---|---|
| `build` | `nest build` | same |
| `start` / `start:dev` / `start:debug` | `nest start` / `--watch` / `--debug --watch` (scaffold's) | same |
| `start:prod` | `node dist/main.js` | same |
| `lint` | `oxlint --type-aware src/ test/` | same |
| `format` | `prettier --write .` | same |
| `format:check` | `prettier --check .` | same |
| `typecheck` | `tsc --noEmit -p tsconfig.json` | same |
| `test` | `vitest run` | `node --experimental-vm-modules ./node_modules/jest/bin/jest.js` |
| `test:watch` / `test:debug` | scaffold's | scaffold's |
| `coverage` | `vitest run --coverage` | `<jest> --coverage` |
| `test:cov` | alias of `coverage` (Nest's own name, kept for Nest docs/readers) | alias |
| `test:e2e` | `vitest run --config ./vitest.config.e2e.ts` | `<jest> --config ./test/jest-e2e.json` |
| `docs` | `compodoc -p tsconfig.build.json -d docs/api --disableSourceCode --disableGraph --silent` (`docs-tool: compodoc`) or `typedoc` (`docs-tool: typedoc`); no script for `none` | same |

  plus the ORM scripts from the matching `orm-*.md` (`prisma:generate`/`db:migrate`/`db:migrate:dev`,
  `migration:generate`/`migration:run`/`migration:revert`, or `db:generate`/`db:migrate`).
- Install, with `<package-manager>` (`npm install` / `pnpm add` / `yarn add`; `-D` for dev):
  - always: `@nestjs/config`, `@nestjs/terminus`, `zod`, `class-validator`, `class-transformer`; dev: the
    `docs-tool` package (`@compodoc/compodoc` or `typedoc`).
  - `http: fastify`: `@nestjs/platform-fastify` (same version as `@nestjs/core`), and uninstall
    `@nestjs/platform-express` + `@types/express`.
  - `orm` ≠ `none`: the packages listed at the top of the matching `orm-*.md`, plus `testcontainers` and
    `@testcontainers/<postgresql|mysql|mongodb>` (dev).
  - Run the plain install once for the scaffold's own dependencies first (`npm install`).
  - `configureApp()` calls `app.useSecurityHeaders()`, which exists from Nest **12.1**; the scaffold declares
    `^12.0.1`. Raise the floor of `@nestjs/common`, `@nestjs/core`, the platform package, and `@nestjs/testing` to
    the installed version (`npm install @nestjs/common@^<core-version> …`) so an older lockfile can't resolve 12.0.
- npm 11 prints `install-scripts` warnings (dependency install scripts are blocked until approved): expected and
  harmless here — nothing in this stack needs them (verified, Prisma included). Don't approve them blindly; mention
  it in the report.

## Step 6 — Configuration files

From `reference/app-templates.md` (Vitest or Jest forms per `module-system`):

- `vitest.config.ts` + `vitest.config.e2e.ts` (ESM) or `jest.config.ts` + `test/jest-e2e.json` (CJS): unit specs
  only under `src/`, e2e only `test/**/*.e2e-spec.ts`, coverage over `src/**/*.ts` excluding `*.spec.ts`,
  `*.module.ts`, `main.ts`, `src/generated/**`, `src/database/migrations/**`, `src/database/data-source.ts`;
  reporters text + lcov + json-summary into `coverage/`; threshold 80 % for lines/statements/functions. **No branch
  threshold**: verified on every variant, each injected constructor parameter compiles to a decorator-metadata
  `typeof X === "undefined" ? Object : X` branch no test can take (70–77 % branches at 100 % lines).
- `tsconfig.json`: add `"exclude": ["node_modules", "dist", "docs", "coverage"]`. **Required** — verified: Compodoc
  writes `.ts` files under `docs/api/template-playground/`, and the scaffold's include-everything `tsconfig.json`
  then fails `npm run typecheck` with 20+ errors after the first `npm run docs`.
- `.oxlintrc.json`: keep the scaffold's (`typescript/no-floating-promises: error`), but set
  `typescript/no-explicit-any` to `error` (the scaffold turns it off; this catalog's rule is no `any`) and add
  `"ignorePatterns": ["src/generated/**"]`.
- `.prettierrc`: keep the scaffold's (`singleQuote`, `trailingComma: all`). Add `.prettierignore` (template) —
  `format`/`format:check` run on `.`, and the gate runs `prettier --list-different .`, so generated output
  (`dist`, `coverage`, `docs`, `src/generated`, `drizzle`), workflow YAML, `.claude`, `CHANGELOG.md`, `README.md`,
  and lockfiles must be ignored or the first CI run fails on files Prettier never produced.
- `typedoc.json` (only `docs-tool: typedoc`; verified, writes `docs/api`):

  ```json
  {
    "$schema": "https://typedoc.org/schema.json",
    "entryPoints": ["src"],
    "entryPointStrategy": "expand",
    "exclude": ["**/*.spec.ts", "src/main.ts", "src/generated/**"],
    "tsconfig": "tsconfig.build.json",
    "out": "docs/api",
    "excludePrivate": true,
    "treatWarningsAsErrors": true
  }
  ```

## Step 7 — Application skeleton

Write the source files from `reference/app-templates.md` (converted with its CommonJS rules for `cjs`):

- `src/config/env.schema.ts` (+ spec) — Zod schema passed to `ConfigModule.forRoot({ isGlobal: true,
  validationSchema })` (Standard Schema, `@nestjs/config` 12); `PORT` coerced, `DATABASE_URL` added by the ORM file.
- `src/app.module.ts` — `ConfigModule`, `HealthModule`, the feature module(s), `DatabaseModule` when an ORM is
  used, and the global `ValidationPipe({ whitelist, forbidNonWhitelisted, transform })` as an `APP_PIPE` provider.
- `src/app.setup.ts` (+ spec) — `configureApp(app)`: `app.useSecurityHeaders()` (Nest 12.1+, Helmet 8 defaults,
  Express and Fastify) and `app.enableShutdownHooks()`. `main.ts` and `test/app.factory.ts` both call it, so the
  e2e suite tests what production runs (`main.ts` never runs under a test runner).
- `src/main.ts` — `configureApp(await NestFactory.create(AppModule))`, port from `ConfigService.getOrThrow`, listen
  on `0.0.0.0`.
- `src/health/` — `TerminusModule`, `GET /health/live` (no dependency checks) and `GET /health/ready` (the
  database ping from the ORM file, or nothing without one), with specs.
- `src/books/` — the sample feature (new apps, or existing ones when the user asked): entity, `CreateBookDto`,
  `ListBooksQuery` (capped page), repository (in-memory without an ORM), service, controller, module, and a spec for
  each of them. Rename it only if the user asked for a different first feature (keep the shape).
- `test/app.factory.ts` + `test/health.e2e-spec.ts` + `test/books.e2e-spec.ts` — the whole app through supertest,
  including the 400 paths (missing field, unknown property, non-integer id, page above the cap) and 404.
- `http: fastify` — the Fastify `main.ts` and `test/app.factory.ts`, and the e2e spec typing, from the same file.

## Step 8 — Persistence (`orm` ≠ `none`)

Follow the matching `reference/orm-*.md` completely: the files it lists replace or extend Step 7's
(`books.repository.ts` + spec, health readiness + spec, `env.schema.ts` + spec, `app.module.ts`), the
`src/database/` wiring, the initial migration (generated as that file says — no database needed), the scripts, and
the e2e global setup that starts **one** Testcontainers database for the run, applies the migrations, and exports
`DATABASE_URL` before any spec imports `AppModule`. Container-backed e2e tests need a running Docker daemon — the
unit suite and the coverage gate never do. Schema changes always ship as migrations; never `synchronize: true`.

For `database: mysql` (not verified here): `@testcontainers/mysql`, `mysql2` (TypeORM `type: 'mysql'`, Drizzle
`drizzle-orm/mysql2` + `mysqlTable`), Prisma `provider = "mysql"` with `@prisma/adapter-mariadb`; regenerate the
initial migration for that dialect, and say in the report that this combination was not verified.

## Step 9 — Container image and `.env.example`

Write `Dockerfile`, `.dockerignore`, and `.env.example` from `reference/docker-and-sonar.md` (Prisma build-stage
delta and package-manager variants included; `node:<node-version>-slim`). Written for every run:
`distribution: internal` only decides whether `release.yml` pushes the image.

## Step 10 — `sonar-project.properties`

Only when `sonar` is `cloud`/`self-hosted`: write it from `reference/docker-and-sonar.md`. With `sonar: none`,
skip it and note in the report that Sonar was deliberately not wired up.

## Step 11 — Format and generate

Run once, in order: the ORM's generate step (`npx prisma generate` for Prisma — CI runs the same before lint),
then `npx prettier --write .` (the templates are already Prettier-formatted; this catches anything adapted).

## Step 12 — Verify with the gate skills' commands

Run, in order, and fix until green before reporting success (each is what CI and the gates run):

```bash
npm run lint && npm run format:check && npm run typecheck && npm run test && npm run coverage \
  && npm run build && npm run docs
docker info >/dev/null 2>&1 && npm run test:e2e   # Docker needed only when orm != none
docker build -t <app-name>:verify .                 # when Docker is available
```

(`pnpm run …` / `yarn …` for the other package managers; skip `docs` with `docs-tool: none`.)

- Without an ORM the e2e suite needs no Docker — always run it.
- With an ORM and no reachable Docker daemon: report `test:e2e` as **not run (Docker unavailable)**, never as
  passed. Same for the image build.
- When Docker is available, also smoke-test the image: `docker run -d -p <free-port>:3000 [-e DATABASE_URL=…]
  <app-name>:verify`, wait ~25 s, confirm `docker inspect --format '{{.State.Health.Status}}'` is `healthy` and
  `curl /health/live` answers `200`, then remove the container. With an ORM, run a database container on a user
  network and apply the migrations first (see `docker-and-sonar.md`), or skip the run and say so.
- The coverage gate (`iru-typescript-coverage`) passes its own `--coverage.include/exclude` flags; on the Prisma
  variant those don't exclude `src/generated/**`, which still measured above 80 % (82.8 %) — mention it if a future
  run gets close.

## Step 13 — Report

Start with the mode announced in Step 1 (**scaffolded from scratch** or **updated an existing setup**) and the
location (repository root or subdirectory). Then:

- Per owned artifact, the action actually taken — **created / updated / replaced / kept as is / removed** — and,
  for every kept one, each mismatch with this run's choices.
- The resolved choices: `module-system`, `http`, `orm` + `database`, `distribution`, `docs-tool`, `package-manager`,
  `node-version`, license, `open-source`; `sonar` (with the `visibility` used and where it came from — `args`,
  `gh`, or the user; if `ci: no` and Sonar was still configured, say no CI step sends reports).
- The exact npm scripts written (the table in Step 5 plus the ORM ones) — the names
  `iru-setup-typescript-github-workflows` calls are `lint`, `format:check`, `typecheck`, `coverage`, `test:e2e`,
  `build`, `docs`.
- Versions: which came from a live lookup and which from the fallback table; that the scaffold's TypeScript 6 pin
  was kept on purpose.
- Every verification command run (Step 12) with its result, the coverage numbers and `coverage/lcov.info`, and
  anything reported as not run (Docker unavailable, MySQL unverified).
- Removed scaffold pieces: the Hello World controller/service/specs, the `deploy` script and `@nestjs/mau`.

Finish with a **Warn explicitly** block:

- Review every generated file before committing — `package.json` `author`/`description`/`license`, the Sonar keys.
- The generated Prisma client (`src/generated/`) is not committed — `iru-setup-typescript-gitignore` ignores it;
  run `npx prisma generate` after every clone (CI does).
- Migrations are not run by the app or the image — run them as a deployment step (commands in
  `docker-and-sonar.md`).
- `sonar: cloud`/`self-hosted`: a `SONAR_TOKEN` secret and the Sonar project must exist before CI scans succeed.
- `distribution: internal`: the image is pushed to GHCR by the workflows; the package's visibility on GHCR follows
  the repository's — check it before the first release.
- No `.gitignore`, workflows, `CHANGELOG.md`, or `README.md` were written — `iru-setup-typescript-gitignore`,
  `iru-setup-typescript-github-workflows`, `iru-setup-changelog`, and `iru-setup-readme` cover them (the
  `iru-setup-typescript-repository` orchestrator runs them next).
- If a license was chosen and no `LICENSE` file exists, suggest `iru-check-license`.

## Sources

- irurueta docs: `backend/nestjs/getting-started-and-cli.adoc` (CLI 12, ESM vs CommonJS, generated files,
  scripts), `testing.adoc` (runners, decorator metadata, Testcontainers, coverage), `configuration.adoc` (Standard
  Schema validation), `ci-cd.adoc` (pipeline scripts, coverage thresholds), `deployment.adoc` (multi-stage
  Dockerfile, health endpoints, `0.0.0.0` on Fastify), `health-checks-and-observability.adoc`,
  `data-overview-and-typeorm.adoc`, `prisma-drizzle-mikroorm-and-sequelize.adoc`, `mongodb-with-mongoose.adoc`,
  `project-structure-and-workspaces.adoc`
- This catalog: `iru-nestjs-code-one-task/reference/*` (the conventions the skeleton exemplifies),
  `iru-setup-react-web`, `iru-setup-typescript-library` (structure), `iru-setup-typescript-github-workflows`
  (script names)
- NestJS: <https://docs.nestjs.com/cli/usages>, <https://docs.nestjs.com/techniques/configuration>,
  <https://docs.nestjs.com/recipes/terminus>, <https://docs.nestjs.com/fundamentals/testing>
- Prisma 7: <https://www.prisma.io/docs/orm/overview/databases/database-drivers>; TypeORM:
  <https://typeorm.io/docs/migrations/>; Drizzle: <https://orm.drizzle.team/docs/migrations>; Testcontainers for
  Node.js: <https://node.testcontainers.org/>; Compodoc: <https://compodoc.app/>
