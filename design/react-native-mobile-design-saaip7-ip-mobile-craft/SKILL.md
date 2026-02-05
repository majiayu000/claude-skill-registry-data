---
name: react-native-mobile-design
description: Create distinctive, production-grade React Native mobile applications with modern best practices. Use this skill when the user asks to build React Native components, screens, or complete mobile apps for iOS and Android. Handles UI creation from scratch, design-to-code conversion (Figma/mockups), state management (Zustand, Redux Toolkit), navigation (React Navigation), styling (NativeWind, StyleSheet), and performance optimization. Generates beautiful, performant cross-platform code.
---

This skill guides creation of distinctive, production-grade React Native mobile applications. Implement real working TypeScript/React Native code with attention to aesthetics, performance, and platform conventions.

## Design Thinking

Before coding, understand context and commit to a design direction:

- **Purpose**: What problem does this app solve? Who uses it?
- **Platform**: iOS, Android, or both? Consider platform-specific patterns.
- **Tone**: Vibrant & playful, calm & professional, bold & expressive, minimal & clean.
- **Design System**: React Native Paper (M3), NativeBase, Tamagui, or custom.

## Recommended Stack

| Category | Recommended | Alternative |
|----------|-------------|-------------|
| **Runtime** | Expo | Bare React Native |
| **Language** | TypeScript | - |
| **State** | Zustand | Redux Toolkit, Jotai |
| **Server State** | TanStack Query | SWR |
| **Navigation** | React Navigation 6+ | Expo Router |
| **Styling** | NativeWind | StyleSheet, Tamagui |
| **UI Library** | React Native Paper | NativeBase |
| **Animations** | Reanimated 3 | Animated API |
| **Lists** | FlashList | FlatList |

## Quick Patterns

### NativeWind Styling
```tsx
<View className="flex-1 bg-white p-4">
  <Text className="text-xl font-bold text-gray-900">Title</Text>
  <Pressable className="bg-blue-500 py-3 px-6 rounded-xl active:opacity-80">
    <Text className="text-white font-semibold text-center">Button</Text>
  </Pressable>
</View>
```

### Zustand Store
```tsx
import { create } from 'zustand';

interface AuthStore {
  user: User | null;
  login: (user: User) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthStore>((set) => ({
  user: null,
  login: (user) => set({ user }),
  logout: () => set({ user: null }),
}));
```

### Navigation Setup
```tsx
const Stack = createNativeStackNavigator<RootStackParamList>();

function RootNavigator() {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Detail" component={DetailScreen} />
    </Stack.Navigator>
  );
}
```

### Optimized List
```tsx
import { FlashList } from '@shopify/flash-list';

<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={100}
  keyExtractor={(item) => item.id}
/>
```

## Project Structure

```
src/
├── app/                    # Expo Router or entry
├── components/
│   ├── ui/                 # Button, Input, Card
│   └── features/           # ProductCard, CartItem
├── hooks/                  # Custom hooks
├── stores/                 # Zustand stores
├── services/               # API calls
├── utils/                  # Helpers
└── types/                  # TypeScript types
```

## Platform-Specific Code

```tsx
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 8,
    },
    android: {
      elevation: 4,
    },
  }),
});
```

## Quality Checklist

- [ ] TypeScript strict mode
- [ ] Dark mode support (`useColorScheme`)
- [ ] Safe area handling
- [ ] Accessibility labels
- [ ] Loading & error states
- [ ] Keyboard avoiding for forms
- [ ] 60fps animations

## Advanced Topics

For detailed implementation guides:

- **Performance & Optimization**: See [references/optimization.md](references/optimization.md) for startup time, memory, bundle size, rendering optimization
- **Component Patterns & Architecture**: See [references/patterns.md](references/patterns.md) for reusable patterns, animations, advanced navigation

## Code Style

```tsx
// Prefer: TypeScript, memo, proper typing
import { memo, useCallback } from 'react';

interface Props {
  item: Product;
  onPress?: (id: string) => void;
}

export const ProductCard = memo(function ProductCard({ item, onPress }: Props) {
  const handlePress = useCallback(() => onPress?.(item.id), [item.id, onPress]);

  return (
    <Pressable onPress={handlePress} className="bg-white rounded-2xl p-4">
      <Text className="text-lg font-semibold">{item.name}</Text>
    </Pressable>
  );
});
```

## Restricted

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

Generate distinctive, crafted React Native code. Avoid generic boilerplate.
