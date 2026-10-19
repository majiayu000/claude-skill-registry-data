---
name: minecraft-cosmic-rendering
description: 从自然语言制作 Minecraft 程序天空、球形大气、世界云雾天光与生物群系雨雪，兼含双虹、冰晕、星云、巨型天体和两类动态远景黑洞，提供调参工作台及 Forge 1.20.1 原版玻璃水面接入。不用于近距离世界黑洞、世界生成或 Photon 粒子编辑。
---

# Minecraft 天空与宇宙渲染

把视觉目标落到正确的绘制入口，并以相机、数据和深度契约验证实现。已有实测模板仅覆盖 **Minecraft 1.20.1 / Forge 47.4.22 / Java 17**。通用数学可以迁移，API 与 shader 加载格式不能直接外推到其他版本或加载器。

## 确定承载方式

从现有工程读取 MC、加载器、mappings、Java、渲染依赖与已有入口。沿用用户指定的版本和项目；不要为套模板另换版本或默认替换全部主世界天空。

| 目标 | 合适的承载方式与契约 |
|---|---|
| 无限远大气/日月/薄云/星空 | 真实天空入口，世界方向驱动，消除相机平移，使用当前实际投影 |
| 方块/实体/物品上的宇宙材质 | 对应几何与 RenderType，区分模型 mask/UV 和效果方向，保留承载物遮挡 |
| 可以进入、有视差的局部星云 | 有限体积边界与射线积分，统一场景深度和射线参数 |
| 世界云层、雾、雨与云影天光 | 当前世界相机、真实颜色/深度与有限积分；透明层另立深度契约 |
| 屏幕空间光晕/合成 | 后处理入口，明确 framebuffer、viewport、输入纹理与混合 |

只有用户要求研究时，交付证据链和结论即可；不要自行把研究变成效果开发。普通模组脚手架、资源包打包或 Photon 操作遵循目标工程/相应技能，本技能负责宇宙渲染的特殊决策。

## 按任务读取

- 玩家自制天空、天气、世界云/雾/天光、双虹/冰晕、巨型天体/两类远景黑洞、调参或配方导入导出：读 [authoring.md](references/authoring.md)，按需复制 [assets/procedural-sky-lab](assets/procedural-sky-lab)。浏览器与 Forge 共用五份原创 GLSL，严格 `cosmic-sky/6`，188 字段、39 预设；完整旧 `/1`、`/2`、`/3`、`/4`、`/5` 可在工作台显式升级。
- 球形大气LUT、气候雨雪、屋顶、原版玻璃/水的分层环境、低分辨率或Oculus/Embeddium所有权切换：读 [advanced-sky.md](references/advanced-sky.md)。这些入口有明确单位、缓存及渲染契约，不能把原版BLOCK适配扩展为任意透明物体或任意第三方光影同时叠加。
- 相机漂移、旋转、FOV、窗口变化或深度问题：读 [coordinates.md](references/coordinates.md)。
- 选择星点、FBM 或体积算法、设置质量档：读 [algorithms.md](references/algorithms.md)。
- Forge 1.20.1 接入、重载或复现实验：读 [forge-1.20.1.md](references/forge-1.20.1.md)，需要模板时再复制 [assets/forge-1.20.1-lab](assets/forge-1.20.1-lab)。
- 排查黑屏、覆盖地形、接缝、光影兼容或规划验收：读 [diagnostics.md](references/diagnostics.md)。
- 研究 ArcaneVortex 或核对已有结论：读 [evidence.md](references/evidence.md)。它区分参考代码静态发现和独立实验实测，不是参考 MOD 的运行认证。
- 选择更高质量大气、体积云、天气、光学现象或异界天空路线：读 [sky-materials.md](references/sky-materials.md)。资料库区分原创已实现能力、物理质量路线和第三方静态发现。

- 七种二维巨型天体或电影黑洞背景透镜：读 [celestial-giants.md](references/celestial-giants.md)。
- Bliss指定2.1.2末地云分布及间歇云内闪光研究：读 [bliss-end-clouds.md](references/bliss-end-clouds.md)。此项仅为源码研究，尚未实现云闪光。

## 实施与验证

先闭合 `注册 → 当前实例 → 数据上传 → 实际 draw → 输出目标`，再按需要增加效果复杂度。排查时从常量色/方向色收窄问题；已有稳定效果的小改动不必强制重搭整套实验。

明确 Position、相机、视图矩阵、深度和每个 sampler/uniform 的空间与来源。Java、JSON、GLSL 核对名字、类型、数量、顶点格式与上传时机；区分源码中声明的参数和编译后真正活跃的参数。重载后使用回调交付的新实例，不长期缓存旧 uniform 句柄。

对无限远天空，优先做固定时间的平移、旋转、FOV、resize、资源重载和地形遮挡检查。有限体积另测离轴遮挡和进出边界。只运行与改动风险相关的检查；无法启动 GPU 时明确停在静态/编译证据，不将之写成视觉通过。

模板自动实验的 JSON 与截图可交给 [scripts/check_validation.py](scripts/check_validation.py)：

```text
python <skill>/scripts/check_validation.py <copied-project>/validation
```

脚本核对该模板固定 15 个用例的记录、误差、重载、PNG 尺寸和计时完整性，不分析画面美感或证明任意着色器正确。仍需查看星点、星云与遮挡截图。修改用例协议时同步调整检查器，不能把缺测项悄悄算作通过。

性能记录要包含硬件、分辨率、质量预算和测量区间。GPU 单 pass 耗时不等于整帧 FPS；模板的颜色、频率和质量数字是实验选择，不是通用规范。

交付实际改动/证据定位、已做验证与未覆盖项。无需每次照搬完整研究报告。不要把“没有经纬度 UV”写成已证明全天球无缝，也不要把普通 Forge 天空验证扩展为 Oculus/Shader Pack 兼容保证。
