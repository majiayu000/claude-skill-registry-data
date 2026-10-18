---
name: mobile-ci-cd
description: "Automate mobile app build, test, and deployment pipelines for iOS and Android using Fastlane, EAS Build, or GitHub Actions."
category: mobile
tags: [ci-cd, mobile, fastlane, eas-build, github-actions, deployment]
complexity: advanced
risk: low
compatibility: [claude-code, antigravity, gemini-cli, cursor, copilot, codex-cli, autohand, kiro]
source: antigravity-official
version: "1.0.0"
date_added: "2026-07-10"
last_updated: "2026-07-10"
---

# Mobile CI/CD Engineer

## Purpose
Establish automated CI/CD pipelines for mobile applications that build, test, and deploy to stores without manual intervention.

## Pipeline Architecture

### Option A: EAS Build + Submit (React Native/Expo)
```json
// eas.json
{
  "cli": { "version": ">= 10.0.0" },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": { "simulator": true }
    },
    "preview": {
      "distribution": "internal",
      "ios": { "resourceClass": "m-medium" },
      "android": { "buildType": "apk" }
    },
    "production": {
      "ios": { "resourceClass": "m-medium" },
      "android": { "buildType": "aab" }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "apple@example.com",
        "ascAppId": "1234567890"
      },
      "android": {
        "serviceAccountKeyPath": "./play-service-account.json",
        "track": "internal"
      }
    }
  }
}
```

```yaml
# .github/workflows/mobile-ci.yml
name: Mobile CI/CD
on:
  push:
    branches: [main]
    tags: ['v*']

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      - run: npm test -- --ci --coverage

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm
      - run: npm ci
      
      - name: Setup EAS
        uses: expo/expo-github-action@v8
        with:
          eas-version: latest
          token: ${{ secrets.EXPO_TOKEN }}
      
      - name: Build for all platforms
        run: eas build --platform all --profile production --non-interactive
      
      - name: Submit to stores
        if: startsWith(github.ref, 'refs/tags/v')
        run: eas submit --platform all --profile production --non-interactive
```

### Option B: Fastlane (Native iOS/Android)
```ruby
# Fastfile
before_all do |lane, options|
  ensure_git_status_clean
end

platform :ios do
  lane :test do
    run_tests(scheme: "MyApp", devices: ["iPhone 15 Pro"])
  end

  lane :beta do |options|
    increment_build_number
    build_app(scheme: "MyApp", export_method: "app-store")
    upload_to_testflight(
      skip_waiting_for_build_processing: true,
      changelog: options[:changelog] || git_commit_message
    )
    slack(message: "New iOS beta build uploaded to TestFlight!")
  end

  lane :release do
    deliver(submit_for_review: true, automatic_release: false)
  end
end

platform :android do
  lane :beta do
    gradle(task: "bundle", build_type: "Release")
    upload_to_play_store(track: "internal")
  end
end
```

### Version Management
```bash
# Automated version bumping
npx standard-version --release-as minor    # 1.0.0 → 1.1.0
npx standard-version --release-as patch    # 1.0.0 → 1.0.1

# For React Native: sync version across platforms
# package.json version → android versionName → iOS CFBundleShortVersionString
```

## Outputs
1. EAS Build / Fastlane configuration
2. GitHub Actions workflow
3. Version management strategy
4. Environment configuration for dev/staging/prod
5. Store submission automation
6. Slack/notification integration
