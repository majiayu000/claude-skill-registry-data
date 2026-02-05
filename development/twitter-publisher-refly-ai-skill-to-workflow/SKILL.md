---
name: twitter-publisher
description: 通过 bird CLI 发布和管理 Twitter/X 内容。使用此 skill 当用户需要：(1) 发布推文或帖子，(2) 回复推文，(3) 读取或获取推文内容，(4) 搜索推文，(5) 查看 mentions/bookmarks/likes，(6) 附带图片或视频发推。触发词包括：发推、tweet、发帖、回复推文、读取推文、Twitter、X 平台。
---

# Twitter Publisher

通过 [bird CLI](https://github.com/steipete/bird) 与 Twitter/X 交互，支持发推、回复、读取和搜索。

## 前置要求

安装 bird CLI：
```bash
npm install -g @steipete/bird
# 或 bunx @steipete/bird <command>
```

## 认证

bird 使用浏览器 cookie 认证（无需 API key），按以下优先级获取凭证：

1. CLI flags: `--auth-token`, `--ct0`
2. 环境变量: `AUTH_TOKEN`, `CT0`
3. 浏览器 cookies（自动提取）

验证认证状态：
```bash
bird whoami    # 显示当前登录账户
bird check     # 显示凭证来源
```

## 核心操作

### 发布推文

```bash
# 纯文本
bird tweet "推文内容"

# 附带媒体（最多4张图片或1个视频）
bird tweet "内容" --media image.png --alt "图片描述"
bird tweet "内容" --media img1.png --media img2.png

# 支持格式：jpg, jpeg, png, webp, gif, mp4, mov
```

### 回复推文

```bash
bird reply <tweet-id-or-url> "回复内容"
bird reply https://x.com/user/status/123456789 "回复内容"
bird reply 123456789 "回复内容" --media image.png
```

### 读取推文

```bash
bird read <tweet-id-or-url>           # 文本输出
bird read <url> --json                # JSON 输出
bird <tweet-id>                       # 简写形式
bird thread <url>                     # 完整对话线程
bird replies <url>                    # 查看回复
```

### 搜索与查询

```bash
bird search "关键词" -n 10            # 搜索推文
bird search "from:username" -n 5      # 搜索特定用户
bird mentions -n 10                   # 查看提及
bird mentions --user @handle -n 5     # 查看他人被提及
bird bookmarks -n 10                  # 查看收藏
bird likes -n 10                      # 查看喜欢
```

### 用户关系

```bash
bird following -n 20                  # 我关注的人
bird followers -n 20                  # 关注我的人
bird following --user <userId> -n 10  # 指定用户关注的人
```

## 常用选项

| 选项 | 说明 |
|------|------|
| `--json` | JSON 格式输出 |
| `--plain` | 稳定输出（无 emoji、无颜色） |
| `-n <count>` | 返回数量 |
| `--timeout <ms>` | 请求超时 |
| `--cookie-source <browser>` | 指定浏览器：safari/chrome/firefox |

## JSON 输出结构

推文对象包含：`id`, `text`, `author`, `authorId`, `createdAt`, `replyCount`, `retweetCount`, `likeCount`, `conversationId`, `inReplyToStatusId`, `quotedTweet`

## 错误处理

- GraphQL 错误 226：自动回退到 legacy API
- Query ID 过期：使用 `bird query-ids --fresh` 刷新
- 429 限流：等待后重试

## 工作流示例

**发布带图推文：**
```bash
# 1. 准备图片
# 2. 发布
bird tweet "分享今天的成果！" --media screenshot.png --alt "项目截图"
```

**监控并回复提及：**
```bash
# 1. 获取提及
bird mentions -n 5 --json > mentions.json
# 2. 处理并回复
bird reply <tweet-id> "感谢反馈！"
```

**搜索并分析：**
```bash
bird search "关键词 lang:zh" -n 20 --json
```
