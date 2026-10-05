---
name: open-design
description: 作为 Open Design 设计总控技能，将含糊需求转为高质量 HTML 设计产物。凡是用户提出设计页面、原型、营销页、UI 视觉探索、品牌风格对齐、多屏界面草图等请求时都应优先使用本技能；通过问卷澄清、方向选择、设计系统绑定、反 AI 味清单与五维自检来稳定产出质量。
---

# Open Design Master Skill

将 Open Design 的核心方法论迁移到 PilotDeck：先澄清，再定调，再落地，再自检。

## 目标

- 把用户意图快速收敛成可执行设计 brief。
- 用可解释的视觉方向和设计系统约束生成 HTML 产物。
- 降低“AI 味”与风格漂移，提升首稿命中率。

## 何时触发

遇到以下任务，优先触发本技能并编排后续子技能：

- 设计单页网站、落地页、产品页、营销页、海报页。
- 设计多屏原型、应用界面、仪表盘、登录/引导/流程页。
- 用户只给目标，不给风格，希望“你来定方向”。
- 用户提供品牌规范、参考网址、截图，希望对齐品牌。

## 工作流

### 1) 用结构化问答锁定 brief

使用 `ask_user_question` 一次性收集核心信息（最多 4-6 个问题）：

- 输出类型（原型/营销页/多屏界面/仪表盘/其他）
- 目标人群
- 视觉调性（最多两项）
- 品牌上下文（系统选方向 / 用户提供品牌规范 / 对齐参考）
- 规模（页数/屏数）

如果用户信息非常完整，可压缩问题；但不要完全跳过“风格与品牌来源”确认。
**例外**：手机多屏界面且用户已给出 App 名、屏数、风格（如「世界杯观赛指南、三屏、FIFA」）时，跳过问卷，直接路由 `od-mobile-app` 并调用 `scaffold_mobile_mockup`。

推荐问题头（可直接复用）：

- `What are we making?`：`Single web prototype` / `Marketing landing` / `Dashboard` / `Multi-screen app` / `Other`
- `Who is this for?`：文本
- `Visual tone`：多选最多 2 项
- `Brand context`：`Pick direction` / `I have brand spec` / `Match reference`
- `Scale`：文本（页数/屏数）

### 2) 如果无品牌规范，走方向选择器

用 `read_skill` skillName=`open-design` relativePath=`references/directions.md` 读取方向库，并通过 `ask_user_question` 提供 5 个方向。
可在每个选项中附短预览（调色板/字体说明）。

### 3) 绑定设计系统并路由子技能

- 用 `read_skill` skillName=`open-design` relativePath=`references/design-systems/_index.md` 选一个最接近的系统，再 read_skill relativePath 读对应 `references/design-systems/<名>.md`。
- 用户可读目录：`docs/open-design-design-catalog.md`（类别、文件、提问示例；接入变更后需重新生成）。
- 再根据任务类型路由到 `od-*` 表面技能（它们负责具体模板/检查清单）。

建议路由：

- 官网/落地页/产品介绍：`od-saas-landing`
- 定价与套餐对比：`od-pricing-page`；升级付费/会员：`od-pricing-upgrade`
- 后台/数据看板：`od-dashboard`；数据汇报摘要：`od-data-report`
- 手机 App 界面：`od-mobile-app`（多屏必先 `scaffold_mobile_mockup`，勿贴 HTML）；新用户引导：`od-mobile-onboarding`
- 登录注册验证：`od-login-flow`
- 营销邮件版面：`od-email-marketing`；社媒多图轮播：`od-social-carousel`
- 帮助中心/常见问题：`od-faq-page`；杂志长文：`od-article-magazine`
- 宣传海报/分享长图：`od-poster-hero`；线框结构草图：`od-wireframe-sketch`
- 杂志风演示稿：`od-deck-magazine`；简洁动画演示稿：可配合 `frontend-slides`
- 版本发布说明：`od-release-notes-one-pager`；求职简历：`od-resume`
- 编辑风页面：`od-after-hours-editorial` / `od-field-notes-editorial` / `od-editorial-burgundy`
- 金融/数据气质页：`od-digits-fintech`
- 研究决策看板：`od-research-decision-room`；创意作品集：`od-swiss-creative`
- 视频叙事脚本页：`od-swiss-user-research-video` / `od-weread-year-in-review-video` / `od-8bit-orbit-video`
- 页面精修打磨：`od-web-artifacts-builder`
- 候补名单 / 网页原型：`od-waitlist-page` / `od-web-prototype`
- 团队协作页：`od-team-okrs` / `od-kanban-board` / `od-meeting-notes`
- 文档与内容：`od-docs-page` / `od-blog-post` / `od-pm-spec`
- 财务 / 入职 / 游戏化：`od-finance-report` / `od-hr-onboarding` / `od-gamified-app`
- 瑞士风 Deck / X 分享卡：`od-deck-swiss` / `od-social-x-card`
- 审稿 / 手机流程线框（内部）：`od-creative-director` / `od-wireframe-mobile-flow`

### 4) 生成与自检

- 用户要求**官网实际大图 / 禁止 AI 生图**时：先读 `references/official-product-images.md`，用 `fetch_page_images`（首选）或 `web_fetch` 取 CDN 地址，**禁止** `web_search` 搜图与 `bash curl grep`。
- 生成 HTML 后，必须执行：
  - `references/anti-slop-checklist.md`
  - `references/critique.md`
- 若任一维度低于阈值，先修正再交付。

### 5) 交付规范

- 优先交付可直接预览的 HTML 文件（**`write_file` 落盘**到**系统分配的任务目录** `artifacts/task-*/`，细则见 `references/artifact-naming.md`）。**禁止**再写 `artifacts/design/` 语义目录。
- **创意视觉（海报/封面/杂志/落地页 Hero/轮播主卡）**：图片 API 可用且用户**未**要求官图时，先 `generate_image` 落盘 PNG 再写 HTML；禁止首轮 CSS/SVG 冒充主视觉。官图任务仍读 `references/official-product-images.md`，禁止 AI 冒充。
- 对话中必须引用**完整相对路径**（如 `artifacts/task-20260803-abcd1234/index.html`），禁止只写 `index.html`。
- **手机多屏示意**：路由 `od-mobile-app`，用 `scaffold_mobile_mockup`，禁止在对话中贴整页 `html` 代码块。
- **读技能附属文件**（清单、设计系统、取图规则）：用 `read_skill` 的 `relativePath`（如 `references/checklist.md`），**不要** `read_file skills/...`（租户工作区读不到）。
- 如用户要求，可补充导出 PDF 的操作步骤（复用现有 `frontend-slides` 流程）。

## 必读参考

- `references/directions.md`
- `references/brand-spec-protocol.md`
- `references/anti-slop-checklist.md`
- `references/critique.md`
- `references/render-workflow.md`
- `references/artifact-naming.md`（成果目录与时间戳，防多任务串台）
- `references/official-product-images.md`（官网大图 / 禁止生图任务必读）
- `references/question-flow.md`
- `references/design-systems/_index.md`

## 编排规则

- 本技能是“总控”，表面技能是“执行器”。
- 表面技能只处理具体产物，不重复定义完整设计哲学。
- 当用户仅说“做个页面/原型”，默认先走本技能再路由。

