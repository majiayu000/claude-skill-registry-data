---
name: minecraft-animated-material-adapter
description: 为 Minecraft 动态物品、ModelPart 和骨骼载体适配程序材质与动画挂点，保留原动作、法线与显示变换，附 Forge 1.20.1 BEWLR 层级模型示例。用于 Cosmic、黑洞和碎晶的动态几何接入。
---

# 动态模型材质适配

从既有 renderer 取得最终动画几何、材质区域和挂点，选择材质采样空间后绘制。先识别普通 quads、BEWLR、ModelPart、刚性骨骼或带权重蒙皮。读取目标库版本及真实调用入口，保留原模型解析、动作和姿态。

本例包含两部件刚性 ModelPart、运动子部件、骨骼局部程序材质和刀尖挂点；没有实现 GeckoLib、穿戴护甲或多权重 GPU 蒙皮。接到这些目标时完成真实适配器，不能以示例动画宣称通用兼容。

## 制作与验证

1. 用户给自然语言时先按 [设计与字段](references/design.md) 形成可看初稿；字段不足就增加消费者。预设是起点，不限制主题。
2. 查看 [接入契约](references/integration.md)，使用目标工程版本和 renderer。默认例子为 Forge 1.20.1 / 47.4.10 / Java 17；尊重目标 Forge 补丁选择。
3. `python scripts/scaffold.py <空目录>` 复制完整例子；`python scripts/validate_recipe.py <配方.json>` 检查字段；`python scripts/preview.py <配方.json> <预览目录>` 生成动态 HTML 工作台。
4. 在目标目录用 JDK 17 执行 `gradlew.bat --console plain build`，生产包完成 reobfJar。首次构建需依赖下载；本机可使用完整缓存 offline。
5. 按 [验收与证据](references/validation.md) 检查视觉和生命周期。WebGL/Canvas、数值测试、Forge 构建与游戏实测分别记录；新适配器不继承其他实验的认证。

示例中改变资源 JSON 后重载，再重新 start；无效配方保留上一份有效配置并打印错误。scaffold 不部署 mod、不启动游戏、不覆盖已有工程。采用既有实例时遵循用户选择及启动器工作流；本技能不隐含选择某个存档。

资产为原创 Java/GLSL/JSON；参考项目定位和许可边界见 [来源](references/sources.md)。交付时附运行结果、已实现字段、实际目标类别和剩余边界。只交参数表不构成用户要求的完整效果制作。

真实装备几何捕获、世界/GUI分流或静态材质拆层时，读 [宿主几何适配](references/host-geometry-capture.md)。
