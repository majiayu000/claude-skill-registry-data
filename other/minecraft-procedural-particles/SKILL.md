---
name: minecraft-procedural-particles
description: 从自然语言制作 Minecraft 代码驱动的发射器、环绕、喷发和聚合粒子，提供稳定 tick 模拟、挂点与世界空间、生命周期、容量和 Forge 1.20.1 示例；用于 Java 或数据驱动运行库的粒子制作。
---

# 程序化粒子制作

将描述拆为发射时序与形状、初始条件、运动场、外观曲线、挂接方式和寿命预算。输出真实数据消费者、模拟核与绘制入口，不只给参数清单。

用户要 Photon 编辑器或已有 Photon FX 操作时沿用 minecraft-vfx-automation；本 skill 面向原创 Java/数据驱动发射器，允许在既有运行库中实现相同设计。本例四种 motion 是起点，自由设计可新增场和发射形状。

## 制作与验证

1. 用户给自然语言时先按 [设计与字段](references/design.md) 形成可看初稿；字段不足就增加消费者。预设是起点，不限制主题。
2. 查看 [接入契约](references/integration.md)，使用目标工程版本和 renderer。默认例子为 Forge 1.20.1 / 47.4.10 / Java 17；尊重目标 Forge 补丁选择。
3. `python scripts/scaffold.py <空目录>` 复制完整例子；`python scripts/validate_recipe.py <配方.json>` 检查字段；`python scripts/preview.py <配方.json> <预览目录>` 生成动态 HTML 工作台。
4. 在目标目录用 JDK 17 执行 `gradlew.bat --console plain build`，生产包完成 reobfJar。首次构建需依赖下载；本机可使用完整缓存 offline。
5. 按 [验收与证据](references/validation.md) 检查视觉和生命周期。WebGL/Canvas、数值测试、Forge 构建与游戏实测分别记录；新适配器不继承其他实验的认证。

示例中改变资源 JSON 后重载，再重新 start；无效配方保留上一份有效配置并打印错误。scaffold 不部署 mod、不启动游戏、不覆盖已有工程。采用既有实例时遵循用户选择及启动器工作流；本技能不隐含选择某个存档。

资产为原创 Java/GLSL/JSON；参考项目定位和许可边界见 [来源](references/sources.md)。交付时附运行结果、已实现字段、实际目标类别和剩余边界。只交参数表不构成用户要求的完整效果制作。

独立内核可在设置 `JAVA_HOME` 为 JDK 17 后执行 `python scripts/check_core.py`，无需 Minecraft 或 Gradle。

地面图案、定向薄片、实体附着火焰或状态停止效果时，读 [粒子表面与生命周期](references/host-particle-surfaces.md)。
