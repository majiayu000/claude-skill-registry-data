---
name: od-pm-spec
description: 制作产品规格 / PRD 展示页（背景、需求、验收）。用户提到产品规格页、PRD 页面时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-pm-spec

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-pm-spec` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 含背景、目标用户、功能列表、验收标准分区。
- 可用表格列出优先级；示意数据贴合 brief。
- 单文件 HTML，结构清晰便于评审。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
