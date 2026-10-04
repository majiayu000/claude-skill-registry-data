---
name: <skill-name-kebab-case>
description: "<一句话说清『这个 skill 做什么 + 何时调用』。把最关键的触发场景放最前面。结尾给 2-3 个用户会说的关键词。>"
# 可选字段（按需打开）：
# when_to_use: "更多触发线索；与 description 合计 ≤1536 字符"
# disable-model-invocation: false   # true = 只允许用户 /xxx 触发
# user-invocable: true              # false = 从 / 菜单隐藏
---

# <Skill Display Name>

> 单行用途描述。

## 何时使用

- 触发场景 1
- 触发场景 2
- **不**适用于：<明确的反向边界>

## 工作流程

1. <步骤 1>
2. <步骤 2>
3. <步骤 3>

## 输入

| 参数 | 类型 | 说明 |
|------|------|------|
| arg1 | string | … |

## 输出

```
<期望输出格式，markdown / json / 文件>
```

## 引用资源

- `references/<file>.md`：<说明>
- `scripts/<file>.sh`：<说明>
- `examples/<file>`：<说明>

## 错误处理

| 场景 | 处理 |
|------|------|
| 输入缺字段 | escalate-user，不要猜测 |
| 工具失败 | 重试 ≤ N 次，仍失败则记录到 .handoff/ |

## 检查清单

- [ ] 描述里有 3+ 触发关键词
- [ ] 主体 ≤ 2000 词；超出移到 references/
- [ ] 输出格式可被下游 skill / agent 直接消费
- [ ] 边界明确（"不"适用于 X）
