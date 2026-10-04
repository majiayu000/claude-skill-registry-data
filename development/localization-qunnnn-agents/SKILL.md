---
tags: [flutter, l10n, localization, arb]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Localization (ARB-based)

## Context

Apply when adding, modifying, or fixing localized strings in Flutter projects using `.arb` files.

## Instructions

1. **Never hardcode user-facing strings** — always use localization keys.
2. **ARB file structure**: One `.arb` file per locale (e.g., `app_en.arb`, `app_zh.arb`).
3. **Key naming**: Use `camelCase`, prefixed by feature:
   - `walletSendTitle`, `walletGasFeeLabel`, `profileEditButton`
4. **Placeholders**: Define placeholders with types in the `@key` metadata:
   ```json
   "walletBalance": "Balance: {amount} {unit}",
   "@walletBalance": {
     "placeholders": {
       "amount": { "type": "String" },
       "unit": { "type": "String" }
     }
   }
   ```
5. **Parameter ordering**: Ensure call-sites pass arguments in the **same order** as declared in the `@key` placeholders. Mismatched order is a common source of bugs.
6. **Always update ALL locale files** when adding a new key.
7. **Run code generation** after modifying `.arb` files:
   ```bash
   flutter gen-l10n
   ```

## Examples

### Adding a new key

```json
// app_en.arb
"gasFeeValue": "Fee {value} {unit}",
"@gasFeeValue": {
  "placeholders": {
    "value": { "type": "String" },
    "unit": { "type": "String" }
  }
}
```

```dart
// Usage in widget
Text(context.l10n.gasFeeValue(fee.value, fee.unit))
```

## Anti-patterns

- ❌ Hardcoded strings in widgets
- ❌ Mismatched parameter order between `.arb` definition and call-site
- ❌ Adding keys to only one locale file
- ❌ Using string interpolation instead of ARB placeholders

## Resources

- https://docs.flutter.dev/ui/internationalization
- https://docs.flutter.dev/release/breaking-changes/flutter-generate-i10n-source
- https://docs.flutter.dev/release/breaking-changes/material-localized-strings
- https://docs.flutter.dev/release/breaking-changes/text-field-material-localizations
- https://docs.flutter.dev/release/breaking-changes/cupertino-tab-bar-localizations
