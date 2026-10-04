---
name: ielts-mock-review
description: 说明如何读取 IELTS Buddy 模考与已提交练习的事实数据；不定义模考解读、诊断或训练优先级。
---

# IELTS Buddy 模考数据接口

本 Skill 只说明模考和练习结果的数据读取。需要账号数据时，先按[Agent API 配置](references/setup.md)绑定并检查能力。

## 接口

| 能力 | 数据 | 调用约束 |
| --- | --- | --- |
| `ielts_mock_search_papers` | 当前账号可见的模考试卷目录与稳定 `contentRef` | 可传 `subjects`、`maxDurationMinutes`、`limit`；只读目录，不创建模考 session。 |
| `ielts_review_recent_activity` | 可复盘记录和已完成科目的 `reviewTargets` | 传 `kind:"mock"`，按返回的 `nextOffset` 分页。 |
| `ielts_review_read_snapshot` | 指定模考科目的逐题作答和批改快照 | 把列表中的一个 `reviewTargets` 元素原样作为 `target`；材料按需读取。 |

```sh
python3 scripts/ielts_buddy_api.py capabilities
python3 scripts/ielts_buddy_api.py call ielts_review_recent_activity --json '{"kind":"mock"}'
```

## 边界

- 返回的数据不是 IELTS 官方成绩。
- 模考只读取列表已返回复盘引用的完成科目；不要自行把未完成科目当作已提交结果。
- 本 Skill 不生成能力判断、修复任务或后续计划。
- `workflows/` 是独立的可选推荐层，不属于本 Skill 的接口契约。

## 列表与详情

查询学习记录分两步：先读取列表摘要，再按需用返回的 `reviewTarget` 调用 `ielts_review_read_snapshot` 查看某次练习或某个已完成模考科目的详情；精听使用 `attemptId` 调用 `ielts_dictation_read_attempt`，未提交普通练习使用 `sessionId` 调用 `ielts_practice_read_session`。不要为了列出记录逐条展开详情。使用前以当前账号的 capabilities 为准。

列表中的 `sessionId` 是练习次数，`partId` 是不同篇目；区分零作答、已作答未提交和已提交，不从部分题目的正确率推算 IELTS 分数。需要完整记录时按 `nextOffset`、`nextCursor` 或 `nextPage` 翻页，直到 `hasMore=false`；空页有后续游标时仍需继续。`observationTruncated=true` 或 `coverage.sourceTruncated=true` 表示数据仍不完整，不得声称查全。计划列表只含摘要，用 `planId` 调用 `ielts_study_plans_get` 获取任务页。

## 足迹与学习统计

跨产品活动使用 `ielts_footprints_list`。直接读取服务端 `summary`、`dailyCounts`、`todayCounts` 和 `total`；`activities` 只是本页，不能用它的长度或日期分布重算历史总量、热力图、连续天数及本周次数。只查询统计时无需拉完时间线。

足迹优先将 `nextCursor` 原样作为下一次请求的 `cursor`，保持 `kinds/query/timeRange` 不变。统计范围是 `statisticsScope=filtered_history`，时区是 `Asia/Shanghai`，每日计数覆盖截至 `asOf` 所在日的 28 天。同章节同日的视频进度折叠为一次展示活动，原始事件保留。

`ielts_learning_pull_events` 同步的是原始学习证据，数字 cursor 与足迹的字符串 cursor 不可互换，两者条数也不应直接比较。网页未显示记录时，先核对分页和覆盖范围，不用 `ielts_learning_push_events` 补写已经存在的事实。返回缺失字段或 `coverage.sourceTruncated=true` 时保持“不完整”的结论，以当前部署的[足迹接口文档](https://ieltsbuddy.igopx.cn/developers/api/ielts_footprints_list)为准。
