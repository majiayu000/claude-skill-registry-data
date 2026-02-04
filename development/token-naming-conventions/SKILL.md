---
name: token-naming-conventions
description: Standardizes design token naming patterns using hierarchical slash notation, dimension ordering, and consistent formatting rules. Use when establishing token naming standards, converting between naming formats, or organizing token hierarchies.
---

# Token Naming Conventions

## When to use this skill

Use this skill when you need to:
- Establish consistent token naming patterns across design systems
- Convert between different naming conventions (hyphens vs slashes)
- Create hierarchical token structures with proper organization
- Define dimension ordering for token names
- Transform token names for different platforms (CSS, Figma, code)
- Validate token naming compliance

## Core naming principles

### 1. Hierarchical structure
Tokens use forward slash notation to create clear hierarchies:
```
component/variant/state/property
button/primary/hover/background-color
card/elevated/default/shadow-blur
```

### 2. Semantic organization
Names should read naturally from general to specific:
- **General → Specific**: `typography/heading/large/font-size`
- **Context → Detail**: `surface/primary/hover/background-color`
- **Category → Property**: `spacing/component/padding-x`

### 3. Consistent formatting
- Use lowercase letters only
- Use hyphens within segments: `background-color`, `font-weight`
- Use forward slashes between segments: `button/primary/hover`
- No spaces or special characters

## Dimension ordering patterns

### Default order (recommended)
1. **Component** (optional): `button`, `card`, `input`
2. **Variant/Intent**: `primary`, `secondary`, `success`  
3. **State**: `default`, `hover`, `active`, `disabled`
4. **Size**: `xs`, `sm`, `md`, `lg`, `xl`
5. **Property**: `background-color`, `border-radius`, `font-size`

Example: `button/primary/hover/md/background-color`

### Custom ordering
You can customize dimension order based on design system needs:

#### Priority-based ordering
1. **Component**: `button`
2. **Property**: `background-color`
3. **Variant**: `primary`
4. **State**: `hover`

Example: `button/background-color/primary/hover`

#### Context-first ordering  
1. **Theme**: `light`
2. **Component**: `button`
3. **Variant**: `primary`
4. **State**: `hover`
5. **Property**: `background-color`

Example: `light/button/primary/hover/background-color`

## Token categories and naming

### Primitive tokens
Raw foundational values with simple, descriptive names:

#### Color primitives
```
colors/red/100
colors/red/500
colors/red/900
colors/neutral/50
colors/blue/600
```

#### Spacing primitives  
```
spacing/xs    (4px)
spacing/sm    (8px)
spacing/md    (16px)
spacing/lg    (24px)
spacing/xl    (32px)
```

#### Typography primitives
```
font-size/xs   (12px)
font-size/sm   (14px)  
font-size/md   (16px)
font-size/lg   (18px)
font-weight/light    (300)
font-weight/normal   (400)
font-weight/semibold (600)
```

### Semantic tokens
Purpose-driven tokens that reference primitives:

#### Color semantics
```
color/primary         → colors/blue/500
color/success         → colors/green/500
color/warning         → colors/yellow/500
color/danger          → colors/red/500
```

#### Role-based semantics
```
surface/primary       → colors/neutral/50
surface/secondary     → colors/neutral/100
text/primary          → colors/neutral/900
text/secondary        → colors/neutral/600
border/default        → colors/neutral/200
```

### Component tokens
Component-specific tokens for contextual usage:

#### Button tokens
```
button/primary/default/background-color
button/primary/hover/background-color
button/primary/active/background-color
button/primary/disabled/background-color
button/primary/default/text-color
button/primary/default/border-radius
```

#### Card tokens
```
card/elevated/default/background-color
card/elevated/default/shadow-color
card/elevated/default/border-radius
card/flat/default/border-color
```

## Platform-specific formatting

### CSS custom properties
Convert slashes to double hyphens:
```
button/primary/hover/background-color
  ↓
--button--primary--hover--background-color
```

### JavaScript/JSON
Convert slashes to nested objects:
```javascript
{
  button: {
    primary: {
      hover: {
        backgroundColor: '#value'
      }
    }
  }
}
```

### Figma variables
Keep slash notation (Figma supports it natively):
```
button/primary/hover/background-color
```

### SCSS variables
Convert slashes to hyphens with prefix:
```
button/primary/hover/background-color
  ↓
$button-primary-hover-background-color
```

## Naming validation rules

### Valid characters
- Lowercase letters: `a-z`
- Numbers: `0-9`
- Hyphens: `-` (within segments only)
- Forward slashes: `/` (between segments only)

### Invalid patterns
❌ `Button/Primary/Hover` (uppercase)
❌ `button_primary_hover` (underscores)  
❌ `button-primary-hover` (no hierarchy)
❌ `button//primary//hover` (double slashes)
❌ `button/primary-/hover` (trailing hyphens)

### Valid patterns
✅ `button/primary/hover/background-color`
✅ `typography/heading/large/font-size`
✅ `spacing/component/padding-x`
✅ `color/semantic/success`

## Common patterns

### State variations
```
// Interactive states
component/variant/default/property
component/variant/hover/property
component/variant/active/property
component/variant/focus/property
component/variant/disabled/property

// Validation states
component/state/success/property
component/state/warning/property  
component/state/error/property
```

### Size variations
```
// T-shirt sizing
component/variant/xs/property
component/variant/sm/property
component/variant/md/property
component/variant/lg/property
component/variant/xl/property

// Numeric sizing
component/variant/100/property
component/variant/200/property
component/variant/400/property
```

### Theme variations
```
// Theme-aware tokens
theme/light/component/variant/property
theme/dark/component/variant/property
theme/high-contrast/component/variant/property
```

## Best practices

1. **Be consistent**: Establish rules and follow them across all tokens
2. **Be descriptive**: Names should clearly indicate purpose and context
3. **Be hierarchical**: Order dimensions from general to specific
4. **Be platform-aware**: Consider how names will be used in different contexts
5. **Be scalable**: Design naming patterns that can grow with your design system
6. **Document conventions**: Maintain clear guidelines for your team

## Migration strategies

When updating naming conventions:

1. **Create mapping**: Document old → new name conversions
2. **Gradual transition**: Support both old and new names during migration
3. **Automated tools**: Use scripts to convert tokens systematically
4. **Team communication**: Ensure all stakeholders understand changes
5. **Update documentation**: Reflect new conventions in design system docs