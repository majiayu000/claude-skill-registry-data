---
name: "ok-cosmic"
description: "金蝶云苍穹开发主 Skill，优先复用 kd-cd-cosmic-commons 封装。适用于插件开发、单据/列表/表单逻辑、操作服务、BOTP 转换、后台视图打开、附件处理、DynamicObject 与元数据处理、弹性域解析及 OpenAPI 集成。默认优先使用仓库封装；在涉及原生插件事件、SDK API、方法签名或封装未覆盖场景时，使用内置脚本进行查询。"
---

# 苍穹开发

默认按"封装优先，原生兜底"工作，避免在仓库已封装的场景里退回到 BOS 原生低层 API。

## 最短决策路径

1. 先判断插件类型或能力类别（查下方决策矩阵）。
2. 先读对应 `references/*.md`，确认事件边界与适用场景。
3. 再读对应 `assets/*.java` 模板，沿用已有方法签名和骨架。小场景可直接用 `assets/snippets/*.java`。
4. 字段不确定先查 `cosmic-form-metadata.py`，SDK 签名不确定先查 `cosmic-api-knowledge.py`。
5. 只有"插件类型 + 事件方法 + 字段/签名"都确认后，才开始生成代码。
6. **代码生成后，必须执行 `cosmic-post-lint.py` 自动校验**；若存在 ERROR 级问题须立即修复并重新校验直到通过。

## 快速决策矩阵

| 需求关键词 | 插件类型          | 封装文档 (先读) | 原生文档 (兜底) | 模板文件 |
|---|---------------|---|---|---|
| 表单 UI / 字段联动 / 控件交互 | 表单插件          | [plugin-base.md](references/adv/plugin-base.md) | [plugin-form.md](references/base/plugin/plugin-form.md) | [FormPluginTemplate.java](assets/FormPluginTemplate.java) |
| 单据 UI / 审核提交按钮 | 单据插件          | [plugin-base.md](references/adv/plugin-base.md) | [plugin-bill.md](references/base/plugin/plugin-bill.md) | [BillPlugInTemplate.java](assets/BillPlugInTemplate.java) |
| 列表 / 多选操作 / 批量 | 列表插件          | [plugin-base.md](references/adv/plugin-base.md) | [plugin-list.md](references/base/plugin/plugin-list.md) | [ListPluginTemplate.java](assets/ListPluginTemplate.java) |
| 左树右表（单据） | 单据树列表插件（列表）   | [plugin-base.md](references/adv/plugin-base.md) | [plugin-tree-list.md](references/base/plugin/plugin-tree-list.md) | [TreeListPluginTemplate.java](assets/TreeListPluginTemplate.java) |
| 左树右表（基础资料） | 基础资料树列表插件（列表） | [plugin-base.md](references/adv/plugin-base.md) | [plugin-tree-list.md](references/base/plugin/plugin-tree-list.md) | [StandardTreeListPluginTemplate.java](assets/StandardTreeListPluginTemplate.java) |
| 审核 / 保存 / 状态流转 / 校验 | 操作插件          | [operate-chain.md](references/adv/operate-chain.md) | [plugin-operation.md](references/base/plugin/plugin-operation.md) | [OpPluginTemplate.java](assets/OpPluginTemplate.java) |
| 下推 / 选单 / 转换 | 转换插件          | [botp-convert.md](references/adv/botp-convert.md) | [plugin-botp.md](references/base/plugin/plugin-botp.md) | [ConvertPlugInTemplate.java](assets/ConvertPlugInTemplate.java) |
| 反写 / 关联更新 | 反写插件          | [botp-convert.md](references/adv/botp-convert.md) | [plugin-writeback.md](references/base/plugin/plugin-writeback.md) | [WriteBackPlugInTemplate.java](assets/WriteBackPlugInTemplate.java) |
| 报表 / 数据分析 | 报表插件          | — | [plugin-report-form.md](references/base/plugin/plugin-report-form.md) | [ReportFormPluginTemplate.java](assets/ReportFormPluginTemplate.java) |
| 报表取数 | 报表取数插件        | — | [plugin-report-data.md](references/base/plugin/plugin-report-data.md) | [ReportListDataPluginTemplate.java](assets/ReportListDataPluginTemplate.java) |
| 打印 / 套打 | 打印插件          | — | [plugin-print.md](references/base/plugin/plugin-print.md) | [PrintPluginTemplate.java](assets/PrintPluginTemplate.java) |
| OpenAPI / 外部集成 | OpenAPI 控制器   | — | [plugin-openapi.md](references/base/plugin/plugin-openapi.md) | [OpenApiControllerTemplate.java](assets/OpenApiControllerTemplate.java) |
| 后台任务 / 定时 | 后台任务          | — | [plugin-task.md](references/base/plugin/plugin-task.md) | [TaskTemplate.java](assets/TaskTemplate.java) |
| 工作流 / 审批流 | 工作流插件         | — | [plugin-workflow.md](references/base/plugin/plugin-workflow.md) | [IWorkflowPluginTemplate.java](assets/IWorkflowPluginTemplate.java) |
| 导入 / 批量导入 | 导入插件          | — | [plugin-import.md](references/base/plugin/plugin-import.md) | [BatchImportPluginTemplate.java](assets/BatchImportPluginTemplate.java) |

## 能力封装路由（按需加载，只读相关的 1-2 个文档）

- **IF** 涉及保存/提交/审核/回滚 → 读 [operate-chain.md](references/adv/operate-chain.md)
- **IF** 涉及下推/选单/来源追踪 → 读 [botp-convert.md](references/adv/botp-convert.md)
- **IF** 涉及查询/聚合/DataSet → 读 [query-dataset.md](references/adv/query-dataset.md)
- **IF** 涉及后台打开表单/列表 → 读 [view-handler.md](references/adv/view-handler.md)
- **IF** 涉及表单控件/UI消息/元数据读取 → 读 [form-utils.md](references/adv/form-utils.md)
- **IF** 涉及 DynamicObject 安全取值/序列化 → 读 [dynamic-object.md](references/adv/dynamic-object.md)
- **IF** 涉及实体元数据/字段路径/DBRoute → 读 [entity-metadata.md](references/adv/entity-metadata.md)
- **IF** 涉及弹性域字段/值解析 → 读 [flex-prop.md](references/adv/flex-prop.md)
- **IF** 涉及附件上传/下载/复制 → 读 [attachment-api.md](references/adv/attachment-api.md)
- **IF** 涉及跨线程身份/上下文恢复 → 读 [request-context.md](references/adv/request-context.md)

## 原生 SDK 兜底路由（仅在封装层不够用时）

- ORM/QFilter/KSQL → [sdk-orm-access.md](references/base/sdk/sdk-orm-access.md)
- 内存计算/DataSet → [sdk-algo.md](references/base/sdk/sdk-algo.md)
- 公共服务/ServiceHelper → [sdk-dynamic-model-svc.md](references/base/sdk/sdk-dynamic-model-svc.md)
- DynamicObject → [sdk-dynamic-object.md](references/base/sdk/sdk-dynamic-object.md)
- 元数据/EntityModel → [sdk-entity-model.md](references/base/sdk/sdk-entity-model.md)
- 分布式ID → [sdk-id.md](references/base/sdk/sdk-id.md) | 锁 → [sdk-lock.md](references/base/sdk/sdk-lock.md) | 缓存 → [sdk-cache.md](references/base/sdk/sdk-cache.md) | 事务KDTX → [sdk-tx.md](references/base/sdk/sdk-tx.md)
- 日志 → [sdk-log.md](references/base/sdk/sdk-log.md) | 异常 → [sdk-exception.md](references/base/sdk/sdk-exception.md) | 线程池 → [sdk-threadpool.md](references/base/sdk/sdk-threadpool.md)
- 文件 → [sdk-file.md](references/base/sdk/sdk-file.md) | 上下文 → [sdk-request-context.md](references/base/sdk/sdk-request-context.md) | 网控 → [sdk-network-control.md](references/base/sdk/sdk-network-control.md)
- 工具类 → [sdk-utils.md](references/base/sdk/sdk-utils.md)

## 子文件引用

以下文件提供详细规则，AI 应在需要时按需加载：

- 高频 API 速查表（无需脚本验证） → [rules/cheat-sheet.md](rules/cheat-sheet.md)
- 禁忌清单（幻觉方法名/类名/场景错配） → [rules/anti-patterns.md](rules/anti-patterns.md)
- 插件开发 8 步流程 → [rules/plugin-dev-flow.md](rules/plugin-dev-flow.md)
- 编码偏好与实现细则 → [rules/coding-preferences.md](rules/coding-preferences.md)
- 强制约束与验证策略 → [rules/constraints.md](rules/constraints.md)
- 工作流与配置自检 → [rules/workflow.md](rules/workflow.md)
- **生成后自动校验规则** → [rules/post-lint.md](rules/post-lint.md)
- 场景化代码片段 → 见下方 snippets 映射表

## 场景化代码片段 (snippets)

模板骨架给出完整插件结构，snippets 给出**单个场景的最小可运行示例**。遇到以下场景时，优先读对应 snippet 再写实现：

| 场景关键词 | snippet 文件 |
|---|---|
| 字段取值/赋值/getValue/setValue | [GetAndSetValueSample.java](assets/snippets/form/GetAndSetValueSample.java) |
| 分录行计算/汇总/金额联动 | [EntryRowCalculateSample.java](assets/snippets/form/EntryRowCalculateSample.java) |
| 确认框/二次确认/ConfirmCallBack | [ConfirmDialogSample.java](assets/snippets/form/ConfirmDialogSample.java) |
| 操作前拦截确认/beforeDoOperation | [BeforeOperationConfirmSample.java](assets/snippets/form/BeforeOperationConfirmSample.java) |
| F7 过滤/基础资料弹窗过滤 | [F7FilterSample.java](assets/snippets/form/F7FilterSample.java) |
| 打开单据弹窗/showForm/Modal | [OpenBillModalSample.java](assets/snippets/form/OpenBillModalSample.java) |
| 子页面回传数据/closedCallBack | [ReturnParentDataSample.java](assets/snippets/form/ReturnParentDataSample.java) |
| 树形控件/TreeView/树节点 | [TreeControlSample.java](assets/snippets/form/TreeControlSample.java) |
| 列表插件基础/选中行/批量操作 | [ListPluginBasicSample.java](assets/snippets/list/ListPluginBasicSample.java) |
| 列表预打开过滤/setFilter | [ListPreOpenFilterSample.java](assets/snippets/list/ListPreOpenFilterSample.java) |
| 操作校验器/addValidators | [OpAddValidatorsSample.java](assets/snippets/operation/OpAddValidatorsSample.java) |
| 下推/选单/来源追踪/BotpUtils | [BotpTracePushSample.java](assets/snippets/botp/BotpTracePushSample.java) |
| 查询/聚合/DataSet/统计 | [DataSetQueryStatSample.java](assets/snippets/query/DataSetQueryStatSample.java) |
| 基础资料查询/loadFromCache | [BaseDataQuerySample.java](assets/snippets/query/BaseDataQuerySample.java) |
| DynamicObject 操作/安全取值 | [DynamicObjectOpsSample.java](assets/snippets/data/DynamicObjectOpsSample.java) |
| 附件上传/绑定/AttachmentUtils | [AttachmentUploadBindSample.java](assets/snippets/attachment/AttachmentUploadBindSample.java) |
| 消息通知/邮件/MessageService | [MessageNotifySample.java](assets/snippets/message/MessageNotifySample.java) |
| 后台调度任务/定时任务 | [ScheduleTaskSample.java](assets/snippets/task/ScheduleTaskSample.java) |

## API 知识与元数据查询脚本

本 Skill 提供了两个核心 Python 脚本，用于查询苍穹 SDK API 和表单元数据。

### A. 知识图谱查询脚本 (`cosmic-api-knowledge.py`)
用于模糊搜索类名、获取类方法签名、继承树与注释。
- **用法**: `python3 <SKILL_ROOT>/scripts/cosmic-api-knowledge.py [options] <command> [args]`
- **常用命令**:
  - `search <query...>`: 模糊搜索类名。支持多关键词，默认任一关键词命中即可返回；加 `--all` 表示全部关键词都要命中。
  - `search-method <query...>`: 全局搜索方法名。支持多关键词，默认任一关键词命中即可返回；加 `--all` 表示全部关键词都要命中。结果会优先把与查询词更接近的方法排在前面，并展示方法说明摘要。
  - `detail <classname>`: 获取指定全限定类名的详细信息。
    - 可配合 `--method <keyword>` 只看相关方法。
    - 可配合 `--declared-only` 只看当前类声明的方法，不展开父类。
    - 可配合 `--compact` 输出紧凑事实块，减少 token 消耗，适合继续交给 AI 生成代码。
- **定向过滤能力**:
  - `--class-prefix <prefix>`: 按包前缀或类名前缀过滤，可重复传入多个前缀。
  - `--class-regex <regex>`: 按类全限定名正则过滤。
  - `--kind <helper|servicehelper|plugin|service|utils|runtime|entity|const|enum|controller>`: 按常见类别快速过滤。
- **配置**: 通过 `--config <path/to/ok-cosmic.json>` 指定配置文件(优先匹配当前运行项目的根目录)。

**推荐用法（比裸搜更稳）**
- 查某个领域的 helper：
  `python3 <SKILL_ROOT>/scripts/cosmic-api-knowledge.py --config ok-cosmic.json search Helper --class-prefix kd.bos.servicehelper --kind helper`
- 查某个包下的方法：
  `python3 <SKILL_ROOT>/scripts/cosmic-api-knowledge.py --config ok-cosmic.json search-method send email --class-prefix kd.bos.servicehelper.message`
- 查插件相关类：
  `python3 <SKILL_ROOT>/scripts/cosmic-api-knowledge.py --config ok-cosmic.json search plugin operation --kind plugin --all`
- 精确确认某个类有没有目标方法：
  `python3 <SKILL_ROOT>/scripts/cosmic-api-knowledge.py --config ok-cosmic.json detail "类全限定名" --method "关键词"`
- 精确确认方法是否由当前类自己声明：
  `python3 <SKILL_ROOT>/scripts/cosmic-api-knowledge.py --config ok-cosmic.json detail "类全限定名" --method "关键词" --declared-only`
- 当需要把方法事实继续喂给 AI 做后续生成时：
  `python3 <SKILL_ROOT>/scripts/cosmic-api-knowledge.py --config ok-cosmic.json detail "类全限定名" --method "关键词" --compact`

**AI 调用约束**
- 允许直接传多个关键词，不要再把多个词错误地拆成多个"未知参数"。
- 当第一次裸搜结果过宽时，第二次必须优先补 `--class-prefix` 或 `--kind`，不要连续无过滤地重复大范围搜索。
- 搜 BOS/苍穹核心能力时，优先从这些包前缀收窄：
  - `kd.bos.servicehelper`
  - `kd.bos.entity`
  - `kd.bos.form`
  - `kd.bd`
  - `kd.scm`

**定向搜索优先级**
1. 先定"领域"：
   - BOTP / 下推 / 转换
   - BaseData / 基础资料
   - Message / 邮件 / 消息
   - Form / UI / List / Plugin
2. 再定"包前缀"：
   - BOS 通用服务优先 `kd.bos.servicehelper`
   - 插件事件优先 `kd.bos.entity`、`kd.bos.form`
   - 主数据优先 `kd.bd`
3. 最后再用关键词：
   - 类搜索用 `search`
   - 方法搜索用 `search-method`
   - 类已知时直接 `detail`
4. 需要确认 `@Override` 是否应写在当前类，而不是父类已有实现时：
   - 优先 `detail "类全限定名" --method "关键词" --declared-only`
5. 需要把方法签名、参数说明、返回值作为低噪音事实块继续注入当前会话时：
   - 优先 `detail "类全限定名" --method "关键词" --compact`

### B. 元数据查询脚本 (`cosmic-form-metadata.py`)
用于根据 formId 或 billName 获取单据元数据字段，支持字段模糊筛选。
- **用法**: `python3 <SKILL_ROOT>/scripts/cosmic-form-metadata.py [options] get [args]`
- **参数**:
  - `--form-id`: 表单英文标识。
  - `--bill-name`: 表单中文名称。
  - `--fuzzy`: 字段标识或名称的模糊匹配列表。**[强制] 多个关键词必须用空格分隔（例如 `--fuzzy qty price amount`），支持正则表达式（如 `--fuzzy "qty|price|amount"`），严禁使用逗号分隔。**
  - `--show-detail`: **详情模式开关**。当存在模糊匹配结果时，显示枚举项映射 (`extMap`) 或基础资料引用类型 (`refType`)。
- **配置**: 通过 `--config <path/to/ok-cosmic.json>` 指定配置文件(优先匹配当前运行项目的根目录)。

**AI 调用约束 (元数据查询)**
- **常规对齐**: 仅确认字段标识时，不带 `--show-detail`。
- **深度实现**: 当需要编写 **`if` 条件判断**（针对枚举值）、**手动赋值** 或 **基础资料关联查询** 前，必须带上 `--show-detail`。
- **严禁 SQL**: 有了此参数后，严禁直接通过 SQL 查询 `form_metadata_cache` 表，必须通过脚本获取详情，以保证逻辑的一致性和可维护性。

## 常见实体/能力地图

下面这张"先找哪里"的地图，优先用于缩小搜索范围。

- **操作插件 / 审核保存提交流程**
  - 先看：`kd.bos.entity.plugin.AbstractOperationServicePlugIn`
  - 常看包：`kd.bos.entity.plugin`、`kd.bos.entity.plugin.args`
  - 常见帮助类：`OpUtils`、`OperateChain`、`OperationServiceHelper`

- **表单 / 单据 / 列表 UI 插件**
  - 先看：`kd.bos.form.plugin.*`
  - 常看包：`kd.bos.form`、`kd.bos.form.control`、`kd.bos.list`
  - 关键入口：`this.getView()`、`this.getModel()`

- **BOTP 下推 / 选单 / 转换**
  - 先看：`kd.cd.common.util.BotpUtils`
  - 关键运行时参数：`kd.bos.entity.botp.runtime.PushArgs`、`DrawArgs`、`ConvertOperationResult`
  - 插件扩展：`kd.bos.entity.botp.plugin.AbstractConvertPlugIn`
  - 常见帮助类：`kd.bos.servicehelper.botp.ConvertServiceHelper`

- **基础资料 / 管控策略 / 分配 / 个性化**
  - 先看：`kd.bos.servicehelper.basedata.BaseDataServiceHelper`
  - 主数据扩展包优先：`kd.bd.master.*`
  - 若涉及分配/个性化：再看 `AssignIndividuationHelper`、相关 `helper` / `mservice`

- **数据加载 / 保存 / 查询**
  - 先看：`kd.bos.servicehelper.BusinessDataServiceHelper`
  - 查询类：`kd.bos.servicehelper.QueryServiceHelper`
  - 过滤条件：`kd.bos.orm.query.QFilter`

- **消息 / 邮件 / 短信 / 企业微信**
  - 先看：`kd.bos.servicehelper.message.MessageServiceHelper`
  - 邮件对象：`kd.bos.message.api.EmailInfo`
  - 其他消息对象通常也在 `kd.bos.message.api`

- **DynamicObject / 元数据 / 实体结构**
  - 先看：`kd.bos.dataentity.entity.DynamicObject`
  - 元数据常见入口：`EntityType`、`MainEntityType`
  - 如果字段路径/主键不确定，优先回到元数据脚本和 `entity-metadata.md`

- **附件 / 文件**
  - 先看：`AttachmentUtils`
  - BOS 层常见类：`AttachmentServiceHelper`

- **组织 / 权限 / 上下文**
  - 先看：`RequestContext`、`Permission` 相关 service/helper
  - 碰到组织维度过滤时，优先确认 `appId`、使用组织、主业务组织分别来自哪里

## 代码生成后自动校验（Post-Lint）

**[强制] 在生成或修改任何苍穹 Java 代码后，必须执行以下校验流程：**

1. 对生成的文件执行校验脚本：
   ```bash
   python3 <SKILL_ROOT>/scripts/cosmic-post-lint.py <生成的文件或目录> --fix-hint
   ```
2. 若报告中存在 **ERROR** 级问题，必须**立即修复**后重新执行校验，直到 ERROR 为 0。
3. 若仅存在 **WARNING** 级问题，应优先修复；若有合理理由可保留，须在代码注释中说明原因。
4. **INFO** 级问题为建议项，按团队风格决定是否处理。

**AI 调用约束 (Post-Lint)**
- 每次生成或修改 `.java` 文件后，自动触发 lint 校验，不需要用户手动请求。
- 修复后必须**再次执行**脚本确认通过，形成"生成 → 校验 → 修复 → 复检"闭环。
- 若单次修复后仍有 ERROR，最多重试 3 次；3 次后仍未通过，报告给用户并附带剩余问题清单。
- 校验脚本不替代编译检查；通过 lint 后仍应确保代码可编译。