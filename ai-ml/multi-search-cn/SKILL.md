---
slug: multi-search-cn
version: 1.1.3
name: "multi-search-cn"
displayName: 多引擎联网搜索（multi-search-cn）
summary: 多引擎联网搜索。集成 6 个国内搜索引擎，支持高级搜索语法、时间筛选、站内搜索。无需 API Key。
description: "多引擎联网搜索。集成 6 个国内搜索引擎，支持高级搜索语法、时间筛选、站内搜索。无需 API Key。"
tags: 搜索, search, 中国, china, 多引擎, web-fetch, 无API
---

# 多引擎联网搜索 v1.1.0

集成 6 个国内搜索引擎，通过 web_fetch 直接抓取搜索结果。无需 API Key。

## 搜索引擎（6 个）

| 优先级 | 引擎 | URL 模板 | 适用场景 | 可靠性 |
|--------|------|----------|---------|--------|
| 🥇 1 | **微信搜索** | `https://wx.sogou.com/weixin?type=2&query={keyword}` | 中文深度内容、热点、产品分析 | ⭐⭐⭐⭐⭐ |
| 🥈 2 | **搜狗** | `https://sogou.com/web?query={keyword}` | 中文通用搜索，覆盖面广 | ⭐⭐⭐⭐ |
| 🥉 3 | **360** | `https://www.so.com/s?q={keyword}` | 中文日常搜索，带 AI 摘要 | ⭐⭐⭐⭐ |
| 4 | **必应中文** | `https://cn.bing.com/search?q={keyword}&ensearch=0` | 新闻时事（不稳定，需交叉验证） | ⭐⭐⭐ |
| 5 | **必应国际** | `https://cn.bing.com/search?q={keyword}&ensearch=1` | 仅英文泛搜 | ⭐⭐½ |
| 6 | **头条搜索** | `https://so.toutiao.com/search?keyword={keyword}` | 新闻时事（需后处理，见下方） | ⭐⭐⭐ |

## Quick Examples

```javascript
// 微信公众号文章（首选）
web_fetch({"url": "https://wx.sogou.com/weixin?type=2&query=AI+Agent"})

// 搜狗通用搜索
web_fetch({"url": "https://sogou.com/web?query=特斯拉Model+Y价格"})

// 360 搜索（有 AI 摘要加成）
web_fetch({"url": "https://www.so.com/s?q=2026年两会重点"})

// 必应国际（英文内容）
web_fetch({"url": "https://cn.bing.com/search?q=machine+learning&ensearch=1"})
```

## 头条搜索后处理（重要！）

头条搜索的结果 URL 被包裹在深层 JS 跳转链接中，web_fetch 无法直接提取干净正文。使用头条搜索时，必须执行以下后处理：

### 提取规则

头条返回的链接格式为：
```
/search/jump?...&url=<URL_ENCODED_REAL_URL>&...
```

**步骤：**
1. 从结果中找到 `/search/jump?` 开头的链接
2. 提取 `url=` 参数的值
3. 对该值做 URL decode（可能需要多次 decode）
4. 得到的就是真实文章 URL（通常是 `toutiao.com/article/xxx` 或 `toutiao.com/group/xxx`）
5. 可选：用 `web_fetch` 抓取解码后的真实 URL 获取正文

### 标题提取

头条结果中的标题通常在 `[标题文字](/search/jump?...)` 格式的 markdown 链接中，可直接读取方括号内的文字。

### 示例

```
原始: /search/jump?...&url=https%3A%2F%2Ftoutiao.com%2Farticle%2F7592063983856452130%2F&...
解码: https://toutiao.com/article/7592063983856452130/
```

**如果不需要点击进入文章，只需要搜索结果摘要，可以直接从头条返回内容中提取标题和摘要片段，忽略 URL。**

## 高级搜索操作符

### ⚠️ 重要警告

经实测，**必应（无论中文还是国际模式）的 `site:` `filetype:` 等高级语法在 web_fetch 抓取时全部失效**。搜索结果会完全忽略这些操作符。不要依赖它们。

以下操作符理论上受支持，但实际效果不可靠：

| 操作符 | 示例 | 说明 | 实测状态 |
|--------|------|------|---------|
| `site:` | `site:github.com python` | 站内搜索 | ❌ 不生效 |
| `filetype:` | `filetype:pdf report` | 文件类型 | ❌ 不生效 |
| `""` | `"machine learning"` | 精确匹配 | ⚠️ 未充分测试 |
| `-` | `python -snake` | 排除关键词 | ⚠️ 未充分测试 |
| `OR` | `cat OR dog` | 或运算 | ⚠️ 未充分测试 |

**替代方案：** 如需站内搜索，直接在关键词中加入站名（如 `知乎 AI Agent 创业`），而不是用 `site:zhihu.com`。

## 时间筛选

### 必应时间参数

| 参数 | 说明 |
|------|------|
| `&filters=ex1:"ez1"` | 过去 24 小时 |
| `&filters=ex1:"ez2"` | 过去 1 周 |
| `&filters=ex1:"ez3"` | 过去 1 月 |

## 搜索策略

### 按场景选择引擎

| 场景 | 首选 | 备选 |
|------|------|------|
| 中文日常搜索 | 微信搜索 | 搜狗、360 |
| 中文热点/深度 | 微信搜索 | 搜狗 |
| 中文新闻时事 | 360 | 必应中文、头条搜索 |
| 英文/技术搜索 | 必应国际 | 搜狗 |
| 商品/价格查询 | 360 | 搜狗 |
| 微信公众号 | 微信搜索 | — |

### 引擎已知问题

| 引擎 | 问题 |
|------|------|
| **必应中文** | 极不稳定，部分查询会返回完全不相关的结果（如搜"苹果电脑"返回抖音下载、搜"A股半导体"返回字母 A 百科） |
| **必应国际** | 高级搜索语法（site:/filetype:）全部失效；中文关键词效果差 |
| **头条搜索** | 结果质量好但 URL 被 JS 跳转包裹，需按上方后处理规则提取 |

### 多引擎交叉验证

同一关键词建议用 2-3 个引擎搜索，对比结果：

```javascript
// 推荐组合：微信 + 搜狗 + 360
web_fetch({"url": "https://wx.sogou.com/weixin?type=2&query=AI+Agent+创业"})
web_fetch({"url": "https://sogou.com/web?query=AI+Agent+创业"})
web_fetch({"url": "https://www.so.com/s?q=AI+Agent+创业"})
```

## 文档

- `references/search-guide.md` — 各引擎深度搜索指南

## Changelog

- **v1.1.0** (2026-03-10): 基于 8 场景 × 7 引擎实测重构优先级；剔除集思录；新增头条后处理规则；标注必应高级语法失效
- **v1.0.0**: 初始版本

## License

MIT
