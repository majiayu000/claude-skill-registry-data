---
name: research-topic-compiler
description: >
  Product Research / 产品研究编译器：当用户要围绕一个产品问题做系统调研、竞品证据、替代方案、行业信号、
  用户与市场研究、最佳实践提炼、产品候选池、本地 HTML 研究看板、可视化研究报告或跨职能 Dashboard 时使用。
  当用户只有大白话、模糊方向、业务愿望或 Roadmap/PRD 前置材料想法，需要先转成清晰研究目标、研究问题和输出要求时也使用。
  适合把研究转成 Research Project、学习报告、证据矩阵、PM 决策看板、候选池、模板、实践任务、业务判断、商业化输入或高门槛应用研究前置。适合“系统研究一个主题”
  “整理到 Obsidian”“做深度专题”“研究行业最佳实践”“概念解读”“概念源流”“PM 技术评审提问脚本”
  “行业演进看板”“这个主题对我的产品决策有什么用”“让我系统学会并输出 learning report HTML”。不适合创建 Skill、评审 SKILL.md、普通即时搜索或一次性摘要。
  当用户已经要在明确候选项中选一个、需要最终推荐和排除理由时，应使用 decision-research。
  当 decision-research 或 grill-me 返回一个可研究、可关闭的精确证据 gap 时，也使用本 Skill 只补 Evidence Delta。
---

# 产品研究编译器（research-topic-compiler）
## 中文速查

- 中文名：产品研究 / 证据与决策输入
- 英文稳定名：`research-topic-compiler`
- 分类：研究学习 / Obsidian 知识编译
- 你可以这样叫我：`系统研究这个主题`、`帮我整理到 Obsidian`、`做一个深度专题`、`研究行业最佳实践`、`概念解读`、`概念源流`、`PM 技术评审提问脚本`、`行业演进看板`、`把这个大白话拆成研究目标`
- 适合：围绕产品问题做多渠道证据收集、竞品与替代方案比较、用户/市场信号、证据矩阵、阶段结论、候选池、研究看板和应用转化；也适合把用户的大白话、模糊主题或 Roadmap 前置想法转成研究目标、研究问题和输出要求
- 默认学习型 HTML：当用户要逐步理解、深入解释、对比自身现状并落到行动时，使用 `learning-report-html`，不要把研究控制面直接投影成 Dashboard。
- 不适合：创建或评审 Skill；普通新闻搜索或一次性摘要；明确要“选一个 / 给最终推荐 / 排除其他方案”时改用 `decision-research`
## Overview
使用这个 Skill 把一个研究主题编译成可学习、可追溯、可继续扩展、并能按用户画像转化为实际工作判断的 Obsidian Research Project 或聊天内研究报告。

核心原则：

- 先把用户原话转成明确研究目标、研究问题和输出要求，再判断研究深度、渠道和样本量。
- 研究框架不是固定报告目录：先识别 `Research Job`，分别维护 Evidence/Explanation Framework；V0 只是可修订假设，最终报告必须从证据更新后的 Framework Vn 重新编译。
- 先解析用户画像，再决定解释方式、案例选择、实践任务和应用转化。
- Seed Corpus 是线索和初始假设来源，不默认是权威证据；二手核心 Claim 要追溯原始来源或披露无法追溯的影响。
- Normal Research 和 Application 围绕最高价值证据缺口迭代；每轮只执行一个能降低关键不确定性的 Next Best Evidence Action。
- Research 只拥有证据覆盖、来源、矛盾、置信度和残余 gap；最终推荐、排除逻辑、方案设计和 readiness 属于其他 owner。
- Obsidian 是内部基线和默认沉淀位置，不是唯一研究渠道。
- 外部渠道动态选择，不默认全开；根据主题类型、证据缺口、时效性和可信度要求启用。
- 需要扩源时把 `Pre-Research Source Expansion` 作为候选发现策略：用公开搜索、垂直 API、RSS、产品/市场目录等渠道寻找能关闭当前 Gap 的来源，再筛选进入正式证据矩阵。
- 结论必须能回到证据矩阵；`05_研究报告` 是第一阅读入口，`02_证据与卡片` 是按需深挖层。
- 系统学习不是重型课程仓库；默认保持轻量，只有触发条件满足时才建议独立学习包文件。
- 当研究会影响产品策略、商业化、工作台/连接器设计、企业 adoption 或其他高成本决策时，默认按高门槛应用研究处理，读取 `references/applied-business-research-contract.md`。
- 轻量概念解构属于本 Skill 的研究模式，不再单独使用独立概念看板 Skill；它适合快速建立概念源流、语义漂移、范式阶段和 PM 决策问题。
- 用户画像只影响解释深度、案例选择、输出结构和实践任务，不覆盖用户当前明确要求。
- 研究必须能转成行动：判断、方案、模板、任务、PRD、Workflow、Eval、Checklist、SOP、路线图或实践练习。
- 用户补充的新渠道可以进入渠道库，但要先判断适用主题、访问条件、证据强度和风险。
- 微信公众号、X、私域社区、付费库等渠道默认只能做公开候选发现；任何登录态读取、客户端转发、发送到 Obsidian 同步号或第三方服务的动作，都需要当前 run 的明确授权和可见确认点。

## Input / Context Intake

启动研究前先收集或推断这些上下文；不要问本地文件能发现的信息，只在答案会改变研究范围、访问权限或写回位置时追问：

- 原始意图：用户原话、业务愿望、想产出的材料、隐含的后续动作。
- 研究主题：主题名称、用户要解决的决策或学习目标、是否已有种子资料。
- 预期产物：聊天内报告、Obsidian Research Project、更新已有专题、还是长期雷达。
- 深度约束：用户期望的速度、深度、样本量、是否需要 `L4/L5` 级外部扩展。
- 内部基线：是否扫描 Obsidian、哪些 Vault/目录可用、是否只读 `笔记同步助手`。
- 渠道偏好：必须看的渠道、明确排除的渠道、是否需要产品研究、GitHub、官方文档、论文、社区或 X。
- 访问边界：登录、API token、付费报告、私密社区、公司内部资料和引用限制。
- 写回边界：目标目录、命名规则、是否允许新增渠道到 `channel-registry.md`。
- 用户画像：角色、领域、技术深度、目标类型、输出偏好、应用场景和最终决策需求；先按 `User Context Resolution` 解析，不要默认每次追问。

默认假设：Obsidian 是内部基线，公开外部渠道可用于补证；封闭、付费、登录或私密渠道必须先取得用户授权。用户补充渠道时，先判断是本次临时使用还是值得进入渠道库；只有用户明确希望复用时才写入 `references/channel-registry.md`。

## Research Goal Framing Gate

当用户输入是大白话、宽泛方向、业务愿望、解法名称、Roadmap/PRD 前置材料想法，或没有明确研究问题与输出要求时，先读 `references/research-goal-framing-gate.md`。

这个 Gate 的职责是把用户原话转成可执行研究 brief：

- 保留用户原始意图。
- 推断真正研究目标和本次 `Research Job`，而不是从主题名套用上一次研究的框架。
- 判断目标类型：Concept Lens、Industry Evolution、Application Translation、Product Candidate、Roadmap Input、Learning Pack 或 Research Radar。
- 拆出主研究问题、子问题、out of scope 和证据标准。
- 明确读者、产物形态和研究结果要支持的下一步动作。
- 决定是否需要用户确认；能合理推断时带假设继续。

不要从用户第一句里的名词直接开始搜索。先确认这次研究是为了理解、判断、转译、候选发现、路线图输入、学习沉淀还是持续雷达。

## User Context Resolution

生成研究输出前先解析用户上下文。详细字段和追问规则见 `references/user-context-standards.md`。

优先级：

1. 当前用户消息中的显式要求，例如“我是后端工程师”“给我 PRD 视角”“不要太技术”。
2. 当前项目或目标 Research Project 附近的 `user-profile.md`。
3. 全局 `user-profile.md`，例如 Vault 根目录或用户明确指定的长期画像文件。
4. Skill 内置默认画像 `references/default-user-profile.md`，仅作为本地默认配置。
5. 如果仍缺少会显著影响输出质量的信息，最多问 3-5 个轻量问题。

处理规则：

- 不要每次都询问用户身份；能从当前消息、本地 profile 或默认 profile 推断时直接使用。
- 当前任务指令永远高于长期画像和默认画像。
- 用户画像只影响解释深度、案例选择、输出结构、实践任务和应用建议。
- 用户画像不能改变证据等级、不能绕过访问限制、不能把弱证据升级为稳定结论。
- 如果用户画像未知且主题不复杂，先用通用解释；只有主题复杂且目标不清时再追问。
- 只有当用户要求持久化、当前任务已经写入 Obsidian，或 profile 文件是本次明确产物时，才创建或更新 `user-profile.md`；否则画像只在本次研究中使用。

## Research Modes

按用户目标选择一种主模式，也可以组合使用。先读取 `references/mode-selection.md`；需要细则再读 `references/mode-routing-guide.md`。

| Mode | Use When | Primary Assets |
| --- | --- | --- |
| `Normal Research` | 普通专题研究、证据矩阵、阶段结论 | `research-depth-rubric.md`, `report-writing-standards.md` |
| `Lightweight Concept Lens` | 概念源流、语义演化、PM 技术评审提问脚本、HTML 决策看板 | `concept-lens-*` references |
| `Learning Pack` | 用户对陌生领域建立学习框架 | `learning-pack-standards.md` |
| `Application` | 研究要转成方案、PRD、Workflow、Eval、SOP 或路线图输入 | `applied-business-research-contract.md` |
| `Radar` | 长期变化主题、watchlist、更新日志 | `research-radar-loop-contract.md` |
| `Product Candidate` | 先发现候选、建候选池、为后续决策提供输入 | `product-decision-mode.md`, `candidate-backlog-schema.md` |

### Product Research / Competitive Evidence

当用户要研究竞品、替代方案、定价、onboarding、公开产品页面、评论、更新日志或行业信号时，使用本 Skill 的 `product-research` mode：

1. 先把产品决策和比较维度写成 research brief，不把“竞品分析”当成无目标功能清单。
2. 读取 `references/product-evidence-channel-guide.md`，根据当前 Gap 选择渠道；将产品事实、用户/市场信号、推断和建议分开，记录来源、访问时间、直接性和局限。
3. 需要登录态走查、OAuth、截图、录屏或 Computer Use 时，必须读取 `references/browser-walkthrough-boundaries.md`，先定义最小取证范围和明确禁止动作。
4. 输出 `Evidence Pack`、差异矩阵和对产品决策的启发。需要完整简报时使用 `references/product-decision-brief-template.md`，并运行 `scripts/check_product_decision_brief.py <brief.md>`。
5. 简报只对 `Copy / Adapt / Avoid / Monitor / Validate first` 给出证据导向，不替用户做最终候选选择；Top candidates 只是交给 `decision-research` 的输入。
6. 登录态走查、付费来源、客户资料和外部系统写入仍受当前 run 的授权边界约束。

用户说“选一个”“给最终推荐”“为什么排除其他方案”“基于 Candidate Backlog 下结论”时，转交 `decision-research`。本 Skill 可以给 Top candidates 或排序表，但它们是决策输入，不是最终决策 authority。

## Output Artifact Modes

Research Mode 决定研究方法，Output Artifact Mode 决定交付形态；两者正交选择，不要因为用户要 HTML 就改写研究深度、证据门禁或责任边界。

| Output Artifact Mode | Use When | Deliverable |
| --- | --- | --- |
| `chat-brief` | 用户要直接答案、轻量结论或不需要落盘 | 聊天内答案 |
| `research-project-md` | 用户要 Obsidian Research Project、Markdown 报告或可继续维护的研究资产 | `00-05` 及按需扩展文件 |
| `concept-dashboard-html` | `Lightweight Concept Lens` 的概念源流、范式阶段或概念债务需要可视化 | `dashboard.html` + `summary.md` |
| `research-dashboard-html` | 一般专题、Application 或跨职能评审需要给领导、产品、研发等角色扫描、比较和行动 | `dashboard.html` + `summary.md` |
| `learning-report-html` | 一个主要读者要连续学习、建立机制模型、比较自身现状并采取行动 | `report.html` + `summary.md` |

- 用户明确要求 HTML、网页看板、可视化研究报告或跨职能 Dashboard 时，选择相应 HTML artifact mode。
- 当研究结果需要多角色阅读、证据与结论并列、或直接进入 Roadmap/PRD/评审时，可以建议 `research-dashboard-html`，但只有用户明确要求或接受建议后才生成文件。
- 当用户说“逐步学习 / 深入理解 / 不要蜻蜓点水 / 对比我的现状 / 最后告诉我怎么改”，默认选择 `learning-report-html`；它使用连续编辑式正文，证据放脚注、文末或折叠附录。
- `concept-dashboard-html` 只承载 Concept Lens；一般 Normal Research/Application 使用 `research-dashboard-html`，读取 `references/research-dashboard-output-contract.md`。
- `learning-report-html` 读取 `references/learning-report-output-contract.md`，并在渲染前通过 `references/editorial-projection-gate.md`；它不是研究过程报告，也不是 UI mockup。
- Do not generate HTML for chat/Markdown-only requests, ordinary L1/L2 answers, or UI mockup requests unless the user explicitly asks for a research dashboard artifact.
- 输出形态不能覆盖相邻 Skill 边界；用户要求最终选择和排除理由时仍交给 `decision-research`。

## Pre-Research Source Expansion

当当前 Gap 需要外部证据、主题依赖外部生态或用户要求扩源时，读取 `references/pre-research-source-expansion.md`。它负责 ACQUIRE 阶段的候选发现，不是每次研究固定执行的前置阶段；默认产物是 Candidate Source Table，不把搜索结果直接当结论。登录、付费、私密社区、客户端发送或同步动作都需要当前 run 的明确授权。

## Persona-Adaptive Output

按解析出的 `role` 调整输出重点。角色未知时先用通用解释，不要假设用户是工程师或产品经理；具体字段和追问规则见 `references/user-context-standards.md`。

## Workflow and Mode Routing

1. 捕获用户原话、主题和目标。若输入不够明确，先执行 `Research Goal Framing Gate`，输出 `Research Goal Framing`，把大白话转成研究目标、研究问题、输出要求和 out-of-scope。若用户只要求整理 research brief 或明确“先不要研究”，停在 framing 产物。
2. 按 `User Context Resolution` 解析用户画像，再分别选择研究模式、`L1-L5` 深度和 Output Artifact Mode。
3. 对需要结构化报告的研究读取 `references/research-framework-compilation-contract.md`，生成并映射 Explanation/Evidence Framework；再输出 `Research Run Plan`，明确 scope、Evidence Contract、预算、授权、artifact mode、产物和确认门禁。用户已给合理结构时优先保留；L1/L2 可把计划与 V0 压缩为内部判断。
4. `Normal Research` 与 `Application` 执行下面的七步控制面；完整对象与恢复规则必须读取 `references/iterative-research-loop.md`。
5. `Lightweight Concept Lens`、`Learning Pack`、`Product Candidate` 和 `Radar` 保持各自 mode-specific 主流程与产物，不把七步控制面强行替换它们。可复用来源质量和证据追溯规则；当它们需要结构化报告时仍使用 Framework Compilation Contract，但不得因此创建不必要的状态文件。

### Normal Research / Application Iterative Control Loop

1. **FRAME**：把目标、Seed Claims 和已有材料转成 Evidence Framework V0；同时从 Research Job 生成 Explanation Framework V0，定义主问题、解释逻辑、节点与 Claim 映射。两者都可修订，Seed 的标题、目录或转述不能替代原始来源身份，也不能成为固定报告目录。
2. **IDENTIFY GAP**：维护按价值排序的 Gap Ledger，标出未知、冲突、原始来源缺失、实现/独立验证/反例和迁移风险。
3. **PLAN NEXT BEST EVIDENCE**：每轮只选一个 NBE Action，说明 target Gap、预期信息增益、证据角色、独立性、成本/访问风险和选择理由。
4. **ACQUIRE**：根据 Gap 动态选择渠道并获取公开或已授权来源。Obsidian 是内部基线；扩源、同行权威比较和开源项目抽样都是按需策略，不是固定清单。
5. **EVALUATE**：把 Source、Evidence、Claim 分开，记录可定位摘录、直接性、新鲜度、lineage 和局限；伪官方或无法验证出处的材料降级，不进入最高等级核心结论。
6. **UPDATE FRAMEWORK**：先用 `Fill / Refine / Split / Merge / Challenge / Invalidate / Expand / No change` 更新 Evidence Framework；再判断 Explanation Framework 是否需要 `Add / Split / Merge / Reorder / Reframe / Remove / Challenge / No structural change`。两类事件都保留 before、after、evidence 和 rationale；不得静默覆盖或强行调和冲突。
7. **CHECK SATURATION**：只返回 `Continue / Stop / Pause / Escalate` 之一。Continue 回到步骤 2；Stop 后综合报告；Pause 写 Checkpoint；Escalate 转用户确认、深度升级或 `decision-research`。

### Depth Trimming

- `L1`：内部执行一次 ephemeral 压缩循环，只处理一个核心 Claim/Gap；充分权威材料已覆盖时不扩源、不建文件、不向用户暴露控制面术语。
- `L2`：维护约 3-5 个 Explanation Framework 节点和相应的轻量 Evidence Framework，最多两个 acquisition action；默认不建完整图谱或持久化状态，输出紧凑结论和未解决问题。
- `L3`：所有 Must Claim 有状态；核心二手 Claim 至少尝试一次原始来源追溯；按 `00-05` 增量持久化。
- `L4`：使用完整 Claim/Evidence/Source Graph、Change Log、独立验证、反例和正式饱和门禁。
- `L5`：首轮建立 L4 基线，后续由 Radar mode 做 delta；记录 `No change`，自动化仍需用户明确授权。

### Unique Terminal Gate

终止时按以下优先级自上而下返回一个状态：`blocked-authorization` → `partial-access` → `partial-budget` → `escalated` → `complete-saturated` → `complete-fit-for-purpose`。命中即停止，不得并列多个终态。

任何 `complete-*` 都要求：Must Claim 达到当前 Evidence Contract 或明确降级、核心来源已追溯或披露损失、关键矛盾已处理、剩余 Gap 不阻碍用户下一步。`complete-saturated` 还要求 L4 最近两个不同 lineage 的高质量 NBE 只产生 `Fill` / `No change` 且没有新 Must Gap。来源数、搜索结果数、候选池耗尽或文件写完都不能单独证明完成。

### Dashboard Projection Gate

`research-dashboard-html` 是研究状态的投影层，不是绕过研究循环的替代流程。Normal Research/Application 必须先完成适用深度的研究并命中一个 unique terminal status；同时必须存在 evidence-bearing latest Framework、至少一个可定位的 claim-to-evidence link，以及与当前结论对应的 uncertainty/residual Gap，之后才可渲染 `dashboard.html` 与 `summary.md`。只有终态、没有这些最低研究对象，不构成可投影状态。

- `complete-*`：满足上述可投影状态时可以渲染。
- `partial-access` / `partial-budget`：默认不渲染；只有用户在限制可见后 explicitly requests a partial Dashboard 或明确接受该交付，且页面显著展示证据缺口、弱结论和不可支持的下一步时才渲染。
- `blocked-authorization`：缺少授权导致最低可投影状态不成立时不渲染；不得用 Seed 或未授权材料填充页面。
- `escalated`：默认不渲染，由承接责任的 Skill 或用户决策决定后续产物。

Dashboard 必须从 Framework Vn 投影，并保留它与 Evidence/Source Graph、Framework Change Events、confidence、residual Gap、residual risks 和 next actions 的映射；可视化形式由 Vn 中的阶段、比较、因果、层级、流程、循环或状态关系决定。压缩展示时不得删除影响结论的矛盾、弱证据或未关闭问题，也不得把研究输入包装成最终决策。

### Learning Report Projection Gate

当 Artifact Mode 为 `learning-report-html` 时，先读取 `references/editorial-projection-gate.md` 和 `references/learning-report-output-contract.md`。研究循环仍先完成，但读者页面只投影最新 Explanation Framework 的结论 spine、机制、比较、边界、用户转译和行动；Evidence/Source Graph、Change Events、置信度和方法说明进入脚注、文末或折叠审计层。页面不得把 `NBE`、`terminal status`、Persona tabs 或证据矩阵当作主叙事。

渲染前必须得到唯一的 `ready` 编辑投影决定，并逐项通过 Claim、Mechanism、Evidence、Boundary、User implication、Overturn condition 深度测试。至少形成 3-5 个可争辩核心观点、1 条清晰机制链、1 个有意义对照、1 个边界/反例和至少 2 个面向当前用户的有界行动。若只能做概念普及或证据仍会改变结论，回到研究或改用 Dashboard；不要用视觉设计掩盖深度不足。

Learning Report 的静态验收要把 HTML 与 companion summary 一起传给 validator；它会检查自包含资源、内部链接、主叙事中的研究控制术语、折叠审计层、比较/边界/行动语义。发布级改动还必须按 `evals/graders/learning-report-rubric.md` 做匿名旧新对比，并覆盖 historical regression、transfer、near-boundary negative 与未参与调参的 holdout。

### Product Candidate Research 分支步骤

当 Workflow 第 2 步判定为 Product Candidate Research 模式时，在 Research Run Plan 后按以下独立流程继续，不进入 Normal/Application 七步控制面：

1. 在 `Research Run Plan` 增加决策维度（见 `references/product-decision-mode.md`）、候选池初始边界和评分权重草案。
2. 读取项目上下文。按 `references/project-context-intake.md` 获取项目阶段、约束、已有决策和用户优先级。
3. 做内部基线扫描 + 外部发现，聚焦于形成候选列表而非单一结论。
4. 形成 Candidate Backlog。按 `references/candidate-backlog-schema.md` 的 17 字段 schema 填充每个候选项，通过 Quality Gate 5 项检查。
5. 按用户确认的维度权重评分与排序，输出排序表和关键差异点。
6. 若候选项来自外部体系，按 `references/taxonomy-translation.md` 转译为项目内部分类。
7. 输出阶段产物：
    - Candidate Backlog（完整表格）
    - Candidate Summary（Top candidates + 理由 + 风险，标注为决策输入）
    - Cross-Session Handoff（按 `references/cross-session-handoff.md` 格式，供后续会话或 `decision-research` 继续）
8. 按 `references/post-research-exits.md` 推荐下一步出口（PRD Input / Starter Scenes / Demo Beachhead / Eval 等），不强制执行。

## L5 Automation Handling

`L5` 表示长期雷达，不等于默认创建自动化。只有用户明确要求创建、开启、设置、定期运行或持续自动更新时，才进入 automation 流程。创建前读取 `references/research-radar-loop-contract.md`，并说明频率、写入范围、禁止动作和人工确认点。

## Research Run Plan

L3+、需要用户确认范围/授权、或用户明确要求研究计划时输出完整模板。L1 直接快答和范围清楚的 L2 可保持内部轻量计划，不要为了展示流程制造重型前置产物。

```markdown
**Research Run Plan**
- Topic: <研究主题>
- User goal / Research Job: <用户要学会、判断或沉淀什么；这份研究要帮助谁理解、判断或完成什么>
- Framed from raw intent: <yes/no; if yes, summarize interpreted research goal>
- Research mode: <Normal Research / Lightweight Concept Lens / Learning Pack / Application / Radar / Product Candidate>
- Output artifact mode: <chat-brief / research-project-md / concept-dashboard-html / research-dashboard-html / learning-report-html>
- User context: <role, domain, technical_depth, goal_type, output_preference, application_context, decision_need>
- Recommended depth: <L1 / L2 / L3 / L4 / L5, with reason>
- Topic type: <平台能力 / 开源工程 / 产品竞品 / 学术方法 / 政策合规 / 市场趋势 / 其他>
- Core questions / Explanation Framework V0: <controlling question + dominant logic + provisional nodes; user-provided structure if applicable>
- Output requirements: <读者 / 产物 / 必须支持的下一步 / 不做什么>
- Evidence contract: <Must Claim 所需来源角色、直接性、独立性和完成标准>
- Effort budget: <时间 / acquisition action / 成本边界>
- Current highest-value Gap: <Gap + closure criterion，或 none>
- Next Best Evidence: <单一 action + expected information gain + source role + independence + cost/access risk，或 none>
- Channels selected: <仅列为当前 NBE 服务的渠道 + 选择理由>
- Channels skipped: <未启用渠道 + 原因>
- Access needs: <GitHub token / X token / login / paywall / none>
- Obsidian output: <chat-only / new Research Project / update existing project>
- Expected files: <00-05, optional 06-09, only suggest 10-12 when triggered>
- Confirmation needed: <only if L4/L5, closed channels, credentials, or broad writes>
```

如果用户已经明确要求写入 Obsidian，`L1-L3` 可以在输出计划后继续执行。`L4/L5`、封闭渠道、付费资料、需要登录或凭据、自动化持续跟踪、跨多个项目的大范围写入，都要先取得明确确认。若用户明确确认创建 L5 automation，按 `L5 Automation Handling` 调用 Codex automation。

## Channel Selection Rules

默认不是“所有渠道全开”，而是按当前 Gap 所需证据角色、主题类型和访问边界动态选择渠道。读取 `references/channel-selection-rubric.md` 和 `references/channel-registry.md`；封闭、付费、登录或私密渠道只在用户授权并说明引用限制后使用。

## Obsidian Output Contract

写入 Obsidian 前读取 `references/obsidian-output-contract.md`，按其中的 `00-05` 默认结构和按需扩展规则执行。`笔记同步助手` 是只读来源层；不要移动、删除或覆盖原始同步文章。

## Channel Registry Update

用户明确要求长期补录渠道时，读取 `references/channel-registry.md`，记录适用范围、访问条件、证据强度和风险；临时来源只进入当前研究项目。涉及登录、付费、私密社区或客户数据时，保留授权与引用边界。

## Output Format

完成后输出。L1/L2 可压缩为直接答案、来源、置信度/局限和下一步，不强制暴露 Framework、Gap、NBE、Change Event 或终态枚举；下面的完整格式用于 L3+ Normal/Application 或需要交接、暂停和审计的研究：

```markdown
**Research Result**
- Project/report: <Obsidian path or chat-only>
- Depth used: <L1-L5>
- Research mode: <Normal / Lightweight Concept Lens / Learning Pack / Application / Radar / Product Candidate>
- Output artifact mode: <chat-brief / research-project-md / concept-dashboard-html / research-dashboard-html / learning-report-html>
- Persona adaptation: <role/domain/depth/goal used, or generic>
- Channels used: <channels + each channel's target Gap/evidence role>
- Core conclusions / Explanation Framework: <latest version + controlling question + dominant logic + 3-7 conclusions + material structural changes or justified none>
- Application outputs: <judgment, template, task, PRD/Workflow/Eval/SOP/roadmap, or none>
- Strongest evidence: <top sources>
- Weak or trend evidence: <sources that need caution>
- Added channel candidates: <new registry entries or none>
- Terminal status: <unique terminal status>
- Stop reason: <fit-for-purpose / saturation / access / budget / escalation reason>
- Still uncertain: <evidence gaps>
- Residual risks: <未关闭但不阻断下一步的风险，或受限造成的影响>
- Next actions: <what to read or do next>
```

### Product Candidate Research 输出格式

使用 Product Candidate Research 时，按 `references/product-decision-mode.md` 和 `references/cross-session-handoff.md` 输出决策问题、候选数量、Top candidates、差异、评分、置信度、handoff、推荐出口和开放问题；明确它们是决策输入，不是最终推荐。

## Core Loop Handoff

需要把证据交给 `decision-research`，或消费 Decision/Critic 返回的单一证据 gap 时，读取 `references/core-loop-research-handoff.md`。

- 单点调用在 Evidence Pack 或一个 Research 终态后停止；`next_owner` 只是建议，不代表自动执行下游。
- Evidence Pack 可以提供决策输入，但不得包含最终选择或替其他 Skill 排除候选。
- Return Request 必须指向一个可研究、可关闭的稳定 gap；只返回 Evidence Delta，不重跑整份研究或改写 Decision。
- handoff 保留唯一 target owner、artifact/version、closure criterion、preserved items、resume point 和 cycle count。
- handoff/chain 不构成外部写入授权；Runtime sync、Skillshare/Multica 发布、钉钉/云效写入不属于 Research/B1 合同。遇到这些动作必须停止，并交给另行明确授权的专业 publisher/operation。
- 同一 gap 完成两轮回流后仍未关闭或缩小时，停止自动回流并进入 Human Gate。

## Definition of Done

任务完成必须满足至少一种情况：

- `L1` 快查：给出直接答案、来源和证据局限。
- `Lightweight Concept Lens`：给出概念源流、语义演化、范式阶段、PM 决策问题、反模式或概念债务判断；如果生成 HTML，静态验证已通过或明确说明限制。
- HTML artifact：Dashboard 生成 `dashboard.html` + `summary.md`；学习型报告生成 `report.html` + `summary.md`。两者都使用正确 root marker、运行 `scripts/validate_html_artifact.py` 并完成桌面与移动端检查。Learning Report 还必须通过编辑投影门、深度 rubric 和证据次级呈现检查；Dashboard 还必须保留唯一终态、证据强度、关键变化、residual Gap/risks 和下一步行动。
- `L2`：给出主题地图、核心概念、基础案例、来源和下一步阅读。
- `L3`：Research Project 或聊天报告已覆盖问题清单、证据矩阵、阶段结论和第一阅读入口式 `05_研究报告`；结构化报告已识别 Research Job、建立 Evidence/Explanation Framework 映射并从通过质量门禁的 Framework Vn 综合，未把示例五问、Seed 目录或上一次报告模板当成通用框架。
- `L4`：按当前 Gap 和用户目标形成必要的外部渠道研究、行业案例对照、最佳实践或应用模板，能指导方案设计、选型、商业化、企业 adoption、workflow 设计或 PRD 输入；若是高门槛应用研究，还应给出迁移判断、矩阵、风险和分阶段路径。
- `L5`：形成 watchlist、更新日志、稳定/候选/待验证/废弃结论分层和后续自动化建议；若用户明确确认创建 automation，则调用 Codex `cron` automation，并保留低风险写入边界与人工确认点。
- Product Candidate Research：候选池通过 Quality Gate（至少 3 个候选项有完整 schema 填充）、评分表输出、Candidate Summary 包含 Top candidates 和风险、Cross-Session Handoff 文件可被后续会话或 `decision-research` 直接消费。
- Persona-adaptive 输出：关键结论已说明对当前用户画像、业务目标或应用场景的影响。
- Application 输出：至少给出一个可执行动作、模板、实践任务或判断框架，除非用户只要求快查；当研究是高门槛应用研究时，还要包含决策上下文、证据覆盖、迁移判断、判断矩阵、分阶段建议、风险与待验证假设。
- 如果渠道受限，必须说明未使用的渠道、限制原因和对结论可信度的影响。
- Normal Research/Application 只有命中唯一终态门禁后才算完成；`00-08` 和样本量是按需产物与预算参考，不能替代 Must Claim、关键矛盾、来源追溯和残余 Gap 检查。

## Resource Guide

按当前分支加载，不要一次性读取全部 references：

- 研究入口与 Normal/Application：`mode-selection.md`、`mode-routing-guide.md`、`research-goal-framing-gate.md`、`research-framework-compilation-contract.md`、`research-depth-rubric.md`、`user-context-standards.md`、`iterative-research-loop.md`、`applied-business-research-contract.md`、`source-quality-rules.md`、`report-writing-standards.md`。
- 渠道与写回：`pre-research-source-expansion.md`、`channel-selection-rubric.md`、`channel-registry.md`、`obsidian-output-contract.md`。
- Concept Lens / HTML：`concept-lens-output-contract.md`、`concept-lens-html-dashboard-template.md`、`concept-lens-paradigm-framework.md`、`concept-lens-source-and-factuality.md`、`concept-lens-design-quality.md`；一般研究 Dashboard 使用 `research-dashboard-output-contract.md`；学习型 HTML 使用 `editorial-projection-gate.md`、`learning-report-output-contract.md` 和 `assets/semantic-editorial-template.html`，均运行 `scripts/validate_html_artifact.py`。
- Product Candidate：`product-decision-mode.md`、`project-context-intake.md`、`taxonomy-translation.md`、`candidate-backlog-schema.md`、`cross-session-handoff.md`、`post-research-exits.md`。
- Product Research：`product-evidence-channel-guide.md`；浏览器取证必须读取 `browser-walkthrough-boundaries.md`；完整简报使用 `product-decision-brief-template.md` 和 `scripts/check_product_decision_brief.py`。
- Core Loop：`core-loop-research-handoff.md`；只有发生跨 Skill handoff 或 return edge 时读取。
- Learning/Radar：`learning-pack-standards.md`、`research-radar-loop-contract.md`；回归样例见 `evals/evals.json`。
