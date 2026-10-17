---
name: github
description: '使用 `gh` CLI 与 GitHub 交互。**Auto-trigger**: 当涉及 GitHub 操作、issues、PRs、CI运行时自动使用。'
---

# GitHub 技能

使用 `gh` CLI 与 GitHub 交互。不在 git 目录中时务必指定 `--repo owner/repo`，或直接用 URL。

## Pull Request

检查 PR 上的 CI 状态：
```bash
gh pr checks 55 --repo owner/repo
```

列出最近的工作流运行：
```bash
gh run list --repo owner/repo --limit 10
```

查看某次运行并检查哪些步骤失败了：
```bash
gh run view <run-id> --repo owner/repo
```

仅查看失败步骤的日志：
```bash
gh run view <run-id> --repo owner/repo --log-failed
```

## API 用于高级查询

`gh api` 命令可用于访问其他子命令无法获取的数据。

获取包含指定字段的 PR：
```bash
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'
```

## JSON 输出

大多数命令都支持 `--json` 获取结构化输出。可使用 `--jq` 进行过滤：

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```
