---
name: "Code Quality Gates"
description: "Comprehensive code quality validation using Solargraph, Sorbet, and Rubocop for A+ Rails code. Trigger keywords: quality gates, validation, solargraph, sorbet, rubocop, type checking, linting, code quality, static analysis"
version: 1.0.0
---

# Code Quality Gates

This skill provides patterns for comprehensive code quality validation using three complementary tools: Solargraph (LSP diagnostics), Sorbet (type checking), and Rubocop (style enforcement).

## 1. Tool Stack Overview

### Solargraph (Ruby LSP)

**Purpose**: Language server providing IDE-like features and diagnostics

**Setup**:
```bash
gem install solargraph
solargraph config  # Generates .solargraph.yml
```

**Key Features**:
- Method completion and documentation
- Go to definition/references
- Hover information
- Diagnostics (undefined methods, type errors)
- Integration with cclsp MCP

**Diagnostics Patterns**:
- Undefined methods: `NoMethodError` detection
- Unresolved constants: Missing class/module references
- Parameter count mismatches: Wrong arity
- Unused variables: Dead code detection

**cclsp Integration**:
```ruby
# Agents use cclsp MCP tools
mcp__cclsp__get_diagnostics file_path="app/models/user.rb"
# Returns: errors, warnings, hints for the file
```

**Configuration** (`.solargraph.yml`):
```yaml
include:
  - "**/*.rb"
exclude:
  - spec/**/*
  - test/**/*
  - vendor/**/*
reporters:
  - rubocop
  - require_not_found
plugins: []
require_paths: []
domains: []
max_files: 5000
```

---

## 2. Sorbet (Type Checking)

**Purpose**: Static type checker for Ruby with gradual typing

**Setup**:
```bash
# Add to Gemfile
gem 'sorbet'
gem 'sorbet-runtime'

# Initialize
bundle exec srb init

# Generate RBI files for gems
bundle exec tapioca init
bundle exec tapioca gems
```

### Type Sigils

Gradual adoption through file-level type checking levels:

```ruby
# typed: ignore   # Skip this file entirely
# typed: false    # Only check syntax errors
# typed: true     # Check types, infer missing signatures
# typed: strict   # Require explicit signatures
# typed: strong   # No T.untyped allowed
```

### Common Patterns

**Basic Signature**:
```ruby
sig { params(name: String).returns(User) }
def find_by_name(name)
  User.where(name: name).first
end
```

**Void Methods**:
```ruby
sig { params(user: User).void }
def send_notification(user)
  Mailer.deliver(user.email)
end
```

**Nilable Types**:
```ruby
sig { params(id: Integer).returns(T.nilable(User)) }
def find_user(id)
  User.find_by(id: id)  # May return nil
end
```

**Arrays and Hashes**:
```ruby
sig { params(items: T::Array[String]).returns(T::Hash[String, Integer]) }
def count_items(items)
  items.tally
end
```

**Class Methods**:
```ruby
class << self
  sig { returns(T::Array[User]) }
  def active_users
    where(active: true).to_a
  end
end
```

---

## 3. Rubocop (Style Enforcement)

**Purpose**: Ruby static code analyzer and formatter

**Setup**:
```bash
gem install rubocop
rubocop --init  # Generates .rubocop.yml
```

### Auto-fix Strategy

```bash
# Fix safe offenses automatically
rubocop -a

# Fix all offenses (use with caution)
rubocop -A

# Fix specific file
rubocop -a app/models/user.rb

# Check without fixing
rubocop --fail-level error --format simple app/models/user.rb
```

### Common Violations

**Line Length** (default: 120):
```ruby
# Bad
def very_long_method_name_that_exceeds_the_maximum_allowed_line_length_for_ruby_code_according_to_rubocop_standards

# Good
def descriptive_method_name
  # Implementation
end
```

**Frozen String Literal**:
```ruby
# Add to top of file
# frozen_string_literal: true
```

**Inconsistent Indentation**:
```ruby
# Bad
def method
 puts "inconsistent"
  puts "indentation"
end

# Good
def method
  puts "consistent"
  puts "indentation"
end
```

**Trailing Whitespace**:
```ruby
# Bad
def method
  puts "hello"
end

# Good
def method
  puts "hello"
end
```

### Configuration (`.rubocop.yml`):
```yaml
AllCops:
  TargetRubyVersion: 3.2
  NewCops: enable
  Exclude:
    - 'db/schema.rb'
    - 'vendor/**/*'
    - 'node_modules/**/*'

Layout/LineLength:
  Max: 120

Style/Documentation:
  Enabled: false  # Allow missing class docs

Metrics/MethodLength:
  Max: 20

Metrics/AbcSize:
  Max: 20
```

---

## 4. Validation Strategy

### Phase 4 Quality Gate

Runs after each implementation layer (models, services, components):

**validate-implementation.sh Workflow**:

1. **Check Tool Availability**
   ```bash
   check_tool_available solargraph  # → true/false
   check_tool_available sorbet       # → true/false
   check_tool_available rubocop      # → true/false
   ```

2. **Solargraph Diagnostics**
   ```bash
   for file in $FILES; do
     solargraph check "$file"  # Get diagnostics
     # Check for errors
   done
   ```

3. **Sorbet Type Check** (typed files only)
   ```bash
   # Filter to typed files
   typed_files=$(grep -l "# typed:" $FILES)

   # Run type check
   bundle exec srb tc $typed_files
   ```

4. **Rubocop Style Check**
   ```bash
   # Fail on warnings (blocking mode)
   rubocop --fail-level warning --format simple $FILES
   ```

5. **Exit Based on Validation Level**
   - **blocking**: Exit 1 if any fail (prevents progress)
   - **warning**: Exit 2 if any fail (alerts but allows)
   - **advisory**: Exit 0 always (informational)

---

## 5. Guardian Cycle

Runs after Phase 4 for comprehensive type safety:

**guardian-validation.sh Workflow**:

1. **Collect Modified Files**
   ```bash
   FILES=$(bd show $FEATURE_ID | grep -oE "app/[a-z_/]+\.rb")
   ```

2. **Run Sorbet Type Check**
   ```bash
   bundle exec srb tc $FILES
   ```

3. **Analyze Errors** (if any)
   - Missing signatures
   - Type mismatches
   - Undefined methods
   - T.untyped violations

4. **Attempt Auto-Fix** (simple cases)
   ```ruby
   # Add default signature
   sig { returns(T.untyped) }
   def method_name
     # ...
   end
   ```

5. **Re-validate** (max 3 iterations)
   - Run srb tc again
   - Check if errors resolved
   - Log remaining issues

6. **Block or Pass**
   - Exit 0 if all pass
   - Exit 1 if errors remain after max iterations

---

## 6. Tool Integration Patterns

### Pre-Edit Validation

**Hook**: PreToolUse (before Edit tool)

```bash
# Check syntax before applying edit
echo "$NEW_CONTENT" | ruby -c

# If typed file, warn about Sorbet validation
if grep -q "# typed:" "$FILE_PATH"; then
  echo "ℹ️  Sorbet validation will run post-edit"
fi
```

### Post-Write Validation

**Hook**: PostToolUse (after Write tool)

```bash
# Syntax check (always)
ruby -c "$FILE_PATH"

# Rubocop (if available)
rubocop --fail-level error "$FILE_PATH"

# Sorbet (if typed)
if grep -q "# typed:" "$FILE_PATH"; then
  bundle exec srb tc "$FILE_PATH"
fi
```

---

## 7. Error Messages and Fixes

### Solargraph Errors

**Undefined Method**:
```
Error: Method 'email' is not defined on User

Fix: Define the method or add to class
def email
  # ...
end
```

**Unresolved Constant**:
```
Error: Constant 'PaymentService' not found

Fix: Require the file or fix namespace
require_relative 'payment_service'
```

### Sorbet Errors

**Missing Signature**:
```
Error: Method does not have a `sig`

Fix:
sig { params(name: String).returns(User) }
def find_by_name(name)
  # ...
end
```

**Type Mismatch**:
```
Error: Expected String but found Integer

Fix: Convert type or update signature
name.to_s  # Convert Integer to String
```

**Undefined Method on Typed Value**:
```
Error: Method `email` does not exist on `T.untyped`

Fix: Add type annotation
sig { params(user: User).void }  # Now user has type
def send_email(user)
  user.email  # Safe - user is typed as User
end
```

### Rubocop Violations

**Style/FrozenStringLiteralComment**:
```
Fix: Add to top of file
# frozen_string_literal: true
```

**Layout/LineLength**:
```
Fix: Break long lines
# Bad
very_long_method_call_with_many_parameters(param1, param2, param3, param4)

# Good
very_long_method_call_with_many_parameters(
  param1,
  param2,
  param3,
  param4
)
```

---

## 8. Best Practices

### Gradual Adoption

**Phase 1**: Start with Rubocop
```yaml
# .rubocop.yml - relaxed rules
Metrics/MethodLength:
  Max: 30  # Increase limits initially
```

**Phase 2**: Add Solargraph for diagnostics
```bash
solargraph check app/models/*.rb  # Check specific directories
```

**Phase 3**: Introduce Sorbet with `# typed: false`
```ruby
# typed: false  # Minimal checking
class User
  # No signatures required yet
end
```

**Phase 4**: Gradually upgrade to `# typed: true`
```ruby
# typed: true  # Type inference enabled
class User
  sig { params(name: String).returns(User) }  # Add signatures
  def self.find_by_name(name)
    # ...
  end
end
```

### File-by-File Strategy

Focus on new files first:
```
New files → # typed: true (type-safe from start)
Old files → # typed: false (legacy, upgrade gradually)
Core files → # typed: strict (critical paths)
```

### Continuous Integration

Run quality gates in CI:
```yaml
# .github/workflows/quality.yml
- name: Rubocop
  run: bundle exec rubocop

- name: Sorbet
  run: bundle exec srb tc

- name: Solargraph
  run: solargraph check app/**/*.rb
```

---

## 9. Configuration Templates

### .claude/reactree-rails-dev.local.md

```yaml
---
enabled: true
quality_gates_enabled: true
guardian_enabled: true
validation_level: blocking  # blocking, warning, advisory
guardian_max_iterations: 3
---
```

### .solargraph.yml

```yaml
include:
  - "**/*.rb"
exclude:
  - spec/**/*
  - test/**/*
  - vendor/**/*
  - db/schema.rb
reporters:
  - rubocop
  - require_not_found
max_files: 5000
```

### .rubocop.yml

```yaml
AllCops:
  TargetRubyVersion: 3.2
  NewCops: enable
  Exclude:
    - 'db/schema.rb'
    - 'vendor/**/*'

Layout/LineLength:
  Max: 120

Style/FrozenStringLiteralComment:
  Enabled: true
  EnforcedStyle: always
```

### sorbet/config

```
--dir
.
--ignore=/vendor/
--ignore=/tmp/
```

---

## 10. Troubleshooting

### Solargraph Not Working

```bash
# Rebuild index
solargraph clear
solargraph download-core

# Check configuration
solargraph config
```

### Sorbet Type Errors

```bash
# Regenerate RBI files
bundle exec tapioca gems

# Check Sorbet version
bundle exec srb --version

# Run with verbose output
bundle exec srb tc --verbose
```

### Rubocop False Positives

```ruby
# Disable specific cop for line
# rubocop:disable Style/FrozenStringLiteralComment
code_here
# rubocop:enable Style/FrozenStringLiteralComment

# Disable for file
# rubocop:disable all
```

---

## Summary

Code Quality Gates provide three layers of validation:

1. **Solargraph**: IDE-like diagnostics (undefined methods, constants)
2. **Sorbet**: Static type checking (type safety, signatures)
3. **Rubocop**: Style enforcement (conventions, best practices)

**Integration Points**:
- Phase 4 Quality Gates (after each layer)
- Guardian Validation Cycle (after full implementation)
- PreToolUse/PostToolUse Hooks (real-time validation)

**Gradual Adoption**:
- Start with Rubocop (easiest)
- Add Solargraph (diagnostics)
- Introduce Sorbet (type safety)
- Tighten rules over time

**Result**: A+ type-safe, well-styled Rails code with comprehensive quality validation.
