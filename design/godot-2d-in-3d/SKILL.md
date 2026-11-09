---
name: godot-2d-in-3d
description: 在 Godot 4 的 3D 场景里放 2D 角色时用，2.5D 纸片人 HD-2D 像素角色配 3D 场景。Sprite3D AnimatedSprite3D billboard 正对镜头、pixel_size、投影阴影 cast_shadow、透明排序、像素清晰不发糊、SubViewport 把 2D 贴进 3D、Label3D、景深移轴。纯 2D 游戏见 godot-2d。
---

# Godot 2D 角色放进 3D 场景

用 Sprite3D、SubViewport 把 2D 美术放进真 3D 场景，配 Environment 做 HD-2D 观感。

标了实测的条目来自 4.7.2 软件渲染读像素，Compatibility 与 Forward+ 两个渲染器，方法见 [references/render-check.md](references/render-check.md)。

## 范围

| 不含 | 去哪 |
|---|---|
| 纯 2D 项目、TileMapLayer、Camera2D | godot-2d |
| 动画状态机、帧动画 | godot-animation |
| shader 细节 | godot-shaders-vfx |
| UI 主题与布局 | godot-ui |
| 3D 光照、GI、导入 | godot-3d |

## 先查内置

| 需求 | 用这个 | 别自己写 |
|---|---|---|
| 3D 里的 2D 角色 | `Sprite3D`、`AnimatedSprite3D` | 手写四边形网格加 shader |
| 始终面向相机 | `SpriteBase3D.billboard` 取 `BILLBOARD_FIXED_Y` | 每帧 `look_at` 相机 |
| 朝向翻转 | `flip_h` | `scale.x = -1`，billboard 下无效 |
| 角色阴影 | `alpha_cut` 取 `ALPHA_CUT_DISCARD` 或 `ALPHA_CUT_OPAQUE_PREPASS` | 额外画一个阴影网格 |
| 脚下软阴影 | `Sprite3D` 平放，或 `Decal` 限 Forward+ 与 Mobile | 每帧射线加手摆网格 |
| 2D 场景、2D 骨骼、Spine 贴进 3D | `SubViewport` 加 `ViewportTexture` | 逐帧 `get_image` 拷贝 |
| 世界里的文字 | `Label3D` | 每个文字一个 SubViewport |
| 屏幕固定 HUD | `CanvasLayer` 加 Control | 3D 里摆 UI 面板 |
| 头顶血条跟随 | `Camera3D.unproject_position` 定位 Control，或 Sprite3D | 手算投影矩阵 |
| 泛光、环境光遮蔽、雾 | `WorldEnvironment` 的 `Environment` | 多个 SubViewport 叠 bloom |
| 移轴景深 | `CameraAttributesPractical` 的近远模糊 | 后处理 shader 手写模糊 |

## 做法

### 路线选择

| 维度 | 2D 节点手算透视伪 3D | 真 3D 加 Sprite3D |
|---|---|---|
| 摆放 | 位置、缩放、排序全靠每帧自己算 | 节点在 3D 空间，相机负责投影 |
| 相机自由度 | 固定角度，旋转或俯仰要重写公式 | 任意移动、旋转、改 fov |
| 前后遮挡 | 手改 `z_index` 或 `y_sort_enabled` | 深度缓冲，透明物要处理排序 |
| 光照阴影 | `Light2D` 平面光，阴影靠 `LightOccluder2D` | 真 3D 光源，精灵可接受并投射阴影 |
| 雾、景深、SSAO | 没有，只有 glow，要 HDR 2D 或 `BG_CANVAS` | `Environment` 与相机属性，按渲染器取舍 |
| 像素对齐 | 项目设置一键取整，见 godot-2d | 要满足整数倍像素规则，见下 |
| 物理 | `CharacterBody2D` 现成 | 用 3D 物理，或 2D 逻辑再映射 xz |
| 地图工具 | `TileMapLayer` | `GridMap` 或自建网格 |
| 渲染器限制 | HDR 2D 不支持 Compatibility | 效果随渲染器增减，见 references/hd2d-environment.md |
| 适合 | 横版、固定视角、深度仅作缩放层 | 视角会转或俯仰、要真实光影与景深 |

- 要旋转镜头、动态光影、雾、景深任一项，走真 3D
- 只要前景大后景小，手算缩放更省事
- 中途换路线要重做美术摆放与相机

### Sprite3D 配置

```gdscript
extends Sprite3D

func _ready() -> void:
	pixel_size = 1.0 / 32.0
	billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
	texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
	alpha_cut = SpriteBase3D.ALPHA_CUT_DISCARD
	shaded = true
	var used := texture.get_image().get_used_rect()
	offset.y = used.end.y - texture.get_height() * 0.5
```

| 属性 | 默认 | 改成 |
|---|---|---|
| `pixel_size` | 0.01，32 像素图只有 0.32 米 | 每米贴图像素的倒数，如 `1.0 / 32.0` |
| `shaded` | false，不受光不接收阴影 | true |
| `texture_filter` | `TEXTURE_FILTER_LINEAR_WITH_MIPMAPS`，像素图糊 | `TEXTURE_FILTER_NEAREST` |
| `double_sided` | true | 保持，单面时背光不投影 |

- `offset` 单位是贴图像素，脚底要对准不透明脚底行
- 贴图底部常留透明行，取半个高度会让脚悬空
- `Image.get_used_rect()` 的 `end.y` 是最后不透明行的下沿
- `offset.y` 取它减半个高度，上例只适用单帧贴图
- 精灵表按帧区域量；写 `.tscn` 时用脚本或 PIL 读像素算出常数
- TextureAtlas 导入类型只支持 2D，不能给 Sprite3D 用

| 导入陷阱 | 做法 |
|---|---|
| 贴图首次被 3D 使用时自动改成 VRAM Compressed 加 mipmap，像素图出块 | Import 面板 Detect 3D > Compress To 设 Disabled，Compress > Mode 保持 Lossless，重导入 |

### billboard

| 模式 | 行为 | 用在 |
|---|---|---|
| `BILLBOARD_DISABLED` | 按节点自身朝向，法线固定 | 地面贴花、告示牌 |
| `BILLBOARD_ENABLED` | 平面始终正对相机，相机俯仰时跟着后仰 | 特效、光点、图标 |
| `BILLBOARD_FIXED_Y` | 保持竖直，只绕世界 Y 转向相机 | HD-2D 角色，站立物 |

- 俯仰角 p 下 `FIXED_Y` 屏幕高度乘 cos p，`ENABLED` 不缩短
- 保持原高：`scale.y` 设为 1 除以 cos p
- billboard 下绕 Y 的朝向由相机决定，父节点转 180 度无效，实测
- `ENABLED` 绕原点后仰，原点在中心时下沿抬离地面
- 角色用 `FIXED_Y`，原点放脚底

### 朝向翻转

只用 `flip_h`，`AnimatedSprite3D` 同样有。

```gdscript
extends AnimatedSprite3D

func face(direction_x: float) -> void:
	if direction_x != 0.0:
		flip_h = direction_x < 0.0
```

- billboard 下 `scale.x = -1` 不翻转，父节点转向或负缩放也无效，实测
- 负缩放加 `double_sided = false` 时，`ENABLED` 下精灵被背面剔除消失
- 非 billboard 下负缩放可以翻转

### alpha_cut 与阴影

| `alpha_cut` | 阴影 | 边缘 | 排序 |
|---|---|---|---|
| `ALPHA_CUT_DISABLED` | 不投影，实测 0 像素 | 平滑半透明 | 按原点距离从后往前，会错 |
| `ALPHA_CUT_DISCARD` | 只投不透明部分 | 硬边 | 写深度，无排序问题 |
| `ALPHA_CUT_OPAQUE_PREPASS` | 轮廓正确 | 边缘平滑 | 较稳，更贵 |
| `ALPHA_CUT_HASH` | Forward+ 与 `DISCARD` 一致 | 抖动点阵 | 写深度 |

- 像素风角色选 `DISCARD`，半透明羽化边才选 `OPAQUE_PREPASS`
- `ALPHA_CUT_HASH` 在 Compatibility 实测不裁剪，阴影整块，先别用
- 硬边抗锯齿：`alpha_antialiasing_mode` 设 `ALPHA_ANTIALIASING_ALPHA_TO_COVERAGE`，或开 FXAA、TAA
- 混合透明物不写深度，SSAO 等不作用在它上面
- billboard 加阴影时按场景相机朝向渲染，多相机结果未定义
- 相机绕角色转时影子随相机变形，稳定影子见 [references/shadows.md](references/shadows.md)

### 透明排序

只在 `ALPHA_CUT_DISABLED` 时调，实测两张重叠精灵，A 在前 0.5 米：

| 设置 | 重叠处看到 |
|---|---|
| 默认 | 离相机近的 A |
| B 的 `sorting_offset` 设 2.0 | B |
| B 的 `render_priority` 设 1 | B |
| B 的 `no_depth_test` 设 true | A，B 先画，后画的 A 盖在上面 |
| 两者 `DISCARD`，B 的优先级与偏移都调高 | A，深度决定，两项都无效 |

- `sorting_offset` 在 `VisualInstance3D` 上，单位米
- `render_priority` 只在透明物之间生效
- 不靠 `no_depth_test` 排序，它让精灵穿墙可见

### 光照

- `shaded = true` 后接收 `Light3D`
- billboard 的法线随相机转，光从相机一侧来才亮，背后来为 0
- `FIXED_Y` 法线水平，正上方的光照不亮，实测俯仰 40 度时亮度 0
- 主光要有水平分量并来自相机一侧，背光面靠环境光补
- 环境光：`Environment.ambient_light_source` 设成颜色或天空
- 精灵整面一个法线，要法线贴图用 `QuadMesh` 加 `StandardMaterial3D`
- `billboard_keep_scale` 默认 false，QuadMesh billboard 会丢缩放

### 相机

```gdscript
extends Camera3D

func _ready() -> void:
	projection = Camera3D.PROJECTION_ORTHOGONAL
	size = 360.0 * (1.0 / 32.0)
```

- 正交 `keep_aspect` 默认 `KEEP_HEIGHT`，`size` 是视口高度对应的米数
- 一贴图像素对一屏幕像素：`size = 视口高度像素 × pixel_size`，再除以整数倍
- 透视下该关系只在距离 `视口高度 × pixel_size ÷ (2 × tan(fov ÷ 2))` 的平面成立
- 正交无近大远小，视差靠相机移动与多层场景
- 透视像素风贴图像素大小随距离变，粗细不均
- 竖直物按 cos 俯仰缩短，地面纵深按 sin 缩短
- 经验起点：俯仰 25 到 45 度，透视 fov 20 到 35 度，非官方数值
- `fov` 小透视变形小，相机要退得更远
- `display/window/stretch/mode` 取 `canvas_items` 时 3D 不受拉伸，UI 按比例缩放
- 取 `viewport` 时 3D 也低分辨率渲染再放大

### 像素对齐

- 每个贴图像素占整数个屏幕像素，否则列宽交替不均，实测
- 缩放用整数倍：调相机 `size` 或视口整数缩放
- 整数倍下相机平移亚像素，列宽不变，实测
- `TEXTURE_FILTER_NEAREST` 不采样 mipmap，远处颗粒感
- `TEXTURE_FILTER_NEAREST_WITH_MIPMAPS` 远处平滑，需导入时生成 mipmap
- 透视相机做不到全局整数倍，接受远处不均，或改正交

### 地面阴影

`Decal` 只在 Forward+ 与 Mobile 可用，通用写法是平放的 Sprite3D：

```gdscript
extends Sprite3D

func _ready() -> void:
	var gradient := Gradient.new()
	gradient.set_color(0, Color(0.0, 0.0, 0.0, 0.8))
	gradient.set_color(1, Color(0.0, 0.0, 0.0, 0.0))
	var tex := GradientTexture2D.new()
	tex.gradient = gradient
	tex.fill = GradientTexture2D.FILL_RADIAL
	tex.fill_from = Vector2(0.5, 0.5)
	tex.fill_to = Vector2(1.0, 0.5)
	tex.width = 64
	tex.height = 64
	texture = tex
	axis = Vector3.AXIS_Y
	pixel_size = 0.02
	position.y = 0.01
```

- `axis` 取 Y 让精灵平放朝上，抬高 0.01 米避免深度闪烁
- 用 `Decal` 时 `cull_mask` 排除角色所在层，否则投到角色身上
- 贴花不能改变半透明材质的透明度
- `Decal.texture_albedo` 不能直接用 ViewportTexture，先 `get_image` 再建 `ImageTexture`

### SubViewport 与文字

- 2D 场景、2D 骨骼贴进 3D 用 `SubViewport` 加 `ViewportTexture`
- SubViewport 不继承项目的默认纹理过滤与像素取整
- 设置、`Label3D`、世界内 UI、屏幕叠加见 [references/subviewport-ui.md](references/subviewport-ui.md)
- 雾、景深、移轴见 [references/hd2d-environment.md](references/hd2d-environment.md)

## 陷阱

| 现象 | 做法 |
|---|---|
| billboard 精灵翻转无效，单面时消失 | 用 `flip_h`，不用负缩放 |
| 半透明精灵互相遮挡错序 | 角色用不透明系的 `alpha_cut` |
| 调 `render_priority`、`sorting_offset` 对 `DISCARD` 无效 | 不透明系由深度决定，调位置 |
| 2D 内容进了 SubViewport 又变糊 | SubViewport 单独设过滤，见 subviewport-ui.md |
| Compatibility 下 `Decal` 不显示 | 用平放 Sprite3D |
| HDR 2D 下 SubViewport 色彩异常 | 两个渲染器都未验证，自己读像素确认 |
| Mobile 或真显卡上表现与本页不同 | 本页未在 Mobile 渲染验证，以实机为准 |

## 参考

- [references/csharp.md](references/csharp.md)：C# 项目先读，本文各节示例的 C# 写法
- [references/shadows.md](references/shadows.md)：相机转动时的稳定影子、`double_sided` 与背光、阴影实测数据
- [references/subviewport-ui.md](references/subviewport-ui.md)：SubViewport 贴进 3D 的设置、Label3D、世界内 UI、屏幕叠加
- [references/hd2d-environment.md](references/hd2d-environment.md)：Environment 配方、渲染器支持表、移轴景深
- [references/render-check.md](references/render-check.md)：用虚拟显示器读像素验证渲染行为，已验证项清单
- https://docs.godotengine.org/en/stable/tutorials/3d/3d_rendering_limitations.html
- https://docs.godotengine.org/en/stable/tutorials/3d/3d_text.html
- https://docs.godotengine.org/en/stable/tutorials/3d/environment_and_post_processing.html
- https://docs.godotengine.org/en/stable/tutorials/3d/using_decals.html
- https://docs.godotengine.org/en/stable/tutorials/rendering/viewports.html
- https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html
