---
name: libgdx-file-io-preferences
description: Use when writing libGDX Java/Kotlin code involving file I/O (FileHandle, Gdx.files, FileType) or persistent storage (Preferences). Use when debugging files not found, write failures on Android/iOS, wrong file paths across platforms, or preferences not persisting.
---

# libGDX File I/O & Preferences

Quick reference for `FileHandle`, `Files.FileType`, and `Preferences`. Covers file reading/writing, platform-specific path resolution, and persistent key-value storage.

## FileType Enum (`Files.FileType`)

Five values: `Classpath`, `Internal`, `External`, `Absolute`, `Local`.

| FileType | Writable | Description |
|---|---|---|
| `Classpath` | No | Java classpath resource. Most restrictive — no `list()`, no `isDirectory()`, no Android audio. |
| `Internal` | No | Asset directory. Falls back to classpath on desktop if file not found. |
| `External` | Yes | User/app external storage. |
| `Local` | Yes | App-private storage. |
| `Absolute` | Yes | Literal filesystem path. |

`Classpath` and `Internal` are **always read-only**. Writing throws `GdxRuntimeException`.

### Platform Path Resolution — WHERE Each FileType Points

| FileType | Desktop (LWJGL3) | Android | iOS (RoboVM) | GWT |
|---|---|---|---|---|
| `Internal` | Working dir, falls back to classpath | APK `assets/` via AssetManager | App bundle (`NSBundle.mainBundle`) | Preloaded assets |
| `Local` | Working dir (`new File("").getAbsolutePath()`) | `Context.getFilesDir()` (app private) | `$HOME/Library/local/` | **Not supported** (throws) |
| `External` | User home (`System.getProperty("user.home")`) | `Context.getExternalFilesDir(null)` (app-scoped) | `$HOME/Documents/` | **Not supported** (throws) |
| `Absolute` | Literal path | Literal path | Literal path | **Not supported** (throws) |
| `Classpath` | Classloader resource | Classloader resource | Classloader resource | Preloaded assets |

**Gotchas:**
- Android `External` uses `getExternalFilesDir(null)` (app-scoped, e.g. `/storage/emulated/0/Android/data/<pkg>/files/`). This does **NOT** require `WRITE_EXTERNAL_STORAGE` permission. Files are deleted on app uninstall. Older libGDX versions used `Environment.getExternalStorageDirectory()` which DID need the permission — that is no longer the case.
- Desktop `Local` and `Internal` both resolve relative to the JVM working directory. When launching from IntelliJ/Gradle, this may not be the `assets/` folder — configure the working directory in your run configuration.
- iOS `Local` and `External` are different paths (`Library/local/` vs `Documents/`), unlike what some documentation claims.
- GWT supports **only** `Internal` and `Classpath`. All other types throw `GdxRuntimeException`. GWT files are read-only.

## Gdx.files Methods

```java
FileHandle fh = Gdx.files.internal("data/map.tmx");   // FileType.Internal
FileHandle fh = Gdx.files.local("saves/slot1.json");   // FileType.Local
FileHandle fh = Gdx.files.external("screenshots/s.png"); // FileType.External
FileHandle fh = Gdx.files.absolute("/tmp/debug.log");  // FileType.Absolute
FileHandle fh = Gdx.files.classpath("com/lib/default.json"); // FileType.Classpath

// Storage queries
String path = Gdx.files.getExternalStoragePath();      // platform external root
String path = Gdx.files.getLocalStoragePath();          // platform local root
boolean ok  = Gdx.files.isExternalStorageAvailable();   // false on GWT, or if no SD card
boolean ok  = Gdx.files.isLocalStorageAvailable();      // false on GWT
```

`Gdx.files.classpath()` **does exist** — it is a real method on the `Files` interface. `Classpath` is a real `FileType` enum value. However, prefer `Internal` for game assets — `Classpath` cannot be used with Android audio, cannot list directories, and always reports `isDirectory() = false`.

**DO NOT** use `new FileHandle("path")` for cross-platform code — the public constructors create `Absolute` handles with no backend awareness. Always use `Gdx.files.*()`.

## FileHandle API

### Reading

```java
// Streams
InputStream is  = fh.read();                           // raw InputStream
BufferedInputStream bis = fh.read(bufferSize);          // buffered

// Readers
Reader r        = fh.reader();                          // platform default charset
Reader r        = fh.reader("UTF-8");                   // explicit charset
BufferedReader br = fh.reader(bufferSize);              // buffered, default charset
BufferedReader br = fh.reader(bufferSize, "UTF-8");     // buffered, explicit charset

// Bulk
String s        = fh.readString();                      // platform default charset
String s        = fh.readString("UTF-8");               // explicit charset
byte[] b        = fh.readBytes();                       // entire file
int n           = fh.readBytes(bytes, offset, size);    // into existing array, returns count

// Memory-mapped (not on Classpath or GWT)
ByteBuffer bb   = fh.map();                             // READ_ONLY mode
ByteBuffer bb   = fh.map(FileChannel.MapMode.READ_ONLY);
```

**Gotcha:** `readString()` without a charset uses the **platform default charset**, NOT UTF-8. On most modern JVMs this is UTF-8, but it's not guaranteed. Always pass `"UTF-8"` explicitly for cross-platform consistency.

### Writing

All write methods require `boolean append` — there is **no overload without it**.

```java
// Streams
OutputStream os = fh.write(false);                      // append=false → overwrite
OutputStream os = fh.write(true, bufferSize);           // buffered
fh.write(inputStream, false);                           // copies InputStream, closes it

// Writers
Writer w        = fh.writer(false);                     // platform default charset
Writer w        = fh.writer(false, "UTF-8");            // explicit charset

// Bulk
fh.writeString("data", false);                          // overwrite, default charset
fh.writeString("data", true, "UTF-8");                  // append, explicit charset
fh.writeBytes(bytes, false);                            // overwrite
fh.writeBytes(bytes, offset, length, false);            // slice
```

Writing to `Classpath` or `Internal` throws `GdxRuntimeException`. Parent directories are created automatically.

### Metadata

```java
String s   = fh.path();                    // full path, forward slashes
String s   = fh.name();                    // filename only ("map.tmx")
String s   = fh.extension();               // without dot ("tmx"), or "" if none
String s   = fh.nameWithoutExtension();    // "map"
String s   = fh.pathWithoutExtension();    // "data/map"
FileType t = fh.type();                    // FileType enum value

boolean b  = fh.exists();
boolean b  = fh.isDirectory();
long len   = fh.length();                  // bytes; 0 for dirs or non-existent
long ms    = fh.lastModified();            // millis; 0 for Classpath/Internal on Android

File f     = fh.file();                    // java.io.File — SEE WARNING BELOW
```

**WARNING:** `fh.file()` on Android `Internal` files returns a `File` with a relative path that does NOT point to an accessible filesystem location. Assets live inside the APK. The returned `File` will report `exists() = false`. Use `read()`/`readString()`/`readBytes()` instead. On GWT, `file()` throws `GdxRuntimeException`.

### Directory Operations

```java
FileHandle[] children = fh.list();                  // all children
FileHandle[] children = fh.list(".png");            // suffix filter (endsWith)
FileHandle[] children = fh.list(fileFilter);        // java.io.FileFilter
FileHandle[] children = fh.list(filenameFilter);    // java.io.FilenameFilter

FileHandle child   = fh.child("sub/file.txt");     // child path, same FileType
FileHandle parent  = fh.parent();                   // parent directory
FileHandle sibling = fh.sibling("other.txt");       // same parent, same FileType
```

`list()` returns an empty array (not null) when there are no children. Throws `GdxRuntimeException` for `Classpath`. On Android, `list()` for `Internal` files works via `AssetManager.list()`.

**Gotcha:** `exists()` for Internal directories on Android is extremely slow (tries `assets.open()`, catches exception, then calls `assets.list()`). The source code contains the comment "This is SUPER slow!" Empty Internal directories on Android report `isDirectory() = false`.

### File Operations

```java
fh.mkdirs();                       // create directory + parents (void)
fh.copyTo(destHandle);             // smart copy: file→file, file→dir, dir→dir (recursive)
fh.moveTo(destHandle);             // tries rename, falls back to copy+delete
boolean ok = fh.delete();          // file or empty directory only
boolean ok = fh.deleteDirectory(); // recursive delete
fh.emptyDirectory();               // delete all children (keeps the directory)
fh.emptyDirectory(true);           // delete files but preserve subdirectory structure
```

`mkdirs()`, `delete()`, `deleteDirectory()`, `emptyDirectory()` all throw `GdxRuntimeException` for `Classpath`/`Internal`.

### Static Utilities

```java
FileHandle tmp  = FileHandle.tempFile("prefix");       // Absolute type, system temp dir
FileHandle tmpd = FileHandle.tempDirectory("prefix");   // Absolute type, creates dir
```

These use `java.io.File.createTempFile()` internally. Not available on GWT.

## Preferences

Persistent key-value storage. Backed by platform-native mechanisms.

### Getting Preferences

```java
Preferences prefs = Gdx.app.getPreferences("com.mygame.settings");
```

The name **must be valid as a filename** (it becomes one on Desktop/iOS). Use reverse-domain naming to avoid collisions — all libGDX apps share the same `.prefs/` directory on desktop.

**DO NOT** call `getPreferences()` in a constructor or static initializer — `Gdx.app` is not initialized until `create()`.

### Put Methods (all return `Preferences` for chaining)

```java
prefs.putBoolean("sound", true)
     .putInteger("level", 5)
     .putLong("score", 999999L)
     .putFloat("volume", 0.8f)
     .putString("name", "Player1")
     .flush();                         // MUST call to persist!

prefs.put(Map.of("a", true, "b", 42)); // bulk put from Map<String, ?>
```

There is **no `putDouble()`**. Store doubles as strings or two floats.

### Get Methods

```java
boolean b = prefs.getBoolean("sound");              // default: false
boolean b = prefs.getBoolean("sound", true);        // explicit default
int i     = prefs.getInteger("level");              // default: 0
int i     = prefs.getInteger("level", 1);
long l    = prefs.getLong("score");                  // default: 0
float f   = prefs.getFloat("volume");               // default: 0
String s  = prefs.getString("name");                // default: "" (empty string, NOT null)
String s  = prefs.getString("name", "Unknown");
```

| No-default call | Returns |
|---|---|
| `getBoolean(key)` | `false` |
| `getInteger(key)` | `0` |
| `getLong(key)` | `0` |
| `getFloat(key)` | `0` |
| `getString(key)` | `""` (empty string) |

### Other Methods

```java
Map<String, ?> all = prefs.get();         // read-only map of all entries
boolean exists     = prefs.contains("key");
prefs.remove("key");                       // void
prefs.clear();                             // void
prefs.flush();                             // void — MUST call to persist changes
```

**There is no `save()`, `commit()`, or `apply()`** — it is `flush()`.

### flush() — Critical

`flush()` is the **only** way to persist changes to disk. Without it, all puts are lost when the app exits. There is no auto-flush on any platform.

```java
// WRONG — changes lost on exit:
prefs.putInteger("score", 100);

// CORRECT:
prefs.putInteger("score", 100);
prefs.flush();
```

### Preferences Storage Per Platform

| Platform | Storage Mechanism | Location |
|---|---|---|
| Desktop (LWJGL3) | Java `Properties` XML file | `~/.prefs/<name>` (configurable via `Lwjgl3ApplicationConfiguration.setPreferencesConfig()`) |
| Android | `SharedPreferences` | `/data/data/<pkg>/shared_prefs/<name>.xml` |
| iOS (RoboVM) | `NSMutableDictionary` → `.plist` | `~/Library/<name>.plist` |
| GWT | Browser `localStorage` | Keyed by `"<name>:<key><type>"` |
| Headless | Java `Properties` XML file | `~/.prefs/<name>` (same as desktop) |

**Gotchas:**
- Desktop: All libGDX apps share `~/.prefs/` — use unique names.
- iOS: Multiple `getPreferences()` calls with the same name return **independent instances** that do not share in-memory state. Get the instance once and reuse it.
- GWT: `localStorage` is typically limited to ~5 MB per origin.
- Preferences are **not thread-safe** on any platform.

## GWT File Restrictions Summary

| Feature | Supported on GWT? |
|---|---|
| `Gdx.files.internal()` | Yes (preloaded, read-only) |
| `Gdx.files.classpath()` | Yes (preloaded, read-only) |
| `Gdx.files.local()` | **No** — throws `GdxRuntimeException` |
| `Gdx.files.external()` | **No** — throws `GdxRuntimeException` |
| `Gdx.files.absolute()` | **No** — throws `GdxRuntimeException` |
| `fh.file()` | **No** — throws `GdxRuntimeException` |
| Any write operation | **No** — throws `GdxRuntimeException` |
| `fh.map()` | **No** — throws `GdxRuntimeException` |
| `Preferences` | Yes — uses browser `localStorage` |

On GWT, `Preferences` is the **only** way to persist data.

## Integration Notes

- **AssetManager** uses `Internal` files by default via `InternalFileHandleResolver`. Pass `LocalFileHandleResolver` or `ExternalFileHandleResolver` to the constructor to change this.
- For platform-specific file behavior details, see the backend skills: `libgdx-android-backend`, `libgdx-lwjgl3-desktop`, `libgdx-ios-robovm`.

## Common Mistakes

1. **Writing to Internal files** — `Gdx.files.internal("save.json").writeString(...)` throws `GdxRuntimeException`. Internal is read-only. Use `Gdx.files.local()` for writable app-private storage.
2. **Forgetting `flush()` on Preferences** — Without `flush()`, all puts are lost on app exit. There is no auto-flush, no `save()`, no `commit()`. The method is `flush()`.
3. **Using `java.io.File` or `java.nio.file.Path` instead of `FileHandle`** — Breaks on Android (assets are inside the APK) and iOS. Always use `Gdx.files.*()` for cross-platform code.
4. **Calling `fh.file()` on Android Internal files** — Returns a `File` with a relative path that doesn't exist on the filesystem. Use `fh.read()` / `fh.readString()` / `fh.readBytes()` instead.
5. **Omitting the `append` boolean on write methods** — `writeString(str, append)` requires the boolean. There is no overload without it. Use `false` to overwrite, `true` to append.
6. **Assuming `readString()` uses UTF-8** — It uses the platform default charset. Always pass `"UTF-8"` explicitly: `fh.readString("UTF-8")`.
7. **Confusing `Local` paths across platforms** — Desktop `Local` is the working directory (may not be where you expect in IDE). Android `Local` is `Context.getFilesDir()` (app-private). They are not the same concept.
8. **Calling `Gdx.files.*()` or `Gdx.app.getPreferences()` before `create()`** — `Gdx.files` and `Gdx.app` are null until the application is initialized. Access them in `create()` or later.
9. **Using `Gdx.files.external()` expecting shared storage on modern Android** — External maps to `getExternalFilesDir(null)` (app-scoped, deleted on uninstall). It is NOT shared public storage.
10. **Using file I/O on GWT** — Only `Internal`/`Classpath` reads and `Preferences` work. All writes, `local()`, `external()`, `absolute()`, and `file()` throw exceptions.
11. **Using `new FileHandle("path")` in cross-platform code** — The public constructors create `Absolute` handles with no backend awareness. The Javadoc warns: "Do not use this constructor in case you write something cross-platform."
12. **Not using unique Preferences names** — On desktop, all libGDX apps share `~/.prefs/`. A generic name like `"settings"` will collide. Use reverse-domain naming: `"com.mygame.settings"`.
