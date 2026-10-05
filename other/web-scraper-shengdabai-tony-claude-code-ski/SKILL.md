---
name: web-scraper
description: >
  智能三级降级网页内容提取。当用户发送 URL 链接并要求提取/阅读/总结网页内容时自动触发。
  触发场景：用户发送任何 http/https URL 并期望获取其内容（非 GitHub PR/Issue，非搜索请求）。
  例如："读取这篇文章"、"帮我看看这个链接"、"总结这个网页"、直接发 URL。
metadata:
  author: adam
  version: "1.0.0"
  source: https://juejin.cn/post/7615250753897955391
---

# web-scraper — 智能三级降级网页提取

基于石臻说AI的《OpenClaw 永久免费的提取任何网页的终极方案》，实现三工具智能切换策略。

## 核心原则

三个工具不是竞争关系，是互补关系。通过智能降级覆盖 99% 的内容提取场景。

## 路由决策表

根据 URL 域名和场景，选择最优工具：

| 优先级 | 工具 | 适用场景 | 限制 |
|--------|------|---------|------|
| **1** | **Jina Reader**（via WebFetch） | 英文博客、Substack、Medium、技术文档 | 200次/天，20 RPM |
| **2** | **curl_cffi 脚本** | Jina 失败、微信公众号、反爬平台、中文站点 | 无限制 |
| **3** | **WebFetch 直连** | 静态页面、GitHub README、简单文档 | 全页噪音多 |
| **4** | **CDP 浏览器**（/browse 或 web-access） | 需登录态、极端反爬、JS 渲染页面 | 最慢 |

## 域名直接路由（跳过降级，直达最优）

以下域名已知最优路径，**直接使用对应工具，不走降级链**：

```
mp.weixin.qq.com     → 直接用 curl_cffi 脚本（Jina 403，WebFetch 验证拦截）
weixin.qq.com        → 直接用 curl_cffi 脚本
xhslink.com          → 直接用 CDP 浏览器（web-access skill）
xiaohongshu.com      → 直接用 CDP 浏览器（web-access skill）
weibo.com            → 直接用 CDP 浏览器（web-access skill）
```

## 执行流程

### Step 1: 分析 URL

判断域名，检查是否命中直接路由表。命中则跳到对应工具，否则进入降级链。

### Step 2: Jina Reader（首选）

```
WebFetch(url="https://r.jina.ai/{去掉 http(s):// 的原始URL}", prompt="完整提取文章内容...")
```

- URL 格式：`r.jina.ai/` + 原始域名路径（**不保留 http:// 前缀**）
- 返回干净 Markdown，自动去除导航、广告、侧边栏
- Token 节省 60-70%
- 如果返回 403、空内容、或明显不是正文 → 进入 Step 3

### Step 3: curl_cffi 脚本（反爬杀手）

```bash
~/.miniforge3/bin/python3 ~/.claude/skills/web-scraper/scripts/scrape.py "URL" 30000
```

- 使用 curl_cffi 浏览器指纹模拟，绕过大部分反爬
- html2text 转 Markdown，保留链接和图片
- 自动选择最佳内容区域（article > main > .rich_media_content > body）
- 无次数限制，无需 API Key
- 如果返回 ERROR 或内容过少 → 进入 Step 4

### Step 4: WebFetch 直连（兜底）

```
WebFetch(url="原始URL", prompt="提取文章正文内容...")
```

- 返回全页内容（含噪音），由小模型提取
- 仅适合简单静态页面
- 如果仍然失败 → 进入 Step 5

### Step 5: CDP 浏览器（最终手段）

触发 web-access skill 的 CDP 模式，使用真实浏览器访问。

## 关键参数

- **maxChars / max_chars**: 统一设为 `30000`，保证完整正文同时避免 context 溢出
- **Jina**: prompt 中明确要求"提取正文内容"而非"分析页面"

## 陷阱警告

1. **不要用 get_all_text()**：纯文字提取会丧失标题层级、链接、图片。必须配合 html2text 保留 Markdown 结构。
2. **Jina URL 格式**：`r.jina.ai/example.com/path`，不是 `r.jina.ai/https://example.com/path`。
3. **微信公众号**：Jina 和 WebFetch 都无法获取，必须用 curl_cffi 脚本或 CDP。
4. **提取后处理**：如果用户需要的是文章分析/总结而非原文，在提取完成后再用 Claude 处理，不要在 WebFetch prompt 中同时做提取+分析（分离关注点，提取质量更高）。

## 成功指标

提取结果应包含：
- 文章标题和作者
- 正文段落（保留层级结构）
- 链接和图片 URL（作为引用素材）
- 代码块（如有）
- 无导航栏、广告、推荐列表等噪音
