---
name: safe-pull
description: >
  Safe Git pull with rebase workflow — check remote changes, stash, rebase, restore,
  handle conflicts, and push. Covers main/develop sync and feature branch rebase.
  Use when the user says "sync", "pull latest", "拉取最新", "rebase main", "同步代码",
  "update branch", or wants to safely pull remote changes preserving linear history.
---

# Safe Pull

安全拉取远程代码，使用 rebase 保持线性历史，自动暂存/恢复本地修改。

## 核心流程

```bash
# 1. 先看远程改了什么
git fetch && git log -p main..origin/main

# 2. 暂存本地修改
git stash

# 3. 用 rebase 而不是 merge（保持线性历史）
git pull --rebase

# 4. 恢复本地修改
git stash pop
```

## 完整流程

### 1. 检查远程变更

```bash
git fetch origin
git log --oneline <current-branch>..origin/<current-branch>
```

本地已是最新则直接结束。

### 2. 暂存本地修改

```bash
git status --short
git stash push -u -m "safe-pull: auto stash before rebase"
```

工作区干净则跳过。暂存失败则中止，报告原因。

### 3. Rebase 拉取

```bash
git pull --rebase origin <branch>
```

冲突时进入**冲突处理**子流程。网络失败重试一次，仍失败则中止。

### 4. 恢复本地修改

```bash
git stash pop
```

stash pop 冲突 → 保留 stash，列出冲突文件。空 stash → 跳过。

### 5. 推送（可选）

询问是否需要 `git push` 或 `git push --force-with-lease`。

## 冲突处理

1. `git diff --name-only --diff-filter=U` 列出冲突文件
2. 告知用户冲突内容，**不自动解决**
3. 用户解决后：`git rebase --continue`
4. 用户确认放弃：`git rebase --abort && git stash pop`

## 回滚

```bash
git rebase --abort 2>/dev/null
git stash list | grep "safe-pull:" && git stash pop
```

## 规则

- **禁止** `--no-verify`、`--no-gpg-sign`，**禁止** `git reset --hard` 在 dirty tree 时执行
- **禁止** 对 main/master 执行 `--force` push
- stash 用 `-u` 包含 untracked 文件
- 操作前告知当前分支和目标分支

## 分支场景

| 场景 | 目标分支 | 流程 |
|------|---------|------|
| 同步 main/develop | `origin/main` 或 `origin/develop` | 标准四步 |
| Feature 分支 rebase develop | `origin/develop` | 标准四步 + `--force-with-lease` push |
| 多分支同步 | 依次执行 | 每个分支独立走标准流程 |

## 完成标准

- 本地分支与远程同步，线性历史。
- 本地修改已恢复（或用户已知冲突待处理）。
- 如已推送，远程分支也已更新。
