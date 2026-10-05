---
name: nestjs
description: Use when building NestJS services. Covers module structure, providers and scopes, validation pipes, guards and interceptors, TypeORM/Prisma integration, and testing.
metadata:
  category: backend
  version: 1.0.0
  tags: [nestjs, typescript, node, di, validation]
---

# NestJS

## Purpose

Build NestJS applications where the module graph reflects the domain, validation happens at the edge, and cross-cutting concerns live in guards and interceptors rather than being copied into every controller.

## When to Use

- Building or reviewing a NestJS service.
- Structuring modules, providers, and their scopes.
- Implementing authentication, authorization, and request validation.
- Writing unit and end-to-end tests for a Nest application.

## Capabilities

- Module and provider design, including dynamic modules.
- Validation with `class-validator` and the global `ValidationPipe`.
- Guards (authorization), interceptors (cross-cutting), filters (error mapping).
- Data access with Prisma or TypeORM, correctly scoped.
- Testing with the Nest testing module and Supertest.

## Inputs

- The domain boundaries the modules should follow.
- The authentication scheme and the authorization model.
- The persistence layer.

## Outputs

- Modules that encapsulate a domain and export only their public services.
- A global validation pipe with whitelisting enabled.
- Controllers that are thin, and services that contain the logic.

## Workflow

1. **Model the modules on the domain** — One module per bounded capability, exporting the services other modules may use. A module that exports everything is not a boundary.
2. **Enable strict validation globally** — `whitelist: true` and `forbidNonWhitelisted: true`. Without these, a client can send extra fields and your DTO will happily carry them into the service.
3. **Push cross-cutting concerns out of controllers** — Auth in a guard, logging and timing in an interceptor, error mapping in an exception filter.
4. **Keep providers stateless and singleton** — Request-scoped providers cascade: anything that injects one becomes request-scoped too, and performance degrades quietly.
5. **Test at two levels** — Unit tests for services with mocked dependencies, and end-to-end tests through the real HTTP stack with a real (containerized) database.

## Best Practices

- `ValidationPipe` without `whitelist: true` is decoration, not validation. Extra properties pass straight through.
- `transform: true` on the pipe converts payloads into DTO class instances — otherwise your `@Type` decorators and defaults do nothing.
- Circular module dependencies are a design smell. `forwardRef` is an escape hatch that hides a boundary you drew wrong.
- Do not inject the repository into the controller. The controller's job is HTTP; the service's job is the domain.
- Global exception filters map domain errors to HTTP status codes in one place. Throwing `HttpException` from a service couples the domain to the transport.
- Use `ConfigModule` with a validation schema so a missing environment variable fails at boot.

## Examples

**Validation, guard, and thin controller:**

```typescript
// main.ts
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,             // strip unknown properties
    forbidNonWhitelisted: true,  // and reject the request if any are present
    transform: true,             // instantiate the DTO class
  }),
);
```

```typescript
export class CreateOrderDto {
  @IsUUID() customerId!: string;

  @IsArray()
  @ArrayMinSize(1)
  @ValidateNested({ each: true })
  @Type(() => OrderLineDto)
  lines!: OrderLineDto[];
}

@Controller("orders")
@UseGuards(JwtAuthGuard, TenantGuard)
export class OrdersController {
  constructor(private readonly orders: OrdersService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  create(@Body() dto: CreateOrderDto, @CurrentUser() user: User): Promise<OrderView> {
    return this.orders.place(user.tenantId, dto);
  }
}
```

**Domain errors mapped centrally:**

```typescript
@Catch(DomainError)
export class DomainExceptionFilter implements ExceptionFilter {
  catch(error: DomainError, host: ArgumentsHost) {
    const status = {
      NOT_FOUND: 404,
      CONFLICT: 409,
      INVALID: 422,
    }[error.kind] ?? 400;

    host.switchToHttp().getResponse().status(status).json({
      type: `https://api.example.com/errors/${error.kind.toLowerCase()}`,
      title: error.message,
      status,
    });
  }
}
```

## Notes

- Request-scoped providers instantiate a new instance per request and force the entire injection chain above them to do the same. Measure before using one.
- Nest's `TestingModule` lets you override any provider, which is almost always preferable to mocking a module's internals.
- Interceptors run around the handler and can transform the response. That makes them the right place for a response envelope — and the wrong place for business logic.
