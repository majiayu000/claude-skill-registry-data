---
name: ielts-practice
description: 说明如何发现和调用 IELTS Buddy 考场记录、预测候选题、题库目录、练习记录与结果接口；不定义选题、复盘或教学策略。
---

# IELTS Buddy 练习接口

本 Skill 只说明浏览器练习相关的目录和只读记录接口。个人数据调用前，先按[Agent API 配置](references/setup.md)绑定并检查能力。

## 接口

| 能力 | 数据或动作 | 调用约束 |
| --- | --- | --- |
| `ielts_prediction_search_hits` | 公开考场记录及可能对应的题目 | 可无需 Token；保留来源和回忆信息，只使用服务端返回的候选题及可选练习入口。 |
| `ielts_practice_list_taxonomy`、`ielts_practice_search_parts`、`ielts_practice_read_part` | 题库分类、目录和非答案内容 | 不在聊天中复刻完整试题。 |
| `ielts_dictation_search_materials` | 可逐句精听的听力素材目录与 `contentRef` | 只返回素材事实，不创建精听运行或浏览器入口。 |
| `ielts_practice_recent_activity`、`ielts_practice_read_session` | 当前账号 session 状态 | 只读取当前账号数据。 |
| `ielts_review_read_snapshot` | 已提交 session 的作答、答案 key 和可选材料 | 服务端不提供错因、证据或教学结论。 |

```sh
python3 scripts/ielts_buddy_api.py capabilities
python3 scripts/ielts_buddy_api.py call ielts_practice_search_parts --json '{"subject":"reading","limit":1}'
```

## 边界

- 一条预测命中结果由“考场记录”和 `candidates` 两层组成。`source`、`title`、`recallContent`、日期与考点属于来源记录，不能与候选题合并成同一事实。
- `candidates` 是可能对应的题目，`matchScore` 只表示匹配值，不代表来源平台确认命中。展示时保留服务端返回的全部候选，不只取第一项，也不自行设置第二层阈值。
- 候选题的 `practiceUrl` 是可选项；只有非空时才提供做题入口。没有做题入口不影响考场记录或候选题本身的有效性。
- 三个月以前的考场记录仍可查询，但服务端不再对其执行题库匹配；返回空 `candidates` 属于正常结果。
- Token 只用于数据接口；浏览器网页登录态只用于练习页面，两者不可互换。
- Agent 不创建、填写或提交正式练习；用户在浏览器刷题中心手动开始、作答和交卷，Agent 在完成后读取权威记录。
- 题库来源只使用 `search_parts` 返回的 `origin.questionBank`、`origin.sourceBook`、`origin.sourceTest` 和 `origin.sourceUnit`；不要从标题或普通标签推断来源。
- 本 Skill 不定义选题、诊断、复盘或学习计划。
- `workflows/` 是独立的可选推荐层，不属于本 Skill 的接口契约。

## 列表与详情

查询学习记录分两步：先读取列表摘要，再按需用返回的 `reviewTarget` 调用 `ielts_review_read_snapshot` 查看某次练习或某个已完成模考科目的详情；精听使用 `attemptId` 调用 `ielts_dictation_read_attempt`，未提交普通练习使用 `sessionId` 调用 `ielts_practice_read_session`。不要为了列出记录逐条展开详情。使用前以当前账号的 capabilities 为准。

列表中的 `sessionId` 是练习次数，`partId` 是不同篇目；区分零作答、已作答未提交和已提交，不从部分题目的正确率推算 IELTS 分数。需要完整记录时按 `nextOffset`、`nextCursor` 或 `nextPage` 翻页，直到 `hasMore=false`；空页有后续游标时仍需继续。`observationTruncated=true` 或 `coverage.sourceTruncated=true` 表示数据仍不完整，不得声称查全。计划列表只含摘要，用 `planId` 调用 `ielts_study_plans_get` 获取任务页。

## 足迹与学习统计

跨产品活动使用 `ielts_footprints_list`。直接读取服务端 `summary`、`dailyCounts`、`todayCounts` 和 `total`；`activities` 只是本页，不能用它的长度或日期分布重算历史总量、热力图、连续天数及本周次数。只查询统计时无需拉完时间线。

足迹优先将 `nextCursor` 原样作为下一次请求的 `cursor`，保持 `kinds/query/timeRange` 不变。统计范围是 `statisticsScope=filtered_history`，时区是 `Asia/Shanghai`，每日计数覆盖截至 `asOf` 所在日的 28 天。同章节同日的视频进度折叠为一次展示活动，原始事件保留。

`ielts_learning_pull_events` 同步的是原始学习证据，数字 cursor 与足迹的字符串 cursor 不可互换，两者条数也不应直接比较。网页未显示记录时，先核对分页和覆盖范围，不用 `ielts_learning_push_events` 补写已经存在的事实。返回缺失字段或 `coverage.sourceTruncated=true` 时保持“不完整”的结论，以当前部署的[足迹接口文档](https://ieltsbuddy.igopx.cn/developers/api/ielts_footprints_list)为准。
