---
name: od-article-magazine
description: 制作杂志风长文章阅读页（大标题、章节、引用、配图区）。用户提到博客长文、公众号文章、专题报道时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-article-magazine

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-article-magazine` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 编辑排版：标题、作者/日期、导语、2–4 个小节、引用块、配图区。
- **配图先生图**：非官图任务时对关键配图位 `generate_image`（合计 ≤3）落盘 PNG 再引用；禁止首轮空占位当完成。官图任务除外。
- 行宽适合长文阅读（约 65–75 字符）。
- 用户提供提纲或正文时优先沿用，不杜撰事实。

## 资源

- 上游：OpenDesign/skills/article-magazine
- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
