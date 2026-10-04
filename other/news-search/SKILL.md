---
name: news-search
description: 新闻搜索与获取技能，支持多数据源（Google News RSS、NewsAPI、中文新闻源）的关键词搜索、分类浏览、时间过滤。触发词：新闻搜索、news search、获取新闻、搜索新闻、今日新闻。
---

# News Search Skill

新闻搜索与获取技能，支持多个免费/付费数据源，提供关键词搜索、分类浏览、时间范围过滤等功能。

## 功能特性

- **多数据源支持**
  - Google News RSS（免费，无需 API Key）
  - NewsAPI（免费版 100 请求/天）
  - 中文新闻源（新浪、网易、腾讯 RSS）
  
- **搜索能力**
  - 关键词搜索
  - 分类浏览（科技/财经/体育/娱乐等）
  - 时间范围过滤（24h/7天/30天）
  - 语言过滤（中文/英文）

- **智能处理**
  - 新闻摘要提取
  - 缓存机制减少重复请求
  - 结果去重

## 使用方式

```bash
# 搜索新闻
news-search search "人工智能" --lang zh --days 7

# 按分类获取
news-search category tech --lang en

# 获取头条
news-search headlines --country cn
```

## 工具调用示例

```python
# 在对话中使用
search_news("苹果公司", lang="zh", days=7)
get_headlines(category="tech", country="us")
```

## 数据源配置

### 免费数据源（无需配置）

- **Google News RSS** - 默认启用
- **新浪新闻 RSS** - 默认启用
- **网易新闻 RSS** - 默认启用

### 需要 API Key 的数据源

在 `~/.openclaw/keys/news-search.json` 配置：

```json
{
  "newsapi": "YOUR_NEWSAPI_KEY",
  "tavily": "YOUR_TAVILY_KEY"
}
```

## 依赖

```
feedparser>=6.0.0
httpx>=0.25.0
beautifulsoup4>=4.12
newspaper3k>=0.2.8
```

## 安装

```bash
pip install feedparser httpx beautifulsoup4 newspaper3k
```

## 集成建议

- 与 `stock-analysis` 配合：搜索股票相关新闻
- 与 `akshare` 配合：获取财经新闻影响分析
- 与 `teach-cofounder` 配合：解释新闻背景知识
## Activation Keywords

- `news-search`
- `news-search`
- `news search`

## Tools Used

- `exec`
- `read`
- `write`
- `edit`

## Instructions for Agents

1. Read the task description carefully
2. Follow the step-by-step process
3. Use the appropriate tools
4. Verify the results

## Examples

### Example 1: Basic Usage

**User:** <example user request>

**Agent:** <example agent response>

### Example 2: Advanced Usage

**User:** <example user request>

**Agent:** <example agent response>
