---
name: qt-cpp-docs
version: 1.0.0
description: Write QDoc API documentation for Qt6 C++ code, covering classes, properties, signals/slots, enums, and QML-exposed types.
author: matrixx0070
tags: [qt6, qdoc, documentation, api, cpp]
capabilities: []
---
## When to use
Use this when you are documenting a Qt 6.x C++ class or module with QDoc so it renders into Qt-style HTML/DocBook reference pages. **Not for:** setting up the build that runs QDoc (see `qt-cmake-project`) or judging the correctness of the code you are documenting (see `qt-cpp-review`).

## Method
1. Open a QDoc comment block with `/*!` and close with `*/`. QDoc ignores ordinary `//` and `/* */` comments, so use `/*!` only where you want output.
2. Document the class first: `\class Namespace::ClassName`, a one-line `\brief`, `\inmodule <ModuleName>`, and `\since <version>`. Decision point: if the class is meant for QML, also emit `\qmltype` / `\qmlproperty` for the exposed surface.
3. Document each public function with `\fn` (only needed when the comment is detached from the declaration), referencing parameters with `\a name` and inline code with `\c`.
4. Document `Q_PROPERTY` with `\property Class::propName`; describe the read/write/notify behavior in prose. The getter/setter get `\sa` links back to the property.
5. Document signals and slots as functions; explicitly say when a signal is emitted, and cross-link the related property or slot with `\sa`.
6. Document enums with `\enum Class::EnumName` and each value with `\value Name description`.
7. Add thread guarantees where relevant: `\reentrant`, `\threadsafe`. Add `\note` for caveats and `\l` for external links.
8. Point QDoc at the module via a `.qdocconf` file and run `qdoc project.qdocconf`. Decision point: for offline `.qch` help, run `qhelpgenerator` on the generated help project afterward.

## Example
```cpp
/*!
    \class Media::Player
    \inmodule MediaKit
    \brief Plays audio and video streams.
    \since MediaKit 2.1
    \reentrant

    Use \c Player to load a source and control playback. Call
    \l {Media::Player::play()}{play()} after setting \l source.
*/

/*!
    \property Media::Player::volume
    \brief the output volume in the range 0.0 to 1.0.

    The default is \c 1.0. Setting a value outside the range clamps it.
    \sa volumeChanged()
*/

/*!
    \fn void Media::Player::play()
    Starts playback of the current \a source and emits \l stateChanged().
    \note This is a no-op if no source is set.
    \sa stop(), stateChanged()
*/

/*!
    \enum Media::Player::State
    \value Stopped  Playback is halted.
    \value Playing  Media is advancing.
    \value Paused   Position is held.
*/
```

## Pitfalls
- **Wrong comment marker.** `/**` or `//` blocks are invisible to QDoc; only `/*!` is parsed.
- **\a for markup, not prose.** Use `\a paramName` to reference a parameter; writing the bare name loses the cross-reference and italic styling.
- **Undocumented Q_PROPERTY.** Documenting only the getter leaves the property page empty — QDoc keys the property page on `\property`.
- **Missing \inmodule.** Without `\inmodule`, the class is orphaned from the module's class list and index.
- **Stale \since.** Copy-pasting `\since` from another class misreports availability; set it to the version that introduced the symbol.
- **QML types under \fn.** QML-exposed members need `\qmlproperty`/`\qmlmethod`; documenting them only as C++ hides them from the QML reference.

## Output format
```cpp
/*!
    \class <Ns::Class>
    \inmodule <Module>
    \brief <one line>.
    \since <Module x.y>

    <prose using \a, \c, \l, \sa, \note>
*/
// + per-member /*! \fn ... */, /*! \property ... */,
//   /*! \enum ... \value ... */, and /*! \qmlproperty ... */ blocks
```

## Reference
- Comment block: `/*! ... */` (the bang after the slash is required); QDoc runs across headers and `.cpp`.
- Topic commands: `\class`, `\fn`, `\property`, `\enum` (+ `\value`), `\namespace`, `\module`, `\qmltype`, `\qmlproperty`, `\qmlmethod`.
- Metadata: `\brief`, `\since <version>`, `\inmodule <name>`, `\reentrant`, `\threadsafe`, `\deprecated`.
- Inline markup: `\a <arg>` (parameter), `\c <code>` (monospace), `\l <target>` or `\l {target}{text}` (link), `\sa` (see-also list), `\note`, `\e` (emphasis).
- `Q_PROPERTY(type name READ getter WRITE setter NOTIFY sig)` is documented with `\property Class::name`; document `NOTIFY` signals as functions and `\sa` them.
- Config: a `.qdocconf` file sets `project`, `outputdir`, `headerdirs`, `sourcedirs`, `depends`, and `outputformats` (HTML/DocBook).
- Invocation: `qdoc <project.qdocconf>`; generate compressed help with `qhelpgenerator <project.qhp> -o <out.qch>`.
- QDoc ships in the Qt 6 tools; run it with the compile database or explicit include paths so it resolves types.
