---
name: maestro-flutter
description: |
  Maestro E2E testing knowledge for Flutter apps.
  YAML-based flows, TestKeys, visual regression, Maestro MCP integration.
  Background knowledge for QE E2E testing phase.
user-invocable: false
---

# Maestro Flutter E2E Testing Guide

## Reference Guide

| Topic | Reference | Use When |
|-------|-----------|----------|
| Flow Patterns | `references/flow-patterns.md` | Writing YAML flows, Flutter-specific tips |
| CI & Visual Regression | `references/ci-visual-regression.md` | CI/CD setup, visual comparison, troubleshooting |

## Core Principles

1. **ADD semantic labels** — `Key()` / `Semantics` on all interactive widgets
2. **WRITE flows in YAML** — simple, readable, no code
3. **RUN on emulator first**, then real devices
4. **CAPTURE screenshots** at key assertion points
5. **USE visual regression** for Pixel Perfect validation

## TestKeys Pattern (MANDATORY)

```dart
// lib/core/constants/test_keys.dart
abstract class TestKeys {
  static const emailField = Key('email_field');
  static const passwordField = Key('password_field');
  static const loginButton = Key('login_button');
  static const registerButton = Key('register_button');
  static const homeTab = Key('home_tab');
  static const profileTab = Key('profile_tab');
  static const loadingIndicator = Key('loading_indicator');
  static const errorMessage = Key('error_message');
}
```

## Project Structure

```
.maestro/
├── config.yaml
└── flows/
    ├── auth/
    │   ├── login.yaml
    │   └── register.yaml
    ├── {feature}/
    │   └── {action}.yaml
    └── smoke_test.yaml
```

## Flow YAML Syntax

```yaml
appId: com.example.myapp
name: User Login
---
- launchApp:
    clearState: true
- extendedWaitUntil:
    visible: "Welcome"
    timeout: 10000
- tapOn:
    id: "email_field"
- inputText: ${TEST_EMAIL}
- tapOn:
    id: "password_field"
- inputText: ${TEST_PASSWORD}
- tapOn:
    id: "login_button"
- waitForAnimationToEnd
- assertVisible:
    id: "home_tab"
- takeScreenshot: "login_success"
```

## Key Commands

| Command | Description |
|---------|-------------|
| `tapOn: { id: "key" }` | Tap by widget Key |
| `inputText: "value"` | Type text |
| `assertVisible: "text"` | Assert visible |
| `assertNotVisible: "text"` | Assert gone |
| `extendedWaitUntil` | Wait for element |
| `waitForAnimationToEnd` | Wait animations |
| `takeScreenshot: "name"` | Screenshot |
| `runFlow: path.yaml` | Reuse flow |
| `launchApp: { clearState: true }` | Fresh start |

## Running Tests

```bash
flutter build apk --debug
maestro test .maestro/flows/
```

## Testing Pyramid

```
              ┌─────────────────┐
              │    Maestro      │  10% — Full user journeys
              └────────┬────────┘
            ┌──────────┴──────────┐
            │   Widget Tests      │  20% — UI components
            └──────────┬──────────┘
  ┌────────────────────┴────────────────────┐
  │              Unit Tests                  │  70% — Business logic
  │  (BLoC, UseCases, Repositories)          │  mocktail, bloc_test
  └──────────────────────────────────────────┘
```
