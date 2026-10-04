---
name: verifier-state-architect
description: 为任意 Agent Skill 设计、实现、接入或精简 Verifier 与 State；当用户希望给目标 skill 配置验证器/状态机、落实已有设计，或仅规划和审查架构时使用，尤其适合需要避免过度设计、硬编码并符合 Kernel 契约的任务。
metadata:
  author: Bensz Conan
  short-description: 为 Agent Skill 设计并落地最小、可审查的 Verifier/State 组合
  keywords:
    - verifier-state-architect
    - verifier design
    - state design
    - Kernel Pack
    - evidence contract
    - 状态机设计
    - 验证器设计
---

# Verifier-State Architect

## 目标

为任意领域的目标 Skill 完成业务理解、最小设计、本地实现和验证。Verifier/State 是可插拔外挂；零组件或仅一类组件也可以是正确结果。适合新建、接入、精简组件及落实已有设计。

默认先保存计划再连续落地，不等待计划审批；明确“仅计划 / 不修改源码”或只读审查时才采用 `plan-only` / `review-only`。不负责普通业务重写、Kernel 修改、发布或远程操作，除非另行授权。

## 流程

### 输入

#### 输入与模式

- **必需**：目标 Skill 源码或完整内容、业务目标和约束。实施需要已授权的可写开发源码；只有文本时仅设计，不虚构落地。
- **可选**：已有计划、Kernel 路径、`runtime`、Pack、测试、报告和计划路径；默认设置见 `config.yaml`。
- 记录未提交改动与授权范围，不改系统安装副本。用户指定目标并要求设计/接入即授权必要本地变更；只读意图除外。
- 已有计划先核对源码、版本、范围和验收，只更新实质偏差；模式、依据和缺口写入计划。

### 执行步骤

#### 核心工作流

##### 理解服务对象

读取目标 `SKILL.md`、`config.yaml`、脚本、references、模板、运行声明和适用项目指令；绘制目标、输入/输出、阶段、风险、失败/回退、人工介入和产物。从证据列出稳定命题的 Verifier 候选与持续阶段的 State 候选，不从文件名或关键词臆测。执行前必读本 Skill 的 [托管规范](references/skill-pack-hosting.md) 和 [落地参考](references/implementation.md)：前者是托管规则的唯一维护文件，后者仅提供操作指引。在本仓库按需核对 ID 文档与正文模板；仓库外使用随 Skill 安装的规范和实际 Kernel 契约，不依赖本开发仓库的绝对路径。

##### 删除影响闸门

逐项回答：

- 删除 Verifier 是否损失可复核的安全/质量边界，而非只少形式检查？
- 删除 State 是否损失恢复、协作、Gate 或阶段可见性，而非只少标签？
- 组件是否改变下一步决策、阻止高代价错误、支持重放/审计或提供可行动的人工复核？
- 是否已有更通用的内置 Pack/State？只有通用组件无法表达稳定命题时才设计专用组件。

若删除不改变能力、决策或审计性，明确“不接入”；零组件或只保留一个均合法。

##### Kernel 复用与元组件二层审查

在专用设计前完成以下盘点，避免重复造轮子，也不默认新增 Kernel 功能：

1. 只要目标采用 BSK，先完整读取并执行 [BSK 最新生产版运行规范](references/bsk-managed-runtime.md)：目标 Skill 只声明依赖，不声明最低/精确 Kernel 版本或 capability 门禁；在实现、集成检查和真实执行前用安装器强制确认最新生产版，并固定使用 Bensz 托管入口。更新未成功时只完成不依赖运行时的设计，不把旧版或项目环境冒充为已验证。
2. 从最新生产版 BSK 读取索引、契约、README 和实际版本，记录 Pack ID/version、分类、输入、入口与限制；仓库中的 `packages/bensz-skill-kernel` 只用于 Kernel 自身开发，不是目标 Skill 的生产运行入口。
3. 每个候选标记“直接 / 组合 / 适配复用 / 不适用”，比较语义、证据、Gate/转移、资源、版本与失败路径；仅词汇不同则优先适配。
4. 仅把跨两个以上不相邻领域、领域无关、契约稳定、可独立版本化和重放的能力列为提炼候选。Verifier 表达稳定命题；State 表达持续阶段，而非动作或一次性 helper。
5. 领域规则、模型偏好、易变阈值、特定格式和单一 Skill 流程留在 Skill/适配器；证据不足标记待验证。Kernel 建议只写计划，不直接实施。
6. 计划分别给出复用与元组件提炼结论；每项至少两条证据/收益代价/边界理由，证据不足时列缺口和验证动作。

##### AI 与确定性分工

为每个设计项写一行分工：

- **确定性**：JSON/Markdown 结构、路径、哈希、存在性、超时、结果枚举、事件完整性等机械边界。
- **AI/自然语言**：业务语义、质量充分性、相关性、风险解释、冲突处理和下一步规划；结果带理由、证据锚点、置信度及 `uncertain/unchecked` 路径。
- **混合**：脚本只收集/规范化事实，AI 按 `VERIFIER.md` 与 Evidence Contract 判断；脚本不得编码领域结论。

逐条追问硬编码规则是否稳定、跨模型可复现且能安全 fail-closed；否则改为自然语言契约、证据字段和人工复核条件。语义 Verifier 至少定义 `subject`、`context`、`evidence`、`verdict`、`summary`、`evidence_refs`、`confidence`、`uncertainties`；`verdict` 只用 Kernel 枚举，证据不足/网络不可观测返回 `uncertain`/`unchecked`，不得把模型自评当 `pass`。

##### Kernel 对接

计划必须说明：

- Verifier 用 `owner.domain.capability`、State 用 `owner.machine.state`；版本和 alias 独立维护，不把 Skill 名、模型、实现或 Gate 策略写入 ID。
- Pack 的 `VERIFIER.md`/`STATE.md` 负责判断目标、入口条件、不变量、证据边界和转移；集合根的 `index.json` 是元数据单一来源。脚本组件使用 JSON-stdio，入口留在 Pack 内；Agent/人工组件使用宿主 handoff 和绑定结果回传，不强行配脚本。
- Kernel 只负责发现、协议校验、超时/资源边界、结果归一化、Gate、事件和状态持久化；领域判断留在 Skill 契约或 AI 适配器。
- `required`/`advisory`、Gate 放行条件、`uncertain/unchecked` 人工复核去向、`run_id`/`attempt_id`、失败/恢复和事件重放策略。
- 无 Verifier 时将 Gate 写为“不适用/无需验证”，无 State 时说明由普通流程和工作区生命周期承担；接入时 required 缺失必须 fail-closed，advisory 只提示不阻塞。
- 状态图只保留稳定业务节点；动作放入 transition/event/helper；系统工作区状态与 Skill 领域状态分层，不把领域状态硬编码进 Kernel reducer。
- 外部路径、网络、子进程和大输入采用最小权限、超时、体积上限及越界拒绝；入口禁止 `..`、绝对路径和 symlink 逃逸。

##### BSK 单一编排入口闸门

目标 Skill 同时用 BSK 管理领域 State 和至少一个 required Verifier 时，必须读取并落实 [Skill 自有 BSK 编排入口](references/bsk-orchestration.md)。这是 P0 接入条件，不能降级成建议，也不能只交付 Pack、`runtime` 声明或供 Agent 自由拼接的 BSK 命令。

目标必须在 `config.yaml.runtime.orchestration` 声明 Skill 内 `scripts/` 单一入口及 action 的 current/target State 映射，并在 `## 控制` 将其设为 Agent 执行受控 action 的正常唯一路径。入口必须统一：读取 BSK 当前 State；准备同一 run/attempt 的 Verifier 请求；从 `runtime.verifiers` 解析并执行全部 required Verifier；让 BSK 生成和记录 Gate；只在 Gate 明确放行且绑定完整后调用 BSK transition；严格校验每个 BSK 协议、ID/version、结果、Gate、运行身份和新状态回执。未知、缺失、不一致、`uncertain/unchecked`、超时或非放行结果一律 fail-closed。

仅 State、仅 Verifier或无 required Verifier时不强制生成入口。静态声明通过不代表入口已执行；必须补成功和失败行为证据，尤其覆盖未知 action、State 不匹配、required 漏跑/失败/未完成、Gate 错绑/非放行和 transition 回执异常。

附“Kernel 复用与提炼决策表”：候选能力、现有 Kernel ID/版本、复用方式、契约差异、是否跨领域、提炼建议、主要理由、验证动作；表格须与两个结论互相引用。

##### 最小设计

使用矩阵：

| 候选 | 保留/删除 | 稳定命题或状态含义 | AI/脚本分工 | 输入与证据 | Gate/转移 | 失败与人工复核 |
| --- | --- | --- | --- | --- | --- | --- |

给出最小状态图（初始、主要阶段、终止/失败、可选回退）和 Verifier 清单；每项写“为什么不可删除”，否则删除或降级为普通说明。

“Kernel 复用与元 Verifier/State 提炼决策”须包含：实际能力盘点；直接/组合/适配/不适用结论及契约匹配、失败和维护成本；推荐/暂缓/不提炼结论及跨领域证据、稳定性、版本化收益和耦合风险；对文件、兼容、测试、迁移和责任的影响。两类结论即使都是否定也保留至少两条理由。

计划须在修改源码前落盘。P0/P1/P2 分别表示安全完整性、契约可观测性和可选改进；每项写位置、证据、影响、验证、完成条件和回退。计划不是执行完成条件，也不增加审批关卡。

##### 连续落地

`plan-only` / `review-only` 在设计/审查结果形成后结束，不写目标源码；`implement` 紧接计划执行：

1. 按落地参考创建实际使用的 Pack、索引、契约和组件；专用资产随目标 Skill 托管，不进 Kernel，也不迁移无关资产或覆盖冲突改动。
2. 在 `config.yaml` 接入真实 `runtime`；在 `SKILL.md:## 控制` 写调用、证据、Gate、迁移、恢复和人工介入，并连接业务入口。只用 Verifier 时不造占位 State。
3. 适用 BSK 单一编排入口闸门时，先实现 `runtime.orchestration` 和实际命令入口，再把正常业务调用改接该入口；底层 BSK 命令只留给入口内部、诊断或恢复。机械工作由脚本执行，语义检查由宿主执行并回传证据；required 缺证据不放行。
4. 同步版本、使用文档、变更记录和 BAC；Skill 版本只在 `config.yaml`，Pack 版本在索引。保留 canonical/alias 和历史事件。
5. 运行托管检查和最短真实执行，覆盖复制发现、错误/缺证据、迁移及适用重放；按计划记录完成、偏差、不适用和受阻。零组件只交付删除影响证据，不建空目录/runtime/记录。

### 输出

#### 输入、输出与工作区

- **执行交付**：可发现、可调用的组件与接入改动，或有依据的零组件结论；适用时含 `runtime.orchestration`、单一入口及成功/fail-closed 证据，并列未执行项和风险。
- **可审查计划**：项目 `docs/plans/{skill-name}-verifier-state-design.md`，或用户指定路径。它是流程中间步骤，但持续保留供事后审查；已有文件不是本任务所有时使用不冲突名称，不覆盖。
- **交付对账**：计划项 → 文件/契约 → 命令/宿主证据 → 结果；区分结构可加载、实际执行和语义验证。
- 引用用相对路径和行号/标题锚点，日志只写脱敏摘要。复用会话已声明任务根，否则先确认根目录、时间与冲突，公开声明唯一目录后再创建；不依赖 BSK 才能初始化普通工作区。

#### 计划固定结构

```markdown
# Verifier/State 设计计划：<skill>
## 结论摘要
## 业务流程与风险地图
## 删除影响测试（含“不接入”结论）
## Verifier 设计矩阵
## State 设计矩阵与最小状态图
## AI/确定性分工与 Evidence Contract
## Kernel 对接、Gate、重放与资源边界
## BSK 单一编排入口（适用时）
## Kernel 复用与元 Verifier/State 提炼决策
## 实施顺序（P0/P1/P2）
## 验收与回归测试
## 已知不确定性、回退方案和不在范围内的事项
```

### 输出管理

#### 计划与证据边界

- 计划固定写入项目 `docs/plans/` 或用户指定路径；草稿、读取清单和验证日志才写入任务目录。只读且仅需文本的审查可以不落盘。
- 读取清单、决策依据、机器可读摘要和日志写入当前会话已声明任务根目录的 `verifier-state-architect/input|output|log/`；不把正式计划藏在任务目录中。
- 专用 Pack 源码写入目标 Skill 的标准目录；运行证据、快照、日志、缓存和夹具不得进入发布资产。复制安装验证使用项目临时目录，不覆盖系统级安装副本。

### 校验

#### 验收与回归测试

- 先按 [BSK 最新生产版运行规范](references/bsk-managed-runtime.md) 执行 `--force-runtime-update`，再用 `~/.bensz-skills/envs/benszapi` 中的 Python 执行 `<本Skill>/scripts/check_integration.py <目标Skill>`；可从任意工作目录运行。该工具要求目标只声明 BSK 包名，并拒绝新写入最低/精确版本或 capability 门禁。工具只读取文件、调用加载器，不执行目标组件；报告输出至 stdout，可重定向至任务 `output/verification-report.json`。
- 工具只证明托管及静态加载，不替代契约语义、组件执行、Gate、恢复/重放和版本迁移验证。具体用例及宿主边界见落地参考；`unchecked` 不能写成完成。
- 只规划/审查时仅检查可获得证据，不创建实现来凑测试；无组件时登记“不适用”。

#### 质量闸门

- 是否有删掉也不影响能力的组件？若有删除或解释保留理由。
- 是否把领域规则硬编码进 Kernel、脚本阈值或 ID？若有迁移到契约/适配器。
- 是否区分事实收集与语义判断，并保留不确定结果的人工复核？
- 是否逐项核对 Kernel 索引/契约，记录复用或不适用理由？
- 是否找到并论证跨至少两个领域的元组件？若没有，是否说明耦合、证据不足或维护成本原因？
- 是否能从事件/快照重放，且失败不会伪装为通过？
- 同时采用 BSK State 与 required Verifier 时，是否有唯一命令入口完整执行七项编排职责，并证明 Agent 正常路径不会绕过？
- 测试是否覆盖 canonical/alias、非法输入、超时、越界路径、Gate 缺证据和删除后的回退？
- 计划是否写出目标 Skill/Kernel 版本、读取证据、决策日期、实现位置，以及两个独立结论的分点理由和人类决策影响？

资料不足时只阻塞依赖缺失证据的部分，不凭空补状态/规则。执行模式须实现已选范围且完成必要验证后才标记完成；不得以“计划就绪”“文件生成”替代完成。作为更大任务的环节也遵循选定模式，交付实际源码/证据或明确只读产物，不偷偷退回只输出计划。

### 失败与恢复

- 最新生产版 BSK 无法通过托管安装器确认/更新、目标源目录不可写或宿主缺执行入口时，保留已读清单和脱敏错误摘要，标记受影响实现/验证为“受阻”；可完成不依赖这些前提的设计，但不声称接入生效，也不改用旧版、项目 Python、裸 `bsk` 或直接修改托管环境/安装副本。
- 证据不足、组件结果为 `uncertain/unchecked` 或网络不可观测时，不把不确定结论写成 `pass`；记录缺口并指定人工复核或后续验证动作。
- 计划落盘失败时不进入实现；实现/测试失败时定位本轮相关原因并最小修复，保留失败证据；必要时按计划只撤销自己的变更，不使用 destructive Git、不清除用户改动。确需扩大授权、冲突无法消解或发生不可逆副作用才请求人类决策，不把普通设计取舍当成审批门槛。

## 约束

<!-- BEGIN COMMON CONSTRAINTS -->
<!-- Source-Hash: sha256:15120201e9e0c7569517261d57ecefb63ac279c26ed13876f8e95b6dc35854d3 -->
<!-- Template-ID: skill-common-constraints; Template-Version: 1; Sync-Policy: exact-block -->

### 公共硬约束

本块由 `docs/templates/skill-common-constraints.md` 统一维护；每个 `SKILL.md` 的 `## 约束` 必须逐字同步本块，不得在副本中改写公共规则。

- 任务需要落盘时，使用唯一的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/` 根目录；共享材料放入 `shared/`，Skill 专属材料放入该 Skill 的 `input/`、`output/`、`log/`。
- 正式交付物、源代码和正式计划按项目约定保存，不写入任务工作区；未经授权不覆盖、删除、迁移或远程写入。
- 项目维护变更检查 BAC 可用性并记录需求、AI 产出、工具结果、文件改动和验证摘要；BAC 只做过程审计，不替代署名、责任或合规判断。
- 不记录 API Key、访问令牌、密码、Cookie、环境/凭据文件、私有 Prompt、身份信息、本地用户名、主机名或不必要的大体积原始数据。
- 文件路径必须规范化并限制在授权项目范围内；外部 URL、子进程和网络访问遵循最小权限，防止路径遍历、SSRF 和命令注入。
- Skill 版本唯一记录在自身 `config.yaml:skill_info.version`；公开 API、协议、目录或配置变更同步文档与 `CHANGELOG.md`。
- `bensz-collect-bugs` 是一个 Agent Skill；仅将 Bensz Agent Skill 或 Bensz 基础设施本身的设计缺陷交给它。先脱敏写入 `~/.bensz-skills/bugs/`，当前任务不中断，只有用户明确要求才公开上报，禁止直接修改用户已安装的 Skill 源码。

<!-- End of canonical common constraints. -->
<!-- END COMMON CONSTRAINTS -->
