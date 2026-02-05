---
name: expo-router-patterns
description: Expo Router file-based navigation patterns. Use when implementing navigation.
---

# Expo Router Patterns Skill

This skill covers Expo Router navigation for React Native.

## When to Use

Use this skill when:
- Setting up navigation
- Creating screens and routes
- Implementing deep linking
- Protecting routes

## Core Principle

**FILE-BASED ROUTING** - Routes are defined by file structure (like Next.js).

## File Structure

```
app/
├── (auth)/             # Route group (not in URL)
│   ├── login.tsx      # /login
│   ├── register.tsx   # /register
│   └── _layout.tsx    # Layout for auth routes
├── (tabs)/            # Tab navigation group
│   ├── _layout.tsx    # Tabs layout
│   ├── index.tsx      # /
│   └── profile.tsx    # /profile
├── settings/
│   ├── index.tsx      # /settings
│   └── [id].tsx       # /settings/123 (dynamic)
├── _layout.tsx        # Root layout
├── +not-found.tsx     # 404 page
└── [...missing].tsx   # Catch-all route
```

## Basic Navigation

### Link Component

```typescript
import { Link } from 'expo-router';

<Link href="/profile">Go to Profile</Link>

// With params
<Link
  href={{
    pathname: '/user/[id]',
    params: { id: '123' },
  }}
>
  View User
</Link>

// As child (for custom styling)
<Link href="/settings" asChild>
  <TouchableOpacity>
    <Text>Settings</Text>
  </TouchableOpacity>
</Link>
```

### useRouter Hook

```typescript
import { useRouter } from 'expo-router';

function Component(): React.ReactElement {
  const router = useRouter();

  const handleNavigate = () => {
    // Push new screen
    router.push('/profile');

    // Replace current screen
    router.replace('/login');

    // Go back
    router.back();

    // Navigate with params
    router.push({
      pathname: '/user/[id]',
      params: { id: '123' },
    });
  };

  return <Button onPress={handleNavigate}>Navigate</Button>;
}
```

## Layout Components

### Root Layout

```typescript
// app/_layout.tsx
import { Stack } from 'expo-router';
import { StatusBar } from 'expo-status-bar';

export default function RootLayout(): React.ReactElement {
  return (
    <>
      <StatusBar style="auto" />
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="(auth)" options={{ headerShown: false }} />
        <Stack.Screen
          name="modal"
          options={{
            presentation: 'modal',
            headerTitle: 'Modal',
          }}
        />
      </Stack>
    </>
  );
}
```

### Tab Layout

```typescript
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout(): React.ReactElement {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#3B82F6',
        tabBarInactiveTintColor: '#6B7280',
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="search"
        options={{
          title: 'Search',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="search" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
```

## Dynamic Routes

### Single Parameter

```typescript
// app/user/[id].tsx
import { useLocalSearchParams } from 'expo-router';
import { View, Text } from 'react-native';

export default function UserPage(): React.ReactElement {
  const { id } = useLocalSearchParams<{ id: string }>();

  return (
    <View className="flex-1 items-center justify-center">
      <Text className="text-lg">User ID: {id}</Text>
    </View>
  );
}
```

### Multiple Parameters

```typescript
// app/[category]/[id].tsx
import { useLocalSearchParams } from 'expo-router';

export default function ProductPage(): React.ReactElement {
  const { category, id } = useLocalSearchParams<{
    category: string;
    id: string;
  }>();

  return (
    <View>
      <Text>Category: {category}</Text>
      <Text>Product ID: {id}</Text>
    </View>
  );
}
```

### Catch-All Route

```typescript
// app/[...path].tsx
import { useLocalSearchParams } from 'expo-router';

export default function CatchAllPage(): React.ReactElement {
  const { path } = useLocalSearchParams<{ path: string[] }>();

  return (
    <View>
      <Text>Path segments: {path?.join('/')}</Text>
    </View>
  );
}
```

## Protected Routes

```typescript
// app/_layout.tsx
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '@/hooks/useAuth';
import { Loading } from '@/components/Loading';

export default function RootLayout(): React.ReactElement {
  const { user, isLoading } = useAuth();

  if (isLoading) {
    return <Loading />;
  }

  if (!user) {
    return <Redirect href="/login" />;
  }

  return <Stack />;
}
```

## Route Groups

```
app/
├── (auth)/           # Auth group (no /auth in URL)
│   ├── login.tsx    # /login
│   └── register.tsx # /register
├── (app)/           # App group (no /app in URL)
│   ├── home.tsx     # /home
│   └── profile.tsx  # /profile
```

## Modal Routes

```typescript
// app/_layout.tsx
<Stack>
  <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
  <Stack.Screen
    name="modal"
    options={{
      presentation: 'modal',
      animation: 'slide_from_bottom',
    }}
  />
</Stack>

// Navigate to modal
router.push('/modal');

// Close modal
router.back();
```

## Deep Linking

### Configuration

```json
// app.json
{
  "expo": {
    "scheme": "myapp",
    "web": {
      "bundler": "metro"
    }
  }
}
```

### Links

```
myapp://                    # Opens app
myapp://profile             # Opens /profile
myapp://user/123            # Opens /user/123
https://myapp.com/profile   # Universal link
```

## Navigation Hooks

### usePathname

```typescript
import { usePathname } from 'expo-router';

function Component(): React.ReactElement {
  const pathname = usePathname();
  // Returns: "/user/123"

  return <Text>Current path: {pathname}</Text>;
}
```

### useSegments

```typescript
import { useSegments } from 'expo-router';

function Component(): React.ReactElement {
  const segments = useSegments();
  // Returns: ["user", "123"]

  return <Text>Segments: {segments.join(', ')}</Text>;
}
```

### useFocusEffect

```typescript
import { useFocusEffect } from 'expo-router';
import { useCallback } from 'react';

function Screen(): React.ReactElement {
  useFocusEffect(
    useCallback(() => {
      // Runs when screen is focused
      console.log('Screen focused');

      return () => {
        // Cleanup when screen loses focus
        console.log('Screen unfocused');
      };
    }, [])
  );

  return <View />;
}
```

## Notes

- Use route groups `(name)` to organize without affecting URLs
- Layouts cascade (parent layouts wrap children)
- `_layout.tsx` defines the navigation structure
- `+not-found.tsx` handles 404 routes
- Deep linking is configured automatically
- Use typed params with generics for type safety
