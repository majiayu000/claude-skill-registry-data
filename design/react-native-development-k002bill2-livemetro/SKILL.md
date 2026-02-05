---
name: react-native-development
description: React Native component development with TypeScript, Expo, and React Navigation. Use when creating UI components, screens, or implementing navigation flows.
---

# React Native Development Guidelines

## When to Use This Skill
- Creating new React Native components
- Building screens with navigation
- Implementing custom hooks
- Working with Expo SDK features
- Styling with StyleSheet and responsive design

## Core Principles

### 1. Component Structure
```tsx
import React, { memo } from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface ComponentProps {
  // Props with JSDoc comments
  title: string;
  onPress?: () => void;
}

export const Component: React.FC<ComponentProps> = memo(({
  title,
  onPress
}) => {
  // 1. Hooks (useState, useEffect, custom hooks)
  // 2. Derived state
  // 3. Event handlers
  // 4. Return JSX

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
    </View>
  );
});

Component.displayName = 'Component';

const styles = StyleSheet.create({
  container: {
    // Styles here
  },
  title: {
    // Styles here
  },
});
```

### 2. File Organization
```
src/
├── components/        # Reusable UI components
│   └── train/        # Domain-specific components
├── screens/          # Screen components
│   └── home/         # Feature-based screens
├── hooks/            # Custom React hooks
├── navigation/       # Navigation configuration
└── utils/            # Helper functions
```

### 3. TypeScript Standards
- Always use TypeScript strict mode
- Define interfaces for all component props
- Use type inference where possible
- Avoid `any` type - use `unknown` with type guards

### 4. Performance Best Practices
```tsx
// Use memo for expensive components
export const ExpensiveComponent = memo(({ data }) => {
  // Component logic
}, (prevProps, nextProps) => {
  // Custom comparison if needed
  return prevProps.data === nextProps.data;
});

// Use useMemo for expensive calculations
const processedData = useMemo(() => {
  return heavyComputation(data);
}, [data]);

// Use useCallback for stable callback references
const handlePress = useCallback(() => {
  // Handler logic
}, [dependencies]);
```

### 5. Navigation Pattern
```tsx
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import { AppStackParamList } from '@/navigation/types';

type Props = NativeStackScreenProps<AppStackParamList, 'ScreenName'>;

export const ScreenComponent: React.FC<Props> = ({ navigation, route }) => {
  const handleNavigate = () => {
    navigation.navigate('OtherScreen', {
      param: 'value'
    });
  };

  // Screen implementation
};
```

### 6. Error Handling
```tsx
const [error, setError] = useState<string | null>(null);

try {
  await someAsyncOperation();
} catch (err) {
  setError(err instanceof Error ? err.message : 'Unknown error');
  console.error('Operation failed:', err);
}

// Display error to user
{error && (
  <Text style={styles.error}>{error}</Text>
)}
```

## Styling Guidelines

### 1. Responsive Design
```tsx
import { Dimensions, Platform } from 'react-native';

const { width, height } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    width: width * 0.9,
    padding: width < 375 ? 12 : 16, // Smaller phones
  },
});
```

### 2. Platform-Specific Styles
```tsx
const styles = StyleSheet.create({
  text: {
    ...Platform.select({
      ios: {
        fontFamily: 'System',
      },
      android: {
        fontFamily: 'Roboto',
      },
    }),
  },
});
```

## Common Patterns

### 1. Loading States
```tsx
const [loading, setLoading] = useState(true);
const [data, setData] = useState<DataType | null>(null);

useEffect(() => {
  fetchData()
    .then(setData)
    .finally(() => setLoading(false));
}, []);

if (loading) {
  return <ActivityIndicator size="large" />;
}
```

### 2. List Rendering
```tsx
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <ItemComponent item={item} />}
  ListEmptyComponent={<EmptyState />}
  ListHeaderComponent={<Header />}
  onEndReached={loadMore}
  onEndReachedThreshold={0.5}
/>
```

### 3. Form Input Handling
```tsx
const [value, setValue] = useState('');

<TextInput
  value={value}
  onChangeText={setValue}
  placeholder="Enter text"
  autoCapitalize="none"
  autoCorrect={false}
/>
```

## Testing Requirements
- Write unit tests for all components
- Test user interactions
- Test error states
- Mock API calls and navigation

## Accessibility
- Add `accessibilityLabel` to touchable elements
- Use `accessibilityRole` appropriately
- Ensure proper contrast ratios
- Support screen readers

## Important Notes
- Always use path aliases (@/) instead of relative imports
- Clean up subscriptions and timers in useEffect cleanup
- Handle keyboard dismissal on iOS and Android
- Test on both platforms before committing
