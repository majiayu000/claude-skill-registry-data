---
name: code-review
description: 对分支、PR 或未提交改动做审查，分别核对项目规范与原任务要求，并给出证据。
---

先按当前宿主读取 [Pi 说明](../../README.pi.md)或 [Delta 说明](../../README.delta.md)，再读取仓库内的[源工作流](../../skill-sources/code-review/SKILL.md)及其 smell baseline。

- 先固定范围：分支审查记录 merge base/HEAD；未提交工作包含暂存、未暂存和相关新文件，不用分支 diff 代替。保留他人的改动。
- 从 `docs/agents/issue-tracker.md` 确认任务来源；需要远程证据时用 `gh-app` 读取原 Issue、评论与标签。规范来自适用 AGENTS 和现行合同，标签不等于授权。
- Standards 与 Spec 独立核对并分开报告；独立审查按当前宿主说明执行。能力不足时以单 Agent 分两遍核对并披露，不冒称独立并行审查；明确要求独立审查的任务仍需补足。
- finding 包含严重性、路径位置、真实触发条件及规范/任务依据。未验证事项与确认缺陷分开，不把可选探测失败升级成无关 BLOCK。
- 结果返回当前任务；公开发布需授权，不继续追加已归档的根任务账本。审查角色不修改审查对象。
