---
name: weixin-article-to-obsidian-cn
description: 当用户需要把 mp.weixin.qq.com 微信公众号文章抓取为 Obsidian Markdown，并将图片本地化到 vault assets 目录时使用。
---

# 微信公众号文章转 Obsidian

## Overview

把微信公众号文章保存为 Obsidian 知识库里的 Markdown 文档，并把正文图片下载到本地资源目录。流程优先使用 `opencli weixin download` 获取正文，再解析页面源码补齐长图文章的图片和文章元信息。

## 何时使用

当用户提出以下需求时使用本技能：
- 提供 `mp.weixin.qq.com` 文章链接
- 要把微信公众号文章正文保存为 Markdown 笔记
- 要把文章图片下载到本地，而不是保留远程 CDN 链接
- 要使用 Obsidian 图片双链，例如 `![[assets/标题/图片.png]]`
- 要把这类微信公众号剪藏流程沉淀为可重复执行的操作

## 不要使用

以下场景不应使用本技能：
- 链接不是微信公众号文章
- 用户只想提取文章视觉样式或排版主题
- 用户想把 Markdown 发布回微信公众号
- 目标不是本地 Markdown 或 Obsidian 知识库

## 使用说明

1. 先阅读目标知识库规则，重点确认文档分类、图片资源目录、索引维护要求。
2. 根据文章主题选择语义目录。知识库已有更具体分类时，不要默认放到通用剪藏目录。
3. 如果本机有 `opencli`，先运行：

```bash
opencli weixin download --url "https://mp.weixin.qq.com/s/example" --output /tmp/weixin-article --download-images true -f yaml
```

4. 如果 `opencli` 没有抓全图片，或文章是长图页，运行本技能脚本：

```bash
python3 scripts/download_weixin_article.py "https://mp.weixin.qq.com/s/example" \
  --vault-root /path/to/obsidian-vault \
  --target-dir "FrontEnd/安全"
```

5. 检查生成的 Markdown，删除平台按钮、推荐阅读、打赏、重复元信息等残留内容。
6. 确认所有图片引用都指向 `assets/<文档标题>/` 下的本地文件，并使用 Obsidian 双链语法。
7. 如果知识库要求维护专题索引，把新文档以 wiki 链接加入对应索引页。

## 脚本行为

`scripts/download_weixin_article.py` 会执行以下操作：
- 优先尝试 `opencli weixin download`，在正文足够完整时复用其 Markdown 正文
- 直接抓取文章 HTML 作为兜底或补充
- 提取标题、公众号名称、发布时间、正文摘要和长图文章图片 URL
- 下载图片到 `assets/<安全标题>/`
- 将 Markdown 写入指定 `--target-dir`
- 输出 JSON 摘要，包含文档路径、资源目录、图片数量、是否运行 opencli

常用参数：
- `--vault-root`：Obsidian 知识库根目录，默认当前目录。
- `--target-dir`：知识库内的相对文档目录，默认知识库根目录。
- `--title`：覆盖自动提取到的标题，同时影响资源目录名。
- `--locale`：元信息标签语言，可选 `zh` 或 `en`，默认 `zh`。
- `--overwrite`：允许覆盖同名 Markdown 文档。

## 输出规则

- Markdown 放在语义正确的内容目录下。
- 图片放在知识库根目录的 `assets/<文档标题>/` 下。
- 图片引用使用 Obsidian 双链语法，不使用普通 Markdown 图片语法。
- 默认保留原文链接这一行，除非用户明确要求删除。
- 不主动添加 YAML frontmatter，除非目标知识库已有此要求。

## 校验清单

- 文档已出现在选择的目录中。
- 资源目录存在，并包含预期数量的文章图片。
- `rg "mmbiz|data:image|http" <文档>` 只剩原文链接，没有远程图片引用。
- 图片引用格式是 `![[assets/...]]`。
- 目标知识库要求索引时，对应专题索引已经更新。
