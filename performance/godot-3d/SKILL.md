---
name: godot-3d
description: 搭建或调试 Godot 4 的 3D 场景时用。CharacterBody3D 角色移动、第一 第三人称相机 SpringArm3D、Jolt 物理与碰撞层、RayCast3D 查询、渲染器与光照 GI 选型 SDFGI VoxelGI LightmapGI、阴影、glTF 导入、GridMap、CSG、LOD 与遮挡剔除、MultiMesh、NavigationAgent3D、骨骼修改器 IK。3D scenes, character controllers, lighting, level import.
---

# Godot 3D

3D 场景用哪个节点、哪个资源、哪个项目设置，以及照直觉会写错的地方。

## 范围

| 不含 | 去哪 |
|---|---|
| 着色器、粒子、后处理 | godot-shaders-vfx |
| 动画状态机、AnimationTree | godot-animation |
| 2D 精灵放进 3D | godot-2d-in-3d |
| 帧率剖析、大量实体 | godot-performance |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 角色走跑跳 | `CharacterBody3D` + `move_and_slide()` | 手算坡度和地面检测 |
| 推得动的箱子、球 | `RigidBody3D`，一次性冲击 `apply_central_impulse`，持续推力 `apply_central_force` | 每帧改 `global_position` 或 `linear_velocity` |
| 第三人称相机不穿墙 | `SpringArm3D` | 每帧射线加手动拉近 |
| 点选 狙击 视线 | `PhysicsRayQueryParameters3D` + `intersect_ray()` | 遍历所有物体算相交 |
| 前方探测 持续检测 | `RayCast3D` `ShapeCast3D` | 每帧 new 查询参数 |
| 敌人寻路与避让 | `NavigationRegion3D` + `NavigationAgent3D` | 手写 A* 和路点 |
| 大量相同网格 草 石头 | `MultiMeshInstance3D` | 几千个 `MeshInstance3D` |
| 远处降面 | 导入时自动 mesh LOD | 脚本按距离换网格 |
| 远处整组替换 淡出标签 | `GeometryInstance3D.visibility_range_end` | 脚本逐帧算距离 |
| 室内遮挡 | `OccluderInstance3D` | 手动隐藏房间 |
| 弹孔 污渍 假阴影 | `Decal` | 运行时拼贴图网格 |
| 灰盒关卡 | CSG 节点 后转 `MeshInstance3D` | 把 CSG 带进发布版 |
| 网格拼装关卡 | `GridMap` + `MeshLibrary` | 脚本循环摆几百个实例 |
| 头部看向 尾巴发丝摆动 腿部 IK | 骨骼修改器 见下文版本表 | 每帧手改 `Skeleton3D` 骨骼姿态 |
| 天空 雾 泛光 色调映射 | `WorldEnvironment` + `Environment` | 多个 `SubViewport` 堆后处理 |
| 曝光 景深 | `CameraAttributesPractical` | 脚本改亮度 |
| 间接光 | SDFGI VoxelGI LightmapGI | 到处摆补光灯 |
| 导入后加碰撞 | 名字后缀 `-col` 或高级导入设置 | 导入后脚本遍历加 `CollisionShape3D` |
| 高刷新率下相机抖动 | `physics/common/physics_interpolation` | 自己在 `_process` 里插值 |

## 做法

### 角色移动

```gdscript
extends CharacterBody3D

@export var speed: float = 5.0
@export var jump_velocity: float = 4.5

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity += get_gravity() * delta
	elif Input.is_action_just_pressed("jump"):
		velocity.y = jump_velocity

	var input: Vector2 = Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	var direction: Vector3 = global_basis * Vector3(input.x, 0.0, input.y)
	velocity.x = direction.x * speed
	velocity.z = direction.z * speed
	move_and_slide()
```

- `velocity` 是每秒速度，不乘 `delta`
- `get_vector` 长度已限制为 1，不再 `normalized()`，摇杆轻推保持慢速
- `is_on_floor()` 读的是上一次 `move_and_slide()` 的结果
- 相机相对移动时用相机的 yaw 基底代替 `global_basis`
- 没有内置台阶，用斜面碰撞体，或 `ShapeCast3D` 自己检测
- 重力方向不是 Y 时改 `up_direction`

- 坡度、贴地、撞墙等属性默认值见 [references/physics-3d.md](references/physics-3d.md)

### 物理引擎

| 引擎 | 状态 |
|---|---|
| Jolt Physics | 4.4+ 内置，4.6 起新建项目默认，通常更快更稳 |
| GodotPhysics3D | 设置值 `DEFAULT` 在 4.7 仍等于它，老项目升级后保持 |

```ini
[physics]

3d/physics_engine="Jolt Physics"
```

- 4.5 及更早升级的项目手动改，改完重启编辑器
- Jolt 与 GodotPhysics3D 的差异见 [references/physics-3d.md](references/physics-3d.md)

### 碰撞层

先列碰撞对再分层，在 `layer_names/3d_physics/layer_1` 到 `layer_32` 里起名。

| 层 | 内容 | 它的 mask 勾选 |
|---|---|---|
| 1 world | 静态关卡 | 无 |
| 2 player | 玩家身体 | 1 3 |
| 3 enemy | 敌人身体 | 1 2 3 |
| 4 player_hit | 玩家子弹与近战判定 `Area3D` | 3 |
| 5 enemy_hit | 敌人攻击判定 `Area3D` | 2 |
| 6 pickup | 拾取物 `Area3D` | 无 玩家的 `Area3D` 勾 6 |
| 7 camera_block | 只给 `SpringArm3D` 用的墙体 | 无 |

```gdscript
extends CharacterBody3D

const LAYER_WORLD: int = 1 << 0
const LAYER_PLAYER: int = 1 << 1
const LAYER_ENEMY: int = 1 << 2

@export_flags_3d_physics var hit_mask: int = LAYER_ENEMY

func _ready() -> void:
	collision_layer = LAYER_PLAYER
	collision_mask = LAYER_WORLD | LAYER_ENEMY
```

- `collision_layer` 是我在哪层，`collision_mask` 是我扫描哪层
- 位掩码第 n 层是 `1 << (n - 1)`，单层开关 `set_collision_mask_value(n, true)`
- `Area3D` 检测不到谁，先查对方 layer 是否在自己的 mask 里

### 空间查询

| 需求 | 用这个 |
|---|---|
| 固定方向持续探测 地面 前方墙 | `RayCast3D` 节点 每物理帧自动更新 |
| 同一物理帧改参数后立刻读 | `RayCast3D.force_raycast_update()` |
| 点选 hitscan 一次性射线 | `intersect_ray()` |
| 有厚度的探测 扫过一个形状 | `ShapeCast3D` 或 `cast_motion()` |
| 某位置的范围内有谁 | `intersect_shape()` |
| 两个形状是否相交与接触点 | `collide_shape()` 与 `get_rest_info()` |

```gdscript
extends Camera3D

const RAY_LENGTH: float = 1000.0

func pick(mouse_position: Vector2) -> Dictionary:
	var space: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
	var from: Vector3 = project_ray_origin(mouse_position)
	var to: Vector3 = from + project_ray_normal(mouse_position) * RAY_LENGTH
	var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(from, to, 1 << 2)
	query.collide_with_areas = true
	return space.intersect_ray(query)
```

- 结果是字典，没命中为空，有 `position` `normal` `collider` `rid` `shape`
- `direct_space_state` 只在 `_physics_process()` 里访问，`_input()` 里只记鼠标位置

### 第三人称相机

节点结构：`Node3D` 枢轴，下面 `SpringArm3D`，下面 `Camera3D`。

```gdscript
extends Node3D

@export var mouse_sensitivity: float = 0.003

@onready var _arm: SpringArm3D = $SpringArm3D

func _ready() -> void:
	var body: CollisionObject3D = get_parent() as CollisionObject3D
	if body != null:
		_arm.add_excluded_object(body.get_rid())

func _unhandled_input(event: InputEvent) -> void:
	var motion: InputEventMouseMotion = event as InputEventMouseMotion
	if motion == null or Input.mouse_mode != Input.MOUSE_MODE_CAPTURED:
		return
	rotate_y(-motion.screen_relative.x * mouse_sensitivity)
	_arm.rotation.x = clampf(_arm.rotation.x - motion.screen_relative.y * mouse_sensitivity, -1.2, 1.2)
```

- `shape` 留空且相机是直接子节点时，用相机近平面做形状
- `collision_mask` 默认第 1 层，玩家层在内又没排除时被自己顶短
- 第一人称不用弹簧臂，yaw 转身体，pitch 转相机所在的头节点

### 渲染器

| 选这个 | 条件 |
|---|---|
| Forward+ | 桌面 3D 要 SDFGI VoxelGI SSR SSIL 体积雾 |
| Mobile | 手机 一体机 XR 要 `CompositorEffect` 要光照投影 |
| Compatibility | 网页 老硬件 简单 3D 与 2D |

- 导出到网页只能用 Compatibility，切换后场景和环境要重调
- 能力差异表见 [references/rendering-lighting.md](references/rendering-lighting.md)

### 光照与 GI

| 技术 | 渲染器 | 实时性 | 动态物体 | 工作量 |
|---|---|---|---|---|
| 无 GI 加环境光 | 全部 | 是 | 是 | 无 |
| `ReflectionProbe` | 全部 | 更新模式 Once 或 Always | 接收 | 手摆 |
| `LightmapGI` | 全部渲染 烘焙需 RenderingDevice | 否 | 靠 `LightmapProbe` | UV2 加烘焙 |
| `VoxelGI` | 仅 Forward+ | 是 动态物体可发光 | 是 | 摆节点加烘焙 几秒 |
| SDFGI | 仅 Forward+ | 半实时 | 只接收 | 环境里开关 |
| SSIL | 仅 Forward+ | 是 | 是 | 环境里开关 只当补充 |

- 桌面项目先开 SDFGI，不够再换
- 手机只能 `LightmapGI` 加 `ReflectionProbe`
- 由快到慢：`ReflectionProbe`、`LightmapGI`、`VoxelGI`、SSIL、SDFGI

- 小型动态物体 `gi_mode` 设 Disabled，大型设 Dynamic，只对 VoxelGI 有效
- `gi_mode`、灯的烘焙模式见 [references/rendering-lighting.md](references/rendering-lighting.md)

### 环境与相机属性

- `WorldEnvironment` 每个场景树只放一个，`Camera3D.environment` 优先
- `Environment.tonemap_mode` 默认 Linear，亮部截断，换 Filmic、ACES 或 AgX 4.4+
- `Camera3D.attributes` 优先于 `WorldEnvironment` 上的 `CameraAttributes`
- `CameraAttributesPhysical` 覆盖相机 `fov` `near` `far`，拿不准用 `CameraAttributesPractical`
- `tonemap_white` 取值、泛光阈值见 [references/rendering-lighting.md](references/rendering-lighting.md)

### 场景导入与关卡

- 格式优先 glTF 2.0，`.glb` 单文件；OBJ 没有骨骼、动画、PBR、UV2
- Blender 对象名后缀决定导入结果，如 `-col` `-colonly` `-rigid` `-navmesh`
- 动画名以 `loop` 或 `cycle` 开头或结尾自动循环
- 改材质先 Extract Materials，加节点用继承场景
- 网格拼装用 `GridMap` 加 `MeshLibrary`，CSG 只做灰盒
- 后缀全表、MeshLibrary、CSG、运行时加载 glTF 见 [references/import-and-levels.md](references/import-and-levels.md)

### 剔除与 LOD

- 远处降面：导入的 glTF 默认生成 mesh LOD
- 手做多级模型：`visibility_range_begin` `visibility_range_end`
- 室内遮挡：开 `rendering/occlusion_culling/use_occlusion_culling`，加 `OccluderInstance3D` 烘焙
- 完整做法与 `MultiMesh` 见 [references/culling-and-instancing.md](references/culling-and-instancing.md)

### 导航

```gdscript
extends CharacterBody3D

@export var speed: float = 4.0

@onready var _agent: NavigationAgent3D = $NavigationAgent3D

func go_to(target: Vector3) -> void:
	_agent.target_position = target

func _physics_process(_delta: float) -> void:
	if NavigationServer3D.map_get_iteration_id(_agent.get_navigation_map()) == 0:
		return
	if _agent.is_navigation_finished():
		return
	var next: Vector3 = _agent.get_next_path_position()
	velocity = global_position.direction_to(next) * speed
	move_and_slide()
```

- 场景放 `NavigationRegion3D` 加 `NavigationMesh`，下面放参与烘焙的网格，点 Bake
- `NavigationMesh.cell_size` 与 `navigation/3d/default_cell_size` 一致
- 运行时烘焙用 `bake_navigation_mesh(true)`
- 地图后台同步，进场头几帧 `map_get_iteration_id()` 为 0，先判断
- `get_next_path_position()` 每物理帧调一次，到达后不再调
- 避让：开 `avoidance_enabled`，连 `velocity_computed`，给 `velocity` 赋值，且设过 `target_position`

### 骨骼修改器

作为 `Skeleton3D` 的子节点，在动画之后运行。`influence` 做淡入淡出，`active` 开关。

| 需求 | 节点 |
|---|---|
| 头、炮塔看向目标 | `LookAtModifier3D` 4.4+ |
| 头发、布料、尾巴 | `SpringBoneSimulator3D` 4.4+ |
| 手臂、腿两段 IK | `TwoBoneIK3D` 4.6+ |

- `SkeletonIK3D` 已弃用
- 全部修改器与版本见 [references/skeleton-modifiers.md](references/skeleton-modifiers.md)

## 陷阱

| 现象 | 做法 |
|---|---|
| `RayCast3D` 打不到其他层 | 节点 `collision_mask` 默认只有第 1 层，查询参数默认全部层 |
| 射线打不到 `Area3D` | 设 `collide_with_areas` |
| 射线从碰撞体内部出发不命中该体 | 设 `hit_from_inside` |
| 查询命中自己 | `PhysicsRayQueryParameters3D` 自己填 `exclude`，只有 `RayCast3D` 有 `exclude_parent` |
| 物理变慢或不稳 | 不平移旋转缩放 `CollisionShape3D`，改形状尺寸 |
| 角色或刚体的三角网碰撞不工作 | `ConcavePolygonShape3D` 只用于静态体，改基本形状或凸包 |
| 碰撞形状不生效 | `PhysicsBody3D` 只认直接子级的 `CollisionShape3D` |
| `CharacterBody3D` 推不动 `RigidBody3D` | `move_and_slide()` 后对碰到的刚体 `apply_central_force`，方向取法线反向 |
| 角色在斜坡抖动或飞出 | 先看 `floor_snap_length`，再看是否在 `_process` 里移动 |
| 开物理插值后瞬移出现拖影 | 瞬移后调 `reset_physics_interpolation()` |
| 阴影、GI、glow 显示不对 | 见 [references/rendering-lighting.md](references/rendering-lighting.md) 的阴影参数与环境 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/physics-3d.md](references/physics-3d.md)：Jolt 差异、范围查询、ShapeCast3D
- [references/rendering-lighting.md](references/rendering-lighting.md)：渲染器差异、灯、阴影、GI 烘焙
- [references/import-and-levels.md](references/import-and-levels.md)：导入、后缀全表、GridMap、CSG、继承场景
- [references/culling-and-instancing.md](references/culling-and-instancing.md)：LOD、遮挡、MultiMesh、Decal
- [references/skeleton-modifiers.md](references/skeleton-modifiers.md)：骨骼修改器与版本
- https://docs.godotengine.org/en/stable/tutorials/3d/index.html
- https://docs.godotengine.org/en/stable/tutorials/physics/using_jolt_physics.html
- https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html
