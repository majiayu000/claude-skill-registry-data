---
name: git-sync-checker-enhanced
description: Git 仓库同步状态检查工具。检查本地与远程仓库的同步状态、预测潜在冲突、检测敏感文件和大文件。当用户提到"检查同步状态"、"检查冲突"、"批量检查仓库"、"检查 gitignore"或类似的 Git 状态分析需求时使用此技能。
allowed-tools: Bash, Read, Grep
---

# Instructions

## 核心职责

提供 Git 仓库状态检查和冲突预测功能。

**核心功能**：
- ✅ 检查本地与远程的同步状态
- ✅ 预测合并或拉取时的潜在冲突
- ✅ 批量检查多个仓库
- ✅ 检测敏感文件和大文件
- ❌ 不自动执行任何 Git 操作（只检查不修改）

## 可用脚本

项目包含三个 Shell 脚本：

1. **conflict-predictor.sh** - 冲突预测
   - 检测本地和远程是否修改了相同的文件
   - 根据共同修改文件数量判断风险级别
   - 提供合并建议

2. **batch-checker.sh** - 批量检查
   - 扫描目录下的所有 Git 仓库
   - 显示每个仓库的同步状态
   - 支持 JSON 输出

3. **gitignore-checker.sh** - 配置检查
   - 检测已提交的敏感文件（.env、密钥等）
   - 检测大文件（>5MB）
   - 检查常见问题文件（node_modules等）

## 使用场景

### 场景 1: 合并前检查冲突

**用户可能说**：
- "我要合并最新代码，会有冲突吗？"
- "检查一下合并风险"
- "pull 代码会有问题吗？"

**执行步骤**：

1. 确认当前在 Git 仓库中
2. 运行冲突预测脚本：

```bash
bash conflict-predictor.sh
```

3. 解释输出结果：
   - **低风险**：本地和远程没有修改相同文件，可以安全合并
   - **中等风险**：有1-3个文件被双方修改，可能需要手动解决冲突
   - **高风险**：有多个文件被双方修改，很可能遇到冲突

4. 如果有冲突文件，列出具体的文件名

5. 提供建议的操作步骤（脚本会自动输出）

**注意事项**：
- 这是基于文件级别的检测，即使修改了同一文件也可能不冲突（如果修改的代码行不重叠）
- 这是一个有用的参考，但不是100%准确的预测

### 场景 2: 检查当前仓库状态

**用户可能说**：
- "检查同步状态"
- "查看 Git 状态"
- "准备下班，检查一下代码"

**执行步骤**：

1. 使用 Bash 工具运行标准 Git 命令：

```bash
# 检查工作区状态
git status

# 获取远程更新（不拉取）
git fetch --all

# 检查本地领先/落后的提交数
git rev-list --left-right --count HEAD...@{u}
```

2. 解释输出：
   - 工作区是否干净
   - 有多少未推送的提交
   - 有多少未拉取的提交

3. 如果用户关心冲突，运行 conflict-predictor.sh

### 场景 3: 批量检查多个仓库

**用户可能说**：
- "检查 ~/projects 下所有仓库"
- "批量检查项目状态"
- "看看所有项目的同步情况"

**执行步骤**：

1. 确认目录路径
2. 运行批量检查脚本：

```bash
bash batch-checker.sh ~/projects
```

3. 解释输出：
   - 总共找到多少个仓库
   - 每个仓库的状态（✅已同步、⚠️需要同步、🔴需要处理）
   - 图标含义：
     - ↑N = N个未推送的提交
     - ↓N = N个未拉取的提交
     - +N = N个未提交的文件

4. 如果有问题，建议用户优先处理标记为🔴的仓库

**可选参数**：
```bash
# 指定搜索深度（默认3）
bash batch-checker.sh ~/projects 2

# JSON 输出（供脚本使用）
bash batch-checker.sh ~/projects 3 json
```

### 场景 4: 检查 .gitignore 配置

**用户可能说**：
- "检查 gitignore"
- "有没有不该提交的文件"
- "检查敏感文件"

**执行步骤**：

1. 运行 gitignore 检查脚本：

```bash
bash gitignore-checker.sh
```

2. 解释输出：
   - 敏感文件：.env、密钥文件等
   - 大文件：超过5MB的文件
   - 常见问题：node_modules、__pycache__等

3. 如果发现问题，提供清理步骤：
   - 从 Git 移除但保留本地文件：`git rm --cached <文件>`
   - 添加到 .gitignore
   - 提交修改

4. 提醒用户：文件仍在 Git 历史中，如需彻底清除需要使用 git filter-branch 或 BFG Repo-Cleaner

## 执行原则

### 安全限制

- ❌ 永不执行任何修改 Git 仓库的命令
- ❌ 永不自动推送或拉取代码
- ❌ 永不删除分支或重置提交
- ✅ 只执行只读的检查命令
- ✅ 所有建议的操作都需要用户手动执行

### 输出原则

1. **简洁明了**：直接告诉用户状态和风险
2. **提供上下文**：解释为什么有风险
3. **具体建议**：提供可执行的命令
4. **诚实透明**：说明检测的局限性

### 错误处理

如果脚本执行失败：

1. 检查是否在 Git 仓库中：`git rev-parse --git-dir`
2. 检查脚本是否有执行权限：`chmod +x *.sh`
3. 检查 Git 是否已安装：`git --version`
4. 向用户报告具体的错误信息

## 输出示例

### 冲突检测输出

```
🔍 Git 冲突检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
分支: feature/new-ui
远程: origin

📊 状态概览
本地修改文件: 5 个
远程修改文件: 3 个
共同修改文件: 2 个

⚠️  中等风险
本地和远程修改了相同的文件，可能需要手动解决冲突。

⚠️  可能冲突的文件：
  • src/components/Header.tsx
  • package.json

建议操作：
# 1. 备份当前分支
git branch backup-20251125-1430

# 2. 拉取并合并
git pull origin feature/new-ui

# 3. 如遇冲突，手动解决后：
git add <已解决的文件>
git commit
```

### 批量检查输出

```
🔍 Git 仓库批量检查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
搜索目录: /Users/you/projects
最大深度: 3

找到 5 个仓库

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅  project-a                  (main)
⚠️  project-b                  (dev)                 ↑2
🔴  project-c                  (feature/auth)        +3
✅  project-d                  (main)
⚠️  project-e                  (main)                ↓1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 检查完成

总计: 5 个仓库
✅ 已同步: 2
⚠️  需要同步: 2
🔴 需要立即处理: 1
```

## 常见问题

### Q: 脚本找不到或无法执行？

检查脚本路径和权限：

```bash
# 查找脚本位置
find ~/.claude/skills -name "*.sh"

# 添加执行权限
chmod +x ~/.claude/skills/git-sync-checker-enhanced/*.sh

# 测试执行
bash ~/.claude/skills/git-sync-checker-enhanced/conflict-predictor.sh
```

### Q: 脚本显示"未找到远程仓库"？

检查远程配置：

```bash
git remote -v
```

如果没有远程仓库，脚本会提示用户添加。

### Q: 批量检查很慢？

对于大量仓库，可以：
1. 减少搜索深度
2. 缩小搜索范围
3. 每个仓库有30秒超时保护

## 技术说明

### 冲突预测算法

1. 找共同祖先：`git merge-base HEAD REMOTE/BRANCH`
2. 列出本地修改：`git diff --name-only BASE HEAD`
3. 列出远程修改：`git diff --name-only BASE REMOTE`
4. 找交集：`comm -12 <(local_files) <(remote_files)`
5. 判断风险：0个=低，1-3个=中，>3个=高

**局限性**：
- 只检测文件级别，不检测行级别
- 不考虑文件类型和重要性
- 不考虑开发者经验

### 批量检查流程

1. 使用 `find` 搜索 `.git` 目录
2. 对每个仓库执行：
   - `git status --porcelain` 检查工作区
   - `git fetch` 获取远程更新
   - `git rev-list --count` 计算提交差异
3. 汇总结果并输出

### 敏感文件检测

使用正则表达式匹配常见模式：
- 环境变量：`\.env$`、`\.env\.local$`
- 密钥文件：`.*\.key$`、`.*\.pem$`
- SSH密钥：`id_rsa`、`id_dsa`
- 配置文件：`database\.yml`、`secrets\.yml`

## 参考文档

- 完整使用说明：[README.md](README.md)
- 改进提案：[IMPROVEMENT_PROPOSAL.md](IMPROVEMENT_PROPOSAL.md)
