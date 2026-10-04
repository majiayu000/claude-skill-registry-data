---
name: flutter
description: "Build Flutter widget interfaces, organize state and async behavior, and prepare platform integrations and release builds."
category: development
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["flutter", "dart", "widgets", "mobile", "cross-platform", "claude"]
tools: ["claude", "cursor", "gemini", "codex"]
---

# Flutter Cross-Platform UI AI Skill Guide

## Overview & Engine Architecture

Flutter paints UI with a widget tree compiled to native ARM/x64 (and web/desktop targets). Everything is a widget; rebuilds are cheap when state is localized. Agents prefer composition over deep inheritance, choose an explicit state approach (Riverpod/Bloc/Provider) and stick to it, and keep platform-specific code behind clean facades.

```
Dart app
  -> Widget tree (build)
      -> Element / RenderObject
          -> Skia / Impeller
              -> iOS / Android / Web / Desktop
```

## When to use this skill

- Building or refactoring Flutter screens
- Fixing unnecessary rebuilds and async UI races
- Adding platform views or method channels carefully
- Preparing release/signing build configs

## Operational directives

1. Keep `build()` pure - no side effects; trigger work from callbacks/initState/providers.
2. Use `const` constructors where possible to cut rebuild cost.
3. Handle loading/error/empty states explicitly for every async boundary.
4. Do not block the UI isolate with heavy JSON/parse - use compute/isolates when needed.
5. Match Flutter/Dart SDK constraints in CI to local `pubspec` constraints.

## Widget sketch

```dart
class ItemCount extends StatelessWidget {
  const ItemCount({super.key, required this.qty});
  final int qty;

  @override
  Widget build(BuildContext context) {
    return Text('Qty: $qty');
  }
}

class AddItemButton extends StatefulWidget {
  const AddItemButton({super.key, required this.onAdd});
  final Future<void> Function() onAdd;

  @override
  State<AddItemButton> createState() => _AddItemButtonState();
}

class _AddItemButtonState extends State<AddItemButton> {
  bool _busy = false;

  Future<void> _handle() async {
    if (_busy) return;
    setState(() => _busy = true);
    try {
      await widget.onAdd();
    } finally {
      if (mounted) setState(() => _busy = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: _busy ? null : _handle,
      child: Text(_busy ? 'Saving...' : 'Add'),
    );
  }
}
```

## Commands

```bash
flutter doctor
flutter pub get
flutter run
flutter test
flutter build apk
flutter build ipa
```

## Common pitfalls

| Pitfall | Why it hurts | Fix |
| --- | --- | --- |
| setState after dispose | Crashes | Check `mounted` |
| Giant Build methods | Unmaintainable rebuilds | Extract widgets |
| Ignoring null-safety | Runtime surprises | Sound null safety |
| Unsigned release experiments | Store rejection | Proper signing configs |

## Best practices

- Use keys when reordering lists of stateful children.
- Centralize theme and text styles; avoid one-off magic numbers.
- Add golden/widget tests for critical UI; integration tests for flows.
- Document min iOS/Android OS versions for the project.

## Limitations

- Plugin quality varies across platforms - verify each target.
- Impeller vs Skia behavior can differ by Flutter version/OS.
- Heavy native UI embedding is still a specialized path.

## Related skills

- `@dart` - language fundamentals when present
- `@android-studio` / `@xcode-ios` - native tooling underneath
- `@firebase` - common backend for Flutter apps
