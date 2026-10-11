---
name: aily-doc-group-chat-summary
label: 群聊内容摘要
description: 基于飞书群聊的**智能摘要与洞察**生成能力。从指定群聊/时间范围的消息中提取关键信息，识别决策、行动项、风险，生成**飞书云文档结构化摘要**。
---

# SKILL: aily-doc-group-chat-summary

基于飞书群聊的**智能摘要与洞察**生成能力。从指定群聊/时间范围的消息中提取关键信息，识别决策、行动项、风险，生成**飞书云文档结构化摘要**。

---

## 1) Overview

### ⚠️ 输出形式（强制）
- **本 skill 被触发即代表用户期望生成飞书云文档**，主 Agent 无需询问用户是否需要写成文档，也不得以对话文本替代文档作为最终交付物。
- 数据收集完成后，必须通过 `task`（subagent_type: writer）委托 Writer Agent 创建飞书云文档。

### 飞书工具优先（必须遵守）
- 所有飞书相关信息获取与写作，先参考 `feishu-use-skills-map` 并按其指引调用对应技能
- 需要访问飞书文档/群消息/会议/任务时，必须先 `get_skills` 获取对应飞书技能说明
- 禁止绕过飞书工具直接构造 API 请求

### 工具/Skill 明确清单（执行前先 get_skills）

| Agent | 工具名 | 用途 | 使用阶段 |
|-------|--------|------|---------|
| 主 Agent | `aily-im`（search-chats） | 搜索/定位目标群聊 | Module A |
| 主 Agent | `aily-im`（list-messages / search-messages） | 拉取群聊消息 | Module A |
| 主 Agent | `aily-im`（提取链接） → `fetch` / `aily-doc` | 获取群内分享的云文档内容 | Module A |
| 主 Agent | `aily-user` | 查询用户信息（姓名、部门） | Module A / B |
| 主 Agent | `knowledge_answer` | 补充历史决策、项目背景等上下文 | Module A / B |
| 主 Agent | `todo_write` | 分解任务、追踪执行进度 | 全流程 |
| 主 Agent | `file` | 写入 draft.md 素材 | Module A / B |
| 主 Agent | `task`（subagent_type: writer） | 分发写作任务给 Writer Agent | Module C |
| Writer Agent | `file_read` | 读取 draft.md | Module C |
| Writer Agent | `outline_generator` | 生成文档大纲 | Module C |
| Writer Agent | `feishu_doc_create` | 创建飞书云文档 | Module C |

### 证据与时间约束（与主/写作 Agent 一致）
- 任何数据/结论必须来自可追溯来源；不确定则明确标注"需补充资料"
- 若用户指定时间范围，必须严格筛选在时间窗内的资料，过期内容不得使用
- 不可编造事实、链接或来源；引用必须有明确出处

### 可读性规则（强制）
- 并列项 >= 3：优先使用无序/有序列表或表格
- 单段 > 150 字必须拆分（列表/小节/Callout）
- 连续两段无列表且信息密度高：插入列表或 Callout

### 触发方式（Triggers）
- "帮我总结一下 {群名} 群的聊天记录"
- "把这个群最近一周的讨论整理成摘要"
- "总结今天群里的重要决策和待办事项"
- "帮我追踪 {群名} 群里关于 {话题} 的讨论"

### 输入（Inputs）
- **必选**：群聊标识（群名 / 群 ID / 群链接）
- **可选**：
  - 时间范围（默认：过去 24 小时）
  - 关注主题/关键词
  - 输出粒度（简洁版 / 标准版 / 详细版）

### 核心输出（Deliverables）
- **飞书云文档群聊摘要**：结构化、可追溯、行动项可执行

### 质量标准
- **完整性**：不遗漏关键决策与行动项
- **准确性**：可回溯到原始消息
- **可操作**：行动项有 Owner / 截止时间
- **时效性**：严格遵守用户指定的时间窗口

---

## 2) 任务分解示例（todo_write）

主 Agent 收到群聊摘要请求后，使用 `todo_write` 分解任务：

```json
{
  "todos": [
    {"content": "确定目标群聊和时间范围", "status": "in_progress"},
    {"content": "获取群聊消息（aily-im）", "status": "pending"},
    {"content": "预处理：去噪、分段、去重", "status": "pending"},
    {"content": "结构化提取：议题/决策/行动项/风险/链接", "status": "pending"},
    {"content": "整理素材，写入 draft.md", "status": "pending"},
    {"content": "调用 writer agent 生成摘要云文档", "status": "pending"}
  ]
}
```

---

## 3) Module A — 消息获取（主 Agent 执行）

> **核心原则**：先拉取原始消息，再做时间过滤、去噪、分段。所有数据写入 draft.md 以供后续模块使用。

### A1. 定位目标群聊

**工具调用**：`aily-im`（search-chats）

根据用户提供的群名/群 ID/群链接定位目标群聊，获取群聊的 `chat_id`。

### A2. 拉取群聊消息

**工具调用**：`aily-im`（list-messages / search-messages）

按 `chat_id` + 时间范围拉取全部消息。

### A3. 时间窗口定义

**默认**：过去 24 小时（用户时区）

**支持自定义**：
- "今天" / "本周" / "最近 3 天"
- 指定起止时间："{start_time} ~ {end_time}"

**写入 draft.md** — 执行 `file(path: "/home/workspace/draft.md", mode: "append")`：
```markdown
## 群聊信息
- 群名：{群名}
- 群 ID：{chat_id}
- 统计范围：{start_date} {start_time} ~ {end_date} {end_time} (UTC+8)
- 消息总数：{msg_count} 条
- 参与人数：{user_count} 人
```

### A4. 消息预处理

**去噪规则**：
- 纯表情/贴纸：标记但不纳入主分析
- 系统消息（入群/退群/群名变更）：单独记录或忽略
- 重复消息：去重，保留首次
- 纯闲聊（问候/感谢/无实质内容）：降权处理

**消息分段**：
- 按时间间隔（> 30 分钟无消息）自动切分
- 按话题切换辅助分段
- 每段标注：起止时间、参与人、主题标签

**写入 draft.md** — 执行 `file(path: "/home/workspace/draft.md", mode: "append")`：
```markdown
## 消息分段

### 段落 1：{主题标签}
- 时间：{seg_start_time} ~ {seg_end_time}
- 参与人：{participant_list}
- 消息数：{seg_msg_count} 条
- 核心内容摘要：{segment_summary}

### 段落 2：{主题标签}
- 时间：{seg_start_time} ~ {seg_end_time}
- 参与人：{participant_list}
- 消息数：{seg_msg_count} 条
- 核心内容摘要：{segment_summary}
```

### A5. 补充上下文（可选）

**工具调用**：`knowledge_answer` / `aily-doc`

当消息中涉及项目背景、历史决策时，使用 `knowledge_answer` 或 `aily-doc` 检索关联文档，补充上下文信息写入 draft.md。

---

## 4) Module B — 结构化提取（主 Agent 执行）

> **核心原则**：提取"决策、行动、风险、资源"四类关键信息。每项必须可溯源到原始消息。

### B1. 核心议题识别

**识别方法**：
- 从讨论段落中提取主要话题（3-7 个）
- 按讨论热度（消息数、参与人数）排序
- 合并高度重叠的子话题

**写入 draft.md** — 执行 `file(path: "/home/workspace/draft.md", mode: "append")`：
```markdown
## 核心议题

| 序号 | 议题 | 热度 | 时间段 | 参与人 |
|------|------|------|--------|--------|
| 1 | {议题名称} | {高/中/低} | {time_range} | {participant_list} |
| 2 | {议题名称} | {高/中/低} | {time_range} | {participant_list} |
| ... | ... | ... | ... | ... |
```

---

### B2. 关键决策提取

**识别信号**：
- "决定..."、"确认..."、"就这样定了"、"同意"、"通过"
- 投票结果
- 领导/关键人拍板

**写入 draft.md** — 执行 `file(path: "/home/workspace/draft.md", mode: "append")`：
```markdown
## 关键决策

### 决策 1：{决策内容}
- **决策时间**：{decision_time}
- **决策人**：{decision_maker}
- **参与人**：{participant_list}
- **背景**：{decision_context}
- **原始消息**："{quoted_message}"
```

---

### B3. 行动项提取

**识别信号**：
- "@{人名} 你来负责..."、"{人名} 跟进一下"
- "我来做..."、"我负责..."
- 截止时间提及："周五前"、"明天"、"{date}"

**写入 draft.md** — 执行 `file(path: "/home/workspace/draft.md", mode: "append")`：
```markdown
## 行动项

| 任务 | 负责人 | 截止时间 | 状态 | 原始消息 |
|------|--------|---------|------|---------|
| {task_description} | {owner} | {due_date} | {status} | "{quoted_message}" |
| {task_description} | {owner} | {due_date} | {status} | "{quoted_message}" |
```

> **注意**：若消息中未明确指定负责人，填写"待分配"并将该项列入"待跟进"。

---

### B4. 风险与问题提取

**识别信号**：
- "问题是..."、"风险在于..."、"卡住了"、"阻塞"
- "谁能帮忙..."、"这个怎么解决"
- 依赖未就绪、资源不足等表述

**写入 draft.md** — 执行 `file(path: "/home/workspace/draft.md", mode: "append")`：
```markdown
## 风险与问题

### 问题 1：{问题描述}
- **严重程度**：{高/中/低}
- **提出人**：{reporter}
- **提出时间**：{report_time}
- **状态**：{待解决/已解决}
- **解决方案**：{solution}（如有）
- **原始消息**："{quoted_message}"
```

---

### B5. 重要链接与资源

**提取类型**：
- 飞书文档链接
- GitHub / GitLab 链接
- 外部链接（文章/工具）
- 文件附件

**工具调用**（可选）：对飞书文档链接使用 `aily-doc` 获取文档标题与摘要。

**写入 draft.md** — 执行 `file(path: "/home/workspace/draft.md", mode: "append")`：
```markdown
## 重要链接

| 资源 | 类型 | 分享人 | 时间 | 关联议题 |
|------|------|--------|------|---------|
| {resource_name} | {飞书文档/GitHub/外部链接} | {sharer} | {share_time} | {related_topic} |
| {resource_name} | {飞书文档/GitHub/外部链接} | {sharer} | {share_time} | {related_topic} |
```

---

## 5) Module C — 调用 Writer Agent 生成摘要

### C1. 素材完整性检查

在调用 Writer Agent 前，主 Agent 必须确认 draft.md 包含以下完整章节：
- 群聊信息（群名、时间范围、消息数、参与人数）
- 消息分段（每段含主题、时间、参与人、摘要）
- 核心议题表
- 关键决策（含决策人、时间、原始消息）
- 行动项（含负责人、截止时间、状态）
- 风险与问题
- 重要链接

### C2. 任务分发

主 Agent 完成提取后，调用 `task` 工具分发给 Writer Agent：

```json
{
  "description": "生成群聊摘要云文档",
  "prompt": "基于 /home/workspace/draft.md 中的群聊分析结果，生成一份飞书云文档群聊摘要。\n\n要求：\n1. TL;DR 放在最前面（3-5 条要点，使用 Callout 格式）\n2. 核心议题按热度排序展示\n3. 决策和行动项使用表格展示\n4. 行动项必须有负责人和截止时间\n5. 使用 Callout 突出高风险项\n6. 保留原始消息引用以支持溯源\n7. 末尾附待跟进清单\n\n摘要模板见 SKILL 文件第 6 节。",
  "subagent_type": "writer"
}
```

### C3. Writer Agent 执行流程

1. `file_read`：读取 `/home/workspace/draft.md`
2. `outline_generator`：基于 draft.md 生成文档大纲
3. `feishu_doc_create`：按照下方摘要模板生成飞书云文档
   - 使用 Callout 突出决策和风险
   - 使用表格展示行动项
   - 保留消息溯源引用
4. `end`：返回文档链接

---

## 6) 文档结构模板（Writer Agent 遵循）

```markdown
# 群聊摘要：{群名}

> 统计范围：{start_date} {start_time} ~ {end_date} {end_time} (UTC+8)
> 消息总数：{msg_count} 条 | 参与人数：{user_count} 人
> 生成时间：{gen_date} {gen_time}

---

## TL;DR

<!-- 3-5 条核心要点，使用 Callout -->

> **[决策]** {tldr_decision_summary}
> **[行动]** {action_count} 项待办，最近截止：{nearest_due_date}
> **[风险]** {tldr_risk_summary}

---

## 核心议题

### 1. {议题名称}

- **讨论摘要**：{topic_summary}
- **结论/共识**：{topic_conclusion}
- **参与人**：{participant_list}

---

### 2. {议题名称}

- **讨论摘要**：{topic_summary}
- **结论/共识**：{topic_conclusion}
- **参与人**：{participant_list}

---

## 关键决策

| 决策内容 | 决策人 | 时间 | 备注 |
|---------|-------|------|------|
| {decision_content} | {decision_maker} | {decision_time} | {decision_note} |
| {decision_content} | {decision_maker} | {decision_time} | {decision_note} |

---

## 行动项

| 任务 | 负责人 | 截止时间 | 状态 |
|-----|-------|---------|------|
| {task_description} | {owner} | {due_date} | {status} |
| {task_description} | {owner} | {due_date} | {status} |

---

## 风险与问题

<!-- 使用 Callout 突出高风险 -->

> **[高风险]** {risk_description}
> - 影响：{risk_impact}
> - 状态：{risk_status}
> - 建议：{risk_suggestion}

### 其他问题
- **{issue_name}**：{issue_description} —— 状态：{issue_status}

---

## 重要链接

- [{resource_name}]({resource_url}) - {sharer} 分享于 {share_time}
- [{resource_name}]({resource_url}) - {sharer} 分享于 {share_time}

---

## 待跟进

- [ ] {followup_item_1}
- [ ] {followup_item_2}
- [ ] 下次同步：{next_sync_date}
```

---

## 7) 执行流程图

```
用户: "帮我总结 {群名} 群的聊天记录"
          |
          v
+-------------------------------------------------------------+
|                    主 Agent 执行                              |
+-------------------------------------------------------------+
| 1. todo_write: 分解任务                                      |
|                                                             |
| 【Module A — 消息获取】                                      |
| 2. aily-im(search-chats): 定位目标群聊                       |
| 3. aily-im(list-messages): 拉取指定时间范围消息               |
| 4. 时间过滤 + 去噪 + 分段                                    |
| 5. file → draft.md (群聊信息 + 消息分段)               |
|                                                             |
| 【Module B — 结构化提取】                                    |
| 6. 识别核心议题 → file → draft.md                      |
| 7. 提取关键决策 → file → draft.md                      |
| 8. 提取行动项 (Owner/Due) → file → draft.md            |
| 9. 提取风险与问题 → file → draft.md                    |
| 10. 整理重要链接 → file → draft.md                     |
|                                                             |
| 【Module C — 分发任务】                                      |
| 11. 素材完整性检查                                           |
| 12. task(writer): 分发写作任务                               |
+-------------------------------------------------------------+
          |
          v
+-------------------------------------------------------------+
|                    Writer Agent 执行                         |
+-------------------------------------------------------------+
| 1. file_read: 读取 /home/workspace/draft.md                  |
| 2. outline_generator: 生成文档大纲                           |
| 3. feishu_doc_create: 生成飞书云文档                          |
|    - TL;DR (Callout)                                        |
|    - 核心议题                                                |
|    - 关键决策 (表格)                                         |
|    - 行动项 (表格)                                           |
|    - 风险与问题 (Callout)                                    |
|    - 重要链接                                                |
|    - 待跟进                                                  |
| 4. end: 返回文档链接                                         |
+-------------------------------------------------------------+
          |
          v
      飞书云文档群聊摘要
```

---

## 8) Checklist

### 主 Agent 检查项
- [ ] 群聊标识正确（已通过 aily-im 验证）
- [ ] 时间范围已明确标注（含时区 UTC+8）
- [ ] 消息已预处理（去噪、分段）
- [ ] 核心议题已识别（3-7 个，按热度排序）
- [ ] 关键决策已提取（含决策人、时间、原始消息）
- [ ] 行动项已提取（含 Owner / Due，无 Owner 标注"待分配"）
- [ ] 风险与问题已识别（含严重程度）
- [ ] 重要链接已整理（含类型、分享人）
- [ ] draft.md 所有章节完整
- [ ] 无编造数据，所有信息可溯源

### Writer Agent 检查项
- [ ] TL;DR 完整（3-5 条，使用 Callout）
- [ ] 核心议题按热度排序
- [ ] 决策使用表格展示
- [ ] 行动项有负责人和截止时间
- [ ] 高风险使用 Callout 突出
- [ ] 重要链接可点击
- [ ] 待跟进清单完整
- [ ] 已创建飞书云文档

---

## 9) 常见失败模式与修复

| 失败模式 | 原因 | 修复方法 |
|---------|------|---------|
| 遗漏关键决策 | 识别信号词覆盖不全 | 扩大决策识别信号词，加入"拍板"、"OK就这样" |
| 行动项无 Owner | 消息中未明确分配 | 标注"待分配"，列入待跟进清单 |
| 噪音过多 | 闲聊/表情未过滤 | 加强去噪规则，降权非实质内容 |
| 时间范围错误 | 时区未统一 | 明确标注 UTC+8，解析用户意图时确认时区 |
| 摘要过于笼统 | 缺少具体信息 | 引用原始表述，补充具体时间、人名、数据 |
| 消息拉取不全 | 分页未处理 | 循环调用 list-messages 直至所有页获取完毕 |
| 议题识别偏差 | 话题切分不准 | 结合时间间隔 + 语义相似度双重分段 |
| draft.md 数据缺失 | 跳过某提取步骤 | 执行前对照 Checklist 逐项检查 |

---

## 10) 扩展场景

### 10.1 主题追踪模式
- 用户指定关键词/话题
- 跨时间段追踪该话题演进
- 输出：话题时间线 + 各阶段结论
- 适用场景：跟踪某技术方案从提出到落地的全过程

### 10.2 多群聚合
- 多个相关群的讨论汇总
- 识别跨群关联话题
- 全局行动项汇总表
- 适用场景：项目涉及多个子群，需要统一视图

### 10.3 周期性摘要
- 每日/每周自动生成
- 与历史摘要对比，标注新增/变化项
- 追踪长期议题进展
- 适用场景：例会群/项目群的持续跟踪
