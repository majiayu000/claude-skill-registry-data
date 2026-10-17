---
name: api-design
description: "REST API 设计模式，包括资源命名、状态码、分页、过滤、错误响应、版本管理以及针对生产环境 API 的速率限制。"
origin: ECC
---

# API 设计模式 (API Design Patterns)

设计一致且开发者友好的 REST API 的约定与最佳实践。

## 何时激活

- 设计新的 API 端点
- 评审现有的 API 契约
- 添加分页、过滤或排序功能
- 为 API 实现错误处理
- 规划 API 版本管理策略
- 构建面向公众或合作伙伴的 API

## 资源设计 (Resource Design)

### URL 结构

```
# 资源应为名词、复数、小写、中划线命名 (kebab-case)
GET    /api/v1/users
GET    /api/v1/users/:id
POST   /api/v1/users
PUT    /api/v1/users/:id
PATCH  /api/v1/users/:id
DELETE /api/v1/users/:id

# 用于表示关系的子资源
GET    /api/v1/users/:id/orders
POST   /api/v1/users/:id/orders

# 无法映射到 CRUD 的操作（谨慎使用动词）
POST   /api/v1/orders/:id/cancel
POST   /api/v1/auth/login
POST   /api/v1/auth/refresh
```

### 命名规则

```
# 建议做法 (GOOD)
/api/v1/team-members          # 多单词资源使用中划线命名
/api/v1/orders?status=active  # 使用查询参数进行过滤
/api/v1/users/123/orders      # 使用嵌套资源表示归属关系

# 错误做法 (BAD)
/api/v1/getUsers              # URL 中包含动词
/api/v1/user                  # 使用单数（应使用复数）
/api/v1/team_members          # URL 中使用下划线命名 (snake_case)
/api/v1/users/123/getOrders   # 嵌套资源中包含动词
```

## HTTP 方法与状态码

### 方法语义

| 方法 | 幂等性 | 安全性 | 用途 |
|--------|-----------|------|---------|
| GET | 是 | 是 | 获取资源 |
| POST | 否 | 否 | 创建资源，触发操作 |
| PUT | 是 | 否 | 完整替换资源 |
| PATCH | 否* | 否 | 部分更新资源 |
| DELETE | 是 | 否 | 删除资源 |

*通过合理的实现，PATCH 也可以做到幂等。

### 状态码参考

```
# 成功 (Success)
200 OK                    — GET, PUT, PATCH（包含响应体）
201 Created               — POST（应包含 Location 响应头）
204 No Content            — DELETE, PUT（无响应体）

# 客户端错误 (Client Errors)
400 Bad Request           — 验证失败，JSON 格式错误
401 Unauthorized          — 缺失或无效的身份认证
403 Forbidden             — 已登录但无权访问
404 Not Found             — 资源不存在
409 Conflict              — 重复条目，状态冲突
422 Unprocessable Entity  — 语义错误（JSON 合法但数据无效）
429 Too Many Requests     — 超过速率限制

# 服务器错误 (Server Errors)
500 Internal Server Error — 意外错误（绝不能泄露详细堆栈）
502 Bad Gateway           — 上游服务失败
503 Service Unavailable   — 临时过载，应包含 Retry-After
```

### 常见错误

```
# 错误做法：所有响应都返回 200
{ "status": 200, "success": false, "error": "Not found" }

# 建议做法：按语义使用 HTTP 状态码
HTTP/1.1 404 Not Found
{ "error": { "code": "not_found", "message": "用户不存在" } }

# 错误做法：针对验证错误返回 500
# 建议做法：返回 400 或 422，并包含具体的字段级错误详情

# 错误做法：针对已创建的资源返回 200
# 建议做法：返回 201 并附带 Location 响应头
HTTP/1.1 201 Created
Location: /api/v1/users/abc-123
```

## 响应格式

### 成功响应

```json
{
  "data": {
    "id": "abc-123",
    "email": "alice@example.com",
    "name": "Alice",
    "created_at": "2025-01-15T10:30:00Z"
  }
}
```

### 集合响应（带分页）

```json
{
  "data": [
    { "id": "abc-123", "name": "Alice" },
    { "id": "def-456", "name": "Bob" }
  ],
  "meta": {
    "total": 142,
    "page": 1,
    "per_page": 20,
    "total_pages": 8
  },
  "links": {
    "self": "/api/v1/users?page=1&per_page=20",
    "next": "/api/v1/users?page=2&per_page=20",
    "last": "/api/v1/users?page=8&per_page=20"
  }
}
```

### 错误响应

```json
{
  "error": {
    "code": "validation_error",
    "message": "请求验证失败",
    "details": [
      {
        "field": "email",
        "message": "必须是有效的电子邮件地址",
        "code": "invalid_format"
      },
      {
        "field": "age",
        "message": "必须介于 0 到 150 之间",
        "code": "out_of_range"
      }
    ]
  }
}
```

### 响应封装变体

```typescript
// 选项 A：使用 data 外层封装（推荐用于公众 API）
interface ApiResponse<T> {
  data: T;
  meta?: PaginationMeta;
  links?: PaginationLinks;
}

interface ApiError {
  error: {
    code: string;
    message: string;
    details?: FieldError[];
  };
}

// 选项 B：扁平化响应（更简单，常用于内部 API）
// 成功：直接返回资源对象
// 错误：返回错误对象
// 通过 HTTP 状态码进行区分
```

## 分页 (Pagination)

### 基于偏移量 (Offset-Based) —— 简单

```
GET /api/v1/users?page=2&per_page=20

# 实现参考
SELECT * FROM users
ORDER BY created_at DESC
LIMIT 20 OFFSET 20;
```

**优点**：实现简单，支持“跳转到第 N 页”。
**缺点**：大偏移量下性能差 (OFFSET 100000)，在有并发插入时结果不一致。

### 基于游标 (Cursor-Based) —— 可扩展

```
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=20

# 实现参考
SELECT * FROM users
WHERE id > :cursor_id
ORDER BY id ASC
LIMIT 21;  -- 多取一个以判断是否有下一页 (has_next)
```

```json
{
  "data": [...],
  "meta": {
    "has_next": true,
    "next_cursor": "eyJpZCI6MTQzfQ"
  }
}
```

**优点**：无论位置多深性能都保持一致，在有并发插入时依然稳定。
**缺点**：无法跳转到任意页，游标内容是不透明的。

### 如何选择分页方式

| 使用场景 | 分页类型 |
|----------|----------------|
| 管理后台、小数据集 (<10K) | 偏移量 (Offset) |
| 无限滚动、Feed 流、大数据集 | 游标 (Cursor) |
| 公众 API | 游标 (默认) 配合 偏移量 (可选) |
| 搜索结果 | 偏移量 (用户期望看到页码) |

## 过滤、排序与搜索

### 过滤 (Filtering)

```
# 简单相等
GET /api/v1/orders?status=active&customer_id=abc-123

# 比较操作符（使用括号标记法）
GET /api/v1/products?price[gte]=10&price[lte]=100
GET /api/v1/orders?created_at[after]=2025-01-01

# 多值过滤（逗号分隔）
GET /api/v1/products?category=electronics,clothing

# 嵌套字段（点号标记法）
GET /api/v1/orders?customer.country=US
```

### 排序 (Sorting)

```
# 单个字段（前缀 - 表示降序）
GET /api/v1/products?sort=-created_at

# 多个字段（逗号分隔）
GET /api/v1/products?sort=-featured,price,-created_at
```

### 全文搜索

```
# 搜索查询参数
GET /api/v1/products?q=wireless+headphones

# 特定字段搜索
GET /api/v1/users?email=alice
```

### 稀疏字段集 (Sparse Fieldsets)

```
# 仅返回指定字段（减小传输负载）
GET /api/v1/users?fields=id,name,email
GET /api/v1/orders?fields=id,total,status&include=customer.name
```

## 身份认证与授权

### 基于令牌的认证

```
# Authorization 响应头中的 Bearer 令牌
GET /api/v1/users
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...

# API 密钥（用于服务间调用）
GET /api/v1/data
X-API-Key: sk_live_abc123
```

### 授权模式 (Authorization Patterns)

```typescript
// 资源级：检查归属权
app.get("/api/v1/orders/:id", async (req, res) => {
  const order = await Order.findById(req.params.id);
  if (!order) return res.status(404).json({ error: { code: "not_found" } });
  if (order.userId !== req.user.id) return res.status(403).json({ error: { code: "forbidden" } });
  return res.json({ data: order });
});

// 角色级：检查权限
app.delete("/api/v1/users/:id", requireRole("admin"), async (req, res) => {
  await User.delete(req.params.id);
  return res.status(204).send();
});
```

## 速率限制 (Rate Limiting)

### 响应头

```
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000

# 超过限制时
HTTP/1.1 429 Too Many Requests
Retry-After: 60
{
  "error": {
    "code": "rate_limit_exceeded",
    "message": "已超过速率限制。请在 60 秒后重试。"
  }
}
```

### 速率限制分级

| 等级 | 限制 | 窗口 | 使用场景 |
|------|-------|--------|----------|
| 匿名用户 | 30/min | 按 IP | 公共端点 |
| 已登录用户 | 100/min | 按用户 | 标准 API 访问 |
| 高级用户 | 1000/min | 按 API 密钥 | 付费 API 套餐 |
| 内部服务 | 10000/min | 按服务 | 服务间调用 |

## 版本管理 (Versioning)

### URL 路径版本（推荐）

```
/api/v1/users
/api/v2/users
```

**优点**：显式、易于路由、可缓存。
**缺点**：版本升级时 URL 会变。

### 响应头版本

```
GET /api/users
Accept: application/vnd.myapp.v2+json
```

**优点**：URL 保持整洁。
**缺点**：测试较难，容易遗忘。

### 版本管理策略

```
1. 以 /api/v1/ 开始 —— 在确实需要之前不要进行版本升级。
2. 最多维护 2 个活跃版本（当前版本 + 上一个版本）。
3. 弃用时间线：
   - 公布弃用计划（公众 API 建议提前 6 个月通知）
   - 添加 Sunset 响应头：Sunset: Sat, 01 Jan 2026 00:00:00 GMT
   - 在 Sunset 日期之后返回 410 Gone
4. 非破坏性变更不需要新版本：
   - 在响应中添加新字段
   - 添加新的可选查询参数
   - 添加新的端点
5. 破坏性变更必须使用新版本：
   - 移除或重命名字段
   - 更改字段类型
   - 更改 URL 结构
   - 更改认证方式
```

## 实现模式示例

### TypeScript (Next.js API 路由)

```typescript
import { z } from "zod";
import { NextRequest, NextResponse } from "next/server";

const createUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
});

export async function POST(req: NextRequest) {
  const body = await req.json();
  const parsed = createUserSchema.safeParse(body);

  if (!parsed.success) {
    return NextResponse.json({
      error: {
        code: "validation_error",
        message: "请求验证失败",
        details: parsed.error.issues.map(i => ({
          field: i.path.join("."),
          message: i.message,
          code: i.code,
        })),
      },
    }, { status: 422 });
  }

  const user = await createUser(parsed.data);

  return NextResponse.json(
    { data: user },
    {
      status: 201,
      headers: { Location: `/api/v1/users/${user.id}` },
    },
  );
}
```

### Python (Django REST Framework)

```python
from rest_framework import serializers, viewsets, status
from rest_framework.response import Response

class CreateUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length=100)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name", "created_at"]

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateUserSerializer
        return UserSerializer

    def create(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserService.create(**serializer.validated_data)
        return Response(
            {"data": UserSerializer(user).data},
            status=status.HTTP_201_CREATED,
            headers={"Location": f"/api/v1/users/{user.id}"},
        )
```

### Go (net/http)

```go
func (h *UserHandler) CreateUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest
    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        writeError(w, http.StatusBadRequest, "invalid_json", "无效的请求体")
        return
    }

    if err := req.Validate(); err != nil {
        writeError(w, http.StatusUnprocessableEntity, "validation_error", err.Error())
        return
    }

    user, err := h.service.Create(r.Context(), req)
    if err != nil {
        switch {
        case errors.Is(err, domain.ErrEmailTaken):
            writeError(w, http.StatusConflict, "email_taken", "该电子邮件已被注册")
        default:
            writeError(w, http.StatusInternalServerError, "internal_error", "内部错误")
        }
        return
    }

    w.Header().Set("Location", fmt.Sprintf("/api/v1/users/%s", user.ID))
    writeJSON(w, http.StatusCreated, map[string]any{"data": user})
}
```

## API 设计检查清单

在发布新端点之前：

- [ ] 资源 URL 遵循命名规范（复数、中划线命名、无动词）
- [ ] 使用了正确的 HTTP 方法（读操作用 GET，创建用 POST 等）
- [ ] 返回了恰当的状态码（不要所有响应都返回 200）
- [ ] 输入数据通过了模式 (Schema) 验证 (Zod, Pydantic, Bean Validation 等)
- [ ] 错误响应遵循包含代码 (Code) 和消息 (Message) 的标准格式
- [ ] 列表端点实现了分页（游标或偏移量）
- [ ] 需要身份认证（或已明确标记为公共端点）
- [ ] 检查了授权逻辑（用户只能访问自己的资源）
- [ ] 配置了速率限制
- [ ] 响应中未泄露内部细节（如堆栈跟踪、SQL 错误）
- [ ] 命名与现有端点保持一致（全驼峰 camelCase 或 下划线 snake_case）
- [ ] 已编写文档（更新了 OpenAPI/Swagger 规范）
