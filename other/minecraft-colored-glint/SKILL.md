---
name: minecraft-colored-glint
description: 从自然语言、HEX 色值或色板制作 Minecraft 物品彩色附魔流光，支持任意自定义单色、多色渐变、整体彩虹变色与流动渐变，生成贴图、配方、GLSL 和 Forge 着色器接入资源。处理按物品选色、Glint RenderType、foil 入口、缓冲串色、循环接缝及 Cosmic 叠加；不用于普通天空星场、粒子特效或只改物品名称颜色。
---

# Minecraft 彩色附魔流光

以项目内 RenderBlender 的 `GlintManager → GlintLayerManager → ItemRendererMixin` 为研究基线：颜色选择绑定到物品，纹理和流动状态绑定到实际 glint 绘制层。保留基础模型、动作和深度遮挡；单独决定是否绘制流光、采用哪种外观。

**证据范围：**原始 RenderBlender 快照为 Forge 1.20.1 / 47.4.13 / Java 17，仅静态分析，存在接入缺口。独立提炼的 Colored Glint Lab 已在 Forge 1.20.1 / 47.4.10 的 ASTRA-TEST 客户端完成 12 场景实测：同屏四色、强制青色流光、左右手、第三人称、满弓、掉落物/展示框、两次资源重载及 Cosmic 叠加。两类证据分开；详情见 [运行基线](references/forge-1.20.1-runtime.md)。

自定义/渐变生成器另有颜色、文件保护和 GPU 编译/采样验证。Lab 0.2.0 的玫瑰金、极光、彩虹循环和余烬流动另完成 15 场景游戏采集与 73 项证据检查；动态 shader 仅接入 direct，其余模式保留原版流光。原九色与新渐变证据分开，均不证明穿戴护甲或其他版本已通过。

## 工作流程

1. 读取目标工程的 Minecraft、加载器、Java、mappings 和已有渲染入口。按用户目标处理普通 baked item、动态/自定义渲染物品或穿戴护甲；不把一个 `getFoilBufferDirect` hook 当成全覆盖。只有研究请求时交付分析，实施请求才改代码。
2. 复用本项目素材或研究原实现时读 [源码依据与缺陷](references/source-audit.md)。明确这是参考快照，不是无须修正的模板。
3. 实施前读 [Forge 接入与渲染状态](references/integration.md)。将配置解析、是否发光、RenderType 分支及绘制时状态分开；先实现用户要求的物品类别，再扩大覆盖范围。
4. 用户要自定义颜色、渐变、彩虹或调色辅助时，先读 [配色创作](references/authoring.md)。把自然语言转换成明确色值、色标、模式、坐标、插值、周期和强度；用 `author_glint.py` 生成可重复配方、素材、预览与接入清单。预设只作起点，不能限制用户色板。仅需批量单色 PNG 时可按 [素材与调色](references/textures.md) 使用轻量脚本。
5. 读 [渐变接入](references/gradient-integration.md)：静态 PNG 与动态 shader 分路处理。实验模组使用有限 ID 注册表（0.2.0 为原九色加四套配方），用户的新 ID 仍须注册；动态颜色在真实 draw 时绑定时间，并使用中性载体，避免重复染色。剑尖/剑柄固定渐变需要模型坐标适配，不能用默认滚动 glint UV 冒充。
6. 同一物品还带星空材质时，读 [与 Cosmic/动态模型共存](references/cosmic-and-custom-models.md)，先确认基础几何、星空与流光的实际 draw 顺序。
7. 按 [验收与排错](references/validation.md) 检查用户要求的场景。交付修改内容、实际构建/运行结果及未覆盖边界；未启动游戏时明确写“运行效果未验证”。

复用本地 Forge 1.20.1 成果时，先读 [运行基线](references/forge-1.20.1-runtime.md)。它使用实际调用点参数和不可变 buffer 包装器，不需要静态 current-stack；配置键为 `ColoredGlint`，不要混用原库 NBT 示例。其余物品类别仍需按对应入口扩展。

## 实施不变量

- **发光与选色独立。**常规语义为 `drawFoil = vanillaFoil || forceFoil`；颜色在 draw 已启用后解析。`forceFoil=false` 不应阻止原本附魔物品使用配置颜色。
- **保持原分支语义。**未知 ID、未配置、`default` 或空 provider 返回原调用的 `origin`。物品、实体、透明和护甲入口必须分别匹配，不能一律回退或替换成 `glintDirect()`。
- **配置决定每次 draw，而非全局残留。**不要只改共享 uniform 后排队多个物品；采用颜色/模式分组的 RenderType、真正匹配的顶点参数或有边界的 flush。用同屏红蓝物品检查串色。
- **渲染上下文可嵌套且必须恢复。**优先显式传 `ItemStack`；需要桥接无 stack 的 helper 时用作用域及 `try/finally` 恢复外层上下文。单个静态 stack 的 HEAD/TAIL 写入不能保证重入和异常安全。
- **保留渲染契约。**参考使用 `POSITION_TEX + QUADS`、glint 混合、只写颜色、EQUAL 深度及滚动纹理状态。新增 shader 必须同步顶点格式、sampler 和 draw 时参数；不能通过禁用深度解决覆盖问题。
- **配色方案可以任意，运行状态必须有界。**允许用户任意合法 HEX 色值和 2–16 色标，不能只从九色或四个预设中选择。渐变 `repeat` 必须闭合首尾颜色，开放色板默认 `pingpong`；按配方 ID/模式缓存，不按每帧 RGB 或时间增长缓存。
- **客户端隔离。**glint 渲染类和 Mixin 仅客户端加载。共有物品配置不要在专用服务器初始化客户端 RenderType。
- **尊重版本差异。**本技能的 NBT 示例仅指 1.20.1；新版本的组件、RenderType、foil 方法与 Mixin 描述符必须从目标源码核对。纯资源包可以替换已有纹理，但不能凭空创建按物品分派的 Java 管线。

## 三维工作台

需要实时流光预览、多个光纹起点和参数回放时，使用 [三维工作台](references/workbench.md)。三种层次方案、水光对照和旧八个预设随包交付；新版采用整件装备共用坐标，包含持续光流与局部受击回应。共享 GLSL 与本机护甲贴图提取器随包交付，原版贴图不打包。它们是设计预览，不能继承旧游戏基线的穿戴验收。

## 随附资源

- `assets/glint/glint_item_{red,yellow,blue,orange,green,purple,white,pink,aqua}.png`：原快照中的 9 张贴图，未改像素；来源与原许可见 [assets/NOTICE.md](assets/NOTICE.md)。这是纹理素材，不是可安装模组。
- [scripts/author_glint.py](scripts/author_glint.py)：Python + Pillow；按 JSON 配方生成自定义单色、空间渐变、时间变色和流动渐变，附 PNG、GLSL、Forge 1.20.1 shader 三件套及接入清单。具体输出与限制见 [配色创作](references/authoring.md)。
- `assets/presets/`：[玫瑰金单色](assets/presets/rose-gold.json)、[极光渐变](assets/presets/aurora.json)、[彩虹循环](assets/presets/rainbow-cycle.json)、[余烬流动](assets/presets/ember-wave.json)。修改副本制作用户自己的色板。
- [scripts/recolor_glint.py](scripts/recolor_glint.py)：按亮度轮廓批量生成单色，保留尺寸、alpha 和存在的 `.mcmeta`。侧车复制仅保留数据，不保证独立 glint 纹理会自动播放帧动画。
- [references/source-manifest.json](references/source-manifest.json)：源文件、贴图及许可的 SHA-256 与图像属性；用于追溯快照，不代表运行通过。

后续交付模组时将选用贴图放进目标命名空间，保留来源声明。不要直接在已安装技能目录构建模组或运行游戏。
