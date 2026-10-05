---
name: xogot
description: 'Debug Godot games on iPhone/iPad via USB:'
---
# Xogot Skill

**Trit**: +1 (PLUS/Generator)  
**Domain**: game-development, mobile, godot, ios  
**Language**: GDScript, Swift  

---

## Overview

**Xogot** = Godot game engine for iPhone and iPad. Full 2D/3D game development environment running natively on iOS with touch-optimized interface.

```
┌─────────────────────────────────────────────────────────────────┐
│                         XOGOT STACK                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐         │
│  │   GDScript  │    │  3D Engine  │    │  2D Engine  │         │
│  │   Editor    │    │  Lighting   │    │  Tile Maps  │         │
│  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘         │
│         │                  │                  │                 │
│         └──────────────────┼──────────────────┘                 │
│                            ▼                                    │
│              ┌─────────────────────────┐                        │
│              │   Xogot iOS Runtime     │                        │
│              │   (SwiftGodot Bridge)   │                        │
│              └─────────────────────────┘                        │
│                            │                                    │
│              ┌─────────────┴─────────────┐                      │
│              ▼                           ▼                      │
│     ┌────────────────┐         ┌────────────────┐              │
│     │  iPhone/iPad   │         │  xogot_connect │              │
│     │  App Store     │         │  (USB Debug)   │              │
│     └────────────────┘         └────────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Full Godot Editor** | 2D/3D scene editing, animation, shaders on mobile |
| **Touch-Optimized** | Redesigned UI for small screens |
| **xogot_connect** | USB debugging from Mac to iOS device |
| **iCloud/GitHub Sync** | Projects sync via iCloud or Working Copy |
| **SwiftGodot** | Swift bindings for Godot extensions |
| **Free for Students** | Full access for 1 year |

---

## xogot_connect

Debug Godot games on iPhone/iPad via USB:

```gdscript
# In your Godot project, add xogot_connect addon
# Then in _ready():
extends Node

func _ready():
    if OS.has_feature("ios"):
        XogotConnect.start_debug_server()
```

### Setup

1. Install Xogot from App Store
2. Clone xogot_connect addon: `git clone https://github.com/xibbon/xogot_connect`
3. Copy `addons/xogot_connect` to your project
4. Enable in Project Settings → Plugins
5. Connect iPhone via USB
6. Run `xogot-connect` CLI on Mac

---

## GDScript Examples

### 2D Player Movement

```gdscript
extends CharacterBody2D

@export var speed: float = 200.0

func _physics_process(delta):
    var velocity = Vector2.ZERO
    
    # Touch input for mobile
    if Input.is_action_pressed("ui_right"):
        velocity.x += 1
    if Input.is_action_pressed("ui_left"):
        velocity.x -= 1
    if Input.is_action_pressed("ui_down"):
        velocity.y += 1
    if Input.is_action_pressed("ui_up"):
        velocity.y -= 1
    
    velocity = velocity.normalized() * speed
    move_and_slide()
```

### 3D Scene with Lighting

```gdscript
extends Node3D

func _ready():
    # Create directional light
    var light = DirectionalLight3D.new()
    light.light_energy = 1.0
    light.shadow_enabled = true
    add_child(light)
    
    # Create mesh
    var mesh_instance = MeshInstance3D.new()
    mesh_instance.mesh = BoxMesh.new()
    add_child(mesh_instance)
```

### Touch Input

```gdscript
extends Control

func _input(event):
    if event is InputEventScreenTouch:
        if event.pressed:
            print("Touch at: ", event.position)
    elif event is InputEventScreenDrag:
        print("Drag to: ", event.position)
```

---

## SwiftGodot Integration

For Swift extensions (advanced):

```swift
import SwiftGodot

@Godot
class MySwiftNode: Node {
    @Export var health: Int = 100
    
    override func _ready() {
        GD.print("Swift node ready!")
    }
    
    @Callable
    func takeDamage(amount: Int) {
        health -= amount
        if health <= 0 {
            queueFree()
        }
    }
}
```

---

## Project Structure

```
my_xogot_game/
├── project.godot
├── addons/
│   └── xogot_connect/
│       ├── plugin.cfg
│       └── xogot_connect.gd
├── scenes/
│   ├── main.tscn
│   ├── player.tscn
│   └── level_01.tscn
├── scripts/
│   ├── player.gd
│   └── game_manager.gd
├── assets/
│   ├── sprites/
│   ├── audio/
│   └── models/
└── export_presets.cfg
```

---

## GF(3) Integration

Xogot game development triadic workflow:

```
MINUS (-1): Design Phase
  - Scene composition
  - Asset import
  - Level layout

ERGODIC (0): Code Phase  
  - GDScript logic
  - State machines
  - Input handling

PLUS (+1): Deploy Phase
  - Build to device
  - Debug via xogot_connect
  - App Store submission
```

### Balanced Pipeline

```clojure
;; catp verification
[:import-assets :write-scripts :build-ios]  ; -1 + 0 + 1 = 0 ✓
[:design-scene :test-local :deploy-device]  ; -1 + 0 + 1 = 0 ✓
```

---

## Commands

```bash
# Clone xogot_connect
git clone https://github.com/xibbon/xogot_connect

# Check Xogot issues
gh issue list -R xibbon/XogotIssues

# SwiftGodot binary (for extensions)
gh release list -R xibbon/SwiftGodotXogotBinary
```

---

## Related Skills

| Skill | Trit | Bridge |
|-------|------|--------|
| `swift-ios` | 0 | SwiftGodot extensions |
| `iroh-p2p` | +1 | Multiplayer networking |
| `gay-mcp` | +1 | Deterministic color palettes |
| `algorithmic-art` | +1 | Procedural generation |

---

## Resources

- **App Store**: https://apps.apple.com/app/xogot-make-games-anywhere/id6469385251
- **Documentation**: https://docs.xogot.com
- **Blog**: https://blog.xogot.com
- **Discord**: https://discord.gg/TDEcyfHZAh
- **xogot_connect**: https://github.com/xibbon/xogot_connect
- **Issues**: https://github.com/xibbon/XogotIssues

---

**Skill Name**: xogot  
**Type**: Game Development / Mobile  
**Trit**: +1 (PLUS)  
**GF(3)**: Generator role - creates deployable games


---

## Autopoietic Marginalia

> **The interaction IS the skill improving itself.**

Every use of this skill is an opportunity for worlding:
- **MEMORY** (-1): Record what was learned
- **REMEMBERING** (0): Connect patterns to other skills  
- **WORLDING** (+1): Evolve the skill based on use



*Add Interaction Exemplars here as the skill is used.*
