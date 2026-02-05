---
name: tel-start
description: 启动 Telegram Webhook 服务器（主服务器或项目服务器）
allowed-tools: Bash, Read, AskUserQuestion
---

# 启动 Telegram Webhook 服务器

## 目的
在 tmux session 中启动 Claude Code + Telegram 集成系统的 webhook 服务器。
- **主服务器模式**: 在 `main` session 中运行，使用 `~/.claude-telegram/config.json`
- **项目模式**: 在项目特定 session 中运行，使用项目的 `.claude-telegram/config.json`

## 架构说明

### Session 命名规则
- **main**: 主服务器 session（全局，不属于任何项目）
- **<project-name>**: 项目 session（每个项目独立）

### 配置文件优先级
1. 当前目录 `.claude-telegram/config.json`（项目配置）
2. `~/.claude-telegram/config.json`（主配置）

### Session 名称确定逻辑
1. 检查配置文件中的 `claude.session_name`
2. 如果未配置，检查是否为 git 仓库，使用仓库名
3. 如果不是 git 仓库，使用当前目录名

### 端口分配
- 主服务器: 8000（固定）
- 项目服务器: 从 8100 开始递增（8100, 8101, 8102...）

## 执行逻辑

**默认行为**: 总是启动主服务器（main session）。

### 1. 启动主服务器

直接运行 tel-start 启动主服务器：
```bash
./.claude/templates/tel-start.sh
```

### 2. 读取项目列表并询问用户

读取 `~/.claude-telegram/sessions.json` 获取最近使用的项目：
```bash
cat ~/.claude-telegram/sessions.json
```

使用 AskUserQuestion 询问用户要启动哪些项目服务器（支持多选）。

### 3. 为每个选中的项目启动服务器

对每个项目执行：
```bash
cd <project_path> && ./.claude/templates/tel-start.sh
```

### 3. tel-start 内部流程

**检查依赖**
- 检查 Python 库（flask, requests）
- 缺少则自动安装

**启动 Cloudflared Tunnel**
- 检查 cloudflared 进程是否运行
- 自动查找 cloudflared 可执行文件（/opt/homebrew/bin, /usr/local/bin, ~/bin）
- 从配置读取 tunnel 名称（默认: claude-bot）
- 后台启动 tunnel，日志输出到 `~/.claude-telegram/logs/cloudflared.log`
- 等待 3 秒确保连接建立

**确保主服务器运行**
- 检查 `main` session 是否存在，存在则重启
- 自动启动/重启主服务器（端口 8000）
- 使用 `~/.claude-telegram/config.json`

**查找项目配置文件**
- 优先使用 `.claude-telegram/config.json`
- 否则使用 `~/.claude-telegram/config.json`

**确定项目 session 名称**
- 从配置读取 `claude.session_name`
- 或从 git 仓库名获取
- 或使用当前目录名

**获取端口号**
- 从配置读取或自动分配（从 8100 开始递增）

**检查/创建 tmux session**
```bash
tmux has-session -t <session_name> 2>/dev/null || tmux new-session -d -s <session_name>
```

**在 session 中启动服务器**
```bash
tmux send-keys -t <session_name> "cd $(pwd)" C-m
tmux send-keys -t <session_name> "export TEL_CONFIG='<config_file>'" C-m
tmux send-keys -t <session_name> "export TEL_PORT='<port>'" C-m
tmux send-keys -t <session_name> "python3 <project_root>/webhook_server.py" C-m
```

**健康检查**
```bash
curl -s http://127.0.0.1:<port>/health
```

**记录到历史**
- 将 session 信息保存到 `~/.claude-telegram/sessions.json`
- 保留最近 10 个项目

## 工具需求
- Bash（执行命令）
- Read（读取 sessions.json）
- AskUserQuestion（询问用户选择项目）

## 成功输出

### 主服务器启动
```
✅ 全局命令已安装: /usr/local/bin/tel-start
✅ 依赖检查通过

🔹 检查 cloudflared tunnel 状态...
🔹 启动 cloudflared tunnel: claude-bot
✅ Cloudflared tunnel 已启动
✅ 日志文件: /Users/tk/.claude-telegram/logs/cloudflared.log

✅ 配置验证通过 (~/.claude-telegram/config.json)

🚀 启动主服务器...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 主服务器已启动
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 Session: main
🌐 服务地址: http://127.0.0.1:8000
🌐 公网地址: https://claude-bot.blueif.me
📊 健康检查: http://127.0.0.1:8000/health
📝 日志文件: ~/.claude-telegram/logs/webhook.log

可用端点:
  • /claude-hook - 接收 Claude Code 通知
  • /telegram-webhook - 接收 Telegram 命令
  • /health - 健康检查

查看 session: tmux attach -t main
```

### 项目服务器启动
```
✅ 全局命令已安装: /usr/local/bin/tel-start
✅ 依赖检查通过
✅ 配置验证通过 (.claude-telegram/config.json)

🚀 启动项目服务器...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 项目服务器已启动
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 Session: my-project
🔹 项目路径: /path/to/my-project
🌐 服务地址: http://127.0.0.1:8100
📊 健康检查: http://127.0.0.1:8100/health
📝 日志文件: /path/to/my-project/logs/webhook.log

查看 session: tmux attach -t my-project
```

## 错误处理

### 全局命令未安装
```
⚠️  tel-start 命令未安装

运行安装脚本:
./.claude/templates/install-tel-start.sh

是否现在安装？[y/N]
```

### 缺少依赖
```
❌ 缺少依赖: tmux, jq
请运行: ./setup.sh
```

### 配置无效
```
❌ 配置文件未找到
请创建以下任一配置文件:
  • .claude-telegram/config.json (项目配置)
  • ~/.claude-telegram/config.json (主配置)
```

### 端口被占用
```
⚠️  端口 8100 已被占用
PID: 12345 (python3 webhook_server.py)

建议操作:
  • 终止现有进程: kill 12345
  • 或使用其他端口（修改配置文件）
```

## 使用场景

### 1. 首次使用 - 安装全局命令
```
用户: /tel-start
Claude: 检测到 tel-start 未安装，是否安装？
用户: 是
Claude: 执行安装命令
```

### 2. 在项目目录直接启动（bash）
```bash
cd /path/to/my-project
tel-start
```

**执行结果**：
1. 自动检查并启动主服务器（如果未运行）
2. 启动当前项目的服务器
3. 记录到 sessions 历史

### 3. 使用 Skill 启动多个项目
```
用户: /tel-start
Claude:
  1. 检查并启动主服务器
  2. 读取最近的项目列表
  3. 显示选项：
     [ ] my-project (/path/to/my-project) - 上次使用: 2小时前
     [ ] another-project (/path/to/another) - 上次使用: 1天前
     [ ] 输入新项目路径
用户: 选择 my-project 和 another-project
Claude:
  cd /path/to/my-project && tel-start
  cd /path/to/another && tel-start
```

### 4. 只启动主服务器
```bash
# 在任意目录执行，如果没有项目配置，只启动主服务器
cd ~
tel-start
```

**注意**: 实际上你不会这样做，因为 tel-start 总是会尝试启动项目服务器。
如果只想启动主服务器，可以直接检查 tmux session。

## 相关命令

- `tel-start` - 全局启动命令
- `tmux attach -t <session>` - 连接到 session
- `tmux list-sessions` - 查看所有 session
- `./setup.sh` - 完整设置向导
- `./tests/test_local_only.sh` - 测试本地功能
