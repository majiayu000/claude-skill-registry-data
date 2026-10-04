---
name: flutter-caching-data
description: Implements caching strategies for Flutter apps to improve performance and offline support. Use when retaining app data locally to reduce network requests or speed up startup.
tags: [flutter, caching, offline-first, shared-preferences, image-cache, repository]
applies-to: [antigravity, cursor, copilot]
level: project
---

# Flutter Data Caching

## Contents
- [Selecting a Caching Strategy](#selecting-a-caching-strategy)
- [Offline-First Data Synchronization](#offline-first-data-synchronization)
- [Image Caching](#image-caching)
- [Widget and Scroll Caching](#widget-and-scroll-caching)
- [Workflows](#workflows)
- [Examples](#examples)

## Selecting a Caching Strategy

Apply the appropriate caching mechanism based on data lifecycle and size:

| Data Type | Solution |
|---|---|
| Small key-value (preferences, settings) | `shared_preferences` |
| Large structured datasets | SQLite (`sqflite`, `drift`), Hive CE, Isar |
| Binary data / large media files | File system via `path_provider` |
| User session state (scroll, navigation) | Flutter's built-in state restoration |
| Remote images | `cached_network_image` package |
| In-memory API responses | `Map` cache in Repository layer |

## Offline-First Data Synchronization

Design repositories as the single source of truth, combining local databases and remote API clients.

### Read Operations (Stream Approach)

Yield local data immediately for fast UI rendering, then fetch remote data, update local cache, and yield fresh data.

```dart
Stream<UserProfile> getUserProfile() async* {
  // 1. Yield local cache first
  final localProfile = await _databaseService.fetchUserProfile();
  if (localProfile != null) yield localProfile;

  // 2. Fetch remote, update cache, yield fresh data
  try {
    final remoteProfile = await _apiClientService.getUserProfile();
    await _databaseService.updateUserProfile(remoteProfile);
    yield remoteProfile;
  } catch (e) {
    // Handle network failure; UI already has local data
  }
}
```

### Write Operations

Select write strategy based on data criticality:

- **Online-only (strict sync required):** Attempt API call first. Only update local database if API succeeds.
- **Offline-first (availability prioritized):** Write to local database immediately. Attempt API call. If it fails, flag the local record for background sync.

### Background Synchronization

Add a `synchronized` boolean flag to data models. Run a periodic background task (e.g., via `workmanager` or a `Timer`) to push unsynchronized local changes to the server.

## Image Caching

Image I/O and decompression are expensive.

- **Use `cached_network_image`** to handle file-system caching of remote images.
- **Cache Sizing:** `ImageCache.maxByteSize` no longer automatically expands for large images. If loading large images, manually increase `ImageCache.maxByteSize`.
- **Prefer `const` constructors** on image widgets to allow framework rebuild short-circuiting.

```dart
CachedNetworkImage(
  imageUrl: 'https://example.com/avatar.jpg',
  placeholder: (context, url) => const CircularProgressIndicator(),
  errorWidget: (context, url, error) => const Icon(Icons.error),
  fit: BoxFit.cover,
)
```

## Widget and Scroll Caching

- **Scroll Cache Extent:** Configure caching for scrollable widgets using `cacheExtent` to preload items outside the visible viewport.
- **Avoid overriding `operator ==`** on Widget objects — causes O(N²) behavior during rebuilds.
  - **Exception:** Override only on leaf widgets (no children) where comparing properties is faster than rebuilding.
- **Prefer `const` constructors** to allow framework to short-circuit rebuilds automatically.

```dart
ListView.builder(
  cacheExtent: 500.0, // Preload 500 pixels of content beyond viewport
  itemCount: items.length,
  itemBuilder: (context, index) => ItemWidget(item: items[index]),
)
```

## Workflows

### Implementing an Offline-First Repository

- [ ] Define the data model with a `synchronized` boolean flag (default `false`).
- [ ] Implement the local `DatabaseService` (SQLite/Hive) with CRUD operations.
- [ ] Implement the remote `ApiClientService` for network requests.
- [ ] Create the `Repository` class combining both services.
- [ ] Implement read method returning a `Stream<T>` (yield local → fetch remote → update local → yield remote).
- [ ] Implement write method (write local → attempt remote → update `synchronized` flag).
- [ ] Implement a background sync function to process records where `synchronized == false`.
- [ ] Run validator → test offline behavior by disabling network.

### Implementing Image Caching

- [ ] Add `cached_network_image` to `pubspec.yaml`.
- [ ] Replace `Image.network()` calls with `CachedNetworkImage()`.
- [ ] Provide `placeholder` and `errorWidget` callbacks.
- [ ] (Optional) Configure custom `CacheManager` for cache duration and max objects.

## Examples

### File System Caching

```dart
import 'dart:io';
import 'package:path_provider/path_provider.dart';

class FileCache {
  Future<File> get _localFile async {
    // Use documents dir for persistent data
    final directory = await getApplicationDocumentsDirectory();
    return File('${directory.path}/cache.json');
  }

  Future<File> get _tempFile async {
    // Use temp dir for data the OS can clear
    final directory = await getTemporaryDirectory();
    return File('${directory.path}/temp_cache.json');
  }

  Future<String> readCache() async {
    final file = await _localFile;
    return file.readAsString();
  }

  Future<File> writeCache(String data) async {
    final file = await _localFile;
    return file.writeAsString(data);
  }
}
```

### Offline-First Repository with BLoC

```dart
class BookingRepository {
  BookingRepository({
    required DatabaseService databaseService,
    required BookingApi apiService,
  })  : _db = databaseService,
        _api = apiService;

  final DatabaseService _db;
  final BookingApi _api;

  Stream<List<Booking>> observeBookings() async* {
    // 1. Yield cached data immediately
    final local = await _db.getAllBookings();
    if (local.isNotEmpty) {
      yield local.map((m) => Booking.fromDbModel(m)).toList();
    }

    try {
      // 2. Fetch fresh data
      final remote = await _api.getBookings();
      // 3. Update local cache
      await _db.replaceAllBookings(remote);
      // 4. Yield fresh data
      yield remote.map((m) => Booking.fromApiModel(m)).toList();
    } on DioException catch (_) {
      // Network error — UI already has local data
    }
  }

  Future<void> createBooking(Booking booking) async {
    final dbModel = booking.toDbModel().copyWith(isSynced: false);
    // 1. Save locally immediately
    await _db.insertBooking(dbModel);

    try {
      // 2. Attempt remote sync
      await _api.createBooking(booking.toApiModel());
      await _db.updateBooking(dbModel.copyWith(isSynced: true));
    } on DioException catch (_) {
      // Leave as isSynced: false for background sync
    }
  }
}
```

## Anti-patterns

- ❌ Fetching remote data without checking local cache first (slow startup)
- ❌ Not handling network failures in offline-first reads (crashes on no internet)
- ❌ Using `Image.network()` for frequently loaded images (no caching)
- ❌ Overriding `operator ==` on widgets with children (O(N²) rebuilds)
- ❌ Missing `synchronized` flag on locally-written records (data loss risk)

## Resources

- https://docs.flutter.dev/cookbook/persistence/key-value
- https://docs.flutter.dev/cookbook/persistence/reading-writing-files
- https://pub.dev/packages/cached_network_image
- https://pub.dev/packages/shared_preferences
- https://pub.dev/packages/path_provider
- https://pub.dev/packages/hive
- https://pub.dev/packages/sqflite
