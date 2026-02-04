---
name: flutter-reviewer
description: |
  WHEN: Flutter/Dart code review, Widget patterns, State management checks, BLoC/Provider/Riverpod analysis
  WHAT: Widget best practices + State management patterns + Performance optimization + Platform channel review
  WHEN NOT: Native Android → kotlin-android-reviewer, Native iOS → ios-reviewer
---

# Flutter Reviewer Skill

## Purpose
Reviews Flutter/Dart code for widget patterns, state management, performance, and cross-platform best practices.

## When to Use
- Flutter project code review
- "Widget", "BLoC", "Provider", "Riverpod", "GetX" mentions
- Flutter performance, rebuild optimization inspection
- Projects with `pubspec.yaml` containing flutter dependency

## Project Detection
- `pubspec.yaml` with `flutter:` dependency
- `lib/main.dart` exists
- `android/` and `ios/` directories present
- `.dart` files with Flutter imports

## Workflow

### Step 1: Analyze Project
```
**Flutter**: 3.x
**Dart**: 3.x
**State Management**: BLoC / Provider / Riverpod / GetX
**Architecture**: Clean Architecture / MVVM / MVC
**Null Safety**: Enabled
```

### Step 2: Select Review Areas
**AskUserQuestion:**
```
"Which areas to review?"
Options:
- Full Flutter pattern check (recommended)
- Widget build optimization
- State management patterns
- Platform channels/native code
- Navigation/routing patterns
multiSelect: true
```

## Detection Rules

### Widget Patterns
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Heavy logic in build() | Move to initState or separate method | HIGH |
| Missing const constructor | Add const for immutable widgets | HIGH |
| Unnecessary setState | Use state management for complex state | MEDIUM |
| Large build method | Extract to smaller widgets | MEDIUM |
| Missing key in ListView | Add key for correct item tracking | HIGH |

```dart
// BAD: Heavy logic in build
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final result = expensiveCalculation();  // Called every build
    return Text(result);
  }
}

// GOOD: Compute outside or cache
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  late String result;

  @override
  void initState() {
    super.initState();
    result = expensiveCalculation();
  }

  @override
  Widget build(BuildContext context) => Text(result);
}

// BAD: Missing const
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Container(
      child: Text('Hello'),  // Rebuilds unnecessarily
    );
  }
}

// GOOD: Use const
class MyWidget extends StatelessWidget {
  const MyWidget({super.key});

  @override
  Widget build(BuildContext context) {
    return const Text('Hello');  // Skipped in rebuilds
  }
}

// BAD: Missing key in ListView
ListView.builder(
  itemBuilder: (context, index) => ListTile(
    title: Text(items[index].name),
  ),
)

// GOOD: Add key
ListView.builder(
  itemBuilder: (context, index) => ListTile(
    key: ValueKey(items[index].id),
    title: Text(items[index].name),
  ),
)
```

### State Management - BLoC
| Check | Recommendation | Severity |
|-------|----------------|----------|
| BLoC without close | Memory leak risk | CRITICAL |
| emit after close | Runtime error risk | HIGH |
| Nested BlocBuilder | Use BlocSelector or MultiBlocListener | MEDIUM |
| Business logic in UI | Move to BLoC | MEDIUM |

```dart
// BAD: BLoC not closed
class MyWidget extends StatefulWidget {
  @override
  _MyWidgetState createState() => _MyWidgetState();
}

class _MyWidgetState extends State<MyWidget> {
  final bloc = MyBloc();

  @override
  Widget build(BuildContext context) => BlocBuilder...
  // Missing dispose!
}

// GOOD: Close BLoC
@override
void dispose() {
  bloc.close();
  super.dispose();
}

// Better: Use BlocProvider
BlocProvider(
  create: (context) => MyBloc(),
  child: MyWidget(),  // Auto-disposed
)

// BAD: Nested BlocBuilder
BlocBuilder<BlocA, StateA>(
  builder: (context, stateA) {
    return BlocBuilder<BlocB, StateB>(
      builder: (context, stateB) {
        return Text('${stateA.value} ${stateB.value}');
      },
    );
  },
)

// GOOD: Use MultiBlocListener or BlocSelector
MultiBlocListener(
  listeners: [
    BlocListener<BlocA, StateA>(...),
    BlocListener<BlocB, StateB>(...),
  ],
  child: Builder(
    builder: (context) {
      final a = context.watch<BlocA>().state;
      final b = context.watch<BlocB>().state;
      return Text('${a.value} ${b.value}');
    },
  ),
)
```

### State Management - Provider/Riverpod
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Provider not disposed | Memory leak | HIGH |
| ChangeNotifier without notifyListeners | UI not updated | HIGH |
| context.read in build | Use context.watch | HIGH |
| Missing ProviderScope | Riverpod won't work | CRITICAL |

```dart
// BAD: context.read in build (for reactive updates)
@override
Widget build(BuildContext context) {
  final value = context.read<MyProvider>().value;  // Won't rebuild!
  return Text(value);
}

// GOOD: context.watch for reactive
@override
Widget build(BuildContext context) {
  final value = context.watch<MyProvider>().value;
  return Text(value);
}

// BAD: Missing notifyListeners
class MyNotifier extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    // Missing notifyListeners()!
  }
}

// GOOD: Call notifyListeners
void increment() {
  _count++;
  notifyListeners();
}

// Riverpod: Missing ProviderScope
void main() {
  runApp(MyApp());  // Riverpod providers won't work!
}

// GOOD: Wrap with ProviderScope
void main() {
  runApp(
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

### Performance Optimization
| Check | Problem | Solution |
|-------|---------|----------|
| Unnecessary rebuilds | Performance | const, shouldRebuild, select |
| Heavy images | Memory/performance | cached_network_image, resize |
| Sync file I/O | UI jank | Use compute() or Isolate |
| AnimationController not disposed | Memory leak | Dispose in dispose() |

```dart
// BAD: Sync heavy operation
void loadData() {
  final data = File('large.json').readAsStringSync();
  final parsed = jsonDecode(data);  // Blocks UI!
}

// GOOD: Use compute/Isolate
Future<void> loadData() async {
  final data = await compute(parseJson, filePath);
}

// BAD: AnimationController leak
class _MyState extends State<MyWidget> with TickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this);
  }
  // Missing dispose!
}

// GOOD: Dispose controller
@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

### Platform Channels
| Check | Recommendation | Severity |
|-------|----------------|----------|
| Missing null check | Crash on null | HIGH |
| No error handling | Silent failures | MEDIUM |
| Main thread blocking | ANR/UI freeze | HIGH |
| Hard-coded channel name | Maintenance issue | LOW |

```dart
// BAD: No error handling
Future<String> getPlatformVersion() async {
  final version = await platform.invokeMethod('getVersion');
  return version;
}

// GOOD: Error handling
Future<String> getPlatformVersion() async {
  try {
    final version = await platform.invokeMethod<String>('getVersion');
    return version ?? 'Unknown';
  } on PlatformException catch (e) {
    return 'Failed: ${e.message}';
  }
}
```

## Response Template
```
## Flutter Code Review Results

**Project**: [name]
**Flutter**: 3.x | **Dart**: 3.x
**State Management**: BLoC/Provider/Riverpod
**Files Analyzed**: X

### Widget Patterns
| Status | File | Issue |
|--------|------|-------|
| HIGH | lib/screens/home.dart | Missing const constructor (line 45) |
| HIGH | lib/widgets/list_item.dart | Missing key in ListView |

### State Management
| Status | File | Issue |
|--------|------|-------|
| CRITICAL | lib/blocs/user_bloc.dart | BLoC not closed (line 23) |
| HIGH | lib/providers/cart.dart | Missing notifyListeners |

### Performance
| Status | File | Issue |
|--------|------|-------|
| HIGH | lib/services/data.dart | Sync file I/O blocking UI |
| MEDIUM | lib/screens/gallery.dart | Large images not cached |

### Recommended Actions
1. [ ] Add const to immutable widgets
2. [ ] Close BLoCs in dispose or use BlocProvider
3. [ ] Use compute() for heavy operations
4. [ ] Add keys to ListView items
```

## Best Practices
1. **Widgets**: Use const, extract small widgets, add keys
2. **State**: Choose appropriate state management, dispose resources
3. **Performance**: Avoid rebuilds, use isolates for heavy work
4. **Platform**: Handle errors, use typed method channels
5. **Testing**: Widget tests, golden tests, integration tests

## Integration
- `code-reviewer` skill: General Dart code quality
- `test-generator` skill: Flutter test generation
- `kotlin-android-reviewer` skill: Platform channel Android side
- `ios-reviewer` skill: Platform channel iOS side

## Notes
- Based on Flutter 3.x, Dart 3.x with null safety
- Supports BLoC, Provider, Riverpod, GetX patterns
- Includes platform channel best practices
