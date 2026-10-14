---
name: ui
description: Build Godot UI with Control nodes, themes, and anchors — use when creating menus, HUDs, or any CanvasLayer UI.
type: implementation
---

# Godot UI

> You are a Godot 4 UI specialist who builds responsive, theme-driven interfaces using Control nodes, containers, and GDScript 4.x.

## Overview

Godot UI is built on the `Control` node hierarchy. Every visible UI element extends `Control`, which handles anchors, size flags, and theme lookups. Use `CanvasLayer` to render UI above the 3D/2D world. Lay out controls with containers (`VBoxContainer`, `HBoxContainer`, `GridContainer`, `MarginContainer`) rather than manual position math. Style everything through `Theme` resources and `StyleBox` types so changes propagate automatically.

## Key Nodes & APIs

| Node / Class | Purpose |
|---|---|
| `Control` | Base class for all UI nodes; handles anchors, rect, focus |
| `CanvasLayer` | Renders UI independent of Camera2D/3D; `layer` sets draw order |
| `Panel` | Opaque background; styled via `StyleBox` theme override |
| `Label` | Single- or multi-line text with `autowrap_mode` |
| `Button` / `LinkButton` | Clickable controls; emit `pressed` signal |
| `TextureRect` | Displays a texture; `expand_mode` controls scaling |
| `VBoxContainer` / `HBoxContainer` | Stack children vertically or horizontally |
| `GridContainer` | Grid layout with fixed column count |
| `MarginContainer` | Adds padding around a single child |
| `CenterContainer` | Centers a single child in available space |
| `AspectRatioContainer` | Keeps child at fixed aspect ratio |
| `SubViewportContainer` | Embeds a `SubViewport` (e.g. 3D preview) inside UI |
| `ScrollContainer` | Scrollable area around an oversized child |
| `TabContainer` | Tabbed panels |
| `PopupMenu` | Right-click or dropdown menu |
| `Theme` | Resource holding all style data for a subtree |
| `StyleBoxFlat` | Programmatic box: fill color, border, corner radius |
| `StyleBoxTexture` | 9-patch texture for scalable bordered UI |
| `StyleBoxLine` | Single horizontal or vertical divider line |

## Core Patterns

### 1. Anchoring a panel to the bottom-right corner

```gdscript
@onready var panel: Panel = %Panel

func _ready() -> void:
    panel.set_anchor_and_offset(SIDE_LEFT,   1.0, -220.0)
    panel.set_anchor_and_offset(SIDE_TOP,    1.0, -120.0)
    panel.set_anchor_and_offset(SIDE_RIGHT,  1.0,    0.0)
    panel.set_anchor_and_offset(SIDE_BOTTOM, 1.0,    0.0)
```

### 2. Code-driven theme overrides

```gdscript
# Applies only to this node, overriding the inherited theme.
# Hierarchy (most specific wins):
#   node override → type override → project theme

var stylebox := StyleBoxFlat.new()
stylebox.bg_color = Color(0.1, 0.1, 0.1, 0.9)
stylebox.corner_radius_top_left    = 8
stylebox.corner_radius_top_right   = 8
stylebox.corner_radius_bottom_left = 8
stylebox.corner_radius_bottom_right = 8

%MyPanel.add_theme_stylebox_override("panel", stylebox)
%MyLabel.add_theme_font_override("font", preload("res://fonts/ui.ttf"))
%MyLabel.add_theme_color_override("font_color", Color.WHITE)
%MyLabel.add_theme_constant_override("line_spacing", 4)
```

### 3. HUD on a CanvasLayer with tween animation

```gdscript
# hud.gd
extends CanvasLayer

@onready var damage_panel: Panel = %DamagePanel
@onready var health_label: Label = %HealthLabel

func update_health(value: int) -> void:
    health_label.text = tr("HUD_HEALTH") % value

func flash_damage() -> void:
    damage_panel.modulate.a = 1.0
    create_tween().tween_property(damage_panel, "modulate:a", 0.0, 0.4)

func show_panel(target: Control) -> void:
    target.modulate.a = 0.0
    target.visible = true
    create_tween().tween_property(target, "modulate:a", 1.0, 0.3)

func hide_panel(target: Control) -> void:
    var tw := create_tween()
    tw.tween_property(target, "modulate:a", 0.0, 0.3)
    tw.tween_callback(target.hide)
```

### 4. Gamepad / keyboard focus management

```gdscript
# menu.gd
extends Control

@onready var play_btn:   Button = %PlayButton
@onready var quit_btn:   Button = %QuitButton
@onready var options_btn: Button = %OptionsButton

func _ready() -> void:
    # Allow all input methods to focus these buttons.
    for btn: Button in [play_btn, options_btn, quit_btn]:
        btn.focus_mode = Control.FOCUS_ALL

    # Wire up neighbors so gamepad d-pad navigates correctly.
    play_btn.focus_neighbor_bottom    = options_btn.get_path()
    options_btn.focus_neighbor_top    = play_btn.get_path()
    options_btn.focus_neighbor_bottom = quit_btn.get_path()
    quit_btn.focus_neighbor_top       = options_btn.get_path()

    play_btn.grab_focus()
```

### 5. Responsive layout with AspectRatioContainer and SubViewportContainer

```gdscript
# Maintain a 16:9 preview window inside the UI.
@onready var arc: AspectRatioContainer = %PreviewContainer
@onready var sub_vp: SubViewport       = %PreviewViewport

func _ready() -> void:
    arc.ratio = 16.0 / 9.0
    arc.stretch_mode = AspectRatioContainer.STRETCH_FIT_WIDTH
    sub_vp.size = Vector2i(320, 180)
```

### 6. Localization

```gdscript
# In script — wrap all user-visible strings.
health_label.text = tr("HUD_HEALTH_LABEL") % current_hp
status_label.text = tr("STATUS_READY")

# Switch language at runtime.
func set_language(locale: String) -> void:
    TranslationServer.set_locale(locale)
```

### 7. Masking children with clip_children

```gdscript
# Clip child controls to this node's rect (acts as a mask).
@onready var card: Panel = %Card

func _ready() -> void:
    # CLIP_CHILDREN_ONLY clips without a separate CanvasItem draw.
    card.clip_children = CanvasItem.CLIP_CHILDREN_ONLY
```

## Common Pitfalls

- **Mixing anchor presets with manual offsets.** Calling `set_anchor_and_offset` after the Layout menu preset is applied will conflict. Pick one approach per node and keep it consistent.
- **`z_index` does not cross CanvasLayer boundaries.** `z_index` only sorts siblings within the same `CanvasLayer`. To reorder entire UI layers (e.g. tooltip above modal), set `CanvasLayer.layer` on the parent `CanvasLayer` instead.
- **Forgetting `FOCUS_ALL` for gamepad menus.** The default `focus_mode` on many controls is `FOCUS_NONE`. Any button or input that must be reachable via keyboard or gamepad needs `focus_mode = Control.FOCUS_ALL` and wired `focus_neighbor_*` paths.
- **Nesting containers unnecessarily.** Each container triggers a layout pass on its children. Deep nesting (e.g. `HBox > VBox > HBox > MarginContainer`) multiplies layout cost. Flatten where possible using `size_flags` and `custom_minimum_size`.
- **Animating `position` instead of `modulate`.** Moving controls via `position` during layout causes the container to re-layout every frame. Prefer `modulate:a` for fade animations and `scale` for pop effects; reserve `position` tweens for floating overlays outside containers.
- **SubViewport renders every frame.** `SubViewportContainer` redraws the embedded viewport each frame even when nothing changes. Set `render_target_update_mode = SubViewport.UPDATE_ONCE` or `UPDATE_DISABLED` when the preview is static.
- **Hardcoded color/font in scripts instead of theme.** `add_theme_color_override` is fine for one-off dynamic changes, but do not scatter color literals throughout scripts. Define palette colors in a shared `Theme` resource so redesigns require only one edit.

## Performance

**Draw call batching.** Every unique `CanvasItem` with a different material, texture, or `z_index` break batches. Group controls that share a texture atlas under a single parent and avoid per-node material overrides.

**Avoid deeply nested containers.** Containers recalculate child sizes whenever their own size changes. A five-level-deep hierarchy means five layout passes per resize. Prefer `Control` with anchors and `size_flags` over container chains when the relationship is simple.

**SubViewport cost.** A `SubViewportContainer` with `UPDATE_ALWAYS` re-renders its scene graph every frame at its own resolution. For UI previews, portraits, or minimap thumbnails that update infrequently, set:

```gdscript
$SubViewportContainer/SubViewport.render_target_update_mode = SubViewport.UPDATE_ONCE
# Call UPDATE_ONCE again whenever content changes.
```

**Theme lookups.** `add_theme_*_override` is O(1). Inheriting from a deeply nested theme chain is also fast at runtime but can be slow to author. Keep the project `Theme` as the single source of truth and use overrides only for dynamic runtime changes.

**Visibility toggling.** Prefer `visible = false` over `modulate.a = 0.0` for controls that should not receive input or process layout. Invisible nodes skip draw and input entirely; transparent nodes still participate in layout.

## Anti-Patterns

**Positioning controls manually when a container would work:**

```gdscript
# Wrong — brittle, breaks at different resolutions.
$Label.position = Vector2(10, 200)
$Button.position = Vector2(10, 240)

# Right — VBoxContainer handles spacing automatically.
# (Add Label and Button as children of a VBoxContainer in the scene.)
%MyVBox.add_child(label_instance)
%MyVBox.add_child(button_instance)
```

**Using `z_index` to reorder across CanvasLayers:**

```gdscript
# Wrong — z_index has no effect across CanvasLayer boundaries.
$TooltipLayer.z_index = 100

# Right — set the layer property on the CanvasLayer itself.
$TooltipLayer.layer = 10   # renders above layers with lower values
$ModalLayer.layer   = 5
```

**Hardcoding translated strings:**

```gdscript
# Wrong — breaks localization.
health_label.text = "Health: %d" % hp

# Right — use translation keys.
health_label.text = tr("HUD_HEALTH") % hp
```

**Animating layout properties inside a container:**

```gdscript
# Wrong — fighting the container's layout pass every frame.
create_tween().tween_property(%Panel, "position:y", 0.0, 0.3)

# Right — animate a property the container ignores.
create_tween().tween_property(%Panel, "modulate:a", 1.0, 0.3)
# Or move the panel outside its container if a slide-in is required.
```

## References

- Control node: https://docs.godotengine.org/en/stable/classes/class_control.html
- CanvasLayer: https://docs.godotengine.org/en/stable/classes/class_canvaslayer.html
- Theme: https://docs.godotengine.org/en/stable/classes/class_theme.html
- StyleBoxFlat: https://docs.godotengine.org/en/stable/classes/class_styleboxflat.html
- StyleBoxTexture: https://docs.godotengine.org/en/stable/classes/class_styleboxtexture.html
- StyleBoxLine: https://docs.godotengine.org/en/stable/classes/class_styleboxline.html
- Using Containers: https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html
- Anchors and Margins: https://docs.godotengine.org/en/stable/tutorials/ui/size_and_anchors.html
- Themes: https://docs.godotengine.org/en/stable/tutorials/ui/gui_using_theme_editor.html
- Tween: https://docs.godotengine.org/en/stable/classes/class_tween.html
- TranslationServer: https://docs.godotengine.org/en/stable/classes/class_translationserver.html
- AspectRatioContainer: https://docs.godotengine.org/en/stable/classes/class_aspectratiocontainer.html
- SubViewport: https://docs.godotengine.org/en/stable/classes/class_subviewport.html

## Delegate to

- Use the `godot:animation` skill for AnimationPlayer-driven UI sequences longer than a single tween.
- Use the `godot:shader` skill for custom `CanvasItem` shaders on UI materials.
