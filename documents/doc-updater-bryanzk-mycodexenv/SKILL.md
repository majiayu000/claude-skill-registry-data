---
name: doc-updater
description: 文档与 codemap 更新专家，用于生成/更新 docs/CODEMAPS、README 与指南；在功能变更、API 变更或架构调整后主动执行。
---

# Doc Updater

## 概述

保持文档与代码一致，生成或更新 codemap，并刷新 README 与各类指南，确保示例可运行、链接可用。

## 工作流

1. 结构扫描
   - 识别工作区/包、入口文件、主要模块
2. 模块与依赖分析
   - 提取导出与依赖关系
   - 识别路由、模型、任务/队列
3. 生成/更新 codemap
   - 默认输出到 `docs/CODEMAPS/*`
4. 更新文档
   - README、指南、API 文档等
5. 校验
   - 检查链接、示例可运行、路径存在

## 执行要点

- 优先使用项目已有脚本或命令（若存在）
- 生成内容需基于代码事实，避免手写猜测
- 仅在确认路径与示例有效后更新文档

## 参考资料

需要 codemap 结构模板、命令示例或质量清单时，读取 `references/doc-updater-details.md`。
