---
name: validate-architecture
description: Validates architectural patterns and code quality per CLAUDE.md, detects anti-patterns and design violations
user-invocable: true
---

# Validate Architecture Skill

## Purpose
Validates architectural patterns and code quality standards per CLAUDE.md. Detects anti-patterns, placeholders, and violations of Pierre's design principles.

## CLAUDE.md Compliance
- ✅ Enforces zero tolerance policies (no unwrap, no anyhow!, no placeholders)
- ✅ Validates architectural patterns (DI, resource management)
- ✅ Checks algorithm isolation (enum-based DI)
- ✅ Detects Claude Code anti-patterns

## Usage
Run this skill:
- Before committing code
- Before pull requests
- After refactoring
- Weekly code quality audits
- After major feature additions

## Prerequisites
- Python 3 (for pattern parsing)
- ripgrep (`rg`)
- Validation patterns file: `scripts/validation-patterns.toml`

## Commands

### Comprehensive Validation
```bash
# Run all architectural validations
./scripts/architectural-validation.sh
```

### Specific Pattern Categories

#### Critical Failures
```bash
# Check for placeholder implementations
python3 scripts/parse-validation-patterns.py \
  scripts/validation-patterns.toml placeholder_patterns

# Check for unwrap/expect/panic
rg "\.unwrap\(\)|\.expect\(|panic!\(" src/ --type rust -n | \
  grep -v "^tests/" | \
  grep -v "^src/bin/" | \
  grep -v "// Safe:"
```

#### Error Handling Anti-Patterns
```bash
# Check for anyhow::anyhow! (FORBIDDEN per CLAUDE.md)
rg "anyhow::anyhow!|\\banyhow!\(" src/ --type rust -n

# Verify structured error types
rg "#\[derive.*thiserror::Error" src/ --type rust -A 5 | head -30
```

#### Algorithm DI Validation
```bash
# Detect hardcoded algorithm formulas
python3 scripts/parse-validation-patterns.py \
  scripts/validation-patterns.toml algorithm_di_patterns

# Verify enum-based algorithm dispatch
rg "pub enum.*Algorithm" src/intelligence/algorithms/ --type rust -A 10
```

#### Resource Management
```bash
# Check for direct resource creation (should use DI)
rg "AuthManager::new|OAuthManager::new|TenantOAuthManager::new" src/ --type rust -n | \
  grep -v "^tests/" | \
  grep -v "^src/bin/"

# Check for fake ServerResources (test-only pattern)
rg "Arc::new\(ServerResources" src/ --type rust -n | \
  grep -v "^tests/"
```

#### Unsafe Code Policy
```bash
# ZERO tolerance for unsafe (except approved locations)
rg "unsafe " src/ --type rust -n | \
  grep -v "^src/health.rs" && \
  echo "❌ Unauthorized unsafe code!" || \
  echo "✓ Unsafe code properly isolated"
```

## Validation Categories

### 1. Placeholder Detection
Catches incomplete implementations:
```rust
// ❌ FORBIDDEN patterns
"Implementation would..."
"TODO: Implementation"
"stub implementation"
"placeholder implementation"
unimplemented!()
todo!()
```

### 2. Error Handling
Enforces proper error handling:
```rust
// ❌ FORBIDDEN
.unwrap()  // except tests/bins with "// Safe:"
.expect()  // except tests/bins with "// Safe:"
panic!()   // except tests only
anyhow::anyhow!()  // ZERO TOLERANCE

// ✅ REQUIRED
Result<T, E>
AppError or specific error types
thiserror::Error enums
```

### 3. Algorithm Isolation
Ensures formulas in algorithm modules:
```rust
// ❌ FORBIDDEN (hardcoded formula outside algorithms/)
let max_hr = 220.0 - age;  // In random module

// ✅ CORRECT (enum-based DI)
let max_hr = MaxHrAlgorithm::Fox.calculate(age)?;  // In algorithms/maxhr.rs
```

### 4. Architectural Patterns
Validates design patterns:
```rust
// ❌ FORBIDDEN (direct resource creation)
let auth = AuthManager::new(config);  // Should use DI

// ✅ CORRECT (dependency injection)
pub struct MyService {
    resources: Arc<ServerResources>,  // Contains auth_manager
}
```

### 5. Code Quality
Checks for anti-patterns:
```rust
// ❌ String allocation anti-patterns
.to_string().as_str()  // Unnecessary round-trip
String::from("text").as_str()

// ✅ Use &str directly
"text"

// ❌ Iterator anti-patterns
let mut vec = Vec::new();
for item in items {
    vec.push(process(item));
}

// ✅ Use functional style
let vec: Vec<_> = items.iter().map(process).collect();
```

## Pattern Validation Results

### Expected Output (Success)
```
✓ No placeholder implementations found
✓ No unwrap/expect/panic in production code
✓ No anyhow::anyhow! usage (using structured errors)
✓ Algorithm formulas properly isolated
✓ Resource creation uses dependency injection
✓ Unsafe code limited to approved files
✓ No development artifacts (TODO/FIXME)
✓ Clone usage within threshold (600 max)

ARCHITECTURAL VALIDATION: PASSED
```

### Failure Example
```
❌ Found 3 placeholder implementations:
  src/new_feature.rs:45: "stub implementation"
  src/new_feature.rs:67: "TODO: Implementation"

❌ Found 2 unwrap() calls in production:
  src/routes/new_endpoint.rs:123: .unwrap()
  src/services/processor.rs:89: .unwrap()

❌ Found 1 anyhow::anyhow! usage (FORBIDDEN):
  src/error_handler.rs:56: anyhow::anyhow!("Error")

❌ Found hardcoded formula:
  src/intelligence/new_module.rs:34: 220.0 - age

ARCHITECTURAL VALIDATION: FAILED
```

## Success Criteria
- ✅ Zero placeholder implementations
- ✅ Zero unwrap/expect/panic in src/ (except approved)
- ✅ Zero anyhow::anyhow! usage
- ✅ All algorithms use enum-based DI
- ✅ All resources use dependency injection
- ✅ Unsafe code only in approved files (src/health.rs)
- ✅ Clone count under threshold (600)
- ✅ No hardcoded secrets
- ✅ No development artifacts (TODO/FIXME) in src/

## Related Files
- `scripts/architectural-validation.sh` - Main validation script
- `scripts/validation-patterns.toml` - Pattern definitions (539 lines)
- `scripts/parse-validation-patterns.py` - Pattern parser
- `docs/tutorial/appendix-b-claude-md.md` - CLAUDE.md standards

## Related Skills
- `strict-clippy-check` - Code quality linting
- `check-no-secrets` - Secret detection
- `test-multitenant-isolation` - Security validation
