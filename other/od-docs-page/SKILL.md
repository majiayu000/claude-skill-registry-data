---
name: od-docs-page
description: 制作产品文档或帮助中心单页（侧栏目录 + 正文）。用户提到文档站、帮助文档页时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-docs-page

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-docs-page` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 左侧目录 + 右侧正文（或顶部分段导航）。
- 至少 3 个章节标题与可读正文；代码块可选。
- 窄屏目录可折叠或置顶，不横向溢出。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
