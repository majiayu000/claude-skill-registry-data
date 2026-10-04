---
name: cc-go-dev
description: Go 开发规范，适用于 Go 源码、包结构、错误处理、并发和测试相关任务；不负责 review、debug 或运维流程。
---

# CC Go Dev

在编辑或审查 Go 代码时使用本技能，重点处理 idiomatic Go、包结构、错误处理、并发与测试。

不要用于：

- 正式 review 或 fix/debug 工作流
- 运维风险判断
- 与 Go 无关的通用改动边界

## 核心规则

- 保持实现简单、显式、idiomatic。
- 优先清晰的包边界和职责拆分。
- 错误必须处理，并保留足够上下文。
- 并发要考虑生命周期、取消和数据竞争。
- 测试优先覆盖受影响行为。

## 按需展开

- 风格：`references/style.md`
- 错误处理：`references/errors.md`
- 并发：`references/concurrency.md`
- 测试：`references/testing.md`
- 项目结构：`references/project-shape.md`
