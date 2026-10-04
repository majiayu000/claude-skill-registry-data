---
name: bootgs-quickstart
description: Bootstraps a new Google Apps Script project on the bootgs framework (decorator-based routing and DI, Spring Boot/NestJS style). Covers the TypeScript config, appsscript.json manifest, clasp config, entry-point wiring (createApp/createAsyncApp, doGet/doPost/onOpen/onInstall/onMenu), directory layout, and build/deploy scripts. Use when starting a new bootgs project, adding bootgs to an existing Apps Script project, or when doGet/doPost/entry-point wiring needs to be set up or is misbehaving. Not for layering rules once the project has grown (`bootgs-architecture`), parameter validation (`bootgs-validation`), or calling the backend from a UI (`bootgs-client`).
license: Apache-2.0
compatibility: Requires Node.js >=22.14.0 and npm; scripts/check-latest-version.sh additionally requires curl and python3.
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
  framework: bootgs
---

# Bootgs Quickstart

## Available files

- **`assets/tsconfig.appsscript.json`** — starting `tsconfig.json`, see TypeScript configuration below.
- **`assets/appsscript.json`** — starting manifest, see Manifest below.
- **`scripts/fetch_policy.py`** — the shared fetching contract the version check fetches through: it names the script and the repository in the User-Agent, reads `robots.txt` before the target, paces requests, and stops rather than retries on 403/429/503. Vendored from `template/scripts/fetch_policy.py`; don't edit it here.
- **`scripts/check-latest-version.sh`** — checks the current published `bootgs`/`apps-script-utils` versions against what's installed. Run with `--help` for options.

## Install

```bash
npm install bootgs
```

Before scaffolding, check what's actually current — this skill is written against a specific release, and bootgs moves faster than any doc snapshot:

```bash
scripts/check-latest-version.sh
```

(`--json` for machine-readable output, `--help` for the full reference.) Queries the npm registry for the latest published `bootgs` and `apps-script-utils`, and compares against whatever's in your local `node_modules` if present. A version gap doesn't necessarily mean this skill's guidance is wrong, but it's the first thing to check before assuming a decorator or option documented here doesn't exist.

`apps-script-utils` and `reflect-metadata` come in transitively — bootgs depends on both directly. Do not add your own `import "reflect-metadata"`; bootgs's own entry point already does the side-effect import once, and a second import anywhere is harmless but redundant.

Requires Node >=22.14.0 to build (matches bootgs's own `engines` field) — CI images pinned to an older Node will fail to install, not just run.

## TypeScript configuration

Copy `assets/tsconfig.appsscript.json` as your starting point. The load-bearing options:

| Option | Value | Why |
|---|---|---|
| `experimentalDecorators` | `true` | bootgs decorators (`@RestController`, `@Injectable`, `@Get`, ...) require the legacy decorator proposal, not TC39 stage-3 decorators. |
| `emitDecoratorMetadata` | `true` | DI resolves constructor parameter types from emitted metadata (`reflect-metadata`). Without this, `@Inject` still needs an explicit token, but implicit type-based resolution silently breaks. |
| `useDefineForClassFields` | `false` | **Critical.** If left at the modern default (`true`), class fields are defined via `Object.defineProperty` after the constructor body runs, which overwrites values that decorator-based DI already injected into `this`. Symptom: injected services are `undefined` at runtime with no compile error. |
| `target` / `module` | `ESNext` | GAS's V8 runtime supports modern syntax; your bundler (not `tsc`) is what has to emit GAS-compatible output. |
| `types` | include `"google-apps-script"` | Native `GoogleAppsScript.*` ambient types for event objects, services, etc. |

## Manifest (`appsscript.json`)

Copy `assets/appsscript.json` as a baseline and trim `oauthScopes` to what you actually call — GAS enforces the declared scope list at authorization time, and an over-broad list just adds friction to the consent screen.

Non-negotiable fields:
- `runtimeVersion: "V8"` — required; bootgs uses class syntax and decorators that don't run on the legacy Rhino engine.
- `webapp.executeAs` / `webapp.access` — only needed if you expose `doGet`/`doPost` as a deployed web app (REST controllers). Skip this block for menu/sidebar-only add-ons.
- `exceptionLogging: "STACKDRIVER"` — routes uncaught errors to Cloud Logging; without it you're limited to the old Stackdriver-less execution log, which drops on script deletion.

## Directory layout

bootgs doesn't enforce a layout, but the framework's own decorator vocabulary (`@RestController`, `@Injectable`/`@Service`/`@Repository`) maps directly onto a layered structure:

```
src/
├── controller/    # @RestController / @Controller classes — HTTP or native-event entry points
├── service/       # @Injectable() business logic, injected into controllers
├── repository/    # @Injectable() (or @Repository()) data access — SpreadsheetApp, PropertiesService, etc.
├── domain/        # DTOs, entities, enums — no bootgs decorators, no dependency on the layers above
├── exceptions/    # AppException/HttpException subclasses + any @ControllerAdvice
└── main.ts        # entry point — see below
```

Controllers must only call services, services must only call repositories — bootgs won't enforce this for you (there's no module system to scope it). See `bootgs-architecture` for the full layering rules, an Interface+Impl convention, and a working `eslint-plugin-boundaries` config that enforces it mechanically; `bootgs-validation` for parameter validation inside controllers; `bootgs-openapi` for keeping a spec in sync with this layer.

## Entry point wiring

GAS calls global functions (`doGet`, `doPost`, `onOpen`, `onInstall`, ...) directly — there's no process you control the startup of. Every one of those globals must construct an app instance and delegate to it:

```ts
import { createApp, createAsyncApp, BootApplication, AsyncBootApplication, Newable } from "bootgs";
import { WidgetController } from "./controller/WidgetController";
import { MenuController } from "./controller/MenuController";
import { WidgetServiceImpl } from "./service/WidgetServiceImpl";
import { WidgetRepositoryImpl } from "./repository/WidgetRepositoryImpl";

const providers: Newable[] = [WidgetServiceImpl, WidgetRepositoryImpl];

// Menu-only entry points can pass a smaller controller set than the REST entry points.
export function onOpen(event: GoogleAppsScript.Events.SheetsOnOpen) {
  const app: BootApplication = createApp({ controllers: [MenuController], providers });
  app.onOpen(event);
}

export function onInstall(event: GoogleAppsScript.Events.AddonOnInstall) {
  const app: BootApplication = createApp({ controllers: [MenuController], providers });
  app.onInstall(event);
}

// Synchronous app — use only if no controller method returns a Promise.
export function doGet(event: GoogleAppsScript.Events.DoGet) {
  const app: BootApplication = createApp({ controllers: [WidgetController], providers });
  return app.doGet(event);
}

// Async app — use if any controller method is `async` or returns a Promise
// (e.g. it calls UrlFetchApp-wrapping code that you've promisified).
export async function doPost(event: GoogleAppsScript.Events.DoPost) {
  const app: AsyncBootApplication = createAsyncApp({ controllers: [WidgetController], providers });
  return app.doPost(event);
}
```

Gotchas:
- A new `createApp`/`createAsyncApp` call per global function is normal and cheap — GAS re-executes the whole file on every invocation anyway (no persistent process), so there's no shared-instance benefit to hoist it further.
- `ApplicationConfig.apiPrefix` defaults to `"/api"`. Every controller path is mounted under it unless you override it (`createApp({ controllers, providers, apiPrefix: null })` to disable, or a custom string). Forgetting this is the most common "route not found" cause — see `bootgs-client`.
- Menu callbacks: `app.onMenu` is a `Proxy` — any property access (`app.onMenu.myCallback`) dispatches an `AppsScriptEvent` named `myCallback` to a matching handler. You don't need to enumerate menu callback names anywhere except where you build the `Menu` UI itself.
- `Provider` accepts `useClass`/`useValue` today. `useFactory` and `useExisting` are declared in the types but not implemented (resolve to `null` at runtime as of the current release) — don't design around them yet.

## Build & deploy

`tsc` alone does not produce GAS-runnable output — GAS needs plain top-level function exports it can call by name, not an ES module graph. Use `tsc` only for type-checking (and `.d.ts` emit if you publish types), and a bundler (esbuild, Vite, Webpack — pick one) to produce the final bundle clasp pushes.

```json
{
  "scripts": {
    "typecheck": "tsc -p tsconfig.appsscript.json --noEmit",
    "build": "npm run typecheck && <bundler> build",
    "push": "clasp push -f",
    "deploy": "npm run build && npm run push"
  }
}
```

See `apps-script-clasp-workflow` for `.clasp.json`, versioned deployments, and multi-environment setups.

## Verification checklist

- [ ] `useDefineForClassFields: false` is set — otherwise DI fails silently.
- [ ] `runtimeVersion: "V8"` is set in `appsscript.json`.
- [ ] Every GAS global entry point (`doGet`, `doPost`, `onOpen`, `onInstall`, ...) constructs its own app instance and delegates — none are left as raw framework-less functions.
- [ ] `oauthScopes` in the manifest match only the services actually called.
- [ ] `npm run typecheck` passes before bundling.
