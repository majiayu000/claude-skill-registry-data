---
name: flutter-ui
description: Flutter UI patterns including layouts, Material 3 components, and responsive design. Use when building screens, creating reusable widgets, or implementing responsive layouts.
---

# Flutter UI Building

## Widget Decision

| Need | Widget |
|------|--------|
| Vertical list | `Column` (few) or `ListView` (many) |
| Horizontal list | `Row` (few) or `ListView.horizontal` (many) |
| Overlapping widgets | `Stack` + `Positioned` |
| Grid | `GridView.builder` |
| Spacing/sizing | `SizedBox` (preferred) or `Container` |
| Decorations (shadow, border) | `Container` with `BoxDecoration` |

## Detailed Guides

| Topic | Guide | Use When |
|-------|-------|----------|
| Layouts | [layouts.md](references/layouts.md) | Row, Column, Stack, Flex patterns |
| Material 3 | [material-components.md](references/material-components.md) | Scaffold, AppBar, Cards, Buttons |
| Responsive | [responsive.md](references/responsive.md) | LayoutBuilder, MediaQuery, adaptive |

## Essential Patterns

### Standard Widget Structure

```dart
class ProductCard extends StatelessWidget {
  const ProductCard({
    super.key,
    required this.product,
    this.onTap,
  });

  final Product product;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Card(
      child: InkWell(
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(product.name, style: theme.textTheme.titleMedium),
              const SizedBox(height: 8),
              Text(product.description, style: theme.textTheme.bodyMedium),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Use const Constructors

```dart
// ✅ Widget cached, never rebuilds
const SizedBox(height: 16)
const Icon(Icons.home)
const Text('Static text')

// ❌ Recreated every build
SizedBox(height: 16)
Icon(Icons.home)
```

### SizedBox vs Container

```dart
// ✅ SizedBox for spacing (lighter)
const SizedBox(height: 16)
const SizedBox(width: 8)
SizedBox(width: 100, height: 100, child: widget)

// ✅ Container for decoration
Container(
  padding: const EdgeInsets.all(16),
  decoration: BoxDecoration(
    color: Colors.white,
    borderRadius: BorderRadius.circular(8),
    boxShadow: [BoxShadow(...)],
  ),
  child: widget,
)
```

### Keys for Lists

```dart
// ✅ Use keys when list items can reorder
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(
      key: ValueKey(items[index].id),  // Unique, stable key
      title: Text(items[index].name),
    );
  },
)
```

## Layout Quick Reference

### Expand vs Flexible

```dart
Row(
  children: [
    Expanded(child: Text('Takes remaining space')),     // flex: 1, fit: tight
    Flexible(child: Text('Takes needed space, can shrink')),  // fit: loose
    const SizedBox(width: 100),  // Fixed width
  ],
)
```

### Stack Positioning

```dart
Stack(
  children: [
    // Background (fills entire stack)
    Positioned.fill(child: Image.asset('bg.png', fit: BoxFit.cover)),
    
    // Top-right corner
    Positioned(top: 16, right: 16, child: CloseButton()),
    
    // Centered
    Center(child: Text('Centered content')),
    
    // Bottom, full width
    Positioned(left: 0, right: 0, bottom: 0, child: BottomBar()),
  ],
)
```

## Theme Usage

```dart
// Access theme
final theme = Theme.of(context);
final colorScheme = theme.colorScheme;
final textTheme = theme.textTheme;

// Use theme values
Text('Title', style: textTheme.headlineMedium)
Container(color: colorScheme.primaryContainer)
Icon(Icons.star, color: colorScheme.primary)
```

## Common Patterns

### Loading State

```dart
Widget build(BuildContext context) {
  if (isLoading) {
    return const Center(child: CircularProgressIndicator());
  }
  
  if (error != null) {
    return Center(child: Text('Error: $error'));
  }
  
  return ContentWidget(data: data);
}
```

### Pull to Refresh

```dart
RefreshIndicator(
  onRefresh: () async {
    await viewModel.refresh();
  },
  child: ListView.builder(...),
)
```

### Safe Area

```dart
Scaffold(
  body: SafeArea(
    child: Column(
      children: [...],
    ),
  ),
)
```
