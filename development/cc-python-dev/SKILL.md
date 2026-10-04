---
name: cc-python-dev
description: Python 开发规范，适用于类型注解、验证模型、pytest 和 uv 工具链；不负责 review、debug 或运维流程。
---

# CC Python Dev

在编辑 Python 代码时使用本技能，重点处理类型注解、数据模型、pytest 和工具链约束。

不要用于：

- 正式 review 或 fix/debug 工作流
- 运维风险判断
- 与 Python 无关的语言细节

## 核心规则

- 公开接口优先补类型信息。
- 数据校验和数据模型边界要清晰。
- 测试优先覆盖受影响行为和边界输入。
- 工具链优先保持与项目既有约定一致。

## 按需展开

- 风格：`references/style.md`
- 类型：`references/typing.md`
- Pydantic：`references/pydantic.md`
- pytest：`references/pytest.md`
- 工具链：`references/toolchain.md`
