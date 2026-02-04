---
name: code-generator
version: 1.0.0
description: Generates production-ready code with proper error handling, type safety, SOLID principles, and comprehensive documentation
author: Selek Team
tags: [code, typescript, javascript, python, generator, solid]
activation_keywords:
  - write code
  - generate code
  - create function
  - create class
  - implement feature
  - build component
  - code for
  - write a function
  - write a class
requires_code_execution: false
---

# Code Generator Skill

## Overview
This skill helps you generate high-quality, production-ready code following industry best practices. It emphasizes type safety, error handling, documentation, and testability.

## When to Use
Activate this skill when the user:
- Asks to write, generate, or create code
- Mentions implementing a feature or component
- Requests code following specific patterns (SOLID, DRY, KISS, etc.)
- Needs code with tests and documentation
- Wants to refactor existing code

## Core Principles

### 1. Type Safety First
- Use TypeScript for JavaScript projects
- Include type annotations in Python (type hints)
- Leverage static typing features
- Never use `any` without justification

### 2. Error Handling
- **Custom exception classes**, not generic exceptions
- **Fail fast** with clear error messages
- Include context in error messages
- Log errors appropriately with contextual information

### 3. SOLID Principles
- **Single Responsibility**: Each class/function does one thing
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable
- **Interface Segregation**: Many specific interfaces over one general
- **Dependency Inversion**: Depend on abstractions, not concretions

### 4. Code Organization
- Clear function/class names that describe purpose
- Small, focused functions (< 30 lines ideally)
- Meaningful variable names (balance conciseness with clarity)
- Consistent code style

### 5. Documentation
- JSDoc/docstrings for all public APIs
- Explain *why*, not just *what*
- Include usage examples
- Document edge cases and assumptions

## Instructions

### Step 1: Understand Requirements
Before generating code, ensure you understand:
1. What problem are we solving?
2. What language/framework should be used?
3. Are there specific patterns or constraints?
4. What are the inputs and expected outputs?
5. What error cases need handling?

If anything is unclear, ask clarifying questions.

### Step 2: Design the Solution
1. Identify the main components needed
2. Define interfaces/types first
3. Plan error handling strategy
4. Consider edge cases

### Step 3: Implement

#### For Classes:
```typescript
/**
 * Brief description of what this class does
 * 
 * @example
 * ```typescript
 * const instance = new MyClass(config);
 * await instance.doSomething();
 * ```
 */
export class MyClass {
  private dependency: Dependency;
  
  constructor(dependency: Dependency) {
    if (!dependency) {
      throw new ValidationError('Dependency is required');
    }
    this.dependency = dependency;
  }
  
  /**
   * Description of what this method does
   * 
   * @param input - Description of input
   * @returns Description of return value
   * @throws {CustomError} When this error occurs
   */
  async doSomething(input: string): Promise<Result> {
    if (!input) {
      throw new ValidationError('Input cannot be empty');
    }
    
    try {
      const result = await this.dependency.process(input);
      return result;
    } catch (error) {
      throw new ProcessingError(
        'Failed to process input',
        error instanceof Error ? error : undefined
      );
    }
  }
}
```

#### For Functions:
```typescript
/**
 * Brief description
 * 
 * @param input - Description
 * @returns Description
 * @throws {CustomError} When this happens
 * 
 * @example
 * ```typescript
 * const result = await processData(input);
 * ```
 */
export async function processData(input: DataInput): Promise<DataOutput> {
  // Validate input
  if (!input.id) {
    throw new ValidationError('Input must have an id');
  }
  
  try {
    // Main logic
    const result = await doWork(input);
    return result;
  } catch (error) {
    // Log with context
    console.error('processData failed:', {
      error,
      input: input.id,
      timestamp: new Date().toISOString(),
    });
    
    throw new ProcessingError(
      `Failed to process data for id: ${input.id}`,
      error instanceof Error ? error : undefined
    );
  }
}
```

### Step 4: Add Error Classes
Always create custom error classes:

```typescript
export class CustomError extends Error {
  constructor(
    message: string,
    public readonly cause?: Error,
    public readonly context?: Record<string, any>
  ) {
    super(message);
    this.name = 'CustomError';
  }
}

export class ValidationError extends CustomError {
  constructor(message: string, cause?: Error) {
    super(message, cause);
    this.name = 'ValidationError';
  }
}
```

### Step 5: Include Tests
Generate corresponding tests:

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { MyClass, ValidationError } from './MyClass';

describe('MyClass', () => {
  let instance: MyClass;
  
  beforeEach(() => {
    instance = new MyClass(mockDependency);
  });
  
  it('should process valid input successfully', async () => {
    const result = await instance.doSomething('valid');
    expect(result).toBeDefined();
  });
  
  it('should throw ValidationError for empty input', async () => {
    await expect(instance.doSomething('')).rejects.toThrow(ValidationError);
  });
  
  it('should handle processing errors', async () => {
    mockDependency.process = vi.fn().mockRejectedValue(new Error('fail'));
    await expect(instance.doSomething('test')).rejects.toThrow(ProcessingError);
  });
});
```

### Step 6: Provide Usage Examples
Include a usage section showing:
- Basic usage
- Advanced usage
- Error handling
- Common patterns

## Language-Specific Guidelines

### TypeScript/JavaScript
- Use `const` by default, `let` when needed, never `var`
- Prefer async/await over promises chains
- Use optional chaining (`?.`) and nullish coalescing (`??`)
- Enable strict mode in tsconfig.json

### Python
- Follow PEP 8 style guide
- Use type hints (from typing import ...)
- Use dataclasses for data containers
- Context managers for resource management

### Go
- Follow Go idioms (accept interfaces, return structs)
- Error handling: return errors, don't panic
- Use defer for cleanup
- Keep packages focused

## Anti-Patterns to Avoid

❌ **Don't:**
- Use generic error messages: `throw new Error('Error')`
- Ignore errors: `catch (e) { }`
- Use magic numbers: `if (status === 200)`
- Write functions > 50 lines
- Mix concerns in a single function
- Skip input validation
- Forget to clean up resources

✅ **Do:**
- Use descriptive error messages: `throw new AuthenticationError('Invalid API key provided')`
- Handle or propagate errors properly
- Use constants: `if (status === HTTP_OK)`
- Break large functions into smaller ones
- Separate concerns (validation, logic, persistence)
- Validate all inputs at boundaries
- Use try/finally or context managers for cleanup

## Code Review Checklist

After generating code, self-review using this checklist:
- [ ] All functions have clear, descriptive names
- [ ] Input validation is present
- [ ] Errors are handled with custom exception classes
- [ ] Error messages include helpful context
- [ ] Code follows SOLID principles
- [ ] Documentation is complete (JSDoc/docstrings)
- [ ] Edge cases are handled
- [ ] No code duplication (DRY principle)
- [ ] Tests cover happy path and error cases
- [ ] Resource cleanup is handled
- [ ] Type safety is enforced
- [ ] No TODO comments without issue tracking

## Templates Reference

Common templates are available in the `templates/` directory:
- `class-template.ts` - Basic class structure
- `function-template.ts` - Standalone function
- `api-route-template.ts` - Express/REST API endpoint
- `react-component-template.tsx` - React component
- `test-template.ts` - Test file structure

## Examples

### Example 1: User Authentication Class

**User Request:** "Create a user authentication class with login and logout"

**Generated Code:**
```typescript
import { hash, compare } from 'bcrypt';

export class AuthenticationError extends Error {
  constructor(message: string, public readonly cause?: Error) {
    super(message);
    this.name = 'AuthenticationError';
  }
}

export class UserNotFoundError extends AuthenticationError {
  constructor(userId: string) {
    super(`User not found: ${userId}`);
    this.name = 'UserNotFoundError';
  }
}

export interface User {
  id: string;
  email: string;
  passwordHash: string;
}

export interface AuthResult {
  user: User;
  token: string;
}

/**
 * Handles user authentication operations including login, logout, and token management
 * 
 * @example
 * ```typescript
 * const auth = new UserAuthentication(userRepo, tokenService);
 * const result = await auth.login('user@example.com', 'password');
 * ```
 */
export class UserAuthentication {
  constructor(
    private userRepository: UserRepository,
    private tokenService: TokenService
  ) {
    if (!userRepository) {
      throw new Error('userRepository is required');
    }
    if (!tokenService) {
      throw new Error('tokenService is required');
    }
  }

  /**
   * Authenticate a user with email and password
   * 
   * @param email - User's email address
   * @param password - Plain text password
   * @returns Authentication result with user and token
   * @throws {UserNotFoundError} If user doesn't exist
   * @throws {AuthenticationError} If credentials are invalid
   */
  async login(email: string, password: string): Promise<AuthResult> {
    if (!email || !password) {
      throw new AuthenticationError('Email and password are required');
    }

    try {
      const user = await this.userRepository.findByEmail(email);
      
      if (!user) {
        throw new UserNotFoundError(email);
      }

      const isValid = await compare(password, user.passwordHash);
      
      if (!isValid) {
        throw new AuthenticationError('Invalid credentials');
      }

      const token = await this.tokenService.generate(user.id);

      return { user, token };
    } catch (error) {
      if (error instanceof AuthenticationError) {
        throw error;
      }

      console.error('Login failed:', {
        error,
        email,
        timestamp: new Date().toISOString(),
      });

      throw new AuthenticationError(
        'Login failed due to internal error',
        error instanceof Error ? error : undefined
      );
    }
  }

  /**
   * Logout a user by invalidating their token
   * 
   * @param token - Authentication token to invalidate
   * @throws {AuthenticationError} If logout fails
   */
  async logout(token: string): Promise<void> {
    if (!token) {
      throw new AuthenticationError('Token is required for logout');
    }

    try {
      await this.tokenService.revoke(token);
    } catch (error) {
      console.error('Logout failed:', {
        error,
        timestamp: new Date().toISOString(),
      });

      throw new AuthenticationError(
        'Logout failed',
        error instanceof Error ? error : undefined
      );
    }
  }
}
```

### Example 2: Data Processing Function

**User Request:** "Write a function to validate and transform API input data"

**Generated Code:**
```typescript
export class ValidationError extends Error {
  constructor(
    message: string,
    public readonly field?: string,
    public readonly cause?: Error
  ) {
    super(message);
    this.name = 'ValidationError';
  }
}

export interface ApiInput {
  userId: string;
  action: 'create' | 'update' | 'delete';
  data: Record<string, unknown>;
  timestamp?: number;
}

export interface TransformedData {
  userId: string;
  action: string;
  payload: Record<string, unknown>;
  processedAt: Date;
}

/**
 * Validates and transforms API input data with comprehensive error checking
 * 
 * @param input - Raw API input data
 * @returns Validated and transformed data
 * @throws {ValidationError} If input is invalid
 * 
 * @example
 * ```typescript
 * const result = validateAndTransform({
 *   userId: '123',
 *   action: 'create',
 *   data: { name: 'John' }
 * });
 * ```
 */
export function validateAndTransform(input: unknown): TransformedData {
  // Type guard
  if (!input || typeof input !== 'object') {
    throw new ValidationError('Input must be an object');
  }

  const data = input as Partial<ApiInput>;

  // Validate userId
  if (!data.userId || typeof data.userId !== 'string') {
    throw new ValidationError('userId is required and must be a string', 'userId');
  }

  if (data.userId.trim().length === 0) {
    throw new ValidationError('userId cannot be empty', 'userId');
  }

  // Validate action
  const validActions: Array<ApiInput['action']> = ['create', 'update', 'delete'];
  if (!data.action || !validActions.includes(data.action)) {
    throw new ValidationError(
      `action must be one of: ${validActions.join(', ')}`,
      'action'
    );
  }

  // Validate data
  if (!data.data || typeof data.data !== 'object') {
    throw new ValidationError('data is required and must be an object', 'data');
  }

  // Transform
  return {
    userId: data.userId.trim(),
    action: data.action,
    payload: data.data,
    processedAt: new Date(),
  };
}
```

## Quick Reference Card

| Scenario | Pattern |
|----------|---------|
| Input validation | Check at function entry, throw ValidationError |
| Error handling | Use try-catch, custom error classes, log with context |
| Async operations | Use async/await, handle rejections |
| Resource cleanup | Use try-finally or context managers |
| Dependencies | Inject via constructor (DI pattern) |
| Configuration | Validate in constructor, fail fast |
| Logging | Include error, context, timestamp |
| Testing | Happy path + error cases + edge cases |

## Final Notes

- **Quality over speed**: Take time to write proper error handling
- **Think about the user**: They will read your error messages
- **Consider maintenance**: Someone will need to debug this code later
- **Be consistent**: Follow the patterns shown here throughout the codebase

Remember: Code is read many more times than it's written. Make it clear, make it safe, make it maintainable.