---
name: dev-vue-component
description: Create, modify, and maintain Vue 3 components with TypeScript and SCSS. Use when building Vue components, modifying .vue files, defining component props/emits, styling with SCSS, or documenting component APIs. Handles component architecture, type safety, styling patterns, and documentation.
license: Apache-2.0
compatibility: Requires Vue 3, TypeScript, SCSS, UnoCSS.
metadata:
  author: xiaoland
  version: "1.0"
  related-skills: "vue-story"
---

# Developing Vue Components

## When to use this skill

Use this skill when you need to:

- Create new Vue 3 components from scratch
- Modify existing Vue components (template, logic, or styles)
- Define or update component props, emits, and TypeScript types
- Write or update component SCSS styles
- Document component APIs and usage
- Refactor components for better type safety or structure
- Review components for best practices compliance

## Component File Structure

- `compName.vue`: Template and component logic , read more in[vue-guide.md](references/vue-guide.md)
- `compName.ts`: Props, emits, types, constants (public API) read more in [typescript-guide.md](references/typescript-guide.md)
- `compName.scss`: Component styles, read more in [scss-guide.md](references/scss-guide.md)
- `compName.md`: Component documentation, read more in [documentation-guide.md](references/documentation-guide.md)

## Instructions

### Creating a New Component

Follow these steps to create a new Vue component:

1. **Create component folder**: `compName/`

2. **Document the component** (spec-first):
   - Create `compName.story.md` if using Histoire, otherwise create `compName.md`
   - Document intended props, emits, slots, and usage
   - Define component behavior and user interaction patterns
   - See [documentation-guide.md](references/documentation-guide.md) for format

3. **Define types and API** (`compName.ts`):
   - Define props interface with JSDoc comments
   - Define emits interface
   - Export types, constants, and utilities
   - See [typescript-guide.md](references/typescript-guide.md) for patterns

4. **Implement component logic** (`compName.vue`):
   - Import types from `compName.ts`
   - Use `<script setup>` with TypeScript
   - Implement component logic based on documented behavior
   - See [vue-guide.md](references/vue-guide.md) for structure

5. **Build template and styling** (`compName.vue` + `compName.scss`):
   - Implement template structure in `compName.vue`
   - Style the component in `compName.scss` using BEM or scoped styles
   - Avoid magic values, use CSS variables
   - See [scss-guide.md](references/scss-guide.md) for guidelines

### Modifying an Existing Component

1. **Understand current state**:
   - Read `compName.md` for component intent
   - Review existing implementation files

2. **Make changes**:
   - Update `compName.ts` if props/emits/types change
   - Update `compName.vue` for template or logic changes
   - Update `compName.scss` for styling changes
   - Consult reference docs as needed

3. **Update documentation**:
   - Update component documentation to reflect changes
   - Update tests if behavior changed (if tests exist)
   - Update stories if using Histoire (see vue-story skill)

4. **Verify consistency**:
   - Ensure all files are aligned
   - Check type safety (no `any` or `unknown`)
   - Verify tests pass (if tests exist)

### Quality Checklist

Before completing work on any component, verify:

- [ ] Type-safe props and emits with JSDoc documentation
- [ ] Component documentation is current and accurate
- [ ] Styles follow project patterns (no magic values)
- [ ] No hard-coded strings (use i18n if available)
- [ ] Tests updated and passing (if tests exist)
- [ ] Stories updated (if using Histoire - see vue-story skill)
- [ ] Code follows naming conventions (camelCase for JS, kebab-case for CSS/events)
- [ ] Error handling with graceful degradation

## Best Practices

Follow these principles for maintainable, high-quality components:

**Architecture**:

- Single Responsibility Principle - each component does one thing well
- High cohesion, low coupling - minimize dependencies
- Clear and consistent API design
- Avoid prop drilling - use provide/inject or composables for deep data
- Design for testability and maintainability

**Naming**:

- `camelCase` for component names, variables, functions, TypeScript interfaces
- `kebab-case` for CSS class names and event names
- Descriptive names that convey purpose

**Type Safety**:

- Always define props and emits interfaces
- Avoid `any` and `unknown` types
- Use JSDoc comments for props and emits
- Leverage TypeScript's inference when possible

**Error Handling**:

- Implement graceful degradation
- Provide user-friendly error messages
- Add appropriate console warnings/errors for developers
- Handle edge cases explicitly

---

**Note**:

- For detailed patterns and examples, consult the reference documentation in the `references/` directory.
- Starter templates are available in the `assets/` directory.
