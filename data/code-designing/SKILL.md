---
name: code-designing
description: |
  Domain type design and architectural planning for Go code.
  Use when planning new features, designing self-validating types, preventing primitive obsession, or when refactoring reveals need for new types.
  Focuses on vertical slice architecture and type safety.
allowed-tools:
  - Skill(go-linter-driven-development:testing)
---

<objective>
Domain type design and architectural planning for Go code.
Use when planning new features or identifying need for new types during refactoring.

**Reference**: See `reference.md` for complete design principles and examples.
</objective>

<quick_start>
1. **Analyze Architecture**: Check for vertical vs horizontal slicing
2. **Understand Domain**: Identify problem domain, concepts, invariants
3. **Identify Core Types**: Find primitives that need type wrappers
4. **Design Self-Validating Types**: Create types with validating constructors
5. **Plan Package Structure**: Vertical slices by feature
6. **Output Design Plan**: Present structured plan before implementation

Ready to implement? Use @testing skill for test structure.
</quick_start>

<when_to_use>
- Planning a new feature (before writing code)
- Refactoring reveals need for new types (complexity extraction)
- Linter failures suggest types should be introduced
- When you need to think through domain modeling
</when_to_use>

<purpose>
Design clean, self-validating types that:
- Prevent primitive obsession
- Ensure type safety
- Make validation explicit
- Follow vertical slice architecture
</purpose>

<workflow>

<architecture_pattern_analysis priority="FIRST_STEP">
**Default: Always use vertical slice architecture** (feature-first, not layer-first).

Scan codebase structure:
- **Vertical slicing**: `internal/feature/{handler,service,repository,models}.go`
- **Horizontal layering**: `internal/{handlers,services,domain}/feature.go`

<decision_flow>
1. **Pure vertical** → Continue pattern, implement as `internal/[new-feature]/`
2. **Pure horizontal** → Propose: Start migration with `docs/architecture/vertical-slice-migration.md`, implement new feature as first vertical slice
3. **Mixed (migrating)** → Check for migration docs, continue pattern as vertical slice
</decision_flow>

**Always ask user approval with options:**
- Option A: Vertical slice (recommended for cohesion/maintainability)
- Option B: Match existing pattern (if time-constrained)
- Acknowledge: Time pressure, team decisions, consistency needs are valid

**If migration needed**, create/update `docs/architecture/vertical-slice-migration.md`:
```markdown
# Vertical Slice Migration Plan
## Current State: [horizontal/mixed]
## Target: Vertical slices in internal/[feature]/
## Strategy: New features vertical, migrate existing incrementally
## Progress: [x] [new-feature] (this PR), [ ] existing features
```

See reference.md section #3 for detailed patterns.
</architecture_pattern_analysis>

<understand_domain>
- What is the problem domain?
- What are the main concepts/entities?
- What are the invariants and rules?
- How does this fit into existing architecture?
</understand_domain>

<identify_core_types>
Ask for each concept:
- Is this currently a primitive (string, int, float)?
- Does it have validation rules?
- Does it have behavior beyond simple data?
- Is it used across multiple places?

If yes to any → Consider creating a type
</identify_core_types>

<design_self_validating_types>
For each type:
```go
// Type definition
type TypeName underlyingType

// Validating constructor
func NewTypeName(input underlyingType) (TypeName, error) {
    // Validate input
    if /* validation fails */ {
        return zero, errors.New("why it failed")
    }
    return TypeName(input), nil
}

// Methods on type (if behavior needed)
func (t TypeName) SomeMethod() result {
    // Type-specific logic
}
```
</design_self_validating_types>

<plan_package_structure>
- **Vertical slices**: Group by feature, not layer
- Each feature gets its own package
- Within package: separate by role (service, repository, handler)

Good structure:
```
user/
├── user.go          # Domain types
├── service.go       # Business logic
├── repository.go    # Persistence
└── handler.go       # HTTP/API
```

Bad structure:
```
domain/user.go
services/user_service.go
repository/user_repository.go
```
</plan_package_structure>

<design_orchestrating_types>
For types that coordinate others:
- Make fields private
- Validate dependencies in constructor
- No nil checks in methods (constructor guarantees validity)

```go
type Service struct {
    repo        Repository  // private
    notifier    Notifier    // private
}

func NewService(repo Repository, notifier Notifier) (*Service, error) {
    if repo == nil {
        return nil, errors.New("repo required")
    }
    if notifier == nil {
        return nil, errors.New("notifier required")
    }
    return &Service{
        repo:     repo,
        notifier: notifier,
    }, nil
}

// Methods can trust fields are valid
func (s *Service) DoSomething() error {
    // No nil checks needed
    return s.repo.Save(...)
}
```
</design_orchestrating_types>

<review_against_principles>
Check design against (see reference.md):
- [ ] No primitive obsession
- [ ] Types are self-validating
- [ ] Vertical slice architecture
- [ ] Types designed around intent, not just shape
- [ ] Clear separation of concerns
</review_against_principles>

</workflow>

<output_format>
After design phase:

```
DESIGN PLAN

Feature: [Feature Name]

Core Domain Types:
- UserID (string) - Self-validating, prevents empty IDs
- Email (string) - Self-validating, RFC 5322 validation
- Age (int) - Self-validating, range 0-150

Orchestrating Types:
- UserService - Coordinates user operations
   Dependencies: Repository, Notifier
   Methods: CreateUser, GetUser, UpdateUser

Package Structure:
user/
  ├── user.go          # UserID, Email, Age, User
  ├── service.go       # UserService
  ├── repository.go    # Repository interface + implementations
  ├── notifier.go      # Notifier interface + implementations
  └── handler.go       # HTTP handlers

Design Decisions:
- UserID is custom type to prevent passing empty/invalid IDs
- Email validation centralized in NewEmail constructor
- Vertical slice keeps all user logic in one package
- Repository as interface allows multiple backends (Postgres, in-memory for tests)

Integration Points:
- Consumed by: HTTP API (/users endpoints)
- Depends on: Database, Email service
- Events: UserCreated event published after creation

Next Steps:
1. Create types with validating constructors
2. Write unit tests for each type
3. Implement UserService
4. Write integration tests

Ready to implement? Use @testing skill for test structure.
```
</output_format>

<key_principles>
See reference.md for detailed principles:
- Primitive obsession prevention (Yoke design strategy)
- Self-validating types
- Vertical slice architecture
- Types around intent and behavior, not just shape
- Single responsibility per type
</key_principles>

<pre_code_review>
Before writing code, ask:
- Can logic be moved into smaller custom types?
- Is this type designed around intent and behavior?
- Have I avoided primitive obsession?
- Is validation in the right place (constructor)?
- Does this follow vertical slice architecture?

Only after satisfactory answers, proceed to implementation.

See reference.md for complete design principles and examples.
</pre_code_review>

<success_criteria>
Design phase is complete when ALL of the following are true:

- [ ] Architecture pattern analyzed (vertical/horizontal/mixed)
- [ ] Core domain types identified with validation rules
- [ ] Self-validating type design documented
- [ ] Package structure follows vertical slice pattern
- [ ] Design decisions documented with rationale
- [ ] Pre-code review questions answered satisfactorily
- [ ] Design plan output presented to user
</success_criteria>
