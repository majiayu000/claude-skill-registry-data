---
name: persona-learning
description: |
  在 AI 人格操作系统中捕获、审查和晋升学习内容、错误和功能请求。将结构化条目记录到 ~/workspace/.learnings/（LEARNINGS.md、ERRORS.md、FEATURE_REQUESTS.md），每周扫描模式，将重复的学习内容（3 次以上出现）晋升到 MEMORY.md，并实现 4 个成长反馈循环：好奇心（知识缺口 → 提问 → 模式跟踪）、模式识别（重复请求 → 自动化提案）、能力扩展（限制 → 研究 → 工具化）和成果跟踪（决策 → 跟进 → 教训）。通过结构化学习捕获、错误分析、错误跟踪、模式检测和成长导向的行为循环支持持续改进。触发关键词：learn、mistake、error、review、promote、growth、learning、capture、pattern、improvement、feature request、学习、错误、复盘、提升、记录。
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# 人格学习系统

本技能实现 AI 人格操作系统的学习捕获、审查和晋升系统。提供结构化机制来捕获学习内容、错误和功能请求，然后将有价值的模式提升到长期记忆。

## 阶段 1：捕获

将结构化条目记录到 `~/workspace/.learnings/` 中的相应文件：

### 步骤 1.1：确定条目类型

分类条目：
- **学习内容** → `LEARNINGS.md`（洞察、发现、成功的方法）
- **错误** → `ERRORS.md`（失误、失败、错误假设）
- **功能请求** → `FEATURE_REQUESTS.md`（期望的功能、工具缺口、工作流改进）

### 步骤 1.2：确保学习目录存在

```pseudocode
if not exists(~/workspace/.learnings/):
    create directory ~/workspace/.learnings/

if not exists(target_file):
    create target_file with header
```

### 步骤 1.3：格式化条目

使用以下字段结构化条目：

```markdown
## [YYYY-MM-DD] 类别：简要标题

**描述：** 对学习到的内容/遇到的错误/需要的功能的清晰说明

**上下文：** 导致此学习/错误/需求的情况
- 相关项目/任务
- 尝试了什么
- 目标是什么

**解决方案/操作：**
- 学习内容：什么有效、为什么有效、何时应用
- 错误：根本原因、如何修复、预防策略
- 功能请求：提议的解决方案、实现前的替代方案

**标签：** #关键词1 #关键词2 #关键词3

**状态：** 活跃 | 已晋升 | 已解决
```

### 步骤 1.4：追加到相应文件

```pseudocode
Read target_file
Append formatted_entry to target_file
Write updated target_file
Confirm to user: "条目已捕获到 {target_file}"
```

## 阶段 2：审查

扫描学习文件以发现模式和晋升候选。

### 步骤 2.1：扫描所有学习文件

```pseudocode
learnings = Read ~/workspace/.learnings/LEARNINGS.md
errors = Read ~/workspace/.learnings/ERRORS.md
feature_requests = Read ~/workspace/.learnings/FEATURE_REQUESTS.md (if exists)

entries = parse_all_entries(learnings, errors, feature_requests)
```

### 步骤 2.2：检测模式

查找以下内容：

1. **重复错误**（相同错误类型 3 次以上）
2. **常见主题**（标签出现在 5 个以上条目中）
3. **晋升候选**（状态：活跃，出现 3 次以上）
4. **已解决模式**（多个条目具有相同根本原因）

```pseudocode
patterns = {
    "repeated_errors": [],
    "common_tags": {},
    "promotion_candidates": [],
    "resolved_themes": []
}

for entry in entries:
    if entry.status == "Active":
        increment tag_counts[entry.tags]

    if entry appears 3+ times (by description similarity):
        add to promotion_candidates

    if entry.type == "error" and similar_errors >= 3:
        add to repeated_errors
```

### 步骤 2.3：生成审查摘要

输出格式：

```markdown
# 学习审查 - [日期]

## 统计摘要
- 学习内容总数：{数量}
- 错误总数：{数量}
- 功能请求：{数量}
- 已晋升条目：{数量}

## 检测到的模式

### 重复错误（{数量}）
1. [错误主题] - {数量} 次出现
   - 最近出现：[日期]
   - 预防策略：[如有]

### 常见主题（{数量} 个标签出现 5 次以上）
- #标签1：{数量} 个条目
- #标签2：{数量} 个条目

### 晋升候选（{数量}）
1. [标题] - {数量} 次出现
   - 首次出现：[日期]
   - 最近出现：[日期]
   - 准备晋升到 MEMORY.md

### 已解决模式
1. [主题] - {数量} 个实例已解决
   - 解决方案：[摘要]
```

**询问用户的审查偏好：**

```json
{
  "questions": [
    {
      "id": "review_frequency",
      "question": "您希望安排每周自动审查，还是手动运行审查？",
      "type": "choice",
      "choices": ["每周自动", "仅手动"]
    }
  ]
}
```

## 阶段 3：晋升

将重复模式（3 次以上出现）提升到 `~/workspace/MEMORY.md`。

### 步骤 3.1：识别晋升候选

```pseudocode
candidates = []
for entry in all_entries:
    if entry.status == "Active":
        occurrences = count_similar_entries(entry)
        if occurrences >= 3:
            candidates.append(entry)
```

### 步骤 3.2：请求用户批准

**在修改 MEMORY.md 之前，始终询问：**

```json
{
  "questions": [
    {
      "id": "promotion_approval",
      "question": "发现 {数量} 个条目准备晋升到 MEMORY.md。审查候选：\n\n{候选摘要}\n\n是否继续晋升？",
      "type": "confirm"
    }
  ]
}
```

### 步骤 3.3：晋升到 MEMORY.md

```pseudocode
if user_approves:
    memory = Read ~/workspace/MEMORY.md

    for candidate in approved_candidates:
        promoted_entry = format_promotion(candidate)
        append promoted_entry to memory

        # 标记原始条目为已晋升
        update_entry_status(candidate, "Promoted")

    Write memory to ~/workspace/MEMORY.md
    Confirm: "已将 {数量} 个条目晋升到 MEMORY.md"
```

**晋升格式：**

```markdown
## [模式名称]

**来源：** {原始文件} - {出现日期}

**摘要：** {所有出现的合并描述}

**应用场景：** {何时应用此学习内容}

**证据：** 在 {首次日期} 和 {最近日期} 之间出现 {数量} 次
```

### 步骤 3.4：更新原始条目

```pseudocode
for promoted_entry in promoted_list:
    locate original_entry in source_file
    change status from "Active" to "Promoted"
    add reference: "参见 MEMORY.md：[模式名称]"
```

## 阶段 4：成长循环

实现 4 个在正常操作中持续运行的反馈循环。

### 循环 1：好奇心循环

**目的：** 系统性地填补知识缺口。

```pseudocode
# 持续的行为模式
while working_on_task:
    if encounter_unknown:
        log to computed.knowledge_gaps[]
        ask 1-2 clarifying questions

        if pattern_emerges (3+ similar gaps):
            propose adding to ~/workspace/USER.md
            generate targeted learning ideas
```

**示例状态跟踪：**

```pseudocode
computed.knowledge_gaps = [
    {topic: "Docker networking", count: 1, first_seen: "2026-02-15"},
    {topic: "Kubernetes ingress", count: 3, first_seen: "2026-02-10"}
]

if knowledge_gaps["Kubernetes ingress"].count >= 3:
    suggest: "将 Kubernetes ingress 学习目标添加到 USER.md"
```

### 循环 2：模式识别循环

**目的：** 自动化重复的手动工作。

```pseudocode
while handling_request:
    track request_type in computed.request_history[]

    if same_request_type >= 3:
        propose: "这是您第 3 次需要 {任务}。要构建自动化吗？"

        if user_approves:
            design system
            build with approval
            document in ~/workspace/WORKFLOWS.md
```

**示例：**

```pseudocode
computed.request_history = [
    {type: "format_json", count: 1},
    {type: "git_commit", count: 5},  # 自动化候选
    {type: "run_tests", count: 2}
]

if request_history["git_commit"].count >= 3:
    propose: "创建 /commit 技能来自动化 git 工作流？"
```

### 循环 3：能力扩展循环

**目的：** 通过工具化克服限制。

```pseudocode
while attempting_task:
    if hit_limitation:
        log to computed.capability_gaps[]
        research available_tools/skills

        if solution_found:
            install/build tool
            document in ~/workspace/TOOLS.md
            retry original problem
```

**示例：**

```pseudocode
if cannot_parse_yaml:
    research: "Claude Code 的 YAML 解析工具"
    find: yq 工具
    install: yq
    document: "添加 yq 用于 YAML 处理" → TOOLS.md
    apply to original_task
```

### 循环 4：成果跟踪循环

**目的：** 通过跟进从决策中学习。

```pseudocode
while making_significant_decision:
    log decision to computed.pending_outcomes[]

    after time_passes (weekly/monthly):
        review outcome
        extract lessons
        update approach based on results
```

**示例：**

```pseudocode
computed.pending_outcomes = [
    {
        decision: "选择 PostgreSQL 而非 MySQL",
        date: "2026-02-01",
        follow_up_date: "2026-03-01",
        outcome: null  # 稍后检查
    }
]

# 在跟进日期：
review PostgreSQL choice:
    if successful: document why it worked
    if problematic: document what to do differently
    update MEMORY.md with lesson
```

## 状态管理

在 `computed.*` 变量中跟踪成长循环状态：

```pseudocode
computed.knowledge_gaps = []
computed.request_history = {}
computed.capability_gaps = []
computed.pending_outcomes = []
computed.last_review_date = "YYYY-MM-DD"
computed.promotion_candidates = []
```

## 关键规则

1. **修改 MEMORY.md 前始终询问** — 晋升需要明确批准
2. **仅结构化条目** — 强制执行条目格式模板
3. **成长循环是行为模式** — 它们持续运行，不是一次性流程
4. **3 次重复阈值** — 模式需要 3 次以上出现才能晋升
5. **来源跟踪** — 已晋升条目引用原始位置和日期
6. **状态转换** — 活跃 → 已晋升（绝不删除原始条目）

## 使用示例

### 捕获学习内容

```
用户："我发现使用 --depth=1 可以显著加速 git clone"

Claude：在 ~/workspace/.learnings/LEARNINGS.md 创建条目：

## [2026-02-17] Git：浅克隆优化

**描述：** 使用 git clone --depth=1 创建只包含最新提交的浅克隆，显著减少大型仓库的克隆时间和磁盘空间。

**上下文：** 使用大型 monorepo 工作
- 尝试：对 5GB 仓库执行常规 git clone
- 目标：为 CI/CD 加速本地设置
- 结果：克隆时间从 15 分钟减少到 2 分钟

**解决方案/操作：**
- CI 构建中使用 --depth=1（不需要历史记录的场景）
- 最适用于：测试、部署管道、一次性检查
- 避免用于：需要完整 git 历史的仓库
- 可稍后转换为完整克隆：git fetch --unshallow

**标签：** #git #performance #optimization #devops

**状态：** 活跃
```

### 运行审查

```
用户："运行学习审查"

Claude：扫描所有 .learnings/ 文件，生成摘要：

# 学习审查 - 2026-02-17

## 统计摘要
- 学习内容总数：23
- 错误总数：8
- 功能请求：5
- 已晋升条目：3

## 检测到的模式

### 晋升候选（2）
1. Git 浅克隆优化 - 3 次出现
   - 首次出现：2026-01-15
   - 最近出现：2026-02-17
   - 准备晋升到 MEMORY.md

2. Docker 层缓存 - 4 次出现
   - 首次出现：2026-01-20
   - 最近出现：2026-02-15
   - 准备晋升到 MEMORY.md

您想将这 2 个条目晋升到 MEMORY.md 吗？
```

### 成长循环示例

```
# 好奇心循环
用户："如何配置 Kubernetes ingress？"

Claude 跟踪：
computed.knowledge_gaps["Kubernetes"] = 3  # 第三次

Claude："我注意到这是我们第三次遇到 Kubernetes 相关问题。您想让我把'学习 Kubernetes 网络'添加到您的 USER.md 学习目标中吗？我还可以研究相关文档添加到您的知识库。"

# 模式识别循环
用户："格式化这个 JSON"（第 5 次）

Claude："这是您第 5 次需要 JSON 格式化。您想让我创建一个 /format-json 技能来自动处理吗？它可以：
- 检测剪贴板/选区中的 JSON
- 自动格式化为正确缩进
- 验证语法
- 处理紧凑和美化两种模式"

# 能力扩展循环
Claude 遇到 YAML 解析限制

Claude："我需要一个 YAML 解析器来完成此任务。让我研究一下可用方案... 找到：yq 工具。正在安装并记录到 TOOLS.md..."

# 成果跟踪循环
用户："这个 API 应该用 REST 还是 GraphQL？"

Claude："基于以下原因我们选择 GraphQL：[分析]。我将跟踪此决策并在 2 周后跟进评估效果。"

computed.pending_outcomes.append({
    decision: "选择 GraphQL API",
    rationale: "[原因]",
    follow_up: "2026-03-03"
})
```
