---
name: expo-configuration
description: Expo SDK configuration and setup. Use when configuring Expo projects.
---

# Expo Configuration Skill

This skill covers Expo SDK configuration for React Native projects.

## When to Use

Use this skill when:
- Setting up a new Expo project
- Configuring app.json/app.config.js
- Adding native modules
- Configuring build settings

## Core Principle

**MANAGED WORKFLOW** - Use Expo's managed workflow for best developer experience.

## Project Initialization

```bash
# Create new Expo project
npx create-expo-app@latest my-app

# With specific template
npx create-expo-app@latest my-app --template tabs
```

## App Configuration

### app.json

```json
{
  "expo": {
    "name": "My App",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "assetBundlePatterns": ["**/*"],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.company.myapp"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.company.myapp"
    },
    "web": {
      "bundler": "metro",
      "output": "static",
      "favicon": "./assets/favicon.png"
    },
    "plugins": [],
    "experiments": {
      "typedRoutes": true
    }
  }
}
```

### app.config.js (Dynamic Configuration)

```javascript
export default ({ config }) => {
  return {
    ...config,
    name: process.env.APP_NAME || 'My App',
    version: process.env.APP_VERSION || '1.0.0',
    extra: {
      apiUrl: process.env.API_URL,
      enableAnalytics: process.env.ENABLE_ANALYTICS === 'true',
    },
  };
};
```

## Environment Variables

### .env Files

```bash
# .env
EXPO_PUBLIC_API_URL=https://api.example.com
EXPO_PUBLIC_ANALYTICS_KEY=abc123
```

### Using Environment Variables

```typescript
// Must be prefixed with EXPO_PUBLIC_
const apiUrl = process.env.EXPO_PUBLIC_API_URL;

// Or use expo-constants for extra config
import Constants from 'expo-constants';
const { apiUrl } = Constants.expoConfig?.extra ?? {};
```

## Common Plugins

### Install Plugins

```bash
# Expo Router
npx expo install expo-router

# Secure Store
npx expo install expo-secure-store

# Image Picker
npx expo install expo-image-picker

# Camera
npx expo install expo-camera

# Location
npx expo install expo-location

# Notifications
npx expo install expo-notifications

# Haptics
npx expo install expo-haptics
```

### Configure Plugins

```json
{
  "expo": {
    "plugins": [
      "expo-router",
      "expo-secure-store",
      [
        "expo-image-picker",
        {
          "photosPermission": "Allow $(PRODUCT_NAME) to access your photos."
        }
      ],
      [
        "expo-camera",
        {
          "cameraPermission": "Allow $(PRODUCT_NAME) to access camera."
        }
      ],
      [
        "expo-location",
        {
          "locationAlwaysAndWhenInUsePermission": "Allow $(PRODUCT_NAME) to use your location."
        }
      ]
    ]
  }
}
```

## New Architecture

### Enable New Architecture

```json
{
  "expo": {
    "newArchEnabled": true
  }
}
```

## EAS Configuration

### eas.json

```json
{
  "cli": {
    "version": ">= 5.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal"
    },
    "production": {}
  },
  "submit": {
    "production": {}
  }
}
```

### EAS Update Configuration

```json
{
  "expo": {
    "updates": {
      "url": "https://u.expo.dev/your-project-id"
    },
    "runtimeVersion": {
      "policy": "appVersion"
    }
  }
}
```

## Development Commands

```bash
# Start development server
npx expo start

# Start with specific platform
npx expo start --ios
npx expo start --android

# Clear cache
npx expo start --clear

# Prebuild native projects
npx expo prebuild

# Run native build
npx expo run:ios
npx expo run:android
```

## TypeScript Configuration

### tsconfig.json

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUncheckedIndexedAccess": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  },
  "include": ["**/*.ts", "**/*.tsx", ".expo/types/**/*.ts", "expo-env.d.ts"]
}
```

### expo-env.d.ts

```typescript
/// <reference types="expo/types" />

// Add custom type declarations here
declare module '*.png' {
  const value: number;
  export default value;
}
```

## Metro Configuration

### metro.config.js

```javascript
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

// Add custom configuration
config.resolver.sourceExts.push('cjs');

module.exports = config;
```

## Splash Screen

### Configure Splash

```json
{
  "expo": {
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "cover",
      "backgroundColor": "#3B82F6"
    }
  }
}
```

### Programmatic Control

```typescript
import * as SplashScreen from 'expo-splash-screen';

// Prevent auto-hide
SplashScreen.preventAutoHideAsync();

// Hide when ready
await SplashScreen.hideAsync();
```

## App Icons

### Configure Icons

```json
{
  "expo": {
    "icon": "./assets/icon.png",
    "ios": {
      "icon": "./assets/ios-icon.png"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      }
    }
  }
}
```

## Notes

- Use `EXPO_PUBLIC_` prefix for client-side env vars
- Enable typed routes for type-safe navigation
- Configure EAS for production builds
- Use app.config.js for dynamic configuration
- Add plugins for native functionality
