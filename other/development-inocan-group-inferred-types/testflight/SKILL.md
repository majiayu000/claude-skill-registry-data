---
name: testflight
description: TestFlight and App Store distribution guide. Use when preparing app for TestFlight, creating production builds, or submitting to App Store Connect.
---

# TestFlight & App Store Distribution

## Prerequisites

- Apple Developer Program membership ($99/year)
- Xcode installed
- EAS CLI installed: `npm install -g eas-cli`
- Expo account: `eas login`

## Build Profiles (eas.json)

```json
{
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal"
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "simulator": false
      }
    },
    "production": {
      "ios": {
        "buildConfiguration": "Release"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-apple-id@example.com",
        "ascAppId": "your-app-store-connect-app-id"
      }
    }
  }
}
```

## Environment Variables for Production

```bash
# mobile/.env.production
EXPO_PUBLIC_SIGNALING_SERVER_URL=https://webrtc-signaling-xxxx.onrender.com
```

## Build Commands

```bash
cd mobile

# Configure EAS (first time)
eas build:configure

# Development build (for testing)
eas build --platform ios --profile development

# Preview build (internal distribution)
eas build --platform ios --profile preview

# Production build (App Store)
eas build --platform ios --profile production

# Submit to App Store Connect
eas submit --platform ios --latest
```

## TestFlight Distribution Steps

1. **Create Production Build**
   ```bash
   eas build --platform ios --profile production
   ```

2. **Submit to App Store Connect**
   ```bash
   eas submit --platform ios
   ```

3. **Configure in App Store Connect**
   - Go to https://appstoreconnect.apple.com
   - Select app → TestFlight tab
   - Wait for build processing (5-30 minutes)
   - Add test information if required

4. **Add Testers**
   - Internal testers: Up to 100 (Apple Developer team members)
   - External testers: Up to 10,000 (requires brief review)

5. **Tester Installation**
   - Testers receive email invitation
   - Install TestFlight app from App Store
   - Open invitation link → Install app

## App Store Submission Checklist

- [ ] App icons (all required sizes)
- [ ] Screenshots for required device sizes
- [ ] App description and keywords
- [ ] Privacy policy URL
- [ ] Support URL
- [ ] Age rating questionnaire
- [ ] Export compliance information
- [ ] Production environment variables set

## Common Issues

| Issue | Solution |
|-------|----------|
| Build fails with signing error | Check Apple Developer certificates in Xcode |
| "Missing compliance" | Complete export compliance in App Store Connect |
| Build stuck in processing | Wait up to 30 minutes, or rebuild |
| TestFlight invite not received | Check spam folder, verify email address |

## EAS Build Troubleshooting

### npm workspaces との競合

**問題**: `npm ci can only install packages when your package.json and package-lock.json are in sync`

**原因**: npm workspacesを使用しているモノレポ構成では、子ディレクトリ（mobile/）に独立したpackage-lock.jsonが生成されない。EAS Buildは`npm ci`を使用するため、package-lock.jsonが必要。

**解決方法**:
```json
// root package.json - mobile を workspaces から除外
{
  "workspaces": [
    "web",
    "server"
    // "mobile" を削除
  ]
}
```

その後、mobile/ で独立した package-lock.json を生成:
```bash
cd mobile
rm -rf node_modules package-lock.json
npm install
```

### ⚠️ TestFlight アプリが起動直後にクラッシュする（最重要）

**症状**: EAS Build は成功、App Store Connect に提出成功、TestFlight からインストール成功、しかしアプリを開くと即座にクラッシュ。

**原因**: Expo SDK 54 と互換性のない依存関係バージョンを使用している。

**確認方法**:
```bash
npx expo install --check
```

**解決方法**: 以下のバージョンに厳密に合わせる:
```json
{
  "dependencies": {
    "react": "19.1.0",
    "react-dom": "19.1.0",
    "react-native-gesture-handler": "~2.28.0",
    "react-native-safe-area-context": "~5.6.0",
    "react-native-screens": "~4.16.0"
  }
}
```

**注意**: `react@19.2.1` など推奨より新しいバージョンを使うと、開発ビルドでは動作するが**本番ビルドでクラッシュ**する。

バージョン修正後:
```bash
rm -rf node_modules package-lock.json
npm install
eas build --platform ios --profile production
```

### expo-router のピア依存関係

**問題**: `Unable to find a specification for RNScreens depended upon by ExpoHead`

**原因**: expo-router は react-native-screens などのピア依存関係を必要とするが、明示的にインストールされていない。

**解決方法**: mobile/package.json に以下を追加:
```json
{
  "dependencies": {
    "react-native-gesture-handler": "~2.28.0",
    "react-native-safe-area-context": "~5.6.0",
    "react-native-screens": "~4.16.0"
  }
}
```

### Xcode 16 / iOS SDK 26 互換性

**問題**: `no member named 'move' in namespace 'std'` (RNSScreenStackHeaderConfig.mm)

**原因**: react-native-screens の古いバージョンは Xcode 16 / iOS SDK 26 と互換性がない。

**解決方法**: react-native-screens を ~4.16.0 以上にアップグレード:
```bash
npx expo install react-native-screens
```

### 推奨 eas.json 設定

```json
{
  "build": {
    "production": {
      "env": {
        "EXPO_PUBLIC_SIGNALING_SERVER_URL": "https://your-server.com",
        "NPM_CONFIG_LEGACY_PEER_DEPS": "true"
      },
      "node": "22.12.0"
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your-apple-id@example.com",
        "appleTeamId": "YOUR_TEAM_ID"
      }
    }
  }
}
```

### ビルド成功のためのチェックリスト

- [ ] `npx expo install --check` でバージョン互換性を確認
- [ ] react が 19.1.0（19.2.x はクラッシュの原因）
- [ ] mobile が npm workspaces から除外されている
- [ ] mobile/ に独立した package-lock.json がある
- [ ] expo-router のピア依存関係がインストールされている
- [ ] eas.json に appleTeamId が設定されている
- [ ] Info.plist に必要な権限が設定されている（下記参照）

### Info.plist の必須権限（App Store 提出用）

```json
// app.json の ios.infoPlist
{
  "NSMicrophoneUsageDescription": "音声通話のためにマイクを使用します",
  "NSSpeechRecognitionUsageDescription": "音声を文字に変換するために使用します",
  "NSPhotoLibraryUsageDescription": "プロフィール画像の設定に使用します",
  "NSCameraUsageDescription": "ビデオ通話のためにカメラを使用します",
  "ITSAppUsesNonExemptEncryption": false
}
```

**注意**: これらがないと App Store Connect が自動拒否 (ITMS-90683) します。

## Important Notes

- TestFlight builds expire after 90 days
- Each new build requires incrementing version or build number
- External testers require Apple review (usually 24-48 hours)
- Keep production signaling server running on Render
