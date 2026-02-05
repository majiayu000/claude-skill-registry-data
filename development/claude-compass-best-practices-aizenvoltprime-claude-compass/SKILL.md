---
name: claude-compass-best-practices
description: Enforce Claude Compass development standards and best practices. This skill should be used when writing or modifying code in the Claude Compass repository, including parsers, database migrations, graph builders, MCP tools, and core services. It ensures adherence to code quality principles, proper error handling, self-documenting code, and established architectural patterns.
---

# Claude Compass Best Practices

## Overview

Maintain code quality and architectural consistency across the Claude Compass codebase by enforcing established development principles. This skill provides comprehensive guidance on code quality standards, parser development patterns, and database best practices specific to Claude Compass.

## When to Apply These Standards

Apply these standards proactively when:

- **Writing new code** - parsers, services, utilities, MCP tools
- **Modifying existing code** - refactoring, bug fixes, feature enhancements
- **Adding language support** - new Tree-sitter parsers and grammar integrations
- **Creating database migrations** - schema changes, table additions, index creation
- **Implementing framework detection** - Vue, Laravel, React, Godot pattern recognition
- **Building graph relationships** - dependency detection, cross-stack connections

## Core Development Principles

### The Foundational Rule: No Fallback Logic

**NEVER implement fallback business logic, backwards compatibility, or lazy solutions.**

This principle permeates all Claude Compass development:

- Write robust, well-designed code from the start
- Avoid temporary fixes or "quick and dirty" solutions
- Do not add fallback mechanisms that mask underlying issues
- Implement proper error handling instead of silent failures
- Address root causes rather than symptoms
- Never use inline comments
- Write self-documenting code with clear naming and structure

For detailed examples and anti-patterns, consult `references/code-quality-standards.md`.

### Self-Documenting Code

Code should be self-explanatory through clear naming and structure. Use documentation comments for methods, classes, and properties to describe their **purpose**, not their implementation.

**Key practices:**
- Clear, descriptive variable and function names
- Small, focused functions with single responsibilities
- Logical code organization and structure
- Type safety (avoid `any`, use proper TypeScript types)

For comprehensive naming conventions and examples, consult `references/code-quality-standards.md`.

## Parser Development

When working with parsers or adding new language support:

### Standard Parser Workflow

1. **Add Tree-sitter Grammar Dependency** - Install appropriate grammar package
2. **Create Parser Module** - Single file or modularized directory structure
3. **Implement Chunking Strategy** - For languages with large files (>100KB)
4. **Add Comprehensive Tests** - Test all language constructs and error cases
5. **Register in Multi-Parser** - Make parser available to the system

### Tree-sitter Usage

- Use cursor-based traversal for efficiency
- Employ query-based extraction for specific patterns
- Always check node types before extracting data
- Handle errors with full context (file path, line numbers, chunk info)

### Debugging Parser Issues

```bash
# Enable verbose debug logging
CLAUDE_COMPASS_DEBUG=true ./dist/src/cli/index.js analyze /path --verbose

# Debug single file (isolates parsing of one file)
./dist/src/cli/index.js analyze /path/to/repo \
  --debug-file relative/path/to/file.cs \
  --verbose
```

**For complete parser patterns, including:**
- Modularization strategies
- Chunking error handling
- Framework detection patterns
- Cross-stack dependency detection
- Performance optimization techniques

**Consult `references/parser-patterns.md`**

## Database Development

All database schema changes must be done through migrations. Never modify the database schema directly.

### Migration Standards

**Naming**: `NNN_description.ts`
- `NNN` = 3-digit sequential number (001, 002, 003, ...)
- `description` = kebab-case description

**Structure**: Every migration MUST include both `up` and `down` methods

```bash
# Create new migration
npm run migrate:make add_entity_type_column

# Apply migrations
npm run migrate:latest

# Check status
npm run migrate:status

# Rollback (if needed)
npm run migrate:rollback
```

### Schema Design Principles

- Use appropriate, specific data types (not generic)
- Define foreign keys with proper cascade behavior (`CASCADE`, `SET NULL`, `RESTRICT`)
- Add indexes for columns used in WHERE, JOIN, ORDER BY clauses
- Be explicit about nullability and default values
- Use composite indexes strategically (order matters)

### Query Patterns

- Always use parameterized queries (prevent SQL injection)
- Use transactions for multi-step atomic operations
- Batch large insertions for performance
- Structure joins to use indexes effectively

**For complete database patterns, including:**
- Service layer structure
- Transaction handling
- Vector search (pgvector) implementation
- Database testing strategies
- Migration workflow

**Consult `references/database-patterns.md`**

## Modularization Strategy

Claude Compass follows strict modularization for maintainability:

### When to Modularize

Modularize when a file:
- Exceeds 500 lines of code
- Contains multiple distinct responsibilities
- Would benefit from clearer separation of concerns

### Directory Structure Pattern

```
src/parsers/<feature>/
├── index.ts              # Public API exports (backward compatibility)
├── <feature>.ts          # Main logic
├── <service-1>.ts        # Focused, single-purpose modules
├── <service-2>.ts
└── types.ts              # Shared type definitions
```

Examples in codebase:
- `src/parsers/csharp/` - C# language parser (modularized)
- `src/parsers/orm/` - ORM parsers (modularized)
- `src/parsers/framework-detector/` - Framework detection (modularized)
- `src/graph/builder/` - Graph construction (modularized)

## Error Handling

### Fail Fast, Fail Loudly

Detect and report errors as early as possible with maximum context.

### Context-Rich Errors

Include all relevant information in error messages:
- File path and line numbers
- Operation being performed
- Related data (chunk index, symbol name, etc.)
- Original error cause

Example:
```typescript
throw new ChunkingError(
  `Failed to parse chunk: syntax error in object literal`,
  {
    filePath: '/path/to/file.ts',
    chunkIndex: 3,
    totalChunks: 5,
    startLine: 250,
    endLine: 499,
    cause: originalError
  }
);
```

## Testing Requirements

Every feature or bug fix should include tests:

- **Parsers**: Test each language construct (classes, functions, imports)
- **Graph builders**: Test relationship detection and edge cases
- **Database operations**: Test CRUD operations and queries
- **MCP tools**: Integration tests for each tool
- **Error handling**: Test that errors include proper context

Test files: `tests/**/*.test.ts`

## Reference Files

This skill includes three comprehensive reference documents:

### 1. Code Quality Standards (`references/code-quality-standards.md`)

Load when:
- Writing new code that needs architectural guidance
- Refactoring existing code for quality improvements
- Reviewing code for adherence to standards
- Questions about self-documenting code or naming conventions

Contains:
- Detailed fallback logic anti-patterns
- Self-documenting code examples
- Modularization patterns and checklists
- Error handling philosophy
- Type safety guidelines
- Testing requirements

### 2. Parser Patterns (`references/parser-patterns.md`)

Load when:
- Adding support for a new programming language
- Working with Tree-sitter parsing logic
- Implementing or debugging chunking strategies
- Adding framework detection capabilities
- Detecting cross-stack dependencies

Contains:
- Complete language support workflow (5 steps)
- Tree-sitter cursor traversal patterns
- Query-based extraction techniques
- Chunking error handling strategies
- Framework detection patterns
- Performance optimization techniques

### 3. Database Patterns (`references/database-patterns.md`)

Load when:
- Creating database migrations
- Designing new tables or schema changes
- Writing database queries or services
- Implementing vector search with pgvector
- Working with database transactions

Contains:
- Migration naming and structure standards
- Schema design principles (types, foreign keys, indexes)
- Query patterns (parameterized queries, transactions, batching)
- Service layer architecture
- Vector search implementation
- Migration workflow and rollback strategies

## Quick Decision Guide

Use this guide to determine which reference to consult:

| Task | Reference to Load |
|------|-------------------|
| Writing a new function/class | `code-quality-standards.md` |
| Adding language support (Rust, Go, etc.) | `parser-patterns.md` |
| Creating database migration | `database-patterns.md` |
| Implementing Tree-sitter parsing | `parser-patterns.md` |
| Designing database schema | `database-patterns.md` |
| Refactoring for code quality | `code-quality-standards.md` |
| Debugging parser errors | `parser-patterns.md` |
| Writing database queries | `database-patterns.md` |
| Modularizing a large file | `code-quality-standards.md` |
| Adding framework detection | `parser-patterns.md` |

## Progressive Consultation

Start with the relevant reference sections and load additional context as needed:

1. **Identify the task** - Determine which category (code quality, parser, database)
2. **Load relevant reference** - Consult the appropriate reference file
3. **Apply patterns** - Follow established patterns and examples
4. **Verify compliance** - Ensure adherence to core principles
