---
name: analytics
description: Analytics and crash reporting with Firebase Analytics, Crashlytics, Sentry, or PostHog. Event tracking, user properties, screen views, crash reports, error logging. Plug-and-play provider architecture. Use when implementing analytics, crash reporting, or switching providers.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebFetch
---

# Analytics & Crash Reporting

Track user behavior, monitor app health, and debug production issues. Supports multiple providers with a plug-and-play architecture.

## When to Use This Skill

- Adding analytics to a Flutter app
- Setting up crash/error reporting
- Implementing custom event tracking
- Switching analytics providers
- User asks "add analytics", "track events", "crash reporting", "Sentry", or "PostHog"

## Questions to Ask

1. **Analytics provider:** Firebase Analytics (default), PostHog, or Mixpanel?
2. **Error tracking provider:** Firebase Crashlytics (default) or Sentry?
3. **Analytics scope:** Full analytics (events + properties + screens) or just crash reporting?
4. **Custom events:** What key user actions need tracking? (purchases, signups, feature usage)
5. **Privacy:** GDPR/CCPA compliance needed? User consent flow required?

## Provider Quick Reference

| Need | Recommended | Why |
|------|-------------|-----|
| **Just get started** | Firebase | Free, easy setup |
| **Better product analytics** | PostHog | Funnels, retention, session replay |
| **Better error tracking** | Sentry | Superior debugging |
| **Data ownership** | PostHog (self-hosted) | Your servers |

**See:** [providers-guide.md](providers-guide.md) for detailed comparison.

## Reference Files

- `reference/services/` - Provider-agnostic interface + implementations (Firebase, Sentry, PostHog)
- `reference/repositories/` - Domain interface + implementations
- `reference/providers/` - Riverpod state management
- `reference/failures/` - Sealed Failure types
- `reference/utils/` - Route observer, consent helpers

## Workflow

### Phase 1: Choose Providers
1. Select analytics provider (Firebase Analytics / PostHog / Mixpanel)
2. Select error tracking provider (Crashlytics / Sentry)
3. Add dependencies to `pubspec.yaml`

### Phase 2: Platform Config
**Firebase:**
- Add `GoogleService-Info.plist` (iOS) and `google-services.json` (Android)
- Configure dSYM upload for Crashlytics

**Sentry:**
- Get DSN from Sentry dashboard
- Configure sentry-cli for dSYM upload

**PostHog:**
- Get API key from PostHog dashboard
- Optional: Configure self-hosted URL

### Phase 3: Implementation
1. Copy provider-agnostic interface + chosen implementations
2. Initialize services in `main.dart`
3. Wire up Riverpod providers
4. Add screen tracking via router observer
5. Implement event tracking for key actions
6. Test error reporting

## Core API (Provider-Agnostic)

```dart
final analytics = ref.read(analyticsServiceProvider);
final errorTracking = ref.read(errorTrackingServiceProvider);
await analytics.logEvent(name: 'purchase_completed', parameters: {'item_id': 'sku_123'});
await analytics.setUserProperty(name: 'tier', value: 'premium');
await analytics.logScreenView(screenName: 'HomeScreen');
await errorTracking.recordError(error, stackTrace, reason: 'API failed');
await errorTracking.addBreadcrumb('User tapped checkout');
```

## Dependencies by Provider

**Firebase (default):**
```yaml
dependencies:
  firebase_core: ^3.9.0
  firebase_analytics: ^11.4.0
  firebase_crashlytics: ^4.3.0
```

**Sentry:**
```yaml
dependencies:
  sentry_flutter: ^8.12.0
```

**PostHog:**
```yaml
dependencies:
  posthog_flutter: ^4.0.0
```

**Mixed (PostHog + Sentry):**
```yaml
dependencies:
  posthog_flutter: ^4.0.0
  sentry_flutter: ^8.12.0
```

## Swapping Providers

Change the provider in Riverpod to swap implementations:

```dart
@riverpod
ProductAnalyticsService analyticsService(Ref ref) => FirebaseAnalyticsService.instance;
// Alternative: PostHogAnalyticsService.instance

@riverpod
ErrorTrackingService errorTrackingService(Ref ref) => FirebaseCrashlyticsService.instance;
// Alternative: SentryErrorTrackingService.instance
```

## Guides

| File | Content |
|------|---------|
| [providers-guide.md](providers-guide.md) | Provider comparison & selection |
| [implementation-guide.md](implementation-guide.md) | Step-by-step code setup |
| [firebase-setup-guide.md](firebase-setup-guide.md) | Firebase Console configuration |
| [local-setup-guide.md](local-setup-guide.md) | Xcode Build Phase setup for dSYMs |
| [checklist.md](checklist.md) | Verification checklist |

**For CI/CD integration:** See `/ci-cd` skill → `debug-symbols-guide.md`

## Checklist

**Core:**
- [ ] Provider selected (analytics + error tracking)
- [ ] Dependencies added to pubspec.yaml
- [ ] Services initialized in main.dart
- [ ] FlutterError.onError configured
- [ ] PlatformDispatcher.instance.onError configured
- [ ] Screen tracking via router observer
- [ ] Key events tracked
- [ ] User ID set on login/logout

**Firebase-specific:**
- [ ] `GoogleService-Info.plist` added
- [ ] `google-services.json` added
- [ ] dSYM upload script in Xcode Build Phases

**Sentry-specific:**
- [ ] SENTRY_DSN configured
- [ ] sentry-cli installed for dSYM upload
- [ ] Release/environment configured

**PostHog-specific:**
- [ ] POSTHOG_API_KEY configured
- [ ] Host URL set (if self-hosted)

## Related Skills

- `/push-notifications` - Firebase project setup (shared)
- `/release` - iOS build phases, Android signing
- `/ci-cd` - dSYM upload automation
- `/design` - Consent dialogs, settings UI
- `/i18n` - Localized consent text
- `/testing` - Mock analytics for tests
