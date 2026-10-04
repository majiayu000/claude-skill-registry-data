---
name: deep-linking
description: Deep linking with Universal Links (iOS) and App Links (Android). Platform setup, domain verification, GoRouter integration, path-based routing. Use when implementing deep links, URL handling, or app-to-web navigation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebFetch
---

# Deep Linking - Universal Links & App Links

Deep linking setup for iOS (Universal Links) and Android (App Links) with GoRouter integration.

## When to Use This Skill

- Adding deep link support to a Flutter app
- Configuring Universal Links for iOS
- Configuring App Links for Android
- Handling custom URL schemes
- Integrating deep links with GoRouter
- User asks "add deep linking", "universal links", "app links", or "URL handling"

## Questions to Ask

1. **Domain:** What domain will host the deep links? (e.g., `example.com`)
2. **Paths:** Which paths should open the app? (e.g., `/products/*`, `/users/*`)
3. **Custom scheme:** Need a custom URL scheme fallback? (e.g., `myapp://`)
4. **Environments:** Multiple domains? (e.g., staging.example.com, example.com)
5. **Backend access:** Can you host `.well-known` files on the server?

## Reference Files

- `reference/router/deep_link_handler.dart` - GoRouter deep link config
- `templates/ios/Runner.entitlements` - Associated Domains
- `templates/android/android_manifest_deeplinks.xml` - Intent filters

**See:** [implementation-guide.md](implementation-guide.md) for complete setup.

## Workflow

### Phase 1: Domain Verification

1. Create `apple-app-site-association` file (see ios-guide.md)
2. Create `assetlinks.json` file (see android-guide.md)
3. Host files at `https://domain.com/.well-known/`
4. Verify HTTPS and correct MIME types

### Phase 2: iOS Configuration

1. Add Associated Domains capability in Xcode
2. Add domain to `Runner.entitlements`
3. Handle links in AppDelegate (if needed)

### Phase 3: Android Configuration

1. Add intent filters to `AndroidManifest.xml`
2. Set `autoVerify="true"` for App Links
3. Generate and add SHA-256 fingerprint to `assetlinks.json`

### Phase 4: GoRouter Integration

1. Configure `GoRouter` with deep link paths
2. Add route parameter extraction
3. Handle unknown deep links gracefully
4. Test with `adb` and `xcrun` commands

## Core API

```dart
// GoRouter handles deep links automatically
GoRouter(routes: [
  GoRoute(path: '/products/:id', builder: (context, state) =>
    ProductScreen(productId: state.pathParameters['id']!)),
]);
// Manual: GoRouter.of(context).go(Uri.parse(deepLink).path);
```

## URL Types

| Type | iOS | Android | Format |
|------|-----|---------|--------|
| **Universal/App Links** | Yes | Yes | `https://domain.com/path` |
| **Custom Scheme** | Yes | Yes | `myapp://path` |
| **Firebase Dynamic Links** | Deprecated | Deprecated | Use Universal/App Links |

## Domain Verification Files

### iOS: apple-app-site-association

Host at: `https://domain.com/.well-known/apple-app-site-association`

```json
{
  "applinks": {
    "apps": [],
    "details": [{
      "appID": "TEAM_ID.com.example.app",
      "paths": ["/products/*", "/users/*"]
    }]
  }
}
```

### Android: assetlinks.json

Host at: `https://domain.com/.well-known/assetlinks.json`

```json
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.example.app",
    "sha256_cert_fingerprints": ["SHA256_FINGERPRINT"]
  }
}]
```

## Platform Requirements

### iOS

- Associated Domains capability enabled
- HTTPS domain with valid certificate
- `apple-app-site-association` file accessible (no redirects)
- MIME type: `application/json`

### Android

- Intent filters with `autoVerify="true"`
- SHA-256 fingerprints (debug, release, Play Store)
- `assetlinks.json` file accessible
- MIME type: `application/json`

## Testing Commands

```bash
xcrun simctl openurl booted "https://example.com/products/123"  # iOS
adb shell am start -a android.intent.action.VIEW -d "https://example.com/products/123" com.example.app
adb shell pm get-app-links com.example.app                      # Verify Android
curl -I https://example.com/.well-known/apple-app-site-association
```

## Guides

| File | Content |
|------|---------|
| [ios-guide.md](ios-guide.md) | Universal Links, Associated Domains, AASA file |
| [android-guide.md](android-guide.md) | App Links, Intent Filters, Digital Asset Links |
| [implementation-guide.md](implementation-guide.md) | GoRouter integration, path handling |
| [checklist.md](checklist.md) | Verification checklist |

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| iOS link opens Safari | AASA not found | Check `.well-known` path and MIME type |
| Android shows app chooser | `autoVerify` failed | Verify `assetlinks.json` and SHA-256 |
| Path not matched | Wrong pattern | Check path patterns in AASA/router |
| Works in dev, not prod | Wrong fingerprint | Add release/Play Store SHA-256 |

## Checklist

- [ ] Domain supports HTTPS with valid certificate
- [ ] `apple-app-site-association` hosted at `.well-known/`
- [ ] `assetlinks.json` hosted at `.well-known/`
- [ ] iOS: Associated Domains capability added in Xcode
- [ ] iOS: Domain added to `Runner.entitlements`
- [ ] Android: Intent filters added to `AndroidManifest.xml`
- [ ] Android: All SHA-256 fingerprints in `assetlinks.json`
- [ ] GoRouter configured with deep link paths
- [ ] Deep links tested on both platforms
- [ ] Unknown paths handled gracefully

## Related Skills

- `/core` - GoRouter setup (run first)
- `/push-notifications` - Deep links from notifications
- `/release` - iOS capabilities, Android signing
- `/testing` - Deep link integration tests
