---
name: documentation
description: Generate and update technical documentation
phases: [P, C]
---

# Documentation Generator

## When to Use
Use this skill when writing or updating documentation.

## Documentation Types

### 1. API Documentation
- Endpoint description
- Request/response examples
- Error codes
- Authentication requirements

### 2. README
- Project overview
- Installation steps
- Quick start guide
- Configuration options

### 3. Architecture Docs
- System overview
- Component diagram
- Data flow
- Decision records

### 4. Code Comments
- Why, not what
- Complex algorithm explanations
- Public API documentation

## Format Guidelines
- Use clear headings hierarchy
- Include code examples
- Add diagrams where helpful
- Keep it up to date with code

## Template: Function Documentation
```typescript
/**
 * Brief description of what the function does.
 *
 * @param paramName - Description of parameter
 * @returns Description of return value
 * @throws ErrorType - When this error occurs
 *
 * @example
 * const result = functionName(arg);
 */
```