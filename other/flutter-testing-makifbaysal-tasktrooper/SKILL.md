---
name: flutter-testing
category: testing
description: Use when testing Flutter code - unit tests for logic, widget tests for UI behavior, golden tests for appearance, the multi-size/text-scale/dark matrix, accessibility guidelines, test-first
tech_stack: Flutter
source: flutter/agent-plugins (BSD-3-Clause), adapted
---
# Flutter Testing

## Overview

Test-first in Flutter (see tdd-workflow). Three layers, each for a different question: does the logic work, does the widget behave, does it look right.

**Core principle:** Most tests are fast unit + widget tests. Golden tests guard appearance; integration tests guard whole flows — use them sparingly.

## Test layers

| Layer | Question | Tool |
|-------|----------|------|
| Unit | Does the controller/logic compute correctly? | `flutter_test`, mock the repository |
| Widget | Does the widget render state and respond to taps? | `testWidgets` + `pumpWidget` + finders |
| Golden | Does it match the approved pixels? | `matchesGoldenFile` |
| Integration | Does the whole flow work on a device? | `integration_test` |

## Widget test example

```dart
testWidgets('shows error view and retries', (tester) async {
  final controller = FakeTaskController()..emitError('boom');
  await tester.pumpWidget(wrap(TaskListScreen(controller: controller)));
  await tester.pump();

  expect(find.text('boom'), findsOneWidget);
  await tester.tap(find.byType(RetryButton));
  await tester.pump();
  expect(controller.loadCalled, isTrue);   // intent reached the controller
});
```

## Rules

- **Unit-test controllers/logic without pumping a widget** — that's the payoff of keeping logic out of widgets (see flutter-state-management).
- **Widget tests assert observable behavior** (text visible, tap triggers intent), not internal structure.
- **Mock the repository/ports**, not the widget under test. Prefer a hand-written fake or `mocktail` per the app's convention.
- **Golden tests:** commit the golden, review changes deliberately; regenerate only when the change is intended.
- Cover loading, data, empty, and error states — the branches most likely to ship broken.
- `pump` vs `pumpAndSettle`: use `pump` for controlled frames, `pumpAndSettle` to drain animations — never rely on real timers.

## Matrix test: size, text scale, dark mode

A widget test that only runs at the default size and text scale misses the most common mobile layout bug — overflow at larger text scales. See `mobile-visual-self-review` for the full size matrix and the worked `PriceRow` example (verified: passes at text scale 1.0 everywhere, overflows by 82px at 360×640/2.0). The shape:

```dart
tester.view.physicalSize = const Size(360, 640) * 3;
tester.view.devicePixelRatio = 3;
tester.platformDispatcher.textScaleFactorTestValue = 2.0;
addTearDown(tester.view.reset);
addTearDown(tester.platformDispatcher.clearAllTestValues);
```

Run this as a real `testWidgets` case per matrix cell for any screen/component whose layout changed — it is the failing test a layout change starts from (see `tdd-first`), not an afterthought bolted on once the happy path passes.

## Accessibility guidelines (verified)

`meetsGuideline` from `flutter_test`/`flutter/accessibility`, run inside `tester.ensureSemantics()`:

```dart
final handle = tester.ensureSemantics();
await expectLater(tester, meetsGuideline(androidTapTargetGuideline));   // 48x48
await expectLater(tester, meetsGuideline(iOSTapTargetGuideline));       // 44x44
await expectLater(tester, meetsGuideline(labeledTapTargetGuideline));   // every tappable has a label
await expectLater(tester, meetsGuideline(textContrastGuideline));
handle.dispose();
```

Run these against every new or changed interactive widget's test, not just a dedicated accessibility suite.

## Golden test pitfalls (verified)

- **Fonts:** by default, text renders as box glyphs in a golden unless the app's real fonts are loaded in `flutter_test_config.dart` (`loadAppFonts()` or equivalent) — a golden taken without that setup locks in boxes, not the real typography. Use goldens for layout/shape verification, or load the fonts first.
- **OS differences:** text rendering and anti-aliasing differ per OS, so the same golden can legitimately differ on macOS vs Linux CI. Tag golden tests (`@Tags(['golden'])`) and generate/update them on one OS consistently (match CI's).
- **Never `--update-goldens` to make a red test green** without looking at the diff first — that silently accepts a visual regression as the new baseline.

## Common Mistakes

- `pumpWidget` for logic that could be a plain unit test (slow, indirect).
- Asserting widget-tree internals instead of visible behavior.
- No error/empty-state test.
- Golden files regenerated blindly, hiding a visual regression.
- A layout test that only runs at the default device size and text scale 1.0.

## Red Flags

- The test passes before the production code exists (tests a fake).
- Every test boots the full app.
- Only the happy path is covered.
- No test exercises text scale 2.0 on a screen that changed layout.
