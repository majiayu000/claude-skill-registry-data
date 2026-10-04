---
name: qt-cpp-review
version: 1.0.0
description: Review Qt6 C++ code for correctness, memory ownership, and idiomatic use of QObject, signals/slots, and implicit sharing.
author: matrixx0070
tags: [qt6, cpp, code-review, memory, clazy]
capabilities: []
---
## When to use
Use this when you are reviewing Qt 6.x C++ for ownership bugs, signal/slot mistakes, threading hazards, and non-idiomatic Qt usage. **Not for:** wiring up the build or QML modules (see `qt-cmake-project`) or writing the API docs (see `qt-cpp-docs`).

## Method
1. Check `QObject` identity: every class deriving from `QObject` that declares signals, slots, or `Q_PROPERTY` must have the `Q_OBJECT` macro and be reachable by `moc`. Decision point: if `Q_OBJECT` is missing, signals/slots and `qobject_cast` silently break — flag it before anything else.
2. Trace ownership: confirm each heap `QObject` has a parent or a clear owner. Decision point: parented object → do not `delete` it manually; unparented → require a smart pointer or explicit lifetime.
3. Audit connections: prefer function-pointer `connect(sender, &S::sig, receiver, &R::slot)` for compile-time checking over the string-based `SIGNAL()/SLOT()` form. Check `Qt::ConnectionType` for cross-thread cases.
4. Look for dangling access: raw `QObject*` held across time should be `QPointer` so it nulls on destruction.
5. Review value semantics: containers and `QString` passed by value where a `const T&` (or `QStringView` for read-only string args) would avoid copies.
6. Check copy control: classes managing resources or identity should use `Q_DISABLE_COPY` or the PIMPL/d-pointer idiom; verify the d-pointer is deleted.
7. Inspect implicit sharing (COW): detachments from calling non-const methods, and iterator invalidation when a shared container is modified elsewhere.
8. Review threading: an object's thread affinity, `moveToThread`, and whether slots touch GUI objects off the main thread.
9. Run tooling: clazy (`level0`/`level1`/`level2`) and clang-tidy against `compile_commands.json`. Decision point: pre-merge gate → require clazy level1 clean; deep audit → level2.

## Example
```cpp
// FLAG: missing Q_OBJECT -> signals won't fire, moc emits nothing
class Worker : public QObject {
    // Q_OBJECT
public:
    explicit Worker(QObject *parent = nullptr) : QObject(parent) {}
signals:
    void done(int code);
};

// FLAG: string-based connect - no compile-time check, typo compiles
connect(w, SIGNAL(done(int)), this, SLOT(onDone(int)));
// PREFER: function-pointer connect, checked at compile time
connect(w, &Worker::done, this, &Controller::onDone);

// FLAG: raw pointer may dangle if child is destroyed elsewhere
QLabel *label;              // -> QPointer<QLabel> label;

// FLAG: pass-by-value copy of a container
void render(QList<QString> items);          // -> const QList<QString>&
void setTitle(QString title);               // read-only -> QStringView

// Ownership-managing type: forbid copies + use d-pointer
class Session {
    Q_DISABLE_COPY(Session)
    class Private;
    Private *d;   // deleted in ~Session
};
```

## Pitfalls
- **Missing Q_OBJECT.** No meta-object means no signals/slots, no `qobject_cast`, no runtime property system — and no moc output.
- **Double delete via parent.** Deleting a parented `QObject` yourself leaves the parent with a dangling child pointer.
- **String connects.** `SIGNAL()/SLOT()` typos fail only at runtime as a silent no-op with a console warning.
- **Cross-thread direct call.** A `Qt::DirectConnection` slot runs in the emitter's thread; touching GUI there is undefined.
- **Dangling raw pointer.** A cached `QObject*` outliving its target crashes; `QPointer` nulls itself.
- **Unnecessary detach.** Calling a non-const container method detaches the COW buffer, copying the whole container.
- **Copy of identity type.** Copying a `QObject`-owning wrapper without `Q_DISABLE_COPY` duplicates ownership and double-frees.

## Output format
```
# Qt C++ Review: <file/target>
## Blocking
- [ownership] <file:line> — <QObject parent / delete issue>
- [signals]   <file:line> — string connect / missing Q_OBJECT
## Non-blocking
- [perf]      <file:line> — pass const& / QStringView; avoid COW detach
- [threading] <file:line> — connection type / thread affinity
## Tooling
- clazy: level<N> — <clean | findings>
- clang-tidy: <clean | findings>
```

## Reference
- `Q_OBJECT` in the private section is mandatory for signals/slots, `Q_PROPERTY`, `qobject_cast`, and runtime type info; the class must be processed by `moc`.
- Ownership: `QObject(QObject *parent)`; children are deleted with the parent — never manually delete a parented object still owned.
- Connect (Qt 6): `QMetaObject::Connection connect(sender, &Sender::sig, receiver, &Receiver::slot, Qt::ConnectionType)` — function-pointer form is compile-time checked; string `SIGNAL()/SLOT()` is not.
- `Qt::ConnectionType`: `AutoConnection` (default), `DirectConnection`, `QueuedConnection`, `BlockingQueuedConnection`, `UniqueConnection`.
- `QPointer<T>` becomes null when its `QObject` is destroyed; use for observer pointers.
- `emit` is a no-op macro for readability; signals are invoked like functions.
- Copy control: `Q_DISABLE_COPY(Class)` deletes copy ctor/assign; PIMPL uses a `Private *d` (d-pointer), often via `QScopedPointer`/`Q_DECLARE_PRIVATE`.
- Strings: prefer `QStringView` for non-owning read-only string parameters; `QString` is implicitly shared (copy-on-write).
- Implicit sharing (COW): copies are cheap until a mutating (non-const) call triggers a detach; be wary of iterator invalidation across shared copies.
- Threading: `QObject::thread()` reports affinity; `moveToThread(QThread*)` reparents affinity; queued connections marshal calls to the receiver's thread; GUI objects live on the main thread only.
- `SkipEmptyParts` is the Qt 6 `QString::split` flag (replaces the removed `QString::SkipEmptyParts`); the string-based connect enum lives under `Qt::` too.
- Tooling: clazy check levels `level0` (safe, no false positives), `level1` (default), `level2` (may have false positives); run clazy and `clang-tidy` against `compile_commands.json`.
