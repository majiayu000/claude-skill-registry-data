---
name: feishu-project-official
label: 飞书项目-官方
description: 飞书项目（Meego/Meegle）操作工具。支持查询和管理工作项、节点流转、视图查询、个人待办、排期统计等功能。Use when user needs to work with Feishu/Lark Meego project management — including querying work items, creating/updating work items, completing workflow nodes, checking views, listing todos, analyzing schedules/workloads, or searching with MQL. 关键词：飞书项目、meego、meegle、工作项、需求、任务、缺陷、排期、视图、待办、节点。
---

# 飞书项目 (Meego) 操作指南

本技能通过调用飞书项目 MCP 服务器 `ms_official_meego` 来操作飞书项目数据。输出语言跟随用户输入语言，默认中文。

> 各工具的 `aily-mcp call` 调用示例见 [references/api-examples.md](references/api-examples.md)。

## 前置检查

在执行任何操作前，先确认 MCP 服务器可用：

```bash
aily-mcp servers
```

确认 `ms_official_meego` 在列表中。如果不在，需要调用如下命令安装：
```bash
aily-mcp install ms_official_meego
```

---

## 核心工具 — 元数据查询

### 1. search_project_info

查询空间基础信息，将空间名转换为 project_key 或验证空间是否存在。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_key | string | 是 | 空间 projectKey、simpleName 或空间名称 |

### 2. list_workitem_types

获取指定空间下所有工作项类型列表。用户描述模糊时用此工具确认合法 type_key。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_key | string | 是 | 空间 projectKey |

### 3. list_workitem_field_config

获取指定空间和工作项类型的可用字段配置（不含禁用字段和角色配置）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_key | string | 是 | 空间 key |
| work_item_type | string | 是 | 工作项类型 key 或名称 |
| page_num | number | 是 | 页数，每页 50 条，从 1 开始 |
| field_keys | array | 否 | 精确匹配字段 key 或名称 |
| field_query | string | 否 | 模糊查询字段 key 和名称 |
| field_types | array | 否 | 按字段类型筛选 |

### 4. list_workitem_role_config

获取指定工作项类型的角色列表。用于查询/创建/更新工作项前确认合法 role_key。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_key | string | 是 | 空间 key |
| work_item_type | string | 是 | 工作项类型 key 或名称 |
| page_num | number | 是 | 页数，每页 50 条，从 1 开始 |
| role_keys | array | 否 | 精确匹配角色 key 或名称 |
| role_query | string | 否 | 模糊查询角色 key 和名称 |

### 5. search_user_info

批量查询用户基础信息。用于将姓名/邮箱转换为 userkey。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| user_keys | array | 是 | userKey、Email 或名字，最多 20 个 |
| project_key | string | 否 | 空间 key |

---

## 核心工具 — 数据查询

### 6. search_by_mql

使用 MQL 查询工作项数据。语法详见 [references/mql-syntax.md](references/mql-syntax.md)。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_key | string | 是 | 空间标识（支持名称、simpleName、projectKey） |
| mql | string | 是（翻页时可用 session_id 替代） | MQL 查询语句（完整 SQL） |
| session_id | string | 否 | 分页会话 ID，传入后不解析 MQL 直接翻页 |
| group_pagination_list | array | 否 | 分页信息，首次查询可不传 |

**要点**：
- 务必先用 `list_workitem_field_config` 查询字段类型和结构，查不到直接报错不要继续
- 如涉及角色信息，用 `list_workitem_role_config` 获取角色结构
- SELECT 后属性不宜过多，**优先使用字段 key**（如 `name`、`priority`、`status`）而非字段名称（如 `任务名称`）
- 返回按页返回，需全量数据时必须使用翻页参数

### 7. get_workitem_brief

按 ID/名称查询工作项概况。不传 fields 时仅返回固定基础字段；如需自定义字段数据，先调 `list_workitem_field_config` 获取字段 key 后传入 fields。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| work_item_id | string | 是 | 工作项 ID 或名称 |
| project_key | string | 否 | 空间 key |
| fields | array | 否 | 要查询的 field_key 或 field_name |
| url | string | 否 | 工作项实例链接，可自动解析 |

### 8. list_todo

按 action 类型查询当前用户的工作项列表。无需 MQL 即可查询待办/已办。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| action | string | 是 | todo(待办)/done(已办)/overdue(逾期)/this_week(本周待办) |
| page_num | number | 是 | 页码，从 1 开始，每页 50 条 |
| asset_key | string | 否 | 工作区 key（格式 Asset_xxx），仅在报错需要选择时传 |

**注意**：需完整结果时，从 page_num=1 开始连续查询直到没有更多数据。

### 9. list_schedule

获取指定人员在时间区间内的排期与工作量明细。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| project_key | string | 是 | 空间 key |
| user_keys | array | 是 | 用户标识（名称/邮箱/userkey），**每次最多 3 个** |
| start_time | string | 是 | 开始时间，格式 YYYY-MM-DD |
| end_time | string | 是 | 结束时间，格式 YYYY-MM-DD，**单次跨度最大 2 个月** |
| work_item_type_keys | array | 否 | 工作项类型列表，查询所有传入 `_all` |

**调用约束**（必须遵守）：
1. 每次最多 3 个用户，多人拆分批次并行
2. 单次跨度 ≤ 2 个月，超出按月拆分
3. 所有批次完成后再汇总，未完整获取前不得输出结论

### 10. get_view_detail

根据视图 ID 获取该视图下的工作项列表。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| view_id | string | 是 | 视图 ID |
| project_key | string | 否 | 空间 key |
| page_num | number | 否 | 分页页数起点 |
| fields | array | 否 | 要查询的字段 |
| url | string | 否 | 视图链接，可自动解析 |

### 11. get_node_detail

获取工作项中指定节点或所有节点的完整详情。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| work_item_id | string | 是 | 工作项 ID 或名称 |
| node_id_list | array | 否 | 节点 ID 列表，传空或 `_all` 获取所有节点 |
| field_key_list | array | 否 | 节点字段 key，传空或 `_all` 获取所有字段 |
| need_sub_task | boolean | 否 | 是否需要节点子项（子任务） |
| page_num | number | 否 | 节点信息一次最多 20 个，按页返回 |
| project_key | string | 否 | 空间 key |
| url | string | 否 | 链接，可自动解析 |

---

## 核心工具 — 数据操作

### 12. create_workitem

创建工作项实例。**务必先用 `list_workitem_field_config` 获取字段信息，`list_workitem_role_config` 获取角色信息。模板 ID 是必填项。**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| work_item_type | string | 是 | 工作项类型 |
| project_key | string | 否 | 空间标识 |
| fields | array | 否 | 字段值列表，每项含 field_key 和 field_value |
| url | string | 否 | 可从链接解析空间信息 |

### 13. update_field

修改指定实例的字段值或角色。节点字段更新请用 `update_node`。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| work_item_id | string | 是 | 工作项 ID 或名称 |
| project_key | string | 否 | 空间 key |
| fields | array | 否 | 要更新的字段列表，每项含 field_key 和 field_value |
| role_operate | array | 否 | 角色操作，每项含 op(add/remove)、role_key、user_keys |
| url | string | 否 | 可从链接解析信息 |

**角色更新**：不能通过 fields 更新角色，必须用 `role_operate`。role_key 通过 `list_workitem_role_config` 获取，user_keys 通过 `search_user_info` 获取。

### 14. transition_node

仅用于节点流工作项，操作节点完成流转或回滚。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| work_item_id | string | 是 | 工作项 ID |
| action | string | 否 | confirm（流转） / rollback（回滚） |
| node_id | string | 否 | 节点 ID |
| node_ids | array | 否 | 节点名称或节点 ID 列表 |
| rollback_reason | string | 否 | 回滚原因，action=rollback 时需填写 |
| project_key | string | 否 | 空间 key |

> **扩展工具**：评论、视图搜索/创建、团队、子任务、工时、操作记录、关联工作项、可流转状态查询等工具见 [references/tools-extended.md](references/tools-extended.md)，按需查阅。

---

## 字段值格式（field_value）

`create_workitem` / `update_field` 中 field_value 的格式因字段类型而异：

| 字段类型 | 格式 | 示例 |
|---------|------|------|
| template | 模板 ID（**创建必填**） | `145405865`。用 `list_workitem_field_config(field_keys=["template"])` 获取 |
| text / multi-pure-text / link / bool / number | 单个字面值 | `"测试工作项"` |
| user | 单个 userkey | `"7509072868295085608"` |
| multi-user | userkey 数组 | `["7509072868295085608","7509072868295085609"]` |
| select / radio / tree-select | 枚举项 option_id | `"437794"`。先从字段配置获取枚举值 |
| multi-select | option_id 数组，支持 free_add | `[{"option_id":"111"},{"option_id":"222"}]` |
| multi-text | markdown 格式 | `"**加粗**内容"` |
| date | 毫秒时间戳（天精度） | `1722182400000` |
| schedule | 时间戳数组 [开始, 结束] | `[1722182400000,1722355199999]` |
| precise_date | 对象 {start_time, end_time} | `{"start_time":1722182400000,"end_time":1722355199999}` |
| workitem_related_select | 关联工作项 ID | `145405865` |
| workitem_related_multi_select | 关联 ID 数组（**数字类型**） | `[145405865,145405866]` |
| role_owners（仅创建时） | 角色-人员数组 | `[{"role":"RD","owners":["userkey1"]}]` |

> 更新角色时不用 fields，用 `update_field` 的 `role_operate` 参数。

---

## 常用场景速查

| 场景 | 推荐工具 | 说明 |
|------|----------|------|
| 验证空间 | search_project_info | 空间名 → project_key |
| 查询工作项类型 | list_workitem_types | 确认合法 type_key |
| 查询字段配置 | list_workitem_field_config | 字段 key、枚举值、类型 |
| 人名→userkey | search_user_info | 批量转换，最多 20 个 |
| 复杂条件查询 | search_by_mql | 支持条件筛选、时间范围、团队等 |
| 查我的工作项 | list_todo | 直接获取当前用户的待办/已办 |
| 团队排期统计 | list_schedule | 每次 ≤3 人，≤2 月 |
| 创建需求/任务 | create_workitem | 需先确认字段信息和模板 ID |
| 修改状态/负责人 | update_field | 字段用 fields，角色用 role_operate |
| 完成/回滚节点 | transition_node | action=confirm 或 rollback |
| 查看视图数据 | get_view_detail | 获取视图下的工作项列表 |

## URL 参数处理

用户可能直接提供飞书项目链接，大部分工具支持 `url` 参数自动解析：
- `project_key`、`work_item_type`、`work_item_id`、`view_id`

**常见 URL 动作**：
- 详情页 URL + 无明确意图 → `get_workitem_brief(url=...)`
- 详情页 URL + "修改XX为YY" → `update_field(url=..., fields=...)`
- 详情页 URL + "完成/流转" → 先 `get_workitem_brief(url=...)` 获取 node_id → `transition_node(action="confirm")`
- 详情页 URL + "回滚" → 同上 → `transition_node(action="rollback", rollback_reason=...)`
- 视图页 URL → `get_view_detail(url=...)`

## 通用规范

### 请求处理流程

收到用户输入后，按以下步骤处理：

**1. 参数提取**：从自然语言中提取关键参数：
- 空间名、工作项类型、时间范围、人员、筛选条件等
- 正确区分空间名与筛选维度（如「XX空间下YY业务线的缺陷」中 XX 是空间名，YY 是筛选条件）
- 含 URL 时直接传入工具的 `url` 参数，跳过后续确认步骤

**2. 参数确认**（禁止猜测）：
- **空间**：用 `search_project_info` 探测 → 唯一则用，多个则让用户选，无匹配则问用户
- **工作项类型**：用 `list_workitem_types` 获取类型列表 → 唯一相关则用，多个则让用户选
- **人员**：用 `search_user_info` 转换人名 → 匹配到多个用户时，**禁止自行选择**，展示完整列表让用户指定；无歧义的不需确认
- **缺失的必要参数**：直接问用户，多项缺失时合并为一条消息询问
- **探测 ≠ 猜测**：探测结果不唯一时，必须展示并询问用户，禁止自行选择

> 个人待办（`list_todo`）和 URL 直接操作无需确认步骤。

**3. 元数据收集**（无需用户参与）：
- 调用 `list_workitem_field_config` 获取字段定义（key、类型、枚举值）
  - 需要特定字段时用 `field_keys` 精确查询（如 `field_keys=["template"]`）
  - 不确定字段名时用 `field_query` 模糊查询
- 如涉及角色，并行调用 `list_workitem_role_config`
- **从字段配置中提取关键信息**：
  - 状态字段：type 为 `_work_item_status`，含「完成」「关闭」「终止」的值为完成态
  - 排期字段：type 为 `schedule`，MQL 中用 `__排期字段名_开始时间` / `__排期字段名_结束时间`
  - 优先级字段：key 为 `priority` 或 name 含「优先级」

> 简单直调场景（如添加评论、查看操作记录等只需 project_key + work_item_id 的操作）可跳过此步骤。

**4. 执行**：调用目标工具完成操作，按下方「并行调用」和「大结果处理」规范执行。

### 并行调用

无依赖的工具调用应并行发起。

**必须串行**（前者输出是后者输入）：
- `search_project_info` → `list_workitem_field_config` → `search_by_mql`
- `get_workitem_brief` → `transition_node` / `update_field`
- `list_workitem_field_config` → `create_workitem`

**可并行**：
- `list_workitem_field_config` 和 `list_workitem_role_config`（同类型）
- 多种工作项类型的 `list_workitem_field_config`（如 story + issue）
- 各条件的 count 查询、多人排期分批查询

### 大结果处理

- **分批查询**：`list_schedule` 多人时拆成每批 ≤ 3 人并行
- **精简 SELECT**：只选必要字段，避免富文本等大体积字段
- **按需翻页**：先读首页获取总数，按需翻页

### 错误处理

- 失败后分析错误信息，针对性修正后重试
- **连续 3 次同类失败后停止**，向用户说明原因，询问如何继续

**高频错误速查**：

| 错误现象 | 修复方式 |
|---------|---------|
| 找不到空间 | 用 `search_project_info` 验证，确认 project_key |
| 找不到工作项类型 | 用 `list_workitem_types` 确认合法 type_key |
| 权限错误 | 确认当前用户是否有对应空间的访问权限 |
| MQL 查询失败 | 确认 FROM 用 `` `空间名`.`工作项类型` `` 格式 |
| 数组字段比较报错 | 改用 `array_contains` 或 `any_match` |
| node not found | 先 `get_workitem_brief` 获取真实 node_id，禁止猜测 |
| list_todo 需选择工作区 | 根据报错中的工作区列表，将 asset_key（Asset_xxx）传入重试 |
| 人名/团队名重复 | 用 `<id:xxxx>` 消歧语法（见 MQL 语法参考） |
| 节点流转失败 | 先 `get_transitable_states` 确认可流转状态，再 `get_transition_required` 获取必填项 |
| 创建工作项缺少模板 | `list_workitem_field_config(field_keys=["template"])` 获取 |
| 角色更新失败 | 不用 fields，用 `update_field` 的 `role_operate` 参数 |
| 人名→userkey 失败 | 用 `search_user_info` 批量查询 |

