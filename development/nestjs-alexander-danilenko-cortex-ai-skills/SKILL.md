---
name: nestjs
description: "Opinionated house conventions for NestJS backends — module boundaries and layering, provider wiring and injection scopes, guards/interceptors/pipes/filters, DTOs and validation, domain exceptions, config, and the Nest 11 / Express 5 behaviour that compiles cleanly and fails at runtime. Use whenever the code is NestJS (`@nestjs/*` in package.json, or `@Module`/`@Injectable`/`@Controller`/`@Cron` in the file), including when the question sounds like plain TypeScript, an OOP refactor, a code review, or an ops problem — the Nest-specific answer differs from the generic one. Typical asks: scaffolding a module, adding a controller, provider, or endpoint, wiring an enhancer, a boot-time DI or circular-import failure, a response leaking entity fields despite `@Exclude()`, a cron job firing on every replica, upgrading NestJS, or reviewing a Nest diff. Not for plain Express or Fastify, Angular, frontend, SQL, or CI."
---

# NestJS

House conventions for NestJS backends on v11 / Express 5. Apply them to code you are writing or changing — don't restructure untouched modules unless asked.

Examples throughout use an invented shipment domain purely to make the shape concrete. Read the structure, not the names.

## Layering

Two layers, and the dependency arrow points one way only.

```text
core/   domain + infrastructure. No controllers, no HTTP.        → core only
app/    features. Controllers, DTOs, guards, middleware, CQRS.   → app + core
```

A core module that needs to reach into a feature is telling you the concept it owns sits in the wrong layer — move the concept down rather than importing upward. Keeping the arrow honest is what lets a core module be driven by an HTTP request, a cron job, a CLI, or a queue consumer without dragging a controller along.

## Always apply

These hold for nearly every change, so they live here rather than behind a reference:

- **A module owns one domain, and its root barrel exports only the `.module.ts`.** A provider that isn't exported can be refactored freely; one that is becomes public API.
- **Controllers translate HTTP and delegate; services hold the logic.** A controller that branches on business rules can't be reused by a job, a CLI, or a queue consumer, and its tests need an HTTP layer to say anything.
- **Every request body, query, and param goes through a DTO with `class-validator`**, behind a `ValidationPipe` with `whitelist: true`, `forbidNonWhitelisted: true`, `transform: true`. Without whitelisting, an unexpected property rides through into your persistence layer.
- **Response DTOs are what leaves the process.** Returning an entity leaks whatever a future migration adds to the table — password hashes, internal flags, soft-delete columns — with no code change to notice.
- **Domain errors extend one base class and are rendered by one global filter.** A bare `Error` becomes a 500, so a legitimate "not found" pages someone.
- **Global enhancers are registered with `APP_GUARD` / `APP_PIPE` / `APP_INTERCEPTOR` / `APP_FILTER`.** `app.useGlobal*()` binds outside any module, so those instances cannot inject anything.
- **No domain service imports a vendor SDK.** The payment gateway, database client, and mail provider each get a wrapper module; a major SDK bump becomes one module's problem.

## Wrong by default

Six behaviours that contradict what the API name suggests, so they get stated here rather than in a reference you would only open if you already suspected a problem. Each one compiles cleanly and fails at runtime.

- **Express 5 wildcards must be named.** `@Get("files/*")` and `forRoutes("*")` no longer match — write `@Get("files/*splat")` and `forRoutes("{*splat}")`. `:param?` is gone too.
- **Exception filters resolve route → controller → global**, the inverse of guards and pipes, and interceptors unwind first-in-last-out. A route-scoped filter shadows the global one.
- **`@Res()` opts the handler out of the framework's response handling** — `@HttpCode`, `@Header`, serialization, and every response interceptor stop applying. Add `{ passthrough: true }` unless you are sending the response yourself.
- **`ClassSerializerInterceptor` only transforms class instances.** Returning `{ user: new UserEntity() }` skips `@Exclude()` silently and ships the excluded field.
- **`ttl` is milliseconds** in `@nestjs/cache-manager` and `@nestjs/throttler`, and a cache `ttl: 0` means never expire, not "don't cache".
- **`ClientProxy.send()` returns a cold Observable** and `HttpService` returns one too — nothing happens until something subscribes.

The first and the fifth are version-specific. Check `@nestjs/core` in `package.json` before applying anything in this skill marked v11, and read `references/nestjs-11-migration.md` if the project is older.

## Reference map

Read the file that matches the change; don't preload all of them.

| Working on | Read |
| --- | --- |
| Directory layout, filenames, barrels, CQRS vs service, persistence | `references/architecture.md` |
| Providers, tokens, scopes, `ModuleRef`, circular deps, lifecycle hooks | `references/dependency-injection.md` |
| Guards, interceptors, pipes, middleware, decorators, responses, versioning | `references/request-lifecycle.md` |
| DTOs, class-validator, serialization, Swagger/OpenAPI | `references/dto-validation-openapi.md` |
| Exceptions, exception filters, error messages | `references/errors.md` |
| `ConfigModule`, `ConfigService`, logging | `references/configuration-and-logging.md` |
| `@nestjs/axios`, `event-emitter`, `bullmq`, `throttler`, `cache-manager`, `schedule`, microservices | `references/ecosystem-packages.md` |
| Upgrading from v10, or code that predates Express 5 | `references/nestjs-11-migration.md` |
| Tests | the `cortex-testing:conventions` skill's NestJS Jest references |

When you are reviewing rather than writing, `references/request-lifecycle.md` and `references/nestjs-11-migration.md` catch the most defects per line read: enhancer ordering and Express 5 route syntax both fail in ways that type-check cleanly.
