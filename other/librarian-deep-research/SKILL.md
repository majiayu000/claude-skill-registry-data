---
name: librarian-deep-research
description: 当用户需要深度搜索、找资料、全网搜索、资料核验、中文资料、知乎、小红书、微信公众号、linux.do、Linux Do、Telegram、Grok、X、淘宝、天猫、京东、闲鱼、Amazon、亚马逊、比价、价格历史、电商口碑、商品调研时触发；为 librarian 提供跨平台深度研究路由和证据输出格式。
---

# Librarian Deep Research

用于指导 librarian 执行只读、跨平台、可追溯的深度搜索。不要保存 secrets，不读取 cookie/token/密码明文，不执行下单、发消息、询价、发布、点赞、关注等改变外部状态的动作。

## 路由策略

1. 明确问题：主题、时间范围、地区/语言、平台范围、输出粒度、可信度要求。
2. 基础证据：优先官方文档、原始公告、论文/标准、权威媒体、项目仓库、平台原帖。
3. 中文社区：
   - 知乎：调用 `search-zhihu` 查问答、专栏、长讨论。
   - 小红书：调用 `search-xiaohongshu` 查笔记、消费体验、图文口碑。
   - 微信公众号：调用 `search-wechat` 查机构/品牌/媒体长文。
   - linux.do：调用 `search-linuxdo` 查技术社区讨论与经验帖。
4. 社交与实时线索：
   - Grok/X：调用 `search-grok-x` 查实时观点和英文线索。
   - Telegram：调用 `search-telegram` 查公开频道/群组资料；只读，不发消息。
5. 电商与价格：
   - 综合中国电商：调用 `search-cn-ecommerce`。
   - 淘宝/天猫：调用 `search-taobao-tmall`。
   - 京东：调用 `search-jd`。
   - 闲鱼：调用 `search-xianyu`。
   - Amazon：调用 `search-amazon`。
   - 价格历史：调用 `search-price-history` 交叉核验历史低价、促销周期和价格波动。
6. 交叉验证：关键结论至少使用两个独立来源；单一来源必须标注为未完全证实。

## Firefox 当前会话复用

- 默认复用用户当前已经打开并登录的 Firefox 主会话；登录态平台必须优先用 `firefox.exe -new-tab <url>` 打开到现有 Firefox 新标签页。
- 如果用户确认当前 Firefox 已登录，直接把该会话视为已认证来源；不要重复要求扫码、验证码或重新登录。
- 本搜索增强走 skill-only：不要新增或依赖 MCP。公开页面用 WebSearch/WebFetch/浏览器；登录态页面用当前 Firefox 可见会话。
- 需要登录态时，优先尝试 Firefox 已有 cookies/profile session 的浏览器托管登录态：先打开到当前 Firefox；如仍未登录，再在用户明确要求下尝试使用本机 Firefox profile/session。不得导出、打印、保存或手工解析 cookie 明文。
- 需要提取资料时，优先从用户可见页面通过桌面自动化、复制页面文本、截图/OCR、手动确认等方式获取证据。
- 不读取/导出 token、密码、账号数据库或 Firefox profile 内的敏感文件；cookie 只能由 Firefox/浏览器引擎在本机进程内自动携带。
- 如果当前 Firefox 无法自动提取内容，先说明限制，再询问用户是否允许重启 Firefox 加远程调试/自动化参数；未经允许不得重启当前浏览器。
- 卡在 QR、验证码、SMS、二次验证、API key 或授权页时，停止并要求用户自行操作。

## 证据输出格式

最终输出按结论组织，每条证据建议包含：

| 字段 | 要求 |
| --- | --- |
| 结论 | 一句话说明可支持的判断 |
| 来源/链接 | 原始链接或可复核路径 |
| 平台/来源类型 | 官方、媒体、社区、社交、电商、价格历史等 |
| 时间 | 发布时间、更新时间或抓取时间 |
| 关键引用 | 支撑结论的短摘录或关键数据 |
| 可信度 | 高/中/低，并说明理由 |
| 限制 | 样本偏差、地域、时效、登录可见性、单一来源等 |

## 安全边界

- 电商只读：不下单、不加入购物车、不发消息、不询价、不改地址、不收藏/关注。
- Telegram 只读：不发消息、不加群、不私聊、不改设置。
- 社交平台只读：不点赞、不评论、不关注、不转发、不发布。
- 不保存或输出 secrets、cookie、token、验证码、短信内容、账号密码；不把 Firefox cookie 明文化。
