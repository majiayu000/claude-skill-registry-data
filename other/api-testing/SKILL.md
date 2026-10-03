---
name: api-testing
description: 基于 httpflex-py 自主完成 HTTP API 测试：把自然语言接口描述解析为端点清单，生成测试客户端、构造并发送请求、对响应 data 做业务断言，产出结构化测试报告。触发："测试/验证这个 API"、"自动化接口测试"。
---

# API 自主测试（基于 httpflex-py）

## 概述

**目的**：把 Postman 的"人点鼠标"变成"AI 读规格、写用例、发请求、判结果"。让 AI 在没有人逐步操作的情况下，自主完成一组 API 的连通性与业务正确性验证。

**功能**：
- 将自然语言/文字描述的接口解析为结构化端点清单
- 基于 httpflex-py 的 `BaseClient` 生成测试客户端（参数映射、占位符、鉴权）
- 自动设计用例矩阵（正常 / 边界 / 错误 / 鉴权缺失）
- 对响应 `data` 做业务断言（字段、类型、值）
- 输出结构化测试报告

**使用场景**：
- 用户说"测试一下这个 API""帮我验证这几个接口""做个自动化接口测试"
- 用户用文字描述了接口（方法、路径、参数、期望返回），需要 AI 自己去跑
- 用户提供了 base_url + 若干端点说明，希望 AI 自主判断通过/失败

## 前置条件

- Python ≥ 3.11
- 安装 httpflex（**未上 PyPI**，需从 GitHub 安装，属第三方代码，执行前必须获得用户显式批准）：
  ```bash
  pip install "git+https://github.com/HACK-WU/httpflex.git"
  # 或附带可选依赖：...#egg=httpflex[all]
  ```
- 已掌握目标 API 的 `base_url` 与鉴权方式（无鉴权 / Bearer Token / Cookie / 自定义头）

> httpflex 的具体用法（cookie 加载、认证、重试、并发、缓存、钩子）见 [reference.md](reference.md)；完整端到端示例见 [examples.md](examples.md)。**优先复用 reference.md 中的代码模板，不要凭空猜测库 API。**

> ⚠️ **依赖与版本风险**：httpflex 当前为 `0.1.1-beta`，从 GitHub 安装且 API 仍可能变动。建议固定版本（如 `#egg=httpflex==0.1.1b0`）以避免后续破坏性更新；对生产/敏感接口先在非生产环境试跑。

## 工作流程（5 步）

```
[1] 解析描述 → [2] 生成客户端 → [3] 设计用例 → [4] 执行断言 → [5] 出报告
```

### 步骤 1：解析自然语言 API 描述

把用户的文字描述转成如下结构化清单（每个端点一条）。

**最小必需信息**（缺失任一必须先向用户确认，不得臆测）：
- `base_url`：API 根地址
- 鉴权方式：无 / Bearer / Cookie / 自定义头，以及凭证来源
- 至少一个端点的期望响应（用于业务断言的基准）

| 字段 | 说明 |
|------|------|
| `name` | 人类可读名称，如"获取用户详情" |
| `method` | GET / POST / PUT / PATCH / DELETE |
| `endpoint` | 路径模板，如 `/users/{user_id}`（占位符用 `{}`） |
| `path_params` | 占位符列表，如 `["user_id"]` |
| `params` | 查询/请求体参数字段：名称、类型、必填、示例值 |
| `auth` | `none` / `bearer` / `cookie` / `header:<Key>` |
| `expected` | 期望 `result` / `code` / `data` 的关键结构与取值（用于业务断言） |

### 步骤 2：生成测试客户端

为每组 base_url + 鉴权方式定义一个 `BaseClient` 子类（或复用同类）。最小骨架：

```python
from httpflex import BaseClient, JSONResponseParser

class UserAPIClient(BaseClient):
    base_url = "https://api.example.com"
    endpoint = "/users/{user_id}"
    method = "GET"
    response_parser_class = JSONResponseParser
```

带鉴权 / cookie / 自定义头 / 重试的写法，直接照搬 [reference.md](reference.md) 对应小节，**不要自行发明属性名**。

### 步骤 3：设计用例矩阵

对每个端点，至少覆盖下面 4 类用例（可合并进一张表）：

| 类别 | 目的 | 期望 |
|------|------|------|
| 正常路径 | 合法参数可正确返回 | `result=True`, `code` 为 2xx, `data` 含期望字段 |
| 边界值 | 空值 / 极值 / 超长 / 越界 ID | 依接口约定，通常为 2xx 或 4xx |
| 错误参数 | 缺必填 / 类型错 / 非法值 | `result=False`, `code` 为 4xx |
| 鉴权缺失 | 不带 token/cookie 调用受保护接口 | `result=False`, `code` 为 401/403 |

### 步骤 4：执行与业务断言

- 调用 `client.request(request_data)` 发请求；批量用 `client.request([...], is_async=True)`（结果顺序与输入一致）。
- 归一化响应结构：`{"result": bool, "code": int, "message": str, "data": any}`。失败时 `code` 见 reference.md 错误码表。
- **业务断言**（本技能核心深度）：不仅看 `code`，还要校验 `data`：
  - 存在性：`data` 非 `None` 且含期望字段
  - 类型：字段类型匹配（如 `int` / `str` / `list`）
  - 取值：关键字段值等于期望值（如 `data["id"] == 123`）；可用嵌套取值 `data["user"]["name"]`
  - 错误用例：断言 `result == False` 且 `code` 落在预期区间
- 单请求失败**不抛异常**（除非钩子中断），务必先判 `result` 再读 `data`，否则 `data` 可能是 `None`。
- **非 JSON 响应**：下载 / HTML 等接口改用 `StreamResponseParser` / `FileWriteResponseParser`（见 reference.md §11），不要假设 `data` 是字典。
- **网络 / 超时错误**：不可达主机返回 `code == -1`，按预期处理（如"应超时"用例判 `result==False and code==-1`）。
- **嵌套取值**：优先用 `data.get("user", {}).get("name")` 等防御式取值，避免 KeyError 使整段断言崩溃。

### 步骤 5：出报告

按下方模板输出，区分通过与失败，并给出失败根因（实际 `code` / `data` 与期望的差异）。

**根因超出接口层时转排错**：若失败原因无法从请求/响应本身判定（疑似服务端逻辑、环境配置、数据状态或依赖问题），调用 `use_skill("debug")` 定位根因——本 skill 负责**判定通过/失败**，不负责定位服务侧为什么失败，不凭响应差异猜测实现原因。

```markdown
# API 测试报告

## 概览
- 通过：X / 总 Y
- base_url：https://api.example.com
- 鉴权方式：bearer

## 明细
| 端点 | 用例 | 结果 | code | 说明 |
|------|------|------|------|------|
| GET /users/{id} | 正常路径 | ✅ PASS | 200 | data.id==123 |
| GET /users/{id} | 缺 token | ❌ FAIL | 200 | 期望 401，实际返回 200（鉴权未生效？）|
...

## 建议
- ...（如：该接口未校验鉴权 / 响应缺少约定字段）
```

## 常见陷阱

- **默认超时 30s**：慢接口会超时失败，按需调大 `default_timeout`。
- **凭证保密**：报告与日志中只展示 token/cookie 的占位或前缀（如 `Bearer eyJ…`），不要把完整凭证回显给用户或写入文件。
- **占位符会被消耗**：`endpoint` 中的 `{user_id}` 会从 `request_data` 取值并移除，不再进入 query/body。路径参数务必放进 `request_data`。
- **GET 参数为 query，POST/PUT/PATCH 为 JSON body**：同一份 `request_data` 字典按方法自动映射，不要手动拼 URL。
- **失败不抛异常**：默认 `request()` 返回结构字典；别直接 `result["data"]["x"]` 而不先判断 `result["result"]`。
- **Cookie 走请求头**：httpflex 无独立 cookie 属性，用 `default_headers={"Cookie": "session=xxx"}`（见 reference.md）。
- **缓存客户端无 `delete_cache()`**：清缓存用 `clear_cache()`。

## 更多资源

- httpflex 用法 demo/规范（cookie、鉴权、重试、并发、缓存、钩子、错误码）：[reference.md](reference.md)
- 完整端到端测试示例：[examples.md](examples.md)
