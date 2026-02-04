---
name: shadcn-ui-design-validator
description: Automatically validates frontend design patterns to prevent generic aesthetics (Inter fonts, purple gradients, minimal animations) and enforce distinctive, branded design during Tanstack Start (React) development with shadcn/ui
triggers: ["tsx file creation", "component changes", "tailwind config changes", "shadcn component usage", "design system updates"]
note: "Updated for Tanstack Start + shadcn/ui. Validates React/TSX components with shadcn/ui patterns."
---

# shadcn/ui Design Validator SKILL

## Activation Patterns

This SKILL automatically activates when:
- New `.tsx` React components are created
- Tailwind configuration (`tailwind.config.ts`) is modified
- Tanstack Start configuration (`app.config.ts`) is modified
- Component styling or classes are changed
- Design token definitions are updated
- Before deployment commands are executed

## Expertise Provided

### Design Pattern Validation
- **Generic Pattern Detection**: Identifies default/overused design patterns
- **Typography Analysis**: Ensures distinctive font choices and hierarchy
- **Animation Validation**: Checks for engaging micro-interactions and transitions
- **Color System**: Validates distinctive color palettes vs generic defaults
- **Component Customization**: Ensures shadcn/ui components are customized, not default

### Specific Checks Performed

#### ❌ Critical Violations (Generic Design Patterns)
```tsx
<!-- These patterns trigger alerts: -->

<!-- Generic font (Inter/Roboto) -->
<div className="font-sans">  <!-- Using default Inter -->

<!-- Purple gradient on white (overused pattern) -->
<div className="bg-gradient-to-r from-purple-500 to-purple-600">

<!-- No animations/transitions -->
<Button onClick="submit">Submit</Button>  <!-- No hover state -->

<!-- Default background colors -->
<div className="bg-gray-50">  <!-- Generic #f9fafb -->
```

#### ✅ Correct Distinctive Patterns
```tsx
<!-- These patterns are validated as correct: -->

<!-- Custom distinctive fonts -->
<h1 className="font-heading">  <!-- Custom font family -->

<!-- Custom brand colors -->
<div className="bg-brand-coral">  <!-- Distinctive palette -->

<!-- Engaging animations -->
<Button
  className="transition-all duration-300 hover:scale-105 hover:shadow-xl"
  onClick="submit"
>
  Submit
</Button>

<!-- Atmospheric backgrounds -->
<div className="bg-gradient-to-br from-brand-ocean via-brand-sky to-brand-coral">
```

## Integration Points

### Complementary to Existing Components
- **frontend-design-specialist agent**: Handles deep design analysis, SKILL provides immediate validation
- **tanstack-ui-architect agent**: Component expertise, SKILL validates implementation
- **es-design-review command**: SKILL provides continuous validation between explicit reviews

### Escalation Triggers
- Complex design system questions → `frontend-design-specialist` agent
- Component customization help → `tanstack-ui-architect` agent
- Accessibility concerns → `accessibility-guardian` agent
- Full design review → `/es-design-review` command

## Validation Rules

### P1 - Critical (Generic Patterns to Avoid)
- **Default Fonts**: Inter, Roboto, Helvetica (in over 80% of sites)
- **Purple Gradients**: `from-purple-*` to `to-purple-*` on white backgrounds
- **Generic Grays**: `bg-gray-50`, `bg-gray-100` (overused neutrals)
- **No Animations**: Interactive elements without hover/focus transitions
- **Default Component Props**: Using shadcn/ui components with all default props

### P2 - Important (Polish and Engagement)
- **Missing Hover States**: Buttons/links without hover effects
- **No Loading States**: Async actions without loading feedback
- **Inconsistent Spacing**: Not using Tailwind spacing scale consistently
- **No Micro-interactions**: Forms/buttons without feedback animations
- **Weak Typography Hierarchy**: Similar font sizes for different heading levels

### P3 - Best Practices
- **Font Weight Variety**: Using only one or two font weights
- **Limited Color Palette**: Not defining custom brand colors
- **No Custom Tokens**: Not extending Tailwind theme with brand values
- **Missing Dark Mode**: No dark mode variants (if applicable)

## Remediation Examples

### Fixing Generic Fonts
```tsx
<!-- ❌ Critical: Default Inter font -->
  <h1 className="text-4xl font-sans">Welcome</h1>

<!-- ✅ Correct: Distinctive custom font -->
  <h1 className="text-4xl font-heading tracking-tight">Welcome</h1>

<!-- tailwind.config.ts -->
export default {
  theme: {
    extend: {
      fontFamily: {
        // ❌ NOT: sans: ['Inter', 'sans-serif']
        // ✅ YES: Distinctive fonts
        sans: ['Space Grotesk', 'system-ui', 'sans-serif'],
        heading: ['Archivo Black', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace']
      }
    }
  }
}
```

### Fixing Generic Colors
```tsx
<!-- ❌ Critical: Purple gradient (overused) -->
  <div className="bg-gradient-to-r from-purple-500 to-purple-600">
    <h2 className="text-white">Hero Section</h2>
  </div>

<!-- ✅ Correct: Custom brand colors -->
  <div className="bg-gradient-to-br from-brand-coral via-brand-ocean to-brand-sunset">
    <h2 className="text-white">Hero Section</h2>
  </div>

<!-- tailwind.config.ts -->
export default {
  theme: {
    extend: {
      colors: {
        // ❌ NOT: Using only default Tailwind colors
        // ✅ YES: Custom brand palette
        brand: {
          coral: '#FF6B6B',
          ocean: '#4ECDC4',
          sunset: '#FFE66D',
          midnight: '#2C3E50',
          cream: '#FFF5E1'
        }
      }
    }
  }
}
```

### Fixing Missing Animations
```tsx
<!-- ❌ Critical: No hover/transition effects -->
  <Button onClick="handleSubmit">
    Submit Form
  </Button>

<!-- ✅ Correct: Engaging animations -->
  <Button
    className="transition-all duration-300 hover:scale-105 hover:shadow-xl active:scale-95"
    onClick="handleSubmit"
  >
    <span className="inline-flex items-center gap-2">
      Submit Form
      <Icon
        name="i-heroicons-arrow-right"
        className="transition-transform duration-300 group-hover:translate-x-1"
      />
    </span>
  </Button>
```

### Fixing Default Component Usage
```tsx
<!-- ❌ P2: All default props (generic appearance) -->
  <Card>
    <p>Content here</p>
  </Card>

<!-- ✅ Correct: Customized for brand distinctiveness -->
  <Card
    :ui="{
      background: 'bg-white dark:bg-brand-midnight',
      ring: 'ring-1 ring-brand-coral/20',
      rounded: 'rounded-2xl',
      shadow: 'shadow-xl hover:shadow-2xl',
      body: { padding: 'p-8' }
    }"
    className="transition-all duration-300 hover:-translate-y-1"
  >
    <p className="text-gray-700 dark:text-gray-300">Content here</p>
  </Card>
```

## MCP Server Integration

When shadcn/ui MCP server is available:
- Query component customization options before validation
- Verify that suggested customizations use valid props
- Get latest component API to prevent hallucination
- Validate `ui` prop structure against actual schema

**Example MCP Usage**:
```typescript
// Validate Button customization
const buttonDocs = await mcp.shadcn.get_component("Button");
// Check if suggested props exist: color, size, variant, ui, etc.
// Ensure customizations align with actual API
```

## Benefits

### Immediate Impact
- **Prevents Generic Design**: Catches overused patterns before they ship
- **Enforces Brand Identity**: Ensures consistent, distinctive aesthetics
- **Improves User Engagement**: Validates animations and interactions
- **Educates Developers**: Clear explanations of design best practices

### Long-term Value
- **Consistent Visual Identity**: All components follow brand guidelines
- **Faster Design Iterations**: Immediate feedback on design choices
- **Better User Experience**: Polished animations and interactions
- **Reduced Design Debt**: Prevents accumulation of generic patterns

## Usage Examples

### During Component Creation
```tsx
// Developer creates: <div className="font-sans bg-purple-500">
// SKILL immediately activates: "⚠️ WARNING: Using default 'font-sans' (Inter) and purple gradient. Consider custom brand fonts and colors for distinctive design."
```

### During Styling
```tsx
// Developer adds: <Button>Click me</Button>
// SKILL immediately activates: "⚠️ P2: Button lacks hover animations. Add transition utilities for better engagement: class='transition-all duration-300 hover:scale-105'"
```

### During Configuration
```typescript
// Developer modifies tailwind.config.ts with default Inter
// SKILL immediately activates: "⚠️ P1: Using Inter font (appears in 80%+ of sites). Replace with distinctive font choices like Space Grotesk, Archivo, or other brand-appropriate fonts."
```

### Before Deployment
```tsx
// SKILL runs comprehensive check: "✅ Design validation passed. Custom fonts, distinctive colors, engaging animations, and customized components detected."
```

## Design Philosophy Alignment

This SKILL implements the core insight from Claude's "Improving Frontend Design Through Skills" blog post:

> "Think about frontend design the way a frontend engineer would. The more you can map aesthetic improvements to implementable frontend code, the better Claude can execute."

**Key Mappings**:
- **Typography** → Tailwind `fontFamily` config + utility classes
- **Animations** → Tailwind `transition-*`, `hover:*`, `duration-*` utilities
- **Background effects** → Custom gradient combinations, `backdrop-*` utilities
- **Themes** → Extended Tailwind color palette with brand tokens

## Distinctive vs Generic Patterns

### ❌ Generic Patterns (What to Avoid)
```tsx
<!-- The "AI default aesthetic" -->
<div className="bg-white">
  <h1 className="font-sans text-gray-900">Title</h1>
  <div className="bg-gradient-to-r from-purple-500 to-purple-600">
    <Button>Action</Button>
  </div>
</div>
```

**Problems**:
- Inter font (default)
- Purple gradient (overused)
- Gray backgrounds (generic)
- No animations (flat)
- Default components (no customization)

### ✅ Distinctive Patterns (What to Strive For)
```tsx
<!-- Brand-distinctive aesthetic -->
<div className="bg-gradient-to-br from-brand-cream via-white to-brand-ocean/10">
  <h1 className="font-heading text-6xl text-brand-midnight tracking-tighter">
    Title
  </h1>
  <div className="relative overflow-hidden rounded-3xl bg-brand-coral p-8">
    <!-- Atmospheric background -->
    <div className="absolute inset-0 bg-gradient-to-br from-brand-coral to-brand-sunset opacity-80" />

    <Button
      :ui="{
        font: 'font-heading',
        rounded: 'rounded-full',
        size: 'xl'
      }"
      className="relative z-10 transition-all duration-500 hover:scale-110 hover:rotate-2 hover:shadow-2xl active:scale-95"
    >
      <span className="flex items-center gap-2">
        Action
        <Icon
          name="i-heroicons-sparkles"
          className="animate-pulse"
        />
      </span>
    </Button>
  </div>
</div>
```

**Strengths**:
- Custom fonts (Archivo Black for headings)
- Brand-specific colors (coral, ocean, sunset)
- Atmospheric gradients (multiple layers)
- Rich animations (scale, rotate, shadow transitions)
- Heavily customized components (ui prop + utility classes)
- Micro-interactions (icon pulse, hover effects)

This SKILL ensures every Tanstack Start project develops a distinctive visual identity by preventing generic patterns and guiding developers toward branded, engaging design implementations.
