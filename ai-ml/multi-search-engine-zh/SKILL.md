---
name: "multi-search-engine"
description: "多搜索引擎集成，支持 17 个搜索引擎（8 个国内 + 9 个国际）。支持高级搜索操作符、时间筛选、站内搜索、隐私搜索引擎和 WolframAlpha 知识查询。无需 API 密钥。"
---

# 多搜索引擎 v2.0.1

集成 17 个搜索引擎，无需 API 密钥即可进行网页搜索。

## 搜索引擎列表

### 国内搜索引擎（8 个）
- **百度**: `https://www.baidu.com/s?wd={keyword}`
- **必应中国**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **必应国际**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **360搜索**: `https://www.so.com/s?q={keyword}`
- **搜狗**: `https://sogou.com/web?query={keyword}`
- **微信**: `https://wx.sogou.com/weixin?type=2&query={keyword}`
- **头条**: `https://so.toutiao.com/search?keyword={keyword}`
- **集思录**: `https://www.jisilu.cn/explore/?keyword={keyword}`

### 国际搜索引擎（9 个）
- **Google**: `https://www.google.com/search?q={keyword}`
- **Google 香港**: `https://www.google.com.hk/search?q={keyword}`
- **DuckDuckGo**: `https://duckduckgo.com/html/?q={keyword}`
- **Yahoo**: `https://search.yahoo.com/search?p={keyword}`
- **Startpage**: `https://www.startpage.com/sp/search?query={keyword}`
- **Brave**: `https://search.brave.com/search?q={keyword}`
- **Ecosia**: `https://www.ecosia.org/search?q={keyword}`
- **Qwant**: `https://www.qwant.com/?q={keyword}`
- **WolframAlpha**: `https://www.wolframalpha.com/input?i={keyword}`

## 快速示例

```javascript
// 基础搜索
web_fetch({"url": "https://www.google.com/search?q=python+tutorial"})

// 站内搜索
web_fetch({"url": "https://www.google.com/search?q=site:github.com+react"})

// 文件类型搜索
web_fetch({"url": "https://www.google.com/search?q=machine+learning+filetype:pdf"})

// 时间筛选（过去一周）
web_fetch({"url": "https://www.google.com/search?q=ai+news&tbs=qdr:w"})

// 隐私搜索
web_fetch({"url": "https://duckduckgo.com/html/?q=privacy+tools"})

// DuckDuckGo Bangs 快捷搜索
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+tensorflow"})

// 知识计算
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})
```

## 高级搜索操作符

| 操作符 | 示例 | 说明 |
|--------|------|------|
| `site:` | `site:github.com python` | 站内搜索 |
| `filetype:` | `filetype:pdf report` | 指定文件类型 |
| `""` | `"machine learning"` | 精确匹配 |
| `-` | `python -snake` | 排除关键词 |
| `OR` | `cat OR dog` | 或运算 |

## 时间筛选参数

| 参数 | 说明 |
|------|------|
| `tbs=qdr:h` | 过去1小时 |
| `tbs=qdr:d` | 过去24小时 |
| `tbs=qdr:w` | 过去1周 |
| `tbs=qdr:m` | 过去1月 |
| `tbs=qdr:y` | 过去1年 |

## 隐私搜索引擎

- **DuckDuckGo**: 不追踪用户
- **Startpage**: Google 结果 + 隐私保护
- **Brave**: 独立索引
- **Qwant**: 符合欧盟 GDPR 标准

## DuckDuckGo Bangs 快捷搜索

| Bang | 跳转目标 |
|------|---------|
| `!g` | Google |
| `!gh` | GitHub |
| `!so` | Stack Overflow |
| `!w` | Wikipedia |
| `!yt` | YouTube |

## WolframAlpha 知识查询

- 数学计算: `integrate x^2 dx`
- 单位换算: `100 USD to CNY`
- 股票数据: `AAPL stock`
- 天气查询: `weather in Beijing`

## 文档

- `references/advanced-search.md` - 国内搜索指南
- `references/international-search.md` - 国际搜索指南
- `CHANGELOG.md` - 版本历史

## 许可证

MIT
