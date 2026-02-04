---
name: quality-code-check
description: |
  Code quality validation through linting, type checking, and build verification.
  Multi-language support for automated quality gates.

  Use when validating code quality:
  - After implementation to validate code meets standards
  - Before creating pull requests or commits
  - When debugging build/type/lint issues
  - User explicitly requests quality checks

  Provides language-specific tool commands and validation workflows for:
  - JavaScript/TypeScript (ESLint, tsc, build tools)
  - Python (Ruff, MyPy, Pyright)
  - Go (golangci-lint, go build)
  - Rust (Clippy, cargo check/build)
  - Java (Gradle, Maven)

  Focuses on detecting issues early through systematic automated checks.
---

# Quality Code Check

## Purpose
Establish consistent code quality standards through automated validation tools, ensuring code reliability, maintainability, and consistency.

---

## Core Principle

Code quality validation is a safety gate that catches errors early, prevents tech debt accumulation, and ensures code meets project standards.

---

## Quality Check Categories

### 1. Linting - Code Style & Best Practices

**What linting detects:**
- Code style violations (indentation, spacing, naming)
- Unused variables and imports
- Missing error handling patterns
- Potentially dangerous patterns
- Code complexity issues

**Language-specific tools:**
- **JavaScript/TypeScript**: ESLint
- **Python**: Ruff, Flake8
- **Go**: golangci-lint
- **Rust**: Clippy
- **Java**: Spotbugs, Checkstyle

**Approach:**
- Run linting on all modified files
- Auto-fix warnings when possible
- Fix remaining errors manually
- Minimize warnings to project standards

---

### 2. Type Checking - Type Safety

**What type checking validates:**
- Type consistency
- Function parameter and return types
- Null/undefined safety
- Generic type parameters

**Language-specific tools:**
- **TypeScript**: `tsc --noEmit`
- **Python**: MyPy, Pyright
- **Go**: Compiler (built-in)
- **Rust**: Compiler (built-in)
- **Java**: Compiler (built-in)

**Approach:**
- Enable strict type checking when available
- Run on all modified code
- Fix type errors before proceeding
- Use type annotations for function signatures

---

### 3. Build Verification - Compilability & Packaging

**What build checking validates:**
- Code compiles without errors
- All imports and dependencies resolve
- Asset bundling completes
- Runtime entry points exist

**Language-specific tools:**
- **JavaScript/TypeScript**: Webpack, Vite, or `npm run build`
- **Python**: `python -m py_compile` or test imports
- **Go**: `go build ./...`
- **Rust**: `cargo build`
- **Java**: Maven (`mvn compile`), Gradle (`gradle build`)

**Approach:**
- Run full build after all changes complete
- Use production build configuration when available
- All build steps must succeed without errors

---

## Tool Invocation

**Note:** Commands are examples. Adjust to your project's package manager, config files, and scripts.

### Project Detection

**Use Glob to detect project type:**
- Glob(pattern="`**`/package.json") → JavaScript/TypeScript
- Glob(pattern="`**`/pyproject.toml") or Glob(pattern="`**`/requirements.txt") → Python
- Glob(pattern="`**`/go.mod") → Go
- Glob(pattern="`**`/Cargo.toml") → Rust
- Glob(pattern="`**`/pom.xml") or Glob(pattern="`**`/build.gradle") → Java

### Language-Specific Commands

#### JavaScript/TypeScript

```bash
# Check package.json scripts first
npm run lint
npx eslint . --max-warnings=0

# Type checking
npm run typecheck
npx tsc --noEmit

# Build
npm run build
```

#### Python

```bash
# Linting
ruff check .
ruff check . --fix  # auto-fix

# Type checking
mypy .
pyright

# Import check
python -c 'import your_package'
```

#### Go

```bash
# Linting
golangci-lint run
go vet ./...

# Build (includes type checking)
go build ./...
```

#### Rust

```bash
# Linting
cargo clippy -- -D warnings

# Type checking
cargo check

# Build
cargo build
cargo build --release  # production
```

#### Java

```bash
# Gradle
./gradlew check
./gradlew build

# Maven
mvn verify
mvn compile
```

### Error Handling

**Tool not found:**
- Try command, catch error
- If not found: Skip check, notify user
- Continue with remaining checks

**Check fails:**
- Parse error output
- Report specific violations
- Suggest fixes based on error type
- Retry after fixes

---

## Validation Workflow

### When to Run

- After implementation is stable enough
- Before creating pull requests or commits
- When user explicitly requests
- Incrementally during development (optional)

### Quality Check Sequence

1. **Detect available tools** from project configuration
   - Use Glob to find config files
   - Identify which tools are available

2. **Run linting** (scoped to changed files when possible)
   - Execute appropriate commands
   - Fix auto-fixable issues first (--fix flag)
   - Manually fix remaining violations
   - Target: Meet project's warning standards

3. **Run type checks**
   - Execute appropriate commands
   - Fix all type errors
   - Validate type consistency across modules
   - Target: No type errors

4. **Run build** (full build, production config when available)
   - Execute appropriate commands
   - Ensure all code compiles
   - Validate all imports resolve
   - Confirm output artifacts generated
   - Target: Build succeeds without critical errors

### Error Recovery

**If quality checks fail:**
1. **Analyze errors** - Identify root causes
2. **Fix issues** - Make minimal changes to resolve
3. **Re-run checks** - Execute same commands again
4. **Repeat** - Continue until checks pass

**If unable to fix:**
- Document the issue and root cause
- Mark as blocked if preventing progress
- Escalate or ask user for guidance

---

## Common Mistakes

1. **Ignoring warnings** - Warnings often indicate real problems
   → Fix them or understand why acceptable
2. **Only checking one file** - Changes can break type checking across others
   → Check all modified files and dependencies
3. **Skipping the build step** - Code might lint/type-check but fail to compile
   → Always verify full build
4. **Accepting auto-fixes blindly** - Auto-fixes might hide real issues
   → Review each auto-fix before committing
5. **Not checking package.json scripts** - Projects often define custom commands
   → Check scripts first before running tools directly
6. **Inconsistent standards** - Allowing different levels across features
   → Maintain consistent standards for your project

---

## Validation Checklist

Before considering quality checks complete:
- [ ] Code is stable enough to validate
- [ ] Linting tool runs successfully on changed files
- [ ] Lint warnings minimized to project-acceptable levels
- [ ] Type checking tool runs successfully
- [ ] No critical type errors remain
- [ ] Build completes successfully
- [ ] No critical build errors present
- [ ] Warnings at project-acceptable levels
- [ ] All blocking issues fixed or escalated

---

## Key Takeaway

**Systematic quality validation catches issues early and maintains consistency.**

Quality checks are flexible gates that validate code against project standards:
- Run when code is stable enough
- Adjust tool commands to your project's needs
- Target project-appropriate warning levels
- Use as validation before PRs, commits, or deployment

Commands shown are examples - check your project's scripts first. Quality standards should be consistent within your project but may vary between projects.

Systematic checks catch errors early, prevent tech debt accumulation, and build confidence in code readiness.
