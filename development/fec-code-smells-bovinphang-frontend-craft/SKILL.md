---
name: fec-code-smells
description: 需要在不修改业务代码的前提下诊断既有前端代码的结构性可维护性问题，并要求提供证据、误判检查与候选重构方向时。
---

# 代码坏味道诊断

## 概览
基于具体证据诊断结构问题。坏味道是进一步调查的信号，不等于必须修改代码的结论。

## 执行流程
1. 明确分析范围和项目事实。
2. 收集结构、依赖方向、职责和变化耦合证据。
3. 对照[坏味道目录](references/smell-catalog.md)。
4. 执行[误判检查](references/detection-guide.md)。
5. 根据[坏味道到重构手法映射](references/smell-to-refactoring-map.md)报告置信度、影响和候选方案。
6. 如果用户只要求诊断，不修改业务代码。

## Finding 输出契约
每项必须包含位置、证据、坏味道 ID/名称、影响、置信度（`HIGH`、`MEDIUM`、`LOW`）、候选重构、优先级和重要误判因素。`LOW` 置信度不能作为自动修改依据。

## 快速索引
| 需要 | 资料 |
| --- | --- |
| 24 种标准坏味道 | [坏味道目录](references/smell-catalog.md) |
| 证据与误判保护 | [检测指南](references/detection-guide.md) |
| 候选重构手法 | [映射指南](references/smell-to-refactoring-map.md) |

## 常见错误
- 把指标阈值当成坏味道证据。
- 不指出文件/符号就下结论。
- 把所有循环、switch、注释、包装层或管道都视为缺陷。
- 用户要求只诊断时仍直接改代码。
