---
name: godot-performance
description: 排查卡顿 掉帧 帧率低 内存增长时用，也用于几百个怪物 子弹同屏、CharacterBody 拥挤变慢、每帧重建网格、线程池只用上两三个核、C# 跨界开销。先测再改 Profiler Monitors。不降画面与数量的内置解法 管理器统一驱动、MultiMesh、Server、对象池、空间哈希、WorkerThreadPool 分块、网格局部更新、物理插值、线程加载、着色器编译卡顿、每帧分配。Godot performance, stutter, many entities.
---

# Godot 性能

定位瓶颈、选内置方案、再测确认。默认只做不降画面、数量与更新频率的优化。

## 范围

| 不含 | 去哪 |
|---|---|
| 着色器与特效写法 | godot-shaders-vfx |
| 3D 剔除、LOD、`visibility_range` | godot-3d |
| GDScript 语法与静态类型 | godot-gdscript |
| C# 分配、`StringName` 缓存、跨界开销 | godot-csharp |
| 加载进度条与资源缓存 | godot-resources-data |

## 先查内置

| 现象 | 用这个 | 别自己写 |
|---|---|---|
| 数千个相同物体 | `MultiMeshInstance2D` `MultiMeshInstance3D` 加 `MultiMesh` | 每个物体一个 Sprite 或 MeshInstance 节点 |
| 数千颗 2D 子弹 | `RenderingServer` canvas item 加 `PhysicsServer2D`，或 `MultiMesh` 加数组，至少对象池 | 每颗子弹一个 Area2D 加 Sprite2D |
| 屏幕外的敌人或装置仍在运行 | `VisibleOnScreenEnabler2D` `VisibleOnScreenEnabler3D` | 手写矩形相交判断 |
| 只用于事件响应的节点 | 删掉 `_process`，`set_process(false)` | 空 `_process` 留着 |
| 周期逻辑 | `Timer` 节点 | `_process` 里累加计时 |
| 移动抖动 | 物理插值 | `_process` 里手动推进物理体 |
| 大批量计算 | `WorkerThreadPool.add_group_task()` 按块分，传 `high_priority` | 自建 `Thread` 池 |
| 几百个同类实体各自回调 | 一个管理器循环处理全部，见 [many-entities.md](references/many-entities.md) | 每个实体一个 `_physics_process` |
| 大量 `CharacterBody3D` 挤在一起变慢 | 收紧碰撞掩码、胶囊形状、静止跳过，见 [crowd-characters.md](references/crowd-characters.md) | 降 tick 率、调小 `max_slides` |
| 每帧形状都变的网格 | 预分配加 `ArrayMesh.surface_update_vertex_region()` 加 `custom_aabb` | 每帧 `clear_surfaces()` 重建 |
| 逐点变换、多边形运算、拼字符串 | `Transform2D` 乘 `PackedVector2Array`、`Geometry2D`、`PackedStringArray` 的 `join` | 手写循环 |
| 进关卡或换场景卡顿 | `ResourceLoader.load_threaded_request()` 加轮询 | 玩法中途同步 `load()` |
| 特效第一次出现卡一下 | 预热场景，看 Pipeline 监视器 | 运行时第一次才实例化特效 |
| 频繁创建销毁同类节点 | 对象池 | 每次 `instantiate()` 再 `queue_free()` |
| 找固定目标 | 分组加缓存引用，或信号 | 每帧遍历全部对象做字符串比较 |
| 项目自己的指标 | `Performance.add_custom_monitor()` | `print` 刷屏 |

## 做法

### 不降效果

| 默认做 | 用户点名才做 |
|---|---|
| 合批调度、纯计算并行 | 隔帧更新、按距离降频 |
| 只更新变化的部分 | 屏幕外的东西停止运动 |
| 去掉重复查询 | 降 `physics_ticks_per_second` |
| 屏幕外停用看不见也不影响结果的东西 | 调小 `max_slides` 或物理迭代 |
| | 压缩顶点精度、关阴影、减数量 |

### 测量

确认是 CPU 还是 GPU，定位到函数或渲染阶段，改一处，再测。

| 工具 | 看什么 |
|---|---|
| Profiler | 脚本函数、物理、音频耗时，按 Self 排序 |
| Visual Profiler | 渲染各阶段 CPU 与 GPU 耗时，不含脚本与物理 |
| Monitors | FPS、节点数、孤儿节点、绘制调用、显存、Pipeline 编译数 |
| 手动计时 | `Time.get_ticks_usec()` 前后相减，跑 1000 次取平均 |

- 以上都在 Debugger 面板，Profiler 要手动点 Start
- Profiler 不支持 C# 脚本，C# 用手动计时或 IDE 工具
- 填充率判断：关 V-Sync，对比大窗口与小窗口 FPS
- 看毫秒帧时间，不看封顶的 FPS
- 以导出构建为准，编辑器里运行有额外开销

```gdscript
extends Node

var _bullets: int = 0

func _ready() -> void:
	Performance.add_custom_monitor("game/bullets", get_bullet_count)

func _exit_tree() -> void:
	Performance.remove_custom_monitor("game/bullets")

func get_bullet_count() -> int:
	return _bullets
```

- id 里一个斜杠分类，没有或多于一个归到 Custom
- 回调返回值不支持负数
- 同一 id 重复添加报错，场景重载前先 `remove_custom_monitor()`
- 第四个参数 `type` 4.6+，如 `Performance.MONITOR_TYPE_MEMORY` 传字节
- 游戏内读取：`Performance.get_custom_monitor()`，放在 `OS.is_debug_build()` 里

### 回调开关

```gdscript
extends Node2D

func _ready() -> void:
	set_process(false)
	set_physics_process(false)

func activate() -> void:
	set_physics_process(true)

func _physics_process(delta: float) -> void:
	position.x += 100.0 * delta
```

- 定义了 `_process` 或 `_physics_process` 的节点默认开启，`_ready()` 里按需关
- `hide()` 只停绘制，回调仍在跑
- 停整棵子树：`process_mode = Node.PROCESS_MODE_DISABLED`
- 整片区域不用时 `remove_child()` 摘出树，自己持有引用并负责 `free()`
- 互不依赖的节点可设 `process_thread_group` 为 `PROCESS_THREAD_GROUP_SUB_THREAD`
- 子线程组里不能访问组外节点，跨组用 `call_deferred_thread_group()`
- 物理查询与 `move_and_slide()` 只能在主线程

屏幕外自动停用：

```ini
[node name="Enemy" type="CharacterBody2D" parent="."]

[node name="Enabler" type="VisibleOnScreenEnabler2D" parent="Enemy"]
rect = Rect2(-64, -64, 128, 128)
```

| 属性 | 默认 | 作用 |
|---|---|---|
| `enable_node_path` | `..` | 被开关的节点 |
| `enable_mode` | `ENABLE_MODE_INHERIT` | 进屏幕时的处理模式，离开时设 DISABLED |

- 只要信号用 `VisibleOnScreenNotifier2D` 的 `screen_entered` 与 `screen_exited`
- 依赖渲染剔除，Enabler 自身不可见时不工作

### MultiMesh

```gdscript
extends MultiMeshInstance2D

func _ready() -> void:
	var quad := QuadMesh.new()
	quad.size = Vector2(8.0, 8.0)
	var mm := MultiMesh.new()
	mm.transform_format = MultiMesh.TRANSFORM_2D
	mm.use_colors = true
	mm.mesh = quad
	mm.instance_count = 2000
	mm.visible_instance_count = 0
	multimesh = mm

func show_count(count: int) -> void:
	multimesh.visible_instance_count = count
	for i in count:
		multimesh.set_instance_transform_2d(i, Transform2D(0.0, Vector2(i * 10.0, 0.0)))
		multimesh.set_instance_color(i, Color.WHITE)
```

- 先设 `transform_format` `use_colors` `use_custom_data`，最后设 `instance_count`
- 一次分配最大数量，`visible_instance_count` 控制显示数量
- 不按实例剔除，分散的实例按区域拆成多个 MultiMesh
- 设 `custom_aabb`，免得每次重算包围盒
- 每帧写上千个实例用 `buffer` 一次写入，布局见 [references/hotspots.md](references/hotspots.md)

### Server

场景树节点开销成为瓶颈时，绕过节点直接调 `RenderingServer` 与 `PhysicsServer2D`。

- 先试管理器加紧凑数组、MultiMesh 与对象池
- 服务器对象用 `RID` 引用，必须 `free_rid()`
- `PhysicsServer3D.body_test_motion()` 等物理查询只认主线程

### 物理 tick 与插值

```ini
[physics]

common/physics_ticks_per_second=30
common/physics_interpolation=true
```

| 设置 | 默认 | 说明 |
|---|---|---|
| `physics/common/physics_ticks_per_second` | 60 | 降低属于降效果，用户同意才改 |
| `physics/common/physics_interpolation` | false | 渲染在物理帧之间插值，2D 4.3+，3D 4.4+ |
| `physics/common/max_physics_steps_per_frame` | 8 | 单帧最多步数，tick 率高于 60 时调高 |

- 移动放 `_physics_process()`，Tween 与 AnimationPlayer 也设为物理处理
- 瞬移后先设变换，再 `reset_physics_interpolation()`
- 3D 相机读 `Node3D.get_global_transform_interpolated()` 4.4+
- 细节见 [references/stutter.md](references/stutter.md)

### 线程

```gdscript
extends Node

const CHUNK := 256
var _results: Array[float] = []
var _task_id: int = -1

func start(count: int) -> void:
	_results.resize(count)
	var chunks := ceili(count / float(CHUNK))
	_task_id = WorkerThreadPool.add_group_task(_compute_chunk, chunks, -1, true, "compute")

func _compute_chunk(chunk: int) -> void:
	for i in range(chunk * CHUNK, mini((chunk + 1) * CHUNK, _results.size())):
		_results[i] = sqrt(float(i))

func _process(_delta: float) -> void:
	if _task_id != -1 and WorkerThreadPool.is_group_task_completed(_task_id):
		WorkerThreadPool.wait_for_group_task_completion(_task_id)
		_task_id = -1
		print(_results[0])

func _exit_tree() -> void:
	if _task_id != -1:
		WorkerThreadPool.wait_for_group_task_completion(_task_id)
```

- `add_group_task()` 每个元素调一次，传块数，每块处理一段下标
- `high_priority` 默认 `false`，低优先级最多占 30% 线程
- 8 线程机器上低优先级只用 2 个，每帧要结果的传 `true`
- 每个任务都要 `wait_for_task_completion()` 或 `wait_for_group_task_completion()`
- 线程里不碰场景树，用 `call_deferred()` `set_deferred()`
- 不在树里的节点可在线程里组装，再 `add_child.call_deferred(node)`
- Array 与 Dictionary 可多线程读写元素，改大小要 `Mutex`
- `AStar2D` `AStar3D` `AStarGrid2D` 一个实例只给一个线程用

### 加载卡顿

```gdscript
extends Node

const LEVEL_PATH := "res://levels/level_1.tscn"
var _progress: Array = []

func _ready() -> void:
	set_process(false)

func start_load() -> void:
	ResourceLoader.load_threaded_request(LEVEL_PATH, "PackedScene", true)
	set_process(true)

func _process(_delta: float) -> void:
	var status := ResourceLoader.load_threaded_get_status(LEVEL_PATH, _progress)
	match status:
		ResourceLoader.THREAD_LOAD_IN_PROGRESS:
			print(_progress[0])
		ResourceLoader.THREAD_LOAD_LOADED:
			set_process(false)
			var scene := ResourceLoader.load_threaded_get(LEVEL_PATH) as PackedScene
			get_tree().change_scene_to_packed(scene)
		_:
			set_process(false)
			push_error("load failed")
```

- 请求后立刻 `load_threaded_get()` 会阻塞，等于同步加载
- 大场景 `instantiate()` 仍在主线程，拆成小场景分帧添加

### 着色器编译卡顿

Forward+ 与 Mobile 4.4+ 用 ubershader 与加载时预编译管线，Compatibility 没有。

- 看 `Performance.PIPELINE_COMPILATIONS_SURFACE` 等监视器，游戏中突增即编译卡顿
- 预热办法与 Shader Baker 见 [references/stutter.md](references/stutter.md)

### 每帧分配

- 缓冲放成员变量复用，`clear()` 后再填
- 数值没变不给 Label 赋值
- `get_tree().get_nodes_in_group()` 每次返回新数组，不每帧调
- N 乘 M 的线性扫描先建 Dictionary 索引
- 调试统计只在 `OS.is_debug_build()` 且面板可见时算

## 陷阱

| 现象 | 做法 |
|---|---|
| 优化前后数字差别是噪声 | 固定场景与窗口，多次取平均 |
| 小窗口 FPS 不变，误判非填充率 | 先关 V-Sync |
| 对象池隐藏的节点仍有碰撞和计时 | 摘出树，或关回调与碰撞 |
| `queue_free()` 后节点数没立刻下降 | 到帧末才释放 |
| `Performance.OBJECT_ORPHAN_NODE_COUNT` 持续增长 | `Node.print_orphan_nodes()` 列出未释放的节点 |
| 服务器 RID 泄漏 | 节点释放不带走 RID，`_exit_tree()` 里 `free_rid()` |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/profiling.md](references/profiling.md)：监视器清单、Profiler 用法、CPU 与 GPU 判断、命令行选项
- [references/many-entities.md](references/many-entities.md)：几百上千个同类实体，管理器统一驱动、紧凑数组、空间哈希、对象池上限
- [references/crowd-characters.md](references/crowd-characters.md)：大量 CharacterBody 拥挤，`move_and_slide()` 开销、不改行为的省法、避让
- [references/hotspots.md](references/hotspots.md)：Server 画子弹、对象池、MultiMesh 一次写入、查找缓存
- [references/render-submission.md](references/render-submission.md)：引擎已有的渲染缓存、动态网格局部更新、共用蒙皮、2D 断批、动画子线程组
- [references/engine-fast-paths.md](references/engine-fast-paths.md)：替代脚本循环的内置批量操作、GDScript 写法快慢
- [references/stutter.md](references/stutter.md)：物理插值细节、加载卡顿、着色器编译卡顿
- https://docs.godotengine.org/en/stable/tutorials/performance/general_optimization.html
- https://docs.godotengine.org/en/stable/tutorials/performance/cpu_optimization.html
- https://docs.godotengine.org/en/stable/tutorials/performance/gpu_optimization.html
- https://docs.godotengine.org/en/stable/tutorials/performance/using_servers.html
- https://docs.godotengine.org/en/stable/tutorials/performance/thread_safe_apis.html
