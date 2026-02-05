---
name: eas-build-setup
description: EAS Build configuration for iOS and Android. Use when setting up cloud builds.
---

# EAS Build Setup Skill

This skill covers EAS Build configuration for React Native apps.

## When to Use

Use this skill when:
- Setting up cloud builds
- Configuring build profiles
- Managing credentials
- Building for app stores

## Core Principle

**CLOUD-FIRST BUILDS** - Let EAS handle the complexity of native builds.

## Installation

```bash
# Install EAS CLI globally
npm install -g eas-cli

# Login to Expo account
eas login

# Initialize EAS in project
eas build:configure
```

## Basic Configuration

```json
// eas.json
{
  "cli": {
    "version": ">= 12.0.0"
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

## Full Configuration

```json
// eas.json
{
  "cli": {
    "version": ">= 12.0.0",
    "appVersionSource": "remote"
  },
  "build": {
    "base": {
      "node": "20.11.0",
      "env": {
        "EXPO_PUBLIC_API_URL": "https://api.example.com"
      }
    },
    "development": {
      "extends": "base",
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      },
      "android": {
        "buildType": "apk"
      },
      "env": {
        "EXPO_PUBLIC_API_URL": "https://api.dev.example.com"
      }
    },
    "preview": {
      "extends": "base",
      "distribution": "internal",
      "ios": {
        "resourceClass": "m-medium"
      },
      "android": {
        "buildType": "apk"
      },
      "channel": "preview",
      "env": {
        "EXPO_PUBLIC_API_URL": "https://api.staging.example.com"
      }
    },
    "production": {
      "extends": "base",
      "autoIncrement": true,
      "ios": {
        "resourceClass": "m-medium"
      },
      "channel": "production",
      "env": {
        "EXPO_PUBLIC_API_URL": "https://api.example.com"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "ABCD1234"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "internal"
      }
    }
  }
}
```

## App Configuration

```typescript
// app.config.ts
import { ExpoConfig, ConfigContext } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: 'My App',
  slug: 'my-app',
  version: '1.0.0',
  orientation: 'portrait',
  icon: './assets/icon.png',
  splash: {
    image: './assets/splash.png',
    resizeMode: 'contain',
    backgroundColor: '#ffffff',
  },
  ios: {
    bundleIdentifier: 'com.company.myapp',
    supportsTablet: true,
    infoPlist: {
      NSCameraUsageDescription: 'This app uses the camera for...',
      NSPhotoLibraryUsageDescription: 'This app accesses photos for...',
    },
  },
  android: {
    package: 'com.company.myapp',
    adaptiveIcon: {
      foregroundImage: './assets/adaptive-icon.png',
      backgroundColor: '#ffffff',
    },
    permissions: [
      'CAMERA',
      'READ_EXTERNAL_STORAGE',
      'WRITE_EXTERNAL_STORAGE',
    ],
  },
  extra: {
    eas: {
      projectId: 'your-project-id',
    },
  },
  owner: 'your-expo-account',
});
```

## Credentials Management

```bash
# iOS credentials
eas credentials --platform ios

# Android credentials
eas credentials --platform android

# View current credentials
eas credentials

# Generate new iOS distribution certificate
eas credentials --platform ios

# Generate new Android keystore
eas credentials --platform android
```

## Build Commands

```bash
# Development build (with dev client)
eas build --profile development --platform ios
eas build --profile development --platform android

# Preview build (internal testing)
eas build --profile preview --platform all

# Production build
eas build --profile production --platform all

# Build with specific message
eas build --profile production --message "Release v1.0.0"

# Local build (without cloud)
eas build --local --platform ios
```

## iOS Specific Configuration

```json
// eas.json - iOS section
{
  "build": {
    "production": {
      "ios": {
        "resourceClass": "m-medium",
        "image": "latest",
        "credentialsSource": "remote",
        "buildConfiguration": "Release"
      }
    }
  }
}
```

### iOS Entitlements

```xml
<!-- ios/MyApp/MyApp.entitlements -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>aps-environment</key>
  <string>production</string>
  <key>com.apple.developer.associated-domains</key>
  <array>
    <string>applinks:example.com</string>
  </array>
</dict>
</plist>
```

## Android Specific Configuration

```json
// eas.json - Android section
{
  "build": {
    "preview": {
      "android": {
        "buildType": "apk",
        "gradleCommand": ":app:assembleRelease"
      }
    },
    "production": {
      "android": {
        "buildType": "app-bundle",
        "gradleCommand": ":app:bundleRelease",
        "resourceClass": "medium"
      }
    }
  }
}
```

## Environment Variables

```json
// eas.json
{
  "build": {
    "production": {
      "env": {
        "EXPO_PUBLIC_API_URL": "https://api.example.com",
        "EXPO_PUBLIC_ANALYTICS_ID": "UA-XXXXX-Y"
      }
    }
  }
}
```

```bash
# Or use EAS Secrets for sensitive values
eas secret:create --name API_KEY --value "your-secret-key" --scope project
eas secret:list
```

## Build Hooks

```json
// package.json
{
  "scripts": {
    "eas-build-pre-install": "echo 'Running pre-install hook'",
    "eas-build-post-install": "echo 'Running post-install hook'",
    "eas-build-on-success": "echo 'Build succeeded!'",
    "eas-build-on-error": "echo 'Build failed!'"
  }
}
```

## Internal Distribution

```bash
# Register devices for internal distribution
eas device:create

# List registered devices
eas device:list

# Build for internal distribution
eas build --profile preview --platform ios
```

## Monitoring Builds

```bash
# View build status
eas build:list

# View specific build
eas build:view <build-id>

# Cancel build
eas build:cancel <build-id>

# Download build artifacts
eas build:download --platform ios --latest
```

## CI/CD Integration

```yaml
# .github/workflows/eas-build.yml
name: EAS Build

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Setup EAS
        uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}

      - name: Build preview
        if: github.event_name == 'pull_request'
        run: eas build --profile preview --platform all --non-interactive

      - name: Build production
        if: github.ref == 'refs/heads/main'
        run: eas build --profile production --platform all --non-interactive
```

## Version Management

```json
// eas.json
{
  "cli": {
    "appVersionSource": "remote"
  },
  "build": {
    "production": {
      "autoIncrement": true
    }
  }
}
```

```bash
# Manually set version
eas build:version:set --platform ios --version 1.2.0 --build-number 45
eas build:version:set --platform android --version 1.2.0 --version-code 45

# Get current version
eas build:version:get --platform ios
```

## Notes

- Use development builds for debugging
- Use preview builds for internal testing
- Use production builds for store submission
- Keep credentials in EAS (remote) for team sharing
- Use EAS Secrets for sensitive environment variables
- Set up CI/CD for automated builds
- Monitor build times and optimize as needed
