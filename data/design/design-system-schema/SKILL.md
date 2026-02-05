---
name: design-system-schema
description: Defines comprehensive schemas for design token dimensions, value scales, and component mappings. Use when building design system taxonomies, organizing token categories, or establishing token dimension relationships and hierarchies.
---

# Design System Schema

## When to use this skill

Use this skill when you need to:
- Define design token dimension schemas and taxonomies
- Organize token categories (primitives, semantic, component-specific)
- Create value scales for colors, spacing, typography, and other properties
- Map dimensions to specific components
- Establish relationships between token dimensions
- Structure token metadata including types and scopes

## Schema structure

### Dimension categories

Design tokens are organized into three main categories:

#### 1. Primitives
Raw, foundational values that form the basis of the design system:
- **Colors**: Base color palettes with numeric scales
- **Spacing**: Numerical spacing values in consistent increments
- **Typography**: Font sizes, weights, families
- **Radius**: Border radius values
- **Opacity**: Transparency levels
- **Motion**: Animation duration and easing

#### 2. Semantic
Purpose-driven tokens that reference primitives:
- **Intent/Variant**: primary, secondary, success, warning, danger
- **State**: default, hover, active, disabled, focus
- **Theme**: light, dark, high-contrast
- **Role**: surface, text, border, background
- **Emphasis**: subtle, default, strong, inverse

#### 3. Component-specific
Tokens tailored for specific UI components:
- **Size**: xs, sm, md, lg, xl (contextual sizing)
- **Content**: text, icon, text-icon combinations
- **Hierarchy**: primary, secondary, tertiary priorities
- **Density**: compact, comfortable, spacious layouts

### Dimension structure

Each dimension follows this structure:
```javascript
{
  id: 'dimension-name',           // Unique identifier
  label: 'Display Name',          // Human-readable label
  column: 1,                      // UI organization column (1-3)
  enabled: true,                  // Whether dimension is active
  categories: ['semantic'],       // Which categories include this dimension
  values: ['value1', 'value2']    // Available values for this dimension
}
```

### Property values with metadata

Property dimensions include Figma variable metadata:
```javascript
{
  name: 'background-color',
  type: 'COLOR',                  // Figma variable type
  scopes: ['FRAME_FILL', 'SHAPE_FILL']  // Figma scopes
}
```

## Common dimension patterns

### Color scales (primitives)
```javascript
{
  id: 'colors',
  label: 'Colors',
  categories: ['primitives'],
  values: ['red', 'green', 'blue', 'neutral', 'purple']
}
```

Combined with scale values:
```javascript
{
  id: 'scale',
  label: 'Scale', 
  categories: ['primitives'],
  values: ['50', '100', '200', '300', '400', '500', '600', '700', '800', '900']
}
```

Generates: `red/500`, `neutral/100`, `blue/800`

### Spacing scales (primitives)
```javascript
{
  id: 'spacing',
  label: 'Spacing',
  categories: ['primitives'], 
  values: ['0', '4', '8', '12', '16', '24', '32', '48', '64', '80', '96']
}
```

Generates: `spacing/8`, `spacing/16`, `spacing/32`

### Semantic tokens
```javascript
{
  id: 'variant',
  label: 'Intent',
  categories: ['semantic'],
  values: ['primary', 'secondary', 'success', 'warning', 'danger']
},
{
  id: 'state', 
  label: 'State',
  categories: ['semantic'],
  values: ['default', 'hover', 'active', 'disabled', 'focus']
}
```

Generates: `primary/default`, `success/hover`, `warning/disabled`

### Component-specific dimensions
```javascript
{
  id: 'size',
  label: 'Size',
  categories: ['component-specific'],
  values: ['xs', 'sm', 'md', 'lg', 'xl']
},
{
  id: 'content',
  label: 'Content', 
  categories: ['component-specific'],
  values: ['text', 'icon', 'icon-text']
}
```

## Property definitions

Properties define the CSS attributes and their Figma mappings:

### Color properties
```javascript
{ name: 'background-color', type: 'COLOR', scopes: ['FRAME_FILL', 'SHAPE_FILL'] },
{ name: 'text-color', type: 'COLOR', scopes: ['TEXT_FILL'] },
{ name: 'border-color', type: 'COLOR', scopes: ['STROKE_COLOR'] }
```

### Sizing properties
```javascript
{ name: 'width', type: 'FLOAT', scopes: ['WIDTH_HEIGHT'] },
{ name: 'height', type: 'FLOAT', scopes: ['WIDTH_HEIGHT'] },
{ name: 'border-radius', type: 'FLOAT', scopes: ['CORNER_RADIUS'] }
```

### Typography properties  
```javascript
{ name: 'font-family', type: 'STRING', scopes: ['FONT_FAMILY'] },
{ name: 'font-size', type: 'FLOAT', scopes: ['FONT_SIZE'] },
{ name: 'font-weight', type: 'FLOAT', scopes: ['FONT_WEIGHT'] }
```

## Component mappings

Define which dimensions apply to specific components:

```javascript
components: {
  button: {
    label: 'Button',
    dimensions: ['variant', 'state', 'size', 'content', 'property']
  },
  card: {
    label: 'Card', 
    dimensions: ['elevation', 'theme', 'size', 'property']
  },
  input: {
    label: 'Input',
    dimensions: ['state', 'size', 'validation', 'property']
  }
}
```

## Value organization patterns

### Numerical progressions
- **Linear**: 4, 8, 12, 16, 20, 24 (consistent increments)
- **Exponential**: 2, 4, 8, 16, 32, 64 (powers of 2)
- **Tailwind-style**: 0, 1, 2, 4, 6, 8, 12, 16, 20, 24

### Scale-based systems
- **T-shirt sizes**: xs, sm, md, lg, xl, xxl
- **Numeric scales**: 100, 200, 300, 400, 500, 600, 700, 800, 900
- **Named scales**: none, subtle, default, strong, max

### State progressions
- **Interaction**: default, hover, active, disabled
- **Validation**: default, success, warning, error
- **Emphasis**: muted, default, strong, inverse

## Schema validation

Ensure your schema follows these patterns:

### Required fields
- `id`: Unique, kebab-case identifier
- `label`: Human-readable display name
- `categories`: Array of category membership
- `values`: Array of possible values

### Naming conventions
- Dimension IDs: kebab-case (variant, state, background-color)
- Value names: lowercase with hyphens (primary, light-blue, extra-large)
- Categories: hyphenated (component-specific, design-system)

### Relationships
- Property dimensions should include type/scope metadata
- Component mappings should reference existing dimension IDs
- Categories should align with design system taxonomy

## Examples

See [references/buttonSchema.js](references/buttonSchema.js) for a comprehensive schema example covering:
- 30+ predefined dimensions
- All three category types
- Complete property definitions with Figma metadata
- Component dimension mappings