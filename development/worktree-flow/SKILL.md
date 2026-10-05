---
name: worktree-flow
description: 用 git worktree 在同一个仓库里跑多分支并行的全生命周期 SOP——从 base 分支开新 worktree + 新临时分支，本地干活，合回 base，销毁 worktree，销毁分支。触发：用户说"开一个 worktree / 起一个新分支并行干 / wt 一下 / 切到一个新工作区 / 把这个 worktree 收尾 / 干完合回 main / 清掉这个临时分支"，或者同时想跑两件事不想 stash。本 skill 只负责生命周期纪律，不替代具体仓库的 release / PR / review 流程。
---

# worktree-flow

Git worktree 让你在**同一个仓库**里同时挂载多个工作目录、每个目录跟着不同分支走，互不打扰。这条 skill 是它的"开-合-销毁"全套纪律。

## 概念

| 词 | 在本 skill 里的意思 |
| --- | --- |
| **base 分支** | 你想从哪条分支出发，干完之后再合回那条分支。最常见是 `main` / `master` / `develop`，也可以是 `feat/big-feature` 这种本来就是临时主干的分支 |
| **临时分支** | 在 worktree 里实际干活的分支，从 base 分叉出来 |
| **worktree** | 一个挂载到磁盘上的工作目录，跟着一条分支走。一个 git 仓库可以有多个 worktree，主仓本身算"主 worktree" |
| **主仓** | 你 `git clone` 出来的那个目录 |

> 一条分支同一时间只能被一个 worktree 持有。要在不同 worktree 切到同一条分支，必须先把另一边的 worktree 移到别的分支或先销毁。

## 适用场景

- 在不打断当前主线工作的前提下，临时插一个修复 / 实验 / review 别人的 PR
- 同时跑两个长任务（一个 build / 一个 test）互不抢工作树
- AI agent / 长跑 codegen 在隔离副本里干活，不污染主仓
- 需要在两个分支间对比看代码而又不想反复 `git stash`

## 不适用

- 跨仓库的并行：那是多 clone 的事
- 想保留分支但**不想再用它的代码**：用 `git branch --orphan` 或干脆 push 完就放着，别走 worktree

## 完整生命周期

### 0. 选定 base

```bash
git -C <主仓> fetch origin
git -C <主仓> rev-parse origin/<base>   # 确认 base 存在且最新
```

> base 必须是你**想合回去**的分支。如果你只是想要一个干净的 sandbox 不打算合回，跳过后面的"合回 base"，但仍然要按 cleanup 步骤销毁。

### 1. 起 worktree + 临时分支

约定：

- 临时分支名：`wt/<purpose>-<short-slug>`，例如 `wt/fix-login-redirect`、`wt/spike-mongo-vs-pg`
- worktree 目录：放在主仓**同级**目录的 `<repo>--<branch-slug>/`，例如主仓在 `~/workspace/foo/`，worktree 就在 `~/workspace/foo--wt-fix-login-redirect/`

```bash
cd <主仓>
branch="wt/fix-login-redirect"
wt_dir="../$(basename "$PWD")--${branch//\//-}"

git worktree add -b "$branch" "$wt_dir" "origin/<base>"
cd "$wt_dir"
```

`-b "$branch" ... "origin/<base>"` 这一组合，等价于"从 `origin/<base>` 拉一条新分支 `wt/...` 出来，并且把这条新分支挂到 `$wt_dir`"。

> 不要从本地 `<base>` 拉，本地的 base 可能落后 origin。除非你**特意**想在落后的 base 上分叉。

### 2. 干活

在 `$wt_dir` 里像正常仓库一样工作。规则：

- 不要 `git checkout <base>` 切回 base——直接去主仓做这件事；worktree 就让它一直跟着自己的临时分支
- commit / rebase / cherry-pick 自由
- 推到 remote 可选：本地 PR / review / archive 才需要 push；纯本地短 spike 可以全程不 push

### 3. 合回 base（如果要合）

把临时分支合回 base，**有三种主流策略**，选其一：

| 策略 | 何时用 | 命令 |
| --- | --- | --- |
| **fast-forward**（最简单） | 临时分支始终是 base 的线性延伸（没人在 base 上又提交东西） | 见下 |
| **squash merge** | 临时分支里有一堆中间提交，base 上只想看到一条干净 commit | 见下 |
| **rebase-then-ff** | 想保留所有 commit 但要线性历史 | 见下 |

> 不推荐用默认的 `git merge`（会生成 merge commit），除非你的项目历史本来就允许 merge commit。

#### 3a. fast-forward

```bash
cd <主仓>
git fetch origin
git checkout <base>
git pull --ff-only origin <base>
git merge --ff-only "$branch"
git push origin <base>   # 如果 base 是要推上去的
```

`--ff-only` 关键——如果不能 fast-forward 就报错，逼你回去 rebase 临时分支。

#### 3b. squash merge

```bash
cd <主仓>
git fetch origin
git checkout <base>
git pull --ff-only origin <base>
git merge --squash "$branch"
git commit -m "<summary of $branch>"
git push origin <base>
```

#### 3c. rebase-then-ff

```bash
cd "$wt_dir"
git fetch origin
git rebase origin/<base>   # 把临时分支 rebase 到最新 base
# 解冲突，重测
cd <主仓>
git checkout <base>
git pull --ff-only origin <base>
git merge --ff-only "$branch"
git push origin <base>
```

### 4. 销毁 worktree + 销毁分支

合完（或者决定放弃）后**马上**清理。不清就是技术债。

```bash
cd <主仓>

# 4.1 销毁 worktree（物理目录会被删）
git worktree remove "$wt_dir"

# 4.2 销毁本地分支
git branch -d "$branch"        # -d：要求已合并；没合并会拒绝
# 如果是放弃不合并的实验分支：
# git branch -D "$branch"      # -D：强删，确认你真的不要

# 4.3 销毁 remote 分支（如果 push 过）
git push origin --delete "$branch"
```

> `git worktree remove` 会拒绝删带未提交改动的 worktree。**先**确认 `git -C "$wt_dir" status` 是 clean，再删——这是故意保护你的。

### 5. 收尾自检

```bash
git -C <主仓> worktree list      # 应该不再看到那个 worktree
git -C <主仓> branch | grep "$branch"      # 应该没了
git -C <主仓> branch -r | grep "$branch"   # 应该没了
```

## 多 worktree 并行时

```bash
git -C <主仓> worktree list
```

会列出所有 worktree + 它们当前跟着的分支。当你同时挂 3-4 个的时候靠脑子记不住，靠这个命令记。

### 命名秩序

并行越多越要严格守约定。建议：

- **每个 worktree 名字里包含 purpose**：`<repo>--wt-fix-login` 而不是 `<repo>--temp1`
- **临时分支名跟 worktree 目录名对得上**：`wt/fix-login-redirect` ↔ `<repo>--wt-fix-login-redirect`，grep 的时候直接通
- **每天扫一遍 `git worktree list`**：超过 1 周没用的 worktree 要么决定合掉、要么决定弃掉——挂着不动是最坏的

### 常见冲突

| 症状 | 真因 | 处理 |
| --- | --- | --- |
| `fatal: '<branch>' is already checked out at '<other-path>'` | 一条分支只能被一个 worktree 持有，你想第二次挂它 | 去那个 `<other-path>` 看一下；要么先 `git worktree remove` 掉它，要么换条临时分支名 |
| `git worktree remove` 报 `working tree has modifications` | worktree 里有未提交改动 | `cd` 进去看 `git status` 决定 stash / commit / 丢弃；都不想要就 `--force` 删，但**先**确认没未保存工作 |
| 主仓 `git pull` 时跟 worktree 抢 packfile 锁 | 极少见，并发 fetch 时偶尔 | 等几秒重试；持续就 `kill` 掉无主的 git 进程 |
| `git worktree list` 里有"prunable"标记 | worktree 目录被你 `rm -rf` 直接删了，git 记录还在 | `git worktree prune` 清掉残余索引 |

## 与现有约定的关系

- Claude Code 本身会在 `<repo>/.claude/worktrees/<id>/` 里自动建 worktree，那是 Claude harness 自己的事，**不要**复用那个目录给手动 worktree——会被 Claude 清理掉
- 手动 worktree 一律走"主仓同级目录"约定，避免和 Claude 自己的 worktree 撞名

## 触发短语速查

| 用户说 | 你应该 |
| --- | --- |
| "开一个 worktree" / "起一个新分支并行干" / "wt 一下" | 走第 1 步（确认 base → 起 worktree） |
| "切到那个 worktree" / "在 X worktree 里干 Y" | `cd` 到对应 wt_dir，确认 `git status` clean 再干活 |
| "把这个 worktree 收尾" / "干完合回 main" | 走第 3 步选合并策略 + 第 4 步清理 + 第 5 步自检 |
| "清掉这个临时分支" / "销毁那个 worktree" | 走第 4 步 + 第 5 步 |
| "我现在挂了几个 worktree" / "列一下" | `git -C <主仓> worktree list` |

## 不在本 skill 范围内

- 该不该开一个 worktree 来做这件事（那是判断题，看主仓 / 任务大小）
- 临时分支里的代码 review / PR / CI（那是仓库自己的流程）
- 跨仓库的并行（多 clone，不是 worktree）
