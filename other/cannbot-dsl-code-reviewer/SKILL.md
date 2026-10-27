---
name: cannbot-dsl-code-reviewer
description: "检视调用方提供的 CANNBotDSL 算子代码，依据真实调用链核查生产执行约束、计算与导出路径，以及命名、魔数和可读性。当用户要求 DSL 代码审查、检视实现或复核 PR 时使用。"
metadata:
  category: review
---

# CANNBotDSL 代码检视

## 输入

- 调用方指定的算子源码文件、目录或 PR 差异。
- 可选：算子规格、设计资料、Unit 和测试结果，用于理解代码职责与排除误报。

## 输出

在调用方指定的位置写代码检视报告，分别给出生产执行约束和可读性结论。每项发现包含文件、准确行号、最短必要代码片段、问题、分级、证据与修复建议；没有发现时也给出明确结论。报告格式参考 [报告写法](steps/report-write.md)。

## 检视方法

1. 实际阅读公开入口、helper、注册/适配层、分配、搬运与启动，按 [生产执行约束](references/execution-rules.md) 核查全部生产路径；再按 [可读性规则](references/readability-rules.md) 检查命名、魔数与结构风格。
2. 按 [检视方法](core/methodology.md) 对候选问题检测、核实、判定。每条正反证据都引用真实代码行；缺少证据的候选不判为 FAIL。
3. 报告使用 FAIL、SUSPICIOUS、待确认分级。已证实的生产执行约束违规直接判 FAIL，不参与风格置信度抵扣，也不降为普通建议。执行域或证据不清楚时保留待确认，不能把缺少设备证据标为 PASS。

本 Skill 提供检视方法与报告内容。调用方安排执行角色、并行和报告路径。
