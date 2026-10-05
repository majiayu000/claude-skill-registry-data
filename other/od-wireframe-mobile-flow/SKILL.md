---
name: od-wireframe-mobile-flow
description: 制作手机多屏流程线框（灰盒结构、关键标注）。用户要细化手机流程线框时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-wireframe-mobile-flow

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-wireframe-mobile-flow` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 至少 3 屏手机外框并排或纵向流，灰盒保真。
- 关键热区与流转箭头标注；禁高饱和装饰。
- 交付 index.html；与 od-wireframe-sketch 互补（本技能偏流程）。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
