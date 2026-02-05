---
name: musubix-ears-validation
description: Guide for validating and creating EARS-format requirements. Use this when asked to write requirements, validate requirement syntax, or convert natural language to EARS format.
license: MIT
---

# MUSUBIX EARS Validation Skill

This skill helps you create and validate requirements using EARS (Easy Approach to Requirements Syntax) format.

## EARS Pattern Reference

### 1. Ubiquitous Pattern
**Use for**: Requirements that must always be satisfied.

**Syntax**:
```
THE [system name] SHALL [requirement]
```

**Example**:
```markdown
THE AuthService SHALL authenticate users with valid credentials.
```

### 2. Event-Driven Pattern
**Use for**: Requirements triggered by specific events.

**Syntax**:
```
WHEN [trigger event], THE [system name] SHALL [response]
```

**Example**:
```markdown
WHEN a user submits login credentials, THE AuthService SHALL validate the credentials within 2 seconds.
```

### 3. State-Driven Pattern
**Use for**: Requirements that apply while in a specific state.

**Syntax**:
```
WHILE [system state], THE [system name] SHALL [behavior]
```

**Example**:
```markdown
WHILE the system is in maintenance mode, THE API SHALL return 503 Service Unavailable.
```

### 4. Unwanted Behavior Pattern
**Use for**: Behaviors that must be prevented.

**Syntax**:
```
THE [system name] SHALL NOT [unwanted behavior]
```

**Example**:
```markdown
THE AuthService SHALL NOT store passwords in plain text.
```

### 5. Optional Pattern
**Use for**: Conditional requirements.

**Syntax**:
```
IF [condition], THEN THE [system name] SHALL [response]
```

**Example**:
```markdown
IF two-factor authentication is enabled, THEN THE AuthService SHALL require a verification code.
```

## Validation Checklist

When validating EARS requirements, check:

- [ ] **Pattern Compliance**: Does it follow one of the 5 EARS patterns?
- [ ] **System Name**: Is the system/component clearly identified?
- [ ] **SHALL Keyword**: Is "SHALL" used for mandatory requirements?
- [ ] **Measurable**: Is the requirement testable and measurable?
- [ ] **Atomic**: Does it describe a single requirement?
- [ ] **No Ambiguity**: Is the language clear and unambiguous?

## CLI Commands

```bash
# Validate EARS syntax
npx musubix requirements validate <file>

# Convert natural language to EARS
npx musubix requirements analyze <file>

# Map to ontology
npx musubix requirements map <file>
```

## Conversion Examples

### Natural Language → EARS

**Input**: "Users should be able to login"

**Output**:
```markdown
THE AuthenticationModule SHALL authenticate users with valid credentials.
```

**Input**: "Show error when password is wrong"

**Output**:
```markdown
WHEN invalid credentials are provided, THE AuthenticationModule SHALL display an error message.
```

**Input**: "Don't allow SQL injection"

**Output**:
```markdown
THE InputValidator SHALL NOT accept input containing SQL injection patterns.
```

## Priority Levels

| Priority | Description | Usage |
|----------|-------------|-------|
| **P0** | 必須 (Must Have) | Release blocker |
| **P1** | 重要 (Should Have) | Implement if possible |
| **P2** | 任意 (Nice to Have) | Time permitting |

## Requirement Document Template

```markdown
### REQ-[CATEGORY]-[NUMBER]: [Title]

**種別**: [UBIQUITOUS|EVENT-DRIVEN|STATE-DRIVEN|UNWANTED|OPTIONAL]
**優先度**: [P0|P1|P2]

**要件**:
[EARS形式の要件文]

**検証方法**: [Unit Test|Integration Test|E2E Test|Manual]
**受入基準**:
- [ ] Criterion 1
- [ ] Criterion 2

**トレーサビリティ**: DES-XXX, TEST-XXX
**憲法準拠**: Article IV (EARS Format)
```

## Common Mistakes to Avoid

1. ❌ Using "should" instead of "SHALL"
2. ❌ Combining multiple requirements in one statement
3. ❌ Vague or unmeasurable criteria
4. ❌ Missing system name
5. ❌ Using implementation details in requirements
