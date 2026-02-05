---
name: zellij-control
description: 使用 Zellij 终端复用器控制交互式 CLI 程序。当需要运行需要键盘交互的 TUI 应用（htop、btop、lazygit、fzf）、REPL（python、bun repl）或分页器（less、bat）时使用此技能。不适用于非交互式命令（直接用 Bash）或文件编辑（直接用 Edit 工具）。
---

# Zellij 交互式命令控制

## 核心命令

```bash
# 获取会话名
zellij list-sessions

# 发送文本和按键（始终以 zellij 开头，便于批量授权）
zellij -s SESSION_NAME action write-chars 'command'
zellij -s SESSION_NAME action write-chars $'\n'     # Enter
zellij -s SESSION_NAME action write-chars $'\x1b'   # ESC
zellij -s SESSION_NAME action write-chars $'\x03'   # Ctrl+C
zellij -s SESSION_NAME action write-chars $'\x04'   # Ctrl+D
zellij -s SESSION_NAME action write-chars $'\t'     # Tab
zellij -s SESSION_NAME action write-chars $'\x7f'   # Backspace

# 方向键
zellij -s SESSION_NAME action write-chars $'\x1b[A'  # 上
zellij -s SESSION_NAME action write-chars $'\x1b[B'  # 下
zellij -s SESSION_NAME action write-chars $'\x1b[C'  # 右
zellij -s SESSION_NAME action write-chars $'\x1b[D'  # 左

# 读取屏幕（用 /dev/shm 内存文件系统，不写磁盘）
zellij -s SESSION_NAME action dump-screen /dev/shm/zj.txt && cat /dev/shm/zj.txt
zellij -s SESSION_NAME action dump-screen --full /dev/shm/zj.txt  # 含回滚历史
```

## 窗格管理

```bash
zellij -s SESSION_NAME action new-pane              # 新窗格
zellij -s SESSION_NAME action new-pane -d right     # 向右
zellij -s SESSION_NAME action new-pane -d down      # 向下
zellij -s SESSION_NAME action close-pane            # 关闭当前窗格
zellij -s SESSION_NAME action focus-next-pane       # 下一窗格
zellij -s SESSION_NAME action move-focus right      # 向右移动焦点
```

## 常用工具退出方式

| 工具 | 退出键 |
|------|-------|
| htop, btop, lazygit, less, bat | `q` |
| fzf | `ESC` 或 `Enter` |
| Python REPL | `Ctrl+D` ($'\x04') |
| Bun REPL | `.exit` + Enter |

## 工作流程

```bash
# 1. 获取会话
zellij list-sessions

# 2. 运行交互式程序
zellij -s SESSION_NAME action write-chars 'htop'
zellij -s SESSION_NAME action write-chars $'\n'
sleep 2

# 3. 读取输出
zellij -s SESSION_NAME action dump-screen /dev/shm/zj.txt && cat /dev/shm/zj.txt

# 4. 退出程序
zellij -s SESSION_NAME action write-chars 'q'
```

## 注意事项

- 始终在命令后发送 Enter (`$'\n'`)
- 等待程序渲染 (`sleep 1-3`)
- dump-screen 只支持文件路径，用 `/dev/shm/zj.txt` 避免写磁盘
- 文件编辑用 Claude Code 的 Edit 工具，无需 zellij
- 不确定时递归查看帮助：`zellij --help`、`zellij action --help`、`zellij action <cmd> --help`
- **重要**：bash 命令必须以 `zellij` 开头，不要用注释或变量赋值开头，否则需要逐一授权
