---
name: search-amazon
description: "Use when Amazon、亚马逊、ASIN、Amazon reviews、Amazon price，需要只读检索 Amazon 商品、评价和价格。"
---

# search-amazon

## 目标
在用户需要 Amazon/亚马逊商品、ASIN、评价或价格信息时，通过只读搜索、详情读取和历史价工具整理商品资料、评价摘要、当前价与来源。

## 适用请求
- 搜索 Amazon 商品、ASIN、品牌型号或同类竞品。
- 读取 Amazon reviews、评分、变体、卖家和 Amazon price。
- 查询 Amazon 历史价格或价格趋势。

## 首选通道
- skill-only：优先使用 WebSearch/WebFetch 与 Amazon 页面只读读取商品、ASIN、评价和价格。
- 需要登录后内容时复用当前 Firefox 已登录会话；历史价优先使用 Keepa/公开价格历史网页或用户已有 API，不新增或依赖 MCP。

## 兜底通道
- 使用 WebSearch 查询 ASIN、商品标题、`site:amazon.com` 或对应站点域名。
- 使用浏览器只读打开 Amazon 页面；遇到登录、验证码、地区或年龄限制时请求用户人工处理。

## 操作流程
1. 确认目标站点地区、关键词、ASIN、价格范围、是否需要 reviews 或历史价。
2. 优先用 WebSearch/WebFetch + 浏览器只读读取页面可见信息；历史价查 Keepa/公开历史价来源。
3. 如用户已有官方 API 或 Keepa API，可在用户明确要求且不写入密钥的前提下只读查询。
4. 全程只读搜索/读取，不发起新的登录流程、不下单、不私信、不发帖、不写入平台，也不加入购物车、订阅、写评价或联系卖家。
5. 输出 ASIN、标题、价格、币种、卖家/配送、评分、评价摘要、历史价来源、URL 和检索时间。

## 只读安全边界
- 只搜索、打开、读取和总结 Amazon 公开或授权可见内容。
- 不发起新的 Amazon 登录流程；如当前 Firefox 已登录则只读复用，不绕过验证码、地区、年龄、Prime 或付费限制。
- 不加购、不下单、不付款、不订阅、不写评价、不联系卖家、不发布内容。
- 不保存 API Key、Cookie、Token、地址或支付信息。

## 验证方式
- 后续可运行：`dir C:\Users\Zhang\.config\opencode\skills\search-amazon\SKILL.md`
- 人工检查：确认流程为 skill-only + WebSearch/WebFetch/当前 Firefox，不依赖 MCP。

## 已知限制
- Amazon 价格、库存、配送和优惠因地区、账号和时间变化。
- 评价分页、反爬和验证码可能影响读取完整性。
- Keepa 或官方 API 需要用户已有可用配置；本 skill 不写入密钥。
