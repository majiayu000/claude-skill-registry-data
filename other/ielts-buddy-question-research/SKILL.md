---
name: ielts-buddy-question-research
description: 在已绑定且具备 IELTS Buddy 后台题库权限的账号下，发现并调用只读题库数据接口；不定义题库研究或分析方法。
---

# IELTS Buddy 题库数据接口

本 Skill 只说明题库数据接口、授权和字段使用。它不规定研究方法、分析流程、结论形式或后续动作。

## 访问

使用普通 `bind`、`IELTS_BUDDY_TOKEN` 和 `/api/v1/agent`。先执行：

```sh
python3 scripts/ielts_buddy_api.py capabilities
```

仅当当前账号返回下列能力时才可调用；未返回即停止，不尝试使用数据库、Cookie、私有接口或普通刷题接口绕过权限。详情见[访问边界](references/access.md)。

## 接口

| 能力 | 数据 | 调用约束 |
| --- | --- | --- |
| `ielts_question_research_coverage` | 标签维度的 Part 与题目数量 | 可传 `subject`、`groupCodes`、`scope`。 |
| `ielts_question_research_list_parts` | Part 目录、科目、难度、来源更新时间、标签和题目数 | 使用返回的 `nextOffset` 翻页。 |
| `ielts_question_research_read_parts` | 指定 Part 的题干、材料、题型、标签、来源和可选答案解析 | 只传已确定的 `partIds`；不需要答案时设 `includeAnswers:false`。 |

```sh
python3 scripts/ielts_buddy_api.py call ielts_question_research_coverage --json '{"subject":"reading"}'
python3 scripts/ielts_buddy_api.py call ielts_question_research_list_parts --json '{"subject":"reading","limit":20,"offset":0}'
python3 scripts/ielts_buddy_api.py call ielts_question_research_read_parts --json '{"partIds":[123],"includeAnswers":false}'
```

## 边界

- 只读；不导入、修改、发布、隐藏或归档题库内容。
- 不返回做题记录、正确率或用户行为数据。
- `workflows/` 是独立的可选推荐层，不属于本 Skill 的接口契约。
