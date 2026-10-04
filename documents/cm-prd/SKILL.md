---
name: cm-prd
description: 用户说“把需求拆成可开发规格”“变更现有功能需求”或要求整理方案、任务和验收时使用。支持新项目、存量二开与需求变更；完成后停在人审规格，不直接编码。
---

# cm-prd — 需求文档 → 开发规格生成

执行前读取 `../../runtime/project-context.md`、`../../runtime/review.md`、
`../../runtime/model-efficiency.md` 与 `../../runtime/logging.md`。在需求、方案或任务拆分
命中重要歧义/对抗审查时，追加读取 `../../runtime/steelman-review.md`；它是推理合同，
不增加审查轮次或审批状态。Codex 入口为 `$cm-prd`；Claude Code 跨平台入口为
`/cm-prd`，macOS/Linux 另有历史别名 `/cm:prd`。

新建和变更模式都读取 `references/phase-timing.md`，只为实际执行的阶段写配对
`progress/start|complete`；人工等待前关闭 segment，恢复后递增，不手算耗时。

用户明确要求外部专家，或为本次规格任务开启 AUTO 时，读取
`../../runtime/external-expert.md` 并执行 `../external-expert/SKILL.md` 的任务路由。
AUTO 可把复杂方案比较路由到 CONSULT、权威事实查证路由到 VERIFY，其余保持 LOCAL。
外部结论属于需求/设计输入，必须在本地对照项目事实并进入正常规格人审；AUTO 不
授权外发 docs 或代码内容。

支持两种模式：新建需求和需求变更。

## 输入参数

`用户本轮输入` 格式：

- **新建模式**：`$cm-prd {项目文件夹路径}`
- **变更模式**：`$cm-prd --change {N}.{feature-name} 变更内容描述`
- **可选用例输入**：追加 `--cases {json/md/txt路径}`，或在本轮消息直接粘贴用例

用户提供一个项目文件夹路径，文件夹结构约定：

```text
{项目文件夹}/
├── docs/           ← 需求文档（必须存在，PRD 从这里读取）
├── 1.xxx/          ← 已有的 specs（如有）
├── 2.xxx/          ← 本次生成的 specs
└── ...
```

## JS 准入与当前会话执行

在读取需求正文、解析角色、写 `run_start`、创建或修改 specs 之前，把已解析路径和模式传给：

```bash
node "{CM_WORKFLOW_ROOT}/scripts/cm-prd-entry.mjs" \
  --skill-dir "{CM_WORKFLOW_ROOT}/skills/cm-prd" \
  --project "{CODE_PROJECT}" --specs "{SPECS_DIR}" \
  [--change "{N 或 N.feature}"] [--cases "{用例文件路径}"]
```

准入只核对路径/清单，不读正文或授权写入；selection_required请用户选feature，blocked按reason停。
两种模式ready后读取`references/js-host.md`，以当前会话连接JS宿主；下方步骤提供业务约束，不再手写日志/规格/审批位。
变更、已审修订、恢复及原材料真正变更时，读取`references/js-change-recovery.md`；输入替换须明确授权终止旧批次，再关联新批次全量重审。
两条路径均保留原Step 0–11和人审停点；变更描述、粘贴用例由Skill保留，不能当成工具授权。

## 项目角色路由

路径验证通过后，使用 `{CM_WORKFLOW_ROOT}/scripts/cm-workflow-config.mjs` 读取有效配置，
分别解析 `analyst`（需求分析）、`planner`（方案/任务拆分）及 `policies.generate_cases`：

```bash
node {CM_WORKFLOW_ROOT}/scripts/cm-workflow-config.mjs \
  --project {CODE_PROJECT} --role analyst --runtime {codex|claude} --print-role
node {CM_WORKFLOW_ROOT}/scripts/cm-workflow-config.mjs \
  --project {CODE_PROJECT} --role planner --runtime {codex|claude} --print-role
node {CM_WORKFLOW_ROOT}/scripts/cm-workflow-config.mjs \
  --project {CODE_PROJECT} --print-effective
```

把返回的 `adapter`、`model`、`source` 和 `route_state` 当作本轮的请求路由元数据，
在对应分析/规划提示中注明；`model` 是别名，不能声称为已观测的后端模型。每次角色
边界按 `runtime/workflow-routing.md` 写一条 `decision`/`phase: route` 事件。配置未提供
时使用内置默认值；resolver 返回非零或配置错误时立即 `BLOCKED` 并报告字段路径，
不得进入分析/规划或生成规格。配置的适配器当前运行时不可用时记录 `warning`/`degrade`，
不得伪造调用成功或把外部专家变成编码执行器。

`analyst` 与 `planner` 的上下文和输出按 `runtime/model-efficiency.md` 分包：前者只取
当前需求与相关业务地图，后者接收分析结论、波及模块、约束和 AC 候选。稳定规则前缀
与动态需求分离；不得为方便而重复发送完整项目地图、全部源码或前序对话。只有真实
适配器响应返回 usage 时才记录计数。`route_state: managed-adapter` 时按共享合同调用
`cm-openai-compatible-call.py`，由它写唯一的 `model_usage`；不得由 Skill 重复写。

`generate_cases: false` 只关闭 CM 根据需求自动补生成的 `origin: generated` 用例；用户
或需求源已提供的测试用例仍须保留、规范化并进入审批，不能用项目配置删除测试意图。

项目/specs 路径验证通过后按 `runtime/logging.md` 写 `run_start`。生成规格、重置
审批位或终止时分别写 `spec_lifecycle` 与 `run_done`；详细需求和设计内容不进入主日志。

## 模式判断

如果 `用户本轮输入` 以 `--change` 开头 → **读取 `references/change-mode.md`** 执行变更模式（C1–C8）
否则 → 进入新建模式

---

## 新建模式

### Step 1: 解析输入，读取需求文档

从 `用户本轮输入` 提取项目文件夹路径，记为 `SPECS_DIR`。

读取 `{SPECS_DIR}/docs/` 下的所有文件作为需求源：

- 支持 `.md`、`.txt`、`.pdf`、`.html` 等文档格式
- **HTML 交互原型（可点击 PRD）→ 执行交互遍历协议，禁止只做静态截图**。可交互原型是一份可执行的需求文档，必须用无头浏览器（Playwright / Chrome DevTools）**主动遍历**：

  1. **枚举**每个页面的全部可交互元素（按钮/链接/tab/表单/开关/列表项…）
  2. **逐个操作**并记录三元组：`元素 → 动作 → 结果`（跳转到哪/弹了什么/状态怎么变/无响应）
  3. 产出**功能点清单**：每个有响应的交互 → 对应一条 [F-xxx]；**点了没反应的 → 列为"原型死区"进开放问题**（问用户：是原型没做完，还是本就不需要？不许静默丢弃）
  4. **覆盖率自检**：可交互元素总数 = 功能需求数 + 死区数，对不上不得进入 Step 6
  5. 遍历过程中逐状态截图（Step 8.5 的候选基准）；三元组记录直接生成**交互流 AC 与 E2E 走查清单**

  原型首先是需求，其次才是视觉候选。注意原型通病：只画理想态——异常态/空态/边界值靠 Step 5.5 歧义五问补齐
- 如果 docs/ 下有多个文件，全部读取并综合分析
- 输入含 `--cases` 或本轮粘贴了测试用例时，将其作为用户来源交给 Step 10.4；
  JSON 先做语法校验，Markdown/文本在生成时归一化为测试合同
- 如果 docs/ 不存在或为空，报错提示用户先在 docs/ 下放入需求文档

### Step 2: 获取项目名称

- 从当前目录的 `package.json` name 字段、`Cargo.toml`、`go.mod` 等提取项目名
- 如无法提取，使用当前目录名
- 转为 kebab-case，记为 `PROJECT_NAME`

### Step 3: 探测项目架构类型

**代码项目根的确定（防在错误目录生成脏规格）**：`用户本轮输入` 中显式给了代码项目路径（如 `代码在~/code/app`）→ 以其为准；未给 → 用当前工作目录（约定:在代码项目内运行本命令），但**必须先自检**——当前目录含项目描述文件或源码、且其内容与需求文档所述业务相符；明显不符（如当前目录是另一个项目/工具仓库）→ **停下询问代码项目路径**，不得静默把错误目录当项目上下文（空目录检测只兜全空 case，兜不住"错但有效"的目录）。

扫描项目根目录、配置文件、目录结构、依赖声明，自行判断架构类型（monorepo / 多仓库 / 单体应用 / Web3 等）。记录 `ARCH_TYPE`。

交付形态为微信小程序，或项目存在原生 `project.config.json` + `app.json`、Taro/uni-app
微信构建目标时，标记 `DELIVERY_SHAPE=wechat-miniprogram` 并读取
`../cm-miniprogram-engineer/references/platform-readiness.md`。只出现“小程序”字样但
形态证据不足时进入 Step 5.5 确认，不得根据仓库名猜测。

**空项目检测**：代码项目不存在、或为空目录（无 package.json / Cargo.toml / go.mod 等项目描述文件，且无源码目录）→ **先问用户确认空目录的含义，不得自行假设**：

> "代码目录为空——这是【全新项目】（走 0→1 分支，我来推荐架构和脚手架），还是【存量项目还没 clone】（请先 clone 到该目录，再重新运行 $cm-prd）？"

- 确认全新项目 → 标记 `GREENFIELD=true`，**读取 `references/greenfield.md`** 叠加 G1–G4 规则，Step 4 跳过
- 确认未 clone → **中止本次执行**，提示 clone 完成后重跑（在不存在的项目上下文上生成 design.md 是有毒规格）

### Step 4: 读取项目上下文（存量项目 = 二开模式，叠加 B 规则）

- 按 `runtime/project-context.md` 读取项目约束和本需求相关规则，扫描两层目录了解模块划分
- 读取 `references/context-scope.md`，先做定向代码搜索，再设置
  `CONTEXT_SCOPE=targeted|full`、加载对应地图/代码，并写 `decision/context_scope` 日志
- **B1 代码库参考文档判定**：先读代码项目根 CLAUDE.md 的「业务地图」字段（多层仓库
  下以代码项目根为准，仓库根 CLAUDE.md 无此字段再看地图 00-index 头部；init 已判定过，
  仍须核对相关内容与当前代码）。字段=已生成/已刷新或目录存在 → 按 context-scope 渐进加载并核实；字段=
  跳过(小项目) → 不建议 scan，按范围直接读代码；字段缺失且文档不存在 → 按共享回写合同
  定向还原本次链路，将必要地图文档纳入后续任务范围，不强制先全量 scan；skill 未安装 → 提示重装最新包并按
  直接代码搜索继续。任何路径都不得因追求 targeted 猜测波及面

**二开模式追加规则**（GREENFIELD=false 且本次需求会修改存量代码时生效）→ **读取 `references/brownfield.md`** 执行 B2 波及面 / B3 防护网基线 / B4 增量 specs / B5 拆分锚定地图。


### Step 5: 分析需求

**调用 `cm-product-manager` skill 执行本步和 Step 5.5**——用户故事、编号功能需求、验收标准的编写方法和歧义五问以该 skill 为准。

需求涉及**交易/资产/支付/代币/证券/金融营销**时，同时加载 `cm-finance-expert` skill 协同：领域正确性审核 + 营销合规红线扫描 + 合规开放问题（并入 Step 5.5）。法域确认结果须写入代码项目 `.claude/rules/finance.md` 头部字段；文件不存在时，以 `{CM_WORKFLOW_ROOT}/templates/rules/finance.md` 为骨架现场补生成，并在 AGENTS.md 与 CLAUDE.md 的相关规则说明中补充引用。

从文档中提取功能目标、用户故事、验收标准、约束条件、依赖。

命中重要歧义或方案分歧时，按 `../../runtime/steelman-review.md` 区分已观察事实、参与者主张、当前推断和未知项；“用户真正想要什么”只能写成可修正假设，不能替用户补全业务规则。

### Step 5.5: 开放问题确认

分析需求后，如果存在以下情况，**必须暂停并与用户对话确认**，不要自行假设：

- 需求描述模糊或有歧义的功能点
- 多种技术实现方案且差异较大
- 缺少关键信息（如目标平台、兼容性要求、第三方服务选型）
- 业务逻辑有矛盾或不完整
- 涉及权限、支付、敏感操作等需要明确确认的功能

`DELIVERY_SHAPE=wechat-miniprogram` 时追加平台就绪检查：账号主体、服务类目/资质、
变现路径、权限与隐私、后端/合法域名和发布通道。会改变功能可行性或范围但未确认的
项目必须暂停；只影响后续提审的材料可记为发布待决，不阻塞本地规格与开发。平台政策
结论须记录当前官方查证日期与来源，无法查证时保留开放问题。

格式：

```
❓ 需要确认以下问题：

1. {问题描述} — {为什么需要确认}
2. {问题描述} — {为什么需要确认}

请逐一回复后继续生成 specs
```

所有问题确认完毕后再进入 Step 6。

双向钢人审查只用于暴露假设和失败场景：支持方与反方都取最强版本，但按证据质量加权；无法验证的反方写入开放问题，不强迫给确定结论。

### Step 6: 推断 feature 名称

根据需求内容生成一个简洁的 kebab-case 英文名称。

### Step 7: 生成 specs 目录

检查 `{SPECS_DIR}/` 下已有的编号目录（如 `1.xxx/`、`2.xxx/`），取最大编号 +1。

```text
{SPECS_DIR}/
├── docs/                        ← 需求文档（输入）
├── 1.比如这是一个已有的标题/     ← 已有 specs
└── 2.{feature-name}/            ← 本次新建
    ├── requirements.md
    ├── design.md
    ├── tasks.md
    └── test-cases.json           ← 有可观察行为时生成
```

### Step 8: 生成 requirements.md

```markdown
# {Feature 名称} — 需求规格

## 概述

{一句话描述}

## 项目信息

- 项目名: {PROJECT_NAME}
- 架构类型: {ARCH_TYPE}

## 需求版本

| 日期         | 版本 | 说明     |
| ------------ | ---- | -------- |
| {YYYY-MM-DD} | v1   | 初始需求 |

## 用户故事

- 作为 {角色}，我想要 {功能}，以便 {价值}

## 功能需求

1. [F-001] {需求描述}
2. [F-002] {需求描述}

## 非功能需求

- 性能: {要求}
- 安全: {要求}
- 兼容性: {要求}

## 验收标准

- [ ] [AC-001] {标准描述}

## 依赖

- {外部服务/库}

## 平台就绪（仅微信小程序生成）

{按 cm-miniprogram-engineer/references/platform-readiness.md 记录状态、证据与负责人；
不写任何密钥、证件、Cookie 或测试账号密码}

## 开放问题

- {待确认事项}
```

### Step 8.5: UI 设计基准（涉及 UI 的 feature）

feature 涉及页面/界面时，在生成 design.md 前确定设计基准：

- **有 Figma/设计稿** → 通过 MCP 导出截图 + token 提取物，落盘 `{SPECS_DIR}/{N}.{feature-name}/design-baseline/`（防链接失效与云端改版导致基准漂移）
- **有 Stitch 项目** → 通过 Stitch MCP 拉取设计并导出 HTML/CSS 落盘 design-baseline/；导出的 HTML **按 Step 1 交互遍历协议处理**（多屏/流转设计可直接提取交互流与功能点）——Stitch 导出物默认按像素基准对待（它就是设计本体，不是示意）
- **有 HTML 交互原型**（Step 1 已截图）→ **必须人工三选一确认基准档位**（中性提问不带引导；高保真原型建议像素档，线框灰稿建议结构档）：
  - **① 像素基准**：UI 与交互 **1:1 还原**——截图落盘 design-baseline/ 作 BackstopJS 基准（≤1%），且**交互流提取为 E2E 走查清单**（每个跳转/状态切换/反馈逐条断言，交互不 1:1 视为验收失败）
  - **② 结构基准**（多数原型的合理档）：页面结构、信息层级、**交互流程必须一致**，视觉样式可再设计——验收为逐页元素清单核对 + 流程走查
  - **③ 纯参考**：仅辅助理解需求，无对照验收——选此档即明确接受 UI 由 AI 自行发挥（历史事故：原型被降为参考后，产出与原型完全不符）
  档位写入 design.md「设计基准」节；**无论哪档，原型的页面清单与跳转流程都已是需求的一部分（Step 1 规则），流程不允许自由发挥**
- **无设计稿且环境已安装 `huashu-design` skill** → 调用其生成高保真原型（**要求包含 hover/空态/错误态等交互态**），落盘同上；**人审规格时一并确认设计方向**（复用既有强制卡点，执行期零设计决策）
- **两者皆无** → 不建基准、**不生成 UI 还原任务**，该 feature 的 UI 由前端任务按 design.md 自行实现；可提示用户 `npx skills add alchaincyf/huashu-design`

**基准机读化(四种来源统一要求——截图给人看,规格表给 AI 抄)**:design-baseline/ 除截图外必须含**逐元素规格表**(spec-sheet.json:字体五件套/色值/几何/间距)。AI 看图估值的精度天花板极低,是还原度不理想的头号根因(实跑反馈);规格表按基准形态产出:

- Figma MCP → 直接读取节点精确值(排版/填充/自动布局间距)导出成表,不经截图转译
- Stitch 导出 / HTML 原型 → 用 `{CM_WORKFLOW_ROOT}/templates/ui-lens/cm-ui-lens-extract.mjs` 对基准页提取计算值成表；样式值优先**移植改造**而非重新想象
- **纯截图(最弱形态)** → 色板可精确采样成表;几何只能估算——规格表标注「几何估算档」,并明确提示用户:有 Figma/原型源尽量给源,纯截图基准的还原精度天花板显著更低
- **基准字体文件一并落盘**(还原页先加载同款字体再对比,防字体回退噪声淹没真差异)

有基准时，design.md 记录基准路径，且「接口契约」节须包含**组件契约**（组件名 / props / 事件）。

### Step 9: 生成 design.md

复用 Step 4 已加载的项目约束与规则；根据最终波及层补读新命中的相关规则，禁止再次
全量读取未变化的 CLAUDE/rules。设计方案必须遵循项目已有的技术规范和约定。

按功能模块设计，每个模块说明涉及哪些层（前端、后端、数据库、合约等），具体分层根据项目实际架构决定，不做硬编码限制。

```markdown
# {Feature 名称} — 技术设计

## 设计版本

| 日期         | 版本 | 说明     |
| ------------ | ---- | -------- |
| {YYYY-MM-DD} | v1   | 初始设计 |

## 项目架构

- 架构类型: {ARCH_TYPE}
- 涉及层: {根据项目实际情况列出}

## 功能模块设计

### 模块 1: {模块名}

{技术方案，遵循 .claude/rules/ 中的规范}

**涉及层及关键设计:**

{根据项目实际分层描述，如数据模型、API 接口、组件设计、合约接口等}

### 模块 2: {模块名}

...

## 接口契约

{API、RPC、合约接口等 — 根据项目类型决定}

## 数据模型

{数据表/模型/链上存储 — 根据项目类型决定}

## 安全考虑

{基于 .claude/rules/security.md 和项目特有的安全规范}

## 技术决策

| 决策 | 选项 | 理由 |
| ---- | ---- | ---- |
```

### Step 9.5: 方案对抗审查（最贵的决策补上第二双眼睛）

design.md 生成后，满足任一触发条件 → 按 `runtime/review.md` 交**新上下文的独立审查者对抗审查一轮**：

- GREENFIELD 的 ADR（架构选型是最贵决策）
- design 含新模块、架构边界或依赖方向变化、跨模块/跨仓库数据流
- 新增第三方运行时依赖或改变核心工具链
- 修改公开接口契约、数据模型/数据库迁移、认证授权、支付资产或其他安全敏感逻辑
- 功能点 F ≥ 5 的大 feature

**仅修改存量模块不再单独触发本步。** 单模块内部的文案、样式、小交互、校验、
现有模式下的小型 CRUD、缺陷修复或补测试，在没有命中上述风险信号时跳过本步，
并把关键方案检查合并到 Step 10.6。执行过程中一旦发现真实范围扩大并命中风险信号，
必须补做本步后再继续生成最终任务单。

**投喂内容**：requirements.md + design.md 全文 + 项目上下文中的相关规范 +（二开）「波及面」段与被改存量模块现状代码。
提示词要义：审查者同时读取 `../../runtime/steelman-review.md`，把当前方案当成可证伪假设：
先列关键前提和最强支持，再重点检查架构隔离、模块边界、与现有管线的耦合、数据流缺口，
给出“输入/状态 → 路径 → 错误结果”的最强反方失败场景，以及能区分双方的最小验证。
支持与反方不等权；只报告有具体后果的问题，零发现明说（审查产出纪律同 N4）。

调 reviewer 前先真跑 `cm-prd-review-gate.py inspect --stage design`，证据固定为
`prd-{feature}-design-r1.md`，处置回执固定为
`prd-{feature}-design-disposition.json`：`dispatch_once` 才允许调用 reviewer；
`resume_disposition` 表示 r1 已落盘，直接继续应用/升级现有 findings，禁止重审；
`completed` 直接进入 Step 10。处置完成后真跑 `record --artifact {design.md}`，记录
`applied|no_findings|escalated`、finding/unresolved 数量和 r1 SHA。进程在 r1 落盘后
崩溃也只能恢复处置，不能再消耗一轮审查。

**单轮硬边界（ROUND_LIMIT=1）**：每个 feature 在本阶段只允许一次 review attempt，
独立 reviewer 与 `self-degraded` 复查二选一。零发现直接进 Step 10；
采纳项由主执行者修正 design.md 后进 Step 10，并由后续 10.5 自检验证完整规格；分歧或
无法机械确认的项写入摘要卡「风险点」交人裁决。**禁止 review → 修正 → 再 review**，
也禁止换一个审查者变相开启第 2 轮；凭证只允许 `design-r1.md`，不得生成 `design-r2.md`。
任何审查尝试（包括 `self-degraded`）均消耗唯一一轮；通道恢复后不得补审。
（实跑教训：公共 CLI 契约的 3 轮方案复审耗时 11m59s，后两轮应由自检与人审承担。）
未命中上述风险信号的低风险 feature 不触发，零额外负担。
**凭证落盘**:审查原文 tee 到 `{SPECS_DIR}/.reviews/prd-{feature}-design-r1.md`——摘要卡「方案对抗审查」行必须与凭证对得上,无凭证的数字是自报(凭证教义全框架一体,规格期不豁免)。

> 依据：代码有 N4 对抗、规格有 10.5 自检，唯独技术方案此前无第二模型把关——而方案错误是最贵的错误（行业重度实践的最大单笔收益正是方案期拦截架构缺陷）。

### Step 10: 生成 tasks.md

**按功能拆任务。** AI 执行时根据 design.md 自动判断每个任务涉及哪些层。

```markdown
# {Feature 名称} — 任务清单

## 任务版本

| 日期         | 版本 | 说明     |
| ------------ | ---- | -------- |
| {YYYY-MM-DD} | v1   | 初始任务 |

## 项目信息

- 项目名: {PROJECT_NAME}
- 架构类型: {ARCH_TYPE}
- specs 路径: {SPECS_DIR}/{N}.{feature-name}/

## 任务列表

### UI 还原（仅当存在 design-baseline 时生成本节）

- [ ] T-001: 还原 {页面/组件} ~30min（基准: design-baseline/；本 feature 的前端功能任务依赖本任务）

### 功能 1: {功能名}

- [ ] T-002: {任务描述} ~{预估时间}
- [ ] T-003: {任务描述} ~{预估时间}

### 功能 2: {功能名}

- [ ] T-003: {任务描述} ~{预估时间}

### 集成与测试

- [ ] T-010: 联调测试 ~{预估时间}
- [ ] T-011: E2E 测试 ~{预估时间}
- [ ] T-012: 部署 staging 并冒烟验证 ~15min（依赖本 feature 全部开发与测试任务）

> 部署任务前提：项目存在部署形态（Dockerfile / CI 配置 / 部署脚本，或 0→1 项目——bootstrap 已建 CI 骨架）才生成 T-012；**纯本地工具、库等无部署形态的项目不生成**，避免执行期反复触发"无 staging 环境"上报。

## 依赖关系

- T-002 依赖 T-001

## 风险点

- {可能遇到的问题及应对}
```

**任务拆解原则：**

- 按功能拆，AI 执行时读 design.md 自动识别涉及哪些层；**二开项目按 B5 锚定业务地图**（feature 沿 07 线路、任务尽量单模块）
- 原子性，可独立完成和验证
- **同一组件/同一文件内的行为不拆分为多个任务**（如"渲染列表项"和"列表项的删除确认"归一个任务）——拆开会导致执行时自然合并、任务标记与提交失配（实跑验证的教训）
- 预估完成时间（5min / 15min / 30min / 1h）
- **粒度控制**：每个子 specs（feature 目录）不宜过大，单个 tasks.md 控制在 **10-15 个任务以内**。如果需求过大，应在 Step 6 之前拆成多个独立的 feature 目录（如 `2.user-auth-login`、`3.user-auth-register`），每个 feature 有自己的 requirements/design/tasks 三件套。这样 cm:ai 执行时上下文可控，不会因为 specs 太大导致丢失关键信息。
- **假依赖不写**：基线/度量类任务只读基准提交，仅当后续任务真正读取其产物时才写前置依赖，避免无必要的串行等待。
- **接口先行**：设计中接口签名已冻结且实现方与调用方可分人时，先落 5–15min 的契约任务（导出签名 + 抛错占位体 + 契约测试），实现任务与调用方任务都依赖契约任务、彼此不依赖，以便独立开发。调用方与实现方任务的描述里必须写明「契约任务的占位体会抛错，这是预期状态，不要等待它被实现、不要因此报 blocked」。
- **测试文件按任务独立**：每个任务的新增用例写入自己的测试文件（命名遵循项目 testing 规则，无规则时用 `test/<feature>-<task>.test.*`），不向同一个已有测试文件追加，避免任务间写入冲突。

### Step 10.4: 生成 AI 测试合同（条件触发）

读取 `../../runtime/test-contract.md`，按其中的生成条件为适用 feature 写
`test-cases.json`。用户或需求源提供的用例优先且标记 `origin: "user"`；其余根据
AC、design 和 tasks 补齐，保证 AC→TC→Task 可追踪。纯文档/注释/类型/无行为重构
不生成空文件。写完执行 `scripts/validate-test-cases.mjs`。

`DELIVERY_SHAPE=wechat-miniprogram` 时同时读取
`../cm-miniprogram-engineer/references/release-checklist.md`，只为本 feature 实际使用的
授权、平台 API、网络/云能力和真机差异生成用例；不用的能力不扩写。需要开发者工具、
真机或后台才能证明的 expected 必须保留相应执行前提，不得改写成 Web 可替代验证。

### Step 10.5: 规格自检（机器项，AI 自查自修，人不参与）

读取 `references/spec-self-check.md` 并逐项执行；测试合同必须调用 `scripts/validate-test-cases.mjs`，不得靠目测。设计已接受后，仅整稿自检失败可附原因修订原清单内的需求/设计，保留失败和两轮上限，改动交本轮拆分审查并在风险点说明，不另做设计审查。

### Step 10.6: 独立规格审查（方案 + 任务拆分）

10.5 自检是机器项，查不出「**方案是否明显错向、任务是否拆对**」。自检通过后，
按 `runtime/review.md` 把精简的方案与拆分结果交给新上下文的独立审查者。Step 9.5
已触发时不重复审原方案，但须审自检失败后登记的需求/设计改动；因低风险跳过时，本步同时承担关键方案检查：

- **投喂内容**：requirements.md 功能点清单 + tasks.md 全文 + design.md 的方案摘要、
  关键技术决策、接口/数据契约与「波及面」段（二开）。不喂三件套全文；Step 9.5
  已审过完整方案时，核对任务是否偏离已审设计；有自检修订时，同时审阅登记的改动。
- **提示词要义**：审查者读取 `../../runtime/steelman-review.md`，把规格当成可证伪假设。
  先检查方案有没有明显错向、遗漏的
  失败场景或与现有边界冲突，再检查拆分质量：①任务边界有无重叠/遗漏 ②依赖顺序
  会不会卡死 ③粒度是否适合单任务交付验证 ④二开：波及面有没有漏掉会被牵连的
  模块。反方必须写成具体后果；不把正反意见当等权，不用推理替代测试或需求证据。
  只报有具体后果的问题，没有问题就明说。
- **单轮硬边界（ROUND_LIMIT=1）**：每个 feature 在本阶段只允许一次 review attempt，
  独立 reviewer 与 `self-degraded` 复查二选一。采纳项修正 specs 后
  重跑一次 10.5 自检；失败记 `self_check_failed` 回执，保留失败与决定，写入摘要卡「风险点」交人裁决。
  **禁止 review → 修正 → 再 review**，也禁止换审查者变相开启第 2 轮；凭证只允许
  `split-r1.md`，不得生成 `split-r2.md`。（实跑教训：规格修正后的再次召回复审没有
  新增独立决策层，却继续占用主流程时间。）
  任何审查尝试（包括 `self-degraded`）均消耗唯一一轮；通道恢复后不得补审。
- **凭证落盘**：原始审查结果写入 `{SPECS_DIR}/.reviews/prd-{feature}-split-r1.md`，文件头使用 review contract 的 `reviewer/independent/at/scope` 字段
- 调 reviewer 前同样真跑 `cm-prd-review-gate.py inspect --stage split`；只在
  `dispatch_once` 调用一次，`resume_disposition` 复用已有 r1，`completed` 不再审。
  split 处置可修正 requirements.md、design.md 及任务文件；先按原发现登记并保存，任何改动都须执行一次 10.5 自检，失败不重试、不冒充通过。
  再 `record` 全部三件套及已有 test-cases.json，生成 `prd-{feature}-split-disposition.json`；其中新 SHA 成为后续读取的版本；失败回执只表示处置完成，仍待人裁决（见 `references/js-host.md`）。
  待登记时仅原包、完整处置计划与磁盘 SHA 匹配的补正可继续；回执后再改、跨 feature 借用或出现 r2 均阻断。
- **降级**：无法建立独立上下文时，由主执行者对抗式复查，凭证写 `self-degraded` / `independent: false`；这是增益层，不单独因降级停车

> 依据：低风险小需求不值得额外支付一轮完整方案对抗，但仍需要第二双眼睛同时检查
> 关键方案与任务拆分；高风险需求继续保留 Step 9.5 + 本步两层审查。

### Step 11: 输出总结（附规格摘要卡 + 审查清单）

**先输出规格摘要卡**——人审的第一入口是这张一屏卡片，不是三个长文件（实跑教训：直接丢长文件，人审会退化成扫一眼就"通过"）：

```text
┌─ 📋 规格摘要卡 ────────────────────────────
│ 交付形态: {Web/App/小程序…}   ← 第一分叉,看错全错
│ Feature: {N 个}: {名称列表}
│ 历史 feature：{N} 个已登记，{M} 个含旧版归档说明
│ 功能点: {N} 个 | AC: {N} 条 | 任务: {N} 个(预估 {x}h)
│ 开放问题: {已答 N / 共 N}——{逐条一行: 问题→答案}
│ 风险点: {金融/合规/破坏性操作等敏感项,无则"无"}
│ 上下文范围: {定向 / 完整 / 定向→完整（reason_code）}
│ 平台就绪: {就绪/待官方核验 N 项/不适用}
│ UI 基准: {像素级/结构级/纯参考/无}
│ 🧪 AI 测试合同: {N 条(user N/generated N) / 跳过(无可观察行为)}
│ 🔎 规格自检: {N}/{N} 通过{（未过项已列入风险点）}
│ 🧠 方案对抗审查: {通过 / {N}条已修 / 跳过(低风险,并入独立规格审查)}
│ 🤖 独立规格审查(方案+拆分): {通过 / {N}条已修 / 降级自审}
└────────────────────────────────────────────
有疑问的行,点开对应文件细看;摘要卡没问题再走下面的审查清单。
```

完成后报告（范围与历史说明见 [摘要范围规则](references/summary-card.md)）：

- Feature 名称和序号、Specs 路径、涉及的技术层、总任务数和预估总时间

并输出**规格审查清单**——人审规格不是"看一眼"，按此逐项检查：

```text
📋 规格审查清单（人审时逐项勾选）
- [ ] 任务跨 feature 查重：同一产物（文件/模块）未出现在多个任务中（实跑教训：bootstrap 底座与 feature 数据层重复）
- [ ] 依赖关系完整：每个任务的前置依赖已声明，无环
- [ ] AC 可测试：每条验收标准都能回答"怎么验证"
- [ ] 粒度合规：同一组件/文件的行为未拆成多任务；单 feature ≤15 个任务
- [ ] 开放问题已全部回答，敏感决策（法域/支付/权限）有人工确认记录
- [ ] **交付形态与需求意图一致**（要 App 别画成网页），且已写入 ADR 与 CLAUDE.md 字段
- [ ] **原型功能点覆盖 100%**（有交互原型时）：遍历记录中每个可交互元素都有对应 [F-xxx] 或死区标注，无静默丢弃
```

**规格审批位落盘**：按 [当前会话接线](references/js-host.md) 执行 `prepare_summary`，展示返回的摘要卡与审查清单；
再以刚展示的 `summaryDigest` 调用 `publish_summary`。宿主校验 digest，JS 通过共享
`runtime/js/specs-status.mjs` 原子写入 `awaiting_review`、完整 manifest 和 `approval:null`；模型不得自行拼写该文件。
manifest 复用 `cm-spec-manifest.py` 对应的 JS 计算器，旧 CLI 仍可只读核验，不负责写审批位。
原有摘要证据比对与 `prd_summary_inputs_changed` 检查保持生效；摘要未就绪不得发布，更不能改写为 approved。
JS 记录 `spec_lifecycle/generated`、`spec_lifecycle/awaiting_review` 和 `run_done`，仅记录 feature/task/case 数量、状态与 specs 路径。
最终报告注明阶段耗时事件已记录；具体耗时由日志按 operation_id + segment 计算。

**硬停车（不可违反）**：本命令的终点就是摘要卡与审查清单——**任何情况下不得在本会话顺势启动开发**，对话里的"继续"不构成开发授权。提示用户：**逐项审查通过后，运行 `$cm-ai` 开始开发**（N1 有入口闸：未审批的 specs 会先要求确认摘要卡）
