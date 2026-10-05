---
name: od-social-carousel
description: 制作多张可左右滑动的社媒图文卡片（干货要点、统一视觉系列）。用户提到小红书风格、轮播图、多张配图时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-social-carousel

## 使用方式

1. 先 `read_skill` 读取 `open-design`。
2. 用 `read_skill` skillName=`od-social-carousel` relativePath=`references/checklist.md` 读清单并自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 3–7 张卡片，比例约 3:4（如 1080×1440）。
- **封面/主卡先生图**：首张或真图轮播位先 `generate_image` 落盘 PNG（约 1 次）再引用；次卡可用 CSS。禁止整套纯渐变充数。
- 系列统一配色与字体，每张一个要点标题+短说明。
- 支持横向滑动浏览（CSS/JS）。
- 内容来自用户主题，不 filler 文案。

## 资源

- 上游：OpenDesign/skills/card-xiaohongshu
- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
