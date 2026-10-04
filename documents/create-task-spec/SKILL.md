---
name: create-task-spec
description: A skill for creating structured task specifications based on detailed analysis of the provided task description. Use this skill to generate comprehensive technical specifications that will serve as input for task-master, ensuring that all necessary context, relevant files, code snippets, and a clear action plan are included to facilitate efficient task implementation.
argument-hint: "[task_description]: A string containing the detailed description of the task to be analyzed and transformed into a structured technical specification document. Or a file path to a markdown file containing the task description."
metadata:
  author: Ronnasayd Machado - github.com/Ronnasayd
  version: 1.0.0
aliases:
---

MANDATORY: Use task-reviewer-specialist agent
MANDATORY: execute the **{task_description}** argument as a task description and analyze it according to the system instructions.

Your objective is to analyze the task and produce a structured technical specification document that will later be used as input for task-master.

📋 **COMPACT SPECIFICATIONS APPROACH**: Target document size 400-600 lines by using code references, tables, and matrices instead of narrative descriptions. See APPENDIX at the end for detailed best practices.

====================
PHASE 1 — CONTEXT DISCOVERY
====================

1. Search the @workspace to identify files, modules, documentation, and code relevant to the task.
2. Prioritize local documentation (\*.md files), starting from:
   - docs/SUMMARY.md
   - docs/
3. Only search the web if:
   - The workspace does not contain sufficient information, OR
   - External documentation is clearly required (e.g., framework or library behavior).
4. When searching the web, prioritize official documentation and stable sources.

⚠️ Do NOT implement any code.
⚠️ Do NOT execute any terminal commands in this phase.

====================
PHASE 2 — SPECIFICATION GENERATION
====================

Based on your analysis, generate a task specification and save it as:

docs/agents/specs/yyyy-mm-dd-<short-task-description>.md

⚠️ **COMPACT FORMAT STRATEGY**: Keep document size 400-600 lines by:

- Using code references (file#L123-L456) instead of full code snippets
- Including snippets ONLY for new patterns without equivalent in the codebase
- Describing tests in tables (cases, inputs, outputs) instead of code blocks
- Using matrices/tables instead of narrative text wherever possible
- Referring to existing patterns in codebase rather than duplicating examples

You MUST strictly follow the format below. Do not add, remove, reorder, or rename sections.

<format>

## Problem Summary

## Relevant Files for Solving the Problem

## Key Code References

| File         | Location                                   | Pattern     | Application  |
| ------------ | ------------------------------------------ | ----------- | ------------ |
| path/to/file | [file.ts#L10-L20](path/to/file.ts#L10-L20) | description | how to apply |

## Proposed Action Plan for Task Implementation

## Testing Strategy for Validating the Implementation

## Context Map

```markdown
### Files to Modify

| File         | Purpose     | Changes Needed |
| ------------ | ----------- | -------------- |
| path/to/file | description | what changes   |

### Dependencies (may need updates)

| File        | Relationship                 |
| ----------- | ---------------------------- |
| path/to/dep | imports X from modified file |

### Test Files

| Test         | Coverage                     |
| ------------ | ---------------------------- |
| path/to/test | tests affected functionality |

### Reference Patterns

| File            | Pattern           |
| --------------- | ----------------- |
| path/to/similar | example to follow |

### Risk Assessment

- [ ] Breaking changes to public API
- [ ] Database migrations needed
- [ ] Configuration changes required
```

## Relevant Links (Optional)

  </format>

====================
PHASE 3 — USER REVIEW
====================

Ask the user to review the generated document.

- If the user suggests modifications or extensions, apply them to the same document.
- Repeat this step until the user explicitly confirms with a phrase equivalent to:
  "You can proceed."

Do NOT proceed without explicit confirmation.

====================
APPENDIX: COMPACT SPECIFICATION BEST PRACTICES
====================

### Code References Format

Replace long code snippets with file references. Examples:

```markdown
| Pattern               | Location                                                                   | How to Apply                             |
| --------------------- | -------------------------------------------------------------------------- | ---------------------------------------- |
| Validation with Zod   | [event.dto.ts#L45-L52](src/modules/event/event.dto.ts#L45-L52)             | Add `native: z.boolean()` to schema      |
| Create service method | [event.service.ts#L156-L175](src/modules/event/event.service.ts#L156-L175) | Extract field from DTO, pass to create   |
| Event logging pattern | [auth.controller.ts#L93-L96](src/modules/auth/auth.controller.ts#L93-L96)  | Call EventLogService.createAuthenticated |
```

### Testing Strategy Format

Use tables instead of code examples:

```markdown
| Test Case          | Input               | Expected  | Assertion              |
| ------------------ | ------------------- | --------- | ---------------------- |
| Valid boolean true | `{ native: true }`  | Parsed    | Type is boolean        |
| Omitted field      | `{}`                | Defaults  | Value is false         |
| Invalid string     | `{ native: "sim" }` | Error 400 | ValidationError thrown |
```

### Scenario Matrix Format

For complex interactions, use decision tables:

```markdown
| Local State  | Remote State   | Action | Result              |
| ------------ | -------------- | ------ | ------------------- |
| false→true   | Add suffix     | Update | `[native]` appended |
| true→false   | Has suffix     | Update | `[native]` removed  |
| Receive sync | Has `[native]` | Parse  | Set local=true      |
```

### When to Include Code Snippets

Only include snippets for:

- ✅ **New patterns** not present in the codebase (e.g., a new synchronization algorithm)
- ✅ **Complex business logic** that requires explanation
- ❌ **Never** for existing code patterns — use file references instead
- ❌ **Never** for demonstrations of standard library usage

### Implementation Phases Format

Use checklists with time estimates:

```markdown
### Phase 1: Database & Schema (Est: 4 hours)

- [ ] Add `native Boolean @default(false)` to Prisma schema
  - See [event.prisma#L61-L83](src/modules/event/event.prisma#L61-L83) for context
- [ ] Create database migration with `yarn prisma:migrate dev`
- [ ] Update DTOs in [event.dto.ts#L45-L52](src/modules/event/event.dto.ts#L45-L52)
- [ ] Verify Prisma generation with `yarn prisma:generate`
```

### Expected Outcomes

- **Document Size**: 400-600 lines vs. 1500+ (50-60% reduction)
- **Context Usage**: ~30% reduction in token consumption
- **Clarity**: Maintained through clear section structure and tables
- **Navigability**: Enhanced with file line references

### Quality Checklist

Before finalizing the spec, verify:

- [ ] No code snippets > 15 lines (except new patterns)
- [ ] All file references include line numbers ([file.ts#L10-L20])
- [ ] All complex scenarios converted to tables/matrices
- [ ] Problem Summary is 1-2 paragraphs maximum
- [ ] Implementation Phases use checklist format with estimates
- [ ] Testing Strategy uses comparison tables instead of code blocks
- [ ] No narrative text where a table fits better
- [ ] Document size is within 400-600 line target
