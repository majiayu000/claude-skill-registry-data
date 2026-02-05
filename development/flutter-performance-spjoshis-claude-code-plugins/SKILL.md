---
name: flutter-performance
description: Optimize Flutter app performance with widget rebuilds, memory management, rendering optimization, and profiling techniques. Achieve smooth 60fps rendering.
---

# Flutter Performance Optimization

Master Flutter performance optimization techniques including widget rebuild optimization, memory management, rendering performance, and using DevTools for profiling.

## When to Use This Skill

- App is dropping frames or feels laggy
- High memory usage or memory leaks
- Slow startup time
- Inefficient list scrolling
- Large build times
- Image loading performance issues
- Profiling and benchmarking

## Key Performance Principles

### 1. Widget Rebuild Optimization

```dart
// BAD: Widget rebuilds unnecessarily
class BadExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        ExpensiveWidget(),
        AnotherWidget(),
      ],
    );
  }
}

// GOOD: Use const constructors
class GoodExample extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        ExpensiveWidget(),
        AnotherWidget(),
      ],
    );
  }
}

// GOOD: Extract static widgets
class OptimizedExample extends StatelessWidget {
  static const _staticWidget = ExpensiveWidget();

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _staticWidget,
        AnotherWidget(),
      ],
    );
  }
}
```

### 2. Efficient List Rendering

```dart
// BAD: Creates all widgets upfront
ListView(
  children: items.map((item) => ItemWidget(item)).toList(),
)

// GOOD: Lazy loading with builder
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ItemWidget(items[index]);
  },
)

// BEST: With separator and const
ListView.separated(
  itemCount: items.length,
  separatorBuilder: (context, index) => const Divider(),
  itemBuilder: (context, index) {
    return ItemWidget(items[index]);
  },
)
```

### 3. Image Optimization

```dart
// Cached network images
CachedNetworkImage(
  imageUrl: 'https://example.com/image.jpg',
  placeholder: (context, url) => const CircularProgressIndicator(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
  memCacheWidth: 600, // Resize in memory
  memCacheHeight: 600,
)

// Precache images
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  precacheImage(AssetImage('assets/large_image.png'), context);
}

// Use appropriate image formats
// WebP for better compression
// SVG for scalable graphics (flutter_svg package)
```

### 4. Memory Management

```dart
// Dispose controllers
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late ScrollController _scrollController;
  late StreamSubscription _subscription;

  @override
  void initState() {
    super.initState();
    _scrollController = ScrollController();
    _subscription = someStream.listen((data) {/* ... */});
  }

  @override
  void dispose() {
    _scrollController.dispose();
    _subscription.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListView(controller: _scrollController);
  }
}
```

### 5. Use RepaintBoundary

```dart
// Isolate expensive widgets from parent rebuilds
RepaintBoundary(
  child: ExpensiveAnimatedWidget(),
)

// Custom painter optimization
RepaintBoundary(
  child: CustomPaint(
    painter: MyComplexPainter(),
    child: Container(),
  ),
)
```

### 6. Async Operations

```dart
// Use compute for heavy calculations
Future<List<Photo>> fetchPhotos() async {
  final response = await http.get(Uri.parse('https://api.example.com/photos'));
  return compute(parsePhotos, response.body);
}

List<Photo> parsePhotos(String responseBody) {
  final parsed = jsonDecode(responseBody).cast<Map<String, dynamic>>();
  return parsed.map<Photo>((json) => Photo.fromJson(json)).toList();
}

// Use Isolates for long-running tasks
Future<void> runInIsolate() async {
  final result = await Isolate.run(() {
    // Heavy computation
    return heavyComputation();
  });
}
```

## Performance Best Practices

1. **Use const constructors** wherever possible
2. **Implement shouldRebuild** in custom painters
3. **Use keys** appropriately for list items
4. **Avoid** rebuilding entire widget trees
5. **Profile** with DevTools before optimizing
6. **Lazy load** data and widgets
7. **Cache** network images
8. **Dispose** resources properly
9. **Use ListView.builder** for long lists
10. **Minimize setState** scope

## Profiling with DevTools

```bash
# Run with performance profiling
flutter run --profile

# Use DevTools
flutter pub global activate devtools
flutter pub global run devtools

# Performance overlay in app
MaterialApp(
  showPerformanceOverlay: true,
  // ...
)
```

## Resources

- https://docs.flutter.dev/perf
- https://docs.flutter.dev/perf/best-practices
