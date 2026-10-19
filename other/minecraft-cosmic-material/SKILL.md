---
name: minecraft-cosmic-material
description: 从自然语言制作 Minecraft 物品、穿戴防具和盾牌的 Cosmic 与奇幻材质，涵盖内部星空及多种奇幻质感，提供原创 GLSL、盾牌预设工作台、Forge 1.20.1 接入与验证方法。不用于普通天空盒。
---

# Minecraft Cosmic 与奇幻物品材质

把 Cosmic 作为附着在物品几何上的材质系统：**几何与遮罩限制覆盖范围，效果坐标生成内部宇宙，渲染适配器负责绘制。** 改造已有物品时保留它的模型状态、动作、显示变换和原有渲染行为。

参考依据来自五份源码快照：1.18.2 Cosmic/Halo 示例、Re-Avaritia Forge 1.20.1、NeoForge 1.21.1、Avaritia-Render 片段和 RenderBlender。原项目仅做静态分析；另行提炼的 Cosmic Material Lab 已于 2026-09-28 在 Forge 1.20.1 / 47.4.10 启动器环境完成真实物品渲染、满弓和资源重载实测。两类证据分开记录，不把天空实验或少量样本扩大为全物品兼容。

后续增加了用户提供的 ArcaneVortex 0.6.8 着色器方块研究，以及原创的内部星空制作台。它们补充材质创作方法，不扩大上述 Forge 运行认证。原 JAR 的许可和独立片元出图边界见 [arcanevortex-study.md](references/arcanevortex-study.md)。

## 用户用文字描述效果时

用户不需要填写 shader 参数。把描述转成“内部是什么空间、主形/留黑、发光与遮挡层、观察响应、动态节奏、覆盖区域”，按 [material-authoring.md](references/material-authoring.md) 决定核心算法。保留参考风格的要求优先；不要让所有主题都变成同一组噪声换色。

- 深邃星空、近星远星、星云暗尘：读制作方法与 [配方及词汇映射](references/material-recipes.md)。
- 星点需要移动或闪烁：读 [星点动态与验收](references/authoring-workbench.md#星点动态与验收)，独立控制星体输运和亮度包络。关闭星云后跟踪星点、关闭漂移后验证原地闪烁；用随包 `validate_star_motion.cjs` 保留连续片段，不能用星云变化代替星点动态。
- 统一工坊使用 `serve_authoring.py --lab fantasy`：包含十四种奇幻材质及原有三种内部星空，类别切换保留编辑状态。`?preset=aurora-veil` 等有效 ID 可直接选择材质。两类配方格式与 Forge 接入边界仍分别处理，见 [奇幻材质制作](references/fantasy-materials.md)。
- 水波、清潭、风浪、波峰泡沫：读 [水波材质](references/water-material.md)，使用 `tidal-water / mode 12`。波形、解析法线和光学共用相位，九个水面字段（含不透明度和光照位置）须在预览、资源包与 Forge 中完整传递；不把它称作 FFT 海洋或真实场景反射。
- 电视雪花、CRT、VHS 抖动或模拟信号噪声：读 [电视雪花材质研究](references/tv-snow-material.md)，使用 `crt-static / mode 13`。当前预设输出黑白二值雪花和不规则逐像素换帧，不读取视频、不模拟真实解码器，也不把信号雪花扩展成屏幕后处理。
- 用户希望跳出星空、制作不同质感：读 [奇幻材质制作](references/fantasy-materials.md)，使用 `assets/fantasy-lab` 的独立算法及 `scripts/validate_fantasy.cjs`。这些是创作起点，用户描述超出其结构时继续新增算法。
- 极光幕、雷晶放电、上浮泡壳、机械机芯或生物输光：对应 mode 7–11。先读奇幻材质中的结构与动态契约，分别改幕面、弧路、球壳、齿轮或分支；不能统一加噪声换色。
- 用户强调 FantasyBlock 那种内部翻卷与纵深流动：先读 [内部流动](references/internal-flow.md)，使用 `fantasy-flow / mode 6`；表面法线、UV 漂移与整体提速不能代替其共享视点和三维云壁。参考真实时钟要包括 renderer 的时间倍率。
- 用户指出方块像六面复制：检查内部采样是否依赖逐面 UV。FantasyBlock 式窗口使用共享屏幕射线，固定时间旋转原生方块，与完整窗口逐像素比较；随包 `validate_flow_continuity.py` 保留零色差判据。不要把此方法宣传为物体局部实体体积。
- 方块内的分形、折叠云层或有限星云：读 [ArcaneVortex 研究](references/arcanevortex-study.md)，先核对实际 renderer 与 shader 绑定。
- 需要可看、可调的材质初稿：使用 [原创制作台](references/authoring-workbench.md)；它实际支持的字段和未实现的效果有明确边界。
- 制作台启动读取实际分配的端口；复跑使用随包 `scripts/validate_preview.cjs`，核验服务身份并保留冻结零容差。异常像素不能未经诊断归因于 GPU 舍入或放宽为通过。
- 用户只是要求学习/完善 skill：交付方法、证据与可复用资源；用户要求落地物品时再进入目标工程接入和游戏验证。既有用户授权不必重复询问。

交付初稿时附可辨认的视觉结果，固定 time/seed 的版本对照，以及大图与实际小图。仅写“紫蓝、16 层、慢速”不构成完成材质制作。原生 shader 参数不足时补接口；不要把设计记录冒充已经生效的 JSON/NBT。

用户重视动态流动时，先确定输运路径、形变、前后遮挡和保持静止的实体部分。提供原速连续片段及时间对照，使用随包 `record_fantasy_motion.cjs`；单张截图或“过几秒像素改变”不证明动态质量。检查帧率上限、沿射线采样条纹与暂停/配方时间一致性。详见奇幻材质的动态制作章节。

Forge高分辨率动态与跨面冻结是不同验收：`flow-continuity-hd` 固定时间检查接缝，`flow-motion-hd` 固定几何并记录真实游戏时钟的连续变化。动态证据用随包 `validate_flow_motion.py` 校验，不能把冻结测试叫作动态实测。

## 工作方式

先读取目标工程版本、加载器、Java、mappings、已有模型与渲染入口。研究请求交付证据和方案；实施请求才修改目标工程。以用户选择的版本为准，不能把 Forge 1.20.1、NeoForge 1.21.1 或后续版本 API 混用。

1. 判断目标是二维 generated/handheld、三维 baked model、BEWLR/动态模型，还是穿戴模型。按 [integration.md](references/integration.md) 选择适配器；已有自定义 loader 不可简单覆盖。
2. 区分两种任务：忠实复现时保留参考的视觉机制；自由设计时按材质制作方法确定内部结构，再使用 [design.md](references/design.md) 对接覆盖区域、模型、状态与成本。明确哪些参数已有实现，哪些需要新增 shader/Java/JSON 接口。
3. 实现前读 [algorithm.md](references/algorithm.md)：不要把物品 UV 当作宇宙方向，不要把 `mask.r` 当成 `mask.a`，不要把 10 张 sprite 与 16 个效果层混为一谈。
4. 闭合 `模型解析 → 实际绘制入口 → shader 实例 → sampler/参数 → 顶点 → flush → framebuffer`。版本特例和快照缺陷见 [sources.md](references/sources.md)。
5. 根据覆盖范围使用 [validation.md](references/validation.md) 验收。交付已支持的物品类别及未验证边界，不能以一把剑成功承诺所有物品兼容。

实施 Forge 1.20.1 的普通 baked items 时，优先读 [已实测接入路径](references/forge-1.20.1-runtime.md)：它提供原 quads 单 pass、最终 override 包装、draw 时参数绑定、有效 NBT 和本地可复跑工程位置。穿戴防具和原版盾牌读 [装备适配与实测](references/forge-1.20.1-equipment.md)：分别接 `HumanoidArmorLayer` 与原版盾牌 BEWLR，并提供保留金属边框预设及 HTML 工作台。第三方自定义 renderer 和骨骼动画仍需各自适配器，不能强行套入 baked wrapper。

## 实施不变量

物品描边需要可视化调参时，先区分用途：`assets/outline-lab/index.html` 是支持透明 PNG、配方往返与导出的二维配色草图，见 [描边工作台](references/item-outline-workbench.md)；真实八角几何与模型空间宽度使用 Forge 1.20.1 的 `/cosmicmaterial outline` 游戏内界面，见 [描边实测](references/item-outline-runtime.md)。两者的宽度单位和颜色函数不同，浏览器配方不直接驱动 Forge。

制作 ArcaneVortex 式物品勾边/描边时，读 [物品描边研究](references/item-outline-study.md)：八方向原几何重绘负责轮廓，shader 负责边内材质。原创 Forge 实验已在六种普通 baked 物品及十个场景跑通核心几何方法，但没有与原 JAR 同场景对照，也未实现原屏幕折射模式；范围和证据见 [描边实测](references/item-outline-runtime.md)。不要把它等同于 Halo、屏幕边缘检测或固定像素宽度。

需要物品内真实场景、镜面、选择性 bloom、动态光或动作拖尾时，读 [渲染框架研究](references/render-frameworks-study.md)。它区分单次离屏视图与递归门户、发光与照明，并记录四份 1.21.1 源码快照的迁移边界；普通 Cosmic 不必引入完整世界渲染。

设计涉及 Halo、玻璃边缘、黑洞、折射或多 pass 时，按 [六份参考的进阶研究](references/advanced-effects-study.md) 选择模块，并核对场景输入、状态生命周期和专用验收；这些新增静态方法不继承已有 Forge 基线的运行认证。

- 为遮罩与星体坐标建立不同契约。参考实现共用 block atlas 的 Sampler0，既采样 mask 又采样星体；如果拆成独立 sampler，要同步修改绑定和 UV 来源。
- 三维物品优先复用原几何，重映射遮罩 UV；不能把 `ItemModelGenerator.processFrames` 生成的平面壳当成任意模型的覆盖层。
- 每次实际 draw 使用与该物品一致的材质参数。共享 shader uniform 不随缓冲顶点自动保存；flush、状态分组或参数随顶点传递需择一实现。先保证正确，再减少 draw call。
- RenderType、ShaderInstance 注册格式、真实 VertexConsumer 输出格式必须一致；重载替换 shader 及 uniform 句柄，并重新获取 sprite UV。
- 参考物品层的 EQUAL 深度测试依赖基础几何先写深度且完全对齐；改用 LEQUAL、偏移或透明材质时重新验证遮挡，不能靠禁用深度消除问题。
- 明确 GUI 与世界方向策略、时间单位及暂停行为。参考的玩家 yaw/pitch 和 GUI scale=100 是特定实现选择；新实现使用实际相机/投影或明确的物体局部空间，避免重复应用视图旋转。
- 纹理资源包只能配置已存在的 loader/shader 能力；纯资源包不能凭空注册这套 Java 渲染系统。NeoForge 1.21.1 此案例仍是 `models/item` 管线，不能套用 1.21.4+ 的 item definition 格式。

技能提供决策、设计方法和经过实测的工程入口；JAR 与参考素材保留在独立实验工程并附来源许可，不作为“全物品通用包”内嵌在技能里。需要源码细节时依照运行说明或来源相对路径定位，缺少工程时先获取资料，不编造运行结果。

