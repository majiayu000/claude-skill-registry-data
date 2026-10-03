---
name: baku-design-system
description: 当 Codex 需要为 Baku/Basic-XYZ 个人品牌构建 HTML 页面、个人网站、教程页、介绍页、landing page、App 型页面、作品集、图文卡片、小红书卡片，或需要根据品牌 DNA 与多套页面风格设计/更新个人虚拟形象、头像和视觉规范时使用。适用于前端视觉设计、品牌页面、Notion 风格暖白文档页、Baku workbench 工作台页、复古未来/主机终端/暗色技术作品集页面、图文转卡片、个人 IP 形象、设计系统复用和模板化 HTML 交付。
---

# Baku Design System

## 概览

用 Baku 的品牌 DNA 生成可直接打开的 HTML 页面、图文卡片和个人虚拟形象。这个 skill 复用 `esther-design-system` 的结构：先读品牌 DNA，再选择页面风格和场景参考，最后用 checklist 验收；但颜色、字体、气质和头像都换成 Baku 自己的方向。

## 8 步工作流

1. 澄清需求。
   只问缺失的必要信息：类型、受众、屏数/卡片数、已有文案或素材、硬约束。用户已经给出明确内容时不要重复问。

2. 读取品牌 DNA。
   必读 `brand-dna.md`。如果用户说“换颜色、字体、气质关键词”，直接更新这个文件，不要把变化散落到模板里。

3. 选择视觉风格。
   默认使用 `references/style-baku-workbench.md`。如果用户提到 Notion、暖白、文档型官网、极简产品页、notion-like，但又明确不想替换 Baku 主风格，则读取 `references/style-notion.md`。如果用户提到复古未来、retro future、mainframe、terminal、暗色技术作品集、个人网站那种黑底网格霓虹风，则读取 `references/style-retro-future-mainframe.md`。不要把多套风格混在同一页面里，除非用户明确要求混合。

4. 根据场景读取参考。
   - 教程型、介绍型、科普型：`references/scene-tutorial.md`
   - 活动页、分享会、landing page：`references/scene-landing.md`
   - App 型、工具型、看板型页面：`references/scene-app.md`
   - 图文卡片、小红书卡片、文章转卡片：`references/scene-cards.md`
   - 个人虚拟形象或头像：`references/virtual-avatar.md`

5. 从模板开始。
   优先复制并修改 `assets/template-tutorial.html`、`assets/template-landing.html`、`assets/template-app.html`、`assets/template-cards.html`、`assets/template-notion.html` 或 `assets/template-retro-future.html`。Notion Warm Doc 风格优先从 `assets/template-notion.html` 开始；Retro Future Mainframe 风格优先从 `assets/template-retro-future.html` 开始。不要从空白 HTML 开始，除非用户明确要求。

6. 组合布局和组件。
   从 `references/layouts.md` 选择 3-5 种布局模式，从 `references/components.md` 选择组件。每个主要 section 的布局应有差异，避免整页都是同一种卡片网格。

7. 处理虚拟形象。
   默认兼容头像资产是 `assets/avatar.jpg`，多头像库在 `assets/avatars/`。头像不是所有页面的必选项；只有个人介绍、作者页、品牌页、图文卡片封面或用户明确要求使用 Baku 形象时才放头像。使用前读取 `references/virtual-avatar.md`，按页面风格选择合适头像，不要每次机械使用同一张。

8. 自检并交付。
   对照 `references/checklist.md`，P0 项必须全过。最终交付 HTML 文件、更新过的品牌文件或头像资产，并说明验证方式。

## 沟通调整位

- 改品牌：编辑 `brand-dna.md`，集中调整颜色、字体、气质关键词、禁忌和头像使用规则。
- 换默认头像：替换 `assets/avatar.jpg`，保持文件名不变，避免旧模板引用失效。
- 扩展头像库：把新头像放入 `assets/avatars/`，使用 `baku-avatar-风格-场景.png` 命名，并同步更新 `references/virtual-avatar.md` 的选择规则。
- 改模板：优先改对应 `assets/template-*.html`，再把可复用规则沉淀回 `references/`。

## 场景速查

| 需求 | 读取 | 起点 |
|---|---|---|
| 教程/介绍/科普页 | `references/scene-tutorial.md` | `assets/template-tutorial.html` |
| 活动页/Landing | `references/scene-landing.md` | `assets/template-landing.html` |
| App/工具/看板 | `references/scene-app.md` | `assets/template-app.html` |
| 图文卡片/小红书 | `references/scene-cards.md` | `assets/template-cards.html` |
| 虚拟形象/头像 | `references/virtual-avatar.md` | `assets/avatar.jpg`、`assets/avatars/` |
| Notion 暖白文档页 | `references/style-notion.md` | `assets/template-notion.html` |
| 复古未来个人网站/暗色技术作品集 | `references/style-retro-future-mainframe.md` | `assets/template-retro-future.html` |

## 风格速查

| 风格 | 读取 | 适合 |
|---|---|---|
| Baku Workbench | `references/style-baku-workbench.md` | 工程报告、流程说明、工作台、技术总结、个人品牌页 |
| Notion Warm Doc | `references/style-notion.md` | 暖白文档页、产品说明、知识库、极简 landing、内容型官网 |
| Retro Future Mainframe | `references/style-retro-future-mainframe.md` | 个人网站、AI workbench、暗色技术作品集、主机终端感 landing、项目 case study |

## 关键原则

- Baku 的视觉应该像“有工程判断的个人工作台”，不是通用 SaaS 模板。
- 页面第一屏必须让人知道这是 Baku/Basic-XYZ 的东西，不只在 nav 里出现小字。
- 颜色要克制但有识别度；用户明确偏好黑色、暖白和 Baku Yellow。避免蓝紫渐变、玻璃拟态、AI 光效和泛滥卡片。
- 文案要像真实工程师在说话，短、具体、可验证。
- 产物必须可落地：HTML 能打开，图文卡片能截图，头像路径能被模板引用。
