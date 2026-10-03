---
name: law086
description: 案件云(law086) AI集成。让律师通过自然语言操作案件云：查询案件列表和详情、创建案件、更新案件进度和状态、管理日程和办案记录、查看和更新客户信息、创建客户、查看项目信息、创建项目、查看财务记录和应收款、收款记录管理、生成文书模板、查询合同、新增合同、更新合同。当用户说"查询案件"、"我的案件"、"创建案件"、"新建案件"、"登记案件"、"录入案件"、"更新案件状态"、"查看日程"、"创建日程"、"查看财务"、"案件云"、"帮我查案件"、"今天有什么安排"、"帮我记录"、"办案记录"、"记录一下"、"添加记录"、"创建办案记录"、"查看客户"、"更新客户"、"创建客户"、"新增客户"、"查看项目"、"创建项目"、"新增项目"、"团队日程"、"应收款"、"收款"、"收款记录"、"未收款"、"待收款"、"已收款"、"逾期"、"应收款汇总"、"财务摘要"、"今年应收"、"今年收款"、"查看合同"、"合同列表"、"我的合同"、"新增合同"、"创建合同"、"更新合同"、"合同信息"、"上传文件"、"上传附件"、"案件文件"、"案件附件"、"查看文件"、"下载文件"、"预览文件"时触发此技能。
---

# 案件云 Open API 集成 V2.0

通过 PAT Token 授权，用自然语言操作案件云。详细 API 文档见 [references/api-reference.md](references/api-reference.md)。

## 前置配置

1. 用户在 OA「个人设置 > AI管理」生成 PAT Token（以 `law086_pat_` 开头）
2. 将 `API_BASE_URL` 和 `PAT_TOKEN` 写入 `.env` 文件（与 SKILL.md 同级）
3. 若 Token 为占位值，提示用户替换

## 数据可见范围

- **个人空间**：本人全部数据。
- **团队/律所管理员或拥有者**：本 org 下全部数据。
- **团队/律所普通成员**：只能看自己参与的数据。
- **律所拥有者（顶层律所 org + OWNER 角色，全所范围始终开启）**：可见/可写范围自动展开为「顶层律所 + 所有直接子团队 org」（扁平一层）。
  - **读端点**：全所可见（cases/clients/projects/finance/dashboard/search/calendar/team/records/contracts 等）。
  - **编辑端点**（PATCH/PUT/上传）：可跨子团队编辑/上传全所任意记录（保留记录自身 org_id，编辑不改归属）。
  - **新建端点**（`POST /cases`、`/clients`、`/projects`、`/calendar`、`/contracts`）：支持可选请求参数 `org_id`（hashid）把新记录归属到本所内任意子团队；不在全所集合则报错「目标组织不在本所范围」；未传默认 PAT 绑定 org。
  - 非 owner 的 PAT 行为零变化（写端点传非自身 org 会报错「目标组织不在本所范围」）。
  - 组织结构目前仅支持扁平一层，多级团队递归为二期；跨子团队 host/assit 改派未开放（指**案件层面**主办/协办律师的改派，需到 OA 网页端；**待办层面** owner 已支持创建时指定主办人，见下方"主办人指派")。
  - **日程/待办跨子团队关联（owner 专属）**：owner 给**子团队案件**推送待办/办案记录（`POST /calendar` type=1，或 `PUT /calendar/{id}` 改关联案件）时，**可不传 `org_id`**，后端会自动把待办归属到案件所在子团队（`POST`）；`PUT` 改关联案件时记录自身 org 不变，但允许关联到全所任意子团队案件。协办人(assit)校验按**案件自身 org**（属于案件所在子团队才合法）。非 owner 维持原严格校验（关联案件必须 ∈ 自身 org），行为不变。
  - **主办人指派（owner 专属）**：律所拥有者通过 `POST /calendar` 推送待办/办案记录时，可指定**主办人**（`huser`），让被指派的员工成为待办主办并能在「我的待办」看到。主办人确定优先级：
    1. 传了 `huser`（hashid，来自 `GET /team/members`）→ 解码并校验属于目标 org 后使用
    2. 未传 `huser` 但传了 `assit` → `huser` = `assit` 解码后的第一个员工
    3. 都没传 → 回落调用者本人（`add_uid` 始终 = 调用者，记录"谁派发的"）
    - **非 owner**：忽略传入的 `huser`，主办人恒为调用者本人（即使传了 `huser` 也会被丢弃）
    - **个人空间**（`org_id=0`）：主办人恒为自己，不允许指定他人
    - **派活推荐用 `huser` 精确指定主办**（与 `PUT /calendar/{id}` 行为一致）；`assit` 回归"协办"本职。owner 派活后**不**把 owner 加入 `assit`（owner 靠全所视图查看）
    - 同时传 `huser` 和 `assit` 时，`huser` 参数优先；`assit` 多人时取第一个作为兜底主办

## 更新 Skill

**更新只需 `git pull`，不要删除重装**（会丢失 `.env` 中的 PAT Token 配置）。详见 README.md。

## API 调用

```bash
python3 scripts/api.py <METHOD> <PATH> [JSON_BODY]
# 示例：
python3 scripts/api.py GET "/cases?keyword=张三&g_status=1"
python3 scripts/api.py POST /calendar '{"title":"开庭","htime":"2026-05-10 14:00","endtime":"2026-05-10 15:00","type":0}'
```


脚本自动处理认证、中文编码和响应解析。所有时间使用**北京时间 (CST, UTC+8)**。

### 响应与错误处理

| code | 含义 | 处理 |
|------|------|------|
| 0 | 成功 | 读取 data。**注意**: code 为整数，须用 `==` 宽松比较，禁止 `===` |
| 1 | 业务错误 | 展示 msg |
| 2 | Token 无效/过期 | 提示重新生成 PAT |
| 3 | 权限不足 | 提示重新生成 PAT 并勾选对应 scope |

### 校验失败处理

当返回 `code:"1"`（业务错误）时，后端 `msg` 会返回字段级、可读性强的具体原因（如 "案件类型无效，只允许 1-5"、"当事人名称不能为空"、"案由长度不能超过 64"）。处理流程：

1. 读取 `msg`，定位到出错的字段或参数
2. 按提示修正对应字段（如枚举值不在合法范围就替换为合法值、必填项缺失就补全）
3. 修正后**直接重试**，不要把原始失败原因直接抛给用户

## 端点速查

> 参数和响应字段的详细说明见 [references/api-reference.md](references/api-reference.md)。

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /dashboard | 每日概览（今日日程、案件动态、待办） |
| GET | /search?keyword= | 统一搜索（跨案件+客户+项目） |
| GET | /enums | 枚举数据字典（案件类型、状态等） |
| GET | /cases | 案件列表（keyword/g_status/type 筛选） |
| GET | /cases/{code} | 案件详情（含当事人、阶段、财务） |
| POST | /cases | 创建案件（必填: type/privyc_data；process_code 参考 GET /enums） |
| PATCH | /cases/{code} | 更新案件（process_code/case_mark/anhao/degree/charge_desc/current_stage_id/anyou/unit_name+unit_type/stage_text）⚠️ unit_name 与 unit_type 须同时提供 |
| GET | /cases/{code}/stages | 案件阶段列表 |
| POST | /cases/{code}/files | 上传文件到案件（multipart/form-data） |
| GET | /cases/{code}/files | 案件附件列表（支持 folder_id 筛选） |
| GET | /cases/{code}/files/{fileId}/url | 获取文件访问链接 |
| GET | /calendar | 日程/记录列表（支持 type+linkid 按案件/项目/客户筛选） |
| POST | /calendar | 创建日程（必填: title/htime/endtime/type；可选: huser 主办人UID仅owner、assit 协办人UID列表） |
| PUT | /calendar/{id} | 更新日程/记录（状态、人员、时间、阶段等，统一更新入口） |
| GET | /team/members | 团队成员列表（个人空间不可用） |
| GET | /clients | 客户列表（keyword 搜索） |
| GET | /clients/{code} | 客户详情（含关联案件） |
| GET | /clients/create-form | 获取客户创建表单 schema |
| POST | /clients | 创建客户 |
| PATCH | /clients/{code} | 更新客户 |
| GET | /clients/{code}/contacts | 客户联系人 |
| GET | /projects | 项目列表 |
| GET | /projects/{code} | 项目详情（含团队、关联客户） |
| GET | /projects/create-form | 获取项目创建表单 schema |
| POST | /projects | 创建项目 |
| PATCH | /projects/{code} | 更新项目 |
| GET | /finance | 财务记录（高阶版以上） |
| GET | /finance/receivables | 应收款列表（全量返回，支持多维筛选） |
| GET | /finance/receivables/{id} | 应收款详情（含收款记录、案件/客户信息） |
| GET | /finance/receiverecord | 收款记录列表（全量返回，与 OA 逻辑一致） |
| GET | /finance/receiverecord/{id} | 收款记录详情 |
| PUT | /finance/receiverecord/{id} | 更新收款记录 |
| GET | /finance/summary | 财务摘要（支持按案件、日期范围筛选） |
| GET | /records/{id} | 记录详情（按ID直接查单条） |
| GET | /contracts | 合同列表（keyword 模糊搜客户/项目名称，client_keyword/project_keyword 精确按客户/项目搜索，管理员支持 follow_uid） |
| POST | /contracts | 创建合同（cl_id/pr_id 至少填一个） |
| PATCH | /contracts/{code} | 更新合同（按 code 标识） |

## 关键概念

### 日程与办案记录的关系

日程和办案记录是同一张表（`sr_record`）的不同视图。**所有创建和更新统一走 calendar 端点**：
- `POST /calendar` — 创建日程/待办/办案记录（唯一入口）
- `PUT /calendar/{id}` — 更新任何记录（状态、人员、时间、阶段等，统一入口）
- `GET /calendar` — 查看日程和记录列表（按日期范围，或按 type+linkid 查案件/项目/客户记录）
- `GET /records/{id}` — 按ID直接查单条记录详情

### 用户意图 → API 映射（创建记录类）

无论用户怎么描述，**创建任何记录都调 `POST /calendar`**：

| 用户说 | 推断 | 调用 |
|--------|------|------|
| "创建日程"、"安排一下" | 不关联日程 | `POST /calendar {type:0}` |
| "帮我记录：去法院阅卷" | 需关联案件的办案记录 | 先搜案件 → `POST /calendar {type:1,linkid:...}` |
| "记录一下跟华为的沟通" | 需关联客户的联系记录 | 先搜客户 → `POST /calendar {type:3,linkid:...}` |
| "给XX项目添加工作记录" | 需关联项目的工作记录 | 先搜项目 → `POST /calendar {type:2,linkid:...}` |
| "创建办案记录" | 问用户关联哪个案件 | 确认后 → `POST /calendar {type:1,linkid:...}` |

**关键规则**：只要提到具体案件/项目/客户名称，就必须搜索获取 ID 并传入 `linkid`+`type`。只有完全没提任何实体时才用 `type:0`。

### 日程关联（重要）

创建日程时**必须主动识别用户语境中的关联实体**，通过 `linkid`+`type` 建立关联。`type` 为必填字段。

**规则：只要用户提到具体的案件、项目或客户名称，就必须先搜索获取其 `id`，然后在创建日程时传入 `linkid` 和对应的 `type`。禁止在已识别到实体的情况下传 `type:0`。**

| type | 含义 | linkid 来源 |
|------|------|-------------|
| 0 | 不关联 | 无（仅在用户完全没提到任何实体时使用） |
| 1 | 案件 | `GET /cases` 返回的 `id`（hashid 字符串） |
| 2 | 项目 | `GET /projects` 返回的 `id`（hashid 字符串） |
| 3 | 客户 | `GET /clients` 返回的 `id`（hashid 字符串） |

识别优先级：案件(1) > 项目(2) > 客户(3)。`linkid` 直接使用实体返回的 `id` 字段值（hashid 字符串，如 `"J3GGbB3j"`），不要转成 int。

**示例**：用户说"江西建工案明天开庭"→ 搜索案件 → `POST /calendar '{"title":"开庭","htime":"...","endtime":"...","type":1,"linkid":"B31ewk3n"}'`

### 重名案件消歧（重要）

当 `GET /cases?keyword=X` 命中 **≥2 条**时，**必须先列出候选让用户确认选择**，取定后再 `POST /calendar` 或继续后续操作，禁止凭猜测直接关联。命中 1 条可直接进行（仍展示一句确认）。

**展示格式**（利用响应中的 `org_name` 字段消歧，仅顶层律所 owner 的响应才含此字段）：

- **owner（响应含 `org_name`）**：`序号. [团队名] 案件名（案号 anhao）`
- **普通用户（响应无 `org_name`）**：`序号. 案件名（案号 anhao）`

| 场景 | 命中数 | 处理 |
|------|--------|------|
| owner 搜"张三诉李四"命中 2 条分属不同子团队 | ≥2 | 列「1. [华东团队] 张三 诉 李四（（2026）京01民初123号）」「2. [华南团队] 张三 诉 李四（（2026）粤03民终456号）」→ 用户选 1 或 2 → 再创建 |
| 普通用户搜"张三"命中 2 条（同 org） | ≥2 | 列「1. 张三 诉 李四（...）」「2. 张三 诉 王五（...）」→ 用户选择 |
| 任意用户搜"江西建工"命中 1 条 | 1 | 直接进行，展示一句确认即可 |

> **关键**：仅当响应项含 `org_name` 时才展示团队名前缀；普通用户响应没有该字段，按原行为（案件名/案号）消歧即可。

### time_cost vs htime/endtime

- **`htime`/`endtime`** = 日程起止时间（什么时候开会）
- **`time_cost`** = 实际工时（分钟），用于统计。"花费了2.5小时"→ `time_cost=150`，不是改 endtime

### 日程查询时间范围

始终用 `start_date`/`end_date`（YYYY-MM-DD），**禁用** `today`/`this_week`（服务端不准）。默认查本周。

### 财务查询指南

应收款和收款记录接口返回**全量数据**（不分页），必须通过参数筛选来限定范围：

**按时间筛选**：使用 `yd_time_range`（约定收款日期）或 `ss_time_range`（实收日期），值为 JSON `{"start":"YYYY-MM-DD","end":"YYYY-MM-DD"}`，最长跨度 1 年。

**常用筛选参数**：

| 参数 | 说明 | 适用端点 |
|------|------|---------|
| `receivable_status` | 应收款状态: 1=全部未收回, 2=部分收回, 3=全部收回 | receivables |
| `record_status` | 收款记录状态: 1=待收款, 2=已收款 | receiverecord |
| `overdue_status` | 过期: 1=未过期, 2=已过期 | receiverecord |
| `link_keyword` | 关联资源名称搜索（案件/项目/客户） | receivables, receiverecord |
| `linktype` | 关联类型: 1=案件, 2=项目, 3=客户 | receivables, receiverecord |
| `title` | 款项名称搜索 | receivables, receiverecord |
| `amount_ys` | 应收金额范围 | receivables, receiverecord |
| `amount_ss` | 实收金额范围 | receivables, receiverecord |
| `sk_uid` | 收款人 | receivables |
| `uid` | 收款人 | receiverecord |

> **禁止使用** `year`、`status`（在 receiverecord 中无效）等不存在的参数。日期筛选**必须**用 `yd_time_range`/`ss_time_range`/`kp_date`，不接受 `start_date`/`end_date`（那是 summary 接口的参数）。

### 团队日程

`is_team=1` 查看团队日程（需团队版以上），`uids` 用 `/team/members` 返回的 hashid。展示用 `htime_text`/`huser_text`/`type_text` 等后端预处理好字段。

### 创建流程（客户/项目）

创建客户或项目前，**必须先调 `create-form` 端点**获取完整表单 schema（含枚举选项、级联树、自定义字段等）。流程：

1. AI 调用 `GET /clients/create-form` 或 `GET /projects/create-form` 获取表单 schema
2. AI 根据 schema 将用户描述映射为正确的枚举值和分类 ID
3. AI 展示确认信息（人类可读格式），等待用户确认
4. 用户确认后，AI 调用 `POST /clients` 或 `POST /projects` 创建
5. 创建成功后返回实体编号（客户返回 `code`/`c_num`，项目返回 `pr_code`/`p_num`）

**关键**：schema 中的枚举选项和级联树由后端动态返回，AI 必须依据 schema 中的值进行映射，不能凭猜测。

### 创建流程（案件）

创建案件走**直接 POST + enums 引导**范式（**不走 create-form 两步流程**）。流程：

1. AI 调用 `GET /enums` 获取枚举字典（取 `case_type` 案件类型、`case_unit_type` 受理单位类型等）
2. AI 收集用户输入：`type`（案件类型 1-5）+ `privyc_data`（当事人，至少一个含 name）+ 其他可选字段
3. AI 按枚举值把人类可读描述（如"民事案件"）映射为数字（如 1），把当事人原被告关系映射为 `type`(1=原告方/委托方、2=被告方/对方)
4. AI 展示人类可读的确认信息（案件类型、当事人列表、案由、审理程序等），等待用户确认
5. 用户确认后，AI 调用 `POST /cases` 创建
6. 创建成功后返回 `{ case_code, c_num, id, case_name }`

**必填**：`type`（1-5 整数）+ `privyc_data`（JSON 字符串，至少一个对象含非空 name）。

**自动生成（客户端不要传）**：`case_code`、`c_num`（留空按组织序号生成）、案件名（未传 `case_name` 时按"原告名 诉 被告名"拼接，识别不出原被告用"类型+日期"兜底）、主办律师（自动写入 related_worker = PAT 调用者）。

**关键**：当事人原被告关系决定自动生成的案件名拼接，尽量引导用户指明谁是原告/委托方（type=1）、谁是被告/对方（type=2）。

### 合同查询指南

合同列表接口返回**全量数据**（不分页），与客户/项目关联。

**数据权限**：
- **普通员工**：只能看到自己跟进的客户或项目关联的合同
- **管理员**：可看到组织下所有合同，支持 `follow_uid` 按跟进人筛选

**筛选参数**：

| 参数 | 说明 |
|------|------|
| `keyword` | 模糊搜索（同时匹配客户名称和项目名称），不确定是客户还是项目时使用 |
| `client_keyword` | 精确按关联客户名称搜索，用户明确提到"客户"时使用 |
| `project_keyword` | 精确按关联项目名称搜索，用户明确提到"项目"时使用 |
| `follow_uid` | 指定跟进人筛选（hashid，仅管理员可用） |

**合同状态**：1=未执行, 2=履行中, 3=已终止

**合同字段说明**：

| 字段 | 说明 |
|------|------|
| title | 合同名称 |
| amount | 合同金额（元） |
| sign_at / sign_at_text | 起始日期 |
| end_time / end_time_text | 终止日期 |
| cp_content | 合作内容 |
| status / status_text | 合作状态（1=未执行/2=履行中/3=已终止） |
| client | 关联客户（id/code/name） |
| project | 关联项目（id/pr_code/name） |
| part_a / part_b | 签约甲方/乙方 |

**新增/更新合同**：`cl_id` 和 `pr_id` 至少填一个（均为 hashid 或数字 ID），其他字段（title/amount/sign_at/end_time/status/cp_content 等）可选。

**识别用户筛选意图**（根据用户描述中的实体类型选择正确的搜索参数）：

| 用户说 | 识别的搜索对象 | 调用 |
|--------|---------------|------|
| "我的合同" / "查看合同" | 无筛选 | `GET /contracts` |
| "华为的合同" | 不确定是客户还是项目 | `GET "/contracts?keyword=华为"` |
| "客户华为的合同" | 明确是客户 | `GET "/contracts?client_keyword=华为"` |
| "XX项目的合同" | 明确是项目 | `GET "/contracts?project_keyword=XX"` |
| "张三跟进的合同" | 跟进人张三 | 先 `GET /team/members` 找张三 UID → `GET "/contracts?follow_uid=xxx"` |
| "华为的合同" | 不确定客户/项目 | `GET "/contracts?keyword=华为"` |
| "客户华为的合同" | 明确客户 | `GET "/contracts?client_keyword=华为"` |
| "XX项目的合同" | 明确项目 | `GET "/contracts?project_keyword=XX"` |
| "华为的建筑工程项目合同" | 客户+项目 | `GET "/contracts?client_keyword=华为&project_keyword=建筑工程"` |
| "履行中的合同" | 按状态 | `GET /contracts` 后按 `status=2` 过滤展示 |
| "金额大于10万的合同" | 按金额 | `GET /contracts` 后按 `amount` 过滤展示 |

**关键字无结果时的降级策略（仅管理员）**：当使用 `keyword` 模糊搜索（即用户未明确指定是客户/项目/跟进人）返回空数据时，如果当前用户是管理员，可以尝试按跟进人搜索：先 `GET /team/members` 查找姓名匹配的成员 UID，再用 `GET "/contracts?follow_uid=xxx"` 查询。如果用户已经明确指定了"客户"、"项目"或"跟进人"，则不走此降级流程，直接告知用户未找到结果。

### 案件附件管理

AI Agent 可以为案件上传文件、查看附件列表、获取文件访问链接。

**上传文件**：使用 `POST /cases/{code}/files`，发送 `multipart/form-data`，包含 `file` 字段（文件本身）。可选参数：
- `record_id`（hashid）— 关联到指定日程/办案记录，文件在日程详情中可见

**文件限制**：
- 允许的文件类型: `jpg,jpeg,bmp,png,rar,zip,7z,doc,docx,rtf,txt,xls,xlsx,pdf,mp3,m4a,ppt,pptx,eml,csv`
- 文件大小: 最大 10MB
- 文件名: 最大 128 字符
- 每日上传: 基础版 10 个/天，其他版本 100 个/天
- 超出限制时会提示"请到 OA 网页端上传"

**识别用户意图**：

| 用户说 | 推断意图 | 调用 |
|--------|----------|------|
| "上传文件到XX案" | 上传附件 | 先 `GET /cases?keyword=XX` → `POST /cases/{code}/files` |
| "给这条记录上传文件" | 关联日程上传 | 先获取 record_id → `POST /cases/{code}/files`（带 `record_id`） |
| "把文件附加到今天的日程" | 日程关联文件 | 先 `GET /calendar` 获取 record_id → `POST /cases/{code}/files`（带 `record_id`） |
| "查看案件附件" | 文件列表 | 先 `GET /cases?keyword=XX` → `GET /cases/{code}/files` |
| "下载文件" / "预览文件" | 获取文件链接 | `GET /cases/{code}/files/{fileId}/url` |

**关联日程的流程**：用户说"把XX文件附加到今天的日程"时，需先通过日程获取 `record_id`，再上传文件并传入 `record_id`。注意日程必须已关联案件（`type:1`），这样才能确定 `case_code`。

## 高危操作

- **PATCH /cases/{code}** 中变更 `process_code`（审理程序变更影响流程）、`current_stage_id`（切换当前阶段）、`unit_name`+`unit_type`（变更受理单位）→ 均需先向用户确认
- **POST /cases** 创建案件属写操作 → 创建前必须向用户展示案件名、当事人、类型等人类可读信息并确认

## 不支持的操作

当前 Open API **不支持删除类操作**（删除案件、删除日程、删除客户、删除项目等），也没有对应端点。当用户提出删除需求，或请求的业务场景没有相应的 API 端点时，直接回复：

> 该操作暂不支持在 AI 助手中完成，请在 OA 网页端或 APP 中进行相应操作。

不要尝试调用不存在的端点，也不要模拟删除行为。

## 使用示例

| 用户说 | 推断意图 | 脚本调用 |
|--------|----------|----------|
| "查询我的案件" | 案件列表 | `GET /cases` |
| "张三案件进度" | 搜索案件 | `GET "/cases?keyword=张三"` |
| "在办案件" | 筛选状态 | `GET "/cases?g_status=1"` |
| "创建案件：张三诉李四，民事借款纠纷" | 创建案件 | `GET /enums` → 收集 type/当事人 → 确认 → `POST /cases '{"type":1,"privyc_data":"[{\"name\":\"张三\",\"type\":1},{\"name\":\"李四\",\"type\":2}]","anyou":"借款纠纷"}'` |
| "新建一个民事案件，原告王五，被告赵六" | 创建案件（原被告） | `GET /enums` → 确认 → `POST /cases '{"type":1,"privyc_data":"[{\"name\":\"王五\",\"type\":1},{\"name\":\"赵六\",\"type\":2}]"}'` |
| "登记一个刑事案件" | 创建案件（仅一方） | `GET /enums` → 收集当事人 → 确认 → `POST /cases '{"type":4,"privyc_data":"[{\"name\":\"某某\",\"type\":1}]"}'` |
| "案件ABC123详情" | 案件详情 | `GET /cases/ABC123` |
| "把案件ABC123的受理单位改成海淀法院" | 更新受理单位 | `PATCH /cases/ABC123 '{"unit_name":"海淀法院","unit_type":1}'`（unit_name+unit_type 须同时传） |
| "给案件ABC123加一个阶段：质证" | 新增当前阶段 | `PATCH /cases/ABC123 '{"stage_text":"质证"}'` |
| "帮我记录：去法院阅卷" | 添加办案记录 | `POST /calendar '{title,htime,endtime,type:1,linkid:case_id}'` |
| "今天有什么安排" | 今日日程 | `GET "/calendar?start_date=今天&end_date=今天"` |
| "创建明天下午2点的日程" | 创建日程 | `POST /calendar '{title,htime,endtime,type:0}'` |
| "明天约小康米开会" | 关联客户日程 | 先 `GET "/clients?keyword=小康米"` → `POST /calendar '{...,linkid:id,type:3}'` |
| "明天和同事一起开庭" | 带协办人日程 | 先 `GET /team/members` 获取 UID → `POST /calendar '{...,assit:"uid1,uid2"}'` |
| "把这件事派给张三负责" / "让张三主办明天的开庭" | owner 派活（指定主办） | 先 `GET /team/members` 取张三 UID → `POST /calendar '{...,huser:"张三uid"}'`（owner 专属，详见「主办人指派规则」） |
| "张三主办、李四协办这个待办" | owner 派活（主办+协办） | 先 `GET /team/members` 取 UID → `POST /calendar '{...,huser:"张三uid",assit:"李四uid"}'` |
| "帮小米案加开庭日程" | 关联案件日程 | 先 `GET "/cases?keyword=小米"` → `POST /calendar '{...,linkid:id,type:1}'` |
| "记录一下跟华为的沟通" | 客户联系记录 | 先 `GET "/clients?keyword=华为"` → `POST /calendar '{title:"与华为沟通",...,type:3,linkid:client_id}'` |
| "给XX项目添加工作记录" | 项目工作记录 | 先 `GET "/projects?keyword=XX"` → `POST /calendar '{...,type:2,linkid:project_id}'` |
| "日程花费了2.5小时" | 记录工时 | `PUT /calendar/{id} '{"time_cost":150}'` |
| "把记录标记为已办" | 更新记录 | `PUT /calendar/{id} '{"hstatus":1}'` |
| "更新客户类型为签约" | 更新客户 | `PATCH /clients/{code} '{"type":1}'` |
| "帮我创建客户张三，个人，电话138xxxx" | 创建客户 | `GET /clients/create-form` → 确认 → `POST /clients '{name,mark,contact,...}'` |
| "创建一个单位客户华为" | 创建客户 | `GET /clients/create-form` → 确认 → `POST /clients '{name:"华为",mark:1,...}'` |
| "新建一个项目xxx，合同纠纷，预算5万" | 创建项目 | `GET /projects/create-form` → 确认 → `POST /projects '{pr_name,pr_type,pr_status,funding,...}'` |
| "团队日程" | 团队视图 | `GET "/calendar?is_team=1&start_date=...&end_date=..."` |
| "查询今年应收款" | 应收款列表（按日期） | `GET "/finance/receivables?ss_time_range={\"start\":\"2026-01-01\",\"end\":\"2026-12-31\"}"` |
| "未收回的应收款" | 筛选未收回 | `GET "/finance/receivables?receivable_status=1"` |
| "XX案件的应收款" | 按案件名称搜 | `GET "/finance/receivables?link_keyword=XX"` |
| "应收款汇总" | 财务摘要 | `GET /finance/summary` |
| "今年收款情况" | 摘要按日期 | `GET "/finance/summary?start_date=2026-01-01&end_date=2026-12-31"` |
| "收款记录" | 收款记录列表 | `GET /finance/receiverecord` |
| "待收款记录" | 筛选待收款 | `GET "/finance/receiverecord?record_status=1"` |
| "已逾期的收款" | 筛选已过期 | `GET "/finance/receiverecord?overdue_status=2"` |
| "案件云" | 每日概览 | `GET /dashboard` |
| "查看合同" / "我的合同" | 合同列表 | `GET /contracts` |
| "华为的合同" | 不确定是客户/项目/跟进人 | `GET "/contracts?keyword=华为"` |
| "客户华为的合同" | 按客户名搜 | `GET "/contracts?client_keyword=华为"` |
| "XX项目的合同" | 按项目名搜 | `GET "/contracts?project_keyword=XX"` |
| "张三跟进的合同" | 按跟进人筛 | 先 `GET /team/members` 找张三 UID → `GET "/contracts?follow_uid=xxx"` |
| "新增合同：法律服务合同，客户华为" | 创建合同 | 先 `GET "/clients?keyword=华为"` → `POST /contracts '{"title":"法律服务合同","cl_id":"xxx"}'` |
| "更新合同状态为已终止" | 更新合同 | `PATCH /contracts/{code} '{"status":3}'` |
| "查看案件附件" | 案件文件列表 | `GET /cases/{code}/files` |
| "上传文件到XX案" | 上传附件 | 先搜索案件 → `POST /cases/{code}/files` (multipart) |
| "把文件附加到这条记录" | 关联日程上传 | 获取 record_id → `POST /cases/{code}/files`（带 record_id） |
| "下载文件" / "预览文件" | 获取文件链接 | `GET /cases/{code}/files/{fileId}/url` |
