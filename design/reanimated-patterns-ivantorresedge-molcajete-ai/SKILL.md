---
name: reanimated-patterns
description: React Native Reanimated animation patterns. Use when implementing animations.
---

# Reanimated Patterns Skill

This skill covers React Native Reanimated for performant animations.

## When to Use

Use this skill when:
- Implementing smooth animations
- Gesture-based interactions
- Complex animation sequences
- Performance-critical animations

## Core Principle

**UI THREAD ANIMATIONS** - Reanimated runs animations on the UI thread for 60fps.

## Installation

```bash
npx expo install react-native-reanimated
```

Update babel.config.js:
```javascript
module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: ['react-native-reanimated/plugin'],
  };
};
```

## Basic Concepts

### Shared Values

```typescript
import { useSharedValue } from 'react-native-reanimated';

// Shared values are synchronized between JS and UI threads
const scale = useSharedValue(1);
const opacity = useSharedValue(0);
const translateX = useSharedValue(0);

// Update shared values
scale.value = 2;
opacity.value = 1;
```

### Animated Styles

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
} from 'react-native-reanimated';

function AnimatedBox(): React.ReactElement {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <Animated.View style={[styles.box, animatedStyle]} />
  );
}
```

## Animation Functions

### withSpring

```typescript
import { withSpring } from 'react-native-reanimated';

// Spring animation (natural bounce)
scale.value = withSpring(2, {
  damping: 10,
  stiffness: 100,
  mass: 1,
});
```

### withTiming

```typescript
import { withTiming, Easing } from 'react-native-reanimated';

// Timed animation
opacity.value = withTiming(1, {
  duration: 300,
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),
});
```

### withDelay

```typescript
import { withDelay, withSpring } from 'react-native-reanimated';

// Delayed animation
scale.value = withDelay(500, withSpring(2));
```

### withSequence

```typescript
import { withSequence, withTiming } from 'react-native-reanimated';

// Sequential animations
scale.value = withSequence(
  withTiming(1.2, { duration: 100 }),
  withTiming(0.9, { duration: 100 }),
  withTiming(1, { duration: 100 })
);
```

### withRepeat

```typescript
import { withRepeat, withTiming } from 'react-native-reanimated';

// Repeating animation
rotation.value = withRepeat(
  withTiming(360, { duration: 1000 }),
  -1,  // -1 for infinite
  false // reverse
);
```

## Common Animations

### Fade In/Out

```typescript
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
} from 'react-native-reanimated';

function FadeView({ visible }: { visible: boolean }): React.ReactElement {
  const opacity = useSharedValue(0);

  useEffect(() => {
    opacity.value = withTiming(visible ? 1 : 0, { duration: 300 });
  }, [visible]);

  const animatedStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
  }));

  return (
    <Animated.View style={animatedStyle}>
      {children}
    </Animated.View>
  );
}
```

### Scale on Press

```typescript
function ScaleButton({ onPress, children }: Props): React.ReactElement {
  const scale = useSharedValue(1);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  const handlePressIn = () => {
    scale.value = withSpring(0.95);
  };

  const handlePressOut = () => {
    scale.value = withSpring(1);
  };

  return (
    <TouchableOpacity
      onPressIn={handlePressIn}
      onPressOut={handlePressOut}
      onPress={onPress}
      activeOpacity={1}
    >
      <Animated.View style={animatedStyle}>
        {children}
      </Animated.View>
    </TouchableOpacity>
  );
}
```

### Slide In

```typescript
import { Dimensions } from 'react-native';

const { width } = Dimensions.get('window');

function SlideIn({ visible }: { visible: boolean }): React.ReactElement {
  const translateX = useSharedValue(width);

  useEffect(() => {
    translateX.value = withSpring(visible ? 0 : width);
  }, [visible]);

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ translateX: translateX.value }],
  }));

  return (
    <Animated.View style={[styles.panel, animatedStyle]}>
      {children}
    </Animated.View>
  );
}
```

## Entering/Exiting Animations

```typescript
import Animated, {
  FadeIn,
  FadeOut,
  SlideInRight,
  SlideOutLeft,
  ZoomIn,
  BounceIn,
} from 'react-native-reanimated';

// Fade
<Animated.View entering={FadeIn.duration(300)} exiting={FadeOut.duration(200)}>

// Slide
<Animated.View entering={SlideInRight} exiting={SlideOutLeft}>

// Zoom
<Animated.View entering={ZoomIn.springify()}>

// Bounce
<Animated.View entering={BounceIn.delay(200)}>

// Custom
<Animated.View
  entering={FadeIn.duration(500).delay(100).springify()}
  exiting={FadeOut.duration(300)}
>
```

## Layout Animations

```typescript
import Animated, { Layout } from 'react-native-reanimated';

// Animate layout changes
<Animated.View layout={Layout.springify()}>
  {items.map((item) => (
    <Animated.View
      key={item.id}
      entering={FadeIn}
      exiting={FadeOut}
      layout={Layout}
    >
      <Text>{item.name}</Text>
    </Animated.View>
  ))}
</Animated.View>
```

## Gesture Handler Integration

```typescript
import { GestureDetector, Gesture } from 'react-native-gesture-handler';
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withSpring,
} from 'react-native-reanimated';

function DraggableBox(): React.ReactElement {
  const translateX = useSharedValue(0);
  const translateY = useSharedValue(0);

  const gesture = Gesture.Pan()
    .onUpdate((event) => {
      translateX.value = event.translationX;
      translateY.value = event.translationY;
    })
    .onEnd(() => {
      translateX.value = withSpring(0);
      translateY.value = withSpring(0);
    });

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [
      { translateX: translateX.value },
      { translateY: translateY.value },
    ],
  }));

  return (
    <GestureDetector gesture={gesture}>
      <Animated.View style={[styles.box, animatedStyle]} />
    </GestureDetector>
  );
}
```

## Interpolation

```typescript
import { interpolate, Extrapolation } from 'react-native-reanimated';

const animatedStyle = useAnimatedStyle(() => {
  const scale = interpolate(
    scrollY.value,
    [0, 100],
    [1, 0.5],
    Extrapolation.CLAMP
  );

  const opacity = interpolate(
    scrollY.value,
    [0, 50, 100],
    [1, 0.5, 0]
  );

  return {
    transform: [{ scale }],
    opacity,
  };
});
```

## Worklets

```typescript
import { runOnJS } from 'react-native-reanimated';

// Call JS function from worklet
const updateState = (value: number) => {
  setState(value);
};

const animatedStyle = useAnimatedStyle(() => {
  if (position.value > 100) {
    runOnJS(updateState)(position.value);
  }
  return { transform: [{ translateX: position.value }] };
});
```

## Notes

- All animation logic runs on UI thread
- Use worklets ('worklet' directive) for custom functions
- Use runOnJS to call JS functions from worklets
- Test animations on real devices
- Reanimated is compatible with Expo
