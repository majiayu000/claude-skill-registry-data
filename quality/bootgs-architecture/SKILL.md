---
name: bootgs-architecture
description: Establishes a strict layered architecture for a bootgs project — Controller → Service → Repository → Domain, one-directional dependencies, an Interface+Impl naming convention, and a working eslint-plugin-boundaries config that enforces it mechanically. Use when structuring a bootgs backend beyond a single controller, reviewing a PR that adds a repository or service, or when "hold the layering by discipline" has already broken down once. Not for initial project setup or entry-point wiring (`bootgs-quickstart`), nor for validating a handler's inputs (`bootgs-validation`).
license: Apache-2.0
metadata:
  author: Maksym Stoianov
  version: "1.0.0"
  framework: bootgs
---

# Bootgs Architecture

## Available files

- **`assets/eslint-boundaries.config.ts`** — a working [`eslint-plugin-boundaries`](https://www.npmjs.com/package/eslint-plugin-boundaries) config enforcing every rule below. Copy it in and adjust the `files` glob to your source root. The `index.ts`-barrel rules are marked `OPTIONAL` — see Gotchas. The rule option names (`boundaries/elements`, `boundaries/dependencies`, the `captured`/`disallow`/`to` syntax) are a versioned fact about the plugin's own API, not this skill's — if lint throws an unrecognized-option error on install, check the installed `eslint-plugin-boundaries` version's own docs/changelog before assuming this config is wrong.

## Layers and the one rule that matters

Dependencies point in one direction only: **Controller → Service → Repository → Domain**. bootgs's `@RestController`/`@Injectable()`/`@Repository()` decorators (see `bootgs-quickstart`) don't enforce this — there's no module system to scope it — so the rule has to be held either by review discipline or by the lint config below. Discipline erodes after a few PRs; the lint config doesn't.

| Layer | Contains | May import | Must not import |
|---|---|---|---|
| **Domain** | Entities (rich models with invariants), DTOs, enums, types, constants — pure TypeScript, no bootgs decorators | nothing above it | controller, service, repository, exceptions |
| **Exceptions** | Domain-specific `Error` subclasses | domain | controller, service, repository |
| **Repository** | Data access via `SpreadsheetApp`/`PropertiesService`/`CacheService`, marked `@Repository()` | domain, exceptions, shared | controller, service, another repository (one narrow exception — see Gotchas) |
| **Service** | Business logic, coordinates repositories, marked `@Injectable()` | domain, exceptions, repository, shared | controller |
| **Controller** | `@RestController` classes — deserialize input, call services, format output | domain, exceptions, service, shared | another controller, a repository directly |
| **Shared** | Cross-cutting utilities (guards, formatters) with no domain knowledge | nothing above it | controller, service, repository, domain, exceptions |

## The Interface + Impl convention

Every repository and service is split into an interface (the contract) and an `*Impl` class (the bootgs-decorated implementation). Callers depend on the interface; DI is wired to the concrete class:

```ts
// repository/interfaces/WidgetRepository.ts — the contract, safe to import from the layer above
export abstract class WidgetRepository {
  abstract findById(id: string): Widget | null;
  abstract save(widget: Widget): void;
}
```

```ts
// repository/WidgetRepositoryImpl.ts — the only file that knows it's PropertiesService/SpreadsheetApp underneath
import { Repository } from "bootgs";
import { WidgetRepository } from "./interfaces/WidgetRepository";

@Repository()
export class WidgetRepositoryImpl implements WidgetRepository {
  findById(id: string): Widget | null { /* ... */ return null; }
  save(widget: Widget): void { /* ... */ }
}
```

```ts
// service/WidgetServiceImpl.ts — depends on the interface, injected with the concrete class token
import { Injectable, Inject } from "bootgs";
import { WidgetRepository } from "../repository/interfaces/WidgetRepository";
import { WidgetRepositoryImpl } from "../repository/WidgetRepositoryImpl";

@Injectable()
export class WidgetServiceImpl {
  constructor(@Inject(WidgetRepositoryImpl) private readonly repository: WidgetRepository) {}
}
```

Swapping `WidgetRepositoryImpl` for a different storage backend later touches one `@Inject` token, not every caller.

## Gotchas

- **The one legitimate cross-repository import is a storage primitive, not a shortcut.** A repository may depend on another repository only when that other repository is a genuinely generic, business-logic-free storage wrapper — for example, a settings/key-value repository built directly on `PropertiesService` that other repositories reuse instead of re-implementing property-access boilerplate. This is not precedent for two domain-specific repositories depending on each other. If a review argues "we already allow one exception," check whether the dependency is actually a storage primitive first — if it has any business logic of its own, it isn't.
- **Whether a layer funnels its public surface through `index.ts` is a project choice, not something this skill mandates.** Barrel-exporting a layer (and treating everything else in it as private) makes internal reshuffling cheap and gives every consumer one import path — at the cost of a file to maintain and an extra hop when navigating. Pick a style and apply it consistently: if the project uses `index.ts` barrels, a deep import that reaches past one is a real boundary violation worth flagging; if it doesn't, importing a layer's files directly is just how the project works. The bundled ESLint rules for barrel enforcement are marked and separated from the core layer-direction rules in `assets/eslint-boundaries.config.ts` — delete that block if the project doesn't use barrels.
- **Domain must not import forward.** An entity that imports a repository or exception "just this once" to validate itself against stored data has already moved orchestration into the model layer — that validation belongs in a service.
- **Keep DTOs one-per-file in `domain/dto/`.** `bootgs-openapi`'s generator resolves request/response shapes from exactly this convention — a DTO folded into a larger file or inlined in a controller signature won't resolve into a clean schema (see `bootgs-openapi`).

## Enforcing it with ESLint

`assets/eslint-boundaries.config.ts` implements every rule in the table above, including the storage-primitive exception (generalize the filename match if your project's primitive repository is named differently). The `index.ts`-barrel rules are marked `OPTIONAL` and grouped separately — keep them only if the project actually funnels layers through barrel files. Add the config to a flat ESLint config:

```ts
import boundariesConfig from "./eslint-boundaries.config";
import { defineConfig } from "eslint/config";

export default defineConfig([/* ...your other configs */, boundariesConfig]);
```

## Verification

- [ ] Every repository and service has a separate interface and a `*Impl` file; nothing outside its own layer imports the `*Impl` class directly except through DI.
- [ ] No repository imports another repository, except a documented storage-primitive one.
- [ ] No controller imports another controller or a repository directly.
- [ ] Domain and exceptions have zero imports from controller, service, or repository.
- [ ] `eslint-plugin-boundaries` (or an equivalent rule) runs in CI, not just in a human review checklist.
