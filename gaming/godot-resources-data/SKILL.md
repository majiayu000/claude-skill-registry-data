---
name: godot-resources-data
description: 定义游戏数据表 配置 存档 资源加载时用。自定义 Resource class_name @export .tres 与 C# [GlobalClass]、JSON 与 Resource 怎么选、导入时把 JSON CSV 转成 Resource、资源共享与 duplicate local_to_scene、load preload 与线程加载进度条、user:// 存档、导出后读不到 res:// 目录。game data, custom resource, save game.
---

# Godot 资源与数据

游戏数据的定义、编辑、加载与存档。默认：数据做成自定义 `Resource` 存 `.tres`，存档用 JSON 写到 `user://`。

## 范围

| 不含 | 去哪 |
|---|---|
| 场景拆分、Autoload、节点通信 | godot-scene-architecture |
| `EditorImportPlugin`、编辑器插件 | godot-editor-tooling |
| shader 里采样曲线纹理 | godot-shaders-vfx |
| Animation 资源与 AnimationPlayer | godot-animation |
| C# 命名映射、源码生成器 | godot-csharp |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 武器 敌人 物品 技能数据表 | 自定义 `Resource` + `@export`，`.tres` | JSON 加手写解析，字符串键取字段 |
| 伤害成长 缓动 衰减曲线 | `Curve`，`sample(t)`；给 shader 用 `CurveTexture` | 自写关键帧曲线类 |
| 颜色渐变 | `Gradient`，`sample(t)`；给 shader 用 `GradientTexture1D` | 颜色数组加手写插值 |
| 路径 轨道 | `Curve2D` `Curve3D` | 点数组加手算切线 |
| 关键帧动画 | `Animation` + `AnimationPlayer` | 自写属性曲线播放器 |
| 缓存纹理 音频 场景 | `load()` 自带缓存 | `static var` 字典缓存 `Texture2D` |
| 大场景不卡顿加载 | `load_threaded_request` + 每帧 `load_threaded_get_status` | 请求后立刻循环 `load_threaded_get` |
| 枚举某类资源 | 数据库资源里的 `Array[Resource]`，或 `ResourceLoader.list_directory` 4.4+ | 运行时 `DirAccess` 扫 `res://` |
| 兼容外部工具的数据 | 导入期转成 `.tres` 或 `.res` | 运行时全量解析 JSON 再手建对象 |
| MB 级几何或查找表 | 导入期烘焙成 `.res` | 运行时解析 JSON 建 `ArrayMesh` |
| 存档 | JSON 到 `user://` | `ResourceSaver` 存自定义 `Resource` 再 `load` 回来 |
| 稳定的资源引用 | `@export` 拖拽，或 `uid://` | 手写 `res://` 字符串当主键 |

## 做法

### 自定义 Resource

数据类继承 `Resource`，字段用 `@export`，实例存成 `.tres`。

```gdscript
class_name ItemData
extends Resource

@export var id: StringName
@export var title: String
@export_multiline var description: String
@export var icon: Texture2D
@export var price: int = 10
@export var price_curve: Curve
@export var tags: Array[StringName] = []
```

- 文件系统面板右键 New Resource 选 `ItemData`，存 `.tres`
- 撤销重做、拖拽引用、复制粘贴都是原生的
- 资源可互相引用：`@export var drops: Array[ItemData]`
- `_init` 的参数必须都有默认值
- Inspector 新建与 `duplicate()` 都无参构造，有必填参数时返回空壳
- 资源只放静态配置，当前血量等运行时状态放节点或 `RefCounted`
- 不需要 Inspector 编辑的内存数据包用 `RefCounted` 子类

| 格式 | 用于 |
|---|---|
| `.tres` 文本 | 手改、版本控制 |
| `.res` 二进制 | 烘焙出的大数据 |

### 数据库资源

整张表由一个资源持有，运行时按 id 建索引。

```gdscript
class_name ItemDb
extends Resource

@export var items: Array[ItemData] = []

var _by_id: Dictionary[StringName, ItemData] = {}

func get_item(id: StringName) -> ItemData:
	if _by_id.is_empty():
		for item in items:
			_by_id[item.id] = item
	return _by_id.get(id)
```

- 增删条目在 Inspector 里做，不扫目录
- 元素为 `null` 时 Inspector 不报错，用到时判空

### JSON 与 Resource

| 场景 | 选择 |
|---|---|
| 只在游戏侧用的数据 | `Resource` |
| 表格工具维护，导出 JSON 或 CSV | 源文件保留，导入期转成 `Resource` |
| 玩家 mod 或下载内容，不能带脚本 | JSON，加载时校验字段 |
| 网络协议 | JSON 或二进制 |
| 存档 | JSON |
| 与其他引擎共用 | JSON |

| 导入期转换 | 适合 |
|---|---|
| `@tool` 的 `EditorScript` 一键转 `.tres`，结果提交 | 数据很少改 |
| `EditorImportPlugin`，改源文件自动重导 | 数据常改 |

- 表格与 Inspector 只能有一个源头
- 表格还在导出：JSON 为源，`.tres` 只生成不手改
- 改在 Inspector：`.tres` 为源，用工具脚本导出 JSON
- 类型错误在导入时暴露，运行时不再有解析代码

### 共享与复制

同一路径 `load` 多次得到同一对象，同一场景多次实例化共用其 sub_resource。

| 做法 | 行为 |
|---|---|
| `load(path)` 两次 | 同一实例 |
| `duplicate()` | 浅拷贝，嵌套 `Array` `Dictionary` `Resource` 共享 |
| `duplicate(true)` | 复制数组、字典和内嵌子资源，外部资源仍共享 |
| `duplicate_deep(mode)` 4.5+ | 按 `Resource.DeepDuplicateMode` 选复制范围 |
| `resource_local_to_scene = true` | 场景每次实例化各得一份，外部 `.tres` 也适用 |
| `ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE)` | 绕过缓存读新的一份 |

| `Resource.DeepDuplicateMode` | 子资源 |
|---|---|
| `DEEP_DUPLICATE_NONE` | 不复制 |
| `DEEP_DUPLICATE_INTERNAL` 默认 | 只复制内嵌的 |
| `DEEP_DUPLICATE_ALL` | 连外部资源也复制 |

```gdscript
class_name StatBlock
extends Resource

@export var hp: int = 10
@export var speed: float = 120.0
```

```gdscript
extends CharacterBody2D

@export var base_stats: StatBlock

var stats: StatBlock

func _ready() -> void:
	stats = base_stats.duplicate()
```

- 每个敌人独立血量：`_ready` 里 `duplicate()`，或勾 `resource_local_to_scene`
- 运行时要改子资源数组里的项：`duplicate(true)` 或 `duplicate_deep()`
- local_to_scene 只复制数组，数组里的子资源仍共享
- 子资源自己也勾 `resource_local_to_scene` 才各得一份
- 数据表资源当只读，改了所有引用方都变
- 复制时做初始化：重写 `Resource._setup_local_to_scene`

### 加载方式

| 做法 | 用于 |
|---|---|
| `preload("res://x.tscn")` | 常量路径，脚本加载时读入，小而必用 |
| `load(path)` | 变量路径或用到才读，同步，大资源卡帧 |
| `@export var scene: PackedScene` | 路径交给 Inspector，移动文件引用不断 |
| `ResourceLoader.load_threaded_request` | 大资源、加载界面 |
| `ResourceLoader.exists(path)` | 导出后判断资源在不在 |

- `load` 按路径缓存，没有引用时释放，不另建字典缓存

| `ResourceLoader.CacheMode` | 行为 |
|---|---|
| `CACHE_MODE_REUSE` 默认 | 有缓存用缓存，没有就读并存入 |
| `CACHE_MODE_IGNORE` | 不读不写缓存，得到独立副本，依赖仍走缓存 |
| `CACHE_MODE_REPLACE` | 重读并刷新已缓存的同一对象，用于热重载 |
| `CACHE_MODE_IGNORE_DEEP` `CACHE_MODE_REPLACE_DEEP` | 同上，递归到依赖 |

### 异步加载

请求后每帧查状态，加载完再取结果。

```gdscript
extends Control

signal finished(resource: Resource)

@export var bar: ProgressBar

var _path: String = ""
var _progress: Array = []

func _ready() -> void:
	set_process(false)

func start(path: String) -> void:
	_path = path
	ResourceLoader.load_threaded_request(path)
	set_process(true)

func _process(_delta: float) -> void:
	var status := ResourceLoader.load_threaded_get_status(_path, _progress)
	match status:
		ResourceLoader.THREAD_LOAD_IN_PROGRESS:
			bar.value = float(_progress[0]) * 100.0
		ResourceLoader.THREAD_LOAD_LOADED:
			set_process(false)
			finished.emit(ResourceLoader.load_threaded_get(_path))
		_:
			set_process(false)
			push_error("加载失败 " + _path)
```

- `load_threaded_get` 在未加载完时阻塞，只在 `THREAD_LOAD_LOADED` 后调
- 进度按依赖估算，单个大文件可能从 0 直接到 1
- `use_sub_threads = true` 更快，可能拖慢主线程
- 加载完的场景交给 `SceneTree.change_scene_to_packed`

### 导出后的 res://

导入资源在包里只剩 `.import` 与 `.godot/imported`，`.tres` `.tscn` 默认转二进制只剩 `.remap`。

| 需求 | 做法 |
|---|---|
| 列出某类资源 | 数据库资源清单 |
| 必须枚举目录 | `ResourceLoader.list_directory` 4.4+ |
| 读导出后的资源 | `ResourceLoader.load`，不用 `FileAccess.open` |
| `.txt` 等无导入器文件进包 | 导出预设 `include_filter` 写 `*.txt` |
| 运行时读数据 CSV | Import 面板改 Keep File，即 `importer="keep"` |
| 可写目录 | `user://`，展示绝对路径用 `OS.get_user_data_dir()` |

- `list_directory` 返回原文件名，子目录带 `/`，顺序不固定
- 导出前 `list_directory("res://")` 含 `.godot/`，要过滤
- `.json` 在 `export_filter="all_resources"` 时默认进包，4.7.2 实测
- `.csv` 默认导入成 `Translation`，原文件不进包

### uid 引用

编辑器给每个资源分配 `uid://`，引用方同时存 uid 与路径，编辑器内移动文件引用不断。

| 操作 | API |
|---|---|
| 路径取 uid | `ResourceLoader.get_resource_uid`，无 uid 返回 -1 |
| int 转文本 | `ResourceUID.id_to_text` |
| 路径与 uid 互转 4.5+ | `ResourceUID.path_to_uid` `ResourceUID.uid_to_path` |
| 生成新 uid | `ResourceUID.create_id` |

- `load("uid://...")` 与 `preload("uid://...")` 可用
- `@export_file` 存 uid，`@export_file_path` 4.5+ 存裸路径
- 脚本的 `.gd.uid` 文件 4.4+ 要提交版本库
- 编辑器外移动文件后，让编辑器重扫并重存引用方
- 不手写 uid，字符集只有 `a` 到 `y` 与 `0` 到 `8`
- uid 与目标不符时打印 `invalid UID` 并退回路径

### 存档

存档文件在玩家手里，按不可信输入处理。

| 格式 | 适合 | 注意 |
|---|---|---|
| JSON | 存档、跨版本、可读 | 数字读回是 `float`，类型用 `JSON.from_native` `JSON.to_native` 4.4+ |
| `ConfigFile` | 设置、简单键值 | 会实例化文本里的 `Object(...)` |
| `FileAccess.store_var` | 紧凑二进制 | `get_var` 的 `allow_objects` 保持 `false` |
| `ResourceSaver.save` | 编辑器工具、开发期烘焙 | 不用于玩家存档 |

- 不 `load()` 玩家可写位置的 `.tres` `.res` `.tscn`
- 内嵌 `GDScript` 子资源的 `.tres`，`load` 时执行 `_init`，实测

## 陷阱

| 现象 | 做法 |
|---|---|
| 改 `AudioStreamOggVorbis.loop` 后所有 `load` 都循环 | 在导入设置里改，或 `duplicate()` 后再改 |
| 一个实例改 `material.albedo_color`，同场景全变 | 勾 `resource_local_to_scene` 或 `_ready` 里 `duplicate()` |
| `duplicate()` 后改数组元素，原件跟着变 | `duplicate(true)` 或 `duplicate_deep()` 4.5+ |
| 字典缓存的 `Texture2D` 永不释放 | 删掉缓存，`load` 已缓存 |
| `load_threaded_request` 后立刻 `load_threaded_get` 卡主线程 | 每帧查 `load_threaded_get_status` |
| 改类名或移动脚本后旧 `.tres` 失效 | 在编辑器里改名，保留 `.uid` |
| 编辑器里 `DirAccess` 扫 `res://` 正常，导出后漏项 | 清单资源或 `ResourceLoader.list_directory` |
| 导出后读不到 `res://` 下的 CSV | 导入方式改 `importer="keep"` |
| `str_to_var` 实例化了文本里的对象 | 不可信文本用 `JSON` |
| 有必填参数的 `_init`，`duplicate()` 报 `Error constructing a GDScriptInstance` | 参数都给默认值 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法，`[GlobalClass]` 资源
- [references/builtin-data-resources.md](references/builtin-data-resources.md)：`Curve` `Gradient` `CurveTexture` `Curve2D` `Animation` 的取值与替换对照
- [references/saving-data.md](references/saving-data.md)：存档位置、格式比较、版本迁移、原子写入、加密
- [references/baking-data.md](references/baking-data.md)：JSON 转 `.tres`，大数据烘焙成 `.res`
- https://docs.godotengine.org/en/stable/tutorials/scripting/resources.html
- https://docs.godotengine.org/en/stable/tutorials/io/background_loading.html
- https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html
