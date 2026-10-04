---
name: flutter-improving-accessibility
description: Configures a Flutter app to support assistive technologies like Screen Readers. Use when ensuring an application is usable for people with disabilities.
tags: [flutter, accessibility, semantics, a11y, screen-reader, wcag, aria]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Accessibility

## Contents
- [UI Design Standards](#ui-design-standards)
- [Accessibility Widgets](#accessibility-widgets)
- [Web Accessibility](#web-accessibility)
- [Workflow: Accessibility Implementation](#workflow-accessibility-implementation)
- [Workflow: Accessibility Validation](#workflow-accessibility-validation)
- [Examples](#examples)

## UI Design Standards

Design layouts to accommodate dynamic scaling and high visibility. Flutter automatically calculates font sizes based on OS-level accessibility settings.

### Minimum Requirements

| Requirement | Standard |
|---|---|
| **Color Contrast (small text)** | ≥ 4.5:1 ratio (W3C WCAG AA) |
| **Color Contrast (large text)** | ≥ 3.0:1 ratio (18pt+ regular or 14pt+ bold) |
| **Tap Target Size** | ≥ 48 × 48 logical pixels |
| **Font Scaling** | Layouts must not clip/overflow at maximum OS font settings |

### Design Rules

- **Font Scaling:** Ensure layouts provide sufficient room when font sizes are increased to maximum OS settings. Avoid hardcoding fixed heights on text containers.
- **Color Contrast:** Never rely solely on color to convey information. Always pair with icons, labels, or patterns.
- **Tap Targets:** Use `Material` or `InkWell` widgets with minimum 48×48 touch areas. Add padding to small interactive elements.

## Accessibility Widgets

Use Flutter's catalog of accessibility widgets to manipulate the semantics tree exposed to assistive technologies (TalkBack, VoiceOver).

| Widget | Purpose |
|---|---|
| `Semantics` | Annotate the widget tree with meaning. Assign roles using `SemanticsRole` enum. |
| `MergeSemantics` | Merge descendants into a single selectable node for screen readers. |
| `ExcludeSemantics` | Hide decorative/redundant sub-widgets from accessibility tools. |

### When to Use Each Widget

- **`Semantics`**: Custom interactive components (buttons, list items, toggles) that don't automatically expose their role.
- **`MergeSemantics`**: Composite widgets where individual children shouldn't be separate screen reader stops (e.g., a card with icon + text + subtitle).
- **`ExcludeSemantics`**: Purely decorative elements (background images, decorative dividers, redundant icons next to labels).

## Web Accessibility

Flutter web renders UI on a single canvas, requiring a specialized DOM layer.

- **Semantics Disabled by Default:** For performance, web accessibility is off by default. Users can enable via an invisible button.
- **Programmatic Enablement:** For web-first apps requiring default accessibility, force semantics at startup:

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/semantics.dart';

void main() {
  if (kIsWeb) {
    SemanticsBinding.instance.ensureSemantics();
  }
  runApp(const MyApp());
}
```

- **Semantic Roles:** Standard widgets (`TabBar`, `MenuAnchor`, `Table`) automatically map to ARIA roles. For custom components, explicitly assign `SemanticsRole` values.

## Workflow: Accessibility Implementation

Apply this checklist during UI development:

- [ ] Verify all interactive elements have a minimum tap target of 48×48 pixels.
- [ ] Test layout with maximum OS font size settings — ensure no text clipping or overflow.
- [ ] Validate color contrast ratios (4.5:1 for normal text, 3.0:1 for large text).
- [ ] Wrap custom interactive widgets in `Semantics` and assign the appropriate `SemanticsRole`.
- [ ] Group complex composite widgets using `MergeSemantics` to prevent screen reader fatigue.
- [ ] Hide decorative elements from screen readers using `ExcludeSemantics`.
- [ ] If targeting web, verify ARIA roles are correctly mapped.
- [ ] Add `Tooltip` to icon-only buttons for screen reader context.

## Workflow: Accessibility Validation

Run this loop when finalizing a view or component:

1. **Run validator:** Execute accessibility tests or use OS-level screen readers (VoiceOver on iOS/macOS, TalkBack on Android).
2. **Review errors:** Identify unannounced interactive elements, trapped focus, or clipped text.
3. **Fix:** Apply `Semantics`, adjust constraints, or modify colors.
4. **Repeat** until the screen reader provides a clear, logical traversal of the UI.

### Automated Testing

```dart
testWidgets('button has correct semantics', (tester) async {
  await tester.pumpWidget(const MaterialApp(home: MyButton()));

  final semantics = tester.getSemantics(find.byType(MyButton));
  expect(semantics.label, 'Submit form');
  expect(semantics.hasAction(SemanticsAction.tap), isTrue);
});
```

## Examples

### Custom Component with Semantics

```dart
class CustomListItem extends StatelessWidget {
  final String title;
  final String subtitle;
  final VoidCallback onTap;

  const CustomListItem({
    super.key,
    required this.title,
    required this.subtitle,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return MergeSemantics(
      child: Semantics(
        button: true,
        label: '$title, $subtitle',
        child: InkWell(
          onTap: onTap,
          child: Padding(
            padding: const EdgeInsets.all(16.0), // Ensures > 48px tap target
            child: Row(
              children: [
                ExcludeSemantics(
                  child: Icon(Icons.person), // Decorative — already described in label
                ),
                const SizedBox(width: 16),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(title, style: const TextStyle(fontSize: 16)),
                    Text(subtitle, style: const TextStyle(fontSize: 14)),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

### Icon Button with Tooltip

```dart
// Always add tooltip to icon-only buttons for screen reader users
IconButton(
  icon: const Icon(Icons.delete),
  tooltip: 'Delete item',
  onPressed: () => _deleteItem(),
)
```

### Image with Semantic Description

```dart
Semantics(
  label: 'Profile photo of the service provider',
  child: ExcludeSemantics(
    child: CircleAvatar(
      backgroundImage: NetworkImage(user.avatarUrl),
      radius: 24,
    ),
  ),
)
```

## Anti-patterns

- ❌ Using color alone to indicate status (error states, success, warnings)
- ❌ Icon-only buttons without `tooltip` or `Semantics` label
- ❌ Interactive elements smaller than 48×48 logical pixels
- ❌ Hardcoding text container heights (breaks with font scaling)
- ❌ Leaving decorative images announced by screen readers
- ❌ Not testing with actual screen readers (VoiceOver / TalkBack)

## Resources

- https://docs.flutter.dev/ui/accessibility-and-internationalization/accessibility
- https://docs.flutter.dev/ui/adaptive-responsive
- https://www.w3.org/WAI/WCAG21/quickref/
- https://api.flutter.dev/flutter/widgets/Semantics-class.html
- https://api.flutter.dev/flutter/widgets/MergeSemantics-class.html
- https://api.flutter.dev/flutter/widgets/ExcludeSemantics-class.html
