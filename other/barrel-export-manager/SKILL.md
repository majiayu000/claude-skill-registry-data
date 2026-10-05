---
name: barrel-export-manager
description: This skill should be used when the user asks to "create barrel exports", "add index.ts", "organize exports", "create entity", "add DTO", "create service", or when adding files to NestJS module directories. Auto-maintains barrel exports.
---

# Barrel Export Manager

Auto-creates and maintains `index.ts` barrel export files in NestJS modules for clean, maintainable imports.

## Activation Triggers

This skill activates when:
- Creating new entity, DTO, service, controller, guard, decorator
- Adding files to module directories
- Organizing NestJS module structure
- Mentioning "NestJS", "module", "create"
- Importing from module directories

## Required Pattern (MANDATORY)

Every NestJS module folder MUST have `index.ts` barrel exports:

```
users/
├── entities/
│   ├── user.entity.ts
│   ├── profile.entity.ts
│   └── index.ts          # ✅ Barrel export
├── dto/
│   ├── create-user.dto.ts
│   ├── update-user.dto.ts
│   └── index.ts          # ✅ Barrel export
├── services/
│   ├── users.service.ts
│   └── index.ts          # ✅ Barrel export
└── controllers/
    ├── users.controller.ts
    └── index.ts          # ✅ Barrel export
```

## Auto-Management Process

### Step 1: Detect New File

When user creates:
```typescript
// users/entities/user.entity.ts
@Entity('users')
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string
  // ...
}
```

### Step 2: Auto-Create/Update index.ts

Automatically create or update `users/entities/index.ts`:

```typescript
// users/entities/index.ts
export * from './user.entity'
export * from './profile.entity'
```

### Step 3: Verify Imports Use Barrel

Ensure other files import from barrel:

```typescript
// ✅ CORRECT - Import from barrel
import { User, Profile } from 'src/users/entities'

// ❌ WRONG - Import from specific file
import { User } from 'src/users/entities/user.entity'
```

### Step 4: Update on File Changes

When files are added/removed/renamed, automatically update the barrel export:

```typescript
// User adds: organization.entity.ts
// Automatically update index.ts:
export * from './user.entity'
export * from './profile.entity'
export * from './organization.entity'  // ✅ Added automatically
```

## Barrel Export Patterns

### Entities Directory

```typescript
// users/entities/index.ts
export * from './user.entity'
export * from './profile.entity'
export * from './organization.entity'

// Usage
import { User, Profile, Organization } from 'src/users/entities'
```

### DTOs Directory

```typescript
// users/dto/index.ts
export * from './create-user.dto'
export * from './update-user.dto'
export * from './user-response.dto'
export * from './filter-user.dto'

// Usage
import { CreateUserDto, UpdateUserDto, UserResponseDto } from 'src/users/dto'
```

### Services Directory

```typescript
// users/services/index.ts
export * from './users.service'
export * from './auth.service'
export * from './email.service'

// Usage
import { UsersService, AuthService } from 'src/users/services'
```

### Controllers Directory

```typescript
// users/controllers/index.ts
export * from './users.controller'
export * from './auth.controller'

// Usage
import { UsersController, AuthController } from 'src/users/controllers'
```

### Guards Directory

```typescript
// auth/guards/index.ts
export * from './jwt-auth.guard'
export * from './roles.guard'
export * from './api-key.guard'

// Usage
import { JwtAuthGuard, RolesGuard } from 'src/auth/guards'
```

### Decorators Directory

```typescript
// common/decorators/index.ts
export * from './current-user.decorator'
export * from './roles.decorator'
export * from './api-paginated-response.decorator'

// Usage
import { CurrentUser, Roles } from 'src/common/decorators'
```

## Complete Module Example

```
users/
├── users.module.ts
├── entities/
│   ├── user.entity.ts
│   ├── profile.entity.ts
│   └── index.ts              # export * from './user.entity'; export * from './profile.entity'
├── dto/
│   ├── create-user.dto.ts
│   ├── update-user.dto.ts
│   └── index.ts              # export * from './create-user.dto'; ...
├── services/
│   ├── users.service.ts
│   └── index.ts              # export * from './users.service'
├── controllers/
│   ├── users.controller.ts
│   └── index.ts              # export * from './users.controller'
└── tests/
    └── users.service.spec.ts
```

**Module file uses barrel exports:**

```typescript
// users/users.module.ts
import { Module } from '@nestjs/common'
import { TypeOrmModule } from '@nestjs/typeorm'

// ✅ Clean imports from barrels
import { User, Profile } from './entities'
import { UsersService } from './services'
import { UsersController } from './controllers'

@Module({
  imports: [TypeOrmModule.forFeature([User, Profile])],
  controllers: [UsersController],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

## Benefits of Barrel Exports

### 1. Clean Imports

```typescript
// ❌ WITHOUT barrels - Verbose
import { User } from 'src/users/entities/user.entity'
import { Profile } from 'src/users/entities/profile.entity'
import { Organization } from 'src/users/entities/organization.entity'
import { CreateUserDto } from 'src/users/dto/create-user.dto'
import { UpdateUserDto } from 'src/users/dto/update-user.dto'

// ✅ WITH barrels - Clean
import { User, Profile, Organization } from 'src/users/entities'
import { CreateUserDto, UpdateUserDto } from 'src/users/dto'
```

### 2. Easier Refactoring

```typescript
// Rename user.entity.ts → user-account.entity.ts
// Only update one file (index.ts):
export * from './user-account.entity'  // Updated filename

// All imports still work:
import { User } from 'src/users/entities'  // ✅ No changes needed
```

### 3. Encapsulation

```typescript
// Control what's exported
// users/services/index.ts
export { UsersService } from './users.service'
// Don't export internal helpers
// export { InternalHelper } from './internal-helper' // ❌ Keep private
```

## Auto-Barrel Creation Rules

Automatically create `index.ts` when:

1. **2+ files in directory** (avoids unnecessary barrels)
2. **Files export classes/types** (entities, DTOs, services, etc.)
3. **Directory is part of module structure** (entities/, dto/, services/, etc.)

## Selective Exports

For specific exports instead of `export *`:

```typescript
// users/services/index.ts

// ✅ Export public API
export { UsersService } from './users.service'
export { AuthService } from './auth.service'

// ❌ Don't export internal utilities
// export { InternalHelper } from './internal.helper'
```

## Integration with TypeORM

```typescript
// users/entities/index.ts
export { User } from './user.entity'
export { Profile } from './profile.entity'

// users.module.ts - Clean!
import { User, Profile } from './entities'

@Module({
  imports: [TypeOrmModule.forFeature([User, Profile])],
  // ...
})
```

## Module Organization Best Practices

```typescript
// ✅ CORRECT - Organized with barrels
src/
├── users/
│   ├── users.module.ts
│   ├── entities/
│   │   ├── user.entity.ts
│   │   └── index.ts
│   ├── dto/
│   │   ├── create-user.dto.ts
│   │   ├── update-user.dto.ts
│   │   └── index.ts
│   ├── services/
│   │   ├── users.service.ts
│   │   └── index.ts
│   └── controllers/
│       ├── users.controller.ts
│       └── index.ts
```

## Auto-Update Scenarios

### Scenario 1: New Entity Added

```typescript
// User creates: payment-method.entity.ts

// Automatically update entities/index.ts:
export * from './user.entity'
export * from './profile.entity'
export * from './payment-method.entity'  // ✅ Auto-added
```

### Scenario 2: DTO Renamed

```typescript
// User renames: update-user.dto.ts → modify-user.dto.ts

// Automatically update dto/index.ts:
export * from './create-user.dto'
export * from './modify-user.dto'  // ✅ Auto-updated
```

### Scenario 3: File Deleted

```typescript
// User deletes: profile.entity.ts

// Automatically update entities/index.ts:
export * from './user.entity'
// export * from './profile.entity'  // ✅ Auto-removed
```

## Cross-Module Imports

```typescript
// orders/services/orders.service.ts
import { Injectable } from '@nestjs/common'

// ✅ Import from other module's barrel
import { User } from 'src/users/entities'
import { UsersService } from 'src/users/services'

@Injectable()
export class OrdersService {
  constructor(private usersService: UsersService) {}

  async createOrder(userId: string) {
    const user = await this.usersService.findOne(userId)
    // ...
  }
}
```

## Circular Dependency Prevention

When two services or modules re-export and inject each other, JavaScript runtime evaluation order may cause one dependency to resolve to `undefined` at runtime:

### Diagnostic Warning:
`Nest can't resolve dependencies of the XService (?, YService). Please make sure that the argument at index [0] is available in the current context.`

### Resolution:
1. **Never** import a service from another module's barrel export if that module imports back from your module's barrel.
2. If two services must reference each other, use NestJS `forwardRef()` in both module definitions and constructor injections:
```typescript
// users.service.ts
@Injectable()
export class UsersService {
  constructor(
    @Inject(forwardRef(() => OrdersService))
    private ordersService: OrdersService,
  ) {}
}

// users.module.ts
@Module({
  imports: [forwardRef(() => OrdersModule)],
  providers: [UsersService],
  exports: [UsersService],
})
export class UsersModule {}
```

## Success Criteria

✅ Every module directory has barrel exports
✅ All imports use barrel exports (not specific files)
✅ Barrels auto-update when files change
✅ Clean, maintainable import structure
✅ Easy refactoring (rename/move files)

## Behavior

**Proactive enforcement:**
- Create barrels without being asked
- Update barrels automatically when files change
- Convert direct imports to barrel imports
- Explain benefits of barrel exports
- Maintain consistent structure

**Never:**
- Require explicit "create barrel export" request
- Allow direct file imports when barrel exists
- Wait for imports to break

**Always:**
- Create `index.ts` in module directories
- Keep barrel exports up to date
- Use `export *` for simplicity (unless selective needed)
- Ensure imports use barrels

This ensures clean, maintainable NestJS module structure from day one.
