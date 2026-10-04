---
name: flutter-implementing-navigation-and-routing
description: Handles routing, navigation, and deep linking in a Flutter application. Use when moving between screens or setting up URL-based navigation.
tags: [flutter, navigation, routing, deep-linking, go-router]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Navigation & Routing

## Contents
- [Core Concepts](#core-concepts)
- [Implementing Imperative Navigation](#implementing-imperative-navigation)
- [Implementing Declarative Navigation](#implementing-declarative-navigation)
- [Implementing Nested Navigation](#implementing-nested-navigation)
- [Workflows](#workflows)
- [Examples](#examples)

## Core Concepts
- **Routes:** In Flutter, screens and pages are referred to as *routes*. A route is simply a widget.
- **Navigator vs. Router:**
  - Use `Navigator` (Imperative) for small applications without complex deep linking requirements.
  - Use `Router` (Declarative) for applications with advanced navigation, web URL synchronization, and deep linking.
- **Deep Linking:** Allows an app to open directly to a specific location based on a URL. Supported on iOS, Android, and Web.
- **Named Routes:** Avoid using named routes (`MaterialApp.routes` and `Navigator.pushNamed`) for most applications. They have rigid deep linking behavior and do not support the browser forward button. Use `go_router` instead.

## Implementing Imperative Navigation
Use the `Navigator` widget to push and pop routes using platform-specific transition animations.

### Pushing and Popping
- Navigate to a new route using `Navigator.push(context, route)`.
- Return to the previous route using `Navigator.pop(context)`.
- Use `Navigator.pushReplacement()` to replace the current route, or `Navigator.pushAndRemoveUntil()` to clear the stack.

### Passing and Returning Data
- **Sending Data:** Pass data directly into the constructor of the destination widget. Alternatively, pass data via `RouteSettings(arguments: data)` and extract with `ModalRoute.of(context)!.settings.arguments`.
- **Returning Data:** Pass the return value to `Navigator.pop(context, resultData)`. Await the result: `final result = await Navigator.push(...)`.

## Implementing Declarative Navigation
For apps requiring deep linking, web URL support, or complex routing, use `go_router`.

- Switch from `MaterialApp` to `MaterialApp.router`.
- Define a router configuration that parses route paths and configures the `Navigator` automatically.
- Navigate using `context.go('/path')`.
- **Page-backed vs. Pageless Routes:** Declarative routes are *page-backed* (deep-linkable). Imperative pushes (e.g., dialogs) are *pageless*.

## Implementing Nested Navigation
Implement nested navigation for sub-flows (e.g., multi-step setup, persistent bottom navigation tabs).

- Instantiate a new `Navigator` widget inside the host widget.
- Assign a `GlobalKey<NavigatorState>` to control it programmatically.
- Implement `onGenerateRoute` within the nested `Navigator` to resolve sub-routes.
- Intercept hardware back button presses using `PopScope`.

## Workflows

### Standard Screen Transition
- [ ] Create the destination widget (Route).
- [ ] Define required data parameters in the destination widget's constructor.
- [ ] Implement `Navigator.push()` in the source widget.
- [ ] Wrap the destination widget in a `MaterialPageRoute` or `CupertinoPageRoute`.
- [ ] Implement `Navigator.pop()` in the destination widget to return.

### Implementing Deep-Linkable Routing
- [ ] **If** the app is simple and requires no deep linking:
  - [ ] Use standard `MaterialApp` and `Navigator.push()`.
- [ ] **If** the app requires deep linking, web support, or complex flows:
  - [ ] Add the `go_router` package.
  - [ ] Change `MaterialApp` to `MaterialApp.router`.
  - [ ] Define the `GoRouter` configuration with all top-level routes.
  - [ ] Replace `Navigator.push()` with `context.go()` or `context.push()`.

### Creating a Nested Navigation Flow
- [ ] Define string constants for the nested route paths.
- [ ] Create a `GlobalKey<NavigatorState>` in the host widget's state.
- [ ] Return a `Navigator` widget in the host's `build` method, passing the key.
- [ ] Implement `onGenerateRoute` to map string paths to step widgets.
- [ ] Wrap the host `Scaffold` in a `PopScope` to handle back-button interceptions.
- [ ] Use `navigatorKey.currentState!.pushNamed()` to advance steps within the flow.

## Examples

### Passing Data via Constructor (Imperative)

```dart
class Todo {
  final String title;
  final String description;
  const Todo(this.title, this.description);
}

class TodosScreen extends StatelessWidget {
  final List<Todo> todos;
  const TodosScreen({super.key, required this.todos});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Todos')),
      body: ListView.builder(
        itemCount: todos.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(todos[index].title),
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                  builder: (context) => DetailScreen(todo: todos[index]),
                ),
              );
            },
          );
        },
      ),
    );
  }
}

class DetailScreen extends StatelessWidget {
  final Todo todo;
  const DetailScreen({super.key, required this.todo});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(todo.title)),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Text(todo.description),
      ),
    );
  }
}
```

### Nested Navigation Flow

```dart
class SetupFlow extends StatefulWidget {
  final String initialRoute;
  const SetupFlow({super.key, required this.initialRoute});

  @override
  State<SetupFlow> createState() => _SetupFlowState();
}

class _SetupFlowState extends State<SetupFlow> {
  final _navigatorKey = GlobalKey<NavigatorState>();

  void _exitSetup() => Navigator.of(context).pop();

  @override
  Widget build(BuildContext context) {
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, _) async {
        if (didPop) return;
        _exitSetup();
      },
      child: Scaffold(
        appBar: AppBar(title: const Text('Setup')),
        body: Navigator(
          key: _navigatorKey,
          initialRoute: widget.initialRoute,
          onGenerateRoute: _onGenerateRoute,
        ),
      ),
    );
  }

  Route<Widget> _onGenerateRoute(RouteSettings settings) {
    Widget page;
    switch (settings.name) {
      case 'step1':
        page = StepOnePage(
          onComplete: () => _navigatorKey.currentState!.pushNamed('step2'),
        );
        break;
      case 'step2':
        page = StepTwoPage(onComplete: _exitSetup);
        break;
      default:
        throw StateError('Unexpected route name: ${settings.name}!');
    }

    return MaterialPageRoute(
      builder: (context) => page,
      settings: settings,
    );
  }
}
```

## Resources

- https://docs.flutter.dev/ui/navigation
- https://docs.flutter.dev/ui/navigation/deep-linking
- https://docs.flutter.dev/cookbook/navigation/navigation-basics
- https://docs.flutter.dev/cookbook/navigation/named-routes
- https://docs.flutter.dev/cookbook/navigation/passing-data
- https://docs.flutter.dev/cookbook/navigation/navigate-with-arguments
- https://docs.flutter.dev/cookbook/effects/nested-nav
- https://docs.flutter.dev/learn/tutorial/navigation
