---
name: godot-2d
description: 写 Godot 4 的 2D 场景时用。CharacterBody2D 角色移动与平台跳跃、碰撞层、Area2D、TileMapLayer 瓦片地图与地形自动接边、Camera2D 跟随 平滑 limit 震屏、Parallax2D、y_sort 绘制顺序、像素风缩放、2D 光照、寻路、射线与物理查询、_draw 自绘。也用于查某个 2D 需求有没有内置节点。3D 里放 2D 角色见 godot-2d-in-3d。
---

# Godot 2D

2D 游戏常见需求的内置节点选择、最短写法和易错点。

## 范围

| 不含 | 去哪 |
|---|---|
| 动画播放、Tween | godot-animation |
| shader、粒子、命中闪白写法 | godot-shaders-vfx |
| UI 控件、HUD 布局 | godot-ui |
| 输入映射 | godot-input |
| 3D 场景里放 2D 角色 | godot-2d-in-3d |
| 大量实体的性能 | godot-performance |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 角色、敌人移动与碰撞 | `CharacterBody2D.move_and_slide` | 手写碰撞检测与滑动 |
| 单向平台 | `CollisionShape2D.one_way_collision` | 按 Y 坐标手动开关碰撞 |
| 推得动的箱子、球 | `RigidBody2D`，一次性冲击 `apply_central_impulse`，持续推力 `apply_central_force` | 每帧改 `position` 或 `linear_velocity` |
| 拾取、伤害区、触发区 | `Area2D` 加信号 | 手写矩形相交 |
| 脚下、身前持续探测 | `RayCast2D`、`ShapeCast2D` 节点 | 每帧 new 查询参数 |
| 一次性射线、点选、范围内有谁 | `direct_space_state` 的 `intersect_ray`、`intersect_point`、`intersect_shape` | 遍历全部物体手算相交 |
| 瓦片地图 | `TileMapLayer` 加 `TileSet` | `TileMap` 已弃用，每格一个节点 |
| 相机边界 | `Camera2D` 的 `limit_*` | 每帧手写夹取 |
| 相机平滑与死区 | `position_smoothing_enabled`、`drag_*_enabled` | 手写 SmoothDamp |
| 震屏 | `Camera2D.offset` 加 `FastNoiseLite` | 移动相机节点本身 |
| 视差背景 | `Parallax2D`（4.3+） | `ParallaxBackground` 与 `ParallaxLayer` 已弃用，手算偏移 |
| 是否在屏幕内 | `VisibleOnScreenNotifier2D` | 手写矩形与相机比较 |
| 离屏暂停逻辑 | `VisibleOnScreenEnabler2D` | 每帧距离判断 |
| 遮挡排序 | `y_sort_enabled`、`z_index` | 每帧改 z_index |
| 固定在屏幕上的层 | `CanvasLayer` | 手算相机反向偏移 |
| 光照与阴影 | `PointLight2D`、`DirectionalLight2D`、`LightOccluder2D`、`CanvasModulate` | 多个 SubViewport 拼光照 |
| 泛光 | `WorldEnvironment` 的 `Environment.glow_enabled` | SubViewport 手搓 bloom |
| 实时寻路 | `NavigationRegion2D` 加 `NavigationAgent2D` | 手写 A* 与路径跟随 |
| 格子寻路 | `AStarGrid2D` | 手写 A* |
| 线、轨迹、血条形状 | `Line2D`、`Polygon2D`、`_draw` | 一格一个 `ColorRect` |
| 大量相同物体 | `MultiMeshInstance2D` | 几千个 Sprite2D |
| 像素风 | 项目设置，见下 | 手写缩放与取整 |
| 命中闪白 | shader uniform 加 Tween | 把 Modulate 调到大于 1 |

## 做法

### CharacterBody2D

平台跳跃：

<!-- check: extends CharacterBody2D -->
```gdscript
const SPEED := 160.0
const JUMP := -320.0

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity += get_gravity() * delta
	elif Input.is_action_just_pressed("jump"):
		velocity.y = JUMP
	velocity.x = Input.get_axis("left", "right") * SPEED
	move_and_slide()
```

俯视角：

<!-- check: extends CharacterBody2D -->
```gdscript
func _physics_process(_delta: float) -> void:
	velocity = Input.get_vector("left", "right", "up", "down") * 120.0
	move_and_slide()
```

| 属性或方法 | 用途 |
|---|---|
| `motion_mode` | 俯视角设 `MOTION_MODE_FLOATING`，所有碰撞按墙处理 |
| `floor_snap_length` | 下坡不脱地 |
| `floor_constant_speed` | 上下坡速度一致 |
| `floor_stop_on_slope` | 站定不下滑 |
| `platform_on_leave` | 移动平台带动角色是内置的，此项管离开时的速度 |
| `get_slide_collision(i).get_collider()` | 本帧撞到什么，数量 `get_slide_collision_count()` |

- `velocity` 单位像素每秒，`move_and_slide` 不乘 delta，`move_and_collide` 要乘
- 默认 grounded 模式按 `up_direction` 区分地面墙天花板，斜坡加减速

### 单向平台与推动刚体

- 单向平台：平台的 `CollisionShape2D` 勾 `one_way_collision`
- 角色撞上 `RigidBody2D` 不推动它，每物理帧对它 `apply_central_force`
- 下穿、漏穿、推箱写法见 [references/bodies.md](references/bodies.md)

### 碰撞层

layer 是我在哪一层，mask 是我扫描哪些层。先在项目设置里给层起名，代码只用 1 到 32 的编号。

```ini
[layer_names]

2d_physics/layer_1="world"
2d_physics/layer_2="player"
2d_physics/layer_3="enemy"
2d_physics/layer_4="player_hitbox"
2d_physics/layer_5="enemy_hitbox"
```

| 对象 | layer | mask |
|---|---|---|
| 地形、墙 | world | 无 |
| 玩家 | player | world |
| 敌人 | enemy | world |
| 玩家攻击判定 Area2D | player_hitbox | enemy |
| 敌人攻击判定 Area2D | enemy_hitbox | player |
| 拾取物 Area2D | 无 | player |

- 检测方 Area2D 只设 mask，除非别的 Area2D 要检测它
- 改单个位：`set_collision_layer_value(2, true)`，编号从 1 起
- 函数参数里的位掩码是 `1 << (层号 - 1)`，全部层 `0xffffffff`
- 敌人互不挤：敌人的 mask 不放 enemy 层

### Area2D

<!-- check: extends Area2D -->
```gdscript
signal collected(by: Node2D)

@onready var _shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	body_entered.connect(_on_body_entered)


func _on_body_entered(body: Node2D) -> void:
	collected.emit(body)
	_shape.set_deferred("disabled", true)
```

- `monitoring` 是我检测别人，`monitorable` 是别人能检测我
- 信号回调里禁用形状、改 `monitoring` 用 `set_deferred`
- `get_overlapping_bodies` 每物理步更新一次，刚移动完查不到，优先用信号
- 撞 TileMapLayer 时 `body_entered` 的参数是 `TileMapLayer`，不是格子
- 回查格子见 [references/tilemaplayer.md](references/tilemaplayer.md)

### 射线与空间查询

| 需求 | 用这个 |
|---|---|
| 固定方向持续探测，脚下、身前 | `RayCast2D` 节点，每物理步自动更新 |
| 有宽度的探测，台阶、宽激光 | `ShapeCast2D` 节点 |
| 一次性射线，hitscan、视线 | `intersect_ray` |
| 点下去有谁 | `intersect_point` |
| 圆形或矩形范围内有谁 | `intersect_shape` |

```ini
[node name="GroundProbe" type="RayCast2D" parent="."]
target_position = Vector2(0, 12)
collision_mask = 1
```

<!-- check: extends CharacterBody2D -->
```gdscript
@onready var _ground: RayCast2D = $GroundProbe

func _physics_process(_delta: float) -> void:
	if _ground.is_colliding():
		var point: Vector2 = _ground.get_collision_point()
		print(point, _ground.get_collider())
```

<!-- check: extends CharacterBody2D -->
```gdscript
const MASK := (1 << 0) | (1 << 2)

func _physics_process(_delta: float) -> void:
	if not Input.is_action_just_pressed("fire"):
		return
	var query := PhysicsRayQueryParameters2D.create(
			global_position, get_global_mouse_position(), MASK, [get_rid()])
	var hit: Dictionary = get_world_2d().direct_space_state.intersect_ray(query)
	if not hit.is_empty():
		var point: Vector2 = hit.position
		print(point, hit.collider)
```

- `RayCast2D.target_position` 相对自己
- `exclude_parent` 默认 true，排除父级碰撞体
- 同一物理步改了位置要读结果，先 `force_raycast_update()`
- `enabled` 为 false 时 `force_raycast_update()` 仍有效
- 查询参数的 mask 默认全部层，节点的 `collision_mask` 默认只有第 1 层

- `intersect_ray` 返回字典，没命中为空
- `intersect_point` `intersect_shape` 返回字典数组，无 `position`
- ShapeCast2D、范围与点查询、结果字段见 [references/physics-queries.md](references/physics-queries.md)

### TileMapLayer

一层一个节点，多层靠多个节点，旧 `TileMap` 在编辑器里一键转换。

- 读写用 `set_cell`、`erase_cell`、`get_cell_tile_data`、`local_to_map`
- 地形接边用 `set_cells_terrain_connect`，不手写位掩码，挖掉时 terrain 传 -1
- `erase_cell` 不刷新邻格地形
- 碰撞、导航、遮挡、自定义数据、地形先在 TileSet 建层，再给瓦片填
- 宝箱、火把等带逻辑物件用 Scenes Collection 源，或直接放场景
- 预置格子用无头脚本 `set_cell` 加 `ResourceSaver.save` 生成
- 手编 `tile_map_data` 头 2 字节须为 0，否则整层读成 0 格
- 配置表、peering bit、运行时改瓦片、Y 排序见 [references/tilemaplayer.md](references/tilemaplayer.md)

### Camera2D

```ini
[node name="Camera2D" type="Camera2D" parent="Player"]
position_smoothing_enabled = true
position_smoothing_speed = 6.0
limit_left = 0
limit_top = 0
limit_right = 2560
limit_bottom = 720
```

- 相机做玩家子节点，跟随、边界、平滑、死区都内置
- `limit_*` 是整数像素
- 震屏改 `offset` 不改节点位置，噪声用 `FastNoiseLite`
- `offset` 在 limit 之后叠加，贴边会露出界外，要夹紧
- 复活、传送后同一段代码里紧接着调 `reset_smoothing()`
- 不在相机里比较位移距离猜传送，冲刺会误判
- 视差背景用 `Parallax2D` 4.3+，`scroll_scale` 小于 1 是远景
- 画面抖、`zoom`、完整震屏、算 limit、Parallax2D 摆法见 [references/camera-parallax.md](references/camera-parallax.md)

### 绘制顺序

| 工具 | 规则 |
|---|---|
| `y_sort_enabled` | 共同父节点开，子节点按原点 Y 排序，角色原点放脚底 |
| 子节点未开 y_sort | 整棵子树作为一个整体参与排序 |
| `z_index` | Y 排序只在同 `z_index` 间生效，默认相对父节点累加 |
| `z_as_relative` | 关掉后 `z_index` 是绝对值 |
| 同级不排序 | 场景树里靠后的画在上面 |
| `CanvasLayer` | 不随 Camera2D 移动缩放，`layer` 大的在上，负数在世界后 |

- HUD、暂停菜单、转场放 CanvasLayer，不靠 `z_index` 堆高
- 同一 `layer` 值的多个 CanvasLayer 前后顺序不确定
- 跟着世界走带深度感：`follow_viewport_enabled` 加 `follow_viewport_scale`

### 像素风

| 路线 | 设置 |
|---|---|
| 低分辨率整体放大 | `display/window/stretch/mode` 设 `viewport`，`display/window/stretch/scale_mode` 设 `integer` |
| 高分辨率加取整 | `canvas_items`，开 `rendering/2d/snap/snap_2d_transforms_to_pixel` |

- 两条路线都把 `rendering/textures/canvas_textures/default_texture_filter` 设 0 即 Nearest
- 4.7 新建项目默认 `canvas_items` 加 `expand`，要手动改
- `Sprite2D.centered` 默认 true，奇数尺寸贴图落在半像素上变形
- 完整设置、抖动排查、字体、光影分辨率见 [references/pixel-art.md](references/pixel-art.md)

### 光照、离屏、寻路、自绘

| 需求 | 要点 | 文件 |
|---|---|---|
| 2D 光照与阴影 | `CanvasModulate` 压暗，`PointLight2D` 必须有 `texture`，`LightOccluder2D` 投影 | [lighting-glow.md](references/lighting-glow.md) |
| 泛光与 HDR 2D | `rendering/viewport/hdr_2d` 加 `WorldEnvironment`，`modulate` 大于 1 发光 | [lighting-glow.md](references/lighting-glow.md) |
| 离屏销毁与暂停 | `VisibleOnScreenNotifier2D`，`VisibleOnScreenEnabler2D` | [navigation-culling.md](references/navigation-culling.md) |
| 寻路 | `NavigationRegion2D` 烘焙，`NavigationAgent2D` 每物理帧取 `get_next_path_position` | [navigation-culling.md](references/navigation-culling.md) |
| 线、多边形、网格线 | `Line2D`、`Polygon2D`、`_draw` 加 `queue_redraw` | [drawing.md](references/drawing.md) |

## 陷阱

| 现象 | 做法 |
|---|---|
| 信号回调里直接改碰撞形状 `disabled` 出错 | 用 `set_deferred` |
| `_process` 或 `_input` 里查 `direct_space_state` 结果滞后，物理单独线程时报 `Space state is inaccessible` | 查询放进 `_physics_process`，输入里只记标志 |
| `PhysicsRayQueryParameters2D` 命中发射者自己 | `exclude` 填 `[get_rid()]`，查询不会自动排除 |
| 射线与点查询打不到 `Area2D` | `collide_with_areas` 默认 false，手动开 |
| Area2D 检测不到 TileMapLayer 或 StaticBody2D | 对方 layer 放进 mask，TileSet 配碰撞形状 |
| 静止的 Area2D 检测不到后生成或瞬移进来的 StaticBody2D | 会动的固体用 `AnimatableBody2D` |
| `Camera2D.zoom` 放大后文字糊 | 文字放进 CanvasLayer，或开 MSDF |
| `viewport` 拉伸下精灵无亚像素位置和旋转 | 需要时改 `canvas_items` 加取整 |
| 2D 节点每帧手算透视缩放伪 3D | 改真 3D 加 `Sprite3D`，见 godot-2d-in-3d |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/camera-parallax.md](references/camera-parallax.md)：相机边界、平滑死区、完整震屏、Parallax2D 尺寸与摆法
- [references/bodies.md](references/bodies.md)：单向平台、下穿、推动刚体、改刚体状态
- [references/physics-queries.md](references/physics-queries.md)：ShapeCast2D、`intersect_shape`、`intersect_point`、结果字段
- [references/tilemaplayer.md](references/tilemaplayer.md)：TileSet 配置表、格子读写、地形、碰撞回查、运行时改瓦片、Y 排序
- [references/pixel-art.md](references/pixel-art.md)：两条像素风路线、抖动排查、导入与字体、光影分辨率
- [references/lighting-glow.md](references/lighting-glow.md)：2D 光照与阴影、HDR 2D 与 glow
- [references/navigation-culling.md](references/navigation-culling.md)：VisibleOnScreen 系列、NavigationAgent2D 最短用法
- [references/drawing.md](references/drawing.md)：Line2D、Polygon2D、`_draw` 的选择与写法
- https://docs.godotengine.org/en/stable/tutorials/physics/ray-casting.html
- https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html
- https://docs.godotengine.org/en/stable/tutorials/2d/2d_parallax.html
- https://docs.godotengine.org/en/stable/tutorials/2d/2d_lights_and_shadows.html
- https://docs.godotengine.org/en/stable/tutorials/2d/canvas_layers.html
- https://docs.godotengine.org/en/stable/tutorials/rendering/multiple_resolutions.html
- https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_introduction_2d.html
