---
name: nestjs
description: NestJS modules, DI, guards, interceptors, OpenAPI. Use when building NestJS applications.
---

## nestjs

Build structured server-side apps with NestJS.

### Architecture
- Modules organize feature domains
- Controllers handle HTTP requests
- Providers (services) contain business logic
- Dependency injection via constructor injection

### Decorators & Guards
- Guards for auth/role-based access control
- Interceptors for request/response transformation
- Pipes for validation and transformation
- Exception filters for structured error responses

### OpenAPI / Swagger
- @nestjs/swagger decorators for API docs
- DTO classes with class-validator decorators
- Auto-generated Swagger UI at /api

### Database
- TypeORM or Prisma integration via modules
- Repository pattern with @InjectRepository
- Migrations for schema versioning

### Testing & Microservices
- Jest with Test.createTestingModule
- Microservices via @nestjs/microservices (TCP, Redis, RabbitMQ, Kafka)
- Hybrid apps with HTTP + microservice
