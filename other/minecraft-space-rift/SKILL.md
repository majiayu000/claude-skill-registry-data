---
name: minecraft-space-rift
description: 制作 Minecraft Forge 1.20.1 程序化空间裂缝、横向动态星河、立体蓝紫撕裂边缘及开合动画，提供共享 GLSL、14 个 JSON 预设和 Forge 源码接口。用于算法裂隙，不用于贴图裂缝、真实地形破坏或可穿越第二世界。
---

# 程序化空间裂缝

先检查目标工程已有 Shader、参数系统、天空和异空间接口，优先复用。此公开包只含算法与接入资源，不包含个人整合工作台。

1. 使用 `python scripts/create_project.py <新目录>` 复制资源。阅读生成目录的 README.md 和 NOTICE.md。
2. `shader/geometry.js` 生成稳定种子的分形骨架；`shader/parameters.js` 管理参数、质量及预设。改变种子或几何后更新骨架 Uniform，普通视觉变化直接更新 Uniform。
3. `rift_core.glsl` 计算开口，`rift_rim.glsl` 和 `rift_horizon.glsl` 计算边缘及深度；保留物理局部坐标采样和导数抗锯齿，不拉伸固定纹理。
4. 横向干净裂隙选 `horizon-slash`、`horizon-tear`、`horizon-giant`，保留 `horizon=1`。其它预设允许分支、破碎演出及算法风格。按需求禁用外围装饰。
5. 内部渲染通过 `interior-adapter.glsl` 替换；复用目标天空或子场景时明确相机、坐标与遮罩。内部只在真实开口可见。
6. 用 `python scripts/build.py` 生成 WebGL2、Shadertoy 和 Forge GLSL150；不手改生成文件。通过长度、宽度、progress/open/shrink/sequence 等参数控制演出。
7. Forge 接入读 `forge/src`：使用世界位置与朝向，正确管理场景颜色副本、深度、混合及缓冲生命周期。背景折射必须使用真实场景缓冲；测试背景不能称为真实折射。
8. 验证 `node scripts/check_geometry.mjs`、生成脚本、可选桌面 GL 测试和 Java17 Gradle 构建。游戏运行验收另行完成；浏览器或桌面 GL 通过不等于已验证 Minecraft。

修改前优先研究相关 Shadertoy 算法并保留来源；无法读取时说明限制。保留 psrdnoise 作者和 MIT 通知；附件衍生代码的许可边界见 NOTICE，不将组合整体宣称为 MIT。
