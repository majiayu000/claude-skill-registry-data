---
name: enforce-file-limits
description: Enforce 500-line file size limits. Warn at 400 lines. Guide splitting large files into focused modules. Apply when writing or editing code.
---

# File Size Limits Enforcement

**CRITICAL: All files MUST stay under 500 lines. This is NON-NEGOTIABLE.**

## Why This Exists

Large files are:
- Hard to navigate
- Hard to test
- Hard to maintain
- Easy to violate Single Responsibility Principle

## When to Apply

Use this skill when:
- Creating new files
- Editing existing files
- Reviewing code
- Splitting large files

## How It Works

### Line Limits

- **Hard limit**: 500 lines (WILL BE REJECTED)
- **Warning threshold**: 400 lines (PLAN TO SPLIT)
- **Optimal range**: 200-300 lines

### What Counts as Lines

Count EVERYTHING:
- Code lines
- Comment lines (including block comments)
- Blank lines
- Import statements
- Type definitions

**The only exception**: File header comments (first 1-5 lines describing the file).

### Checking Current File Size

Before editing, check line count:

```bash
wc -l path/to/file.ts
```

If output shows > 400 lines, plan to split BEFORE adding more code.

### Splitting Strategies

#### 1. Extract Utilities

```typescript
// ❌ BEFORE: UserService.ts (550 lines)
class UserService {
  validateEmail() { /* 50 lines */ }
  hashPassword() { /* 50 lines */ }
  generateToken() { /* 50 lines */ }
  createUser() { /* 400 lines */ }
}

// ✅ AFTER: Split utilities
// utils/userValidation.ts (50 lines)
export function validateEmail() {}

// utils/passwordUtils.ts (50 lines)
export function hashPassword() {}

// utils/tokenGenerator.ts (50 lines)
export function generateToken() {}

// UserService.ts (400 lines)
class UserService {
  createUser() { /* uses imported utilities */ }
}
```

#### 2. Extract Sub-Services

```typescript
// ❌ BEFORE: UserService.ts (600 lines)
class UserService {
  // User CRUD (200 lines)
  // Password management (200 lines)
  // Profile management (200 lines)
}

// ✅ AFTER: Split by domain
// UserService.ts (200 lines)
// UserPasswordService.ts (200 lines)
// UserProfileService.ts (200 lines)
```

#### 3. Extract Component Logic

```typescript
// ❌ BEFORE: Dashboard.tsx (550 lines)
export function Dashboard() {
  // State management (100 lines)
  // Data fetching logic (100 lines)
  // Event handlers (100 lines)
  // Render multiple sections (250 lines)
}

// ✅ AFTER: Split into focused components
// Dashboard.tsx (200 lines) - main component
// hooks/useDashboardData.ts (100 lines) - data fetching
// components/DashboardStats.tsx (150 lines)
// components/DashboardCharts.tsx (150 lines)
```

### When File Approaching 400 Lines

**STOP and plan extraction BEFORE adding more code:**

1. Identify logical boundaries (utilities, sub-domains, components)
2. Create new files with descriptive names
3. Move code to new files
4. Update imports
5. Verify tests still pass

### Handling Large Files in Codebase

If you encounter a file > 500 lines:

1. **Flag it immediately**: "⚠️ This file exceeds 500 lines and needs refactoring"
2. **If editing**: Plan split BEFORE making changes
3. **If creating new feature**: Don't add to large files - create new focused files instead

## Examples

### Good: Properly Sized Files

```
src/features/auth/
├── services/
│   ├── AuthService.ts (280 lines) ✅
│   ├── TokenService.ts (180 lines) ✅
│   └── PasswordResetService.ts (220 lines) ✅
```

### Bad: Oversized Files

```
src/features/auth/
└── services/
    └── AuthService.ts (850 lines) ❌ MUST SPLIT!
```

### Refactoring Large Files

```typescript
// BEFORE: AuthService.ts (850 lines) ❌
class AuthService {
  // Login logic (200 lines)
  // Registration logic (200 lines)
  // Password reset logic (200 lines)
  // Token management (150 lines)
  // Email verification (100 lines)
}

// AFTER: Split into focused services ✅
// AuthService.ts (200 lines)
class AuthService {
  login() {}
  logout() {}
}

// RegistrationService.ts (200 lines)
class RegistrationService {
  register() {}
  verifyEmail() {}
}

// PasswordService.ts (200 lines)
class PasswordService {
  resetPassword() {}
  changePassword() {}
}

// TokenService.ts (150 lines)
class TokenService {
  generateToken() {}
  validateToken() {}
  refreshToken() {}
}
```

## Enforcement

The code-quality-auditor will:
- ✅ Check file line counts
- ✅ Reject files > 500 lines
- ✅ Warn on files > 400 lines
- ✅ Suggest split strategies

## Quick Checklist

- [ ] File is under 500 lines (hard limit)
- [ ] File is under 400 lines (warning threshold)
- [ ] If approaching 400, plan extraction
- [ ] Large files have been split before editing
- [ ] New code added to focused files, not large files
