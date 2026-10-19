---
name: minecraft-dynamic-lighting
description: 制作 Minecraft 客户端动态点光与局部场景照明，处理位置重建、法线、光源数据、范围衰减及合成，附 Forge 1.20.1 地形深度重建示例；用于武器或粒子照亮场景。
---

# 动态照明

先判断用户要表面自发光、屏幕光晕、客户端周围场景照明还是改变游戏方块光等级。本 skill 处理场景照明，选择重建/材质注入/框架灯光后端，明确有无阴影、影响哪些几何、颜色空间与预算。

示例是一个固定客户端点光对已绘制地形颜色的风格化附加照明。它缺少原始 albedo/BRDF、阴影和透明/实体照明；收到更完整目标时实现对应生产入口，不能用这一基线冒充完整 PBR 或真实方块光系统。

## 制作与验证

1. 用户给自然语言时先按 [设计与字段](references/design.md) 形成可看初稿；字段不足就增加消费者。预设是起点，不限制主题。
2. 查看 [接入契约](references/integration.md)，使用目标工程版本和 renderer。默认例子为 Forge 1.20.1 / 47.4.10 / Java 17；尊重目标 Forge 补丁选择。
3. `python scripts/scaffold.py <空目录>` 复制完整例子；`python scripts/validate_recipe.py <配方.json>` 检查字段；`python scripts/preview.py <配方.json> <预览目录>` 生成动态 HTML 工作台。
4. 在目标目录用 JDK 17 执行 `gradlew.bat --console plain build`，生产包完成 reobfJar。首次构建需依赖下载；本机可使用完整缓存 offline。
5. 按 [验收与证据](references/validation.md) 检查视觉和生命周期。WebGL/Canvas、数值测试、Forge 构建与游戏实测分别记录；新适配器不继承其他实验的认证。

示例中改变资源 JSON 后重载，再重新 start；无效配方保留上一份有效配置并打印错误。scaffold 不部署 mod、不启动游戏、不覆盖已有工程。采用既有实例时遵循用户选择及启动器工作流；本技能不隐含选择某个存档。

资产为原创 Java/GLSL/JSON；参考项目定位和许可边界见 [来源](references/sources.md)。交付时附运行结果、已实现字段、实际目标类别和剩余边界。只交参数表不构成用户要求的完整效果制作。

接入已有方块或材质并区分自发光与场景光时，读 [宿主照明边界](references/host-limits-and-emission.md)。
