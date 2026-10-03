---
name: behavior-preserving-refactor
description: Refactor existing code while preserving observable behavior. Use for a requested extraction, relocation, renaming, or structural simplification; not for a new feature, bug fix, or deletion-only cleanup.
---

# 保持行为的重构

把用户指定范围内的代码结构改清楚，同时证明外部可观察行为没有变化。范围只有“重构一下”而没有目标文件、模块或问题时，先确认边界和期望的结构变化。

## 工作方式

1. **列出必须保持的契约。** 从现有调用方和测试提取输入、输出、异常、状态变化、持久化结果、公开 API、序列化格式与调用顺序中相关的约束。区分明确需求与仅由现有实现表现出的行为；不擅自把疑似缺陷改成新行为。
2. **建立基线。** 运行与范围相关的现有测试并记录结果。测试不足时，针对重要的可观察行为补少量特征测试或可重复的对照样例；基线本来失败时，标出原有失败，不用重构后的结果掩盖它。
3. **做最小结构修改。** 只处理约定的结构问题，按项目现有风格更新调用方、导入与必要文档。每步保持改动可审查；不顺手添加功能、修复无关缺陷或引入为了未来可能性准备的抽象。
4. **比对前后行为。** 运行相关测试，并检查公开签名、错误语义、数据格式和副作用是否保持。项目要求或用户要求时再做编译、构建或类型检查。发现行为变化就定位并修正，无法证明等价的部分明确列出。

报告改动范围、保留的契约、基线与修改后验证结果，以及尚未覆盖的风险。若用户实际要求改变行为，应转为相应功能开发或故障修复流程。

## 边界

- 只删冗余、就地内联：`code-slimming`。
- 决定是否使用某个设计模式：`design-pattern-advisor`。
- 定位并修复现有故障：`systematic-debugging`。
- 新增业务能力：`code-vibe-workflow`。
