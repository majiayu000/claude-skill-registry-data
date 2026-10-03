---
name: react-native-expert
description: >
  Use when building, optimizing, or debugging cross-platform mobile applications with
  React Native and Expo. Provides guidance for navigation setup, native module integration,
  performance optimization, and platform-specific handling for iOS and Android.
---

# React Native Expert

Senior mobile engineer building production-ready cross-platform applications with React Native and Expo.

## When to Use

- Building a new React Native or Expo mobile app from scratch
- Setting up navigation (tabs, stacks, drawers, deep linking)
- Integrating native modules or platform-specific code
- Optimizing list performance (FlatList, SectionList)
- Handling SafeArea, keyboard avoidance, or platform differences
- Debugging Metro bundler, Xcode, or Gradle build issues
- Configuring Expo SDK projects

**Don't use when:** Building web-only apps, native Swift/Objective-C iOS apps, or native Kotlin/Java Android apps — use the appropriate platform-specific skills instead.

## Core Workflow

1. **Setup** — Scaffold with Expo, configure TypeScript → run `npx expo doctor` to verify environment and SDK compatibility; fix any reported issues before proceeding
2. **Structure** — Organize by feature, set up routing (Expo Router or React Navigation)
3. **Implement** — Build components with platform handling → verify on iOS simulator and Android emulator; check Metro bundler output for errors before moving on
4. **Optimize** — Optimize lists, images, memory → profile with Flipper or React DevTools
5. **Test** — Test on both platforms, prioritize real devices over simulators

### Error Recovery

- **Metro bundler errors** → Clear cache with `npx expo start --clear`, then restart
- **iOS build fails** → Check Xcode logs → resolve native dependency or provisioning issue → rebuild with `npx expo run:ios`
- **Android build fails** → Check `adb logcat` or Gradle output → resolve SDK/NDK version mismatch → rebuild with `npx expo run:android`
- **Native module not found** → Run `npx expo install <module>` to ensure compatible version, then rebuild native layers

## Key Patterns

### Optimized FlatList with memo + useCallback

```tsx
import React, { memo, useCallback } from 'react';
import { FlatList, View, Text, StyleSheet } from 'react-native';

type Item = { id: string; title: string };

const ListItem = memo(({ title, onPress }: { title: string; onPress: () => void }) => (
  <View style={styles.item}>
    <Text onPress={onPress}>{title}</Text>
  </View>
));

const keyExtractor = (item: Item) => item.id;

export function ItemList({ data }: { data: Item[] }) {
  const renderItem = useCallback(
    ({ item }: { item: Item }) => (
      <ListItem title={item.title} onPress={() => console.log(item.id)} />
    ),
    []
  );

  return (
    <FlatList
      data={data}
      renderItem={renderItem}
      keyExtractor={keyExtractor}
      removeClippedSubviews
      maxToRenderPerBatch={10}
    />
  );
}

const styles = StyleSheet.create({
  item: { padding: 16, borderBottomWidth: 1, borderBottomColor: '#eee' },
});
```

### SafeAreaView + Keyboard Avoidance

```tsx
import React from 'react';
import { SafeAreaView, KeyboardAvoidingView, Platform, TextInput, StyleSheet } from 'react-native';

export function SafeForm() {
  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.inner}
      >
        <TextInput placeholder="Enter text" style={styles.input} />
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  inner: { padding: 16 },
  input: { borderWidth: 1, borderColor: '#ccc', borderRadius: 8, padding: 12 },
});
```

### Platform-Specific Code

```tsx
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOpacity: 0.25, shadowRadius: 4 },
      android: { elevation: 4 },
      default: {},
    }),
  },
});
```

## Constraints

### MUST DO

- Use FlatList/SectionList for scrollable lists (never ScrollView for large data)
- Implement `memo` + `useCallback` for list items to prevent unnecessary re-renders
- Wrap top-level content in `SafeAreaView` for device notches and safe areas
- Use `KeyboardAvoidingView` for forms and text input screens
- Handle Android back button behavior in navigation stacks
- Test on both iOS and Android — platform differences are common
- Use `npx expo install` (not `npm install`) for native modules to ensure SDK compatibility

### MUST NOT DO

- Use ScrollView for large or dynamic lists (causes memory and performance issues)
- Use inline styles extensively (creates new style objects every render)
- Hardcode dimensions (use flex, Dimensions API, or responsive helpers)
- Ignore memory leaks from event listeners and subscriptions
- Skip platform-specific testing — behavior differs between iOS and Android
- Use `waitFor`/`setTimeout` for animations (use `react-native-reanimated` instead)
- Render heavy lists without `removeClippedSubviews` or `maxToRenderPerBatch`

## Project Setup Checklist

- [ ] Expo SDK version matches across `package.json` and native binaries
- [ ] `npx expo doctor` passes with no issues
- [ ] TypeScript configured with strict mode
- [ ] Navigation library chosen (Expo Router recommended for file-based routing)
- [ ] Platform-specific folders (`ios/`, `android/`) exist and build successfully
- [ ] ESLint + Prettier configured for `.tsx`/`.ts` files
- [ ] Metro config customized if needed (asset extensions, resolver config)

## Performance Optimization

| Issue | Solution |
|-------|----------|
| Janky scrolling | Use `FlatList` with `removeClippedSubviews`, `maxToRenderPerBatch` |
| Slow re-renders | Wrap components with `memo`, use `useCallback` for handlers |
| Image loading delays | Use `react-native-fast-image`, implement caching |
| Navigation lag | Lazy-load screens, defer heavy computations |
| Memory leaks | Clean up subscriptions in cleanup functions, use `useEffect` return |
| Large bundle size | Use `@expo/config-plugins`, tree-shake unused dependencies |

## Cross-Team Integration

**Related Skills:** `react-expert`, `flutter-expert`, `test-driven-development`, `systematic-debugging`, `mobile-code-impact-assessment`

**Used By:** Any agent building mobile features, especially frontend engineers in DevForge AI or dedicated mobile engineering teams.