---
name: qt-qml
version: 1.0.0
description: Write idiomatic QML for Qt Quick applications with sound property design, bindings, and C++ integration.
author: matrixx0070
tags: [qt6, qml, qtquick, cpp-integration, bindings]
capabilities: []
---

## When to use

You are authoring or refactoring `.qml` files for a Qt Quick UI and want declarative, binding-driven code that integrates cleanly with C++ backends. Reach here when the question is "how should this QML be written?"

**Not for:** documenting QML types with QDoc (use `qt-qml-docs`) or auditing existing QML for defects and performance (use `qt-qml-review`).

## Method

1. Model state as properties, not imperative mutation. Declare `property`, `readonly property`, or `required property` on the object that owns the state. **Decision point:** if a value is derived from other properties, express it as a binding (`width: parent.width / 2`); if it is set once from outside, use `required property` so the parent must supply it.
2. Prefer bindings over assignment. **Decision point:** if you write `x = y` in JavaScript (a signal handler, `Component.onCompleted`), you have destroyed any existing binding on `x` — only do this for genuinely one-shot values; otherwise keep the declarative `x: y` form or restore with `Qt.binding()`.
3. Wire behavior through signal handlers (`onClicked`, `onTextChanged`, `on<Property>Changed`). **Decision point:** if you must react to a signal on an object you cannot annotate inline (e.g. a target referenced by id), use a `Connections` element with `target:`.
4. Scope references by `id`. **Decision point:** if a child needs a value from an ancestor, give the ancestor an `id` and reference it explicitly rather than relying on unqualified lookup — unqualified access is slower and lint-flagged.
5. Expose C++ types with `QML_ELEMENT` + `qt_add_qml_module`. **Decision point:** if the type is a stateless service or global, mark it `QML_SINGLETON`; if it is instantiable UI-facing state, plain `QML_ELEMENT` with `Q_PROPERTY(... NOTIFY ...)`.
6. Add `pragma ComponentBehavior: Bound` (Qt 6.5+) at the top of components that capture outer ids in delegates, so captured references bind to the defining context.
7. Use versionless imports (`import QtQuick`) for Qt 6; pin a version only when you must target a specific minor API.

## Example

```qml
// Counter.qml
pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls

Item {
    id: root
    required property BackendModel model      // must be injected by parent
    readonly property int doubled: model.count * 2   // binding, auto-updates

    property alias label: title.text          // alias exposes child property

    Text { id: title }

    Button {
        text: "inc"
        onClicked: root.model.increment()     // qualified via id, one-shot call
    }

    Connections {
        target: root.model
        function onCountChanged() { title.text = "n=" + root.model.count }
    }
}
```

```cpp
// backendmodel.h  — exposed via qt_add_qml_module(app URI Demo VERSION 1.0)
#include <QObject>
#include <QtQml/qqmlregistration.h>

class BackendModel : public QObject {
    Q_OBJECT
    QML_ELEMENT
    Q_PROPERTY(int count READ count NOTIFY countChanged)
public:
    int count() const { return m_count; }
public slots:
    void increment() { ++m_count; emit countChanged(); }
signals:
    void countChanged();
private:
    int m_count = 0;
};
```

## Pitfalls

- **Binding loss on assignment.** Writing `prop = value` in JS silently removes the declarative binding; use `prop = Qt.binding(() => expr)` to reassign a binding.
- **Unqualified access.** Referencing a property without an `id` or `this` resolves through the scope chain, is slower, and breaks under `ComponentBehavior: Bound`.
- **var overuse.** Typed properties (`int`, `real`, `string`, `BackendModel`) let the engine optimize and catch errors; `property var` defeats that.
- **Missing NOTIFY.** A `Q_PROPERTY` without a `NOTIFY` signal cannot drive QML bindings — they won't update.
- **Singleton misuse.** `QML_SINGLETON` needs a default constructor or a `create` function; instantiating it in QML is an error.
- **Alias vs value.** `property alias` is a live reference to another property; a plain property copies once. Choose deliberately.

## Output format

```qml
pragma ComponentBehavior: Bound
import QtQuick

Item {
    id: <root>
    required property <Type> <injected>
    readonly property <type> <derived>: <binding expression>

    // signal handlers
    on<Signal>: <one-shot action>

    Connections {
        target: <id>
        function on<Signal>() { /* ... */ }
    }
}
```

## Reference

- **Bindings vs assignment:** `prop: expr` creates a binding re-evaluated when dependencies change; `prop = expr` in JS is a one-time write that removes the binding. Restore with `Qt.binding(() => expr)`.
- **Property keywords:** `property <type> name`, `readonly property` (init-only), `required property` (must be set by creator/instantiator or model role), `property alias name: target.prop`.
- **Signal handlers:** auto-generated `on<Signal>` for signals and `on<Prop>Changed` for properties; custom signals declared with `signal clicked(int x)`.
- **id scoping:** ids are unique per component scope; unqualified name resolution walks the scope chain — always qualify via id.
- **C++ exposure (Qt 6):** put `QML_ELEMENT` (from `<QtQml/qqmlregistration.h>`) in the class, then in CMake `qt_add_qml_module(target URI My.Module VERSION 1.0 SOURCES ...)`. `QML_SINGLETON` marks a singleton; `QML_NAMED_ELEMENT("Name")` renames.
- **Q_PROPERTY:** `Q_PROPERTY(int count READ count WRITE setCount NOTIFY countChanged)` — NOTIFY is required for reactive bindings.
- **pragma ComponentBehavior: Bound** (Qt 6.5+): binds captured ids to the component's own context; recommended for delegates capturing outer state; qmllint warns without it in Qt 6.7+.
- **Loader/Component:** `Loader { sourceComponent: ... }` or `source:` for lazy/dynamic instantiation; `Component { }` defines an un-instantiated template; access loaded root via `Loader.item`.
- **Imports:** Qt 6 supports versionless imports (`import QtQuick`, `import QtQuick.Controls`); versioned imports (`import QtQuick 6.5`) still work for pinning.
- **Connections:** `Connections { target: obj; function onSignalName() {} }` — the Qt 6 syntax uses `function on...`, not the deprecated `onSignal:` shorthand.
