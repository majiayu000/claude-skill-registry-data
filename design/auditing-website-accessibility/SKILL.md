---
name: auditing-website-accessibility
description: Audits website accessibility for WCAG 2.2 AA compliance, generating findings and code fixes. Use when reviewing accessibility, keyboard navigation, screen reader compatibility, or inclusive design.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
  argument-hint: [url-or-file-path]
  stability: stable
  content-hash: sha256:74f858aeef05a3248b1ec5f9d9a36d4867c364e3150c262879e1593a3302e47b
  last-verified-cc-version: 1.0.34
---

# Website Accessibility Audit

**Target**: $ARGUMENTS

Conducts focused accessibility audits against WCAG 2.2 AA and generates
implementable code fixes. No over-analysis.

## WCAG Quick Reference

**MUST READ** `references/wcag-quick-reference.md` before auditing. Use it as
the checklist for all findings.

## Audit Areas

### Keyboard Navigation

- Tab order and focus management
- Skip links and keyboard shortcuts
- Focus indicators and styling

### Screen Reader Compatibility

- ARIA landmarks and roles
- Semantic HTML structure
- Alternative text and descriptions
- Live region announcements

### Visual Accessibility

- Color contrast ratios (4.5:1 minimum)
- Responsive zoom (200% minimum)
- Motion and animation controls

### Forms and Data Tables

- Label associations and error handling
- Fieldset/legend usage and required field indicators
- Table header associations and caption elements

## Workflow

1. **Identify scope** from $ARGUMENTS (URL, file, or directory)
2. **Run automated checks** (axe-core, HTML validation, contrast ratios)
3. **Manual review** (keyboard-only navigation, screen reader, 200% zoom)
4. **Classify findings** by WCAG level and impact
5. **Generate code fixes** for each finding

## Output Format

### Findings

```text
CRITICAL (WCAG Level A)
- [Issue] - Impact: [High/Medium/Low] - Element: [selector]
  Fix: [Code snippet]
  WCAG: [Success Criterion]

COMPLIANCE (WCAG Level AA)
- [Issue] - Impact: [High/Medium/Low] - Element: [selector]
  Fix: [Code snippet]
  WCAG: [Success Criterion]
```

### Implementation Checklist

```text
- [ ] [Fix description] - Impact: [High/Medium/Low]
```

Group fixes by: Keyboard Navigation, Screen Readers, Visual, Forms/Tables.

## Rules

- Prioritize Level A violations before Level AA
- Every finding must include a specific, implementable code fix
- Test keyboard navigation and screen reader paths manually
- Keep output concise: findings + fixes + checklist only

## Further Reading

- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/)
- [Understanding WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/)
- [WCAG Techniques](https://www.w3.org/WAI/WCAG22/Techniques/)
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/)
- [axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
