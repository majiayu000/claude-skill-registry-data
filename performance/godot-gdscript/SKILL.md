---
name: godot-gdscript
description: 写或改 GDScript 时用。静态类型 := 与 Array[T] Dictionary[K, V]、class_name、@export @onready、信号 connect emit lambda、await 协程、match、setter getter、call_deferred、警告设置。GDScript typing, signals, coroutine, warnings.
---

# GDScript 写法

GDScript 语言层的写法与陷阱：类型、注解、信号、协程、对象有效性、警告。断言与日志见 references/syntax.md。目标 4.7，最低 4.4，更新的特性标版本号。

## 范围

| 不含 | 去哪 |
|---|---|
| 节点选型、场景组织、节点通信 | godot-scene-architecture |
| 数据资源 | godot-resources-data |
| C# 写法 | godot-csharp |
| 卡顿与每帧分配 | godot-performance |
| 无头加载脚本、抓警告 | godot-headless-testing |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 延时一次 | `await get_tree().create_timer(t).timeout` 或 Timer 节点 | `_process` 里累加 delta |
| 周期执行 | Timer 节点的 `timeout` 信号 | `_process` 里 `if elapsed > 0.5` |
| 输入轴 | `Input.get_vector()`、`Input.get_axis()` | 手写正负键相减 |
| 数值靠近目标 | `move_toward()`、`lerp()`、`Tween` | 手写 SmoothDamp |
| 取子节点 | `%Name`、`@export var x: Node`、`@onready` | 长硬路径 `get_node("../../A/B")` |
| 枚举名字互转 | `State.keys()`、`State.find_key(v)`、`State["RUN"]` | match 字符串表 |
| 数组变换 | `filter` `map` `reduce` `any` `all` `pick_random` `sort_custom` | for 加临时数组 |
| 随机 | `randi_range()`、`randf_range()`、`RandomNumberGenerator` | 自写 LCG |
| 浮点比较 | `is_equal_approx()`、`is_zero_approx()` | `==` 比较浮点 |
| 帧末调用 | `callable.call_deferred()`、`set_deferred()` | 用 Timer 凑一帧 |
| 数据放 Inspector 里改 | `Resource` 子类加 `@export` | JSON 手写解析 |

## 做法

### 静态类型

<!-- check: gdonly -->
```gdscript
extends Node

var speed: float = 200.0
var hp := 10
var names: Array[String] = []
var scores: Dictionary[StringName, int] = {}
var target: Node2D

func take_damage(amount: int) -> bool:
	hp -= amount
	return hp <= 0

func _ready() -> void:
	var raw: Dictionary = {"k": 1}
	var value: int = raw["k"]
	var sprite := get_node_or_null("Sprite") as Sprite2D
	print(value, sprite)
```

| 写法 | 结果 | 改法 |
|---|---|---|
| `:=` 右值是 Variant，如无类型 Dictionary 取值、`call()` | 错误 `inference_on_variant` | `var v: int = raw["k"]` |
| `var x := max(a, b)` | 同上，`clamp` `min` `max` `lerp` `abs` `sign` `floor` `ceil` `round` `snapped` 都返回 Variant | 用 `maxf` `clampi` 这类带类型版本 |
| `load(path)` | 返回 `Resource` | `var tex: Texture2D = load(path)`，常量路径用 `preload()` |
| `$Node`、`get_node()` | 返回 `Node` | `@onready var sprite: Sprite2D = $Sprite` |
| `x as Sprite2D` 类型不符 | 静默得 `null` | 只在就要这个结果时用 |
| `map()` 结果赋给 `Array[T]` | 报错，`map()` 返回无类型 Array | `typed.assign(untyped)` |
| 整数传给枚举参数 | `int_as_enum_without_cast` | 写成员名或显式转换 |

- `Array[T]` 运行时强制元素类型，`filter()` 保留元素类型
- `Dictionary[K, V]` 4.4+，不支持再嵌套类型
- 循环变量写类型：`for n: Node in nodes:`
- 大量数值用 `PackedFloat32Array`，`Array[float]` 仍是 Variant 数组
- 对象类型可为 `null`，数值与字符串类型不可

### class_name 与 preload

- `class_name Foo` 注册全局类，任何脚本可直接当类型和构造
- 类名不能与 autoload 同名，报 `Class "Foo" hides an autoload singleton`
- 类名不能与引擎类同名
- 无 `class_name` 的脚本用常量引用，`preload` 参数须是常量字符串
- 路径运行时才定用 `load()`

<!-- check: skip; gdonly -->
```gdscript
const Rifle := preload("res://weapons/rifle.gd")

var main_weapon: Rifle = Rifle.new()
```

- 两个脚本互相 `preload` 在 4.7 可加载，仍建议用 `class_name` 打断环
- `@export` 类型只能是内置类型、`Resource`、`Node`、枚举
- 3.x 的 `export var` `onready var` `yield` `connect("sig", obj, "method")` 在 4.x 都没了

### 注解

<!-- check: gdonly -->
```gdscript
extends Node2D

@export var speed: float = 200.0
@export_range(0.0, 1.0, 0.01) var ratio := 0.5
@export_enum("Idle", "Run") var mode: int = 0
@export_file("*.tscn") var next_scene: String
@export var bullet_scene: PackedScene
@export var spawn_point: Marker2D
@export_flags_2d_physics var hit_mask: int

@export_group("Loot")
@export var drops: Array[Resource] = []

@onready var label: Label = %Label
@onready var timer: Timer = $Timer

func _ready() -> void:
	timer.start()
	label.text = str(speed)
```

全表见 [references/annotations.md](references/annotations.md)。

| 时刻 | 发生 |
|---|---|
| 声明初值 | 脚本默认值 |
| `_init()` | 读到的是默认值 |
| 场景保存的值赋入 | 导出变量的 setter 此时调用，`@onready` 变量仍是 `null` |
| `@onready` 赋值 | 紧接着 `_ready()` |

- `@export` 的类型来自标注或默认值，都没有是解析错误，要 Variant 写 `: Variant`
- `@export var n: Node` 只在 Node 派生脚本里可用
- setter 里用节点前判断 `is_node_ready()`
- `@onready` 与 `@export` 同用是错误 `onready_with_export`
- 成员默认值里用 `$` 不带 `@onready` 是错误 `get_node_default_without_onready`
- 代码 `add_child()` 的节点直接赋成员，不需要 `@onready`
- 场景里已存的属性值覆盖脚本的新默认值
- 导出 `Resource` 随场景一起加载，大资源用 `@export_file` 存路径，用时 `load()`
- 4.5+ `@export_file` 存 UID，要原始路径用 `@export_file_path`
- `@export_tool_button("名字")` 4.4+，须配 `@tool`

### 信号

<!-- check: gdonly -->
```gdscript
extends Node

signal died
signal damaged(amount: int, source: Node)

@export var button: Button

func _ready() -> void:
	button.pressed.connect(_on_pressed)
	damaged.connect(_log_damage.bind("player"))
	died.connect(queue_free, CONNECT_ONE_SHOT)

func _on_pressed() -> void:
	damaged.emit(3, self)

func _log_damage(amount: int, _source: Node, tag: String) -> void:
	print(tag, amount)
```

- `bind()` 的参数追加在发射参数之后，`unbind(n)` 丢掉末尾 n 个发射参数
- 同一 Callable 连两次返回 `ERR_INVALID_PARAMETER` 并打印错误，先 `is_connected()`
- `CONNECT_ONE_SHOT` 触发一次后断开，`CONNECT_DEFERRED` 推迟到帧末
- 接收者释放时连接自动断开，lambda 捕获 `self` 成员时也一样
- 只由外部发射的信号加 `@warning_ignore("unused_signal")`
- `emit()` 不检查参数类型，接收方法参数类型不符时调用报错

<!-- check: gdonly -->
```gdscript
extends Node

func _ready() -> void:
	var stats: Dictionary = {"count": 0}
	var bump := func() -> void:
		stats["count"] += 1
	bump.call()
	bump.call()
	print(stats["count"])
```

- lambda 创建时按值捕获局部变量一次
- lambda 里 `count += 1` 只改副本，触发 `confusable_capture_reassignment`
- 要回写就捕获 Array、Dictionary 或对象，改其内容

### await 与协程

<!-- check: gdonly -->
```gdscript
extends Node

signal answered(choice: int)

func open_door(door: Node3D) -> void:
	await get_tree().create_timer(1.0).timeout
	if not is_inside_tree() or not is_instance_valid(door):
		return
	door.hide()

func ask() -> int:
	var choice: int = await answered
	return choice
```

| 情况 | 结果 |
|---|---|
| 调用协程不写 `await` | 跑到第一个 `await` 就返回，`missing_await` 默认关 |
| 信号带 1 个参数 | `await` 得到该值 |
| 信号带多个参数 | 得到 Array |
| 信号无参数 | 得到 `null` |
| `await` 期间自己离开场景树 | `get_tree()` 打印错误并返回 `null` |
| `await` 期间自己被 `free()` | 协程不再恢复，后面的清理不执行 |

- `await` 之后先检查 `is_inside_tree()` 和目标 `is_instance_valid()`
- 要清理的状态放 `_exit_tree()` 或 `tree_exiting` 里复位
- `create_timer` 默认暂停时也走，要受暂停影响第二参数传 `false`
- 等一帧 `await get_tree().process_frame`，等物理帧 `physics_frame`
- 没有内置超时，用 Timer 的 `timeout` 和业务信号谁先到谁处理

### 对象有效性

| 对象 | 规则 |
|---|---|
| 已 `free()` 的对象变量 | 不自动变 `null`，访问报 `previously freed`，用 `is_instance_valid()` 判断 |
| `queue_free()` 后帧末前 | `is_instance_valid()` 仍为真，用 `is_queued_for_deletion()` |
| `RefCounted`、`Resource` | 引用计数，不悬空，不用 `free()` |
| 长期持有可能被释放的节点 | 存 `weakref(node)`，用时 `get_ref()` |

- 物理回调、信号回调、遍历子节点时释放用 `queue_free()`
- `_init()` 里节点不在树内，`get_node()` 失败

### Callable 与延迟调用

<!-- check: gdonly -->
```gdscript
extends Node

func _ready() -> void:
	var child := Node.new()
	add_child.call_deferred(child)
	set_deferred(&"process_mode", Node.PROCESS_MODE_DISABLED)
	var sorted: Array[int] = [3, 1, 2]
	sorted.sort_custom(func(a: int, b: int) -> bool: return a > b)
```

- `call_deferred` 在当前帧空闲阶段末尾执行，返回值永远是 `null`
- 物理回调里改碰撞形状、`Area2D.monitoring`、`CollisionShape2D.disabled` 用 `set_deferred`
- 线程里碰场景树只能 `call_deferred`
- 方法引用写 `_on_pressed`，不写 `Callable(self, "_on_pressed")`
- `callable.is_valid()` 判断绑定对象是否还在

### 警告设置

项目设置 `debug/gdscript/warnings/*`，0 忽略、1 警告、2 错误，高级设置里可见。全表见 [references/warnings.md](references/warnings.md)。全类型化项目建议：

```ini
[debug]

gdscript/warnings/untyped_declaration=2
gdscript/warnings/missing_await=2
gdscript/warnings/narrowing_conversion=2
gdscript/warnings/int_as_enum_without_cast=2
gdscript/warnings/unassigned_variable=2
```

- 单句忽略 `@warning_ignore("unused_signal")`
- 区域忽略 `@warning_ignore_start` 与 `@warning_ignore_restore`
- `directory_rules` 默认忽略 `res://addons`

## 陷阱

match、静态成员、setter、super 的完整写法见 [references/syntax.md](references/syntax.md)。

| 现象 | 做法 |
|---|---|
| `5 / 2` 得 `2`，触发 `integer_division` | `5 / 2.0` 或 `float(a) / b` |
| `var b = a` 后改 `b`，`a` 也变 | Array Dictionary 按引用传递，`duplicate()`，嵌套 `duplicate(true)` |
| `const` 数组 `append` 报 `Array is in read-only state` | `const` 集合只读，改用 `var` |
| 父类 `_init()` `_ready()` 没执行 | 子类覆盖后要显式 `super()` |
| 声明初值没触发 setter | 初值不调 setter，类内其他赋值才调 |
| `unused_parameter` | 参数名加下划线前缀 `_delta` |
| `narrowing_conversion` | 浮点传整数参数时 `int()` `roundi()` `floori()` |
| 固定种子不生效 | 运行时已自动 `randomize()`，用 `seed()`，之后别再 `randomize()` |
| 遍历数组时增删元素跳项 | 遍历 `arr.duplicate()` 或倒序下标 |
| `call("do_it")` 拼写错到运行时才暴露 | 用 Callable 引用与信号对象 |
| `native_method_override` 报错 | 方法与引擎原生方法同名，改名 |
| `shadowed_variable` | 局部变量与成员同名，改名 |
| 带 `static var` 的脚本持有大资源不释放 | 脚本不会卸载，手动清空 |

## 参考

- [references/annotations.md](references/annotations.md)：导出与其他注解全表
- [references/syntax.md](references/syntax.md)：match、静态成员、StringName、setter、super、可变参数与抽象类、断言与日志
- [references/warnings.md](references/warnings.md)：全部警告与默认值
- https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_exports.html
- https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/warning_system.html
