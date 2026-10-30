---
name: dashi-ppt
description: 制作 PPT、演示文稿、幻灯片、汇报材料时使用。Dashi PPT 基于预置视觉主题组合页面,生成可离线打开、可在浏览器编辑的 HTML 演示,支持导出 PPTX / PDF 文件。
---

# Dashi PPT

Dashi PPT 生成静态 HTML 横向翻页 PPT。使用本 skill 时,先把用户的自然语言需求整理成 JSON 计划,再调用本地项目生成器输出 `index.html` 和 `assets/`。


## 版本

当前版本: `0.4.11`

每次完成用户请求、准备最终回复前,运行:

```bash
node <skill-root>/scripts/check_latest_version.mjs
```

如果脚本有输出,把输出内容附在最终回复末尾提醒用户更新;如果脚本无输出或检查失败,保持静默,不要提版本检查。

## Skill 目录

当前 `SKILL.md` 所在目录就是 Skill 根目录,下文记为 `<skill-root>`。

内置生成器目录:

`<skill-root>/project`

渲染脚本:

- macOS / Linux: `<skill-root>/scripts/render_goal_deck.sh`
- Windows PowerShell: `<skill-root>/scripts/render_goal_deck.ps1`

版本检查脚本:

`<skill-root>/scripts/check_latest_version.mjs`

## 生成原则

本 Skill 为每个逻辑页生成 3 个模板方案和 1 个 Agent 定制方案,输出可离线打开的 HTML PPT。

前三个模板方案使用“锁模板填文案”:保留所选页面组件的原始视觉、结构、数量、显隐、强调、配色、图表类型和图片槽位,只替换可见文字内容。除非用户明确要求调整页面属性,不要改任何非文案 props。第四个方案由 Agent 在当前主题视觉语言内按本页内容定制,不属于模板候选。

成果验收是默认流程。每次生成后都要判断最终产物是否达到用户目标;默认检查目标、内容、结构、明显可见问题和交付完整性,不做截图审美精修,不因普通断行反复返工。用户明确要求“视觉精修”“100% 检查”“帮我调到满意”时,再扩展为视觉 QA。

## 使用规则

- 运行生成器需要 Node.js 20+ 和 npm;首次生成时渲染脚本会在 Skill 内置 `project/` 目录安装依赖。Windows 用 `render_goal_deck.ps1`(直接 PowerShell,不经 WSL/bash);macOS / Linux 用 `render_goal_deck.sh`。
- 风格选择提问:用户可见回复必须嵌入 `<skill-root>/assets/skill/theme-style-grid.png` 的 Markdown 图片,先展开绝对路径;这是回复展示用内置风格图,不可写入 `goal.json` 或任何 media 字段;列出当前可选风格和极简“适合/人群”,不能只在内部进度提示中提到风格图。
- 开工前确认两件事:主题风格、是否需要图片/视频。用户未明确表达且非整体委托时,先提问等答复,不得代选;无法提问的环境(脚本/批处理)才自选,并在交付说明中列出所选与理由。
- 委托模式:仅当用户对整体明确委托(“都你来定”“不用问,直接开干”)时,才自选主题、默认 HTML、默认不使用 image-gen,最终说明假设。用户只说内容/文案“随意”“自拟”时,仅自拟内容;风格、页数、媒体等已给的不得擅自改变,未给的按上一条先问。
- 非交互/一次性执行(无法追问)时:未指定风格按内容主题自选已验收主题;无真实素材且不能生图时优先选无媒体页,不调 image-gen;最终说明全部假设。
- Deck 语言跟随用户沟通语言:非中文用户在 `goal.json` 顶层加 `"language": "en"`;全部文案字段用目标语言撰写,页面自带的默认中文文案(含结尾页“感谢阅读”类装饰字段)一律覆盖,不得残留中文。编辑器界面语言自动跟随打开者的系统语言,右上角可手动切换,无需在生成时处理。
- 交付格式:默认 HTML;“生成 PPT”“做 PPT”“做一个 PPT”“制作 ppt”表示 PPT 呈现形态。只有明确 `PPTX`、`PowerPoint`、`可编辑 PPTX`、`导出 PPTX`、`PPT 格式` 或“格式/文件类型为 PPT/PPTX”时才交付 PPTX 文件。
- PPTX 文件:仍先生成 HTML 并启动本机预览服务,再调用本机 HTTP 导出服务;最终只给 PPTX 文件路径或下载结果。
- 当前可选风格: `theme01` 轻拟态风、`theme02` 炫光紫绿风、`theme03` 深浅代码风、`theme04` 玻璃糖果风、`theme05` 色谱图表风、`theme06` 深色图谱风、`theme07` 冷白调研风、`theme08` 黑金实验风、`theme09` 深蓝杂志风、`theme10` 金色指数风、`theme11` 高能增长风、`theme12` 声波霓虹风。
- 普通自动选择不选 `theme10`;只有用户明确指定,或金融/投资指数内容强相关且 inspect 确认可填时才用。
<!-- theme-choice-hints:start -->
  - `theme01` 轻拟态风 | 适合: 产品介绍 / 企业汇报 | 人群: 创业团队 / 产品经理
  - `theme02` 炫光紫绿风 | 适合: 科技发布会 / AI/自动驾驶/机器人主题 | 人群: 科技公司创始人 / 技术负责人
  - `theme03` 深浅代码风 | 适合: 技术方案 / 开发者大会 | 人群: 工程师 / 技术管理者
  - `theme04` 玻璃糖果风 | 适合: 年轻化品牌 / 消费产品 | 人群: 品牌团队 / 设计师
  - `theme05` 色谱图表风 | 适合: 数据报告 / 市场分析 | 人群: 数据分析师 / 咨询顾问
  - `theme06` 深色图谱风 | 适合: 高密度数据展示 / 战略分析 | 人群: 战略团队 / 投资人
  - `theme07` 冷白调研风 | 适合: 调研报告 / 白皮书 | 人群: 研究机构 / 咨询团队
  - `theme08` 黑金实验风 | 适合: 高端发布 / 品牌提案 | 人群: 高端品牌 / 创意总监
  - `theme09` 深蓝杂志风 | 适合: 品牌故事 / 人物访谈 | 人群: 公关团队 / 媒体编辑
  - `theme10` 金色指数风 | 适合: 金融数据 / 投资报告 | 人群: 投资机构 / 金融分析师
  - `theme11` 高能增长风 | 适合: 增长复盘 / 商业计划 | 人群: 创业者 / 增长团队
  - `theme12` 声波霓虹风 | 适合: 音乐娱乐 / 潮流活动 | 人群: 娱乐品牌 / 活动策划
<!-- theme-choice-hints:end -->
- 不使用旧 token、旧主题、旧媒体槽、旧风格分支或旧入场动画控制。
- 先冻结本页 `slide.content.presentation`,再按真实容量传入 `--title-chars`、`--summary-chars`、`--takeaway-chars`、`--item-count`、`--value-item-count`、`--raw-numeric-item-count`、`--textual-value-item-count`、`--nested-depth` 和 `--priority`,例如 `npm --prefix <skill-root>/project run layout:query -- --theme <themePack> --item-count 4 --value-item-count 4 --textual-value-item-count 4 --priority metrics --limit 12 --seed <randomSeed>:slide-<n>`。标题、items、`value/displayValue` 和明确媒体是硬条件;摘要、结论、detail、unit、focus 和 role 只影响排序。每页选择 3 个结构家族不同的 layout,整份 deck 统一分配,不重复同一组三布局。需要媒体槽时加 `--needs-media`、`--planned-images <n>`、`--provided-images <n>` 或 `--image-gen`。
- 字段不清楚、对象/数组/count、图片/媒体:先运行 `npm --prefix <skill-root>/project run inspect:layout -- --compact <layout...>` 检查该页 3 个模板方案。scaffold 同时识别数组容器和重复标量槽组,只把完整 `items` 投影到唯一主容器;辅助可见容器可隐藏时设为 0,不能隐藏且没有合法支持内容时该 layout 退出候选。不要让 Agent 手写 30 份 `contentMap`;只有用户显式指定复杂 layout 时才按 `goal.fill-plan.json` 补该页映射。写对象、数组、数量或图片 props:运行 `props:safe`,整份 goal 用 `props:safe -- --goal <file> --write`。
- 把 `layout:query` / `inspect:layout` 的 JSON 管道给程序解析时,改用 `node <skill-root>/project/scripts/layout-query.mjs` / `node <skill-root>/project/scripts/inspect-layout.mjs`:`npm run` 会在 stdout 前打印生命周期 banner,污染 JSON。
- 长 deck:先写逐页 brief JSON,每页包含 `role`、`priority` 和唯一的 `content`,再用 `npm --prefix <skill-root>/project run goal:scaffold -- --title <title> --goal <goal> --theme <themePack> --pages <n> --content-briefs <briefs.json> --layout-variants 3 --seed <randomSeed> --workflow-run-id <workflowRunId> --chunk-size 5 --out output/<deck-name>/goal.json`。scaffold 按内容容量和字段能力选 3 个模板,并追加可直接渲染的主题化 v4 初稿。
- 文案长度和数组数量:优先按 `fillPlan.text[].maxChars`、`fillPlan.arrays[].visibleCount`、`fillPlan.arrays[].nestedArrays` 写;`display` / `metric` 字段只写短词、短句或数字。
- Html 字段(如 `headlineHtml` / `quoteHtml`)写文案只用 `<br>` 换行加 `<b>` / `<em>` 行内强调,禁止 `<span>` 等自由 HTML;主题默认值里的 `<span class>` 依赖主题 CSS,只是占位,不要照抄。`validate:goal-spec` 会拦截自由 HTML。
- 可见数组项必须写实文案;被 count/显隐控制隐藏的尾项可保留“请输入文本”占位。
- 元素出现动画使用页面组件自带的原生效果。
- 页面切换动画可以在预览控制面板里调整。
- 面向用户交付的 deck 默认不显示风格/主题切换选项;风格切换只保留在内部调试 demo 页面。用户明确要求保留主题切换时,在 goal 顶层写 `preview: {"themeSwitcher": true}`。
- 不手写自由 HTML slide。新生成 deck 使用 `schemaVersion: 2`;每个逻辑页只保存一份 `content`,前三项是 `{kind:"template", layout, props, contentMap}`,第四项是 `{kind:"bespoke", adjustable:false, composition, contentMap}`,且 v4 不写 `layout`、`props` 或 `controls`。旧 deck 的单 layout 和 3 候选仍可读取。
- 每套主题的前 5 页 `themeXX_page001` 到 `themeXX_page005` 都是封面候选。一个 deck 只能有 1 个逻辑封面页,其 3 个模板方案都从前 5 页选择;正文模板方案从第 6 页以后选择。
- 同一逻辑页内 3 个 template layout 必须互不重复且优先来自不同结构家族;整稿先使用尚未出现的 layout 和结构指纹,候选确实不足时才复用,相邻页不循环同一组视觉骨架。
- 面向用户交付的 deck 不能只写 `role` 后依赖页面默认文案。每一页先在 `slide.content` 写真实内容,模板 props 只保留非内容配置。
- 每个逻辑页先写一份 `slide.content.presentation` 文案包,包含 `title/titleShort`、`summary/summaryShort`、`takeaway/items` 和可选 `structure`;每个 item 使用稳定 `id/label/value/displayValue/detail/unit/required/priority`。v1-v3 共享页面意图、核心结论、全部 required facts、关键数字及其单位,只选择长短文案、排序、分组和视觉层级,不分别创作三套故事。简单数组映射使用 `{source:"presentation.items",fields:{目标字段:"label"}}`。
- v4 必须独立分析用户目标、受众、本页叙事作用和重点信息后设计;允许从同一事实源重组、聚焦或改写表达,但不新增事实。只使用当前主题 runtime 暴露的字体层级、页框、色带、线条、卡片和图表 recipe,不得另写 raw CSS,也不是前三个模板的小改。
- Codex 环境提供 `baoyu-design` 时,v4 设计前先读取该 Skill,用其设计论点、视觉焦点、节奏和构图方法完成整稿艺术指导;当前主题 runtime 视为 binding design system,最终只落成受约束 `composition`,不输出独立 HTML/CSS。未提供该 Skill 时沿用同一艺术指导标准。
- v4 `composition.designIntent.compositionFamily` 使用 scaffold 已分配的 `hero/split/metric-spotlight/chart-led/timeline/matrix/editorial/comparison/process`;页面几何必须明显实现该家族,不能把不同家族都画成标题加卡片墙。整稿同一家族不连续出现,卡片网格最多占正文 v4 的三分之一。
- v4 `composition` 使用主题背景语义和 12×8 网格元素;元素类型只用 `text` / `metric` / `list` / `quote` / `media` / `shape` / `chart`。图表型页面以数据图形为主视觉,时间线/流程页以方向和连接关系为主视觉,split/editorial 页面用非对称层级,不把标签换色当成设计。
- v4 从 scaffold 的完整主题化 composition 初稿上优化;保留已分配的构图家族和主题 recipe,只重组真正改善表达的页面,不要清空 `elements` 后重新批量生成同一套卡片。
- 3 个模板方案各自的 `copyKeys` / `fillPlan.text` 文案槽必须由 canonical content 覆盖;唯一主数组或标量槽组消费完整 `items`,辅助内容容器只能合法隐藏或使 layout 退出候选。`title` 与 `titleShort` 属于同一标题语义家族。
- 优先只写 `layout:query` / `inspect:layout` 暴露的文案字段。字段是对象或数组时按 `fillPlan` 和 `propShapes` 填内部 key。`copyKeys` 已展开嵌套路径(如 `copy.quote`、`items[].label`),按列出的路径直接填。
- `inspect:layout` 标 `contentLocked: true` 的页正文由组件固定、props 填不进:换一页能填正文的布局,或仅当用户接受其默认正文时使用。数组按 `fillPlan.arrays[].visibleCount` 填满可见项;`decorativeKeys` 是装饰位,不要填。
- 不要改页面元数据、组件源码、className、CSS、样式字段或默认视觉结构来完成内容填充。只在 `props` 内填写内容和用户明确要求的页面属性。
- 允许用顶层 `text` 覆盖可见文字槽位,但只用于替换文字内容。不要在普通生成中启动浏览器批量抽取全页面文本槽位;只有用户明确要求“彻底清除所有模板默认文案/逐页校对可见文案”时才做运行时槽位抽取。
- 禁止复用 `output/` 里已有的旧 `goal.json` 或旧 HTML。每次请求都新建本次输出目录和本次 JSON 计划。
- 输出目录写在当前会话工作目录,不要写入 `<skill-root>/project/output`。
- HTML 交付:给用户的预览地址只给 `http://127.0.0.1:<port>/`(不给 https 或 .local 变体);本机 HTTP 可导出 HTML/PDF/PPTX,本地 HTML 或 `file://` 不能导出可编辑 PPTX。不要返回 `theme-preview`。在自带浏览器的 Agent APP(如 Codex)里生成时,提醒用户导出 PDF/PPTX 前把该地址在系统浏览器中打开。
- PPTX 交付:调用 `/api/export-editable-pptx`;最终只给 PPTX 文件路径或下载结果。
- 无浏览器会话、脚本直调、或预览导出接口返回 403/5xx 时:改用 `npm run export:pptx -- <deck>/ppt <out.pptx>`(PDF 用 `export:pdf`)直接产出文件,不需要先起浏览器会话。
- 如果输出正文里出现与用户主题无关的默认文案,例如 AI Capital / 投融资 / SoundWave / 声浪 / Key Metrics / Roadmap / End of Report 等,必须重写 JSON 后重新渲染,不能交付。

## 媒体工作流

- 媒体字段只写 `mediaSlots[].canPresetMedia: true` 的槽,按该槽 `presetProp` / `fieldPath` 写路径;`goal.json` 只引用 deck 内相对媒体路径,不可引用临时目录、外部绝对路径、`file://` 或远程 URL。
- 视觉素材任务先判断意图:无图但需要视觉素材时先问是否预留图片槽;无真实素材且不能生图时优先选无媒体页。用户提供素材库/素材目录路径即视为有图意图:至少选 2 个带媒体槽页面并填入合适素材。素材路径不可访问时改选无媒体页并在交付说明中告知,不在页面内留占位提示文字。用户同意用 `--planned-images <n>` / `--needs-media`,用户给素材用 `--provided-images <n>` / `--provided-media`,用户明确要求原创视觉图/生图时,Codex 环境用 image-gen 生成图片并加 `--image-gen`;未明确生图时先询问用户。`plannedImages` / `needsVisual` / `imageGen` 只表示选页意图,除非用户明确选择预留空槽,交付前必须写入真实媒体路径,不能交付空媒体槽或伪造路径。
- 用户本地图片/视频先运行 `npm --prefix <skill-root>/project run media:stage -- <deck-output-dir-or-ppt-dir> <media-file...>`,使用返回的 `relative` 路径;AVIF 会转成浏览器可用格式。image-gen 输出也先落到本次 deck 目录。
- 渲染后核对 goal 引用的每个图片/视频:`ppt/<relative>` 存在且 HTML 包含文件名;缺失时只补最终 `ppt/assets` 并重跑校验。图片/视频素材每个最多使用一次;同一逻辑页的 4 个方案共用同一份素材,算 1 次逻辑使用,不同逻辑页不要重复填充同一素材。素材用完后,媒体插槽留空或改选无媒体插槽页面。
- 需要 image-gen 生成 2 张以上独立图片时,用多个 subagent 并行生成,不要串行逐张等待;每张图独立生成,不要用一张拼图/素材板再拆分。subagent 只用于生图,不用于选题、文案、选页或校验。

## 工作流

1. 提炼用户目标: `title`、`goal`、`audience`、`owner`、页数、内容重点和最终产物格式;同时形成验收清单,记录用户显式要求、已确认选项和必要假设。用户未指定页数时默认 10 页左右,不少于 8 页。
2. 确认 `themePack`。用户未指定时先询问风格;用户选定后生成 `randomSeed` 和本次任务唯一的 `workflowRunId`,例如 `<主题>-<日期>-<3位随机词>`,保证随机选页可复现;同一任务重试复用该 run ID,新任务生成新 ID。
3. 判断图片意图:无图但需要视觉素材时先问是否预留图片槽;用户给本地素材先 `media:stage`;明确生图时用 image-gen。
4. 一次写完整份 deck 的逐页 brief 和 `content.presentation` 文案包;前三个模板共享 required facts 和关键数字,标题/摘要提供 full/short 两档。把硬容量和软偏好一次传给 `goal:scaffold`,不逐页试错换主题。
5. scaffold 对整份 deck 一次完成候选查询、唯一主容器投影、辅助容器处理、三布局组合分配和 v4 主题化初稿;3 个模板直接物化同一文案包,不逐页手工补 `contentMap`。Agent 使用 `baoyu-design` 先定整稿设计论点、节奏和每页视觉焦点,再在既有 `compositionFamily` 与主题 recipe 上批量绘制 v4,禁止清空初稿后逐页临时都退化成卡片网格。
6. 把 schema v2 JSON 写入本次工作目录的 `output/<deck-name>/goal.json`;每页写 `selectedVariant: "v1"` 和恰好 3 template + 1 bespoke。渲染前运行 `npm --prefix <skill-root>/project run props:safe -- --goal output/<deck-name>/goal.json --write` 和 goal spec 校验。`--write` 后核对 3 个模板方案的 `layoutChanges`;不认可替换就改回并换页。
7. 图表页填入自己的数据后,页内 insight/读图/结论类文案字段必须据新数据一并改写,不保留默认结论。
8. 运行渲染脚本输出 `output/<deck-name>/ppt/index.html`;脚本会使用 Skill 内置生成器,不要切回外部项目目录。
9. 渲染后核对素材路径,缺失时补最终 `ppt/assets`。
10. 确认脚本完成 `validate:swiss`、`validate:goal-copy` 和 `validate:four-variant-quality` 校验;后者在同一浏览器会话批量检查并截图每页 v4。一次用户生成任务只创建一个 `workflowRunId`,所有 scaffold attempts 和后续阶段复用它。
11. 渲染脚本会启动本地 HTTP 预览服务并输出 `http://127.0.0.1:<port>/`;需要指定端口时设置 `DASHI_PPT_PREVIEW_PORT` 后再运行脚本(端口用 5200-5999 段,4178/4300/4400 为用户保留端口不可用)。只能用该预览服务,不得用 `python -m http.server`、`npx serve` 等静态服务器替代:静态服务器没有导出和自动保存接口。预览服务下编辑自动保存到 `index.html` 本体;`file://` 打开的本地文件不自动保存,交付前需导出。
12. 对最终产物执行成果验收:模板方案只做一次批量内容映射、尺寸和运行时检查;浏览器视觉验收一次查看全部 v4 截图。
13. v4 待修正时只修改失败页并重新渲染一次;不重新选模板,不重写其余页面,不重复整稿视觉检查。
14. 运行 `node <skill-root>/scripts/check_latest_version.mjs` 做静默版本检查。
15. 验收通过后按交付格式回复:HTML 只给 `http://127.0.0.1:<port>/`;PPTX 调用 `/api/export-editable-pptx` 后只给文件路径或下载结果。

## 成果验收与返工

机器校验通过只是技术基线,不等于成果达标。最终验收以用户原始需求、已确认选项、明示假设和最终渲染产物为准:

- 目标一致性:Deck 回答用户的核心问题,重点、结论和语气适合目标受众。
- 内容覆盖:指定的主题、必含要点、页数、风格、语言、媒体和产物格式都已落实,无跑题、缺项或无关模板文案。
- 逐页检查:每页都服务于整体目标;标题、正文、数据、图表和 insight 相互一致,没有重复、断层、空白页或明显不匹配的 layout。
- 方案检查:v1-v3 共享页面意图、required facts 和关键数字,整稿不循环同一组三布局;v4 基于同一事实源按用户目标重新组织表达,并在几何上实现已分配的 compositionFamily。模板完成运行时检查,bespoke 完成视觉检查。
- 叙事完整性:开场、论证/展开和结论/行动顺序清晰,页与页之间有逻辑承接。
- 交付完整性:最终文件存在且能打开,页数和格式正确,素材可用,首尾页非空白。

有浏览器能力时,最终一轮批量打开 v4,检查内容可见、媒体正常,无明显溢出、遮挡或裁切;模板不做截图审美复查。

验收状态只有“通过”“待修正”“阻塞”。v4 不合格时只修正对应 composition,必要时更换 layout,然后重新渲染并复验这些页面一次;仍不通过则标记“阻塞”并说明未达标项。

示例命令(macOS / Linux):

```bash
<skill-root>/scripts/render_goal_deck.sh \
  output/client-review/goal.json \
  output/client-review/ppt/index.html
```

Windows PowerShell:

```powershell
& "<skill-root>/scripts/render_goal_deck.ps1" `
  "output/client-review/goal.json" `
  "output/client-review/ppt/index.html"
```

## JSON 结构

```json
{
  "schemaVersion": 2,
  "title": "美国 AI 融资调研",
  "goal": "面向投资团队汇报 2024-2026 年美国 AI 大额融资结构、资本流向和后续判断",
  "audience": "投资团队 / 产业研究团队",
  "owner": "研究团队",
  "randomSeed": "ai-funding-20260609-a7k",
  "workflowRunId": "20260609T120000000-a7k9m3x2",
  "pageCount": 1,
  "themePack": "theme01",
  "variantOutputMode": "comparison",
  "slides": [
    {
      "id": "s1",
      "content": {
        "presentation": {
          "title": "美国 AI 融资调研",
          "summary": "2024-2026 年大额融资结构、资本流向与后续判断",
          "takeaway": "为投资决策建立统一研究范围",
          "items": []
        },
        "media": [],
        "meta": {
          "brand": "研究团队",
          "pageLabel": "2026",
          "panelTitle": "融资调研"
        }
      },
      "selectedVariant": "v1",
      "variants": [
        {"id": "v1", "kind": "template", "layout": "theme01_page001", "props": {}, "contentMap": {"kicker": "meta.panelTitle", "titleTop": "presentation.title", "titleBottom": "presentation.summary", "lead": "presentation.takeaway"}},
        {"id": "v2", "kind": "template", "layout": "theme01_page002", "props": {}, "contentMap": {"enKicker": "meta.panelTitle", "titleTop": "presentation.title", "titleBottom": "presentation.summary", "subtitle": "presentation.takeaway"}},
        {"id": "v3", "kind": "template", "layout": "theme01_page003", "props": {}, "contentMap": {"kicker": "meta.panelTitle", "titleTop": "presentation.title", "titleBottom": "presentation.summary", "bigNumber": "meta.pageLabel"}},
        {
          "id": "v4",
          "kind": "bespoke",
          "adjustable": false,
          "composition": {
            "designIntent": {
              "objective": "快速建立调研范围",
              "audience": "投资团队",
              "narrativeRole": "封面定调",
              "emphasis": "研究对象与决策价值",
              "rationale": "用单一标题中心和三项范围提示缩短理解路径",
              "compositionFamily": "hero"
            },
            "background": "dark",
            "elements": [
              {"id": "title", "type": "text", "grid": {"column": 1, "row": 1, "width": 10, "height": 2}, "role": "title", "text": ""},
              {"id": "summary", "type": "text", "grid": {"column": 1, "row": 4, "width": 7, "height": 2}, "role": "body", "text": ""}
            ]
          },
          "contentMap": {"elements[0].text": "presentation.title", "elements[1].text": "presentation.summary"}
        }
      ]
    }
  ]
}
```

如果 `slides` 为空,`pageCount` 只适合临时草稿预览。新生成 deck 面向用户交付前必须落成 schema v2 的 3 template + 1 bespoke;旧单版式和旧 3 候选 goal 仍可读取。

## 页面角色

`role` 只用于草稿选页,最终 JSON 的前三个方案必须落成具体 `layout`,v4 必须落成无 layout 的 bespoke composition。角色说明见 `references/layout-roles.md`;真实模板候选以 `layout:query` 输出为准。

`cover` 只能从当前主题前 5 页选择。`image` / `media` 候选基于真实 `mediaSlots`,不是页面标题关键词。动态背景页可用 `ambient` 作为氛围页或章节页。

可以直接指定页面:

```json
{"layout": "theme01_page030", "props": {"title": "典型案例"}}
```

## 交付能力

编辑器和左侧目录始终只显示 N 个逻辑页,同页候选切换不改变逻辑页码。右侧面板可切换或标记 4 个方案;前三个模板方案可调 props,v4 为固定的 Agent 定制方案。仅在 `variantOutputMode:"comparison"` 的导出阶段派生 4N 页(PDF/PPTX 和用户明确要求的比较稿使用此模式);`"selected-only"` 导出 N 页。面向用户交付的页面底部不显示页码标识、翻页引导、圆点导航或索引提示。

## 页面属性契约

普通生成不要读 `layout-manifest.json`。先用 `layout:query` 输出的候选摘要。只有需要更细契约时,再用 `npm --prefix <skill-root>/project run inspect:layout -- --compact <layout...>` 看页面契约:

- `copyKeys`: 可安全改写的文案/数据字段。
- `copyBudgets`: 文案长度预算;`display` / `metric` 超长会被 goal spec 拦截。
- `propShapes`: `copyKeys` / 数组字段的内部形状;写 `copy`、`cells`、`items`、`rows` 等对象字段时只使用这里列出的 key。
- `fillPlan.arrays[].itemFields[].enum`: 该字段为结构枚举,只能从列出的值中选,不是自由文案。
- `mediaSlots`: 图片/视频写入字段、count key、默认数量和最大数量。
- `countBindings`: 数量参数与数组字段的绑定。
- `fillPlan` 里数值字段看 `numericBounds` 填数:`enforced:false` 是提示、真实数据可超出,`enforced:true` 必须遵守,`semantics:'normalized'` 填 0-1 比例;定长嵌套数组看 `fixedLength`/`fixedLengths` 按下标填,不试错。
- `controlKeys`: 右侧面板可操作字段,不是普通内容填充清单;仅用户明确要求调整页面属性时使用。默认只填 `copyKeys`、可见数组和真实媒体槽。

## 校验

- 渲染前必须运行 `validate:goal-spec`。
- 输出后必须运行 `validate:swiss`。
- 输出后必须运行 `validate:goal-copy`。
- 改动展示 demo 后运行 `npm run showcase:update`。
