---
name: github
description: "使用 `gh` CLI 与 GitHub 交互。使用 `gh issue`、`gh pr`、`gh run` 和 `gh api` 处理问题、PR、CI 运行和高级查询。"
---

# GitHub 技能

使用 `gh` CLI 与 GitHub 交互。当不在 git 目录中时，始终指定 `--repo owner/repo`，或直接使用 URL。

## Pull Requests（拉取请求）

检查 PR 的 CI 状态：
```bash
gh pr checks 55 --repo owner/repo
```

列出最近的 workflow 运行：
```bash
gh run list --repo owner/repo --limit 10
```

查看运行记录并查看哪些步骤失败：
```bash
gh run view <run-id> --repo owner/repo
```

仅查看失败步骤的日志：
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## 高级查询 API

`gh api` 命令对于访问其他子命令无法获取的数据非常有用。

获取 PR 的特定字段：
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON 输出

大多数命令支持 `--json` 以获得结构化输出。你可以使用 `--jq` 进行过滤：

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

## 常用命令示例

### Issues（问题）

列出仓库的 issues：
```bash
gh issue list --repo owner/repo
```

创建新 issue：
```bash
gh issue create --repo owner/repo --title "标题" --body "描述"
```

查看 issue 详情：
```bash
gh issue view 123 --repo owner/repo
```

### Pull Requests（拉取请求）

创建 PR：
```bash
gh pr create --repo owner/repo --title "PR 标题" --body "PR 描述"
```

查看 PR 详情：
```bash
gh pr view 55 --repo owner/repo
```

合并 PR：
```bash
gh pr merge 55 --repo owner/repo
```

### Workflows（工作流）

查看特定的 workflow 运行：
```bash
gh run view <run-id> --repo owner/repo
```

重新运行失败的 workflow：
```bash
gh run rerun <run-id> --repo owner/repo
```

### Repositories（仓库）

克隆仓库：
```bash
gh repo clone owner/repo
```

创建新仓库：
```bash
gh repo create repo-name --public
```

查看仓库信息：
```bash
gh repo view owner/repo
```

## 使用场景

- **CI/CD 监控**：检查持续集成状态，查看构建失败原因
- **Issue 管理**：创建、查看和管理 GitHub issues
- **PR 工作流**：处理拉取请求的完整生命周期
- **自动化脚本**：在脚本中使用 GitHub API 进行自动化操作
- **项目协作**：管理团队项目和代码审查流程

## 安装

确保已安装 GitHub CLI (`gh`)：
```bash
# macOS
brew install gh

# Linux
# 参考: https://github.com/cli/cli/blob/trunk/docs/install_linux.md

# Windows
winget install GitHub.cli
```

首次使用需要进行身份认证：
```bash
gh auth login
```

## 提示

- 使用 `--help` 标志查看任何命令的详细帮助
- 使用 `--json` 和 `--jq` 进行灵活的数据提取和处理
- 在脚本中使用 `--quiet` 或 `--silent` 减少输出
- 使用 `gh api` 访问 GitHub REST API 的任何端点
