---
name: ai-web-feedback
description: 将用户反馈、bug 报告、功能建议提交为 GitHub/Gitee Issue（非 PR）。
---

# 反馈 → Issue

当用户要**记录问题或建议**、且**尚未准备好代码改动**时，使用 Issue 工具而非 PR。

## 何时用 Issue

- 「帮我提个 bug」「记录一下这个问题」
- 功能建议、体验反馈
- 无法立即修复、需要先跟踪

## 何时用 PR

- 已修改代码并要合入 → `publish_changes` / `report_bug_and_publish_pr`

## 流程

1. `discover_issue_templates(unit_id=assistant)` 查看模板
2. `report_issue(kind=bug|feature|suggestion, …, confirm=false)` 预览
3. 用户确认后 `confirm=true`
4. 返回 `issue_url` 给用户

## 默认目标

- op助手相关问题 → `assistant` 单元 → `mouxangithub/ai`
- openpilot 项目问题 → `openpilot` 单元 → 当前 remote 或 fork

详见 `ai/docs/ISSUES.md`。
