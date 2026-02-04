---
name: platform-specific-code
description: Platform-specific patterns for iOS and Android. Use when writing platform-conditional code.
---

# Platform-Specific Code Skill

This skill covers patterns for handling iOS and Android differences.

## When to Use

Use this skill when:
- Writing platform-specific UI
- Handling platform APIs differently
- Creating platform-specific files
- Styling for each platform

## Core Principle

**WRITE ONCE, ADAPT WHERE NEEDED** - Share code where possible, diverge only when necessary.

## Platform Detection

```typescript
import { Platform } from 'react-native';

// Basic detection
if (Platform.OS === 'ios') {
  // iOS-specific code
} else if (Platform.OS === 'android') {
  // Android-specific code
}

// Platform.select for values
const styles = {
  container: {
    paddingTop: Platform.select({
      ios: 20,
      android: 0,
    }),
  },
};

// With default value
const shadowStyle = Platform.select({
  ios: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
  },
  android: {
    elevation: 5,
  },
  default: {},
});
```

## Platform-Specific Files

```
// File structure
components/
├── Button.tsx          // Shared code
├── Button.ios.tsx      // iOS-specific
├── Button.android.tsx  // Android-specific
```

```typescript
// Button.ios.tsx
import { TouchableOpacity, Text } from 'react-native';

export function Button({ onPress, children }) {
  return (
    <TouchableOpacity
      onPress={onPress}
      style={{ paddingVertical: 12, paddingHorizontal: 24 }}
    >
      <Text>{children}</Text>
    </TouchableOpacity>
  );
}

// Button.android.tsx
import { Pressable, Text } from 'react-native';

export function Button({ onPress, children }) {
  return (
    <Pressable
      onPress={onPress}
      android_ripple={{ color: 'rgba(0,0,0,0.1)' }}
      style={{ paddingVertical: 12, paddingHorizontal: 24 }}
    >
      <Text>{children}</Text>
    </Pressable>
  );
}

// Usage - automatically picks correct file
import { Button } from './Button';
```

## Platform-Specific Styling

```typescript
import { Platform, StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    // Platform-specific values
    ...Platform.select({
      ios: {
        paddingTop: 44, // iOS notch
      },
      android: {
        paddingTop: 24, // Android status bar
      },
    }),
  },
  shadow: Platform.select({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 4,
    },
    android: {
      elevation: 4,
    },
  }),
});
```

## NativeWind Platform Classes

```typescript
// Using NativeWind with platform prefixes
<View className="ios:pt-12 android:pt-6">
  <Text>Platform-specific padding</Text>
</View>

<View className="ios:shadow-lg android:elevation-4">
  <Text>Platform-specific shadows</Text>
</View>
```

## Safe Area Handling

```typescript
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';

// Using SafeAreaView
function Screen() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <Content />
    </SafeAreaView>
  );
}

// Using hook for fine control
function Header() {
  const insets = useSafeAreaInsets();

  return (
    <View style={{ paddingTop: insets.top }}>
      <Text>Header</Text>
    </View>
  );
}

// Platform-specific safe area
function PlatformHeader() {
  const insets = useSafeAreaInsets();

  return (
    <View
      style={{
        paddingTop: Platform.select({
          ios: insets.top,
          android: insets.top + 8, // Extra padding on Android
        }),
      }}
    >
      <Text>Header</Text>
    </View>
  );
}
```

## Status Bar

```typescript
import { StatusBar, Platform } from 'react-native';

function App() {
  return (
    <>
      <StatusBar
        barStyle={Platform.select({
          ios: 'dark-content',
          android: 'light-content',
        })}
        backgroundColor={Platform.OS === 'android' ? '#ffffff' : undefined}
        translucent={Platform.OS === 'android'}
      />
      <Content />
    </>
  );
}
```

## Platform-Specific Navigation

```typescript
import { Platform } from 'react-native';
import { Stack } from 'expo-router';

function StackLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: {
          backgroundColor: '#fff',
        },
        // iOS-specific
        ...(Platform.OS === 'ios' && {
          headerLargeTitle: true,
          headerTransparent: true,
          headerBlurEffect: 'regular',
        }),
        // Android-specific
        ...(Platform.OS === 'android' && {
          animation: 'slide_from_right',
        }),
      }}
    >
      <Stack.Screen name="index" />
    </Stack>
  );
}
```

## Platform-Specific Haptics

```typescript
import * as Haptics from 'expo-haptics';
import { Platform, Vibration } from 'react-native';

async function triggerFeedback() {
  if (Platform.OS === 'ios') {
    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
  } else {
    Vibration.vibrate(50);
  }
}

// Selection feedback
async function selectionFeedback() {
  if (Platform.OS === 'ios') {
    await Haptics.selectionAsync();
  }
  // Android handles selection feedback automatically
}
```

## Platform-Specific Keyboards

```typescript
import { Platform, KeyboardAvoidingView } from 'react-native';

function FormScreen() {
  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      keyboardVerticalOffset={Platform.select({
        ios: 88, // Header height
        android: 0,
      })}
      style={{ flex: 1 }}
    >
      <Form />
    </KeyboardAvoidingView>
  );
}
```

## Platform-Specific Permissions

```typescript
import * as ImagePicker from 'expo-image-picker';
import { Platform } from 'react-native';

async function requestCameraPermission() {
  if (Platform.OS === 'ios') {
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    return status === 'granted';
  } else {
    // Android handles permissions differently
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    return status === 'granted';
  }
}
```

## Platform-Specific Links

```typescript
import { Linking, Platform } from 'react-native';

function openSettings() {
  if (Platform.OS === 'ios') {
    Linking.openURL('app-settings:');
  } else {
    Linking.openSettings();
  }
}

function openMaps(latitude: number, longitude: number) {
  const url = Platform.select({
    ios: `maps:0,0?q=${latitude},${longitude}`,
    android: `geo:0,0?q=${latitude},${longitude}`,
  });

  if (url) {
    Linking.openURL(url);
  }
}

function openPhone(phoneNumber: string) {
  const url = Platform.select({
    ios: `telprompt:${phoneNumber}`,
    android: `tel:${phoneNumber}`,
  });

  if (url) {
    Linking.openURL(url);
  }
}
```

## Platform-Specific Components

```typescript
import { Platform, Pressable, TouchableOpacity } from 'react-native';

// Use Pressable with ripple on Android
function PlatformButton({ onPress, children, style }) {
  if (Platform.OS === 'android') {
    return (
      <Pressable
        onPress={onPress}
        android_ripple={{ color: 'rgba(0,0,0,0.1)' }}
        style={style}
      >
        {children}
      </Pressable>
    );
  }

  return (
    <TouchableOpacity onPress={onPress} style={style}>
      {children}
    </TouchableOpacity>
  );
}
```

## Platform-Specific Fonts

```typescript
import { Platform } from 'react-native';

const fontFamily = Platform.select({
  ios: 'System',
  android: 'Roboto',
});

// With custom fonts
const customFont = Platform.select({
  ios: 'SF Pro Display',
  android: 'sans-serif-medium',
});
```

## Version Checking

```typescript
import { Platform } from 'react-native';

// Check platform version
const isIOS15OrLater = Platform.OS === 'ios' && parseInt(Platform.Version, 10) >= 15;
const isAndroid12OrLater = Platform.OS === 'android' && Platform.Version >= 31;

// Conditional features
if (isIOS15OrLater) {
  // Use iOS 15+ features
}
```

## Platform Constants

```typescript
import { Platform } from 'react-native';

// iOS specific
if (Platform.OS === 'ios') {
  console.log('iOS Version:', Platform.Version); // e.g., "17.0"
  console.log('Is iPad:', Platform.isPad);
  console.log('Is TV:', Platform.isTV);
}

// Android specific
if (Platform.OS === 'android') {
  console.log('API Level:', Platform.Version); // e.g., 34
}
```

## Testing Platform Code

```typescript
import { Platform } from 'react-native';

// Mock Platform in tests
jest.mock('react-native/Libraries/Utilities/Platform', () => ({
  OS: 'ios',
  select: jest.fn((obj) => obj.ios),
}));

// Or for Android
jest.mock('react-native/Libraries/Utilities/Platform', () => ({
  OS: 'android',
  select: jest.fn((obj) => obj.android),
  Version: 31,
}));
```

## Notes

- Use platform-specific files for large differences
- Use Platform.select for simple value differences
- Test on both platforms regularly
- Consider using design system that handles differences
- Document platform-specific behavior
- Use Expo's cross-platform APIs when available
