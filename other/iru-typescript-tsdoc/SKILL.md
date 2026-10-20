---
name: iru-typescript-tsdoc
description: Audit given TypeScript file(s)/scope for complete TSDoc coverage on every exported function, class, interface, type alias, and enum (React components' props interfaces and hooks, Angular components/services/inputs/outputs, NestJS controllers/route handlers/services/DTOs/modules/guards/pipes, and Next.js exported components/pages/layouts/server actions/route handlers/hooks included) — `/** ... */` with `@param`/`@returns`/`@throws` where applicable and `@example` on public entry points — generate any missing or incomplete TSDoc grounded in the actual code and current changes, then run the project's own doc-build tooling (TypeDoc or Compodoc, whichever the project uses — Compodoc is common on NestJS) to confirm the result builds without warnings/errors; for NestJS, Next.js, and React Native apps, where neither tool is guaranteed to be installed, it verifies with whichever one the project actually configured and reports the run as audit-only when neither is. Invoke as `/iru-typescript-tsdoc <path-or-glob>` (comma-separated paths/globs accepted), or `/iru-typescript-tsdoc` with no argument to scope to files touched by uncommitted changes plus commits on the current branch not yet on the base branch. Works against any TypeScript project (npm/TypeScript library, React, Angular, Ionic, a Vaadin Hilla frontend, NestJS, Next.js, or a React Native app on either toolchain — `expo` or a bare React Native CLI/`metro` app, with TypeDoc entry points limited to the in-scope TypeScript files so the native `android/`/`ios/` projects, `.expo/`, config files and the root `index.js`/`index.ts` registration entry never enter the run, and audit-only when the app has no TypeDoc configured) — it detects the project's flavor and doc toolchain at runtime rather than assuming one. Use whenever the user wants TSDoc completeness checked and filled in for specific files, instead of relying on a full docs-site build to surface gaps.
model: sonnet
---

# TypeScript TSDoc

Make sure a set of TypeScript files carry complete, well-formed TSDoc on every exported symbol, filling in
whatever is missing, then prove the result actually builds via the project's own doc tooling (TypeDoc or
Compodoc). This skill only adds/completes documentation comments — it does not change behavior, signatures, or
non-comment code. Test files (`*.test.ts(x)`, `*.spec.ts(x)`, anything under `test/`, `tests/`, `__tests__/`, or
`e2e/`) are out of scope for documentation requirements — they don't need TSDoc added, even if named explicitly —
but any TSDoc a test file already has must be left as-is; never strip or "clean up" existing comments in test
code. It makes no assumptions about this being any particular repository — discover the project's actual flavor,
conventions, and build setup fresh each run.

## Step 0 — Detect the project's flavor

Framework detection rule (shared with every other skill in this catalog's TypeScript group — apply the same
checks here so the doc bar and verification command match what the rest of the pipeline assumes):

- `@vaadin/hilla`/`hilla-spring-boot-starter` in `pom.xml`, or a `src/main/frontend/` directory → **hilla-frontend**
- `expo` or `react-native` in `package.json` dependencies → **react-native** — toolchain **expo** when `expo` is a
  dependency (even with `android/`/`ios/` present as `npx expo prebuild` output), otherwise **metro** (bare React
  Native CLI app; Expo also bundles with Metro — the name only distinguishes the two toolchains)
- `@ionic/angular` or `@ionic/react` + `@capacitor/core` in `package.json` → **ionic**
- `@nestjs/core` in `package.json` → **nestjs**
- `next` in `package.json` → **nextjs**
- `@angular/core` in `package.json` → **angular**
- `react` + `vite` in `package.json` → **react**
- none of the above → **library**

This drives two things later: which build tool verifies the docs (Step 5 — Compodoc for `angular`, TypeDoc for
every other flavor except `nestjs`/`nextjs`/`react-native`, which use whichever tool the project actually
configured, or none) and what "exported" means for the audit (Step 1).

**Doc tool for `nestjs`/`nextjs`** — these app flavors often ship no doc tool at all, so never fetch one on the fly
with a bare `npx typedoc`/`npx compodoc` (that downloads and runs a tool the project never chose):

- **nestjs**: Compodoc is the de-facto Nest documentation tool (it understands modules, controllers, providers,
  and routes) — use it when `@compodoc/compodoc` is a devDependency or a `.compodocrc*`/`compodoc` script exists.
  Otherwise use TypeDoc when `typedoc` is a devDependency or a `typedoc.json` exists. Neither → **audit-only**.
- **nextjs**: TypeDoc when `typedoc` is a devDependency or a `typedoc.json` exists; otherwise **audit-only**.
- **react-native** (both toolchains): same rule as nextjs — TypeDoc only when `typedoc` is a devDependency or a
  `typedoc.json` exists (neither the React Native CLI template nor `create-expo-app` ships one); otherwise
  **audit-only**.
- **Audit-only** means Steps 1-4 still run in full (the audit and the generated TSDoc don't depend on a build
  tool), Step 5 is skipped, and the Step 6 report says "doc build not verified: no TypeDoc/Compodoc configured in
  this project" — never a pass.

## Step 1 — Determine scope

- **Argument provided** (comma-separated paths or globs): resolve each to its file(s) via `find`/`ls`. Drop any
  resolved file that is a test file per the definition above — say so in the Step 6 report rather than silently
  ignoring it, since test files carry no TSDoc requirement here.
- **No argument**: default to every non-test `.ts`/`.tsx` file touched by uncommitted changes plus commits on the
  current branch not yet on the base branch, same approach as `iru-update-docs`:
  ```bash
  git status
  git diff <base-branch>...HEAD --name-only
  git diff --name-only
  ```
  (determine the base branch via `git symbolic-ref refs/remotes/origin/HEAD` or `git branch -a` if unclear; ask
  the user only if genuinely ambiguous). Filter out `node_modules/`, `dist/`, `build/`, generated files
  (`src/main/frontend/generated/` for Hilla, `.d.ts` files), and non-TypeScript files.
- If the resulting scope is empty (no argument and no relevant changes), tell the user there is nothing to
  document and stop.
- **What "exported" means, per flavor** (this defines the audit set within each in-scope file):
  - **library**: every symbol reachable from the package's public entry point (`src/index.ts` or whatever
    `package.json`'s `exports`/`main`/`types` fields name) — an exported symbol re-exported from `index.ts`
    counts even if the file itself is not directly in scope; a symbol exported from a file but never re-exported
    from the entry point is still in scope if its *file* is in scope (it's still part of that file's API surface
    for anyone importing it directly) but is lower priority for `@example` (Step 3).
  - **react / react-native / ionic / hilla-frontend (apps)**: simply every `export`ed function, class, interface,
    type alias, and enum in each in-scope file — there is no single public entry point to trace, since app code
    is consumed by the bundler, not by external importers.
  - **react-native specifics** (both toolchains): screens/components (a one-line summary of what the screen
    renders, plus its props type — React Navigation screens' `route.params` shape, Expo Router routes' search
    params), hooks, and services are in scope; so is a Turbo Module/Codegen spec (`Native*.ts` exporting `interface
    Spec extends TurboModule`) — document each method with what the native side does, its `@param`s, and the
    promise's resolve/reject contract, since the TypeScript spec is the only shared contract between the JS and the
    Kotlin/Obj-C++ implementations. Never in scope: anything under `android/`, `ios/`, `.expo/`, `node_modules/`;
    `metro.config.js`, `babel.config.js`, `react-native.config.js`, `app.config.*`, `jest.config.*`; and the root
    `index.js`/`index.ts` that only calls `AppRegistry.registerComponent`/`registerRootComponent` — drop them from
    the scope like test files and say so in the report. An Expo Router `_layout.tsx`/route file's default export
    gets a one-line summary and never an `@example`.
  - **nestjs**: every exported class in scope by its Nest role — **controllers** (`@Controller`: the class, plus
    every route-handler method with what the endpoint does, a `@param` per `@Param()`/`@Query()`/`@Body()`
    argument, `@returns` describing the response body, and `@throws` per `HttpException` subclass it can raise —
    `NotFoundException`, `ConflictException`, …), **services/providers/repositories** (`@Injectable`: class and
    public methods), **DTOs** (the class and each property, stating its validation constraints in words where the
    `class-validator` decorators make them non-obvious), **modules** (`@Module`: a class-level comment saying what
    the feature module provides and exports — Compodoc lists modules as their own pages), **guards, pipes,
    interceptors, filters, and custom decorators** (class/factory plus `canActivate`/`transform`/`intercept`/
    `catch`), **entities/schemas**, and exported interfaces/types/enums. Compodoc also counts the non-exported
    `bootstrap` function in `src/main.ts` (verified on a Nest 12 scaffold: it was listed as `0 % for file
    src/main.ts - bootstrap - under minimum per file`) — give it a one-line comment when `main.ts` is in scope
    and Compodoc is the verifier.
  - **nextjs**: every exported component (including the default-exported `page.tsx`/`layout.tsx`/`template.tsx`/
    `loading.tsx`/`error.tsx`/`not-found.tsx` components — a one-line summary of what the route renders), its props
    type, every exported custom hook in `'use client'` files, every **server action** exported from a `'use server'`
    file or defined inline (inputs, the authentication/authorization it performs, what it revalidates/redirects to,
    and `@throws`/the error state it returns), every **route handler** exported from `route.ts` (`GET`/`POST`/…:
    the request it accepts, `ctx.params` route parameters, response status codes and body), `generateMetadata`/
    `generateStaticParams`, and exported library functions under `lib/`. Route-segment config exports (`dynamic`,
    `revalidate`, `runtime`, `fetchCache`, `metadata` objects, a `proxy.ts`/`middleware.ts` `config` matcher) need
    at most a one-line comment and never an `@example`. Skip `next.config.*`, `next-env.d.ts`, and `.next/`.
  - **angular**: every exported class (`@Component`, `@Injectable`, `@Directive`, `@Pipe`), its public
    `@Input()`/`@Output()` members and public methods, and every exported interface/type/enum in scope — Compodoc's
    coverage percentage (Step 5) counts components, services, inputs, and outputs the same way it counts plain
    classes, so the manual audit here must match that scope or the two checks will disagree.

## Step 2 — Discover this project's actual TSDoc bar before auditing

Don't assume a fixed documentation scope — discover it from the project itself:

- Check for a contributor guide (`CLAUDE.md`, `AGENTS.md`, a top-level `README`, or a `CONTRIBUTING` file) for any
  stated TSDoc convention.
- Check `typedoc.json` (or the `typedoc` key in `package.json`) for `treatWarningsAsErrors` and `requiredToBeDocumented` (used verbatim as a config key — a JSON array of reflection kind names, e.g.
  `["Class", "Interface", "Function", "TypeAlias", "Enum"]`) and for `validation.notDocumented` — **verified
  locally: TypeDoc 0.28.20 does *not* warn about undocumented exports by default, even with
  `--treatWarningsAsErrors` set. `validation.notDocumented` must be explicitly `true` (CLI:
  `--validation.notDocumented true`) for TypeDoc to flag a symbol with no doc comment at all; without it,
  `typedoc --emit none --treatWarningsAsErrors` exits `0` against a completely undocumented file.** If the
  project's own `typedoc.json` doesn't set `validation.notDocumented`, still audit for missing docs manually in
  Step 3 — don't rely on the project's own config to have caught what this skill is here to catch.
- Check for `eslint-plugin-jsdoc` or `eslint-plugin-tsdoc` rules in `eslint.config.js` (flat config) —
  `jsdoc/require-jsdoc`, `jsdoc/require-param`, `jsdoc/require-returns`, `tsdoc/syntax` set to `"error"` for
  exported members raise the bar; note their exact rule ids and severities, they matter for `iru-typescript-code-quality`
  agreeing with what this skill just fixed.
- For Angular, check `.compodocrc.json` (or a `compodoc` key in `package.json`) for `coverageTest`/
  `coverageMinimumPerFile`; if absent, the default threshold Compodoc itself uses is 70 % (Step 5 still runs this
  skill's own request, typically 80 %, matching the group's own convention below unless the project states
  otherwise).
- If none of the above give a clear answer, skim 2-3 existing exported symbols near the ones in scope to see
  empirically whether the project already writes full TSDoc (with `@param`/`@returns`) or only summary lines —
  treat that observed practice as the bar.
- Reconcile any conflict between a stated/configured convention and the actually-enforced/observed one by
  following the **stricter** of the two, so this skill's output would pass the project's own lint/doc-build
  checks.

Skim a couple of existing, well-documented exports in the project (prefer ones structurally similar to what's in
scope — a hook if auditing a hook, a service if auditing a service) to internalize the exact phrasing and tag
style before writing new TSDoc: person and tense used, whether summary sentences end in a period, how generic
type parameters are documented, whether `@remarks` is used for longer explanation versus a plain paragraph after
the summary, and the `@param`/`@returns`/`@throws` ordering. If the project has no existing TSDoc to learn from,
fall back to standard TSDoc convention:

- **`@param name - description`** — TSDoc uses a hyphen before the description and no `{type}` annotation (the
  type already comes from the TypeScript signature); this is the one point where TSDoc differs visibly from
  classic JSDoc (`@param {type} name description`). Never write the JSDoc form in a TSDoc-audited project.
- `@returns` (not the JSDoc `@return`) — one sentence describing the returned value; omitted for `void`/`Promise<void>`.
- `@throws` — one per distinct error/exception type that can propagate out, only when the implementation actually
  throws or explicitly documents a promise rejection reason.
- `@remarks` — a paragraph of additional detail beyond the one-line summary, when the summary alone isn't enough
  (design rationale, caveats, performance notes) — keep the first line a single concise summary regardless.
- `@example` — a fenced ` ```ts ` code block showing realistic usage; required on every public entry point (a
  library's `index.ts` exports, an app's exported hooks/components used by more than one caller) per the
  invocation form's own requirement; optional elsewhere.
- `@public` / `@internal` — mark the intended visibility only where the project already does this consistently
  (common in library flavor to distinguish the stable API surface from implementation details still exported for
  internal reasons); don't introduce the convention into a project that doesn't already use it.
- `@deprecated` — carried over verbatim from an existing comment being extended; never add it new — that's a
  decision only the code owner makes.
- `{@link OtherSymbol}` — use for cross-references instead of a bare name in backticks when pointing at another
  exported symbol in the same package; TypeDoc's `validation.invalidLink` (when enabled) fails the build on a
  `{@link}` that doesn't resolve, so only add one where the referenced symbol actually exists and is exported.

## Step 3 — Audit each in-scope file

Read the full file, then check every symbol that counts as "exported" per Step 1's per-flavor definition has a
non-empty `/** ... */` doc comment that actually describes its purpose (not just restates its name), scoped per
the bar established in Step 2:

- **Functions** (including arrow-function exports and custom hooks — `useXyz`): `@param` per parameter,
  `@returns` unless `void`, `@throws` for any error path the implementation can actually take.
- **Classes**: a doc comment on the class itself; its exported/public constructor and public methods each with
  their own `@param`/`@returns`/`@throws`; public and `protected` fields with a one-line comment. Angular
  services (`@Injectable`) and components (`@Component`) follow this same shape.
- **Interfaces and type aliases**: a doc comment on the type itself. For a **React component's props interface**,
  document the interface and, where a prop's purpose isn't obvious from its name/type alone, a one-line comment
  above that individual prop. For an Angular component's class, document each `@Input()`/`@Output()` member the
  same way — Compodoc's coverage counts each of these as its own documentable symbol.
- **Enums**: a doc comment on the enum itself and on each member whose meaning isn't self-evident from its name.
- **Re-exports** (`export { Foo } from './foo'`, `export * from './foo'`): no comment needed on the re-export
  line itself — the documentation requirement lives on the original declaration, which is either already in scope
  or covered by a different file's audit.

For each item found incomplete or missing entirely, record: the symbol, its kind, what's missing (whole comment
vs. a missing `@param`/`@returns`/`@throws`/`@example`), and the file it's in.

## Step 4 — Generate the missing TSDoc

For every gap found in Step 3, write the TSDoc directly grounded in:

- The symbol's actual implementation (parameter usage, return expression, thrown/rejected errors, a component's
  actual rendered output or a hook's actual returned value) — read the function/class body, don't infer purely
  from the signature/name.
- Any current uncommitted/branch changes to that symbol (`git diff` / `git log -p` for that file/hunk if it was
  just added or modified) — if the change altered behavior, the new TSDoc must describe the current behavior, not
  stale prior behavior a name alone might suggest.
- The phrasing and tag conventions gathered in Step 2 — match voice, tense, and tag style exactly so the new
  comments are indistinguishable from hand-written ones in this codebase, and use the TSDoc hyphen form for
  `@param`, never the JSDoc `{type}` form.

Apply the edits with the Edit tool. Do not modify code logic, signatures, formatting outside the added comments,
or reorder members — this skill only adds/completes TSDoc comments.

## Step 5 — Verify the docs actually build

Which tool verifies depends on the flavor detected in Step 0.

### library / react / ionic / hilla-frontend (and nestjs / nextjs / react-native when TypeDoc is configured) — TypeDoc

```bash
npx typedoc --emit none --treatWarningsAsErrors --validation.notDocumented true
```

- `--emit none` skips writing the HTML site — this only needs TypeDoc's own analysis/validation pass, not a full
  docs build, mirroring how the Java Javadoc skill runs `mvn javadoc:jar` rather than a full site build.
- **A repository with no valid `origin` git remote makes this command fail for a non-doc reason** (verified in a
  smoke test against a generated library): TypeDoc warns `The provided git remote "origin" was not valid` while resolving
  source links, and `--treatWarningsAsErrors` turns that into a non-zero exit even when every export is documented.
  Check `git remote get-url origin` first; if it fails, append `--disableGit --disableSources` (verified in the same smoke test: `--disableGit` alone
  fails differently — `disableGit is set, but sourceLinkTemplate is not, so source links cannot be produced`, exit 4 —
  because TypeDoc still tries to emit source links; `--disableSources` drops them) so the exit code reflects
  documentation warnings only, and say so in the Step 6 report.
- **`--validation.notDocumented true` must be passed even if the project's own `typedoc.json` doesn't set it** —
  verified locally that without it, `--treatWarningsAsErrors` alone does not catch an entirely undocumented
  export (exit `0`); with it, TypeDoc warns per symbol, e.g. `undocumentedAdd (CallSignature), defined in
  <pkg>/src/index.ts, does not have any documentation`, and exits non-zero once warnings are treated as errors.
  If the project's own `requiredToBeDocumented` narrows which kinds are checked (e.g. excludes `Property`), honor
  that instead of the tool's full default kind list — pass it through via the project's own `typedoc.json` rather
  than overriding it, since Step 2 already reconciled it as the effective bar.
- **TypeDoc needs a resolvable entry point regardless of `--emit none`** — verified locally: with no
  `entryPoints` in `typedoc.json`/CLI and no `exports` field in `package.json`, TypeDoc warns `No entry points
  were provided or discovered from package.json exports, this is likely a misconfiguration` and (with
  `--treatWarningsAsErrors`) exits non-zero without analyzing anything. TypeDoc *can* auto-discover the entry
  point from `package.json`'s `exports` map (verified: an `exports: { ".": "./src/index.ts" }` field alone was
  enough, no explicit `entryPoints` needed) — this is exactly the `exports` map `iru-setup-typescript-library`
  writes, so a library scaffolded by this catalog needs no extra flag. For app flavors without a meaningful
  `exports` map (react, react-native, ionic, hilla-frontend), pass `--entryPoints` explicitly, scoped to the
  in-scope files themselves, e.g. `--entryPoints src/features/foo/useFoo.ts --entryPoints src/features/foo/Foo.tsx`,
  rather than the whole `src/` tree, to keep the run scoped and fast.
- **nextjs**: run `npx next typegen` first, and add `--validation.notExported false`. Verified locally on a Next
  16.4 scaffold with TypeDoc 0.28 + TypeScript 5.9.3, `--entryPoints` per in-scope file and `--disableGit
  --disableSources`: without typegen, TypeDoc stops on `error TS2304` for the global `LayoutProps` route helper
  type (it type-checks the project first); after typegen it still warned `__global.LayoutProps, defined in
  .next/types/routes.d.ts, is referenced by ... but not included in the documentation`, which
  `--treatWarningsAsErrors` turns into a failure unrelated to any missing comment — `--validation.notExported
  false` removes exactly that warning while the `does not have any documentation` warnings for `add`, the layout's
  default export, and its `metadata` export remained (exit `4`).
- **nestjs**: point `--entryPoints` at the in-scope files exactly as for app flavors above; Nest's `tsconfig.json`
  already enables `experimentalDecorators`/`emitDecoratorMetadata`, which TypeDoc honors.
- **react-native** (both toolchains, only when TypeDoc is configured — Step 0): `--entryPoints` per in-scope
  `.ts`/`.tsx` file, never a directory glob, so nothing under `android/`/`ios/`/`.expo/` and no config or root
  `index.js`/`index.ts` file is ever an entry point. Verified locally with TypeDoc 0.28.20 + TypeScript 6.0.3 on
  both scaffolds (`--entryPoints App.tsx` on the React Native CLI 0.87.1 app; `--entryPoints App.tsx --entryPoints
  src/math.ts` on the Expo SDK 57 app; `--disableGit --disableSources` since neither had an `origin`): each
  undocumented default-exported component was reported as `default (CallSignature) ... does not have any
  documentation` (exit `4`), and after adding a one-line comment the metro run exited `0`. Two things the run
  depends on beyond the comments themselves:
  - **TypeDoc type-checks the whole `tsconfig.json` program first**, test files included — so a type error anywhere
    stops it with exit `3` before any doc validation. Verified on the Expo app: with Jest tests present and
    TypeScript 6's `types: []` default (which `expo/tsconfig.base` doesn't override), TypeDoc failed on `error
    TS2593: Cannot find name 'test'` in `__tests__/App.test.tsx`; adding `"types": ["jest"]` to the app's
    `tsconfig.json` fixed it (the metro template's `@react-native/typescript-config` already sets it). Report such a
    failure as "TypeDoc blocked by type errors (see `iru-typescript-code-quality`)", not as a doc gap — fixing the
    tsconfig is out of this skill's scope.
  - Expo's base tsconfig excludes `android`/`ios`; the metro template's `include: ["**/*.ts", "**/*.tsx"]` only
    excludes `node_modules` and `Pods`, which is harmless because the native projects hold no TypeScript — but if an
    `android/`/`ios/` `.ts` file ever shows up in a TypeDoc error, it's a tsconfig scoping issue to report, not a
    file to document.
  - The TypeDoc 0.28.20 + TypeScript 6.0.3 crash described below did **not** reproduce on either React Native
    scaffold (both ship TypeScript 6.0.3) — still check `npm ls typescript typedoc` if TypeDoc throws a `TypeError`.
- **Version-compatibility quirk (verified locally, worth checking before trusting a crash for a doc bug)**:
  TypeDoc 0.28.20 crashes outright (`TypeError: Cannot read properties of undefined (reading
  'PropertyDeclaration')`, not a warning) against a bare `npm install typescript`'s current default (TypeScript
  6.0.3), despite 6.0.x being in its declared peer range. Pinning `typescript` to `5.9.3` resolved it in this
  verification. If TypeDoc crashes this way, run `npm ls typescript typedoc` first and report the mismatch rather
  than treating it as an undocumented-symbol issue — it needs a dependency fix, not a doc fix, and is out of this
  skill's scope to silently "fix" by downgrading a project dependency.

### angular (and nestjs when Compodoc is configured) — Compodoc

```bash
npx compodoc -p tsconfig.json --silent --coverageTest <threshold> --coverageMinimumPerFile <threshold> --coverageTestShowOnlyFailed
```

- `--silent` (short form `-t`) is required to suppress Compodoc's own banner/progress log (an ASCII-art logo plus
  per-file parse trace) — verified locally this is pure noise the report must not surface; a **passing** run under
  `--silent` prints nothing at all and exits `0` (no "coverage OK" confirmation line — treat a clean exit code as
  the pass signal, not the absence of the word "not over threshold").
- `--coverageTest <threshold>` (project-wide gate; Compodoc's own default is 70 if omitted) and
  `--coverageMinimumPerFile <threshold>` (per-file gate; Compodoc's own default is 0, i.e. off, if omitted) —
  default both to 80 to match this catalog's coverage convention unless the project's own `.compodocrc.json`
  states otherwise (Step 2). A failing run's exit code is non-zero (verified: `1`) and — this is the useful part —
  it prints exactly which symbols dragged the file below the per-file minimum, e.g. `0 % for file src/index.ts -
  UndocumentedThing - under minimum per file`, which is symbol-level detail, not a raw report dump, safe to
  forward into the Step 6 report as-is.
- `--coverageTestShowOnlyFailed` keeps the output to failing files/symbols only, which is what keeps this
  report-only rather than a full coverage listing.
- `--coverageTestThresholdFail` defaults to `true` (non-zero exit on failure) — never pass `false`, that would
  turn a real gap into a silent warning.
- Compodoc writes its HTML site (default `./documentation/`) even in coverage-test mode — pass `-d
  "$TMPDIR/compodoc-out"` (or another scratch directory) so the run leaves nothing in the working tree; verified
  locally on a Nest 12 scaffold that with `-d` no `documentation/` directory was created and the exit code (`1`,
  coverage below threshold) was unchanged. **nestjs**: same command against the project's `tsconfig.json` (spec
  files are left out of the coverage count — verified: `app.controller.spec.ts` was not listed); the scaffold's
  own controller, service, and `main.ts` `bootstrap` each reported `0 % ... under minimum per file` before any
  TSDoc was added.
- Compodoc needs `-p <tsconfig>` pointing at a `tsconfig.json` that actually includes the in-scope files (verified
  locally it runs fine against a plain non-Angular `tsconfig.json` too, so this same invocation works even before
  Angular-specific decorators are involved) — if the project has a dedicated `tsconfig.doc.json` or similar,
  prefer that.

If either verification fails or warns, fix the offending comment(s) (syntax, a broken `{@link}`, a missing tag
the project's bar requires) and re-run until it succeeds. A failure naming a symbol **outside** the current scope
is pre-existing — note it in the report but don't fix it unless the user asks.

## Step 6 — Report

Per file in scope, state: how many exported symbols were already fully documented, how many gaps were found and
filled (name each, with its kind), and the final doc-build result (TypeDoc: pass, or the exact warning text and
symbol names that failed; Compodoc: the coverage percentage(s) achieved vs. the threshold, and the per-symbol
lines it reported for anything still under the per-file minimum; audit-only for a `nestjs`/`nextjs`/`react-native` project with
neither tool configured — say so explicitly rather than reporting a pass). If any argument resolved to a test file (Step
1), name it and note it was excluded since test files carry no TSDoc requirement here. If any out-of-scope
pre-existing doc-build failure surfaced in Step 5, mention it separately as a follow-up rather than silently
leaving it out of the report. Never paste the raw TypeDoc/Compodoc console output or generated HTML — report only
the symbol names, tags, and pass/fail result, per this catalog's report-only gate contract (mirrors how
`iru-gate-runner` expects every doc-comment audit it runs to summarize).

Do not run a full docs-site build beyond what Step 5 needs, fix lint/static-analysis issues unrelated to TSDoc, or
add/modify tests — those are a separate quality/implementation skill's job, if this project has one.
