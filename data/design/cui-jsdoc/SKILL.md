---
name: cui-jsdoc
description: JSDoc documentation standards for JavaScript functions, classes, modules, and web components
allowed-tools:
  - Read
  - Grep
  - Glob
---

# JSDoc Documentation Standards

## Overview

Provides JSDoc documentation standards for CUI JavaScript projects covering functions, classes, modules, types, and web components.

## Standards Documents

- **jsdoc-essentials.md** - Core JSDoc syntax, required tags, ESLint setup, writing style
- **jsdoc-patterns.md** - Documentation patterns for all code element types with examples

## What This Skill Provides

### JSDoc Essentials
- ESLint plugin configuration and rules
- Documentation requirements (mandatory vs optional)
- Required and optional tags (@param, @returns, @throws, @example, @since, @see, @deprecated)
- Type annotations (basic types, unions, custom types)
- Writing style guidelines (present tense, active voice, clear language)
- Build integration (npm scripts, jsdoc.conf.json)
- Validation and common mistakes

### Documentation Patterns
- **Functions**: Simple, async, complex with nested parameters
- **Classes**: Declaration, constructor, methods, inheritance
- **Modules**: File overview, exports, constants
- **Types**: Custom types (@typedef), callbacks, union/literal types
- **Web Components**: Lit components, properties, events, CSS properties
- **Quality Examples**: Good vs bad documentation patterns

## When to Activate

Use this skill when:
- Documenting JavaScript code (functions, classes, modules)
- Building web components (Lit or vanilla custom elements)
- Setting up JSDoc and ESLint integration
- Reviewing code documentation quality
- Updating documentation after refactoring

## Workflow

1. **Identify what to document** - Check if element is mandatory (public APIs) or optional
2. **Apply appropriate pattern** - Use pattern from jsdoc-patterns.md for code element type
3. **Include required tags** - @param, @returns, @throws, @example for public functions
4. **Follow writing style** - Present tense, active voice, specific descriptions
5. **Validate** - Run ESLint to check documentation completeness

## Quick Reference

### Required for Public Functions
- Brief description
- @param (all parameters with types)
- @returns (for non-void returns)
- @throws (all possible errors)
- @example (for complex functions)

### Required for Classes
- @class tag with description
- Constructor documentation
- Public method documentation

### Required for Modules
- @fileoverview
- @module tag
- Export documentation

## Best Practices

1. Document as you code - Don't defer documentation
2. Be specific - Avoid vague descriptions
3. Document all errors - Use @throws for all exceptions
4. Provide examples - Show realistic usage
5. Keep synchronized - Update docs when code changes
6. Validate with ESLint - Run linting before commit

## Common Mistakes

- Missing @param, @returns, or @throws
- Vague descriptions ("processes data")
- Parameter names not matching function signature
- No examples for complex functions
- Outdated documentation after refactoring

## Integration

Works with:
- **cui-javascript** skill - Core JavaScript development
- **cui-javascript-unit-testing** skill - Test documentation
- ESLint for automated validation
- JSDoc CLI for documentation generation
