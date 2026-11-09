---
name: godot-scene-architecture
description: 拆分 Godot 4 场景与组织节点时用。PackedScene 组件复用、节点引用 @onready @export %UniqueName、信号与直接调用的选择、分组 call_group、Autoload 与普通节点、组合与继承、状态机、暂停 process_mode、queue_free 与 is_instance_valid、_ready 顺序、场景切换。scene tree architecture, signals, autoload.
---

# Godot 场景架构

场景拆分、节点引用、节点通信、状态机、暂停与场景切换的约定。

默认结构：一个概念一个 `.tscn`，脚本挂在场景根，对外只露 `@export` 属性、信号和少量方法。

## 范围

| 不含 | 去哪 |
|---|---|
| 内容摆进 `.tscn` 还是代码生成、脚本生成场景文件 | godot-scene-authoring |
| 具体节点用法 | godot-2d godot-3d godot-ui godot-animation |
| `Resource` 当数据、存档 | godot-resources-data |
| `@tool` 与编辑器插件 | godot-editor-tooling |
| C# 信号、导出、生命周期写法 | godot-csharp |
| 失焦自动暂停、设置界面 | godot-ui |
| 屏幕外停用、大量实体 | godot-performance |
| 收尾音效、同时多声 | godot-audio |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 可复用对象 敌人 子弹 面板 | 独立 `.tscn` + `PackedScene.instantiate()` | 代码 `new` 整棵节点树 |
| 同场景内的节点引用 | `%UniqueName` 或 `@onready` 缓存 | 长路径 `get_node("A/B/C")`，每帧 `get_node` |
| 场景外的目标引用 | `@export var target: Node2D` | 写死 `/root/Main/Level/Player` |
| 一类对象批量通知 | `add_to_group` + `get_tree().call_group` | 手写注册表数组，全局事件总线 |
| 子对象通知父对象 | 信号 | 子节点 `get_parent().foo()` |
| 全局共享数据 | 自定义 `Resource`，或 autoload 只放全局状态 | Manager 套 Manager |
| 状态切换 | `enum` + `match`、状态子节点、`AnimationTree` | 一串 `is_jumping` `is_attacking` bool |
| 暂停菜单 | `SceneTree.paused` + `Node.process_mode` | 每个脚本判断 `is_paused` |
| 多个场景共用逻辑 | `class_name` 组件节点 | 复制粘贴，深继承链 |
| 场景切换 | `change_scene_to_file`、`change_scene_to_packed` | 手动 `free` 旧场景再 `add_child` |
| 非节点的纯逻辑对象 | `RefCounted` 或 `Resource` | 继承 `Node` 只为存数据 |

## 做法

### 实例化

```gdscript
class_name Bullet
extends Area2D

var direction: Vector2 = Vector2.RIGHT
var speed: float = 400.0

func _physics_process(delta: float) -> void:
	position += direction * speed * delta
```

```gdscript
class_name Spawner
extends Node2D

@export var bullet_scene: PackedScene

func fire(dir: Vector2) -> void:
	var bullet := bullet_scene.instantiate() as Bullet
	bullet.direction = dir
	get_parent().add_child(bullet)
	bullet.global_position = global_position
```

- 初始参数在 `add_child` 前设，`_ready` 里可读
- `global_position` 在 `add_child` 后设
- `add_child` 前设 `global_position`：2D 按本地坐标算，3D 报错
- 场景引用用 `@export var scene: PackedScene`，文件移动后引用不断
- 同脚本内固定不变的小场景可用 `preload`
- 代码生成节点并存进 `PackedScene` 时，每个节点设 `owner`，见 [references/lifecycle.md](references/lifecycle.md)

### 节点引用

```gdscript
extends Node2D

@export var target: Node2D
@export_node_path("Marker2D") var spawn_path: NodePath

@onready var score: Label = %ScoreLabel
@onready var sprite: Sprite2D = $Sprite2D
@onready var spawn: Marker2D = get_node(spawn_path)

func _process(_delta: float) -> void:
	if target != null:
		look_at(target.global_position)
```

| 写法 | 用于 |
|---|---|
| `$Name` | 直接子节点 |
| `%Name` | 同场景更深的节点，先在场景面板右键 `Access as Unique Name` |
| `@export var x: Node2D` | 场景外的目标，Inspector 里连 |
| `get_node_or_null` | 节点可能不存在 |

- 引用用 `@onready` 缓存为带类型成员，不在 `_process` 里取
- `@export` 节点引用在 `instantiate()` 返回时已解析
- `@export` 节点引用在 `_enter_tree` 和 `_ready` 可用，`_init` 里是 `null`
- 代码 `instantiate()` 的场景，场景外的引用由调用方赋值

### 通信

原则 call down, signal up。

| 方向 | 做法 |
|---|---|
| 父到子 | 直接调方法或设属性 |
| 子到父 | 子 `emit` 信号，父 `connect` |
| 兄弟之间 | 经共同父节点转发，或各自 `@export` 对方 |
| 子需要父提供的行为 | 父把方法赋给子的 `Callable` 属性 |

```gdscript
class_name Health
extends Node

signal changed(current: int, maximum: int)
signal died

@export var maximum: int = 100

@onready var current: int = maximum

func damage(amount: int) -> void:
	current = maxi(current - amount, 0)
	changed.emit(current, maximum)
	if current == 0:
		died.emit()
```

```gdscript
extends CharacterBody2D

@onready var health: Health = $Health

func _ready() -> void:
	health.died.connect(queue_free)
```

- 信号名用过去式：`died` `item_collected`
- 信号只报告已发生的事，要对方做事就调方法
- 成员初始化器读 `@export` 得到脚本默认值
- 依赖 Inspector 所设值的初值用 `@onready`
- 编辑器 Node 面板连的信号存在 `.tscn`，改方法名无提示。优先脚本里 `connect`

### 分组

```gdscript
extends Node2D

func raise_alarm() -> void:
	get_tree().call_group("guards", "alert", global_position)
```

- 分组用作一类对象的广播通道，不当全局注册表
- 加入分组：节点面板 Groups 页签，或 `add_to_group("guards")`
- `call_group_flags(SceneTree.GROUP_CALL_DEFERRED, ...)` 帧末执行，遍历中会增删节点时用
- 场景唯一对象用 `get_first_node_in_group("player")`，`_ready` 里取一次并缓存

### Autoload

用于跨场景存活的全局状态：存档槽、设置、场景切换器、跨关卡任务进度。`change_scene_to_*` 不释放 autoload。

```ini
[autoload]

Settings="*res://src/autoload/settings.gd"
```

- 能放进场景的就放进场景
- 不做全局音效池，场景自带 `AudioStreamPlayer`
- `*` 对应面板 Enable 列，开启后 GDScript 才有全局名
- C# 不读 `*`，自己写静态 Instance 属性
- autoload 的 `_ready` 早于主场景加载，取不到场景节点
- 共享函数用 `class_name` + `static func`，不需要 autoload
- 共享数据用自定义 `Resource`，不需要 autoload
- 不建 GameManager、EventBus、UIManager
- 不建信号总线，收发方无法追踪

### 组合与继承

```gdscript
class_name HurtBox
extends Area2D

@export var health: Health

func _ready() -> void:
	area_entered.connect(_on_area_entered)

func _on_area_entered(area: Area2D) -> void:
	if area is HitBox:
		health.damage(area.damage)
```

```gdscript
class_name HitBox
extends Area2D

@export var damage: int = 1
```

| 手段 | 用于 | 限制 |
|---|---|---|
| 组件子节点 | 多种对象共有的行为，如 `Health` `HurtBox`，不建 Damageable 基类 | 宿主用 `@export` 传入，不用 `get_parent()` |
| 脚本继承 | 同类事物的细分 | 一层，要第三层先拆组件 |
| 继承场景 | 同一模板的变体，如换贴图和数值的敌人 | 父场景改结构影响所有变体 |
| `Editable Children` | 改子场景内部节点 | 改动存在宿主场景，父场景改结构后易失效 |

### 状态机

| 状态数与转移 | 用法 |
|---|---|
| 2 到 5 个，转移简单 | `enum State` + `match`，见 [references/enum-state.md](references/enum-state.md) |
| 每个状态有进出逻辑和数据 | 每个状态一个子节点，见 [references/state-machine.md](references/state-machine.md) |
| 状态对应动画，转移由动画条件驱动 | `AnimationTree` 的 `AnimationNodeStateMachine` |

- 所有转移走一个入口函数，进出逻辑放在里面

### 暂停

`SceneTree.paused` 为 `true` 时，可暂停的节点停止 `_process`、`_physics_process` 和输入，物理模拟一并暂停。

```gdscript
extends Control

func _ready() -> void:
	process_mode = Node.PROCESS_MODE_ALWAYS
	hide()

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("pause"):
		get_tree().paused = not get_tree().paused
		visible = get_tree().paused
		get_viewport().set_input_as_handled()
```

| `process_mode` | 未暂停 | 暂停时 | 用于 |
|---|---|---|---|
| `PROCESS_MODE_INHERIT` 默认 | 同父级 | 同父级 | 普通节点，根节点按 PAUSABLE |
| `PROCESS_MODE_PAUSABLE` | 运行 | 停止 | 游戏内容 |
| `PROCESS_MODE_WHEN_PAUSED` | 停止 | 运行 | 暂停菜单内容 |
| `PROCESS_MODE_ALWAYS` | 运行 | 运行 | 切换暂停的节点、背景音乐、转场 |
| `PROCESS_MODE_DISABLED` | 停止 | 停止 | 关掉整棵子树 |

- `create_timer` 的 `process_always` 默认 `true`，暂停时照常计时
- `PROCESS_MODE_DISABLED` 不拦截已连接的信号，见 [references/lifecycle.md](references/lifecycle.md)
- `Node.set_process(false)` 只停 `_process`，不停 `_physics_process` 和输入

## 陷阱

| 现象 | 做法 |
|---|---|
| 子节点 `_ready` 里父节点未就绪 | `_ready` 子先于父。依赖子节点的初始化放在父的 `_ready` |
| `queue_free()` 后 `is_instance_valid` 仍为 `true` | 帧末才释放。判断销毁中用 `is_queued_for_deletion()` |
| 物理回调里改碰撞体报 `Can't change this state while flushing queries` 或 `Function blocked during in/out signal` | `set_deferred` 或 `call_deferred`，见 [references/lifecycle.md](references/lifecycle.md) |
| 手写 `.tscn` 的 `@export` 节点属性运行时为 `null` | 节点头写 `node_paths=PackedStringArray(...)`，见 [references/lifecycle.md](references/lifecycle.md) |
| `%Name` 取不到 | 跨实例化子场景无效。代码 `add_child` 的节点要设 `owner` |
| `await get_tree().process_frame` 报错 | 树外 `get_tree()` 为 `null`，先 `add_child` |
| `change_scene_to_*` 后 `current_scene` 为 `null` | 帧末才切换，见 [references/scene-switching.md](references/scene-switching.md) |
| 节点释放后 lambda 回调报错 | 用方法引用连接，对象释放时自动断开 |
| 每帧 `get_node` `find_child` `get_nodes_in_group`，或 `../Sibling` 路径 | `@onready` 缓存，或改 `@export` 和信号 |
| 一个 `Level.gd` 管相机、HUD、生成、计时 | 按职责拆子场景，Level 只组装 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/lifecycle.md](references/lifecycle.md)：回调顺序、构造期设值、`owner`、手写 `.tscn` 的 `node_paths`、`call_deferred`、释放与失效引用、禁用时的信号
- [references/scene-switching.md](references/scene-switching.md)：`change_scene_to_*` 行为、自己做切换、加载界面
- [references/enum-state.md](references/enum-state.md)：`enum` 加 `match` 完整示例
- [references/state-machine.md](references/state-machine.md)：状态子节点模板、`AnimationTree` 状态机
- https://docs.godotengine.org/en/stable/tutorials/best_practices/index.html
