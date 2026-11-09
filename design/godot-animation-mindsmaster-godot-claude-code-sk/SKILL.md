---
name: godot-animation
description: 写动画 缓动 角色状态动画 UI 动效 转场 精灵帧动画时用。AnimationPlayer 与 RESET 轨道、AnimationTree 状态机 BlendSpace、Tween create_tween 链式与 parallel、AnimatedSprite2D SpriteFrames、Tween 驱动 shader 参数、Curve 代替手写插值。animation tween state machine sprite frames.
---

# Godot 动画

动画节点选型：用引擎的 Animation 资源和 Tween，不手写插值器和曲线播放器。

## 范围

| 不含 | 去哪 |
|---|---|
| shader 写法、3D 网格闪白 | godot-shaders-vfx |
| 血条等 UI 控件结构 | godot-ui |
| 3D 骨骼修改器、IK | godot-3d |
| 帧动画用于 3D 场景里的 2D 角色 | godot-2d-in-3d |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 一次性动效 弹出 淡入 转场 | Tween | `_process` 里累计时间再 lerp |
| 多属性多轨道编排 关键帧编辑 | AnimationPlayer 加 Animation 资源 | 手写关键帧数组与播放器 |
| 动画里触发代码 音效 特效 | Animation 的方法调用轨道、音频轨道 | `_process` 里按时间判断 |
| 角色状态切换 混合 | AnimationTree 的 StateMachine BlendSpace2D | 一堆 bool 加 `if` 切 `play()` |
| 攻击叠加在移动上 | AnimationNodeOneShot 加骨骼过滤 | 手动停止与恢复 |
| 逐帧精灵动画 | AnimatedSprite2D 加 SpriteFrames，或 Sprite2D 的 `frame` 轨道 | 自己按 FPS 换贴图 |
| 缓动曲线 | `Tween.TRANS_*` 与 `Tween.EASE_*`、Curve、bezier 轨道 | 手写 smoothstep 与弹性函数 |
| 任意起止值的插值 | `Tween.interpolate_value`、`lerp`、`Curve.sample` | 自制 Lerp 工具类 |
| 数字滚动 血量残影 | `tween_method` | 每帧手动逼近 |
| 命中闪白 受击染色 | shader 的 `instance uniform` 加 Tween | `modulate` 超过 1 的取巧值 |
| 镜头运动 | Camera2D 内置平滑与 FastNoiseLite 抖动 | 手写 SmoothDamp |
| 2D 骨骼 | Skeleton2D Bone2D Polygon2D | 手写层级变换 |

## 做法

### 选型

| 场景 | 选 |
|---|---|
| 终点运行时才知道 | Tween |
| 简单短动效，UI 弹出、受击抖动 | Tween |
| 美术要在编辑器里调关键帧 | AnimationPlayer |
| 同时驱动多个节点、音频、方法调用 | AnimationPlayer |
| 按帧 seek 回放 | AnimationPlayer，见确定性回放 |
| 状态多、要混合 | AnimationPlayer 加 AnimationTree |
| 溶解、描边、闪白 | shader uniform，由 Tween 或 AnimationPlayer 驱动 |
| 纯逐帧像素动画 | AnimatedSprite2D |

### AnimationPlayer

```gdscript
extends CharacterBody2D

@onready var _anim: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
	_anim.animation_finished.connect(_on_animation_finished)
	_anim.play(&"attack")

func _on_animation_finished(anim_name: StringName) -> void:
	if anim_name == &"attack":
		_anim.play(&"idle")
```

| 轨道 | 用途 |
|---|---|
| 属性 `Animation.TYPE_VALUE` | 任意属性，如 `CollisionShape2D:disabled`、`Area2D:monitoring` 开关命中盒 |
| 方法调用 `TYPE_METHOD` | 判定帧、脚步声、生成特效 |
| 音频 `TYPE_AUDIO` | 驱动 AudioStreamPlayer，复音上限 `audio_max_polyphony` |
| 贝塞尔 `TYPE_BEZIER` | 曲线值 |
| 动画播放 `TYPE_ANIMATION` | 播放其他 AnimationPlayer 的动画 |
| 3D 位置旋转缩放、混合形状 | 骨骼与网格变形 |

- 动画存在 AnimationLibrary 里，一个播放器可挂多个库
- 默认库名为空，直接写动画名；命名库写 `play(&"enemy/attack")`
- 对正在播的同名动画再 `play()` 不重头，要重播先 `stop()` 或 `seek(0.0, true)`
- `play()` 下一次处理才生效，同帧要看到用 `advance(0)`
- `animation_finished` 对循环动画不发
- 循环由 Animation 的 `loop_mode` 在编辑器里设，运行时不改共享资源
- 淡入淡出用 `playback_default_blend_time` 或 `set_blend_time()`
- 播一段用 `play_section()` 或 `play_section_with_markers()` 4.4+，改区间用 `set_section()`
- 运行时建 Animation 只用于程序生成，常规动画在编辑器里做

### RESET

名为 `RESET` 的动画，区分大小写，保存默认姿态，每条轨道只有 0 秒一个关键帧，不用来播放。点关键帧图标时编辑器会提示创建。

| 开关 | RESET 的作用 |
|---|---|
| `reset_on_save` 为 true | 场景以 RESET 姿态存盘，不把动画中间状态存进 `.tscn` |
| `deterministic` 为 true | 混合中缺轨道的动画以 RESET 值作初始值，没有 RESET 按 0，位置被拉向原点 |
| `deterministic` 为 false，默认 | 缺轨道的动画不参与该属性的混合 |


### 处理模式

`AnimationMixer` 上，AnimationPlayer 和 AnimationTree 共用：

| 属性 | 值 | 用途 |
|---|---|---|
| `callback_mode_process` | `ANIMATION_CALLBACK_MODE_PROCESS_IDLE` 默认 | 普通视觉动画 |
| | `ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS` | 驱动物理体、命中盒、平台 |
| | `ANIMATION_CALLBACK_MODE_PROCESS_MANUAL` | 自己调 `advance(delta)`，确定性回放 |
| `callback_mode_method` | `ANIMATION_CALLBACK_MODE_METHOD_DEFERRED` 默认 | 方法调用延到处理后，安全删节点 |
| | `ANIMATION_CALLBACK_MODE_METHOD_IMMEDIATE` | 到点立即调用 |

- `AnimationPlayer.set_process_callback` 与 `set_method_call_mode` 已弃用

### AnimationTree

设 `anim_player`，建 `tree_root`，`active = true`。之后播放器不再自己 `play()`。

| 节点 | 用途 |
|---|---|
| AnimationNodeStateMachine | 状态与转场，脚本 `travel()` |
| AnimationNodeBlendSpace1D 2D | 按速度或方向混合 idle walk run |
| AnimationNodeOneShot | 叠加一次性动作 |
| AnimationNodeTransition | 简化版状态切换，`transition_request` |
| AnimationNodeBlend2 | 两路按比例混合 |
| AnimationNodeTimeScale TimeSeek | 变速与跳转 |

```gdscript
extends CharacterBody2D

@onready var _tree: AnimationTree = $AnimationTree
@onready var _state: AnimationNodeStateMachinePlayback = _tree["parameters/Locomotion/playback"]

func _physics_process(_delta: float) -> void:
	_tree["parameters/Locomotion/Move/blend_position"] = velocity / 200.0
	if Input.is_action_just_pressed(&"attack"):
		_tree["parameters/Attack/request"] = AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE
	if is_on_floor():
		_state.travel(&"Ground")
```

- 参数路径格式 `parameters/<节点名>/<参数>`，Inspector 的 Parameters 里悬停可见
- 上例 `tree_root` 是 BlendTree，含状态机 Locomotion 和 OneShot 节点 Attack
- Move 是 Locomotion 里的 BlendSpace2D 状态
- OneShot 放进 BlendTree，连 `in` 与 `shot` 两个输入
- 状态机直接做 `tree_root` 时路径是 `parameters/playback`
- Advance Mode 为 Auto 时才按条件自动走转场
- Advance Condition 只判断变量为 true，不能取反
- 取反和比较用 Advance Expression，区分大小写
- 表达式的变量来源由 `advance_expression_base_node` 指定
- `travel()` 沿转场图寻路，无路径直接跳
- 状态机须已运行：连了 Start，或先调 `start()`
- 转场 Priority 数值小的优先
- 动画节点是共享资源，参数按 AnimationTree 实例分开
- 运行时只改参数，不改节点资源
- 参数路径、状态机操作、OneShot、BlendSpace 见 [references/animation-tree.md](references/animation-tree.md)

### Tween

```gdscript
extends Control

var _tween: Tween

func pop() -> void:
	if _tween:
		_tween.kill()
	pivot_offset = size / 2.0
	_tween = create_tween()
	_tween.tween_property(self, "scale", Vector2.ONE * 1.2, 0.08).set_trans(Tween.TRANS_BACK).set_ease(Tween.EASE_OUT)
	_tween.tween_property(self, "scale", Vector2.ONE, 0.12)
```

| 规则 | 说明 |
|---|---|
| 创建 | `create_tween()` 绑定节点，出树暂停，释放时 kill |
| 不绑定 | `get_tree().create_tween()` 不随节点停，要自己 `kill()` |
| 复用 | 不复用，每次新建，构造函数 new 出的无效 |
| 同一属性 | 只留一个 Tween，后建的覆盖先建的，重播前 `kill()` |
| 默认顺序执行 | `set_parallel(true)` 全部并行，`parallel()` 单步并行，`chain()` 回到顺序 |
| 起点终点 | `.from(v)`、`.from_current()`、`.as_relative()` |
| 无限循环 | `set_loops()` 不带参数，每圈须有非零时长，否则被截断 |
| 暂停 | 默认 `Tween.TWEEN_PAUSE_BOUND` 跟随节点 `process_mode`，暂停菜单里 `set_pause_mode(Tween.TWEEN_PAUSE_PROCESS)` |
| 慢动作里照常走 | `set_ignore_time_scale(true)` |
| 物理节点位置 | `set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)` |

- `tween_method(callable, from, to, duration)` 驱动 setter、数字滚动、shader 参数
- `tween_callback()` 调函数，`tween_interval()` 延时
- 单独当计时器：`await create_tween().tween_interval(2.0).finished`
- `tween_subtween()` 4.4+ 把另一个 Tween 当一步嵌入
- `tween_await()` 4.7+ 等信号再走下一步，配 `set_timeout()` 兜底：

```gdscript
extends Node2D

signal dialogue_closed

func cutscene() -> void:
	var tween := create_tween()
	tween.tween_property(self, "position:x", 600.0, 1.5)
	tween.tween_callback(print.bind("Hello"))
	tween.tween_await(dialogue_closed).set_timeout(30.0)
	tween.tween_property(self, "position:x", 0.0, 1.5)
```

- 打断重播、飘字、数字滚动、转场、手动推进见 [references/tween-recipes.md](references/tween-recipes.md)

### AnimatedSprite2D 与 AnimatedSprite3D

- 帧在 SpriteFrames 资源里，每个动画单独设 FPS 与循环
- SpriteFrames 面板导入图片或切 sprite sheet
- `play(&"run")`，`speed_scale` 整体变速
- `animation_finished` 对循环动画不发，`animation_looped` 才发
- `frame_changed` 做脚步声和判定
- 判定要和精灵帧同一时间线时，用 Sprite2D 的 `frame` 属性轨道加 AnimationPlayer
- 对正在播的同名动画再 `play()` 不重启，`stop()` 把 `frame` 归零
- SpriteFrames 是共享资源，独立改动先 `duplicate()`
- 既换帧又动骨骼，用 Sprite2D 的 `hframes` `vframes` `frame` 加 AnimationPlayer

### 命中闪白

```glsl
shader_type canvas_item;

instance uniform float flash : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	COLOR.rgb = mix(COLOR.rgb, vec3(1.0), flash);
}
```

```gdscript
extends Sprite2D

var _tween: Tween

func hit_flash() -> void:
	if _tween != null:
		_tween.kill()
	set_instance_shader_parameter(&"flash", 1.0)
	_tween = create_tween()
	_tween.tween_property(self, "instance_shader_parameters/flash", 0.0, 0.12)
```

- `instance uniform` 每个实例独立，同一材质的敌人不会一起闪
- 普通 `uniform` 改的是共享材质

### 确定性回放

锁步联机、回放要逐帧复现表现时：

| 工具 | 做法 |
|---|---|
| AnimationPlayer | `callback_mode_process` 设 `ANIMATION_CALLBACK_MODE_PROCESS_MANUAL`，每 tick `advance(delta)` |
| AnimationPlayer 跳转 | `seek(秒, true)`，`update` 为 true 才立即应用 |
| Tween | 无 seek，`pause()` 后 `custom_step(delta)` 只能前进 |
| Tween 回到更早时刻 | 重建 Tween 再从零 `custom_step` |

- `seek` 只调用目标时刻前最近的一个方法键，不逐个触发
- 要逐个触发方法键用 `advance`
- `seek` 的 `update_only` 为 true 时方法和音频轨道都不处理，到末尾不发 `animation_finished`
- `custom_step` 走完的那次仍返回 true，判断结束用 `finished` 信号
- 动画只影响表现，模拟状态不读 AnimationPlayer 或 Tween 的值

### 曲线

| 需求 | 用这个 |
|---|---|
| 缓动 | `Tween.TRANS_*` 加 `Tween.EASE_*` |
| 自定义形状缓动 | Curve 资源，`tween_method` 把 t 从 0 到 1，回调里 `curve.sample(t)` |
| 一次性插值计算 | `Tween.interpolate_value(initial, delta, elapsed, duration, trans, ease)` |
| AnimationPlayer 里的曲线 | bezier 轨道，取值 `Animation.bezier_track_interpolate()` |
| 渐变色 | Gradient 的 `sample()` |

### 外部来源

| 来源 | 做法 |
|---|---|
| 3D 角色动画 | 导出 glTF，导入得到带 AnimationPlayer 的场景，高级导入设置里拆剪辑设循环，骨架不同看 Retargeting |
| 2D 骨骼 | 内置 Skeleton2D 加 Bone2D 加 Polygon2D，动画仍是 AnimationPlayer |
| Aseprite | 无内置导入，导出 sprite sheet 后用 SpriteFrames 面板的 Add frames from a Sprite Sheet，或用社区插件 |
| Spine | 无内置支持，走厂商的 Godot 运行时，先核对支持的 Godot 版本 |

## 陷阱

| 现象 | 做法 |
|---|---|
| `modulate` 设大于 1 闪白，暗部仍偏暗 | modulate 是乘法，换 shader 的 `mix` |
| Container 子节点的 `position` 动画被覆盖 | 容器重新排版，动画外层包一个普通 Control |
| 目标释放后带回调的循环 Tween 仍在跑 | 用节点的 `create_tween()` 绑定，或销毁时 `kill()` |
| AnimationPlayer 与 Tween 同写一个属性时抖动 | 同一属性只留一个驱动方 |
| AnimationTree 激活后又调 AnimationPlayer 的 `play()`，两边抢轨道 | 只改树的参数或 `travel()` |
| 方法调用轨道读到处理之后的状态 | 默认 DEFERRED，要同帧顺序时改 `ANIMATION_CALLBACK_MODE_METHOD_IMMEDIATE` |
| 方法调用轨道没反应，无报错 | 核对轨道的目标节点路径 |
| 改动画或 SpriteFrames 影响所有实例 | 共享资源，先 `duplicate()` |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/animation-tree.md](references/animation-tree.md)：搭建顺序、参数路径、状态机操作、OneShot、BlendSpace、根运动
- [references/tween-recipes.md](references/tween-recipes.md)：打断重播、飘字、数字滚动、转场、循环、Subtween、等信号、手动推进
- https://docs.godotengine.org/en/stable/tutorials/animation/index.html
- https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html
- https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html
