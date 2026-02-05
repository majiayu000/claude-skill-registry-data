---
name: validate-style-complete
description: Complete 3-component style validation (Checkstyle + PMD + Manual rules)
allowed-tools: Bash, Read
---

# Validate Style Complete Skill

**Purpose**: Perform complete 3-component style validation (Checkstyle + PMD + Manual rules) to prevent incomplete validation.

**Performance**: Prevents missed violations, ensures comprehensive style compliance

## When to Use This Skill

### ✅ Use validate-style-complete When:

- In VALIDATION state
- Ready to validate style compliance
- Need comprehensive style check
- Before declaring style validation complete

### ❌ Do NOT Use When:

- Still implementing features (use during development)
- Only need quick Checkstyle check
- Style already validated and no code changes
- Not a Java project (no Checkstyle/PMD)

## What This Skill Does

### 1. Runs Checkstyle

```bash
./mvnw checkstyle:check
```

### 2. Runs PMD

```bash
./mvnw pmd:check
```

### 3. Checks Manual Rules

```bash
# Reviews code-style-human.md
# Checks for TIER1/TIER2/TIER3 violations
```

### 4. Reports Results

```markdown
## Style Validation Results

### Checkstyle: ✅ PASSED
- 0 violations found

### PMD: ✅ PASSED
- 0 violations found

### Manual Rules: ✅ PASSED
- TIER1 violations: 0
- TIER2 violations: 0
- TIER3 violations: 0

**Overall**: ✅ COMPLETE STYLE VALIDATION PASSED
```

## Usage

### Basic Validation

```bash
# Complete 3-component validation
/workspace/main/.claude/scripts/validate-style-complete.sh
```

### For Specific Module

```bash
# Validate single module
MODULE="formatter"

/workspace/main/.claude/scripts/validate-style-complete.sh \
  --module "$MODULE"
```

### With Manual Rule Details

```bash
# Include detailed manual rule checks
/workspace/main/.claude/scripts/validate-style-complete.sh \
  --detailed-manual-rules true
```

## Validation Components

### Component 1: Checkstyle (Automated)

**Purpose**: Enforce code formatting and style conventions

**Checks**:
- Line length (120 chars max)
- Indentation (tabs, not spaces)
- Naming conventions (camelCase, UPPER_CASE)
- JavaDoc requirements
- Import organization
- Whitespace rules
- Modifier order

**Command**:
```bash
./mvnw checkstyle:check
```

**Output**:
```
[INFO] --- checkstyle:3.x.x:check (default-cli) ---
[INFO] There are 0 errors reported by Checkstyle
```

### Component 2: PMD (Automated)

**Purpose**: Detect code quality issues and anti-patterns

**Checks**:
- Unused code (variables, methods, imports)
- Empty code blocks
- Complexity metrics (cyclomatic complexity)
- Best practice violations
- Performance issues
- Security vulnerabilities
- Design problems

**Command**:
```bash
./mvnw pmd:check
```

**Output**:
```
[INFO] --- pmd:3.x.x:check (default-cli) ---
[INFO] PMD Failure: 0 violations found
```

### Component 3: Manual Rules (Human Review)

**Purpose**: Check rules not automatable

**Source**: `docs/code-style-human.md`

**TIER1 Violations (Critical)**:
- Incorrect JavaDoc format
- Missing public API documentation
- Improper exception handling patterns
- Violation of SOLID principles

**TIER2 Violations (Important)**:
- Inconsistent naming across related classes
- Magic numbers without explanation
- Complex boolean expressions
- Missing edge case handling

**TIER3 Violations (Minor)**:
- Overly verbose variable names
- Suboptimal code organization
- Missing helper methods

**Check Process**:
1. Read code-style-human.md
2. Review recent code changes
3. Identify any TIER1/TIER2/TIER3 violations
4. Document findings
5. Fix violations

## Complete Validation Checklist

**BEFORE declaring style validation complete, verify ALL components**:

- [ ] Checkstyle passes: `./mvnw checkstyle:check`
- [ ] PMD passes: `./mvnw pmd:check`
- [ ] Manual rules reviewed from code-style-human.md
- [ ] All TIER1 violations fixed
- [ ] All TIER2 violations fixed
- [ ] All TIER3 violations fixed or documented

## Common Mistake

### ❌ INCOMPLETE: Checkstyle Only

```bash
# Only checking Checkstyle
./mvnw checkstyle:check
# [INFO] 0 errors

Agent: "✅ Style validation complete"
# WRONG: PMD and manual rules not checked
```

### ✅ COMPLETE: All 3 Components

```bash
# Check all components
./mvnw checkstyle:check pmd:check
# [INFO] Checkstyle: 0 errors
# [INFO] PMD: 0 violations

# Review manual rules
cat docs/code-style-human.md
# Manually check for TIER1/TIER2/TIER3 violations

Agent: "✅ Complete style validation passed:
- Checkstyle: 0 violations
- PMD: 0 violations
- Manual rules: All tiers validated"
```

## Workflow Integration

### Validation Phase Flow

```markdown
VALIDATION state
  ↓
[validate-style-complete skill] ← THIS SKILL
  ↓
Run Checkstyle
  ↓
Run PMD
  ↓
Check manual rules
  ↓
If ALL PASS:
  ✅ Style validation complete
  → Continue to test validation

If ANY FAIL:
  ❌ Style violations found
  → Re-invoke formatter agent
  → Fix violations
  → Re-run validation
```

## Output Format

Script returns JSON:

```json
{
  "status": "success",
  "message": "Complete style validation passed",
  "checkstyle": {
    "passed": true,
    "violations": 0
  },
  "pmd": {
    "passed": true,
    "violations": 0
  },
  "manual_rules": {
    "reviewed": true,
    "tier1_violations": 0,
    "tier2_violations": 0,
    "tier3_violations": 0
  },
  "overall": "PASSED",
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

**Or if failures**:

```json
{
  "status": "failed",
  "message": "Style violations found",
  "checkstyle": {
    "passed": false,
    "violations": 12,
    "details": "src/main/java/Foo.java:15: Line too long"
  },
  "pmd": {
    "passed": false,
    "violations": 5,
    "details": "UnusedPrivateMethod: Method bar() is unused"
  },
  "manual_rules": {
    "reviewed": true,
    "tier1_violations": 2,
    "tier2_violations": 3,
    "tier3_violations": 1,
    "details": "TIER1: Missing JavaDoc on public API"
  },
  "overall": "FAILED",
  "total_violations": 23,
  "timestamp": "2025-11-11T12:34:56-05:00"
}
```

## Handling Violations

### Checkstyle Violations

**Common Violations**:
```
- Line too long (>120 chars)
- Tabs vs spaces (use tabs)
- Missing JavaDoc on public method
- Import order incorrect
- Whitespace at end of line
```

**Fix Strategy**:
```bash
# Run Checkstyle to identify violations
./mvnw checkstyle:check

# Fix violations systematically
# - Line length: Break long lines
# - Indentation: Use tabs consistently
# - JavaDoc: Add missing documentation
# - Imports: Reorganize with IDE

# Verify fixed
./mvnw checkstyle:check
```

### PMD Violations

**Common Violations**:
```
- UnusedPrivateMethod
- UnusedLocalVariable
- EmptyCatchBlock
- AvoidDuplicateLiterals
- CyclomaticComplexity (>10)
```

**Fix Strategy**:
```bash
# Run PMD to identify violations
./mvnw pmd:check

# Fix violations
# - Remove unused code
# - Handle exceptions properly
# - Extract constants for duplicates
# - Refactor complex methods

# Verify fixed
./mvnw pmd:check
```

### Manual Rule Violations

**TIER1 (Critical)**:
```markdown
Example: Public API missing JavaDoc

Fix:
/**
 * Validates the input according to formatting rules.
 *
 * @param input the text to validate
 * @return validation result with errors if any
 * @throws NullPointerException if input is null
 */
public ValidationResult validate(String input)
```

**TIER2 (Important)**:
```markdown
Example: Magic number without explanation

❌ BAD:
if (count > 42) {

✅ GOOD:
private static final int MAX_RETRIES = 42;
if (count > MAX_RETRIES) {
```

**TIER3 (Minor)**:
```markdown
Example: Verbose variable name

❌ VERBOSE:
String theCurrentUserInputStringValue = ...

✅ CONCISE:
String userInput = ...
```

## Safety Features

### Comprehensive Coverage

- ✅ Runs all automated tools
- ✅ Checks all manual rule tiers
- ✅ Reports all violation types
- ✅ Prevents incomplete validation

### Clear Reporting

- ✅ Separate results per component
- ✅ Violation counts per category
- ✅ Detailed violation descriptions
- ✅ Overall pass/fail status

### Error Handling

- ✅ Continues validation even if one component fails
- ✅ Reports partial results
- ✅ Identifies which component failed
- ✅ Provides fix guidance

## Related Skills

- **reinvoke-agent-fixes**: Re-invokes formatter for style violations
- **checkpoint-approval**: Style validation before user approval

## Troubleshooting

### Error: "Checkstyle passes but PMD fails"

```bash
# Both tools check different things
# Checkstyle: Formatting and conventions
# PMD: Code quality and anti-patterns

# Fix PMD violations separately
./mvnw pmd:check
# Then re-run complete validation
```

### Error: "Tools pass but manual violations exist"

```bash
# Automated tools can't catch everything
# Human review required for manual rules

# Review code-style-human.md
cat docs/code-style-human.md

# Check code against manual rules
# Fix violations
# Document any exceptions
```

### Conflicting Rules

```bash
# Sometimes Checkstyle and PMD conflict
# Example: LineLength vs UnderutilizedLines

# Resolution:
1. Check fixers module for conflict handling
2. Prioritize Checkstyle over PMD for style
3. Document exceptions in comments
4. Configure tools to align if possible
```

## Best Practices

### Run Early and Often

```bash
# ✅ GOOD: Validate incrementally
Edit Component1.java
./mvnw checkstyle:check pmd:check -q
git commit -m "Add Component1 (style validated)"

Edit Component2.java
./mvnw checkstyle:check pmd:check -q
git commit -m "Add Component2 (style validated)"

# ❌ BAD: Validate at end
Edit Component1.java
Edit Component2.java
Edit Component3.java
./mvnw checkstyle:check pmd:check
# 60 violations to fix with stale context
```

### Fix by Category

```bash
# ✅ GOOD: Fix all of one type
# Fix all 20 line-length violations
# Commit: "Fix all line length violations"

# Fix all 10 missing JavaDoc violations
# Commit: "Add missing JavaDoc to public API"

# ❌ BAD: Fix randomly
# Fix violation 1 from file A
# Fix violation 2 from file B
# Fix violation 3 from file A
# Hard to review, hard to verify
```

### Use IDE Integration

```bash
# Configure IDE with project settings
# - Checkstyle plugin
# - PMD plugin
# - Code style from checkstyle.xml

# Benefits:
# - Real-time violation detection
# - Auto-fix for many violations
# - Prevent violations before commit
```

## Implementation Notes

The validate-style-complete script performs:

1. **Checkstyle Phase**
   - Run: mvn checkstyle:check
   - Parse output
   - Count violations
   - Extract violation details

2. **PMD Phase**
   - Run: mvn pmd:check
   - Parse output
   - Count violations
   - Extract violation details

3. **Manual Rules Phase**
   - Read code-style-human.md
   - Review recent code changes
   - Check for TIER1 violations
   - Check for TIER2 violations
   - Check for TIER3 violations

4. **Aggregation Phase**
   - Combine results from all components
   - Calculate total violations
   - Determine overall status
   - Categorize by severity

5. **Reporting Phase**
   - Format results per component
   - Report overall status
   - List specific violations
   - Provide fix guidance

6. **Exit Phase**
   - Return 0 if all pass
   - Return 1 if any fail
   - Include detailed JSON output
