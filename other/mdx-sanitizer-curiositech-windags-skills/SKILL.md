---
license: Apache-2.0
name: mdx-sanitizer
description: Comprehensive MDX content sanitizer that escapes angle brackets, generics, and other JSX-conflicting patterns to prevent build failures
version: 1.0.0
category: Productivity & Meta
tags:
  - mdx
  - sanitization
  - content
  - markdown
  - security
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
triggers:
  - mdx error
  - angle bracket
  - jsx parsing
  - build failure mdx
  - escape angle brackets
  - sanitize markdown
---

# MDX Sanitizer

Comprehensive MDX content sanitizer that prevents JSX parsing errors caused by angle brackets, generics, and other conflicting patterns.

## Decision Points

**When to sanitize vs validate vs wrap:**

```
Content Analysis:
├── Inside code blocks (```, `)
│   └── → Skip sanitization (already protected)
├── Contains TypeScript generics (`Promise<T>`)
│   └── → Sanitize with HTML entities
├── Contains comparisons (`<100ms`, `<=`)
│   └── → Sanitize with HTML entities  
├── Contains arrows (`->`, `<--`)
│   └── → Sanitize with HTML entities
├── Valid JSX components (PascalCase)
│   └── → Skip sanitization (preserve functionality)
├── Valid HTML5 elements (`<div>`, `<span>`)
│   └── → Skip sanitization (preserve functionality)
├── Invalid pseudo-tags (`<link>` in prose)
│   └── → Sanitize with HTML entities
└── Documentation examples
    ├── If showing code syntax → Wrap in code blocks
    └── If showing output/prose → Sanitize with HTML entities
```

**Content type decision matrix:**

| Pattern | Action | Reason |
|---------|--------|--------|
| `Promise<T>` | Sanitize | TypeScript generic, not JSX |
| `<MyComponent>` | Skip | Valid JSX component |
| `<div>` | Skip | Valid HTML5 element |
| `<link>` in prose | Sanitize | Invalid context for HTML |
| `<100ms` | Sanitize | Comparison, not JSX |
| `` `<T>` `` | Skip | Already in code block |

## Failure Modes

**Schema Bloat**: Over-sanitizing valid JSX
- *Detection*: Valid React components getting escaped (`&lt;Button&gt;` instead of `<Button>`)
- *Diagnosis*: Sanitizer not recognizing PascalCase or valid HTML5 elements
- *Fix*: Update whitelist for valid JSX patterns, test with `isMdxSafe()` first

**Escape Cascade**: Double-escaping already sanitized content
- *Detection*: Seeing `&amp;lt;` instead of `&lt;` in output
- *Diagnosis*: Running sanitizer multiple times on same content
- *Fix*: Check if content already escaped with `validateMdxSafety()` before processing

**Code Block Pollution**: Sanitizing content that should stay literal
- *Detection*: Code examples showing `&lt;T&gt;` instead of `<T>`
- *Diagnosis*: Sanitizer processing content inside code fences
- *Fix*: Verify code block detection logic, wrap examples properly

**Context Blindness**: Wrong sanitization strategy for content type
- *Detection*: Documentation examples breaking or looking wrong
- *Diagnosis*: Not distinguishing between code syntax vs prose descriptions
- *Fix*: Analyze context - if showing syntax, use code blocks; if describing, sanitize

**Validation Bypass**: Files passing validation but failing build
- *Detection*: `npm run validate:all` passes but `npm run build` fails with JSX errors
- *Diagnosis*: Build-time MDX parsing stricter than validation regex
- *Fix*: Clear Docusaurus cache, re-run full sanitization, check for edge patterns

## Worked Examples

**Scenario 1: TypeScript API Documentation**

*Input content:*
```markdown
The `createMap` function returns `Promise<Map<string, User>>` where each User has...
Performance is <100ms for datasets <=1000 items.
```

*Decision process:*
1. Scan for code blocks → None found
2. Identify patterns → `Promise<Map<string, User>>`, `<100ms`, `<=1000`
3. Check if valid JSX → No, these are TypeScript generics and comparisons
4. Apply HTML entity escaping

*Output:*
```markdown
The `createMap` function returns `Promise&lt;Map&lt;string, User&gt;&gt;` where each User has...
Performance is &lt;100ms for datasets &lt;=1000 items.
```

*Expert insight*: Novice might wrap entire line in code block, losing prose flow. Expert selectively escapes only the problematic characters while preserving readability.

**Scenario 2: Component Usage Guide**

*Input content:*
```markdown
Use <Button variant="primary"> for main actions.
The <link> tag should be avoided in favor of <Link>.
```

*Decision process:*
1. Analyze first pattern → `<Button variant="primary">` has PascalCase, valid JSX
2. Skip sanitization for Button component
3. Analyze second pattern → `<link>` in prose context, not valid JSX usage
4. Sanitize invalid tag references

*Output:*
```markdown
Use <Button variant="primary"> for main actions.  
The &lt;link&gt; tag should be avoided in favor of <Link>.
```

*Trade-off analysis*: Preserving functional JSX while sanitizing prose references maintains both functionality and safety.

## Quality Gates

- [ ] All `<` characters outside code blocks are either valid JSX components or HTML-entity escaped
- [ ] No `&amp;lt;` double-escaping patterns in output
- [ ] Code blocks (``` and `) preserve original angle brackets
- [ ] PascalCase components (`<MyComponent>`) remain unescaped
- [ ] Valid HTML5 elements (`<div>`, `<span>`, `<a>`) remain unescaped
- [ ] TypeScript generics (`Promise<T>`) are escaped to `Promise&lt;T&gt;`
- [ ] Comparison operators (`<100`, `<=`) are escaped
- [ ] `validateMdxSafety()` returns no issues for processed content
- [ ] `npm run build` completes without JSX parsing errors
- [ ] Visual inspection confirms proper rendering in browser

## NOT-FOR Boundaries

**This skill is NOT for:**

- **Dynamic JSX props with runtime values** → Use proper JSX escaping libraries like `escape-html` or React's built-in escaping
- **Server-side HTML sanitization** → Use `DOMPurify` or similar XSS protection libraries  
- **Markdown-to-HTML conversion** → Use dedicated parsers like `marked` or `remark`
- **Syntax highlighting in code blocks** → Handled by Prism.js/highlight.js in build pipeline
- **User-generated content sanitization** → Use `isomorphic-dompurify` with CSP policies
- **Build-time MDX plugin development** → Use `@mdx-js/mdx` plugin API instead

**Delegation patterns:**
- For XSS protection → `xss-security-skill`
- For React component escaping → `react-escaping-skill` 
- For build system integration → `docusaurus-config-skill`
- For regex pattern development → `regex-patterns-skill`