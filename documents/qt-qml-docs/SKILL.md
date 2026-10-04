---
name: qt-qml-docs
version: 1.0.0
description: Document QML types, properties, signals, and modules with QDoc for Qt6 QML modules.
author: matrixx0070
tags: [qt6, qml, qdoc, documentation, api-docs]
capabilities: []
---

## When to use

You are writing QDoc comments for QML types (in `.cpp`/`.h` backing a QML type, or in `.qml`/`.qdoc` files) and want correctly linked, buildable API reference pages. Reach here when the goal is documentation output.

**Not for:** writing the QML itself (use `qt-qml`) or reviewing QML for defects and performance (use `qt-qml-review`).

## Method

1. Open each type with `\qmltype` and place it in a module with `\inqmlmodule`. **Decision point:** if the QML type is backed by a C++ class, add `\nativetype <Class>` (Qt 6.6+; older Qt uses `\instantiates`) so the pages cross-link.
2. Document every public property with `\qmlproperty <type> <name>`. **Decision point:** if the property is init-only mark `\readonly`; if it is the type's default property mark `\default`.
3. Document signals with `\qmlsignal`, invokable methods with `\qmlmethod`, and attached properties with `\qmlattachedproperty`. **Decision point:** if a member exists only on an attached type, use the attached variants so it renders under the attaching type.
4. Version each addition with `\since QtQuick 6.x`. **Decision point:** if a member arrived in a later minor release than the type, put `\since` on the member, not the type.
5. Cross-link with `\sa` and inline `\l`. **Decision point:** if you reference another module's type, link the fully qualified name so QDoc resolves across modules.
6. Configure the module's `.qdocconf` to scan QML sources and register the module, then build with `qdoc`.

## Example

```cpp
/*!
    \qmltype BackendModel
    \inqmlmodule Demo
    \nativetype BackendModel
    \brief Holds and mutates the demo counter.

    \section1 Usage
    \qml
    BackendModel { id: model }
    Text { text: model.count }
    \endqml
*/

/*!
    \qmlproperty int BackendModel::count
    \readonly
    The current counter value. Emits \l countChanged on update.
    \sa increment
*/

/*!
    \qmlmethod void BackendModel::increment()
    \since QtQuick 6.5
    Increments \l count by one.
*/

/*!
    \qmlsignal BackendModel::countChanged()
    Emitted whenever \l count changes.
*/
```

## Pitfalls

- **Missing \inqmlmodule.** Without it QDoc cannot place the type in a module and the page is orphaned / links break.
- **Wrong backing command.** `\instantiates` is legacy; on Qt 6.6+ use `\nativetype` to link the QML type to its C++ class (and vice-versa).
- **Type-and-name mismatch.** `\qmlproperty` needs `<type> <TypeName>::<prop>`; omitting the type or the qualifier breaks resolution and the property renders untyped.
- **Undocumented enums.** Enums exposed to QML need their own doc block with each value listed via `\value`, or they render blank.
- **Signal vs handler confusion.** Document the signal with `\qmlsignal`; QDoc auto-generates the `on<Signal>` handler entry — do not document the handler separately.
- **qdocconf not scanning QML.** If `.qml`/headers aren't in the source/header dirs, QML types silently never appear.

## Output format

```
/*!
    \qmltype <TypeName>
    \inqmlmodule <Module>
    \nativetype <BackingClass>      // if C++-backed
    \since QtQuick 6.x
    \brief <one line>.

    <description, optionally with \qml ... \endqml or \code ... \endcode>
*/

/*!
    \qmlproperty <type> <TypeName>::<prop>
    \readonly                       // if applicable
    \default                        // if default property
    <description>  \sa <related>
*/
```

## Reference

- **Core commands:** `\qmltype`, `\qmlproperty`, `\qmlsignal`, `\qmlmethod`, `\qmlattachedproperty`, `\qmlattachedsignal` — declare the documented QML members.
- **Module placement:** `\inqmlmodule <Module>` assigns the type to its QML module; must match the URI in `qt_add_qml_module`.
- **C++ linking:** `\nativetype <Class>` (Qt 6.6+) links QML type ⇄ backing C++ class; the older `\instantiates <Class>` command does the same on pre-6.6 and is now deprecated.
- **Property syntax:** `\qmlproperty <type> <TypeName>::<name>` — the type and the `TypeName::` qualifier are both required. Modifiers: `\readonly`, `\default`, `\required`.
- **Enums:** document an enum exposed to QML with a doc block and one `\value <Name> <desc>` per enumerator; expose from C++ via `Q_ENUM`/`QML_ELEMENT` on the enclosing type.
- **Versioning:** `\since QtQuick 6.x` (or `\since <Module> 6.x`) marks the introducing release; place on the member if later than the type.
- **Cross-links:** `\sa` for "See also" lists; `\l <Type>` / `\l {Module::Type}` for inline links; `\brief` for the summary line.
- **Code blocks:** `\qml ... \endqml` for QML snippets (syntax-highlighted as QML), `\code ... \endcode` for generic/C++ code.
- **qdocconf:** set `sourcedirs`/`headerdirs` to include the QML module's sources, list the module under `qhp` config, and set `outputdir`; run `qdoc <project>.qdocconf` (or via `qt_add_docs` / `qt_generate_qml_docs` in CMake).
