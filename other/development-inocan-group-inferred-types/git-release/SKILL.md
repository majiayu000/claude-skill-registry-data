---
name: git-release
description: |
  Git 项目版本发布自动化工具。支持语义化版本号升级 (major/minor/patch)，
  基于 Angular commit 规范自动生成 CHANGELOG，创建 git tag 并推送到远程仓库。
  触发关键词：
  - "发布版本"、"升级版本"、"更新版本"、"版本发布"、"发新版"
  - "更新版本并提交"、"升级并提交"、"发布并推送"
  - "bump version"、"release"、"new release"
  - "打tag"、"创建发布"、"创建tag"
  - "大版本更新"、"小版本更新"、"补丁版本"
  - "major release"、"minor release"、"patch release"
---

# Git Release Skill

自动化 Git 项目版本发布流程。

## 重要：必须询问版本类型

在执行发布前，**必须使用 AskUserQuestion 工具询问用户版本升级类型**：

```
问题：本次发布是什么类型的版本升级？

选项：
- patch (补丁版本) - Bug 修复、小改动 (例: 1.0.0 → 1.0.1)
- minor (小版本) - 新功能、向后兼容 (例: 1.0.0 → 1.1.0)
- major (大版本) - 破坏性变更、重大更新 (例: 1.0.0 → 2.0.0)
```

除非用户在请求中已明确指定版本类型（如"大版本更新"、"patch release"），否则必须询问。

## 发布流程

### 1. 检查前置条件

```bash
# 确认工作区状态
git status --porcelain

# 确认当前分支
git branch --show-current

# 获取当前版本号
grep '"version"' package.json

# 获取最新 tag
git describe --tags --abbrev=0 2>/dev/null || echo "无现有 tag"
```

### 2. 询问版本类型

**必须询问用户**，提供以下选项：

| 类型 | 描述 | 版本变化示例 |
|------|------|-------------|
| patch | 补丁版本：Bug 修复、文档更新、小改动 | 1.2.3 → 1.2.4 |
| minor | 小版本：新功能、向后兼容的改进 | 1.2.3 → 1.3.0 |
| major | 大版本：破坏性变更、API 重构 | 1.2.3 → 2.0.0 |

如果用户说"小更新"/"小版本" → minor
如果用户说"大更新"/"大版本" → major
如果用户说"修复"/"补丁" → patch

### 3. 处理未提交更改

如果工作区有未提交更改，询问用户：
- 先提交再发布（推荐）
- 先 stash 再发布
- 取消发布

### 4. 更新版本号

```bash
# 使用脚本升级版本
bash scripts/bump-version.sh <patch|minor|major>
```

或手动更新 `package.json` 中的 `version` 字段。

### 5. 生成 CHANGELOG

按 Angular 规范分组 commits（见 `references/angular-commit.md`）：

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Breaking Changes
- 破坏性变更描述

### Features
- feat(scope): description

### Bug Fixes
- fix(scope): description
```

### 6. 提交发布

```bash
git add package.json CHANGELOG.md
git commit -m "chore(release): vX.Y.Z"
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

### 7. 推送到远程

询问用户是否推送，确认后执行：

```bash
git push origin <branch>
git push origin vX.Y.Z
```

## 版本类型关键词映射

用户可能使用的表达方式：

| 用户说 | 版本类型 |
|-------|---------|
| 大版本、大更新、重大更新、breaking | major |
| 小版本、小更新、新功能、feature | minor |
| 补丁、修复、bugfix、hotfix、小改动 | patch |

## 注意事项

- 发布前确保测试通过
- 工作区有未提交更改时先处理
- 破坏性变更必须升级 major 版本
- Tag 命名统一使用 `vX.Y.Z` 格式
- 首次发布建议从 `0.1.0` 或 `1.0.0` 开始

## 参考文档

- **Angular Commit 规范**: 见 `references/angular-commit.md`
- **语义化版本指南**: 见 `references/semver-guide.md`
- **CHANGELOG 模板**: 见 `assets/CHANGELOG.template.md`
