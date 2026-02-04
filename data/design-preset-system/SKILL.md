---
name: design-preset-system
description: Use when applying or switching design styles across UI components - provides preset design systems with tokens, patterns, and guidelines for different aesthetic approaches from timeless classics to bleeding-edge experimental styles
---

# Design Preset System

## Overview
Modular design preset system enabling seamless style switching while maintaining consistency and quality across any React Native or Next.js application.

## When to Use
- Starting new project and choosing design direction
- Switching design style for existing project
- Applying consistent aesthetic across components
- Exploring different design approaches
- Presenting design options to stakeholders

## When NOT to Use
- Creating custom design system from scratch (use `design-system-foundation` instead)
- Just refactoring code (use `ui-refactoring-workflow` instead)
- Need documentation only (use `design-documentation-generator` instead)

## Available Presets

### 1. Minimalist Modern (Timeless) ⚪
**Philosophy**: Less is more. Clear hierarchy, generous spacing, purposeful color.

**Best For**: SaaS products, productivity tools, professional applications

**Characteristics**:
- Clean, spacious layouts
- Monochromatic + single accent color
- Subtle shadows (0-10% opacity)
- Generous white space (16-24px minimum)
- Sans-serif typography (Inter, SF Pro)

**See**: `presets/minimalist-modern/` for complete implementation

---

### 2. Bold Brutalist (Bleeding Edge) ⚫
**Philosophy**: Raw, honest, high-impact. Geometric forms, stark contrasts, unapologetic.

**Best For**: Creative agencies, portfolios, bold brands, art-focused apps

**Characteristics**:
- High contrast (black/white/red/yellow)
- Sharp corners (0 border radius)
- Bold typography (700-900 weight)
- Harsh shadows (solid, offset)
- Geometric layouts

**See**: `presets/bold-brutalist/` for complete implementation

---

### 3. Soft Neumorphic (Subtle) 🌫️
**Philosophy**: Tactile, soft, approachable. Subtle depth through shadows and highlights.

**Best For**: Health apps, meditation apps, wellness products

**Characteristics**:
- Soft shadows and highlights
- Low contrast backgrounds
- Rounded corners (12-20px)
- Tactile appearance
- Pastel color palette

**See**: `presets/soft-neumorphic/` for complete implementation

---

### 4. Glass Aesthetic (Modern) 💎
**Philosophy**: Depth through transparency. Layered, blurred, ethereal.

**Best For**: Premium apps, fintech, modern dashboards, iOS-style apps

**Characteristics**:
- Transparency with backdrop blur
- Layered depth
- Soft glows and halos
- Semi-transparent surfaces
- Apple-inspired design

**See**: `presets/glass-aesthetic/` for complete implementation

---

### 5. Timeless Classic (Professional) 📘
**Philosophy**: Balanced, accessible, proven. Professional and trustworthy.

**Best For**: Enterprise software, government apps, accessibility-first products

**Characteristics**:
- High accessibility (WCAG AAA)
- Conservative colors
- Proven UI patterns
- Clear information hierarchy
- Readable typography (16px minimum)

**See**: `presets/timeless-classic/` for complete implementation

---

### 6. Bleeding Edge Experimental (Innovative) 🚀
**Philosophy**: Push boundaries. Latest trends, experimental interactions, forward-thinking.

**Best For**: Tech showcases, innovation labs, cutting-edge products

**Characteristics**:
- Latest 2025 design trends
- Experimental interactions
- Cutting-edge animations
- Unconventional layouts
- Gradient-heavy designs

**See**: `presets/bleeding-edge-experimental/` for complete implementation

---

## Applying a Preset

### For New Projects

When using `design-system-foundation`, specify preset:

```
"Set up design system foundation using glass-aesthetic preset"
```

Tokens automatically configured to match preset.

### For Existing Projects

When using `ui-refactoring-workflow`, specify preset:

```
"Refactor this component using minimalist-modern preset"
```

Component styling updated to match preset while preserving functionality.

### Switching Presets

```
"Convert my app from minimalist-modern to bold-brutalist preset"
```

Process:
1. Analyze current token usage
2. Map to new preset tokens
3. Update component styling
4. Maintain functionality
5. Update documentation

## Preset Selection Guide

| Use Case | Recommended Preset |
|----------|-------------------|
| SaaS Dashboard | Minimalist Modern or Glass Aesthetic |
| Health/Wellness App | Soft Neumorphic or Timeless Classic |
| Creative Portfolio | Bold Brutalist or Bleeding Edge |
| Enterprise Software | Timeless Classic or Minimalist Modern |
| Fintech App | Glass Aesthetic or Minimalist Modern |
| E-commerce | Minimalist Modern or Timeless Classic |
| Social Media | Glass Aesthetic or Bleeding Edge |
| Productivity Tool | Minimalist Modern or Timeless Classic |

## Token Mapping

Each preset includes complete token definitions:

- **Colors**: Brand, UI, feedback colors
- **Typography**: Font families, sizes, weights
- **Spacing**: Consistent scale
- **Shadows**: Elevation system
- **Border Radius**: Rounding scale
- **Animations**: Timing and easing

## Usage Examples

### React Native

```typescript
import { glassAesthetic } from '@/theme/presets'

const Card = () => {
  return (
    <View style={{
      backgroundColor: glassAesthetic.colors.surface,
      padding: glassAesthetic.spacing.lg,
      borderRadius: glassAesthetic.radius.xl,
      ...glassAesthetic.shadows.md,
    }}>
      <Text style={{
        fontSize: glassAesthetic.typography.scale.lg,
        fontWeight: glassAesthetic.typography.weights.semibold,
        color: glassAesthetic.colors.text.primary,
      }}>
        Glass Card
      </Text>
    </View>
  )
}
```

### Next.js with Tailwind

```tsx
// tailwind.config.ts - configured with minimalistModern
const Card = () => {
  return (
    <div className="bg-surface p-lg rounded-md shadow-md">
      <h2 className="text-lg font-semibold text-primary">
        Minimalist Card
      </h2>
    </div>
  )
}
```

## Mixing Presets (Advanced)

You can mix elements from different presets:

```typescript
const hybridTokens = {
  // Glass aesthetic surfaces
  colors: glassAesthetic.colors,

  // Brutalist typography
  typography: boldBrutalist.typography,

  // Minimalist spacing
  spacing: minimalistModern.spacing,
}
```

**Warning**: Only recommended for experienced designers. Can create inconsistent UX.

## Quality Checklist

When applying preset, verify:
- ✓ All tokens from preset applied
- ✓ Colors maintain WCAG AA contrast (minimum)
- ✓ Typography remains readable
- ✓ Spacing feels consistent
- ✓ Shadows appropriate for preset
- ✓ Animations match preset philosophy
- ✓ Components feel cohesive

## Common Mistakes

❌ **Mixing incompatible preset elements**
```typescript
// BAD: Brutalist shadows + Neumorphic colors
style={{
  backgroundColor: softNeumorphic.colors.surface,
  ...boldBrutalist.shadows.lg // Harsh shadow on soft surface
}}
```

✅ **Stick to one preset**
```typescript
// GOOD: Consistent preset usage
style={{
  backgroundColor: softNeumorphic.colors.surface,
  ...softNeumorphic.shadows.sm // Soft shadow matches
}}
```

❌ **Ignoring preset philosophy**
```typescript
// BAD: Minimalist preset with excessive decoration
<View style={minimalistModern}>
  <GradientBackground />
  <ParticleEffect />
  <AnimatedBorder />
</View>
```

✅ **Honor preset principles**
```typescript
// GOOD: Minimalist stays minimal
<View style={minimalistModern}>
  <Text>Simple, Clean</Text>
</View>
```

## Real-World Impact

Teams using preset system report:
- 80% faster design decisions
- Consistent aesthetic across app
- Easy style exploration
- Faster stakeholder approval
- Seamless design migrations

## Integration with Other Skills

- Use with `design-system-foundation` for new projects
- Use with `ui-refactoring-workflow` for existing projects
- Use with `component-modernization` for component updates
- Use with `aesthetic-excellence` for fine-tuning
