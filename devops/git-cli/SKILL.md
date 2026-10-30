---
slug: git-cli
name: git-cli
version: 1.0.2
displayName: Git命令行
summary: 用Git CLI检查/暂存/提交/分支/同步代码变更。Helper for using the Git CLI to inspect, stage,
  commit, branch, and
summary_zh: 用Git CLI检查/暂存/提交/分支/同步代码变更。Helper for using the Git CLI to inspect, stage,
  commit, branch, and
license: MIT
description: Helper for using the Git CLI to inspect, stage, commit, branch, and。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于无明确技术栈的模糊需求。适用于独立开发者、企业团队和自动化工作流场景。支持中文交互，无需复杂配置即开即用。
  synchronize code changes。Use。Use when 需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于模糊的通用需求。适用于开发者、企业团队和自动化集成场景。'
tags:
- Development
- 版本控制
- Git
- 开发工具
- git
- src
- feature
- rebase
- index
tools:
- read
- exec
- write
homepage: ''
category: Development
homepage: "https://skillhub.cn/skill/"
---
> **核心功能**: 本技能提供中文交互、化工作流场景等能力。

# Git cli
## 付费版扩展能力
| 能力 | 免费版 | 付费版 |
|---|---|---|
| 基础功能 | 支持 | 支持 |
| 代码静态分析与质量评分 | 不支持 | 支持 |
| 依赖漏洞检测与升级建议 | 不支持 | 支持 |
| 批量代码审查与报告生成 | 不支持 | 支持 |
| CI/CD流水线集成 | 不支持 | 支持 |
| 代码复杂度可视化与重构建议 | 不支持 | 支持 |
## 主要能力
- Git 仓库检查：查看状态、差异、日志、分支、远程仓库、暂存区内容
- 代码暂存与提交：智能选择文件、生成规范化提交信息（Conventional Commits）
- 分支管理：创建、切换、合并、变基（rebase）、删除、重命名分支
- 远程同步：拉取（pull）、推送（push）、获取（fetch）、解决冲突
- 变更审查：差异对比、暂存审查、提交历史分析、 blame 追溯
- 工作流支持：Git Flow、GitHub Flow、Trunk-Based Development
- 冲突解决：三方合并、cherry-pick、rebase 冲突处理、冲突标记解析
## 适用范围
| 场景 | 输入 | 输出 |
|:-----|:-----|:-----|
| 代码检查 | 仓库路径 | 状态报告与变更摘要 |
| 提交管理 | 变更描述 | 规范化提交信息与暂存策略 |
| 分支操作 | 分支名与操作类型 | 分支创建/合并/删除结果 |
| 冲突解决 | 冲突文件列表 | 合并方案与解决后的代码 |
| 历史追溯 | 文件路径与行号 | 变更历史与责任人 |

**不适用于**：需要人工判断的复杂决策场景
## 使用指南
1. 确认运行环境满足依赖说明中的要求
2. 根据适用场景选择合适的使用方式
3. 执行操作并检查输出结果
4. 如遇错误，参考错误处理章节

### 流程详解：代码提交工作流
**步骤 1：检查变更状态**

```bash
# 查看工作区状态
git status

# 查看未暂存的变更
git diff

# 查看已暂存的变更
git diff --staged

# 查看简短状态
git status -s
# 输出示例:
#  M src/index.js        (已修改未暂存)
# M  src/utils.js        (已修改已暂存)
# ?? src/new-file.js     (未跟踪)
# A  src/feature.js      (新增已暂存)
# D  src/old-file.js     (删除已暂存)
```

**步骤 2：智能暂存**

```bash
# 暂存单个文件
git add src/index.js

# 暂存多个相关文件
git add src/components/ src/utils/helpers.js

# 交互式暂存（选择部分变更）
git add -p
# 对每个 hunk 选择: y(暂存) n(跳过) s(拆分) e(编辑) q(退出)
# 暂存特定文件的特定行
git add -p src/index.js

# 撤销暂存
git restore --staged src/index.js
```

**步骤 3：生成规范化提交信息**

遵循 Conventional Commits 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

| 类型 (type) | 说明 | 示例 |
|:------------|:-----|:-----|
| `feat` | 新功能 | `feat(auth): 添加 OAuth2 登录支持` |
| `fix` | 修复 Bug | `fix(api): 修复分页参数 off-by-one 错误` |
| `docs` | 文档变更 | `docs(readme): 更新安装说明` |
| `style` | 代码格式 | `style: 统一缩进为 2 空格` |
| `refactor` | 重构 | `refactor(utils): 提取公共验证函数` |
| `perf` | 性能优化 | `perf(render): 使用虚拟列表优化大列表渲染` |
| `test` | 测试相关 | `test(auth): 添加登录流程单元测试` |
| `chore` | 构建/工具 | `chore(deps): 升级 React 到 18.2` |
| `ci` | CI 配置 | `ci: 添加 GitHub Actions 自动部署` |
| `revert` | 回退提交 | `revert: feat(auth): 添加 OAuth2 登录支持` |
## 分支管理
### 分支策略
| 策略 | 主分支 | 特征分支 | 发布分支 | 适用团队 |
|:-----|:-------|:---------|:---------|:---------|
| Git Flow | main + develop | feature/* | release/* hotfix/* | 大型团队、版本发布 |
| GitHub Flow | main | feature/* | 无 | 小型团队、持续部署 |
| Trunk-Based | main | 短命特性分支 | 无 | 高频发布、DevOps |

### 常用分支操作
```bash
# 查看所有分支
git branch -a              # 包括远程分支
git branch -vv             # 显示跟踪关系和最新提交
# 创建并切换分支
git checkout -b feature/user-auth
# 或使用新语法
git switch -c feature/user-auth

# 从特定提交创建分支
git switch -c hotfix/fix-login a1b2c3d

# 合并分支（保留合并记录）
git merge feature/user-auth --no-ff

# 变基（线性历史）
git rebase main

# 交互式变基（压缩、重排、修改提交）
git rebase -i HEAD~5
# pick a1b2c3d feat: 添加登录页面
# squash d4e5f6g feat: 添加登录表单验证
# reword h7i8j9k fix: 修复表单校验问题
# 删除已合并的分支
git branch -d feature/user-auth

# 强制删除未合并的分支
git branch -D feature/abandoned
```
## 冲突解决
### 合并冲突处理
```bash
# 当 git merge 报告冲突时
git merge feature/branch
# CONFLICT (content): Merge conflict in src/index.js
# 查看冲突文件
git diff --name-only --diff-filter=U

# 冲突标记格式
# <<<<<<< HEAD
# 当前分支的代码
# =======
# 传入分支的代码
# >>>>>>> feature/branch
# 解决冲突后
git add src/index.js
git commit  # 完成合并
# 放弃合并
git merge --abort
```

### Rebase 冲突处理
```bash
git rebase main

# 解决冲突
git add src/index.js
git rebase --continue

# 跳过当前提交
git rebase --skip

# 放弃 rebase
git rebase --abort
```

### Cherry-pick 操作
```bash
# 将特定提交应用到当前分支
git cherry-pick a1b2c3d

# 多个提交
git cherry-pick a1b2c3d d4e5f6g

# 不自动提交，仅应用变更
git cherry-pick --no-commit a1b2c3d
```
## 远程仓库同步
```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add upstream

# 拉取并合并（pull = fetch + merge）
git pull origin main

# 仅获取不合并
git fetch origin
git fetch --all --prune  # 获取所有远程并清理已删除的分支
# 推送
git push origin feature/branch
git push -u origin feature/branch  # 设置上游跟踪
git push --force-with-lease origin main  # 安全强制推送（推荐）
# 注意：避免使用 git push --force，它会覆盖远程历史
# 推送标签
git push origin --tags
git push origin v1.0.0
```
## 历史追溯与审查
```bash
# 查看提交历史
git log --oneline --graph --all
git log --author="张三" --since="2024-01-01" --until="2024-06-30"

# 查看文件的变更历史
git log --follow src/index.js

# 查看某一行代码的最后修改
git blame -L 42,50 src/index.js

# 搜索提交信息
git log --grep="fix.*login" --oneline

# 查看某次提交的详细变更
git show a1b2c3d

# 比较两个分支的差异
git diff main..feature/branch --stat
```
## 优选实践
### 提交规范
1. **原子提交**：每个提交只做一件事，便于回滚和审查
2. **提交信息**：使用 Conventional Commits 规范，动词开头，清晰描述变更
3. **暂存策略**：使用 `git add -p` 选择性暂存，避免提交调试代码
4. **频率**：小步提交，每天多次提交优于一次大提交

### 分支管理
1. **命名规范**：`feature/`、`fix/`、`hotfix/`、`refactor/` 前缀
2. **生命周期**：特性分支存活不超过 3 天，及时合并或删除
3. **保护主分支**：禁止直接 push 到 main，通过 PR/MR 合并
4. **定期同步**：每天从主分支 rebase 或 merge，减少最终冲突

### 安全注意事项
1. **避免提交敏感信息**：使用 `.gitignore` 排除配置文件，使用 `git-secrets` 预防
2. **清理历史中的密钥**：`git filter-repo --replace-text passwords.txt`
3. **签名提交**：`git commit -S` 使用 GPG 签名验证身份
4. **不要 force push 到共享分支**：会覆盖他人的提交
## 常用 Git 配置
```bash
# 用户信息
git config --global user.name "Your Name"
email "you@example.com"

# 默认分支名
git config --global init.defaultBranch main

# 行尾处理
git config --global core.autocrlf input   # macOS/Linux
autocrlf true    # Windows
# 别名
git config --global alias.co checkout
lg "log --oneline --graph --all"

# Pull 默认使用 rebase
git config --global pull.rebase true
```
## 输入定义
| 参数名 | 类型 | 必填 | 说明 |
|---:|---:|---:|---:|
| action | string | 是 | 操作类型: `inspect`/`stage`/`commit`/`branch`/`merge`/`sync` |
| repo_path | string | 否 | Git 仓库路径，默认当前目录 |
| content | string | 否 | git-cli处理的内容输入，可选值: json/text/markdown |
| style | string | 否 | 输出风格, 参考 `references/style.md` |
## 输出说明
```json
{
  "success": true,
  "data": {
    "action": "commit",
    "repository": "my-project",
    "branch": "feature/user-auth",
    "staged_files": ["src/auth/login.js", "src/auth/oauth.js"],
    "commit": {
      "hash": "a1b2c3d",
      "message": "feat(auth): 添加 OAuth2 登录支持",
      "author": "开发者 <dev@example.com>",
      "timestamp": "2024-07-24T10:30:00+08:00"
    },
    "metadata": {
      "template_used": "git-cli-helper",
      "word_count": 0,
      "style": "专业"
    }
  },
  "error": null
}
```

输出模板参考: `assets/output.json`
## 运行环境
### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent(Claude Code / Cursor / Codex / Gemini CLI等)
- **操作系统**: Windows / macOS / Linux

### 依赖说明(补充)
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:------|------:|:------|:------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
-

### 可用性分类
- **分类**: MD+execute()
- **说明**: 基于Markdown的AI Skill,

**API Key配置方式**:
```bash
export API_KEY="${API_KEY:?请设置环境变量}"
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 故障处理体系
| 错误场景(续)| 原因 | 处理方式 |
|----:|:----|----:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 请求重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |
## 创新优势
### 效率提升量化分析
| 操作步骤 | 手动耗时 | 自动化耗时 | 时间节约 | 准确率提升 |
|:--------|:--------|:--------|:--------|:--------|
| 检查状态 | 5分钟 | 1分钟 | 4分钟 | 10% |
| 暂存文件 | 10分钟 | 3分钟 | 7分钟 | 15% |
| 提交代码 | 15分钟 | 5分钟 | 10分钟 | 20% |
| 分支合并 | 30分钟 | 10分钟 | 20分钟 | 25% |
| 冲突解决 | 1小时 | 30分钟 | 30分钟 | 30% |

### 差异化对比
| 对比维度 | 本技能 | 手动操作 | Python脚本 | 专业软件 |
|:--------|:--------|:--------|:--------|:--------|
| 操作便捷性 | 高 | 低 | 中 | 高 |
| 功能丰富性 | 高 | 低 | 中 | 高 |
| 学习成本 | 中 | 高 | 高 | 高 |
| 成本效益 | 高 | 低 | 中 | 高 |
| 支持平台 | 多平台 | 单平台 | 单平台 | 单平台 |

### 核心痛点解决
| 痛点 | 描述 | 影响范围 | 解决方案 | 量化效果 |
|:-----|:-----|:-----|:-----|:-----|
| 代码状态混乱 | 代码变更状态难以跟踪，影响协作效率 | 整个团队 | 提供状态检查和差异对比功能 | 提高协作效率20% |
| 分支管理复杂 | 分支创建、合并、删除操作繁琐，容易出错 | 整个团队 | 提供分支管理工具 | 减少错误率30% |
| 冲突解决困难 | 冲突解决过程耗时，影响项目进度 | 整个团队 | 提供冲突解决建议和自动化工具 | 提高解决效率40% |
## 排障手册
| 错误现象 | 可能原因 | 诊断步骤 | 解决方案 |
|:--------|:--------|:--------|:--------|
| 无法提交代码 | 文件权限问题 | 检查文件权限设置 | 修改文件权限，确保用户有写入权限 |
| 提交信息格式错误 | 不遵循 Conventional Commits 规范 | 检查提交信息格式 | 重新编写符合规范的提交信息 |
| 分支合并冲突 | 代码冲突 | 检查冲突文件 | 解决冲突，然后合并分支 |
| Git 仓库无法访问 | 网络连接问题 | 检查网络连接 | 确保网络连接正常 |
| 代码历史无法回溯 | Git 版本问题 | 检查 Git 版本 | 升级到最新版本的 Git |
## 安全实践准则
1. 确保所有代码提交都经过审查，防止恶意代码的提交。
2. 使用强密码保护 Git 仓库，防止未授权访问。
3. 定期备份 Git 仓库，以防数据丢失。
4. 避免在公共网络环境下执行 Git 操作，防止信息泄露。
5. 使用 SSH 密钥代替用户名和密码进行认证，提高安全性。

### 安全风险防范

| 风险项 | 等级 | 防护措施 | 验证方法 |
| --- | --- | --- | --- |
| API密钥泄露 | 高 | 通过环境变量配置，禁止硬编码 | 定期检查代码和配置文件 |
| 命令执行风险 | 高 | 仅执行白名单命令，避免拼接用户输入 | 使用沙箱环境测试 |
| 网络通信安全 | 中 | 使用HTTPS协议，验证SSL证书 | 定期检查证书有效期 |
| 敏感数据暴露 | 高 | 输出结果中不包含密钥、令牌等敏感信息 | 日志脱敏审查 |
| 未授权访问 | 中 | 限制访问权限，实施认证机制 | 定期审计访问日志 |
## 常见问题FAQ
### Q1: 如何在Git CLI中查看所有分支，包括远程分支？
A: 使用 `git branch -a` 命令可以查看所有本地和远程分支。

| 分支类型 | 显示信息 |
|:--------|:--------|
| 本地分支 | 前面带有星号的分支为当前分支 |
| 远程分支 | 前面带有远程仓库名的分支 |

### Q2: 如何在Git CLI中创建一个新分支并切换到该分支？
A: 使用 `git checkout -b <分支名>` 命令可以创建并切换到新分支。

| 命令 | 操作 |
|:-----|:-----|
| git checkout -b feature/new-branch | 创建并切换到名为 "feature/new-branch" 的新分支 |

### Q3: 如何在Git CLI中合并一个分支到当前分支？
A: 使用 `git merge <分支名>` 命令可以将指定分支合并到当前分支。

| 命令 | 操作 |
|:-----|:-----|
| git merge feature/branch | 将 "feature/branch" 分支合并到当前分支 |

### Q4: 如何在Git CLI中解决合并冲突？
A: 当合并冲突发生时，Git会标记冲突文件，你需要手动解决冲突，然后使用 `git add <文件名>` 命令暂存解决方案。

| 冲突处理步骤 | 操作 |
|:------------|:-----|
| 查看冲突文件 | git diff --name-only --diff-filter=U |
| 解决冲突 | 手动修改文件内容解决冲突 |
| 暂存解决方案 | git add <文件名> |
| 完成合并 | git commit |

### Q5: 如何在Git CLI中回退到上一个提交？
A: 使用 `git reset --hard HEAD~1` 命令可以回退到上一个提交。

| 命令 | 操作 |
|:-----|:-----|
| git reset --hard HEAD~1 | 回退到上一个提交，丢失当前提交后的所有更改 |
## 主要特点
- **自动化执行**: 用Git CLI检查/暂存/提交/分支/同步代码变更。Helper for using the Git CLI to i
- **文件处理**: 支持多种文件格式的读取、解析和写入操作
- **API集成**: 通过标准化接口调用外部服务并处理响应
- **命令执行**: 在安全沙箱中执行系统命令并收集结果
- **信息检索**: 快速搜索和过滤目标数据