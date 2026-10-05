---
name: od-kanban-board
description: 制作看板任务板页面（多列状态、卡片、优先级标签）。用户提到看板、Kanban、任务板时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-kanban-board

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-kanban-board` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 至少 3 列（如待办 / 进行中 / 完成），每列有示例卡片。
- 卡片含标题、标签、负责人占位；列宽在桌面可读。
- 示例数据贴合用户场景，禁空白骨架。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
