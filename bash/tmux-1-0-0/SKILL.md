---
name: tmux
description: "通过发送击键和抓取窗格输出来远程控制交互式 CLI 的 tmux 会话。"
metadata: {"clawdbot":{"emoji":"🧵","os":["darwin","linux"],"requires":{"bins":["tmux"]}}}
---

# tmux 技能 (Clawdbot)

仅当您需要交互式 TTY 时才使用 tmux。对于长时间运行的非交互式任务，首选 bash 后台模式。

## 快速入门（隔离套接字、bash 工具）

```bash
SOCKET_DIR="${CLAWDBOT_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/clawdbot-tmux-sockets}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/clawdbot.sock"
SESSION=clawdbot-python

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- 'PYTHON_BASIC_REPL=1 python3 -q' Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
```

启动会话后，始终打印监视器命令：

```
监控命令:
  tmux -S "$SOCKET" attach -t "$SESSION"
  tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
```

## 套接字约定

- 使用 `CLAWDBOT_TMUX_SOCKET_DIR`（默认 `${TMPDIR:-/tmp}/clawdbot-tmux-sockets`）。
- 默认套接字路径：`"$CLAWDBOT_TMUX_SOCKET_DIR/clawdbot.sock"`。

## 定位窗格和命名

- 目标格式：`session:window.pane`（默认为 `:0.0`）。
- 名称要简短；避免空格。
- 检查：`tmux -S "$SOCKET" list-sessions`、`tmux -S "$SOCKET" list-panes -a`。

## 查找会话

- 列出套接字上的会话：`{baseDir}/scripts/find-sessions.sh -S "$SOCKET"`。
- 扫描所有套接字：`{baseDir}/scripts/find-sessions.sh --all`（使用 `CLAWDBOT_TMUX_SOCKET_DIR`）。

## 安全发送输入

- 首选文字发送：`tmux -S "$SOCKET" send-keys -t target -l -- "$cmd"`。
- 控制键：`tmux -S "$SOCKET" send-keys -t target C-c`。

## 观察输出

- 捕获最近的历史记录：`tmux -S "$SOCKET" capture-pane -p -J -t target -S -200`。
- 等待提示：`{baseDir}/scripts/wait-for-text.sh -t session:0.0 -p 'pattern'`。
- 连接即可；使用 `Ctrl+b d` 分离。

## 生成进程

- 对于 python REPL，设置 `PYTHON_BASIC_REPL=1`（非基本 REPL 会中断发送密钥流）。

## Windows / WSL

- macOS/Linux 支持 tmux。在 Windows 上，使用 WSL 并在 WSL 内安装 tmux。
- 此技能与 `darwin`/`linux` 相关，并且需要在 PATH 上添加 `tmux`。

## 编排编码代理（Codex、Claude Code）

tmux 擅长并行运行多个编码代理：

```bash
SOCKET="${TMPDIR:-/tmp}/codex-army.sock"

# 创建多个会话
for i in 1 2 3 4 5; do
  tmux -S "$SOCKET" new-session -d -s "agent-$i"
done

# 在不同的工作目录中启动代理
tmux -S "$SOCKET" send-keys -t agent-1 "cd /tmp/project1 && codex --yolo 'Fix bug X'" Enter
tmux -S "$SOCKET" send-keys -t agent-2 "cd /tmp/project2 && codex --yolo 'Fix bug Y'" Enter

# 轮询完成状态（检查是否返回提示符）
for sess in agent-1 agent-2; do
  if tmux -S "$SOCKET" capture-pane -p -t "$sess" -S -3 | grep -q "❯"; then
    echo "$sess: 完成"
  else
    echo "$sess: 运行中..."
  fi
done

# 从已完成的会话获取完整输出
tmux -S "$SOCKET" capture-pane -p -t agent-1 -S -500
```

**提示：**
- 使用单独的 git 工作树进行并行修复（无分支冲突）
- 在新克隆中运行 codex 之前先进行 `pnpm install`
- 检查 shell 提示符（`❯` 或 `$`）以检测完成情况
- Codex 需要 `--yolo` 或 `--full-auto` 来进行非交互式修复

## 清理

- 终止会话：`tmux -S "$SOCKET" kill-session -t "$SESSION"`。
- 终止套接字上的所有会话：`tmux -S "$SOCKET" list-sessions -F '#{session_name}' | xargs -r -n1 tmux -S "$SOCKET" kill-session -t`。
- 删除私有套接字上的所有内容：`tmux -S "$SOCKET" kill-server`。

## 助手：wait-for-text.sh

`{baseDir}/scripts/wait-for-text.sh` 轮询窗格中是否有超时的正则表达式（或固定字符串）。

```bash
{baseDir}/scripts/wait-for-text.sh -t session:0.0 -p 'pattern' [-F] [-T 20] [-i 0.5] [-l 2000]
```

- `-t`/`--target` 窗格目标（必需）
- `-p`/`--pattern` 要匹配的正则表达式（必需）；添加 `-F` 用于固定字符串
- `-T` 超时秒数（整数，默认 15）
- `-i` 轮询间隔秒（默认 0.5）
- `-l` 要搜索的历史行（整数，默认 1000）
