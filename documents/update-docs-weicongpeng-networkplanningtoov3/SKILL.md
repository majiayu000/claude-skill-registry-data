---
name: update-docs
description: Helps update documentation based on code changes. Provides a workflow for maintainers to review documentation completeness in PRs. Guide for scaffolding docs, checking what docs need updating, and reviewing docs for completeness.
---

# Update Docs

This skill helps you update documentation based on code changes. It provides a workflow for maintainers to review documentation completeness in PRs and guides for scaffolding docs.

## When to Use This Skill

Use this skill when the user:

- Asks to "update documentation for my changes"
- Wants to "check docs for this PR"
- Asks "what docs need updating"
- Says "sync docs with code"
- Wants to "scaffold docs for this feature"
- Asks to "document this feature"
- Says "review docs completeness"
- Wants to "add docs for this change"
- Mentions "docs/", ".mdx files", or documentation updates

## Workflow Overview

### Step 1: Analyze Code Changes

First, understand what has changed in the codebase:

```bash
# View all changed files on the branch
git diff main...HEAD --stat

# View changes in a specific area
git diff main...HEAD -- src/
```

### Step 2: Identify Documentation-Impacting Changes

Determine which source code changes require documentation updates:

| Source Code Path         | Potentially Affected Docs        |
| ------------------------- | -------------------------------- |
| `src/components/`        | Component API references         |
| `src/lib/`               | Feature docs, utility functions  |
| `src/app/`               | Routing, file conventions        |
| `types/`                  | TypeScript type references       |
| Config files              | Configuration options           |

### Step 3: Update Existing Documentation

When updating existing docs:

1. **Read the current doc** to understand structure and style
2. **Identify what needs updating**:
   - New props/options: Add to props table
   - Behavior changes: Update descriptions and examples
   - Deprecated features: Add deprecation notices and migration guidance
   - New examples: Add code blocks following conventions

### Step 4: Create New Feature Documentation

For new features, determine the appropriate doc location:

| Feature Type          | Doc Location                           | Template Type  |
| ------------------- | -------------------------------------- | -------------- |
| New Component        | `docs/api/components/`                  | API Reference  |
| New Function/Hook    | `docs/api/functions/`                  | API Reference  |
| New Config Option    | `docs/api/configuration/`              | Config Ref     |
| New Concept/Guide     | `docs/guides/`                         | Guide          |
| New File Convention  | `docs/api/file-conventions/`          | File Convention|

## Documentation Standards

### Frontmatter Requirements

Every page must have frontmatter with at least:

```yaml
---
title: Page Title
description: One or two sentences describing what this page covers.
---
```

### Code Block Conventions

Use proper filename attributes and language tags:

``````mdx
```tsx filename="app/page.tsx"
// TypeScript example
``````

```jsx filename="app/page.js"
// JavaScript example
``````

``````

### Props Table Format

For components with props, use a table format:

| Prop    | Example             | Type    | Required |
| ------- | ------------------- | ------- | -------- |
| `prop`  | `prop="value"`      | string  | Yes      |

### Links and References

- Use relative links for internal docs
- Include full URLs for external references
- Test links before submitting

## Verification Checklist

Before submitting documentation changes:

- [ ] Frontmatter includes `title` and `description`
- [ ] Code blocks have proper `filename` attributes
- [ ] TypeScript examples use `switcher` where applicable
- [ ] Props tables are properly formatted
- [ ] Related links point to valid paths
- [ ] Changes render correctly (preview if available)
- [ ] Spelling and grammar are correct
- [ ] Code examples are accurate and tested

## Common Documentation Patterns

### Component Documentation

```markdown
# ComponentName

Description of what this component does.

## Usage

Basic usage example:
```tsx filename="app/example.tsx"
import { ComponentName } from 'package'

export default function Page() {
  return <ComponentName prop="value" />
}
```

## Props

| Prop    | Type    | Required | Description        |
| ------- | ------- | -------- | ------------------ |
| `prop`  | string  | Yes      | Prop description   |

## Examples

Example 1: Basic usage
Example 2: Advanced usage
```

### Function/Hook Documentation

```markdown
# useHookName

Description of what this hook does.

## Usage

```tsx filename="hooks/use-hook.ts"
import { useHookName } from 'hooks'

export default function Component() {
  const result = useHookName()
  return <div>{result}</div>
}
```

## Parameters

| Parameter | Type     | Description        |
| --------- | -------- | ------------------ |
| `param`   | string   | Parameter description |

## Returns

Return value description.
```

## Tips for Effective Documentation

1. **Be concise but complete**: Include all necessary information without verbosity
2. **Use examples liberally**: Show, don't just tell
3. **Keep examples simple**: Focus on the feature being documented, not unrelated complexity
4. **Update in parallel**: When changing code, update docs at the same time when possible
5. **Link liberally**: Help users find related information easily

## When No Documentation Is Needed

Not every code change requires documentation:

- Bug fixes that don't affect user-facing behavior
- Internal refactoring with no API changes
- Test updates
- Build configuration changes (unless user-facing)

If documentation isn't needed, acknowledge this and proceed.
