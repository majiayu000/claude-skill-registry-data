---
name: godot-input
description: 写移动 跳跃 攻击 视角控制 改键菜单 手柄支持时用。InputMap 动作代替硬编码按键、get_axis get_vector 死区、键盘手柄双绑定、_unhandled_input 与轮询的选择、运行时改键并存档、鼠标捕获、输入缓冲、手柄震动与热插拔。input map keybinding gamepad.
---

# Godot 输入

玩法输入走 InputMap 动作，同一动作绑键盘与手柄，用 `Input` 的轴和向量接口读值。

## 范围

| 不含 | 去哪 |
|---|---|
| UI 控件焦点、点击、按键提示文本 | godot-ui |
| 设置界面与存档格式 | godot-ui godot-resources-data |
| 联机输入同步 | godot-multiplayer |
| 无头测试里模拟输入 | godot-headless-testing |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 判断按键 | InputMap 动作加 `Input.is_action_pressed` | `event.keycode == KEY_W` |
| 一维轴 二维移动 | `Input.get_axis` `Input.get_vector` | 分别读两个方向再相减拼向量 |
| 摇杆死区 | 动作的 `deadzone`，`get_vector` 取各动作死区平均值做圆形死区 | `if abs(x) < 0.2` |
| 手柄支持 | 同一动作加 `InputEventJoypadButton` `InputEventJoypadMotion` | 另写一套手柄分支 |
| 改键 | `InputMap.action_erase_event` 加 `action_add_event` | 自己维护按键表 |
| 触屏摇杆 | VirtualJoystick 4.7+，TouchScreenButton | 自己解析 `InputEventScreenTouch` |
| 模拟输入 | `Input.action_press`，`Input.parse_input_event` | 直接改自己的状态 |

## 做法

### 定义动作

在项目设置 Input Map 页添加，键盘与手柄放进同一个动作：

```ini
[input]

jump={
"deadzone": 0.2,
"events": Array[InputEvent]([Object(InputEventKey,"resource_local_to_scene":false,"resource_name":"","device":-1,"window_id":0,"alt_pressed":false,"shift_pressed":false,"ctrl_pressed":false,"meta_pressed":false,"pressed":false,"keycode":0,"physical_keycode":32,"key_label":0,"unicode":0,"location":0,"echo":false,"script":null)
, Object(InputEventJoypadButton,"resource_local_to_scene":false,"resource_name":"","device":-1,"button_index":0,"pressure":0.0,"pressed":false,"script":null)
])
}
```

| 字段 | 规则 |
|---|---|
| 移动键 | 绑 `physical_keycode`，AZERTY 上 WASD 位置不变 |
| 字符含义的快捷键 | 绑 `keycode` |
| 摇杆方向 | 每方向一个 `InputEventJoypadMotion`，`axis_value` -1.0 绑左，+1.0 绑右 |
| 扳机 | 只有 +1.0 |
| `device` | -1 为所有设备，本地多人每位玩家单独动作如 `p1_jump` 并指定设备号 |

- 动作名用玩法语义，不复用驱动 UI 焦点的 `ui_accept` `ui_up`

```gdscript
extends CharacterBody2D

const SPEED := 220.0

func _physics_process(_delta: float) -> void:
	velocity = Input.get_vector(&"move_left", &"move_right", &"move_up", &"move_down") * SPEED
	move_and_slide()
```

- `get_vector` 长度已限制为 1，不用再 `normalized()`
- `get_vector` 第五个参数可覆盖死区
- 只有横向的平台游戏用 `Input.get_axis(&"move_left", &"move_right")`
- 模拟量用 `Input.get_action_strength`

### 回调选择

| 方式 | 适用 |
|---|---|
| `_physics_process` 里轮询 `Input.*` | 持续状态：移动、蓄力、按住 |
| `_unhandled_input(event)` | 一次性动作：跳、攻击、交互，UI 已处理的事件到不了这里 |
| `_input(event)` | 须先于 UI 看到：全局热键、改键捕获 |

事件顺序：`_input`、GUI、`_shortcut_input`、`_unhandled_key_input`、`_unhandled_input`。处理完调 `get_viewport().set_input_as_handled()`。

- 事件回调里用 `event.is_action_pressed(&"jump")`，不用 `Input.is_action_just_pressed`
- `event.is_action_pressed` 默认不含按住重复，要重复传 `allow_echo = true`
- `Input.is_action_just_pressed` 在 `_process` 里按帧、在 `_physics_process` 里按 tick 判断
- 一帧跑多个 tick 时只有一个 tick 为 true，按下后迅速松开也为 true
- 在哪个回调里消费就在哪个回调里读，不在 `_process` 置标志给物理消费

### 输入缓冲

`_unhandled_input` 记录，物理里消费。时间用 `Engine.get_physics_frames()`，回放时结果一致：

```gdscript
extends CharacterBody2D

const BUFFER_TICKS := 6
const JUMP_SPEED := -420.0

var _jump_pressed_tick: int = -1000

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed(&"jump"):
		_jump_pressed_tick = Engine.get_physics_frames()

func _physics_process(delta: float) -> void:
	if not is_on_floor():
		velocity += get_gravity() * delta
	elif Engine.get_physics_frames() - _jump_pressed_tick <= BUFFER_TICKS:
		velocity.y = JUMP_SPEED
		_jump_pressed_tick = -1000
	move_and_slide()
```

### 改键

```gdscript
extends Node

const SAVE_PATH := "user://keybinds.cfg"

func rebind(action: StringName, event: InputEventKey) -> void:
	_apply(action, event)
	var cfg := ConfigFile.new()
	cfg.load(SAVE_PATH)
	cfg.set_value("keys", action, event.physical_keycode)
	cfg.save(SAVE_PATH)

func load_saved(actions: Array[StringName]) -> void:
	var cfg := ConfigFile.new()
	if cfg.load(SAVE_PATH) != OK:
		return
	for action in actions:
		if cfg.has_section_key("keys", action):
			var event := InputEventKey.new()
			event.physical_keycode = cfg.get_value("keys", action) as Key
			_apply(action, event)

func _apply(action: StringName, event: InputEventKey) -> void:
	for old: InputEvent in InputMap.action_get_events(action):
		if old is InputEventKey:
			InputMap.action_erase_event(action, old)
	InputMap.action_add_event(action, event)
```

- 只清同一类设备的事件，改键盘键不清手柄绑定
- 存档存键码整数，启动时调一次 `load_saved`
- 恢复默认：`InputMap.load_from_project_settings()` 再删存档文件
- 冲突检测：遍历 `InputMap.get_actions()` 逐个 `InputMap.action_has_event()`
- 捕获新按键：监听状态下在 `_input` 里接第一个 `pressed` 的 `InputEventKey`，调 `set_input_as_handled()`
- 捕获时 Esc 取消，手柄接 `InputEventJoypadButton`

### 鼠标与触屏

| 需求 | 做法 |
|---|---|
| 视角控制 | `Input.mouse_mode = Input.MOUSE_MODE_CAPTURED`，读 `InputEventMouseMotion.screen_relative` |
| 打开菜单 | 切回 `Input.MOUSE_MODE_VISIBLE` |
| 2D 世界坐标 | `get_global_mouse_position()`，`get_viewport().get_mouse_position()` 是视口坐标 |
| 自由画线要逐点轨迹 | 关 `Input.use_accumulated_input`，默认同帧鼠标移动合并 |
| 触屏按钮 | TouchScreenButton 的 `action` 属性 |
| 触屏摇杆 | VirtualJoystick 4.7+，`action_left` 等指到玩法动作，`Input.get_vector` 照常读 |

- `InputEventMouseMotion.relative` 按拉伸缩放，灵敏度随分辨率变
- VirtualJoystick 的 `action_*` 默认是 `ui_*`，必须改成玩法动作
- VirtualJoystick 的 `deadzone_ratio` 默认 0.0，设了以后先于动作死区生效
- `input_devices/pointing/emulate_mouse_from_touch` 默认开，触摸合成鼠标事件

### 手柄

- 震动：`Input.start_joy_vibration(device, weak, strong, duration)`，强度 0 到 1
- `duration` 为 0 时约 65 秒，`Input.stop_joy_vibration` 提前停，给玩家留关闭选项
- 热插拔：连 `Input.joy_connection_changed` 信号，已连接设备用 `Input.get_connected_joypads()`

## 陷阱

| 现象 | 做法 |
|---|---|
| 斜向速度到 1.414 倍 | 两次 `get_axis` 拼向量没有圆形死区，用 `get_vector` |
| 插手柄毫无反应 | InputMap 只绑了键盘，每个动作检查手柄绑定 |
| 改键和换键盘布局后玩法键失效 | 用了 `Input.is_key_pressed(KEY_W)` 或 `event.keycode`，改用动作 |
| 游戏内点击穿透按钮 | 在 `_input` 里处理，改 `_unhandled_input` |
| LineEdit 打字时角色跟着移动 | 轮询不看 GUI 焦点，输入框打开时暂停轮询 |
| 菜单打开时玩法键同时触发 | 把 `ui_accept` `ui_cancel` 当了玩法键 |
| 某些组合键按下读不到 | 键盘幽灵键，组合键少设计 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html
- https://docs.godotengine.org/en/stable/tutorials/inputs/input_examples.html
- https://docs.godotengine.org/en/stable/tutorials/inputs/controllers_gamepads_joysticks.html
