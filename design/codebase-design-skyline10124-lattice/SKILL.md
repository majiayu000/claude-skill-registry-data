---
name: codebase-design
description: 设计模块接口、寻找职责封装与测试边界，或比较不同接口方案。
---

先按当前宿主读取 [Pi 说明](../../README.pi.md)或 [Delta 说明](../../README.delta.md)，再读取仓库内的[源工作流](../../skill-sources/codebase-design/SKILL.md)。

按分支读取源目录的 [DEEPENING.md](../../skill-sources/codebase-design/DEEPENING.md) 或 [DESIGN-IT-TWICE.md](../../skill-sources/codebase-design/DESIGN-IT-TWICE.md)。保留源工作流的深模块、接口、测试 seam 与方案比较方法，设计以现行领域合同和依赖边界为准。

通用词汇与项目领域冲突时使用 `docs/reference/glossary.md`；Component、API 可以是本项目的真实领域概念。源流程中的 CONTEXT 读取遵循共用适配。

替换测试只在原断言已被等效保护时进行，不因源示例直接删除独立回归。不为假设中的需求预建抽象或依赖。独立设计者按当前宿主说明委派；不可用时顺序比较并披露局限，不能替代任务明确要求的独立设计。
