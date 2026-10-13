---
name: persona-setup
description: AI 人格操作系统首次运行设置向导。引导用户完成初始工作区配置，包括预设选择（编程助手、行政助理、营销助手或自定义人格）。检测现有安装，收集个性化上下文，使用模板构建工作区结构，配置 SOUL.md、USER.md 和 MEMORY.md 文件。触发关键词：setup、install、preset、get started、first run、fresh install、initialize、wizard、onboard、configure workspace、initial setup、persona configuration、设置、安装、初始化、向导、配置。
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - AskUserQuestion
---

# AI 人格操作系统设置向导

本技能引导用户完成 AI 人格操作系统的首次运行设置，在 `~/workspace` 创建个性化工作区并配置人格文件。

## 概述

设置向导执行以下操作：
1. 检测现有安装以避免覆盖用户数据
2. 展示预设选择菜单，提供 4 种人格模板
3. 通过交互式问题收集个性化上下文
4. 使用适当的模板和示例构建工作区结构
5. 显示完成摘要并提供可选的高级功能

## 关键规则

- **绝不要告诉用户运行命令** — 始终使用 Bash 工具直接执行命令
- **未经用户明确许可，绝不要修改现有工作区文件**
- 只存在 4 个已记录的预设（coding-assistant、executive-assistant、marketing-assistant、custom）
- 所有操作仅限于 `~/workspace` 范围内
- 高级功能（cron、网关、Discord）仅为可选提及，绝不强行推送

## 阶段 1：安装后检测

### 步骤 1.1：检查现有工作区

使用 Bash 工具检查 `~/workspace` 是否存在并包含核心文件：

```pseudocode
if [ -d ~/workspace ]; then
  existing_files = []
  for file in SOUL.md USER.md MEMORY.md; do
    if [ -f ~/workspace/$file ]; then
      existing_files.append(file)
    fi
  done

  if existing_files.length > 0; then
    state.workspace_exists = true
    state.existing_files = existing_files
  fi
fi
```

### 步骤 1.2：处理现有安装

如果 `state.workspace_exists == true`，通知用户：

"检测到 ~/workspace 下已有 AI 人格操作系统工作区，包含以下文件：[列出 state.existing_files]。此设置向导用于全新安装。您希望：
- 跳过设置，使用现有工作区
- 创建备份并重新初始化（将备份到 ~/workspace.backup.TIMESTAMP）
- 取消设置"

根据响应：
- **跳过**：以成功消息退出
- **备份**：使用 Bash 执行 `mv ~/workspace ~/workspace.backup.$(date +%Y%m%d_%H%M%S)`，然后进入阶段 2
- **取消**：正常退出

如果未检测到现有工作区，进入阶段 2。

## 阶段 2：预设选择

### 步骤 2.1：展示预设菜单

向用户展示以下**完全一致**的预设选择菜单（原文照搬）：

```
欢迎使用 AI 人格操作系统设置！

请选择一个预设以开始：

1. 编程助手
   - 协助软件开发、调试、代码审查
   - 主动建议测试、文档编写、代码重构
   - 跟踪项目、任务、技术决策

2. 行政助理
   - 管理日程、会议、邮件草稿
   - 主动提醒、截止日期跟踪、优先级管理
   - 处理通讯、报告、战略规划支持

3. 营销助手
   - 内容创作、活动策划、数据分析
   - 主动内容创意、发布提醒、趋势分析
   - 社交媒体管理、SEO 优化、受众洞察

4. 自定义人格
   - 定义自己的人格名称、角色和行为
   - 选择沟通风格和主动程度
   - 完全控制人格和能力

您希望选择哪个预设？（1-4）
```

### 步骤 2.2：捕获预设选择

使用 AskUserQuestion 获取选择：

```json
{
  "questions": [
    {
      "id": "preset_choice",
      "question": "您希望选择哪个预设？（1-4）",
      "default": "1"
    }
  ]
}
```

映射响应：
- `1` → `state.preset = "coding-assistant"`
- `2` → `state.preset = "executive-assistant"`
- `3` → `state.preset = "marketing-assistant"`
- `4` → `state.preset = "custom"`
- 模糊/不清楚的回答 → `state.preset = "coding-assistant"`（默认）

将预设存储在 `state.preset`。

## 阶段 3：收集个性化上下文

### 步骤 3.1：询问通用问题（预设 1-3）

对于预设 1、2 或 3，收集基本个性化信息：

```json
{
  "questions": [
    {
      "id": "user_name",
      "question": "您的名字是什么？",
      "default": "User"
    },
    {
      "id": "user_nickname",
      "question": "我该怎么称呼您？（昵称或首选名称）",
      "default": "<与 user_name 相同>"
    },
    {
      "id": "user_role",
      "question": "您的职业角色或职位是什么？",
      "default": "Professional"
    },
    {
      "id": "user_goal",
      "question": "您使用 AI 人格操作系统的主要目标是什么？",
      "default": "提高生产力"
    }
  ]
}
```

将响应存储在：
- `state.user_name`（默认："User"）
- `state.user_nickname`（默认：与 user_name 相同）
- `state.user_role`（默认："Professional"）
- `state.user_goal`（默认："提高生产力"）

设置预设特定的默认值：
- `state.persona_name = "Persona"`
- `state.persona_role = "personal assistant"`
- `state.comm_style = "c"`（平衡型）
- `state.proactive_level = "b"`（适度）

### 步骤 3.2：询问扩展问题（预设 4 - 自定义）

对于预设 4（自定义），收集所有个性化信息，包括人格配置：

```json
{
  "questions": [
    {
      "id": "user_name",
      "question": "您的名字是什么？",
      "default": "User"
    },
    {
      "id": "user_nickname",
      "question": "我该怎么称呼您？（昵称或首选名称）",
      "default": "<与 user_name 相同>"
    },
    {
      "id": "user_role",
      "question": "您的职业角色或职位是什么？",
      "default": "Professional"
    },
    {
      "id": "user_goal",
      "question": "您使用 AI 人格操作系统的主要目标是什么？",
      "default": "提高生产力"
    },
    {
      "id": "persona_name",
      "question": "您想给 AI 人格取什么名字？",
      "default": "Persona"
    },
    {
      "id": "persona_role",
      "question": "人格应扮演什么角色？（如"编程导师"、"行政助理"、"创意伙伴"）",
      "default": "personal assistant"
    },
    {
      "id": "comm_style",
      "question": "选择沟通风格：\n  a) 正式专业\n  b) 友好随和\n  c) 平衡型（专业但不失亲和力）\n  d) 技术精确\n您的选择（a-d）？",
      "default": "c"
    },
    {
      "id": "proactive_level",
      "question": "选择主动程度：\n  a) 仅响应式（等待请求）\n  b) 适度主动（偶尔建议）\n  c) 高度主动（频繁建议和提醒）\n您的选择（a-c）？",
      "default": "b"
    }
  ]
}
```

存储所有响应，默认值与步骤 3.1 相同，加上：
- `state.persona_name`（默认："Persona"）
- `state.persona_role`（默认："personal assistant"）
- `state.comm_style`（默认："c"）
- `state.proactive_level`（默认："b"）

## 阶段 4：构建工作区结构

### 步骤 4.1：创建目录结构

使用 Bash 工具创建工作区目录：

```pseudocode
mkdir -p ~/workspace/memory
mkdir -p ~/workspace/projects
mkdir -p ~/workspace/context
```

### 步骤 4.2：复制预设专属启动包

根据 `state.preset`，从插件资源复制适当的启动包：

```pseudocode
preset_examples = {
  "coding-assistant": "${CLAUDE_PLUGIN_ROOT}/examples/coding-assistant/",
  "executive-assistant": "${CLAUDE_PLUGIN_ROOT}/examples/executive-assistant/",
  "marketing-assistant": "${CLAUDE_PLUGIN_ROOT}/examples/marketing-assistant/",
  "custom": "${CLAUDE_PLUGIN_ROOT}/examples/custom/"
}

source_dir = preset_examples[state.preset]

# 将预设示例目录中的所有文件复制到 ~/workspace
cp -r ${source_dir}/* ~/workspace/
```

使用 Bash 工具执行复制操作。

### 步骤 4.3：复制共享模板

复制所有预设都需要的共享模板文件：

```pseudocode
# 复制 SOUL.md 模板
cp ${CLAUDE_PLUGIN_ROOT}/assets/SOUL.md.template ~/workspace/SOUL.md

# 复制 MEMORY.md 模板
cp ${CLAUDE_PLUGIN_ROOT}/assets/MEMORY.md.template ~/workspace/MEMORY.md
```

使用 Bash 工具执行复制操作。

### 步骤 4.4：个性化模板文件

使用 Bash 工具配合 `sed` 来个性化已复制的模板：

```pseudocode
# 个性化 SOUL.md
sed -i 's/{{PERSONA_NAME}}/'"${state.persona_name}"'/g' ~/workspace/SOUL.md
sed -i 's/{{PERSONA_ROLE}}/'"${state.persona_role}"'/g' ~/workspace/SOUL.md
sed -i 's/{{COMM_STYLE}}/'"${state.comm_style}"'/g' ~/workspace/SOUL.md
sed -i 's/{{PROACTIVE_LEVEL}}/'"${state.proactive_level}"'/g' ~/workspace/SOUL.md

# 个性化 MEMORY.md
sed -i 's/{{USER_NAME}}/'"${state.user_name}"'/g' ~/workspace/MEMORY.md
sed -i 's/{{USER_NICKNAME}}/'"${state.user_nickname}"'/g' ~/workspace/MEMORY.md
```

通过 Bash 工具使用 && 链接在一个调用中执行所有 sed 命令。

### 步骤 4.5：生成 USER.md

使用 heredoc 配合收集的信息创建 USER.md。使用 Bash 工具：

```bash
cat > ~/workspace/USER.md <<'EOF'
# 用户档案

## 基本信息

**姓名：** ${state.user_name}
**称呼：** ${state.user_nickname}
**角色：** ${state.user_role}
**主要目标：** ${state.user_goal}

## 工作区上下文

**预设：** ${state.preset}
**设置日期：** $(date +%Y-%m-%d)

## 偏好设置

沟通风格：参见 SOUL.md 中的人格配置
主动程度：参见 SOUL.md 中的人格配置

## 活跃项目

<!-- 此部分将在您工作时填充 -->

## 重要上下文

<!-- 添加 AI 应始终记住的任何上下文 -->

---

*此文件由 AI 人格操作系统设置向导生成。您可以随时编辑和扩展。*
EOF
```

执行前替换实际的变量值。

## 阶段 5：显示设置摘要

### 步骤 5.1：验证安装

使用 Bash 工具列出已创建的文件：

```bash
ls -la ~/workspace/
ls -la ~/workspace/memory/
```

将输出存储在 `state.workspace_contents`。

### 步骤 5.2：显示成功摘要

向用户展示包含文件检查清单的完成消息：

```
✓ AI 人格操作系统设置完成！

您的工作区已创建在 ~/workspace，包含以下结构：

核心文件：
  ✓ SOUL.md       - 人格配置和行为
  ✓ USER.md       - 您的档案和偏好
  ✓ MEMORY.md     - 跨会话的持久记忆

目录：
  ✓ memory/       - 会话日志和历史上下文
  ✓ projects/     - 项目专用文件和笔记
  ✓ context/      - 额外上下文文档

预设专属文件：
  [列出 state.workspace_contents 中的额外文件]

您的 ${state.preset} 人格已准备就绪！

下一步：
1. 审查并自定义 SOUL.md 以微调人格行为
2. 更新 USER.md 添加额外上下文
3. 启动新会话 — 您的人格将自动加载
```

### 步骤 5.3：提供可选高级功能（不强制）

将高级功能作为可选增强提及，绝不强制：

"您后续可以探索的可选高级功能：
- **心跳监控**：定期检查和进度跟踪
- **Cron 集成**：定时任务和自动化工作流
- **团队模式**：多用户工作区支持
- **Discord 集成**：通知和远程交互

这些都是完全可选的。您当前的设置已完全可用。您想了解其中任何功能的详情，还是准备好开始使用您的人格了？"

根据响应：
- 如果用户询问某个功能，提供简要说明并提及可以稍后配置
- 如果用户准备好开始，以以下信息结束："好的！您的 AI 人格操作系统已就绪。启动新会话，您的人格将从 ~/workspace 自动加载。"

## 状态管理

在整个执行过程中跟踪以下变量：

```pseudocode
state.workspace_exists = false  # 检测到 ~/workspace 时为 true
state.existing_files = []       # 现有核心文件列表
state.preset = ""               # 选定的预设标识
state.user_name = "User"
state.user_nickname = ""        # 默认为 user_name
state.user_role = "Professional"
state.user_goal = "提高生产力"
state.persona_name = "Persona"
state.persona_role = "personal assistant"
state.comm_style = "c"          # a/b/c/d
state.proactive_level = "b"     # a/b/c
state.workspace_contents = ""   # 创建后的 ls 输出
```

## 错误处理

### 缺少插件资源

如果在 `${CLAUDE_PLUGIN_ROOT}/assets/` 或 `${CLAUDE_PLUGIN_ROOT}/examples/` 未找到模板文件：

1. 使用 Glob 搜索插件根目录
2. 如果仍未找到，通知用户："设置向导需要 AI 人格操作系统插件资源。请确保插件已正确安装。"
3. 提供继续最小化设置的选项（创建目录和基本文件，不使用模板）

### 权限错误

如果 `mkdir` 或 `cp` 命令因权限错误失败：

1. 向用户展示错误消息
2. 建议检查目录权限："您可能需要对主目录的写入权限。"
3. 提供替代方案："您想指定不同的工作区位置吗？"

### 无效的预设选择

如果用户输入无法映射到 1-4：

1. 默认使用预设 1（coding-assistant）
2. 通知用户："默认使用编程助手预设。您可以稍后通过编辑 SOUL.md 来自定义您的人格。"

## 成功标准

设置完成条件：
- `~/workspace` 目录存在且结构正确
- SOUL.md、USER.md 和 MEMORY.md 已创建并个性化
- 预设专属示例文件已复制
- 用户收到确认摘要
- 目录创建和文件操作过程中无错误

## 注意事项

- 本技能创建**新的**工作区。如需修改现有工作区，用户应直接编辑文件或使用 persona-update 技能（如果可用）
- 模板替换使用简单的 sed 替换。对于复杂的个性化，考虑使用 Write 工具配合模板渲染
- 预设示例应包含适合各人格类型的启动文件（如 coding-assistant 包含示例项目结构，executive-assistant 包含会议模板等）
- 所有 Bash 操作应通过 Bash 工具执行，绝不要建议用户手动运行命令
