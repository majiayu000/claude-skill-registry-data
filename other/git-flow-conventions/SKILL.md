---
name: git-flow-conventions
description: >
  Git Flow 分支管理与提交规范指南。当用户进行分支操作、合并代码、提交 PR/MR、
  规划发版、修复线上 Bug、或询问 Git 协作规范时使用。覆盖完整 Git Flow 模型
  (develop/feature/release/hotfix)、分支命名规范、commit message 格式、
  PR 提交流程和最佳实践。触发场景包括：创建分支、合并代码、git commit、发版、
  hotfix、分支命名、PR 描述、代码审查提交。
---

# Git Flow 分支管理与提交规范

基于 Vincent Driessen 的 A Successful Git Branching Model，指导团队按 GitFlow 进行分支操作、提交和合并。

完整分支模型、命名规范、红线、对比矩阵见 [`references/gitflow.md`](references/gitflow.md)。

## 操作命令速查

### Develop 分支初始化

```bash
git branch develop
git push -u origin develop
```

### Feature 分支

**开始开发**：
```bash
git checkout -b feature/<功能名> develop
git push -u origin feature/<功能名>
```

**提交代码**：
```bash
git add .
git commit -m "feat(<模块>): <简述>"
```

**合并回 develop**（使用 `--no-ff` 保留分支 commit 历史）：
```bash
git checkout develop
git pull origin develop
git merge --no-ff feature/<功能名>
git push origin develop
```

**清理**：
```bash
git branch -d feature/<功能名>
git push origin --delete feature/<功能名>
```

### Release 分支

**开始发版**：
```bash
git checkout -b release/<版本号> develop
```

**完成发版**：
```bash
# 合并到 master
git checkout master
git merge --no-ff release/<版本号>
git push origin master

# 合并回 develop
git checkout develop
git merge --no-ff release/<版本号>
git push origin develop

# 打 tag + 清理
git tag -a v<版本号> -m "Release v<版本号>"
git push --tags
git branch -d release/<版本号>
git push origin --delete release/<版本号>
```

### Hotfix 分支

**开始修复**：
```bash
git checkout -b hotfix/<版本号> master
```

**完成修复**：
```bash
# 合并到 master
git checkout master
git merge --no-ff hotfix/<版本号>
git push origin master

# 合并回 develop
git checkout develop
git merge --no-ff hotfix/<版本号>
git push origin develop

# 打 tag + 清理
git tag -a v<版本号> -m "Hotfix v<版本号>"
git push --tags
git branch -d hotfix/<版本号>
git push origin --delete hotfix/<版本号>
```

### 合并策略

| 策略 | 说明 | 适用场景 |
|------|------|---------|
| `--no-ff` | 不使用 fast-forward，保留分支 commit 历史 | **默认推荐**，保留完整开发记录 |
| `--squash` | 把多次分支 commit 压缩为一次 | 功能分支 commit 杂乱时 |

## Commit Message 规范

采用 **Conventional Commits** 格式：

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add JWT token refresh` |
| `fix` | Bug 修复 | `fix(api): handle null user profile` |
| `docs` | 文档变更 | `docs(readme): update install guide` |
| `style` | 格式调整（不影响逻辑） | `style(layout): reorder imports` |
| `refactor` | 重构 | `refactor(db): extract query builder` |
| `perf` | 性能优化 | `perf(list): add virtual scrolling` |
| `test` | 测试相关 | `test(auth): add 2FA unit tests` |
| `chore` | 构建/工具变更 | `chore(deps): bump axios to 1.6` |
| `ci` | CI 配置 | `ci: add GitHub Actions workflow` |
| `revert` | 回滚 | `revert: undo feat(user-search)` |

### 规则

- Subject 用现在时、首字母小写、不加句号
- 中文项目 scope 可用中文，如 `feat(登录): 增加验证码校验`
- Body 解释 **为什么** 这个变更是必要的
- Footer 引用关联 issue：`Closes #123`

## PR / MR 规范

### 分支准备

提交 PR 前必须：
1. 从目标分支 rebase 或 merge 最新代码
2. 确保 CI 通过
3. 自己 Review 一遍 diff

```bash
# Rebase 到最新 develop
git fetch origin
git rebase origin/develop
# 解决冲突后
git push --force-with-lease origin feature/<功能名>
```

### PR 描述模板

```markdown
## 变更说明
<一句话描述做了什么>

## 变更类型
- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 重构 (refactor)
- [ ] 其他

## 测试
- [ ] 单元测试通过
- [ ] 手动验证通过

## 关联 Issue
Closes #<编号>
```

### 合并策略选择

| 策略 | 适用场景 |
|------|---------|
| `--no-ff` (non-fast-forward) | **默认推荐**。保留分支历史，可追溯功能开发过程 |
| `--squash` | 功能分支 commit 杂乱时，压缩成一个干净 commit |
| `--ff-only` | 简单修复，分支历史已是线性时 |

## Release Note 格式

每次发版必须使用规范的 Release Note 格式，通过 `gh release create` 或 `gh release edit` 发布。

**格式参考**：见 [`references/release-note-format.md`](references/release-note-format.md)

**快速要点**：
- 固定分类：新功能 / 问题修复 / 文档 / 测试 / 杂项
- 无变更时写"无"，不可省略
- 摘要 2-4 句概括核心变更
- 升级指南给出具体命令
- 尾部带 `compare` 链接

**创建命令**：
```bash
gh release create v<版本号> --title "v<版本号>: <简述>" --notes "<完整 note>" --target main
```

## 扩展：其他主流工作流

完整 Git Flow 偏重，主干又必须稳定时，还有两种常见替代：**GitHub Flow**（轻量 + PR 强协作）和 **Trunk-Based Development**（主干高频集成）。

各工作流完整内容：

- GitFlow（含横向对比矩阵 + 选型决策表）：[`references/gitflow.md`](references/gitflow.md)
- GitHub Flow：[`references/github-flow.md`](references/github-flow.md)
- Trunk-Based Development：[`references/trunk-based.md`](references/trunk-based.md)

**何时读这些 reference**：

- 用户明确问"我们应不应该换工作流"——先读 `references/gitflow.md` 顶部拿对比矩阵和决策表
- 用户已经在用 GitHub Flow / Trunk-Based——直接读对应文件
- 用户在 GitFlow 上下文里讨论某条特定规则——留在主文件即可，不要跳转
