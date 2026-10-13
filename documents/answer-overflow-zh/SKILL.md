---
name: answer-overflow-zh
description: 通过 Answer Overflow 搜索已索引的 Discord 社区讨论。非常适合查找编程问题解决方案、库问题和社区问答，这些内容通常只存在于 Discord 对话中。
---

# Answer Overflow 技能

通过 Answer Overflow 搜索已索引的 Discord 社区讨论。非常适合查找编程问题解决方案、库问题和社区问答。

## 什么是 Answer Overflow？

Answer Overflow 索引公开的 Discord 支持频道，并通过 Google 和直接 API 访问使其可搜索。非常适合查找只存在于 Discord 对话中的答案。

## 快速搜索

使用 web_search 查找 Answer Overflow 结果：
```bash
# 搜索某个主题（Answer Overflow 结果通常出现在 Google 中）
web_search "site:answeroverflow.com prisma connection pooling"
```

## 获取线程内容

### Markdown URL
添加 `/m/` 前缀或 `.md` 后缀以获取 Markdown 格式的内容：

```
# 标准URL
https://www.answeroverflow.com/m/1234567890123456789

# 带 .md 后缀（替代方案）
https://www.answeroverflow.com/m/1234567890123456789.md
```

### 使用 web_fetch
```bash
# 以 Markdown 格式获取线程
web_fetch url="https://www.answeroverflow.com/m/<message-id>"
```

### Accept 头
发起请求时，API 会检查 `Accept: text/markdown` 头以返回 Markdown 格式。

## MCP 服务器（参考）

Answer Overflow 在 `https://www.answeroverflow.com/mcp` 提供了一个 MCP 服务器，包含以下工具：

| 工具 | 描述 |
|------|------|
| `search_answeroverflow` | 搜索所有已索引的 Discord 社区。可按服务器或频道 ID 过滤。 |
| `search_servers` | 发现 Answer Overflow 上索引的 Discord 服务器。返回服务器 ID 用于过滤搜索。 |
| `get_thread_messages` | 获取特定线程/讨论的所有消息。 |
| `find_similar_threads` | 查找与给定线程相似的线程。 |

## URL 模式

| 模式 | 示例 |
|---------|---------|
| 线程 | `https://www.answeroverflow.com/m/<message-id>` |
| 服务器 | `https://www.answeroverflow.com/c/<server-slug>` |
| 频道 | `https://www.answeroverflow.com/c/<server-slug>/<channel-slug>` |

## 常见搜索

```bash
# 查找 Discord.js 帮助
web_search "site:answeroverflow.com discord.js slash commands"

# 查找 Next.js 解决方案
web_search "site:answeroverflow.com nextjs app router error"

# 查找 Prisma 答案
web_search "site:answeroverflow.com prisma many-to-many"
```

## 技巧

- 结果是真实的 Discord 对话，因此上下文可能比较非正式
- 线程通常在找到解决方案之前会有来回讨论
- 检查服务器/频道名称以了解上下文（例如官方支持 vs 社区）
- 许多开源项目在此索引其 Discord 支持频道

## 链接

- **网站：** https://www.answeroverflow.com
- **文档：** https://docs.answeroverflow.com
- **MCP：** https://www.answeroverflow.com/mcp
- **Discord：** https://discord.answeroverflow.com
