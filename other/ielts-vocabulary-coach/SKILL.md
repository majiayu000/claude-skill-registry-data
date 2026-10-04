---
name: ielts-vocabulary-coach
description: 说明如何读取、维护、导入导出和记录 IELTS Buddy 内置或个人词汇数据；不定义词汇教学或复习策略。
---

# IELTS Buddy 词汇数据接口

本 Skill 只说明词汇数据接口。调用前，先按[Agent API 配置](references/setup.md)绑定并检查能力。

## 接口

| 能力组 | 数据或动作 | 调用约束 |
| --- | --- | --- |
| `ielts_vocabulary_builtin_prepare_cards`、`ielts_vocabulary_builtin_progress`、`ielts_vocabulary_builtin_record_review` | 内置词书卡片与复习进度 | 仅记录实际完成的复习结果。 |
| `ielts_vocabulary_personal_search`、`ielts_vocabulary_personal_prepare_cards`、`ielts_vocabulary_personal_progress` | 当前账号个人词汇数据 | 仅读取当前账号数据。 |
| `ielts_vocabulary_personal_add`、`ielts_vocabulary_personal_update`、`ielts_vocabulary_personal_delete`、`ielts_vocabulary_personal_import`、`ielts_vocabulary_personal_export` | 个人词汇维护与迁移 | 写入、删除或导入前须取得用户明确确认。 |
| `ielts_vocabulary_personal_record_review` | 实际完成的个人词汇复习结果 | 不将推荐或推断记作复习。 |

```sh
python3 scripts/ielts_buddy_api.py capabilities
python3 scripts/ielts_buddy_api.py call ielts_vocabulary_personal_search --json '{}'
```

## 边界

- 仅迁移词汇内容，不推断或迁移未证实的复习进度。
- `update` 只修改词条内容；学习状态只能由实际 `record_review` 结果推进。
- 本 Skill 不定义出题、提示、反馈或复习频率。
- `workflows/` 是独立的可选推荐层，不属于本 Skill 的接口契约。
