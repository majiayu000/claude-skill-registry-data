---
name: aa-ana-wo-direct-auth
description: "真实浏览器已登录态取证，由 Hermes 中介提取页面/请求/存储证据，再交给 anything-analyzer 或其他 agent 离线分析。"
triggers:
  - 真实浏览器登录态分析
  - 不让 aa 直接访问
  - 中介取证
  - 已登录页面导给 aa
  - browser harness + aa
  - 离线分析已认证页面
---

# 真实浏览器取证 -> Hermes 中介 -> AA 离线分析

## 适用场景

当用户希望：
- 使用自己真实浏览器中的现成登录态
- 不让 anything-analyzer 直接持有或主动使用该登录态
- 仍借助 anything-analyzer 的分析能力（协议逆向、流程梳理、接口归纳、风控观察）

优先采用此流，而非让 AA 直接登录。

## 核心原则

1. 认证发生在用户真实浏览器。
2. Hermes 作为中介采集证据。
3. AA 仅消费导出的证据，不直接控制用户真实登录会话。
4. 只抽取分析所需最小材料，避免无关凭证扩散。

## 推荐工具面

- 首选：`browser` / browser harness / 真实 Chrome CDP
- 辅助：`browser_console` 提取 DOM、storage、JS 状态
- 需要时：anything-analyzer 仅用于分析文本化证据或整理后的请求样本

## 标准流程

### Phase 1 — 锁定目标页

1. 让用户在真实浏览器中打开并登录目标站点。
2. Hermes 连接该已登录浏览器页。
3. 确认当前 URL、页面标题、关键 DOM 已正确加载。

建议先取：
- 当前 URL
- 页面标题
- 关键按钮/列表/表单是否可见
- 是否存在 SPA 路由跳转或懒加载

### Phase 2 — 中介取证

按需提取下列材料，不必全取。

#### A. 页面结构
- `document.documentElement.outerHTML`
- 关键区域 `outerHTML`
- 页面文本摘要
- 必要截图

#### B. 浏览器存储
- `localStorage`
- `sessionStorage`
- 必要 cookies（仅名称、作用域、是否存在；非必要不回传完整值）

#### C. 网络证据
- fetch/XHR 请求 URL
- method
- headers（必要字段）
- request payload
- response body
- 时序关系（先调谁，再调谁）

#### D. 运行态线索
- 全局变量
- 前端签名/加密函数入口
- token 刷新逻辑
- 路由参数
- WebSocket / SSE 端点

### Phase 3 — 证据整理

将采集结果整理成 AA 易消费的结构化材料。推荐格式：

```json
{
  "page": {
    "url": "https://target.example/app",
    "title": "Dashboard"
  },
  "dom": {
    "key_sections": ["..."],
    "summary": "..."
  },
  "storage": {
    "localStorage": {},
    "sessionStorage": {},
    "cookies_present": ["session", "csrf"]
  },
  "requests": [
    {
      "url": "https://api.target.example/v1/list",
      "method": "POST",
      "headers": {"content-type": "application/json"},
      "request_body": "...",
      "response_body": "..."
    }
  ],
  "notes": [
    "点击按钮 A 后先请求 /profile，再请求 /list",
    "Authorization 由前端从 localStorage.token 注入"
  ]
}
```

## 喂给 AA 的方式

### 模式 1：文本/JSON 离线分析

将上述材料直接作为 prompt/context 发给 AA，请其：
- 归纳 API
- 解释认证流程
- 识别签名算法入口
- 推断关键状态机
- 生成复现脚本

此模式下，AA 无需访问真实站点。

### 模式 2：仅喂请求样本

若目标是逆向协议，可只提供：
- 一组关键请求/响应
- header 差异
- storage 摘要
- 页面动作与请求的映射

可显著减少凭证暴露面。

## 选择策略

### 优先用本流，若：
- 用户已在真实浏览器登录
- 登录流程复杂（2FA、验证码、硬件密钥）
- 不希望 AA 直接持有登录态
- 只需分析，不需 AA 长时间实时操控

### 改用 `aa-human-auth-cdp-flow`，若：
- 需要 AA 自己持续抓包
- 需要其 session DB / hooks / reports 全链路能力
- 需要在同一 Electron 会话中连续操作多步流程

## 提取最小化原则

- 非必要，不导出完整 cookie 值
- 非必要，不导出全量 storage；先列 key，再按需取值
- 非必要，不贴全量 HTML；优先关键片段
- 长响应先摘要，必要时再补原文
- 将敏感字段与业务字段分离存放

## 输出建议

默认按：结果 -> 关键证据 -> 可复现步骤 -> 下一步。

证据块尽量集中：
- URL
- headers 关键项
- request/response 样本
- storage key
- 事件顺序

## 常见用途

- 已登录 SaaS 控制台接口逆向
- OAuth / SPA token 注入路径确认
- 风控前端逻辑梳理
- 页面点击到 API 时序映射
- WebSocket / SSE 消息格式分析
- 导出最小复现请求集给其他 agent

## 一句话模板

当用户表达“别让 AA 直接碰登录态，只分析已登录页面”时，执行：

1. 连接真实浏览器已登录页面
2. 采集最小必要证据
3. 结构化整理
4. 把证据交给 AA 做离线分析

而非让 AA 直接访问目标站点。
