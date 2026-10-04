---
name: git-push-secondary-merge-primary-cn
description: 当用户需要提交并推送工作分支，再合并到主分支并推送双分支结果时使用。
---

# Git 推送副分支并合并主分支

## Overview

执行标准的双分支交接流程：在副分支完成工作并推送，再合并到主分支并推送，最后切回副分支。

- **副分支**：承载当前工作的分支，如 `dev`、`develop` 或其他集成分支。
- **主分支**：受保护的发布分支，如 `main` 或 `master`。

这个流程适合需要同时推送副分支和主分支的发布同步场景，并尽量保留主分支上清晰的合并结果。

## 何时使用

当用户要求执行以下操作时使用本技能：
- 推送工作分支后再合并到发布分支
- 双分支同步发布流程，例如 `dev` → `main` 或 `develop` → `master`
- 在副分支完成功能后同步到主分支
- 保留主分支上的清晰合并提交，同时不丢失副分支的提交历史

## 不要使用

以下场景不要使用本技能：
- 单分支的提交/推送（使用普通的 commit + push 流程）
- 强制推送、改写历史或 rebase 操作
- 从 Git 历史生成汇总报告（请使用 `git-weekly-report-cn`）
- 评审代码变更（请使用 `code-reviewer` 或 `frontend-code-review`）

## 使用说明

先按分支识别规则确定主分支和副分支，再按工作流程顺序执行。遇到分支名不明确、合并冲突、脏工作区或推送被拒绝且无法安全处理时，停止并说明阻塞原因，不要猜测执行。

## 分支识别

1. 优先采用用户显式指定的分支名。
2. 当用户说 `dev` 或 `main`，但仓库实际使用 `develop` 或 `master` 时，先核对真实分支再选择。
3. 优先通过 `git symbolic-ref refs/remotes/origin/HEAD` 识别主分支。
4. 远端 HEAD 不可用时，优先选择已存在的 `main`，其次 `master`。
5. 当前分支若不是主分支，就将其视为副分支。
6. 若当前已在主分支且未指定副分支，优先选择已存在的 `dev`，其次 `develop`。
7. 仍无法安全确定时，向用户询问主分支和副分支名称。

## 使用说明

严格执行以下工作流程，保留用户改动，并在分支、合并或推送条件不安全时停止。

## 工作流程

1. 检查仓库状态。
   - 运行 `git status --short`、`git branch --show-current`、`git remote -v`。
   - 确认工作区属于目标仓库。
   - 不得丢弃或回滚用户改动。
   - 按分支识别规则确定 `<secondary_branch>` 和 `<primary_branch>`。

2. 将工作切换到 `<secondary_branch>`。
   - 已经在 `<secondary_branch>` 上则继续。
   - 当前在其他分支且工作区有未提交改动时，只有 Git 允许干净切换才执行；否则停下来向用户说明阻塞原因。
   - 当前在其他干净分支时，执行 `git checkout <secondary_branch>` 与 `git pull --ff-only origin <secondary_branch>`。

3. 如果 `<secondary_branch>` 上有本地改动，先提交。
   - 使用 `git add` 暂存相关变更，除非用户要求更小的范围。
   - 生成符合 Conventional Commits 的提交信息：英文 `type(scope):` 前缀 + 冒号后接中文摘要。
   - 不允许使用 `--no-verify`。
   - 钩子或校验失败时，先修复问题再提交。
   - 若 `<secondary_branch>` 无本地改动，跳过提交直接进入推送步骤。

4. 推送 `<secondary_branch>`。
   - 执行 `git push origin <secondary_branch>`。
   - 推送因远端更新而被拒绝时，先 `git fetch` 并查看再重试；除非用户明确要求，否则不执行强制推送。

5. 合并到 `<primary_branch>`。
   - 执行 `git checkout <primary_branch>`。
   - 执行 `git pull --ff-only origin <primary_branch>`。
   - 当 `<primary_branch>` 未包含 `<secondary_branch>` 时，使用 `git merge --no-ff <secondary_branch> -m "chore(<primary_branch>): 合并 <secondary_branch> 到 <primary_branch>"` 保留合并提交。
   - 出现合并冲突时立即停止，列出需要用户解决的文件。

6. 推送 `<primary_branch>`。
   - 执行 `git push origin <primary_branch>`。

7. 切回 `<secondary_branch>`。
   - 执行 `git checkout <secondary_branch>`。
   - 通过 `git status --short` 和 `git branch --show-current` 复核。
   - 最终所在分支必须是 `<secondary_branch>`。
   - 汇报副分支提交 SHA、（若存在）主分支合并提交 SHA、已推送的分支和最终所在分支。

## 汇报

保持最终回复简洁。包含成功推送的分支与提交哈希。若宿主应用支持 Git 指令，仅在对应 Git 动作成功后再发出相关指令。
