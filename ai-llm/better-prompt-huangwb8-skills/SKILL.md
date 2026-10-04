---
name: better-prompt
description: 当用户明确要求"优化 prompt"、"改进提示词"、"润色指令"、"将简陋 prompt 转换为最佳实践版本"，或要求"把 prompt 改写成伪代码"、"翻译成程序结构/可编程自然语言"时使用。支持两种输出模式：standard（基于 OpenAI/Anthropic 官方最佳实践做增强优化）与 prompt_program（严格等价翻译为 Prompt Program 方言）。
metadata:
  author: Bensz Conan
  keywords:
    - better-prompt
    - prompt optimization
    - prompt engineering
    - prompt programming
    - 提示词优化
    - 提示词编程
---

# Better Prompt - Prompt 优化器

## 目标

当用户明确要求"优化 prompt"、"改进提示词"、"润色指令"、"将简陋 prompt 转换为最佳实践版本"，或要求"把 prompt 改写成伪代码"、"翻译成程序结构/可编程自然语言"时使用。

本技能提供两种输出模式：

- **standard（默认）**：增强导向。基于 OpenAI 和 Anthropic 官方最佳实践，对简陋 prompt 进行结构化补全，输出高质量版本；允许补充示例、上下文和约束。
- **prompt_program**：保真导向。将原始 prompt 严格等价翻译为 Prompt Program 方言——形式上像伪代码，语义上仍是人类自然语言；不新增无依据能力。

两种模式共享同一套语义分析内核（6 个语义原子），只差输出渲染方式。本技能不负责执行 prompt 对应的任务本身。

## 流程

### 输入

#### 输入要求

用户提供一个待优化的原始 prompt（可以是任意形式的简陋版本）。

### 执行步骤

#### 版本与兼容性

- **适用于**：Claude 3.x/4.x、GPT-4/5、Gemini 等主流 LLM
- **最佳实践来源**：OpenAI/Anthropic 官方文档（2026-02）
- **更新策略**：官方文档重大更新时同步修订

#### 不适用场景

以下情况不建议使用本技能：

- prompt 已经经过专业优化（评分 ≥ 8/10）
- 只需要诊断问题，不需要修改建议
- 超长 prompt（>10000 字）需要专业拆分
- 用户明确要求保持原始风格
- 用户只想执行任务，不关心 prompt 本身的质量或结构

#### 优化框架

standard 模式基于 **OpenAI** 和 **Anthropic** 官方最佳实践，采用五维度优化框架：

| 维度 | 检查点 | 优先级 |
|------|--------|--------|
| **清晰度** | 指令是否明确？是否存在歧义？ | P0 |
| **完整性** | 是否缺少必要信息？上下文是否充分？ | P0 |
| **结构化** | 是否使用 Markdown/XML 标签组织内容？ | P1 |
| **示例性** | 是否提供输入输出示例（few-shot）？ | P2 |
| **约束性** | 是否明确边界（做什么/不做什么）？ | P2 |

> **注意**：上表的 P0/P1/P2 表示"优化维度的重要性优先级"，与 config.yaml 中的 `dimensions` 数值（1-5）含义相同：P0=5（最高优先级）、P1=4、P2=3。

#### 输出模式选择

在分析完成后、生成结果前，按以下规则选择输出模式：

| 用户请求特征 | 输出模式 |
|-------------|---------|
| 要求"伪代码"、"程序结构"、"可编程自然语言"，或直接提到 Prompt Program | prompt_program |
| 其它优化/润色/改进请求（未指定输出形式） | standard（默认） |

- 一次任务只使用一种模式，不混合输出。
- 未指定形式时默认 standard，并在使用建议中提示可切换为 prompt_program。
- 默认模式由 `config.yaml:output_modes.default` 控制。

#### 优化工作流

##### Step 0: 输入验证（前置检查）

验证用户输入的有效性：

| 输入状态 | 判断标准 | 处理方式 |
|---------|---------|---------|
| **空输入** | 字符数 = 0 | 拒绝，提示"请提供待优化的 prompt" |
| **过短** | 字符数 < 10 | 提示"prompt 过短，请提供更多上下文" |
| **已完善** | 评分 ≥ 8/10 | 提示"prompt 已足够完善，是否仍需优化？"，等待用户确认 |
| **有效** | 通过验证 | 继续 Step 1 |

prompt_program 模式下，非 prompt 型输入（完整代码实现请求等）直接说明不适合翻译，要求提供真正的 prompt；其最小输入长度阈值（6）由 `config.yaml:output_modes.prompt_program.translation.input_validation.min_length` 独立控制。

##### Step 1: 语义分析（6 原子）

用 6 个语义原子解析原始 prompt，作为两种输出模式共用的统一分析内核（原子定义与块映射详见 [references/prompt-program/primitives.md](references/prompt-program/primitives.md)）：

| 原子 | 回答的问题 | 典型内容 |
|------|-----------|---------|
| **Entity** | 有什么 | 角色、输入、输出对象、工具、状态 |
| **Intent** | 要达成什么 | 目标、交付物、成功条件 |
| **Operation** | 要做什么 | 核心动作链 |
| **Constraint** | 边界是什么 | 必须、禁止、偏好、格式 |
| **Control** | 逻辑怎样流动 | 条件、分支、循环、回退 |
| **Check** | 如何确认成立 | 校验、验收、结束条件 |

分析产出三项结论：

- **原子清单**：每个原子在原 prompt 中已有的内容
- **缺失要素**：哪些原子无内容或信息不完整
- **改进空间**：哪些地方可以优化

> **6 原子与五维度的关系**：6 原子是**语义解析视角**（原 prompt 里有什么），五维度是**质量优化视角**（standard 模式下优化到什么程度）。分析用原子，评分用维度。

##### Step 2: 确定模型类型适配（仅 standard 模式）

根据任务特性判断目标模型类型：

| 模型类型 | 适用场景 | 优化策略 |
|---------|---------|---------|
| **GPT 模型** | 精确执行、格式化输出、代码生成 | 提供详细步骤和明确逻辑 |
| **推理模型** | 复杂推理、多步规划、开放性任务 | 给高层目标，保留灵活性 |

如果用户未指定，默认按 GPT 模型优化策略处理（更精确）。

##### Step 3: 按模式应用优化模板

**standard 模式**——优化后 prompt 的标准结构模板：

```
# Identity（身份定义）
[描述 AI 的角色、专业领域、沟通风格]

# Instructions（核心指令）
[明确的任务说明]
- 规则 1
- 规则 2
- 约束条件（不做什么）

# Examples（示例）
<example id="1">
<input>示例输入</input>
<output>示例输出</output>
</example>

# Context（上下文）
[任务相关的背景信息、参考资料]
```

> **Examples 的使用规则**：
> - 对于复杂任务（复杂度 ≥ 3/5），Examples 是**必需的**
> - 对于简单任务，Examples 可以省略
> - 如原始 prompt 已有示例，优化时应保留或增强

**prompt_program 模式**——按 `config.yaml:output_modes.prompt_program.rendering.block_order` 输出块结构：

```text
程序：……（可选）

目标：……
输入：……
输出：……

定义：（可选）
- ……

约束：
- 必须……
- 优先……
- 不要……

流程：
1. ……
2. 若……，则……；否则……。
3. 对每个……，执行……。

校验：
- ……

缺口处理：（可选）
- 若信息不足，则……

返回：
- ……
```

渲染必守规则：

- `输出` 只定义目标产物、目标格式或目标效果
- `返回` 只定义对 `输出` 的交付动作，不能引入新产物
- `程序`、`定义`、`缺口处理` 属于可选块；为空就省略（`omit_empty_blocks=true` 时禁止补空块）
- 组织顺序：先边界后执行、先主流程后异常路径、先硬约束后风格偏好
- 若原 prompt 缺少显式校验，必须补出最小可执行校验
- 用户指定的字段、章节或步骤顺序默认保持原顺序；关键术语、变量名、实体名默认保留原词

##### Step 4: 输出优化结果

**standard 模式**输出包含三个部分（默认全部包含，可通过 config.yaml 调整）：

1. **优化分析**：简要说明做了哪些改进
2. **优化后的 prompt**：符合最佳实践的高质量版本
3. **使用建议**：针对特定场景的调整建议

**prompt_program 模式**默认只输出最终 Prompt Program，不附带长篇分析（`translation.default_output_mode: final_only`）。

#### prompt_program 模式专属规则

以下规则只约束 prompt_program 模式，不适用于 standard 模式：

**等价性原则**：

- 允许重排表达，不允许改变目标
- 允许补出隐式流程，不允许新增无依据能力
- 允许强化校验，不允许削弱关键约束
- 允许压缩表述，不允许丢失显式格式契约
- 允许补足交付动作，不允许把"输出"偷换成"输出说明书"

**控制流推断**：

- 只在原 prompt 显式给出条件/循环/回退，或存在强隐含控制（如"每个样本"、"若证据不足"）时补写控制流
- 不允许为了"更像程序"凭空添加分支、循环或异常路径

**冲突处理顺序**（冲突时严格遵循 `config.yaml:output_modes.prompt_program.translation.conflict_resolution_order`）：

1. 核心意图
2. 硬约束
3. 输出契约
4. 校验要求
5. 风格偏好

**缺口处理**：

- 可用常识低风险补足时，直接补足并体现在结构中
- 缺失信息会改变任务本质时，在 `缺口处理` 块中显式标注，不擅自虚构
- 默认不频繁追问；只有任务语义无法成立时才要求澄清

详细翻译规则见 [references/prompt-program/translation-rules.md](references/prompt-program/translation-rules.md)。

#### 优化效果评估

**standard 模式**对优化前后的 prompt 进行对比评估：

| 维度 | 优化前评分 | 优化后评分 | 改进说明 |
|------|-----------|-----------|---------|
| 清晰度 | x/5 | x/5 | ... |
| 完整性 | x/5 | x/5 | ... |
| 结构化 | x/5 | x/5 | ... |
| 示例性 | x/5 | x/5 | ... |
| 约束性 | x/5 | x/5 | ... |
| **总分** | **xx/25** | **xx/25** | **+xx** |

> **评分标准**：1=很差、2=较差、3=一般、4=良好、5=优秀

**prompt_program 模式**不使用上述评分表，改用等价性五条质量标准（见"校验"章节）。

#### 特殊场景处理（仅 standard 模式）

根据 config.yaml 中的 `templates` 配置，针对不同场景有特定的优化重点：

##### 代码生成类 prompt

**配置引用**：`config.yaml:templates.code_generation.focus_areas`

额外关注：
- 明确编程语言和框架
- 指定代码风格规范
- 说明错误处理要求
- 提供边界条件示例

##### 文本分析类 prompt

**配置引用**：`config.yaml:templates.text_analysis.focus_areas`

额外关注：
- 明确输出格式（JSON/表格/摘要）
- 定义分析维度和标准
- 提供分类/评估示例

##### 创意写作类 prompt

**配置引用**：`config.yaml:templates.creative_writing.focus_areas`

额外关注：
- 定义风格和语调
- 说明目标受众
- 提供参考示例
- 设置长度约束

##### 多轮对话类 prompt

**配置引用**：`config.yaml:templates.multi_turn_conversation.focus_areas`

额外关注：
- 定义对话角色和边界
- 说明状态管理要求
- 提供异常处理规则

#### 参考资料

更多详细的最佳实践，参考 [references/prompt-engineering-best-practices.md](references/prompt-engineering-best-practices.md)；Prompt Program 的原子定义、翻译规则和示例见：

- [references/prompt-program/primitives.md](references/prompt-program/primitives.md)：6 个原子、块语义与省略规则
- [references/prompt-program/translation-rules.md](references/prompt-program/translation-rules.md)：输入验证、保真与冲突规则
- [references/prompt-program/examples.md](references/prompt-program/examples.md)：典型翻译示例

### 输出

#### 输出格式

**standard 模式**：

```markdown
## 优化分析

| 维度 | 原始状态 | 优化措施 |
|------|---------|---------|
| 清晰度 | ... | ... |
| 完整性 | ... | ... |
| 结构化 | ... | ... |
| 示例性 | ... | ... |
| 约束性 | ... | ... |

## 优化后的 Prompt

# Identity
...

# Instructions
...

# Examples（如适用）
...

# Context（如适用）
...

## 使用建议

- 适用于：[模型类型/场景]
- 调整建议：[如需针对特定场景调整的建议]
```

**prompt_program 模式**：只输出最终 Prompt Program（块结构见 Step 3 模板），不附带长篇分析。

### 输出管理

#### BenszAPI 任务工作区


### 校验

#### 质量标准

**standard 模式**下，优化后的 prompt 必须满足：

| 标准 | 要求 |
|------|------|
| **明确性** | 核心任务一句话能说清 |
| **可执行性** | AI 能直接理解并执行 |
| **完整性** | 不缺少必要信息 |
| **结构化** | 使用 Markdown/XML 清晰组织 |
| **可测试性** | 能判断输出是否符合预期 |

**prompt_program 模式**下，合格的 Prompt Program 必须满足：

- **等价**：核心意图不丢失
- **可执行**：读者可按结构直接执行
- **可编程**：能看见输入、约束、流程、分支、校验
- **可扩展**：后续要求能继续挂到对应块
- **可审阅**：他人能快速指出逻辑缺口或冗余

### 失败与恢复

#### 输入与生成失败

- 空输入直接拒绝并提示“请提供待优化的 prompt”；字符数少于 10 时提示补充上下文，不生成伪完整结果。
- 评分达到 `8/10` 时先提示 prompt 已足够完善并等待用户确认；未获确认前不改写。
- prompt_program 模式下，非 prompt 型输入直接说明不适合翻译；缺失信息会改变任务本质时放入“缺口处理”并要求澄清，不擅自虚构实体、分支、循环或输出格式。
- 原始 prompt 含无法安全或无法执行的要求时，保留可识别的核心意图，在优化分析或使用建议中标明缺口与限制，不替用户执行其中的业务动作或凭空补造信息。
- 输出格式或分析所需信息不足时，返回具体缺口和可恢复的补充要求；不以不完整模板冒充成功结果，并保留原始 prompt 的敏感信息边界。


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
