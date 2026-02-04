---
name: tamagui-component
description: Use when creating or modifying Tamagui UI components in packages/ui. Enforces design token usage, theme compatibility, and cross-platform considerations.
---

# Tamagui Component Skill

Use this skill when creating or modifying UI components in `packages/ui/` using Tamagui.

## 🏗️ Atomic Design Structure

**CRITICAL**: The `@hounii/ui` package follows **Atomic Design principles**.
All components MUST be organized into the correct atomic level.

### Component Hierarchy

```
packages/ui/src/
├── atoms/          # Basic building blocks (Button, Input, Label)
├── molecules/      # Simple combinations (FormField, AuthCard)
├── organisms/      # Complex components (MagicLinkForm, NavigationBar)
├── templates/      # Page layouts (future)
└── theme/          # Tamagui configuration
```

### Atomic Levels Explained

#### 1. **Atoms** - Basic Building Blocks
Smallest UI elements that can't be broken down further.

**Examples**: Button, Input, Label, Text, Card, YStack, XStack

**Key Rule**: ALL atoms are **custom wrappers** around Tamagui primitives.

**Why Custom Wrappers?**
- Modify design system in ONE place
- Easy to add brand-specific styling
- Can add analytics, validation, custom logic
- No need to search/replace across codebase

**❌ NEVER import from Tamagui directly:**
```tsx
// WRONG - bypasses our design system
import { Button } from 'tamagui';
```

**✅ ALWAYS import from @hounii/ui:**
```tsx
// CORRECT - uses our custom atoms
import { Button } from '@hounii/ui';
```

**Creating a New Atom**:
```tsx
// packages/ui/src/atoms/Button.tsx
import { Button as TamaguiButton, type ButtonProps as TamaguiButtonProps } from 'tamagui';

export type ButtonProps = TamaguiButtonProps;

/**
 * Button Atom
 * Custom wrapper around Tamagui's Button.
 * Modify this file to change button behavior across the entire app.
 */
export function Button(props: ButtonProps) {
  return <TamaguiButton {...props} />;
}
```

Then export in `packages/ui/src/atoms/index.ts`:
```tsx
export * from './Button';
```

#### 2. **Molecules** - Simple Combinations
Combinations of atoms working together as a functional unit.

**Examples**: FormField (Label + Input + Error), AuthCard (Card + YStack), SearchBar (Input + Button)

**Key Rule**: Molecules combine atoms, not Tamagui primitives directly.

**Creating a Molecule**:
```tsx
// packages/ui/src/molecules/FormField.tsx
import { Input, Label, Paragraph, YStack } from '../atoms';
import type { InputProps } from '../atoms';

export interface FormFieldProps extends InputProps {
  label: string;
  error?: string;
}

/**
 * FormField Molecule
 * Combines Label + Input + Error for consistent form fields.
 */
export function FormField({ label, error, ...props }: FormFieldProps) {
  return (
    <YStack space="$2">
      <Label>{label}</Label>
      <Input {...props} />
      {error && <Paragraph color="$red10">{error}</Paragraph>}
    </YStack>
  );
}
```

#### 3. **Organisms** - Complex Components
Complex UI components with specific functionality, composed of molecules/atoms.

**Examples**: MagicLinkForm, NavigationBar, UserProfileCard, DataTable

**Key Rule**: Organisms implement complete features and business logic.

**Creating an Organism**:
```tsx
// packages/ui/src/organisms/MagicLinkForm.tsx
'use client';

import { useState } from 'react';
import { Button, Form, YStack } from '../atoms';
import { FormField } from '../molecules/FormField';

/**
 * MagicLinkForm Organism
 * Complete authentication form for magic link login.
 */
export function MagicLinkForm({ onSubmit, ...props }) {
  const [email, setEmail] = useState('');

  return (
    <Form onSubmit={() => onSubmit(email)} {...props}>
      <YStack space="$4">
        <FormField
          label="Email"
          value={email}
          onChangeText={setEmail}
        />
        <Button>Send Magic Link</Button>
      </YStack>
    </Form>
  );
}
```

### Decision Tree: Where Does My Component Go?

1. **Can it be broken down further?**
   - No → It's an **Atom** (Button, Input, Label)
   - Yes → Continue...

2. **Does it combine 2-3 atoms into a simple unit?**
   - Yes → It's a **Molecule** (FormField, AuthCard)
   - No → Continue...

3. **Does it implement a complete feature with business logic?**
   - Yes → It's an **Organism** (MagicLinkForm, NavigationBar)

### Import Rules

**✅ CORRECT** - Always import from `@hounii/ui`:
```tsx
import { Button, Input, YStack, AuthCard, MagicLinkForm } from '@hounii/ui';
```

**❌ WRONG** - Never import from Tamagui directly in apps:
```tsx
import { Button } from 'tamagui';  // Bypasses design system!
```

**✅ CORRECT** - Internal imports in UI package:
```tsx
// In molecules/FormField.tsx
import { Input, Label } from '../atoms';

// In organisms/MagicLinkForm.tsx
import { Button, Form } from '../atoms';
import { FormField } from '../molecules/FormField';
```

## Tamagui Overview

**Tamagui** is a universal UI framework that works across React Native and Web, providing:
- Design tokens (colors, spacing, typography)
- Theme system (light/dark modes)
- Responsive design utilities
- Optimized performance
- Type-safe styling

## Design Token System

### Always Use Tokens, Never Hardcoded Values

**❌ WRONG: Hardcoded values**
```tsx
<View backgroundColor="#3b82f6" padding={16}>
  <Text color="#000000" fontSize={18}>Hello</Text>
</View>
```

**❌ WRONG: Using `as any` to bypass type safety**
```tsx
<Text color={"$colorSecondary" as any}>Text</Text>
<View borderColor={"$borderColor" as any}>Content</View>
```

**✅ CORRECT: Standard Tamagui tokens (no type casting needed)**
```tsx
<View backgroundColor="$background" padding="$4">
  <Text color="$color" fontSize="$5">Hello</Text>
  <View borderColor="$borderColor">Content</View>
</View>
```

**✅ CORRECT: Extend theme if you need custom semantic tokens**
```typescript
// packages/ui/src/theme/tamagui.config.ts
export const config = createTamagui({
  ...defaultConfig,
  themes: {
    ...defaultConfig.themes,
    light: {
      ...defaultConfig.themes.light,
      colorSecondary: '$gray11',  // Now $colorSecondary is valid!
      backgroundHover: '$gray2',
    },
    dark: {
      ...defaultConfig.themes.dark,
      colorSecondary: '$gray4',
      backgroundHover: '$gray11',
    },
  },
});

// Now use without type casting
<Text color="$colorSecondary">Secondary text</Text>
```

### Token Categories

#### Colors (`$color`, `$background`, `$primary`, etc.)
```tsx
// Semantic colors (adapt to theme)
backgroundColor="$background"     // Background color
color="$color"                    // Text color
borderColor="$borderColor"        // Border color

// Brand colors
backgroundColor="$primary"        // Primary brand color
backgroundColor="$secondary"      // Secondary brand color

// State colors
backgroundColor="$success"        // Success state
backgroundColor="$error"          // Error state
backgroundColor="$warning"        // Warning state
```

#### Spacing (`$1` - `$12`, etc.)
```tsx
// Spacing scale (follows 4px base)
padding="$2"      // 8px
padding="$4"      // 16px
padding="$6"      // 24px

// Compound spacing
paddingHorizontal="$4"
paddingVertical="$2"
gap="$3"
```

#### Typography (`$1` - `$10`)
```tsx
// Font size scale
fontSize="$3"     // Small
fontSize="$5"     // Body
fontSize="$7"     // Heading
fontSize="$9"     // Display

// Font weights
fontWeight="$4"   // Regular
fontWeight="$7"   // Bold
```

#### Border Radius (`$1` - `$6`)
```tsx
borderRadius="$2"     // Subtle
borderRadius="$4"     // Standard
borderRadius="$true"  // Circle/pill
```

## Theme System

Tamagui provides a comprehensive theme system that allows users to select different visual styles. Hounii will support **user-selectable themes**, so understanding the complete theme architecture is critical.

### Theme Architecture Overview

Tamagui themes are organized hierarchically:

```
1. Base Themes (light, dark)
   ├── 2. Accent Themes (inverse of base)
   └── 3. Child Themes (blue, red, green, yellow, etc.)
       └── 4. Component Themes (Button, Card, Input, etc.)
           └── 5. State Themes (hover, press, focus)
```

### Creating Custom Themes for User Selection

**Hounii Goal**: Users can select from multiple theme presets (e.g., "Ocean", "Forest", "Sunset").

#### Method 1: Using `createThemes` (Recommended)

```tsx
import { createThemes, defaultComponentThemes } from '@tamagui/config/v4';
import * as Colors from '@tamagui/colors';

// Define custom palettes for each theme preset
const oceanPalette = [
  '#001f3f', '#003366', '#004d99', '#0066cc', '#0080ff',
  '#3399ff', '#66b3ff', '#99ccff', '#cce6ff', '#e6f2ff',
  '#f0f8ff', '#ffffff',
];

const forestPalette = [
  '#0d3a1a', '#1a4d2e', '#266040', '#337354', '#408866',
  '#4d9a78', '#66b38a', '#80cc9e', '#99e6b3', '#b3f0cc',
  '#e6f9f0', '#ffffff',
];

const sunsetPalette = [
  '#4a1a00', '#663300', '#804d00', '#996600', '#b37f00',
  '#cc9933', '#e6b366', '#ffcc99', '#ffe6cc', '#fff0e6',
  '#fff8f0', '#ffffff',
];

export const themes = createThemes({
  componentThemes: defaultComponentThemes,

  // Base light/dark (default)
  base: {
    palette: {
      dark: oceanPalette,
      light: oceanPalette.slice().reverse(),
    },
  },

  // Child themes for user selection
  childrenThemes: {
    ocean: {
      palette: {
        dark: oceanPalette,
        light: oceanPalette.slice().reverse(),
      },
    },
    forest: {
      palette: {
        dark: forestPalette,
        light: forestPalette.slice().reverse(),
      },
    },
    sunset: {
      palette: {
        dark: sunsetPalette,
        light: sunsetPalette.slice().reverse(),
      },
    },
  },
});
```

#### Method 2: Using `createThemeBuilder` (Advanced)

For more control over theme generation:

```tsx
import { createThemeBuilder } from '@tamagui/theme-builder';

const themeBuilder = createThemeBuilder()
  .addPalettes({
    ocean: oceanPalette,
    forest: forestPalette,
    sunset: sunsetPalette,
  })
  .addTemplates({
    base: {
      background: 0,
      backgroundHover: 1,
      backgroundPress: 2,
      backgroundFocus: 3,
      color: 11,
      colorHover: 10,
      colorPress: 9,
    },
  })
  .addThemes({
    ocean: {
      template: 'base',
      palette: 'ocean',
    },
    forest: {
      template: 'base',
      palette: 'forest',
    },
    sunset: {
      template: 'base',
      palette: 'sunset',
    },
  });

export const themes = themeBuilder.build();
```

### Theme Structure and Keys

Every theme must include these **standard keys**:

```tsx
{
  // Backgrounds
  background: string,           // Primary background
  backgroundHover: string,      // Background on hover
  backgroundPress: string,      // Background on press
  backgroundFocus: string,      // Background on focus
  backgroundStrong: string,     // Strong/emphasized background
  backgroundTransparent: string, // Transparent background

  // Text colors
  color: string,                // Primary text color
  colorHover: string,           // Text on hover
  colorPress: string,           // Text on press
  colorFocus: string,           // Text on focus
  colorTransparent: string,     // Transparent text

  // Borders
  borderColor: string,          // Border color
  borderColorHover: string,     // Border on hover
  borderColorFocus: string,     // Border on focus
  borderColorPress: string,     // Border on press

  // Form elements
  placeholderColor: string,     // Placeholder text
  outlineColor: string,         // Focus outline

  // Shadows (optional)
  shadowColor: string,
  shadow1: string,
  shadow2: string,
  // ... up to shadow6
}
```

**You can add custom tokens**:
```tsx
{
  brandPrimary: '#0080ff',
  brandSecondary: '#00cc66',
  accentColor: '#ff6b35',
}
```

### Using Themes in Components

#### Basic Theme Usage

```tsx
import { View, Text, Theme } from 'tamagui';

export function ThemedComponent() {
  return (
    <View backgroundColor="$background">
      <Text color="$color">Adapts to current theme</Text>
    </View>
  );
}
```

#### Applying Specific Themes

```tsx
import { View, Text, Theme } from 'tamagui';

export function UserSelectableTheme({ userTheme = 'ocean' }) {
  return (
    <Theme name={userTheme}>
      <View backgroundColor="$background" padding="$4">
        <Text color="$color">
          This uses the {userTheme} theme
        </Text>
      </View>
    </Theme>
  );
}
```

#### Nested Theme Layering

Themes can be nested, creating powerful compositions:

```tsx
<Theme name="ocean">
  {/* Everything here uses ocean theme */}
  <View backgroundColor="$background">

    <Theme name="sunset">
      {/* This section uses ocean_sunset (layered theme) */}
      <Card backgroundColor="$background" />
    </Theme>

  </View>
</Theme>
```

**Theme name resolution**:
- `<Theme name="dark">` → applies `dark` theme
- `<Theme name="blue">` inside `dark` → applies `dark_blue` theme
- `<Theme name="Button">` inside `dark_blue` → applies `dark_blue_Button` theme

### Theme Inversion

Invert the current theme (light ↔ dark):

```tsx
import { Theme } from 'tamagui';

<Theme name="dark">
  <View backgroundColor="$background">
    {/* Dark background */}

    <Theme inverse>
      {/* Light background (inverted) */}
      <Card backgroundColor="$background" />
    </Theme>
  </View>
</Theme>
```

### Theme Reset

Reset to grandparent theme (skip intermediate themes):

```tsx
<Theme name="dark">
  <Theme name="blue">
    <Theme reset>
      {/* This uses "dark" theme, skipping "blue" */}
      <View backgroundColor="$background" />
    </Theme>
  </Theme>
</Theme>
```

### Accessing Theme Values with useTheme

```tsx
import { useTheme } from 'tamagui';

export function CustomComponent() {
  const theme = useTheme();

  // Access theme values
  console.log(theme.background.val);     // Raw value: "#ffffff"
  console.log(theme.background.variable); // CSS var: "var(--background)"

  // Use .get() for performance (returns CSS var on web)
  const bg = theme.background.get();

  return (
    <View
      style={{
        backgroundColor: bg,
        color: theme.color.val
      }}
    />
  );
}
```

**Theme object structure**:
```tsx
{
  background: {
    val: '#000',              // Raw color value
    variable: 'var(--background)', // CSS variable
    name: 'background',       // Token name
    isVar: true,              // Is CSS variable?
  },
  // ... other theme keys
}
```

### Dynamic Theme Management

Tamagui provides runtime helpers for theme management:

#### Adding Themes Dynamically

```tsx
import { addTheme } from '@tamagui/theme';

// User creates a custom theme
export function addUserTheme(themeName: string, themeColors: Theme) {
  addTheme({
    name: themeName,
    theme: themeColors,
  });
}

// Example usage
addUserTheme('midnight', {
  background: '#0a0a0a',
  color: '#e0e0e0',
  borderColor: '#333',
  // ... other required keys
});
```

#### Updating Themes

```tsx
import { updateTheme } from '@tamagui/theme';

// Update existing theme (merges with existing values)
updateTheme({
  name: 'ocean',
  theme: {
    background: '#001f3f', // Update only this key
  },
});
```

#### Replacing Themes

```tsx
import { replaceTheme } from '@tamagui/theme';

// Replace entire theme
replaceTheme({
  name: 'ocean',
  theme: {
    // Must provide all required keys
    background: '#001f3f',
    color: '#ffffff',
    // ... all other keys
  },
});
```

### Component-Specific Themes

Components can have their own theme overrides:

```tsx
const themes = createThemes({
  base: {
    palette: { /* ... */ },
  },

  childrenThemes: {
    // Component themes auto-append to parent
    Button: {
      palette: {
        dark: buttonDarkColors,
        light: buttonLightColors,
      },
    },
    Input: {
      palette: {
        dark: inputDarkColors,
        light: inputLightColors,
      },
    },
  },
});
```

**Usage**:
```tsx
// Automatically applies ocean_Button theme
<Theme name="ocean">
  <Button>Uses ocean_Button theme</Button>
</Theme>
```

### Theme Switching for User Preferences

**Example: User theme selector**

```tsx
import { useState } from 'react';
import { Theme, Select, YStack } from 'tamagui';

const AVAILABLE_THEMES = [
  { label: 'Ocean', value: 'ocean' },
  { label: 'Forest', value: 'forest' },
  { label: 'Sunset', value: 'sunset' },
  { label: 'Midnight', value: 'midnight' },
];

export function ThemeSelector() {
  const [selectedTheme, setSelectedTheme] = useState('ocean');

  return (
    <YStack gap="$4">
      <Select value={selectedTheme} onValueChange={setSelectedTheme}>
        {AVAILABLE_THEMES.map((theme) => (
          <Select.Item key={theme.value} value={theme.value}>
            {theme.label}
          </Select.Item>
        ))}
      </Select>

      <Theme name={selectedTheme}>
        <PreviewCard />
      </Theme>
    </YStack>
  );
}

function PreviewCard() {
  return (
    <YStack
      backgroundColor="$background"
      padding="$4"
      borderRadius="$4"
      borderWidth={1}
      borderColor="$borderColor"
    >
      <Text color="$color" fontSize="$6" fontWeight="bold">
        Preview
      </Text>
      <Text color="$colorTransparent">
        This card uses the selected theme
      </Text>
    </YStack>
  );
}
```

### Storing User Theme Preference

```tsx
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface ThemeStore {
  userTheme: string;
  setUserTheme: (theme: string) => void;
}

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set) => ({
      userTheme: 'ocean',
      setUserTheme: (theme) => set({ userTheme: theme }),
    }),
    {
      name: 'hounii-theme-preference',
      version: 1,
    }
  )
);

// Usage in app root
export function AppWithTheme() {
  const userTheme = useThemeStore((state) => state.userTheme);

  return (
    <Theme name={userTheme}>
      <App />
    </Theme>
  );
}
```

### Theme Configuration in tamagui.config.ts

**Location**: `packages/ui/tamagui.config.ts`

```tsx
import { createTamagui, createTokens } from 'tamagui';
import { createThemes, defaultComponentThemes } from '@tamagui/config/v4';
import * as Colors from '@tamagui/colors';

// 1. Define tokens
const tokens = createTokens({
  color: {
    // Add custom colors
    oceanBlue: '#0080ff',
    forestGreen: '#00cc66',
    sunsetOrange: '#ff6b35',
  },
  size: {
    sm: 38,
    md: 46,
    lg: 60,
  },
  space: {
    // Spacing scale
  },
  radius: {
    // Border radius scale
  },
});

// 2. Create themes
const themes = createThemes({
  componentThemes: defaultComponentThemes,

  base: {
    palette: {
      dark: ['#000', '#111', /* ... */, '#fff'],
      light: ['#fff', '#eee', /* ... */, '#000'],
    },
  },

  childrenThemes: {
    ocean: { /* ... */ },
    forest: { /* ... */ },
    sunset: { /* ... */ },
  },
});

// 3. Create Tamagui config
const config = createTamagui({
  tokens,
  themes,
  // ... other config
});

export default config;
```

### Performance Optimization

**Bundle size optimization** for production:

```tsx
export const themes: TamaguiThemes =
  process.env.TAMAGUI_ENVIRONMENT === 'client' &&
  process.env.NODE_ENV === 'production'
    ? {} // Empty in production (hydrates from CSS)
    : (generatedThemes as any);
```

This reduces bundle size by ~20KB, relying on server-rendered CSS for theme hydration.

### Light and Dark Mode Handling

```tsx
import { useColorScheme } from 'react-native';
import { Theme } from 'tamagui';

export function AdaptiveThemeProvider({ children, userTheme = 'ocean' }) {
  const systemTheme = useColorScheme(); // 'light' or 'dark'

  // Combine user theme with system preference
  const themeName = `${systemTheme}_${userTheme}`;

  return <Theme name={themeName}>{children}</Theme>;
}
```

**Result**:
- User selects "ocean"
- System is in dark mode
- Applied theme: `dark_ocean`

## Component Structure

### Basic Component Template

```tsx
import { styled, Stack, Text } from 'tamagui';
import type { StackProps } from 'tamagui';

// Define props extending Tamagui props
export interface CardProps extends StackProps {
  title: string;
  description?: string;
}

// Create styled component
export const Card = styled(Stack, {
  name: 'Card',
  backgroundColor: '$background',
  padding: '$4',
  borderRadius: '$4',
  borderWidth: 1,
  borderColor: '$borderColor',
  gap: '$2',

  // Variants
  variants: {
    variant: {
      elevated: {
        shadowColor: '$shadowColor',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
      },
      flat: {
        shadowOpacity: 0,
      },
    },
  } as const,

  defaultVariants: {
    variant: 'flat',
  },
});

// Compound component pattern
export function CardContent({ title, description, ...props }: CardProps) {
  return (
    <Card {...props}>
      <Text fontSize="$6" fontWeight="$7" color="$color">
        {title}
      </Text>
      {description && (
        <Text fontSize="$4" color="$colorTransparent">
          {description}
        </Text>
      )}
    </Card>
  );
}
```

## Variants System

### Creating Variants

```tsx
export const Button = styled(Stack, {
  name: 'Button',
  alignItems: 'center',
  justifyContent: 'center',
  paddingHorizontal: '$4',
  paddingVertical: '$3',
  borderRadius: '$4',

  variants: {
    variant: {
      primary: {
        backgroundColor: '$primary',
        color: '$white',
      },
      secondary: {
        backgroundColor: '$secondary',
        color: '$white',
      },
      outline: {
        backgroundColor: 'transparent',
        borderWidth: 1,
        borderColor: '$borderColor',
        color: '$color',
      },
    },

    size: {
      small: {
        paddingHorizontal: '$3',
        paddingVertical: '$2',
        fontSize: '$3',
      },
      medium: {
        paddingHorizontal: '$4',
        paddingVertical: '$3',
        fontSize: '$4',
      },
      large: {
        paddingHorizontal: '$6',
        paddingVertical: '$4',
        fontSize: '$5',
      },
    },

    disabled: {
      true: {
        opacity: 0.5,
        cursor: 'not-allowed',
      },
    },
  } as const,

  defaultVariants: {
    variant: 'primary',
    size: 'medium',
  },
});
```

### Using Variants

```tsx
// Primary medium button (default)
<Button>Click me</Button>

// Secondary small button
<Button variant="secondary" size="small">Small</Button>

// Outline large disabled button
<Button variant="outline" size="large" disabled>
  Disabled
</Button>
```

## Responsive Design

### Media Queries

```tsx
export const Container = styled(Stack, {
  name: 'Container',
  padding: '$4',

  // Mobile-first responsive design
  $sm: {
    padding: '$6',
  },
  $md: {
    padding: '$8',
    maxWidth: 768,
  },
  $lg: {
    padding: '$10',
    maxWidth: 1024,
  },
});
```

**Breakpoints:**
- `$xs`: < 660px (mobile)
- `$sm`: ≥ 660px (tablet portrait)
- `$md`: ≥ 860px (tablet landscape)
- `$lg`: ≥ 1020px (desktop)
- `$xl`: ≥ 1280px (large desktop)

## Pressable Components

### Interactive States

```tsx
export const PressableCard = styled(Stack, {
  name: 'PressableCard',
  backgroundColor: '$background',
  padding: '$4',
  borderRadius: '$4',

  // Hover state (web)
  hoverStyle: {
    backgroundColor: '$backgroundHover',
    cursor: 'pointer',
  },

  // Press state (native + web)
  pressStyle: {
    backgroundColor: '$backgroundPress',
    scale: 0.98,
  },

  // Focus state (accessibility)
  focusStyle: {
    borderColor: '$primary',
    borderWidth: 2,
  },
});
```

## Icons Integration

### Using Lucide Icons

```tsx
import { styled } from 'tamagui';
import { User, Settings, LogOut } from '@tamagui/lucide-icons';

export function IconExample() {
  return (
    <Stack gap="$4">
      {/* Default size */}
      <User color="$color" />

      {/* Custom size */}
      <Settings size={24} color="$primary" />

      {/* With tokens */}
      <LogOut size="$5" color="$error" />
    </Stack>
  );
}
```

## Animation

### Basic Animations

```tsx
import { AnimatePresence } from 'tamagui';

export const AnimatedCard = styled(Stack, {
  name: 'AnimatedCard',
  backgroundColor: '$background',
  padding: '$4',

  animation: 'quick',  // Built-in animation timing

  enterStyle: {
    opacity: 0,
    scale: 0.9,
  },

  exitStyle: {
    opacity: 0,
    scale: 0.9,
  },
});

// Usage with AnimatePresence
function Example() {
  const [show, setShow] = useState(false);

  return (
    <AnimatePresence>
      {show && (
        <AnimatedCard>
          <Text>Animated content</Text>
        </AnimatedCard>
      )}
    </AnimatePresence>
  );
}
```

**Animation timings:**
- `quick`: 100ms
- `medium`: 200ms
- `slow`: 300ms

## Cross-Platform Considerations

### Platform-Specific Styles

```tsx
import { Platform } from 'react-native';

export const PlatformAwareComponent = styled(Stack, {
  name: 'PlatformAwareComponent',
  padding: '$4',

  ...(Platform.OS === 'web' && {
    cursor: 'pointer',
    userSelect: 'none',
  }),

  ...(Platform.OS === 'ios' && {
    shadowColor: '$shadowColor',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  }),

  ...(Platform.OS === 'android' && {
    elevation: 3,
  }),
});
```

### Web-Only Features

```tsx
// Use carefully - ensure graceful fallback on native
{Platform.OS === 'web' && (
  <Stack cursor="pointer" userSelect="none">
    Web-specific
  </Stack>
)}
```

## Accessibility

### Always Include Accessibility Props

```tsx
export function AccessibleButton({ label, onPress }: Props) {
  return (
    <Button
      onPress={onPress}
      accessible
      accessibilityLabel={label}
      accessibilityRole="button"
      accessibilityHint="Double tap to activate"
    >
      <Text>{label}</Text>
    </Button>
  );
}
```

**Required props:**
- `accessible={true}`: Makes element accessible
- `accessibilityLabel`: Screen reader label
- `accessibilityRole`: Element role (button, header, etc.)
- `accessibilityHint`: Additional context

## Component Composition

### Compound Components Pattern

```tsx
// Base Card
export const Card = styled(Stack, {
  name: 'Card',
  backgroundColor: '$background',
  borderRadius: '$4',
  overflow: 'hidden',
});

// Card Header
export const CardHeader = styled(Stack, {
  name: 'CardHeader',
  padding: '$4',
  borderBottomWidth: 1,
  borderBottomColor: '$borderColor',
});

// Card Body
export const CardBody = styled(Stack, {
  name: 'CardBody',
  padding: '$4',
  gap: '$3',
});

// Card Footer
export const CardFooter = styled(Stack, {
  name: 'CardFooter',
  padding: '$4',
  borderTopWidth: 1,
  borderTopColor: '$borderColor',
  flexDirection: 'row',
  justifyContent: 'flex-end',
  gap: '$2',
});

// Usage
function Example() {
  return (
    <Card>
      <CardHeader>
        <Text fontSize="$6" fontWeight="$7">Title</Text>
      </CardHeader>
      <CardBody>
        <Text>Content goes here</Text>
      </CardBody>
      <CardFooter>
        <Button variant="outline">Cancel</Button>
        <Button>Confirm</Button>
      </CardFooter>
    </Card>
  );
}
```

## Common Pitfalls

### ❌ Hardcoded Values

```tsx
// ❌ WRONG
<View backgroundColor="#ffffff" padding={16} />

// ✅ CORRECT
<View backgroundColor="$background" padding="$4" />
```

### ❌ Inline Styles

```tsx
// ❌ WRONG - loses theme support
<View style={{ backgroundColor: '#fff' }} />

// ✅ CORRECT - uses tokens
<View backgroundColor="$background" />
```

### ❌ Missing Dark Mode Support

```tsx
// ❌ WRONG - only works in light mode
<View backgroundColor="#ffffff">
  <Text color="#000000">Text</Text>
</View>

// ✅ CORRECT - adapts to theme
<View backgroundColor="$background">
  <Text color="$color">Text</Text>
</View>
```

### ❌ Platform-Specific Code Without Fallback

```tsx
// ❌ WRONG - breaks on native
<View cursor="pointer" />

// ✅ CORRECT - web-only
<View {...(Platform.OS === 'web' && { cursor: 'pointer' })} />
```

## When to Extend the Theme

**Extend `tamagui.config.ts` when**:
- ✅ You need a semantic token used across the entire app (e.g., `$colorSecondary`)
- ✅ You need custom brand colors as tokens
- ✅ Multiple components will use the same custom value

**DON'T extend when**:
- ❌ One-off colors (just use `$gray10` directly)
- ❌ Component-specific styling (use styled() variants instead)
- ❌ Local overrides (use inline props)

**Example - When to extend**:
```typescript
// ✅ GOOD - Used everywhere in the app
themes: {
  light: {
    colorSecondary: '$gray11',    // Used by all secondary text
    backgroundHover: '$gray2',    // Used by all hover states
  }
}

// ❌ BAD - Just use standard tokens directly
themes: {
  light: {
    myButtonColor: '$blue10',  // Just use $blue10 in the component
  }
}
```

## Component Checklist

When creating a Tamagui component:

- [ ] **Design Tokens**
  - [ ] Uses `$` tokens for colors, spacing, typography
  - [ ] No hardcoded values
  - [ ] No `as any` type casts

- [ ] **Theme Compatibility**
  - [ ] Works in light mode
  - [ ] Works in dark mode
  - [ ] Uses semantic tokens (`$background`, `$color`)

- [ ] **Variants**
  - [ ] Includes common variants (size, variant, disabled)
  - [ ] Has sensible default variants
  - [ ] Variants use design tokens

- [ ] **Responsiveness**
  - [ ] Uses responsive breakpoints (`$sm`, `$md`, `$lg`)
  - [ ] Mobile-first approach
  - [ ] Tested on multiple screen sizes

- [ ] **Accessibility**
  - [ ] Includes `accessible` prop
  - [ ] Has `accessibilityLabel`
  - [ ] Defines `accessibilityRole`
  - [ ] Keyboard navigation support (web)

- [ ] **Cross-Platform**
  - [ ] Works on React Native (iOS/Android)
  - [ ] Works on Web
  - [ ] Platform-specific code has fallbacks

- [ ] **Interactive States**
  - [ ] `hoverStyle` for web hover
  - [ ] `pressStyle` for press feedback
  - [ ] `focusStyle` for keyboard focus

- [ ] **Performance**
  - [ ] Uses `styled()` for static styles
  - [ ] Avoids inline styles
  - [ ] Memoizes expensive computations

- [ ] **Type Safety**
  - [ ] Exports TypeScript props interface
  - [ ] Extends appropriate Tamagui base props
  - [ ] No `any` types

## Package Structure

```
packages/ui/
├── src/
│   ├── components/
│   │   ├── Button.tsx
│   │   ├── Card.tsx
│   │   ├── Input.tsx
│   │   └── index.ts
│   ├── theme/
│   │   ├── tokens.ts
│   │   └── themes.ts
│   └── index.ts
└── package.json
```

## References

- Main config: [CLAUDE.md](../../../CLAUDE.md)
- UI package: [packages/ui/](../../../packages/ui/)
- Tamagui docs: https://tamagui.dev
