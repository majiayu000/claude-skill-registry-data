---
name: godot-scene-authoring
description: 在 Godot 4 里新做关卡、房间、HUD、菜单、NPC、道具、背景时用，决定内容摆进 .tscn 还是代码运行时搭。新建项目第一个场景，往已有项目加场景，打开场景一片空看不到东西，美术策划要在编辑器里直接看和调，自定义显示节点在编辑器里不显示，@tool 节点把材质 z_index 写进 tscn，确定性模拟 联机 服务器要读场景里摆的位置。先自查项目是摆在场景里还是运行时生成，再按结果新做或迁移。脚本生成 tscn、@tool 自绘节点、预制场景、_validate_property、internal 子节点、NOTIFICATION_EDITOR_PRE_SAVE、C# 重载。level authoring, WYSIWYG, prefab, data-driven, bake on save, empty scene, audit.
---

# Godot 场景摆放

内容定义在哪：有位置、有外观的东西摆进 `.tscn`，代码只管规则和运行时才出现的东西。

验收标准：不运行游戏，在编辑器里拖动灯、NPC、血条，存盘后游戏里同样改变。

## 范围

| 不含 | 去哪 |
|---|---|
| 场景拆分、节点通信、`owner` 规则 | godot-scene-architecture |
| `EditorPlugin`、Inspector 插件、导入插件 | godot-editor-tooling |
| 自定义 `Resource`、配表 | godot-resources-data |
| C# 热重载通用规则 | godot-csharp |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 背景 道具 灯 HUD 菜单布局 | 节点直接摆进 `.tscn`，UI 用 Container 和 `Theme` | 代码 `new` 整棵树，场景只剩空壳 |
| 运行时才出现的敌人 子弹 列表行 | 预制 `.tscn` + `PackedScene.instantiate()` | 代码逐个 `new` 子节点再设外观 |
| 不开编辑器生成场景文件 | `extends SceneTree` 脚本建节点、设 owner、`PackedScene.pack`、`ResourceSaver.save` | 手拼大段 tscn 文本 |
| 自定义显示节点在编辑器里可见 | `@tool` + 按导出属性 `_draw` 或建内部子节点 | 只在运行时按配表建 |
| 代码派生的属性不进 tscn | `_validate_property` 去掉 `PROPERTY_USAGE_STORAGE` | 存盘前清掉、存完再设回 |
| 节点自己生成的辅助子节点 | `add_child(n, false, Node.INTERNAL_MODE_BACK)` 不设 owner | 设 owner 存进场景 |
| 模拟 服务器 回放要读摆好的位置 | 存盘时导出：`Node.NOTIFICATION_EDITOR_PRE_SAVE` 或 `EditorPlugin.scene_saved` | JSON 里手写坐标 |
| 同一类物件不同外观 | 预制场景实例后覆盖属性，或继承场景 | 配表里写贴图路径 颜色 尺寸 |
| Tiled LDtk 外部关卡 | `EditorImportPlugin` 导入成场景，见 godot-editor-tooling | 运行时解析 |

- 默认直接导出 `Texture2D`，拖进 Inspector
- 有资源表或 MOD 覆盖时导出 ID 字符串，`@tool` 里解析成贴图

## 做法

### 自查

动手前先确认项目现在的做法，细节和脚本见 [references/audit.md](references/audit.md)：

1. 读几个现有 `.tscn`，看节点数和游戏画面对不对得上
2. 搜脚本里的 `.new()` 加 `add_child`、给 `Control` 设 `position` `size`、`load` 贴图
3. 搜配表里的坐标、贴图路径、颜色字段
4. 无头跑审计脚本，数 `_ready` 后多出的、owner 为空的节点

| 结果 | 做法 |
|---|---|
| 新项目，或还没有内容场景 | 按下文新做 |
| 内容摆在场景里 | 照现有结构加 |
| 场景空壳，内容运行时建 | 报告自查结果和迁移范围，同意后按 [references/migration.md](references/migration.md) 迁 |
| 未同意迁移 | 新系统摆进场景，已有的代码搭系统跟着现状写 |
| 两种都有 | 按系统分开判断，HUD、菜单、关卡、NPC 各算一项 |

- 程序生成的地图、按数据数量建的列表行属于运行时内容，不算问题

### 内容归属

| 内容 | 放哪 |
|---|---|
| 背景层、灯、NPC 站位和朝向、道具、机关外观、HUD 和菜单布局 | `.tscn` |
| 敌人、投射物、掉落、列表行、弹窗 | 预制 `.tscn`，代码 `instantiate()` 后设数据 |
| 出现条件、对话、商店、波次、伤害 | `Resource` 或配表 |
| 模拟 服务器要的位置和尺寸 | 场景里摆，存盘导出成数据 |
| 程序生成的地图 | 代码生成，`@tool` 里用同一种子给编辑器生成 |

- 同一项只有一个来源，外观不在场景和配表里各写一份

### 新做场景

关卡的树，每一项都是存盘的节点，重复的东西是预制场景实例：

```
Level            Node2D  level.gd
├ Background     Parallax2D / Sprite2D
├ Ground         TileMapLayer
├ Props          Node2D / crate.tscn 实例若干
├ Npcs           Node2D / npc.tscn 实例 覆盖朝向和对话 ID
├ SpawnPoints    Node2D / Marker2D 若干
└ Hud            hud.tscn 实例
```

不开编辑器时用一次性脚本生成，`godot --headless -s make_level.gd`，跑完删掉脚本：

<!-- check: gdonly -->
```gdscript
extends SceneTree

func _initialize() -> void:
	var level := Node2D.new()
	level.name = "Level"
	var points := Node2D.new()
	points.name = "SpawnPoints"
	level.add_child(points)
	points.owner = level
	for i in 3:
		var marker := Marker2D.new()
		marker.name = "Spawn%d" % i
		marker.position = Vector2(200.0 * i, 0.0)
		points.add_child(marker)
		marker.owner = level
	var packed := PackedScene.new()
	packed.pack(level)
	ResourceSaver.save(packed, "res://level.tscn")
	level.free()
	quit()
```

- 每个后代都设 `owner` 为场景根，只设直接子节点不够
- 实例化的子场景只给它的根设 owner
- 编辑器里的场景根是 `EditorInterface.get_edited_scene_root()`
- 小场景可直接写 tscn 文本，注意事项见 godot-scene-architecture

脚本只取场景里摆好的节点，运行时内容从预制场景实例化：

```gdscript
extends Node2D

@export var enemy_scene: PackedScene
@onready var spawn_points: Node2D = $SpawnPoints

func spawn_wave() -> void:
	for point: Node in spawn_points.get_children():
		var enemy := enemy_scene.instantiate() as Node2D
		enemy.position = (point as Node2D).position
		add_child(enemy)
```

### 自绘节点

`Sprite2D` 能表达的用 `Sprite2D`。需要自己语义的节点，如按米算高度，同样按导出属性在编辑器里画出来：

```gdscript
@tool
class_name GroundProp
extends Node2D

@export var texture: Texture2D:
	set(value):
		texture = value
		queue_redraw()
@export var height: float = 64.0:
	set(value):
		height = value
		queue_redraw()

func _draw() -> void:
	if texture == null:
		return
	var size := texture.get_size() * (height / texture.get_height())
	draw_texture_rect(texture, Rect2(Vector2(-size.x / 2.0, -size.y), size), false)
```

- 存盘的是节点和导出属性，画法跟着脚本走
- setter 里只 `queue_redraw()` 或改自身状态
- setter 在进树前就会调用，用到树的操作先判断 `is_inside_tree()`

### 派生属性

`_ready` 或 setter 里按环境算出的属性，如按视口选的 `material`、按深度算的 `z_index`，存盘时照样写进 tscn。用 `_validate_property` 去掉存盘位：

```gdscript
@tool
extends Node2D

@export var depth: float = 0.0:
	set(value):
		depth = value
		z_index = -10 if depth > 0.0 else 10

func _validate_property(property: Dictionary) -> void:
	if property.name == "z_index":
		property.usage &= ~PROPERTY_USAGE_STORAGE
```

- 对继承来的引擎属性也生效，脚本须是 `@tool`
- 去掉后场景里手设的值也不存，该属性只能由代码决定

节点自己生成、不属于内容的子节点，如地面条、阴影，用 internal 子节点，不设 owner：

```gdscript
@tool
extends Node2D

var _shadow: Sprite2D

func _ready() -> void:
	_shadow = Sprite2D.new()
	_shadow.modulate = Color(0.0, 0.0, 0.0, 0.4)
	add_child(_shadow, false, Node.INTERNAL_MODE_BACK)
```

| | 不设 owner | 不设 owner 且 internal |
|---|---|---|
| 视口里画出来 | 是 | 是 |
| 场景面板里看得到、点得中 | 否 | 否 |
| 存进 tscn | 否 | 否 |
| `get_children()` 拿得到 | 是 | 否，要 `get_children(true)` |
| `duplicate()` 和 Ctrl+D 带上 | 是 | 否 |

- 只不设 owner 时，复制节点会连生成的子节点一起复制，新节点 `_ready` 再建一份
- 设了 owner 的 internal 子节点照样存盘，读回来变成普通子节点

### 存盘导出

确定性模拟、回滚联机、服务器不依赖场景树时，位置照样摆在场景里，存盘时导出成数据文件一起提交：

```gdscript
@tool
extends Node2D

@export_file("*.json") var export_path: String = "res://room_points.json"

func _notification(what: int) -> void:
	if what == NOTIFICATION_EDITOR_PRE_SAVE:
		export_points()

func export_points() -> void:
	var points: Array[Dictionary] = []
	for child: Node in get_children():
		var marker := child as Marker2D
		if marker != null:
			points.append({"name": String(marker.name), "x": marker.position.x, "y": marker.position.y})
	var file := FileAccess.open(export_path, FileAccess.WRITE)
	file.store_string(JSON.stringify({"points": points}, "\t"))
```

- 只在编辑器里、打包场景前发给被存场景的每个节点
- 这时节点被锁，`add_child` `remove_child` 报错，只能读写属性和文件
- 统一导出放在插件里时连 `EditorPlugin.scene_saved`，文件写盘后调用

### 编辑器视口

| 项 | 编辑器里 |
|---|---|
| 场景里的 `Camera2D` | 不生效，跟镜头走的视差层、跟随节点停在原点 |
| `CanvasLayer` 内容 | 跟着编辑器平移缩放 |
| `SubViewport` 内容 | 按单位变换贴出，只显示子视口尺寸以内 |
| 单个 `SubViewport` 开的 `Viewport.use_hdr_2d` | 不生效，只按项目设置 `rendering/viewport/hdr_2d` |
| `@tool` 的 `_process` | 低处理器模式下只在重绘时推进 |
| 切换场景标签页 | 场景根先出树再进树，`_ready` 只跑一次 |

- 材质按 `get_viewport()` 在进树后选
- `_process` 里每帧 `queue_redraw()` 会让编辑器一直刷新
- `_exit_tree` 里释放的东西在 `_enter_tree` 里补回
- 改了全局着色器参数、静态缓存的节点，在 `_exit_tree` 里还原
- 换场景时先 `remove_child()` 再 `queue_free()`，否则旧节点帧末出树会还原掉新设的值
- 只在当前编辑场景里做的事，判断 `is_part_of_edited_scene()`，`_ready` 里可用

## 陷阱

| 现象 | 做法 |
|---|---|
| 生成节点存进了子场景文件 | 生成节点挂在实例化子场景下且 owner 设为子场景根。生成节点一律不设 owner |
| 预制场景里多个 ColorRect Label 要统一换材质 | 子节点勾 `CanvasItem.use_parent_material`，代码只给根设 |
| 只打开存盘也出 diff | 编辑器给旧 tscn 补 `uid`，新版补 `unique_id`，和逻辑改动分开提交 |
| 提交的导出数据过期 | 导出只在编辑器存盘时写。加无头检查：重新导出并与提交的文件比对 |
| 美术在编辑器看得到但改了不生效 | 编辑器里只画了一份不存盘的假画面。内容要真的在场景里 |
| 同一系统里混用摆场景和代码搭 | 先自查，跟随该系统现状 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法、`[Tool]` 热重载
- [references/audit.md](references/audit.md)：自查清单、搜索命令、无头审计脚本、报告格式
- [references/migration.md](references/migration.md)：迁移顺序、坐标换算、无头编辑器验证插件、常见报错
- https://docs.godotengine.org/en/stable/tutorials/best_practices/scenes_versus_scripts.html
- https://docs.godotengine.org/en/stable/tutorials/best_practices/scene_organization.html
- https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html
