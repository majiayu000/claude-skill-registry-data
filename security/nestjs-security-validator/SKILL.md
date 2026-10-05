---
name: nestjs-security-validator
description: Enforces NestJS security best practices including input validation with class-validator, rate limiting with @nestjs/throttler, route authentication guards, Helmet headers, and CORS configuration.
version: 1.0.0
---

# NestJS Security Validator

Enforces security defaults and defensive programming across NestJS applications.

## 1. Global Input Validation (ValidationPipe)

In `main.ts`, always configure `ValidationPipe` with stripping and rejection of unwhitelisted properties to prevent parameter injection:

```typescript
// main.ts
import { ValidationPipe } from '@nestjs/common'

async function bootstrap() {
  const app = await NestFactory.create(AppModule)

  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,               // Strips properties without decorators in DTO
      forbidNonWhitelisted: true,    // Throws error if unknown property is sent
      transform: true,               // Auto-transforms payloads to DTO instance types
      transformOptions: {
        enableImplicitConversion: false, // Explicit types only
      },
    }),
  )
}
```

---

## 2. Rate Limiting (`@nestjs/throttler` v5+)

Prevent brute-force and DoS attacks:

```typescript
// app.module.ts
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler'
import { APP_GUARD } from '@nestjs/core'

@Module({
  imports: [
    ThrottlerModule.forRoot([
      {
        name: 'short',
        ttl: 1000,
        limit: 10, // 10 requests per second
      },
      {
        name: 'medium',
        ttl: 60000,
        limit: 100, // 100 requests per minute
      },
    ]),
  ],
  providers: [
    {
      provide: APP_GUARD,
      useClass: ThrottlerGuard,
    },
  ],
})
export class AppModule {}
```

---

## 3. Helmet & CORS Protection

```typescript
import helmet from 'helmet'

async function bootstrap() {
  const app = await NestFactory.create(AppModule)

  // Security HTTP headers
  app.use(helmet())

  // Explicit CORS
  app.enableCors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') ?? ['http://localhost:3000'],
    methods: ['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    credentials: true,
  })
}
```

---

## 4. DTO Validation Decorators

Every field in DTOs must have explicit `class-validator` decorators:

```typescript
import { IsEmail, IsNotEmpty, IsString, MinLength } from 'class-validator'

export class CreateUserDto {
  @IsEmail()
  @IsNotEmpty()
  email: string

  @IsString()
  @MinLength(8)
  password: string
}
```
