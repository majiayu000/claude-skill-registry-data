---
name: fix-rubocop
description: Fixes RuboCop offenses systematically and safely. Use when the user wants to reduce RuboCop warnings, clean up .rubocop_todo.yml, fix linting errors, or improve code style compliance.
allowed-tools: [Bash, Read, Edit, Grep]
---

# Fix RuboCop Violations Skill

Assists with systematically reducing RuboCop offenses while preserving behavior and keeping changes focused.

**IMPORTANT: When using this skill, announce to the user**: "Using fix-rubocop skill to fix RuboCop violations systematically."

## Goals

- **Keep changes minimal and behavior-preserving**: Prefer small, focused changes
- **Use safe autocorrect first**: Apply unsafe corrections only when reviewed and covered by tests
- **Centralize rule changes in `.rubocop.yml`**: Never hand-edit `.rubocop_todo.yml`
- **No inline disables**: This project forbids `# rubocop:disable` comments

## Quick Reference Commands

```bash
# Full lint check
rake rubocop

# Lint specific file or directory
bundle exec rubocop path/to/file.rb

# Safe autocorrect (recommended first step)
bundle exec rubocop -a path/to/file.rb

# Unsafe autocorrect for specific cop (use with caution)
bundle exec rubocop -A --only Cop/Name path/to/file.rb

# Run tests to verify no behavior changes
rake spec

# Regenerate .rubocop_todo.yml after fixes
bundle exec docquet regenerate-todo
```

## Complete Workflow

### Step 1: Reproduce and Identify Offenses

```bash
# Run full lint to see all offenses
rake rubocop

# Note the failing cops and affected files
# Example output:
# lib/foxtail/formatter.rb:15:3: C: Style/StringLiterals: ...
```

**Identify the scope**:
- Which cop(s) are failing?
- Which file(s) are affected?
- How many offenses?

### Step 2: Safe Autocorrect First

Start with the safest approach - automatic fixes that preserve behavior:

```bash
# Target specific files to reduce blast radius
bundle exec rubocop -a lib/foxtail/specific_file.rb

# Or target a directory
bundle exec rubocop -a lib/foxtail/

# Verify no new failures
rake rubocop

# CRITICAL: Verify tests still pass
rake spec
```

**If tests fail after autocorrect**:
- Revert changes: `git checkout lib/foxtail/specific_file.rb`
- Proceed to Step 3 for manual fixes

### Step 3: Target Specific Cops (If Still Failing)

For remaining offenses, fix specific cops one at a time:

```bash
# For stylistic issues
bundle exec rubocop -A --only Style/StringLiterals lib/foxtail/

# For performance issues (manual review recommended)
bundle exec rubocop --only Performance/MapCompact lib/foxtail/
# Review and fix manually based on suggestions

# Verify after each cop
rake rubocop
rake spec
```

**Important**: For logic-sensitive cops (Performance, Lint), prefer manual fixes with test verification.

### Step 3a: Fixing Cops Disabled in .rubocop_todo.yml

If a cop is disabled in `.rubocop_todo.yml`, you must temporarily enable it:

```bash
# 1. Check if cop is in TODO file
grep -A 5 "Cop/Name" .rubocop_todo.yml

# 2. Temporarily comment out that cop's block in .rubocop_todo.yml
# (RuboCop respects TODO disables even with --only)

# 3. Run targeted fix
bundle exec rubocop --only Cop/Name path/to/file.rb
# or with autocorrect:
bundle exec rubocop -A --only Cop/Name path/to/file.rb

# 4. Validate changes
rake rubocop
rake spec

# 5. Regenerate TODO file (removes fixed cops automatically)
bundle exec docquet regenerate-todo

# 6. Commit code changes AND regenerated .rubocop_todo.yml together
```

**CRITICAL**: Always use `docquet regenerate-todo` to update the TODO file. Never edit it manually.

### Step 4: Update Configuration (Rare)

If a rule conflicts with project style:

```bash
# Edit .rubocop.yml to adjust the rule
# Add clear comment explaining the rationale
```

Example in `.rubocop.yml`:
```yaml
# We prefer double quotes for consistency with string interpolation
Style/StringLiterals:
  EnforcedStyle: double_quotes
```

**After configuration changes**:
```bash
# Regenerate TODO to reflect new config
bundle exec docquet regenerate-todo

# Verify
rake rubocop
```

### Step 5: No Inline Disables

**FORBIDDEN**:
```ruby
# ❌ NEVER do this
def some_method
  # rubocop:disable Style/SomeCop
  code_here
  # rubocop:enable Style/SomeCop
end
```

**If a finding cannot be safely fixed**:
1. Ask the user for guidance
2. Options:
   - Refine the rule in `.rubocop.yml`
   - Adjust the code approach
   - Document why this specific pattern is needed

### Step 6: Validate and Commit

```bash
# Ensure everything is clean
rake

# Should show:
# - All tests passing
# - No RuboCop offenses (or reduced offenses)
```

**Commit message format**:
```bash
cat > /tmp/commit_msg.txt <<'EOF'
:police_officer: Fix Style/StringLiterals violations in lib/foxtail

Convert single quotes to double quotes for consistency.
EOF

git commit -F /tmp/commit_msg.txt
rm /tmp/commit_msg.txt
```

**Commit message patterns**:
- `:police_officer:` - All RuboCop fixes (style, lint, performance)
- `:wrench:` - Update RuboCop configuration

## Common Scenarios

### Scenario 1: Reduce .rubocop_todo.yml Violations

```bash
# 1. Check current state
cat .rubocop_todo.yml
# Note: List of disabled cops and offense counts

# 2. Pick one cop to fix (start with lowest count)
# Example: Style/CommentedKeyword (1 offense)

# 3. Find affected files
bundle exec rubocop --only Style/CommentedKeyword

# 4. Apply fix
bundle exec rubocop -A --only Style/CommentedKeyword lib/foxtail/

# 5. Verify
rake spec
rake rubocop

# 6. Regenerate TODO
bundle exec docquet regenerate-todo
# The fixed cop should be removed automatically

# 7. Commit
git add .
git commit -m ":police_officer: Fix Style/CommentedKeyword violations"
```

### Scenario 2: Fix All Offenses in One File

```bash
# 1. Target specific file
bundle exec rubocop lib/foxtail/date_time_format.rb

# 2. Safe autocorrect first
bundle exec rubocop -a lib/foxtail/date_time_format.rb

# 3. Check remaining offenses
bundle exec rubocop lib/foxtail/date_time_format.rb

# 4. Fix remaining manually or with targeted cops
bundle exec rubocop -A --only Naming/VariableNumber lib/foxtail/date_time_format.rb

# 5. Verify
rake spec

# 6. If cop was in TODO, regenerate
bundle exec docquet regenerate-todo

# 7. Commit
git commit -m ":police_officer: Fix all RuboCop violations in date_time_format.rb"
```

### Scenario 3: Fix Specific Cop Across Entire Codebase

```bash
# 1. Check scope
bundle exec rubocop --only Style/StringLiterals
# Shows all files and offense counts

# 2. Start with smallest files or directories
bundle exec rubocop -A --only Style/StringLiterals lib/foxtail/helpers/

# 3. Verify incrementally
rake spec
git add lib/foxtail/helpers/
git commit -m ":police_officer: Fix Style/StringLiterals in helpers"

# 4. Continue with other directories
bundle exec rubocop -A --only Style/StringLiterals lib/foxtail/models/
rake spec
git commit -m ":police_officer: Fix Style/StringLiterals in models"

# 5. Final regenerate
bundle exec docquet regenerate-todo
git commit -m ":wrench: Regenerate RuboCop TODO after fixes"
```

## Examples by Cop Type

### Style Cops (Usually Safe)

```bash
# String literals
bundle exec rubocop -A --only Style/StringLiterals lib/

# Hash syntax
bundle exec rubocop -A --only Style/HashSyntax lib/

# Frozen string literals
bundle exec rubocop -A --only Style/FrozenStringLiteralComment lib/
```

### Naming Cops (May Need Review)

```bash
# Variable naming
bundle exec rubocop -A --only Naming/VariableNumber lib/foxtail/file.rb

# Method naming (often requires manual decision)
bundle exec rubocop --only Naming/PredicateMethod lib/foxtail/file.rb
# Review output and fix manually:
# - Either rename method to end with ?
# - Or document why it shouldn't be a predicate
```

### Lint Cops (Require Careful Review)

```bash
# Unused variables (manual fix recommended)
bundle exec rubocop --only Lint/UnusedMethodArgument lib/
# Review each and either use or prefix with _

# Verify with tests
rake spec
```

### Performance Cops (Test Thoroughly)

```bash
# Performance improvements (review before applying)
bundle exec rubocop --only Performance/MapCompact lib/
# Apply manually to ensure behavior preservation

# ALWAYS run full test suite
rake spec
```

## Common Pitfalls to Avoid

1. **Don't run unsafe autocorrect on entire codebase**: Use `-A` on small scopes only
2. **Don't skip test verification**: Always run `rake spec` after fixes
3. **Don't manually edit .rubocop_todo.yml**: Always use `docquet regenerate-todo`
4. **Don't use inline disables**: This project forbids `# rubocop:disable` comments
5. **Don't commit without regenerating TODO**: If fixing TODO cops, always regenerate
6. **Don't mix unrelated fixes**: Keep commits focused on one cop or one area
7. **Don't ignore test failures**: Revert and fix manually if tests fail after autocorrect

## Troubleshooting

### Issue: Cop not showing offenses despite being in .rubocop_todo.yml

**Problem**: Cop is disabled in TODO file

**Solution**:
```bash
# Temporarily comment out the cop in .rubocop_todo.yml
# Then run:
bundle exec rubocop --only Cop/Name

# After fixing, regenerate TODO
bundle exec docquet regenerate-todo
```

### Issue: Tests fail after autocorrect

**Problem**: Unsafe autocorrect changed behavior

**Solution**:
```bash
# Revert changes
git checkout path/to/file.rb

# Fix manually or use safer approach
bundle exec rubocop --only Cop/Name path/to/file.rb
# Review suggestions and fix by hand

# Verify each change
rake spec
```

### Issue: docquet regenerate-todo not working

**Problem**: Command not found or gem not installed

**Solution**:
```bash
# Ensure bundler is up to date
bundle install

# Check if docquet is installed
bundle exec docquet --version

# If not, check Gemfile and install dependencies
```

### Issue: Too many offenses to fix at once

**Problem**: Overwhelming number of violations

**Solution**:
1. Pick ONE cop type to fix
2. Start with lowest offense count
3. Fix incrementally, one file/directory at a time
4. Commit after each successful fix
5. Use PR per cop type or per area

## PR Guidance

**Keep changes small and single-purpose**:
- Good: "Fix Style/StringLiterals in lib/foxtail/formatters"
- Bad: "Fix multiple RuboCop issues across codebase"

**Include context in PR body**:
```markdown
## Summary
Fix Style/StringLiterals violations in formatter classes

## Changes
- Convert single quotes to double quotes in 5 files
- Applied safe autocorrect (-a flag)

## Verification
- All tests pass (rake spec)
- RuboCop clean for these files
- Regenerated .rubocop_todo.yml
```

**Link rule changes to rationale**:
If updating `.rubocop.yml`, explain why in PR description.

## Best Practices

1. **Start with safe autocorrect**: Use `-a` before `-A`
2. **Small, focused PRs**: One cop type or one directory at a time
3. **Test after every change**: Run `rake spec` frequently
4. **Regenerate TODO incrementally**: After fixing each cop type
5. **Commit incrementally**: Don't wait to fix everything before committing
6. **Document decisions**: If excluding a cop, explain why in `.rubocop.yml`
7. **Review Performance/Lint changes**: Don't blindly autocorrect these
8. **Keep blast radius small**: Target specific files/directories when possible
