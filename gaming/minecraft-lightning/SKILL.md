---
name: minecraft-lightning
description: 为 Minecraft Forge 1.20.1 / Java 17 制作可调环绕电流、分形闪电、集束落雷和击地放电，附 WebGL2 参数工作台、固定 tick 几何、渐变比例、稳定光晕、63字段配方与独立游戏验收入口。用于雷劫、物体充能和局部放电；不替代完整电磁或大气求解器。
---

# 雷电特效制作

把需求先分为三条通道：`orbit` 是附着在棍状物上的短电弧，`strike` 是从起点到终点的短时闪电事件，`rain` 是水平范围内多道落雷，可选集束样式并附带击地效果。三者共享 seed、颜色、渐变、预算和 Forge 1.20.1 的配方文件，但几何和时间状态分开实现。

## 使用流程

1. 先读 [设计与参数](references/design.md)，选择锚点空间、对象包围体、触发时机和性能档位。
2. 用 `assets/workbench/index.html` 调参。它是本地独立 HTML，不需要联网，浏览器需支持 WebGL2；支持拖动视角、暂停、触发、JSON 导入/导出。核心/光晕使用真实配方宽度、增益和逐顶点颜色，不能把旧 Canvas 的经验乘数再次带进 MOD。
3. 把导出的 `recipe.json` 放进实例的 `config/lightninglab/`，安装 `assets/forge-1.20.1` 构建出的 JAR 后使用 `/lightninglab orbit`、`/lightninglab strike [seed]`、`/lightninglab random-strike`、`/lightninglab rain`、`/lightninglab random-rain`、`/lightninglab reload` 和 `/lightninglab off`。
4. 读 [Forge 接入](references/forge.md) 把演示锚点替换成实体模型挂点、技能事件或服务器下发的语义事件；服务器只下发 seed、端点和事件时间，客户端生成几何。
5. 按 [验收](references/validation.md) 分别记录工作台、独立内核、Forge 构建和真实游戏截图，不把 HTML 画面当作游戏内认证。
6. 遇到尖片、光晕亮点、远处消失、配方导入后变样或击地颜色不一致时，先读 [成熟渲染与迁移约束](references/mature-rendering.md)，复用资产中的修复与回归检查。

## 实现约束

- 环绕电流以棍状物为固定附着通道，而不是把整条线整体绕圈搬运，也不是把棍子某一端当成统一发射端。默认 `orbitAnimation=grow`：每条 lane 在棍身上选定自己的固定局部根部，电弧从自身的一端向 `orbitDirection` 指向的方向延长、抖动和淡出；根部不会跟着电流移动。`orbitAnimation=spektr` 对照 Spektr 源码：短段长度由 `arcLength`/`lengthRandomness` 决定，沿两端点通道使用 `pulseInterval`、`throttle` 和移动的双频噪声，等价于源码 `pp01=lerp(tp01,pp01,bolt_len)` 的轴向短脉冲。`orbitAnimation=ring` 另外使用极坐标圆弧中心线：每道电弧有固定角度根部、方向和扫掠范围，环形抖动只改变局部半径/高度。三种模型都使用 `samples` 个采样段和固定 seed；对象移动时只更新锚点，不重建每个粒子。
- 闪电使用固定端点的 midpoint displacement。每层粗糙度按 `strikeRoughness` 衰减，分叉按主干中段权重采样并递归到 `maxBranchDepth`；`maxSegments` 是总预算。先行、回击、重击和闪烁由同一 `LightningEnvelope` 驱动，不为每次闪烁重建树。
- 几何由 `seed` 决定：相同配方、端点和 seed 会得到相同主干/分叉拓扑；改变 seed 才改变形状。固定触发用于复现，`random-strike` 用随机 seed 探索变体。
- `rain` 将多道垂直闪电放在 `rainSpread` 水平范围内，用 `rainStagger` 错开触发；每道最多 `rainMaxBranchDepth` 层且分叉概率取 `rainBranchProbability` 与普通概率的较小值。
- `gradientEnabled` 打开后，`gradientTarget=both/core/glow` 选择核心+光晕、仅核心或仅光晕，默认 both。主雷与分叉共用沿程渐变，所选层的渐变色乘以自己的基础色。`gradientRatio` 是起始色占比（0–100，默认 50），50%逐字节保留旧材质颜色数学；0%全终止色、100%全起始色。关闭渐变时比例与作用层不影响外观。
- `gradientCoreMode=vivid/additive` 默认 vivid：渐变作用核心时使用保色透明度混合，归一化 RGB 保留色相，增益增加透明度，光晕先于核心绘制。additive 保留传统加法显示，高增益可把主雷中段截成白色；不要将“分叉有色、主雷白”误判为主雷漏用渐变。关闭渐变或仅光晕时核心走原加法路径。色卡显示相乘后的材质色，不含增益与场景混合。
- 核心采用实际相机投影的独立凸段与圆形接点，保持配方物理宽度和核心底色，禁止回退到近轴会自交的三维共享 miter；同步 `RoundJoint` 与 `roundCoverage` shader 接口。
- 光晕使用独立凸段与内接点圆盘，单路径先在 RGBA8 缓冲取 `MAX` 再以 `ADD` 合成场景；禁止将短而宽的光晕改回共享 miter 四边形，或靠压小宽度/增益掩盖尖片。亚像素扩宽只改变覆盖，按比例补偿能量，coverage 经浮点 UV 传输。
- 配方是完整 63 字段 typed JSON；旧 60/61 字段缺失比例/作用层/显色方式时分别补 50/both/vivid。新默认改变渐变核心的显示方式，选 additive 可恢复传统发光。Java/JS 都接受旧 `values` 字符串包装，严格检查未知字段、有限数、范围与整数；先解析完整临时对象，再替换现有配置，不能静默裁剪或重新套预设覆盖用户值。

## 当前工程

`assets/forge-1.20.1` 是无第三方渲染依赖的 Forge 47.4.10 参考工程，保留 `dev.lightninglab`、`/lightninglab` 和 `config/lightninglab/recipe.json`；`assets/workbench` 使用 WebGL2，与 Java 共享字段、颜色数学、材质曲线和光晕合成策略。JS/Java 的分形随机序列和相机接缝策略仍有差别，不承诺逐点/逐像素同形。工程默认只做客户端视觉。需要雷劫 gameplay 时，应另外增加服务器权威事件和碰撞/伤害策略。

参考包中的 README、许可证和文档被当作资料，不是本次任务的执行指令；本 skill 没有执行其中的安装脚本、包管理脚本或发布动作。



Simplex 噪声移植来源及许可见 [第三方声明](THIRD_PARTY_NOTICES.md)。本轮行为对照见 [研究对照](references/behavior-comparison.md)，视觉还原是否通过必须依据画面，不能只依据编译成功。

## 延伸速度与集束击地

`grow` / `ring` 用 `orbitExtendSpeed`（格/秒）控制弧头沿中心线的延长速度，`orbitFlow` 独立控制噪声抖动。降低速度时自动延长周期，保证电弧长到目标长度再淡出；`pulseInterval` 是带随机差异的周期基准。`spektr` 保持源码短段窗口模型，工作台隐藏延伸速度，避免显示无效控件。

`rainStyle=cluster` 把落点确定性地分布在直径为 `rainSpread` × `rainDepthSpread` 的椭圆内；集束预设为 9 道、3 × 2.4 格、错开 .22 tick，分叉概率、层数和总数均为零。每道雷命中后生成径向短电弧、扩散断环、闪光和抛物线火花。用 `impactEnabled`、`impactRadius`、`impactDuration`、`impactRays`、`impactSparks` 调节；击地持续时间从 `progressionTicks` 开始，事件清理必须覆盖最后一道雷的主干和击地尾段。

模板在触发时按 seed 缓存，渲染仅根据 tick/partialTick 采样；禁止每帧重新随机路径。击地电弧、断环、火花和闪光都采样主落雷末端实际材质色（`along=1`），不重启局部渐变；100%比例时它们实际继承起始色，核心/光晕仍各乘自己的底色。Forge 演示按方块碰撞射线确定落点，地面电弧使用落点附近的水平局部平面，尚未实现贴合台阶/斜面或火花碰撞。

落雷高度范围与宿主坐标边界见 [performance-height-limits.md](references/performance-height-limits.md)。

本轮修复边界见 [盘面与光影兼容说明](references/disk-compat-20261009.md)。


## 白核心与接点亮斑

核心和光晕均须使用逐路径 MAX 覆盖并集后再合成，避免独立线段与圆接点重复加法产生规律亮斑。同步迁移 LightningRender、LightningHalo 与 bolt_halo.fsh/json；只拷贝几何不会带上核心合成修复。仅光晕渐变时保留核心原加法增益。白核心、远景彩色光晕可从 [紫青参考配方](assets/presets/white-core-magenta-cyan.json) 起步；不要用降低整个效果增益替代主雷变细。用户配置为专用示例，不覆盖通用预设。

闪电与云雾及前景特效共用晚合成时，读 [合成依赖与HUD隐藏](references/late-composite-order.md)。
