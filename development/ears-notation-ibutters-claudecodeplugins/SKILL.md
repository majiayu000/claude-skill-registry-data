---
name: EARS Notation
description: This skill should be used when the user asks about "EARS syntax", "EARS notation", "acceptance criteria format", "SHALL patterns", "formal requirements", "WHEN THE SHALL", or needs guidance on writing testable requirements using EARS (Easy Approach to Requirements Syntax).
version: 1.0.0
---

# EARS Notation for Requirements Engineering

EARS (Easy Approach to Requirements Syntax) is a formal notation for writing unambiguous, testable acceptance criteria.

## Core Principle

Every acceptance criterion follows a strict pattern with uppercase keywords. The keyword **SHALL** is mandatory - never use "should", "must", "will", "can", or "may".

## The Six EARS Patterns

### 1. Ubiquitous (Always True)
```
THE [System] SHALL [behavior]
```
Use for requirements that are always active, with no preconditions.

**Example:** THE System SHALL encrypt all passwords using bcrypt

### 2. Event-Driven (Triggered by Action)
```
WHEN [event] THE [System] SHALL [response]
```
Use when a specific trigger causes behavior.

**Example:** WHEN a user submits the login form THE System SHALL validate credentials

### 3. State-Driven (Ongoing Condition)
```
WHILE [state] THE [System] SHALL [behavior]
```
Use for behavior that continues as long as a condition is true.

**Example:** WHILE the user is authenticated THE System SHALL display the dashboard

### 4. Optional Feature
```
WHERE [feature is present] THE [System] SHALL [behavior]
```
Use for behavior dependent on a feature flag or configuration.

**Example:** WHERE two-factor authentication is enabled THE System SHALL require a verification code

### 5. Error Handling / Unwanted Behavior
```
IF [condition] THEN THE [System] SHALL [response]
```
Use for error cases, edge cases, and exception handling.

**Example:** IF the password is incorrect THEN THE System SHALL display an error message

### 6. Complex (Combined Conditions)
```
WHILE [state] WHEN [event] THE [System] SHALL [response]
```
Use when both a state and an event trigger behavior.

**Example:** WHILE the cart is not empty WHEN the user clicks checkout THE System SHALL navigate to payment

## Strict Rules

1. **Keywords MUST be UPPERCASE**: WHEN, THE, SHALL, IF, THEN, WHILE, WHERE
2. **Always use "THE [System]"** - never lowercase "the system"
3. **Only use SHALL** - reject "should", "must", "will", "can", "may"
4. **Be specific** - avoid vague terms like "appropriate", "quickly", "properly"
5. **Make it testable** - each criterion should be verifiable

## Pattern Selection Guide

| Scenario | Pattern | Keywords |
|----------|---------|----------|
| Always happens | Ubiquitous | THE...SHALL |
| User action triggers | Event-Driven | WHEN...THE...SHALL |
| During a state | State-Driven | WHILE...THE...SHALL |
| Feature-dependent | Optional | WHERE...THE...SHALL |
| Error/edge case | Error Handling | IF...THEN THE...SHALL |
| State + action | Complex | WHILE...WHEN...THE...SHALL |

## Common Mistakes

| Wrong | Right |
|-------|-------|
| "The system should..." | "THE System SHALL..." |
| "When clicking..." | "WHEN the user clicks... THE System SHALL..." |
| "Must validate..." | "THE System SHALL validate..." |
| "Handle errors appropriately" | "IF validation fails THEN THE System SHALL display..." |

## Additional Resources

For detailed patterns and examples:
- **`references/patterns.md`** - Comprehensive pattern documentation with edge cases
- **`examples/good-requirements.md`** - Complete example requirements document

## Validation

To validate EARS syntax, use the ears-validator script:
```bash
node scripts/ears-validator.js .specs/<feature>/requirements.md
```
