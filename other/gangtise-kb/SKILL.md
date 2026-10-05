---
name: gangtise-kb
description: Query Gangtise knowledge base API to search and retrieve financial/market information. Use when the user asks about stocks, companies, market concepts, financial reports, or any content stored in the Gangtise knowledge base system.
---

# Gangtise Knowledge Base Skill

This skill provides access to Gangtise's knowledge base API for querying financial and market information.

## First Time Setup

Before using this skill, you need to configure your API credentials:

```bash
python3 scripts/configure.py
```

You will be prompted to enter your **Access Key** and **Secret Key**, which can be obtained from: https://open.gangtise.com

## Authentication

The API uses OAuth2-style authentication:
1. Use **Access Key** + **Secret Access Key** to get an access token via `loginV2`
2. V2 接口返回的 accessToken **已经携带了 Bearer 前缀**，后续接口调用不需要再拼接

### Auth Request
```json
{
  "accessKey": "your-access-key",
  "secretAccessKey": "your-secret-key"
}
```

### Auth Response
```json
{
  "code": "000000",
  "data": {
    "accessToken": "Bearer xxxx-xxxx-xxxx-xxxx",
    "expiresIn": 3600,
    "uid": 123,
    "userName": "your-name",
    "tenantId": 1,
    "time": 1704067200
  }
}
```

## Base URL

- Base URL: `https://open.gangtise.com`

## Available Scripts

### Configuration (First Time Setup)

```bash
python3 scripts/configure.py
```

Interactive setup for API credentials. Run this first before using any other scripts.

### Get Access Token

```bash
python3 scripts/get_token.py
```

Returns a valid access token for API calls.

### Query Knowledge Base

```bash
# Basic query
python3 scripts/query_kb.py "比亚迪最新消息"

# With options
python3 scripts/query_kb.py "特斯拉" --type 10,40 --top 5 --days 180

# With explicit token
python3 scripts/query_kb.py "宁德时代" --token YOUR_TOKEN
```

## API Endpoints

### Authentication
- **POST** `/application/auth/oauth/open/loginV2`
  - Body: `{ "accessKey": "...", "secretAccessKey": "..." }`
  - Returns: `{ "code": "000000", "data": { "accessToken": "..." } }`
  - **Note**: V2接口返回的accessToken已经携带了Bearer前缀

### Knowledge Base Query
- **POST** `/application/open-data/ai/search/knowledge/batch`
  - Header: `Authorization: Bearer {token}`
  - Content-Type: `application/json`

## Request Parameters

| 参数名 | 必选 | 类型 | 说明 |
|--------|------|------|------|
| queries | 是 | List<String> | 查询条件列表，最大支持5个查询条件 |
| top | 否 | Integer | 返回文档数量，默认10，最大支持20 |
| resourceTypes | 否 | List<Integer> | 知识库资源类型列表 |
| knowledgeNames | 否 | List<String> | 知识库类型（默认只使用系统库） |
| startTime | 否 | Long | 数据查询开始时间（13位时间戳） |
| endTime | 否 | Long | 数据查询结束时间（13位时间戳） |

## Resource Types

| 代码 | 类型 | 说明 |
|------|------|------|
| 10 | 券商研究报告 | 证券公司发布的研究报告 |
| 20 | 内部研究报告 | 机构内部研究报告 |
| 40 | 首席分析师观点 | 分析师观点文章 |
| 50 | 公司公告 | 上市公司公告 |
| 60 | 会议平台纪要 | 会议纪要 |
| 70 | 调研纪要公告 | 调研纪要 |
| 80 | 网络资源纪要 | 网络资源 |
| 90 | 产业公众号 | 产业相关公众号文章 |

## Knowledge Names

- `system_knowledge_doc` - 系统库（默认）
- `tenant_knowledge_doc` - 租户库

## Response Format

```json
{
  "code": "000000",
  "msg": "操作成功",
  "status": true,
  "data": [
    {
      "query": "查询问题",
      "data": [
        {
          "content": "文本切片内容",
          "resourceType": 10,
          "title": "文件标题",
          "company": "公司",
          "industry": "行业",
          "time": 1746506803000,
          "sourceId": "溯源id",
          "knowledgeName": "知识库名称",
          "extraInfo": {
            "position": {
              "page": [1],
              "totalPages": 14,
              "polygon": []
            }
          }
        }
      ]
    }
  ]
}
```

## HTTP Status Codes

| 状态码 | 说明 |
|--------|------|
| 200 | 操作成功 |
| 429 | 接口繁忙，请稍后再试 |

## Usage Examples

### Query single topic
```bash
python3 scripts/query_kb.py "比亚迪" --top 3
```

### Query with specific resource types
```bash
python3 scripts/query_kb.py "新能源" --type 10,50 --top 5
```

### Query with time range (last 30 days)
```bash
python3 scripts/query_kb.py "AI芯片" --days 30 --top 10
```

### Raw JSON output
```bash
python3 scripts/query_kb.py "宁德时代" --json
```

## Configuration File

Credentials are stored in `config.json` (created automatically by `configure.py`):

```json
{
  "ACCESS_KEY": "your-access-key",
  "SECRET_KEY": "your-secret-key",
  "BASE_URL": "https://open.gangtise.com"
}
```

**Note**: The configuration file has restricted permissions (600) to protect your credentials.
