---
name: fec-refactoring-validation
description: 用于证明前端重构保持了既有行为、选择合适的安全网、逐步验证结构修改，或依据证据给出 PASS、PARTIAL、NOT PROVEN 的行为保持结论。
---

# 技能：重构验证

## 用途

定义可观察行为契约，并为每个结构步骤选择足够且不过度的验证证据。

## 流程

1. 在重要编辑前记录相关行为契约。
2. 将安全网分为 A、B、C 三个等级。
3. 运行并记录修改前基线。
4. 根据当前步骤的风险和边界选择验证方式。
5. 每个结构步骤后立即运行最小有效检查。
6. 新增失败出现时先回滚当前步骤，再扩大排查。
7. 最后运行与影响面匹配的更广门禁。
8. 只按证据给出 PASS、PARTIAL 或 NOT PROVEN。

纯结构重构使用 **GREEN → REFACTOR → GREEN**。

## 安全网等级

| 等级 | 证据 | 执行建议 |
| --- | --- | --- |
| A — 强 | 既有测试直接覆盖相关行为 | 直接作为主要安全网 |
| B — 部分 | 重要行为覆盖不完整 | 高风险步骤前补当前行为的特征测试 |
| C — 无 | 没有有效自动化覆盖 | 不自动安装框架；CAUTION/DANGER 默认只规划，除非已授权补最小安全网 |

## 前端行为契约清单

按实际范围检查：函数输入输出、异常和错误映射；DOM、可见状态、焦点、键盘和无障碍语义；props、emits、slots、Hook/Composable 返回值和事件顺序；请求、载荷、取消、重试、缓存键和加载/错误状态；store、持久化、对象身份、memoization、响应式和生命周期；路由、URL、guard、包导出、序列化字段和后端 DTO。

## 参考资料

- 构建行为契约和证明等级见 [behavior-preservation.md](references/behavior-preservation.md)。
- 按前端风险选择目标验证见 [refactoring-test-checklist.md](references/refactoring-test-checklist.md)。

## 约束

- 无关测试通过不能证明行为保持。
- 只在修改后新增并通过的测试，证据弱于可比较的修改前基线。
- 不因为重构改变了行为就改测试期望值。
- 证据不足时不能用 PASS 掩盖缺口。
- 未经明确授权不安装新的测试框架。

## 预期输出

输出行为契约、基线状态、安全网等级、逐步验证、最终门禁、覆盖缺口，以及 PASS、PARTIAL 或 NOT PROVEN 结论。
