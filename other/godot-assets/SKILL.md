---
name: godot-assets
description: |
  Visual quality system for Godot games. Creates polished, layered procedural visuals
  using shaders, _draw(), particles, and post-processing. Also handles external art
  pipelines (user-provided or AI-generated sprites). The goal is games that look
  intentional and stylish — never flat colored rectangles.
---

# Visual Quality System

## Core Principle: NEVER Ship Flat Shapes

A colored rectangle is not a game entity. Every visible object needs visual depth:
- **Body** — the main shape with gradients or texture
- **Outline** — 1-2px outline for contrast and readability
- **Shadow** — drop shadow or ambient occlusion effect
- **Highlight** — inner glow or specular highlight
- **Animation** — idle bob, pulse, rotation, or shimmer

This applies to EVERYTHING: player, enemies, bullets, pickups, UI elements, backgrounds.

## Visual Tiers

| Tier | When | Quality |
|------|------|---------|
| **Procedural** (default) | Full game builds | Shaders + layered _draw() + particles + post-processing |
| **Custom art** | User provides sprites | Sprite2D + AnimatedSprite2D + shader effects on top |
| **AI-generated** | User generates art externally | Art prompts + sprite pipeline + shader enhancement |
| **Prototype** | Quick/simple builds only | Basic shapes (only if user explicitly asks) |

## Procedural Visuals (Default for Full Builds)

### Entity Drawing Pattern (use for ALL game entities)
```gdscript
extends Node2D

@export var body_color := Color(0.2, 0.6, 1.0)
@export var outline_color := Color(0.1, 0.3, 0.6)
@export var size := 16.0

var _time := 0.0

func _process(delta):
    _time += delta
    queue_redraw()

func _draw():
    # Drop shadow
    draw_circle(Vector2(1, 2), size, Color(0, 0, 0, 0.3))

    # Body with gradient (darker at bottom)
    draw_circle(Vector2.ZERO, size, body_color.darkened(0.15))
    draw_circle(Vector2(0, -1), size * 0.9, body_color)

    # Inner highlight (top-left)
    draw_circle(Vector2(-size * 0.2, -size * 0.25), size * 0.45, body_color.lightened(0.3))

    # Outline
    draw_arc(Vector2.ZERO, size, 0, TAU, 32, outline_color, 1.5, true)

    # Pulse glow (subtle breathing)
    var glow_alpha = 0.1 + sin(_time * 2.0) * 0.05
    draw_circle(Vector2.ZERO, size * 1.3, Color(body_color.r, body_color.g, body_color.b, glow_alpha))
```

### Player Character (example: top-down shooter)
```gdscript
# Layered visual: body + cockpit + engine glow + shield arc
func _draw():
    var t = _time

    # Engine glow (behind)
    var engine_glow = Color(0.3, 0.6, 1.0, 0.15 + sin(t * 8.0) * 0.05)
    draw_circle(Vector2(0, 8), 10.0, engine_glow)

    # Shadow
    draw_circle(Vector2(1, 3), 14.0, Color(0, 0, 0, 0.25))

    # Body — rounded ship shape using polygon
    var body_pts = PackedVector2Array([
        Vector2(0, -16), Vector2(10, -4), Vector2(12, 8),
        Vector2(6, 14), Vector2(-6, 14), Vector2(-12, 8),
        Vector2(-10, -4)
    ])
    draw_colored_polygon(body_pts, body_color.darkened(0.1))

    # Inner lighter layer
    var inner_pts = PackedVector2Array([
        Vector2(0, -12), Vector2(7, -3), Vector2(8, 6),
        Vector2(4, 10), Vector2(-4, 10), Vector2(-8, 6),
        Vector2(-7, -3)
    ])
    draw_colored_polygon(inner_pts, body_color.lightened(0.1))

    # Cockpit highlight
    draw_circle(Vector2(0, -4), 4.0, body_color.lightened(0.5))
    draw_circle(Vector2(-1, -5), 2.0, Color(1, 1, 1, 0.4))

    # Outline
    draw_polyline(body_pts + PackedVector2Array([body_pts[0]]), outline_color, 1.5, true)
```

### Enemy (example: pulsing threat)
```gdscript
func _draw():
    var t = _time
    var pulse = 1.0 + sin(t * 3.0) * 0.05

    # Danger glow
    draw_circle(Vector2.ZERO, size * 1.4 * pulse, Color(body_color.r, body_color.g, body_color.b, 0.08))

    # Shadow
    draw_circle(Vector2(1, 2), size * pulse, Color(0, 0, 0, 0.3))

    # Spiky body
    var points = PackedVector2Array()
    for i in range(6):
        var angle = i * TAU / 6.0 - PI / 2.0
        var r = size * pulse * (1.0 if i % 2 == 0 else 0.6)
        points.append(Vector2(cos(angle), sin(angle)) * r)
    draw_colored_polygon(points, body_color)

    # Inner core (brighter)
    draw_circle(Vector2.ZERO, size * 0.4, body_color.lightened(0.3))

    # Eyes (menacing)
    draw_circle(Vector2(-4, -2), 3, Color.WHITE)
    draw_circle(Vector2(4, -2), 3, Color.WHITE)
    draw_circle(Vector2(-3.5, -1.5), 1.5, Color(0.1, 0, 0))
    draw_circle(Vector2(4.5, -1.5), 1.5, Color(0.1, 0, 0))

    # Outline
    draw_polyline(points + PackedVector2Array([points[0]]), outline_color, 1.5, true)
```

## Shader Library

### Glow Outline Shader (use on important entities)
```glsl
// glow_outline.gdshader
shader_type canvas_item;

uniform vec4 outline_color : source_color = vec4(0.0, 0.8, 1.0, 1.0);
uniform float outline_width : hint_range(0.0, 10.0) = 2.0;
uniform float glow_intensity : hint_range(0.0, 3.0) = 1.0;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    if (tex.a < 0.1) {
        // Check neighbors for outline
        float a = 0.0;
        float step_x = outline_width / float(textureSize(TEXTURE, 0).x);
        float step_y = outline_width / float(textureSize(TEXTURE, 0).y);
        a += texture(TEXTURE, UV + vec2(step_x, 0)).a;
        a += texture(TEXTURE, UV + vec2(-step_x, 0)).a;
        a += texture(TEXTURE, UV + vec2(0, step_y)).a;
        a += texture(TEXTURE, UV + vec2(0, -step_y)).a;
        a += texture(TEXTURE, UV + vec2(step_x, step_y)).a;
        a += texture(TEXTURE, UV + vec2(-step_x, step_y)).a;
        a += texture(TEXTURE, UV + vec2(step_x, -step_y)).a;
        a += texture(TEXTURE, UV + vec2(-step_x, -step_y)).a;
        if (a > 0.0) {
            COLOR = outline_color * glow_intensity;
        } else {
            COLOR = vec4(0.0);
        }
    } else {
        COLOR = tex;
    }
}
```

### Hit Flash Shader (better than modulate)
```glsl
// hit_flash.gdshader
shader_type canvas_item;

uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 flash_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    COLOR = mix(tex, flash_color * tex.a, flash_amount);
}
```

### Gradient Background Shader
```glsl
// gradient_bg.gdshader
shader_type canvas_item;

uniform vec4 color_top : source_color = vec4(0.05, 0.02, 0.12, 1.0);
uniform vec4 color_bottom : source_color = vec4(0.02, 0.01, 0.06, 1.0);
uniform float noise_amount : hint_range(0.0, 0.1) = 0.02;

void fragment() {
    vec4 grad = mix(color_top, color_bottom, UV.y);
    // Subtle noise for texture
    float n = fract(sin(dot(UV * 100.0, vec2(12.9898, 78.233))) * 43758.5453);
    grad.rgb += (n - 0.5) * noise_amount;
    COLOR = grad;
}
```

### Dissolve Death Shader
```glsl
// dissolve.gdshader
shader_type canvas_item;

uniform float dissolve_amount : hint_range(0.0, 1.0) = 0.0;
uniform vec4 edge_color : source_color = vec4(1.0, 0.3, 0.0, 1.0);
uniform float edge_width : hint_range(0.0, 0.2) = 0.05;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    float noise = fract(sin(dot(UV * 50.0, vec2(12.9898, 78.233))) * 43758.5453);
    float threshold = dissolve_amount;

    if (noise < threshold) {
        discard;
    } else if (noise < threshold + edge_width) {
        COLOR = edge_color;
    } else {
        COLOR = tex;
    }
}
```

### Applying Shaders in Code
```gdscript
# Create shader material
func _apply_glow_outline(node: CanvasItem, color: Color):
    var mat = ShaderMaterial.new()
    mat.shader = load("res://shaders/glow_outline.gdshader")
    mat.set_shader_parameter("outline_color", color)
    mat.set_shader_parameter("outline_width", 2.0)
    node.material = mat

# Hit flash effect
func _flash_hit(node: CanvasItem):
    if node.material is ShaderMaterial:
        node.material.set_shader_parameter("flash_amount", 1.0)
        var tw = create_tween()
        tw.tween_method(func(v): node.material.set_shader_parameter("flash_amount", v), 1.0, 0.0, 0.12)

# Dissolve death
func _dissolve_death(node: CanvasItem):
    var mat = ShaderMaterial.new()
    mat.shader = load("res://shaders/dissolve.gdshader")
    node.material = mat
    var tw = create_tween()
    tw.tween_method(func(v): mat.set_shader_parameter("dissolve_amount", v), 0.0, 1.0, 0.5)
    tw.tween_callback(node.queue_free)
```

## Background Systems (never plain solid color)

### Layered Background
```gdscript
func _build_background():
    # Layer 1: Gradient shader
    var bg = ColorRect.new()
    bg.set_anchors_preset(Control.PRESET_FULL_RECT)
    bg.z_index = -100
    var bg_mat = ShaderMaterial.new()
    bg_mat.shader = load("res://shaders/gradient_bg.gdshader")
    bg.material = bg_mat
    add_child(bg)

    # Layer 2: Animated grid / stars / dots
    var grid = Node2D.new()
    grid.z_index = -99
    grid.set_script(load("res://scripts/effects/animated_grid.gd"))
    add_child(grid)

    # Layer 3: Floating ambient particles
    var ambient = GPUParticles2D.new()
    ambient.z_index = -98
    ambient.amount = 30
    ambient.lifetime = 6.0
    var mat = ParticleProcessMaterial.new()
    mat.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_BOX
    mat.emission_box_extents = Vector3(600, 400, 0)
    mat.initial_velocity_min = 5.0
    mat.initial_velocity_max = 15.0
    mat.direction = Vector3(0, -1, 0)
    mat.spread = 30.0
    mat.scale_min = 1.0
    mat.scale_max = 3.0
    mat.color = Color(1, 1, 1, 0.05)
    ambient.process_material = mat
    add_child(ambient)

    # Layer 4: Vignette overlay
    var vignette = ColorRect.new()
    vignette.set_anchors_preset(Control.PRESET_FULL_RECT)
    vignette.z_index = 90
    vignette.mouse_filter = Control.MOUSE_FILTER_IGNORE
    var vig_mat = ShaderMaterial.new()
    # Use a simple vignette shader or darken edges
    vignette.color = Color(0, 0, 0, 0)
    add_child(vignette)
```

## UI Quality Standards

### Styled Button (not default Godot buttons)
```gdscript
func _create_button(text: String, accent: Color, callback: Callable) -> Button:
    var btn = Button.new()
    btn.text = text
    btn.custom_minimum_size = Vector2(240, 56)
    btn.add_theme_font_size_override("font_size", 20)

    # Style overrides
    var normal = StyleBoxFlat.new()
    normal.bg_color = accent.darkened(0.3)
    normal.corner_radius_top_left = 8
    normal.corner_radius_top_right = 8
    normal.corner_radius_bottom_left = 8
    normal.corner_radius_bottom_right = 8
    normal.border_width_bottom = 3
    normal.border_color = accent.darkened(0.5)
    normal.content_margin_top = 12
    normal.content_margin_bottom = 12
    btn.add_theme_stylebox_override("normal", normal)

    var hover = normal.duplicate()
    hover.bg_color = accent.darkened(0.15)
    btn.add_theme_stylebox_override("hover", hover)

    var pressed = normal.duplicate()
    pressed.bg_color = accent.darkened(0.45)
    pressed.border_width_bottom = 1
    pressed.content_margin_top = 14
    btn.add_theme_stylebox_override("pressed", pressed)

    btn.add_theme_color_override("font_color", Color.WHITE)
    btn.add_theme_color_override("font_hover_color", Color(1, 1, 1, 0.95))

    btn.pressed.connect(callback)

    # Hover animation
    btn.pivot_offset = btn.custom_minimum_size / 2
    btn.mouse_entered.connect(func():
        var t = btn.create_tween()
        t.tween_property(btn, "scale", Vector2(1.03, 1.03), 0.1)
    )
    btn.mouse_exited.connect(func():
        var t = btn.create_tween()
        t.tween_property(btn, "scale", Vector2.ONE, 0.1)
    )
    return btn
```

### HUD Panel Style
```gdscript
func _create_hud_panel(pos: Vector2, size: Vector2) -> PanelContainer:
    var panel = PanelContainer.new()
    panel.position = pos
    panel.custom_minimum_size = size

    var style = StyleBoxFlat.new()
    style.bg_color = Color(0, 0, 0, 0.6)
    style.corner_radius_top_left = 6
    style.corner_radius_top_right = 6
    style.corner_radius_bottom_left = 6
    style.corner_radius_bottom_right = 6
    style.border_width_left = 1
    style.border_width_top = 1
    style.border_width_right = 1
    style.border_width_bottom = 1
    style.border_color = Color(1, 1, 1, 0.1)
    style.content_margin_left = 12
    style.content_margin_right = 12
    style.content_margin_top = 8
    style.content_margin_bottom = 8
    panel.add_theme_stylebox_override("panel", style)
    return panel
```

## Entity Visual Setup Pattern (MANDATORY for all entities)

Every game entity MUST use this pattern to ensure it is never invisible and always uses
existing assets when available. This is the FIRST thing to call when creating any entity.

```gdscript
## Call this for EVERY game entity in _ready() or when constructing nodes.
## It checks for user-provided sprites first, then falls back to procedural visuals.
## An entity should NEVER be left without a visual.

func _setup_entity_visual(node: Node2D, entity_name: String, size: Vector2, fallback_color: Color) -> void:
    # Priority 1: Check for user-provided PNG/JPG sprite
    var png_path = "res://assets/sprites/" + entity_name + ".png"
    var jpg_path = "res://assets/sprites/" + entity_name + ".jpg"

    if ResourceLoader.exists(png_path):
        var sprite = Sprite2D.new()
        sprite.texture = load(png_path)
        # Scale to desired size
        var tex_size = sprite.texture.get_size()
        sprite.scale = size / tex_size
        node.add_child(sprite)
        return

    if ResourceLoader.exists(jpg_path):
        var sprite = Sprite2D.new()
        sprite.texture = load(jpg_path)
        var tex_size = sprite.texture.get_size()
        sprite.scale = size / tex_size
        node.add_child(sprite)
        return

    # Priority 2: Check for generated SVG asset
    var svg_path = "res://assets/sprites/" + entity_name + ".svg"
    if ResourceLoader.exists(svg_path):
        var sprite = Sprite2D.new()
        sprite.texture = load(svg_path)
        node.add_child(sprite)
        return

    # Priority 3: Procedural visual (layered — NOT a flat shape)
    # This is the fallback. It MUST have visual depth.
    _draw_procedural_entity(node, size, fallback_color)


func _draw_procedural_entity(node: Node2D, size: Vector2, color: Color) -> void:
    # Create a dedicated drawing node for layered visuals
    var visual = Node2D.new()
    visual.name = "Visual"
    visual.set_script(_create_procedural_script(size, color))
    node.add_child(visual)


## Returns a GDScript string for procedural visuals (use with set_script or save to file)
## This ensures every procedural entity has: shadow + body gradient + highlight + outline + pulse
static func get_procedural_template(size: float, color: Color) -> String:
    return """extends Node2D

var body_color := Color(%f, %f, %f)
var outline_color := Color(%f, %f, %f)
var size := %f
var _time := 0.0

func _process(delta):
    _time += delta
    queue_redraw()

func _draw():
    # Drop shadow
    draw_circle(Vector2(1, 2), size, Color(0, 0, 0, 0.3))
    # Body with gradient
    draw_circle(Vector2.ZERO, size, body_color.darkened(0.15))
    draw_circle(Vector2(0, -1), size * 0.9, body_color)
    # Inner highlight
    draw_circle(Vector2(-size * 0.2, -size * 0.25), size * 0.45, body_color.lightened(0.3))
    # Outline
    draw_arc(Vector2.ZERO, size, 0, TAU, 32, outline_color, 1.5, true)
    # Pulse glow
    var glow_alpha = 0.1 + sin(_time * 2.0) * 0.05
    draw_circle(Vector2.ZERO, size * 1.3, Color(body_color.r, body_color.g, body_color.b, glow_alpha))
""" % [color.r, color.g, color.b,
       color.darkened(0.4).r, color.darkened(0.4).g, color.darkened(0.4).b,
       size.x / 2.0]
```

### When to use this pattern
- **Building a city map with building entities?** → `_setup_entity_visual(building_node, "bank", Vector2(64, 64), Color.BLUE)`
- **Creating enemies?** → `_setup_entity_visual(enemy_node, "guard", Vector2(48, 48), Color.RED)`
- **Player character?** → `_setup_entity_visual(player_node, "player", Vector2(64, 64), Color.CYAN)`

The pattern guarantees:
1. User-provided art is ALWAYS used when it exists (no more "drew dots instead of buildings")
2. Generated SVGs are used as second priority
3. Procedural fallback is NEVER a flat shape — always layered with depth
4. An entity is NEVER invisible

---

## External Art Pipeline

### AI Art Prompt Template
When visual_tier is "ai-art", generate prompts for each asset:
```
ASSET LIST FOR AI GENERATION:

1. player.png (64x64, transparent BG)
   Prompt: "Top-down pixel art knight character, blue armor, silver sword,
   idle stance, clean sprite sheet style, transparent background"
   Tool: DALL-E 3 / Midjourney --ar 1:1 --style raw

2. enemy_goblin.png (48x48, transparent BG)
   Prompt: "Top-down pixel art goblin enemy, green skin, red eyes,
   aggressive pose, game sprite, transparent background"

3. tileset_grass.png (256x256, seamless)
   Prompt: "Top-down grass tile texture, pixel art, seamless tileable,
   slight variation, game tileset, green tones"
```

### User-Provided Art Pipeline
```gdscript
# Check if user has provided sprites
func _setup_sprite(node: Node2D, sprite_name: String, fallback_color: Color):
    var sprite_path = "res://assets/sprites/" + sprite_name + ".png"
    if ResourceLoader.exists(sprite_path):
        var sprite = Sprite2D.new()
        sprite.texture = load(sprite_path)
        node.add_child(sprite)
    else:
        # Fall back to procedural visual
        var visual = _create_procedural_visual(fallback_color)
        node.add_child(visual)
```

## MCP Asset Tools

Use the MCP tools in this order for full-game builds:
1. `godot_generate_asset_pack` to create a coherent baseline set for the genre
2. `godot_generate_asset` for missing/special assets

The generated sprites should still be ENHANCED with shaders (glow outline, etc.) after loading:

```gdscript
var sprite = Sprite2D.new()
sprite.texture = load("res://assets/sprites/player.svg")
_apply_glow_outline(sprite, Color(0, 0.8, 1.0))
node.add_child(sprite)
```

Example asset-pack call (top-down shooter):
```json
{
  "preset": "top_down_shooter",
  "style": "neon",
  "format": "svg",
  "include_background": true,
  "include_ui": true
}
```

## Visual Quality Checklist

Before declaring any entity "done":
- [ ] Has visual depth (not flat color) — shadow + highlight + outline
- [ ] Has idle animation (bob, pulse, shimmer, rotation)
- [ ] Has feedback on interaction (flash, scale punch, particles)
- [ ] Contrasts against background (readable at all times)
- [ ] Consistent with color palette
- [ ] Uses shader for at least one effect (outline, glow, or hit flash)

Before declaring the game "done":
- [ ] Background has 2+ visual layers (gradient + grid/particles + vignette)
- [ ] UI panels are styled (not default Godot theme)
- [ ] Buttons have hover/press states with animation
- [ ] Transitions between screens are smooth (fade, slide)
- [ ] At least 3 particle effects in the game
- [ ] Game has a visual identity (someone could screenshot it and it looks intentional)
