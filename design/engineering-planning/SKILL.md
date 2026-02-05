---
name: engineering-planning
description: Guidelines for planning engineering tasks with precision and clarity. Use this skill when creating todo lists, breaking down complex engineering tasks, or designing implementation plans for software development work. Emphasizes concrete, actionable steps without time estimates.
---

# Engineering Planning

## Overview

This skill provides principles and guidelines for planning engineering tasks effectively. Apply these principles when breaking down software development work into actionable steps, creating todo lists, or designing implementation approaches.

## Core Planning Principles

Follow these principles when planning any engineering task:

### 1. Be Concrete and Precise

Every task should describe a specific, observable action or outcome. Avoid vague language.

**Bad examples:**
- ❌ "Improve performance"
- ❌ "Fix the bug"
- ❌ "Update the frontend"
- ❌ "Refactor the code"

**Good examples:**
- ✅ "Add database index on users.email column to optimize login queries"
- ✅ "Fix null pointer exception in AuthController.validateToken() at line 145  "
- ✅ "Update UserProfile component to display avatar images from S3"
- ✅ "Extract duplicate validation logic from UserService into ValidationUtils class"

### 2. Never Estimate Timeframes

Do not include time estimates, durations, or speed qualifiers in task descriptions. Focus on what needs to be done, not how long it might take.

**Bad examples:**
- ❌ "Quick fix for login redirect"
- ❌ "This should take 2-3 hours"
- ❌ "Simple refactor of the auth module"
- ❌ "Fast optimization pass"

**Good examples:**
- ✅ "Fix login redirect to preserve original destination URL"
- ✅ "Refactor authentication module to separate concerns"
- ✅ "Optimize image loading by implementing lazy loading"
- ✅ "Add error handling for failed API requests"

### 3. Focus on Actionable Outcomes

Each task should result in a clear, testable outcome. State what will exist or what will change after completing the task.

**Bad examples:**
- ❌ "Work on database"
- ❌ "Handle errors better"
- ❌ "Look into caching"

**Good examples:**
- ✅ "Add foreign key constraint between orders and users tables"
- ✅ "Add try-catch blocks to all async API calls with user-facing error messages"
- ✅ "Implement Redis cache for product catalog queries with 1-hour TTL"

## Task Breakdown Guidelines

When breaking down complex engineering work into tasks, follow this approach:

### Step 1: Identify the Major Components

List the distinct parts of the system that need to change. Examples:
- Database schema
- API endpoints
- Frontend components
- Business logic
- Configuration
- Tests
- Documentation

### Step 2: Create Tasks for Each Component

For each component, define specific changes needed. Include:
- **What** is being changed (file, function, class, table)
- **Why** the change is necessary (purpose, problem being solved)
- **How** it will be verified (what confirms the task is complete)

### Step 3: Order by Dependencies

Arrange tasks so that:
- Foundation work comes first (database, models, core logic)
- Dependent work comes later (UI that depends on APIs)
- Independent work can be done in any order
- Testing and validation come after implementation

### Step 4: Make Tasks Self-Contained

Each task should be completable independently. If a task requires another task's output, split it further or ensure proper ordering.

## Task Description Format

Use this format for task descriptions:

**Pattern:** `[Action verb] + [Specific target] + [Context/purpose]`

**Examples:**
- "Add UserContext provider to manage authentication state across components"
- "Update API endpoint /api/users/:id to return 404 when user not found"
- "Create PostgreSQL migration to add email_verified column to users table"
- "Implement input validation for email field in RegistrationForm component"
- "Extract duplicate date formatting logic into shared DateUtils module"

## When Breaking Down Different Task Types

### Feature Implementation

**Structure:**
1. Define data model changes
2. Implement backend logic/APIs
3. Create frontend components
4. Add validation and error handling
5. Write tests
6. Update documentation

### Bug Fixes

**Structure:**
1. Identify root cause location (file, function, line)
2. Define the fix (what code change resolves it)
3. Add tests to prevent regression
4. Verify no side effects in related code

### Refactoring

**Structure:**
1. Identify code to be refactored (specific files/functions)
2. Define the target structure
3. Extract/move/rename in small steps
4. Run tests after each step
5. Update references and imports

### Performance Optimization

**Structure:**
1. Identify specific bottleneck (query, function, component)
2. Define the optimization approach (index, cache, algorithm)
3. Implement the optimization
4. Measure impact with metrics
5. Verify no functionality regression

## Red Flags to Avoid

Watch for these patterns and revise tasks that contain them:

- **Vague qualifiers**: "better", "improved", "optimized", "cleaned up"
- **Time qualifiers**: "quick", "simple", "fast", "should be easy"
- **Missing targets**: "fix bugs", "update code", "handle errors"
- **Ambiguous scope**: "work on authentication", "deal with the database"
- **Unclear outcomes**: "investigate issue", "look into performance"

## Task Completion Criteria

Mark a task as complete only when:

1. **The specific change described has been implemented**
2. **The implementation has been verified** (manually tested or automated tests pass)
3. **No blocking errors or failures exist**

If errors occur or the task cannot be completed as planned:
- Keep the task as in-progress
- Create new tasks to resolve blockers
- Document what prevented completion

## Examples of Well-Planned Task Sequences

### Example 1: Adding Authentication

```
1. Create users table with email, password_hash, created_at columns
2. Implement bcrypt password hashing in AuthService.hashPassword()
3. Add POST /api/auth/register endpoint to create new users
4. Add POST /api/auth/login endpoint to validate credentials and return JWT
5. Create AuthContext provider to store JWT and user state
6. Add ProtectedRoute component to redirect unauthenticated users
7. Update App.tsx to wrap authenticated routes with ProtectedRoute
8. Add logout functionality to clear JWT from AuthContext
```

### Example 2: Fixing Performance Issue

```
1. Add database index on products.category_id column
2. Update ProductRepository.findByCategory() to use indexed query
3. Implement Redis caching for ProductRepository.findByCategory() results
4. Set cache TTL to 15 minutes for product category queries
5. Add cache invalidation on product updates in ProductService.updateProduct()
6. Run load tests to verify query time reduced below 100ms threshold
```

### Example 3: Refactoring Duplicate Code

```
1. Extract email validation regex to ValidationUtils.EMAIL_REGEX constant
2. Create ValidationUtils.isValidEmail(email) method
3. Replace validation logic in RegistrationForm with ValidationUtils.isValidEmail()
4. Replace validation logic in ProfileEditForm with ValidationUtils.isValidEmail()
5. Replace validation logic in AdminUserForm with ValidationUtils.isValidEmail()
6. Run all form validation tests to ensure behavior unchanged
```

## Integration with Todo Lists

When using the TodoWrite tool, apply all principles above to ensure:

- Each todo item is concrete and actionable
- No time estimates appear in todo descriptions
- Tasks are ordered by dependencies
- The active form uses present continuous tense (e.g., "Adding database index" not "Add database index")
- Tasks are marked complete only when fully finished

Remember: Planning is about clarity and precision, not prediction. Focus on defining what needs to be done, not when it will be done.
