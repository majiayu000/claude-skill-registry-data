---
name: camofox-browser
description: 通过 camofox-browser HTTP API（localhost:9377）进行无头浏览器自动化。创建标签页、导航、抓取页面快照、点击、输入、滚动、提取链接与内容。
---

# camofox-browser

camofox-browser 是基于 Camoufox（Firefox 反检测引擎）的无头浏览器自动化服务器，端口 9377。

## 启动服务

```bash
cd ~/Downloads/camofox-browser && npm start &
```

服务监听 http://localhost:9377。若端口被占用：`lsof -ti:9377 | xargs kill -9`。

## API 用法

全部请求 `Content-Type: application/json`，用 curl 调用。

### 创建标签页
```bash
curl -s -X POST http://localhost:9377/tabs \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","sessionKey":"task1","url":"https://example.com"}'
```
返回：`{"tabId":"...","url":"...","title":"..."}`

### 导航
```bash
curl -s -X POST http://localhost:9377/tabs/<tabId>/navigate \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","url":"https://fanqienovel.com/..."}'
```

### 获取页面快照
```bash
curl -s "http://localhost:9377/tabs/<tabId>/snapshot?userId=agent1"
```
返回无障碍树文本，含元素 ref（e1, e2, ...）。导航后 ref 重置，须重新获取快照。

### 点击
```bash
curl -s -X POST http://localhost:9377/tabs/<tabId>/click \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","ref":"e1"}'
# 或用 CSS 选择器：
  -d '{"userId":"agent1","selector":"button.submit"}'
```

### 输入
```bash
curl -s -X POST http://localhost:9377/tabs/<tabId>/type \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","ref":"e2","text":"搜索","pressEnter":true}'
```

### 滚动
```bash
curl -s -X POST http://localhost:9377/tabs/<tabId>/scroll \
  -H 'Content-Type: application/json' \
  -d '{"userId":"agent1","direction":"down","amount":500}'
```

### 前后退/刷新
```bash
curl -s -X POST http://localhost:9377/tabs/<tabId>/back     -d '{"userId":"agent1"}'
curl -s -X POST http://localhost:9377/tabs/<tabId>/forward  -d '{"userId":"agent1"}'
curl -s -X POST http://localhost:9377/tabs/<tabId>/refresh  -d '{"userId":"agent1"}'
```

### 获取链接
```bash
curl -s "http://localhost:9377/tabs/<tabId>/links?userId=agent1&limit=50"
```

### 关闭标签页
```bash
curl -s -X DELETE "http://localhost:9377/tabs/<tabId>?userId=agent1"
```

### 搜索宏

用宏替代直接拼 URL：

| 宏 | 站点 |
|---|---|
| `@google_search` | Google |
| `@youtube_search` | YouTube |
| `@amazon_search` | Amazon |
| `@reddit_search` | Reddit |
| `@wikipedia_search` | Wikipedia |
| `@twitter_search` | Twitter/X |
| `@yelp_search` | Yelp |
| `@linkedin_search` | LinkedIn |

用法：`{"userId":"agent1","macro":"@google_search","query":"关键词"}`

## 关键点

- 不同 `userId` 隔离 cookie/存储；不同 `sessionKey` 分组标签页。
- 会话 30 分钟不活动超时。
- Camoufox 反检测引擎可绕过 Google 验证码。
- 渲染中文页面时无字体混淆，可直接抓取真实文字。
