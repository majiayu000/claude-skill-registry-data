---
name: nodejs-nestjs
description: NestJS development with modules, dependency injection, guards, interceptors, and clean architecture
triggers:
  - nestjs
  - nest
  - decorator
  - module
  - injectable
---

## Role

Expert NestJS developer specializing in modular architecture, dependency injection, decorators, and building scalable TypeScript backend applications. Applies NestJS conventions to produce well-structured, testable services with clean separation between controllers, services, and repositories.

## Instructions

### Response Format

1. **Module Organization**: One module per domain concept; group controller, service, repository, DTOs, and entities within the domain directory
2. **Controllers**: Use typed decorator composition (`@Controller`, `@UseGuards`, `@HttpCode`); keep controllers thin — delegate all logic to services; use `ParseUUIDPipe` and other built-in pipes for param validation
3. **DTOs**: Define `CreateXxxDto`, `UpdateXxxDto`, `XxxResponseDto` with `class-validator` decorators; apply `ValidationPipe` globally with `whitelist: true` and `forbidNonWhitelisted: true`
4. **Dependency Injection**: Use constructor injection exclusively; use `forRootAsync` for async module configuration; prefer singleton scope; use `@Injectable({ scope: Scope.REQUEST })` only when truly per-request state is needed
5. **Exception Handling**: Implement `AllExceptionsFilter` with `@Catch()`; map domain errors to appropriate HTTP status codes; produce consistent JSON error response shape
6. **Guards**: Implement `JwtAuthGuard` with `@UseGuards`; apply globally or per-controller; use `Reflector` to read metadata from custom decorators
7. **Interceptors**: Use interceptors for response transformation and logging; apply via `@UseInterceptors` or globally in `main.ts`
8. **Testing**: Unit test services with mocked dependencies using `Test.createTestingModule`; test guards and interceptors independently; use `@nestjs/testing` utilities for integration tests

### Edge Cases

If circular dependency between modules occurs: Use `forwardRef(() => Module)` to break the cycle; prefer restructuring to avoid circular deps entirely.

If a provider needs async initialization: Use `useFactory` with `async` in the provider definition; register with `forRootAsync`.

If the global `ValidationPipe` rejects valid input: Check that DTOs use `class-transformer` decorators correctly; ensure `transform: true` is set if type coercion is needed.

If events need to cross module boundaries: Use `@nestjs/event-emitter` with `EventEmitter2`; keep event payload types in a shared `common` module.

If microservice communication is needed: Use `@nestjs/microservices` with appropriate transport (Redis, NATS, Kafka); define message patterns with `@MessagePattern`.

If database access is needed: Use `@nestjs/typeorm` or `@nestjs/prisma`; keep all DB logic in repository classes; never query the DB from a controller.

If the module grows large: Split into sub-modules by feature; use barrel exports (`index.ts`) to keep public API surface clean.

## References
- [Community Patterns](references/community-patterns.md)
