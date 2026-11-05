---
name: scaffold-webapp
description: Setup web app page with component, layout, data fetching, and tests
type: scaffold
project_types: [web-app]
trigger: "create page, create page, add new page"
inputs:
  - name: name
    description: Page name (e.g. dashboard, profile, settings)
    required: true
  - name: route
    description: URL path for this page
    required: false
    default: "/{{input.name}}"
  - name: layout
    description: Layout to use (e.g. main, auth, admin)
    required: false
    default: "main"
---

## Context

Project {{project_name}} is a web app using {{stack}}.
You will create a new page "{{input.name}}" at route "{{input.route}}".

Read AGENTS.md for conventions. Read existing pages to understand patterns.

## Instructions

1. **Analyze existing page patterns**
   - Read existing pages
   - Identify: file structure, layout usage, data fetching pattern, state management
   - Note naming conventions (PascalCase, kebab-case, etc.)

2. **Create page component**
   - Path: according to framework convention
     - Next.js App Router: `app/{{input.route}}/page.tsx`
     - Next.js Pages: `pages/{{input.route}}.tsx`
     - React Router: `src/pages/{{input.name}}.tsx`
   - Use layout "{{input.layout}}"
   - Implement basic structure: header, content area, loading state, error state

3. **Create sub-components** (if page is complex)
   - Break into reusable components
   - Path: `src/components/{{input.name}}/`
   - Each component: file + test

4. **Setup data fetching**
   - Follow existing patterns (SSR, client-side, React Query, SWR, etc.)
   - Create mock data for development

5. **Create tests**
   - Render test (component mounts without error)
   - Interaction tests (click, form submit, navigation)
   - Data fetching tests (loading, success, error states)

6. **Update navigation** (if applicable)
   - Add link to the new page in navbar/sidebar

## Script

```bash
#!/bin/bash
# Detect framework routing
if [ -d "app" ] && [ -f "next.config.mjs" -o -f "next.config.js" -o -f "next.config.ts" ]; then
  echo "Framework: Next.js App Router"
  echo "Page path: app/{{input.route}}/page.tsx"
elif [ -d "pages" ] && [ -f "next.config.mjs" -o -f "next.config.js" -o -f "next.config.ts" ]; then
  echo "Framework: Next.js Pages Router"
  echo "Page path: pages/{{input.route}}.tsx"
elif [ -d "src/pages" ]; then
  echo "Framework: React (Pages pattern)"
  echo "Page path: src/pages/{{input.name}}.tsx"
fi
```

## Validation

- [ ] Page component renders without error
- [ ] Route accessible in browser (dev server)
- [ ] Layout applied correctly
- [ ] Loading state works
- [ ] Error state works
- [ ] Tests passing
- [ ] Typecheck passing
- [ ] Navigation updated (if applicable)
