---
name: modus-development
description: 开发、评审、排障或解释 Modus 框架自身，包括代码、Skill 工作流和维护文档，以及基于源码的技术写作。普通业务项目使用 Modus 时读取该项目的 using-modus。
---

# Modus 开发与写作

这是一套服务于 **Modus 框架自身** 的复合技能。一个入口连接全局认知、模块开发、测试发布和文章写作；模块指南按任务加载，不把整个参考目录一次性塞进上下文。

在源码仓库中，先遵循 [仓库指引](../../AGENTS.md) 与 [贡献指南](../../CONTRIBUTING.md)。本技能负责定位和执行方法，不另存一套代码风格或质量规范。

## 先确定当前项目

源码位置以用户指定的 checkout 为准；未指定时使用当前 Git 仓库根目录。本技能目录由加载的 `SKILL.md` 所在位置确定。首次进入一个 checkout，将 `SKILL_DIR` 设为本技能目录，在 Modus 仓库根目录运行只读诊断：

```bash
python3.11 "$SKILL_DIR/scripts/inspect_repository.py" --root .
```

它检查分支、HEAD、上游、本地修改、包版本与知识基线漂移，不联网、不写仓库、不调用已安装的 Modus。使用任一 Python 3.11+ 解释器，可按实际环境替换示例中的 `python3.11`。

诊断使用随技能携带的文件哈希基线提示源码变化；指南用于定位，当前实现与测试决定结论。保持用户选择的分支和工作区，不为匹配基线自动切分支、升级 CLI 或生成项目知识。

先读 [全局概览](references/global-overview.md)，再按下表选择指南。已熟悉项目且任务明确时，可直接进入相关模块。

## 任务路由

| 当前任务 | 读取 |
| --- | --- |
| 功能开发、修复、重构、源码评审 | [开发流程](references/development.md) + 对应模块 + [验证与发布](references/modules/quality-release.md) |
| Skill 划分、description、指令与引用维护 | [Skill 编写规范](../../docs/skill-authoring.md) + [知识创作工作流](references/modules/authoring-templates.md) |
| 帮助、参数、退出码、中文体验、个人包维护 | [CLI 与维护入口](references/modules/cli-maintenance.md) |
| 接入、升级、卸载、清单、资产冲突、Git 保护 | [项目安装与所有权](references/modules/installation.md) |
| CodeBuddy / Claude / Cursor / Codex / DSH 接入与运行时 | [平台与常驻指引](references/modules/platforms-hooks.md) |
| 源码发现、冻结、解析、编译器、语言扩展、缓存命中 | [N1–N2：源码与观察](references/modules/machine-corpus-facts.md) |
| 身份解析、调用关系、拓扑、入口到效果、能力遍历 | [N3–N4：解析与能力](references/modules/machine-resolution-capability.md) |
| 范围候选、聚类建议、证据包、上下文、游标、摘要 | [N5–N6：投影与交付](references/modules/machine-projection-packet.md) |
| 当前项目上下文、知识路由、排名、源码回退、预算 | [检索与编排](references/modules/context-retrieval.md) |
| Markdown 身份、CAS、知识更新、锚点、完整性与发布核验 | [知识写入与核验](references/modules/knowledge-publication.md) |
| init/reinit/update/sync 行为、生成正文、范围确认、模板 | [知识创作工作流](references/modules/authoring-templates.md) |
| 多仓工作区、成员寻址、外层导航、隔离 | [工作区](references/modules/workspace.md) |
| wheel、源码包、依赖、CI、测试选择 | [验证与发布](references/modules/quality-release.md) |
| 文章、汇报、技术介绍、分享大纲、架构图 | [源码依据与写作](references/writing.md)；涉及的机制联读对应模块 |
| 核对实现依据、源码版本与验证范围 | [源码依据与版本核对](references/sources.md) |

## 最容易改错的边界

- Modus 安装接入、初始化证据、长期 Markdown 知识有不同所有者。`modus init` 安装资产；`/modus-init` 由助手调查并创作知识。
- 普通检索读当前源码与正式 Markdown。初始化分析缓存不成为日常运行的事实源；新增能力不要把 `machine` 导入普通 CLI 路径。
- N1–N6 是确定性证据处理，K1–K6 是助手的语义创作。能力组合不调用 LLM，候选与代表路径不等于正式领域或完整运行链路。
- 安装/更新事务与知识更新的失败语义不同。知识更新按文件提交并报告部分成功，不能承诺整批回滚。
- `.modus/` 和宿主副本是受管接入资产；`modus/knowledge/` 是长期知识；人工 `constraint/`、`references/business/` 有独立保护。
- `clean` 只证明检查器所覆盖的完整性或发布承诺，不证明正文真实、完整、清晰，也不证明运行时成功。
- 命令、JSON 字段、状态码、稳定 ID 与中文展示分开维护。模板是随包交付的产品行为契约。

## 完成任务

开发结果说明具体行为、修改所有者、实际验证和未验证边界。写作结果把当前实现、设计目标、历史材料和效果证据分开。引用本技能能加速定位，但实现结论必须回读当前源码。

本技能支持后续开发，不授予发布、提交、推送、外部文档写入或委派权限；这些动作沿用当前用户任务的授权。不要因使用本技能自动重建知识、更新技能或改动无关资产。
