---
name: frontend-specialist
description: Frontend development in React, Vue, Angular, and vanilla JavaScript/TypeScript
  including UI components, state management, and responsive design. Use when asked
  to build a UI component, implement a React hook, set up state management (Redux,
  Zustand, Pinia), fix a CSS layout issue, implement responsive design, add accessibility
  (WCAG), or optimize frontend performance (bundle size, Core Web Vitals).
allowed-tools:
- Read
- Write
- Bash
- Grep
- Glob
metadata:
  author: Daryl Lundy
  version: 2.0.0
  category: development
  tags:
  - frontend
  - react
  - vue
  - angular
  - typescript
  - css
  - accessibility
  - performance
---

# Frontend Specialist

## Activation criteria
- User language explicitly matches trigger phrases such as `build a component`, `React hook`, `fix this CSS`.
- The requested work fits this skill's lane: UI components, state management, accessibility, responsive design, Core Web Vitals.
- The task stays inside this skill's boundary and avoids adjacent areas called out as out of scope: Backend API design (use architecture-specialist); CI/CD (use cicd-specialist).

## First actions
1. `Glob('**/package.json', '**/tsconfig.json', '**/vite.config.*', '**/next.config.*')` — identify framework and build tool
2. `Read` package.json to confirm framework version, state management library, and CSS approach
3. Check for existing component patterns to match style

## Decision rules
- Match the existing component patterns and naming conventions in the codebase
- For new projects: default to React + TypeScript + Vite unless otherwise specified
- For styling: match existing approach (CSS modules, Tailwind, styled-components, etc.)
- Accessibility: all interactive elements need keyboard navigation and ARIA labels

## Output contract
- Components: typed props interface; exported as named export; includes basic JSDoc
- Includes: unit test stub if testing framework is configured

## Constraints
- NEVER use `any` type in TypeScript without a comment explaining why
- Scope boundary: backend API design belongs to architecture-specialist; CI/CD belongs to cicd-specialist

## Reference
- `references/legacy-agent.md`: component patterns, state management, accessibility checklist, performance optimization
