---
name: layout-debugger
description: Diagnoses and resolves common Flutter layout errors, including RenderFlex overflowed by N pixels, Vertical viewport was given unbounded height, and BoxConstraints issues.
version: 1.0.0
---

# Flutter Layout Debugger

Diagnoses and fixes the most common layout constraint errors in Flutter applications.

## 1. "A RenderFlex overflowed by N pixels"

### Cause
A `Column` (vertical) or `Row` (horizontal) contains children whose combined size exceeds the available space on screen (yellow-and-black striped bars).

### Fix 1: Make Scrollable
If the content naturally exceeds screen size (e.g., forms, long pages):
```dart
// ❌ OVERFLOWS on small screens
Column(
  children: [Header(), FormFields(), SubmitButton()],
)

// ✅ FIXED: Wrap in SingleChildScrollView
SingleChildScrollView(
  child: Padding(
    padding: const EdgeInsets.all(16.0),
    child: Column(
      children: [Header(), FormFields(), SubmitButton()],
    ),
  ),
)
```

### Fix 2: Constrain Child with `Expanded` or `Flexible`
If inside a `Row` or `Column` and an inner child (like `Text`) expands too far:
```dart
// ❌ OVERFLOWS if text is long
Row(
  children: [
    Icon(Icons.warning),
    Text('Very long description that will easily overflow the screen horizontally...'),
  ],
)

// ✅ FIXED: Wrap Text in Expanded
Row(
  children: [
    const Icon(Icons.warning),
    Expanded(
      child: Text('Very long description that will wrap cleanly...'),
    ),
  ],
)
```

---

## 2. "Vertical viewport was given unbounded height"

### Cause
A scrollable widget (`ListView`, `GridView`) was placed inside another vertically unconstrained widget (like a `Column` or another `ListView`) without explicit height.

### Fix 1: Wrap in `Expanded`
```dart
// ❌ CRASHES: Column gives infinite vertical height
Column(
  children: [
    HeaderWidget(),
    ListView.builder(...),
  ],
)

// ✅ FIXED: Wrap ListView in Expanded
Column(
  children: [
    HeaderWidget(),
    Expanded(
      child: ListView.builder(...),
    ),
  ],
)
```

### Fix 2: Use `shrinkWrap: true` + `physics: NeverScrollableScrollPhysics()`
When you need a small list embedded inside an already scrollable page:
```dart
// ✅ FIXED: shrinkWrap sizes to content, parent handles scrolling
ListView.builder(
  shrinkWrap: true,
  physics: const NeverScrollableScrollPhysics(),
  itemCount: items.length,
  itemBuilder: (context, index) => ItemTile(items[index]),
)
```

---

## 3. "BoxConstraints forces an infinite width/height"

### Fix:
Avoid using `double.infinity` inside `Row` / `Column` main-axis dimensions without an `Expanded` or `SizedBox(height: ...)` constraint.
