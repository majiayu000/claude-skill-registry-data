---
name: nestjs-testing-patterns
description: Guides writing isolated unit tests and integration tests for NestJS controllers, services, and guards using Test.createTestingModule() and Vitest/Jest.
version: 1.0.0
---

# NestJS Testing Patterns

Best practices for writing unit and integration tests in NestJS applications.

## 1. Service Unit Testing (Mocked Dependencies)

Test business logic in isolation by overriding providers with mocks:

```typescript
import { Test, TestingModule } from '@nestjs/testing'
import { UsersService } from './users.service'
import { getRepositoryToken } from '@nestjs/typeorm'
import { User } from '../entities'

describe('UsersService', () => {
  let service: UsersService
  const mockUserRepository = {
    find: jest.fn(),
    findOneBy: jest.fn(),
    save: jest.fn(),
  }

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [
        UsersService,
        {
          provide: getRepositoryToken(User),
          useValue: mockUserRepository,
        },
      ],
    }).compile()

    service = module.get<UsersService>(UsersService)
  })

  it('should find user by id', async () => {
    const expectedUser = { id: 'uuid-1', email: 'test@example.com' }
    mockUserRepository.findOneBy.mockResolvedValue(expectedUser)

    const result = await service.findById('uuid-1')
    expect(result).toEqual(expectedUser)
    expect(mockUserRepository.findOneBy).toHaveBeenCalledWith({ id: 'uuid-1' })
  })
})
```

---

## 2. Controller Unit Testing

```typescript
import { Test, TestingModule } from '@nestjs/testing'
import { UsersController } from './users.controller'
import { UsersService } from './users.service'

describe('UsersController', () => {
  let controller: UsersController
  const mockUsersService = {
    findAll: jest.fn().mockResolvedValue([]),
  }

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [UsersController],
      providers: [
        {
          provide: UsersService,
          useValue: mockUsersService,
        },
      ],
    }).compile()

    controller = module.get<UsersController>(UsersController)
  })

  it('should return an array of users', async () => {
    expect(await controller.findAll()).toEqual([])
  })
})
```

---

## 3. End-to-End (e2e) Integration Testing

```typescript
import { Test, TestingModule } from '@nestjs/testing'
import { INestApplication, ValidationPipe } from '@nestjs/common'
import * as request from 'supertest'
import { AppModule } from '../src/app.module'

describe('App (e2e)', () => {
  let app: INestApplication

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile()

    app = moduleFixture.createNestApplication()
    app.useGlobalPipes(new ValidationPipe({ whitelist: true }))
    await app.init()
  })

  afterAll(async () => {
    await app.close()
  })

  it('/api/health (GET)', () => {
    return request(app.getHttpServer())
      .get('/api/health')
      .expect(200)
      .expect({ status: 'ok' })
  })
})
```
