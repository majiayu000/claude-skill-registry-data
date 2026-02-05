---
name: react-conventions
description: React and React Native coding conventions with TypeScript. Use this skill when creating components, writing hooks, or reviewing React/React Native code. Enforces naming conventions, component structure, typing patterns, accessibility, and performance best practices.
---

# React Conventions

Coding conventions for React and React Native with TypeScript. It defines how to write good components, props, hooks and styles with tailwind (uniwind).
By keeping in mind accessibility, performances (with and without react-compiler) and testability.

## Exports & Naming

### Named exports only

```typescript
// ✅ Good
export const Button: FC<ButtonProps> = ({ label }) => { ... };

// ❌ Bad
export default function Button({ label }) { ... }
```

### Component typing

Always use `FC<Props>` with arrow functions:

```typescript
// ✅ Good
interface ButtonProps {
  label: string;
  onPress: VoidFunction;
}

export const Button: FC<ButtonProps> = ({ label, onPress }) => {
  return <Pressable onPress={onPress}><Text>{label}</Text></Pressable>;
};

// ❌ Bad
export function Button(props: ButtonProps) { ... }
export const Button = ({ label }: ButtonProps) => { ... }; // Missing FC
```

### Naming conventions

| Element          | Convention                  | Example            |
| ---------------- | --------------------------- | ------------------ |
| Component        | PascalCase                  | `UserProfile.tsx`  |
| Props interface  | `[Component]Props`          | `UserProfileProps` |
| Hook             | camelCase with `use` prefix | `useAuth.ts`       |
| Hook return type | `[Hook]Return`              | `UseAuthReturn`    |

## Component Structure

Order within a component file:

```typescript
// 1. Imports
import { FC, useState } from "react";
import { View, Text, Pressable } from "react-native";

// 2. Types
type UserCardProps = Readonly<{
  name: string;
  avatarUrl?: string;
  onPress: VoidFunction;
}>;

// 3. Component
export const UserCard: FC<UserCardProps> = ({ name, avatarUrl, onPress }) => {
  // 3a. Hooks
  const [isPressed, setIsPressed] = useState(false);

  // 3b. Derived state / computed values
  const displayName = name.toUpperCase();

  // 3c. Handlers
  const handlePress = () => {
    setIsPressed(true);
    onPress();
  };

  // 3d. Render
  return (
    <Pressable onPress={handlePress} className="p-4 bg-white rounded-lg">
      <Text className="text-lg font-bold">{displayName}</Text>
    </Pressable>
  );
};
```

### JSX readability

Extract complex logic from JSX:

```typescript
// ✅ Good
const showError = hasError && !isLoading;
const statusText = isOnline ? "Connected" : "Offline";

return (
  <View>
    {showError && <ErrorMessage />}
    <Text>{statusText}</Text>
  </View>
);

// ❌ Bad
return (
  <View>
    {hasError && !isLoading && <ErrorMessage />}
    <Text>{isOnline ? "Connected" : "Offline"}</Text>
  </View>
);
```

## Props

### Readonly by default

Use the `Readonly` utility type:

```typescript
// ✅ Good
type CardProps = Readonly<{
  title: string;
  subtitle?: string;
}>;

// ❌ Bad — verbose
interface CardProps {
  readonly title: string;
  readonly subtitle?: string;
}
```

### Children with PropsWithChildren

```typescript
// ✅ Good — use PropsWithChildren
type ContainerProps = PropsWithChildren<
  Readonly<{
    padding?: number;
  }>
>;

// Or with no additional props
type WrapperProps = PropsWithChildren;

// ❌ Bad — manual children typing
type ContainerProps = Readonly<{
  children: ReactNode;
  padding?: number;
}>;
```

### Default values via destructuring

```typescript
// ✅ Good
export const Button: FC<ButtonProps> = ({
  variant = "primary",
  size = "medium",
  disabled = false,
}) => { ... };

// ❌ Bad — deprecated pattern
Button.defaultProps = {
  variant: "primary",
};
```

### Optional vs required

Be intentional:

```typescript
type FormFieldProps = Readonly<{
  // Required — component cannot function without these
  label: string;
  value: string;
  onChange: (value: string) => void;

  // Optional — sensible defaults exist
  placeholder?: string;
  disabled?: boolean;
  errorMessage?: string;
}>;
```

## Hooks

### Naming

```typescript
// ✅ Good
const useAuth = () => { ... };
const useUserProfile = (userId: string) => { ... };

// ❌ Bad
const authHook = () => { ... };
const getUserProfile = () => { ... };
```

### One hook per file

```
hooks/
├── useAuth.ts
├── useToggle.ts
└── useDebounce.ts
```

### Explicit return type

```typescript
// ✅ Good
interface UseToggleReturn {
  isOn: boolean;
  toggle: VoidFunction;
  setOn: VoidFunction;
  setOff: VoidFunction;
}

export const useToggle = (initial = false): UseToggleReturn => {
  const [isOn, setIsOn] = useState(initial);

  return {
    isOn,
    toggle: () => setIsOn((v) => !v),
    setOn: () => setIsOn(true),
    setOff: () => setIsOn(false),
  };
};
```

### Rules of hooks

```typescript
// ✅ Good — hooks at top level, stable order
export const Component: FC<Props> = ({ userId }) => {
  const [state, setState] = useState(null);
  const user = useUser(userId);

  // ...
};

// ❌ Bad — conditional hook
export const Component: FC<Props> = ({ userId }) => {
  if (userId) {
    const user = useUser(userId); // ❌ Conditional
  }
};

// ❌ Bad — hook in loop
items.map((item) => {
  const data = useData(item.id); // ❌ In loop
});
```

## Performance

### React Compiler

React 19+ with React Compiler handles most memoization automatically. Avoid premature optimization:

```typescript
// ✅ With React Compiler — usually no manual memoization needed
export const List: FC<ListProps> = ({ items, onItemPress }) => {
  const sortedItems = items.sort((a, b) => a.name.localeCompare(b.name));

  return (
    <FlatList
      data={sortedItems}
      renderItem={({ item }) => (
        <ListItem item={item} onPress={() => onItemPress(item.id)} />
      )}
    />
  );
};
```

### When to manually optimize

Only optimize when you measure a performance problem:

```typescript
// Manual memo — only if React Compiler is not enabled or insufficient
export const ExpensiveComponent: FC<Props> = memo(({ data }) => {
  // Heavy render
});

// Manual useCallback — only for non-compiled code or specific perf issues
const handlePress = useCallback(() => {
  onPress(id);
}, [onPress, id]);

// Manual useMemo — only for genuinely expensive computations
const processedData = useMemo(() => {
  return heavyComputation(rawData);
}, [rawData]);
```

### FlatList optimization

```typescript
// ✅ Good
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={renderItem}
  getItemLayout={(_, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
/>;

// Extract renderItem to avoid recreation
const renderItem = useCallback(
  ({ item }: { item: Item }) => <ItemCard item={item} />,
  []
);
```

### Avoid inline arrays in props

```typescript
// ✅ Good — stable reference
const emptyArray: Item[] = [];

<FlatList data={items ?? emptyArray} />

// ❌ Bad — new array reference every render
<FlatList data={items ?? []} />
```

## Styles (React Native + Tailwind)

Using Tailwind CSS via Uniwind or NativeWind.

### Inline className

```typescript
// ✅ Good
<View className="flex-1 p-4 bg-white">
  <Text className="text-lg font-bold text-gray-900">Title</Text>
</View>;

// ❌ Bad — StyleSheet.create
const styles = StyleSheet.create({
  container: { flex: 1, padding: 16 },
});
```

### Conditional styles

```typescript
// ✅ Good — template literals or clsx
<View className={`p-4 ${isActive ? "bg-blue-500" : "bg-gray-200"}`} />

// With clsx
<View className={clsx(
  "p-4 rounded-lg",
  isActive && "bg-blue-500",
  isDisabled && "opacity-50",
)} />

// ❌ Bad — ternary soup
<View className={isActive ? (isLarge ? "p-8 bg-blue-500" : "p-4 bg-blue-500") : "p-4 bg-gray-200"} />
```

### Extract complex styles

```typescript
// ✅ Good — extract to variable when complex
const containerClass = clsx(
  "flex-1 p-4",
  isActive && "bg-blue-500",
  isDisabled && "opacity-50 pointer-events-none",
  size === "large" && "p-8"
);

return <View className={containerClass}>...</View>;
```

### Custom classes (Uniwind)

Uniwind includes a CSS parser. Define reusable classes in `global.css`:

```css
/* global.css */
@import "tailwindcss";
@import "uniwind";

.btn {
  padding-left: 16px;
  padding-right: 16px;
  padding-top: 8px;
  padding-bottom: 8px;
  border-radius: 8px;
  font-weight: 500;
}

.btn-primary {
  background-color: #3b82f6;
  color: white;
}

.btn-secondary {
  background-color: #e5e7eb;
  color: #111827;
}

.card {
  padding: 16px;
  background-color: white;
  border-radius: 12px;
}
```

```typescript
// Usage — combine custom classes with Tailwind utilities
<Pressable className="btn btn-primary" />
<Pressable className={clsx("btn", isPrimary ? "btn-primary" : "btn-secondary")} />
<View className="card shadow-sm" />
```

### Theme values

Use Tailwind config for design tokens:

```typescript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: "#FF6B35",
        secondary: "#004E89",
      },
      spacing: {
        18: "4.5rem",
      },
    },
  },
};

// Usage
<View className="bg-primary p-18" />;
```

## Accessibility

### Required attributes

```typescript
// ✅ Good
<Pressable
  onPress={handlePress}
  accessibilityRole="button"
  accessibilityLabel="Submit form"
  accessibilityHint="Submits your information and proceeds to the next step"
  accessibilityState={{ disabled: isLoading }}
>
  <Text>Submit</Text>
</Pressable>

// ❌ Bad — no accessibility info
<Pressable onPress={handlePress}>
  <Text>Submit</Text>
</Pressable>
```

### Accessibility roles

Use appropriate roles:

| Element          | Role                          |
| ---------------- | ----------------------------- |
| Clickable action | `button`                      |
| Navigation link  | `link`                        |
| Text input       | `none` (handled by TextInput) |
| Image            | `image`                       |
| Header text      | `header`                      |
| Checkbox         | `checkbox`                    |
| Switch           | `switch`                      |
| Tab              | `tab`                         |

### Accessibility state

```typescript
<Pressable
  accessibilityRole="checkbox"
  accessibilityState={{
    checked: isChecked,
    disabled: isDisabled,
  }}
>
  <Text>Accept terms</Text>
</Pressable>
```

### Screen reader considerations

```typescript
// Group related elements
<View accessibilityRole="summary" accessibilityLabel={`${title}. ${subtitle}`}>
  <Text>{title}</Text>
  <Text>{subtitle}</Text>
</View>

// Hide decorative elements
<Image
  source={decorativeIcon}
  accessibilityElementsHidden={true}
  importantForAccessibility="no-hide-descendants"
/>
```

## Testability

### testID from constants only

Never hardcode testIDs. Always use the centralized constants:

```typescript
// constants/testIDs.ts
export const TestIDs = {
  Login: {
    emailInput: "login-email-input",
    passwordInput: "login-password-input",
    submitButton: "login-submit-button",
    errorMessage: "login-error-message",
  },
  Profile: {
    avatar: "profile-avatar",
    nameText: "profile-name-text",
    editButton: "profile-edit-button",
  },
} as const;
```

### Usage

```typescript
// ✅ Good — from constants
import { TestIDs } from "@/constants/testIDs";

<Pressable testID={TestIDs.Login.submitButton} onPress={handleSubmit}>
  <Text>Submit</Text>
</Pressable>

<TextInput
  testID={TestIDs.Login.emailInput}
  value={email}
  onChangeText={setEmail}
/>

// ❌ Bad — hardcoded
<Pressable testID="submit-button" onPress={handleSubmit}>
  <Text>Submit</Text>
</Pressable>
```

### Naming convention

```
Pattern: [screen]-[element]-[action?]
Format: kebab-case

Examples:
- login-email-input
- profile-save-button
- home-user-list
- settings-notifications-toggle
```
