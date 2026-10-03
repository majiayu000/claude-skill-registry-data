---
name: api-design
description: 基于需求与设计文档生成可实施的 API 设计文档（接口契约、关键代码设计、错误码定义、请求/响应示例）。触发："设计 API"、"接口设计"、"api design"，或 design-craft 之后补充 API 设计细节。
---

# API Design（API 接口设计）

## 概述

**目的**：将设计文档中的 demo 级 API 示例升级为详细的、可实施的 API 设计文档

**功能**：基于需求文档和设计文档，生成包含完整接口契约、关键代码设计、错误码定义、请求/响应示例的 API 设计文档

**使用场景**：
- design-craft 完成设计文档后，作为后续步骤补充 API 设计细节
- 需要从 demo 级别升级为可实施的 API 设计时
- 用户明确要求"设计 API"、"写 API 文档"、"接口设计"时

## 定位

```
requirement-mining → design-craft → api-design（本 skill）
     理解需求           技术设计          API 详细设计
```

- **输入**：需求文档 + 设计文档（含 demo 接口参考）
- **输出**：API 设计文档（详细接口契约 + 关键代码设计）
- **边界**：只设计接口契约和关键代码骨架，不写完整实现代码

## 核心原则

1. **契约优先**：先定义接口契约（方法、路径、参数、返回值），再设计关键代码
2. **独立设计**：设计文档中的 demo 接口只是展示流程用的最简示意，便于理解设计意图。实际 API 设计时，必须基于当前的数据结构、业务场景、使用需求和约束条件，独立重新设计。demo 示例可能正确，也可能不完整或不匹配实际场景——重点是「经过独立判断后再决定是否采纳」，而非直接套用
3. **关键代码**：只写影响接口行为的关键代码（校验逻辑、状态转换、核心算法），不写样板代码
4. **错误完备**：每个接口必须定义完整的错误码和错误响应
5. **示例真实**：请求/响应示例必须是真实可用的，不能是占位符

## 工作流总览

```
阶段 1：输入收集           → 读取设计文档，提取 demo 接口和需求上下文
阶段 2：接口清单确认       → 识别所有需要设计的 API 接口
阶段 3：接口契约设计       → 为每个接口定义完整契约
阶段 4：关键代码设计       → 设计影响接口行为的关键代码
阶段 5：错误码与异常定义   → 定义统一的错误码体系
阶段 6：落盘输出           → 生成 API 设计文档
```

**未得到用户对当前阶段的确认前，不进入下一阶段。**

---

## 阶段 1：输入收集

### 1.1 读取设计文档

检查并读取以下输入：

1. **设计文档**（必需）：
   - 检查 `.requirements/config` 获取 `storage_path`
   - 读取 `{storage_path}/{feature}/design/DESIGN.md`（父文档）
   - 读取 `{storage_path}/{feature}/design/S*.md`（子文档）
   - 提取所有 demo 接口示例和接口设计章节

2. **需求文档**（可选）：
   - 读取 `{storage_path}/{feature}/requirement.md`
   - 提取验收标准和非功能性约束

3. **依赖文档**（可选）：
   - 检查 `{storage_path}/{feature}/dependencies/` 目录
   - 读取第三方 API 文档作为参考

### 1.2 提取 demo 接口

从设计文档中提取所有 demo 接口示例：

> ⚠️ **重要提醒**：设计文档中的 demo 接口仅作为理解设计意图的参考，是最简示意。这些 demo 可能缺少字段、参数不完整、错误处理缺失、数据结构与实际场景不匹配。**真正的 API 设计必须基于需求文档中的业务场景、数据流图中的数据结构、以及实际使用约束独立重新设计，不可直接照搬 demo。**

```text
📥 输入收集
━━━━━━━━━━━━━━━━

【设计文档】
- 父文档：<路径>
- 子文档：<路径列表>

【demo 接口提取】
| 来源 | 接口路径 | 方法 | demo 状态 |
|------|----------|------|-----------|
| S-01 | /api/users | POST | 仅有响应示例 |
| S-02 | /api/orders/{id} | GET | 有请求+响应 |

【需求上下文】
- 功能描述：<摘要>
- 验收标准：<关键点>

请确认输入信息是否完整。
```

---

## 阶段 2：接口清单确认

基于设计文档的接口设计章节，列出所有需要详细设计的 API 接口。

### 2.1 接口识别规则

- 设计文档中标记为"新增"或"修改"的接口
- 设计文档中 demo 示例涉及的接口
- 需求文档中验收标准涉及的接口

### 2.2 输出格式

```text
📋 API 接口清单
━━━━━━━━━━━━━━━━

| 编号 | 方法 | 路径 | 所属子需求 | 优先级 | demo 状态 |
|------|------|------|-----------|--------|-----------|
| API-01 | POST | /api/v1/users | S-01 用户模块 | P0 | 需补充 |
| API-02 | GET | /api/v1/users/{id} | S-01 用户模块 | P0 | 已有 demo |
| API-03 | PUT | /api/v1/users/{id} | S-01 用户模块 | P1 | 需补充 |

【接口分组】
- 用户模块（S-01）：API-01, API-02, API-03
- 订单模块（S-02）：API-04, API-05

请确认接口清单是否完整、优先级是否合理。
```

---

## 阶段 3：接口契约设计

为每个 API 接口定义完整契约。

### 3.1 契约模板

每个接口必须包含以下信息：

```text
## API-XX：{接口名称}

### 基本信息

| 项目 | 值 |
|------|-----|
| 方法 | GET/POST/PUT/DELETE/PATCH |
| 路径 | /api/v1/{resource} |
| 认证 | Bearer Token / API Key / 无 |
| 权限 | {required_role} |
| 限流 | {rate_limit} |
| 幂等 | 是/否 |

### 请求参数

#### Path Parameters

| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| id | string | 是 | 资源唯一标识 | usr_abc123 |

#### Query Parameters

| 参数 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|------|------|------|--------|------|------|
| page | integer | 否 | 1 | 页码 | 1 |
| limit | integer | 否 | 20 | 每页数量 | 20 |

#### Request Body

```typescript
interface CreateUserRequest {
  name: string;          // 用户名，2-50 字符
  email: string;         // 邮箱，唯一
  role?: "admin" | "user";  // 角色，默认 user
}
```

### 响应

#### 成功响应（200/201）

```typescript
interface CreateUserResponse {
  code: 200;
  data: {
    id: string;          // 用户 ID
    name: string;
    email: string;
    role: string;
    created_at: string;  // ISO 8601
  };
  message: "success";
}
```

#### 错误响应

| HTTP Status | 错误码 | 说明 | 触发条件 |
|-------------|--------|------|----------|
| 400 | INVALID_INPUT | 输入参数无效 | name 为空或超长 |
| 409 | EMAIL_EXISTS | 邮箱已存在 | email 唯一约束冲突 |
| 401 | UNAUTHORIZED | 未认证 | Token 无效或过期 |
| 403 | FORBIDDEN | 无权限 | 角色不满足 |

### Demo 请求示例

```bash
curl -X POST https://api.example.com/api/v1/users \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "张三",
    "email": "zhangsan@example.com",
    "role": "user"
  }'
```

### Demo 响应示例

```json
{
  "code": 200,
  "data": {
    "id": "usr_abc123",
    "name": "张三",
    "email": "zhangsan@example.com",
    "role": "user",
    "created_at": "2026-06-22T10:30:00Z"
  },
  "message": "success"
}
```
```

### 3.2 契约设计规则

1. **RESTful 规范**：
   - GET：查询，无 Request Body
   - POST：创建，返回 201
   - PUT：全量更新
   - PATCH：部分更新
   - DELETE：删除，返回 204 或 200

2. **版本控制**：路径中包含版本号 `/api/v1/`

3. **命名规范**：
   - 路径：小写、连字符分隔 `/api/v1/user-profiles`
   - 参数：snake_case
   - JSON 字段：snake_case

4. **分页规范**：
   - 请求：`page` + `limit` 或 `cursor` + `limit`
   - 响应：`total` + `items[]`

### 3.3 输出格式

```text
📝 接口契约设计
━━━━━━━━━━━━━━━━

【API-01：创建用户】
（完整契约内容）

【API-02：查询用户】
（完整契约内容）

请确认接口契约是否完整、参数定义是否准确。
```

---

## 阶段 4：关键代码设计

设计影响接口行为的关键代码，不写样板代码。

### 4.1 关键代码范围

| 代码类型 | 是否需要设计 | 说明 |
|----------|:------------:|------|
| 参数校验逻辑 | ✅ | 复杂校验规则、跨字段校验 |
| 状态转换逻辑 | ✅ | 状态机、状态流转约束 |
| 核心算法 | ✅ | 业务计算、排序、过滤逻辑 |
| 权限校验 | ✅ | 角色检查、资源权限 |
| 数据库 CRUD | ❌ | 标准增删改查 |
| 框架配置 | ❌ | 路由注册、中间件配置 |
| 日志记录 | ❌ | 标准日志 |

### 4.2 关键代码模板

```text
## API-01 关键代码设计

### 参数校验

```python
def validate_create_user(request: CreateUserRequest) -> None:
    # 名称长度校验
    if not (2 <= len(request.name) <= 50):
        raise InvalidInputError("name", "长度必须在 2-50 之间")
    
    # 邮箱格式校验
    if not EMAIL_REGEX.match(request.email):
        raise InvalidInputError("email", "邮箱格式无效")
    
    # 角色枚举校验
    if request.role and request.role not in ("admin", "user"):
        raise InvalidInputError("role", "角色必须是 admin 或 user")
```

### 业务逻辑

```python
async def create_user(request: CreateUserRequest) -> User:
    # 检查邮箱唯一性
    existing = await user_repo.find_by_email(request.email)
    if existing:
        raise ConflictError("EMAIL_EXISTS", "邮箱已存在")
    
    # 创建用户
    user = User(
        id=generate_id("usr"),
        name=request.name,
        email=request.email,
        role=request.role or "user",
        created_at=utc_now()
    )
    
    await user_repo.save(user)
    return user
```

### 权限校验

```python
def check_create_permission(current_user: User) -> None:
    if current_user.role not in ("admin",):
        raise ForbiddenError("只有管理员可以创建用户")
```
```

### 4.3 输出格式

```text
💻 关键代码设计
━━━━━━━━━━━━━━━━

【API-01：创建用户】
- 参数校验：<代码>
- 业务逻辑：<代码>
- 权限校验：<代码>

【API-02：查询用户】
- 参数校验：<代码>
- 业务逻辑：<代码>

请确认关键代码逻辑是否准确。
```

---

## 阶段 5：错误码与异常定义

### 5.1 错误码体系

定义统一的错误码格式和分类：

```text
## 错误码规范

### 格式

{MODULE}_{ERROR_TYPE}

示例：USER_NOT_FOUND, ORDER_ALREADY_PAID

### 分类

| HTTP Status | 错误类型 | 说明 | 示例 |
|-------------|----------|------|------|
| 400 | INVALID_INPUT | 输入参数无效 | 参数缺失、格式错误、范围越界 |
| 401 | UNAUTHORIZED | 未认证 | Token 缺失、Token 过期 |
| 403 | FORBIDDEN | 无权限 | 角色不足、资源无权限 |
| 404 | NOT_FOUND | 资源不存在 | ID 不存在 |
| 409 | CONFLICT | 冲突 | 唯一约束冲突、状态冲突 |
| 422 | UNPROCESSABLE | 语义错误 | 业务规则不满足 |
| 429 | RATE_LIMITED | 限流 | 请求过于频繁 |
| 500 | INTERNAL_ERROR | 服务器内部错误 | 未捕获异常 |
```

### 5.2 错误响应格式

```typescript
interface ErrorResponse {
  code: number;           // HTTP Status
  error: string;          // 错误码，如 "USER_NOT_FOUND"
  message: string;        // 用户可读的错误描述
  details?: {             // 可选，字段级错误详情
    field: string;
    message: string;
  }[];
}
```

### 5.3 输出格式

```text
⚠️ 错误码定义
━━━━━━━━━━━━━━━━

【统一错误响应格式】
（格式定义）

【错误码清单】
| 错误码 | HTTP Status | 说明 | 触发条件 |
|--------|-------------|------|----------|
| USER_NOT_FOUND | 404 | 用户不存在 | ID 查询不到 |
| EMAIL_EXISTS | 409 | 邮箱已存在 | 创建时邮箱重复 |

【字段级错误】
| 字段 | 错误码 | 说明 |
|------|--------|------|
| name | INVALID_LENGTH | 长度不在 2-50 范围 |
| email | INVALID_FORMAT | 邮箱格式无效 |

请确认错误码体系是否完整。
```

---

## 阶段 6：落盘输出

### 6.1 文档结构

按模块拆分，每个接口模块一个独立 md 文档，外加一份索引文件汇总接口清单和错误码体系。

```
api/
├── INDEX.md              # API 总览：接口清单 + 错误码 + 通用约定
├── users.md              # 用户模块：API-01~03 契约 + 关键代码
├── orders.md             # 订单模块：API-04~05 契约 + 关键代码
```

**INDEX.md（索引枢纽）**：

```markdown
# API 总览：{功能名称}

> 版本：v1
> 状态：草案
> 基础路径：/api/v1

## 1. 概述
- 接口数量：X 个
- 认证方式：{Bearer Token / API Key / 无}
- 通用约定（分页、排序、过滤）

## 2. 接口清单
| 编号 | 方法 | 路径 | 模块 | 文档 | 优先级 |
|------|------|------|------|------|--------|
| API-01 | POST | /api/v1/users | 用户 | [users.md](users.md) | P0 |
| API-02 | GET | /api/v1/users/{id} | 用户 | [users.md](users.md) | P0 |
| API-03 | PUT | /api/v1/users/{id} | 用户 | [users.md](users.md) | P1 |
| API-04 | POST | /api/v1/orders | 订单 | [orders.md](orders.md) | P0 |

## 3. 错误码定义
（阶段 5 统一错误码体系）

## 4. 待确认事项
| 编号 | 事项 | 影响范围 | 状态 |
|------|------|----------|------|
```

**{module}.md（模块 API 文档）**：

```markdown
# {模块名称} API

> 所属需求：{REQ-NNN}
> 基础路径：/api/v1

## API-XX：{接口名称}

### 基本信息
| 项目 | 值 |
|------|-----|
| 方法 | GET/POST/PUT/DELETE/PATCH |
| 路径 | /api/v1/{resource} |
| 认证 | Bearer Token / API Key / 无 |
| 权限 | {required_role} |
| 限流 | {rate_limit} |
| 幂等 | 是/否 |

### 请求参数

#### Path Parameters
| 参数 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|

#### Query Parameters
| 参数 | 类型 | 必填 | 默认值 | 说明 | 示例 |
|------|------|------|--------|------|------|

#### Request Body
```typescript
interface XxxRequest { ... }
```

### 响应

#### 成功响应（200/201）
```typescript
interface XxxResponse { ... }
```

#### 错误响应
| HTTP Status | 错误码 | 说明 | 触发条件 |
|-------------|--------|------|----------|

### Demo 请求示例
```bash
curl ...
```

### Demo 响应示例
```json
{ ... }
```

### 关键代码设计
（阶段 4 内容：参数校验、业务逻辑、权限校验）
```

### 6.2 存储位置

检查项目中是否已配置存储位置（`.requirements/config`）：

- **已配置**：读取 `storage_path`，API 设计文档存放在 `{storage_path}/{feature}/api/` 目录下
  - `INDEX.md`：接口清单 + 错误码 + 通用约定
  - `{module}.md`：每个模块一个独立文件（如 `users.md`、`orders.md`）
- **未配置**：询问用户，给出默认建议 `.requirements/{feature}/api/`

### 6.3 质量自检

```text
✅ API 设计文档已生成

📄 <路径>

🔍 质量自检清单
━━━━━━━━━━━━━━━━

【契约完整性】
☐ 每个接口都有完整的方法、路径、认证、权限定义
☐ 每个接口都有完整的请求参数定义（Path/Query/Body）
☐ 每个接口都有完整的响应定义（成功+错误）
☐ 每个接口都有 Demo 请求和响应示例

【关键代码】
☐ 复杂参数校验逻辑已设计
☐ 状态转换逻辑已设计
☐ 核心业务算法已设计
☐ 权限校验逻辑已设计

【错误处理】
☐ 统一错误响应格式已定义
☐ 每个接口的主要错误码已列出
☐ 字段级错误详情已定义

【一致性】
☐ 接口命名符合 RESTful 规范
☐ 错误码格式统一
☐ 分页/排序/过滤规范一致

下一步建议：
- 是否需要将 API 设计文档传递给开发团队？
- 是否需要生成 API 测试计划？
```

### 6.4 后续行动

```text
🚀 后续行动选择
━━━━━━━━━━━━━━━━

API 设计已完成，文档已输出。请选择后续行动：

1. 📁 落盘归档
   将 API 设计文档保存到需求目录，注册到需求管理系统

2. 📖 生成前端集成指南
   使用 frontend-api-guide 技能为前端生成可直接编码的调用流程文档

3. 📋 生成测试计划
   使用 test-planner 技能基于 API 设计生成接口测试计划

4. ⏭️ 跳过
   不进行后续操作，结束 API 设计流程

请选择 [1/2/3/4]：
```

---

## 与 design-craft 的衔接

### 作为后续步骤推荐

design-craft 完成设计文档后，在"后续行动选择"中推荐：

```
2. 📡 补充 API 设计
   使用 api-design 技能将设计文档中的 demo 接口升级为详细的 API 设计文档
```

### 输入输出关系

| design-craft 产出 | api-design 使用方式 |
|-------------------|---------------------|
| 接口设计章节（含 demo） | 作为接口契约设计的基础，补充完整契约 |
| 数据模型章节 | 作为 Request/Response 结构的参考 |
| 异常处理章节 | 作为错误码定义的参考 |
| 时序图 | 作为关键代码设计的参考 |

---

## 反模式

- ❌ 跳过设计文档直接设计 API → 缺乏业务上下文，设计可能偏离需求
- ❌ 写完整实现代码 → 本 skill 只设计关键代码，实现留给开发
- ❌ **直接照搬 demo 示例** → 设计文档的 demo 仅是最简示意便于理解流程，实际设计需基于数据结构、业务场景、使用约束独立重新判断
- ❌ Demo 示例使用占位符 → 示例必须真实可用
- ❌ 遗漏错误响应定义 → 每个接口必须有完整错误码
- ❌ 不定义幂等性 → POST/PUT 接口必须明确是否幂等
- ❌ 跳过确认直接进入下一阶段 → 接口契约是开发的基础，必须确认
