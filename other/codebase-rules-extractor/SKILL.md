---
name: codebase-rules-extractor
description: "Extract and document coding rules, patterns, conventions, and anti-patterns from a codebase. Maps the code structure, identifies what to do and what to avoid when creating new code, and generates a comprehensive rules reference document."
argument-hint: "[project_path]: Optional path to the project root to analyze. If not provided, analyzes the current workspace."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: "1.0.0"
---

MANDATORY: Use codebase-rules-extractor-specialist agent
MANDATORY: Conduct a comprehensive analysis of the codebase to extract rules and conventions.

Your objective is to thoroughly analyze a codebase and extract all coding rules, patterns, conventions, best practices, and anti-patterns that should guide future code creation.

====================
PHASE 1 — CODEBASE DISCOVERY & MAPPING
====================

1. **Structure Analysis**
   - Map the directory structure and identify modules/domains
   - Identify project type(s) (frontend, backend, full-stack, library, etc.)
   - Document technology stack and frameworks used
   - List all programming languages present

2. **Documentation Review**
   - Read ALL markdown files: README.md, docs/SUMMARY.md, design docs, ADRs, RFCs
   - Check for existing style guides, conventions documents, or coding standards
   - Identify any .instructions.md, .rules, or similar documentation files
   - Extract explicit rules already documented

3. **Code Pattern Analysis**
   - Scan key files from each domain/module
   - Identify naming conventions (functions, classes, variables, constants)
   - Analyze code structure patterns (architecture, design patterns used)
   - Document folder organization and file naming patterns
   - Identify error handling approaches
   - Analyze dependency management and import patterns
   - Study test structure and testing conventions

====================
PHASE 2 — RULES EXTRACTION
====================

Extract both **explicit rules** (documented, commented) and **implicit rules** (inferred from consistent patterns):

**Categories to Extract:**

1. **Naming Conventions**
   - Function/method naming (camelCase, snake_case, PascalCase, prefixes/suffixes)
   - Variable naming conventions (abbreviations usage, boolean prefixes like `is`, `has`)
   - Class/type naming rules
   - Constant naming (UPPER_SNAKE_CASE, other)
   - File naming conventions

2. **Code Structure & Organization**
   - Module organization principles
   - File size/complexity limits (if observed)
   - Function/method length preferences
   - Code grouping strategies
   - Import organization and ordering
   - Export patterns

3. **Architecture & Design Patterns**
   - Architectural patterns observed (MVC, MVVM, layered, hexagonal, etc.)
   - Design patterns consistently used (Singleton, Factory, Observer, etc.)
   - Component structure (if applicable)
   - Dependency injection approaches
   - State management patterns

4. **Type System & Safety**
   - Type annotation requirements
   - Null/undefined handling strategies
   - Generic type usage patterns
   - Type narrowing approaches
   - Any/unknown type usage policy

5. **Error Handling & Validation**
   - Error throwing conventions
   - Error catching and handling patterns
   - Input validation approaches
   - Error recovery strategies
   - Logging patterns

6. **Testing Conventions**
   - Test file naming and location patterns
   - Testing framework preferences
   - Test structure conventions (describe/it patterns)
   - Mocking/stubbing approaches
   - Test data management
   - Coverage targets (if documented)

7. **Code Style & Formatting**
   - Indentation (spaces/tabs, size)
   - Line length preferences
   - Whitespace usage
   - Comment style and conventions
   - Documentation comment format (JSDoc, docstrings, etc.)
   - Import/export statement formatting

8. **Performance & Optimization**
   - Performance constraints observed
   - Caching strategies
   - Lazy loading patterns
   - Memory management considerations
   - Bundle size considerations (if applicable)

9. **Security Practices**
   - Authentication/authorization patterns
   - Data protection approaches
   - Input sanitization methods
   - Secret management approaches
   - XSS/CSRF prevention patterns

10. **Dependencies & Libraries**
    - Library selection criteria
    - Version constraints and policies
    - Polyfill/compatibility strategies
    - Internal vs external library usage patterns

====================
PHASE 3 — VALIDATION & ORGANIZATION
====================

1. Cross-reference patterns across multiple files to confirm they are consistent rules, not one-offs
2. Distinguish between:
   - **MUST**: Non-negotiable rules (critical for consistency, security, or functionality)
   - **SHOULD**: Strong conventions (break only with justification)
   - **MAY/OPTIONAL**: Flexible patterns (context-dependent)
3. Identify contradictions or evolving patterns
4. Document the frequency and consistency of each rule

====================
PHASE 4 — DOCUMENTATION GENERATION
====================

Generate a comprehensive rules document and save it as:

`docs/agents/rules/<LANGUAGE>-rules-<timestamp>.md`

Where `<LANGUAGE>` is: typescript, python, javascript, golang, rust, java, etc. Or "multi-language" if analyzing multiple languages.

⚠️ Use the EXACT format below:

---

# Codebase Rules & Conventions

**Project:** [Project Name]
**Analysis Date:** [ISO Date]
**Languages:** [List of languages]
**Frameworks:** [Framework list]
**Analyzer Version:** 1.0

---

## 1. Naming Conventions

### Functions & Methods

- **MUST:** [Rule with examples from codebase or code snippets]
- **SHOULD:** [Rule with reasoning]
- **Examples:** Code references or snippets

### Variables

- **MUST:** [Rule]
- **SHOULD:** [Rule]

### Classes & Types

- **MUST:** [Rule]

### Constants

- **MUST:** [Rule]

### Files & Folders

- **MUST:** [Rule]
- **SHOULD:** [Rule]

---

## 2. Code Organization & Architecture

### Project Structure

- [Diagram or description of folder structure]
- **MUST:** [Rule for organizing modules]

### File Organization

- **MUST:** [Rule for imports, exports, order]
- **SHOULD:** [Rule for file grouping]

### Module Patterns

- **Observed Pattern:** [Pattern name with description]
- **Usage:** [When and where this pattern is used]
- **Example Reference:** [File paths using this pattern]

### Architectural Principles

- [List principles (e.g., separation of concerns, DRY, SOLID)]

---

## 3. Type System & Safety

### Type Annotations

- **MUST:** [Rule about required type annotations]
- **SHOULD:** [Rule about optional types]
- **Avoid:** Types that are discouraged

### Null/Undefined Handling

- **MUST:** [Strategy observed]
- **Examples:** Code references

### Generic Types

- **SHOULD:** [Conventions for generic usage]

---

## 4. Error Handling & Validation

### Error Throwing

- **MUST:** [Error convention observed]
- **Pattern:** [Error structure/wrapping pattern]
- **Example:** Code reference

### Error Catching

- **MUST:** [How errors are caught]
- **SHOULD:** [Error recovery patterns]

### Input Validation

- **MUST:** [Validation approach]
- **Location:** [Where validation occurs]

### Logging

- **Standard:** [Log level conventions]
- **Pattern:** [Log message structure]

---

## 5. Testing Conventions

### Test Structure

- **File Naming:** [Pattern: e.g., *.test.ts, *.spec.ts]
- **Location:** [Path pattern relative to source]
- **Framework:** [Testing framework used]

### Test Writing

- **MUST:** [Rule for test structure]
- **Pattern:** [Test organization pattern]
- **Mocking:** [Mocking/stubbing approach]

### Coverage Targets

- [If documented: minimum coverage %]

---

## 6. Code Style & Formatting

### Indentation

- **MUST:** [Spaces/tabs and size]

### Line Length

- **SHOULD:** [Maximum line length]

### Imports & Exports

- **MUST:** [Import statement rules]
- **MUST:** [Export patterns]

### Comments & Documentation

- **Documentation Format:** [JSDoc, docstrings, etc.]
- **MUST:** [What must be documented]
- **SHOULD:** [What should be commented]

---

## 7. Performance & Optimization

### Patterns Observed

- [Caching strategies]
- [Lazy loading patterns]
- [Bundle optimization approaches]

### Constraints

- [Performance targets if any]

---

## 8. Security Practices

### Authentication & Authorization

- **Pattern:** [How auth is handled]
- **Reference:** [File references]

### Data Protection

- **Approach:** [Data protection strategy]

### Input Sanitization

- **MUST:** [Sanitization rule]

### Secrets Management

- **MUST:** [How secrets are managed]

---

## 9. Dependencies & Libraries

### Selection Criteria

- [Why certain libraries are chosen]

### External Dependencies

- **MUST:** [Rules for adding dependencies]

### Version Constraints

- **Policy:** [How versions are managed]

---

## 10. Anti-Patterns to Avoid

### Critical Anti-Patterns (DO NOT USE)

1. [Pattern 1 - Why it's bad with example reference]
2. [Pattern 2]
3. [Pattern 3]

### Discouraged Patterns (AVOID when possible)

1. [Pattern with explanation]
2. [Pattern with explanation]

---

## 11. Best Practices to Follow

### Essential Practices

1. [Practice 1 with explanation]
2. [Practice 2 with explanation]
3. [Practice 3 with explanation]

### Context-Specific Practices

- [For feature A: practice]
- [For API code: practice]
- [For utilities: practice]

---

## 12. Language-Specific Rules

### [Language Name]

- [Language-specific rules and conventions]

### [Other Language]

- [Rules]

---

## 13. Common Code Patterns

### [Pattern Name 1]

- **Purpose:** [What this pattern solves]
- **Frequency:** [How often it appears]
- **Example References:** [File paths or code snippets]
- **When to Use:** [Context for usage]

### [Pattern Name 2]

- [Similar structure]

---

## 14. Tool Configuration & Automation

### Linters & Formatters

- **Tool:** [ESLint, Prettier, Black, etc.]
- **Config File:** [Location of config]
- **MUST:** [Non-negotiable rules enforced]

### Type Checking

- **Tool:** [TypeScript, mypy, etc.]
- **Config:** [Configuration details]
- **Strictness:** [Level enforced]

### Testing Tools

- **Framework:** [Jest, pytest, etc.]
- **Config:** [Location]
- **Commands:** [How to run tests]

---

## 15. Documentation & Comments

### Code Comments

- **MUST:** [What requires comments]
- **SHOULD:** [What should be explained]
- **Avoid:** [Comment anti-patterns observed]

### Function/Class Documentation

- **Format:** [JSDoc, docstring format]
- **MUST Include:** [Required fields]
- **Example:** [Documentation reference]

### README & Project Docs

- **MUST:** [What must be documented]
- **Location:** [Where docs are kept]

---

## Appendix A: File Structure Reference

[Map of key directories and files with brief descriptions]

---

## Appendix B: Code Examples

[Link to or quote from exemplary files that follow the rules]

---

## Appendix C: Evolution & Change Log

- [Date]: [Rule added/changed/removed with reasoning]

---

## Notes

- Analysis performed on: [Codebase version/date]
- Total files analyzed: [Number]
- Languages analyzed: [List]
- Confidence level: [High/Medium based on data consistency]
- Potential gaps: [Any areas that were unclear or inconsistent]

---

⚠️ **GENERATION RULES:**

1. Every extracted rule MUST have at least ONE concrete code reference from the actual codebase
2. Use relative file paths for references: `src/utils/helpers.ts#L10-L20`
3. For each rule severity level (MUST/SHOULD/AVOID), provide concrete examples
4. If contradictory patterns exist, explicitly document both with frequency of usage
5. Keep examples concise - use line references instead of full code blocks when possible
6. Date the document and version it if this analysis will be repeated
7. Document the scope: entire codebase, specific module, specific language, etc.

This document becomes the **authoritative reference** for how new code should be written in this project.
