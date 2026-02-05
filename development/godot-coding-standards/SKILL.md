---
name: godot-coding-standards
description: Godot 4.x GDScript 编码规范。当编写、审查、修改 Godot 代码时使用。适用于：GDScript 脚本、场景创建、组件设计、Resource 类、信号连接、节点组织、类型注解、命名规范、性能优化。触发词：godot, gdscript, 组件, 信号, export, 场景。
---

# Godot 4.x 编码规范

为 Godot 4.x 项目设计的编码规范，确保代码的**通用性、模块化、可复用性、简洁性**。

## 核心原则

1. **通用性** - 使用 `@export` 使组件可配置，避免硬编码
2. **模块化** - 单一职责，组件模式，信号松耦合
3. **可复用性** - Resource 类存储数据，清晰公共接口
4. **简洁实用** - 注重实用，避免过度设计

## 快速参考

### 命名规范
```gdscript
class_name PlayerHealth      # PascalCase
var max_health: float        # snake_case
const MAX_SPEED = 200.0      # UPPER_SNAKE_CASE
signal health_changed()      # snake_case
func take_damage() -> void:  # snake_case
```

### 代码组织顺序
```gdscript
extends CharacterBody2D
class_name Player
## 类文档注释

signal died()                          # 1. 信号
enum State { IDLE, MOVING }            # 2. 枚举/常量
@export var speed: float = 150.0       # 3. @export 变量
var health: float = 100.0              # 4. public 变量
var _internal: int = 0                 # 5. private 变量 (_前缀)
@onready var sprite: Sprite2D = $Sprite2D  # 6. @onready

func _ready() -> void: pass            # 7. 内置回调
func _physics_process(delta): pass     # 8. 内置回调
func take_damage(dmg: Damage): pass    # 9. 公共方法
func _update_state(): pass             # 10. 私有方法
func on_damaged(): pass                # 11. 信号处理 (on_前缀)
```

### 类型注解 (必须)
```gdscript
var max_health: float = 100.0
var items: Array[Item] = []
func attack(target: Node2D) -> bool:
    return true
```

### Export 变量分组
```gdscript
@export_group("Movement")
@export var speed: float = 150.0
@export var jump_force: float = 300.0

@export_group("Combat")
@export var damage: Damage
```

### 信号使用
```gdscript
# 声明
signal health_changed(current: float, maximum: float)

# 连接 (Godot 4 风格)
health_component.died.connect(on_death)

# 发射
health_changed.emit(health, max_health)
```

## 详细规范

完整的详细规范请参阅：
- [REFERENCE.md](REFERENCE.md) - 完整编码规范和示例
- [CHECKLIST.md](CHECKLIST.md) - 代码审查检查清单

## 组件模式示例

```gdscript
extends Node
class_name Health

## 可复用的生命值组件

signal health_changed(current: float, maximum: float)
signal died()

@export var max_health: float = 100.0

var health: float = max_health:
    set(val):
        health = clamp(val, 0, max_health)
        health_changed.emit(health, max_health)
        if health <= 0:
            died.emit()

func take_damage(amount: float) -> void:
    health -= amount

func heal(amount: float) -> void:
    health += amount
```

## 检查清单 (快速版)

- [ ] 类型注解完整？
- [ ] 使用 `@export` 可配置？
- [ ] 信号而非直接调用？
- [ ] 单一职责？
- [ ] 有文档注释？
