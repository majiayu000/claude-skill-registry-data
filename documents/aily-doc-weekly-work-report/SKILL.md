---
name: aily-doc-weekly-work-report
label: 工作周报
description: 基于飞书生态的**每周周报**自动生成 Skill：从当周**日程、任务、妙记、云文档**中提取工作内容，使用 `knowledge_answer` 兜底补全遗漏信息，最终调用 `doc_agent (writer)` 生成结构化的飞书云文档周报。
---

# SKILL: aily-doc-weekly-work-report

基于飞书生态的**每周周报**自动生成 Skill：从当周**日程、任务、妙记、云文档**中提取工作内容，使用 `knowledge_answer` 兜底补全遗漏信息，最终调用 `doc_agent (writer)` 生成结构化的飞书云文档周报。

---

## 1) Overview

### ⚠️ 输出形式（强制）
- **本 skill 被触发即代表用户期望生成飞书云文档**，主 Agent 无需询问用户是否需要写成文档，也不得以对话文本替代文档作为最终交付物。
- 数据收集完成后，必须通过 `task`（subagent_type: writer）委托 Writer Agent 创建飞书云文档。

### 飞书工具优先（必须遵守）
- 所有飞书相关信息获取与写作，先参考 `feishu-use-skills-map` 并按其指引调用对应技能
- 需要访问飞书文档/群消息/会议/任务时，必须先 `get_skills` 获取对应飞书技能说明
- 本 Skill 是飞书生态工具最密集的 Skill 之一，涉及日程、任务、妙记、云文档、知识库五大数据源

### 工具/Skill 明确清单（执行前先 get_skills）

| Agent | 工具名 | 用途 | 使用阶段 |
|-------|--------|------|----------|
| 主 Agent | `aily-calendar` | 获取日程/会议事件 | A1 日程获取 |
| 主 Agent | `aily_lark_task` (MCP) | 获取任务列表及状态 | A2 任务获取 |
| 主 Agent | `minute` (MCP) | 获取妙记/会议纪要 | A3 妙记获取 |
| 主 Agent | `aily-doc` | 搜索/列出云文档 | A4 云文档获取 |
| 主 Agent | `knowledge_answer` | 兜底补全遗漏信息 | A5 兜底补全 |
| 主 Agent | `todo_write` | 分解任务清单 | 任务规划 |
| 主 Agent | `file` | 写入 draft.md 素材 | A1-A5 + B |
| 主 Agent | `task` | 分发写作任务给 Writer Agent | C 调用 Writer |
| Writer Agent | `file_read` | 读取 draft.md | 读取素材 |
| Writer Agent | `outline_generator` | 生成文档大纲 | 规划结构 |
| Writer Agent | `feishu_doc_create` | 生成飞书云文档 | 最终输出 |

> **说明**：`aily-calendar` 必要时可用 `resources` 获取妙记/共享文档关联信息；`minute` MCP 适用于已有妙记链接的场景。

### 证据与时间约束（主/写作 Agent 一致）
- 任何数据/结论必须来自可追溯来源；不确定则明确标注"需补充资料"
- 若用户指定时间范围，必须严格筛选在时间窗内的资料，过期内容不得使用
- 不可编造事实、链接或来源；引用必须有明确出处

### 可读性规则（强制）
- 并列项 >= 3：优先使用无序/有序列表或表格
- 单段 > 150 字必须拆分（列表/小节/Callout）
- 连续两段无列表且信息密度高：插入列表或 Callout

### 触发方式（Triggers）
- "帮我生成本周周报"
- "总结一下我这周的工作"
- "把这周的日程、任务、会议整理成周报"
- "生成 {start_date} 到 {end_date} 的周报"

### 时间窗口（Week Window）
- **默认**：本周（周一 00:00:00 至周日 23:59:59），按用户时区
- **自定义**：用户可指定具体日期范围
- 周报必须标注：`统计区间：{week_start_date}（周一）~ {week_end_date}（周日）`

### 核心输出（Deliverables）
- **飞书云文档周报**：结构标准、内容翔实、可追溯

### 质量标准
- **完整性**：日程、任务、妙记、云文档四类来源均覆盖
- **洞察优先**：不做流水账，每类来源产出 insights
- **时间正确性**：严格过滤到当周窗口

---

## 2) 任务分解示例（todo_write）

主 Agent 收到周报请求后，使用 `todo_write` 分解任务：

```json
{
  "todos": [
    {"content": "获取本周日程数据并分析", "status": "in_progress"},
    {"content": "获取本周任务数据并分析", "status": "pending"},
    {"content": "获取本周妙记（会议纪要）并提取要点", "status": "pending"},
    {"content": "获取本周创建/编辑的云文档", "status": "pending"},
    {"content": "使用 knowledge_answer 兜底补全遗漏信息", "status": "pending"},
    {"content": "汇总分析结果，调用 writer agent 生成周报云文档", "status": "pending"}
  ]
}
```

---

## 3) Module A — 数据获取（主 Agent 执行）

> **核心原则**：使用 MCP 工具获取四类数据源，最后用 `knowledge_answer` 兜底。每完成一步，立即使用 `file(path: "/home/workspace/draft.md", mode: "append")` 将结果追加写入 draft.md。

### A1. 获取本周日程

**工具**：`aily-calendar`（必要时用 `resources` 获取妙记/共享文档关联信息）

**获取内容**：
- 事件标题、开始/结束时间
- 参与人
- 会议描述/备注

**时间过滤**：仅保留落在周窗口（{week_start_date} 周一 至 {week_end_date} 周日）的事件

**分析维度**：
- 会议数量与时长统计
- 按项目/主题聚类
- 高频协作对象

**写入 draft.md**（使用 `file(path: "/home/workspace/draft.md", mode: "append")`）：
```markdown
## 日程数据

### 原始数据
| 日期 | 时间 | 事件 | 参与人 |
|------|------|------|--------|
| {date} | {start_time}-{end_time} | {event_title} | {attendees} |
| ... | ... | ... | ... |

### 洞察
- 本周共 {meeting_count} 场会议，总时长约 {total_hours} 小时
- Top 3 会议主题：{topic_1}、{topic_2}、{topic_3}
- 高频协作：{collaborator_1}（{count_1}次）、{collaborator_2}（{count_2}次）
```

---

### A2. 获取本周任务

**工具**：`aily_lark_task` (MCP)

**获取内容**：
- 任务标题、负责人、状态（待办/进行中/已完成）
- 截止时间、优先级
- 更新记录

**过滤规则**：
- 本周创建的任务
- 本周完成的任务
- 本周有状态变更的任务

**分析维度**：
- 完成数 / 进行中数 / 阻塞数
- 关键完成项
- 阻塞原因与待解决事项

**写入 draft.md**（使用 `file(path: "/home/workspace/draft.md", mode: "append")`）：
```markdown
## 任务数据

### 本周完成
- [x] {task_title_1}：{task_description_1}
- [x] {task_title_2}：{task_description_2}

### 进行中
- [ ] {task_title_3}：{task_description_3}（预计下周完成）

### 阻塞
- [ ] {task_title_4}：{task_description_4} —— 阻塞原因：{block_reason}

### 洞察
- 本周完成 {completed_count} 项任务，完成率 {completion_rate}%
- 阻塞事项需关注：{blocked_task}（{block_impact}）
```

---

### A3. 获取本周妙记（会议纪要）

**工具**：`minute` (MCP)

**获取内容**：
- 会议标题、时间
- 会议摘要/纪要内容
- 决策事项、行动项

**分析维度**：
- 关键决策清单
- 待办行动项（Action Items）
- 重要讨论要点

**写入 draft.md**（使用 `file(path: "/home/workspace/draft.md", mode: "append")`）：
```markdown
## 妙记数据

### 重要会议纪要
#### 1. {meeting_title_1}（{meeting_date_1}）
- **决策**：{decision_1}
- **行动项**：{assignee_1} {action_item_1}（{deadline_1}前）
- **要点**：{key_point_1}

#### 2. {meeting_title_2}（{meeting_date_2}）
- **决策**：{decision_2}
- **行动项**：{assignee_2} {action_item_2}

### 洞察
- 本周 {minutes_count} 场会议有纪要记录
- 关键决策 {decision_count} 项，待跟进行动项 {action_count} 项
```

---

### A4. 获取本周云文档活动

**工具**：`aily-doc`（通过 `get_skills` 获取技能后调用）

**检索方式**：
```
通过 aily-doc 搜索飞书云文档：
- 过滤条件：owner_name = "{current_user}"
- 时间范围：create_time = "[{week_start_date}, {week_end_date}]"（本周范围）
```

**获取内容**：
- 文档标题、链接
- 创建/更新时间
- 文档类型（文档/表格/幻灯片）

**分析维度**：
- 本周创建的文档（产出）
- 本周编辑的文档（贡献）
- 文档分类（需求文档/技术方案/会议纪要/其他）

**写入 draft.md**（使用 `file(path: "/home/workspace/draft.md", mode: "append")`）：
```markdown
## 云文档活动

### 本周创建
| 文档标题 | 类型 | 链接 |
|---------|------|------|
| {doc_title_1} | {doc_type_1} | [链接]({doc_url_1}) |
| {doc_title_2} | {doc_type_2} | [链接]({doc_url_2}) |

### 本周编辑
| 文档标题 | 更新内容 |
|---------|---------|
| {edited_doc_title} | {edit_summary} |

### 洞察
- 本周产出 {created_doc_count} 篇文档
- 主要产出类型：{doc_category_1}（{category_1_count}篇）、{doc_category_2}（{category_2_count}篇）
```

---

### A5. Knowledge Answer 兜底

**工具**：`knowledge_answer`

**查询策略**（在前4步完成后执行）：
```
knowledge_answer(
  query_list: ["总结我本周（{week_start_date}到{week_end_date}）的主要工作内容和产出"],
  explanation: "兜底补全可能遗漏的本周工作信息"
)
```

**使用规则**：
- 作为**补充来源**，不替代前4步的事实数据
- 若 knowledge_answer 返回的信息与前4步冲突，以 MCP 数据为准
- 若发现前4步遗漏的重要信息，补充到 `draft.md`

**写入 draft.md**（使用 `file(path: "/home/workspace/draft.md", mode: "append")`）：
```markdown
## Knowledge Answer 补充

### 补充信息
- [补充] {supplementary_item_1}（未在{missing_source_1}中体现）
- [补充] {supplementary_item_2}（未在{missing_source_2}中体现）

### 与事实源对照
- 一致：日程、任务、妙记信息与 knowledge_answer 基本吻合
- 补充：发现 {supplement_count} 项遗漏，已补入对应章节
```

---

## 4) Module B — 汇总分析（主 Agent 执行）

在获取完所有数据后，主 Agent 使用 `file(path: "/home/workspace/draft.md", mode: "append")` 在 `draft.md` 末尾生成**全局汇总**：

```markdown
## 全局汇总

### 本周主题
- 主线1：{main_theme_1}
- 主线2：{main_theme_2}

### 关键产出
1. {key_output_1}
2. {key_output_2}
3. {key_output_3}

### 待解决问题
1. {pending_issue_1}
2. {pending_issue_2}

### 下周计划
1. 【高】{high_priority_plan}
2. 【中】{medium_priority_plan}
3. 【低】{low_priority_plan}
```

---

## 5) Module C — 调用 Writer Agent 生成周报

### 任务分发

主 Agent 完成数据收集与汇总后，调用 `task` 工具分发给 Writer Agent：

```json
{
  "description": "生成本周周报云文档",
  "prompt": "基于 /home/workspace/draft.md 中的周报素材，生成一份飞书云文档周报。\n\n要求：\n1. 严格按照周报模板结构\n2. 统计区间：{week_start_date} ~ {week_end_date}\n3. 突出洞察和结论，避免流水账\n4. 所有数据来源于 draft.md，不要编造\n\n周报模板见下方。",
  "subagent_type": "writer"
}
```

### Writer Agent 执行流程

Writer Agent 收到任务后，按以下步骤执行：

1. **file_read**：读取 `/home/workspace/draft.md` 完整内容
2. **outline_generator**：基于周报模板生成飞书文档大纲
3. **feishu_doc_create**：按模板结构生成飞书云文档，内容来源于 draft.md
4. **end**：返回飞书云文档链接，结束任务

---

## 6) 周报模板（Writer Agent 遵循）

Writer Agent 使用 `feishu_doc_create` 生成飞书云文档时，**必须遵循以下模板结构**：

```markdown
# 周报：{week_start_date} ~ {week_end_date}

> 👤 {user_name}
> 📅 统计区间：{week_start_year}年{week_start_month}月{week_start_day}日（周一）~ {week_end_year}年{week_end_month}月{week_end_day}日（周日）
> 🕐 生成时间：{generated_datetime}

---

## 📌 本周摘要

<!-- 3-5 条核心要点，高度概括 -->

- **主线工作**：本周主要推进 {main_work_1}、{main_work_2} 两个方向
- **关键产出**：完成 {key_deliverable_1}、产出 {key_deliverable_2}
- **待解决**：{pending_issue} 事项阻塞，需协调
- **下周重点**：{next_week_focus_1}、{next_week_focus_2}

---

## 📊 一周概览

| 维度 | 数据 |
|------|------|
| 会议数量 | {meeting_count} 场（约 {meeting_hours} 小时） |
| 完成任务 | {completed_task_count} 项 |
| 进行中任务 | {in_progress_task_count} 项 |
| 阻塞任务 | {blocked_task_count} 项 |
| 产出文档 | {doc_count} 篇 |

---

## 📅 日程与会议

### 重点会议

| 日期 | 会议 | 关键结论 |
|------|------|---------|
| {meeting_date_1} | {meeting_name_1} | {meeting_conclusion_1} |
| {meeting_date_2} | {meeting_name_2} | {meeting_conclusion_2} |

### 洞察
- 本周会议集中在 {meeting_focus_area} 方向
- 高频协作对象：{top_collaborator_1}、{top_collaborator_2}

---

## ✅ 任务进展

### 本周完成
- [x] **{completed_task_1}**：{completed_desc_1}（关联项目：{project_1}）
- [x] **{completed_task_2}**：{completed_desc_2}

### 进行中
- [ ] **{ongoing_task_1}**：{ongoing_desc_1} —— 预计下周完成

### 阻塞事项
| 任务 | 阻塞原因 | 解决方案 |
|------|---------|---------|
| {blocked_task_name} | {block_reason} | {resolution_plan} |

---

## 🎙️ 会议纪要要点

### 关键决策
| 会议 | 决策内容 | 决策时间 |
|------|---------|---------|
| {decision_meeting} | {decision_content} | {decision_date} |

### 待跟进行动项
| 行动项 | 负责人 | 截止时间 |
|--------|-------|---------|
| {action_item} | {action_owner} | {action_deadline} |

---

## 📄 文档产出

### 本周创建
| 文档名称 | 类型 | 链接 |
|---------|------|------|
| {created_doc_title_1} | {created_doc_type_1} | [查看]({created_doc_url_1}) |
| {created_doc_title_2} | {created_doc_type_2} | [查看]({created_doc_url_2}) |

### 本周贡献
- 编辑 **{edited_doc_name}**：{edit_detail}
- 评审 **{reviewed_doc_name}**：{review_detail}

---

## ⚠️ 风险与问题

| 风险/问题 | 影响 | 应对措施 |
|----------|------|---------|
| {risk_1} | {risk_impact_1} | {risk_mitigation_1} |
| {risk_2} | {risk_impact_2} | {risk_mitigation_2} |

---

## 📋 下周计划

### 优先级排序

| 优先级 | 事项 | 预期产出 |
|--------|------|---------|
| 🔴 高 | {high_plan} | {high_output} |
| 🟡 中 | {medium_plan} | {medium_output} |
| 🟢 低 | {low_plan} | {low_output} |

### 关键里程碑
- **{milestone_date_1}**：{milestone_1}
- **{milestone_date_2}**：{milestone_2}

---

## 📎 附录

### 重要链接
- [{link_title_1}]({link_url_1})
- [{link_title_2}]({link_url_2})
- [{link_title_3}]({link_url_3})
```

---

## 7) 执行流程图

```
用户: "帮我生成本周周报"
          ↓
┌─────────────────────────────────────────────────────────────┐
│                    主 Agent 执行                              │
├─────────────────────────────────────────────────────────────┤
│ 1. todo_write: 分解任务（6 步）                               │
│ 2. aily-calendar → 分析日程 → file(draft.md, append)   │
│ 3. aily_lark_task → 分析任务 → file(draft.md, append)  │
│ 4. minute → 分析妙记 → file(draft.md, append)          │
│ 5. aily-doc → 分析云文档 → file(draft.md, append)      │
│ 6. knowledge_answer → 兜底补全 → file(draft.md, append)│
│ 7. 汇总分析（Module B） → file(draft.md, append)       │
│ 8. task(writer): 分发写作任务                                │
└─────────────────────────────────────────────────────────────┘
          ↓
┌─────────────────────────────────────────────────────────────┐
│                    Writer Agent 执行                         │
├─────────────────────────────────────────────────────────────┤
│ 1. file_read: 读取 /home/workspace/draft.md                  │
│ 2. outline_generator: 生成大纲（基于周报模板）                │
│ 3. feishu_doc_create: 生成飞书云文档周报                      │
│ 4. end: 返回文档链接，结束                                   │
└─────────────────────────────────────────────────────────────┘
          ↓
      飞书云文档周报
```

---

## 8) Checklist

### 主 Agent 检查项
- [ ] 日程数据已通过 `aily-calendar` 获取并 `file` 写入 draft.md
- [ ] 任务数据已通过 `aily_lark_task` 获取并 `file` 写入 draft.md
- [ ] 妙记数据已通过 `minute` 获取并 `file` 写入 draft.md
- [ ] 云文档活动已通过 `aily-doc` 获取并 `file` 写入 draft.md
- [ ] `knowledge_answer` 兜底已执行并 `file` 写入 draft.md
- [ ] 全局汇总（Module B）已生成并 `file` 写入 draft.md
- [ ] 已调用 `task(writer)` 分发写作任务

### Writer Agent 检查项
- [ ] 已通过 `file_read` 读取 draft.md 完整内容
- [ ] 已通过 `outline_generator` 生成周报大纲
- [ ] 周报结构严格符合模板（📌📊📅✅🎙️📄⚠️📋📎 各节齐全）
- [ ] 统计区间标注正确：{week_start_date} ~ {week_end_date}
- [ ] 所有数据来源于 draft.md，无编造
- [ ] 已通过 `feishu_doc_create` 生成飞书云文档

---

## 9) 常见失败模式与修复

| 失败模式 | 原因 | 修复方法 |
|---------|------|---------|
| 数据缺失 | MCP 工具调用失败或返回空 | 使用 `knowledge_answer` 兜底；在 draft.md 中标注"该来源暂无数据" |
| 内容流水账 | 缺少分析，直接罗列原始数据 | 每类数据必须有"洞察"小节，提炼 insights |
| 时间范围错误 | 未正确设置过滤条件 | 检查日期参数，确保是 {week_start_date}（周一）至 {week_end_date}（周日） |
| 周报结构混乱 | Writer 未遵循模板 | 在 task prompt 中明确要求遵循模板，Checklist 逐项验证 |
| 信息重复 | draft.md 中多来源有冗余 | Module B 汇总时去重，合并同类信息后再调用 Writer |
| draft.md 未写入 | 忘记调用 file | 每个 Module A 子步骤完成后立即 `file(path: "/home/workspace/draft.md", mode: "append")` |
| knowledge_answer 覆盖事实 | 兜底信息与 MCP 数据冲突 | 以 MCP 数据为准，knowledge_answer 仅作补充 |
