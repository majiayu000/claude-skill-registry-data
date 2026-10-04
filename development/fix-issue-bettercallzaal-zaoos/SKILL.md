---
name: fix-issue
description: Use when fixing a GitHub issue — reads the issue, implements the fix, writes tests, and commits referencing the issue number
disable-model-invocation: true
argument-hint: "[issue-number]"
---

# Fix Issue — GitHub Issue to Commit

End-to-end workflow for fixing a GitHub issue.

## Usage

```
/fix-issue 42
```

## Workflow

### 1. Read the Issue

```
Issue details: !`gh issue view $ARGUMENTS`
Issue comments: !`gh issue view $ARGUMENTS --comments`
```

### 2. Understand & Plan

- Read all referenced files
- Identify root cause
- Propose fix approach to the user before implementing

### 3. Implement

- Follow ZAO OS conventions (Zod validation, session checks, Tailwind dark theme, mobile-first)
- Make minimal changes — fix the issue, don't refactor surrounding code

### 4. Test

- Run `npm run lint` and `npm run build` to verify no regressions
- If test files exist nearby, run them with `npx vitest run [file]`
- If the fix touches an API route, verify the Zod schema covers the change

### 5. Commit

- Stage only the files you changed
- Commit message format: `fix(feature): description (closes #$ARGUMENTS)`

## Rules

- Always read the full issue + comments before starting
- Always propose the fix approach before implementing
- Never push — let the user decide when to push
- Reference the issue number in the commit message
