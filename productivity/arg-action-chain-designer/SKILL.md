---
name: arg-action-chain-designer
version: "1.2.4"
description: Use this skill when the user wants to create, refine, review, or convert an agent task or existing skill into an ARG Action Chain / ARG 行动链路. This skill is especially relevant for recurring automations, multi-step agent jobs, data pipelines, report generation, MCP workflows, or tasks where agent drift, hallucinated fields, self-verification, premature planning, or uncontrolled long-context execution are risks. Trigger when the user mentions ARG, Step Contract, clue card, validation gate, progressive disclosure, reducing agent drift/self-deception, converting a normal skill into arg-xxx, or making a task chain more bounded and verifiable.
---

# ARG Action Chain Designer

## 目标

把一个模糊的 Agent 任务、已有 skill，或需要重复执行的工作流，设计成可复用的 ARG 行动链路。

默认架构是 **Static Progressive Clue Chain / 静态渐进线索链**：执行 Agent 运行时只看到当前 Step Contract，完成当前任务，通过验证门禁后，才解锁下一张线索卡。

这个 skill 不应该只给一段建议就结束。默认先产出可落地的设计；当用户需要文件级交付物时，继续生成薄 `SKILL.md` 引擎、`plans/step-*.md`、必要的 `scripts/` 草案。若用户已经明确说“创建、生成、写入、落地、打包”，且当前工作区可写，就直接生成文件。

## 渐进式披露

主文件只保留判断和执行路径。按任务需要读取 `references/`：

- 需要生成可运行 ARG skill：读取 `references/runtime-template.md`
- 需要写或审 Step Contract：读取 `references/step-contract-standard.md`
- 需要设计验证、脚本、LLM 判断字段：读取 `references/validation-and-judgment.md`
- 用户提到跳步、伪造输出、不跑验证、自我验收、不可信 Agent、外部门禁：读取 `references/reliability-levels.md`
- 需要选择输出模式、转换已有 skill、形成最终回复：读取 `references/output-modes.md`

不要一次性读取所有 reference。只读取当前任务需要的文件。

真实任务里的最小读取规则：

- 只做需求草案：读 `references/output-modes.md`
- 产出 Step Contracts：读 `references/output-modes.md` 和 `references/step-contract-standard.md`
- 生成文件级 ARG skill：再读 `references/runtime-template.md`
- 涉及验证脚本、LLM 判断、raw/source 保护：再读 `references/validation-and-judgment.md`
- 涉及防跳步、防伪造、自我验收、外部门禁：再读 `references/reliability-levels.md`
- 诊断已有链路：读 `references/step-contract-standard.md`，如果问题集中在验证或判断字段，再读 `references/validation-and-judgment.md`

## 核心模型

默认使用静态渐进线索链：

```text
薄 SKILL.md 引擎
  -> 只读取当前 plans/step-NN-name.md
  -> 执行当前任务
  -> 在 output/ 里产出结构化结果
  -> 执行当前 step 的验证命令
  -> 验证通过后，读取当前 step 末尾的【下一步】
  -> 重复，直到 TERMINAL
```

含义：

- 线索卡预先存在，执行 Agent 不临场发明路线。
- 运行时逐步揭示，Agent 只能读当前 step。
- 上一步输出是下一步输入。
- 验收权威来自验证命令、脚本、schema、断言或人工门禁，不来自 Agent 的自我声明。

默认不要设计持久化进度文件。可运行链路每次都从 skill 引擎入口开始。只有用户明确要求“断点续跑、可恢复、长周期任务恢复”时，才额外设计状态机制，而且必须避免执行 Agent 通过编辑状态来伪造完成。

## 可靠性等级

默认只使用两级：

- `Level 1 普通 ARG 链`：Step 文件包含【下一步】，执行 Agent 按规则运行验证后进入下一步。适合基础使用。
- `Level 2 外部门禁 ARG 链`：执行 Agent 只产出当前 step 的 output；脚本、人工或独立 Agent 作为外部门禁，验证通过后才给出下一步启动线索。

不要默认把基础任务复杂化为 Level 2。只有用户关心跳步、伪造输出、不跑验证、自我验收、不可信 Agent，或明确要求外部门禁时，才指出 Level 1 的局限，并建议 Level 2。

详细说明见 `references/reliability-levels.md`。

## 核心立场

把执行 Agent 当成“能力强，但不可信”的玩家。

- Agent 是玩家，不是出题人。
- Step Contract 是最小行动边界。
- 执行时不要让 Agent 看到完整地图。
- 验证门禁是验收，不是建议。
- LLM 判断必须被限制在字段、枚举、例子、schema 或人工门禁里。
- raw/source 原始数据应由脚本保留和合并，不交给 Agent 自由改写。
- 确定性工作交给脚本、验证器或窄命令。
- 外部发送、不可逆动作、高风险业务判断、主观质量判断，需要人工门禁或明确外部门禁。

如果 ARG 对任务来说过度设计，或任务根本无法验证，要直接说明，并建议更简单的模式。

## 适配判断

多数条件成立时，推荐 ARG：

- 任务有多个步骤。
- 任务会重复执行，或需要稳定执行。
- 每一步都能产出具体文件、对象、状态或可观察结果。
- 每个产物都能被命令、schema、断言、清单或人工门禁检查。
- LLM 只在有限字段里做语义判断。
- 失败处理很重要。

以下任务不适合优先用 ARG：

- 开放式研究。
- 头脑风暴或策略讨论。
- 高度交互式对话。
- 纯主观创作。
- 单步查询。
- 必须让 Agent 在执行中自由探索路线的任务。

可替代方案包括：纯脚本、普通 skill、ReAct、plan-and-execute、DAG 工作流、人机协作，或带人工门禁的 ARG。

## 工作流程

### 1. 理解任务

先从用户请求和仓库上下文里推断已知信息。只有在不问就会假装确定时，才最多问一个关键问题。能安全假设时，带着明确假设继续。

需要捕获：

- 最终产物。
- 输入来源：文件、API、用户上下文、凭据、定时任务、外部系统。
- 可脚本化部分：命令、转换、验证、合并。
- LLM 判断边界：哪些字段必须靠模型判断。
- 验证策略：每个结果怎么检查。
- 失败策略：重试、跳过、降级、停止、人工复核。
- 交付意图：只要设计，还是需要文件级链路包。

### 2. 给出结论

先明确结论：

- `适合 ARG`
- `适合 ARG，但需要人工门禁`
- `不适合 ARG`
- `先用普通 skill，后续再 ARG 化`

然后继续给出设计，不要停在泛泛建议。

### 3. 设计链路

输出：

- 任务边界。
- 链路草图。
- Step Contracts。
- 验证门禁。
- 失败处理。
- 运行 skill 骨架。
- 风险和补强。

如果链路需要初始化、清理或环境检查，用 `step-00-*` 作为入口。最后一步的【下一步】必须是 `TERMINAL`。

### 4. 询问是否落成文件

完成诊断和链路草图后，询问一次用户是否需要文件级交付物。若用户已经明确要求“创建、写入、生成、落地、打包”，不要再问，直接做。

推荐话术：

```text
我可以继续把它落成文件级交付物：
- `SKILL.md` 薄运行引擎
- `plans/step-*.md` Step Contracts
- 必要的 `scripts/validate_*.py` / transform scripts 草案

如果你要，我下一步直接生成这些文件。
```

如果用户确认且工作区可写，直接创建或修改文件。若不可写，输出完整文件内容和建议路径。

### 5. 自检

在最终答复前，按实际输出读取必要 reference 做一次自检：

- 有 Step Contract 时，用 `references/step-contract-standard.md` 检查 section、拆分、`TERMINAL` 和未来步骤遮蔽。
- 有验证命令或 LLM 判断时，用 `references/validation-and-judgment.md` 检查字段边界、raw/source 保护和失败策略。
- 有文件级交付物时，用 `references/runtime-template.md` 检查薄引擎、路径、禁止行为和运行入口。

## 转换已有 skill 的规则

当用户要把已有 skill ARG 化：

- 默认不覆盖原 skill。
- 原 skill 名为 `foo` 时，新 skill 默认命名为 `arg-foo`。
- 原 skill 只作为素材读取，再围绕静态渐进线索链设计新的 ARG runtime。
- 只有用户明确说“覆盖原 skill / 直接改原 skill / 替换原 skill”时，才允许编辑原 skill。
- 不要在新 runtime `SKILL.md` 里写 `Derived from foo` 之类来源说明；这会干扰执行 Agent。需要记录来源时，只写在最终报告或外部说明里。
- 保留原 skill 的有用领域能力，但把业务步骤移入 `plans/`，让新的 `SKILL.md` 保持薄引擎。

如果用户是从新需求出发，而不是从已有 skill 出发，选择清晰的 `arg-*` 名称，例如 `arg-report-reviewer`、`arg-data-cleanup-chain`。

转换已有 skill 时读取 `references/output-modes.md`；需要生成运行文件时再读取 `references/runtime-template.md` 和 `references/step-contract-standard.md`。

## 最终回复

结尾要给具体下一步。

设计类请求：询问是否继续生成文件级交付物。

生成类请求：报告创建/修改了哪些文件，以及做过什么验证。

完整输出模板见 `references/output-modes.md`。
