---
name: libgdx-collections-json
description: Use when writing libGDX Java/Kotlin code involving collections (Array, ObjectMap, ObjectSet, Queue), object pooling (Pool, DefaultPool), JSON serialization (Json, JsonReader, JsonValue), I18NBundle localization, Timer scheduling, or utility classes (Align, Scaling, TimeUtils, AsyncExecutor). Use when debugging GC pressure, missing identity parameter, wrong map iteration, pooling leaks, JSON parse errors, or java.util vs libGDX collection misuse.
---

# libGDX Collections, Pooling, JSON & Utilities

Quick reference for `com.badlogic.gdx.utils.*` — libGDX's GC-friendly collections, object pooling, JSON serialization, and utility classes. These replace `java.util.*` equivalents to reduce garbage collection pressure, especially on Android.

## Array\<T\> — ArrayList Replacement

```java
Array<String> arr = new Array<>();                   // also: new Array<>(capacity), new Array<>(ordered, capacity)
```

Public fields: `T[] items` (backing array), `int size` (element count), `boolean ordered`.

Key methods: `add`, `get`, `set`, `insert`, `swap`, `pop`, `peek`, `first`, `clear`, `sort`, `reverse`, `shuffle`, `truncate`, `shrink`, `ensureCapacity`, `isEmpty`, `notEmpty`, `select(predicate)`.

**CRITICAL — identity parameter required:** `removeValue(item, identity)`, `contains(item, identity)`, `indexOf(item, identity)`, `lastIndexOf(item, identity)`. `identity=true` uses `==`, `identity=false` uses `.equals()`. There is no single-argument overload.

**There is NO `remove(Object)` method.** It is `removeValue(value, identity)` or `removeIndex(int)`.

**Gotchas:**
- `items` array may be larger than `size` — iterate with `for (int i = 0; i < arr.size; i++)`, **never** `items.length`.
- `items[i]` past `size` contains stale references — always check `i < size`.
- DO NOT modify Array during `for-each` iteration. Use `DelayedRemovalArray`, `SnapshotArray`, or manual index loop.
- When `ordered` is `false`, `removeIndex()` swaps the last element into the gap (O(1)) instead of shifting (O(n)).

## DelayedRemovalArray\<T\> / SnapshotArray\<T\>

Both wrap `begin()`/`end()` around iteration. **DelayedRemovalArray** queues removals during iteration, applies at `end()` (returns `void` from `begin()`). **SnapshotArray** takes a snapshot; `begin()` returns `T[]` to iterate, modifications go to a copy. Both support nested `begin()`/`end()`. Used internally by Scene2D.

## ObjectMap\<K,V\> — HashMap Replacement

```java
ObjectMap<String, Integer> map = new ObjectMap<>();
map.put("hp", 100);                                  // returns old value or null
map.get("hp");  map.get("hp", 0);                    // null or default
map.remove("hp");  map.containsKey("hp");
map.containsValue(100, false);                        // identity param on values too
```

`size` is a **public field** (not a method). Iterate via `for (Entry e : map)`, `map.keys()`, `map.values()`, or `map.entries()`.

**Gotchas:**
- **Same Entry instance is reused** on each `next()` call. Do not store entry references.
- **Iterators are pooled** by default (`Collections.allocateIterators = false`). Nested iteration on the same map throws `GdxRuntimeException`. Set `Collections.allocateIterators = true` if needed.
- **There is no `entrySet()`/`keySet()`** — use `entries()`, `keys()`, `values()` (libGDX iterator types).

**OrderedMap\<K,V\>** — extends `ObjectMap`, maintains insertion order. `orderedKeys()` returns internal `Array<K>`.

## Primitive-Key Maps (Avoid Boxing)

`IntMap<V>`, `LongMap<V>` — object values, `get()` returns null if missing. `IntIntMap`, `ObjectIntMap<K>`, `ObjectFloatMap<K>` — primitive values, **`get()` MUST provide default** (no null for primitives). `ObjectIntMap` has `getAndIncrement(key, defaultValue, increment)`.

Primitive-value maps: `put()` returns `void` (not old value). Use `put(key, value, defaultValue)` overload to get old value.

## Sets

`ObjectSet<T>` — `add`, `remove`, `contains` (NO identity param, unlike Array). `first()` throws if empty. `OrderedSet<T>` — maintains insertion order, `orderedItems()` returns internal `Array<T>`. `IntSet` — primitive int, does NOT implement `Iterable`. `size` is a public field on all sets.

## Queue\<T\> — Double-Ended Queue

`addLast`/`addFirst`, `removeFirst`/`removeLast`, `first()`/`last()` (peek), `get(index)`. `size` is a public field.

## Pooling

### Pool\<T\> and DefaultPool\<T\>

`Pool<T>` is abstract — override `newObject()`. Methods: `obtain()`, `free(obj)` (calls `reset()` if `Pool.Poolable`), `fill(n)`, `getFree()`, `clear()`. Constructor: `Pool(initialCapacity, max)`.

**DefaultPool\<T\>** (since 1.13.5) — preferred. Uses supplier: `new DefaultPool<>(Bullet::new)` or `new DefaultPool<>(Bullet::new, 16, 100)`. No reflection, GWT-safe.

Implement `Pool.Poolable` for automatic `reset()` on `free()`.

### PoolManager — Shared Pool Registry (since 1.14.0)

```java
PoolManager pools = new PoolManager();
pools.addPool(Bullet.class, Bullet::new);            // or pass a Pool directly
Bullet b = pools.obtain(Bullet.class);
pools.free(b);                                        // looks up pool by object's class
```

### Deprecated Pooling APIs

- **DO NOT use `ReflectionPool`** (deprecated 1.13.5) — use `DefaultPool`.
- **DO NOT use `Pools`** (deprecated 1.14.0) — use `DefaultPool` or `PoolManager`.

## JSON

### Json — Serializer/Deserializer

```java
Json json = new Json();
json.setOutputType(JsonWriter.OutputType.json);       // json | javascript | minimal
json.setIgnoreUnknownFields(true);                    // don't fail on extra fields
json.setUsePrototypes(false);                         // write all fields, not just changed
String str = json.toJson(myObject);                   // serialize
MyClass obj = json.fromJson(MyClass.class, jsonStr);  // deserialize (also accepts FileHandle)
```

**There is no `Json.parse()` method.** Use `JsonReader` for raw parsing or `Json.fromJson()` for typed deserialization.

Custom serializer: `json.setSerializer(MyClass.class, new Json.Serializer<MyClass>() { ... })` — implement `write(Json, T, Class)` and `read(Json, JsonValue, Class)`.

### JsonReader — Raw Parsing to Tree

`new JsonReader().parse(fileHandle)` or `.parse(string)` returns `JsonValue` tree.

### JsonValue — DOM Tree Navigation

Navigation: `get("name")` / `get(index)` returns child `JsonValue` (null if not found). `has("name")`, `size` (public field). Type checks: `isObject()`, `isArray()`, `isString()`, `isNumber()`, `isBoolean()`, `isNull()`.

**`as*` vs `get*` — CRITICAL distinction:**
- `asString()`, `asInt()`, `asFloat()`, `asBoolean()` — converts **THIS** node's value.
- `getString("name")`, `getInt("hp")` — finds **child** by name, returns its value. Throws `IllegalArgumentException` if child not found. Use `getString("name", "default")` for safe defaults.

Iterate children: `for (JsonValue entry : root) { entry.name; entry.asString(); }` or `for (JsonValue c = root.child; c != null; c = c.next)`.

## I18NBundle — Localization

`I18NBundle.createBundle(fileHandle)` or `createBundle(fileHandle, locale)`. Methods: `get("key")`, `format("key", args...)`. Resolution: `messages_de_DE.properties` → `messages_de.properties` → `messages.properties`.

**There is no `I18NBundle.load()`** — use the static factory `I18NBundle.createBundle()`.

## Timer

```java
// Static convenience (uses global Timer.instance())
Timer.schedule(new Timer.Task() {
    public void run() { /* runs on GL thread */ }
}, 2f);                                               // delay seconds
Timer.schedule(task, 1f, 0.5f);                       // delay, then repeat every 0.5s forever
Timer.schedule(task, 1f, 0.5f, 5);                    // delay, interval, repeatCount

task.cancel();                                         // cancel a scheduled task
task.isScheduled();                                    // boolean
```

`Timer.Task` is abstract — override `run()`. **`run()` executes on the GL/render thread** (posted via `Gdx.app.postRunnable()`), safe for libGDX API calls.

Instance methods use `scheduleTask(task, ...)` (not `schedule`). The timer also has `stop()`, `start()`, `clear()`.

## Other Utilities

**TimeUtils:**
```java
long start = TimeUtils.nanoTime();
// ... work ...
long elapsed = TimeUtils.timeSinceNanos(start);       // nanoTime() - start
long ms = TimeUtils.millis();                          // System.currentTimeMillis()
long elapsedMs = TimeUtils.timeSinceMillis(startMs);
```

**Align** — bit-flag constants for layout alignment:
```java
Align.center      // 1       Align.topLeft      // top|left
Align.top         // 2       Align.topRight     // top|right
Align.bottom      // 4       Align.bottomLeft   // bottom|left
Align.left        // 8       Align.bottomRight  // bottom|right
Align.right       // 16
```

**Scaling** — abstract class with static instances (NOT an enum):
`Scaling.fit`, `Scaling.fill`, `Scaling.contain`, `Scaling.stretch`, `Scaling.fillX`, `Scaling.fillY`, `Scaling.stretchX`, `Scaling.stretchY`, `Scaling.none`.

**AsyncExecutor** — simple thread pool:
```java
AsyncExecutor executor = new AsyncExecutor(4);         // 4 threads
AsyncResult<String> result = executor.submit(() -> computeExpensiveThing());
if (result.isDone()) {
    String value = result.get();                       // blocks if not done, throws on error
}
executor.dispose();                                    // MUST dispose
```

`AsyncTask<T>` interface has a single `T call()` method. Executor must be disposed.

**ScreenUtils:**
```java
ScreenUtils.clear(0, 0, 0, 1);                        // r, g, b, a
ScreenUtils.clear(Color.BLACK);
ScreenUtils.clear(0, 0, 0, 1, true);                  // also clear depth buffer
```

## GWT Compatibility

libGDX collections are GWT-compatible while many `java.util` features are not. Prefer libGDX collections in cross-platform projects. For reflection on GWT, use `com.badlogic.gdx.utils.reflect.*` instead of `java.lang.reflect.*`.

## Common Mistakes

1. **Using `java.util.ArrayList` / `HashMap` / `HashSet`** — Use `Array`, `ObjectMap`, `ObjectSet` instead. libGDX collections reduce GC pressure and are GWT-compatible.
2. **Omitting the `identity` parameter** — `Array.contains()`, `indexOf()`, `removeValue()`, and `ObjectMap.containsValue()` require a boolean `identity` parameter. `true` = use `==`, `false` = use `.equals()`. There is no single-argument overload.
3. **Using `array.items.length` instead of `array.size`** — `items.length` is the backing array capacity. Elements past `size` are stale. Always use `size`.
4. **Calling `Array.remove(object)`** — This method does not exist. Use `removeValue(object, identity)` or `removeIndex(int)`.
5. **Iterating ObjectMap with `map.entrySet()`** — Does not exist. Use `map.entries()`, `map.keys()`, `map.values()`, or `for (Entry e : map)` directly. Same Entry instance is reused each iteration — do not store references.
6. **Nested iteration on the same map** — By default, iterators are pooled. Nested iteration throws `GdxRuntimeException`. Set `Collections.allocateIterators = true` to allow it.
7. **Using `Pools.obtain()` / `ReflectionPool`** — Both deprecated (1.14.0 / 1.13.5). Use `new DefaultPool<>(MyClass::new)` for local pools or `PoolManager` for shared pools.
8. **Calling `pool.obtain()` without `pool.free()`** — Defeats the purpose of pooling. Always pair obtain/free, ideally in try/finally.
9. **Calling `Json.parse()`** — Does not exist. Use `JsonReader.parse()` for raw `JsonValue` tree, or `Json.fromJson()` for typed deserialization.
10. **Confusing `getString("name")` with `asString()` on JsonValue** — `getString("name")` finds a child named "name" and returns its string value. `asString()` returns THIS node's value. Calling `getString()` on a node without matching children throws `IllegalArgumentException`.
11. **Assuming Timer runs on a background thread** — `Timer.Task.run()` executes on the GL/render thread via `postRunnable()`. Safe for libGDX API calls but do not block it.
12. **Using `I18NBundle.load()`** — Does not exist. Use the static factory `I18NBundle.createBundle()`.
