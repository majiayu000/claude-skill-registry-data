---
name: rails-implementation
description: Rails project implementation, testing, and documentation support. Use this skill when working on Rails projects for implementing new features, adding tests to existing code, updating documentation, creating CRUD operations, building API endpoints, adding authentication, or any Rails development task. Triggers on Rails-specific implementation requests.
---

# Rails Implementation

## Overview

This skill provides comprehensive support for Rails development, including:
- Feature implementation with Rails best practices
- Test creation (RSpec/Minitest) with meaningful coverage
- Code quality maintenance to prevent bloated classes and methods
- Common pattern implementation (CRUD, authentication, APIs, etc.)

## Development Workflow

Follow this workflow when implementing Rails features:

### 1. Understand the Request

- Clarify requirements if ambiguous
- Identify which models, controllers, and views are affected
- Determine if new migrations are needed

### 2. Detect Project Configuration

Before implementation, identify:

**Test Framework:**
```bash
# Check for RSpec
ls spec/

# Check for Minitest
ls test/
```

**Rails Version:**
```bash
cat Gemfile | grep "rails"
```

**Database:**
```bash
cat config/database.yml
```

### 3. Plan the Implementation

Consider:
- **Scope**: Keep methods under 15 lines, classes focused
- **Patterns**: Use service objects, query objects, form objects when appropriate
- **Testing**: Plan meaningful tests (avoid testing constants, simple accessors)
- **References**: Check [rails-patterns.md](references/rails-patterns.md) for common patterns

### 4. Implement

**Code Quality Standards:**
- ✅ Methods: 5-10 lines (max 15)
- ✅ Controllers: Max 7 RESTful actions
- ✅ Models: Max 20 public methods
- ✅ Nesting: Max 2-3 levels (use early returns)
- ✅ Single Responsibility: One purpose per class/method

**When to Extract:**
- **Service Objects**: Complex business logic, multi-step processes
- **Query Objects**: Complex database queries
- **Form Objects**: Multi-model forms
- **Decorators**: Presentation logic

For detailed patterns and examples, see [code-quality.md](references/code-quality.md).

**After Model Changes (if annotate gem exists):**

When creating or modifying models:
1. Run migrations: `rails db:migrate`
2. Check for annotate gem: `bundle list | grep annotate`
3. If annotate exists, run: `bundle exec annotate`
4. Add meaningful descriptions to columns in the generated annotations

See [rails-patterns.md](references/rails-patterns.md) → Model Annotations for details.

### 5. Write Tests

**Test Strategy:**

Tests are **mandatory** but should be **meaningful**.

**✅ DO Test:**
- Custom business logic and methods
- Complex validations with custom logic
- Controller actions (request specs preferred)
- Service objects and POROs
- Scopes with complex logic
- Callbacks with side effects

**❌ DON'T Test:**
- Constant values
- Simple attribute accessors
- Framework features (Rails validations/associations without custom logic)
- Private methods directly
- Database schema

**Test Framework Patterns:**

See [testing-guide.md](references/testing-guide.md) for detailed examples covering:
- RSpec model, controller, and request specs
- Minitest model, controller, and system tests
- What to test and what to avoid

### 6. Update Documentation (If Needed)

Update documentation only when:
- Adding new API endpoints
- Changing public interfaces
- Adding complex features requiring explanation
- Modifying setup/deployment procedures

## Common Implementation Patterns

For quick reference, common patterns include:

**Model Annotations** - Adding schema information with meaningful column descriptions using annotate gem

**CRUD Operations** - Basic resource implementation with model, controller, views

**Authentication** - Devise integration or custom authentication

**API Endpoints** - JSON API with proper status codes and error handling

**Background Jobs** - Active Job for asynchronous processing

**File Uploads** - Active Storage for attachments

**Search & Filtering** - Scopes and query objects for data retrieval

**Associations** - has_many, belongs_to, has_many :through, polymorphic

For detailed implementation examples, see [rails-patterns.md](references/rails-patterns.md).

## Testing Strategy

### Test-Driven Development (TDD)

TDD is **recommended but not mandatory**. The workflow is:

1. **Red**: Write failing test
2. **Green**: Minimal implementation to pass
3. **Refactor**: Improve code while keeping tests green

Whether writing tests first or after implementation, **tests are mandatory** for all custom logic.

### Test Coverage Priorities

**High Priority:**
1. Business logic and custom methods
2. Service objects
3. Controller actions (happy path + error cases)
4. Complex validations

**Low Priority:**
- Simple CRUD without custom logic
- Framework features

**Never Test:**
- Constants, accessors, schema, framework validations (see testing-guide.md)

## Code Quality Checkpoints

Before considering implementation complete, verify:

- [ ] No methods exceed 15 lines
- [ ] No deep nesting (max 2-3 levels)
- [ ] Controllers have max 7 actions
- [ ] Models have max 20 public methods
- [ ] Complex logic extracted to service/query/form objects
- [ ] All custom logic has meaningful tests
- [ ] No useless tests (constants, simple accessors)

If any checkpoint fails, refactor before proceeding.

## References

This skill includes detailed reference documentation:

### [rails-patterns.md](references/rails-patterns.md)
Common Rails implementation patterns with code examples:
- CRUD operations
- Authentication & Authorization
- API endpoints
- Background jobs
- File uploads
- Search & filtering
- Associations

**When to read:** When implementing a feature and need a pattern reference.

### [testing-guide.md](references/testing-guide.md)
Comprehensive testing guide with RSpec and Minitest examples:
- What to test vs. what NOT to test
- Model, controller, and request test examples
- System tests
- Avoiding meaningless tests

**When to read:** When writing tests or unsure if a test is meaningful.

### [code-quality.md](references/code-quality.md)
Code quality guidelines and refactoring patterns:
- Method and class size limits
- Service objects, query objects, form objects, decorators
- Refactoring patterns
- Early returns and extract method

**When to read:** When code feels bloated or before committing large changes.

## Quick Start Examples

### Example 1: Add "Like" Feature to Articles

**Request:** "Add a like feature to articles"

**Workflow:**
1. Create `Like` model with migration
2. Run `rails db:migrate`
3. If annotate gem exists: Run `bundle exec annotate` and add column descriptions
4. Add associations (`Article has_many :likes`, `User has_many :likes`)
5. Create `LikesController` with `create` and `destroy` actions
6. Add routes (`resources :articles { resources :likes, only: [:create, :destroy] }`)
7. Write tests for model associations and controller actions
8. Add UI button in article view

**Check:** Methods stay under 15 lines, tests cover like/unlike behavior, annotations updated.

### Example 2: Create API Endpoint for Articles

**Request:** "Create API endpoint to list articles"

**Workflow:**
1. Create `Api::V1::ArticlesController`
2. Implement `index` action returning JSON
3. Add serializer if response needs custom formatting
4. Add routes under `namespace :api { namespace :v1 { resources :articles } }`
5. Write request specs testing JSON response and status codes

**Reference:** See [rails-patterns.md](references/rails-patterns.md) → API Endpoints section

### Example 3: Add Tests to Existing File

**Request:** "Add tests to app/models/article.rb"

**Workflow:**
1. Read `app/models/article.rb` to understand custom logic
2. Identify meaningful test cases (custom methods, validations, scopes)
3. Skip testing constants, accessors, basic associations
4. Write tests in `spec/models/article_spec.rb` (RSpec) or `test/models/article_test.rb` (Minitest)
5. Run tests to verify

**Reference:** See [testing-guide.md](references/testing-guide.md) → What to Test

## Notes

- **Language:** Always respond in Japanese (日本語) per user's global settings
- **TDD:** Recommended but not mandatory; tests are always mandatory
- **Git Operations:** Only commit/push when explicitly requested
- **Code Style:** Follow existing project patterns and conventions
