---
name: production-code-standards
description: Production-ready code standards following CLAUDE Framework with TDD, security, and quality requirements
triggers: [production, code quality, standards, TDD, best practices, code review, maintainable, SOLID]
version: 1.0.0
agents: [senior-fullstack-developer, code-refactoring-specialist, qa-testing-engineer]
context_levels:
  minimal: Core standards and quick reference
  detailed: Complete patterns and examples
  full: Scripts, templates, and automation tools
---

# Production Code Standards Skill

## Overview
This skill encapsulates the CLAUDE Framework standards for production-ready code development. It ensures consistency, quality, security, and maintainability across all code deliverables.

## When to Use This Skill
- Creating new features requiring production quality
- Code reviews against production standards
- Refactoring legacy code to modern standards
- Training on development best practices
- Pre-deployment quality validation

## Core Principles (Level 1 - Always Loaded)

### 🎯 Priority Rules (CRITICAL - Non-Negotiable)

**Basis Missie - Breaking these = delivery rejected:**
- **BM-1 (MUST)**: Never invent, omit, or skip functionality
- **BM-2 (MUST)**: Follow exact instructions from user
- **BM-3 (MUST)**: Ask questions when unclear, never assume

**Impact Analysis - Before ANY code change:**
- **IA-1 (MUST)**: Analyze impact on existing functionality
- **IA-2 (MUST)**: Check all dependencies that will be affected
- **IA-3 (MUST)**: Search for all files that import/use the code
- **IA-4 (MUST)**: Run existing tests BEFORE changes
- **IA-5 (MUST)**: Backup/document original implementation when overwriting
- **IA-6 (MUST NOT)**: Never overwrite code without impact check
- **IA-7 (MUST)**: Ask permission before overwriting with impact explanation

### 🔴 Code Quality Standards

**Single Responsibility & DRY:**
```typescript
// ✅ GOOD - Single responsibility
class UserAuthenticator {
  authenticate(credentials: Credentials): AuthResult {
    return this.validateAndAuthenticate(credentials);
  }
}

class UserNotifier {
  sendWelcomeEmail(user: User): void {
    this.emailService.send(user.email, 'Welcome!');
  }
}

// ❌ BAD - Multiple responsibilities
class UserManager {
  authenticate() { /* auth logic */ }
  sendEmail() { /* email logic */ }
  updateDatabase() { /* db logic */ }
}
```

**Naming Conventions (MUST):**
- Functions: `getUserData()`, `calculateTotal()` (verbs)
- Variables: `user`, `totalAmount` (nouns)
- Booleans: `isValid`, `hasPermission` (is/has prefix)
- Constants: `MAX_RETRY_COUNT`, `API_BASE_URL`
- Classes: `UserService`, `OrderController` (PascalCase)

**Function Size Limit:**
- Maximum 20 lines per function
- Extract complex logic into helper functions
- One level of abstraction per function

### 🔒 Error Handling (CRITICAL)

```typescript
// ✅ GOOD - Comprehensive error handling
async function fetchUserData(userId: string): Promise<User> {
  try {
    if (!userId || userId.trim() === '') {
      throw new ValidationError('User ID is required');
    }

    const user = await db.users.findById(userId);

    if (!user) {
      throw new NotFoundError(`User ${userId} not found`);
    }

    logger.info('User fetched successfully', { userId });
    return user;

  } catch (error) {
    if (error instanceof ValidationError || error instanceof NotFoundError) {
      throw error;
    }

    logger.error('Failed to fetch user', { userId, error: error.message });
    throw new DatabaseError('Failed to fetch user data');
  }
}

// ❌ BAD - Silent failure
async function fetchUserData(userId: string) {
  try {
    return await db.users.findById(userId);
  } catch (error) {
    return null; // Silent failure - NEVER do this!
  }
}
```

**Error Handling Rules (MUST):**
- Handle all error scenarios explicitly
- Use specific error types/messages
- Log errors with context
- Never silent failures
- Fail fast: validate inputs early

### 🧪 TDD Requirements (MUST)

**Red-Green-Refactor Cycle:**
1. **Red**: Write failing test first
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code quality

**Test Coverage Requirements:**
- Minimum 80% coverage for new code
- Test happy path, errors, edge cases
- Arrange-Act-Assert pattern
- Descriptive test names

```typescript
// ✅ GOOD - Descriptive test with AAA pattern
describe('UserAuthenticator', () => {
  it('should return success when valid credentials provided', () => {
    // Arrange
    const authenticator = new UserAuthenticator();
    const validCredentials = { email: 'test@example.com', password: 'Valid123!' };

    // Act
    const result = authenticator.authenticate(validCredentials);

    // Assert
    expect(result.success).toBe(true);
    expect(result.user).toBeDefined();
  });

  it('should throw ValidationError when email is missing', () => {
    // Arrange
    const authenticator = new UserAuthenticator();
    const invalidCredentials = { email: '', password: 'Valid123!' };

    // Act & Assert
    expect(() => authenticator.authenticate(invalidCredentials))
      .toThrow(ValidationError);
  });
});
```

### 🔐 Security Rules (CRITICAL)

**Input Validation (MUST):**
```typescript
// ✅ GOOD - Validate at boundaries
function createUser(input: unknown): User {
  const validated = userSchema.parse(input); // Zod/Joi validation

  // Sanitize
  const sanitized = {
    email: validator.normalizeEmail(validated.email),
    name: validator.escape(validated.name),
  };

  return userService.create(sanitized);
}

// ❌ BAD - No validation
function createUser(input: any) {
  return userService.create(input); // Unsafe!
}
```

**Security Requirements (MUST):**
- Input validation at system boundaries
- Output sanitization
- Secrets via env vars/vault (never hardcoded)
- Never log sensitive data (passwords, tokens, PII)
- TLS everywhere, HSTS, secure cookies
- Dependency scanning enabled

## Detailed Patterns (Level 2 - Load on Request)

See companion files:
- `detailed-patterns.md` - Advanced patterns and examples
- `refactoring-guide.md` - Step-by-step refactoring strategies
- `security-checklist.md` - Comprehensive security validation

## Automation Tools (Level 3 - Load When Needed)

See scripts directory:
- `scripts/pre-commit-check.sh` - Run before commits
- `scripts/quality-gate.sh` - CI/CD quality validation
- `scripts/security-scan.sh` - Dependency and secret scanning

## Quick Reference Checklist

Before marking any task complete:
- [ ] All MUST rules followed
- [ ] Impact analysis completed
- [ ] Tests written first (TDD)
- [ ] 80%+ test coverage
- [ ] All error scenarios handled
- [ ] Security validation passed
- [ ] No hardcoded secrets
- [ ] Functions under 20 lines
- [ ] Descriptive naming used
- [ ] Code reviewed

## Integration with Agents

**senior-fullstack-developer:**
- Primary agent for implementing these standards
- Uses this skill for all production code
- References detailed patterns for complex scenarios

**code-refactoring-specialist:**
- Uses this skill when modernizing legacy code
- Applies standards during refactoring
- Validates against quality checklist

**qa-testing-engineer:**
- Uses this skill to validate test coverage
- Ensures TDD compliance
- Reviews test quality against standards

## Success Metrics

Track these KPIs:
- First-time success rate > 70%
- Average iterations < 3
- Test coverage > 80%
- Security issues: 0
- Production bugs < 2/week

---

*Version 1.0.0 | Compatible with CLAUDE Framework v5.0*
