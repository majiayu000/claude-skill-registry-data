---
name: gitflow
description: GitFlow - 自动监控 GitHub 和 GitLab 上代码推送的 CI/CD 管道状态，统一查看和管理。自动化DevOps工作流 🦞！
---

# GitFlow — OpenClaw 技能

## 概述
**GitFlow** 是一个 OpenClaw 技能，可自动化代码推送并为 GitHub 和 GitLab 仓库提供实时 CI/CD 管道状态监控。它通过减少仓库和管道仪表板之间的上下文切换来简化开发者工作流。

该技能可以自动推送更改并报告管道结果，实现更快的反馈和更平滑的部署。

## 功能
GitFlow 可以：

- 自动推送本地提交
- 触发远程 CI/CD 管道
- 获取管道状态和结果
- 报告构建成功或失败
- 显示管道 URL 和日志
- 监控多个仓库


## 典型工作流
1. 开发者在本地提交更改。
2. GitFlow 自动或在命令触发下推送更改。
3. 远程 CI/CD 管道运行。
4. 技能报告管道状态。
5. 开发者即时接收构建/部署反馈。


## GitHub CLI 命令

使用 `gh` CLI 工具在推送后获取工作流状态：

### 检查工作流运行状态
```bash
gh run list
```
列出仓库最近的工作流运行。

### 查看当前分支的最新运行
```bash
gh run list --branch $(git branch --show-current) --limit 1
```
显示当前分支的最近工作流运行。

### 查看运行详情
```bash
gh run view <run-id>
```
显示特定工作流运行的详细信息。

### 实时监控运行
```bash
gh run watch
```
监控最近的运行直到完成，流式传输状态更新。

### 查看运行日志
```bash
gh run view <run-id> --log
```
显示工作流运行的完整日志。

### 查看失败任务日志
```bash
gh run view <run-id> --log-failed
```
仅显示失败任务的日志。

### 重新运行失败的任务
```bash
gh run rerun <run-id> --failed
```
仅重新运行工作流运行中失败的任务。

---

## GitLab CLI 命令

使用 `glab` CLI 工具在推送后获取管道状态：

### 检查管道状态
```bash
glab ci status
```
显示当前分支上最近管道的状态。

### 查看管道详情
```bash
glab ci view
```
打开当前管道的交互视图，包含任务详情。

### 列出最近的管道
```bash
glab ci list
```
列出仓库最近的管道。

### 查看特定管道
```bash
glab ci view <pipeline-id>
```
按 ID 查看特定管道的详情。

### 实时监控管道
```bash
glab ci status --live
```
持续监控管道状态直到完成。

### 获取管道任务日志
```bash
glab ci trace <job-id>
```
流式传输特定任务的日志。

---

## 推送后钩子示例

Git 没有原生的推送后钩子，但你可以创建一个 git 别名来在推送后自动监控管道状态。

将此添加到你的 `~/.gitconfig`：

```ini
[alias]
    pushflow = "!f() { \
        git push \"${1:-origin}\" \"${2:-$(git branch --show-current)}\"; \
        url=$(git remote get-url \"${1:-origin}\"); \
        if echo \"$url\" | grep -q 'github.com'; then \
            sleep 3 && gh run watch; \
        elif echo \"$url\" | grep -q 'gitlab'; then \
            sleep 3 && glab ci status --live; \
        fi; \
    }; f"
```

### 使用

```bash
git pushflow
git pushflow origin main
```

---
