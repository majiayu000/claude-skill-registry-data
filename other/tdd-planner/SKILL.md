---
name: tdd-planner
description: This skill should be used when the user asks to "plan a feature", "prepare for dev loop", "structure TDD approach", "break down this task", "create development plan", or when generating structured prompts for iterative development. Creates dev-loop-ready plans with TDD phases, file tables, code snippets, and framework-specific guidance.
---

# TDD Planner

Generate high-quality, structured development plans following Test-Driven Development principles for use with the dev-loop command.

## Quality Standard

Every plan must meet this checklist before saving:

- [ ] Context lists **specific items** to work on (not just "the feature")
- [ ] Success criteria are **measurable** (numbers, specific behaviors)
- [ ] **Every task** has a file path
- [ ] **Code snippets** show implementation structure
- [ ] Verification has **expected output** (PASS/FAIL + why)
- [ ] Self-correction is **phase-specific**, not generic
- [ ] **Files to Modify** table exists
- [ ] **New Files to Create** table exists
- [ ] Stuck handling is **framework/task-specific**

**Reference:** See `references/good-example.md` for expected quality.

## Activation Triggers

This skill activates when:
- Planning a feature for iterative development
- Preparing prompts for dev-loop execution
- Breaking down complex tasks into TDD phases
- Creating structured development workflows

## Core Principles

1. **Specificity Over Vagueness** - File paths, code snippets, measurable outcomes
2. **Iteration Over Perfection** - Expect multiple passes, not first-draft solutions
3. **Failures as Data** - Red phase tests MUST fail first
4. **Framework Awareness** - Use correct patterns for detected framework

## Required Plan Sections

### 1. Context

```markdown
## Context

- **Framework**: Flutter / Django / Next.js / etc.
- **Current State**: What exists now
- **Test Command**: `flutter test` / `pytest` / etc.
- **Lint Command**: `flutter analyze` / `ruff check .` / etc.
- **Items to Work On**:
  - `ComponentA` (description)
  - `ComponentB` (description)
```

### 2. Success Criteria (Measurable)

```markdown
## Success Criteria

- [ ] Login returns JWT token (specific behavior)
- [ ] 81+ tests pass (quantitative)
- [ ] Invalid credentials return 401 (negative case)
- [ ] All tests pass (`flutter test`)
- [ ] Linter clean (`flutter analyze`)
```

### 3. File Tables (Required)

```markdown
## Files to Modify

| File | Action |
|------|--------|
| `lib/main.dart` | Replace MultiProvider with ProviderScope |
| `pubspec.yaml` | Add flutter_riverpod dependency |

## New Files to Create

| File | Purpose |
|------|---------|
| `lib/providers/auth_provider.dart` | Riverpod auth state |
| `test/providers/auth_test.dart` | Auth provider tests |
```

### 4. Phases with Code Snippets

```markdown
### Phase 2: Green - Implement Auth Provider

**Goal:** Create Riverpod provider that passes tests

**Tasks:**
- [ ] Create `lib/providers/auth_provider.dart`:
  - StateNotifierProvider with AuthNotifier
  - Methods: login(), logout(), checkAuth()
  - State: AuthState (authenticated, user, token)

**Implementation Structure:**
```dart
final authProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  return AuthNotifier();
});

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier() : super(AuthState.initial());

  Future<void> login(String email, String password) async {
    // Implementation
  }
}
```

**Verification:**
```bash
flutter test test/providers/auth_test.dart
```
**Expected:** Tests should PASS

**Self-correction:**
- If tests fail, check state class matches test expectations
- Verify StateNotifier lifecycle is correct
```

### 5. Stuck Handling (Framework-Specific)

```markdown
## Stuck Handling

### If same test keeps failing:
1. Read the exact error message
2. Check if ProviderScope wraps the widget tree
3. Verify ref.watch vs ref.read usage
4. Check state class matches expected structure

### If app won't start:
1. Check ProviderScope is at app root
2. Verify no circular provider dependencies
3. Check async initialization is handled

### Alternative approaches if blocked:
1. Keep hybrid approach temporarily (both Provider and Riverpod)
2. Migrate one screen at a time
3. Use ChangeNotifierProvider adapter for gradual migration
```

## Framework Detection

**Package manager auto-detection** (defaults to `bun`):
- `bun.lockb` → bun
- `pnpm-lock.yaml` → pnpm
- `yarn.lock` → yarn
- `package-lock.json` → npm
- No lockfile → bun (default)

**Auto-detected frameworks (17+):**

| Category | Framework | Detection | Test | Lint |
|----------|-----------|-----------|------|------|
| **Mobile** | Flutter | `pubspec.yaml` | `flutter test` | `flutter analyze` |
| | React Native | `react-native` in package.json | `${PM} test` | `${PM} run lint` |
| **Python** | Django | `manage.py` | `pytest` | `ruff check .` |
| | FastAPI | `fastapi` in pyproject.toml | `pytest` | `ruff check .` |
| | Flask | `flask` in pyproject.toml | `pytest` | `ruff check .` |
| **Node.js** | NestJS | `@nestjs/core` | `${PM} test` | `${PM} run lint` |
| | Next.js | `next` | `${PM} test` | `${PM} run lint` |
| | Nuxt.js | `nuxt` | `${PM} test` | `${PM} run lint` |
| | Hono | `hono` | `bun test` | `bun run lint` |
| | Express | `express` | `${PM} test` | `${PM} run lint` |
| | TanStack | `@tanstack/react-router` | `bun test` | `bun run lint` |
| **Systems** | Go | `go.mod` | `go test ./...` | `golangci-lint run` |
| | Rust | `Cargo.toml` | `cargo test` | `cargo clippy` |
| **Web** | Rails | `rails` in Gemfile | `bundle exec rspec` | `bundle exec rubocop` |
| | Laravel | `laravel` in composer.json | `php artisan test` | `./vendor/bin/pint` |

`${PM}` = detected package manager (bun/pnpm/yarn/npm)

**Custom frameworks:**

```bash
/dev-plan "Build API" --framework elixir --test-cmd "mix test" --lint-cmd "mix credo"
/dev-plan "Add feature" --test-cmd "make test" --lint-cmd "make lint"
```

## Phase Generation Rules

### For New Features
1. **Red**: Write tests for the feature interface (expect FAIL)
2. **Green**: Implement minimum code to pass (include code snippet)
3. **Refactor**: Clean up, add types, documentation

### For Bug Fixes
1. **Red**: Write test that reproduces the bug (should fail)
2. **Green**: Fix the bug (test passes)
3. **Refactor**: Ensure no regression, clean up

### For Refactoring/Migration
1. **Red**: Ensure existing tests pass (baseline)
2. **Green**: Apply changes incrementally
3. **Refactor**: Verify tests still pass after each change

## Task Detail Pattern

**Bad Task:**
```markdown
- [ ] Create login view
```

**Good Task:**
```markdown
- [ ] Create `lib/screens/login_screen.dart`:
  - ConsumerStatefulWidget
  - Form with email/password TextFormFields
  - Calls `ref.read(authProvider.notifier).login()`
  - Shows loading state during auth
  - Navigates to home on success
  - Shows error snackbar on failure
```

## Anti-Patterns to Avoid

| Don't | Do Instead |
|-------|------------|
| "Implement the feature" | "Create `lib/auth/login.dart` with ConsumerWidget" |
| "If it fails, try again" | "If tests pass in Red, they're too weak - add assertions" |
| Missing code snippets | Show actual structure with types and patterns |
| No file tables | Always list files to modify/create |
| "App works well" | "Login returns JWT, logout invalidates token, 401 on bad creds" |
| Generic stuck handling | Framework-specific: "Check ProviderScope wraps app" |

## Usage

### Generate Plan
```bash
/dev-plan "Migrate to Riverpod" --framework flutter
/dev-plan "Add user authentication" --interactive
```

### Execute Plan
```bash
/dev-loop --from-plan
```

## References

- `references/plan-template.md` - Full template with all variables
- `references/good-example.md` - High-quality Flutter migration example
- `references/framework-patterns.md` - Framework-specific patterns
