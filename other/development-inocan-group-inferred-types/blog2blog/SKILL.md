---
name: blog2blog
description: 将现有技术博客重写为更自然、有温度的风格。当用户说"重写这篇博客"、"优化文章风格"、"让博客更有人情味"时使用。输出符合 VuePress 格式的重写版本。
---

# 博客风格重写

## Instructions

1. 读取 [reference.md](./reference.md) 中的完整风格指南
2. 分析现有博客的技术内容和结构
3. 按照 reference.md 中的风格要求重写文章
4. 保存重写后的文章到项目的 docs/program 目录下

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
- 保留原文的技术准确性
- date 使用当前日期（格式：YYYY-MM-DD）
- title 可以优化得更吸引人
- 遵循 reference.md 中的所有写作规范
