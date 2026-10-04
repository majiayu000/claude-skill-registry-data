---
name: ielts-study-plan
description: 说明如何读取和写入 IELTS Buddy 学习计划、精确课程与练习内容、任务提醒、学习路径、资源和学习事件；不定义诊断、推荐或计划内容。
---

# IELTS Buddy 学习数据接口

本 Skill 只说明学习数据接口。调用前，先按[Agent API 配置](references/setup.md)绑定并检查当前账号实际可用的能力。

## 接口

| 能力组 | 数据或动作 | 调用约束 |
| --- | --- | --- |
| `ielts_study_plans_list`、`ielts_study_plans_get` | 读取计划和完整任务 | 使用返回的精确 `planId`、任务 ID 与 revision，不猜 ID；下一项由调用方根据事实选择。 |
| `ielts_courses_search_sections`、`ielts_practice_search_parts`、`ielts_dictation_search_materials`、`ielts_mock_search_papers` | 发现可写入计划的精确内容与稳定 `contentRef` | 内容由调用方选择；服务端只返回事实候选。 |
| `ielts_study_plans_create` | 从已选定任务创建计划 | 每项任务必须包含服务端返回的 `contentRef`、中国日历日期和 `morning`、`afternoon` 或 `evening` 时段。 |
| `ielts_study_plans_update`、`ielts_study_plans_change_tasks`、`ielts_study_plans_replan`、`ielts_study_plans_delete` | 修改标题/目标，原子增改删完任务，重排未完成任务或删除计划 | 写入前读取计划；`change_tasks` 不是局部计划 patch，`replan` 会整体替换未完成任务。 |
| `ielts_notifications_get_status`、`ielts_notifications_configure_wechat_task_reminders` | 读取微信 iLink 状态，为现有任务启停微信投递 | 只传精确 `taskId`；提醒工具不创建任务，也不修改日期或时段。 |
| `ielts_learning_route_read`、`ielts_learner_read_profile`、`ielts_learning_pull_events` | 学习路径、画像和历史事实 | 路径用 `view:"route"` 或 `view:"progress"`；缺失字段保持未知，不补造数据。 |
| `ielts_assets_search`、`ielts_resources_related`、`ielts_prep_search_guides`、`ielts_prep_read_guide`、`ielts_prediction_search_hits` | 用户资产、备考内容、考场记录、候选题及关联资源 | 保持考场记录与候选题分层，仅使用服务端返回的记录、`contentRef` 和可选链接。 |
| `ielts_learning_push_events` | 记录已经发生且有证据的学习事件 | 不把建议、草案或推断写成事件。 |

```sh
python3 scripts/ielts_buddy_api.py capabilities
python3 scripts/ielts_buddy_api.py call ielts_study_plans_list --json '{}'
```

## 边界

- 计划的目标、优先级和任务内容由调用方与用户决定；服务端只保存经确认的数据。
- 描述已保存的计划时，以接口最近返回的实际任务、日期、时段、时长和状态为准，不把草案或推测说成已保存事实；只有写入接口成功后才能宣称已创建或修改，分页结果不代表完整计划，已有结果足够时无需重复查询。
- `contentRef` 只接受 `practice_part`、`mock_paper`、`course_section` 或 `listening_dictation`；直接复用目录工具返回的对象，不手工补全内容快照。
- 修改计划标题或目标使用 `update`；改变具体任务使用 `change_tasks`；整体替换未完成安排使用 `replan`，不要混用。
- `workflows/` 是独立的可选推荐层，不属于本 Skill 的接口契约。

## 列表与详情

查询学习记录分两步：先读取列表摘要，再按需用返回的 `reviewTarget` 调用 `ielts_review_read_snapshot` 查看某次练习或某个已完成模考科目的详情；精听使用 `attemptId` 调用 `ielts_dictation_read_attempt`，未提交普通练习使用 `sessionId` 调用 `ielts_practice_read_session`。不要为了列出记录逐条展开详情。使用前以当前账号的 capabilities 为准。

列表中的 `sessionId` 是练习次数，`partId` 是不同篇目；区分零作答、已作答未提交和已提交，不从部分题目的正确率推算 IELTS 分数。需要完整记录时按 `nextOffset`、`nextCursor` 或 `nextPage` 翻页，直到 `hasMore=false`；空页有后续游标时仍需继续。`observationTruncated=true` 或 `coverage.sourceTruncated=true` 表示数据仍不完整，不得声称查全。计划列表只含摘要，用 `planId` 调用 `ielts_study_plans_get` 获取任务页。

## 足迹与学习统计

跨产品活动使用 `ielts_footprints_list`。直接读取服务端 `summary`、`dailyCounts`、`todayCounts` 和 `total`；`activities` 只是本页，不能用它的长度或日期分布重算历史总量、热力图、连续天数及本周次数。只查询统计时无需拉完时间线。

足迹优先将 `nextCursor` 原样作为下一次请求的 `cursor`，保持 `kinds/query/timeRange` 不变。统计范围是 `statisticsScope=filtered_history`，时区是 `Asia/Shanghai`，每日计数覆盖截至 `asOf` 所在日的 28 天。同章节同日的视频进度折叠为一次展示活动，原始事件保留。

`ielts_learning_pull_events` 同步的是原始学习证据，数字 cursor 与足迹的字符串 cursor 不可互换，两者条数也不应直接比较。网页未显示记录时，先核对分页和覆盖范围，不用 `ielts_learning_push_events` 补写已经存在的事实。返回缺失字段或 `coverage.sourceTruncated=true` 时保持“不完整”的结论，以当前部署的[足迹接口文档](https://ieltsbuddy.igopx.cn/developers/api/ielts_footprints_list)为准。
