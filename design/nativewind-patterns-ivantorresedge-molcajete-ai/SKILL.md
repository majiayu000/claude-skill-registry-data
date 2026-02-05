---
name: nativewind-patterns
description: NativeWind (Tailwind CSS for React Native) styling patterns. Use when styling mobile components.
---

# NativeWind Patterns Skill

This skill covers NativeWind styling for React Native applications.

## When to Use

Use this skill when:
- Styling React Native components
- Converting Tailwind patterns to mobile
- Implementing dark mode
- Responsive mobile design

## Core Principle

**UTILITY FIRST** - Use className with Tailwind utilities adapted for mobile.

## Installation

```bash
npx expo install nativewind
npm install --dev tailwindcss
npx tailwindcss init
```

## Configuration

```javascript
// tailwind.config.js
module.exports = {
  content: [
    "./app/**/*.{js,jsx,ts,tsx}",
    "./components/**/*.{js,jsx,ts,tsx}"
  ],
  presets: [require("nativewind/preset")],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

```javascript
// babel.config.js
module.exports = function(api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: ["nativewind/babel"],
  };
};
```

## Basic Usage

```typescript
import { View, Text } from 'react-native';

export function Card(): React.ReactElement {
  return (
    <View className="bg-white rounded-lg p-4 shadow-md">
      <Text className="text-lg font-bold text-gray-900">
        Card Title
      </Text>
      <Text className="text-sm text-gray-600 mt-2">
        Card description
      </Text>
    </View>
  );
}
```

## Flexbox Layouts

```typescript
// Center content
<View className="flex-1 items-center justify-center">
  <Text>Centered</Text>
</View>

// Space between
<View className="flex-row items-center justify-between">
  <Text>Left</Text>
  <Text>Right</Text>
</View>

// Vertical stack with gap
<View className="flex-col gap-4">
  <Text>Item 1</Text>
  <Text>Item 2</Text>
</View>

// Horizontal stack
<View className="flex-row items-center gap-2">
  <Icon />
  <Text>With Icon</Text>
</View>
```

## Dark Mode

```typescript
<View className="bg-white dark:bg-gray-900">
  <Text className="text-gray-900 dark:text-white">
    Adaptive text
  </Text>
</View>

// Check dark mode status
import { useColorScheme } from 'nativewind';

function Component(): React.ReactElement {
  const { colorScheme, toggleColorScheme } = useColorScheme();

  return (
    <TouchableOpacity onPress={toggleColorScheme}>
      <Text>{colorScheme === 'dark' ? 'Light Mode' : 'Dark Mode'}</Text>
    </TouchableOpacity>
  );
}
```

## Platform-Specific Styles

```typescript
import { Platform } from 'react-native';

<View className={Platform.select({
  ios: 'pt-12',      // iOS status bar
  android: 'pt-6',   // Android status bar
  default: 'pt-8'
})}>
  <Text>Platform-adaptive padding</Text>
</View>
```

## Common Mobile Patterns

### Safe Touch Targets

```typescript
// Minimum 44x44 points for accessibility
<TouchableOpacity className="min-h-[44] min-w-[44] items-center justify-center">
  <Text>Tap Me</Text>
</TouchableOpacity>
```

### Card Component

```typescript
<View className="bg-white rounded-xl p-4 shadow-sm border border-gray-100">
  <Text className="text-lg font-semibold">Title</Text>
  <Text className="text-gray-600 mt-1">Description</Text>
</View>
```

### Button Variants

```typescript
// Primary Button
<TouchableOpacity className="bg-blue-600 py-3 px-6 rounded-lg active:bg-blue-700">
  <Text className="text-white font-semibold text-center">Primary</Text>
</TouchableOpacity>

// Secondary Button
<TouchableOpacity className="bg-gray-100 py-3 px-6 rounded-lg active:bg-gray-200">
  <Text className="text-gray-900 font-semibold text-center">Secondary</Text>
</TouchableOpacity>

// Outline Button
<TouchableOpacity className="border border-blue-600 py-3 px-6 rounded-lg">
  <Text className="text-blue-600 font-semibold text-center">Outline</Text>
</TouchableOpacity>
```

### Input Fields

```typescript
<View className="mb-4">
  <Text className="text-gray-700 mb-1 font-medium">Label</Text>
  <TextInput
    className="bg-gray-50 border border-gray-300 rounded-lg px-4 py-3 text-gray-900"
    placeholder="Enter text..."
    placeholderTextColor="#9CA3AF"
  />
</View>
```

## Spacing Scale

```typescript
// Padding
<View className="p-0">   {/* 0 */}
<View className="p-1">   {/* 4px */}
<View className="p-2">   {/* 8px */}
<View className="p-4">   {/* 16px */}
<View className="p-6">   {/* 24px */}
<View className="p-8">   {/* 32px */}

// Margin
<View className="m-4">   {/* All sides */}
<View className="mx-4">  {/* Horizontal */}
<View className="my-4">  {/* Vertical */}
<View className="mt-4">  {/* Top only */}
```

## Colors

```typescript
// Text colors
<Text className="text-gray-900">   {/* Primary text */}
<Text className="text-gray-600">   {/* Secondary text */}
<Text className="text-gray-400">   {/* Muted text */}
<Text className="text-blue-600">   {/* Link/accent */}
<Text className="text-red-500">    {/* Error */}
<Text className="text-green-500">  {/* Success */}

// Background colors
<View className="bg-white">        {/* Surface */}
<View className="bg-gray-50">      {/* Background */}
<View className="bg-gray-100">     {/* Muted background */}
<View className="bg-blue-600">     {/* Primary */}
```

## Limitations

Not all Tailwind classes work on React Native:
- No `hover:` (use `active:` instead)
- No `grid` (use flexbox)
- No `cursor-pointer`
- No CSS filters
- Limited box-shadow (use `shadow-sm`, `shadow-md`, etc.)

## Notes

- Always test on both iOS and Android
- Use `active:` instead of `hover:` for touch feedback
- Keep styles consistent with platform conventions
- Use NativeWind's useColorScheme for dark mode
