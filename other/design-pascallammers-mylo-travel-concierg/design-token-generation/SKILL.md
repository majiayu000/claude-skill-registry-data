---
name: design-token-generation
description: Generates design tokens from multi-dimensional configurations, creating hierarchical token names with proper naming conventions. Use when building design systems, creating token sets from component schemas, or generating token combinations from dimensions like variant, state, size, and properties.
---

# Design Token Generation

## When to use this skill

Use this skill when you need to:
- Generate design tokens from component dimension configurations
- Create token combinations from multiple dimensions (variant, state, size, theme, etc.)
- Build hierarchical token naming structures using slash notation
- Transform dimension schemas into complete token sets
- Generate tokens with proper Figma variable metadata (types and scopes)

## How to generate tokens

### Basic token generation

1. **Define your configuration**:
   - `baseName`: Component name (e.g., "button", "card")
   - `dimensions`: Array of dimension objects with id, enabled status, and selected values
   - `selectedValues`: Object mapping dimension IDs to Sets of selected values
   - `customOrder`: Optional array to specify dimension ordering

2. **Use the generation script**:
   ```javascript
   const config = {
     baseName: 'button',
     dimensions: activeDimensions,
     selectedValues: selectedValuesMap,
     customOrder: ['component', 'variant', 'state', 'property']
   };
   const tokens = generateTokens(config);
   ```

3. **Generated tokens include**:
   - `name`: Hierarchical slash-separated token name
   - `type`: Figma variable type (COLOR, FLOAT, STRING, BOOLEAN)
   - `scopes`: Array of Figma scopes for the property

### Dimension configuration structure

Each dimension must have:
- `id`: Unique identifier (variant, state, size, property, etc.)
- `enabled`: Boolean indicating if dimension is active
- `values`: Array of possible values (strings or objects with metadata)

For property dimensions, values should include Figma metadata:
```javascript
{
  name: 'background-color',
  type: 'COLOR',
  scopes: ['FRAME_FILL', 'SHAPE_FILL']
}
```

### Token naming conventions

Tokens are named using forward slash hierarchy:
- `button/primary/default/background-color`
- `card/elevated/hover/shadow-color`
- `text/heading/large/font-size`

### Custom ordering

You can specify custom dimension ordering including the component name:
```javascript
customOrder: ['component', 'variant', 'state', 'size', 'property']
```

If no custom order is provided, the default is:
1. Component name (if present)
2. Dimensions in their default order

## Property type mapping

The skill automatically maps CSS properties to Figma variable types:

### Colors (COLOR type)
- `background-color` → FRAME_FILL, SHAPE_FILL
- `text-color` → TEXT_FILL
- `border-color` → STROKE_COLOR
- `shadow-color` → EFFECT_COLOR

### Numbers (FLOAT type)
- `width`, `height` → WIDTH_HEIGHT
- `border-radius` → CORNER_RADIUS
- `padding`, `margin`, `gap` → GAP
- `font-size` → FONT_SIZE
- `opacity` → OPACITY

### Text (STRING type)
- `font-family` → FONT_FAMILY
- `font-style`, `text-align` → ALL_SCOPES

## Examples

### Simple button tokens
```javascript
const config = {
  baseName: 'button',
  dimensions: [
    { id: 'variant', enabled: true, values: ['primary', 'secondary'] },
    { id: 'state', enabled: true, values: ['default', 'hover'] },
    { id: 'property', enabled: true, values: [
      { name: 'background-color', type: 'COLOR', scopes: ['FRAME_FILL'] }
    ]}
  ],
  selectedValues: {
    variant: new Set(['primary', 'secondary']),
    state: new Set(['default', 'hover']),
    property: new Set(['background-color'])
  }
};

// Generates:
// button/primary/default/background-color
// button/primary/hover/background-color
// button/secondary/default/background-color
// button/secondary/hover/background-color
```

### Typography tokens with custom order
```javascript
const config = {
  baseName: 'text',
  customOrder: ['component', 'hierarchy', 'size', 'property'],
  // ... dimensions and selectedValues
};

// Generates:
// text/heading/large/font-size
// text/body/medium/line-height
```

## Common patterns

### Primitive tokens
- Color scales: `red/50`, `red/100`, `red/500`
- Spacing: `spacing/xs`, `spacing/md`, `spacing/lg`
- Typography: `font-size/sm`, `font-weight/bold`

### Semantic tokens
- Purpose-based: `color/primary`, `color/success`, `color/warning`
- Context-aware: `surface/elevated`, `text/muted`

### Component tokens
- Component-specific: `button/primary/hover/background-color`
- State-aware: `input/error/border-color`