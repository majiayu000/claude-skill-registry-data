---
name: od-waitlist-page
description: 制作产品预发布 / 候补名单落地页（品牌、一句话价值、邮箱收集与成功态）。用户提到 waitlist、即将上线、早鸟报名时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-waitlist-page

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-waitlist-page` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 首屏一眼看懂产品名与一句话价值，邮箱输入 + 提交按钮可用（可用前端假成功态）。
- **Hero 装饰**：非官图时优先 `generate_image`（≈1 次）再写 HTML；次要装饰可用 CSS。勿堆紫蓝 AI 渐变冒充主视觉。
- 手机窄屏不横向溢出；提交后有成功提示文案。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
