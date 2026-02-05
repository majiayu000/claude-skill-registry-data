---
name: react-native-builder
description: Expert in React Native development, native modules, platform-specific code, navigation, AsyncStorage, styling, animations, and app deployment to iOS/Android stores
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# React Native Builder

Expert skill for building cross-platform mobile applications with React Native. Specializes in native modules, platform-specific code, navigation, styling, and app store deployment.

## Core Capabilities

### 1. React Native Setup
- **Expo**: Managed workflow
- **React Native CLI**: Bare workflow
- **TypeScript**: Type-safe RN
- **Platform-Specific Code**: iOS vs Android
- **Native Modules**: Bridge to native code
- **Metro Bundler**: JS bundling

### 2. UI Components
- **Core Components**: View, Text, Image
- **Lists**: FlatList, SectionList
- **Inputs**: TextInput, Switch
- **Touchables**: TouchableOpacity, Pressable
- **ScrollView**: Scrollable content
- **SafeAreaView**: Notch handling

### 3. Navigation
- **React Navigation**: Stack, Tab, Drawer
- **Deep Linking**: URL schemes
- **State Persistence**: Restore navigation
- **Gestures**: Swipe, pan navigation
- **Transitions**: Custom animations

### 4. Styling
- **StyleSheet**: RN styling API
- **Flexbox**: Layout system
- **Dimensions**: Screen sizes
- **Platform**: Platform-specific styles
- **Styled Components**: CSS-in-JS
- **Responsive**: Adapt to screen sizes

### 5. Data & State
- **AsyncStorage**: Local persistence
- **MMKV**: Fast key-value storage
- **SQLite**: Local database
- **React Query**: API integration
- **Zustand**: Global state
- **Context**: Component state

### 6. Native Features
- **Camera**: expo-camera, react-native-camera
- **Location**: Geolocation
- **Push Notifications**: FCM, APNs
- **Biometrics**: Touch ID, Face ID
- **File System**: Read/write files
- **Permissions**: Request access

### 7. Deployment
- **iOS**: App Store Connect
- **Android**: Google Play Console
- **Code Push**: OTA updates
- **TestFlight**: iOS beta testing
- **Internal Testing**: Android beta

## Basic App Structure

```tsx
// App.tsx
import { StatusBar } from 'expo-status-bar'
import { StyleSheet, Text, View } from 'react-native'

export default function App() {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Hello React Native!</Text>
      <StatusBar style="auto" />
    </View>
  )
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontSize: 20,
    fontWeight: 'bold',
  },
})
```

## Navigation

```tsx
// Navigation.tsx
import { NavigationContainer } from '@react-navigation/native'
import { createNativeStackNavigator } from '@react-navigation/native-stack'

const Stack = createNativeStackNavigator()

export function AppNavigation() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  )
}

// HomeScreen.tsx
function HomeScreen({ navigation }: { navigation: any }) {
  return (
    <View>
      <Button
        title="Go to Details"
        onPress={() => navigation.navigate('Details')}
      />
    </View>
  )
}
```

## Platform-Specific Code

```tsx
import { Platform, StyleSheet } from 'react-native'

const styles = StyleSheet.create({
  container: {
    padding: Platform.OS === 'ios' ? 20 : 10,
    ...Platform.select({
      ios: {
        backgroundColor: 'white',
      },
      android: {
        backgroundColor: 'blue',
      },
    }),
  },
})

// Separate files
import Component from './Component'
// Component.ios.tsx
// Component.android.tsx
```

## AsyncStorage

```typescript
import AsyncStorage from '@react-native-async-storage/async-storage'

// Save data
await AsyncStorage.setItem('user', JSON.stringify(userData))

// Load data
const user = await AsyncStorage.getItem('user')
const userData = user ? JSON.parse(user) : null

// Remove data
await AsyncStorage.removeItem('user')
```

## Lists

```tsx
import { FlatList } from 'react-native'

function ItemList({ items }: { items: Item[] }) {
  return (
    <FlatList
      data={items}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <Item {...item} />}
      ListEmptyComponent={<Text>No items</Text>}
      refreshing={isRefreshing}
      onRefresh={handleRefresh}
      onEndReached={loadMore}
      onEndReachedThreshold={0.5}
    />
  )
}
```

## Animations

```tsx
import { Animated } from 'react-native'
import { useRef, useEffect } from 'react'

function FadeIn({ children }: { children: React.ReactNode }) {
  const opacity = useRef(new Animated.Value(0)).current

  useEffect(() => {
    Animated.timing(opacity, {
      toValue: 1,
      duration: 1000,
      useNativeDriver: true,
    }).start()
  }, [])

  return (
    <Animated.View style={{ opacity }}>
      {children}
    </Animated.View>
  )
}
```

## Responsive Design

```tsx
import { Dimensions, useWindowDimensions } from 'react-native'

// Static dimensions
const { width, height } = Dimensions.get('window')

// Dynamic dimensions (updates on rotation)
function ResponsiveComponent() {
  const { width, height } = useWindowDimensions()

  return (
    <View style={{ width: width * 0.8 }}>
      <Text>Responsive width</Text>
    </View>
  )
}
```

## Best Practices

- Use FlatList for large lists
- Optimize images (use FastImage)
- Enable Hermes engine
- Use useNativeDriver for animations
- Handle keyboard properly
- Test on real devices
- Implement error boundaries
- Use TypeScript
- Follow platform guidelines

## Deployment

### iOS (App Store)
1. Configure app.json
2. Generate provisioning profiles
3. Build with EAS Build or Xcode
4. Upload to App Store Connect
5. Submit for review

### Android (Play Store)
1. Generate signing key
2. Configure app.json
3. Build release APK/AAB
4. Upload to Play Console
5. Submit for review

## When to Use This Skill

Use when you need to:
- Build mobile apps with React Native
- Create platform-specific features
- Implement navigation
- Style RN components
- Integrate native modules
- Deploy to app stores
- Optimize RN performance

## Output Format

Provide:
1. **RN Component**: Cross-platform code
2. **Navigation**: Stack/Tab/Drawer setup
3. **Styling**: StyleSheet configuration
4. **Platform Code**: iOS/Android specific
5. **Deployment Guide**: App store submission
6. **Testing**: Testing strategy
