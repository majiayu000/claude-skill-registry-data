---
name: checkpoint
preamble-tier: 2
version: 1.0.0
description: |
  保存与恢复工作状态检查点。会记录 git 状态、已做决定和剩余工作，
  让你在中断后能准确续跑，包含跨分支、跨 Conductor workspace handoff 的场景。
  当用户说“checkpoint”“保存进度”“我刚做到哪了”“resume”“我在做什么”
  或“接着上次做”时使用；也适合在 session 即将结束、用户要切换上下文、
  或长时间暂停前主动建议。 (gstack)
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
---
<!-- 中文参考译文。共享 preamble 见 ../SKILL.md。 -->

# /checkpoint

把当前工作状态落成可恢复的检查点，或者把之前的检查点重新读回来。

## 命令模式

- `/checkpoint` 或 `/checkpoint save`：保存当前状态
- `/checkpoint resume`：恢复最近或指定检查点
- `/checkpoint list`：列出可恢复检查点

## Save 流程

1. 收集 git 分支、改动文件、最近提交和当前任务上下文。
2. 用对话历史补齐摘要：
   - 当前在做什么
   - 已做过哪些决定
   - 剩余工作有哪些
   - 还有什么注意事项
3. 计算 session 持续时间。
4. 以固定格式写入 checkpoint 文件，并向用户确认：
   - `Title`
   - `Branch`
   - `File`
   - `Modified`
   - `Duration`

## Resume 流程

1. 找到当前分支或用户指定范围内的 checkpoint。
2. 读取 checkpoint，并回显：
   - 标题
   - 保存分支
   - 保存时间
   - 上次 session 时长
   - 状态
3. 用 `AskUserQuestion` 询问下一步：
   - 继续处理剩余工作
   - 显示完整 checkpoint
   - 只取上下文，不继续执行

## List 流程

- 默认只列当前分支的 checkpoint
- `--all` 时扩展到所有分支
- 输出为表格，重点显示日期、标题、状态，以及必要时的分支名

## 关键规则

- 这是状态保存 / 恢复技能，不修改业务代码。
- checkpoint 必须带分支名，便于跨 branch 恢复。
- checkpoint 文件只能追加，不能覆盖或删除旧记录。
- 优先从 git 状态和上下文里推断，不要把本可推断的信息都丢给用户回答。
