---
name: minecraft-water-ripples
description: 从自然语言制作 Minecraft 高度场水波、落水涟漪、雨滴干涉和浅水回波，提供共享参数调试网页、预设、两种波动求解器和 Forge 1.20.1 可构建工程。用于可调式水面特效；不把二维波动系统当作完整流体、真实世界折射或焦散。
---

# 可调水波特效

将需求转换成共享 recipe.json，用工作台观察传播、衰减、干涉和材质，再生成 Forge 1.20.1 / Java 17 工程。附带模板是独立水面补片，并不自动替换原版所有水方块。

## 生成与调参

- 运行 `node scripts/author.cjs --out <新目录> --preset rain`。预设可选 default、rain、impact、shallow、magic。用 `--recipe <JSON路径>` 精确传入参数；两者同时指定时 JSON 覆盖预设。
- 生成目录的 `workbench/index.html` 可直接打开。若环境需要 HTTP，运行 `node workbench/serve.cjs 8766`，访问 localhost。优先给用户展示工作台，并根据其描述改半径、强度、传播速度、衰减、法线和色彩。网页可以导入和导出同一参数格式。
- 导出的文件放在目标实例 `config/waterripple/recipe.json`。`/waterripple demo` 在玩家脚下创建水面；`drop` 注入中心波纹；`rain` 切换连续雨滴；`reload` 重读配置并重建网格；`off` 清除。
- 生成脚本只复制工程和写配置，不启动游戏、不自动向实例安装 JAR。实例启动和安装由当前用户任务决定。

参数含义与数值边界见 [parameters.md](references/parameters.md)。实现来源和三项目差异见 [research.md](references/research.md)。需要接入自己的物品、粒子或技能时读 [forge.md](references/forge.md)。

## 实现约束

- 20 Hz 客户端 tick 内做三个子步，固定 60 Hz 模拟；帧渲染仅插值。不要跟随渲染 FPS 改传播速度。
- velocity 模式保存高度与速度；history 模式保存两时刻高度。切模式须重建，不能把已有速度当成上一高度。速度系数限定 0.1..1，超出需要重新推导数值稳定条件。
- 长度使用 Minecraft 格。半径先按 `(grid-1)/width` 换到网格单位，网格分辨率会改变物理传播速度。需要指定“格/秒”时先根据宽度、分辨率与子步频率换算，不承诺分辨率无关的速度。
- 使用带吸收层或复制邻近边界的反射模式；正负高度可干涉。振幅限幅改变线性叠加行为，故测试干涉应在限幅未触发的区间。
- 客户端专用渲染，订阅器限制 `Dist.CLIENT`；ShaderInstance 由 RegisterShadersEvent 重建；独立缓冲立即完成该水面的 batch，防止不同参数串用。
- 水面透明且深度测试开启、仅写颜色；它是独立平面网格。原版水面附近应略微抬高，过大负振幅会穿进原版表面而被遮挡。不要宣称实现场景折射、SSR、反射地形或世界焦散。
- 网页是参数与算法预览，不能替代 Minecraft 截图验证；着色器包及半透明排序兼容性需要目标实例实测。

## 验证与交付

运行 `node workbench/check-core.cjs`，然后用 JDK 17 执行 `gradlew build`。Windows Unix socket 路径过长时可设置 `JAVA_TOOL_OPTIONS=-Djdk.net.unixdomain.tmpdir=<短的可写目录>`。勿更改用户全局 Java 配置。

若改了网页或求解器，检查预设、点击/拖动、暂停、清空、两模式、边界、JSON 导入导出以及 Java/JS 数值一致性。运行测试覆盖传播、衰减、正负干涉和限幅稳定性；说明构建、网页与游戏实测各自状态。交付参数、源码、JAR和工作台路径。
