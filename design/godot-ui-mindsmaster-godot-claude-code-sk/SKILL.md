---
name: godot-ui
description: 写菜单 HUD 对话框 血条 设置界面 本地化 分辨率适配 UI 导航时用，做设置即时生效 窗口模式 全屏 窗口尺寸确认还原 失焦暂停时也用。Control 布局 Container anchors、项目级 Theme 统一字体、StyleBox、ProgressBar 血条、RichTextLabel、多分辨率 stretch aspect、tr() 本地化、手柄焦点导航、mouse_filter 吃点击、CanvasLayer HUD、弹窗 拖放。UI layout, theme, localization, settings menu, fullscreen, pause on focus loss.
---

# Godot UI

Control 界面：场景里用 Container 和 anchors 搭，项目级 Theme 统一外观，用内置的 ProgressBar、RichTextLabel、翻译系统和焦点导航。

## 范围

| 不含 | 去哪 |
|---|---|
| 2D 世界里的节点摆放 | godot-2d |
| 输入动作定义、改键 | godot-input |
| 动画选型、数字滚动 | godot-animation |
| 3D 场景里的 UI 面板 | godot-2d-in-3d |
| `.tscn` 里导出节点引用的写法 | godot-scene-architecture |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 界面摆放 | 场景里的 Container 加 anchors preset | 代码里按 1920x1080 写死 `position` 和 `size` |
| 边距 | MarginContainer | 手算偏移 |
| 竖排 横排 网格 自动换行 | VBoxContainer HBoxContainer GridContainer 的 `columns` HFlowContainer VFlowContainer | 逐个设 `position`，双重循环算坐标，手写换行 |
| 保持宽高比 | AspectRatioContainer | `_process` 里改 `size` |
| 滚动列表 | ScrollContainer | 手写裁剪与拖动 |
| 屏幕固定的 HUD | `CanvasLayer` 下放铺满的 Control | 世界场景里直接放 Control，随 Camera2D 滚走 |
| 确认框 弹窗 | AcceptDialog ConfirmationDialog，`popup_centered()`，自带 `confirmed` `canceled` 信号与 Esc 关闭 | 手写居中 确定取消按钮与 Esc 处理 |
| 拖放 悬浮提示 | `_get_drag_data` `_can_drop_data` `_drop_data`，`tooltip_text`，`_make_custom_tooltip` | `_gui_input` 里自己算拖拽与悬停计时 |
| 折叠面板 | FoldableContainer 4.5+ | Button 加手动 `visible` |
| 面板背景 | PanelContainer 或 Panel 加 StyleBoxFlat | ColorRect 叠 ColorRect |
| 血条 经验条 | ProgressBar 或 TextureProgressBar | 改 ColorRect 的 `size.x` |
| 全局字体颜色按钮样式 | 项目级 Theme | 到处 `add_theme_*_override` |
| 同类控件多种样式 | theme type variation | 每个节点单独覆盖 |
| 富文本 打字机效果 | RichTextLabel 的 BBCode 与 `visible_ratio` | 多个 Label 拼接 |
| 玩家可见文本 | `tr()` 加翻译表 | 字符串硬编码 |
| 按键提示 | `InputMap.action_get_events` | 写死 "E" |
| 手柄菜单导航 | focus_neighbor 与 `grab_focus()` | 自己监听方向键切换高亮 |
| 分辨率适配 | `display/window/stretch/mode` | 运行时按窗口大小手动缩放根节点 |

## 做法

### 布局

HUD 与菜单在场景里搭：根 Control 用 `Full Rect` preset，其下嵌套 Container。

```ini
[node name="Hud" type="Control"]
layout_mode = 3
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
mouse_filter = 2

[node name="Margin" type="MarginContainer" parent="."]
layout_mode = 1
anchors_preset = 15
anchor_right = 1.0
anchor_bottom = 1.0
theme_type_variation = &"HudMargin"

[node name="Row" type="HBoxContainer" parent="Margin"]
layout_mode = 2

[node name="HealthBar" type="ProgressBar" parent="Margin/Row"]
custom_minimum_size = Vector2(240, 24)
layout_mode = 2
show_percentage = false
```

- 有 Camera2D 时 HUD 放 `CanvasLayer` 下，否则随相机移动
- `CanvasLayer.layer` 默认 1，大的在上
- 根 Control 设 `mouse_filter = 2` 即 IGNORE，否则吃掉所有点击
- Container 决定子节点位置，子节点只表达尺寸需求

| 子节点属性 | 作用 |
|---|---|
| `custom_minimum_size` | 尺寸下限 |
| `size_flags_horizontal = 3` | 即 `Control.SIZE_EXPAND_FILL`，占满剩余空间 |
| `size_flags_stretch_ratio` | 多个 EXPAND 子节点间按比例分配 |
| 空 Control 加 EXPAND_FILL | 当弹簧，推开左右两组控件 |

浮动控件，如跟随角色的血条、弹出提示，才用代码摆，仍用 preset：

```gdscript
extends Control

func _ready() -> void:
	set_anchors_and_offsets_preset(Control.PRESET_CENTER_BOTTOM, Control.PRESET_MODE_MINSIZE, 32)
```

- `set_anchors_preset` 只改锚点，不改偏移
- 一般用 `set_anchors_and_offsets_preset`
- `PRESET_FULL_RECT` 铺满，`PRESET_TOP_WIDE` 贴顶拉宽

### 容器限制

Container 在子节点变化和 `queue_sort()` 时重排，子节点的 `position` `size` 动画会被覆盖。

- 动画改动 `scale` `modulate` `rotation`，或外包一层普通 Control
- 按中心缩放、Label 换行、滚动区宽度见 [references/layout.md](references/layout.md)

### Theme

外观放一个 Theme 资源，项目设置里挂成全局默认：

```ini
[gui]

theme/custom="res://ui/theme/main.tres"
theme/custom_font="res://ui/fonts/main.ttf"
```

- 对应 `gui/theme/custom` 与 `gui/theme/custom_font`
- 任何 Control 不设 `theme` 也继承它，代码建的 UI 同样继承
- 局部换主题：给 Control 设 `theme`，Control 与 Window 后代继承
- 遇到其他类型的节点，继承断开
- 颜色字号间距在 Theme 编辑器里改，脚本只读：`get_theme_color(&"font_color", &"Label")`
- 同类控件多种样式用 theme type variation，单个 Label 用 `label_settings`
- StyleBox 种类、变体、LabelSettings 见 [references/theme.md](references/theme.md)

单个节点的一次性差异才用 override，如血条填充色随阵营变：

```gdscript
extends ProgressBar

func set_team_color(color: Color) -> void:
	var fill := get_theme_stylebox(&"fill").duplicate() as StyleBoxFlat
	fill.bg_color = color
	add_theme_stylebox_override(&"fill", fill)
```

- `duplicate()` 必须有，否则改到 Theme 里共享的 StyleBox

### 血条

ProgressBar 做纯色条，TextureProgressBar 做贴图条或环形条。样式在 Theme 里改 `fill` 与 `background`。

| 属性 | 用法 |
|---|---|
| ProgressBar `show_percentage` | 默认 true，血条关掉 |
| ProgressBar `step` | 默认 0.01 |
| TextureProgressBar `step` | 默认 1.0，Tween 平滑时设 0.01 或更小，否则出阶梯 |
| TextureProgressBar `fill_mode` | 径向值做冷却环、圆形血球，不用 shader |
| TextureProgressBar `nine_patch_stretch` | 贴图拉伸，配 `stretch_margin_*` |

缓动与受伤残影：

```gdscript
extends Control

@onready var _front: ProgressBar = %Front
@onready var _chip: ProgressBar = %Chip

var _tween: Tween

func set_health(value: float) -> void:
	_front.value = value
	if _tween:
		_tween.kill()
	_tween = create_tween()
	_tween.tween_interval(0.4)
	_tween.tween_property(_chip, "value", value, 0.3).set_trans(Tween.TRANS_CUBIC).set_ease(Tween.EASE_OUT)
```

- 前景条与残影条同位置叠放，残影条在下，填充用浅色
- 前景条 `background` 设 StyleBoxEmpty，否则盖住残影条

### RichTextLabel

| 需求 | 用法 |
|---|---|
| BBCode | `bbcode_enabled = true`，写 `[b]` `[color=red]` `[url]` `[img]` |
| 打字机 | Tween 驱动 `visible_ratio` 从 0 到 1，或改 `visible_characters` |
| 高度随内容 | `fit_content = true`，放在 VBox 里常用 |
| 链接点击 | 连 `meta_clicked`，`[url]` 默认点击无反应 |
| 自定义效果 | 继承 RichTextEffect，`bbcode` 定标签名，`_process_custom_fx` 改 `CharFXTransform` |

- 带自定义效果的 RichTextLabel 每帧处理，不用时隐藏
- 标签清单与效果示例见 [references/richtext.md](references/richtext.md)

### 多分辨率

| 游戏 | `display/window/stretch/mode` | `display/window/stretch/aspect` |
|---|---|---|
| 大多数游戏 | `canvas_items` | `expand` |
| 像素风 | `viewport` | `keep` 或 `expand` |

- 4.7 起新建项目默认 `canvas_items` 加 `expand`
- 除 `keep` 外，HUD 靠 anchors 和 Container 贴边
- 各取值、整数缩放、界面缩放、安全区见 [references/layout.md](references/layout.md)

### 本地化

玩家可见文本一律进翻译表，含按钮文字、提示、地点名。

| 文本 | 写法 |
|---|---|
| 控件的 `text` | 填翻译键如 `MENU_START`，运行时自动翻译 |
| 脚本拼接 | `tr("KEY")` |
| 带变量 | `tr("PICKED_UP").format({item = name})`，占位符位置由译者调整 |
| 复数 | `tr_n("%d item", "%d items", count) % count` |
| 同词不同义 | 第二个参数 context：`tr("Close", "Distance")` |
| 不翻译，如玩家名 | `auto_translate_mode` 设 `Node.AUTO_TRANSLATE_MODE_DISABLED` |
| 切换语言 | `TranslationServer.set_locale("zh_CN")`，存进设置，启动时恢复 |

- 复数形式不止两种，不写 `if count == 1`
- `tr_n` 前两个参数写带 `%d` 的英文原文，它是键也是回退文本
- CSV 复数要 `?plural` 列 4.6+，4.5 及以前用 PO
- `tr()` 的结果切换语言后不自动更新，在 `NOTIFICATION_TRANSLATION_CHANGED` 里重设：

```gdscript
extends Label

var _count: int = 0

func _notification(what: int) -> void:
	if what == NOTIFICATION_TRANSLATION_CHANGED:
		text = tr_n("%d item", "%d items", _count) % _count
```

- 导入、注册、伪本地化、字体回退见 [references/localization.md](references/localization.md)

### 焦点导航

- 场景启动后须有控件拿焦点，否则方向键和手柄无反应
- 写法：`$StartButton.grab_focus.call_deferred()`
- 控件隐藏会丢焦点，面板重新显示要再抓
- `focus_mode`、邻居、弹窗还焦点、无障碍名称见 [references/focus-navigation.md](references/focus-navigation.md)

### 按键提示

- 提示文本从 `InputMap.action_get_events` 取，改键后自动跟随
- 绑定 `physical_keycode` 时用 `as_text_physical_keycode()`
- 手柄按 `InputEventJoypadButton.button_index` 映射到自己的图标
- 完整写法与键帽字母见 [references/focus-navigation.md](references/focus-navigation.md)

### 输入顺序

`_input`、`_gui_input`、`_shortcut_input`、`_unhandled_key_input`、`_unhandled_input`，依次传递。

| 输入 | 放哪 |
|---|---|
| Control 内部拖动、自绘区域点击 | `_gui_input`，处理完 `accept_event()` |
| 游戏世界的点击与按键 | `_unhandled_input`，UI 处理过的到不了 |
| 暂停、截图等全局键 | `_unhandled_input` 或 `_shortcut_input` |
| 按钮快捷键 | `BaseButton.shortcut` |

- 不手写鼠标是否在 UI 上的判断

### mouse_filter

| 值 | 行为 | 默认值为它的控件 |
|---|---|---|
| `MOUSE_FILTER_STOP` | 吃掉事件，下层和 `_unhandled_input` 收不到 | Control Panel PanelContainer ColorRect Button ProgressBar RichTextLabel |
| `MOUSE_FILTER_PASS` | 未 `accept_event()` 就冒泡给父 Control，到 STOP 为止 | 各 Container、TextureRect、TextureProgressBar |
| `MOUSE_FILTER_IGNORE` | 不收事件，也不挡下层 | Label NinePatchRect |

- 滚轮例外：`mouse_force_pass_scroll_events` 默认 true，STOP 也放行
- HUD 根节点、装饰 ColorRect TextureRect Panel、按钮上的图标设 IGNORE
- 子树关鼠标：`mouse_behavior_recursive = Control.MOUSE_BEHAVIOR_DISABLED` 4.5+

## 陷阱

| 现象 | 做法 |
|---|---|
| `custom_minimum_size` 设小了控件仍很大 | 它只是下限，文字内容也会撑大 |
| 手写 `.tscn` 给导出的节点引用赋 NodePath，运行时为 null | 节点头补 `node_paths=PackedStringArray("player")`，见 godot-scene-architecture |
| 改 `get_theme_stylebox()` 的返回值，同类控件一起变 | 先 `duplicate()` |
| 显示玩家名的 Label 被替换成译文 | 关 `auto_translate_mode`，名字与翻译键同名时会被翻译 |
| 菜单打开时玩法重复触发 | 玩法不用 `ui_accept` 等内置动作 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/localization.md](references/localization.md)：CSV 与 PO 导入、注册翻译、复数与上下文、TranslationServer、伪本地化、字体回退
- [references/theme.md](references/theme.md)：StyleBox 种类与代码构造、theme type variation、LabelSettings
- [references/layout.md](references/layout.md)：容器排版限制、stretch 各取值、整数缩放、界面缩放、安全区
- [references/focus-navigation.md](references/focus-navigation.md)：手柄焦点导航、`focus_mode`、按键提示与键帽字母、设备切换、无障碍
- [references/richtext.md](references/richtext.md)：BBCode 标签速查、自定义 RichTextEffect、打字机
- [references/settings-menu.md](references/settings-menu.md)：设置即时生效、离开即保存与按应用保存、未保存状态显示、窗口模式与尺寸的确认倒计时和还原、全屏与窗口尺寸陷阱、启动参数恢复入口、失焦暂停
- https://docs.godotengine.org/en/stable/tutorials/ui/index.html
- https://docs.godotengine.org/en/stable/tutorials/i18n/index.html
- https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html
