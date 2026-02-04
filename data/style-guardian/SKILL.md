---
name: style-guardian
description: "Style Guardian - Unified Design System Enforcement Tool. Use for: (1) Preventing hardcoded styles (colors, spacing, typography), (2) Preventing hardcoded text (i18n violations), (3) Guiding unified configuration usage, (4) Detecting and fixing style violations"
---

# Style Guardian - Unified Design System Enforcement

## Core Principles

### Design Philosophy: Flat Design 2.0 + Monochrome System

| Principle | Description | Source |
|-----------|-------------|--------|
| Minimalism | Clean, uncluttered layouts | Flat Design |
| 2D Styling | Simple, flat shapes without 3D effects | Flat Design |
| Subtle Shadows | Shadows hint at interactivity (Flat 2.0) | Material Design |
| Monochrome | Primarily use different saturations of blue | Project Design Spec |
| Three-Color System | Blue (primary) + Green (positive) + Orange (negative) | Project Design Spec |

### Key Files

| File | Purpose |
|------|---------|
| `lib/core/ui/ui_config.dart` | Core style configuration system |
| `lib/core/ui/flat_design_config.dart` | Flat design component configuration |
| `lib/core/ui/responsive_config.dart` | Responsive layout configuration |
| `lib/app/theme.dart` | Application theme (uses UIColors) |
| `docs/ui_design_specification.md` | UI design specification document |

---

## Color System

### Primary Color (Blue, 90% usage)

| Hardcoded | UIColors | Purpose | Hex |
|-----------|----------|---------|-----|
| `Colors.blue` | `UIColors.primary` | Primary buttons | #2196F3 |
| `Color(0xFF2196F3)` | `UIColors.primary` | Primary buttons | #2196F3 |
| `Colors.blue[50]` | `UIColors.primaryLightest` | Background blocks | #E3F2FD |
| `Colors.blue[100]` | `UIColors.primaryLight` | Secondary blocks | #BBDEFB |
| `Colors.blue[300]` | `UIColors.primaryMedium` | Interactive elements | #64B5F6 |
| `Colors.blue[700]` | `UIColors.primaryDark` | Selected states | #1976D2 |
| `Colors.blue[900]` | `UIColors.primaryDarkest` | Emphasis text | #0D47A1 |

### Positive Color (Green, 5% usage)

| Hardcoded | UIColors | Purpose |
|-----------|----------|---------|
| `Colors.green` | `UIColors.positive` | Success, confirmation |
| `Colors.green[100]` | `UIColors.positiveLight` | Success backgrounds |
| `Colors.green[700]` | `UIColors.positiveDark` | Success emphasis |

### Negative Color (Orange, 5% usage)

| Hardcoded | UIColors | Purpose |
|-----------|----------|---------|
| `Colors.orange` | `UIColors.negative` | Warning, error |
| `Colors.amber` | `UIColors.negative` | Warning, caution |
| `Colors.red` | `UIColors.negative` | **Project does NOT use red** |

### Background Colors

| Hardcoded | UIColors | Purpose |
|-----------|----------|---------|
| `Colors.white` | `UIColors.surfaceLight` | Card backgrounds |
| `Colors.grey[50]` | `UIColors.backgroundLight` | Page backgrounds |
| `Colors.grey[600]` | `UIColors.onSurfaceMuted` | Muted text |

---

## Spacing System (4dp Grid)

### SizedBox Spacing

| Hardcoded | UISpacing | Responsive |
|-----------|-----------|------------|
| `SizedBox(height: 4)` | `SizedBox(height: UISpacing.xxs)` | `.h` suffix |
| `SizedBox(height: 8)` | `SizedBox(height: UISpacing.xs)` | `.h` suffix |
| `SizedBox(height: 12)` | `SizedBox(height: UISpacing.sm)` | `.h` suffix |
| `SizedBox(height: 16)` | `SizedBox(height: UISpacing.md)` | `.h` suffix |
| `SizedBox(height: 24)` | `SizedBox(height: UISpacing.lg)` | `.h` suffix |
| `SizedBox(height: 32)` | `SizedBox(height: UISpacing.xl)` | `.h` suffix |
| `SizedBox(width: 8)` | `SizedBox(width: UISpacing.xs)` | `.w` suffix |

### EdgeInsets Padding

| Hardcoded | UISpacing |
|-----------|-----------|
| `EdgeInsets.all(4)` | `EdgeInsets.all(UISpacing.xxs)` |
| `EdgeInsets.all(8)` | `EdgeInsets.all(UISpacing.xs)` |
| `EdgeInsets.all(16)` | `EdgeInsets.all(UISpacing.md)` |
| `EdgeInsets.symmetric(horizontal: 16)` | `EdgeInsets.symmetric(horizontal: UISpacing.md)` |
| `EdgeInsets.symmetric(vertical: 8)` | `EdgeInsets.symmetric(vertical: UISpacing.xs)` |

---

## Typography System

### Font Sizes

| Hardcoded | UIFontSizes | Purpose |
|-----------|-------------|---------|
| `fontSize: 10` | `UIFontSizes.overline` | Overline text |
| `fontSize: 12` | `UIFontSizes.bodySmall` | Small body text |
| `fontSize: 14` | `UIFontSizes.bodyMedium` | Standard body text |
| `fontSize: 16` | `UIFontSizes.bodyLarge` | Large body text |
| `fontSize: 18` | `UIFontSizes.titleMedium` | Medium titles |
| `fontSize: 20` | `UIFontSizes.titleLarge` | Large titles |
| `fontSize: 24` | `UIFontSizes.headline3` | Headlines |

### Responsive Font Sizes

Use `.rsp` suffix for responsive scaling:

```dart
// Correct
TextStyle(fontSize: UIFontSizes.bodyMedium)  // Already includes .rsp

// Incorrect
TextStyle(fontSize: 14)
TextStyle(fontSize: 14.sp)  // Manual scaling
```

---

## Border Radius System

| Hardcoded | UIBorderRadius |
|-----------|----------------|
| `BorderRadius.circular(4)` | `BorderRadius.circular(UIBorderRadius.xs)` |
| `BorderRadius.circular(8)` | `BorderRadius.circular(UIBorderRadius.sm)` |
| `BorderRadius.circular(12)` | `BorderRadius.circular(UIBorderRadius.md)` |
| `BorderRadius.circular(16)` | `BorderRadius.circular(UIBorderRadius.lg)` |
| `BorderRadius.circular(20)` | `BorderRadius.circular(UIBorderRadius.xl)` |
| `BorderRadius.circular(999)` | `BorderRadius.circular(UIBorderRadius.circular)` |

---

## Internationalization (i18n)

### Correct Usage

```dart
// Correct - use l10n
Text(context.l10n!.libraryTitle)
Text(context.l10n!.selectedCount(count, total))
Text(context.l10n!.errorMessage)

// Incorrect - hardcoded strings
Text('My Library')
Text('$count items selected')
Text('An error occurred')
```

### Adding New Translation Keys

1. Edit `lib/l10n/app_en.arb`:
   ```json
   {
     "newKey": "New text value",
     "@newKey": {
       "description": "Description of the text"
     }
   }
   ```

2. Run `flutter gen-l10n`

3. Use in code:
   ```dart
   Text(context.l10n!.newKey)
   ```

### Supported Languages

- en (English)
- en_US (English - US)
- zh_TW (Traditional Chinese)
- zh_CN (Simplified Chinese)
- zh (Chinese)
- es (Spanish)
- fr (French)
- hi (Hindi)
- ja (Japanese)
- ko (Korean)

---

## Common Violations and Fixes

### Violation 1: Hardcoded Colors

```dart
// Violation
Container(color: Colors.blue)
Container(color: Color(0xFF2196F3))

// Fix
Container(color: UIColors.primary)
```

### Violation 2: Hardcoded Spacing

```dart
// Violation
SizedBox(height: 16)
Padding(padding: EdgeInsets.all(8))

// Fix
SizedBox(height: UISpacing.md)
Padding(padding: EdgeInsets.all(UISpacing.xs))
```

### Violation 3: Hardcoded Font Size

```dart
// Violation
TextStyle(fontSize: 14)

// Fix
TextStyle(fontSize: UIFontSizes.bodyMedium)
```

### Violation 4: Hardcoded Border Radius

```dart
// Violation
BorderRadius.circular(8)

// Fix
BorderRadius.circular(UIBorderRadius.sm)
```

### Violation 5: Hardcoded Text

```dart
// Violation
Text('My Library')
AppBar(title: Text('Settings'))

// Fix
Text(context.l10n!.libraryTitle)
AppBar(title: Text(context.l10n!.settingsTitle))
```

### Violation 6: ViewModel Hardcoded User Messages

**Scope**: `lib/presentation/**/viewmodel.dart`, `lib/presentation/**_viewmodel.dart`

**Detection Pattern**: String literals assigned to error/message state properties

```dart
// Violation - Hardcoded user messages in ViewModel
state = state.copyWith(errorMessage: 'Invalid file format');
state = state.copyWith(errorMessage: '網路連線失敗');
_errorMessage = 'Something went wrong';

// Fix - Use i18n or ErrorHandler
state = state.copyWith(errorMessage: context.l10n!.invalidFileFormat);
state = state.copyWith(errorMessage: ErrorHandler.getUserMessage(exception));
```

**Allowed Exceptions**:
- `e.toString()` for unknown system exceptions
- String interpolation with i18n: `context.l10n!.errorWithCode(code)`

**Related**: [FLUTTER.md - ViewModel 層使用者訊息規範](../../../FLUTTER.md)

---

## Detection Script Usage

### Manual Scan

```bash
# Scan entire project
uv run .claude/skills/style-guardian/scripts/style_checker.py scan lib/

# Scan specific directory
uv run .claude/skills/style-guardian/scripts/style_checker.py scan lib/presentation/

# Generate report
uv run .claude/skills/style-guardian/scripts/style_checker.py report
```

### Hook Integration

The style checker is integrated into PostEdit Hook:
- Automatically scans edited files in `lib/presentation/`
- Reports violations in hook output
- Suggests fixes based on this guide

---

## Related Documentation

### Project Files
- [UI Configuration](../../../lib/core/ui/ui_config.dart)
- [Flat Design Config](../../../lib/core/ui/flat_design_config.dart)
- [Responsive Config](../../../lib/core/ui/responsive_config.dart)
- [UI Design Specification](../../../docs/ui_design_specification.md)
- [i18n Guide](../../../docs/i18n_guide.md)

### Reference Files (in this SKILL)
- [Color System Reference](./references/color-system.md)
- [Spacing System Reference](./references/spacing-system.md)
- [Typography System Reference](./references/typography-system.md)
- [i18n Guidelines Reference](./references/i18n-guidelines.md)

### External Resources
- [Flat Design Explained - MasterClass](https://www.masterclass.com/articles/flat-design-explained)
- [Best Practices for Flat Design - Usersnap](https://usersnap.com/blog/flat-design/)
- [Material Design 3 Color System](https://m3.material.io/styles/color/overview)

---

## Quick Reference Card

### Import Statement

```dart
import 'package:book_overview_app/core/ui/ui_config.dart';
```

### Common Replacements

| Type | Hardcoded | Configuration |
|------|-----------|---------------|
| **Color** | `Colors.blue` | `UIColors.primary` |
| **Success** | `Colors.green` | `UIColors.positive` |
| **Warning** | `Colors.orange` | `UIColors.negative` |
| **Spacing** | `16` | `UISpacing.md` |
| **Font** | `14` | `UIFontSizes.bodyMedium` |
| **Radius** | `8` | `UIBorderRadius.sm` |
| **Text** | `'My Library'` | `context.l10n!.libraryTitle` |

### Responsive Suffixes

| Suffix | Purpose | Example |
|--------|---------|---------|
| `.w` | Width scaling | `16.w` |
| `.h` | Height scaling | `16.h` |
| `.rsp` | Font scaling | `14.rsp` |
| `.r` | Radius scaling | `8.r` |
