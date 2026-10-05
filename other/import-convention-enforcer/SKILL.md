---
name: nestjs-import-enforcer
description: Automatically enforce absolute imports from barrel exports in NestJS. Use when writing imports, creating TypeScript files, or organizing NestJS module structure.
---

# Import Convention Enforcer (NestJS)

Auto-enforces absolute imports from barrel exports for clean, maintainable NestJS code.

## When This Skill Activates

I automatically run when:
- User writes or modifies TypeScript files
- User creates entities, DTOs, services, controllers
- User imports from other modules
- User mentions "import", "NestJS", "module"
- User organizes project structure

## Required Import Pattern (MANDATORY)

**✅ CORRECT - Absolute imports from barrel exports:**
```typescript
// Absolute path from src/
import { User, Profile } from 'src/users/entities'
import { UsersService } from 'src/users/services'
import { CreateUserDto, UpdateUserDto } from 'src/users/dto'
import { JwtAuthGuard } from 'src/auth/guards'

// NestJS/Third-party - standard imports
import { Injectable, NotFoundException } from '@nestjs/common'
import { InjectRepository } from '@nestjs/typeorm'
```

**❌ WRONG - Relative imports:**
```typescript
import { User } from './entities/user.entity'
import { UsersService } from '../services/users.service'
import { JwtAuthGuard } from '../../auth/guards/jwt-auth.guard'
```

**❌ WRONG - Import from specific files (not barrel):**
```typescript
import { User } from 'src/users/entities/user.entity'
```

## Auto-Fix Process

### Step 1: Detect Violations

```typescript
// ❌ User writes
import { User } from './entities/user.entity'
import { CreateUserDto } from '../dto/create-user.dto'
import { AuthService } from '../../auth/services/auth.service'
```

### Step 2: Convert to Absolute Barrel Imports

```typescript
// ✅ Auto-fixed to
import { User } from 'src/users/entities'
import { CreateUserDto } from 'src/users/dto'
import { AuthService } from 'src/auth/services'
```

### Step 3: Organize Import Order

```typescript
// ✅ Final organized imports
// 1. NestJS core
import { Injectable, NotFoundException } from '@nestjs/common'
import { InjectRepository } from '@nestjs/typeorm'

// 2. Third-party
import { Repository } from 'typeorm'

// 3. Project modules (absolute from src/)
import { User, Profile } from 'src/users/entities'
import { CreateUserDto, UpdateUserDto } from 'src/users/dto'
import { AuthService } from 'src/auth/services'
```

## Import Organization Rules

### 1. Import Categories (Top to Bottom)

```typescript
// 1. NestJS core
import { Module, Injectable, Controller } from '@nestjs/common'
import { TypeOrmModule } from '@nestjs/typeorm'

// 2. Third-party libraries
import { Repository } from 'typeorm'
import { ApiTags, ApiOperation } from '@nestjs/swagger'

// 3. Project modules (src/ absolute imports)
import { User } from 'src/users/entities'
import { UsersService } from 'src/users/services'
import { JwtAuthGuard } from 'src/auth/guards'

// 4. Local module imports (from barrel)
import { CreateUserDto } from './dto'
import { UserResponseDto } from './dto'
```

### 2. Named Imports (Alphabetical)

```typescript
// ✅ CORRECT
import { Injectable, Logger, NotFoundException } from '@nestjs/common'

// ❌ WRONG
import { NotFoundException, Injectable, Logger } from '@nestjs/common'
```

## Module Structure with Barrel Exports

```
users/
├── users.module.ts
├── entities/
│   ├── user.entity.ts
│   └── index.ts       # export * from './user.entity'
├── dto/
│   ├── create-user.dto.ts
│   └── index.ts       # export * from './create-user.dto'
├── services/
│   ├── users.service.ts
│   └── index.ts       # export * from './users.service'
└── controllers/
    ├── users.controller.ts
    └── index.ts       # export * from './users.controller'
```

## Complete Service Example

```typescript
// users/services/users.service.ts
import { Injectable, NotFoundException } from '@nestjs/common'
import { InjectRepository } from '@nestjs/typeorm'
import { Repository } from 'typeorm'

// ✅ Absolute imports from barrels
import { User } from 'src/users/entities'
import { CreateUserDto, UpdateUserDto } from 'src/users/dto'
import { AuthService } from 'src/auth/services'

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private readonly userRepository: Repository<User>,
    private readonly authService: AuthService,
  ) {}

  async create(dto: CreateUserDto): Promise<User> {
    const user = this.userRepository.create(dto)
    return this.userRepository.save(user)
  }

  async findOne(id: string): Promise<User> {
    const user = await this.userRepository.findOne({ where: { id } })

    if (!user) {
      throw new NotFoundException(`User with ID ${id} not found`)
    }

    return user
  }
}
```

## Complete Controller Example

```typescript
// users/controllers/users.controller.ts
import {
  Controller,
  Get,
  Post,
  Body,
  Param,
  UseGuards,
} from '@nestjs/common'
import { ApiTags, ApiOperation, ApiBearerAuth } from '@nestjs/swagger'

// ✅ Absolute imports from barrels
import { UsersService } from 'src/users/services'
import { CreateUserDto, UpdateUserDto, UserResponseDto } from 'src/users/dto'
import { JwtAuthGuard } from 'src/auth/guards'
import { CurrentUser } from 'src/common/decorators'
import { User } from 'src/users/entities'

@ApiTags('users')
@Controller('users')
@UseGuards(JwtAuthGuard)
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Post()
  @ApiOperation({ summary: 'Create new user' })
  async create(@Body() dto: CreateUserDto): Promise<UserResponseDto> {
    return this.usersService.create(dto)
  }

  @Get(':id')
  @ApiBearerAuth()
  @ApiOperation({ summary: 'Get user by ID' })
  async findOne(@Param('id') id: string): Promise<UserResponseDto> {
    return this.usersService.findOne(id)
  }
}
```

## Cross-Module Imports

```typescript
// orders/services/orders.service.ts
import { Injectable } from '@nestjs/common'

// ✅ Import from other modules using absolute paths
import { User } from 'src/users/entities'
import { UsersService } from 'src/users/services'
import { Product } from 'src/products/entities'
import { ProductsService } from 'src/products/services'

@Injectable()
export class OrdersService {
  constructor(
    private readonly usersService: UsersService,
    private readonly productsService: ProductsService,
  ) {}

  async createOrder(userId: string, productId: string) {
    const user = await this.usersService.findOne(userId)
    const product = await this.productsService.findOne(productId)
    // Create order...
  }
}
```

## Local Module Imports

Within the same module, you can use local barrel imports:

```typescript
// users/services/users.service.ts
import { Injectable } from '@nestjs/common'

// ✅ Local barrel import (shorter)
import { User } from '../entities'
import { CreateUserDto } from '../dto'

// ✅ Also acceptable (explicit)
import { User } from 'src/users/entities'
import { CreateUserDto } from 'src/users/dto'
```

## TypeScript Configuration

Ensure `tsconfig.json` supports absolute imports:

```json
{
  "compilerOptions": {
    "baseUrl": "./",
    "paths": {
      "src/*": ["src/*"]
    }
  }
}
```

## Common Violations

### Violation 1: Relative Imports

```typescript
// ❌ WRONG
import { User } from './entities/user.entity'
import { UsersService } from '../services/users.service'

// ✅ CORRECT
import { User } from 'src/users/entities'
import { UsersService } from 'src/users/services'
```

### Violation 2: Importing from Specific Files

```typescript
// ❌ WRONG - Skip barrel
import { User } from 'src/users/entities/user.entity'

// ✅ CORRECT - Use barrel
import { User } from 'src/users/entities'
```

### Violation 3: Inconsistent Paths

```typescript
// ❌ WRONG - Mixing styles
import { User } from 'src/users/entities'
import { CreateUserDto } from './dto/create-user.dto'

// ✅ CORRECT - Consistent
import { User } from 'src/users/entities'
import { CreateUserDto } from 'src/users/dto'
```

## Module Pattern Best Practices

```typescript
// users/users.module.ts
import { Module } from '@nestjs/common'
import { TypeOrmModule } from '@nestjs/typeorm'

// ✅ Clean local imports from barrels
import { User, Profile } from './entities'
import { UsersService } from './services'
import { UsersController } from './controllers'

// ✅ Cross-module imports absolute
import { AuthModule } from 'src/auth/auth.module'

@Module({
  imports: [
    TypeOrmModule.forFeature([User, Profile]),
    AuthModule,
  ],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

## Success Criteria

✅ ALL imports use absolute paths from `src/`
✅ ALL imports use barrel exports
✅ NO relative imports
✅ Imports organized by category
✅ Consistent import style across project

## Skill Behavior

**I am PROACTIVE:**
- I detect relative imports AUTOMATICALLY
- I convert to absolute barrel imports IMMEDIATELY
- I organize import order
- I ensure barrel exports exist
- I explain import patterns

**I do NOT:**
- Allow relative imports
- Allow imports from specific files (skip barrels)
- Accept inconsistent import styles

**I ALWAYS:**
- Use `src/` absolute paths
- Import from barrel exports (`index.ts`)
- Organize imports by category
- Keep imports clean and maintainable

This ensures clean, maintainable NestJS import structure from day one.
