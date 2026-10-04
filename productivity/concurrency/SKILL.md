---
name: flutter-handling-concurrency
description: Executes long-running tasks in background isolates to keep the UI responsive. Use when performing heavy computations or parsing large datasets.
tags: [flutter, concurrency, isolates, async, performance]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Concurrency & Isolates

## Contents
- [Core Concepts](#core-concepts)
- [Decision Matrix: Async vs. Isolates](#decision-matrix-async-vs-isolates)
- [Workflows](#workflows)
- [Examples](#examples)

## Core Concepts
Dart utilizes a single-threaded execution model driven by an Event Loop. By default, all Flutter application code runs on the Main Isolate.

- **Asynchronous Operations (`async`/`await`):** Use for non-blocking I/O tasks (network requests, file access). The Event Loop continues processing other events while waiting for the `Future` to complete.
- **Isolates:** Dart's implementation of lightweight threads. Isolates possess their own isolated memory and do not share state. They communicate exclusively via message passing.
- **Main Isolate:** The default thread where UI rendering and event handling occur. Blocking this isolate causes UI freezing (jank).
- **Worker Isolate:** A spawned isolate used to offload CPU-bound tasks to prevent Main Isolate blockage.

## Decision Matrix: Async vs. Isolates

- **If** the task is I/O bound (e.g., HTTP request, database read) → **Use `async`/`await`** on the Main Isolate.
- **If** the task is CPU-bound but executes quickly (<16ms) → **Use `async`/`await`** on the Main Isolate.
- **If** the task is CPU-bound, takes significant time, and runs once → **Use `Isolate.run()`**.
- **If** the task requires continuous or repeated background processing → **Use `Isolate.spawn()` with `ReceivePort` and `SendPort`**.

## Workflows

### Implementing Standard Asynchronous UI
- [ ] Mark the data-fetching function with the `async` keyword.
- [ ] Return a `Future<T>` from the function.
- [ ] Use the `await` keyword to yield execution until the operation completes.
- [ ] Wrap the UI component in a `FutureBuilder<T>` (or `StreamBuilder` for streams).
- [ ] Handle `ConnectionState.waiting`, `hasError`, and `hasData` states within the builder.

### Offloading Short-Lived Heavy Computation
- [ ] Identify the CPU-bound operation blocking the Main Isolate.
- [ ] Extract the computation into a standalone callback function.
- [ ] Ensure the callback accepts exactly one required, unnamed argument.
- [ ] Invoke `Isolate.run()` passing the callback.
- [ ] `await` the result of `Isolate.run()` in the Main Isolate.

### Establishing Long-Lived Worker Isolates
- [ ] Instantiate a `ReceivePort` on the Main Isolate to listen for messages.
- [ ] Spawn the worker isolate using `Isolate.spawn()`, passing the `ReceivePort.sendPort`.
- [ ] In the worker isolate, instantiate its own `ReceivePort`.
- [ ] Send the worker's `SendPort` back to the Main Isolate.
- [ ] Implement listeners on both `ReceivePort` instances to handle incoming messages.
- [ ] Ensure ports are closed when the isolate is no longer needed.

## Examples

### Asynchronous UI with FutureBuilder

```dart
Future<String> fetchUserData() async {
  await Future.delayed(const Duration(seconds: 2));
  return "User Data Loaded";
}

Widget build(BuildContext context) {
  return FutureBuilder<String>(
    future: fetchUserData(),
    builder: (context, snapshot) {
      if (snapshot.connectionState == ConnectionState.waiting) {
        return const CircularProgressIndicator();
      } else if (snapshot.hasError) {
        return Text('Error: ${snapshot.error}');
      } else {
        return Text('Result: ${snapshot.data}');
      }
    },
  );
}
```

### Short-Lived Isolate (`Isolate.run`)

```dart
import 'dart:isolate';
import 'dart:convert';

List<dynamic> decodeHeavyJson(String jsonString) {
  return jsonDecode(jsonString) as List<dynamic>;
}

Future<List<dynamic>> processDataInBackground(String rawJson) async {
  final result = await Isolate.run(() => decodeHeavyJson(rawJson));
  return result;
}
```

### Long-Lived Isolate (`ReceivePort` / `SendPort`)

```dart
import 'dart:isolate';

class WorkerManager {
  late SendPort _workerSendPort;
  final ReceivePort _mainReceivePort = ReceivePort();
  Isolate? _isolate;

  Future<void> initialize() async {
    _isolate = await Isolate.spawn(_workerEntry, _mainReceivePort.sendPort);

    _mainReceivePort.listen((message) {
      if (message is SendPort) {
        _workerSendPort = message;
        _startCommunication();
      } else {
        print('Main Isolate received: $message');
      }
    });
  }

  void _startCommunication() {
    _workerSendPort.send("Process this data");
  }

  static void _workerEntry(SendPort mainSendPort) {
    final workerReceivePort = ReceivePort();
    mainSendPort.send(workerReceivePort.sendPort);

    workerReceivePort.listen((message) {
      print('Worker Isolate received: $message');
      final result = "Processed: $message";
      mainSendPort.send(result);
    });
  }

  void dispose() {
    _mainReceivePort.close();
    _isolate?.kill();
  }
}
```

## Resources

- https://docs.flutter.dev/perf/isolates
- https://docs.flutter.dev/get-started/fundamentals/dart
- https://docs.flutter.dev/resources/architectural-overview
- https://docs.flutter.dev/flutter-for/dart-swift-concurrency
- https://docs.flutter.dev/data-and-backend/serialization/json
- https://docs.flutter.dev/resources/bootstrap-into-dart
