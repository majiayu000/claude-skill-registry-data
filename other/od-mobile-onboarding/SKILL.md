---
name: od-mobile-onboarding
description: 制作新用户首次打开应用的引导画面，通常 3 屏（欢迎、价值说明、登录或开始）。用户提到新手引导、首次使用、开屏引导时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-mobile-onboarding

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-mobile-onboarding` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 3 屏左右：欢迎 → 核心好处 → 登录/注册/开始使用。
- 进度指示（圆点或步骤条）、主按钮、跳过入口（可选）。
- 手机比例，文案简短。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
