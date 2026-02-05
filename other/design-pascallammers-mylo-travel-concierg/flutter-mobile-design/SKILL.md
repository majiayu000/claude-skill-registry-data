---
name: flutter-mobile-design
description: Create distinctive, production-grade Flutter mobile applications with Material Design 3. Use this skill when the user asks to build Flutter widgets, screens, pages, or complete mobile apps. Handles UI creation from scratch, design-to-code conversion (Figma/mockups), architecture patterns (Riverpod, BLoC), and Flutter best practices. Generates beautiful, performant Flutter code that avoids generic aesthetics.
---

This skill guides creation of distinctive, production-grade Flutter mobile applications using Material Design 3. Implement real working Dart/Flutter code with exceptional attention to aesthetic details, performance, and platform conventions.

The user provides mobile app requirements: a widget, screen, feature, or complete application to build. They may include context about the purpose, target platform (iOS/Android), or design references.

## Design Thinking

Before coding, understand the context and commit to a strong design direction:

- **Purpose**: What problem does this app solve? Who uses it?
- **Platform**: iOS, Android, or both? Consider platform-specific conventions.
- **Tone**: Material Design 3 offers flexibility - choose a personality: vibrant & playful, calm & professional, bold & expressive, minimal & clean, warm & organic.
- **Color Scheme**: Use dynamic color (Material You) or create a custom ColorScheme with clear semantic meaning.
- **Differentiation**: What makes this app memorable? What's the signature interaction or visual element?

Then implement working Flutter code that is:
- Production-grade and functional
- Visually polished with Material Design 3
- Performant and responsive
- Accessible and platform-aware

## Flutter & Material Design 3 Guidelines

### Typography

Use Material 3 type scale with `Theme.of(context).textTheme`:

```dart
Text(
  'Headline',
  style: Theme.of(context).textTheme.headlineMedium,
)
```

Type roles: `displayLarge/Medium/Small`, `headlineLarge/Medium/Small`, `titleLarge/Medium/Small`, `bodyLarge/Medium/Small`, `labelLarge/Medium/Small`.

For custom fonts, define in `TextTheme` and apply via `ThemeData`. Prefer Google Fonts that complement Material 3.

### Color System

Use Material 3 ColorScheme with semantic colors:

```dart
ThemeData(
  colorScheme: ColorScheme.fromSeed(
    seedColor: Colors.deepPurple,
    brightness: Brightness.light,
  ),
  useMaterial3: true,
)
```

Access colors semantically:
- `colorScheme.primary` / `onPrimary` - Key actions, FAB
- `colorScheme.secondary` / `onSecondary` - Less prominent actions
- `colorScheme.tertiary` / `onTertiary` - Contrasting accents
- `colorScheme.surface` / `onSurface` - Cards, sheets, dialogs
- `colorScheme.error` / `onError` - Error states

Support dark mode with `Brightness.dark` variant.

### Components & Widgets

Prefer Material 3 widgets:
- `FilledButton`, `FilledButton.tonal`, `OutlinedButton`, `TextButton`
- `FloatingActionButton.extended` with icon
- `NavigationBar` (bottom), `NavigationRail` (side), `NavigationDrawer`
- `Card` with `elevation` and `surfaceTintColor`
- `SearchAnchor` for search
- `SegmentedButton` for toggles
- `Slider`, `Switch`, `Checkbox` with M3 styling

Use `Material` widget with proper `elevation` and `surfaceTintColor` for custom surfaces.

### Motion & Animation

Use purposeful, expressive motion:

```dart
// Implicit animations
AnimatedContainer(
  duration: const Duration(milliseconds: 300),
  curve: Curves.easeOutCubic,
  // ...
)

// Hero transitions
Hero(
  tag: 'item-$id',
  child: Image.network(url),
)

// Page transitions
MaterialPageRoute(
  builder: (context) => DetailScreen(),
)
```

Motion principles:
- **Informative**: Motion shows spatial relationships
- **Focused**: Draw attention to what matters
- **Expressive**: Reflect brand personality

Duration guidelines: 150ms (small), 300ms (medium), 500ms (large/complex).

### Layout & Spacing

Use Material spacing scale (multiples of 4dp):

```dart
const EdgeInsets.all(16) // Standard padding
const EdgeInsets.symmetric(horizontal: 24, vertical: 16)
const SizedBox(height: 8) // Vertical spacing
```

Responsive layouts:
```dart
LayoutBuilder(
  builder: (context, constraints) {
    if (constraints.maxWidth > 600) {
      return WideLayout();
    }
    return NarrowLayout();
  },
)
```

Use `Flex`, `Wrap`, `GridView.builder` for adaptive grids.

## Architecture & State Management

### Recommended: Riverpod

```dart
// Define providers
final counterProvider = StateNotifierProvider<CounterNotifier, int>((ref) {
  return CounterNotifier();
});

class CounterNotifier extends StateNotifier<int> {
  CounterNotifier() : super(0);
  void increment() => state++;
}

// Use in widget
class CounterWidget extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final count = ref.watch(counterProvider);
    return Text('$count');
  }
}
```

### Alternative: BLoC (for larger apps)

```dart
class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<Increment>((event, emit) => emit(state + 1));
  }
}
```

### Project Structure

```
lib/
├── main.dart
├── app/
│   ├── app.dart              # MaterialApp setup
│   └── router.dart           # Navigation (go_router)
├── features/
│   └── feature_name/
│       ├── presentation/     # Widgets, screens
│       ├── application/      # Business logic, providers/blocs
│       ├── domain/           # Entities, repositories interfaces
│       └── data/             # Repository implementations, DTOs
├── shared/
│   ├── widgets/              # Reusable widgets
│   └── theme/                # ThemeData, ColorScheme
└── core/
    ├── constants/
    └── utils/
```

## Performance Checklist

- Use `const` constructors everywhere possible
- Implement `ListView.builder` / `GridView.builder` for long lists
- Cache network images with `cached_network_image`
- Avoid rebuilding entire widget trees - use selective `Consumer` or `BlocBuilder`
- Profile with Flutter DevTools
- Keep build methods lean - extract widgets
- Use `RepaintBoundary` for complex animations

## Platform-Specific Guidelines

### iOS Considerations
- Support safe areas (`SafeArea` widget)
- Consider `CupertinoPageRoute` for iOS-style transitions
- Support dynamic type / text scaling
- Handle notch and home indicator

### Android Considerations
- Support edge-to-edge display
- Handle back button / predictive back
- Material You dynamic colors when available
- Support foldables with adaptive layouts

## Quality Checklist

- [ ] App size optimized (tree-shake, deferred loading)
- [ ] Startup time < 2 seconds
- [ ] Smooth 60fps animations
- [ ] Dark mode supported
- [ ] Accessibility: semantic labels, sufficient contrast
- [ ] Responsive across screen sizes
- [ ] Offline capability considered
- [ ] Error states handled gracefully

## Code Style

```dart
// Good: Descriptive, const, proper typing
const EdgeInsets kDefaultPadding = EdgeInsets.all(16);

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
    final colors = theme.colorScheme;

    return Card(
      clipBehavior: Clip.antiAlias,
      child: InkWell(
        onTap: onTap,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Widget content
          ],
        ),
      ),
    );
  }
}
```

## Restricted

NEVER use generic AI-generated aesthetics like overused font families (Inter, Roboto, Arial, system fonts), cliched color schemes (particularly purple gradients on white backgrounds), predictable layouts and component patterns, and cookie-cutter design that lacks context-specific character.

NEVER generate generic, boilerplate Flutter code. Each implementation should feel crafted for its specific purpose with thoughtful Material Design 3 application and attention to detail.
