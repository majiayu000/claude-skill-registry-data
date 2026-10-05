---
name: dart
description: Dart programming language — isolates, streams, futures, null safety, records and patterns, FFI, pub package manager, and Flutter integration.
trigger: dart, dart lang, dart ffi, dart futures, dart isolates, dart streams, pub, dart convert, dart io, dart async
---

# Dart

## Isolates
Dart uses isolates for concurrency — independent workers with their own memory heap. Communicate via `SendPort` / `ReceivePort` message passing. No shared state, no data races.

## Asynchronous: Futures and Streams
Futures represent single async values with `.then()` and `async`/`await`. Streams emit sequences of values over time, supporting `listen()`, `map()`, `where()`, and `async*` generators.

## Null Safety
Sound null safety is enforced at compile time. Types are non-nullable by default. Use `?` for nullable types, `late` for delayed initialization, and `!` for null assertion.

## Records and Patterns
Records are lightweight anonymous data aggregates (`(name, age)`). Patterns enable destructuring in variable declarations, switch expressions, and collection matching.

## Dart FFI
`dart:ffi` provides C-language interop. Define native types, call external functions, manage memory manually. Supports ABI-specific types and handle-based APIs.

## Pub Package Manager
`pub add`, `pub get`, `pub publish`. Packages hosted on `pub.dev`. Supports semantic versioning, lockfiles, and workspace-style packages.

## Flutter Integration
Dart is the language of Flutter. Key libraries like `dart:ui`, `package:flutter/material.dart`, and platform channels are designed around Dart's reactive model.

## dart:convert
Built-in JSON, UTF-8, Base64, and LineSplitter encoders/decoders. `jsonDecode` / `jsonEncode` for serialization. Support for codec chaining.
