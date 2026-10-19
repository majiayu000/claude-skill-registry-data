---
name: minecraft-crystal-refraction
description: 从自然语言制作 Minecraft 碎晶折射、棱镜色散和裂隙玻璃材质，提供原创可调预览、GLSL 资源生成、物品内部场与世界背景两种接入方法。用于折射星空、水晶武器和空间扭曲；不用于仅改色的附魔流光或普通透明贴图。
---

# 碎晶折射与色散

把效果拆成 **碎片形状 → 面法线 → 折射偏移 → 分色采样 → 覆盖与边缘**。折射的内容必须明确：物品自己的内部星空，还是已经绘制的世界。前者可以查询内部场或离屏材质图；后者需要正确阶段的场景副本和遮挡处理。

## 从用户描述开始

无需用户填写参数。根据主体、碎片大小、弯曲强度、彩边宽度、透明比例和动态节奏制作初稿。具体映射、参数范围及算法见 [design-and-algorithm.md](references/design-and-algorithm.md)。不要把碎晶做成全屏随机 RGB 偏移，也不要以彩色边线冒充背景折射。

- “剑里折射星空”：局部晶片扭曲内部背景；原几何 alpha 保轮廓，区域 mask 限制覆盖。
- “水晶扭曲后面的世界”：使用场景输入路径，确认捕获阶段、深度和透明排序；不能从同一 framebuffer 附件边读边写。
- “细小彩边”：先做无色折射，再增加色散；底色 tint 与色散分别调节。
- “稳定碎晶”：固定 seed 与晶片中心；动态只改变法线/角度，不逐帧重排格子。

## 制作与交付

1. 从 [配方](assets/lab/recipes.json) 选择起点，运行 `python scripts/serve_preview.py --port 8771`，打开打印的 loopback 地址。预览支持星域/网格、窗口形状、参数、暂停、原图、导入/导出和实际 16/32 px 小图。
2. 先调无色折射与碎片主形，再调色散、边缘、底色和动画。固定 time/seed 比较，检查真正的小分辨率重渲染。自然语言可生成新配方，不限于三个预设。
3. 导出配方；需要移植时运行 `python scripts/build_shader.py --out <新输出目录>` 生成 GLSL 150 shader 三件套。固定资源名 crystalrefraction:crystal_refraction。这些是 shader 资源，不是独立 mod；接入说明见 [forge-1.20.1.md](references/forge-1.20.1.md)。
4. 按 [validation.md](references/validation.md) 检查效果与绘制链。用户只要求 skill 时交付方法、资源和验证；要求落地模组时继续完成注册、模型适配、构建和目标游戏验收。

## 不可混淆的契约

- 晶片坐标与背景采样坐标分开。局部图案随物体移动；屏幕副本按实际 viewport/目标分辨率采样，GUI scale 不是 framebuffer 尺寸。
- 原纹理 alpha、区域 mask、材质透明度独立。背景采样 UV 可越过窗口去读取背景；内部内容的采样边界须显式定义。
- 附带内核是薄层三通道美术近似，没有厚实体出口追踪、全反射、焦散或严格光谱积分。
- 单次 draw 的参数、sampler、矩阵和资源代次一致。每物品参数不能先写共享 uniform 再被延迟批次覆盖；在 draw 时绑定或明确 flush。
- UV clamp 不解决前景漏色、遮挡或屏外信息缺失。没有深度路径时不能宣称解决这些问题。
- 原创代码与参考源码分开，来源及验证边界见 [sources-and-status.md](references/sources-and-status.md)。

## 资源边界

随附 WebGL 2 制作台、确定性验证脚本与 GLSL 150 资源生成器。制作台通过独立背景纹理和单独输出目标真实执行 GPU shader；窗口与星域是示意，不是 Minecraft 截图。Forge 路线以 1.20.1 为目标，本技能未获得 Forge 运行认证，也不继承 Cosmic Material Lab 的认证。
