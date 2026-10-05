---
name: od-blog-post
description: 制作博客 / 长文阅读页（标题、作者信息、正文排版）。用户提到博客页、文章页时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-blog-post

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-blog-post` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 标题、作者/日期、导语；正文层级清晰（h2/h3）。
- 适合阅读的行宽与字距；有配图诉求时先 `generate_image`（≤2）落盘再引用，禁止空占位当完成。
- 文末可附相关阅读或 CTA。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
