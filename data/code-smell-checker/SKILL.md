---
name: code-smell-checker
description: Review TypeScript + Vue code for maintainability issues. Use when checking code quality, architectural problems, type safety, or Vue best practices. Identifies technical debt in components, types, and reactive data handling.
license: Apache-2.0
compatibility: TypeScript + Vue 3 projects
metadata:
  author: xiaoland
  version: "1.0"
  related-skills: "dev-vue-component"
---

# Code Smell Checker

## When to use

Review code when you need to:

- Check AI-generated or developer code for maintainability
- Identify technical debt and quality issues
- Validate TypeScript type design and semantic clarity
- Review Vue component architecture
- Ensure reactive data handling best practices
- Conduct code quality assessments

## What's covered

**TypeScript Types:**
- Organization and coupling → [type-organization.md](references/type-organization.md)
- Extensibility and complexity → [type-design.md](references/type-design.md)

**Vue Components:**
- Structure and lifecycle → [component-structure.md](references/component-structure.md)
- Props and state → [component-props-state.md](references/component-props-state.md)
- Templates and communication → [component-template.md](references/component-template.md)

**Reactive Data:**
- Ref, reactive, depth → [reactive-basics.md](references/reactive-basics.md)
- Computed properties → [reactive-computed.md](references/reactive-computed.md)
- Watch patterns → [reactive-watch.md](references/reactive-watch.md)
- Performance → [reactive-optimization.md](references/reactive-optimization.md)
- Memory management → [reactive-memory.md](references/reactive-memory.md)

## How to use

**1. Identify scope:**
- Which area? (types, components, reactive)
- Which files to review?

**2. Apply checklist:**
- Read relevant reference doc
- Check code against items
- Note violations

**3. Report findings:**
- Categorize by severity
- Focus on maintainability impact
- Consider project context

**4. Provide feedback:**
- Explain why it's a problem
- Show the bad pattern
- Suggest concrete improvements
- Reference checklist item

## Quick reference

**TypeScript red flags:**
- Scattered type definitions
- `any`, `object`, overly broad types
- Complex type gymnastics
- Types don't match runtime

**Vue component red flags:**
- Components >300 lines
- Props drilling >3 levels
- Mixed local/global/derived state
- Weak prop types

**Reactive data red flags:**
- Deep reactive on large data
- Computed with side effects
- Watch for transformations
- Wrong ref/reactive usage

## Output format

```
## Review: [Component/Module]

### [Category]

#### [Issue]
- Severity: [Critical/Important/Minor]
- Location: file.ts:123
- Reference: [Link to checklist]
- Problem: [Explain]
- Fix: [Suggest]
```

## Best practices

**Be constructive:**
- Focus on maintainability not preferences
- Explain "why" behind each smell
- Provide concrete alternatives
- Recognize when rules should bend

**Be systematic:**
- Review one category at a time
- Use checklist for coverage
- Document patterns
- Track recurring issues

**Be pragmatic:**
- Not all items apply to every project
- Consider project maturity
- Balance idealism with reality
- Prioritize high-impact issues
