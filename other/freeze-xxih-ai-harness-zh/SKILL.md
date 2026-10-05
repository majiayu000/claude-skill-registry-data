---
name: freeze
version: 0.1.0
description: |
  把文件编辑限制在指定目录内。阻止对边界外文件的 Edit / Write。
  适用于调试、范围受限改动或希望只动单一模块的场景。 (gstack)
allowed-tools:
  - Bash
  - Read
  - AskUserQuestion
hooks:
  PreToolUse:
    - matcher: "Edit"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
    - matcher: "Write"
      hooks:
        - type: command
          command: "bash ${CLAUDE_SKILL_DIR}/bin/check-freeze.sh"
          statusMessage: "Checking freeze boundary..."
---
<!-- 中文参考译文。 -->

# /freeze

这个 skill 会把编辑权限锁到某个目录。目录外的 `Edit` / `Write` 不是警告，而是**直接阻止**。

## 设置步骤

1. 询问用户要把编辑范围限制到哪个目录。
2. 把用户给的路径解析成绝对路径。
3. 自动补全末尾 `/`，写入 `${CLAUDE_PLUGIN_DATA:-$HOME/.gstack}/freeze-dir.txt`。
4. 告知用户：当前只允许编辑该目录，修改边界请重新运行 `/freeze`，解除边界请运行 `/unfreeze`。

## 工作方式

- hook 从 Edit / Write 的工具输入中读取 `file_path`。
- 只有以 freeze 目录为前缀的路径才允许通过。
- 否则直接返回 `permissionDecision: "deny"`。

## 注意事项

- 目录末尾强制加 `/`，避免 `/src` 误匹配 `/src-old`。
- `freeze` 只拦截 `Edit` / `Write`，不影响 `Read`、`Bash`、`Glob`、`Grep`。
- 这是防误改边界，不是强安全边界；如果用 `sed` 一类 Bash 命令直接改文件，仍可能越界。
