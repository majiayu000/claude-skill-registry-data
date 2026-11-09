---
name: godot-editor-tooling
description: 写 Godot 4 编辑器扩展时用。@tool 工具脚本、@export_tool_button、EditorPlugin 与 plugin.cfg、EditorInspectorPlugin 定制 Inspector、EditorImportPlugin 导入插件、EditorScript 批处理、撤销重做、停靠面板、主屏幕插件、_get_property_list 动态属性、配置警告。editor plugin, tool script, inspector, importer.
---

# Godot 编辑器工具

编辑器内的扩展：@tool 脚本、数据编辑、Inspector 定制、插件、导入。默认：数据编辑器做成 Inspector 编辑的 `Resource`，不做独立工具窗口。

## 范围

| 不含 | 去哪 |
|---|---|
| 数据怎么定义、加载、存档 | godot-resources-data |
| 游戏内 UI | godot-ui |
| 节点在编辑器里生成子节点与 `owner` | godot-scene-authoring |
| 无头运行、CI、导出命令行 | godot-headless-testing |
| C# 命名映射、源码生成器 | godot-csharp |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 编辑一张数据表 | 自定义 `Resource` + `@export` | 独立编辑窗口，JSON 加手写表单 |
| Inspector 里放按钮 | `@export_tool_button` 4.4+ | 为放一个按钮写 `EditorInspectorPlugin` |
| 按条件隐藏 禁用属性 | `_validate_property` | 重写 `_get_property_list` 整体伪造 |
| 属性联动刷新 | setter 里 `notify_property_list_changed()` | 定时器刷新 Inspector |
| 节点配置检查 | `_get_configuration_warnings` | 打印日志代替警告三角 |
| 属性分组 范围 下拉 文件选择 | `@export_*` 注解 | 自定义属性控件 |
| 外部文件变成资源 | `EditorImportPlugin` | 运行时解析，或手动转换后忘了重转 |
| 3D 场景导入后统一处理 | `EditorScenePostImport` | 手动改每个场景 |
| 一次性批处理 | `EditorScript`，或 tool 按钮 | 临时场景加 `_ready` 里跑完再删 |
| 撤销重做 | `EditorUndoRedoManager` | 直接改属性，Ctrl+Z 无效 |
| 文件变化通知 | `EditorFileSystem` 信号 | `_process` 里轮询 mtime |
| 编辑器颜色 图标 缩放 | `get_theme_color(名, "Editor")`、`EditorInterface.get_editor_theme()` | 硬编码 `Color` 和像素 |
| 快捷键 | `Shortcut` 资源 | `_input` 里手写 `keycode` 判断 |
| 停靠面板 | `EditorDock` 4.6+，4.5 及以下 `add_control_to_dock` | 独立 `Window` |
| 右键菜单 命令面板 | `EditorContextMenuPlugin` 4.4+，`EditorCommandPalette.add_command` | 监听鼠标自己弹菜单 |
| 项目里自定义设置 | `ProjectSettings.add_property_info` | 另存一份配置文件 |
| 插件自带 Autoload | `_enable_plugin` 里 `add_autoload_singleton` | 让用户手动加 Autoload |
| 顶部主屏幕标签页 | `_has_main_screen` | 独立窗口 |

## 做法

### 数据编辑器

数据做成 `@tool` 的 `Resource`，Inspector 自带撤销、拖拽引用、复制粘贴与 diff。

```gdscript
@tool
class_name SpawnRule
extends Resource

enum Kind { ONCE, TIMED }

@export var kind: Kind = Kind.ONCE:
	set(value):
		kind = value
		notify_property_list_changed()
		emit_changed()
@export var interval: float = 1.0:
	set(value):
		interval = value
		emit_changed()
@export var scene: PackedScene

func _validate_property(property: Dictionary) -> void:
	if property.name == "interval" and kind != Kind.TIMED:
		property.usage = PROPERTY_USAGE_NO_EDITOR
```

- 资源加 `@tool`，`_validate_property` 才在编辑器里运行
- `PROPERTY_USAGE_NO_EDITOR` 只隐藏，值照常存盘
- 只读：`property.usage |= PROPERTY_USAGE_READ_ONLY`
- 整张表用数据库资源持有 `Array[SpawnRule]`，Inspector 里增删排序
- 重置箭头：重写 `_property_can_revert` 与 `_property_get_revert`
- 图形数据如对话树、空间数据如地图，才考虑主屏幕插件或 `GraphEdit`
- 自定义界面只是另一个编辑入口，数据仍存 `Resource`

### @tool 脚本

```gdscript
@tool
extends Node2D

@export var rule: SpawnRule:
	set(value):
		if rule != null and rule.changed.is_connected(queue_redraw):
			rule.changed.disconnect(queue_redraw)
		rule = value
		if rule != null:
			rule.changed.connect(queue_redraw)
		queue_redraw()

func _draw() -> void:
	if rule != null and Engine.is_editor_hint():
		draw_circle(Vector2.ZERO, 16.0, Color.RED)

func _process(delta: float) -> void:
	if Engine.is_editor_hint():
		return
	position.x += 10.0 * delta
```

- `@tool` 脚本的 `_process` `_physics_process` `_input` 在编辑器里都跑
- 游戏逻辑用 `Engine.is_editor_hint()` 挡住
- `@export` 的 setter 在进树前调用，用子节点先判断 `is_node_ready()`
- 改资源内部属性不触发持有者的 setter
- 资源的 setter 里 `emit_changed()`，持有者连 `changed`，换资源时断开旧的
- `_init` 里读 `@export` 得到默认值，Inspector 的值在之后赋入
- 子类脚本不继承 `@tool`，要再写一遍

| `@tool` 脚本用到的非 tool 脚本 | 编辑器里的行为 |
|---|---|
| `load` 到的资源、`set_script` 挂上的 | 占位实例，方法不可用 |
| `.new()` 造的实例 | 正常 |
| 静态方法、常量、枚举 | 正常 |
| 静态变量 | 初值不执行，带类型读出类型默认值，无类型读出 `null` |

- 脚本对节点的改动没有撤销，场景也不标为未保存
- 批量改动走 `EditorUndoRedoManager`，否则调 `EditorInterface.mark_scene_as_unsaved()`

### 动态属性

属性集合由其他数据决定时才重写 `_get_property_list`，配合 `_get` 与 `_set`。

```gdscript
@tool
class_name WaveTable
extends Resource

@export var wave_count: int = 3:
	set(value):
		wave_count = clampi(value, 1, 20)
		counts.resize(wave_count)
		notify_property_list_changed()

var counts: PackedInt32Array = PackedInt32Array([5, 8, 12])

func _get_property_list() -> Array[Dictionary]:
	var props: Array[Dictionary] = []
	for i in wave_count:
		props.append({
			"name": "wave_%d_count" % i,
			"type": TYPE_INT,
			"usage": PROPERTY_USAGE_DEFAULT,
		})
	return props

func _get(property: StringName) -> Variant:
	if property.begins_with("wave_") and property.ends_with("_count"):
		return counts[property.get_slice("_", 1).to_int()]
	return null

func _set(property: StringName, value: Variant) -> bool:
	if property.begins_with("wave_") and property.ends_with("_count"):
		counts[property.get_slice("_", 1).to_int()] = value
		return true
	return false
```

- 可变长度数据先用 `@export var counts: Array[int]`，Inspector 原生增删
- 属性要带 `PROPERTY_USAGE_STORAGE` 才存盘，`PROPERTY_USAGE_DEFAULT` 已含
- 结构变了调 `notify_property_list_changed()`，Inspector 才重建
- `_validate_property` 不处理这些属性，`usage` 直接写在返回字典里
- `_get_property_list` 可能在保存线程调用，不碰场景树
- JSON 键值伪装成属性要自己做撤销与存盘，数据改成 `Resource`

### Inspector 按钮与校验

```gdscript
@tool
extends Node2D

@export var target: Node2D:
	set(value):
		target = value
		update_configuration_warnings()
@export_tool_button("Snap To Target", "Reload") var snap_action: Callable = snap_to_target

func _get_configuration_warnings() -> PackedStringArray:
	var warnings := PackedStringArray()
	if target == null:
		warnings.append("target 未设置")
	return warnings

func snap_to_target() -> void:
	var ur := EditorInterface.get_editor_undo_redo()
	ur.create_action("Snap To Target", UndoRedo.MERGE_DISABLE, self)
	ur.add_do_property(self, &"global_position", target.global_position)
	ur.add_undo_property(self, &"global_position", global_position)
	ur.commit_action()
```

- `@export_tool_button` 第二个参数是编辑器内置图标名
- 按钮回调的改动走 `EditorUndoRedoManager`
- `EditorInterface.get_editor_undo_redo()` 4.4+，插件里 `get_undo_redo()` 是同一对象
- `_get_configuration_warnings` 要求脚本 `@tool`，条件变了调 `update_configuration_warnings()`
- `Resource` 没有警告三角，校验用 tool 按钮加 `push_warning`
- 游戏里也运行的脚本不能直接写 `EditorInterface`，编辑器部分拆到单独脚本

### 插件

目录 `addons/<名>/` 放 `plugin.cfg` 与 `plugin.gd`，在 Project Settings 的 Plugins 页启用。

| 内容 | 位置 |
|---|---|
| 骨架、Dock、主题、快捷键、菜单、文件变化、项目设置、Autoload、主屏幕 | [references/editor-recipes.md](references/editor-recipes.md) |
| 编辑器里造节点、`EditorScript`、撤销重做 | [references/editor-recipes.md](references/editor-recipes.md) |
| 自定义属性控件、`EditorInspectorPlugin` | [references/inspector-plugin.md](references/inspector-plugin.md) |
| `@export_*` 注解一览 | [references/export-annotations.md](references/export-annotations.md) |

- `_enter_tree` 注册，`_exit_tree` 反注册并 `queue_free` 自建控件
- 文件变化连 `EditorFileSystem` 的 `filesystem_changed` 与 `resources_reimported`
- 尺寸乘 `EditorInterface.get_editor_scale()`
- 快捷键用 `Shortcut` 资源
- 节点与资源图标用 `class_name` 加 `@icon`，不用 `add_custom_type`
- 图标和面板场景写 `res://addons/<名>/...` 完整路径

### 导入外部数据

| 数据 | 做法 |
|---|---|
| 常改，源文件放进工程自动转 `Resource` | `EditorImportPlugin`，见 [references/import-plugin.md](references/import-plugin.md) |
| 很少改 | `EditorScript` 一次转换，见 godot-resources-data |
| glTF 等 3D 场景导入后统一改节点 | `EditorScenePostImport` |

- 导入器用自定义后缀，游戏里 `load` 源文件路径得到资源

## 陷阱

| 现象 | 做法 |
|---|---|
| 打开场景就被 `@tool` 脚本改动并存盘 | 游戏逻辑先 `Engine.is_editor_hint()` 挡住 |
| 编辑器里 `add_child` 的节点看不到、不存盘 | `owner` 设为 `EditorInterface.get_edited_scene_root()` |
| 改场景实例的子节点，重载后丢失 | 先判断 `node.owner == EditorInterface.get_edited_scene_root()` |
| 导入器或 Inspector 插件里方法不可用 | 用到的 `class_name` 脚本加 `@tool` |
| 导入器抢走 `.json` `.txt` 文件 | 用自定义后缀 |
| 关闭再启用插件后面板和菜单重复 | `_exit_tree` 反注册 |
| 亮色主题下看不见 | 颜色取编辑器主题 |
| 导出后脚本解析失败，报找不到 `EditorInterface` | 编辑器代码拆到编辑器专用脚本，或 `Engine.get_singleton(&"EditorInterface")` |
| C# 导出构建报找不到编辑器类型 | 编辑器代码用 `#if TOOLS` 包住 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法，`[Tool]` 与热重载
- [references/export-annotations.md](references/export-annotations.md)：`@export_*` 注解一览，C# 特性对照
- [references/inspector-plugin.md](references/inspector-plugin.md)：`EditorInspectorPlugin` 与 `EditorProperty`
- [references/import-plugin.md](references/import-plugin.md)：`EditorImportPlugin` 与 `EditorScenePostImport`
- [references/editor-recipes.md](references/editor-recipes.md)：插件骨架、Dock、Autoload、主屏幕、主题、快捷键、菜单、文件变化、项目设置、EditorScript、撤销
- https://docs.godotengine.org/en/stable/tutorials/plugins/running_code_in_the_editor.html
- https://docs.godotengine.org/en/stable/tutorials/plugins/editor/index.html
