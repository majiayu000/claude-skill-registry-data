---
name: Hono API 编写助手
description: Hono API 编写助手，基于用户需求创建新的 API，或修改现有 API。
---

# API 编写助手

Hono API 编写助手用于基于需求规划、实现并维护新的或现有的 API 功能。

## 工作流程

1. 理解需求：核对需求描述与现有规范，必要时向请求方确认边界条件。
2. 分析数据：阅读 [db_schema.md](db_schema.md) 了解实体关系，评估是否需要新增字段或索引，如需请输出对应的迁移脚本草案。
3. 规划接口：在草稿中列出路由、方法、请求体验证、权限策略以及响应结构。
4. 实现功能：按照项目约定在对应 router 中实现逻辑，复用公共工具并保持 EdgeOne 兼容。
5. 编写示例：提供至少一个请求与响应示例，涵盖成功与常见错误场景。
6. 更新文档：同步修改 [apps/server/README.md](../../../apps/server/README.md) 或相关变更记录。

## 交付内容

- 完整的 API 规格说明（路由、方法、参数、响应、错误码、权限）。
- 对应的实现代码及单元测试。
- 示例请求与响应样本。
- 更新后的文档或变更说明。

## 参考资料

- 需求文档: [prd.md](prd.md)
- 项目数据库结构：[db_schema.md](db_schema.md)
- API 接口开发 SOP：[sop.md](sop.md)
- 第三方 AI 集成接口文档 [ai_api_doc](ai_api_doc.md)
- 接口文档：[../../../apps/server/README.md](../../../apps/server/README.md)
