---
name: add-compare-viewer
description: >
  Add a new compare viewer tab to open-bc, wiring UI (Qt C++), Rust FFI shim,
  engine actor, and all required integration points (file-type routing, menus,
  session history, CLI, Home view). Use this skill whenever a user asks to add a
  new viewer kind (e.g. "PDF compare", "JSON diff viewer", "archive compare").
---

# Adding a New Compare Viewer to OpenBC

## Architecture Overview

OpenBC is a Rust/C++ hybrid. Data flows in one direction only:

```
openbc-vfs  ->  openbc-engine  ->  openbc-compute  ->  (result back to engine)
                    |
              tokio::sync::mpsc channel
                    |
            openbc-ui-qt (Rust FFI shim)
                    |
            EventCallback -> Qt GUI thread
                    |
            <Kind>CompareViewer (C++ QWidget)
```

**Crate responsibilities (DO NOT cross these boundaries):**

| Crate | Owns | Must NOT depend on |
|-------|------|--------------------|
| `openbc-core` | Domain types, pure diff algorithms, result types | Qt, Tokio, Rayon, wgpu, VFS |
| `openbc-vfs` | File system & remote adapters (`AsyncVfs`) | UI crates |
| `openbc-compute` | CPU (Rayon) / GPU (wgpu) heavy lifting | Qt, `openbc-ui-qt` |
| `openbc-engine` | Async Tokio orchestration, per-tab actors | (may use core, vfs, compute) |
| `openbc-ui-qt` | Qt bindings, C ABI shims, Qt viewer widgets | Never scan files itself |

---

## Step-by-Step Checklist

### 1. Domain types -- `openbc-core`

Create `crates/openbc-core/src/<kind>_compare/` (or `<kind>_compare.rs` if small) with:
- Options struct: `<Kind>CompareOptions`
- Result/view struct: `<Kind>View`
- Error type if domain-specific
- Pure diff algorithm (no I/O, no threads)

Register in `crates/openbc-core/src/lib.rs`:
```rust
pub mod <kind>_compare;
```

### 2. Compute backend -- `openbc-compute`

Only needed for heavy CPU (Rayon) or GPU (wgpu) work.

- Add `crates/openbc-compute/src/<kind>/mod.rs` or `<kind>.rs`
- Use `ComputeDispatcher` for GPU eligibility (`GPU_MIN_BYTES` = 4 MiB; never GPU below 1 MiB)
- Register in `crates/openbc-compute/src/lib.rs`: `pub mod <kind>;`

### 3. Engine actor -- `openbc-engine`

Create `crates/openbc-engine/src/<kind>_compare.rs`. Follow `BatchedActor` pattern (table, registry, media) or dedicated actor pattern (hex, image, model3d).

**Minimum interface:**
```rust
pub enum <Kind>Command { Reload, SetOptions(<Kind>CompareOptions), /* ... */ }

pub enum <Kind>Event {
    Status(String),
    Error(String),
    Result(Arc<<Kind>View>),
    // Progress { done: u64, total: u64 },
    // Saved { side: Side, path: PathBuf },
}

pub struct <Kind>CompareHandle { /* tx: Sender<<Kind>Command> */ }
impl <Kind>CompareHandle {
    pub fn send(&self, cmd: <Kind>Command) -> bool { /* channel send */ }
}

pub fn spawn_<kind>_compare(
    handle: &tokio::runtime::Handle,
    source: Arc<dyn ByteSource>,  // openbc-engine::common
    left: PathBuf,
    right: PathBuf,
) -> (<Kind>CompareHandle, tokio::sync::mpsc::Receiver<<Kind>Event>)
```

Register in `crates/openbc-engine/src/lib.rs`:
```rust
pub mod <kind>_compare;
```

**I/O and threading rules:**
- Read files through `ByteSource` (not `std::fs` directly)
- CPU-heavy work via `spawn_blocking` or `rayon::scope`
- Never hold a Tokio lock across blocking calls
- Channel size: bounded (4-8 events); backpressure intentional

### 4. Rust FFI shim -- `openbc-ui-qt/src/ffi/<kind>_compare.rs`

Follow the exact pattern from `table_compare.rs` / `hex_compare.rs`:

```rust
use super::common::*; // Sink, EV_*, runtime(), local_source(), path_arg(), out_str(), handle_ref!

pub struct <Kind>Session {
    handle: <Kind>CompareHandle,
    sink: Sink,
}

type ViewHandle = Arc<<Kind>View>;

#[no_mangle]
pub unsafe extern "C" fn openbc_<kind>_session_create(
    left: *const c_char, right: *const c_char,
    callback: EventCallback, user: *mut c_void,
) -> *mut <Kind>Session {
    let sink = Sink::new(callback, user);
    let (handle, mut events) = spawn_<kind>_compare(
        runtime().handle(), local_source(), path_arg(left), path_arg(right),
    );
    let pump = sink.clone();
    std::thread::Builder::new()
        .name("openbc-<kind>-events".into())
        .spawn(move || {
            while let Some(event) = events.blocking_recv() {
                match event {
                    <Kind>Event::Status(m) => pump.message(EV_STATUS, &m),
                    <Kind>Event::Error(m)  => pump.message(EV_ERROR, &m),
                    <Kind>Event::Result(v) => pump.handle(EV_RESULT, Box::new(v)),
                }
            }
        }).ok();
    Box::into_raw(Box::new(<Kind>Session { handle, sink }))
}

#[no_mangle]
pub unsafe extern "C" fn openbc_<kind>_session_destroy(s: *mut <Kind>Session) {
    if let Some(session) = (!s.is_null()).then(|| Box::from_raw(s)) {
        session.sink.close();
    }
}

#[no_mangle]
pub unsafe extern "C" fn openbc_<kind>_view_destroy(v: *mut ViewHandle) {
    if !v.is_null() { drop(Box::from_raw(v)); }
}
```

Register in `src/ffi/mod.rs`:
```rust
pub mod <kind>_compare;
```

**Key `ffi/common.rs` utilities:**

| Utility | Purpose |
|---------|---------|
| `runtime()` | Shared Tokio runtime (2 worker threads "openbc-compare") |
| `local_source()` | `Arc<dyn ByteSource>` backed by local FS |
| `path_arg(ptr)` | `*const c_char` -> `PathBuf` (null -> empty) |
| `out_str(s, len)` | Writes length, returns `*const u8` into `s` |
| `out_opt_str(opt, len)` | Like `out_str` but null-ptr for `None` |
| `handle_ref!(ptr, default)` | Safe deref or early-return with default |
| `Sink` | Thread-safe callback gate; call `close()` before dropping session |
| `EV_STATUS/RESULT/ERROR/SAVED/WINDOW/PROGRESS` | Event kind constants |

### 5. C API header -- `cpp/backend/compare_backend_api.h`

Declare all `openbc_<kind>_*` symbols inside `extern "C" { ... }`:

```cpp
struct OpenBc<Kind>Session;
struct OpenBc<Kind>View;

OpenBc<Kind>Session* openbc_<kind>_session_create(
    const char* left, const char* right,
    OpenBcEventCallback cb, void* user);
void openbc_<kind>_session_destroy(OpenBc<Kind>Session*);
uint8_t openbc_<kind>_reload(const OpenBc<Kind>Session*);
void openbc_<kind>_view_destroy(OpenBc<Kind>View*);
size_t openbc_<kind>_view_rows(const OpenBc<Kind>View*);
// ... add all accessor functions
```

### 6. Qt C++ Viewer widget -- `cpp/viewers/<kind>/<kind>_compare_viewer.h` (+ `.cpp`)

**Required public interface (consumed by `main_window.h`):**

```cpp
class <Kind>CompareViewer : public QWidget {
public:
    <Kind>CompareViewer(const QString& left, const QString& right,
                        QWidget* parent = nullptr);

    QString title() const;
    QString detailedTitle() const;
    QString leftText() const;
    QString rightText() const;

    // Implement if viewer has editable content:
    bool hasUnsavedChanges() const;
    bool confirmClose();

    // Menu items (return empty list if not applicable):
    QList<QAction*> actionsMenuItems();
    QList<QAction*> editMenuItems();
    QList<QAction*> searchMenuItems();
    QList<QAction*> viewMenuItems();

    // Set by main_window.h after construction:
    std::function<void()> onHomeRequested;
    std::function<void()> onSessionsRequested;
    std::function<void()> onTitleChanged;
    std::function<void(const QString&, const QString&)> onComparisonRequested;
};
```

**Required UI components:**
- **PathSelector** (`common/path_selector.h`) -- always use `makeCommitSelector(...)` for path input rows; implement `commitPath(side, path)` -> validate -> `startSession()` / `compare()`; never use bare `QLineEdit` + button
- **DifferenceOverview** (minimap, `common/minimap.h`) -- for row-based diff viewers; omit for picture/3D/media-style viewers
- **Icons** -- only via `openbc::ui::icons::glyph(Glyph::X)` from `style/qt_style.h`; add a new `Glyph` enum value rather than using raw image files
- **UnsavedChangesDialog** (`common/unsaved_changes_dialog.h`) -- when content is editable

**Backend integration pattern in the viewer:**
```cpp
// In constructor - start the session:
session_ = openbc_<kind>_session_create(
    left.toUtf8().constData(), right.toUtf8().constData(),
    &<Kind>CompareViewer::onEvent, this);

// Static callback (runs on Rust worker thread -> must re-post to Qt thread):
static void onEvent(void* user, int32_t kind, const char* message, void* handle) {
    auto* self = static_cast<<Kind>CompareViewer*>(user);
    // Capture; post to GUI thread:
    QMetaObject::invokeMethod(self, [self, kind, msg = QString(message), handle]() {
        self->handleEvent(kind, msg, handle);
    }, Qt::QueuedConnection);
}

// In destructor - always destroy session:
if (session_) {
    openbc_<kind>_session_destroy(session_);
    session_ = nullptr;
}
```

### 7. Register in the four mandatory locations

#### A. `cpp/common/file_kinds.h`

```cpp
// 1. Add to ViewerKind enum:
enum class ViewerKind { Text, Picture, Model3d, Table, Media, Registry, Version, Hex, <Kind> };

// 2. Add extension set (namespace detail):
inline const QSet<QString>& <kind>ExtensionSet() {
    static const QSet<QString> set{ "ext1", "ext2" };
    return set;
}

// 3. Add branch in classifyFilePath():
if (detail::<kind>ExtensionSet().contains(ext)) return ViewerKind::<Kind>;

// 4. Add to sessionKindForViewer():
case ViewerKind::<Kind>: return "<kind>-compare";

// 5. Add to canonicalSessionKind():
if (k == "<kind>") return "<kind>-compare";
```

#### B. `cpp/common/compare_extensions.h`

```cpp
inline const QSet<QString>& <kind>CompareExtensions() {
    static const QSet<QString> set{ "ext1", "ext2" };
    return set;
}
inline bool is<Kind>ComparePath(const QString& path) {
    return <kind>CompareExtensions().contains(compareExtensionOf(path));
}
// Update newViewerSessionKind() to return "<kind>-compare"
```

#### C. `cpp/app/main_window.h`

1. Declare: `std::function<void(const QString&, const QString&)> add<Kind>View;`
2. Define: `add<Kind>View = [&](const QString& l, const QString& r) { addViewerTab(new <Kind>CompareViewer(l, r), "<kind>-compare"); };`
3. Add to `rebuildMenus()`: declare `auto* <kind>View = dynamic_cast<<Kind>CompareViewer*>(current);` and include in all `fill(actionsMenu, ...)` chains
4. Add to `updateWindowTitle()`: handle `<Kind>CompareViewer*`
5. Add to `home->onNewSession` lambda: `} else if (kind == "<kind>-compare") { ... add<Kind>View(pair[0], pair[1]); }`
6. Add to `closeTab()` (if editable): `else if (auto* v = dynamic_cast<<Kind>CompareViewer*>(widget)) mayClose = v->confirmClose();`
7. Add to `duplicateTab()`: `if (auto* v = dynamic_cast<<Kind>CompareViewer*>(...)) { add<Kind>View(...); return; }`
8. Wire in `addSession` if folder-compare can open it: `session->on<Kind>Compare = [&](const QString& l, const QString& r) { add<Kind>View(l, r); };`

#### D. `cpp/app/cli_options.cpp` and `cli_options.h`

- Add `LaunchKind::<Kind>` to the enum in `cli_options.h`
- Add `{"<kind>", LaunchKind::<Kind>}` and `{"<kind>-compare", LaunchKind::<Kind>}` to `kindForType()`
- Handle `LaunchKind::<Kind>` in `parseLaunchArguments`

#### E. `cpp/home/home_view.h` -- `sessionTypes()`

```cpp
{ "<kind>-compare", "<Kind> Compare", icons::glyph(icons::Glyph::<Kind>) }
```

### 8. Add icon -- `style/qt_style.h`

```cpp
// In enum class Glyph:
<Kind>,

// In glyph() implementation:
case Glyph::<Kind>: return QIcon(/* SVG/PNG data or theme icon */);
```

### 9. No build system changes required

`build.rs` and `CMakeLists.txt` glob `cpp/**/*.cpp` and `cpp/**/*.h` automatically. Only update build files if you add a new Qt module dependency.

---

## Verification Checklist

- [ ] `cargo check --workspace` passes
- [ ] New `openbc_<kind>_*` symbols present in compiled `.so`/`.dll`
- [ ] All four registration points updated: `file_kinds.h`, `compare_extensions.h`, `main_window.h`, `cli_options.cpp`
- [ ] `home_view.h` `sessionTypes()` includes new kind
- [ ] `rebuildMenus()`, `updateWindowTitle()`, `closeTab()`, `duplicateTab()` handle new viewer
- [ ] `PathSelector` used for path input rows (no bare `QLineEdit` + button)
- [ ] Icons via `icons::glyph()` only
- [ ] Viewer destructor calls `openbc_<kind>_session_destroy()` and nulls the pointer
- [ ] `Sink::close()` called before session freed
- [ ] No hard-coded path separators; `QDir::toNativeSeparators()` for display
- [ ] Windows-only code behind `#ifdef Q_OS_WIN` / `Q_OS_WIN`
- [ ] `docs/REFACTOR_SAVEPOINT.md` updated if tracked item

---

## Common Mistakes to Avoid

| Mistake | Correct approach |
|---------|-----------------|
| Scanning files in Qt widget constructor | File I/O happens in engine actor; viewer only sends commands |
| Custom `QLineEdit` for paths | Use `PathSelector` / `makeCommitSelector` |
| Calling Qt methods from Rust worker thread | `QMetaObject::invokeMethod(..., Qt::QueuedConnection)` |
| Blocking inside a Tokio task | `spawn_blocking` or Rayon for sync I/O or CPU work |
| GPU compute below 1 MiB | Enforce `GPU_MIN_BYTES` from `openbc-compute::gpu_policy` |
| Hard-coding `/home/user` or `$USER` | `QDir::homePath()`, `qEnvironmentVariable("USER", qEnvironmentVariable("USERNAME", ...))` |
| Importing Tokio/Rayon into `openbc-core` | `openbc-core` must remain pure/dependency-light |
| Forgetting `rebuildMenus()` update | Leads to stale/empty menus when tab is active |
