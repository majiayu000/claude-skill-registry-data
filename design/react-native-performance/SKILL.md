---
name: react-native-performance
description: React Native performance optimization techniques. Use when optimizing app performance.
---

# React Native Performance Skill

This skill covers performance optimization for React Native apps.

## When to Use

Use this skill when:
- App feels slow or janky
- Lists scroll poorly
- Animations stutter
- Bundle size is too large
- Memory usage is high

## Core Principle

**MEASURE FIRST** - Profile before optimizing. Fix actual bottlenecks, not perceived ones.

## Profiling Tools

### React DevTools Profiler

```typescript
// Enable profiling in development
if (__DEV__) {
  // React DevTools will show component render times
}
```

### Flipper

```bash
# Install Flipper for advanced debugging
# https://fbflipper.com/
```

### Performance Monitor

```typescript
// Show FPS and memory in development
import { LogBox } from 'react-native';

if (__DEV__) {
  // Performance overlay available via shake gesture
}
```

## Render Optimization

### Avoid Inline Functions

```typescript
// ❌ Bad: Creates new function every render
<Button onPress={() => handlePress(item.id)} />

// ✅ Good: Stable function reference
const handlePress = useCallback((id: string) => {
  console.log(id);
}, []);

<Button onPress={() => handlePress(item.id)} />

// ✅ Better: If possible, pass id differently
const handleItemPress = useCallback(() => {
  console.log(item.id);
}, [item.id]);

<Button onPress={handleItemPress} />
```

### Memoize Components

```typescript
import { memo } from 'react';

interface ItemCardProps {
  item: Item;
  onPress: (id: string) => void;
}

export const ItemCard = memo(function ItemCard({
  item,
  onPress,
}: ItemCardProps): React.ReactElement {
  return (
    <TouchableOpacity onPress={() => onPress(item.id)}>
      <Text>{item.name}</Text>
    </TouchableOpacity>
  );
});
```

### useMemo for Expensive Computations

```typescript
import { useMemo } from 'react';

function FilteredList({ items, filter }: Props): React.ReactElement {
  // Only recompute when items or filter change
  const filteredItems = useMemo(() => {
    return items.filter((item) =>
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [items, filter]);

  return <FlashList data={filteredItems} {...rest} />;
}
```

### useCallback for Event Handlers

```typescript
import { useCallback } from 'react';

function ItemList(): React.ReactElement {
  const handlePress = useCallback((id: string) => {
    // Handle press
  }, []);

  const renderItem = useCallback(({ item }: { item: Item }) => (
    <ItemCard item={item} onPress={handlePress} />
  ), [handlePress]);

  return (
    <FlashList
      data={items}
      renderItem={renderItem}
      estimatedItemSize={80}
    />
  );
}
```

## List Performance

### Use FlashList Instead of FlatList

```typescript
import { FlashList } from '@shopify/flash-list';

// ✅ FlashList is 10x faster than FlatList
<FlashList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  estimatedItemSize={80}  // Required for FlashList
  keyExtractor={(item) => item.id}
/>
```

### Optimize Item Rendering

```typescript
// ✅ Use getItemType for different item layouts
<FlashList
  data={items}
  renderItem={({ item }) => {
    if (item.type === 'header') return <Header />;
    return <Item item={item} />;
  }}
  getItemType={(item) => item.type}
  estimatedItemSize={60}
/>

// ✅ Use overrideItemLayout for variable heights
<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={60}
  overrideItemLayout={(layout, item) => {
    layout.size = item.type === 'header' ? 100 : 60;
  }}
/>
```

## Image Optimization

### Use expo-image

```typescript
import { Image } from 'expo-image';

// ✅ expo-image is faster than React Native Image
<Image
  source={{ uri: imageUrl }}
  style={{ width: 200, height: 200 }}
  contentFit="cover"
  transition={200}
  cachePolicy="memory-disk"
/>
```

### Optimize Image Size

```typescript
// ✅ Request appropriately sized images
const imageUrl = `${baseUrl}?w=400&h=400`;

// ✅ Use blurhash for placeholders
<Image
  source={{ uri: imageUrl }}
  placeholder={blurhash}
  transition={200}
/>
```

## Animation Optimization

### Use Reanimated

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

// ✅ Animations run on UI thread
function AnimatedBox(): React.ReactElement {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return <Animated.View style={animatedStyle} />;
}
```

### Avoid JS-Driven Animations

```typescript
// ❌ Bad: JS thread animations
const [scale, setScale] = useState(1);
Animated.timing(scale, { toValue: 2 }).start();

// ✅ Good: Reanimated (runs on UI thread)
const scale = useSharedValue(1);
scale.value = withSpring(2);
```

## Bundle Size Optimization

### Analyze Bundle

```bash
npx react-native-bundle-visualizer
```

### Optimize Imports

```typescript
// ❌ Bad: Imports entire library
import { format } from 'date-fns';

// ✅ Good: Import only what you need
import format from 'date-fns/format';

// ❌ Bad: Import all icons
import * as Icons from 'lucide-react-native';

// ✅ Good: Import specific icons
import { Home, Search } from 'lucide-react-native';
```

### Replace Heavy Libraries

```typescript
// Replace moment.js (300KB) with:
// - date-fns (tree-shakeable)
// - dayjs (2KB)

// Replace lodash with:
// - Individual lodash functions
// - Native JavaScript methods
```

## Memory Management

### Clean Up Effects

```typescript
useEffect(() => {
  const subscription = eventEmitter.subscribe(handler);

  // ✅ Always clean up subscriptions
  return () => {
    subscription.unsubscribe();
  };
}, []);
```

### Avoid Memory Leaks

```typescript
// ✅ Cancel async operations
useEffect(() => {
  let isMounted = true;

  fetchData().then((data) => {
    if (isMounted) {
      setData(data);
    }
  });

  return () => {
    isMounted = false;
  };
}, []);
```

## Common Pitfalls

### Avoid

```typescript
// ❌ Inline styles (creates new object every render)
<View style={{ padding: 10 }} />

// ❌ Anonymous functions in render
<Button onPress={() => handlePress()} />

// ❌ FlatList for long lists
<FlatList data={longList} />

// ❌ Unoptimized images
<Image source={{ uri: fullSizeImage }} />
```

### Prefer

```typescript
// ✅ NativeWind or StyleSheet
<View className="p-4" />

// ✅ useCallback for handlers
const handlePress = useCallback(() => {...}, []);

// ✅ FlashList for long lists
<FlashList data={longList} estimatedItemSize={80} />

// ✅ Optimized images with expo-image
<Image source={{ uri: optimizedImage }} cachePolicy="memory-disk" />
```

## Performance Checklist

- [ ] Use FlashList instead of FlatList
- [ ] Memoize expensive computations
- [ ] Use useCallback for event handlers
- [ ] Use React.memo for list items
- [ ] Use Reanimated for animations
- [ ] Use expo-image for images
- [ ] Analyze and optimize bundle size
- [ ] Clean up effects and subscriptions
- [ ] Profile before optimizing

## Notes

- Profile on actual devices, not simulators
- Focus on 60fps for smooth experience
- Monitor memory usage
- Test on lower-end devices
- Use New Architecture for better performance
