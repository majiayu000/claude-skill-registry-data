---
name: cms-component-builder
description: Build Optimizely CMS components for Astro v5. Use when creating/modifying components, pages, experiences, or working with GraphQL fragments, opti-type.json, or opti-style.json files (project)
---

# CMS Component Builder

Build production-ready Optimizely CMS components with proper GraphQL integration, daisyUI styling, and TypeScript type safety.

## When to Use This Skill

**ALWAYS use this skill when the user asks to:**
- Create a new component, page, or experience (e.g., "create a testimonial component", "add a new page type")
- Modify or update `.opti-type.json` files (content type definitions)
- Modify or update `.opti-style.json` files (style/display template definitions)
- Create or modify GraphQL fragments (`.graphql` or `.dam.graphql` files)
- Add components to `allComponents.graphql` or similar aggregation files
- Debug component rendering issues
- Fix GraphQL type errors related to components
- Push/sync content types or styles to the CMS
- Understand how the component system works

## Critical Instructions

**YOU MUST FOLLOW THESE STEPS IN ORDER:**

1. **READ THE GUIDES FIRST** - This skill includes comprehensive guides that YOU MUST reference:
   - `CONTENTTYPE-GUIDE.md` - For creating `.opti-type.json` files
   - `STYLE-GUIDE.md` - For creating `.opti-style.json` files
   - `GRAPHQL-PATTERNS.md` - For creating `.graphql` and `.dam.graphql` files

2. **EXAMINE EXISTING COMPONENTS** - Always look at similar existing components as examples before creating new ones. Check `src/cms/components/` for patterns.

3. **CREATE ALL REQUIRED FILES** - A complete component needs **5 files minimum**:
   - `.astro` - Component template with TypeScript
   - `.opti-type.json` - Content type definition
   - `.opti-style.json` - Style definition(s) (can have multiple)
   - `.graphql` - Base GraphQL fragment
   - `.dam.graphql` - DAM-enabled GraphQL fragment

4. **INTEGRATE PROPERLY** - After creating files:
   - Add fragment to `src/cms/components/allComponents.graphql`
   - Push to CMS: `yarn type:push ComponentName` and `yarn style:push StyleName`
   - Wait 10 seconds for Optimizely Graph sync
   - Generate types: `yarn codegen`

## Quick Start Example

Creating a new "Testimonial" component:

```bash
# 1. Create component directory
mkdir -p src/cms/components/TestimonialComponent

# 2. Create required files
src/cms/components/TestimonialComponent/
├── Testimonial.astro              # Component template
├── Testimonial.opti-type.json     # Content type definition
├── DefaultTestimonial.opti-style.json  # Default style
├── testimonial.graphql            # Base GraphQL fragment
└── testimonial.dam.graphql        # DAM GraphQL fragment
```

## Required Files Explained

Every component needs **at least 5 files**:

### 1. `.astro` - Component Template

**IMPORTANT**: Always follow the pattern from existing components like `Button.astro`

```typescript
---
import type {
    TestimonialFragment,
    DisplaySettingsFragment,
} from '../../../../__generated/sdk';
import type { ContentPayload } from '../../../graphql/shared/ContentPayload';
import { isEditContext } from '../../shared/utils.ts';

const isCmsEdit = isEditContext(Astro.url);

export interface Props {
    key: string;
    data: TestimonialFragment;
    displaySettings: DisplaySettingsFragment[];
    displayTemplateKey: string;
    contentPayload: ContentPayload;
}

const { key, data, displaySettings, displayTemplateKey, contentPayload } = Astro.props as Props;

// Your styling logic here - reference STYLE-GUIDE.md
const componentClass = 'component-testimonial';
---

<div data-epi-block-id={isCmsEdit && key || undefined} class={componentClass}>
    <div class="card bg-base-100 shadow-xl">
        <div class="card-body">
            <p class="text-lg italic" set:html={data.Quote?.html}></p>
            <div class="card-actions justify-end">
                <p class="font-bold">{data.Author}</p>
            </div>
        </div>
    </div>
</div>
```

**Key Points:**
- Import types from `__generated/sdk` (NOT from `@/graphql/__generated/graphql`)
- Include ALL required props: `key`, `data`, `displaySettings`, `displayTemplateKey`, `contentPayload`
- Use `data-epi-block-id` for CMS editing context
- Use `set:html` for rich text fields
- Add a component class for CSS targeting

### 2. `.opti-type.json` - Content Type
See `CONTENTTYPE-GUIDE.md` for complete guide on creating content types.

### 3. `.opti-style.json` - Style Definitions
See `STYLE-GUIDE.md` for complete guide on creating style definitions.

### 4. `.graphql` + `.dam.graphql` - GraphQL Fragments

**ALWAYS create both versions.** See `GRAPHQL-PATTERNS.md` for complete details.

**Base (`testimonial.graphql`):**
```graphql
fragment Testimonial on Testimonial {
    Quote { html }
    Author
    AuthorTitle
    AuthorImage {
        ...ContentUrl
    }
}
```

**DAM (`testimonial.dam.graphql`):**
```graphql
fragment Testimonial on Testimonial {
    Quote { html }
    Author
    AuthorTitle
    AuthorImage {
        ...ContentUrl
        ...ContentReferenceItem
    }
}
```

## Component Integration

### 1. Add to allComponents.graphql

```graphql
fragment AllComponentsExceptGrid on _IComponent {
    ...Text
    ...Button
    ...Testimonial  # Add your component here
}
```

**Important:** Add to `AllComponentsExceptGrid`, NOT `AllComponents`

### 2. Sync to CMS & Generate Types

```bash
# Push content type and styles to CMS
yarn type:push ComponentName
yarn style:push StyleName

# ⚠️ Wait ~10 seconds for Optimizely Graph to sync

# Then generate TypeScript types
yarn codegen
```

### 3. Verify Integration

Check `__generated/graphql.ts` for your component type.

## Component Locations

- **Components:** `src/cms/components/` - Reusable UI (Button, Card, Hero)
- **Pages:** `src/cms/pages/` - Page types (ArticlePage, LandingPage)
- **Experiences:** `src/cms/experiences/` - Experience templates
- **Compositions:** `src/cms/compositions/` - Layout elements (Row, Column)

## GraphQL Shared Fragments

Quick reference (full details in `GRAPHQL-PATTERNS.md`):

- `LinkUrl` - Links with url, title, target, text
- `ContentUrl` - Content reference URLs
- `LinkCollection` - Simple link arrays
- `ContentReferenceItem` - DAM metadata (`.dam.graphql` only)
- `DisplaySettings` - Display/styling settings
- `PageUrl` - Page metadata

**Rich text fields:** Always use `{ html }`:
```graphql
Body { html }
Description { html }
```

## Styling with daisyUI + TailwindCSS

**Prefer daisyUI components:**
```html
<button class="btn btn-primary btn-lg">
<div class="card card-compact">
<div class="hero min-h-screen">
```

**Use theme variables:**
```html
<div class="bg-base-100 text-base-content">
```

**Mobile-first responsive:**
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

## Complete Workflow (FOLLOW IN ORDER)

### Step 1: Research & Planning
1. **Ask the user for requirements**: What should this component do? What properties does it need?
2. **Find similar components**: Use `Glob` to find similar components in `src/cms/components/`
3. **Read example files**: Study at least one similar component to understand the patterns

### Step 2: Create Component Files

Create the component directory and all required files:

```bash
mkdir -p src/cms/components/ComponentNameComponent
cd src/cms/components/ComponentNameComponent
```

**Create these files in order:**

1. **`ComponentName.opti-type.json`** - Content type definition
   - Reference `CONTENTTYPE-GUIDE.md` for structure
   - Look at similar component's `.opti-type.json` as example
   - Set `baseType: "component"` for components
   - Set `compositionBehaviors: ["elementEnabled"]` for components usable in visual editor

2. **`DefaultComponentName.opti-style.json`** - Default style template
   - Reference `STYLE-GUIDE.md` for structure
   - Set `contentType` to match your component's key
   - Set `isDefault: true` for the default style
   - Create meaningful display settings with choices

3. **`componentName.graphql`** - Base GraphQL fragment
   - Reference `GRAPHQL-PATTERNS.md`
   - Fragment name must match component name (PascalCase)
   - Include all properties from `.opti-type.json`
   - Use shared fragments: `...LinkUrl`, `...ContentUrl`, etc.

4. **`componentName.dam.graphql`** - DAM-enabled GraphQL fragment
   - Copy from `componentName.graphql`
   - Add `...ContentReferenceItem` to content references
   - This enables DAM metadata for images/videos

5. **`ComponentName.astro`** - Component template
   - Follow the pattern from existing components (see example above)
   - Import types from `__generated/sdk`
   - Include all required props
   - Handle display settings for styling
   - Use daisyUI classes for styling

### Step 3: Integrate with System

1. **Add to allComponents.graphql**
   ```graphql
   # src/cms/components/allComponents.graphql
   fragment AllComponentsExceptGrid on _IComponent {
       ...ExistingComponent
       ...YourNewComponent  # Add this line
   }
   ```

2. **Push to CMS**
   ```bash
   # Push content type
   yarn type:push ComponentName

   # Push style template
   yarn style:push DefaultComponentName

   # ⚠️ CRITICAL: Wait 10-15 seconds for Optimizely Graph to sync
   ```

3. **Generate TypeScript Types**
   ```bash
   # After waiting for Graph sync
   yarn codegen
   ```

### Step 4: Verify & Test

1. **Check generated types** in `__generated/sdk.ts`:
   - Look for `ComponentNameFragment` type
   - Verify all properties are present

2. **Check for TypeScript errors**:
   ```bash
   yarn tsc --noEmit
   ```

3. **Test in dev server**:
   ```bash
   yarn dev
   ```

4. **Verify in CMS**:
   - Component appears in CMS UI
   - All properties are editable
   - Style options work correctly

## Verification Checklist

**YOU MUST CHECK ALL OF THESE before completing:**

- ✓ **All 5 required files created**:
  - `ComponentName.astro`
  - `ComponentName.opti-type.json`
  - `DefaultComponentName.opti-style.json`
  - `componentName.graphql`
  - `componentName.dam.graphql`

- ✓ **Content type (`.opti-type.json`) is valid**:
  - Has `key`, `displayName`, `baseType`
  - All properties defined correctly
  - Uses correct property types

- ✓ **Style template (`.opti-style.json`) is valid**:
  - Has `key`, `displayName`, `contentType`
  - `contentType` matches component key
  - Has `isDefault: true` for default style
  - All settings have choices

- ✓ **Both GraphQL fragments created**:
  - `.graphql` for base version
  - `.dam.graphql` with `...ContentReferenceItem` for DAM

- ✓ **Fragment added to `allComponents.graphql`**:
  - Added to `AllComponentsExceptGrid` (NOT `AllComponents`)

- ✓ **Pushed to CMS successfully**:
  - `yarn type:push ComponentName` completed
  - `yarn style:push StyleName` completed
  - Waited 10-15 seconds for Graph sync

- ✓ **Types generated successfully**:
  - `yarn codegen` completed without errors
  - `ComponentNameFragment` type exists in `__generated/sdk.ts`

- ✓ **Component template (`.astro`) follows patterns**:
  - Imports from `__generated/sdk`
  - Has all required props
  - Uses `data-epi-block-id` for CMS editing
  - Uses daisyUI classes for styling
  - Handles display settings

- ✓ **No TypeScript errors**:
  - `yarn tsc --noEmit` passes

- ✓ **Component works in dev server**:
  - `yarn dev` runs without errors

## Resources

All guides are bundled with this skill for quick reference:

- **GraphQL Patterns:** See `GRAPHQL-PATTERNS.md` for:
  - Complete fragment syntax and structure
  - DAM vs non-DAM differences
  - Real-world examples from existing components
  - Shared fragment catalog
  - Integration patterns

- **Content Type Creation:** See `CONTENTTYPE-GUIDE.md` for:
  - Content type structure and syntax
  - Property definitions and types
  - Display settings configuration
  - Real-world examples

- **Style Creation:** See `STYLE-GUIDE.md` for:
  - Style definition structure
  - Display settings mapping to CSS classes
  - daisyUI and TailwindCSS patterns
  - Responsive variants

## Common Patterns

**Component with links:**
```graphql
Links {
    ...LinkCollection
}
```

**Component with images:**
```graphql
# Base
Image {
    ...ContentUrl
}

# DAM
Image {
    ...ContentUrl
    ...ContentReferenceItem
}
```

**Component with metadata:**
```graphql
_metadata {
    types
    displayName
}
```

## Common Issues & Troubleshooting

### Issue: GraphQL fragment not found after codegen
**Solution:**
1. Check that fragment is added to `allComponents.graphql`
2. Ensure you pushed to CMS: `yarn type:push ComponentName`
3. Wait 10-15 seconds for Optimizely Graph to sync
4. Run `yarn codegen` again

### Issue: TypeScript errors in .astro file
**Solution:**
1. Verify imports are from `__generated/sdk` not `@/graphql/__generated/graphql`
2. Check that all Props interface fields are present
3. Run `yarn codegen` to regenerate types
4. Check that fragment name matches component name exactly (case-sensitive)

### Issue: Component doesn't appear in CMS
**Solution:**
1. Verify `yarn type:push ComponentName` completed successfully
2. Check that `baseType` is set correctly in `.opti-type.json`
3. Check that `compositionBehaviors: ["elementEnabled"]` is set
4. Clear CMS cache and refresh

### Issue: Display settings not working
**Solution:**
1. Verify `yarn style:push StyleName` completed successfully
2. Check that `contentType` in `.opti-style.json` matches component `key`
3. Ensure `isDefault: true` is set for default style
4. Verify style mapping exists in component's styling helper file

### Issue: Rich text fields not rendering HTML
**Solution:**
1. Use `set:html={data.FieldName?.html}` instead of `{data.FieldName.html}`
2. Ensure GraphQL fragment requests `{ html }` for rich text fields

### Issue: Content references (images/videos) not loading
**Solution:**
1. Check GraphQL fragment includes `...ContentUrl`
2. For DAM assets, verify `.dam.graphql` includes `...ContentReferenceItem`
3. Check that `url?.default` or `url?.hierarchical` is used in template

## Pages and Experiences

This skill also handles Pages and Experiences, which follow the same patterns:

**Pages** (`src/cms/pages/`):
- Set `baseType: "Page"` instead of `"Component"`
- Include SEO settings and page admin settings
- Add to appropriate page aggregation file
- May include `mayContainTypes` for content areas

**Experiences** (`src/cms/experiences/`):
- Define experience templates
- Include composition structure
- Reference Row, Column, and Section compositions

## Using Svelte 5 for Interactive Components

This project uses **Svelte 5** (latest version with runes) for client-side interactivity. Svelte components are primarily used for admin/utility interfaces, NOT for CMS components.

### When to Use Svelte

**Use Svelte for:**
- Admin interfaces (like `/opti-admin` pages)
- Interactive forms and utilities
- Complex client-side state management
- Real-time features (SSE, WebSockets)

**DO NOT use Svelte for:**
- CMS components (use `.astro` instead)
- Content rendering from Optimizely
- SEO-critical content

### Svelte 5 Key Patterns

**State Management with Runes:**
```svelte
<script lang="ts">
    // Props using $props() rune
    interface Props {
        title: string;
        count?: number;
    }
    let { title, count = 0 }: Props = $props();

    // Reactive state using $state() rune
    let currentCount = $state(0);
    let isLoading = $state(false);

    // Derived state using $derived rune
    let doubleCount = $derived(currentCount * 2);

    // Side effects using $effect rune
    $effect(() => {
        console.log('Count changed:', currentCount);
    });

    // Functions
    function increment() {
        currentCount++;
    }
</script>

<div>
    <h1>{title}</h1>
    <p>Count: {currentCount}</p>
    <p>Double: {doubleCount}</p>
    <button onclick={increment}>Increment</button>
</div>
```

**Important Svelte 5 Changes:**
- Use `$props()` instead of `export let`
- Use `$state()` instead of `let` for reactive variables
- Use `$derived` instead of `$:` for computed values
- Use `$effect()` instead of `$:` for side effects
- Use `onclick={}` instead of `on:click={}`
- Use `bind:value={}` for two-way binding

### Example: Admin Component with TypeScript

See `src/pages/opti-admin/components/_CmsSync.svelte` for a complete example showing:
- TypeScript interfaces with Props
- State management with `$state()` and `$derived`
- Event handling with EventSource (SSE)
- Lifecycle with `onMount()`
- Conditional rendering with `{#if}`
- List rendering with `{#each}`

### Embedding Svelte in Astro

```astro
---
// MyPage.astro
import MyCoolComponent from './_components/MyCoolComponent.svelte';

const someData = { title: 'Hello', count: 5 };
---

<div>
    <MyCoolComponent client:load title={someData.title} count={someData.count} />
</div>
```

**Client Directives:**
- `client:load` - Load immediately on page load
- `client:idle` - Load when browser is idle
- `client:visible` - Load when component is visible
- `client:only="svelte"` - Only run on client, no SSR

---

**Remember:** Every component must be production-ready with:
- Complete integration into the system
- Proper TypeScript types
- Consistent daisyUI styling
- Both GraphQL fragment versions (.graphql and .dam.graphql)
- Comprehensive verification before completion
