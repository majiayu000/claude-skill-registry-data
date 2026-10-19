---
name: domain-modeling
description: 澄清 LATTICE 领域术语、编辑 docs/reference/glossary.md，或记录架构决策及其取舍。
---

先按当前宿主读取 [Pi 说明](../../README.pi.md)或 [Delta 说明](../../README.delta.md)，再读取仓库内的[源工作流](../../skill-sources/domain-modeling/SKILL.md)。

修改领域文档前，读取 `docs/agents/domain.md`，按其中顺序核对相关 active 合同、
术语表与必要的 ADR。当前规范以合同及其明确保留的未承接来源为准，
ADR 用于理解理由、取舍与历史；发现冲突先报告，规范变化须交人类裁决。

## 术语读写适配

本项目唯一术语读写路径是 `docs/reference/glossary.md`，ADR 仍位于 `docs/adr/`。
源 `SKILL.md` 和 `CONTEXT-FORMAT.md` 中的布局识别、术语定位、缺失时创建、
词汇对照及 inline update，凡目标为 `CONTEXT.md`，均改用上述术语表路径。
不按源示例重新创建根 `CONTEXT.md`，也不引入多 context 布局。
若术语表缺失，先报告并确认原因；获准创建时也只在 `docs/reference/glossary.md` 写入。

编辑词条前读取源目录的 [CONTEXT-FORMAT.md](../../skill-sources/domain-modeling/CONTEXT-FORMAT.md)，保留现有标题、术语分节、
`**术语**:`、简短中文定义、关键区别、合同链接及 `_Avoid_` 格式。
继续执行源工作流的术语质疑、精确命名、具体场景讨论和必要的源码核对；
术语确定且获准修改后即时回写术语表，不把实现细节或完整规范写进词条。
回写后核对目标路径、词条格式和合同引用，确认未生成根 `CONTEXT.md`。

记录 ADR 时保留源工作流的克制条件，并读取源目录的 [ADR-FORMAT.md](../../skill-sources/domain-modeling/ADR-FORMAT.md)；
ADR 的状态和与现行合同的关系遵循项目治理规则。
