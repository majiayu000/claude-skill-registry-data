---
name: request-refactor-plan
description: 访谈重构目标，核对代码中的问题，并规划小步可验证的改动。
---

先按当前宿主读取 [Pi 说明](../../README.pi.md)或 [Delta 说明](../../README.delta.md)，再读取仓库内的[源工作流](../../skill-sources/request-refactor-plan/SKILL.md)。

保留访谈、范围确认、现有实现核对、测试决策和小步提交计划；按任务复杂度使用必要篇幅，不机械输出长文。现行合同与领域术语的读取遵循 `docs/agents/domain.md`。

任务记录使用 `docs/agents/issue-tracker.md` 和 `triage-labels.md`。保留源模板中有实际信息的目标、边界、验证与风险，使用中文。只有获得发布授权才经 `gh-app` 写入 GitHub，否则返回草案；规划不自动授权产品修改或 Git 写操作。
