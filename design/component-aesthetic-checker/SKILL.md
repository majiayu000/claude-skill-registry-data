---
name: component-aesthetic-checker
description: Validates shadcn/ui component customization depth, ensuring components aren't used with default props and checking for consistent design system implementation across Tanstack Start applications
triggers: ["shadcn ui component usage", "component prop changes", "design token updates", "className customization", "cn() utility usage"]
note: "Updated for Tanstack Start (React) + shadcn/ui. Code examples use React/TSX with className and cn() utility for styling."
---

# Component Aesthetic Checker SKILL

## Activation Patterns

This SKILL automatically activates when:
- shadcn/ui components (`Button`, `Card`, `Input`, etc.) are used in `.react` files
- Component props are added or modified
- The `ui` prop is customized for component variants
- Design system tokens are referenced in components
- Multiple components are refactored together
- Before component library updates

## Expertise Provided

### Component Customization Depth Analysis
- **Default Prop Detection**: Identifies components using only default values
- **UI Prop Validation**: Ensures `ui` prop is used for deep customization
- **Design System Consistency**: Validates consistent pattern usage across components
- **Spacing Patterns**: Checks for proper Tailwind spacing scale usage
- **Icon Usage**: Validates consistent icon library and sizing
- **Loading States**: Ensures async components have loading feedback

### Specific Checks Performed

#### ❌ Critical Issues (Insufficient Customization)
```tsx
<!-- These patterns trigger alerts: -->

<!-- Using default props only -->
<Button onClick="submit">Submit</Button>

<!-- No UI prop customization -->
<Card>
  <p>Content</p>
</Card>

<!-- Inconsistent spacing -->
<div className="p-4">  <!-- Random spacing values -->
  <Button className="mt-3 ml-2">Action</Button>
</div>

<!-- Missing loading states -->
<Button onClick="asyncAction">Save</Button>  <!-- No :loading prop -->
```

#### ✅ Correct Customized Patterns
```tsx
<!-- These patterns are validated as correct: -->

<!-- Deep customization with ui prop -->
<Button
  color="brand-coral"
  size="lg"
  variant="solid"
  :ui="{
    font: 'font-heading',
    rounded: 'rounded-full',
    padding: { lg: 'px-8 py-4' }
  }"
  loading={isSubmitting"
  className="transition-all duration-300 hover:scale-105"
  onClick="submit"
>
  Submit
</Button>

<!-- Fully customized card -->
<Card
  :ui="{
    background: 'bg-white dark:bg-brand-midnight',
    ring: 'ring-1 ring-brand-coral/20',
    rounded: 'rounded-2xl',
    shadow: 'shadow-xl',
    body: { padding: 'p-8' },
    header: { padding: 'px-8 pt-8 pb-4' }
  }"
  className="transition-shadow duration-300 hover:shadow-2xl"
>
  <template #header>
    <h3 className="font-heading text-2xl">Title</h3>
  <p className="text-gray-700 dark:text-gray-300">Content</p>
</Card>

<!-- Consistent spacing (Tailwind scale) -->
<div className="p-6 space-y-4">
  <Button className="mt-4">Action</Button>
</div>

<!-- Proper loading state -->
<Button
  loading={isSubmitting"
  disabled={isSubmitting"
  onClick="asyncAction"
>
  { isSubmitting ? 'Saving...' : 'Save'}
</Button>
```

## Integration Points

### Complementary to Existing Components
- **tanstack-ui-architect agent**: Handles component selection and API guidance, SKILL validates implementation
- **frontend-design-specialist agent**: Provides design direction, SKILL enforces consistency
- **shadcn-ui-design-validator**: Catches generic patterns, SKILL ensures deep customization

### Escalation Triggers
- Component API questions → `tanstack-ui-architect` agent (with MCP lookup)
- Design consistency issues → `frontend-design-specialist` agent
- Complex component composition → `/es-component` command
- Full component audit → `/es-design-review` command

## Validation Rules

### P1 - Critical (Default Component Usage)
- **No UI Prop Customization**: Using shadcn/ui components without `ui` prop
- **All Default Props**: No color, size, variant, or other prop customizations
- **Missing Loading States**: Async actions without `:loading` prop
- **No Hover States**: Interactive components without hover feedback
- **Inconsistent Patterns**: Same component with wildly different customizations

### P1 - Critical (Distributional Convergence Anti-Patterns)

**These patterns indicate generic "AI-generated" aesthetics and MUST be flagged:**

#### Font Anti-Patterns (Auto-Detect)
```tsx
// ❌ CRITICAL: Generic fonts that dominate 80%+ of websites
fontFamily: {
  sans: ['Inter', ...]        // Flag: "Inter is overused - consider Space Grotesk, Plus Jakarta Sans"
  sans: ['Roboto', ...]       // Flag: "Roboto is overused - consider IBM Plex Sans, Outfit"
  sans: ['Open Sans', ...]    // Flag: "Open Sans is generic - consider Satoshi, General Sans"
  sans: ['system-ui', ...]    // Flag: Only acceptable as fallback, not primary
}

// ❌ CRITICAL: Default Tailwind font classes without customization
className="font-sans"         // Flag if font-sans maps to Inter/Roboto
className="text-base"         // Flag: Generic sizing, consider custom scale
```

**Recommended Font Alternatives** (suggest these in reports):
- **Body**: Space Grotesk, Plus Jakarta Sans, IBM Plex Sans, Outfit, Satoshi
- **Headings**: Archivo Black, Cabinet Grotesk, Clash Display, General Sans
- **Mono**: JetBrains Mono, Fira Code, Source Code Pro

#### Color Anti-Patterns (Auto-Detect)
```tsx
// ❌ CRITICAL: Purple gradients (most common AI aesthetic)
className="bg-gradient-to-r from-purple-500 to-purple-600"
className="bg-gradient-to-r from-violet-500 to-purple-500"
className="bg-purple-600"
className="text-purple-500"

// ❌ CRITICAL: Default gray backgrounds without brand treatment
className="bg-gray-50"        // Flag: "Consider brand-tinted background"
className="bg-white"          // Flag: "Consider atmospheric gradient or texture"
className="bg-slate-100"      // Flag if used extensively without brand colors
```

**Recommended Color Approaches** (suggest these in reports):
- Use CSS variables with brand palette (`--brand-primary`, `--brand-accent`)
- Tint grays with brand color: `bg-brand-gray-50` instead of `bg-gray-50`
- Gradients: Use brand colors, not default purple
- Atmospheric: Layer gradients with subtle brand tints

#### Animation Anti-Patterns (Auto-Detect)
```tsx
// ❌ CRITICAL: No transitions on interactive elements
<Button>Click</Button>        // Flag: "Add transition-all duration-300"
<Card>Content</Card>          // Flag: "Add hover:shadow-lg transition"

// ❌ CRITICAL: Only basic hover without micro-interactions
className="hover:bg-blue-600" // Flag: "Consider hover:scale-105 or hover:-translate-y-1"
```

**Detection Rules** (implement in validation):
```typescript
// Font detection
const OVERUSED_FONTS = ['Inter', 'Roboto', 'Open Sans', 'Helvetica', 'Arial'];
const hasBadFont = (config) => OVERUSED_FONTS.some(f =>
  config.fontFamily?.sans?.includes(f)
);

// Purple gradient detection
const PURPLE_PATTERN = /(?:purple|violet)-[4-6]00/;
const hasPurpleGradient = (className) =>
  className.includes('gradient') && PURPLE_PATTERN.test(className);

// Missing animation detection
const INTERACTIVE_COMPONENTS = ['Button', 'Card', 'Link', 'Input'];
const hasNoTransition = (className) =>
  !className.includes('transition') && !className.includes('animate');
```

### P2 - Important (Design System Consistency)
- **Random Spacing Values**: Not using Tailwind spacing scale (p-4, mt-6, etc.)
- **Inconsistent Icon Sizing**: Icons with different sizes in similar contexts
- **Mixed Color Approaches**: Some components use theme colors, others use arbitrary values
- **Incomplete Dark Mode**: Dark mode variants missing on customized components
- **No Focus States**: Interactive elements without focus-visible styling

### P3 - Polish (Enhanced UX)
- **Limited Prop Usage**: Only using 1-2 props when more would improve UX
- **No Micro-interactions**: Missing subtle animations on state changes
- **Generic Variants**: Using 'solid', 'outline' without brand customization
- **Underutilized UI Prop**: Not customizing padding, rounded, shadow in ui prop
- **Missing Icons**: Buttons/actions without supporting icons for clarity

## Remediation Examples

### Fixing Default Component Usage
```tsx
<!-- ❌ Critical: Default props only -->
  <Button onClick="handleClick">
    Click me
  </Button>

<!-- ✅ Correct: Deep customization -->
  <Button
    color="primary"
    size="lg"
    variant="solid"
    icon="i-heroicons-sparkles"
    :ui="{
      font: 'font-heading tracking-wide',
      rounded: 'rounded-full',
      padding: { lg: 'px-8 py-4' },
      shadow: 'shadow-lg hover:shadow-xl'
    }"
    className="transition-all duration-300 hover:scale-105 active:scale-95"
    onClick="handleClick"
  >
    Click me
  </Button>
```

### Fixing Missing Loading States
```tsx
<!-- ❌ Critical: No loading feedback -->
const handleSubmit = async () => {
  await submitForm();
};

  <Button onClick="handleSubmit">
    Submit Form
  </Button>

<!-- ✅ Correct: Proper loading state -->
const isSubmitting = ref(false);

const handleSubmit = async () => {
  isSubmitting.value = true;
  try {
    await submitForm();
  } finally {
    isSubmitting.value = false;
  }
};

  <Button
    loading={isSubmitting"
    disabled={isSubmitting"
    onClick="handleSubmit"
  >
    <span className="flex items-center gap-2">
      <Icon
        {&& "!isSubmitting"
        name="i-heroicons-paper-airplane"
      />
      { isSubmitting ? 'Submitting...' : 'Submit Form'}
    </span>
  </Button>
```

### Fixing Inconsistent Spacing
```tsx
<!-- ❌ P2: Random spacing values -->
  <div className="p-3">
    <Card className="mt-5 ml-7">
      <div className="p-2">
        <Button className="mt-3.5">Action</Button>
      </div>
    </Card>
  </div>

<!-- ✅ Correct: Tailwind spacing scale -->
  <div className="p-4">
    <Card className="mt-4">
      <div className="p-6 space-y-4">
        <Button>Action</Button>
      </div>
    </Card>
  </div>

<!-- Using consistent spacing: 4, 6, 8, 12, 16 (Tailwind scale) -->
```

### Fixing Design System Inconsistency
```tsx
<!-- ❌ P2: Inconsistent component styling -->
  <div>
    <!-- Button 1: Heavily customized -->
    <Button
      color="primary"
      :ui="{ rounded: 'rounded-full', shadow: 'shadow-xl' }"
    >
      Action 1
    </Button>

    <!-- Button 2: Default (inconsistent!) -->
    <Button>Action 2</Button>

    <!-- Button 3: Different customization pattern -->
    <Button color="red" size="xs">
      Action 3
    </Button>
  </div>

<!-- ✅ Correct: Consistent design system -->
// Define reusable button variants
const buttonVariants = {
  primary: {
    color: 'primary',
    size: 'lg',
    ui: {
      rounded: 'rounded-full',
      shadow: 'shadow-lg hover:shadow-xl',
      font: 'font-heading'
    },
    class: 'transition-all duration-300 hover:scale-105'
  },
  secondary: {
    color: 'gray',
    size: 'md',
    variant: 'outline',
    ui: {
      rounded: 'rounded-lg',
      font: 'font-sans'
    },
    class: 'transition-colors duration-200'
  }
};

  <div className="space-x-4">
    <Button v-bind="buttonVariants.primary">
      Action 1
    </Button>

    <Button v-bind="buttonVariants.primary">
      Action 2
    </Button>

    <Button v-bind="buttonVariants.secondary">
      Action 3
    </Button>
  </div>
```

### Fixing Underutilized UI Prop
```tsx
<!-- ❌ P3: Not using ui prop for customization -->
  <Card className="rounded-2xl shadow-xl p-8">
    <p>Content</p>
  </Card>

<!-- ✅ Correct: Proper ui prop usage -->
  <Card
    :ui="{
      rounded: 'rounded-2xl',
      shadow: 'shadow-xl hover:shadow-2xl',
      body: {
        padding: 'p-8',
        background: 'bg-white dark:bg-brand-midnight'
      },
      ring: 'ring-1 ring-brand-coral/20'
    }"
    className="transition-shadow duration-300"
  >
    <p className="text-gray-700 dark:text-gray-300">Content</p>
  </Card>
```

## MCP Server Integration

When shadcn/ui MCP server is available:

### Component Prop Validation
```typescript
// Before validating customization depth, get actual component API
const componentDocs = await mcp.shadcn.get_component("Button");

// Validate that used props exist
// componentDocs.props: ['color', 'size', 'variant', 'icon', 'loading', 'disabled', ...]

// Check for underutilized props
const usedProps = ['color', 'size']; // From component code
const availableProps = componentDocs.props;
const unutilizedProps = availableProps.filter(p => !usedProps.includes(p));

// Suggest: "Consider using 'icon' or 'loading' props for richer UX"
```

### UI Prop Structure Validation
```typescript
// Validate ui prop structure against schema
const uiSchema = componentDocs.ui_schema;

// User code: :ui="{ font: 'font-heading', rounded: 'rounded-full' }"
// Validate: Are 'font' and 'rounded' valid keys in ui prop?
// Suggest: Other available ui customizations (padding, shadow, etc.)
```

### Consistency Across Components
```typescript
// Check multiple component instances
const buttonInstances = findAllComponents("Button");

// Analyze customization patterns
// Flag: Component used with 5 different customization styles
// Suggest: Create composable or variant system for consistency
```

## Benefits

### Immediate Impact
- **Prevents Generic Appearance**: Ensures components are branded, not defaults
- **Enforces Design Consistency**: Catches pattern drift across components
- **Improves User Feedback**: Validates loading states and interactions
- **Educates on Component API**: Shows developers full customization capabilities

### Long-term Value
- **Consistent Component Library**: All components follow design system
- **Faster Component Development**: Clear patterns and examples
- **Better Code Maintainability**: Reusable component variants
- **Reduced Visual Debt**: Prevents accumulation of one-off styles

## Usage Examples

### During Component Usage
```tsx
// Developer adds: <Button>Click me</Button>
// SKILL immediately activates: "⚠️ P1: Button using all default props. Customize with color, size, variant, and ui prop for brand distinctiveness."
```

### During Async Actions
```tsx
// Developer creates async button: <Button onClick="submitForm">Submit</Button>
// SKILL immediately activates: "⚠️ P1: Button triggers async action but lacks :loading prop. Add loading state for user feedback."
```

### During Refactoring
```tsx
// Developer adds 5th different button style
// SKILL immediately activates: "⚠️ P2: Button used with 5 different customization patterns. Consider creating reusable variants for consistency."
```

### Before Deployment
```tsx
// SKILL runs comprehensive check: "✅ Component aesthetic validation passed. 23 components with deep customization, consistent patterns, and proper loading states detected."
```

## Design System Maturity Levels

### Level 0: Defaults Only (Avoid)
```tsx
<Button>Action</Button>
<Card><p>Content</p></Card>
<Input value="value" />
```
**Issues**: Generic appearance, no brand identity, inconsistent with custom design

### Level 1: Basic Props (Minimum)
```tsx
<Button color="primary" size="lg">Action</Button>
<Card className="shadow-lg"><p>Content</p></Card>
<Input value="value" placeholder="Enter value" />
```
**Better**: Some customization, but limited depth

### Level 2: UI Prop + Classes (Target)
```tsx
<Button
  color="primary"
  size="lg"
  :ui="{ rounded: 'rounded-full', font: 'font-heading' }"
  className="transition-all duration-300 hover:scale-105"
>
  Action
</Button>

<Card
  :ui="{
    background: 'bg-white dark:bg-brand-midnight',
    ring: 'ring-1 ring-brand-coral/20',
    shadow: 'shadow-xl'
  }"
>
  <p>Content</p>
</Card>
```
**Ideal**: Deep customization, brand-distinctive, consistent patterns

### Level 3: Design System (Advanced)
```tsx
<!-- Reusable variants from composables -->
<Button v-bind="designSystem.button.variants.primary">
  Action
</Button>

<Card v-bind="designSystem.card.variants.elevated">
  <p>Content</p>
</Card>
```
**Advanced**: Centralized design system, maximum consistency

## Component Customization Checklist

For each shadcn/ui component, validate:

- [ ] **Props**: Uses at least 2-3 props (color, size, variant, etc.)
- [ ] **UI Prop**: Includes `ui` prop for deep customization (rounded, font, padding, shadow)
- [ ] **Classes**: Adds Tailwind utilities for animations and effects
- [ ] **Loading State**: Async actions have `:loading` and `:disabled` props
- [ ] **Icons**: Includes relevant icons for clarity (`:icon` prop or slot)
- [ ] **Hover State**: Interactive elements have hover feedback
- [ ] **Focus State**: Keyboard navigation has visible focus styles
- [ ] **Dark Mode**: Includes dark mode variants in `ui` prop
- [ ] **Spacing**: Uses Tailwind spacing scale (4, 6, 8, 12, 16)
- [ ] **Consistency**: Follows same patterns as other instances

This SKILL ensures every shadcn/ui component is deeply customized, consistently styled, and provides excellent user feedback, preventing the default/generic appearance that makes AI-generated UIs immediately recognizable.
