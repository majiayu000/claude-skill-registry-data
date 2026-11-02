---
name: help-me-study
description: 协调大学课程作业、Notion 笔记与 PPT 演讲稿的组合任务，按需路由要求核验、报告、笔记和演讲。
---

# Help Me Study

先读[共享决策与边界](../help-me-shared/references/core.md)。识别本次课程/学期、任务范围、已有进度和用户授权，复用已确认决定。

| 当前需求 | 加载入口 |
|---|---|
| 只分析要求、核验老师口头说明/评分 | [help-me-assignment](../help-me-assignment/SKILL.md) |
| 完成题目、代码、实验、报告、整理 submit | [help-me-homework](../help-me-homework/SKILL.md) |
| 设计笔记/生成或修改正文 | [help-me-notes](../help-me-notes/SKILL.md) |
| 定位已有笔记、同步现成内容、维护页面 | [help-me-notion-sync](../help-me-notion-sync/SKILL.md) |
| 根据 PPT 写演讲稿或修改口头表达 | [help-me-speech](../help-me-speech/SKILL.md) |

组合任务按依赖顺序串联，不一次读取全部 references。单题/局部改动仅处理对应范围。

作业先明确要求并展示摘要，明确后可继续；笔记先呈交结构大纲，确认后生成完整正文或改正式页；新演讲稿先确认风格、时长、听众与目标，只问缺项。不要混淆或省略这些步骤。

涉及正式课程/实验/项目报告时，默认必须交付完整 LaTeX 源码和实际编译的 PDF，不能以 Markdown 报告结束。用户不必每次重申；编译受阻时保留 `.tex` 并说明缺口，不自行换格式。只要大纲/审阅、无需报告或用户明确指定其他交付物时遵守实际范围；老师格式要求冲突按[报告路线](../help-me-shared/references/report.md)处理。

创建本地工作目录或记录跨会话状态时才读[运行工具](../help-me-shared/references/runtime.md)。作业整理进 submit 默认未打包，即使老师要求 ZIP 也等用户明确压缩指令。

交付说清产物位置、覆盖、实际验证、缺口，以及是否已写 Notion/打包/提交。自动发现保持开启；技能被选中不构成额外外部操作授权。
