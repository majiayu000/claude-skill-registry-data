---
name: signallayer-backlinks-client
description: 使用 SignalLayer.io 的真实 OpenClaw API 创建、查询和分页管理外链 Campaign。适用于用户要求配置 SignalLayer API Key、查询积分、创建外链任务、查看任务状态或列出 Campaign；客户端未指定数量时默认 200，但服务端 linkCount 始终必填。
---

# SignalLayer Backlinks Client

## 安全规则

1. 优先从 `SIGNALLAYER_API_KEY` 环境变量读取 Key。
2. 不在回复、日志或 Campaign 历史中回显完整 Key。
3. 仅在用户明确选择兼容模式时，才保存到 `memory/signallayer-api-user.md`；提醒这是明文文件且不得提交 Git。
4. 配置后必须调用 `GET /credits` 真实验证。仅检查 `sl_` 前缀不算验证成功。

## API 契约

Base URL：`https://signallayer.io/api/openclaw`

| 操作 | 方法与路径 |
|------|------------|
| 查询积分 / 验证 Key | `GET /credits` |
| 创建 | `POST /create-campaign` |
| 查询单个任务 | `GET /campaign-status/{id}` |
| 查询任务列表 | `GET /campaigns?limit=20&offset=0` |

认证 Header：`Authorization: Bearer <USER_API_KEY>`。

## 创建流程

1. 获取 API Key 并调用 `/credits`。
2. 从用户请求提取参数：
   - `targetUrl`：必填。
   - `brandName`：API 必填；用户未提供时，可从目标 hostname 生成候选值并明确告知用户。
   - `linkCount`：API 必填；用户未指定时客户端使用 200。
   - `keywords`：可选，默认空字符串。
   - `strategy`：`safety`（默认）、`neutral`、`aggressive`。
   - `speed`：`natural`（默认）、`standard`、`drip`。
   - `dripDays`：`drip` 时为 10–30，默认 14。
3. 调用：

```http
POST https://signallayer.io/api/openclaw/create-campaign
Authorization: Bearer <USER_API_KEY>
Content-Type: application/json

{
  "targetUrl": "https://example.com",
  "brandName": "Example",
  "keywords": "seo,marketing",
  "linkCount": 200,
  "strategy": "safety",
  "speed": "natural",
  "dripDays": 14,
  "source": "openclaw-skill"
}
```

4. 创建成功必须按 HTTP 201 和 `success: true` 判断。Campaign ID 位于 `campaign.id`。
5. 只记录非敏感 Campaign 元数据。

## 状态与列表

状态响应的进度位于：

```json
{
  "campaign": {
    "progress": {
      "total": 200,
      "completed": 85,
      "pending": 115,
      "percent": 43
    }
  }
}
```

不要读取不存在的顶层 `completed`、`total`、`campaign_id`、`updatedAt` 或预计完成时间。

列表接口默认返回 20 条，`limit` 最大为 100。它是 Campaign 分页数量，与每个 Campaign 的外链数量无关。

## 计费与速度

- 当前计费：`1 条外链 = 1 积分`。
- `aggressive` 不按 1.5 倍扣积分。
- API 不支持 `instant`，不得发送或向用户推荐该值。
- `natural`/`standard` 进入正常 Agent 队列；`drip` 生成 10–30 天的日期排期。
- API 不返回 SLA 或预计完成日期，不要自行承诺。

## 错误处理

读取 HTTP 状态和 JSON 中的 `code`、`error`、可选 `field`：

- 400：参数或 Campaign ID 格式错误。
- 401：Key 缺失或无效。
- 402：积分不足。
- 404：任务不存在或不属于当前 Key。
- 500：服务端创建、列表或状态查询失败。

遇到 HTML 响应时，优先检查是否误用了 `api.signallayer.io/v1` 或 `/campaigns/{id}` 等旧路径。

## 独立客户端

优先使用仓库脚本，避免手写漂移的请求：

```bash
python scripts/signallayer_client.py --credits
python scripts/signallayer_client.py --target "https://example.com" --brand "Example"
python scripts/signallayer_client.py --status "campaign_uuid"
python scripts/signallayer_client.py --list
```

完整契约见 `references/api.md`，排查流程见 `OPERATION-GUIDE.md`。
