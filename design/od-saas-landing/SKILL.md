---
name: od-saas-landing
description: 为企业或产品制作官网、落地页、介绍页（首屏、功能说明、价格或试用入口、页脚联系）。用户提到官网、落地页、产品介绍时使用。先读取 open-design 总控流程，再按本技能清单执行。
---

# od-saas-landing

## 使用方式

1. 先 `read_skill` 读取 `open-design`，完成风格与品牌确认。
2. 若用户要求**官网实际大图 / 不要生成图片**：用 `read_skill` skillName=`open-design` relativePath=`references/official-product-images.md` 读取，用 `fetch_page_images`（首选）或 `web_fetch` 取图，直接 `write_file` 交付，**不要** `web_search` 或 `bash curl`。
3. 用 `read_skill` skillName=`od-saas-landing` relativePath=`references/checklist.md` 读清单，交付前逐条自检（勿 `read_file`）。

## 产物要求

- 交付：`write_file` 到**系统分配的任务目录**（`artifacts/task-*`）下的 `index.html`；对话只给路径，勿贴整页 html。**禁止**写入 `artifacts/design/` 语义目录。

- 单文件 HTML，浏览器可直接打开预览。
- 至少包含：首屏标题与一句话价值、3–6 个功能或服务说明、价格或「立即试用」区域、页脚。
- **Hero 配图**：非官图任务时先 `generate_image`（≈1 次）落盘 PNG 再写 HTML；禁止首轮纯 CSS 渐变冒充 Hero。用户要求官方产品图时：走 `resolve_session_visual_assets`/`fetch_page_images`，禁止 `generate_image` 冒充官图（见 open-design `references/official-product-images.md`）。
- 文案贴合用户提供的行业与产品名，不编造虚假数据。

## 资源

- 清单：`references/checklist.md`（经 read_skill relativePath 读取）
