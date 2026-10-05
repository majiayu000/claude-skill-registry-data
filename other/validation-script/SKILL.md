---
name: validation-script
description: Validation scripts and automated checking tools. Use when running automated validation or understanding quality checks.
---

# Validation Script

Quick validation script to check all gates after operation implementation.

## Usage

```bash
# Make script executable
chmod +x validate-operation.sh

# Run validation
./validate-operation.sh
```

## Script Content

Save this as `validate-operation.sh` in module root:

```bash
#!/bin/bash
# validate-operation.sh
# Validates that an operation meets all quality gates

echo "🚦 Validating operation completion..."

FAILED=0

# Gate 1: API Spec
echo "Checking Gate 1: API Specification..."

if grep -E "describe[A-Z]" api.yml > /dev/null 2>&1; then
  echo "❌ Gate 1 FAILED: 'describe' found in api.yml"
  FAILED=1
fi

if grep "nullable:" api.yml > /dev/null 2>&1; then
  echo "❌ Gate 1 FAILED: 'nullable' found in api.yml"
  FAILED=1
fi

# Check for schema context separation issues
nested_schemas=$(yq eval '.components.schemas[] | .. | select(type == "string" and test("#/components/schemas/")) | capture("#/components/schemas/(?<schema>.+)").schema' api.yml 2>/dev/null | sort -u)
endpoint_schemas=$(yq eval '.paths.*.*.responses.*.content.*.schema["$ref"]' api.yml 2>/dev/null | grep -o '[^/]*$' | sort -u)
for schema in $nested_schemas; do
  if echo "$endpoint_schemas" | grep -q "^${schema}$"; then
    prop_count=$(yq eval ".components.schemas.${schema}.properties | length" api.yml 2>/dev/null)
    if [ "$prop_count" -gt 10 ] 2>/dev/null; then
      echo "⚠️  WARNING: Schema '${schema}' used in BOTH nested and direct contexts with ${prop_count} properties"
      echo "   Consider creating '${schema}Summary' for nested usage (see api-specification.md Rule #19)"
    fi
  fi
done

# Gate 2: Generation
echo "Checking Gate 2: Type Generation..."

if [ ! -d "generated" ]; then
  echo "❌ Gate 2 FAILED: No generated directory"
  FAILED=1
fi

# Gate 3: Implementation
echo "Checking Gate 3: Implementation..."

if grep "Promise<any>" src/*.ts > /dev/null 2>&1; then
  echo "❌ Gate 3 FAILED: Promise<any> found"
  FAILED=1
fi

# Gate 4: Tests exist
echo "Checking Gate 4: Test Creation..."

if ! find test -name "*Test.ts" | grep -q .; then
  echo "❌ Gate 4 FAILED: No test files"
  FAILED=1
fi

# Gate 4b: No hardcoded test values in e2e tests
if [ -d "test/e2e" ]; then
  if grep -E "(const|let|var) [a-zA-Z]*[Ii]d = ['\"][0-9]+['\"]" test/e2e/*.test.ts > /dev/null 2>&1; then
    echo "❌ Gate 4 FAILED: Hardcoded test values in e2e tests"
    echo "   All test values must be in .env and imported from Common.ts"
    FAILED=1
  fi
fi

# Gate 5: Tests pass
echo "Checking Gate 5: Test Execution..."

if ! zbb test --slot local > /dev/null 2>&1; then
  echo "❌ Gate 5 FAILED: Unit tests failing (zbb test --slot local)"
  FAILED=1
fi

if ! zbb testDirect --slot local > /dev/null 2>&1; then
  echo "❌ Gate 5 FAILED: e2e direct tests failing (zbb testDirect --slot local)"
  FAILED=1
fi

# Gate 6: Build passes
echo "Checking Gate 6: Build..."

if ! zbb build > /dev/null 2>&1; then
  echo "❌ Gate 6 FAILED: Build failing"
  FAILED=1
fi

# Gate 6b: Lockfile + gate stamp present, shrinkwrap absent
if [ ! -f "package-lock.json" ]; then
  echo "❌ Gate 6 FAILED: package-lock.json not present (CI uses npm ci against this file)"
  FAILED=1
fi

if [ -f "npm-shrinkwrap.json" ]; then
  echo "❌ Gate 6 FAILED: npm-shrinkwrap.json is forbidden — delete it"
  FAILED=1
fi

if [ ! -f "gate-stamp.json" ]; then
  echo "❌ Gate 6 FAILED: gate-stamp.json missing — run \`zbb gate\` and commit the stamp"
  FAILED=1
fi

# Final result
if [ $FAILED -eq 0 ]; then
  echo ""
  echo "✅ ALL GATES PASSED - Operation complete!"
  exit 0
else
  echo ""
  echo "🚨 VALIDATION FAILED - Fix issues and re-validate"
  exit 1
fi
```

## Example Output (Success)

```
🚦 Validating operation completion...
Checking Gate 1: API Specification...
Checking Gate 2: Type Generation...
Checking Gate 3: Implementation...
Checking Gate 4: Test Creation...
Checking Gate 5: Test Execution...
Checking Gate 6: Build...

✅ ALL GATES PASSED - Operation complete!
```

## Example Output (Failure)

```
🚦 Validating operation completion...
Checking Gate 1: API Specification...
❌ Gate 1 FAILED: 'describe' found in api.yml
Checking Gate 2: Type Generation...
Checking Gate 3: Implementation...
❌ Gate 3 FAILED: Promise<any> found
Checking Gate 4: Test Creation...
Checking Gate 5: Test Execution...
❌ Gate 5 FAILED: Tests failing
Checking Gate 6: Build...

🚨 VALIDATION FAILED - Fix issues and re-validate
```

## Integration with Agents

Agents can reference this script in their validation steps:

```markdown
## Validation

Run the validation script to verify all gates:

```bash
./validate-operation.sh
```

If validation fails, fix issues and re-run.
```

## Manual Gate Checks

If validation script not available, manually verify each gate using the bash commands documented in:
- @.claude/skills/gate-api-spec/SKILL.md
- @.claude/skills/gate-type-generation/SKILL.md
- @.claude/skills/gate-implementation/SKILL.md
- @.claude/skills/gate-unit-tests/SKILL.md
- @.claude/skills/gate-test-execution/SKILL.md
- @.claude/skills/gate-build/SKILL.md
