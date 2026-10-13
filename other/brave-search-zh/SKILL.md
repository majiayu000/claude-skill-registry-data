---
name: brave-search-zh
description: 通过 Brave Search API 进行网页搜索和内容提取。用于搜索文档、事实或任何网页内容。轻量级，无需浏览器。
---

# Brave 搜索

使用 Brave Search 进行无头网页搜索和内容提取。无需浏览器。

## 设置

首次使用前运行：

```bash
cd ~/Projects/agent-scripts/skills/brave-search-zh
npm ci
```

需要环境变量：`BRAVE_API_KEY`。

## 搜索

```bash
./search.js "查询词"                    # 基础搜索（5 条结果）
./search.js "查询词" -n 10              # 更多结果
./search.js "查询词" --content          # 包含页面内容（Markdown 格式）
./search.js "查询词" -n 3 --content     # 组合使用
```

## 提取页面内容

```bash
./content.js https://example.com/article
```

获取 URL 并以 Markdown 格式提取可读内容。

## 输出格式

```
--- 结果 1 ---
标题: 页面标题
链接: https://example.com/page
摘要: 搜索结果中的描述
内容: （如果使用了 --content 标志）
  从页面提取的 Markdown 内容...

--- 结果 2 ---
...
```

## 使用场景

- 搜索文档或 API 参考
- 查找事实或当前信息
- 从特定 URL 获取内容
- 任何需要网页搜索但无需交互式浏览的任务
