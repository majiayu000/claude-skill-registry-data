---
name: persona-heartbeat
description: |
  AI 人格操作系统会话的环境监控和健康心跳。监控上下文窗口使用量，在顾问模式启用时提供主动建议，检测会话启动以恢复先前工作，执行静默记忆维护（清理旧条目、归档日志），并在需要时呈现健康状态。触发关键词：heartbeat、monitor、pulse、context check、health、session start、memory maintenance、ambient、housekeeping、status check、session resume、context health、心跳、监控、健康检查。
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# 人格心跳

AI 人格操作系统的环境监控和健康心跳系统。本技能处理程序化的上下文健康检查、主动建议展示、会话恢复和记忆维护。

## 阶段 1：上下文健康检查

**目的：** 监控上下文窗口使用量并根据阈值触发相应操作。

### 步骤 1.1：确定当前上下文使用量

通过可用的系统指标检查当前上下文窗口使用百分比。

```pseudocode
context_usage_pct = get_context_window_usage()
computed.context_level = context_usage_pct
```

### 步骤 1.2：应用阈值逻辑并呈现用户可见消息

根据上下文使用量，确定用户看到的内容以及需要采取的操作：

| 使用范围 | 用户可见行为 |
|----------|-------------|
| < 50% | 无 — 正常运行 |
| 50-69% | 无 — 内部记录以供跟踪 |
| 70-84% | "📝 上下文 [X]% — 继续前正在保存检查点。"然后委托给 persona-checkpoint |
| 85-94% | "🟠 上下文 [X]% — 已保存紧急检查点。建议尽快启动新会话。" |
| 95%+ | "🔴 上下文 [X]% — 严重。正在保存必要信息。请启动新会话。" |

```pseudocode
if context_usage_pct >= 95:
    show_critical_warning()
    save_essential_state()
    computed.action_taken = "critical_checkpoint"
elif context_usage_pct >= 85:
    show_emergency_warning()
    delegate_to_checkpoint()
    computed.action_taken = "emergency_checkpoint"
elif context_usage_pct >= 70:
    show_checkpoint_notice()
    delegate_to_checkpoint()
    computed.action_taken = "standard_checkpoint"
else:
    computed.action_taken = "none"
```

### 步骤 1.3：记录阈值跨越事件

跟踪阈值跨越时间，避免在同一会话中重复通知。

```pseudocode
if computed.action_taken != "none":
    timestamp = current_timestamp()
    append_to_session_log(threshold_event, timestamp)
```

## 阶段 2：主动建议引擎

**目的：** 在顾问模式启用时提供有用建议，遵循严格规则以避免噪音。

**激活条件：** 仅当 USER.md 中顾问模式为开启状态时。

### 步骤 2.1：检查顾问模式状态

```pseudocode
user_config = read_file("~/workspace/USER.md")
advisor_enabled = parse_advisor_mode(user_config)
computed.advisor_active = advisor_enabled
```

### 步骤 2.2：评估建议条件

仅在满足所有条件时才展示建议：
- 发现了关于用户目标的重要新上下文
- 发现了未注意到的模式或机会
- 存在时间敏感的机会
- 当前未进行复杂任务
- 未超过每会话最多 1 条建议的限制
- 上一条建议未被忽略/拒绝

```pseudocode
if not advisor_enabled:
    return  # 完全跳过建议引擎

suggestion_contexts = [
    "new_goal_context",
    "unnoticed_pattern",
    "time_sensitive_opportunity"
]

blockers = [
    "complex_task_active",
    "session_quota_exceeded",
    "previous_ignored"
]

if any_suggestion_context() and not any_blocker():
    computed.suggestion_eligible = true
else:
    computed.suggestion_eligible = false
```

### 步骤 2.3：格式化并展示建议

**格式：**
```
💡 建议

[一句话描述注意到的情况]

[一句话提出行动方案]

要我执行吗？（是/否）
```

示例：

<invoke name="$ASK_USER_QUESTION">
<parameter name="question_data">{
  "questions": [
    {
      "question": "💡 建议\n\n我注意到您在过去一小时内创建了三个功能相似的脚本。\n\n要我将其整合为一个可复用的模块吗？\n\n要我执行吗？",
      "key": "suggestion_response",
      "options": ["yes", "no"]
    }
  ]
}</parameter>
</invoke>

```pseudocode
if computed.suggestion_eligible:
    formatted_suggestion = format_suggestion(context, proposal)
    response = ask_user(formatted_suggestion)
    
    if response == "yes":
        execute_suggested_action()
        computed.suggestion_accepted = true
    else:
        log_suggestion_declined()
        computed.suggestion_accepted = false
    
    mark_session_suggestion_quota_used()
```

## 阶段 3：会话启动检测

**目的：** 检测新会话并静默恢复先前的工作上下文。

### 步骤 3.1：检测新会话中的第一条消息

```pseudocode
is_session_start = detect_new_session()
computed.is_new_session = is_session_start

if not is_session_start:
    return  # 跳过会话启动流程
```

### 步骤 3.2：静默加载核心人格文件

读取基础文件，不向用户展示内容。

```pseudocode
soul_content = read_file("~/workspace/SOUL.md")
user_content = read_file("~/workspace/USER.md")
memory_content = read_file("~/workspace/MEMORY.md")

computed.persona_loaded = true
```

### 步骤 3.3：检查昨天的日志

```pseudocode
yesterday_date = get_yesterday_date()  # 格式：YYYY-MM-DD
log_path = "~/workspace/memory/daily-{yesterday_date}.md"

if file_exists(log_path):
    yesterday_log = read_file(log_path)
    computed.has_previous_log = true
else:
    computed.has_previous_log = false
```

### 步骤 3.4：展示未完成项目或保持静默

```pseudocode
if computed.has_previous_log:
    uncompleted_items = parse_uncompleted_items(yesterday_log)
    
    if uncompleted_items:
        surface_resumption_message(uncompleted_items)
        # 示例："📋 从上次会话恢复：
        # • 修复登录流程中的认证 bug
        # • 审查 PR #42 的依赖项更新"
    else:
        # 无需展示 — 静默操作
        pass
else:
    # 无先前日志 — 静默操作
    pass
```

## 阶段 4：记忆维护

**目的：** 对记忆文件和日志执行静默维护，仅在有操作时才通知。

**触发条件：** 每约 10 次交互（近似值，非严格）。

### 步骤 4.1：检查 MEMORY.md 大小

```pseudocode
memory_file = "~/workspace/MEMORY.md"
file_size = get_file_size(memory_file)

computed.memory_size_kb = file_size / 1024

if computed.memory_size_kb > 4:
    computed.memory_needs_pruning = true
else:
    computed.memory_needs_pruning = false
```

### 步骤 4.2：清理旧记忆条目

如果文件超过 4KB，移除 30 天前的条目。

```pseudocode
if computed.memory_needs_pruning:
    cutoff_date = current_date() - 30_days
    memory_entries = parse_memory_entries(memory_file)
    
    entries_to_keep = filter(lambda e: e.date >= cutoff_date, memory_entries)
    pruned_count = len(memory_entries) - len(entries_to_keep)
    
    if pruned_count > 0:
        write_file(memory_file, entries_to_keep)
        computed.pruned_entries = pruned_count
    else:
        computed.pruned_entries = 0
```

### 步骤 4.3：归档旧日志

将 90 天前的日志移至归档目录。

```pseudocode
log_directory = "~/workspace/memory/"
archive_directory = "~/workspace/memory/archive/"

daily_logs = glob(log_directory + "daily-*.md")
cutoff_date = current_date() - 90_days

logs_to_archive = []
for log in daily_logs:
    log_date = parse_date_from_filename(log)
    if log_date < cutoff_date:
        logs_to_archive.append(log)

if logs_to_archive:
    ensure_directory_exists(archive_directory)
    for log in logs_to_archive:
        move_file(log, archive_directory)
    
    computed.archived_logs = len(logs_to_archive)
else:
    computed.archived_logs = 0
```

### 步骤 4.4：检查前几天未完成的项目

```pseudocode
recent_logs = get_logs_from_last_7_days("~/workspace/memory/")
uncompleted_items = []

for log in recent_logs:
    items = parse_uncompleted_items(log)
    uncompleted_items.extend(items)

if uncompleted_items and not already_surfaced_this_session():
    surface_once_per_session(uncompleted_items)
    computed.surfaced_uncompleted = true
else:
    computed.surfaced_uncompleted = false
```

### 步骤 4.5：仅在有操作时通知

```pseudocode
actions_taken = []

if computed.pruned_entries > 0:
    actions_taken.append(f"清理了 {computed.pruned_entries} 条旧记忆条目")

if computed.archived_logs > 0:
    actions_taken.append(f"归档了 {computed.archived_logs} 份旧日志")

if actions_taken:
    notification = "🗂️ 维护：" + "、".join(actions_taken) + "。"
    display(notification)
else:
    # 静默操作 — 无通知
    pass
```

## 阶段 5：心跳输出格式

**目的：** 标准化地向用户呈现健康状态。

### 步骤 5.1：确定何时展示心跳

在以下情况展示心跳状态：
- 用户明确请求（"heartbeat"、"status"、"health check"）
- 上下文阈值跨越（70%+）
- 执行了维护操作
- 会话开始时发现未完成项目

### 步骤 5.2：格式化心跳头部

```pseudocode
current_datetime = get_current_datetime()  # 格式：2026-02-17 14:30
model_name = get_current_model()  # 例如 "claude-opus-4-6"
version = "1.0.0"  # AI Persona OS 版本

header = f"🫀 {current_datetime} | {model_name} | AI Persona OS v{version}"
```

### 步骤 5.3：生成信号灯指标

确定健康指标，每个指标之间留空行：

```pseudocode
indicators = []

# 上下文健康
if computed.context_level < 70:
    indicators.append("🟢 上下文：{computed.context_level}%（健康）")
elif computed.context_level < 85:
    indicators.append("🟡 上下文：{computed.context_level}%（建议关注）")
else:
    indicators.append("🔴 上下文：{computed.context_level}%（需要操作）")

# 记忆健康
if computed.memory_size_kb < 4:
    indicators.append("🟢 记忆：{computed.memory_size_kb}KB（健康）")
elif computed.memory_size_kb < 8:
    indicators.append("🟡 记忆：{computed.memory_size_kb}KB（建议关注）")
else:
    indicators.append("🔴 记忆：{computed.memory_size_kb}KB（需要操作）")

# 顾问状态
if computed.advisor_active:
    indicators.append("🟢 顾问：活跃")
else:
    indicators.append("⚪ 顾问：未激活")

# 未完成项目
if computed.surfaced_uncompleted:
    indicators.append("🟡 未完成：前几次会话有待处理项目")
```

### 步骤 5.4：组装并展示心跳

```pseudocode
heartbeat_output = header + "\n\n" + "\n\n".join(indicators)
display(heartbeat_output)
```

**示例输出：**

```
🫀 2026-02-17 14:30 | claude-opus-4-6 | AI Persona OS v1.0.0

🟢 上下文：45%（健康）

🟢 记忆：2.8KB（健康）

🟢 顾问：活跃

⚪ 未完成：无
```

## 注意事项

- 本技能主要在后台运行，大多数阶段静默执行
- 仅在信息对用户有价值时才展示
- 严格遵守每会话最多 1 条建议的规则
- 记忆维护不应中断当前工作
- 心跳格式提供快速的可视化健康评估
