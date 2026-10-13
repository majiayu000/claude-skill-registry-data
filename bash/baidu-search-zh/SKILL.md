---
name: baidu-search-zh
description: 使用百度 AI 搜索引擎进行网页搜索。适用于实时信息查询、文档检索或研究主题。
metadata: { "openclaw": { "emoji": "🔍︎",  "requires": { "bins": ["python3"], "env":["BAIDU_API_KEY"]},"primaryEnv":"BAIDU_API_KEY" } }
---

# 百度搜索

通过百度 AI 搜索 API 进行网页搜索。

## 前置条件

### API 密钥配置
本技能需要配置 **BAIDU_API_KEY** 环境变量。

如果您还没有 API 密钥，请访问：
**https://console.bce.baidu.com/ai-search/qianfan/ais/console/apiKey**

详细的配置步骤请参阅：
[references/apikey-fetch.md](references/apikey-fetch.md)

## 使用方法

```bash
python3 skills/baidu-search-zh/scripts/search.py '<JSON>'
```

## 请求参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|-------|------|----------|---------|-------------|
| query | str | 是 | - | 搜索关键词 |
| count | int | 否 | 10 | 返回结果数量，范围 1-50 |
| freshness | str | 否 | 无 | 时间范围，两种格式：格式一为 "YYYY-MM-DDtoYYYY-MM-DD"；格式二包括 pd、pw、pm、py，分别代表过去 24 小时、过去 7 天、过去 31 天和过去 365 天 |

## 示例

```bash
# 基础搜索
python3 scripts/search.py '{"query":"人工智能"}'

# 时间范围格式一 "YYYY-MM-DDtoYYYY-MM-DD" 示例
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"2025-09-01to2025-09-08"
}'

# 时间范围格式二 pd、pw、pm、py 示例
python3 scripts/search.py '{
  "query":"最新新闻",
  "freshness":"pd"
}'

# 设置 count 参数，指定返回结果数量
python3 scripts/search.py '{
  "query":"旅游景点",
  "count": 20
}'
```

## 当前状态

功能完全正常。
