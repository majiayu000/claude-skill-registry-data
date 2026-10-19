---
name: minecraft-halo-decoration
description: 从自然语言制作 Minecraft 物品 Halo 光晕、旋转魔法环、放射星芒、呼吸与多层装饰，含 16px 小图专用配方、透明素材和动画预览，指导 Forge 1.20.1 接入及与 Cosmic、附魔流光共存。不用于内部宇宙算法、真实场景照明或屏幕 bloom。
---

# Minecraft Halo 与装饰层

把 Halo 当作附着在物品附近的独立装饰几何。分别决定形状、锚点、尺寸、动画、混合与显示场景；保留主体模型、动作、覆盖材质和原有 glint。用户描述风格即可，无需知道 shader 参数。

来源是 Avaritia / Re-Avaritia / RenderBlender 的 Halo 路线和 ArcaneVortex 的 GlowHelper 静态研究。随附生成器和配方为独立实现，不打包参考 JAR 的源码或纹理。**离线生成与行为检查不等于 Halo 游戏运行认证，不继承 Cosmic/彩色 glint 实验的实测结果。**

## 工作流程

1. 确定 GUI 背光、模型固定环、相机朝向光片或主体脉动副本。缺少场景要求时先做 GUI 背景层；用户要求手持、掉落或穿戴时扩展对应入口。空间、尺寸与深度不能由“光晕”一词替代。
2. 读 [设计与配方](references/authoring.md)，将描述转成层表：形状/颜色、半径/线宽、位置/朝向、动画秒数、前后层关系和显示场景。先保证主体可辨，再加高频刻度；预设不是允许风格的白名单。
3. 用 [author_halo.py](scripts/author_halo.py) 生成透明 PNG、配方、渲染契约、固定时间与 16/32 像素预览。面向 16–24px 小图时先选 [小尺寸专用配方](references/small-icons.md)，减少密集环段/射线、增加暗间隔；`--display-px` 仅生成指定大小预览，不自动换配方或实现游戏 LOD。超出 glow/ring/rays 的图案可扩展生成器或采用原创纹理；特定符文、徽记、插画需另制资源，不把未实现字段当作有效配置。
4. 落地 MOD 时读 [Forge 接入](references/forge-1.20.1.md)，检查目标版本、loader、顶点格式和调用链。配方是本工具的制作记录，**没有随附通用 Minecraft JSON/NBT parser 或可安装 JAR**；必须实现配置选择和 renderer 才算接入。
5. 复用参考时读 [来源审查](references/sources.md)，核对混合、draw 顺序及 caller。不要按 GlowRenderType 名称猜 GL factors。
6. 按 [验证](references/validation.md) 检查素材、动画、透明合成、主体遮挡和所需场景。交付预览、复跑命令、实际改动与证据。用户只要 skill/研究时不擅自安装 MOD 或启动实例；已有明确运行授权则完成对应测试。

## 不变量

- Halo 光片、表面自发光、屏幕 bloom/场景照明是不同管线。此技能制作前者，不自动照亮环境或提取任意模型轮廓。
- 在已解析模型与正确变换中添加装饰；保留 overrides、弓动作、左右手、原 render passes 与 glint。自定义/骨骼/穿戴模型需专用入口，不重建成 generated 壳。
- PNG 是 straight-alpha、RGB 已带色、alpha 存覆盖；顶点默认白色，避免重复染色。alpha/additive 与实际 shader 输出、混合方程和深度写入成对设置。
- 以单调时间或 game ticks + partial tick 计算绝对相位，明确暂停策略。同帧多 pass 使用同一时间；不以每帧累加或每次 render 随机缩放代替稳定呼吸。
- 颜色/alpha/变换可随顶点保存；uniform 需实际 draw 时绑定或分组。缓存键不包含逐帧时间，flush 有边界，嵌套与异常路径恢复上下文。
- GUI 背层应能被主体遮住；世界软光通常测深度而不写深度。加法合成不意味着关闭深度。穿墙展示只用于明确要求的场景。
- CPU 预览不证明 Forge、Oculus/Iris、穿戴或任意 MOD 兼容。调成本同时检查小图视觉，不只数层数。

## 随附资源

- [青色呼吸](assets/presets/cyan-breath.json)、[金色双旋环](assets/presets/gold-orbit.json)、[红色放射](assets/presets/crimson-rays.json)：可任意修改 HEX、结构与节奏。
- [小图金色双环](assets/presets/gold-orbit-small.json)、[小图红色六束射线](assets/presets/crimson-rays-small.json)：16–24px 起点；有独立负空间和更低角向频率，大图配方保持可选。
- [素材与动画生成器](scripts/author_halo.py)：Python 3.10+、Pillow；无网络和游戏修改，拒绝覆盖既有输出目录。
- [行为检查](scripts/verify_authoring.py)：检查周期、方向、透明轮廓、混合和输出保护，使用临时目录，不启动游戏。
- [小图对比](scripts/compare_small.py)：原生 16/24/32px 前后对照，附 120 个 16px 动画采样的分离度记录。

生成结果放目标工程或独立目录，不在已安装 skill 内构建 MOD。
