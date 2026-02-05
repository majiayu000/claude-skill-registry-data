---
name: enforce-modularity
description: Apply Single Responsibility Principle when writing code. Keep modules focused, cohesive, and loosely coupled. Guide splitting classes with too many methods. Ensure code is reusable and testable.
---

# Modularity Standards

**CRITICAL: Write modular, focused, maintainable code. Each module should do ONE thing well.**

## Why This Exists

Monolithic code:
- Hard to understand
- Hard to test
- Hard to maintain
- Hard to reuse
- Easy to break

**Modular code is easier to understand, test, maintain, reuse, and evolve.**

## When to Apply

Apply modularity when:
- Creating new files/classes/functions
- Refactoring existing code
- Reviewing code quality
- Planning architecture

## How It Works

### 1. Single Responsibility Principle (SRP)

**Each file, class, and function should do ONE thing well.**

#### File Level
- Each file represents ONE concept/responsibility
- File name clearly indicates single purpose
- If you can't name it without "and" or "or", split it

#### Class Level
- Each class has ONE reason to change
- Maximum 7-10 public methods per class
- Private methods don't count toward limit

#### Function Level
- Each function does ONE task
- Maximum 20-30 lines per function
- Maximum 3-4 parameters per function
- If needs many params, group into object

### 2. High Cohesion

**Functions in a module work on related data.**

Good cohesion:
- ✅ All code in file serves module's single purpose
- ✅ Functions work on same data structures
- ✅ Changes to one part don't cascade

Bad cohesion:
- ❌ Unrelated functions grouped together
- ❌ File does multiple unrelated things
- ❌ Changes require editing multiple sections

### 3. Low Coupling

**Modules depend on interfaces, not implementations.**

Good coupling:
- ✅ Depend on abstractions (interfaces)
- ✅ Easy to swap implementations
- ✅ Changes don't cascade to other modules

Bad coupling:
- ❌ Direct dependencies on concrete classes
- ❌ Hard to test in isolation
- ❌ Changes break other modules

## Examples

### Good: Single Responsibility Per Service

```typescript
// ✅ UserService.ts - User management only
class UserService {
  createUser() {}
  updateUser() {}
  deleteUser() {}
  findUserById() {}
}

// ✅ EmailService.ts - Email only
class EmailService {
  sendWelcomeEmail() {}
  sendPasswordResetEmail() {}
  sendNotification() {}
}

// ✅ TokenService.ts - Tokens only
class TokenService {
  generateToken() {}
  verifyToken() {}
  refreshToken() {}
}
```

### Bad: Multiple Responsibilities

```typescript
// ❌ UserService.ts - Too many responsibilities!
class UserService {
  // User management
  createUser() {}
  updateUser() {}

  // Email (should be EmailService)
  sendEmail() {}

  // Logging (should be Logger)
  logActivity() {}

  // Validation (should be Validator)
  validatePassword() {}

  // Auth (should be TokenService)
  generateToken() {}
}
```

### Good: High Cohesion, Low Coupling

```typescript
// ✅ Interface for abstraction
interface IEmailProvider {
  send(to: string, subject: string, body: string): Promise<void>;
}

// ✅ Service depends on interface, not concrete implementation
class EmailService {
  constructor(private provider: IEmailProvider) {}

  async sendWelcomeEmail(user: User) {
    await this.provider.send(
      user.email,
      'Welcome!',
      this.buildWelcomeBody(user)
    );
  }

  // All email logic together (high cohesion)
  private buildWelcomeBody(user: User): string {
    return `Welcome ${user.name}!`;
  }
}

// ✅ Provider can be swapped without changing EmailService (low coupling)
class SendGridProvider implements IEmailProvider {
  async send(to: string, subject: string, body: string) {
    // SendGrid implementation
  }
}

class MailgunProvider implements IEmailProvider {
  async send(to: string, subject: string, body: string) {
    // Mailgun implementation
  }
}
```

### Good: Testable in Isolation

```typescript
// ✅ Pure, testable function
class PasswordValidator {
  validateStrength(password: string): boolean {
    return (
      password.length >= 8 &&
      /[A-Z]/.test(password) &&
      /[0-9]/.test(password)
    );
  }
}

// Test is simple
test('validates strong password', () => {
  const validator = new PasswordValidator();
  expect(validator.validateStrength('Password123')).toBe(true);
});
```

### Bad: Hard to Test

```typescript
// ❌ Tightly coupled to framework, database, everything
class UserController {
  createUser(req: Request, res: Response) {
    // Validation mixed in
    if (!req.body.email) {
      return res.status(400).json({ error: 'Email required' });
    }

    // Database access mixed in
    const user = await db.users.create(req.body);

    // Email sending mixed in
    await sendgrid.send({
      to: user.email,
      subject: 'Welcome'
    });

    // Response handling mixed in
    res.json(user);
  }
}

// Test requires mocking: HTTP framework, database, sendgrid, etc.
```

## Module Organization

### Feature-Based Structure

```
src/features/auth/
├── controllers/      # HTTP handlers (max 300 lines)
├── services/         # Business logic (max 300 lines)
├── repositories/     # Data access (max 300 lines)
├── models/           # Domain models (max 200 lines)
├── validators/       # Validation (max 150 lines)
├── types/            # TypeScript types (max 100 lines)
└── utils/            # Feature utilities (max 200 lines)
```

### Shared vs Core

```
shared/           # Used by 2+ features
├── services/
├── utils/
├── types/
└── constants/

core/             # Infrastructure (rarely changes)
├── database/
├── config/
├── errors/
└── interfaces/
```

## Code Reusability

**Before writing ANY code:**

1. **Search for existing functionality**
   - Check `shared/utils/`
   - Look in related features
   - Search for similar patterns

2. **Extract common logic**
   - Duplicated in 2+ places? Extract it
   - Function > 20 lines and reusable? Extract it
   - Pattern could benefit others? Extract it

3. **Choose location based on usage:**
   ```
   Used by ONE feature:     feature/utils/
   Used by 2+ features:     shared/utils/
   Used by ALL features:    core/utils/
   ```

### Example: Extracting Common Logic

```typescript
// ❌ BEFORE: Duplicated in multiple files
// UserController.ts
async createUser(req, res) {
  if (!req.body.email || !req.body.email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  // ...
}

// PostController.ts
async createPost(req, res) {
  if (!req.body.email || !req.body.email.includes('@')) {
    return res.status(400).json({ error: 'Invalid email' });
  }
  // ...
}

// ✅ AFTER: Extracted to shared utility
// shared/utils/validation.ts
export function validateEmail(email: string): boolean {
  return email && email.includes('@') && email.length > 3;
}

// Now used everywhere
import { validateEmail } from '@/shared/utils/validation';

if (!validateEmail(req.body.email)) {
  return res.status(400).json({ error: 'Invalid email' });
}
```

## Splitting Large Modules

### When to Split

Split when:
- File approaching 400 lines
- Class has > 10 public methods
- Function > 30 lines
- Multiple responsibilities detected
- Hard to test in isolation

### How to Split

#### Strategy 1: Extract Utilities

```typescript
// ❌ BEFORE: UserService.ts (550 lines)
class UserService {
  validateEmail() { /* 50 lines */ }
  hashPassword() { /* 50 lines */ }
  generateToken() { /* 50 lines */ }
  createUser() { /* 400 lines */ }
}

// ✅ AFTER: Split utilities
// utils/emailValidation.ts
export function validateEmail() {}

// utils/passwordUtils.ts
export function hashPassword() {}

// utils/tokenGenerator.ts
export function generateToken() {}

// UserService.ts (400 lines)
import { validateEmail } from '../utils/emailValidation';
import { hashPassword } from '../utils/passwordUtils';

class UserService {
  createUser() { /* uses imported utilities */ }
}
```

#### Strategy 2: Extract Sub-Services

```typescript
// ❌ BEFORE: UserService.ts (600 lines)
class UserService {
  // User CRUD (200 lines)
  // Password management (200 lines)
  // Profile management (200 lines)
}

// ✅ AFTER: Split by domain
// UserService.ts (200 lines)
class UserService {
  createUser() {}
  updateUser() {}
  deleteUser() {}
}

// UserPasswordService.ts (200 lines)
class UserPasswordService {
  changePassword() {}
  resetPassword() {}
}

// UserProfileService.ts (200 lines)
class UserProfileService {
  updateProfile() {}
  uploadAvatar() {}
}
```

## Enforcement

The code-quality-auditor will reject:
- ❌ Files > 500 lines
- ❌ Classes with > 10 public methods
- ❌ Functions > 30 lines
- ❌ Functions with > 4 parameters
- ❌ Multiple responsibilities in one file
- ❌ Duplicated code (DRY violations)
- ❌ Tight coupling to implementations

## Quick Checklist

- [ ] Each file has single responsibility
- [ ] File name clearly describes purpose
- [ ] Classes have < 10 public methods
- [ ] Functions are < 30 lines
- [ ] Functions have < 4 parameters
- [ ] No code duplication
- [ ] Modules are loosely coupled (interfaces)
- [ ] Code is testable in isolation
- [ ] Reusable logic extracted to utilities
