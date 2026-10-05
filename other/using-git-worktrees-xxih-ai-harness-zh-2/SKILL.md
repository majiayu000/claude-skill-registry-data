---
name: using-git-worktrees
description: 当你开始需要隔离当前工作区的功能开发，或准备执行实现计划时使用；它会优先借助平台原生工具确保存在隔离工作区，必要时才退回到 git worktree
---

# 使用 Git Worktrees

## 概览

确保工作发生在隔离工作区里。优先使用平台原生的 worktree 工具；只有在没有原生能力时，才手工使用 git worktree。

**核心原则：**先检测是否已经隔离，再尝试原生工具，最后才退回 git。不要和 harness 对着干。

**开始时要明确说明：**“我正在使用 using-git-worktrees skill 来建立隔离工作区。”

## 第 0 步：检测现有隔离环境

**创建任何东西之前，先确认你是不是已经在隔离工作区里。**

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

**子模块防护：**在 git submodule 里，`GIT_DIR != GIT_COMMON` 也可能成立。所以在判断“已经在 worktree 中”之前，先确认当前不是 submodule：

```bash
# 如果这里返回路径，说明你在 submodule，而不是 worktree；应按普通仓库处理
git rev-parse --show-superproject-working-tree 2>/dev/null
```

**如果 `GIT_DIR != GIT_COMMON` 且不在 submodule 中：**说明你已经在一个链接 worktree 里。直接跳到第 3 步（项目初始化），**不要**再创建新的 worktree。

按分支状态汇报：
- 在命名分支上：`Already in isolated workspace at <path> on branch <name>.`
- 在 detached HEAD 上：`Already in isolated workspace at <path> (detached HEAD, externally managed). Branch creation needed at finish time.`

**如果 `GIT_DIR == GIT_COMMON`（或当前在 submodule 里）：**说明你仍在普通仓库检出中。

如果用户没有在指令里提前说明 worktree 偏好，就先征得同意再创建：

> `Would you like me to set up an isolated worktree? It protects your current branch from changes.`

如果用户已经明确表达过偏好，就直接遵循；如果用户拒绝，就原地工作并跳到第 3 步。

## 第 1 步：创建隔离工作区

**你有两种机制，必须按这个顺序尝试。**

### 1a. 平台原生 worktree 工具（优先）

如果用户已经同意创建隔离工作区（第 0 步），先判断你当前平台是否自带 worktree 创建能力。它可能叫 `EnterWorktree`、`WorktreeCreate`、`/worktree` 命令，或某个 `--worktree` 标记。只要有，就先用它，并直接跳到第 3 步。

原生工具会自动处理目录放置、分支创建和清理。如果你明明有原生工具，却手工执行 `git worktree add`，就会制造 harness 看不见也管不了的幽灵状态。

只有在完全没有原生 worktree 工具时，才进入第 1b 步。

### 1b. Git worktree 兜底

**只有在第 1a 不适用时才能用**，也就是你确实没有任何原生 worktree 工具。此时才手工用 git 创建 worktree。

#### 目录选择

按这个优先级选择目录。用户的明确偏好永远高于你从文件系统观察到的状态。

1. **先检查指令里是否已经声明了 worktree 目录偏好。**如果有，直接用，不要再问。

2. **检查是否已有项目内 worktree 目录：**
   ```bash
   ls -d .worktrees 2>/dev/null     # 优先，隐藏目录
   ls -d worktrees 2>/dev/null      # 备选
   ```
   如果存在就使用它；如果两个都存在，优先 `.worktrees`。

3. **检查是否已有全局目录：**
   ```bash
   project=$(basename "$(git rev-parse --show-toplevel)")
   ls -d ~/.config/superpowers/worktrees/$project 2>/dev/null
   ```
   如果存在就使用它，用于兼容旧的全局路径。

4. **如果没有任何其他线索，**默认使用项目根目录下的 `.worktrees/`。

#### 安全校验（仅项目内目录）

**在创建 worktree 前，必须确认目录已被 ignore：**

```bash
git check-ignore -q .worktrees 2>/dev/null || git check-ignore -q worktrees 2>/dev/null
```

**如果没有被 ignore：**先把规则加进 `.gitignore`，提交这次改动，再继续。

**为什么重要：**避免把 worktree 内容误提交进仓库。

全局目录（`~/.config/superpowers/worktrees/`）不需要这一步，因为它在仓库外。

#### 创建 worktree

```bash
project=$(basename "$(git rev-parse --show-toplevel)")

# 根据选中的位置确定 path
# 项目内目录：path="$LOCATION/$BRANCH_NAME"
# 全局目录：path="~/.config/superpowers/worktrees/$project/$BRANCH_NAME"

git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

**沙箱兜底：**如果 `git worktree add` 因权限错误失败（沙箱拒绝），就明确告诉用户：沙箱阻止了 worktree 创建，因此你会在当前目录继续工作。随后直接原地执行初始化和基线测试。

## 第 3 步：项目初始化

自动检测项目类型并执行对应初始化：

```bash
# Node.js
if [ -f package.json ]; then npm install; fi

# Rust
if [ -f Cargo.toml ]; then cargo build; fi

# Python
if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
if [ -f pyproject.toml ]; then poetry install; fi

# Go
if [ -f go.mod ]; then go mod download; fi
```

## 第 4 步：验证干净基线

运行测试，确认工作区起始状态是干净的：

```bash
# Use project-appropriate command
npm test / cargo test / pytest / go test ./...
```

**如果测试失败：**报告失败，并询问是继续还是先调查。  
**如果测试通过：**报告工作区已可用。

### 汇报

```
Worktree ready at <full-path>
Tests passing (<N> tests, 0 failures)
Ready to implement <feature-name>
```

## 快速参考

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation (Step 0) |
| In a submodule | Treat as normal repo (Step 0 guard) |
| Native worktree tool available | Use it (Step 1a) |
| No native tool | Git worktree fallback (Step 1b) |
| `.worktrees/` exists | Use it (verify ignored) |
| `worktrees/` exists | Use it (verify ignored) |
| Both exist | Use `.worktrees/` |
| Neither exists | Check instruction file, then default `.worktrees/` |
| Global path exists | Use it (backward compat) |
| Directory not ignored | Add to .gitignore + commit |
| Permission error on create | Sandbox fallback, work in place |
| Tests fail during baseline | Report failures + ask |
| No package.json/Cargo.toml | Skip dependency install |

## 常见错误

### 和 harness 对着干

- **问题：**平台明明已经提供隔离机制，你却仍手工跑 `git worktree add`
- **修复：**第 0 步先检测现有隔离，第 1a 步优先使用原生工具

### 跳过环境检测

- **问题：**在已有 worktree 里再套一层 worktree
- **修复：**任何创建动作前都先跑第 0 步

### 跳过 ignore 校验
- **问题：**worktree 内容被 git 追踪，污染状态
- **修复：**项目内目录一律先 `git check-ignore`

### 擅自决定目录位置
- **问题：**破坏项目约定，造成混乱
- **修复：**严格遵循优先级：现有目录 > 旧全局目录 > 指令偏好 > 默认目录

### 基线测试失败还继续推进
- **问题：**无法区分新 bug 和旧问题
- **修复：**先报告失败，明确征得同意后再继续

## 红旗

**绝不要：**
- 第 0 步已经确认当前已隔离，却还继续创建 worktree
- 在拥有原生 worktree 工具时还手工使用 `git worktree add`；这是头号错误，有原生工具就必须用
- 跳过第 1a 步，直接进入第 1b 的 git 命令
- 在没确认 ignore 之前创建项目内 worktree
- 跳过基线测试验证
- 在测试失败时不问就继续

**始终要做：**
- 先执行第 0 步环境检测
- 优先用原生工具，再考虑 git 兜底
- 遵循目录优先级：现有目录 > 旧全局目录 > 指令偏好 > 默认目录
- 对项目内目录做 ignore 校验
- 自动检测并运行项目初始化
- 验证干净测试基线
