---
name: qt-qml-review
version: 1.0.0
description: Review QML code for correctness, performance, and idiom using qmllint and Qt6 best practices.
author: matrixx0070
tags: [qt6, qml, qmllint, review, performance]
capabilities: []
---

## When to use

You are auditing existing `.qml` files for defects, binding loops, performance regressions, and non-idiomatic patterns before merge. Reach here when the goal is judging code someone else (or you) already wrote.

**Not for:** authoring new QML from scratch (use `qt-qml`) or writing QDoc API documentation (use `qt-qml-docs`).

## Method

1. Run `qmllint` first and triage by warning category. **Decision point:** if it reports unqualified access, fix by adding an `id` (or `this.`) rather than suppressing the warning.
2. Hunt binding loops. **Decision point:** if a property's binding depends transitively on itself (e.g. `width` bound to a child sized by `parent.width`), break the cycle by anchoring to a fixed dimension or introducing an intermediate constant.
3. Check layout discipline. **Decision point:** if an item sets both `anchors` and `Layout.*` attached properties, that's a conflict — inside a `Layout`, use `Layout.*`; outside, use `anchors`.
4. Assess binding cost. **Decision point:** if a binding runs heavy JavaScript or is re-evaluated on every frame, move the work to C++ or precompute; keep binding expressions small and pure.
5. Flag type hygiene. **Decision point:** if a property is `var` where a concrete type fits, recommend the typed form so the engine can optimize and qmllint can check it.
6. Review dynamic objects and images. **Decision point:** if objects are created with `Qt.createObject`/`Component.createObject`, confirm each has a matching `destroy()`; if `Image` shows a large asset, require `sourceSize` to cap decode memory.
7. Enforce style with `qmlformat` and confirm `pragma ComponentBehavior: Bound` on delegate-bearing components.

## Example

```qml
// BEFORE — flagged by qmllint
Rectangle {
    width: childText.width + 20        // unqualified: childText resolved via scope
    Text { id: childText; text: "hi" }
    Image { source: "big.png" }        // full-res decode into memory
}

// AFTER
Rectangle {
    id: box
    width: label.width + 20            // qualified via id
    Text { id: label; text: "hi" }
    Image {
        source: "big.png"
        sourceSize.width: 128          // caps decoded size
        sourceSize.height: 128
    }
}
```

```bash
qmllint MyComponent.qml
qmllint --qmljsdebugger noop MyComponent.qml   # attach JS debugger transport
qmlformat -i MyComponent.qml                    # in-place style fix
```

## Pitfalls

- **Unqualified property access.** Resolving names through the scope chain is slow and fragile; qmllint flags it — fix with an `id` or `this.`, never by ignoring.
- **Binding loops.** qmllint reports "Binding loop detected"; a runtime loop silently stops updating. Break the dependency cycle, don't add a timer hack.
- **anchors + Layout mixing.** Setting `anchors` on a child of a `Layout` is ignored/undefined; pick one positioning system per parent.
- **JavaScript-heavy bindings.** Complex JS in a binding re-runs on every dependency change and blocks the GUI thread; push logic to C++ or cache.
- **var instead of typed.** `property var` disables engine optimizations and type checks; prefer `int`/`real`/`string`/concrete types.
- **Loader overuse.** Every `Loader` adds indirection and a separate context; don't wrap trivial static content in one.
- **Leaked dynamic objects.** Objects from `createObject` without `destroy()` accumulate; property injection into created objects hides their real interface — pass an explicit model/props instead.
- **Item vs Rectangle.** Using `Rectangle` purely as a container adds a needless render node; use `Item` when you don't need fill/border.

## Output format

```
QML Review: <file>

qmllint: <N warnings> (<categories>)

Findings
- [correctness] <file>:<line> — <issue> → <fix>
- [performance] <file>:<line> — <issue> → <fix>
- [idiom]       <file>:<line> — <issue> → <fix>

Verdict: <block | approve-with-nits | approve>
```

## Reference

- **qmllint:** the static QML analyzer shipped with Qt 6; warning categories include `unqualified` (unqualified access), `deprecated`, `import` (unresolved imports), `compiler`, and binding-loop detection. Categories are tunable via `--<category>` flags or a `.qmllint.ini` / `pragma`.
- **--qmljsdebugger:** `qmllint --qmljsdebugger <spec>` enables the QML/JS debugger transport for tooling integration.
- **Unqualified access fix:** add an `id` to the referenced object and qualify (`box.width`), or use `this.` inside the same object.
- **Binding loops:** reported as "Binding loop detected for property"; occur when a binding transitively depends on itself. Break via fixed sizing or intermediate properties.
- **Layout vs anchors:** inside `RowLayout`/`ColumnLayout`/`GridLayout` (from `QtQuick.Layouts`) use `Layout.fillWidth`, `Layout.preferredWidth`, etc.; outside a Layout use `anchors`. Do not mix on the same item.
- **Typed properties:** prefer `int`, `real`, `bool`, `string`, `color`, or concrete QML/registered types over `var` for engine optimization and lint coverage.
- **Image.sourceSize:** sets the decoded pixel dimensions, capping texture/decode memory regardless of display size; essential for large assets.
- **Item vs Rectangle:** `Item` is the base visual with no rendering; `Rectangle` adds a fill/border render node — use `Item` for pure containers.
- **pragma ComponentBehavior: Bound** (Qt 6.5+): required-idiom for delegates capturing outer ids; qmllint warns when captured context is ambiguous without it.
- **qmlformat:** the official formatter; `qmlformat -i <file>` rewrites in place to canonical style. Enforce in CI alongside qmllint.
- **Dynamic objects:** objects from `Component.createObject`/`Qt.createQmlObject` must be released with `destroy()`; prefer passing properties at creation over post-hoc property injection.
