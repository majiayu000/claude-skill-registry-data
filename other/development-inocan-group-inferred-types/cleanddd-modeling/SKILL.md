---
name: cleanddd-modeling
description: 基于 cleanddd-requirements-analysis 结果输出 CleanDDD 建模蓝图，并在 only-danmuku 的 iterate/feature 目录交付 *_gen.json 建模元素与 *_update.sql DDL 变更脚本；用于将已拆解需求落为可生成代码的模型与数据库变更清单。
---

# CleanDDD 建模技能

根据输入需求，输出 CleanDDD 模型并生成 iterate 交付物。

## 前置输入
- 已有 cleanddd-requirements-analysis 的结构化结果（干系人表、需求条目表、业务实体视图、触发/后续动作表、业务规则与依赖、假设与待确认清单）；缺失时先运行需求分析并补齐假设。
- 需求条目/业务实体归类已与用户确认或标注假设。

## 交付产物（必选）
- 在仓库根目录 `iterate/<feature-kebab>/` 生成：
  - `<feature_snake>_gen.json`：建模设计元素
  - `<feature_snake>_update.sql`：DDL 结构变更脚本
- 目录命名使用 kebab-case；文件前缀使用 snake_case，并与目录语义保持一致。
- 如无 DDL 变化，仍输出 `_update.sql` 并注明 `-- no schema change`。
- 参考 `iterate/video-post-processing-variant-encrypt` 的命名与风格。

## 建模元素 JSON
- 参照 `references/iterate-deliverables.md` 的 tag/字段约定；保持与 `design/_gen` 与 `iterate/*/*_gen.json` 一致。

## 数据库注解（表/列 COMMENT）
- 参照 `references/DB_ANNOTATIONS.md` 的注解语法与作用；必要时在 DDL 的 `COMMENT` 中写入 `@Name` / `@Name=value`。
- 注解用于影响 codegen（如表/列忽略、关系、枚举、类型、聚合根/值对象等），需在交付说明中标出关键注解。

## 工作流
1) 校验输入：确认需求条目表、业务实体视图、触发/后续动作表齐备；缺口先追问或注明假设。
2) 定义聚合：基于职责和不变式，定义聚合根、实体/值对象、行为、触发的领域事件；保持聚合间无直接引用。
3) 映射命令与查询：为每个需求条目映射命令/查询；写明输入/输出、幂等性、涉及的聚合行为。
4) 列出领域事件与处理器：根据触发/后续动作表列出领域事件、订阅方、处理动作；通过事件驱动跨聚合协作。
5) 补全 API 端点：补全路径/方法、鉴权范围、幂等性；绑定命令/查询并标明默认排序/分页。
6) 定义定时任务：如有周期性需求，写明任务名称、频率、触发的命令/查询。
7) 生成交付物：把模型写入 `*_gen.json`，把数据库变更写入 `*_update.sql`，并在回复中列出文件路径与要点。

## 模型清单（用于讨论/确认）
- 聚合
  - 名称 | 职责摘要 | 关键不变式
  - 实体/值对象 | 属性（含默认值/可选值） | 行为 | 触发领域事件（DomainEvent）
- 命令（Commands）
  - 名称 | 作用聚合 | 输入 | 触发行为/事件 | 幂等性
- 查询（Queries）
  - 名称 | 作用聚合 | 过滤/排序/分页 | 输出 DTO 或 Response
- 事件处理器（DomainEventHandlers）
  - 领域事件（DomainEvent） | 订阅方 | 处理动作 | 副作用/外部依赖
- API 端点（Endpoints）
  - 路径/方法 | 命令/查询 | 认证/鉴权 | 幂等/一致性说明
- 定时任务（如有）
  - 名称 | 频率 | 触发的命令/查询 | 幂等/补偿

## 统一命名与放置约定
- 命名风格：聚合/命令/事件/查询/端点使用 PascalCase；事件名称采用过去式。
- 输出文件：`iterate/<feature-kebab>/<feature_snake>_gen.json` 与 `iterate/<feature-kebab>/<feature_snake>_update.sql`。
- 术语统一：统一使用“API 端点（Endpoints）”“领域事件（DomainEvent）”“领域事件处理器（DomainEventHandlers）”等术语。
- 交付承接：本技能输出文件应作为 `cleanddd-kotlin-coding` 的输入依据。

## 核心原则
- 边界明确：聚合之间不直接或间接相互引用。
- 实体共享限制：聚合不共享实体，允许共享值对象。
- 领域事件原则：领域事件由聚合行为产生；跨聚合影响通过领域事件实现最终一致性。
- 关键不变式：在聚合行为前置校验，任何状态变更不得破坏。
- API 端点鉴权：依据干系人表与需求条目表明确认证范围与幂等性。

## 交付与确认
- 在回复末尾列出“参数汇总 + 是否执行”提示，确保用户确认后再进入 `cleanddd-kotlin-coding`。
- 列出未决问题或假设，避免后续编码阶段遗漏。
