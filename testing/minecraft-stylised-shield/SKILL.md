---
name: minecraft-stylised-shield
description: 将 Unity Stylised Energy Shield Shader Graph 转换为 Minecraft Forge 1.20.1 的客户端护盾网格特效，附带共享 recipe.json、可自定义 HTML 工作台、六边形/扫描线/边缘光/受击波纹 GLSL 与 Java 17 工程。用于护盾、能量穹顶和全息防护罩；不替代真实折射、场景照明或全屏后处理。
---

# Stylised Shield FX

读取用户给出的 Unity Shader Graph 或类似护盾源码，把可辨认的模块转成 Forge 1.20.1 客户端渲染：Fresnel 边缘亮光、对象空间图案、三维流动噪声、溶解、扫描带、顶点形变、六槽受击波前、火星与护盾破碎。生成目录中的 `assets/forge-1.20.1/workbench/index.html` 是可离线运行的参数编辑器；`shader-source.js` 保存护盾及碎片 GLSL，`fracture-core.js` 负责生命周期和曲面切割，`workbench.js` 负责网格、相机、命中拾取、火星和 JSON 配方。右侧支持拖动旋转、滚轮缩放、正面/侧面/三维视角，参数改变会立即更新同一张护盾网格。导出的 JSON 放到实例 `config/shieldfx/recipe.json`，客户端命令 `/shieldfx demo`、`reload`、`hit`、`off` 控制显示。

保持浏览器和 Java 的 JSON 字段一致，颜色使用 `#RRGGBB`。护盾网格是独立半透明网格，完整球体和穹顶使用背面剔除；碎片采用双面渲染，两端均启用 `LEQUAL` 深度测试。球体图案采用对象空间三平面独占投影：每个片元只选择法线最占优的一个平面，靠近投影交界时留出窄空白带，避免多套图案叠加重影。Forge 的写入掩码是 `COLOR_WRITE`，透明排序与遮挡仍需在实际场景验证。它不自动替换原模型，也不产生周围方块光。场景交界亮边需要另加深度纹理 pass，本模板先保留参数并在片元中作为扩展位。

源码转换时记录 Unity 属性到 GLSL uniform 的映射。新增高质量 Flow Shield、HoloShield 和教程资料的迁移要点见 [source-comparison.md](references/source-comparison.md)。不要复制 Unity Shader Graph 序列化文件到 Forge。保留上游 MIT LICENSE。Java 工程使用 Forge 1.20.1、Java 17，客户端订阅器限制为 `Dist.CLIENT`。工作台的 `schema: 2` 是前端完整配方；导入旧 `schema: 1` 时只做显式字段映射，不把旧的二维参数误当成三维材质。

持续命中逐步降低 `life` 并变红；生命归零的那一击仍保留壳体，下一击才进入一次性破碎状态。破碎期间及结束后拒绝继续命中，恢复、换形状、换预设或导入配方时清除旧碎片和待播放连击。浏览器冻结当前形变曲面，再按 Voronoi 平分面切成刚体碎片，保留对象空间材质坐标；裂纹由命中点向外扩散，碎片独立旋转、飞散、下坠并淡出，内部三角网线不作为裂纹绘制。六个配方字段是 `shatterDuration`、`shardCount`、`shatterSpeed`、`shatterSpin`、`shatterGravity`、`shatterFlash`，旧 v2 配方缺失时使用默认值，`shardCount` 于下次破碎生效。

## 验证

从 `workbench` 目录运行 `node serve.cjs 8766`，用浏览器打开 `http://127.0.0.1:8766/`。检查四种几何形状、拖动视角、透明度/图案实时变化、中心命中、连续命中、破碎、暂停和恢复。`node --test tests/fracture.test.cjs` 验证生命周期与切割几何；安装了 Playwright 与 Edge 的环境可运行 `node tests/browser-smoke.cjs <截图目录>` 验证 WebGL 和回放。导出 JSON 后运行 Forge 工程的 `gradlew build`，再进入客户端执行 `/shieldfx demo`，修改配置后 `/shieldfx reload`。HTML 预览通过不等于游戏运行通过；分别记录浏览器、构建和游戏实测状态。

接入真实受击事件、多人护盾破碎或后台切割时，读 [异步破碎接入](references/async-fracture-integration.md)。
