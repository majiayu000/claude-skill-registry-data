---
name: ielts-writing-review
description: 说明如何读取 IELTS Buddy 浏览器写作练习的不可变版本与结构化批改结果；不定义本地批改方法。
---

# IELTS Buddy 写作数据接口

本 Skill 只说明写作练习的只读数据接口。调用前，先按[Agent API 配置](references/setup.md)绑定并检查能力。

## 接口

| 能力 | 数据或动作 | 调用约束 |
| --- | --- | --- |
| `ielts_writing_read_practice` | 指定 `sessionId` 的不可变版本和结构化教师批改结果 | 只读取当前账号数据；使用返回的版本字段陈述事实。 |

```sh
python3 scripts/ielts_buddy_api.py capabilities
python3 scripts/ielts_buddy_api.py call ielts_writing_read_practice --json '{"sessionId":123}'
```

## 边界

- 正式写作提交和修订由用户在浏览器练习页完成；Agent 不代替用户提交版本或触发正式批改。
- 本 Skill 只定义服务端写作练习接口，不规定本地审题、评分、改写或后续练习流程。
- `workflows/` 是独立的可选推荐层，不属于本 Skill 的接口契约。
