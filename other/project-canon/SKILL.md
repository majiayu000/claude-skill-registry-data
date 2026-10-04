---
name: project-canon
description: "Maintain a project's canonical truth across long-running AI collaboration. Discover authoritative project documents, identify the current valid plan, audit conflicts and duplicates, absorb external materials through Preview and confirmation, route decisions and changes to the right files, separate design acceptance from implementation and verification, archive processed sources safely, and resume after context loss. Use when users ask which plan is current, want to take over or organize project docs, update current/decisions/changes/delivery/evidence, reconcile docs with code, archive reviewed materials, or continue without re-deciding settled issues. Do not use for generic Markdown formatting or one-time mass document summarization."
---

# Project Canon

维护长期项目的唯一有效事实、变更关系、实施证据和接续入口。先服从项目内已有规则；没有规则时，才提出最小必要结构。

## 核心边界

- 把项目文件、代码和新鲜验证证据视为事实源，不把聊天记忆当作事实源。
- 区分目标方案已确认、代码已实现、验证已通过和真实使用有效；不得相互代替。
- 不把未确认候选写入当前有效方案。
- 不用代码现实静默覆盖已确认方案；先记录差异，再裁决修代码还是修方案。
- 不复制近似正文到多个权威文件；选择一个主位置，其余位置链接引用。
- 不为可能的未来需求预建空目录、空模板或完整治理体系。
- 分析、审阅、诊断和报告请求默认只读。只有用户要求修改，才执行写回。
- 归档前先完成提取和映射；默认归档，不默认删除。

## 选择任务路径

先判断本次任务属于哪一类：

| 路径 | 适用请求 | 默认动作 |
| --- | --- | --- |
| 审计 | “哪个方案有效”“检查冲突或重复” | 只读扫描并输出差异与 Preview |
| 接管 | “整理现有项目”“建立当前方案入口” | 先分类和 Preview，确认后迁移 |
| 维护 | “更新 current / Decision / 变更 / 交付状态” | 沿用项目现有格式，进行最小写回 |
| 恢复 | “继续上次工作”“上下文中断后接着做” | 重读权威入口和新鲜现实，不重做已确认决策 |

不要把“接管”当成长期目录模式。不要因为启用本 Skill 就重构项目文档。

## 第一步：发现本地权威

1. 读取适用的 `AGENTS.md`、项目入口 README、文档规则和当前执行入口。
2. 搜索表示当前方案、候选变更、重要决策、实施状态、验证和来源的现有文件。
3. 审计或恢复时先检查版本控制状态，识别未提交、未跟踪和并发修改；写操作前再次检查相关文件，保留用户已有改动。
4. 验证每个权威候选的本地适用性：检查它声明的目录和链接真实存在、项目名称与术语一致、存在采用或确认依据。文件自称“当前生效”不能单独证明权威。
   - 例外：用户明确要求按某份本地规则开始接管时，可把它视为“已采用的启动契约”，即使目标目录尚未创建。
   - 启动契约只授权采用治理方法；不自动确认从旧材料推导出的产品结论、当前 Gate、完成状态或归档清单。
5. 对活跃工作区记录关键入口的修改时间、大小或哈希；形成结论前复核。审计期间发生变化时，标记快照不稳定，不混合不同时间点的内容。
6. 建立临时权威映射：

```text
当前已确认目标：
尚未确认的问题：
重要取舍及原因：
正式实施范围：
实际实现与验证状态：
来源和大型证据：
当前执行入口：
```

7. 如果项目已有一致规则，严格沿用其目录、命名、编号和状态值。
8. 如果规则缺失或互相冲突，先报告冲突，不自行选一套规则覆盖项目。

需要判断信息路由和冲突时，读取 [references/authority-and-routing.md](references/authority-and-routing.md)。
需要采用本地规则、迁移目录或批量归档时，读取 [references/adoption-and-migration.md](references/adoption-and-migration.md)。

## 第二步：选择最小治理结构

- 小项目且尚无治理结构时，优先提出轻量结构：一个项目入口、一个当前方案、一个交付状态；归档目录按需创建。
- 已有清晰结构时，不迁移到本 Skill 的示例结构。
- 只有长期、多阶段、跨产品与技术、存在正式变更和证据追溯需求时，才建议结构化治理。
- 采用结构化治理前，读取 [references/structured-governance-profile.md](references/structured-governance-profile.md)，并把具体目录、文件名和确认主体写入项目自己的入口文档。

除非用户明确要求建立或迁移结构，否则只输出建议，不创建目录。

## 第三步：审阅与 Preview

对外部材料、历史方案、聊天记录或杂乱文档执行：

1. 完整阅读相关材料。
2. 区分用户明确确认、用户仍在讨论、他人或 AI 建议、外部事实、代码与测试证据。
3. 对照当前权威位置，分类为：已覆盖、可吸收、冲突、候选、需核验、无长期价值。
4. 输出写入 Preview，列出每个结论的目标文件、目标章节、理由、来源和预期状态。
5. 单独列出拟新建、修改、移动、归档或删除的文件。
6. 提供两种文件处置方案：
   - 保守整理：建立新结构、来源映射和索引，原文件留在原处。
   - 迁移归档：建立新结构并把已吸收材料移动到归档位置；适合用户明确希望清理散落文件的任务。
7. 分开确认四类授权：采用治理规则、确认内容结论、采用当前 Gate/状态、文件处置方案及范围。不得用其中一种确认替代另一种。
8. 等待用户确认会改变目标方案、确认状态、目录结构或来源处置的内容。

处理来源材料前读取 [references/source-intake-and-archive.md](references/source-intake-and-archive.md)。需要标准确认卡时复制并调整 [assets/templates/intake-preview.md](assets/templates/intake-preview.md)。

## 第四步：按确认结果写回

只写入已获授权且已经确认的内容。推荐顺序：

```text
记录确认凭证
→ 更新重要 Decision
→ 原地更新当前方案
→ 建立 Decision 与当前方案的双向链接
→ 更新候选大纲或正式变更
→ 更新实施与验证状态
→ 更新来源映射
→ 执行已确认的归档
→ 检查链接、状态和唯一权威
```

- 采用迁移归档时先固定清单；可以按确认的文件清单移动，也可以按用户明确批准且已枚举内容的目录整体移动。混有范围外运行资产时，只移动范围内材料。
- 不按扩展名判断材料性质。HTML、CSS、脚本、JSON、图片等既可能是当前实现，也可能是历史原型或大型证据；先检查生命周期、当前引用、运行入口和替代关系。
- 先写新位置并验证覆盖与链接，再执行归档；归档失败时保留源文件并报告，不自行改为复制、删除或扩大范围。
- 未确认问题继续留在候选或提案位置。
- 实施级待定项可留在正式变更，但会改变目标方案的问题必须退回讨论。
- 当前方案只保存已确认结论及必要来源链接，不保存审批流水或开发日志。
- 实施状态和验证证据写入交付位置，不写入当前方案。
- 对 Bug 排查等进行中工作，在项目已有交付入口维护同一条记录，覆盖发现、排查、修复、验证和关闭；只在事实、授权、实施、验证或阻塞发生实质变化时追加检查点，不逐轮复制聊天。
- 修复只是恢复已确认行为时，不必新建 Change；修复改变目标方案、正式范围或重要取舍时，再分别路由到 Change、Decision 或当前方案。
- 项目已有模板时沿用项目模板；没有模板且确有新建需要时，才使用：
  - [assets/templates/decision.md](assets/templates/decision.md)
  - [assets/templates/change.md](assets/templates/change.md)
  - [assets/templates/delivery.md](assets/templates/delivery.md)

## 第五步：验证完成

在声明完成前：

1. 重新读取所有实际修改的文件。
2. 搜索旧文件名、旧路径、旧标题、编号和文字章节引用。
3. 验证 Markdown 链接能定位到真实文件，并检查链接语义没有漂移。
4. 检查每条当前结论只有一个权威主位置。
5. 检查确认、实现、验证状态没有混写或互相倒推。
6. 检查当前执行入口指向真实活跃工作，而不是根据文件排序推断。
7. 对账汇总入口与详细执行文件；不一致时报告状态滞后，不静默选择一处覆盖另一处。
8. 检查来源材料已完成提取、映射和处置记录。
9. 重复运行同一整理流程时，不得产生重复 Decision、变更、索引条目或归档副本。
10. 涉及代码现实的声明必须依据本轮新鲜检查；历史测试结果只能标记为历史证据。
11. 对照操作前清单，确认没有移动未列入 Preview 的文件、目录或运行资产。
12. 实际归档范围必须与来源登记范围一致；整体移动的来源包必须整体登记，不能只登记其中一份说明文档。

恢复接续、审计链接和制作交付检查时，读取 [references/audit-and-continuation.md](references/audit-and-continuation.md)。

## 非目标

- 不替代项目管理系统、需求管理系统或版本控制。
- 不负责一次性批量总结并集中归档整个项目的全部文档。
- 不要求所有项目使用 `current / changes / delivery / decisions / evidence`。
- 不因文档很长就拆分文件；只在职责真正独立且现有结构已经造成问题时拆分。
- 不为交接另建平行总结；优先更新项目已有当前入口和交付状态。
