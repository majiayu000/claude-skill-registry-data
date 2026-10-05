---
name: od-email-marketing
description: 制作可在邮件客户端展示的活动或新品通知版面（标题区、主图、正文、按钮）。用户提到邮件模板、活动邮件、电子报时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-email-marketing

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-email-marketing` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 居中单栏，最大宽约 600px，表格或简单布局利于邮件客户端兼容。
- 含：品牌名、标题、主视觉区、2–4 段正文、主按钮、退订/地址脚注占位。
- 避免复杂动效与外部字体依赖。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
