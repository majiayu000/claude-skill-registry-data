---
name: react-native
description: Use when building cross-platform mobile apps with React Native or Expo. Covers navigation, platform differences, list performance, native modules, offline behavior, and release builds.
metadata:
  category: mobile
  version: 1.0.0
  tags: [react-native, expo, mobile, navigation, performance]
---

# React Native

## Purpose

Build React Native applications that feel native: lists that scroll at 60fps, navigation that matches platform conventions, and a release pipeline that does not surprise you at submission.

## When to Use

- Building or reviewing a React Native or Expo application.
- Diagnosing list performance or dropped frames.
- Bridging to a native module.
- Setting up over-the-air updates and release builds.

## Capabilities

- Navigation with React Navigation or Expo Router, including deep links.
- Platform-specific behavior and styling.
- List performance: `FlashList`, virtualization, memoized rows.
- Native modules and the new architecture (Fabric, TurboModules).
- Offline support, secure storage, and background tasks.
- Release: EAS Build, OTA updates, store submission.

## Inputs

- The feature set, target platforms, and minimum OS versions.
- Whether native modules are needed (this determines Expo Go versus a dev build).
- Performance requirements, especially for lists and animation.

## Outputs

- A navigation structure with deep-link support.
- Lists that maintain frame rate with realistic data volumes.
- A build and release pipeline for both platforms.

## Workflow

1. **Choose the runtime honestly** — Expo with a development build gives you native modules and the Expo tooling. Expo Go is for prototypes; bare React Native is for teams that need full native control and are prepared to maintain it.
2. **Structure navigation first** — Stacks inside tabs, with a typed route map. Retrofitting deep links into an untyped navigator is painful.
3. **Fix lists before they are slow** — `FlashList` with a stable `keyExtractor`, memoized row components, and a fixed item size where possible. `ScrollView` with a hundred children will drop frames on a mid-range Android.
4. **Handle platform differences explicitly** — `Platform.select` for behavior, not just style. Back-button behavior, safe areas, and permission flows differ genuinely.
5. **Move animation off the JS thread** — Reanimated worklets run on the UI thread. Animating via `setState` will jank the moment the JS thread does anything else.
6. **Test the release build** — Debug builds hide performance problems entirely. Profile in release, on a real mid-range device.

## Best Practices

- The JS thread and the UI thread are separate. Any heavy JavaScript blocks interaction, and it will not show up in a simulator on a fast laptop.
- An inline arrow function as a `renderItem` re-creates every row on every render. Memoize the row component and hoist the callback.
- `useNativeDriver: true` on every `Animated` usage, or use Reanimated. Without it, every frame crosses the bridge.
- Store tokens in `expo-secure-store` or Keychain — never `AsyncStorage`, which is unencrypted plain text.
- Images are the main cause of memory pressure. Size them to the display size; do not load a 4000px original into a 100px thumbnail.
- OTA updates cannot change native code. If you added a native module, the update requires a store release.

## Examples

**A list that stays at 60fps:**

```tsx
const OrderRow = memo(function OrderRow({ order, onPress }: OrderRowProps) {
  return (
    <Pressable onPress={() => onPress(order.id)} style={styles.row}>
      <Text style={styles.title}>{order.reference}</Text>
      <Text style={styles.meta}>{order.customerName}</Text>
    </Pressable>
  );
});

export function OrderList({ orders }: { orders: Order[] }) {
  const router = useRouter();
  const onPress = useCallback((id: string) => router.push(`/orders/${id}`), [router]);

  return (
    <FlashList
      data={orders}
      renderItem={({ item }) => <OrderRow order={item} onPress={onPress} />}
      keyExtractor={(item) => item.id}
      estimatedItemSize={72}          // FlashList needs this to recycle correctly
      removeClippedSubviews
    />
  );
}
```

`onPress` is hoisted and stable, `OrderRow` is memoized, so scrolling re-renders nothing that has not changed.

**Animation on the UI thread:**

```tsx
const offset = useSharedValue(0);
const style = useAnimatedStyle(() => ({
  transform: [{ translateY: withSpring(offset.value) }],
}));

// Runs on the UI thread — unaffected by whatever the JS thread is doing.
```

## Notes

- The new architecture (Fabric + TurboModules) removes the asynchronous bridge and is the default from React Native 0.76. Older third-party native modules may not be compatible — check before upgrading.
- `estimatedItemSize` on `FlashList` is not optional in practice; a bad estimate causes visible blank space during fast scrolls.
- Hermes is the default engine and materially improves startup time and memory. If a project is still on JSC, that is usually an oversight.
