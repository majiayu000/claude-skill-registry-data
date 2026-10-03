---
name: api-contract-design
description: Design or revise an API contract before implementation. Use when defining an HTTP, RPC, or event interface, its fields, errors, or compatibility rules; not for merely implementing an already agreed contract.
---

# 接口契约设计

把需求转成调用方和提供方都能实现、测试与演进的接口约定。先识别项目现用的协议、命名、错误模型与文档格式；没有既定约定且选择会改变交付结果时，向用户确认。不要默认所有接口都是 REST。

## 设计流程

1. **确认边界。** 明确谁调用、谁提供、业务动作、成功条件、部署或版本约束，以及新接口还是修改已有接口。读取相关既有接口、消费者和规范，列出尚未确定且影响契约的问题。
2. **写清消息与语义。** 按所用协议定义操作名或路径、输入输出字段、类型、必填/可空、默认值、约束、单位与示例；列出成功、校验失败、业务拒绝、权限失败和系统故障中适用的结果与错误。分页、排序、幂等、超时和重试只在相关场景定义，不能套模板硬加。
3. **核对兼容性。** 对已有调用方检查字段增删、默认值、错误码、枚举扩展、序列化与行为语义是否破坏兼容；需要迁移时给出双方的实施顺序和过渡期。把尚未决定的技术或业务选择作为待决项，而不是写成既定事实。
4. **交付可验证的契约。** 使用仓库已有的 OpenAPI、Proto、AsyncAPI、Markdown 或其他格式；包含正常及边界示例，并把关键规则映射到契约测试或验收用例。用户只要求设计时，不修改业务实现。

最后说明依据、待决项、兼容性结论和验证办法。不要虚构已有消费者或声称未运行的契约测试已通过。

## 与相邻 skill 的边界

- 实现已确定的接口或完整功能：`code-vibe-workflow`。
- 从现有契约编写单元或进程内接口测试：`code-testing`。
- 讨论类和对象的设计模式：`design-pattern-advisor`。
- 审查现有实现缺陷：`code-review-deep-zh`。
