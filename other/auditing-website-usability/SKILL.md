---
name: auditing-website-usability
description: Audits website usability for UX optimization, covering forms, navigation, validation, and microcopy. Use when reviewing user experience, task completion flows, or interface friction points.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
  argument-hint: [url-or-file-path]
  stability: stable
  content-hash: sha256:0e7c6cbfc6559f5799d96568468a418ca323f0fbd15dc5ed294decd5e56874a8
  last-verified-cc-version: 1.0.34
---

# Website Usability Audit

**Target**: $ARGUMENTS

Conducts focused usability audits and generates implementable UX fixes.
Complements `auditing-website-accessibility` (WCAG compliance) with
UX-focused analysis. No overlap: accessibility handles ARIA/contrast/keyboard;
this handles task completion, friction, and clarity.

## Audit Areas

### Forms

- Smart defaults and field reduction
- Logical grouping and progressive disclosure
- Inline validation with helpful messaging

### Navigation

- Information architecture and menu depth (target: <3 levels)
- Mobile usability and touch targets
- Breadcrumbs, search, and task completion paths

### Input Validation

- Real-time feedback and error prevention
- Clear error messages with recovery guidance
- Submission confirmation

### Microcopy

- Button labels, form hints, and instructional text
- Error message clarity and actionability
- User confidence messaging

## Workflow

1. **Identify scope** from $ARGUMENTS (URL, file, or directory)
2. **Audit task flows** - map primary user journeys, identify friction
3. **Inspect forms** - field count, grouping, validation behavior
4. **Review navigation** - menu depth, mobile patterns, findability
5. **Evaluate microcopy** - labels, errors, guidance text
6. **Classify findings** by impact on task completion
7. **Generate fixes** with specific code changes

## Output Format

### Findings

```text
CRITICAL (Task Completion Blockers)
- [Issue] - Impact: [High/Medium/Low] - Element: [selector]
  Fix: [Specific code/design change]
  Metric: [What improves - conversion, completion, error rate]

OPTIMIZATIONS (Friction Reduction)
- [Issue] - Impact: [High/Medium/Low] - Element: [selector]
  Fix: [Specific code/design change]
  Metric: [What improves]
```

### Implementation Checklist

```text
- [ ] [Fix description] - Impact: [High/Medium/Low]
```

Group fixes by: Forms, Navigation, Validation, Microcopy.

## Rules

- Prioritize task-completion blockers before friction reduction
- Every finding must include a specific, implementable fix
- No time estimates -- prioritize by impact only
- Defer WCAG/accessibility concerns to `auditing-website-accessibility`
- Keep output concise: findings + fixes + checklist only

## Further Reading

- [Nielsen Norman Group — UX Research](https://www.nngroup.com/articles/)
- [Usability.gov — User Interface Design](https://www.usability.gov/what-and-why/user-interface-design.html)
- [Baymard Institute — UX Benchmarks](https://baymard.com/blog)
