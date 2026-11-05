---
name: component
description: Generate UI component with component file, test, and story (optional)
type: scaffold
project_types: [web-app]
trigger: "create component, create component, add component"
inputs:
  - name: name
    description: Component name (PascalCase)
    required: true
  - name: type
    description: Component type (page, layout, ui, form, data-display)
    required: false
    default: "ui"
  - name: props
    description: Description of required props
    required: false
---

## Context

Project {{project_name}} uses {{stack}}.
Create component "{{input.name}}" of type {{input.type}}.

Read AGENTS.md for component conventions.
Read existing components to understand patterns (styling, state, testing).

## Instructions

1. **Analyze existing component patterns**
   - Check component directory structure
   - Identify: styling approach (CSS Modules, Tailwind, styled-components)
   - Identify: state management (useState, Zustand, Redux, etc.)
   - Identify: testing pattern (render tests, user-event, MSW)

2. **Create component file**
   - Path: according to project convention
     - `src/components/{{input.name}}/{{input.name}}.tsx`
     - or `src/components/{{input.name}}.tsx`
   - Props interface with TypeScript
   - Implement component according to type:
     - `ui`: presentational, props-driven
     - `form`: form state, validation, submit handler
     - `data-display`: data fetching, loading/error states
     - `layout`: children, responsive design
     - `page`: composition of other components

3. **Create barrel export** (if the project uses this pattern)
   - `src/components/{{input.name}}/index.ts`

4. **Create test file**
   - Path: co-located or in test directory
   - Tests:
     - Renders without crashing
     - Renders with different props
     - User interactions (click, type, etc)
     - Edge cases (empty data, long text, etc)

5. **Create story** (if the project uses Storybook)
   - Path: co-located `{{input.name}}.stories.tsx`
   - Default story + variants

## Validation

- [ ] Component renders without error
- [ ] TypeScript types correct (no any)
- [ ] Tests passing
- [ ] Styling consistent with existing components
- [ ] Accessible (semantic HTML, aria labels if needed)
- [ ] Responsive (if applicable)
