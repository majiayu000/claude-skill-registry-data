---
name: minecraft-energy-vfx
description: 从自然语言或 energy-vfx/2 配方编辑并接入 Minecraft Forge 1.20.1 三维能量、幽气和白蓝烟纱特效。提供 48 个参数、20 个可编辑起点、共用 GLSL、严格 v1 升级、实际 ModelPart 与 baked 装备表面发散及固定文件命令桥。用于持续离体气团、冷焰、薄雾、卷曲细丝、蓄力爆发与局部 Bloom；不是资料台或网格流体求解器。
---

# 能量特效编辑与游戏接入

当前运行版本 v0.2.5，配方为 `energy-vfx/2`。交付实际可编辑效果与消费配方的运行代码。用户已给出配方时以其数值为准；工作台 `current-recipe.json` 比默认起点更优先。精确含原 39 字段的 v1 配方校验后升级，残缺 v2 不升级。

## 操作路径

1. 确认 Forge 1.20.1 / Java 17，读取实际目标项目或启动器游戏目录。此模板目标为 Forge 47.4.10；具体通过范围看 validation.md。用户指定现有物品、实体或技能时保留原动作、世界坐标和挂点。
2. 运行 `scripts/validate_recipe.py <recipe.json>`。v2 必须精确 48 字段，v1 必须精确原 39 字段。未知、缺失、布尔数值、非有限值、范围和整数错误均拒绝，保留上次有效配方。
3. 运行 `scripts/preview.py --port 8796` 打开实时 WebGL2 编辑器。也可离线打开 `assets/lab/index.html`；离线用导出，服务模式可保存当前配方。20 个预设均为可修改起点，包括蓝色幽气、冷焰、薄雾及透明白/蓝卷烟。
4. 独立示例运行 `scripts/scaffold.py --out <新目录> --recipe <recipe.json>`，设置 Java 17 后运行 `gradlew.bat build`。输出生产 JAR 与完整资源。
5. 已授权安装时运行 `scripts/apply_recipe.py --recipe <recipe.json> --game-dir <实际游戏目录> --install-runtime`，安装 `energyvfx-0.2.3.jar` 后重启实例。仅更新运行库时可省略 --recipe，保留用户参数。原文件备份，已知 v0.1.0/v0.2.0/v0.2.1/v0.2.2 JAR 移到固定备份目录以避免重复 mod ID。
6. 已运行 v0.2.3 时加 `--reload`，脚本只写固定 `command.json` 并等待同 nonce 的 `result.json`，根据 `ok` 与实际 status 判断执行。可用 `--action start/off/status`，或 `--action preset --preset 1..20`。命令桥不控制相机、物品栏或服务器命令；继续保持 MCP-HELPER `control_mode=false`。详见 [integration.md](references/integration.md)。
7. 玩家发散选择 attachment=1，装备=2，两者=3；有 32 个三维气团预算。通常保留较低 firstPerson，检查真实装备来源与 fallback 计数。目标 BEWLR/GeckoLib 或非标准盔甲需专用适配，不把挂点 fallback 宣称为完整表面覆盖。
8. 需要修改 GLSL 时同步网页内嵌源码与 Forge 资源并重新构建。打包前核对源码、Forge 资源和 JAR 内六份共用 GLSL 与原生 flow-cache.glsl 的 SHA-256，拒绝把旧 JAR 与新编辑器组合交付。目标技能入口按 integration.md 接入；不能把单个本地玩家效果宣称为已完成多人技能同步。
9. 分别记录网页、构建、独立游戏 QA 与用户实例测试。计数证明代码执行，截图才用于外观检查；第一人称低自身强度分支计数不能证明手部外观。原生客户端通过不代表 Oculus 或其他渲染管线通过。

## 实际实现与边界

- 原创三维密度场和包围盒光线积分；`psrdnoise3.glsl` 来自 Stefan Gustavson / Ian McEwan，保留完整 MIT 许可。
- 旋转梯度噪声、导数域扭曲、径向/上升流、双等值带细丝、侵蚀、核心及环密度，都在实际三维坐标中求值。
- 空间模式包含球、环、涡柱和束；持续发散模式从实际动作中的 ModelPart 表面、盔甲模型及普通持有物品 baked quads 出生，保留渲染与物品显示变换。每包以固定 20 Hz、RK2 在世界坐标独立漂移，内部沿不同轴和相位的局部 curl 场以 RK2 回溯坐标，产生烟纱折叠。
- 烟纱以局部近似 signed distance 求 Gaussian 薄层，对段内线性变化的距离作误差函数解析积分；该路径没有像素 jitter 或 3×3 屏幕模糊。起点 15/16 默认 resolution=1、steps=128，换算为每气团 64 个积分段。shellWidth/sharpness 控制局部宽度，经拉伸与回溯后不保证世界厚度严格恒定。
- 网页人物是观察用代理模型。Forge 记录实际 surfaceTriangles、equippedSlots、renderedPose、bakedItems 与 fallbackItems；任意自定义动态装备需要专用表面提供器。
- 32 包为容量上限，puffRate × puffLife 接近 32 时避免继续叠加生成率和寿命。bodyWeight/gearWeight 控制两类来源强度，inertia 控制运动继承，firstPerson 控制第一人称自身雾强度。
- 生命周期驱动密度、尺度与侵蚀；固定种子和时间支持确定性重放。局部 curl 与坐标回溯不等于完整流体求解；整个程序场的运动不保证不可压缩，也不是 Navier–Stokes 模拟。
- RGBA16F 分离体积和 emission，分离模糊 Bloom，采样独立场景副本做扰动；主深度只读。背景在全分辨率合成，特效曝光不修改远离特效的世界颜色。
- v0.2.2 使用保守屏幕区域与场景复制、流向椭球空段跳过及 uniform 缓存；近裁剪面交叉回退全屏，Bloom=0 跳过模糊。不会自动降低用户 resolution/steps、气团数量或内部运动。性能诊断须显式启用，生产运行不发 GPU 计时 query。数据和同帧对照见 [performance.md](references/performance.md)。
- v0.2.2 在 OpenGL 4.3+ 缓存每帧、六个 RK2 时刻的解析涡旋轴/转速，使用 RGBA32F 精确 texelFetch；不插值烟雾密度或时间。超出缓存范围或不支持计算着色器时回退原公式。GPU cache 的内存读写设 barrier，并恢复 image unit 与纹理数组绑定；原生专用 flow-cache.glsl 也需核对资源/JAR 哈希。
- v0.2.3 为每个气团的流向椭球支撑范围计算保守屏幕投影；完全位于相机后方的包不扩大绘制区域，跨越透视奇点的边按保守极限处理，退化投影回退全屏。片元进入密度求值前先排除不覆盖该像素的包。Bloom 区域留出模糊核和随体积目标比例缩放的线性采样边距，避免低 resolution 下切掉薄烟或光晕边缘。这条裁剪路径保持原积分与烟量；验证范围见 [motion-performance.md](references/motion-performance.md)。
- 自身近距烟使用独立可见性预算：手持装备优先，身体/盔甲按稳定出生序号选择子集，再对近眼范围平滑淡出，避免逐帧选择跳变。v0.2.3 将此策略扩展到本地玩家第三人称：相机到玩家眼睛距离 ≥3 米时完整绘制，≤1.8 米时使用出生时确定的子集与 nearFade，中间以 smoothstep 连续过渡。第一人称继续使用该近距策略。它有意改变自身近距外观；全部包的模拟、寿命与漂移不变。记录 uploadedPackets、firstPersonThinned、nearViewThinned、nearViewWeight、cameraDistanceMeters、nearEyeHidden/nearEyeFaded，不把模拟 packets 冒充全部可见，也不把此策略的收益称为同画质加速。v0.2.2 的第一人称历史对照见 [fullscreen-performance.md](references/fullscreen-performance.md)。
- 仍为单个客户端实例；`startAt(Vec3)` 是空间效果入口，AuraEmitter.bind 是玩家持续发散入口。多角色实例、服务端技能同步、命中判定与多人一致性由宿主项目实现。
- `resolution` 控制体积目标比例，`steps` 控制积分步数；不要承诺任意硬件 60 FPS。Fabulous 与改写主 target 的管线会拒绝执行，其他加速/着色器兼容性另验。

参数、单位与消费者见 [recipe.md](references/recipe.md)，具体拓展参考见 [ghost-sources.md](references/ghost-sources.md)。
- 第三人称拉近、积累后起步的性能判定与测试边界见 [third-person-zoom-performance.md](references/third-person-zoom-performance.md)。许可与已完成验证见 [validation.md](references/validation.md)。研究资料只作技术依据，交付以可编辑效果与实际游戏消费者为准。


## v0.2.5 第三人称拉近预算

第三人称背视角在连续积累后拉近到玩家身体或装备附近时，生产路径保留 32 个气团、resolution=1、steps=128 与完整内部运动；只对本地玩家低贡献烟包应用相机距离相关的连续裁剪：3.25 米开始、2 米达到更强的低贡献筛除，近距筛除与 nearFade 使用同一包序和流向椭球距离，避免逐帧随机跳选。该策略改变贴近镜头的烟量，不能称无画质损失。

验收必须使用单独的第三人称拉近序列，先积累 400 tick，再连续测量 4/2.5/1.5/0.75/4 米；不在阶段之间 reset、重绑或清空。已验证的隐藏 2560×1440 QA 记录见 [third-person-zoom-performance.md](references/third-person-zoom-performance.md) 和 `evidence/game/zoom-cull-run-2560/comparison.json`；该记录证明独立 VFX GPU 趋势，不代替用户实例的全屏总 FPS。

## v0.2.4 第三人称积累起步修正

第三人称静止积累后起步可能使相机穿过离体旧烟。运行时保留所有气团的模拟、生命周期和内部 curl，只对本地玩家缓存绘制包按实际相机到包中心的流向椭球距离做连续可见性淡出：普通第三人称 body 为 8–10 半径、gear 为 6–8 半径，并连续接回既有近眼 body 4–6、gear 2.8–4 策略。它是明确的近镜头外观取舍，不是等画质加速；不改 resolution、steps、容量或样点。独立第三人称积累起步证据见 `静止积累起步优化记录.md`，隐藏窗口测试不等同于用户现场 FPS。
