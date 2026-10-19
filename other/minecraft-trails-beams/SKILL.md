---
name: minecraft-trails-beams
description: 从自然语言制作 Minecraft 武器拖尾、刀光、轨迹残影、分叉能量束和多层光带。附离线 HTML 工作台、七种可编辑起点、严格配方与路径 JSON、原创几何内核、Forge 1.20.1 / Java 17 参考工程及验证。支持真实双挂点适配、任意路径、宽度色带、自定义纹理；不自动适配全部骨骼武器。
---

# 武器拖尾与能量束

默认目标 **Minecraft Forge 1.20.1、Java 17**。从用户的视觉描述决定路径和截面，再组织材质与时间；预设不是风格白名单。用户不必填写参数，先给可见初稿，随后按反馈调整。内部星空、Halo、彩色 glint 保留独立作用，不把动作轨迹变成物品换色。

## 制作流程

1. 阅读 [自由设计](references/authoring.md)，确定历史轨迹/即时束、单点/刀刃双挂点、空间和触发、主形、色带、纹理、动态与遮挡。缺省做合理初稿；只有改变接入范围的歧义才询问。
2. 打开 [离线 HTML 工作台](assets/workbench/index.html)，按 [工作台指南](references/workbench.md)制作可见初稿。七个起点仅供快速选型；改路径、截面、分叉、层、色带、宽度曲线、图案和时间，再导出 `recipe.json`、`path.json`。画布是 Canvas 近似图，实机结果须另验。
3. 阅读 [配方契约](references/recipe.md)与[路径契约](references/path.md)。JSON 字段由 Forge 示例真实解析；超出字段时扩展内核或 shader，不能写无人读取的配置冒充生效。
4. 用 [生成器](scripts/author_effect.py)的 `--recipe` 与 `--path` 从任意设计生成独立 Forge 工程。已有项目只移植所需类和资源，不替换工程结构。
5. 按 [Forge 接入](references/forge-1.20.1.md) 对接真实挂点和动作，区分示例运动与武器自身运动。模型、骨骼、第一人称和服务器触发都是可替换适配器，不强迫采用某种动作库。
6. 按 [验收](references/validation.md) 做 CPU 行为检查、Forge 构建和实际看图。已验证范围见 [当前证据](references/evidence.md)；不能继承其他 skill 的运行认证。

## 实施不变量

- **轨迹来自过去，光束来自当前路径。** 按模拟时间或固定频率采样，不能每个 render pass 增加一帧历史；停止发射后仍推进过期处理。
- 刀光保留刃根/刃尖两个真实挂点，中心线拖尾用单点。玩家位置偏移不能证明任意武器精确贴合。跨维度、瞬移、动作切换、持有者消失时断开或清理。
- 双精度世界位置保留到最后，再只减一次相机位置。点、相机和宽度单位一致；第一人称投影不能机械套世界投影。
- UV 按弧长，删除尾点保留累计偏移。宽度/色带与年龄淡出独立；路径点密度和纹理密度是不同参数。
- 重复点、零长度、视线平行、急转弯和突然反向有明确退化策略。管状束的基尽量连续；默认开口管不承诺任意折线无扭结。
- 透明效果通常测深度、不写深度；加法不等于穿墙。alpha/混合/输出配对。bloom 与场景照明是附加管线。
- 每 draw 绑定本层参数并闭合 flush；逐帧时间不进 RenderType 缓存键。重载刷新缓存，离开世界清理历史。
- 上限是资源预算，不是设计风格限制。需要新截面/更多层时扩展结构并测成本，不静默截断或强行套预设。

## 随附资源

- `assets/forge-1.20.1/`：Forge 47.4.10 完整参考工程、Gradle 8.8 wrapper、原创 Java 几何/历史、严格 JSON parser、GLSL、客户端演示、核心行为检查。无 Lodestone/Veil/Photon 依赖。
- `assets/workbench/index.html`：本地离线工作台；旋转、缩放、时间预览及设计导入导出。`recipe.json` 与 `path.json` 可供游戏示例读取。
- `scripts/author_effect.py`：校验并生成新目录，拒绝覆盖工程；只写文件，不自动安装/启动游戏。
- `scripts/verify_authoring.py`：检查自定义设计、输入拒绝和输出保护，不启动游戏。
- `scripts/verify_workbench.cjs`：可选 Playwright 浏览器回归，检查七种预设、编辑、导出与画布。
- `scripts/verify_runtime.py`：检查已保存的实机截图和记录，需 Pillow；不代替实际看图。
- `assets/presets/`：三份基础配方；HTML 中另有霜蓝、棱彩、螺旋、熔火、紫电、符文和分叉雷束七种起点。第三展示槽可加载配方和路径；任意真实武器的刃根/刃尖仍由适配器提供。

来源和迁移边界见 [sources.md](references/sources.md)。代码和纹理为独立实现，不打包参考 MOD 实现。构建/证据输出到工作目录，不在已安装 skill 内运行 Gradle。

修复第一人称飞行拖尾或速度流时，读 [第一人称分层](references/first-person-layers.md)，分别处理边缘流、世界历史轨迹与中心主体。
