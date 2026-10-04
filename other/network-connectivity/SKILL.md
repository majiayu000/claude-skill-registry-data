---
name: network-connectivity
description: Network connectivity monitoring with global offline banner. Uses connectivity_plus with smart detection that considers actual API success. Use when adding offline detection, network monitoring, or connectivity-aware UI.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Network Connectivity

Global network connectivity monitoring with automatic offline banner display. Uses smart detection that combines `connectivity_plus` status with actual API request success to avoid false negatives from government blocks or captive portals.

## When to Use This Skill

- Adding network connectivity monitoring to an app
- Implementing a global offline banner/indicator
- Setting up connectivity-aware features
- User asks "offline banner", "network status", "connectivity monitoring"

## When NOT to Use This Skill

- **Error handling for failed API calls** - Use `/data` which has `NetworkFailure` types
- **Retry logic** - Handled in repository layer via `/data` patterns
- **Offline data caching** - Use `/data` caching patterns
- **NetworkFailure types** - Already in `/core` errors/failures.dart

## Quick Reference

### Dependencies

```yaml
dependencies:
  connectivity_plus: ^6.0.0
```

### Core Components

| Component | Purpose |
|-----------|---------|
| `ConnectivityService` | Wraps connectivity_plus, provides stream |
| `ActualConnectivity` | Smart notifier combining library + API success |
| `ConnectivityInterceptor` | Dio interceptor reporting request success |
| `ConnectivityBanner` | Global overlay widget for offline banner |
| `ConnectivityWrapper` | Root widget that manages banner display |

### Smart Detection

The `connectivity_plus` library can report false negatives when:
- Government blocks connectivity check endpoints
- Captive portals intercept requests
- DNS issues affect only certain domains

**Solution:** If any real API request succeeds, override "offline" status.

| Scenario | Library Says | API Result | Actual Status |
|----------|--------------|------------|---------------|
| Normal online | online | success | **online** |
| Normal offline | offline | fails | **offline** |
| Blocked endpoints | offline | success | **online** |
| Captive portal | online | fails | online (until timeout) |

### Connectivity States

| State | Meaning | UI Action |
|-------|---------|-----------|
| `wifi` | Connected via WiFi | Hide banner |
| `mobile` | Connected via mobile data | Hide banner |
| `ethernet` | Connected via ethernet | Hide banner |
| `none` | No connectivity | Show banner |

## Workflow

### Phase 1: Add Dependencies

1. Add `connectivity_plus` to `pubspec.yaml`
2. Run `flutter pub get`

### Phase 2: Create Core Files

1. Create `ConnectivityService` in `lib/core/services/`
2. Create `connectivityProvider` in `lib/core/providers/`
3. Create `ConnectivityBanner` widget in `lib/core/widgets/`
4. Create `ConnectivityInterceptor` in `lib/core/network/`

### Phase 3: Integrate

1. Wrap `MaterialApp` with `ConnectivityWrapper`
2. Add `ConnectivityInterceptor` to Dio interceptors
3. Register provider in dependency injection

### Phase 4: Verify

```bash
dart run .claude/skills/network-connectivity/scripts/check.dart
```

## File Structure

After running this skill:

```
lib/
├── core/
│   ├── services/
│   │   └── connectivity_service.dart
│   ├── providers/
│   │   └── connectivity_provider.dart
│   ├── network/
│   │   └── connectivity_interceptor.dart
│   └── widgets/
│       ├── connectivity_banner.dart
│       └── connectivity_wrapper.dart
└── main.dart  # Updated with ConnectivityWrapper
```

## Core API

```dart
// Watch connectivity status (recommended)
final isOnline = ref.watch(isOnlineProvider);

// Report successful request (in Dio interceptor)
ref.read(actualConnectivityProvider.notifier).reportRequestSuccess();
```

**See:** [setup-guide.md](setup-guide.md) for Dio integration and advanced usage.

## Guides

| File | Content |
|------|---------|
| [setup-guide.md](setup-guide.md) | Step-by-step integration guide |

## Reference Files

**See:** `reference/` for complete implementations:

- `reference/connectivity_service.dart` - Service wrapping connectivity_plus
- `reference/connectivity_provider.dart` - Smart providers with API success tracking
- `reference/connectivity_interceptor.dart` - Dio interceptor for request reporting
- `reference/connectivity_banner.dart` - Banner widget implementation
- `reference/connectivity_wrapper.dart` - Root wrapper widget

## Checklist

**Dependencies:**
- [ ] `connectivity_plus: ^6.0.0` added to pubspec.yaml
- [ ] `flutter pub get` run successfully

**Core Files:**
- [ ] `ConnectivityService` created in `lib/core/services/`
- [ ] `connectivityProvider` created in `lib/core/providers/`
- [ ] `ConnectivityInterceptor` created in `lib/core/network/`
- [ ] `ConnectivityBanner` widget created in `lib/core/widgets/`
- [ ] `ConnectivityWrapper` widget created in `lib/core/widgets/`

**Integration:**
- [ ] `MaterialApp` wrapped with `ConnectivityWrapper`
- [ ] `ConnectivityInterceptor` added to Dio
- [ ] Banner displays when airplane mode enabled

**Testing:**
- [ ] Toggle airplane mode - banner appears/disappears
- [ ] App launch in offline mode - banner visible
- [ ] No performance issues from stream subscription

## Related Skills

- `/core` - Creates core infrastructure where connectivity files live
- `/data` - NetworkFailure types for API errors, retry interceptors

## Common Issues

### Banner not showing

Ensure `ConnectivityWrapper` is above `MaterialApp` in widget tree:

```dart
ConnectivityWrapper(
  child: MaterialApp(...),
)
```

### Multiple subscriptions

Use `ref.watch` instead of creating new subscriptions. The provider handles cleanup automatically.

### iOS simulator connectivity

iOS simulator may report incorrect connectivity. Test on real device for accurate results.

### False offline in certain countries

If connectivity_plus reports offline but API requests work, ensure `ConnectivityInterceptor` is added to Dio. The interceptor reports successful requests which overrides false negatives.

## Next Steps

After running this skill:
1. Test by toggling airplane mode
2. Run `/i18n` for localization
3. Run `/design` for UI polish
