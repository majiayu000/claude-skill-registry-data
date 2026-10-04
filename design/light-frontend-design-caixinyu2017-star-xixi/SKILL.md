---
name: light-frontend-design
description: 独特吸睛、审美好、有特色、美观全面的前端设计。当任务涉及前端界面、项目展示页、系统演示、大屏可视化、可视化平台、微信小程序 UI、移动端界面、设计系统、Tailwind v4、shadcn/ui、Next.js、React、Vite、可访问性、动效、重设计审计时使用。不只是能用，而是好看、统一、清晰、有亮点、有视觉记忆点，适合展示/答辩/演示/落地。按主题选风格：科技感、学术感、农业智慧化、数据可视化、极简、玻璃拟态、卡片式、大屏、管理系统、移动端、小程序等。
user-invocable: false
---

# 有审美的前端设计

> **代号词表**（本技能频繁引用的编号，首次见此）：
> - **db05** = 设计系统库（`databases/db05-frontend-styles/`，前端/可视化设计规范 + 范式卡 + `design_tokens.template.json` 视觉真相源）。
> - **db09** = 项目状态库（`databases/db09-projects/`，跨会话项目记忆：项目卡 / 术语表 / 决策日志 / `palette.json` 取色源）。
> - **a04** = system-design（系统设计 / 数据库 / 接口 / ER 图，前端数据接口对接它）。
> - **a07** = consistency（一致性常驻技能，统一项目 palette、PPT / 论文图 / 前端同源视觉）。
> - **m11** = figure-drawing（论文图绘制，与前端共享 palette）。
> - **m16** = slides（答辩 / 路演 PPT，与前端协调视觉风格）。

## 先定设计方向（写码前必答四问，来自 frontend-design skill）
1. **Purpose**：解决什么问题、谁在用、什么场景(答辩/大屏/后台)。
2. **Tone**：从基调谱系选一个并押注到底——科技/学术/农业智慧化/医疗/极简/玻璃拟态/卡片/大屏/管理系统/移动端，或 editorial/brutalist/luxury/organic。先 web 搜索核实涉及的具名产品/品牌(10 秒搜索胜过 1-2 小时返工)。
3. **Constraints**：框架、性能、可访问性、信息密度。
4. **Differentiation**：一个会被记住的唯一视觉/交互记忆点(不是堆特效)。
据此定 **设计语言**：调色板(主/辅/强调/中性) + 字体系统 + 间距栅格 + 圆角阴影 + 图标风格，落到 Design Tokens，登记 db05。**项目有 `databases/db09-projects/projects/<project_name>/palette.json` 则必用其取色**（与论文图 m11/PPT m16 共享的视觉 SSOT 实例，前端不另立色板；schema 见 db09 README，色值锚点真相源是 db05 `design_tokens.template.json`）。设计长在已有语境(品牌/代码库/UI kit/真实截图)上而非凭空造。简报太空(如"做个好看的")时进 Advisor 模式：从风格库提 3 个差异化方向让用户选，再押注其一(canvas-design)。涉及品牌则先按 Core Asset Protocol 收集 logo/产品图/UI 截图/品牌色字，写入 brand-spec.md 当一等公民。
设计系统持久化：用一个全局真相源(如 MASTER.md/design tokens)+ 页级覆盖文件(页文件覆盖全局，无页文件则用全局)，避免跨页风格漂移(ui-ux-pro-max)。
取 db05 卡时按项目学科用 `domain_scope=` 过滤(如农业项目看 general + agri-tech 卡,不被他方向偏科卡干扰;无标注的卡默认 general 对所有可见)。引用任何组件库 license/版本时**不信卡内散文**,跑 `databases/db05-frontend-styles/scripts/style_signal.py --npm <包名>` 实时查 registry.npmjs.org,冲突信官方在线源、无网用快照并标 stale;Pro/定价层无 API,指向官方 pricing 页人工核。

## 设计原则（可量化）
- 视觉层次清晰，留白充足，对齐严格；"主色 + 锐利强调色" 优于均匀分布的怯懦调色板。
- 字体：避开 Inter/Roboto/Arial/系统字体，展示字配精炼正文字，pair 出个性。
- 一致性：组件复用、token 化、风格统一(a07)；用 CSS 变量承载主题。
- 可访问性(WCAG 2.1 AA)：正文对比 ≥4.5:1、大字 ≥3:1、UI 组件 ≥3:1；键盘可达 + 焦点态可见；颜色不作唯一信息载体；图片有意义 alt；尊重 prefers-reduced-motion。完整阈值/触控目标/4-8pt 栅格判据见 [references/visual-a11y-rules.md](references/visual-a11y-rules.md)；玻璃拟态/新拟物等范式专属 a11y 风险见 db05 对应卡 implementation_notes。
- 克制动效：HTML 优先纯 CSS、React 用 Motion/GSAP；一次编排良好的页面载入 + 错峰揭示(animation-delay) > 散落微交互；hover/交互过渡 150-300ms。
- **反 AI-slop 禁令**：紫/粉渐变配白底、emoji 当图标(用 SVG: Lucide/Heroicons)、rounded-card-左边框、gradient-orb 代表 AI、CSS 剪影冒充产品图、千篇一律模板布局。
- 可调三旋钮(taste-skill)：VARIANCE(布局实验度)/MOTION(动效深度)/DENSITY(每屏信息量)，按场景拨——大屏调高 DENSITY，落地页调高 VARIANCE，后台调低两者。

## 技术实现（按需，见 a09）
栈选型与各框架的可执行要点（命令/选项/已知坑）见 `references.md` 与 `references/ecosystem-2026.md`，正文只给决策级提示：
- **Next.js**：默认 Server Components（零客户端 JS），按需 `"use client"` 并守边界防 bundle 膨胀；loading.tsx+Suspense 流式、并行取数、next/font 防 layout shift、`<Image>` 防 CLS；Server Actions 内逐个鉴权；上线前 `next build`+Lighthouse。（细节见 references「next-best-practices」节。）
- **shadcn/ui**：`npx shadcn@latest init` 后 `add [component]` 把源码拷进项目自维护，主题走 CSS 变量，升级手动 diff。（CLI 选项见 references「shadcn/ui」节。）
- **Tailwind v4**：CSS-first（`@import "tailwindcss"` + `@theme` 暴露 token），变体可叠、移动优先，复用走组件而非滥抽 class。
- **组件 API 设计**：组合优于布尔属性、compound+context、只暴露 `{state,actions,meta}`、显式变体优于布尔。（vercel-composition-patterns，见 references。）
- **移动端/小程序**：触控目标 iOS ≥44pt/Android ≥48dp、正文 ≥16、tabBar 3-5；小程序组件库在 TDesign/Vant/WeUI/Ant Design Mini/NutUI Taro 选一不混搭。
- **可视化**：ECharts/D3/Plotly/大屏，色板统一、密度与可读性平衡。
- **设计 token 多端一致**：用 Style Dictionary / Terrazzo 把 token 从单一源编译到 CSS/JS 多端；权威源对齐 db05 `design_tokens.template.json`（DTCG 视觉 SSOT，a07 维护），前端不另立色板/字阶。细节见 `references/ecosystem-2026.md`「设计 token 工程化」节。

## 灵感来源（学版式不抄袭）
- **热门 skill 雷达**：需要更新技能或选择外部设计能力时，先看 `references/ecosystem-2026.md`，优先吸收官方/高安装量/可验证的 workflow，而不是安装未知低信号包。
- **Mobbin**：真实生产 App(iOS/Android/web)的截图与用户流程——定信息架构/交互顺序前，先找 2-3 个同类真实 flow 对照。
- **Awwwards**：高水准网页创意，并直接借用其评审 rubric 自评(见下)。
- 其余：Dribbble、Behance、Land-book、Godly、Siteinspire、Figma Community、Tailwind UI、Vercel templates。总结"为什么好看、适合什么场景、需要哪些组件"，沉淀进 db05。
- **Figma MCP（读设计稿→前端实现）**：已有 Figma 设计稿时，用官方 Figma MCP server 把选中 frame 的布局/样式/design context 喂给 AI 在 IDE 里直接出码（适合科研工具/数据标注界面/项目主页）。**Remote server 免费账号即可用，能读也能写 canvas**（写功能 beta 期免费）；Desktop 版需付费 seat。热门社区 GLips/Figma-Context-MCP（~15.1k★，实测 2026-06）专做"Figma 链接→喂 AI 编码"。注意：Figma MCP 用于**前端界面**，不用于生成论文 figure（学术 figure 无可靠 MCP 实践、且论文图须程序化绘制）。
- **image-to-code 三段法(taste-skill)**：拿不准视觉方向时，先 Generate(出参考板/hero 图)→ Analyze(拆版式/字体/间距/动效线索)→ Implement(照参考帧出码)，比直接凭空写更稳。

## 机械门禁（脚本即真相，规则全文见脚本 selftest）
三个 linter 把"好看"落成可数判定，交付前必过；都支持 `python <脚本> <文件>`（或 `-` 读 stdin）真实输入与 `--selftest` 自测两种模式：
- **可数 checklist** `python scripts/audit_checklist.py <file.html>`（给页面元素加 `data-*` 标注后跑）：R1 eyebrow ≤ceil(sections/3)、R2 连续图文 split ≤2、R3 ≥8 段需 ≥4 种 layout family、R4 hero 副文 ≤20 词/≤4 行、R5 nav 单行 ≤80px、R6 bento N 内容=N 格、R7 nav/hero/bento 关键元素出现却未标注 `data-*` 即 FAIL（防 R4/R5/R6 在没看见的数据上空过）。自带 GOOD/BAD/UNANNOTATED 自测。
- **反 AI-tell 黑名单** `python scripts/ai_tell_lint.py <file>`：T1 scroll cue、T2 装饰性段落编号 eyebrow、T3 版本/Made-with 填充页脚（裸 vX.Y.Z 仅在页脚上下文才算，changelog 列版本不误杀）、T4 英文正文 em-dash（仅扫 HTML 文本节点、排除 CSS/JS/注释/字符串，且与中文相邻的合法破折号不报）——命中即改。自带 DIRTY/CLEAN/CLEAN_TRICKY 自测。
- **对比度门禁** `python scripts/contrast_lint.py <tokens.json|styles.css>`：解析 token/CSS 变量 hex，按 WCAG 相对亮度算两两对比度，按 [references/visual-a11y-rules.md](references/visual-a11y-rules.md) 阈值（正文 4.5:1 / 大字 3:1 / UI 3:1）判 PASS/FAIL。纯 stdlib，JSON 支持 DTCG `$value` 树与显式 `pairs` 指定角色。自带自测。

## 字体与禁用清单（全表见 references/fonts-and-colors.md）
- Sans display 默认池：Geist / General Sans / Satoshi / Clash Display / Cabinet Grotesk；正文配对组合见 references。
- **硬禁**：serif 禁 Fraunces / Instrument Serif（已成 AI-tell）；色禁 premium-consumer「米色#F5F0E8 族+黄铜#B08D57 族+酱黑#1A1714 族」整族 + 紫/粉渐变配白底；正文字避开 Inter/Roboto/Arial/系统字体。

## brief → 官方设计系统映射（见 references/design-systems-map.md）
按 brief 信号选**唯一一套**：Fluent(Office/Teams) / Carbon(数据后台) / Polaris(电商) / Atlaskit(协作) / Primer(devtool) / govuk-frontend(英政府) / USWDS(美政府) / Radix(自建底座)。一仓一套、版本固定（表内 npm 包名与版本经 `curl registry.npmjs.org` 实测 HTTP 200）。

## redesign 审计协议（见 references/redesign-audit.md）
改造已有项目：detect(preserve vs overhaul) → audit 4 轴(Layout/Spacing/Hierarchy/Styling) → preservation rules(守住 IA/品牌/已达标无障碍) → modernisation levers → 改造 vs 重做决策树。

## 可运行代码骨架（assets/，含 prefers-reduced-motion + cleanup）
直接拷进 Next.js client component 或 Vite+React 项目：
- `assets/gsap-sticky-stack.tsx` — GSAP ScrollTrigger 粘性堆叠卡片（gsap.context + ctx.revert 清理）。
- `assets/gsap-horizontal-pan.tsx` — 纵向滚动驱动横向 pan，pin+scrub，reduced-motion 回退原生 overflow。
- `assets/motion-scroll-reveal.tsx` — framer-motion 错峰滚动揭示，useReducedMotion 关动效，observer 自动清理。

## 自评 rubric（交付前必过）
- **Awwwards 维度**：Design 40% / Usability 30% / Creativity 20% / Content 10%，给自己打分，低于 6.5 重做(Awwwards 中 6.5+ 才得 Honorable Mention，开发奖需 >7)。
- **可执行 checklist**：不用 emoji 当图标；所有可点元素 cursor-pointer；hover 态平滑过渡 150-300ms；浅色文字对比 ≥4.5:1；键盘焦点态可见；尊重 prefers-reduced-motion；响应式断点 375/768/1024/1440px 全测；制品在真实浏览器干净加载。
- **机械门禁（必须全过）**：`python scripts/audit_checklist.py <file.html>` 7/7 + `python scripts/ai_tell_lint.py <file>` CLEAN + `python scripts/contrast_lint.py <tokens.json>` 全 PASS。

## 场景适配
- **答辩/演示**：重展示力、首屏冲击、核心数据突出。
- **数据平台/大屏**：信息密度与可读性平衡、实时感、统一色板。
- **落地系统**：可用性 > 炫技，管理系统风规范化。

## 产出
可运行前端代码 + 设计说明(风格/色板/字体/组件清单) + 截图。设计系统登记 db05 与 db09。

## 衔接
数据接口对接 a04；与 PPT(m16)/论文图(m11) 视觉风格协调(a07)；无鉴权接口风险提示(security_awareness)。同一项目 palette 由 a07 统一，前端配色与 PPT/论文图同源，不另起一套。

---
逐工具核查笔记(真实端点/命令/参数/坑)见同目录 references.md。
热门技能/前端栈版本快照见 `references/ecosystem-2026.md`。
机械门禁脚本见 scripts/；可运行代码骨架见 assets/；字体色彩/设计系统/redesign 协议见 references/ 目录。
