---
name: od-deck-swiss
description: 制作瑞士国际主义风格 HTML 演示稿（16 列网格、单一强调色、锁死版式）。用户提到瑞士风 deck、国际主义幻灯网页时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-deck-swiss

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-deck-swiss` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 横屏 16:9 多页（至少 4 页），键盘或点击翻页。
- 强网格对齐、单一饱和强调色；冷静理性，无手绘噪点装饰。
- 真实内容填充，禁 lorem；交付 index.html。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
