---
name: Code Refactoring Patterns
description: This skill should be used when the user asks to "refactor large files", "split code into smaller pieces", "extract methods", "how should I refactor", "improve code structure", "break down large functions", or discusses strategies for dividing monolithic code into smaller, maintainable components.
version: 0.1.0
---

# Code Refactoring Patterns

## Purpose

This skill provides guidance on refactoring large, complex code files into smaller, focused, and maintainable components. It covers fundamental refactoring principles, extraction strategies, and patterns that apply across programming languages and frameworks.

## When to Use

Use this skill when analyzing code structure, planning refactoring strategies, or deciding how to split large files. It provides language-agnostic principles that work whether refactoring Laravel controllers, React components, Node.js services, or any codebase.

## Core Refactoring Principles

### 1. Single Responsibility Principle (SRP)

Each function, class, or module should have one reason to change. Identify when code violates SRP:

- **Controllers handling validation, business logic, and response formatting** → Extract validation and business logic to separate classes
- **Components managing state, data fetching, and rendering** → Extract hooks and services
- **Service classes with 15+ public methods** → Break into focused services
- **Functions doing multiple operations** → Extract each operation to its own function

**Question to ask:** "If this code needs to change, how many different reasons could require that change?" More than one reason signals SRP violation.

### 2. Extractable Boundaries

Identify clear extraction boundaries by looking for:

- **Distinct workflows**: Methods performing completely different operations (e.g., user creation separate from email sending)
- **Reusable logic**: Code that appears in multiple places or could be used elsewhere
- **High complexity**: Methods exceeding 15-20 lines or with nested conditionals
- **Clear input/output**: Methods with well-defined inputs and outputs (easier to extract)
- **Testability**: Logic that would benefit from independent testing

**Extraction pattern:**
```
1. Identify the boundary (start/end of related operations)
2. Extract to new method/function
3. Verify no side effects or tight coupling
4. Test independently
5. Update references
```

### 3. Complexity Metrics

Recognize complexity that signals refactoring need:

- **Cyclomatic Complexity > 10**: Multiple branches, nested conditions → Extract conditional logic to separate methods
- **Method length > 20 lines**: Likely handling multiple concerns → Break into smaller methods
- **Nesting depth > 3 levels**: Hard to follow logic → Extract inner logic to separate methods
- **Parameter count > 4**: Hard to understand and test → Group parameters into objects
- **Method with many local variables**: Suggests multiple concerns → Extract to separate methods

### 4. Naming and Intent

After extraction, ensure clear naming:

- **Method names should describe intent**: `validateUserEmail()` not `check()`, `processPayment()` not `do()`
- **Extract Guard Clauses**: Early returns for edge cases make the happy path clear
- **Extract Error Handling**: Separate validation from business logic
- **Extract Loops**: Extract loop bodies to named methods that describe the operation

**Example**:
```php
// Before: Hard to understand at a glance
public function createUser($data) {
    if (!$data['email']) return false;
    if (User::where('email', $data['email'])->exists()) return false;
    // ... 30 more lines
}

// After: Clear intent with extracted boundaries
public function createUser($data) {
    if (!$this->validateUserData($data)) return false;
    if ($this->userExists($data['email'])) return false;
    return $this->storeUser($data);
}
```

## Extraction Patterns by Language

### PHP / Laravel

**Extract CRUD operations into Action classes:**
- `CreateUserAction` - Only handles creation logic
- `UpdateUserAction` - Only handles updates
- `DeleteUserAction` - Only handles deletion
- `GetUserAction` - Only handles retrieval with related data

**Extract validation into separate methods or Form Requests:**
- `ValidateUserInput` method or Form Request class
- Keep business logic separate from validation

**Extract queries into scopes and methods:**
- `scopeActive()` → `User::query()->active()`
- `scopeByEmail()` → `User::query()->byEmail($email)`

**Extract relationships into dedicated classes:**
- Models with complex relationships → Separate trait files
- Resource formatting → Dedicated Resource class

### React / Vue

**Extract large components into smaller pieces:**
- Container components (data management) separate from presentational components (rendering)
- Extract hooks for reusable logic
- Extract smaller, focused sub-components

**Extract hooks for reusable logic:**
- `useUserPermissions()` → Encapsulates permission checking
- `useFormValidation()` → Handles form state and validation
- `useDataFetching()` → Wraps React Query or SWR

**Extract context providers:**
- Theme context separate from Auth context
- Each context for one concern

### Node.js / TypeScript

**Extract service methods into focused services:**
- `UserService` → User-specific operations
- `EmailService` → Email operations
- `PaymentService` → Payment operations

**Extract helper/utility functions:**
- `validateEmail()`, `hashPassword()`, `formatResponse()`
- Keep pure functions in separate files

**Extract data access patterns:**
- Database queries → Repository pattern or separate data access file
- API calls → Separate API client file

## Refactoring Workflow

### Step 1: Analyze Current Code

Read the file and identify:
- Current responsibilities (what does this code do?)
- Violation areas (where are multiple concerns mixed?)
- Extraction candidates (which parts could be separate?)
- Dependencies (what does extracted code depend on?)

### Step 2: Design Target Structure

Plan the refactoring:
- How many files/classes should be created?
- What will each contain?
- How will they interact?
- What's the folder structure?

### Step 3: Extract with Care

- Extract one concern at a time
- Update references to extracted code
- Verify functionality still works
- Run tests (if available)

### Step 4: Validate

- Does each extracted component have single responsibility?
- Are dependencies clear and minimal?
- Is the code easier to understand and test?
- Can extracted code be reused elsewhere?

## Common Extraction Scenarios

### Scenario 1: Large Controller Class

**Problem:** 50+ line controller method doing validation, business logic, and response formatting

**Solution:**
1. Extract validation to Form Request or validator method
2. Extract business logic to Action class
3. Keep controller thin (3-5 lines)

### Scenario 2: Complex Component

**Problem:** React component with 200+ lines doing data fetching, state management, and rendering

**Solution:**
1. Extract data fetching to custom hook
2. Extract child components for different sections
3. Extract form logic to separate hook
4. Component becomes 30-40 lines focused on layout

### Scenario 3: God Service Class

**Problem:** Service class with 30+ public methods handling multiple unrelated operations

**Solution:**
1. Group related methods into separate service classes
2. Service A: `UserCreation` operations
3. Service B: `UserNotification` operations
4. Service C: `UserPermissions` operations
5. Update references to use appropriate service

### Scenario 4: Conditional Logic

**Problem:** Method with 5+ nested if/else levels

**Solution:**
1. Extract guard clauses to top (early returns)
2. Extract condition checking to named methods
3. Extract branch logic to separate methods
4. Result: Clear happy path with early exits

## Patterns to Follow

### Action Pattern (Preferred for Business Logic)

**Characteristics:**
- Single `handle()` method with clear purpose
- Dependencies injected via constructor
- Reusable from commands, controllers, jobs, API requests
- Easy to test

**When to use:** Any complex business logic (user creation, payment processing, data transformation)

### Hook Pattern (React/Vue)

**Characteristics:**
- Reusable logic encapsulated
- Composed into components
- Separate concerns (state, effects, validation)
- Testable independently

**When to use:** Reusable component logic (form handling, data fetching, permissions)

### Service Pattern (Node.js/Backend)

**Characteristics:**
- Focused on specific domain
- Clear public interface
- Encapsulates related operations
- Stateless or minimal state

**When to use:** Domain-specific operations (UserService, EmailService, PaymentService)

## Red Flags for Refactoring Need

Extract code when you see:

- **DRY Violation**: Same code appears 2+ times → Extract to reusable function
- **Naming Confusion**: Can't describe what a method does in a sentence → Doing too much
- **Test Difficulty**: Hard to test a method in isolation → Likely mixed concerns
- **Multiple Reasons to Change**: Modification requests affect different parts of code → SRP violation
- **Deep Nesting**: More than 3 levels of indentation → Extract inner logic
- **Long Parameter Lists**: More than 4 parameters → Group into object/DTO
- **Many Local Variables**: More than 5-6 variables → Likely multiple concerns
- **Scroll Fatigue**: Method longer than screen height → Break into smaller methods

## Advanced Patterns

### Refactoring with Dependencies

When extracting code with external dependencies:
1. Identify which services/dependencies are needed
2. Pass them as constructor parameters or method arguments
3. Extracted code is testable with mocked dependencies
4. Original code still works, now calling extracted code

### Refactoring with State

When extracting code that manages state:
1. Move state and state-changing logic together
2. Use appropriate state management (Context in React, local in Vue, closures in JS)
3. Ensure clear ownership of state
4. Extracted code has clear input/output

### Refactoring with Side Effects

When extracting code with side effects (DB writes, API calls, file I/O):
1. Extract the effect operation to separate method
2. Keep business logic pure when possible
3. Side effects at boundaries (entry points)
4. Easier to test pure logic separately

## Additional Resources

For language and framework-specific action patterns, see:
- **`references/extraction-patterns.md`** - Detailed extraction techniques
- **`references/smell-indicators.md`** - Code smell checklist
- **`examples/`** - Working refactoring examples

## Next Steps

After understanding refactoring principles, use the `/scan-code` command to identify candidates in your codebase, or `/split-code <file>` to refactor specific files following these patterns.
