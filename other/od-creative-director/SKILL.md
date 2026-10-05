---
name: od-creative-director
description: 对已有设计稿或 HTML 做创意总监式审稿（层级、节奏、品牌一致性与改稿清单）。内部辅助技能，用户明确要求「帮我审稿 / 改设计」时使用。先读 open-design 总控再执行。
---

# od-creative-director

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-creative-director` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `review.md`（若改稿则同步更新 HTML）；对话只给路径。**禁止**写入 `artifacts/design/` 语义目录。

- 输出结构化审稿意见（优点 / 问题 / 优先改 3 项），可写 review.md。
- 若用户要求改稿，再 write_file 更新 HTML；勿空谈不落盘。
- 禁止另起无关新站；锚定用户已有成果路径。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
