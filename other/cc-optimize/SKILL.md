---
name: optimize
description: 结构化系统优化扫描工作流，适用于显式 optimize、性能评估、体验评估或代码质量扫描场景；默认输出问题与建议，不直接改代码。
---

# Optimize

当用户明确要求 optimize、做优化扫描，或只看 `ux`、`perf`、`code` 某一类改进时，使用本技能。

不要用于：

- 直接修复单个 bug
- 正式 security review
- 无证据的大规模重构
- 代替需求分析或设计文档

## 核心方式

1. 先限定范围：全量、前端、后端或指定目录。
2. 范围很大时，先给规模预估和热点，再决定是否全扫。
3. 根据模式组织检查项：`full`、`ux`、`perf`、`code`。
4. 所有结论都要落在具体代码证据上，不做空泛建议。
5. 默认输出排序后的优化报告；只有用户明确点名某项时，才进入实现。

## 输出要求

- 先给项目概览和扫描范围
- findings 按影响优先级排序
- 每条建议同时说明收益、代价和前置条件
- 没有明显问题时，要明确写出，并指出盲区或未扫描范围

## 按需展开

- 范围选择：`references/scope-selection.md`
- 模式定义：`references/optimize-modes.md`
- 报告格式：`references/report-format.md`
- 输出模板：`templates/optimize-report.md`
