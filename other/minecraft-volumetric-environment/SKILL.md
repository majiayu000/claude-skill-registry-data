---
name: minecraft-volumetric-environment
description: 从自然语言制作 Minecraft 世界体积云雾、末地扭卷云与紫雾，附 Forge 1.20.1 基础后端；另含渡劫黑云、陆地龙卷、龙吸水与水龙卷的原创 WebGL 工作台。不用于天空极光、闪电枝条或物品气团。
---

# 世界体积环境

把需求转为世界区域、三维密度、光源与事件、深度和合成。云雾必须随世界位置改变；相机进入介质、转头或改变高度时继续有效。以真实深度限制有限射线，输出预乘辐射 `L` 和透射率 `T`，合成 `scene * T + L`。

## 制作与调参

沿用用户已给版本和工程。随附后端目标是 Minecraft 1.20.1 / Forge 47.4.22 / Java 17；其他版本先核对深度生产入口、矩阵和事件 API。

按需要阅读 [制作与配方](references/authoring.md)，从随附原创资产建立独立作品：

```text
python "<skill目录>/scripts/author.py" --out "<新目录>" --preset alien-storm --name 紫白风暴 --set flashStrength=12 --set surfaceGain=0.8
python "<新目录>/workbench/serve.py" --port 8774
```

使用本机 HTTP 地址打开基础工作台 `/`。六十二个参数、八个起点都是可编辑素材；按用户构图改区域、颜色、密度和风场，提供实际渲染的 PNG、JSON 与接入资源。基础配方为 `world-volume/2`，完整旧 /1 可显式升级并保持原五十值。导出的资源 ZIP 需要配套 Forge 渲染入口，单独启用资源包不会新增体积 pass。修改基础配方后把完整 JSON 放到工程 `run/config/world-volume.json`；目标实例使用它自身的 `config/world-volume.json`。

- 云海：有限高度云层，调整云底/厚度/覆盖率，检查云下、云内和俯瞰。
- 贴地雾：降低高度和密度，以地形遮挡和能见距离为主；距离着色只能作为补充。
- 异界风暴：环形区域与中心空洞、平流和域扭卷、间歇事件；雨雪及闪电几何按需接其他模块。
- 局部雾团：球形支撑、区域固定或显式随目标更新，不能悄悄锚定相机。
- Bliss 式末地云：读 [密度生成](references/bliss-end-density.md)，从 `end-vortex` 开始。先沿高度拉长噪声并按高度/秒数扭转，再减中心椭球与宽环槽，最后加下层雾；近相机清理由积分阶段单独限密度，不进入云影原始密度。
- AstraLex 紫雾：读 [复合分布](references/astralex-purple-fog.md)，把视线光雾、距离雾、极光背景与点星分开。`purple-light-fog` 借鉴世界亮度调制并用有限 Beer 介质独立实现；天空极光/战斗背景不随此预设自动实现。
- 渡劫黑云：读 [事件与旋涡工作台](references/event-workbenches.md)，打开 `/tribulation/`，调整形成时间、向心卷吸、旋转和劫云密度；用时间线检查碎云出现、连片增厚与后期闪光。
- 龙卷风、龙吸水或水龙卷：读 [事件与旋涡工作台](references/event-workbenches.md)，打开 `/vortex/`。`mode=0` 是陆地云漏斗；`mode=1` 从海面卷起连续水团和不规则侧片，保留上段云雾；`mode=2` 提高液体高度，并将上段展开为有内腔的薄壁碗口。先调实体半径与弯曲，再检查螺旋轮廓、根部卷入和顶部飞溅，最后调泡沫与透射。下段以小连续内核保持占据，由三层重叠薄水皮、局部翻卷片和飞溅构形；辅助缺口不裁下段内核，水龙卷顶部空腔则统一裁整组水场，避免旧尖顶堵口。它们与材质共用成熟高度的螺旋节距。使用“顶部碗口”视角检查近侧沿、内壁和远侧沿，保留用户原相机。水柱界面反透射共用细法线、Fresnel 和片缘局部泡沫，按有限水光程吸收调色，避免固定青色底色叠成粗光滑水柱。具体表面、运动和有限折射的分工见 [液体主体重做](references/research/vortex-waterspout-20261011/WATER_BODY_REVISION.md)。

迭代用户已有事件作品时先保留完整参数、相机和固定秒数，再载入新内核复核。

事件页导出 `vortex-cloud/1`、`tribulation-cloud/1`，包裹完整基础配方、对应事件字段和相机/时间；用各自页面导入。涡旋沿用 20 个事件字段，水柱使用周期周向坐标，海面使用有界双相位输运；固定秒数冻结形变与水纹。新密度、液体、水滴及水面尚未接入 Forge，事件作品 JSON 不能直接当基础游戏配置。

## 三种照明分别处理

读取 [渲染合同](references/render-contracts.md) 选择用户需要的效果：

1. `emission`：介质自身发光，不产生表面光源。
2. `mediumGain`：事件局部光进入云雾积分，范围衰减与介质透射独立。
3. `surfaceGain`：事件对可见表面的直接光。随附后端使用深度导数法线和介质遮光，没有地形对光源的遮挡或方块光传播。

共享事件由种子、周期和秒数确定；暂停时间冻结风和事件，固定时间重载可重放。不按渲染回调次数推进。不同客户端只有在种子、区域和时钟相同的条件下才同步；模板没有服务器同步协议。

## 接入与检查

为现有工程接入时读取 [Forge 接入](references/forge-1.20.1.md)。确认当前 renderer 与 shader pack 所有权；模板避让 Oculus/Embeddium，不将原生后端推广到未知管线。复制颜色/深度后再采样，不读正在写入的附件；保持深度和 GL 状态。CPU double 计算相对相机区域位置，再上传 float；射线眼点须考虑投影中走路 bob 的平移。

模板对最近不透明深度合成，不能从它推断水/玻璃的分层深度或类型。透明表面需要对应原绘制入口的额外适配。保留既有天空工作台；新世界环境不自动删除其共享云雾资产。

基础配方使用 `python "<作品>/scripts/recipe.py" validate "<作品>/recipe.json"` 拒绝缺字段、未知字段、非有限数和非法联动。按 [验证范围](references/validation.md) 检查修改涉及的合同：零密度恒等、有限域外不贡献、前景深度截断、固定时间重放、三种照明分离与实际导出。事件页使用自身 JSON 导入与 WebGL 验证；原基础 Forge 验收不认证它们。只有新工程的游戏截图和 GPU 数据才支持新后端实机结论。

## 研究与复用

需要借鉴光影包或迁移其算法时读 [来源研究](references/source-study.md) 与 [源码索引](references/sources.json)。Bliss 两个快照分别核对；Photon 与 Hysteria 不按文件名或缓冲注释假定相同语义；Complementary 的命中云与体积风暴不等于连续 Beer 积分；Solas 是用户本地改动快照。参考代码和纹理只作为学习资料，未打包为原创资产。

根据 GitHub 资料继续改水龙卷时读 [源码应用说明](references/research/github-water-vortex-20261011/IMPLEMENTATION_NOTES.md)：先判断实体占据，再统一螺旋形变与流动。PBF 约束和屏幕表面滤波不会凭空补水；表面流纹不等于粒子速度或流体平流。下载的源码与许可属于独立研究包，当前资产仍是原创程序实体，没有移植求解器。

随附 `assets/world-volume-lab/` 包含共用 GLSL、WebGL2 工作台、严格配方工具和完整 Forge 示例。采用有限单区域与单事件的中点积分，没有历史重投影、任意透明层或多区域灯光管理；在任务需要时扩展相应生产者与验证，而非凭模板名称声明能力。

涡旋与水体的验收范围见 [页面检查](references/validation/vortex.json)、[碗口专项 GPU 检查](references/validation/vortex-revision9.json)、[实际预览](references/validation/vortex-revision9-visual.json) 和 [安装版独立试作](references/validation/vortex-portable.json)。按各报告的源码指纹、原始通过项和失败项判断；顶部空腔应检查中心为空、周围有水及内外法线，旧版全高度实芯指标属于历史。历史少量像素重放差异不能改写成严格通过，资料包完整性也不表示渲染检查全部通过。

接入宿主晚合成、替换原版云或与闪电/前景特效共存时，读 [宿主合成顺序](references/host-late-composite.md)。
