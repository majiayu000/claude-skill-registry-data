---
name: multi-tv-builder
displayName: "Multi-TV Builder"
description: "Complete knowledge base for building production-ready cross-platform TV applications with React Native - supporting Android TV, Apple TV, Fire TV (Fire OS & Vega OS), and Web TV platforms with a single codebase. Use when implementing TV apps, monorepo architecture, spatial navigation, video playback, platform-specific optimizations, or migrating from Vega to multi-platform."
keywords: ["tv", "react-native", "android-tv", "apple-tv", "fire-tv", "vega", "tvos", "web-tv", "video", "streaming", "spatial-navigation", "monorepo", "expo", "migration", "typescript", "cross-platform", "remote-control", "focus-management"]
author: "Giovanni Laquidara"
---

# Multi-TV Builder - Complete Knowledge Base

Build production-ready cross-platform TV applications with React Native, supporting Android TV, Apple TV, Fire TV (Fire OS & Vega OS), and Web TV platforms with a single codebase.

## Quick Reference

- **Sample Repo**: https://github.com/AmazonAppDev/react-native-multi-tv-app-sample
- **Slash Commands**: `/multi-tv-help`, `/multi-tv-setup`, `/multi-tv-build`, `/multi-tv-platform`
- **Skills**: `multi-tv-builder`, `apple-tv-troubleshooter`, `tmdb-integration`
- **Author**: Giovanni Laquidara

## Core Capabilities

- **Cross-platform TV support** with single codebase for 5+ platforms
- **Monorepo architecture** with Yarn workspaces for apps and shared packages
- **Spatial navigation** optimized for TV remote controls and D-pad input
- **Video playback** with custom controls and remote integration
- **Platform-specific optimizations** using automatic file resolution
- **Shared UI library** with reusable TV-optimized components
- **TypeScript-first** with strict type safety across all packages

## Supported Platforms

| Platform | Technology | Output |
|----------|-----------|--------|
| Android TV | react-native-tvos | APK/AAB |
| Apple TV (tvOS) | react-native-tvos + Expo | IPA |
| Fire TV (Fire OS) | react-native-tvos | APK |
| Fire TV (Vega OS) | Amazon Vega SDK | Optimized VPKG |
| Web TV | React Native Web | HTML/JS Bundle |

---

# Product Overview

## React Native Multi-TV App Sample

A production-ready TV application template for building cross-platform TV apps with a single React Native codebase.

### Core Features

1. **Video Playback**
   - Integrated video player with react-native-video (universal) or W3C Media APIs (Vega)
   - Custom overlay controls with play/pause, seek bar, and time display
   - Remote control integration (play/pause, seek ±10s, exit)
   - Auto-hide controls after 5s of inactivity
   - Buffering indicators during loading

2. **Spatial Navigation**
   - React TV Space Navigation for focus management
   - D-pad/arrow key navigation optimized for TV remotes
   - Platform-specific remote control managers
   - Focus restoration when returning from player

3. **Content Discovery**
   - Dynamic content loading from external catalog API
   - Grid layouts optimized for TV screens
   - Detail screens with rich metadata (genre, rating, duration, year)
   - Dynamic hero banner based on focused content
   - Trending flags and content ratings

4. **Navigation**
   - Drawer navigation with left-side menu
   - Stack navigation for detail screens
   - Platform-specific navigation optimizations
   - Deep linking support (optional)

5. **Responsive Design**
   - Adaptive layouts for different TV screen sizes
   - Responsive scaling with useScale hook
   - Platform-specific layout adjustments
   - Safe zone handling for TV overscan

### App Variants

1. **expo-multi-tv** - Universal app supporting Android TV, Apple TV, Fire TV (Fire OS), and Web
2. **vega** - Fire TV Vega OS optimized build using Amazon Vega SDK

### Key Use Cases

- Streaming video applications
- Content discovery and browsing
- TV-optimized user interfaces
- Cross-platform TV development reference

---

# Architecture & Structure

## Monorepo Organization

```
project-root/
├── apps/                    # Application packages
│   ├── expo-multi-tv/      # Universal TV app
│   └── vega/               # Fire TV Vega optimized
├── packages/               # Shared packages
│   └── shared-ui/          # Shared components
├── package.json            # Workspace configuration
├── tsconfig.base.json      # Shared TypeScript config
├── babel.config.js         # Root babel configuration
└── yarn.lock               # Dependency lock file
```

## Apps Directory

### `apps/expo-multi-tv/`
Universal TV application built with Expo SDK.

**Key Files:**
- `App.tsx` - Main entry point
- `app.json` - Expo configuration
- `package.json` - App-specific dependencies
- `tsconfig.json` - TypeScript config extending base
- `metro.config.js` - Metro bundler configuration
- `ios/` - iOS/tvOS native code
- `android/` - Android TV native code

**Platforms Supported:**
- Android TV
- Apple TV (tvOS)
- Fire TV (Fire OS)
- Web (LG WebOS, Samsung Tizen)

### `apps/vega/`
Fire TV Vega OS optimized application using Amazon Vega SDK.

**Key Files:**
- `App.tsx` - Main entry point
- `package.json` - Vega-specific dependencies
- `tsconfig.json` - TypeScript config
- `metro.config.js` - Metro bundler configuration
- `android/` - Fire TV Vega native code

**Platform Supported:**
- Fire TV (Vega OS)

## Shared UI Package Structure

```
packages/shared-ui/src/
├── app/                           # App-level configuration
│   └── remote-control/           # Platform-specific remote managers
│       ├── RemoteControlManager.android.ts
│       ├── RemoteControlManager.ios.ts
│       └── RemoteControlManager.kepler.ts
├── assets/                        # Static assets (fonts, images, icons)
├── components/                    # Reusable UI components
│   ├── player/                   # Video player components
│   ├── CustomDrawerContent.tsx   # Drawer menu
│   ├── FocusablePressable.tsx    # TV-optimized pressable
│   ├── LoadingIndicator.tsx      # Loading spinner
│   ├── MenuContext.tsx           # Menu state management
│   └── PlatformLinearGradient.tsx # Cross-platform gradient
├── data/                          # Data and API
│   └── moviesData.ts             # Movie catalog API
├── hooks/                         # Custom React hooks
│   └── useScale.ts               # Responsive scaling
├── navigation/                    # Navigation configuration
│   ├── AppNavigator.tsx          # Main app navigator
│   ├── DrawerNavigator.tsx       # Drawer navigation
│   ├── RootNavigator.tsx         # Root wrapper
│   └── types.ts                  # Navigation types
├── screens/                       # Screen components
│   ├── DetailsScreen.tsx         # Content detail
│   ├── ExploreScreen.tsx         # Content exploration
│   ├── HomeScreen.tsx            # Home/landing
│   ├── PlayerScreen.tsx          # Video player
│   ├── PlayerScreen.vega.tsx     # Vega-specific player
│   ├── SettingsScreen.tsx        # Settings
│   └── TVScreen.tsx              # TV content
├── theme/                         # Design system
│   ├── colors.ts                 # Color palette
│   ├── spacing.ts                # Spacing scale
│   ├── typography.ts             # Font styles
│   ├── safeZones.ts              # TV safe zones
│   └── index.ts                  # Theme exports
├── utils/                         # Utility functions
└── index.ts                       # Package exports
```

## Platform-Specific File Resolution

Metro bundler automatically resolves platform files:
- `.kepler.ts/tsx` - Fire TV Vega OS (highest priority for Vega builds)
- `.android.ts/tsx` - Android TV & Fire TV Fire OS
- `.ios.ts/tsx` - Apple TV (tvOS)
- `.vega.tsx` - Vega-specific screens
- `.web.ts/tsx` - Web platforms (LG WebOS, Samsung Tizen)
- `.ts/tsx` - Default/shared implementation (lowest priority)

**Example:**
```
RemoteControlManager.android.ts  → Android TV
RemoteControlManager.ios.ts      → Apple TV
RemoteControlManager.kepler.ts   → Fire TV Vega
```

### Key Architectural Patterns

#### Shared UI Library Pattern
- All reusable components live in `@project/shared-ui` package
- Apps import from shared package, never local files
- Platform-specific implementations use file extensions
- Single source of truth for UI components and screens

#### TV-First Design
- **10-foot UI**: Larger touch targets, high-contrast colors, readable typography
- **Safe zones**: Content positioned within TV safe areas (see theme/safeZones.ts)
- **Focus management**: Clear visual focus indicators for all interactive elements
- **Remote control**: D-pad navigation with platform-specific key mappings

---

# Technology Stack

## Build System

- **Yarn Workspaces v4+**: Monorepo management
- **Metro Bundler**: Module bundling with platform-specific resolution
- **TypeScript v5.3+**: Strict mode enabled across all packages

## Core Technologies

- **React Native**: v0.74+ (react-native-tvos fork)
- **Expo SDK**: v51+ (for universal app)
- **React**: v18.2+
- **TypeScript**: v5.3+ with strict mode

## Navigation & Focus

- **React Navigation v6**: Drawer and stack navigators
- **React TV Space Navigation**: Spatial navigation for TV remotes
- **Platform Remote Managers**: Android (react-native-keyevent), iOS (TVEventHandler), Vega (Kepler SDK)

## Video Playback

- **react-native-video v6+**: Universal app video player
- **W3C Media APIs**: Native video for Vega OS
- Custom overlay controls with spatial navigation

## Platform-Specific SDKs

- **Amazon Vega SDK**: Fire TV Vega OS builds
- **@amazon-devices packages**: Kepler SDK components
- **react-native-tvos**: TV platform support (Android TV, Apple TV, Fire TV FOS)

## Development Tools

- **ESLint**: Code quality with TypeScript and React plugins
- **Prettier**: Code formatting (120 char width, single quotes)
- **Husky**: Git hooks for pre-commit checks
- **Commitlint**: Conventional commit enforcement
- **Jest**: Unit testing

---

# Implementation Patterns

## Workspace Configuration

**Root `package.json`:**
```json
{
  "name": "tv-app-project",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "packageManager": "yarn@4.5.0",
  "scripts": {
    "dev": "yarn workspace @project/expo-multi-tv start",
    "dev:android": "yarn workspace @project/expo-multi-tv android",
    "dev:ios": "yarn workspace @project/expo-multi-tv ios",
    "dev:web": "yarn workspace @project/expo-multi-tv web",
    "dev:vega": "yarn workspace @project/vega start",
    "build:vega": "yarn workspace @project/vega run build",
    "test:all": "yarn workspaces foreach -pt run test",
    "lint:all": "yarn workspaces foreach -pt run lint",
    "clean:all": "yarn workspaces foreach run clean"
  }
}
```

## Theme System

Centralized design tokens in `packages/shared-ui/src/theme/`:

**colors.ts:**
```typescript
export const colors = {
  primary: '#E50914',      // Netflix-style red
  background: '#141414',   // Dark background
  card: '#2F2F2F',        // Card background
  text: '#FFFFFF',        // Primary text
  textSecondary: '#B3B3B3' // Secondary text
};
```

**spacing.ts:**
```typescript
export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48
};
```

**safeZones.ts:**
```typescript
export const safeZones = {
  horizontal: 48,  // Left/right margins for TV overscan
  vertical: 27     // Top/bottom margins
};
```

## Responsive Scaling

**useScale hook:**
```typescript
import { Dimensions } from 'react-native';

const BASE_WIDTH = 1920;
const BASE_HEIGHT = 1080;

export const useScale = () => {
  const { width, height } = Dimensions.get('window');

  const scaleWidth = width / BASE_WIDTH;
  const scaleHeight = height / BASE_HEIGHT;
  const scale = Math.min(scaleWidth, scaleHeight);

  return {
    scale: (size: number) => size * scale,
    width,
    height
  };
};
```

## Remote Control Manager Interface

All platform managers implement this interface:

```typescript
export interface RemoteControlManagerInterface {
  initialize(): void;
  cleanup(): void;
}
```

**Android/Fire TV FOS (`RemoteControlManager.android.ts`):**
```typescript
import ReactNativeKeyEvent from 'react-native-keyevent';

export class RemoteControlManager implements RemoteControlManagerInterface {
  initialize() {
    ReactNativeKeyEvent.onKeyDownListener((keyEvent) => {
      // Handle Android TV remote keys
    });
  }

  cleanup() {
    ReactNativeKeyEvent.removeKeyDownListener();
  }
}
```

**Apple TV (`RemoteControlManager.ios.ts`):**
```typescript
import { TVEventHandler } from 'react-native';

export class RemoteControlManager implements RemoteControlManagerInterface {
  private tvEventHandler: TVEventHandler | null = null;

  initialize() {
    this.tvEventHandler = new TVEventHandler();
    this.tvEventHandler.enable(this, (component, evt) => {
      // Handle tvOS remote events
    });
  }

  cleanup() {
    this.tvEventHandler?.disable();
  }
}
```

**Fire TV Vega (`RemoteControlManager.kepler.ts`):**
```typescript
import { TVEventHandler } from '@amazon-devices/react-native-kepler';

export class RemoteControlManager implements RemoteControlManagerInterface {
  private tvEventHandler: TVEventHandler | null = null;

  initialize() {
    this.tvEventHandler = new TVEventHandler();
    this.tvEventHandler.enable(this, (component, evt) => {
      // Handle Vega remote events
    });
  }

  cleanup() {
    this.tvEventHandler?.disable();
  }
}
```

## Spatial Navigation Setup

**Integration with React TV Space Navigation:**
```typescript
import { SpatialNavigation } from 'react-tv-space-navigation';

// Initialize in App.tsx
SpatialNavigation.init({
  debug: __DEV__,
  visualDebug: __DEV__
});

// Use in components
import { useFocusable } from 'react-tv-space-navigation';

const MyComponent = () => {
  const { ref, focused } = useFocusable();

  return (
    <View ref={ref} style={focused ? styles.focused : styles.default}>
      {/* Content */}
    </View>
  );
};
```

## Video Player Implementation

**Universal App (expo-multi-tv):**
```typescript
import Video from 'react-native-video';

<Video
  source={{ uri: videoUrl }}
  style={styles.video}
  controls={Platform.OS === 'ios'} // Native controls on iOS
  resizeMode="contain"
  onLoad={handleLoad}
  onProgress={handleProgress}
  ref={videoRef}
/>
```

**Vega App:**
```typescript
// Use W3C Media APIs through Kepler SDK
import { VideoView } from '@amazon-devices/react-native-kepler';

<VideoView
  source={{ uri: videoUrl }}
  style={styles.video}
  onLoad={handleLoad}
  ref={videoRef}
/>
```

## Dynamic Content Loading

**Catalog API Integration:**
```typescript
// packages/shared-ui/src/data/moviesData.ts
export interface Movie {
  id: string;
  title: string;
  genre: string;
  rating: number;
  contentRating: string;
  year: number;
  duration: number;
  videoUrl: string;
  imageUrl: string;
  trending: boolean;
}

export const fetchMovies = async (): Promise<Movie[]> => {
  const response = await fetch('https://api.example.com/catalog.json');
  const data = await response.json();
  return transformCatalogData(data);
};
```

---

# Common Commands

## Development

```bash
# Install all dependencies
yarn install

# Start Metro bundler for expo-multi-tv
yarn dev

# Run on specific platforms
yarn dev:android    # Android TV & Fire TV FOS
yarn dev:ios        # Apple TV
yarn dev:web        # Web TV platforms

# Start Metro bundler for vega
yarn dev:vega
```

## Building

**Expo Multi-TV App:**
```bash
# Build for all platforms
cd apps/expo-multi-tv

# Android TV / Fire TV (Fire OS)
npx expo build:android
# or: npx expo run:android

# Apple TV (tvOS)
npx expo build:ios
# or: npx expo run:ios

# Web TV platforms
npx expo export --platform web
```

**Fire TV Vega App:**
```bash
# From project root
yarn build:vega         # Build release VPKG
yarn build:vega:debug   # Build debug VPKG

# From apps/vega directory
cd apps/vega

# Build with npm (default from Vega CLI)
npm run build:app       # Builds for all architectures

# Build with Kepler CLI (more control)
kepler build --arch armv7 --buildType release    # Fire TV Stick
kepler build --arch aarch64 --buildType release  # M-series Mac virtual devices
kepler build --arch x86_64 --buildType release   # Intel virtual devices

# Clean build
rm -rf build && npm run build:app
```

## Testing & Linting

```bash
# Run tests across all workspaces
yarn test:all

# Lint all workspaces
yarn lint:all

# Type check
yarn typecheck

# Format code
yarn format
```

## Vega CLI Commands

**Project Management:**
```bash
# List available project templates
kepler project list-templates

# Generate new Vega project
kepler project generate \
  --template hello-world \
  --name myapp \
  --packageId com.company.myapp \
  --outputDir myapp

# Verify Vega SDK installation
kepler --version
```

**Building:**
```bash
# Build for specific architecture and build type
kepler build --arch <armv7|aarch64|x86_64> --buildType <debug|release>

# Examples:
kepler build --arch armv7 --buildType release     # Production Fire TV Stick build
kepler build --arch aarch64 --buildType debug     # Debug build for M-series Mac
kepler build --arch x86_64 --buildType debug      # Debug build for Intel virtual device
```

**Device Management:**
```bash
# List connected devices
kepler device list

# Install VPKG on device
kepler install --vpkg <path-to-vpkg-file>

# Run app on device
kepler run --packageId com.company.myapp
```

---

# Getting Started

## Quick Start (Recommended)

The fastest way to get started is to clone the official React Native Multi-TV App Sample repository.

**Clone the Repository:**
```bash
# Clone the official sample repository
git clone https://github.com/AmazonAppDev/react-native-multi-tv-app-sample.git
cd react-native-multi-tv-app-sample

# Install dependencies
yarn install

# Bootstrap the monorepo
yarn bootstrap
```

**What's Included:**
- ✅ Pre-configured monorepo with Yarn workspaces
- ✅ expo-multi-tv app - Universal app for Android TV, Apple TV, Fire TV (Fire OS), and Web
- ✅ vega app - Fire TV Vega OS optimized app
- ✅ shared-ui package - Complete component library
- ✅ All configuration files

**Next Steps After Cloning:**
1. Review the codebase
2. Set up for Expo TV - Follow Expo TV documentation
3. Set up for Vega (optional) - Install Vega SDK
4. Run on platforms
5. Customize for your needs

## Alternative: Build from Scratch

### 1. Initialize Project Structure

```bash
# Create project directory
mkdir my-tv-app && cd my-tv-app

# Initialize package.json
yarn init -y

# Create directory structure
mkdir -p apps packages/shared-ui
```

### 2. Configure Shared TypeScript

Create `tsconfig.base.json`:
```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "CommonJS",
    "lib": ["ES2021"],
    "jsx": "react-native",
    "strict": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

### 3. Set Up Shared UI Package

```bash
cd packages/shared-ui
yarn init -y

# Install dependencies
yarn add react react-native
yarn add -D typescript @types/react @types/react-native

# Create src directory structure
mkdir -p src/{components,screens,navigation,hooks,theme,app/remote-control,data,utils,assets}
```

### 4. Create Universal App (expo-multi-tv)

**IMPORTANT:** Follow the official Expo TV setup guide.

Option 1: Start with the basic TV template:
```bash
cd apps
npx create-expo-app@latest expo-multi-tv -e with-tv
```

Option 2: Start with the TV Router template (recommended):
```bash
cd apps
npx create-expo-app@latest expo-multi-tv -e with-router-tv
```

**After creating the app:**

1. Link shared-ui package by editing `apps/expo-multi-tv/package.json`
2. Install additional TV dependencies
3. Configure Metro bundler for monorepo

### 5. Create Vega App (Optional - Fire TV Vega OS Only)

**Prerequisites: Install Vega SDK**

**Required Dependencies (macOS):**
```bash
# For Apple Silicon Macs (includes Rosetta 2)
[[ $(arch) == "arm64" ]] && softwareupdate --install-rosetta --agree-to-license; brew update && brew install binutils coreutils gawk findutils grep jq lz4 gnu-sed watchman

# For Intel Macs
brew update && brew install binutils coreutils gawk findutils grep jq lz4 gnu-sed watchman
```

**Install Vega SDK:**
1. Close VS Code before installing
2. Download and run installer
3. Add export commands to shell config
4. Verify: `kepler --version`

**Create Vega Project:**
```bash
cd apps

kepler project generate \
  --template hello-world \
  --name vega \
  --packageId com.yourcompany.yourapp.vega \
  --outputDir vega
```

### 6. Configure Metro Bundler

**metro.config.js** (in each app):
```javascript
const { getDefaultConfig } = require('expo/metro-config');
const path = require('path');

const config = getDefaultConfig(__dirname);

// Add monorepo support
const projectRoot = __dirname;
const workspaceRoot = path.resolve(projectRoot, '../..');

config.watchFolders = [workspaceRoot];
config.resolver.nodeModulesPaths = [
  path.resolve(projectRoot, 'node_modules'),
  path.resolve(workspaceRoot, 'node_modules'),
];

module.exports = config;
```

---

# Vega to Multi-TV Migration Guide

## Prerequisites

- Node.js 18+
- Yarn 4.x (Berry)
- Java 17 (for Android builds)
- Android SDK with TV emulator
- Xcode (for Apple TV builds)

## Phase 1: Monorepo Setup

### 1.1 Initialize Yarn Workspaces

Create root `package.json`:

```json
{
  "name": "@mycompany/multi-tv",
  "version": "1.0.0",
  "private": true,
  "packageManager": "yarn@4.5.0",
  "workspaces": [
    "apps/*",
    "packages/*"
  ],
  "resolutions": {
    "metro-source-map": "0.80.12"
  }
}
```

**CRITICAL**: The `metro-source-map` resolution is required to fix a babel plugin error. Without it, you'll get:
```
.plugins[0] must be a string, object, function
```

### 1.2 Create Root Babel Config

**CRITICAL**: Create `babel.config.js` at monorepo root. Metro looks for babel config starting from the project root.

```javascript
const path = require('path');

module.exports = function (api) {
  api.cache(true);

  // Try to resolve reanimated plugin from the universal TV app
  let reanimatedPlugin;
  try {
    reanimatedPlugin = require.resolve('react-native-reanimated/plugin', {
      paths: [path.join(__dirname, 'apps/universal-tv/node_modules')]
    });
  } catch (e) {
    try {
      reanimatedPlugin = require.resolve('react-native-reanimated/plugin');
    } catch (e2) {
      reanimatedPlugin = null;
    }
  }

  const plugins = reanimatedPlugin ? [reanimatedPlugin] : [];

  return {
    presets: ['babel-preset-expo'],
    plugins,
  };
};
```

## Phase 2: Shared UI Package Setup

### Platform-Specific File Resolution

| Extension | Platform | Description |
|-----------|----------|-------------|
| `.ts` / `.tsx` | All | Base/shared implementation |
| `.native.ts` | React Native | Android TV, Apple TV, Fire TV FOS |
| `.android.ts` | Android | Android TV, Fire TV FOS |
| `.ios.ts` | iOS/tvOS | Apple TV |
| `.kepler.ts` | Vega | Fire TV Vega OS specific |
| `.web.ts` | Web | Web TV specific |

**CRITICAL - Avoiding Circular Dependencies**:

When you have a base class that platform-specific files extend, Metro's platform resolution can create a circular dependency.

```
# BAD - Creates circular dependency
RemoteControlManager.ts        # Base class
RemoteControlManager.android.ts # Imports from RemoteControlManager.ts
```

**FIX**: Rename base files to use `.base.ts` extension:

```
# GOOD - No circular dependency
RemoteControlManager.base.ts    # Base class
RemoteControlManager.android.ts # Imports from RemoteControlManager.base.ts
RemoteControlManager.ios.ts     # Imports from RemoteControlManager.base.ts
```

## Phase 3: Universal TV App Setup (Expo)

### Fix HMRClient Error (CRITICAL)

**CRITICAL**: The `react-native-tvos` fork has an HMR (Hot Module Replacement) incompatibility.

**Fix**: Add HMRClient polyfill to `apps/universal-tv/index.js`:

```javascript
import { registerRootComponent } from 'expo';
import { AppRegistry } from 'react-native';
import App from './App';

// Polyfill for HMRClient to prevent "Module has not been registered as callable" error
if (!AppRegistry.getRunnable('HMRClient')) {
  AppRegistry.registerCallableModule('HMRClient', {
    setup: () => {},
    enable: () => {},
    disable: () => {},
  });
}

registerRootComponent(App);
```

### Configure app.json

```json
{
  "expo": {
    "name": "MyTVApp",
    "slug": "my-tv-app",
    "version": "1.0.0",
    "orientation": "landscape",
    "userInterfaceStyle": "dark",
    "plugins": [
      "@react-native-tvos/config-tv"
    ]
  }
}
```

## Phase 4: Platform Abstraction Layer

### Remote Control Manager Pattern

Create base class in `packages/shared-ui/src/app/remote-control/RemoteControlManager.base.ts`:

```typescript
export type RemoteKey =
  | 'up' | 'down' | 'left' | 'right'
  | 'select' | 'back'
  | 'play' | 'pause' | 'playPause'
  | 'fastForward' | 'rewind'
  | 'menu';

export interface RemoteKeyEvent {
  key: RemoteKey;
  action: 'keyDown' | 'keyUp';
  timestamp: number;
}

export type RemoteKeyHandler = (event: RemoteKeyEvent) => void;

export interface RemoteControlManagerInterface {
  initialize(): void;
  cleanup(): void;
  addKeyListener(handler: RemoteKeyHandler): () => void;
  removeKeyListener(handler: RemoteKeyHandler): void;
}

export class BaseRemoteControlManager implements RemoteControlManagerInterface {
  protected listeners: Set<RemoteKeyHandler> = new Set();

  initialize(): void {
    // Override in platform-specific implementation
  }

  cleanup(): void {
    this.listeners.clear();
  }

  addKeyListener(handler: RemoteKeyHandler): () => void {
    this.listeners.add(handler);
    return () => this.removeKeyListener(handler);
  }

  removeKeyListener(handler: RemoteKeyHandler): void {
    this.listeners.delete(handler);
  }

  protected notifyListeners(event: RemoteKeyEvent): void {
    this.listeners.forEach((handler) => handler(event));
  }
}
```

### Video Player Service Pattern

Create interface in `packages/shared-ui/src/services/videoPlayer/VideoPlayerService.ts`:

```typescript
export interface VideoSource {
  uri: string;
  type?: 'hls' | 'dash' | 'mp4';
  headers?: Record<string, string>;
  drm?: DRMConfig;
}

export interface DRMConfig {
  type: 'widevine' | 'fairplay' | 'playready';
  licenseServer: string;
  headers?: Record<string, string>;
}

export interface PlaybackState {
  isPlaying: boolean;
  isPaused: boolean;
  isBuffering: boolean;
  currentTime: number;
  duration: number;
}

export interface VideoPlayerService {
  initialize(): Promise<void>;
  load(source: VideoSource): Promise<void>;
  play(): Promise<void>;
  pause(): Promise<void>;
  seek(timeInSeconds: number): Promise<void>;
  destroy(): Promise<void>;
  getPlaybackState(): PlaybackState;
}

export const DEFAULT_SEEK_SECONDS = 10;
```

Create native implementation in `VideoPlayerService.native.ts` (uses react-native-video).
Create Vega implementation in `VideoPlayerService.kepler.ts` (uses Shaka/W3C Media).

## Migration Troubleshooting

### Error: `.plugins[0] must be a string, object, function`

**Cause**: `metro-source-map` version mismatch in monorepo
**Fix**: Add resolution in root `package.json`:
```json
"resolutions": {
  "metro-source-map": "0.80.12"
}
```

### Error: `Super expression must either be null or a function`

**Cause**: Circular dependency in class inheritance due to Metro's platform resolution
**Fix**: Rename base class files from `ClassName.ts` to `ClassName.base.ts`

### Error: `HMRClient.setup() Module has not been registered`

**Cause**: react-native-tvos HMR incompatibility with Expo
**Fix**: Add HMRClient polyfill in `index.js`

### Error: `Cannot find module '@mycompany/shared-ui'`

**Cause**: Metro not configured for monorepo workspace resolution
**Fix**:
1. Add `watchFolders` in metro.config.js
2. Add `extraNodeModules` mapping
3. Run `yarn install` from root

### Warning: `Require cycle: X.ts -> X.ts`

**Cause**: Platform-specific file importing itself due to Metro resolution
**Fix**: Rename base file to use `.base.ts` extension

## Version Compatibility Matrix

| Package | Version | Notes |
|---------|---------|-------|
| expo | ~51.0.0 | Required for TV support |
| react | 18.2.0 | Must match expo requirement |
| react-native-tvos | ~0.74.3-0 | Use instead of react-native |
| metro-source-map | 0.80.12 | Force via resolution |
| react-native-reanimated | ~3.10.1 | For animations |
| @react-native-tvos/config-tv | ^0.0.12 | Expo plugin for TV |
| react-tv-space-navigation | ^3.6.1 | Spatial navigation |
| Java | 17 | Required for Android Gradle |
| Node.js | 18+ | Required for Expo |
| Yarn | 4.x | Berry with workspaces |

---

# Best Practices

## TV-Specific Design

- Always test on actual TV hardware, not just emulators
- Maintain 10-foot UI standards (large text, high contrast)
- Position critical UI within safe zones (48px horizontal, 27px vertical)
- Provide clear focus indicators (borders, scale, highlights)
- Design for remote control first, touch second

## Focus Management

- Set default focus on screen mount
- Restore focus when returning from navigation
- Prevent focus traps (ensure all UI is reachable)
- Test navigation flow with D-pad only
- Handle edge cases (first/last item in grid)

## Performance

- Optimize image sizes for TV resolution (1920x1080)
- Use FlatList for long scrolling lists
- Implement image caching strategy
- Lazy load video content
- Monitor memory usage on low-end devices

## Platform-Specific Code

- Use file extensions for platform variants
- Keep shared logic in base files
- Document platform differences
- Test each platform independently
- Abstract platform APIs behind common interfaces

## Video Player

- Always show buffering state
- Handle network failures gracefully
- Implement playback controls with remote support
- Test with various video formats and codecs
- Support multiple video qualities/bitrates

## Content Loading

- Implement retry logic for failed requests
- Show loading states during fetch
- Cache catalog data locally
- Handle empty states gracefully
- Validate API response structure

---

# Testing

## Unit Tests

- Test business logic in shared-ui package
- Mock platform-specific modules
- Test remote control event handlers
- Validate navigation flows
- Test data transformations

## Integration Tests

- Test cross-platform file resolution
- Validate navigation between screens
- Test video player controls
- Verify focus management
- Test catalog API integration

## Platform Testing

- Test on Android TV emulator and device
- Test on Apple TV simulator and device
- Test on Fire TV device
- Test on web browser with keyboard navigation
- Verify remote control functionality per platform

---

# Troubleshooting

## Metro Bundler Issues

- Clear cache: `yarn start --reset-cache`
- Check for port conflicts (default 8081)
- Verify workspace resolution in metro.config.js

## Platform-Specific Build Failures

- **iOS/tvOS**: Check Node binary path in `.xcode.env.local`
- **Android TV**: Verify Android SDK and emulator setup
- **Vega**: See Vega-specific troubleshooting below

## Vega SDK Issues

### Installation Problems

**'Electron quit unexpectedly' during installation**
- This is expected if VS Code is running during installation
- Restart VS Code after installation completes

**Vega SDK not found / kepler command not available**
- Verify: `kepler --version`
- Check environment variables:
  ```bash
  echo $KEPLER_SDK_PATH
  echo $PATH | grep kepler
  ```
- Add exports to shell config if missing

**Development utilities missing (macOS)**
```bash
brew update && brew install binutils coreutils gawk findutils grep jq lz4 gnu-sed watchman
```

### Build Failures

**npm run build:app fails**
- Ensure dependencies installed: `npm install`
- Check Node.js version: `node --version` (requires 16.x or later)
- Verify package ID format (reverse DNS, no `com.amazon`)
- Check Metro not already running on port 8081

**VPKG file not generated**
- Check build output: `build/<architecture>-<buildType>/`
- Try clean build: `rm -rf build && npm run build:app`

### Runtime Issues

**App crashes on Vega device**
- Check device logs for errors
- Verify VPKG architecture matches device
- Test with debug build first
- Ensure native dependencies compatible with Vega SDK

**Metro bundler connection issues**
- Verify Metro is running: `yarn start`
- Check firewall settings
- Ensure device and dev machine on same network

## Navigation Issues

- Verify React Navigation installation
- Check focus restoration logic
- Test with D-pad/arrow keys only
- Enable spatial navigation debug mode

## Video Playback Issues

- Verify video URL accessibility
- Check video format compatibility (MP4 recommended)
- Test with different video codecs
- Monitor network bandwidth

---

# Additional Resources

## Sample Repositories

**React Native Multi-TV App Sample**
- Repository: https://github.com/AmazonAppDev/react-native-multi-tv-app-sample
- Complete monorepo setup
- Working implementations for all platforms
- Reference for best practices

## Official Documentation

**Expo TV Documentation**
- System requirements and prerequisites
- Quick start with TV templates
- EAS Build profiles for TV
- Platform-specific build instructions

**Vega SDK Documentation**
- Installation guide
- Vega CLI guide
- Device setup
- Deployment to Amazon Appstore

## External Resources

- [React Native TV (react-native-tvos)](https://github.com/react-native-tvos/react-native-tvos)
- [React TV Space Navigation](https://github.com/bamlab/react-tv-space-navigation)
- [Expo Examples - TV](https://github.com/expo/examples/tree/master/with-tv)
- [Expo Examples - TV Router](https://github.com/expo/examples/tree/master/with-router-tv)
- [React Navigation](https://reactnavigation.org/)
- [React Native Directory](https://reactnative.directory/?tvos=true)

---

# Adding New Features

## New Shared Component

1. Create in `packages/shared-ui/src/components/ComponentName.tsx`
2. Export from `packages/shared-ui/src/index.ts`
3. Import in apps: `import { ComponentName } from '@project/shared-ui'`

## Platform-Specific Implementation

1. Create base file: `Feature.base.ts`
2. Create platform files: `Feature.android.ts`, `Feature.ios.ts`, `Feature.kepler.ts`
3. Metro automatically resolves correct file at build time

## New Screen

1. Create in `packages/shared-ui/src/screens/ScreenName.tsx`
2. Add to navigation in `navigation/AppNavigator.tsx`
3. Export from `packages/shared-ui/src/index.ts`
4. Use in app's navigation configuration

---

# Next Steps

## Recommended Path (Quick Start)

1. **Clone the repository** - `git clone https://github.com/AmazonAppDev/react-native-multi-tv-app-sample.git`
2. **Install dependencies** - `yarn install && yarn bootstrap`
3. **Review the codebase**
4. **Review documentation**
5. **Review steering files**
6. **Configure for Expo TV**
7. **Install Vega SDK** (optional)
8. **Test on platforms**
9. **Customize for your project**
10. **Deploy**

## Alternative Path (Build from Scratch)

Follow the step-by-step "Build from Scratch" guide above to understand:
- Monorepo setup with Yarn workspaces
- Expo TV configuration
- Vega SDK integration
- Shared component library architecture
- Platform-specific file resolution
- Theme system implementation
- Spatial navigation setup
- Remote control integration

---

**For detailed implementation guides, see:**
- `multi-tv-builder/POWER.md` - Complete implementation guide
- `multi-tv-builder/steering/product.md` - Product overview
- `multi-tv-builder/steering/structure.md` - Project structure details
- `multi-tv-builder/steering/tech.md` - Technology stack reference
- `multi-tv-builder/steering/VEGA_TO_MONOREPO_MIGRATION_GUIDE.md` - Migration guide
