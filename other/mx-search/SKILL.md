---
name: mx_search
description: 妙想资讯搜索工具，基于东方财富妙想搜索能力，专为金融场景设计的信源智能筛选搜索。当用户需要查询任何涉及时效性或特定事件的金融信息时必须使用此技能，包括：个股/行业最新资讯、研报、机构观点、政策解读、板块热点、宏观经济分析、市场异动原因、北向资金流向、A股/港股/美股新闻、上市公司公告、基金动态、债券市场信息、汇率/大宗商品影响分析，以及任何需要检索外部权威金融数据的非常识问题。只要涉及"最新"、"近期"、"今日"、"为什么"（市场现象）、"影响"（金融事件）等时效性或事件性问题，都应优先触发此技能。
---

# 妙想资讯搜索 (mx_search)

根据用户问句搜索相关**金融资讯**，获取研报、新闻、公告、政策解读等内容，并返回可读的文本摘要。

## API 调用方式

**接口**：`POST https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search`

**认证**：从环境变量 `MX_APIKEY` 读取 apikey，若未设置则使用内置默认值。

**调用示例**：

```bash
APIKEY="${MX_APIKEY:-mkt_sTfL6dP0WE2-2nSTwPf47a-gDmo6D9o7hitjcWZuaiE}"

curl -s -X POST \
  'https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search' \
  --header 'Content-Type: application/json' \
  --header "apikey: ${APIKEY}" \
  --data "{\"query\": \"${QUERY}\"}"
```

也可以用 Python：

```python
import os, requests

apikey = os.environ.get("MX_APIKEY", "mkt_sTfL6dP0WE2-2nSTwPf47a-gDmo6D9o7hitjcWZuaiE")
resp = requests.post(
    "https://mkapi2.dfcfs.com/finskillshub/api/claw/news-search",
    headers={"Content-Type": "application/json", "apikey": apikey},
    json={"query": query}
)
data = resp.json()
```

## 问句构造原则

将用户问题直接作为 `query` 传入，保持自然语言形式，无需特殊处理。接口会自动进行金融语义理解和信源筛选。

**问句示例**：

| 类型 | 示例问句 |
|------|---------|
| 个股资讯 | 格力电器最新研报、贵州茅台机构观点 |
| 板块/主题 | 商业航天板块近期新闻、新能源政策解读 |
| 宏观/风险 | 美联储加息对A股影响、人民币汇率最新走势 |
| 综合解读 | 今日大盘异动原因、北向资金流向解读 |

## 返回字段说明

实际响应为嵌套结构，资讯列表位于 `data.data.llmSearchResponse.data[]`：

```python
result = resp.json()
items = result["data"]["data"]["llmSearchResponse"]["data"]
```

每条资讯的字段：

| 字段 | 含义 |
|------|------|
| `title` | 信息标题 |
| `content` | 正文内容 |
| `date` | 发布时间（如 `2026-03-16 21:16:00`） |
| `secuList` | 关联证券列表 |
| `secuList[].secuCode` | 证券代码（如 002475） |
| `secuList[].secuName` | 证券名称（如 立讯精密） |
| `secuList[].secuType` | 证券类型（股票 / 债券 等） |

## 输出规范

搜索完成后，将结果整理为清晰易读的中文摘要：

1. **列出主要资讯条目**：每条包含标题和核心内容摘要
2. **关联证券**：如返回了 secuList，列出相关证券代码和名称
3. **信息时效**：如有日期信息，注明资讯时间
4. **保存选项**：如用户希望保存，将完整内容写入工作目录的 `.md` 或 `.txt` 文件

如果 API 返回为空或报错，告知用户并建议调整问句或检查网络连接。
