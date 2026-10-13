---
name: tavily-search-zh
description: "通过 Tavily API 进行网页搜索（Brave 的替代方案）。当用户要求搜索网页、查找资料、获取链接，且 Brave web_search 不可用或不适合时使用。返回少量相关结果（标题、链接、摘要），可选附带简短回答摘要。"
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "emoji": "🔍",
      },
  }
---

# Tavily 网页搜索

使用内置脚本通过 Tavily 进行网页搜索。

## 前置要求

- 通过以下任一方式提供 API 密钥：
  - 环境变量：`TAVILY_API_KEY`
  - 在 `~/.openclaw/.env` 文件中添加一行：`TAVILY_API_KEY=...`

### 获取 Tavily API 密钥

1. 访问 [Tavily 官网](https://tavily.com) 注册账号
2. 在控制台获取 API 密钥（免费套餐无需信用卡）

## 使用命令

从 OpenClaw 工作目录运行：

```bash
# 原始 JSON 格式（默认）
python3 ~/.openclaw/skills/tavily-search-zh/scripts/tavily_search.py --query "..." --max-results 5

# 包含简短回答摘要（如有）
python3 ~/.openclaw/skills/tavily-search-zh/scripts/tavily_search.py --query "..." --max-results 5 --include-answer

# 稳定结构（接近 web_search 格式）：{query, results:[{title,url,snippet}], answer?}
python3 ~/.openclaw/skills/tavily-search-zh/scripts/tavily_search.py --query "..." --max-results 5 --format brave

# 人类可读的 Markdown 列表
python3 ~/.openclaw/skills/tavily-search-zh/scripts/tavily_search.py --query "..." --max-results 5 --format md
```

## 输出格式

### raw（默认）
- JSON：`query`、可选 `answer`、`results: [{title,url,content}]`

### brave
- JSON：`query`、可选 `answer`、`results: [{title,url,snippet}]`

### md
- 紧凑的 Markdown 列表，包含标题/链接/摘要。

## 使用说明

- 默认将 `max-results` 保持较小值（3–5），以减少 token 消耗和阅读负担。
- 优先返回链接和摘要；仅在需要时再抓取完整页面。
- 支持 `--search-depth basic`（默认）和 `--search-depth advanced` 两种搜索深度。

## 为什么选择 Tavily？

OpenClaw 内置的 `web_search` 工具依赖 Brave Search API，申请需要信用卡。Tavily 提供**免费套餐**，注册即可使用，**无需信用卡**。

## 手动测试

```bash
python3 ~/.openclaw/skills/tavily-search-zh/scripts/tavily_search.py --query "今天的科技新闻" --max-results 3 --format md
```
