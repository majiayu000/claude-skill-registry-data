---
name: coderabbit-fix-flow
description: This skill should be used when CodeRabbit code review feedback needs to be processed and fixed systematically. Use after running `coderabbit --plain` to automatically save feedback, analyze issues using MCP tools, and implement minimal code fixes with proper planning.
---

# CodeRabbit Fix Flow

## Overview

This skill automates the workflow of processing CodeRabbit code review feedback by saving the review output to a timestamped document, then using MCP tools (sequential thinking and Exa context) to analyze and implement fixes with minimal code changes.

## When to Use

Use this skill immediately after running `coderabbit --plain` or when you have CodeRabbit feedback that needs systematic processing. The skill handles type safety issues, code style violations, and other CodeRabbit-identified problems.

## Workflow

### Step 1: Execute CodeRabbit Review

Run the CodeRabbit review command in plain text mode:
```bash
coderabbit --plain
```

### Step 2: Save Feedback Document

Save the CodeRabbit output to a timestamped QA document:
- Create file: `memory-bank/qa/coderabbit/cr-qa-{timestamp}.md`
- Include the full CodeRabbit output in the document
- Add YAML front matter with metadata:
  ```yaml
  ---
  title: "CodeRabbit QA Review - {timestamp}"
  link: "cr-qa-{timestamp}"
  type: "qa"
  tags:
    - code-review
    - coderabbit
    - type-safety
  created_at: "{timestamp}"
  updated_at: "{timestamp}"
  uuid: "{generate-uuid}"
  ---
  ```

### Step 3: Analyze Issues with Sequential Thinking

Use the sequential thinking MCP tool to analyze all identified issues:
1. **Categorize issues** by type (type safety, performance, style, security)
2. **Prioritize fixes** (critical runtime issues first, then documentation)
3. **Plan minimal changes** to achieve the fixes
4. **Identify dependencies** between issues

### Step 4: Get Best Practices Context

Use the Exa code context MCP tool to research current best practices for each issue type:
- For type issues: "TypeScript type guards runtime validation best practices"
- For Python type issues: "Python type annotations Optional None best practices"
- For performance: "Performance optimization best practices [language]"
- For security: "Security vulnerability fixes [language]"

### Step 5: Implement Fixes Systematically

Execute the fixes following the sequential thinking plan:

1. **Create TodoWrite list** tracking all issues
2. **Mark each issue** as in_progress → completed
3. **Apply minimal code changes** using best practices from Exa context
4. **Verify fixes** address the root cause identified by CodeRabbit

### Step 6: Validate and Document

Run validation as appropriate:
- TypeScript: `npm run build` or `tsc --noEmit`
- Python: `mypy` or `ruff check`
- JavaScript: `npm run lint` or biome

Document the fixes in the QA document with:
- What was fixed
- How it was fixed
- Validation results

## Issue Type Patterns

### Type Safety Issues
- Use proper type guards instead of assertions
- Apply Optional/Union types for nullable fields
- Implement runtime validation where needed

### Code Style Issues
- Follow language-specific style guides
- Use linting tools to verify fixes
- Maintain consistency with existing codebase

### Performance Issues
- Research current optimization patterns
- Implement minimal impactful changes
- Measure before/after when possible

### Security Issues
- Understand the vulnerability context
- Apply security best practices
- Ensure fixes don't break functionality

## Examples

### Type Safety Fix Pattern
```typescript
// Before (unsafe)
const data = response as ResearchDataShape;

// After (safe)
const data = isResearchDataShape(response) ? response : {} as ResearchDataShape;
```

### Python Type Annotation Fix Pattern
```python
# Before (incorrect)
timestamp: float = None
metadata: dict[str, Any] = None

# After (correct)
timestamp: float | None = None
metadata: dict[str, Any] | None = None
```

## MCP Tool Usage

### Sequential Thinking Tool
Use for:
- Breaking down complex issues into steps
- Planning fix order and dependencies
- Analyzing multiple issues systematically

### Exa Code Context Tool
Use for:
- Getting current best practices
- Understanding language-specific patterns
- Finding optimal implementation approaches

## Resources

This skill doesn't require bundled resources as it relies on MCP tools for context and the existing codebase for implementation.