---
name: flutter-animating-apps
description: Implements animated effects, transitions, and motion in a Flutter app. Use when adding visual feedback, shared element transitions, or physics-based animations.
tags: [flutter, animation, implicit, explicit, hero, physics, staggered, transition]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Animations

## Contents
- [Animation Strategies](#animation-strategies)
- [Core Concepts](#core-concepts)
- [Workflow: Implementing Implicit Animations](#workflow-implementing-implicit-animations)
- [Workflow: Implementing Explicit Animations](#workflow-implementing-explicit-animations)
- [Workflow: Implementing Hero Transitions](#workflow-implementing-hero-transitions)
- [Workflow: Implementing Physics-Based Animations](#workflow-implementing-physics-based-animations)
- [Examples](#examples)

## Animation Strategies

Select the correct animation approach based on your requirements:

- **If animating simple property changes (size, color, opacity) without playback control:** Use **Implicit Animations** (`AnimatedContainer`, `AnimatedOpacity`, `TweenAnimationBuilder`).
- **If requiring playback control (play, pause, reverse, loop) or coordinating multiple properties:** Use **Explicit Animations** (`AnimationController` with `AnimatedBuilder` or `AnimatedWidget`).
- **If animating elements between two distinct routes:** Use **Hero Animations** (Shared Element Transitions).
- **If modeling real-world motion (e.g., snapping back after a drag):** Use **Physics-Based Animations** (`SpringSimulation`).
- **If animating a sequence of overlapping or delayed motions:** Use **Staggered Animations** (multiple `Tween`s driven by a single `AnimationController` using `Interval` curves).

## Core Concepts

- **`Animation<T>`**: Abstract representation of a value changing over time. Holds state (completed, dismissed) and notifies listeners.
- **`AnimationController`**: Drives the animation, generating values (0.0–1.0) tied to screen refresh rate. Always provide `vsync` (via `SingleTickerProviderStateMixin`). **Always `dispose()` controllers.**
- **`Tween<T>`**: Stateless mapping from input range (0.0–1.0) to an output type (`Color`, `Offset`, `double`). Chain with curves using `.animate()`.
- **`Curve`**: Non-linear timing (`Curves.easeIn`, `Curves.bounceOut`). Apply via `CurvedAnimation` or `CurveTween`.

## Workflow: Implementing Implicit Animations

Use for "fire-and-forget" state-driven animations.

- [ ] Identify the target properties to animate (e.g., width, color).
- [ ] Replace the static widget (e.g., `Container`) with its animated counterpart (e.g., `AnimatedContainer`).
- [ ] Define the `duration` property.
- [ ] (Optional) Define the `curve` property for non-linear motion.
- [ ] Trigger the animation by updating the properties inside a `setState()` or BLoC state emission.
- [ ] Run validator → review UI for jank → adjust duration/curve if necessary.

## Workflow: Implementing Explicit Animations

Use when you need granular control over the animation lifecycle.

- [ ] Add `SingleTickerProviderStateMixin` (or `TickerProviderStateMixin` for multiple controllers) to the `State` class.
- [ ] Initialize an `AnimationController` in `initState()`, providing `vsync: this` and a `duration`.
- [ ] Define a `Tween` and chain it to the controller using `.animate()`.
- [ ] Wrap the target UI in an `AnimatedBuilder` (preferred for complex trees) or subclass `AnimatedWidget`.
- [ ] Pass the `Animation` object to the `AnimatedBuilder`'s `animation` property.
- [ ] Control playback using `controller.forward()`, `controller.reverse()`, or `controller.repeat()`.
- [ ] **Call `controller.dispose()` in the `dispose()` method.**
- [ ] Run validator → check for memory leaks → ensure `dispose()` is called.

## Workflow: Implementing Hero Transitions

Use to fly a widget between two routes.

- [ ] Wrap the source widget in a `Hero` widget.
- [ ] Assign a unique, data-driven `tag` to the source `Hero`.
- [ ] Wrap the destination widget in a `Hero` widget.
- [ ] Assign the **exact same** `tag` to the destination `Hero`.
- [ ] Ensure the widget trees inside both `Hero` widgets are visually similar to prevent jarring jumps.
- [ ] Trigger the transition by pushing the destination route via `Navigator` or `context.go()`.

## Workflow: Implementing Physics-Based Animations

Use for gesture-driven, natural motion.

- [ ] Set up an `AnimationController` (do **not** set a fixed duration).
- [ ] Capture gesture velocity using a `GestureDetector` (e.g., `onPanEnd` providing `DragEndDetails`).
- [ ] Convert the pixel velocity to the coordinate space of the animating property.
- [ ] Instantiate a `SpringSimulation` with mass, stiffness, damping, and the calculated velocity.
- [ ] Drive the controller using `controller.animateWith(simulation)`.

## Examples

### Explicit Animation (Staggered with AnimatedBuilder)

```dart
class StaggeredAnimationDemo extends StatefulWidget {
  @override
  State<StaggeredAnimationDemo> createState() => _StaggeredAnimationDemoState();
}

class _StaggeredAnimationDemoState extends State<StaggeredAnimationDemo>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _widthAnimation;
  late Animation<Color?> _colorAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );

    // Staggered width animation (0.0 to 0.5 interval)
    _widthAnimation = Tween<double>(begin: 50.0, end: 200.0).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.0, 0.5, curve: Curves.easeIn),
      ),
    );

    // Staggered color animation (0.5 to 1.0 interval)
    _colorAnimation = ColorTween(begin: Colors.blue, end: Colors.red).animate(
      CurvedAnimation(
        parent: _controller,
        curve: const Interval(0.5, 1.0, curve: Curves.easeOut),
      ),
    );

    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose(); // CRITICAL: Prevent memory leaks
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        return Container(
          width: _widthAnimation.value,
          height: 50.0,
          color: _colorAnimation.value,
        );
      },
    );
  }
}
```

### Custom Page Route Transition

```dart
Route createCustomRoute(Widget destination) {
  return PageRouteBuilder(
    pageBuilder: (context, animation, secondaryAnimation) => destination,
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      const begin = Offset(0.0, 1.0); // Start from bottom
      const end = Offset.zero;
      const curve = Curves.easeOut;

      final tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));
      final offsetAnimation = animation.drive(tween);

      return SlideTransition(
        position: offsetAnimation,
        child: child,
      );
    },
  );
}

// Usage: Navigator.of(context).push(createCustomRoute(const NextPage()));
```

### Implicit Animation (AnimatedContainer)

```dart
class AnimatedBox extends StatefulWidget {
  const AnimatedBox({super.key});

  @override
  State<AnimatedBox> createState() => _AnimatedBoxState();
}

class _AnimatedBoxState extends State<AnimatedBox> {
  bool _expanded = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _expanded = !_expanded),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
        width: _expanded ? 200.0 : 100.0,
        height: _expanded ? 200.0 : 100.0,
        decoration: BoxDecoration(
          color: _expanded ? Colors.blue : Colors.red,
          borderRadius: BorderRadius.circular(_expanded ? 16.0 : 8.0),
        ),
      ),
    );
  }
}
```

## Anti-patterns

- ❌ Forgetting to call `dispose()` on `AnimationController` (memory leak)
- ❌ Using explicit animations when implicit animations suffice (over-engineering)
- ❌ Creating `AnimationController` in the `build` method (recreated every rebuild)
- ❌ Using `setState` for complex multi-property animations (use `AnimatedBuilder`)
- ❌ Mismatched `Hero` tags between source and destination routes

## Resources

- https://docs.flutter.dev/ui/animations
- https://docs.flutter.dev/ui/animations/implicit-animations
- https://docs.flutter.dev/ui/animations/hero-animations
- https://docs.flutter.dev/ui/animations/staggered-animations
- https://docs.flutter.dev/cookbook/animation
- https://api.flutter.dev/flutter/animation/AnimationController-class.html
