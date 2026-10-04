---
name: build-component
description: Build a premium UI component following design system
argument-hint: <component-name-and-description>
---

# Component Build Protocol

1. Check if similar component exists in codebase
2. Define props interface with TypeScript (strict, no `any`)
3. Implement with: shadcn/ui base + custom styling
4. Add ALL states: loading, error, empty, populated
5. Add Framer Motion animations (enter, hover, exit)
6. Ensure WCAG 2.1 AA accessibility
7. Add keyboard navigation support
8. Test at 375px, 768px, 1024px, 1440px, 1920px
9. Write unit test with React Testing Library
10. Export from components/ui/index.ts barrel file
