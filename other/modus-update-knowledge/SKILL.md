---
name: modus-update-knowledge
description: 用户明确请求根据源码或材料局部维护项目知识时使用，定向更新受影响正文；全量复核使用 modus-reinit，代码任务内的知识同步使用 modus-sync-knowledge。
---

# modus-update-knowledge

局部维护正文时使用。完整读取[增量维护流程](../using-modus/references/authoring/incremental.md)，沿其链接按需加载证据、正文与发布细则。本入口只确定用户意图与授权，不运行全量六阶段、不构建或读取初始化 bundle。

- 以用户目标、当前源码/diff/材料和相关完整正文确定起点，再追踪真实受影响的主定义、消费者与导航；不把初始文件清单当作影响范围的全部。
- 既有稳定身份、主定义与语义分组默认保持。真实新增、拆并、迁移或退役只合并确认一次，沿用已有完整授权；anchor-only、标题和分片调整不重复确认。
- 人工 constraint/business 默认保护。明确委托维护 Team Standard 才启用维护权限，首次初始化权限不用于增量更新；查阅材料不等于授权保存原始副本。
- 完成受影响正文的修订、逐篇回读、实际预览、定向核验与 CAS 发布。报告真实写入、未变、冲突和未验证项，不将局部维护扩大为全库重写。
