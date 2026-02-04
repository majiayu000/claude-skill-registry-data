---
name: component-creator
description: Creates minimal boilerplate structure for new Web Components in Sando Design System following COMPONENT_ARCHITECTURE.md 7-file pattern. Generates only what developer requests - no assumptions, no dead code. Ask first, then scaffold component files, tests, stories based on requirements.
---

# Component Creator Skill

This skill generates **minimal boilerplate structure** for new Web Components following Sando's monolithic 7-file architecture. Creates **only what the developer explicitly requests** - no assumptions, no dead code to delete.

## Guidelines: Single Source of Truth

**CRITICAL**: All scaffolding MUST follow official Sando guidelines in `.claude/guidelines/`.

**Primary Guidelines for Scaffolding**:

- **02-architecture/COMPONENT_ARCHITECTURE.md** - 7-file monolithic pattern (MANDATORY structure)
- **03-development/NAMING_CONVENTIONS.md** - Component naming (sando-\*, PascalCase classes)
- **03-development/CODE_STYLE.md** - TypeScript conventions, imports, JSDoc
- **03-development/TESTING_STRATEGY.md** - Test file structure (unit + E2E + a11y)
- **06-documentation/STORYBOOK_STORIES.md** - Story structure and argTypes
- **06-documentation/API_REFERENCE.md** - JSDoc header format

**Full Index**: `.claude/guidelines/GUIDELINES_INDEX.md`

**Guideline Priority**:

1. **Sando Guidelines** - HIGHEST PRIORITY (structure from COMPONENT_ARCHITECTURE.md)
2. **User Requirements** - What developer explicitly requests (props, slots, variants)
3. **Minimal Defaults** - Only add if guideline requires it

## When to Use This Skill

Invoke when user requests:

- "Create a new component"
- "I need a Card component"
- "Scaffold a Modal component"
- Any request to generate component boilerplate

## Step 1: Ask What Developer Needs

Use AskUserQuestion tool. **DO NOT assume anything.**

**Questions (in order)**:

1. **Component name** (required)
   - Example: "card", "modal", "input"
   - Validate: lowercase, alphanumeric, may contain hyphens

2. **Does this component need variants?**
   - If YES: "What variants?" (e.g., "solid, outline, ghost")
   - If NO: Don't add variant property

3. **Does this component need sizes?**
   - If YES: "What sizes?" (e.g., "small, medium, large")
   - If NO: Don't add size property

4. **What props does this component need?**
   - Examples: "open, onClose" for Modal
   - If none: Only basic structure

5. **What events should this component emit?**
   - Examples: "modal-open, modal-close"
   - If none: Don't add event handling

6. **What slots does this component need?**
   - Examples: "header, content, footer" for Modal
   - If only default: Only include default slot

7. **Brief description** (1-2 sentences)
   - Example: "A modal dialog component for overlay content"

## Step 2: Validate Requirements Against Guidelines

Before generating:

1. Read **COMPONENT_ARCHITECTURE.md** (lines X-Y: 7-file structure)
2. Read **NAMING_CONVENTIONS.md** (lines X-Y: component naming rules)
3. Validate:
   - Component name follows kebab-case per NAMING_CONVENTIONS.md
   - Class name: `Sando{PascalCase}` per guideline
   - HTML tag: `sando-{name}` per guideline

## Step 3: Generate 7 Files (COMPONENT_ARCHITECTURE.md Pattern)

Generate **only requested code** following guidelines:

### File 1: `sando-{name}.types.ts`

```typescript
/**
 * Type definitions for sando-{name} component
 * @see COMPONENT_ARCHITECTURE.md
 */

// Only include if variants requested
{{#if HAS_VARIANTS}}
export type {{COMPONENT_CLASS}}Variant = {{VARIANTS}};
{{/if}}

// Only include if sizes requested
{{#if HAS_SIZES}}
export type {{COMPONENT_CLASS}}Size = {{SIZES}};
{{/if}}

// Always include props interface (minimal)
export interface Sando{{COMPONENT_CLASS}}Props {
  {{#if HAS_VARIANTS}}
  variant?: {{COMPONENT_CLASS}}Variant;
  {{/if}}
  {{#if HAS_SIZES}}
  size?: {{COMPONENT_CLASS}}Size;
  {{/if}}
  {{#each PROPS}}
  {{this.name}}?: {{this.type}};
  {{/each}}
}

// Only include if events requested
{{#if HAS_EVENTS}}
export interface {{COMPONENT_CLASS}}EventDetail {
  // TODO: Define event payload
}
{{/if}}
```

### File 2: `sando-{name}.ts`

```typescript
import { LitElement, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';
import type { Sando{{COMPONENT_CLASS}}Props } from './sando-{{COMPONENT_NAME}}.types';

/**
 * @tag sando-{{COMPONENT_NAME}}
 * @summary {{COMPONENT_DESCRIPTION}}
 * @see API_REFERENCE.md for JSDoc standards
 *
 * @slot - Default slot content
 * {{#each SLOTS}}
 * @slot {{this}} - {{this}} content
 * {{/each}}
 */
@customElement('sando-{{COMPONENT_NAME}}')
export class Sando{{COMPONENT_CLASS}} extends LitElement implements Sando{{COMPONENT_CLASS}}Props {
  // TODO: Add Recipe tokens when ready (var(--sando-{{COMPONENT_NAME}}-*))
  // static styles = css``;

  {{#if HAS_VARIANTS}}
  @property({ type: String, reflect: true })
  variant: {{COMPONENT_CLASS}}Variant = {{DEFAULT_VARIANT}};
  {{/if}}

  {{#if HAS_SIZES}}
  @property({ type: String, reflect: true })
  size: {{COMPONENT_CLASS}}Size = {{DEFAULT_SIZE}};
  {{/if}}

  {{#each PROPS}}
  @property({ type: {{this.propertyType}}, reflect: {{this.reflect}} })
  {{this.name}}{{#if this.optional}}?{{/if}}: {{this.type}};
  {{/each}}

  render() {
    return html`
      <!-- TODO: Implement component template -->
      <slot></slot>
      {{#each SLOTS}}
      <slot name="{{this}}"></slot>
      {{/each}}
    `;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    'sando-{{COMPONENT_NAME}}': Sando{{COMPONENT_CLASS}};
  }
}
```

### Files 3-5: Tests (TESTING_STRATEGY.md pattern)

**`sando-{name}.test.ts`** - Unit tests
**`sando-{name}.spec.ts`** - E2E tests (Playwright) - TODO by developer
**`sando-{name}.a11y.test.ts`** - Accessibility tests (axe-core)

### File 6: `sando-{name}.stories.ts`

Follow **STORYBOOK_STORIES.md** structure per guideline.

### File 7: `index.ts` - Barrel export

```typescript
export { Sando{{COMPONENT_CLASS}} } from './sando-{{COMPONENT_NAME}}';
export type * from './sando-{{COMPONENT_NAME}}.types';
```

## Step 4: Create VitePress Documentation Placeholder

Per **API_REFERENCE.md** format.

## Step 5: Update Package Exports

Add to `packages/components/src/index.ts`:

```typescript
export * from "./components/{{COMPONENT_NAME}}";
```

## Step 6: Inform Developer

```
✅ Component scaffolded per COMPONENT_ARCHITECTURE.md (7-file pattern)

📁 Location: packages/components/src/components/{{COMPONENT_NAME}}/

📄 Files Created:
  ✅ sando-{{COMPONENT_NAME}}.ts (minimal Lit structure)
  ✅ sando-{{COMPONENT_NAME}}.types.ts (only requested types)
  ✅ sando-{{COMPONENT_NAME}}.test.ts (unit tests)
  ✅ sando-{{COMPONENT_NAME}}.spec.ts (E2E tests - TODO)
  ✅ sando-{{COMPONENT_NAME}}.a11y.test.ts (a11y tests)
  ✅ sando-{{COMPONENT_NAME}}.stories.ts (Storybook)
  ✅ index.ts (barrel export)

📝 Documentation:
  ✅ apps/site/components/{{COMPONENT_NAME}}.md (placeholder)

✅ Package exports updated

⚠️  Next Steps (per guidelines):

1. **Create Recipe Tokens** (TOKEN_ARCHITECTURE.md)
   - Create: packages/tokens/src/recipes/{{COMPONENT_NAME}}.json
   - Reference ONLY Flavors: {color.*}, {space.*}
   - Rebuild: `pnpm tokens:build`

2. **Add Styles** (CODE_STYLE.md)
   - Edit: sando-{{COMPONENT_NAME}}.ts
   - Use Recipe tokens: var(--sando-{{COMPONENT_NAME}}-*)

3. **Complete Tests** (TESTING_STRATEGY.md)
   - Target: >85% unit coverage, 100% a11y
   - Run: `pnpm --filter @sando/components test`

4. **Complete Documentation** (API_REFERENCE.md + VITEPRESS_GUIDES.md)
   - Fill API tables in {{COMPONENT_NAME}}.md
   - Add usage examples

📚 Guidelines: `.claude/guidelines/GUIDELINES_INDEX.md`
```

## Important Rules

**DO**:

- ✅ Ask first, generate only requested features
- ✅ Follow COMPONENT_ARCHITECTURE.md 7-file structure EXACTLY
- ✅ Use NAMING_CONVENTIONS.md for all names
- ✅ Add TODO comments for developer to complete
- ✅ Reference guidelines in generated comments

**DO NOT**:

- ❌ Add variants/sizes not requested
- ❌ Add CSS styles by default (developer adds when tokens ready)
- ❌ Generate code that violates guidelines
- ❌ Assume component behavior
