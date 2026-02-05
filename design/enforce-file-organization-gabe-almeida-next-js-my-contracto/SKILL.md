---
name: enforce-file-organization
description: Guide feature-based directory structure and file placement. Apply when creating new files or organizing code. Enforce naming conventions and import ordering for backend and frontend files.
---

# File Organization Standards

**CRITICAL: Maintain consistent, predictable file organization across the codebase.**

## Why This Exists

Poor organization:
- Makes code hard to find
- Slows down development
- Causes merge conflicts
- Creates confusion

**Good organization makes code discoverable and maintainable.**

## When to Apply

Apply when:
- Creating new files
- Moving/renaming files
- Setting up new features
- Refactoring structure

## How It Works

### Directory Structure

#### Feature-Based Organization (Backend)

```
src/features/
├── auth/
│   ├── controllers/      # HTTP request handlers (max 300 lines)
│   ├── services/         # Business logic (max 300 lines)
│   ├── repositories/     # Data access (max 300 lines)
│   ├── models/           # Domain models (max 200 lines)
│   ├── validators/       # Input validation (max 150 lines)
│   ├── types/            # TypeScript types (max 100 lines)
│   ├── utils/            # Feature utilities (max 200 lines)
│   ├── tests/            # Feature tests
│   └── index.ts          # Public API exports
│
├── users/                # Another feature
│   └── ...
│
└── posts/                # Another feature
    └── ...
```

#### Shared Code

```
src/shared/               # Used by 2+ features
├── services/
│   ├── EmailService.ts           (max 300 lines)
│   ├── StorageService.ts         (max 250 lines)
│   └── CacheService.ts           (max 250 lines)
├── utils/
│   ├── dateUtils.ts              (max 200 lines)
│   └── validationUtils.ts        (max 200 lines)
├── types/
│   └── common.ts                 (max 150 lines)
├── constants/
│   ├── errorCodes.ts             (max 100 lines)
│   └── httpStatus.ts             (max 100 lines)
└── middleware/
    ├── authMiddleware.ts         (max 200 lines)
    └── errorHandler.ts           (max 250 lines)
```

#### Core Infrastructure

```
src/core/                 # Core infrastructure (rarely changes)
├── database/
│   ├── connection.ts             (max 200 lines)
│   ├── migrations/
│   └── seeders/
├── config/
│   ├── app.ts                    (max 150 lines)
│   └── database.ts               (max 100 lines)
├── errors/
│   ├── AppError.ts               (max 150 lines)
│   └── ValidationError.ts        (max 100 lines)
└── interfaces/           # Core abstractions
    ├── IRepository.ts            (max 100 lines)
    └── IService.ts               (max 100 lines)
```

#### Frontend Organization (React)

```
src/features/
├── auth/
│   ├── components/       # Feature-specific components
│   │   ├── LoginForm.tsx         (max 250 lines)
│   │   └── RegisterForm.tsx      (max 250 lines)
│   ├── hooks/            # Feature hooks
│   │   └── useAuth.ts            (max 150 lines)
│   ├── services/         # API calls
│   │   └── authApi.ts            (max 200 lines)
│   ├── store/            # State management
│   │   └── authSlice.ts          (max 250 lines)
│   └── types/
│       └── auth.types.ts         (max 100 lines)
│
└── posts/
    └── ...
```

#### Shared UI Components

```
src/components/           # Shared UI components
├── ui/                   # Base UI (buttons, inputs)
│   ├── Button.tsx                (max 150 lines)
│   ├── Input.tsx                 (max 150 lines)
│   └── Modal.tsx                 (max 200 lines)
├── forms/                # Form components
│   ├── FormField.tsx             (max 150 lines)
│   └── FormError.tsx             (max 100 lines)
└── layouts/              # Layout components
    ├── AppLayout.tsx             (max 250 lines)
    └── Header.tsx                (max 200 lines)
```

### File Naming Conventions

#### Backend (Node.js/TypeScript)

```
Controllers:     UserController.ts, AuthController.ts
Services:        UserService.ts, EmailService.ts
Repositories:    UserRepository.ts, PostRepository.ts
Models:          User.ts, Post.ts, Comment.ts
Validators:      UserValidator.ts, PostValidator.ts
Utils:           dateUtils.ts, stringUtils.ts (camelCase)
Types:           user.types.ts, api.types.ts (lowercase + .types)
Constants:       httpStatus.ts, errorCodes.ts (camelCase)
Tests:           UserService.test.ts, AuthController.test.ts
```

#### Frontend (React/TypeScript)

```
Components:      Button.tsx, LoginForm.tsx (PascalCase)
Hooks:           useAuth.ts, useDebounce.ts (camelCase with 'use')
Utils:           format.ts, validation.ts (camelCase)
Types:           auth.types.ts, user.types.ts (lowercase + .types)
Styles:          Button.module.css, LoginForm.module.css
Tests:           Button.test.tsx, LoginForm.test.tsx
```

### Import Organization

**Order imports in this sequence:**

```typescript
// 1. External dependencies (third-party packages)
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import axios from 'axios';

// 2. Internal absolute imports (from src/)
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/features/auth/hooks/useAuth';

// 3. Relative imports from same feature
import { LoginForm } from './components/LoginForm';
import { validateEmail } from './utils/validation';

// 4. Types
import type { User } from '@/types/user.types';
import type { LoginFormData } from './types/auth.types';

// 5. Styles
import styles from './Login.module.css';
```

### File Structure Within Files

#### Service/Class Files

```typescript
/**
 * FILE: UserService.ts
 * PURPOSE: Handles user business logic
 */

// ========================================
// IMPORTS
// ========================================
import { injectable } from 'inversify';
import { UserRepository } from '../repositories/UserRepository';
import type { User, CreateUserDTO } from '../types/user.types';

// ========================================
// CONSTANTS
// ========================================
const MAX_USERNAME_LENGTH = 50;
const MIN_PASSWORD_LENGTH = 8;

// ========================================
// TYPES
// ========================================
interface UserServiceOptions {
  sendWelcomeEmail?: boolean;
}

// ========================================
// CLASS IMPLEMENTATION
// ========================================
@injectable()
export class UserService {
  // ----------------------------------
  // Properties
  // ----------------------------------
  private userRepository: UserRepository;

  // ----------------------------------
  // Constructor
  // ----------------------------------
  constructor(userRepository: UserRepository) {
    this.userRepository = userRepository;
  }

  // ----------------------------------
  // Public Methods
  // ----------------------------------

  /**
   * WHY: Creates new user accounts
   * WHEN: Called during registration
   * HOW: Validates, hashes password, saves to DB
   */
  async createUser(data: CreateUserDTO): Promise<User> {
    // Implementation
  }

  // ----------------------------------
  // Private Methods
  // ----------------------------------

  private validateUserData(data: CreateUserDTO): void {
    // Implementation
  }
}

// ========================================
// HELPER FUNCTIONS (if needed)
// ========================================

function formatUsername(username: string): string {
  return username.trim().toLowerCase();
}
```

#### React Component Files

```tsx
/**
 * FILE: LoginForm.tsx
 * PURPOSE: User authentication form
 */

// ========================================
// IMPORTS
// ========================================
import React, { useState } from 'react';
import { Button } from '@/components/ui/Button';
import type { LoginFormData } from '../types/auth.types';
import styles from './LoginForm.module.css';

// ========================================
// TYPES
// ========================================
interface LoginFormProps {
  onSuccess?: () => void;
  redirectUrl?: string;
}

// ========================================
// COMPONENT
// ========================================

/**
 * WHY: Provides reusable login form
 * WHEN: Use on login pages or modals
 * HOW: Manages form state, validates, calls auth service
 */
export function LoginForm({ onSuccess, redirectUrl }: LoginFormProps) {
  // ----------------------------------
  // State
  // ----------------------------------
  const [formData, setFormData] = useState<LoginFormData>({
    email: '',
    password: ''
  });

  // ----------------------------------
  // Handlers
  // ----------------------------------

  const handleSubmit = async (e: React.FormEvent) => {
    // Implementation
  };

  // ----------------------------------
  // Render
  // ----------------------------------
  return (
    <form onSubmit={handleSubmit} className={styles.form}>
      {/* JSX */}
    </form>
  );
}

// ========================================
// HELPER FUNCTIONS
// ========================================

function validateLoginForm(data: LoginFormData): Record<string, string> {
  const errors: Record<string, string> = {};
  // Implementation
  return errors;
}
```

## When to Split Files

Split when:
1. **File exceeds 400 lines** - Plan extraction before 500 limit
2. **Multiple responsibilities** - Each file should have ONE purpose
3. **Reusable logic found** - Extract utilities, hooks, services
4. **Hard to test** - If mocking too much, split it
5. **Hard to navigate** - If scrolling a lot, split it

## Enforcement

Code quality auditor checks:
- ✅ Files in correct directories
- ✅ Naming conventions followed
- ✅ Import order correct
- ✅ File structure follows template
- ✅ No files exceed line limits
- ✅ Related files co-located

## Quick Checklist

- [ ] File in correct feature/shared/core directory
- [ ] File name follows naming convention
- [ ] Imports organized in correct order
- [ ] File has proper header documentation
- [ ] Sections clearly marked with comments
- [ ] File doesn't exceed line limit
