---
name: od-web-prototype
description: 制作高保真网页原型（导航、核心页面区块、关键交互示意）。用户要「原型 / 高保真 HTML 示意」时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-web-prototype

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-web-prototype` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 完整单页或少量锚点分区，含顶栏导航与页脚。
- 至少 3 个内容区块贴合用户 brief；文案用真实业务词，禁 lorem。
- 交互可用锚点 / 简单 JS；交付可浏览器直接打开。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
