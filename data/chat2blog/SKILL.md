---
name: chat2blog
description: 将 AI 聊天记录、对话内容转换为 VuePress 格式的技术博客文章。当用户说"把对话整理成博客"、"写成文章"、"转换成 blog"、"生成博客"，或提供聊天记录、技术讨论、问题解决过程需要整理时使用。输出包含 frontmatter 的完整 Markdown 文章。
---

# 聊天记录转技术博客

## Instructions

1. 读取 [reference.md](./reference.md) 中的完整 prompt 指令
2. 按照 reference.md 中的思维链流程分析聊天记录
3. 生成符合 VuePress 格式的技术博客文章
4. 保存文章到项目的 docs/program 目录下

## 输出格式

文章顶部必须包含 VuePress frontmatter：

```markdown
---
title: 文章标题
date: YYYY-MM-DD
---

# 文章标题

[文章内容...]
```

注意：
- date 使用当前日期（格式：YYYY-MM-DD）
- title 应该吸引人且准确反映内容
- 遵循 reference.md 中的所有写作规范