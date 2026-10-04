---
name: flutter-working-with-databases
description: Manages local data persistence using SQLite or other database solutions. Use when a Flutter app needs to store, query, or synchronize large amounts of structured data on the device.
tags: [flutter, database, sqlite, sqflite, persistence, local-storage, drift, hive]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Databases & Local Persistence

## Contents
- [Selecting a Database Solution](#selecting-a-database-solution)
- [Architecture: Services and Repositories](#architecture-services-and-repositories)
- [SQLite Implementation](#sqlite-implementation)
- [Caching Strategies](#caching-strategies)
- [Workflows](#workflows)
- [Examples](#examples)

## Selecting a Database Solution

| Requirement | Solution |
|---|---|
| Simple key-value storage | `shared_preferences` |
| Relational data with complex queries | `sqflite` or `drift` |
| NoSQL / document storage | `hive_ce` or `isar_community` |
| Remote images | `cached_network_image` |
| API response caching | In-memory `Map` in repository |

### Decision Criteria

- **If data is small, non-critical (UI preferences, settings):** Use `shared_preferences`.
- **If data is structured with relationships and requires SQL queries:** Use `sqflite` (raw SQL) or `drift` (type-safe ORM with code gen).
- **If data is schema-less or frequently changing structure:** Use `hive_ce`.
- **If prioritizing speed and minimal boilerplate:** Use `isar_community`.

## Architecture: Services and Repositories

Follow Clean Architecture separation. Never access databases directly from the UI or BLoC layer.

### Services (Data Sources)
- Stateless wrappers around external data sources (SQLite, HTTP, platform plugins).
- No business logic — only raw CRUD operations.
- Return raw data models.

### Repositories (Single Source of Truth)
- Consume Services as private dependencies.
- Handle caching, offline sync, and retry logic.
- Transform raw data models into **Domain Models** (clean, UI-focused).
- Expose methods to Cubits/Blocs.

### Domain Models
- Immutable data classes (using `freezed`).
- Strip backend-specific fields (metadata, pagination tokens).

## SQLite Implementation

Use `sqflite` for relational data. Follow these rules:

- Add `sqflite` and `path` packages.
- Use `path` package to define storage location safely across platforms.
- Define table schemas using **constants** to prevent typos.
- Use `id` as primary key with `AUTOINCREMENT`.
- **Always use `whereArgs`** in SQL queries to prevent SQL injection.

```dart
// ✅ SAFE: Use whereArgs
await db.update(
  'records',
  record.toMap(),
  where: 'id = ?',
  whereArgs: [record.id],
);

// ❌ NEVER: String interpolation in SQL
await db.update(
  'records',
  record.toMap(),
  where: 'id = ${record.id}', // SQL INJECTION RISK
);
```

## Caching Strategies

### Online-Only Writes (Strict Sync)

```
User Action → API Call → Success? → Update Local DB → Emit State
                       → Failure? → Show Error
```

### Offline-First Writes

```
User Action → Write to Local DB (synced: false) → Attempt API Call
           → API Success? → Update DB (synced: true)
           → API Failure? → Leave synced: false for background sync
```

## Workflows

### Implementing a New Data Feature

- [ ] Define the Domain Model (immutable, UI-focused, using `freezed`).
- [ ] Define the API/DB raw data models.
- [ ] Create or update the Service(s) for raw data fetching/storage.
- [ ] Create the Repository, injecting Services as private dependencies.
- [ ] Map raw Service models to Domain Models within the Repository.
- [ ] Expose Repository methods to the Cubit/Bloc.
- [ ] Run validator → review errors → fix.

### Implementing SQLite Persistence

- [ ] Add `sqflite` and `path` dependencies.
- [ ] Define table name and column constants.
- [ ] Update `onCreate` or `onUpgrade` to execute `CREATE TABLE`.
- [ ] Implement `insert`, `query`, `update`, `delete` in the Database Service.
- [ ] Inject Database Service into the target Repository.
- [ ] Ensure Repository calls `database.open()` before executing queries.

### Database Migration

- [ ] Increment the database `version` number.
- [ ] Implement `onUpgrade` callback with migration SQL.
- [ ] Test migration from previous version → new version.
- [ ] Test fresh install (only `onCreate` runs).

## Examples

### SQLite Database Service

```dart
class TodoDatabaseService {
  static const String _tableName = 'todos';
  static const String _colId = 'id';
  static const String _colTitle = 'title';
  static const String _colIsSynced = 'is_synced';

  Database? _database;

  Future<void> open() async {
    if (_database != null) return;

    final dbPath = join(await getDatabasesPath(), 'app_database.db');
    _database = await openDatabase(
      dbPath,
      version: 1,
      onCreate: (db, version) {
        return db.execute(
          'CREATE TABLE $_tableName('
          '$_colId INTEGER PRIMARY KEY AUTOINCREMENT, '
          '$_colTitle TEXT, '
          '$_colIsSynced INTEGER DEFAULT 0)',
        );
      },
    );
  }

  Future<List<Map<String, dynamic>>> getAllTodos() async {
    return await _database!.query(_tableName);
  }

  Future<int> insertTodo(Map<String, dynamic> todo) async {
    return await _database!.insert(_tableName, todo);
  }

  Future<void> updateTodo(int id, Map<String, dynamic> todo) async {
    await _database!.update(
      _tableName,
      todo,
      where: '$_colId = ?',
      whereArgs: [id],
    );
  }

  Future<void> deleteTodo(int id) async {
    await _database!.delete(
      _tableName,
      where: '$_colId = ?',
      whereArgs: [id],
    );
  }

  Future<List<Map<String, dynamic>>> getUnsyncedTodos() async {
    return await _database!.query(
      _tableName,
      where: '$_colIsSynced = ?',
      whereArgs: [0],
    );
  }
}
```

### Offline-First Repository

```dart
class TodoRepository {
  TodoRepository({
    required TodoDatabaseService databaseService,
    required TodoApi apiService,
  })  : _db = databaseService,
        _api = apiService;

  final TodoDatabaseService _db;
  final TodoApi _api;

  /// Stream: yields local first, then fetches remote.
  Stream<List<Todo>> observeTodos() async* {
    final localTodos = await _db.getAllTodos();
    if (localTodos.isNotEmpty) {
      yield localTodos.map((m) => Todo.fromMap(m)).toList();
    }

    try {
      final remoteTodos = await _api.getTodos();
      // Update local cache
      for (final todo in remoteTodos) {
        await _db.insertTodo(todo.toMap()..['is_synced'] = 1);
      }
      yield remoteTodos;
    } on DioException catch (_) {
      // Network error — UI already has local data
    }
  }

  /// Offline-first write: save locally, attempt sync.
  Future<void> createTodo(Todo todo) async {
    final localId = await _db.insertTodo(
      todo.toMap()..['is_synced'] = 0,
    );

    try {
      final remoteTodo = await _api.createTodo(todo);
      await _db.updateTodo(localId, remoteTodo.toMap()..['is_synced'] = 1);
    } on DioException catch (_) {
      // Stays unsynced for background sync
    }
  }
}
```

## Anti-patterns

- ❌ Using string interpolation in SQL `where` clauses (SQL injection)
- ❌ Accessing the database directly from widgets or BLoC (bypass repository)
- ❌ Opening a new database connection per query (use singleton)
- ❌ Missing `onUpgrade` handler when changing schema (crashes on update)
- ❌ Storing large binary data in SQLite (use file system instead)
- ❌ Not closing the database when the app is disposed

## Resources

- https://docs.flutter.dev/cookbook/persistence/sqlite
- https://pub.dev/packages/sqflite
- https://pub.dev/packages/drift
- https://pub.dev/packages/hive
- https://pub.dev/packages/path_provider
- https://pub.dev/packages/shared_preferences
