---
name: od-hr-onboarding
description: 制作 HR 新人入职引导页（步骤、清单、联系人）。用户提到入职引导、onboarding 页面时使用。先读 open-design 总控，再按本技能清单执行。
---

# od-hr-onboarding

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认（勿另起无关设计系统问卷）。
2. 用 `read_skill` skillName=`od-hr-onboarding` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。
3. 直接按用户 brief 开做；用户说「直接开始做」时禁止再问风格偏好。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 分步流程（至少 4 步）与进度示意。
- 待办清单、常用链接、对接人卡片。
- 语气友好专业，贴合用户公司名。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
- 上游意图摘要：`references/upstream-notes.md`（经 read_skill relativePath 读取；可选）
