---
name: nestjs
description: "Expert skill for NestJS framework development. Covers modules, providers/DI, controllers, guards, interceptors, pipes, exception filters, request lifecycle, GraphQL integration, WebSockets, microservices, CQRS, scheduling, queues, caching, health checks, testing, and platform abstraction (Express/Fastify). WHEN: \"NestJS\", \"nest.js\", \"@nestjs\", \"NestModule\", \"@Module\", \"@Injectable\", \"@Controller\", \"@Guard\", \"@UseGuards\", \"@UseInterceptors\", \"@UsePipes\", \"@Catch\", \"ExceptionFilter\", \"ValidationPipe\", \"class-validator\", \"NestJS testing\", \"TestingModule\", \"NestJS microservice\", \"NestJS GraphQL\", \"NestJS WebSocket\", \"NestJS CQRS\", \"NestJS guards\", \"NestJS interceptors\", \"NestJS pipes\", \"NestJS Swagger\", \"@nestjs/config\", \"@nestjs/typeorm\", \"@nestjs/mongoose\", \"NestJS Prisma\", \"NestJS BullMQ\". Do NOT use for general Node.js scripting, automation, or CLI-tool questions unrelated to the NestJS framework — that's the `cli-scripting` plugin's `nodejs` skill."
license: MIT
---

# NestJS

This skill covers NestJS framework development (v10.x+). NestJS is a progressive, TypeScript-first Node.js framework built on Angular-inspired module architecture with a powerful dependency injection system. It provides an opinionated structure for building scalable server-side applications while supporting Express or Fastify as the underlying HTTP platform.

## How to Approach Tasks

1. **Classify** the request:
   - **Architecture** -- Load `references/architecture.md` for module system, DI container, request lifecycle, decorator system, platform abstraction (Express/Fastify), guards vs middleware, interceptors vs pipes
   - **Best practices** -- Load `references/best-practices.md` for testing patterns (TestingModule, mock providers), authentication (Passport+JWT), authorization (guards+CASL), database (TypeORM/Prisma), microservices, deployment, common anti-patterns
   - **General backend** -- Use the `overview` skill for cross-framework API design, REST principles, framework comparison

2. **Identify context** -- Determine the specific NestJS subsystem: HTTP controllers, GraphQL resolvers, WebSocket gateways, microservice transports, or CQRS. Each has different decorators and lifecycle behavior.

3. **Load context** -- Read the relevant reference file before answering.

4. **Analyze** -- Apply NestJS-specific reasoning. Consider the request lifecycle order, DI scope propagation, module encapsulation boundaries, and the decorator metadata system.

5. **Recommend** -- Provide concrete TypeScript code examples. Always qualify trade-offs between simplicity and architecture.

6. **Verify** -- Suggest validation steps: unit tests with `TestingModule`, e2e tests with `supertest`, checking DI resolution, verifying guard/interceptor order.

## Core Architecture

### Module System

NestJS organizes code into modules. Each module encapsulates a feature domain with its own controllers, providers, and imports.

```typescript
@Module({
  imports: [TypeOrmModule.forFeature([User]), ConfigModule],
  controllers: [UsersController],
  providers: [UsersService, UsersRepository],
  exports: [UsersService], // only export what other modules need
})
export class UsersModule {}
```

- `imports` -- other modules whose exports this module needs
- `providers` -- DI-registered services, guards, interceptors, etc.
- `controllers` -- route handlers scoped to this module
- `exports` -- subset of providers re-exported for consumers

**Key rule:** Export only what other modules actually import. Over-exporting creates hidden coupling.

### Dependency Injection

NestJS DI is constructor-based by default. Providers are singleton-scoped unless overridden.

```typescript
@Injectable()
export class OrdersService {
  constructor(
    private readonly usersService: UsersService,
    @Inject('CONFIG') private readonly config: AppConfig,
  ) {}
}
```

**Three scopes:**
- `DEFAULT` (singleton) -- shared across the entire app. Use for stateless services.
- `REQUEST` -- new instance per HTTP request. Use for tenant-aware or audit services. **Warning:** propagates upward through the injection chain.
- `TRANSIENT` -- new instance per injection point. Rare.

### Request Lifecycle

Understanding the fixed execution order is essential for placing logic correctly:

```
Incoming Request
  -> Middleware         (Express-style, runs before routing)
  -> Guards            (authentication/authorization, return boolean)
  -> Interceptors      (before handler: transform request, start timers)
  -> Pipes             (validation and transformation of params/body)
  -> Route Handler     (your controller method)
  -> Interceptors      (after handler: transform response, log duration)
  -> Exception Filters (catch errors thrown anywhere above)
  -> Response
```

**Scope ordering within each stage:** Global -> Controller -> Route

Exception filters run in reverse scope order on error: Route -> Controller -> Global.

### Controllers

```typescript
@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  findAll(@Query('page') page = 1, @Query('limit') limit = 20) {
    return this.usersService.findAll({ page, limit });
  }

  @Get(':id')
  findOne(@Param('id', ParseUUIDPipe) id: string) {
    return this.usersService.findOne(id);
  }

  @Post()
  @HttpCode(201)
  create(@Body() dto: CreateUserDto) {
    return this.usersService.create(dto);
  }

  @Delete(':id')
  @HttpCode(204)
  @UseGuards(JwtAuthGuard, RolesGuard)
  @Roles('admin')
  remove(@Param('id', ParseUUIDPipe) id: string) {
    return this.usersService.remove(id);
  }
}
```

### Guards

Guards determine whether a request proceeds. They implement `CanActivate` and have access to `ExecutionContext` (including metadata).

```typescript
@Injectable()
export class RolesGuard implements CanActivate {
  constructor(private reflector: Reflector) {}

  canActivate(context: ExecutionContext): boolean {
    const roles = this.reflector.getAllAndOverride<string[]>('roles', [
      context.getHandler(), context.getClass(),
    ]);
    if (!roles?.length) return true;
    const { user } = context.switchToHttp().getRequest();
    return roles.some(role => user?.roles?.includes(role));
  }
}
```

**Guard vs Middleware:** Guards have `ExecutionContext` and work across HTTP/WS/microservices. Middleware is HTTP-only, runs earlier. Use guards for auth; use middleware for request mutation.

### Interceptors

Interceptors wrap the entire handler call using RxJS. They can transform both request and response.

```typescript
@Injectable()
export class TransformInterceptor<T> implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    return next.handle().pipe(
      map(data => ({ data, timestamp: new Date().toISOString() })),
    );
  }
}
```

### Pipes

Pipes validate and transform input parameters before the handler runs.

```typescript
// Global ValidationPipe -- validates all DTOs via class-validator
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
  transform: true,
  transformOptions: { enableImplicitConversion: true },
}));
```

### Exception Filters

Exception filters catch errors and convert them to HTTP responses.

```typescript
@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const status = exception instanceof HttpException
      ? exception.getStatus() : 500;
    response.status(status).json({
      success: false,
      error: { code: 'ERROR', message: 'Something went wrong' },
      timestamp: new Date().toISOString(),
    });
  }
}
```

## Key Integrations

### GraphQL

Code-first approach with `@nestjs/graphql` and Apollo:

```typescript
@Resolver(() => User)
export class UsersResolver {
  constructor(private readonly usersService: UsersService) {}

  @Query(() => [User])
  users() { return this.usersService.findAll(); }

  @Mutation(() => User)
  createUser(@Args('input') input: CreateUserInput) {
    return this.usersService.create(input);
  }

  @Subscription(() => User)
  userCreated() { return pubSub.asyncIterableIterator('userCreated'); }
}
```

### WebSockets

```typescript
@WebSocketGateway({ namespace: '/chat', cors: { origin: '*' } })
export class ChatGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer() server: Server;

  @SubscribeMessage('sendMessage')
  handleMessage(@MessageBody() payload: { room: string; message: string }) {
    this.server.to(payload.room).emit('message', payload);
  }
}
```

### Microservices

NestJS supports multiple transport layers: TCP, Redis, NATS, Kafka, RabbitMQ, gRPC.

```typescript
// Hybrid app -- HTTP + microservice
const app = await NestFactory.create(AppModule);
app.connectMicroservice<MicroserviceOptions>({
  transport: Transport.RMQ,
  options: { urls: [process.env.RABBITMQ_URL], queue: 'main' },
});
await app.startAllMicroservices();
await app.listen(3000);
```

```typescript
// Message pattern (request/response)
@MessagePattern({ cmd: 'get_order' })
getOrder(@Payload() data: { id: string }) { ... }

// Event pattern (fire and forget)
@EventPattern('user_registered')
handleUserRegistered(@Payload() data: UserRegisteredEvent) { ... }
```

### CQRS

Separate read and write concerns with `@nestjs/cqrs`:

```typescript
// Commands (writes)
const order = await this.commandBus.execute(new CreateOrderCommand(userId, items));

// Queries (reads)
const found = await this.queryBus.execute(new GetOrderQuery(orderId));
```

Use CQRS only when the domain has genuinely asymmetric read/write complexity or requires event sourcing. For CRUD-heavy services, it adds ceremony without benefit.

## Configuration

```typescript
@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      load: [appConfig, databaseConfig],
      validationSchema: Joi.object({
        PORT: Joi.number().default(3000),
        JWT_SECRET: Joi.string().required(),
        DATABASE_URL: Joi.string().required(),
      }),
    }),
  ],
})
export class AppModule {}
```

## Versioning

```typescript
// URI versioning: /v1/users, /v2/users
app.enableVersioning({ type: VersioningType.URI });

@Controller({ path: 'users', version: '1' })
export class UsersControllerV1 {}

@Controller({ path: 'users', version: '2' })
export class UsersControllerV2 {}
```

## Platform Abstraction

NestJS supports Express (default) and Fastify as HTTP adapters:

```typescript
// Fastify adapter -- ~20-30% throughput improvement
import { FastifyAdapter, NestFastifyApplication } from '@nestjs/platform-fastify';
const app = await NestFactory.create<NestFastifyApplication>(AppModule, new FastifyAdapter());
await app.listen(3000, '0.0.0.0');
```

**Caveat:** Express-only middleware (e.g., passport with sessions) may need shims on Fastify.

## Swagger / OpenAPI

```typescript
const config = new DocumentBuilder()
  .setTitle('My API')
  .setVersion('1.0')
  .addBearerAuth()
  .build();
const document = SwaggerModule.createDocument(app, config);
SwaggerModule.setup('api', app, document);
```

Use `@nestjs/swagger` CLI plugin to auto-generate `@ApiProperty` decorators from class-validator, reducing boilerplate.

## Architectural Decisions Quick Reference

| Decision | Guidance |
|---|---|
| **Guard vs Middleware** | Guards for auth (have ExecutionContext); middleware for request mutation (HTTP-only) |
| **Interceptor vs Pipe** | Pipes validate/transform input; interceptors wrap entire handler (modify response shape) |
| **Scope selection** | Default to singleton. REQUEST scope only for per-request state (tenant, audit) |
| **Dynamic modules** | Expose `register` (sync) and `registerAsync` (factory with DI) |
| **CQRS adoption** | Only for asymmetric read/write complexity or event sourcing |
| **forwardRef** | Last resort for circular deps -- prefer extracting shared services |
| **Entity exposure** | Never return ORM entities directly -- map to response DTOs |
| **synchronize: true** | Development only -- use migrations in production |

## Reference Files

Load these for deep knowledge on specific topics:

- `references/architecture.md` -- Module system, DI container, request lifecycle detail, decorator system, platform abstraction, dynamic modules, guards/interceptors/pipes/filters internals, GraphQL, WebSockets, microservices, CQRS, scheduling, queues, caching, health checks. **Load when:** architecture questions, lifecycle ordering, DI issues, integration setup.
- `references/best-practices.md` -- Testing patterns (TestingModule, mock providers, e2e), authentication (Passport+JWT, refresh tokens, OAuth2, API keys), authorization (RBAC guards, CASL policies), database patterns (TypeORM repository, Prisma service, Mongoose, transactions, migrations), microservices, deployment (Docker, PM2, graceful shutdown), performance (Fastify, caching, lazy modules), observability (Pino, OpenTelemetry, health checks), common anti-patterns. **Load when:** "how should I test", auth setup, database patterns, deployment, performance tuning.
