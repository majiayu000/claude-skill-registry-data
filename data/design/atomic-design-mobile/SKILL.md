---
name: atomic-design-mobile
description: Atomic Design component organization pattern for React Native mobile applications. Use when creating new components with proper accessibility and touch targets.
---

# Atomic Design Mobile Skill

This skill covers the Atomic Design pattern for organizing React Native components with mobile-specific considerations including accessibility, touch targets, and platform differences.

## When to Use

Use this skill when:
- Creating new mobile components
- Organizing existing component structures
- Deciding where a component should live
- Ensuring accessibility compliance
- Handling platform-specific requirements

## Core Principle

**ACCESSIBLE BY DEFAULT** - Every component must meet mobile accessibility standards including touch targets, screen reader support, and platform conventions.

## The Five-Level Hierarchy

| Level | Alternative Name | Description | Examples | State | Storybook |
|-------|------------------|-------------|----------|-------|-----------|
| **Atoms** | Elements | Basic building blocks | Button, Input, Text, Icon | Stateless | Yes |
| **Molecules** | Widgets | Functional units combining atoms | SearchBar, FormField, ListItem | Minimal state | Yes |
| **Organisms** | Modules | Complex UI sections | Header, TabBar, LoginForm | Can have state | Yes |
| **Templates** | Layouts | Screen-level layout structures | ScreenLayout, AuthLayout | Layout state only | No |
| **Screens** | - | Specific template instances | Login screen, Dashboard screen | Full state | No |

## Mobile-Specific Requirements by Level

### Atoms

- **Touch targets:** Minimum 44x44pt (Apple HIG, Material Design)
- **Accessibility props:** `accessibilityLabel`, `accessibilityRole`, `accessibilityState`
- **Platform styling:** Use `Platform.OS` or `Platform.select` when needed
- **Haptic feedback:** Consider `expo-haptics` for interactive elements

### Molecules

- **Keyboard handling:** Use `KeyboardAvoidingView` for form inputs
- **Gesture support:** Use `react-native-gesture-handler` when needed
- **Safe areas:** Consider safe area insets for edge components

### Organisms

- **Platform awareness:** iOS vs Android visual differences
- **Safe areas:** Use `useSafeAreaInsets` for edge sections
- **Navigation integration:** Consider navigation context

### Templates

- **Screen layout:** Handle status bar, navigation bar
- **Safe areas:** Manage all safe area insets
- **Keyboard avoidance:** Global keyboard handling
- **Orientation:** Support orientation changes

## Component Classification Decision

Use this flowchart to determine the correct atomic level:

| Question | Answer | Level |
|----------|--------|-------|
| Can it be broken down further? | No | **Atom** |
| Does it combine atoms for a single purpose? | Yes | **Molecule** |
| Is it a larger section with business logic? | Yes | **Organism** |
| Does it define screen structure without content? | Yes | **Template** |
| Does it have real content and data connections? | Yes | **Screen** |

## Classification Checklists

### Is it an Atom?

- [ ] Cannot be broken down into smaller components
- [ ] Single basic element (Pressable, TextInput, Text, Image)
- [ ] No business logic
- [ ] Stateless or only UI state (pressed, focused)
- [ ] No dependencies on other custom components
- [ ] Has minimum 44pt touch target
- [ ] Has accessibility props

### Is it a Molecule?

- [ ] Combines 2+ atoms
- [ ] Single functional purpose
- [ ] Minimal internal state
- [ ] No data fetching
- [ ] No connection to global state
- [ ] Handles keyboard avoidance if containing inputs

### Is it an Organism?

- [ ] Larger interface section
- [ ] May have business logic
- [ ] May connect to stores
- [ ] Relatively standalone
- [ ] Could be used across multiple screens
- [ ] Handles safe areas if at screen edges

### Is it a Template?

- [ ] Defines screen structure
- [ ] Uses slots/children for content
- [ ] No real data
- [ ] Handles safe areas, status bar, keyboard
- [ ] Manages screen-level layout concerns

### Is it a Screen?

- [ ] Uses a template
- [ ] Has real content
- [ ] Connects to data sources
- [ ] Handles routing/navigation

## Code Examples

### Atom Example

```typescript
// components/atoms/Button/Button.tsx
import { Pressable, Text, ActivityIndicator, StyleSheet, Platform } from 'react-native';

interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  onPress?: () => void;
  children: string;
  accessibilityLabel?: string;
}

export function Button({
  variant,
  size = 'md',
  loading,
  disabled,
  onPress,
  children,
  accessibilityLabel,
}: ButtonProps) {
  return (
    <Pressable
      style={({ pressed }) => [
        styles.base,
        styles[variant],
        styles[size],
        (disabled || loading) && styles.disabled,
        pressed && styles.pressed,
      ]}
      onPress={onPress}
      disabled={disabled || loading}
      accessibilityLabel={accessibilityLabel || children}
      accessibilityRole="button"
      accessibilityState={{ disabled: disabled || loading }}
    >
      {loading && <ActivityIndicator color="#fff" style={styles.spinner} />}
      <Text style={[styles.text, styles[`${variant}Text`]]}>{children}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: 8,
    minHeight: 44, // Minimum touch target
    minWidth: 44,
  },
  primary: {
    backgroundColor: '#2563eb',
  },
  secondary: {
    backgroundColor: '#e5e7eb',
  },
  danger: {
    backgroundColor: '#dc2626',
  },
  sm: {
    paddingHorizontal: 12,
    paddingVertical: 8,
  },
  md: {
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  lg: {
    paddingHorizontal: 24,
    paddingVertical: 16,
  },
  disabled: {
    opacity: 0.5,
  },
  pressed: {
    opacity: 0.8,
  },
  spinner: {
    marginRight: 8,
  },
  text: {
    fontWeight: '600',
  },
  primaryText: {
    color: '#ffffff',
  },
  secondaryText: {
    color: '#111827',
  },
  dangerText: {
    color: '#ffffff',
  },
});
```

### Molecule Example

```typescript
// components/molecules/FormField/FormField.tsx
import { View, Text, TextInput, StyleSheet } from 'react-native';

interface FormFieldProps {
  label: string;
  value: string;
  onChangeText: (text: string) => void;
  placeholder?: string;
  error?: string;
  required?: boolean;
  secureTextEntry?: boolean;
  keyboardType?: 'default' | 'email-address' | 'numeric' | 'phone-pad';
  accessibilityLabel?: string;
}

export function FormField({
  label,
  value,
  onChangeText,
  placeholder,
  error,
  required,
  secureTextEntry,
  keyboardType = 'default',
  accessibilityLabel,
}: FormFieldProps) {
  const inputAccessibilityLabel = accessibilityLabel || `${label}${required ? ', required' : ''}`;

  return (
    <View style={styles.container}>
      <Text style={styles.label}>
        {label}
        {required && <Text style={styles.required}> *</Text>}
      </Text>
      <TextInput
        style={[styles.input, error && styles.inputError]}
        value={value}
        onChangeText={onChangeText}
        placeholder={placeholder}
        secureTextEntry={secureTextEntry}
        keyboardType={keyboardType}
        accessibilityLabel={inputAccessibilityLabel}
        accessibilityState={{ disabled: false }}
        accessibilityHint={error}
      />
      {error && (
        <Text style={styles.error} accessibilityRole="alert">
          {error}
        </Text>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    marginBottom: 16,
  },
  label: {
    fontSize: 14,
    fontWeight: '500',
    color: '#374151',
    marginBottom: 4,
  },
  required: {
    color: '#dc2626',
  },
  input: {
    borderWidth: 1,
    borderColor: '#d1d5db',
    borderRadius: 8,
    paddingHorizontal: 12,
    paddingVertical: 12,
    fontSize: 16,
    minHeight: 44, // Minimum touch target
  },
  inputError: {
    borderColor: '#dc2626',
  },
  error: {
    fontSize: 12,
    color: '#dc2626',
    marginTop: 4,
  },
});
```

### Organism Example

```typescript
// components/organisms/LoginForm/LoginForm.tsx
import { useState } from 'react';
import { View, StyleSheet, KeyboardAvoidingView, Platform } from 'react-native';
import { Button } from '@/components/atoms';
import { FormField } from '@/components/molecules';

interface LoginFormProps {
  onSubmit: (email: string, password: string) => Promise<void>;
}

export function LoginForm({ onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = (): boolean => {
    const newErrors: Record<string, string> = {};
    if (!email) newErrors.email = 'Email is required';
    if (!password) newErrors.password = 'Password is required';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) return;

    setLoading(true);
    try {
      await onSubmit(email, password);
    } catch {
      setErrors({ form: 'Invalid credentials' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <FormField
        label="Email"
        value={email}
        onChangeText={setEmail}
        placeholder="you@example.com"
        keyboardType="email-address"
        error={errors.email}
        required
      />
      <FormField
        label="Password"
        value={password}
        onChangeText={setPassword}
        placeholder="Enter password"
        secureTextEntry
        error={errors.password}
        required
      />
      <Button
        variant="primary"
        onPress={handleSubmit}
        loading={loading}
        accessibilityLabel="Sign in"
      >
        Sign In
      </Button>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
  },
});
```

### Template Example

```typescript
// components/templates/ScreenLayout/ScreenLayout.tsx
import { SafeAreaView, View, StyleSheet, StatusBar, Platform } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { Header } from '@/components/organisms';

interface ScreenLayoutProps {
  children: React.ReactNode;
  title?: string;
  showHeader?: boolean;
  showBackButton?: boolean;
  onBack?: () => void;
}

export function ScreenLayout({
  children,
  title,
  showHeader = true,
  showBackButton = false,
  onBack,
}: ScreenLayoutProps) {
  const insets = useSafeAreaInsets();

  return (
    <View style={[styles.container, { paddingTop: insets.top }]}>
      <StatusBar barStyle="dark-content" />
      {showHeader && (
        <Header
          title={title}
          showBackButton={showBackButton}
          onBack={onBack}
        />
      )}
      <View style={[styles.content, { paddingBottom: insets.bottom }]}>
        {children}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  content: {
    flex: 1,
    padding: 16,
  },
});
```

### Screen Example (Expo Router)

```typescript
// app/(auth)/login.tsx
import { useRouter } from 'expo-router';
import { AuthLayout } from '@/components/templates';
import { LoginForm } from '@/components/organisms';
import { useAuth } from '@/hooks/useAuth';

export default function LoginScreen() {
  const router = useRouter();
  const { login } = useAuth();

  const handleLogin = async (email: string, password: string) => {
    await login(email, password);
    router.replace('/(tabs)');
  };

  return (
    <AuthLayout title="Welcome Back" subtitle="Sign in to your account">
      <LoginForm onSubmit={handleLogin} />
    </AuthLayout>
  );
}
```

## React Native Storybook Story Templates

### Atom Story Template

```typescript
// Button.stories.tsx
import type { Meta, StoryObj } from '@storybook/react-native';
import { Button } from './Button';

const meta: Meta<typeof Button> = {
  title: 'Atoms/Button',
  component: Button,
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger'],
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
    },
    loading: { control: 'boolean' },
    disabled: { control: 'boolean' },
  },
};

export default meta;
type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Button',
  },
};

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Button',
  },
};

export const Loading: Story = {
  args: {
    variant: 'primary',
    children: 'Saving...',
    loading: true,
  },
};

export const Disabled: Story = {
  args: {
    variant: 'primary',
    children: 'Disabled',
    disabled: true,
  },
};
```

### Molecule Story Template

```typescript
// FormField.stories.tsx
import type { Meta, StoryObj } from '@storybook/react-native';
import { useState } from 'react';
import { FormField } from './FormField';

const meta: Meta<typeof FormField> = {
  title: 'Molecules/FormField',
  component: FormField,
};

export default meta;
type Story = StoryObj<typeof FormField>;

// Wrapper for controlled input
function FormFieldWrapper(props: any) {
  const [value, setValue] = useState('');
  return <FormField {...props} value={value} onChangeText={setValue} />;
}

export const Default: Story = {
  render: () => (
    <FormFieldWrapper
      label="Email"
      placeholder="you@example.com"
    />
  ),
};

export const WithError: Story = {
  render: () => (
    <FormFieldWrapper
      label="Email"
      error="Email is required"
      required
    />
  ),
};

export const Password: Story = {
  render: () => (
    <FormFieldWrapper
      label="Password"
      placeholder="Enter password"
      secureTextEntry
      required
    />
  ),
};
```

### Organism Story Template

```typescript
// LoginForm.stories.tsx
import type { Meta, StoryObj } from '@storybook/react-native';
import { LoginForm } from './LoginForm';

const meta: Meta<typeof LoginForm> = {
  title: 'Organisms/LoginForm',
  component: LoginForm,
};

export default meta;
type Story = StoryObj<typeof LoginForm>;

export const Default: Story = {
  args: {
    onSubmit: async (email, password) => {
      console.log('Login:', { email, password });
      await new Promise((resolve) => setTimeout(resolve, 1000));
    },
  },
};
```

## Naming Conventions

```
components/
├── atoms/
│   ├── Button/           # PascalCase - noun
│   ├── Input/
│   ├── Text/
│   └── Icon/
├── molecules/
│   ├── SearchBar/        # PascalCase - descriptive compound
│   ├── FormField/
│   └── ListItem/
├── organisms/
│   ├── Header/           # PascalCase - section name
│   ├── TabBar/
│   └── LoginForm/
├── templates/
│   ├── ScreenLayout/     # PascalCase - always end with "Layout"
│   ├── AuthLayout/
│   └── TabLayout/
└── index.ts

app/                      # Screens via Expo Router
├── (auth)/
│   ├── login.tsx         # lowercase - Expo Router convention
│   └── register.tsx
└── (tabs)/
    ├── index.tsx
    └── profile.tsx
```

## Import Strategy

```typescript
// Within same level - use relative imports
import { Button } from '../Button';

// Across levels - use path alias (no src/ prefix for Expo)
import { Button, Input } from '@/components/atoms';
import { SearchBar, FormField } from '@/components/molecules';
import { Header, LoginForm } from '@/components/organisms';
import { ScreenLayout, AuthLayout } from '@/components/templates';

// From top-level barrel
import { Button, Input, SearchBar, Header } from '@/components';
```

### Path Alias Configuration (Expo)

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

**Note:** Expo projects do not use a `src/` directory.

## Barrel Export Patterns

### Atom Level Barrel Export

```typescript
// components/atoms/index.ts
export { Button } from './Button';
export { Input } from './Input';
export { Text } from './Text';
export { Icon } from './Icon';
export { Avatar } from './Avatar';
export { Spinner } from './Spinner';

// Re-export types
export type { ButtonProps } from './Button';
export type { InputProps } from './Input';
```

### Molecule Level Barrel Export

```typescript
// components/molecules/index.ts
export { SearchBar } from './SearchBar';
export { FormField } from './FormField';
export { ListItem } from './ListItem';
export { Card } from './Card';

export type { FormFieldProps } from './FormField';
```

### Organism Level Barrel Export

```typescript
// components/organisms/index.ts
export { Header } from './Header';
export { TabBar } from './TabBar';
export { LoginForm } from './LoginForm';
export { BottomSheet } from './BottomSheet';

export type { LoginFormProps } from './LoginForm';
```

### Template Level Barrel Export

```typescript
// components/templates/index.ts
export { ScreenLayout } from './ScreenLayout';
export { AuthLayout } from './AuthLayout';
export { TabLayout } from './TabLayout';
```

### Main Barrel Export

```typescript
// components/index.ts
export * from './atoms';
export * from './molecules';
export * from './organisms';
export * from './templates';
```

## Accessibility Checklist

### Every Atom Must Have

- [ ] `accessibilityLabel` - descriptive text for screen readers
- [ ] `accessibilityRole` - semantic role (button, link, image, etc.)
- [ ] `accessibilityState` - current state (disabled, selected, checked)
- [ ] Minimum 44x44pt touch target
- [ ] Visible focus indicator (where applicable)

### Every Interactive Element Must Have

- [ ] `accessibilityHint` - describes action result (optional but recommended)
- [ ] Proper contrast ratio (4.5:1 for text)
- [ ] Touch feedback (pressed state visual change)

### Example Accessibility Props

```typescript
<Pressable
  accessibilityLabel="Submit form"
  accessibilityRole="button"
  accessibilityState={{ disabled: isDisabled }}
  accessibilityHint="Submits the login form"
>
  <Text>Submit</Text>
</Pressable>
```

## Platform-Specific Patterns

### Using Platform.OS

```typescript
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    paddingTop: Platform.OS === 'ios' ? 20 : 0,
  },
});
```

### Using Platform.select

```typescript
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.25,
      shadowRadius: 4,
    },
    android: {
      elevation: 4,
    },
    default: {},
  }),
});
```

## Best Practices

1. **Touch targets first** - Every interactive element is at least 44x44pt
2. **Accessibility always** - Never skip accessibilityLabel and accessibilityRole
3. **Use StyleSheet** - Create styles outside components for performance
4. **Pressable over TouchableOpacity** - Better accessibility support
5. **Safe areas everywhere** - Handle notches, home indicators, status bars
6. **Keyboard avoidance** - Wrap forms in KeyboardAvoidingView
7. **Platform awareness** - Test on both iOS and Android
8. **Test with VoiceOver/TalkBack** - Verify screen reader experience

## Notes

- Expo projects do not use a `src/` directory
- Templates and Screens do not get Storybook stories
- React Native Storybook runs on-device, not in browser
- Brad Frost's original article: https://bradfrost.com/blog/post/atomic-web-design/
