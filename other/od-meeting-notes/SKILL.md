---
name: od-meeting-notes
description: 制作会议纪要展示页（议题、决议、行动项与负责人）。用户要「会议纪要页 / 纪要排版」时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-meeting-notes

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-meeting-notes` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 页眉含会议主题、时间、与会人。
- 分区：议题要点、决议、行动项（负责人 + 截止日期占位）。
- 排版清晰可打印；内容贴合用户提供的笔记。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
