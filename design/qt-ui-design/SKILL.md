---
name: qt-ui-design
version: 1.0.0
description: Design a Qt Quick (QML) user interface with sound layouts, theming, responsiveness, and accessibility.
author: matrixx0070
tags: [qml, qt-quick, ui-design, layouts, theming]
capabilities: []
---

## When to use

Use this when you are structuring a Qt Quick UI from requirements — choosing layout containers, wiring a theme, making it responsive across window sizes, and keeping it accessible — rather than transcribing a specific design file.

**Not for:** pulling tokens out of a Figma file (see qt-figma-token-extraction) or code-generating components from Figma frames (see qt-figma-component-generation).

## Method

1. Establish the theme first: create a `Theme.qml` singleton (`pragma Singleton`) for colors, spacing, radii, and fonts so every screen references tokens, not literals.
2. Pick the control layer. **Decision point:** if you want a platform look-and-feel and built-in accessibility, use Qt Quick Controls 2 with a style (`Material`/`Universal`/`Fusion`/`Basic`); if you need fully bespoke visuals, compose `Item`/`Rectangle` with `MouseArea`/`TapHandler`.
3. Choose the positioning system per container. **Decision point:** if children must flow/stretch/share space, use `RowLayout`/`ColumnLayout`/`GridLayout` with `Layout.*` attached properties; if a child is pinned relative to its parent or a sibling, use `anchors`. Never apply both to the same item.
4. Set the base element. **Decision point:** if an element only needs geometry/clipping/opacity, use `Item`; if it needs a fill, border, or radius, use `Rectangle`.
5. Make it responsive: drive size with `Layout.fillWidth`/`Layout.fillHeight`, `Layout.preferredWidth`, and `Layout.minimumWidth`; switch structure at breakpoints via `states` bound to the window/root width.
6. Define `states` and `transitions` for interactive and adaptive changes so geometry and visibility animate instead of snapping.
7. Handle high-DPI by working in logical pixels only — Qt 6 scales by the screen device pixel ratio automatically; provide `@2x`/SVG assets rather than manual multipliers.
8. Add accessibility: attach `Accessible.role`/`Accessible.name` to custom interactive items; Controls provide these by default. **Decision point:** if an item is custom-drawn and clickable, it must carry an `Accessible` role, otherwise screen readers skip it.
9. Verify by resizing the window and running with a screen reader / `Accessible` inspection before considering the layout done.

## Example

```qml
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import MyApp.Theme

ApplicationWindow {
    id: root
    visible: true
    width: 900; height: 600
    readonly property bool compact: width < 600

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: Theme.spacingMd
        spacing: Theme.spacingSm

        Label {
            text: qsTr("Dashboard")
            font: Theme.titleLarge
            color: Theme.colorOnSurface
            Layout.fillWidth: true
        }

        GridLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            columns: root.compact ? 1 : 3      // responsive breakpoint
            columnSpacing: Theme.spacingMd
            rowSpacing: Theme.spacingMd

            Repeater {
                model: 6
                delegate: Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 120
                    radius: Theme.radiusLg
                    color: Theme.colorSurface

                    Accessible.role: Accessible.Button
                    Accessible.name: qsTr("Card %1").arg(index + 1)
                    TapHandler { onTapped: console.log("card", index) }
                }
            }
        }
    }
}
```

## Pitfalls

- **Mixing anchors and Layout.** Setting `anchors.*` and `Layout.*` on the same item produces conflicting geometry and runtime warnings. Choose one system per item.
- **Hardcoded pixel sizes.** Fixed `width`/`height` everywhere breaks responsiveness and high-DPI. Prefer `Layout.fillWidth`/`preferredWidth` and content-driven `implicit*`.
- **Manual DPI math.** Multiplying sizes by a scale factor double-scales against Qt 6's automatic DPR handling. Stay in logical pixels.
- **Styling Controls by editing internals.** Overwriting `contentItem`/`background` per instance instead of using a style is unmaintainable; set the style once and theme via the singleton.
- **Missing accessibility on custom items.** Bespoke `Rectangle`+handler widgets are invisible to assistive tech without an `Accessible.role`/`name`.
- **Non-animated state changes.** Toggling geometry/visibility without `transitions` makes responsive reflows jump; pair `states` with `Transition`/`Behavior`.

## Output format

```
main.qml               # ApplicationWindow root, layout skeleton
Theme.qml              # pragma Singleton design tokens
components/*.qml        # reusable, property-driven UI pieces
qtquickcontrols2.conf  # selected Controls style + palette (optional)
```

```qml
// screen skeleton
ApplicationWindow {
    // root breakpoint props (e.g. compact: width < 600)
    ColumnLayout {            // or Row/GridLayout
        anchors.fill: parent  // anchors on the top container only
        spacing: Theme.spacingSm
        // children use Layout.* for sizing, Theme.* for style,
        // Accessible.* on custom interactive items,
        // states + transitions for responsive/interaction changes
    }
}
```

## Reference

- **Qt Quick Layouts** (`import QtQuick.Layouts`): `RowLayout`, `ColumnLayout`, `GridLayout`. Attached properties on children: `Layout.fillWidth`/`Layout.fillHeight` (bool), `Layout.preferredWidth`/`Layout.preferredHeight`, `Layout.minimumWidth`/`Layout.maximumWidth`, `Layout.alignment` (e.g. `Qt.AlignHCenter | Qt.AlignVCenter`), `Layout.margins`, `Layout.columnSpan`/`Layout.rowSpan`.
- **Anchors vs Layouts:** anchors (`anchors.fill`, `anchors.centerIn`, `left`/`right`/`top`/`bottom`, `margins`) and `Layout.*` must not be combined on the same item. Anchor the outermost container to its parent; use Layouts for children.
- **Qt Quick Controls 2 styling:** styles are `Basic`, `Fusion`, `Material`, `Universal` (also `macOS`/`Windows` native on Qt 6). Select at runtime with `QQuickStyle::setStyle("Material")` in C++ before loading QML, via the `qtquickcontrols2.conf` file (`[Controls] Style=Material`, plus `[Material]` palette keys), or the `QT_QUICK_CONTROLS_STYLE` env var. Style attached props like `Material.theme`/`Material.accent` customize per subtree.
- **Theme singleton:** `pragma Singleton` `QtObject` registered via `qt_add_qml_module` + `QT_QML_SINGLETON_TYPE`; reference as `Theme.<token>`. Keep colors/spacing/typography here (see qt-figma-token-extraction for populating it).
- **High-DPI:** Qt 6 enables high-DPI scaling by default and works in logical/device-independent pixels; the app scales by each screen's `Screen.devicePixelRatio`. Ship `@2x` raster variants or SVG; avoid manual scale factors and `pointSize` guesswork (prefer `pixelSize`).
- **Item vs Rectangle:** `Item` is the base visual type (no painting) for grouping, geometry, clipping (`clip`), and opacity; `Rectangle` adds `color`, `border.color`/`border.width`, `radius`, and gradients. Use `Item` unless a fill/border is needed.
- **States & transitions:** `states: [ State { name; PropertyChanges { target; ... } } ]` with `transitions: [ Transition { NumberAnimation/PropertyAnimation } ]`; `Behavior on <prop>` animates individual property changes. Drive responsive layout by binding container `columns`/visibility/state to root width breakpoints.
- **Accessibility:** the `Accessible` attached property exposes items to assistive tech — `Accessible.role` (e.g. `Accessible.Button`, `Accessible.StaticText`, `Accessible.CheckBox`), `Accessible.name`, `Accessible.description`, `Accessible.focusable`, `Accessible.onPressAction`. Qt Quick Controls set sensible defaults; custom interactive items must set them explicitly. Wrap user-facing strings in `qsTr(...)` for i18n.
