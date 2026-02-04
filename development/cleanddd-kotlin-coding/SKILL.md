---
name: cleanddd-kotlin-coding
description: 在 only-danmuku 的 CleanDDD Kotlin 项目中编写或修改聚合/命令/查询/API 端点/事件/防腐层 Client/仓储/配置/测试时使用；遵循 代码实现规约.md 与 design/_gen + genDesign 的生成流程。
---

# CleanDDD Kotlin Coding（only-danmuku）

## 必读参考
- 若仓库存在 `代码实现规约.md`，先阅读并以其为准；此技能用于补足执行步骤与易错点。
- 需要新增命令/查询/事件/校验器/Client 时，先更新 `design/*_gen.json`，再执行 `./gradlew genDesign`。

## 前置输入
- 已有 cleanddd-modeling 交付：`iterate/<feature>/*_gen.json` 与 `*_update.sql`。
- 已确认聚合边界、不变式、命令/查询清单与事件链路。

## 快速检查
- 遵循 CQRS：命令不依赖查询、查询不依赖仓储；命令内禁止使用读端 `sqlClient`。
- 聚合边界：仅聚合根发布领域事件；命令/事件不以子实体 ID 作为入参。
- 持久化：命令通过仓储整体加载聚合并使用领域方法变更，禁止直接改字段。
- 防腐层：仅做外部系统/文件交互，不包含数据库 ID 概念。
- 规范：DTO 使用 `Request`/`Response` 后缀；JSR-303 校验 + `KnownException` 处理业务错误。
- Kotlin 风格：4 空格缩进；简单返回用表达式体；避免通配符导入。

## 推荐流程
1) 补设计元素：在 `design/*_gen.json` 中补命令/查询/事件/校验器/Client，执行 `./gradlew genDesign`。
2) 实现 domain：聚合/实体/值对象/领域方法/领域事件。
3) 实现 application：命令/查询契约、校验器、Handler、订阅者。
4) 实现 adapter：Controller、QueryHandler、ClientHandler。
5) 补配置与日志：关键路径配置化，关键行为打点。

## 分层职责
- adapter 层：仅做编排与入参校验，调用 `Mediator.commands.send(...)` 或 `Mediator.queries.send(...)`；不写业务分支、不操作聚合、不访问仓储/事务。
- application 层：组织用例流程与事务边界；命令写端、查询读端分离。
- domain 层：聚合根/实体/领域方法/领域事件；不关注 Web 与持久化细节。

## API 端点（Controller）
- 位置：`only-danmuku-adapter/.../portal/api`，按业务拆分文件，统一 `@PostMapping`。
- 使用 `Request` DTO + JSR-303 注解；必要时配合自定义校验器。
- 只做上下文解析与调用 Mediator，不直接操作聚合或仓储。

## 命令（Command）
- 位置：`only-danmuku-application/.../commands`。
- 单命令只修改一个聚合根；跨聚合通过领域事件 + 额外命令解耦。
- 从仓储加载聚合，调用领域方法完成变更，`Mediator.uow.save()` 提交。
- 复杂校验用“校验器 + 查询”承担；缺查询先在 design 中定义并生成。

## 查询（Query）
- 契约：`only-danmuku-application/.../queries`。
- 实现：`only-danmuku-adapter/.../application/queries`，依赖 `KSqlClient` 而非仓储。
- 返回 DTO 或投影模型；在查询层完成过滤/分页/排序/拼装。

## 聚合与领域方法
- 聚合/实体可变字段统一 `internal set`；禁止在命令中直接赋值。
- 通过领域方法封装状态变更、约束检查与事件触发。
- 生命周期使用 `onCreate/onUpdate/onDelete` 框架回调，禁止业务代码手动调用。

## 领域事件与订阅
- 命名：`实体 + 过去式动作`，如 `VideoPostTranscodingRequiredDomainEvent`。
- 监听器只做编排并触发命令；同一事件多动作时拆分监听方法。
- 事件定义缺失时，先在 design 中补齐并 `genDesign` 生成骨架。

## 防腐层 Client
- 契约：`only-danmuku-application/.../distributed/clients`。
- Handler：`only-danmuku-adapter/.../application/distributed/clients`，仅做外部调用与结果映射。
- 设计元素使用 `cli`（或别名 `client`）；先在 design 中定义再生成。

## 校验器
- 位置：`only-danmuku-application/.../validater`（以仓库实际目录为准）。
- 依赖查询、不依赖仓储；尽早失败并抛 `KnownException`。

## 代码生成与设计文件
- 设计文件位于 `only-danmuku/design/*_gen.json`，支持标签别名（如 `cmd/command`、`qry/query`、`cli/client`）。
- 执行 `./gradlew genDesign` 生成命令/查询/事件/校验器/Client 骨架。

## 其他通用约定
- 日志：只记录关键行为（转码、外部调用），包含关键标识（videoId、uploadId 等）。
- 配置：路径、阈值用配置类管理，避免硬编码。
- 规模限制：列表/数量等限制放在命令或聚合内统一收敛。

## 提交前自检
- 领域事件发布完整，监听器不直接跨聚合改数据。
- 命令未混入查询逻辑，查询未依赖仓储。
- 相关新增元素已落入 design 并通过 `genDesign` 生成骨架。
