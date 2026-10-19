---
name: minecraft-glass-rim
description: 从自然语言制作 Minecraft 玻璃边缘亮、水晶外壳与能量护罩的视角相关边缘光，提供原创 GLSL、三维可调预览和 Forge 1.20.1 接入方法。用于法线驱动的 rim/Fresnel 外观；不把它当作真实折射、二维轮廓提取、Halo 或屏幕 bloom。
---

# 玻璃边缘亮

把效果拆成几何法线、观察方向、边缘权重、颜色、透明覆盖与绘制状态。先判断载体是平面图标、硬边模型、光滑曲面还是额外外壳；不要承诺相同 shader 在它们上面产生相同轮廓。

## 从描述到制作

- “冰蓝玻璃，中心很透，边缘细亮”：低中心 alpha、较高 rim power、青白边缘。
- “厚实琥珀外壳”：暖色、较宽边缘与较高表面 alpha；这是外观，不是假定真实厚度吸收。
- “能量护罩”：单独壳几何、宽边缘、适度脉动；是否显示背面由需求决定。
- “剑的像素轮廓亮”：先确认要纹理轮廓还是三维掠射边缘；前者需要 mask 距离场/邻域或扩展几何，此内核不提供二维描边。

先读 [算法与设计](references/design.md)。使用 assets/lab/index.html 的制作台；在技能目录运行 `python scripts/serve_preview.py --port 8783`，打开打印的地址。支持球/硬边方块/平面、非均匀缩放、旋转观察、自定义颜色、参数导出、静止和动画。配方起点不是设计限制。

输出实际画面及配方，再按 [Forge 接入](references/forge-1.20.1.md) 接到目标模型。assets/rim.glsl 是独立原创算法，可拼入 GLSL 150；不是完整 mod。用户要求落地时继续完成注册、几何适配、构建与游戏验证。

## 必须保持的契约

- N 和 V 在同一空间，V 指向观察者；片元中重新归一化插值法线。非均匀缩放使用 inverse-transpose 法线矩阵。
- 原纹理 alpha、区域 mask、玻璃覆盖 alpha 各自独立。物体透明不等于关闭深度测试。
- 本内核输出直通 alpha 的 RGB；普通混合使用 SRC_ALPHA / ONE_MINUS_SRC_ALPHA。改为预乘或 additive 时同步修改输出，不混搭。
- 内核没有背景折射采样、环境反射、厚度吸收、焦散、场景照明或屏外 bloom。需要这些内容时另加对应 pass。
- 使用 `abs(dot(N,V))` 表示双面美术权重；单面模式需明确背面剔除。封闭玻璃双面叠加会改变 alpha，不自动解决透明排序。
- 同 draw 的参数、矩阵、mask、shader 实例必须一致；共享 uniform 不能被后续物品提前覆盖。

按 [验收与来源](references/validation.md) 分别记录独立预览与 Forge 运行证据。不要借用 Cosmic 或其他技能的旧认证。
