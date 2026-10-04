---
name: cc-bash-style
description: Bash、Shell、Dockerfile、Makefile 与命令片段规范，适用于脚本修改、命令编写和文档中的 shell 示例；不负责运维审批策略。
---

# CC Bash Style

在编写或修改 shell 脚本、Dockerfile、Makefile、命令示例时，使用本技能保持脚本风格一致且可维护。

不要用于：

- 运维风险评估或审批判断
- 语言无关的通用编码原则
- 正式 review 或 debug 工作流

## 核心规则

- 保持脚本直接、可读、可复制执行。
- 注释单独成行，不写行尾注释。
- 优先使用清晰的 heredoc、`tee` 和分步命令。
- 避免不必要的 shell 花活和难以审查的复合命令。

## 按需展开

- 注释规范：`references/bash-comments.md`
- heredoc 使用：`references/heredoc.md`
- `tee` 写入：`references/tee-write.md`
