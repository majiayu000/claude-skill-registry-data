---
name: react-native-mobile
category: frontend
difficulty: intermediate
tags:
- react-native
- mobile
- ios
- android
- cross-platform
last_updated: 2025-10-17
applies_to:
- mobile-apps
- hybrid-apps
description: React Native mobile development covering iOS and Android cross-platform apps, navigation, state management, native modules, and performance optimization for production-ready mobile applications
---


# React Native Mobile Development

> **Level 1**: Quick Reference (~700-900 tokens)
> **Level 2**: Implementation Guide (~4000-5000 tokens)
> **Level 3**: Deep Dive Resources (external links)

---

## Level 1: Quick Reference

### Core Components

```typescript
import { View, Text, ScrollView, FlatList, Image, TouchableOpacity } from 'react-native';

// Basic Layout
<View style={styles.container}>
  <Text style={styles.title}>Hello World</Text>
  <Image source={require('./logo.png')} style={styles.image} />
  <TouchableOpacity onPress={handlePress}>
    <Text>Press Me</Text>
  </TouchableOpacity>
</View>

// List Rendering (Performance Optimized)
<FlatList
  data={items}
  renderItem={({ item }) => <ItemCard item={item} />}
  keyExtractor={item => item.id}
  onEndReached={loadMore}
  onEndReachedThreshold={0.5}
/>

// Scrollable Content
<ScrollView contentContainerStyle={styles.scrollContent}>
  {/* Long content */}
</ScrollView>
```

### Navigation (React Navigation v6)

```typescript
// Stack Navigator
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Details" component={DetailsScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}

// Navigate Between Screens
navigation.navigate('Details', { itemId: 42 });
navigation.goBack();
```

### Styling

```typescript
import { StyleSheet } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  text: {
    fontSize: 16,
    color: '#333',
    fontWeight: 'bold',
  },
});
```

### Platform-Specific Code

```typescript
import { Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    marginTop: Platform.OS === 'ios' ? 20 : 0,
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 } },
      android: { elevation: 4 },
    }),
  },
});

// Platform-specific files
// Button.ios.tsx
// Button.android.tsx
```

### Essential Checklist

- [ ] Use `FlatList` for long lists (virtualized rendering)
- [ ] Implement `React.memo()` for expensive components
- [ ] Handle safe area insets (notches, status bars)
- [ ] Test on both iOS and Android devices
- [ ] Optimize images (use proper dimensions, formats)
- [ ] Handle keyboard avoiding behavior
- [ ] Implement proper navigation typing
- [ ] Use `useCallback` and `useMemo` appropriately
- [ ] Handle network errors and offline states
- [ ] Add accessibility labels for screen readers

---

## Level 2:
>
> **📚 Full Examples**: See [REFERENCE.md](./REFERENCE.md) for complete code samples, detailed configurations, and production-ready implementations.

 Implementation Guide

### 1. Core Components and APIs

#### Layout Components


*See [REFERENCE.md](./REFERENCE.md#example-0) for complete implementation.*


#### Interactive Components


*See [REFERENCE.md](./REFERENCE.md#example-1) for complete implementation.*


#### Input Components


*See [REFERENCE.md](./REFERENCE.md#example-2) for complete implementation.*


#### List Components


*See [REFERENCE.md](./REFERENCE.md#example-3) for complete implementation.*


### 2. Navigation Architecture

#### React Navigation v6 Setup


*See [REFERENCE.md](./REFERENCE.md#example-4) for complete implementation.*


#### Tab Navigation


*See [REFERENCE.md](./REFERENCE.md#example-5) for complete implementation.*


#### Drawer Navigation


*See [REFERENCE.md](./REFERENCE.md#example-6) for complete implementation.*


### 3. State Management

#### Redux Toolkit


*See [REFERENCE.md](./REFERENCE.md#example-7) for complete implementation.*


#### Zustand (Lightweight Alternative)


*See [REFERENCE.md](./REFERENCE.md#example-8) for complete implementation.*


#### React Query (Server State)


*See [REFERENCE.md](./REFERENCE.md#example-9) for complete implementation.*


### 4. Styling and Theming

#### StyleSheet API


*See [REFERENCE.md](./REFERENCE.md#example-10) for complete implementation.*


#### Styled Components


*See [REFERENCE.md](./REFERENCE.md#example-11) for complete implementation.*


#### Responsive Design


*See [REFERENCE.md](./REFERENCE.md#example-12) for complete implementation.*


### 5. Platform-Specific Code

#### Platform API


*See [REFERENCE.md](./REFERENCE.md#example-13) for complete implementation.*


#### File Extensions


*See [REFERENCE.md](./REFERENCE.md#example-14) for complete implementation.*


#### Conditional Rendering


*See [REFERENCE.md](./REFERENCE.md#example-15) for complete implementation.*


### 6. Native Modules and Bridges

#### Using Native Modules


*See [REFERENCE.md](./REFERENCE.md#example-16) for complete implementation.*


#### Linking to Native APIs


*See [REFERENCE.md](./REFERENCE.md#example-17) for complete implementation.*


### 7. Performance Optimization

#### Component Optimization


*See [REFERENCE.md](./REFERENCE.md#example-18) for complete implementation.*


#### FlatList Optimization


*See [REFERENCE.md](./REFERENCE.md#example-19) for complete implementation.*


#### InteractionManager


*See [REFERENCE.md](./REFERENCE.md#example-20) for complete implementation.*


#### Image Optimization


*See [REFERENCE.md](./REFERENCE.md#example-21) for complete implementation.*


### 8. Testing

#### Jest Unit Tests


*See [REFERENCE.md](./REFERENCE.md#example-22) for complete implementation.*


#### React Native Testing Library


*See [REFERENCE.md](./REFERENCE.md#example-23) for complete implementation.*


#### E2E Testing (Detox)


*See [REFERENCE.md](./REFERENCE.md#example-24) for complete implementation.*


### 9. Accessibility

#### Screen Reader Support


*See [REFERENCE.md](./REFERENCE.md#example-25) for complete implementation.*


#### Semantic Labels


*See [REFERENCE.md](./REFERENCE.md#example-26) for complete implementation.*


### 10. Deployment

#### iOS App Store


*See [REFERENCE.md](./REFERENCE.md#example-27) for complete implementation.*


#### Android Play Store


*See [REFERENCE.md](./REFERENCE.md#example-28) for complete implementation.*


#### Over-the-Air (OTA) Updates


*See [REFERENCE.md](./REFERENCE.md#example-29) for complete implementation.*


---

## Level 3: Deep Dive Resources

### Official Documentation

- [React Native Docs](https://reactnative.dev/docs/getting-started)
- [React Navigation](https://reactnavigation.org/docs/getting-started)
- [Expo Documentation](https://docs.expo.dev/)

### Performance

- [React Native Performance Guide](https://reactnative.dev/docs/performance)
- [Profiling React Native](https://reactnative.dev/docs/profiling)

### Testing

- [Testing Library for React Native](https://callstack.github.io/react-native-testing-library/)
- [Detox E2E Framework](https://wix.github.io/Detox/)

### State Management

- [Redux Toolkit](https://redux-toolkit.js.org/)
- [Zustand](https://github.com/pmndrs/zustand)
- [React Query](https://tanstack.com/query/latest)

### Native Modules

- [Native Modules Guide](https://reactnative.dev/docs/native-modules-intro)
- [Turbo Modules](https://reactnative.dev/docs/the-new-architecture/pillars-turbomodules)

### Deployment

- [App Store Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Play Store Policies](https://play.google.com/about/developer-content-policy/)
- [CodePush](https://github.com/microsoft/react-native-code-push)

## Examples

### Basic Usage

```javascript
// TODO: Add basic example for mobile-react-native
// This example demonstrates core functionality
```

### Advanced Usage

```javascript
// TODO: Add advanced example for mobile-react-native
// This example shows production-ready patterns
```

### Integration Example

```javascript
// TODO: Add integration example showing how mobile-react-native
// works with other systems and services
```

See `examples/mobile-react-native/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring mobile-react-native functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for mobile-react-native
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Quick Links to Templates

- [Screen Component Template](./templates/screen-component.tsx)
- [Navigation Setup](./templates/navigation-setup.tsx)
- [Redux Toolkit Slice](./templates/redux-slice.ts)
- [Component Test](./templates/component.test.tsx)
- [Metro Config](./config/metro.config.js)
- [Deployment Checklist](./resources/deployment-checklist.md)
