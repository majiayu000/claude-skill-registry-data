---
name: laravel-refactor
description: Elite Laravel and Livewire refactoring skill for 2024-2025, covering modern tooling (Laravel Pint, PHPStan/Larastan, Pest, Rector), automated quality gates, CI/CD practices, static analysis adoption, and comprehensive code refactoring. Use for modernizing legacy code, setting up quality toolchains, eliminating anti-patterns, optimizing performance, implementing automated testing, configuring CI/CD pipelines, or upgrading to Laravel 11 patterns. Handles fat controllers, N+1 queries, security issues, Livewire optimization, static analysis setup, mutation testing, and architecture tests.
---

# Laravel & Livewire Refactoring Skill

Expert guidance for refactoring Laravel and Livewire applications to modern best practices, eliminating anti-patterns, and improving code quality.

## When to Use This Skill

Use this skill when the user:
- Requests to refactor Laravel or Livewire code
- Asks to set up modern Laravel tooling (Pint, PHPStan, Pest, Rector)
- Wants to implement CI/CD pipelines with quality gates
- Needs to configure static analysis and automated testing
- Asks to fix code smells or anti-patterns
- Wants to optimize database queries or performance
- Needs to modernize legacy Laravel code
- Requests to improve code architecture or structure
- Wants to fix security vulnerabilities
- Asks to upgrade to Livewire 3 patterns
- Needs help extracting business logic from controllers
- Requests to implement Laravel best practices
- Wants to set up pre-commit hooks or automated code review
- Asks about mutation testing or architecture tests

## Modern Laravel Tooling Stack (2024-2025)

The Laravel ecosystem has matured around a standardized quality toolchain:

### Core Quality Tools

**Laravel Pint** - Official code formatter (ships with Laravel)
- Zero-configuration formatting for Laravel projects
- Automatically fixes PSR-12 violations and Laravel conventions
- Run: `./vendor/bin/pint` to format, `./vendor/bin/pint --test` for CI validation

**PHPStan + Larastan** - Static analysis standard
- Larastan 2.0+ understands Laravel magic (facades, Eloquent, scopes)
- Most production apps target level 5-6 (catches real bugs without excessive strictness)
- Use baseline feature for legacy code: `./vendor/bin/phpstan analyse --generate-baseline`
- Progressive adoption: start at level 3, increase by 1 level per month

**Pest** - Modern testing framework with mutation testing
- Built-in architecture tests via `arch()` helper
- Mutation testing validates test quality automatically
- Compatible with existing PHPUnit tests (gradual migration)

**Rector** - Automated refactoring via AST transformations
- Used for framework upgrades and PHP version migrations
- Converts patterns at scale (array syntax, constructor promotion, etc.)

### When to Use Modern Tooling

**Setting up new projects**: Configure Pint + PHPStan level 5 + Pest + architecture tests from day one

**Modernizing legacy projects**: See `references/modern_tooling.md` for comprehensive setup guide including:
- Progressive PHPStan adoption with baseline strategy
- CI/CD pipeline configuration (GitHub Actions, GitLab CI)
- Pre-commit hooks setup (GrumPHP vs Husky comparison)
- Quality gates and automated review tools
- Laravel Shift for automated framework upgrades
- Complete toolchain integration patterns

**Quick tooling decisions**:
- Code formatting → Laravel Pint (official, zero-config)
- Static analysis → PHPStan + Larastan level 5-6
- Testing → Pest for new projects (mutation testing + architecture tests)
- CI/CD → GitHub Actions with quality gates (syntax → style → analysis → tests → security)
- Pre-commit hooks → GrumPHP (PHP teams) or Husky (full-stack teams)
- Automated upgrades → Laravel Shift

For detailed tooling setup, configuration examples, and production-proven CI/CD patterns, consult `references/modern_tooling.md`.

## Refactoring Decision Tree

```
User provides Laravel/Livewire code to refactor
    │
    ├─→ Is this a quick fix or specific pattern?
    │   ├─→ YES: Identify the pattern in references/laravel_patterns.md or references/livewire_patterns.md
    │   └─→ NO: Continue to comprehensive analysis
    │
    ├─→ Is this a full codebase or directory?
    │   ├─→ YES: Run scripts/analyze_code.py to identify all issues
    │   └─→ NO: Manual analysis
    │
    ├─→ What type of refactoring is needed?
    │   ├─→ Controllers: Extract to Actions/Services, Form Requests
    │   ├─→ Database: Fix N+1, add eager loading, optimize queries
    │   ├─→ Livewire: Component optimization, Forms, computed properties
    │   ├─→ Architecture: Repository pattern, service layer
    │   ├─→ Security: Mass assignment, validation, authorization
    │   └─→ General: Type hints, code organization, modern patterns
    │
    └─→ Apply refactoring patterns and provide refactored code
```

## Quick Reference: Common Refactoring Patterns

### 1. Fat Controller → Service/Action Class

**When**: Controller methods > 20 lines, complex business logic

```php
// BEFORE: Fat controller
public function store(Request $request)
{
    $validated = $request->validate([...]);
    $user = User::create($validated);
    Mail::to($user)->send(new WelcomeEmail($user));
    event(new UserRegistered($user));
    return redirect()->route('dashboard');
}

// AFTER: Thin controller with action
public function store(StoreUserRequest $request, RegisterUserAction $action)
{
    $user = $action->execute($request->validated());
    return redirect()->route('dashboard');
}
```

### 2. N+1 Query → Eager Loading

**When**: Accessing relationships in loops, slow query counts

```php
// BEFORE: N+1 problem
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name; // Query per post!
}

// AFTER: Eager loading
$posts = Post::with('user')->get();
foreach ($posts as $post) {
    echo $post->user->name; // Uses preloaded data
}
```

### 3. Inline Validation → Form Request

**When**: Validation rules > 5 fields, repeated validation

```php
// BEFORE: Inline validation
public function store(Request $request)
{
    $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        // 10+ more fields...
    ]);
}

// AFTER: Form Request class
public function store(StoreUserRequest $request)
{
    $validated = $request->validated();
}
```

### 4. Livewire Model Binding → Specific Properties

**When**: Direct model binding in Livewire components

```php
// BEFORE: Security risk
class EditUser extends Component
{
    public User $user; // Exposes entire model!
}

// AFTER: Specific properties
class EditUser extends Component
{
    public string $name;
    public string $email;
    private User $user;
    
    public function mount(User $user)
    {
        $this->user = $user;
        $this->name = $user->name;
        $this->email = $user->email;
    }
}
```

## Refactoring Workflow

### Step 1: Analysis

**For specific code snippets:**
1. Read the provided code
2. Identify anti-patterns using the quick reference above
3. Consult references/laravel_patterns.md or references/livewire_patterns.md for detailed patterns

**For full directories/codebases:**
1. Run the analyzer: `python3 scripts/analyze_code.py <directory>`
2. Review the generated report (prioritizes HIGH → MEDIUM → LOW)
3. Create a refactoring plan based on severity

### Step 2: Categorize Issues

Group identified issues by type:
- **Structure**: Fat controllers, missing layers, poor organization
- **Database**: N+1 queries, missing transactions, inefficient queries
- **Security**: Mass assignment, validation, authorization
- **Livewire**: Component patterns, performance, property binding
- **Code Quality**: Type hints, magic values, error handling

### Step 3: Refactor Systematically

Follow this priority order:
1. **Security issues** (HIGH priority)
   - Fix mass assignment vulnerabilities
   - Add proper validation
   - Implement authorization

2. **Performance issues** (HIGH priority)
   - Fix N+1 queries
   - Add database transactions
   - Optimize large queries

3. **Architecture improvements** (MEDIUM priority)
   - Extract business logic from controllers
   - Create service/action classes
   - Implement repository pattern if needed

4. **Code quality** (MEDIUM/LOW priority)
   - Add type hints and return types
   - Replace magic values with enums
   - Improve error handling

### Step 4: Apply Refactoring Patterns

Consult the detailed reference files for specific patterns:

**Laravel patterns**: See `references/laravel_patterns.md` for:
- Fat controller refactoring
- Query optimization techniques
- Modern Laravel features
- Security best practices

**Livewire patterns**: See `references/livewire_patterns.md` for:
- Component optimization
- Livewire 3 migration
- Performance patterns
- Event-driven communication

**Comprehensive checklist**: See `references/refactoring_checklist.md` for:
- Step-by-step refactoring process
- Pre/post-refactoring tasks
- Testing strategies
- Documentation requirements

### Step 5: Validate Changes

After refactoring:
1. Ensure all functionality remains intact
2. Add/update tests for refactored code
3. Verify performance improvements
4. Check security enhancements
5. Document significant architectural changes

## Automated Analysis Tool

Use the code analyzer for comprehensive analysis:

```bash
# Analyze controllers
python3 scripts/analyze_code.py app/Http/Controllers

# Analyze Livewire components
python3 scripts/analyze_code.py app/Http/Livewire

# Analyze entire app directory
python3 scripts/analyze_code.py app

# Generate JSON report
python3 scripts/analyze_code.py app --json
```

The analyzer detects:
- Fat controllers (> 30 lines per method)
- N+1 query problems
- Missing type hints
- Magic numbers and strings
- Inline validation
- Mass assignment vulnerabilities
- Missing transactions
- Livewire anti-patterns

## Best Practices for Refactoring

### Start Small
- Refactor one file/method at a time
- Make incremental changes
- Test after each change
- Commit frequently

### Maintain Backward Compatibility
- Keep existing public APIs intact
- Use deprecation warnings for changes
- Update documentation for breaking changes

### Write Tests First
- Add tests for existing behavior before refactoring
- Verify tests pass after refactoring
- Add new tests for improved functionality

### Follow Laravel Conventions
- Use PSR-12 coding standards
- Follow Laravel naming conventions
- Leverage framework features over custom solutions

## Common Refactoring Scenarios

### Scenario 1: "This controller is too large"
1. Identify distinct responsibilities in the controller
2. Extract business logic to Action/Service classes
3. Move validation to Form Request classes
4. Keep controllers thin (coordinate between layers)
5. Use route model binding where possible

### Scenario 2: "The application is slow"
1. Run analyzer to identify N+1 queries
2. Add eager loading with ->with()
3. Use select() to limit columns
4. Implement caching for frequent queries
5. Add database indexes
6. Consider query optimization (chunk, lazy)

### Scenario 3: "Need to upgrade to Livewire 3"
1. Replace computed property methods with #[Computed] attributes
2. Migrate to Form objects for complex forms
3. Update public property type hints
4. Replace wire:model with wire:model.live where needed
5. Test all component interactions

### Scenario 4: "Code has security vulnerabilities"
1. Replace $request->all() with validated()
2. Add $fillable or $guarded to all models
3. Implement Form Requests for validation
4. Add authorization policies
5. Review and fix SQL injection risks
6. Validate all file uploads

## Tips for Effective Refactoring

**DO:**
- Read the entire reference files when encountering complex patterns
- Use the analyzer for objective assessment
- Refactor with tests to prevent regressions
- Keep changes focused and atomic
- Document significant architectural changes

**DON'T:**
- Make multiple types of changes in one commit
- Skip testing after refactoring
- Over-engineer simple solutions
- Break existing functionality
- Refactor without understanding the business logic

## Additional Resources

This skill includes comprehensive reference documentation:

- **references/modern_tooling.md**: Complete 2024-2025 tooling guide covering Laravel Pint, PHPStan/Larastan, Pest, Rector, CI/CD pipelines, quality gates, pre-commit hooks, automated upgrades, and production-proven patterns from Spatie, Tighten, and Beyond Code
- **references/laravel_patterns.md**: 10+ common Laravel anti-patterns with solutions, query optimization, modern features
- **references/livewire_patterns.md**: Livewire-specific patterns, component optimization, Livewire 3 migration guide
- **references/refactoring_checklist.md**: Complete refactoring workflow, checklists, metrics tracking

The analyzer script provides automated detection of common issues across your codebase.
