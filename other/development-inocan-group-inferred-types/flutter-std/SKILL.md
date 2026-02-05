---
name: flutter-std
description: Build and debug Flutter/Dart apps with Riverpod (codegen), Freezed, and GoRouter. Use when implementing Flutter features, running apps, hot reload/restart, or debugging UI.
---

# Flutter Std Tools

## When to use
- Use when the user is working on Flutter/Dart features, running the app, hot reload/restart, or debugging UI.
- Use when requests mention Riverpod, Freezed, GoRouter, or Flutter widget structure.

## Instructions
1) **Setup**: Ensure the project root is added via `dart___add_roots`. List devices with `dart___list_devices` before launching.
2) **Run & lifecycle**: Use `dart___launch_app` to run on a device. Use `dart___hot_reload` for UI changes (preserves state) and `dart___hot_restart` for logic/state resets. Avoid `flutter run` via shell. Stop apps with `dart___stop_app`.
3) **Debug & inspect**: Connect DTD with `dart___connect_dart_tooling_daemon` when needed. Use `dart___get_widget_tree`, `dart___get_runtime_errors`, and `dart___get_app_logs`.
4) **Testing & maintenance**: Run tests with `dart___run_tests`. Manage deps via `dart___pub`. Analyze/fix with `dart___analyze_files` and `dart___dart_fix`.
5) **Code generation**: `dart run build_runner build --delete-conflicting-outputs` (one-time) or `dart run build_runner watch --delete-conflicting-outputs` (watch).

## Requirements
### Architecture & tech stack
1) **State Management**: Must use **Riverpod** with code generation (`@riverpod`).
2) **Data Models**: Must use **Freezed** for immutable data classes and unions.
3) **Dependency Injection**: Must use **GetIt** and **Injectable** for service location.
4) **Routing**: Must use **GoRouter** for navigation (declarative routing).
5) **Database**: Must use **SQLite** for structured data storage.
6) **Widget State Structure (Stateful/Stateless)**: Follow the Widget State Structure section below and split widget classes into UI, Actions, and Utils extensions.

## Project Structure
- core/ - Core services and singletons
  - config/ - App configuration
  - di/ - Dependency injection setup (GetIt/Injectable)
  - routing/ - GoRouter configuration
  - utils/ - General utilities
- data/ - Data models and storage
  - consts/ - Constant definitions
  - models/ - Freezed data models
  - providers/ - Riverpod providers (using code generation)
  - repos/ - Data access layer
  - services/ - External services (API, Database, etc.)
- views/ - UI components and pages
  - pages/ - Main pages
  - widgets/ - Reusable widgets
  - pops/ - Popups and dialogs
- app.dart - App entry point widget
- main.dart - Main entry file

## Additional guidelines
- **Formatting**: Do NOT run `dart format`. Follow the project's existing code style.
- **Deprecations**: Replace all `Color.withOpacity` usage with `Color.withValues` (Flutter 3.27+).
- **Testing**: `utils` classes require unit test coverage.

# Widget State Structure (Stateful/Stateless)

To maintain clean and manageable code, split widget classes into three parts using `extensions` within the same file. This applies to both `StatefulWidget` (`State` class) and `StatelessWidget` (the widget class), separating UI from logic and event handling.

## Structure

1.  **UI**: The main `State` class containing the `build()` method and widget definitions.
2.  **Actions**: An extension on the `State` class for event handlers (e.g., `_onTap`, `_submit`).
3.  **Utils**: An extension on the `State` class for private helper methods and business logic.

## Example (StatefulWidget)

```dart
import 'package:flutter/material.dart';

class MyPage extends StatefulWidget {
  const MyPage({super.key});

  @override
  State<MyPage> createState() => _MyPageState();
}

// 1. UI - Main State Class
class _MyPageState extends State<MyPage> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Page')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: _controller,
              decoration: const InputDecoration(labelText: 'Enter text'),
            ),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: _onSubmit, // Reference to Actions extension
              child: const Text('Submit'),
            ),
          ],
        ),
      ),
    );
  }
}

// 2. Actions - Event Handlers
extension _MyPageActions on _MyPageState {
  void _onSubmit() {
    final text = _controller.text;
    if (_validateInput(text)) { // Reference to Utils extension
      _showSuccessDialog(text);
    } else {
      _showErrorSnackBar();
    }
  }

  void _showSuccessDialog(String text) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Success'),
        content: Text('You entered: $text'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}

// 3. Utils - Helper Methods & Logic
extension _MyPageUtils on _MyPageState {
  bool _validateInput(String text) {
    return text.isNotEmpty && text.length > 3;
  }

  void _showErrorSnackBar() {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Input must be at least 4 characters')),
    );
  }
}
```

## Example (StatelessWidget)

```dart
import 'package:flutter/material.dart';

class MyStatelessPage extends StatelessWidget {
  const MyStatelessPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Stateless Page')),
      body: Center(
        child: ElevatedButton(
          onPressed: () => _onSubmit(context), // Reference to Actions extension
          child: const Text('Submit'),
        ),
      ),
    );
  }
}

// 2. Actions - Event Handlers
extension _MyStatelessPageActions on MyStatelessPage {
  void _onSubmit(BuildContext context) {
    if (_validateInput('ok')) { // Reference to Utils extension
      _showSuccessDialog(context);
    } else {
      _showErrorSnackBar(context);
    }
  }

  void _showSuccessDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (_) => AlertDialog(
        title: const Text('Success'),
        content: const Text('Submitted.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}

// 3. Utils - Helper Methods & Logic
extension _MyStatelessPageUtils on MyStatelessPage {
  bool _validateInput(String text) {
    return text.isNotEmpty;
  }

  void _showErrorSnackBar(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Invalid input')),
    );
  }
}
```

## Example prompts
- "Run the flutter app on the iOS simulator"
- "Hot reload the app to show the new colors"
- "Create a new Riverpod provider for user authentication using code gen"
- "Implement a settings page using the project's existing preferences store"
- "Add a SQLite table for storing todo items"
- "Add a new route for the profile page using GoRouter"
- "Fix analysis errors in the project"
- "Generate a Freezed model for User with name and age fields"
