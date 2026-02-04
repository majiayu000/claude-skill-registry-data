---
name: eas-update-setup
description: EAS Update for OTA updates. Use when setting up over-the-air updates.
---

# EAS Update Setup Skill

This skill covers EAS Update for over-the-air (OTA) updates in React Native apps.

## When to Use

Use this skill when:
- Setting up OTA updates
- Managing update channels
- Rolling back updates
- A/B testing with updates

## Core Principle

**INSTANT UPDATES** - Ship JavaScript changes without app store review.

## What Can Be Updated OTA

```
✅ CAN update OTA:
- JavaScript code
- TypeScript code
- Assets (images, fonts)
- Styling changes
- New screens/components
- Bug fixes in JS

❌ CANNOT update OTA:
- Native code changes
- New native modules
- Native dependencies
- App permissions
- Build configuration
```

## Installation

```bash
# Install expo-updates
npx expo install expo-updates

# Configure EAS Update
eas update:configure
```

## Basic Configuration

```json
// eas.json
{
  "build": {
    "preview": {
      "channel": "preview"
    },
    "production": {
      "channel": "production"
    }
  }
}
```

```typescript
// app.config.ts
export default {
  expo: {
    // ...other config
    updates: {
      url: 'https://u.expo.dev/your-project-id',
      fallbackToCacheTimeout: 0,
    },
    runtimeVersion: {
      policy: 'appVersion',
    },
  },
};
```

## Runtime Version Strategies

```typescript
// app.config.ts

// Option 1: Based on app version (recommended for most apps)
export default {
  expo: {
    runtimeVersion: {
      policy: 'appVersion', // Uses version from app.json
    },
  },
};

// Option 2: Based on SDK version
export default {
  expo: {
    runtimeVersion: {
      policy: 'sdkVersion',
    },
  },
};

// Option 3: Based on native code fingerprint
export default {
  expo: {
    runtimeVersion: {
      policy: 'fingerprint',
    },
  },
};

// Option 4: Manual version
export default {
  expo: {
    runtimeVersion: '1.0.0',
  },
};
```

## Publishing Updates

```bash
# Publish to preview channel
eas update --channel preview --message "Fix login bug"

# Publish to production channel
eas update --channel production --message "Release 1.2.1 hotfix"

# Publish specific branch
eas update --branch main --message "Latest changes"

# Publish with auto-generated message
eas update --channel production --auto
```

## Update Channels & Branches

```bash
# Create a new branch
eas branch:create staging

# Map channel to branch
eas channel:create staging
eas channel:edit staging --branch staging

# View channels
eas channel:list

# View branches
eas branch:list

# Roll back to previous update
eas channel:rollback production
```

## Programmatic Update Checking

```typescript
import * as Updates from 'expo-updates';

// Check for updates on app start
async function checkForUpdates() {
  try {
    const update = await Updates.checkForUpdateAsync();

    if (update.isAvailable) {
      await Updates.fetchUpdateAsync();
      await Updates.reloadAsync();
    }
  } catch (error) {
    console.error('Error checking for updates:', error);
  }
}

// Use in app entry
useEffect(() => {
  if (!__DEV__) {
    checkForUpdates();
  }
}, []);
```

## Update Hook Pattern

```typescript
import { useEffect, useState } from 'react';
import * as Updates from 'expo-updates';

interface UpdateState {
  isChecking: boolean;
  isAvailable: boolean;
  isDownloading: boolean;
  error: Error | null;
  checkForUpdate: () => Promise<void>;
  downloadAndRestart: () => Promise<void>;
}

export function useUpdates(): UpdateState {
  const [isChecking, setIsChecking] = useState(false);
  const [isAvailable, setIsAvailable] = useState(false);
  const [isDownloading, setIsDownloading] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const checkForUpdate = async () => {
    if (__DEV__) return;

    setIsChecking(true);
    setError(null);

    try {
      const update = await Updates.checkForUpdateAsync();
      setIsAvailable(update.isAvailable);
    } catch (e) {
      setError(e as Error);
    } finally {
      setIsChecking(false);
    }
  };

  const downloadAndRestart = async () => {
    if (!isAvailable) return;

    setIsDownloading(true);
    try {
      await Updates.fetchUpdateAsync();
      await Updates.reloadAsync();
    } catch (e) {
      setError(e as Error);
      setIsDownloading(false);
    }
  };

  // Check on mount
  useEffect(() => {
    checkForUpdate();
  }, []);

  return {
    isChecking,
    isAvailable,
    isDownloading,
    error,
    checkForUpdate,
    downloadAndRestart,
  };
}
```

## Update Banner Component

```typescript
import { useUpdates } from '@/hooks/useUpdates';

export function UpdateBanner(): React.ReactElement | null {
  const { isAvailable, isDownloading, downloadAndRestart } = useUpdates();

  if (!isAvailable) return null;

  return (
    <View className="bg-blue-600 px-4 py-3 flex-row items-center justify-between">
      <Text className="text-white">A new version is available</Text>
      <TouchableOpacity
        onPress={downloadAndRestart}
        disabled={isDownloading}
        className="bg-white px-4 py-2 rounded"
      >
        <Text className="text-blue-600 font-semibold">
          {isDownloading ? 'Updating...' : 'Update Now'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}
```

## Background Updates

```typescript
// app.config.ts
export default {
  expo: {
    updates: {
      url: 'https://u.expo.dev/your-project-id',
      checkAutomatically: 'ON_LOAD', // or 'ON_ERROR_RECOVERY', 'NEVER'
      fallbackToCacheTimeout: 0, // 0 = use cache, don't wait
    },
  },
};
```

## Update Events

```typescript
import * as Updates from 'expo-updates';

useEffect(() => {
  const subscription = Updates.addListener((event) => {
    if (event.type === Updates.UpdateEventType.UPDATE_AVAILABLE) {
      // New update downloaded
      Alert.alert(
        'Update Available',
        'A new version has been downloaded. Restart to apply?',
        [
          { text: 'Later', style: 'cancel' },
          { text: 'Restart', onPress: () => Updates.reloadAsync() },
        ]
      );
    } else if (event.type === Updates.UpdateEventType.ERROR) {
      // Update error
      console.error('Update error:', event.message);
    }
  });

  return () => subscription.remove();
}, []);
```

## CI/CD Integration

```yaml
# .github/workflows/eas-update.yml
name: EAS Update

on:
  push:
    branches: [main, staging]

jobs:
  update:
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

      - name: Publish update
        run: |
          if [ "${{ github.ref }}" == "refs/heads/main" ]; then
            eas update --channel production --auto --non-interactive
          else
            eas update --channel staging --auto --non-interactive
          fi
```

## Rollback Strategy

```bash
# View update history
eas update:list --channel production

# Rollback to previous update
eas channel:rollback production

# Rollback to specific update
eas channel:edit production --branch <branch-name>
```

## A/B Testing with Channels

```bash
# Create experiment channels
eas channel:create production-control
eas channel:create production-variant

# Deploy different versions
eas update --channel production-control --message "Control version"
eas update --channel production-variant --message "Variant A"

# Route users to channels based on criteria
```

## Debug Updates

```typescript
import * as Updates from 'expo-updates';

// Get current update info
console.log('Channel:', Updates.channel);
console.log('Runtime Version:', Updates.runtimeVersion);
console.log('Update ID:', Updates.updateId);
console.log('Created At:', Updates.createdAt);
console.log('Is Embedded Launch:', Updates.isEmbeddedLaunch);
```

## Monitoring

```bash
# View update analytics
eas update:list --channel production --limit 10

# View update details
eas update:view <update-id>
```

## Notes

- OTA updates only work for JS/assets, not native code
- Test updates in preview before production
- Use meaningful update messages for tracking
- Set up CI/CD for automated deployments
- Consider user experience for mandatory vs. optional updates
- Monitor update success rates
- Have a rollback plan ready
