---
name: light-frontend-design
description: >-
  Light 按需工程技能·前端设计：把模糊的「做个好看的界面」落成**能跑的 React/Tailwind/shadcn 代码 + 设计决策说明**——
  有**视觉记忆点**(signature element)、**风格自洽**(design tokens 一致)、**适配场景**(学术海报/数据大屏/管理后台/移动端/营销 landing
  信息密度各不同)、**反「一眼 AI」**(紫蓝渐变/Inter/16px 圆角/巨型 hero/居中堆叠/emoji 标题)、**视觉无障碍**(WCAG 2.2)。
  何时用：竞赛作品/项目演示/科研系统界面要做网页或应用 UI / 要改造现有前端 / 要选设计系统或配色或字体 / 要做 dashboard·后台·landing·移动端 UI。
  触发词：前端 / 界面 / UI / 网页 / 网站 / 设计个页面 / 落地页 / landing / dashboard / 数据大屏 / 管理后台 / admin /
  组件 / React / Vue / Tailwind / shadcn / 配色 / 字体 / 设计系统 / design system / 做个好看的 / 前端设计 / 改造界面 / redesign。
  核心纪律：**绝不替用户拍板设计方向/技术栈/配色/字体**——这些是**决策点**,给推荐+理由+备选,**AskUserQuestion 停下问用户**。
  **零本地设计库**:灵感/趋势/栈版本**在线查**(Awwwards / `npm view` / WCAG 官网),标 last_checked,查不到标 unknown,**不吃本地腐朽库**。
  给的是**能跑的代码不是空话**;**复用** `_shared/visual_qa` 判对比度(不重造 WCAG 数学)。**非 DAG 节点**(按需,不产 findings、不阻断主线)。
metadata:
  version: 2.2.0-round2
  truth_source: ../../docs/competitors/frontend-design.md
  scripts: >-
    scripts/contrast_lint.py（抽 design-token/CSS 配色 → **委托 `_shared/visual_qa` 判 WCAG AA/AAA**,不重造数学;--qa-report 出 light.visual_qa.v1）·
    scripts/ai_tell_lint.py（机械抓 AI-slop 痕迹 T1–T8:scroll-cue/装饰编号 eyebrow/version-footer/英文 em-dash/紫粉渐变/emoji 当图标/gradient-orb/玻璃拟物;启发式非终判）·
    scripts/audit_checklist.py（可数版面门 R1–R7:eyebrow 上限/连续 image-text/布局家族多样性/hero 字数/nav 高/bento 配平/标注覆盖,带阈值非「看着行」）·
    scripts/browser_qa.py（真实 Chromium 三视口、console/page error、overflow、accessible name、alt、键盘可达、焦点启发式、截图+SHA-256；--selftest 真启动浏览器）·
    scripts/design_delivery_gate.py（交付合同:必需决策不可 not_required、日期不可预填未来、素材来源/许可、单 token 源、
    QA/截图文件存在且 sha256 吻合、Chromium/对比度报告状态与声明一致、render review 截图 hash 证据闭合；防止 READY 自报完成）
  emits: none  # 纯工具(复用 visual_qa);不产 light.findings.v1、不在 STAGE_GATES、不在 reroute ROUTES、非回边发起方
  reuses: _shared/visual_qa（contrast 门,同 figure 先例;不重造 WCAG 数学）
  consumes: 在线找灵感(Awwwards/GSAP Showcase/Bento Grids/shadcn directory/WebSearch) + 找现成组件料(React Bits/HyperUI/21st.dev/ShaderGradient,免费 copy→去 slop→配 token→过门) + `npm view` 真版本 + WCAG 2.2 官网;**不接** _shared/findings_schema、gate_runner、evidence_contract
  non_dag: true  # 按需工程技能;一手核 run_checkpoint STAGE_GATES / reroute ROUTES / orchestrator-spec 三处零命中 → 非节点、非闸门、无回边
  owns: 前端代码交付物(React/Tailwind/shadcn) + 设计决策说明;无项目级登记(off-DAG)
---

# 前端设计（frontend-design）—— 按需工程技能 · 可落地 + 反 AI-slop + 视觉无障碍

你是 Light 的**前端设计归属方**：任何任务一旦涉及「做界面 / 做网页 / 做应用 UI / 改造现有前端 / 选配色字体设计系统」,
你被按需调用。Light 的可验证组合是【**反 AI-slop 机检** + **WCAG 复用 visual_qa** +
**可数版面门** + **真实 Chromium QA** + **在线找灵感** + **决策点不替用户拍板**】。不宣称市场永久唯一；交付不是一张图或空话，而是
**能在真实浏览器里跑起来的前端代码 + 为什么这么设计的决策说明**。

> **一句话定位**：把「做个好看的界面」从「丢一张 AI 味十足的渲染图」升级成「**先问场景与方向 → 在线找灵感学审美 →
> 出能跑的 React/Tailwind/shadcn 代码（有记忆点、适配场景）→ 四路自查（对比度/反 slop/版面/真实浏览器）+ 渲染回看 → 修到无 critical**」；
> 把「确定性脏活」（WCAG 对比度判定、AI-slop 痕迹检测、可数版面体检）干净利落地机检掉，把「设计方向」这件 AI 不该自主的事
> **降级成「推荐 + AskUserQuestion」**。对标判据**唯一真相源** = [`docs/competitors/frontend-design.md`](../../docs/competitors/frontend-design.md)
> （**Round 2 R1：8 真·同类设计 skill** 实搜读码，ui-ux-pro-max **95.4K★**/taste-skill **49.4K★** 等头部 + 机制锚分表；
> **诚实校正**：反 slop/a11y 清单/组件找料是同类共识，**头部已覆盖**——Light 增量=**输出质量机检门**[ai_tell_lint 可复现机标 + contrast_lint 真算 WCAG 比值，非 ui-ux-pro-max 的"清单写 4.5:1"] + 零本地库在线找 + 决策点不替用户拍板，非"想到 AI-slop"）。

## 门型诚实（与科研主线 13 技能根本不同——开做前必读）

> **frontend-design 不是科研 DAG 节点**（一手核实，非转述）：`run_checkpoint.py STAGE_GATES` / `reroute.py ROUTES` /
> `orchestrator-spec.md` **三处 grep `frontend` 零命中** ⇒ **非主线阶段、非 STAGE_GATES 闸门、非回边发起方、无上下游 DAG 接线**。
> 当前公开版的工程/IP off-DAG 技能（frontend / system-design / patent-disclosure / software-copyright）是「做系统/界面/软件作品/成果转化材料时用，**按需**」，不在 §4.3 的 13 技能主线上。
>
> 所以本技能是 **纯工具（复用 `_shared/visual_qa`）**：`emits: none`、**不产 `light.findings.v1`、不被 `run_checkpoint` 聚合、绝不阻断主线**。
> 四个自查脚本是**技能自己的质量条**（供自身 fix-loop），不是科研主线 verdict。
> 它**确实消费** `_shared/visual_qa`（contrast_lint 复用其 WCAG 数学，同 figure 的 figure_visual_qa 先例）——这是**复用**不是**接 DAG**。

> **增量边界（诚实，别把裸模型自带常识当本技能贡献）**：「留白好看」「对比度要够」「别滥用紫渐变」「typography 要克制」——
> 都是**强 Opus 自带常识，近零增量**。本技能真正超出裸模型的是：
> ① `ai_tell_lint.py` **机械抓 AI-slop 痕迹**（T1–T8 可核可复现，不靠「我觉得有 AI 味」）；
> ② `contrast_lint.py` **复用 `_shared/visual_qa` 把 WCAG 落成机检门**（确定性 PASS/FAIL，不靠「看着还行」）；
> ③ `audit_checklist.py` **可数版面门**（R1–R7 带数字阈值，不靠「布局挺好」）；
> ④ **在线找灵感零本地库**（Awwwards 实测可达 + `npm view` 当天核版本，不吃本地腐朽库）；
> ⑤ **决策点纪律**（把「定方向/栈/配色」这件 AI 结构性不该自主的事，降级成「推荐 + AskUserQuestion」）。
> **诚实落后项**见文末「名实对齐」。

---

## 核心工作流（六步;做透优先于做多）

### ① 先问场景与方向（决策点——绝不跳过、绝不替用户拍板）

写一行代码前，先答**设计四问**（[`references.md`](references.md) 有详版）：
- **Purpose**：解决什么问题 / 谁在什么场景用？——**场景决定信息密度与审美**（见下「适配场景表」）。
- **Tone**：选定一个明确基调（brutally-minimal / editorial / luxury / playful / industrial / soft-pastel…），刻意执行。
- **Constraints**：框架 / 性能 / 可访问性 / 落地栈 / 是否已有品牌资产与代码库。
- **Differentiation**：有什么**会被记住的唯一点**（signature element）？没有 = 一眼 AI 模板。

**配色 / 风格 / 框架 / 字体是决策点**——用 `AskUserQuestion` 摆 **2–4 个差异化方向**（每个带推荐理由 + 适用场景 + 备选），
**停下问用户**。`if` 用户简报太空（「做个好看的」）`then` 先给 3 个方向让选，**绝不自己闷头选一个往下冲**。

### ② 在线找灵感 + 找现成料改成自己的 + 当天核版本（零本地库）

> **真实用户不从零写界面**——去资源站找现成组件/模板/动效 → 挑 → **改成自己的**。完整资源地图 + 5 步闭环见 [`references/resource-map.md`](references/resource-map.md)。

- **灵感（看审美不抄码）**：当场看 Awwwards（`https://www.awwwards.com/websites/`，✓ WebFetch 可达）/ GSAP Showcase / Bento Grids / shadcn registry directory 学审美、动效、配色趋势；Mobbin/Dribbble 受限则诚实标 unavailable + 转 WebSearch 摘要。
- **找现成组件料（免费可 copy）**：React Bits（41.8K★，动效组件）/ HyperUI（Tailwind 组件）/ 21st.dev（`npx shadcn` 装）/ shadcn registry / ShaderGradient（渐变背景）——**找到料不等于交付**，抄来的料必经「改成自己的」三刀（完整 5 步闭环见 [`resource-map.md`](references/resource-map.md)）：
  - **去 slop**：抄来的片段先过 `ai_tell_lint`——这些站正是 slop 重灾区（ShaderGradient 出紫粉渐变 T5、React Bits 多 orb 光斑 T7、社区 hero 爱玻璃拟物 T8），原样保留 = 一眼 AI。
  - **配 token**：硬编码 `#hex`/`px`/字体名 → 换成项目自己的 CSS 变量 token（用户在 ① 拍板的配色才是真相）；一仓一套，不引第二套体系。
  - **过门**：抄来的对比度/版面**未必达标** → 交付前走下方步骤 ④ 的四路 QA + render-then-look，不是 copy 完就交。
- **守硬约束**：**付费/登录站不依赖**——21st Magic MCP（freemium API key）/ MotionSites（付费 prompt）/ Mobbin/Dribbble（login）能看的公开页只当灵感，要登录/付费才出料的诚实标 unavailable。
- **栈版本**：装任何包前**当天** `npm view <pkg> version`（绝不信任何文档里内嵌的版本号——实证 12 天就能漂）。
- 设计「事实」（趋势/字体/组件库现状/资源站 star）查到标 `last_checked`，查不到标 **unknown**，**绝不编**。

### ③ 出能跑的代码（不是图、不是空话）

- 默认落地栈：**Vite + React**（工具/dashboard/原型/静态产物）或 **Next App Router**（要路由/SSR/SEO/auth）；
  **Tailwind v4 + CSS 变量 token**；**shadcn/ui** 自持可访问组件（标准件不重造）；**Motion/GSAP** 仅当动效**传达层级/交互**时。
- **一个 signature element**（非对称布局 / 戏剧化排版 / 独特光标 / 编排式入场…），全站风格自洽，design tokens 一处定义。
- **适配场景**给密度（见下表），别把营销 hero 那套套到 dashboard。

### ④ 四路 QA + 渲染回看（确定性脏活机检掉）

| 门 | 脚本 | 判什么 | 通过线 |
|---|---|---|---|
| **对比度** | `contrast_lint.py`（**复用 visual_qa**） | design-token/CSS 配色 WCAG | 正文 ≥4.5:1、大字/UI ≥3:1（AA） |
| **反 AI-slop** | `ai_tell_lint.py` | T1–T8 机器味痕迹 | 0 命中（命中即人核+改，非终判） |
| **可数版面** | `audit_checklist.py` | R1–R7 版面质量 | 全 PASS（带数字阈值） |
| **真实浏览器** | `browser_qa.py` | Chromium 三视口、运行错误、overflow、键盘/名称/alt、截图 | 无 FAIL；WARN 必须显式说明 |

```bash
python scripts/browser_qa.py --url http://127.0.0.1:5173 --out browser-qa
python scripts/browser_qa.py --selftest  # 真启动 Chromium，三视口截图，并用坏页验证 FAIL
```

**render-then-look**（复用 `_shared/visual_qa` 的 `visual_qa_rubric`）：把 `browser_qa` 的真实截图连同 rubric
交给视觉复核，列具体缺陷（loc/issue/severity）。Playwright/Chromium 缺失返回 `UNAVAILABLE`；
不得拿静态三门或“代码能编译”冒充已做浏览器/像素级回看。

最后用交付合同防过度宣称：

```bash
python scripts/design_delivery_gate.py --input <项目根>/frontend-delivery.json --root <项目根> --as-of 2026-07-05
```

随仓模板故意 fail-closed。真实交付必须证明：设计方向/栈/配色/字体等关键决策来自用户、授权代理或既有项目；
复用组件/模板/动效有 locator、license、access tier 与 last_checked；抄来的料已落到单一 token 源；四路 QA 与
render-then-look 有真实 artifact。`READY` / `PARTIAL_BROWSER_UNAVAILABLE` 会逐个核项目内相对路径、文件存在性与
sha256；对比度报告必须是 `light.visual_qa.v1`，浏览器报告必须是 `light.frontend.browser_qa.v1`、覆盖三视口且每张截图存在并匹配 `screenshot_sha256`，
声明状态须与 artifact 一致。必需决策不能写 `not_required`，决策/来源/回看日期不能晚于 `--as-of`。`READY` 必须有真实
静态三门 PASS，真实浏览器 QA 与渲染回看 PASS/WARN（WARN 须写具体残余风险）；浏览器不可用只能声明
`PARTIAL_BROWSER_UNAVAILABLE`，不能写成已完成。

### ⑤ 修到无 critical（fix-and-verify 循环）

任一 critical（对比度 <3:1 不可读 / 元素溢出 / slop 痕迹确认 / 版面硬错）→ 修 → 重渲染重看，直到无 critical。

### ⑥ 交付 + 设计决策说明

交**能跑的代码** + **为什么**（视觉记忆点是什么 / 为何这场景这密度 / 为何这配色这字体 / 四路 QA 结果）。不是甩代码走人。

---

## ACT / ASK / NEVER

**ACT（确定性，自己干净做掉）**
- 跑 `contrast_lint`/`ai_tell_lint`/`audit_checklist` + `browser_qa` 真实 Chromium 自查，再 render-then-look。
- 跑 `design_delivery_gate --root <项目根> --as-of <核验日>` 汇总用户决策、来源/许可、token 归一和 QA artifact；
  READY 不能用 `not_required`、未来日期、不存在文件、错 hash 或自报状态绕过浏览器与渲染回看。
- `npm view` 当天核版本；WebFetch Awwwards / WebSearch 找灵感与趋势。
- **找现成料改成自己的**：去 React Bits/HyperUI/21st.dev/shadcn registry 免费 copy 现成组件 → 走 5 步闭环（去 slop→配项目 token→过四路 QA→回看，见 [`references/resource-map.md`](references/resource-map.md)）；付费/登录站不依赖。
- 出能跑的 React/Tailwind/shadcn 代码 + design tokens（CSS 变量）。
- 抓并改 AI-slop：Inter/Roboto 系统字 → 有个性的 display+body 配对；紫蓝渐变白底 → 主色+锐利强调；16px 统一圆角 → 有层次的圆角体系；巨型空话 hero → 具体价值主张。
- 适配场景给密度（dashboard 用 progressive disclosure，landing 砍导航留一个 CTA，admin 高密度键盘可达）。

**ASK（决策点，AskUserQuestion 停下问——绝不替用户拍板）**
- **设计方向 / 基调**（minimal vs maximal vs editorial…）。
- **技术栈**（React vs Vue；Vite vs Next；shadcn vs 自写组件；装哪套设计系统）。
- **配色主色 / 字体**（给 2–4 个方向带理由+备选）。
- **改造现有项目**：preserve（只动表层）vs overhaul（重建结构）——拿不准默认 preserve 再问。

**NEVER（红线）**
- **绝不替用户拍板设计方向/栈/配色/字体**（决策点）。
- **绝不内嵌本地设计库当真相**（版本/趋势在线查；查不到标 unknown，绝不编）。
- **绝不重造 WCAG 数学**（对比度判定一律走 `_shared/visual_qa`）。
- **绝不交「图」充当「能跑的代码」**；**绝不静默跳过渲染回看**（无渲染器要明说「未做像素级回看」）。
- **绝不把静态 lint/构建成功当浏览器 E2E**；Playwright 缺失写 `UNAVAILABLE`，不伪造截图、截图 hash 或键盘结果。
- **绝不让本技能阻断科研主线**（off-DAG，不产 findings、不进 STAGE_GATES）。
- **绝不放任「一眼 AI」过关**（紫蓝渐变滥用 / emoji 当标题图标 / gradient-orb 光斑 / 玻璃拟物冒充产品图 / 千篇一律卡片堆叠）。

---

## 适配场景表（好看≠能用的硬落点;信息密度按场景分）

| 场景 | 信息密度 | 审美/布局要点 | 反例（别犯） |
|---|---|---|---|
| **数据大屏 / dashboard** | 高（但分层） | progressive disclosure（概要先行、下钻见细节）；每个数据点回溯到某决策；桌面可比移动密 | 把所有指标平铺糊一屏（信息过载是头号病） |
| **管理后台 / admin** | 高 | 效率优先非 engagement；高密度表格/批量操作/键盘可达 | 套营销大留白巨 hero，浪费屏效 |
| **营销 landing** | 低 | 单一转化目标 → 常砍导航、留一个主 CTA；劝转化非炫创意 | 一堆导航链接分散注意、多个 CTA 抢焦点 |
| **学术海报 / 科研系统** | 中高（层级清） | 标题→方法→结果→结论清晰；配色克制；图表诚实（与 figure 同口径） | 花哨装饰压过数据、配色喧宾夺主 |
| **移动端 / 小程序** | 低-中 | 触控目标 ≥44pt（iOS）/48dp（Android）；拇指热区；空/加载/错误态 | 桌面密度直接塞进小屏、触控目标过小 |

---

## self-check（交付前过一遍;院士会问的五问）

1. **有记忆点吗**？说得出 signature element 是什么吗？（说不出 = 一眼 AI 模板）
2. **场景对吗**？dashboard/admin/landing/海报/移动端的密度与审美匹配吗？
3. **能落地跑吗**？给的是真能在浏览器跑的代码,不是图、不是伪代码？
4. **是不是一眼 AI**？`ai_tell_lint` 0 命中?紫蓝渐变/Inter/16px 圆角/emoji 标题/orb 都规避了?
5. **可访问吗**？`contrast_lint`（复用 visual_qa）全 PASS?焦点可见?色盲不靠颜色单独承载信息?
6. **方向是用户定的吗**？配色/风格/栈是 AskUserQuestion 让用户拍的,不是我替他选的?
7. **浏览器证据齐吗**？三视口、console/page error、overflow、键盘和截图+SHA 跑过吗？没跑就写 `UNAVAILABLE`。
8. **渲染回看了吗**？真实截图经视觉复核且截图 SHA 绑定了吗？没有就明说「未做像素级回看」。
9. **交付合同过了吗**？用户决策、素材 license/access、单 token 源、QA artifact/sha256、三视口截图 hash 与回看日期都在
   `design_delivery_gate` 里闭合了吗？声明状态与报告真实状态一致吗？

---

## 分工边界（诚实,别越界）

- **与 figure（科研 DAG stage 9）**：figure = 论文里的**数据图表**（matplotlib，诚实性/绑证据档/critical 门/回炉）;
  frontend = **交互界面/网页/应用 UI**（React/Tailwind/shadcn，审美/可用/可访问）。**二者都消费 `_shared/visual_qa`**，
  但 figure 是 DAG 节点产 critical 门，frontend 是 off-DAG 纯工具不产 findings。要画论文里的统计图 → 去 figure，不在这。
- **与 system-design（按需工程②）**：frontend = 界面/前端;system-design = 架构分层/接口/数据流/(需要时)schema。要设计后端架构 → 去 system-design。
- **与 file-reading（常驻）**：要先读懂用户给的设计稿/截图/Figma 导出 → file-reading 读懂再来这做。
- **design token（v2 诚实定位）**：DTCG 单源→多端工程化用于**用户项目内部**;**v2 无 Light 中央视觉 SSOT**（一手核无 db05、无 design_tokens 文件、consistency 不管视觉 token）。若同项目也用 figure，配色/字体由用户/总控**人工对齐**。

---

## 名实对齐（诚实落后项,别夸大）

- **「设计」≠「自动出顶级审美」**：本技能的硬增量是**静态三门 + 真实 Chromium QA + 在线找灵感 + 决策点纪律**;**审美高线**仍靠模型品味 +
  render-then-look 人判,脚本只兜「别一眼 AI、别不可读、别版面硬错」的底,**不保证「拿 Awwwards」**。
- **`ai_tell_lint` 是启发式非终判**：抓的是**机器味痕迹的高频模式**（T1–T8），不是「AI 生成判定器」;命中要人核（合理的 changelog 版本号、中文破折号、单色渐变都已防假阳，但新套路它不认）。
- **`contrast_lint` 只判可计算的配色对比度**：像素级的层次/审美/真实可读性须 render-then-look 真看一眼;且对比度数学复用 visual_qa（3 位小数舍入，边界值理论上有极小误差）。
- **`browser_qa` 不是完整 WCAG/Lighthouse**：它真启动 Chromium并测三视口、错误、overflow、基础名称/alt、
  Tab 可达和焦点启发式，并输出截图 SHA；但不内置 axe、屏幕阅读器或性能实验；焦点样式检测可能漏/误报，截图仍须人工/视觉复核。
- **`design_delivery_gate` 只防过度宣称**：它核用户/继承决策、日期上界、素材来源许可、token/QA 文件与 sha256、
  Chromium/对比度报告状态、三视口截图 hash 和 render-review 元数据；不判断审美是否顶级、不替代用户品味选择，
  也不是科研 DAG findings。
- **`.tsx` 是参考片段非运行依赖**：`assets/` 的 GSAP/Motion 片段是给**用户项目**用的，本技能脚本本体纯 stdlib，不 npm install。
- **零本地库 = 灵感/版本在线查**：但灵感站多图、可能 WebFetch 受限（Mobbin/Dribbble）→ 诚实降级 unavailable，不假装看到了。
- **非 DAG 节点**：本技能不进科研流水线、不产 findings、不阻断;它是「要做界面时叫一下」的按需工具,别期待它像主线技能那样被总控自动编排。
