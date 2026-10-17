---
name: clean-branches
description: "清理本地和远程已合并的 Git 分支。扫描所有本地分支和远程 tracking branches，标记已合并入当前分支的分支，一次性列表让用户勾选确认后删除并验证结果。使用场景包括：分支太多要清理、合并后残留、worktree 未清理、远程 stale branches。当用户提到 清理分支/删分支/整理分支/clean branches/branch cleanup/prune branches/git clean 时务必使用。对于合并后残留的发布分支、废弃的功能分支、已修复的 bugfix 分支尤其适用。"
---

# Clean Branches

清理已合入的 Git 分支，联动删除本地和远程。

## 核心流程

### 1. 收集状态

并行执行以下命令：

```bash
# 当前分支 + 本地全部分支 + 跟踪关系
git branch -vv

# worktree 列表（防止误删正在使用的分支）
wt list 2>/dev/null || git worktree list

# 所有远程分支
git branch -r

# 已合并入当前分支的本地分支（排除当前分支和 main/master）
git branch --merged | sed 's/^\* //' | grep -vE '^(main|master|develop|HEAD)$' | grep -v "^$(git rev-parse --abbrev-ref HEAD)$"

# 检测 squash merge（GitHub squash merge 无 merge commit，--merged 不识别）
# 两类检测方法：
#   a) release/* 分支：匹配对应 tag 是否存在（release 分支的 version bump 使 three-dot diff 永远非空）
#      如 release/<version> -> 查 v<version> tag
#   b) 其他分支：three-dot diff 为空 -> 分支内容已合入
git branch | sed 's/^\* //' | grep -vE '^(main|master|develop|HEAD)$' | grep -v "^$(git rev-parse --abbrev-ref HEAD)$" | while read -r b; do
  b="${b# }"  # 去掉可能的前导空格
  git merge-base --is-ancestor "$b" HEAD 2>/dev/null && continue

  # release/* 分支用 tag 检测
  if echo "$b" | grep -qE '^release/'; then
    ver=$(echo "$b" | sed 's/^release\///')
    if git tag -l "v$ver" | grep -q .; then
      echo "$b  [squash-merged] (tag v$ver exists)"
      continue
    fi
  fi

  # 非 release 分支用 three-dot diff
  git diff --quiet HEAD..."$b" 2>/dev/null && echo "$b  [squash-merged]"
done

# 已合并入当前分支的远程 tracking branches（如有 origin）
git branch -r --merged origin/HEAD 2>/dev/null | sed 's/^\* //' | grep -vE '^(origin/HEAD|origin/main|origin/master)$'

# 检测远程 squash merge 的分支
git branch -r | sed 's/^\* //' | grep -vE '^(origin/HEAD|origin/main|origin/master)$' | while read -r r; do
  r="${r# }"
  git merge-base --is-ancestor "$r" HEAD 2>/dev/null && continue

  # release/* 分支用 tag 检测
  local_name="${r#origin/}"
  if echo "$local_name" | grep -qE '^release/'; then
    ver=$(echo "$local_name" | sed 's/^release\///')
    if git tag -l "v$ver" | grep -q .; then
      echo "$r  [squash-merged] (tag v$ver exists)"
      continue
    fi
  fi

  # 非 release 分支用 three-dot diff
  git diff --quiet HEAD..."$r" 2>/dev/null && echo "$r  [squash-merged]"
done
```

### 2. 分析并呈现

组装一张完整表格，包含：

| 类型 | 分支名 | 最新提交 | 状态 | 关联 worktree | 建议 |
|---|---|---|---|---|---|
| local | feature/xxx | abc123 | 已合并 | 否 | 可删 |
| local | release/x.y.z | def456 | [squash-merged] (tag vx.y.z exists) | 否 | 可删 |
| remote | origin/xxx | ghi789 | 已合并 | - | 可删 |

关键规则：
- **保护当前分支**和 `main`/`master`，绝不建议删除
- **保护 `develop` 分支**（如果当前不在 develop 上，develop 作为长期分支也应保护）
- **有活跃 worktree 的分支**标记为"使用中"，需要用户明确确认才删
- **未合并的分支**标记为"未合并"，说明风险
- **远程有而本地无的分支**如果已合并，标记可删
- **squash-merged 的分支**（含 `[squash-merged]` 标记）视为已合并，标记可删。检测方式：`release/*` 分支检查对应 tag 是否存在（如 `release/0.7.6` -> 查 `v0.7.6` tag）；非 release 分支用 three-dot diff 为空判断内容已合入

### 3. 一次性确认

**不要逐个问。** 一次性呈现完整表格，让用户用编号或批量范围来选：

```
以下分支已合并入当前分支 (develop)，建议删除：

本地 (6):
  1. release/v0.2.0        [4963987] [squash-merged] 可删
  2. feature/payment       [548ad1f] 已合并 可删
  3. feature/ui-taste      [4dfcf23] 已合并 可删
  ...

远程 (3):
  a. origin/feature/payment  已合并 可删
  b. origin/bugfix/login     [squash-merged] 可删
  ...

请选择要删除的分支（如 1,2,3,a,b 或 all）：
```

如果用户说"合并了的都删"或"all"，直接执行全部。

### 4. 执行删除

```bash
# 删除本地分支（安全删除，仅合并过的才会成功）
git branch -d <branch1> <branch2> ...

# 删除远程分支
git push origin --delete <branch1> <branch2> ...
```

### 5. 验证并报告

```bash
git branch -vv
git branch -r
```

输出最终状态，确认清理结果。如果有因未合并而删除失败的分支，单独列出说明。

## 安全防护

- **绝不**在删除前运行 `git fetch --prune` 或 `git remote prune` — 这会让用户丢失远程分支引用，应先让用户确认
- 使用 `git branch -d`（小写 d，安全模式），不是 `-D`（大写 D，强制删除）
- 如果用户要求强制删除未合并分支，必须先警告丢失提交的风险
- 如果当前 worktree 是 detached HEAD、rebase 中、merge 中，先警告不清理
