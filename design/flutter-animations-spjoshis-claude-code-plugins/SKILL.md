---
name: flutter-animations
description: Master Flutter animations including implicit, explicit, hero, and physics-based animations. Create smooth, performant UI transitions and custom animated widgets.
---

# Flutter Animations

Comprehensive guide to creating smooth, performant animations in Flutter using implicit animations, explicit animations, hero transitions, and custom animation patterns.

## When to Use This Skill

- Creating smooth UI transitions
- Implementing custom animations
- Building animated widgets
- Performance optimization for animations
- Hero animations between screens
- Physics-based animations
- Complex animation sequences
- Gesture-driven animations

## Core Animation Types

### 1. Implicit Animations (Recommended for Simple Cases)

```dart
// AnimatedContainer
class AnimatedContainerExample extends StatefulWidget {
  @override
  _AnimatedContainerExampleState createState() => _AnimatedContainerExampleState();
}

class _AnimatedContainerExampleState extends State<AnimatedContainerExample> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _expanded = !_expanded),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        width: _expanded ? 200 : 100,
        height: _expanded ? 200 : 100,
        decoration: BoxDecoration(
          color: _expanded ? Colors.blue : Colors.red,
          borderRadius: BorderRadius.circular(_expanded ? 50 : 10),
        ),
        child: const Center(child: Text('Tap me')),
      ),
    );
  }
}

// AnimatedOpacity
AnimatedOpacity(
  opacity: _visible ? 1.0 : 0.0,
  duration: const Duration(milliseconds: 500),
  child: Container(/* ... */),
)

// AnimatedAlign
AnimatedAlign(
  alignment: _aligned ? Alignment.topLeft : Alignment.bottomRight,
  duration: const Duration(milliseconds: 300),
  child: FlutterLogo(size: 50),
)
```

### 2. Explicit Animations (Full Control)

```dart
class ExplicitAnimationExample extends StatefulWidget {
  @override
  _ExplicitAnimationExampleState createState() => _ExplicitAnimationExampleState();
}

class _ExplicitAnimationExampleState extends State<ExplicitAnimationExample>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );

    _animation = Tween<double>(begin: 0, end: 300).animate(
      CurvedAnimation(
        parent: _controller,
        curve: Curves.easeInOut,
      ),
    );

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Container(
          width: _animation.value,
          height: _animation.value,
          color: Colors.blue,
        );
      },
    );
  }
}
```

### 3. Hero Animations

```dart
// Source screen
class SourceScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => Navigator.push(
        context,
        MaterialPageRoute(builder: (_) => DestinationScreen()),
      ),
      child: Hero(
        tag: 'hero-image',
        child: Image.network('https://example.com/image.jpg'),
      ),
    );
  }
}

// Destination screen
class DestinationScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detail')),
      body: Center(
        child: Hero(
          tag: 'hero-image',
          child: Image.network('https://example.com/image.jpg'),
        ),
      ),
    );
  }
}
```

### 4. Custom Animated Widget

```dart
class FadeInWidget extends StatefulWidget {
  final Widget child;
  final Duration duration;

  const FadeInWidget({
    required this.child,
    this.duration = const Duration(milliseconds: 500),
  });

  @override
  _FadeInWidgetState createState() => _FadeInWidgetState();
}

class _FadeInWidgetState extends State<FadeInWidget>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(duration: widget.duration, vsync: this);
    _animation = Tween<double>(begin: 0, end: 1).animate(_controller);
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return FadeTransition(
      opacity: _animation,
      child: widget.child,
    );
  }
}
```

### 5. Staggered Animations

```dart
class StaggeredAnimation extends StatelessWidget {
  final Animation<double> controller;
  late final Animation<double> opacity;
  late final Animation<double> width;
  late final Animation<EdgeInsets> padding;

  StaggeredAnimation({required this.controller}) {
    opacity = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(
        parent: controller,
        curve: const Interval(0.0, 0.3, curve: Curves.ease),
      ),
    );

    width = Tween<double>(begin: 50.0, end: 150.0).animate(
      CurvedAnimation(
        parent: controller,
        curve: const Interval(0.3, 0.6, curve: Curves.ease),
      ),
    );

    padding = EdgeInsetsTween(
      begin: const EdgeInsets.only(bottom: 16),
      end: const EdgeInsets.only(bottom: 75),
    ).animate(
      CurvedAnimation(
        parent: controller,
        curve: const Interval(0.6, 1.0, curve: Curves.ease),
      ),
    );
  }

  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: controller,
      builder: (context, child) {
        return Container(
          padding: padding.value,
          child: Opacity(
            opacity: opacity.value,
            child: Container(
              width: width.value,
              height: width.value,
              color: Colors.blue,
            ),
          ),
        );
      },
    );
  }
}
```

### 6. Physics-Based Animations

```dart
class PhysicsAnimationExample extends StatefulWidget {
  @override
  _PhysicsAnimationExampleState createState() => _PhysicsAnimationExampleState();
}

class _PhysicsAnimationExampleState extends State<PhysicsAnimationExample>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      lowerBound: 0,
      upperBound: 500,
    );
  }

  void _runAnimation() {
    _controller.animateWith(
      SpringSimulation(
        const SpringDescription(
          mass: 1,
          stiffness: 100,
          damping: 10,
        ),
        0,
        500,
        0,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: _runAnimation,
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Transform.translate(
            offset: Offset(0, _controller.value),
            child: Container(
              width: 100,
              height: 100,
              color: Colors.blue,
            ),
          );
        },
      ),
    );
  }
}
```

## Best Practices

1. **Use const constructors** for child widgets in animations
2. **Dispose controllers** properly to avoid memory leaks
3. **Use AnimatedBuilder** instead of setState for better performance
4. **Prefer implicit animations** for simple cases
5. **Use TweenAnimationBuilder** for custom animations without controllers
6. **Test animations** on real devices for performance
7. **Limit simultaneous animations** to avoid jank
8. **Use RepaintBoundary** to isolate expensive repaints

## Resources

- https://docs.flutter.dev/development/ui/animations
- https://flutter.dev/docs/development/ui/animations/tutorial
