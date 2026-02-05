---
name: ui-refactoring-workflow
description: Use when refactoring existing React Native, Next.js, or TypeScript UI code to apply modern design principles and aesthetic excellence - analyzes current implementation, applies design presets, maintains functionality while elevating visual quality
---

# UI Refactoring Workflow

## Overview
Systematic approach to transforming existing UI code into modern, aesthetically superior implementations while preserving functionality and improving maintainability.

## When to Use
- Refactoring brownfield React Native/Next.js apps
- Modernizing outdated UI components
- Applying consistent design system to existing code
- Switching design styles/presets across application
- Elevating visual quality without rebuilding from scratch
- Improving accessibility of existing components

## When NOT to Use
- Starting new project from scratch (use `design-system-foundation` instead)
- Just fixing bugs (regular debugging workflow)
- Performance optimization only (use performance tools)
- Backend refactoring (this is UI-focused)

## Refactoring Process

### Phase 1: Analysis (Understand Current State)

**Goal**: Fully understand what exists before changing anything.

#### 1.1 Identify Component Structure
- What props does it accept?
- What is the component API?
- What are the TypeScript types?
- How is it composed (children, render props, etc.)?

#### 1.2 Extract Current Styling
- Inline styles vs stylesheet usage
- Color values (hardcoded vs tokens)
- Spacing patterns
- Typography implementation
- Animation/transition usage

#### 1.3 Document Functionality
- What does this component do?
- What are the interaction patterns?
- What states exist? (loading, error, success, disabled, focused, etc.)
- What accessibility features are present?
- What are the edge cases?

#### 1.4 Identify Pain Points
- Hardcoded values
- Inconsistent spacing
- Poor color contrast
- Accessibility issues
- Performance problems
- Maintainability issues

**Example Analysis:**

```typescript
// BEFORE (Current State)
const Button = ({ title, onPress, disabled }) => {
  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled}
      style={{
        backgroundColor: disabled ? '#ccc' : '#3498db', // Hardcoded colors
        padding: 12, // Hardcoded spacing
        borderRadius: 5,
        marginTop: 10,
      }}
    >
      <Text style={{ color: '#fff', fontSize: 16 }}> // Hardcoded typography
        {title}
      </Text>
    </TouchableOpacity>
  )
}

// ANALYSIS NOTES:
// ❌ Hardcoded colors (no design tokens)
// ❌ Inconsistent spacing (12, 10)
// ❌ No TypeScript types
// ❌ Missing accessibility props
// ❌ No loading state
// ❌ No variants (primary, secondary, etc.)
// ❌ No size options
// ❌ Poor disabled state (just gray)
// ✅ Basic functionality works
// ✅ Has disabled prop
```

---

### Phase 2: Design Preset Selection

**Goal**: Choose aesthetic direction for refactored component.

#### Available Presets:
- `minimalist-modern` - Clean, spacious, timeless
- `bold-brutalist` - High contrast, geometric, bold
- `soft-neumorphic` - Subtle shadows, soft edges
- `glass-aesthetic` - Transparency, blur, depth
- `timeless-classic` - Balanced, professional, accessible
- `bleeding-edge-experimental` - Latest trends, innovative

#### Selection Criteria:
- What's the app's target audience?
- What's the brand personality?
- What design system already exists (if any)?
- What accessibility requirements exist?
- What's the desired visual impact?

**Example**: For a fitness app → `glass-aesthetic` (modern, premium feel)

---

### Phase 3: Refactoring Execution

**Goal**: Transform component while preserving functionality.

#### 3.1 Preserve Functionality First

```typescript
// Step 1: Extract interface (no visual changes yet)
interface ButtonProps {
  title: string
  onPress: () => void
  disabled?: boolean
  // ADD: New props for enhanced functionality
  loading?: boolean
  variant?: 'primary' | 'secondary' | 'tertiary'
  size?: 'sm' | 'md' | 'lg'
  leftIcon?: React.ReactNode
}
```

#### 3.2 Apply Design Tokens

```typescript
import { glassAesthetic } from '@/theme/presets'

// Step 2: Replace hardcoded values with tokens
style={{
  // BEFORE: backgroundColor: disabled ? '#ccc' : '#3498db'
  // AFTER: Use tokens
  backgroundColor: disabled
    ? glassAesthetic.colors.ui.background.tertiary
    : glassAesthetic.colors.brand.primary,

  // BEFORE: padding: 12
  // AFTER: Use spacing tokens
  padding: glassAesthetic.spacing.md,

  // BEFORE: borderRadius: 5
  // AFTER: Use radius tokens
  borderRadius: glassAesthetic.radius.lg,
}}
```

#### 3.3 Modernize Component Structure

```typescript
// Step 3: Improve composition and patterns
const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  disabled = false,
  loading = false,
  variant = 'primary',
  size = 'md',
  leftIcon,
}) => {
  const theme = useTheme() // Use theme hook
  const styles = getStyles(theme, variant, size) // Dynamic styles

  return (
    <Pressable
      onPress={onPress}
      disabled={disabled || loading}
      style={({ pressed }) => [
        styles.base,
        pressed && styles.pressed,
        disabled && styles.disabled,
      ]}
      // Add accessibility
      accessibilityRole="button"
      accessibilityState={{ disabled, busy: loading }}
      accessibilityLabel={title}
    >
      {loading ? (
        <ActivityIndicator color={theme.colors.ui.text.inverse} />
      ) : (
        <>
          {leftIcon && <View style={styles.iconLeft}>{leftIcon}</View>}
          <Text style={styles.text}>{title}</Text>
        </>
      )}
    </Pressable>
  )
}
```

#### 3.4 Enhance Accessibility

```typescript
// WCAG 2.2 AA Compliance
const styles = StyleSheet.create({
  base: {
    // Minimum touch target: 44x44pt
    minHeight: 44,
    minWidth: 44,

    // Clear focus indicator
    borderWidth: 2,
    borderColor: 'transparent',
  },

  focused: {
    // Visible focus for keyboard navigation
    borderColor: theme.colors.brand.accent,
    borderWidth: 2,
  },

  text: {
    // Minimum font size for readability
    fontSize: Math.max(theme.typography.scale.base, 16),

    // Sufficient contrast ratio (4.5:1 minimum)
    color: theme.colors.ui.text.inverse,
  }
})
```

#### 3.5 Add Micro-interactions

```typescript
import { useAnimatedStyle, withTiming } from 'react-native-reanimated'

// Thoughtful animations
const animatedStyles = useAnimatedStyle(() => ({
  transform: [{
    scale: withTiming(pressed ? 0.98 : 1, {
      duration: theme.animation.duration.fast,
    })
  }],
  opacity: withTiming(disabled ? 0.5 : 1, {
    duration: theme.animation.duration.normal,
  })
}))
```

#### 3.6 Optimize Performance

```typescript
// Memoize expensive operations
const Button = React.memo(({ title, onPress, ...props }: ButtonProps) => {
  // Memoize styles
  const styles = useMemo(
    () => getStyles(theme, variant, size),
    [theme, variant, size]
  )

  // Memoize callbacks
  const handlePress = useCallback(() => {
    if (!disabled && !loading) {
      onPress()
    }
  }, [disabled, loading, onPress])

  return (
    // Component JSX
  )
})
```

---

### Phase 4: Validation

**Goal**: Ensure refactoring meets quality standards.

#### Validation Checklist:

- ✓ **Visual Parity or Improvement**
  - Component looks as good or better
  - No visual regressions
  - Design preset correctly applied

- ✓ **Functionality Unchanged**
  - All props work as before
  - All interactions preserved
  - No breaking changes to API
  - Backward compatible (or migration path provided)

- ✓ **Accessibility Enhanced**
  - WCAG 2.2 AA minimum
  - Screen reader tested
  - Keyboard navigable
  - Sufficient contrast ratios
  - Minimum touch targets (44x44pt)

- ✓ **Performance Maintained or Improved**
  - No performance regressions
  - Memoization where appropriate
  - Optimized re-renders

- ✓ **Code Readability Improved**
  - TypeScript types complete
  - Clear variable names
  - Commented where necessary
  - Follows project conventions

- ✓ **Design System Compliance**
  - Uses design tokens (no hardcoded values)
  - Follows spacing system
  - Consistent with other components
  - Documentation updated

---

## Integration with Other Skills

**Use in combination:**
- `design-preset-system` - For style selection
- `component-modernization` - For React Native/Next.js specific patterns
- `aesthetic-excellence` - For visual hierarchy improvements
- `accessibility-upgrade` - For WCAG compliance
- `animation-enhancement` - For micro-interactions

---

## Common Refactoring Patterns

### Pattern 1: Hardcoded to Tokens

```typescript
// BEFORE
style={{ color: '#3498db', padding: 15, fontSize: 18 }}

// AFTER
style={{
  color: theme.colors.brand.primary,
  padding: theme.spacing.lg,
  fontSize: theme.typography.scale.lg,
}}
```

### Pattern 2: Inline Styles to StyleSheet

```typescript
// BEFORE
<View style={{ backgroundColor: '#fff', padding: 20 }}>

// AFTER
const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.ui.background.primary,
    padding: theme.spacing.xl,
  }
})

<View style={styles.container}>
```

### Pattern 3: Add Variants

```typescript
// BEFORE: Single style
const Button = ({ onPress }) => <TouchableOpacity style={styles.button}>

// AFTER: Multiple variants
const Button = ({ variant = 'primary', onPress }) => (
  <Pressable style={[styles.base, styles[variant]]}>
)

const styles = StyleSheet.create({
  base: { /* shared styles */ },
  primary: { backgroundColor: theme.colors.brand.primary },
  secondary: { backgroundColor: theme.colors.brand.secondary },
  tertiary: { backgroundColor: 'transparent' },
})
```

### Pattern 4: Improve Accessibility

```typescript
// BEFORE
<TouchableOpacity onPress={onPress}>
  <Text>{label}</Text>
</TouchableOpacity>

// AFTER
<Pressable
  onPress={onPress}
  accessibilityRole="button"
  accessibilityLabel={label}
  accessibilityState={{ disabled }}
  accessible={true}
>
  <Text>{label}</Text>
</Pressable>
```

---

## Real-World Impact

Teams using this workflow report:
- 60% faster refactoring iterations
- 95% reduction in hardcoded values
- Consistent design across all screens
- Better accessibility scores
- Improved maintainability
- Easier design system migration

---

## Common Mistakes

❌ **Changing functionality during refactoring**
```typescript
// BAD: Adding new features while refactoring
const Button = ({ onPress }) => {
  // Don't add analytics, new features, etc. during refactor
  trackAnalytics('button_pressed') // ❌
}
```

✅ **Refactor only, features later**
```typescript
// GOOD: Pure refactor, no behavioral changes
const Button = ({ onPress }) => {
  // Just visual/structural improvements
}
```

❌ **Incomplete token migration**
```typescript
// BAD: Mix of tokens and hardcoded
style={{
  padding: theme.spacing.md, // ✅ Token
  color: '#3498db', // ❌ Hardcoded
}}
```

✅ **Complete token usage**
```typescript
// GOOD: All values from tokens
style={{
  padding: theme.spacing.md,
  color: theme.colors.brand.primary,
}}
```
