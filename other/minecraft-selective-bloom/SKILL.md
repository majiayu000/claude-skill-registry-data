---
name: minecraft-selective-bloom
description: 从自然语言制作 Minecraft 指定对象与材质区域的屏幕 Bloom，提供独立发光缓冲、分离模糊、深度约束与 Forge 1.20.1 原创示例；用于星点、符文和能量核的外扩光晕。
---

# 选择性 Bloom

把用户描述转成发光资格、光晕尺度、颜色与亮度、遮挡和合成阶段。只为选定区域生成 emission；Halo 几何、物品自发光和周围场景照明分别设计。示例证明的是可构建的独立目标流程，不是所有物品自动具备 Bloom。

收到“剑上的蓝色星点发光”时，在已有材质算法中输出 emission 选择；不要把整张剑底图或整屏亮像素都作为源。用户希望真实落地物品时完成对应绘制入口，不用 client-local marker 代替目标物品交付。

## 制作与验证

1. 用户给自然语言时先按 [设计与字段](references/design.md) 形成可看初稿；字段不足就增加消费者。预设是起点，不限制主题。
2. 查看 [接入契约](references/integration.md)，使用目标工程版本和 renderer。默认例子为 Forge 1.20.1 / 47.4.10 / Java 17；尊重目标 Forge 补丁选择。
3. `python scripts/scaffold.py <空目录>` 复制完整例子；`python scripts/validate_recipe.py <配方.json>` 检查字段；`python scripts/preview.py <配方.json> <预览目录>` 生成动态 HTML 工作台。
4. 在目标目录用 JDK 17 执行 `gradlew.bat --console plain build`，生产包完成 reobfJar。首次构建需依赖下载；本机可使用完整缓存 offline。
5. 按 [验收与证据](references/validation.md) 检查视觉和生命周期。WebGL/Canvas、数值测试、Forge 构建与游戏实测分别记录；新适配器不继承其他实验的认证。

示例中改变资源 JSON 后重载，再重新 start；无效配方保留上一份有效配置并打印错误。scaffold 不部署 mod、不启动游戏、不覆盖已有工程。采用既有实例时遵循用户选择及启动器工作流；本技能不隐含选择某个存档。

资产为原创 Java/GLSL/JSON；参考项目定位和许可边界见 [来源](references/sources.md)。交付时附运行结果、已实现字段、实际目标类别和剩余边界。只交参数表不构成用户要求的完整效果制作。

低分辨率光晕需要前景遮挡时，读 [发光深度元数据](references/depth-metadata.md)。
