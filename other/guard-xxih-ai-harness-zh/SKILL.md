---
name: guard
version: 0.1.0
description: |
  完整安全模式：同时启用破坏性命令警告与目录级编辑边界。
  等于把 /careful 与 /freeze 合并到一条命令里。 (gstack)
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/../careful/bin/check-careful.sh"
          statusMessage: "Checking for destructive commands..."
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/../freeze/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/../freeze/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
---
<!-- 中文参考译文。 -->

# /guard

`/guard` 是 `/careful` + `/freeze` 的一体版。适用于生产环境、在线系统排障、或者你想把改动范围锁得非常死的时候。

## 设置步骤

1. 询问用户要把编辑范围限制在哪个目录。
2. 解析成绝对路径，并写入 freeze 状态文件。
3. 告知用户当前有两层保护：
   - 破坏性命令会先警告。
   - 目录外编辑会被硬性阻止。

## 依赖说明

- 这个 skill 直接复用相邻目录中的 `/careful` 与 `/freeze` hook 脚本。
- 因此这两个 skill 必须与 `/guard` 一起安装。

## 如何退出

- 只移除编辑边界：运行 `/unfreeze`
- 整体关闭：结束当前会话
