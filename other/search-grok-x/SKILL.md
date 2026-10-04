---
name: search-grok-x
description: "Use when Grok、X、Twitter、推特、实时新闻、X 舆论、trending，需要只读检索实时讨论和来源。"
---

# search-grok-x

## 目标
在用户需要 Grok、X/Twitter、实时新闻、舆论或 trending 信息时，通过只读搜索和来源交叉验证整理可追溯的公开信息。

## 适用请求
- 查询 X/Twitter 上的实时讨论、热门趋势、账号公开发文或事件时间线。
- 使用 Grok 新闻或相关工具辅助检索公开来源。
- 对社交平台传闻进行多来源交叉验证。

## 首选通道
- 本 skill 走 skill-only：不使用 MCP、不新增 MCP 配置；优先 WebSearch/WebFetch、可用 skill、当前 Firefox 可见会话。
- 如果 `rohunvora/x-research-skill` 已安装/可用，则优先使用原生 X API 做只读检索，否则走兜底。
- Grok 新闻如果 `Lanfei/grok-search-skill` 或 `b-open-io/x-research` 已安装/可用，则可只读检索，否则走兜底。
- 零成本路径如果 `psylch/tech-research-skill` 或 Grok 浏览器自动化已可用，则用于只读浏览和搜索，否则走兜底。

## 兜底通道
- 使用普通 WebSearch 查询 X 帖子、新闻报道、引用页面和缓存摘要。
- 对结果进行来源交叉验证，优先核对原帖、官方公告、可信媒体和多个独立来源。

## 操作流程
1. 明确关键词、账号、话题标签、时间范围、地区和是否需要实时性。
2. 优先用可用的 X API/Grok 工具只读搜索；不可用时使用 WebSearch 和浏览器读取公开页面。
3. 读取内容时全程只读搜索/读取，不发起新的登录流程、不下单、不私信、不发帖、不写入平台，也不关注、点赞、转发或回复。
4. 对实时新闻至少交叉核对多个来源，标注原帖 URL、发布时间、作者账号和验证状态。
5. 输出时区分事实、传闻、观点和未经证实内容，避免把 trending 当作真实性证明。

## 只读安全边界
- 只搜索、读取、摘录和总结公开内容。
- 不发起新的 X/Grok 登录流程；如当前 Firefox 已登录则只读复用，不绕过付费、验证码、年龄限制或访问控制。
- 不关注、点赞、转发、回复、发帖、私信、举报、订阅或写入平台。
- 不保存 API Key、Cookie、Token 或账户会话。

## 验证方式
- 后续可运行：`dir C:\Users\Zhang\.config\opencode\skills\search-grok-x\SKILL.md`
- 人工检查：确认首选通道包含 `rohunvora/x-research-skill`、`Lanfei/grok-search-skill`、`b-open-io/x-research`、`psylch/tech-research-skill`。

## 已知限制
- X/Twitter 内容可能因登录、地区、删除、限流或 API 权限而不可见。
- 实时趋势变化快，结果需要标注检索时间。
- WebSearch 对最新推文和回复链收录可能延迟或缺失。
