---
name: persona-commands
description: AI 人格操作系统运行时聊天指令。将 11 个指令路由到对应操作 — 状态仪表盘（含健康指标）、显示人格（展示 SOUL.md 身份）、显示记忆（展示 MEMORY.md 内容）、健康检查（运行诊断脚本）、安全审计（运行安全验证）、显示配置（验证配置文件）、帮助（指令参考）、检查点（保存上下文快照）、顾问开/关（切换主动模式）、切换预设（更改人格配置）。支持自然语言变体识别，如"系统状态"对应 status、"我是谁"对应 show persona。关键词：status、dashboard、show persona、show memory、health check、security audit、show config、help、checkpoint、advisor、switch preset、commands、diagnostics、validate、proactive mode
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
---

# 运行时聊天指令

本技能处理 AI 人格操作系统的 11 个运行时指令，将用户请求路由到相应的系统操作。

## 指令参考

| 指令 | 操作 | 输出格式 |
|------|------|----------|
| **status** | 运行健康检查，显示仪表盘 | 📊 状态仪表盘（含 🟢🟡🔴 指示器） |
| **show persona** | 读取并格式化 SOUL.md | 🪪 人格身份展示 |
| **show memory** | 显示 MEMORY.md 内容 | 原始记忆文件内容 |
| **health check** | 运行诊断脚本 | 脚本输出（含通过/失败指示器） |
| **security audit** | 运行安全验证 | 脚本输出（含安全发现） |
| **show config** | 验证配置文件 | 脚本输出（含配置验证） |
| **help** | 显示指令参考 | 本参考表 |
| **checkpoint** | 保存上下文快照 | 确认消息（含文件路径） |
| **advisor on** | 启用主动模式 | 确认消息 |
| **advisor off** | 禁用主动模式 | 确认消息 |
| **switch preset** | 更改人格配置 | 预设菜单，委托给 persona-setup |

## 自然语言识别

本技能识别自然语言变体：
- "how's my system" / "system status" / "check status" / "健康检查" / "系统状态" → **status**
- "what's my persona" / "who am I" / "show identity" / "显示人格" / "我是谁" → **show persona**
- "what do I remember" / "show my memory" / "memory contents" / "显示记忆" / "查看记忆" → **show memory**
- "run diagnostics" / "check health" / "system check" / "运行诊断" / "系统诊断" → **health check**
- "check security" / "audit security" / "security check" / "安全审计" / "安全检查" → **security audit**
- "validate config" / "check config" / "show configuration" / "显示配置" / "验证配置" → **show config**
- "what can I do" / "available commands" / "command list" / "帮助" / "有什么命令" → **help**
- "save progress" / "create checkpoint" / "save state" / "检查点" / "保存进度" / "保存上下文" → **checkpoint**
- "enable advisor" / "turn on advisor" / "proactive on" / "开启顾问" / "启用主动模式" → **advisor on**
- "disable advisor" / "turn off advisor" / "proactive off" / "关闭顾问" / "禁用主动模式" → **advisor off**
- "change persona" / "switch configuration" / "change preset" / "切换预设" / "更换人格" → **switch preset**

## 实现指南

### 阶段 1：指令识别

**步骤 1.1：** 解析用户输入以识别指令意图
```pseudocode
command = extract_command(user_input)
if command not in VALID_COMMANDS:
    command = match_natural_language_variant(user_input)
if command is None:
    show_help_and_suggest_closest_match()
    exit
```

**步骤 1.2：** 验证指令可用性
```pseudocode
if command requires script:
    check script exists at ${CLAUDE_PLUGIN_ROOT}/scripts/
if command requires workspace file:
    check file exists at ~/workspace/
```

### 阶段 2：指令执行

**步骤 2.1：status** - 显示系统健康仪表盘

```pseudocode
# 运行健康检查
core_files_count = count files in ${CLAUDE_PLUGIN_ROOT}/core/
memory_size = stat ~/workspace/MEMORY.md | get size in KB
recent_logs = count lines in ~/workspace/.logs/YYYY-MM-DD.log (last 24h)
version = cat ${CLAUDE_PLUGIN_ROOT}/VERSION

# 计算健康指标
core_health = 🟢 if core_files_count >= 8 else 🟡 if >= 6 else 🔴
memory_health = 🟢 if memory_size < 100 else 🟡 if < 500 else 🔴
logs_health = 🟢 if recent_logs < 100 else 🟡 if < 500 else 🔴

# 显示仪表盘
output = format_status_dashboard(core_health, memory_health, logs_health, version)
```

**状态仪表盘格式：**
```
📊 AI Persona OS - 状态仪表盘
🫀 上次心跳：YYYY-MM-DD HH:MM:SS

核心系统：     🟢 已加载 8 个文件
记忆：         🟢 42 KB（健康）
近期日志：     🟡 127 条记录（24h）
版本：         v1.4.1

系统状态：健康
```

**步骤 2.2：show persona** - 从 SOUL.md 显示身份

```pseudocode
soul_content = Read(~/workspace/SOUL.md)
extract:
    - name（来自 # 标题或 name: 字段）
    - role（来自 role: 字段或 Role: 标题）
    - values（来自 Values: 部分，列表项）
    - style（来自 Communication Style: 部分）

output = format_persona_display(name, role, values, style)
```

**显示人格格式：**
```
🪪 人格身份

名称：  高级技术架构师
角色：  专注于分布式系统的系统设计专家

核心价值观：
  • 清晰胜过花哨
  • 测试一切重要的事物
  • 文档是对未来自己的关爱

沟通风格：
  直接、技术化、假定具备专业知识。使用精确术语。
  主动提供建议。被要求时解释推理过程。
```

**步骤 2.3：show memory** - 显示 MEMORY.md 内容

```pseudocode
memory_content = Read(~/workspace/MEMORY.md)
以最小格式化显示 memory_content
```

**步骤 2.4：health check** - 运行诊断脚本

```pseudocode
result = Bash("${CLAUDE_PLUGIN_ROOT}/scripts/health-check.sh")
display result
# 除非用户明确要求，否则不显示原始 exec 命令
```

**步骤 2.5：security audit** - 运行安全验证

```pseudocode
result = Bash("${CLAUDE_PLUGIN_ROOT}/scripts/security-audit.sh")
display result
# 高亮显示安全发现
```

**步骤 2.6：show config** - 验证配置

```pseudocode
result = Bash("${CLAUDE_PLUGIN_ROOT}/scripts/config-validator.sh")
display result
# 显示每个配置文件的验证状态
```

**步骤 2.7：help** - 显示指令参考

```pseudocode
display COMMAND_REFERENCE_TABLE（来自上方章节）
add usage examples:
    "输入 'status' 查看系统健康状态"
    "输入 'show persona' 查看您的人格身份"
    "输入 'checkpoint' 保存当前上下文"
```

**步骤 2.8：checkpoint** - 保存上下文快照

```pseudocode
timestamp = current_timestamp (HH:MM)
date = current_date (YYYY-MM-DD)
checkpoint_file = ~/workspace/memory/${date}.md

# 计算上下文百分比（基于对话长度估算）
context_percentage = min(100, conversation_turns * 5)

# 收集检查点数据
active_task = ask_user("您当前在做什么任务？")
key_decisions = ask_user("有什么关键决策或变更需要记录？")
resume_from = ask_user("下次会话应从哪里继续？")

# 写入检查点
checkpoint_content = format_checkpoint(
    timestamp, context_percentage, active_task, key_decisions, resume_from
)
Write(checkpoint_file, checkpoint_content, mode=append)

confirm "检查点已保存到 ${checkpoint_file}"
```

**检查点格式：**
```markdown
## 检查点 [14:32] — 上下文：35%

**当前任务：** 实现用户认证流程
**关键决策：**
- 选择 JWT 而非 session cookies，以实现 API 无状态
- 在网关层添加了速率限制

**继续从：** 完成 /auth/login 端点的集成测试
```

**步骤 2.9：advisor on** - 启用主动模式

```pseudocode
# 设置主动模式标志（在 SOUL.md 或运行时状态中）
confirm "✅ 主动顾问模式已启用"
confirm "我现在将主动提供建议并预判需求。"
```

**步骤 2.10：advisor off** - 禁用主动模式

```pseudocode
# 清除主动模式标志
confirm "✅ 主动顾问模式已禁用"
confirm "我将在收到明确请求后才提供建议。"
```

**步骤 2.11：switch preset** - 更改人格配置

```pseudocode
# 显示预设菜单
presets = Glob("${CLAUDE_PLUGIN_ROOT}/presets/*.yaml")
display_menu(presets)

# 委托给 persona-setup 技能
confirm "正在切换到 persona-setup 技能进行预设配置..."
# persona-setup 技能将处理预设选择和文件重建
```

### 阶段 3：输出格式化

**步骤 3.1：** 应用指令特定的格式化规则
```pseudocode
if command == "status":
    use traffic light indicators (🟢🟡🔴)
    include timestamp and version
else if command == "show persona":
    use identity header (🪪)
    format as sections with bullet lists
else if command == "checkpoint":
    use markdown heading with timestamp
    include context percentage
else if command in ["health check", "security audit", "show config"]:
    display script output directly
    highlight warnings and errors
else:
    use minimal formatting
```

**步骤 3.2：** 除非明确要求，否则不显示原始执行命令
```pseudocode
# 不好：显示原始命令
"正在运行：/path/to/script.sh --flag"

# 好：显示结果
"健康检查结果：
  ✓ 核心文件存在
  ✓ 记忆在限制范围内
  ⚠ 需要日志轮转"
```

## 关键规则

1. **自然语言识别：** 识别每个指令的常见变体
2. **清洁输出：** 除非用户明确要求，否则不显示原始执行命令
3. **脚本路径：** 所有脚本通过 `${CLAUDE_PLUGIN_ROOT}/scripts/` 引用
4. **工作区路径：** 所有用户数据文件在 `~/workspace/` 或 `~/workspace/memory/`
5. **格式化：** 健康状态使用 emoji 指示器（🟢🟡🔴），人格使用（🪪），仪表盘使用（📊）
6. **检查点时间戳：** 始终包含 HH:MM 时间戳和上下文百分比
7. **委托：** 对于复杂操作（如切换预设），委托给相应技能
8. **错误处理：** 如果指令失败，显示有用的错误消息并建议替代方案
9. **帮助可访问性：** 使帮助指令易于发现且内容全面
10. **主动模式：** advisor on/off 应清楚地确认状态变更

## 错误场景

**缺少脚本：**
```
❌ 错误：未在 ${CLAUDE_PLUGIN_ROOT}/scripts/ 找到 health-check.sh
建议：运行 'persona setup' 初始化插件
```

**缺少工作区文件：**
```
❌ 错误：未在 ~/workspace/ 找到 SOUL.md
建议：运行 'persona setup' 创建您的人格配置
```

**未识别的指令：**
```
❌ 未知指令："statsu"
您是想说：status 吗？
输入 'help' 查看所有可用指令。
```

## 与其他技能的集成

- **persona-setup：** 委托预设切换
- **persona-coder：** 可能在重大重构前触发检查点
- **persona-heartbeat：** 由健康检查指令调用
- **persona-security：** 由安全审计指令调用

## 示例

**用户：** "how's my system"
**操作：** 运行 status 指令，显示带健康指标的仪表盘

**用户：** "save my progress"
**操作：** 运行 checkpoint 指令，提示当前任务/决策/恢复点

**用户：** "turn on advisor mode"
**操作：** 启用主动模式，确认激活

**用户：** "what can I do"
**操作：** 显示 help 指令及完整指令参考表
