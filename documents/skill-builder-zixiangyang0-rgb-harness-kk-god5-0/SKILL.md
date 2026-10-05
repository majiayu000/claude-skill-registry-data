---
name: skill-builder
description: 当 harness 需要新的可复用能力、现有 skill 需要优化，或用户批准的 evolution proposal 需要修改 skill 时，在 .agents/skills 下创建或更新本地 Codex skill。
---

# Skill 构建器

这个 skill 用于指导如何创建有效的 skill。

## 本地 Harness 覆盖规则

在本仓库中，除非用户明确要求创建全局 Codex skill，否则都在 `.agents/skills/` 下创建和更新项目 skill。已批准的 evolution proposal 应优先落到这个本地 harness。

## 关于 Skill

Skill 是模块化、自包含的文件夹，通过提供专门知识、工作流和工具来扩展 Codex 的能力。可以把它们理解为特定领域或任务的“上手指南”：它们把 Codex 从通用 agent 转换成专门 agent，并补充模型无法完全内化的流程知识。

### Skill 提供什么

1. 专门工作流 - 面向特定领域的多步骤流程
2. 工具集成 - 处理特定文件格式或 API 的说明
3. 领域知识 - 公司特定知识、schema、业务逻辑
4. 打包资源 - 面向复杂或重复任务的脚本、参考资料和资产

## 核心原则

### 简洁是关键

上下文窗口是一种公共资源。Skill 会和 Codex 需要的其它内容共同占用上下文窗口：system prompt、对话历史、其它 skill 的 metadata，以及用户的真实请求。

**默认假设：Codex 已经很聪明。** 只添加 Codex 还不知道的上下文。逐条审视信息：“Codex 真的需要这段解释吗？”以及“这段话值得它占用的 token 成本吗？”

优先使用简洁示例，而不是冗长解释。

### 设置合适的自由度

根据任务的脆弱性和变化空间，匹配说明的具体程度：

**高自由度（文字说明）**：当多种方法都有效、决策依赖上下文，或需要启发式判断时使用。

**中自由度（伪代码或带参数脚本）**：当存在首选模式、允许一定变化，或配置会影响行为时使用。

**低自由度（具体脚本、少量参数）**：当操作脆弱且容易出错、一致性至关重要，或必须遵循特定顺序时使用。

把 Codex 想成正在选择路线：狭窄路径需要明确护栏（低自由度），开阔地带允许更多路线（高自由度）。

### 保护验证完整性

迭代时可以使用子 agent 验证 skill 是否能处理真实任务，或验证疑似问题是否真实存在。当你想在修改后独立检查 skill 的行为、输出或失败模式时，这尤其有用。只有在可以启动新子 agent 时才这样做。

使用子 agent 验证时，把它当作评估面。目标是了解 skill 是否能泛化，而不是验证另一个 agent 能否从泄漏的上下文中重构答案。

优先传递原始 artifact，例如示例 prompt、输出、diff、日志或 trace。只提供完成验证所需的最少任务本地上下文。除非验证明确需要，否则不要传递预期答案、疑似 bug、预期修复方案或你之前的结论。

### Skill 的组成

每个 skill 都包含一个必需的 `SKILL.md` 文件，以及可选的打包资源：

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter metadata (必需)
│   │   ├── name: (必需)
│   │   └── description: (必需)
│   └── Markdown instructions (必需)
├── agents/ (推荐)
│   └── openai.yaml - skill 列表和 chip 使用的 UI metadata
└── Bundled Resources (可选)
    ├── scripts/          - 可执行代码 (Python/Bash/etc.)
    ├── references/       - 按需加载进上下文的文档
    └── assets/           - 输出中使用的文件（templates、icons、fonts 等）
```

#### SKILL.md（必需）

每个 `SKILL.md` 都包含：

- **Frontmatter**（YAML）：包含 `name` 和 `description` 字段。Codex 只读取这些字段来判断何时使用该 skill，因此必须清楚、完整地说明这个 skill 是什么，以及什么时候应该使用。
- **Body**（Markdown）：使用该 skill 的说明和指导。只有当 skill 被触发后才会加载（如果会加载的话）。

#### Agents 元数据（推荐）

- 面向 UI 的 metadata，用于 skill 列表和 chip
- 生成值之前先阅读 `references/openai_yaml.md`，并遵守其中的说明和约束
- 创建时：通过阅读该 skill，生成面向人的 `display_name`、`short_description` 和 `default_prompt`
- 通过把值作为 `--interface key=value` 传给 `scripts/generate_openai_yaml.py` 或 `scripts/init_skill.py`，以确定性方式生成
- 更新时：验证 `agents/openai.yaml` 仍然匹配 `SKILL.md`；如果已过时则重新生成
- 只有用户明确提供时，才包含其它可选 interface 字段（icon、brand color）
- 字段定义和示例见 `references/openai_yaml.md`

#### 打包资源（可选）

##### Scripts 脚本（`scripts/`）

可执行代码（Python/Bash/etc.），用于需要确定性可靠性或会被反复重写的任务。

- **何时包含**：当同一段代码会被反复重写，或需要确定性可靠性时
- **示例**：用于 PDF 旋转任务的 `scripts/rotate_pdf.py`
- **收益**：节省 token、确定性高，并且可在不加载进上下文的情况下执行
- **注意**：Codex 仍可能需要阅读脚本，以便 patch 或做环境相关调整

##### References 参考资料（`references/`）

文档和参考材料，用于按需加载到上下文中，辅助 Codex 的流程和判断。

- **何时包含**：当 Codex 工作时应参考某些文档
- **示例**：金融 schema 的 `references/finance.md`、公司 NDA 模板的 `references/mnda.md`、公司政策的 `references/policies.md`、API 规范的 `references/api_docs.md`
- **用途**：数据库 schema、API 文档、领域知识、公司政策、详细工作流指南
- **收益**：让 `SKILL.md` 保持精简，只在 Codex 判断需要时加载
- **最佳实践**：如果文件很大（>10k words），在 `SKILL.md` 中给出 grep 搜索模式
- **避免重复**：信息应只存在于 `SKILL.md` 或 references 文件之一，不要两边重复。除非信息确实是 skill 的核心，否则详细信息优先放到 references 文件中，这能让 `SKILL.md` 精简，同时避免占满上下文窗口。`SKILL.md` 只保留必要的流程说明和工作流指导；详细参考材料、schema 和示例移到 references 文件中。

##### Assets 资产（`assets/`）

不打算加载进上下文、而是供 Codex 生成输出时使用的文件。

- **何时包含**：当 skill 需要在最终输出中使用某些文件时
- **示例**：品牌资产 `assets/logo.png`、PowerPoint 模板 `assets/slides.pptx`、HTML/React 样板 `assets/frontend-template/`、字体 `assets/font.ttf`
- **用途**：模板、图片、图标、样板代码、字体、会被复制或修改的示例文档
- **收益**：把输出资源和文档分开，让 Codex 可以在不加载这些文件进上下文的情况下使用它们

#### 不应放进 Skill 的内容

Skill 应只包含直接支持其功能的必要文件。不要创建多余的文档或辅助文件，例如：

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

Skill 应只包含 AI agent 完成当前工作所需的信息。它不应包含创建过程、安装和测试流程、面向用户的文档等辅助上下文。额外文档只会增加杂乱和混淆。

### 渐进披露设计原则

Skill 使用三级加载系统来高效管理上下文：

1. **Metadata（name + description）** - 始终在上下文中（约 100 words）
2. **SKILL.md body** - skill 触发时加载（<5k words）
3. **Bundled resources** - Codex 按需使用（脚本可执行，不必读入上下文窗口，因此不限）

#### 渐进披露模式

把 `SKILL.md` body 保持在必要内容范围内，并控制在 500 行以内，以减少上下文膨胀。接近这个限制时，把内容拆到单独文件中。拆分到其它文件时，必须在 `SKILL.md` 中引用它们，并清楚说明何时阅读，确保 skill 的读者知道这些文件存在以及何时使用。

**关键原则：** 当一个 skill 支持多种变体、framework 或选项时，`SKILL.md` 只保留核心工作流和选择指导。把特定变体的细节（pattern、示例、配置）移到单独的 reference 文件中。

**模式 1：带 reference 的高层指南**

```markdown
# PDF 处理

## 快速开始

使用 pdfplumber 提取文本：
[code example]

## 高级功能

- **表单填写**：完整指南见 [FORMS.md](FORMS.md)
- **API reference**：所有方法见 [REFERENCE.md](REFERENCE.md)
- **示例**：常见模式见 [EXAMPLES.md](EXAMPLES.md)
```

Codex 只在需要时加载 `FORMS.md`、`REFERENCE.md` 或 `EXAMPLES.md`。

**模式 2：按领域组织**

对于包含多个领域的 skill，按领域组织内容，避免加载不相关上下文：

```
bigquery-skill/
├── SKILL.md (概览和导航)
└── reference/
    ├── finance.md (收入、计费指标)
    ├── sales.md (机会、pipeline)
    ├── product.md (API 使用、功能)
    └── marketing.md (campaigns、归因)
```

当用户询问 sales metrics 时，Codex 只读取 `sales.md`。

类似地，对于支持多个 framework 或变体的 skill，按变体组织：

```
cloud-deploy/
├── SKILL.md (工作流 + provider 选择)
└── references/
    ├── aws.md (AWS 部署模式)
    ├── gcp.md (GCP 部署模式)
    └── azure.md (Azure 部署模式)
```

当用户选择 AWS 时，Codex 只读取 `aws.md`。

**模式 3：条件性细节**

展示基础内容，链接到进阶内容：

```markdown
# DOCX 处理

## 创建文档

新建文档使用 docx-js。见 [DOCX-JS.md](DOCX-JS.md)。

## 编辑文档

简单编辑可直接修改 XML。

**修订模式**：见 [REDLINING.md](REDLINING.md)
**OOXML 细节**：见 [OOXML.md](OOXML.md)
```

Codex 只在用户需要对应功能时读取 `REDLINING.md` 或 `OOXML.md`。

**重要准则：**

- **避免深层嵌套 reference** - reference 与 `SKILL.md` 保持一层关系。所有 reference 文件都应直接从 `SKILL.md` 链接。
- **组织较长 reference 文件** - 对超过 100 行的文件，在顶部加入目录，让 Codex 预览时能看到完整范围。

## Skill 创建流程

创建 skill 包含这些步骤：

1. 通过具体示例理解 skill
2. 规划可复用的 skill 内容（scripts、references、assets）
3. 初始化 skill（运行 `init_skill.py`）
4. 编辑 skill（实现资源并编写 `SKILL.md`）
5. 验证 skill（运行 `quick_validate.py`）
6. 根据真实使用情况迭代，并对复杂 skill 做前向测试

按顺序执行这些步骤；只有在有明确理由说明某步不适用时，才跳过它。

### Skill 命名

- 只使用小写字母、数字和连字符；把用户提供的标题规范化为 hyphen-case（例如 `"Plan Mode"` -> `plan-mode`）。
- 生成名称时，长度控制在 64 个字符以内（字母、数字、连字符）。
- 优先使用简短、动词开头的短语描述动作。
- 当能提升清晰度或触发准确性时，按工具命名空间命名（例如 `gh-address-comments`、`linear-address-issue`）。
- skill 文件夹名称必须与 skill name 完全一致。

### 步骤 1：通过具体示例理解 Skill

只有当 skill 的使用模式已经非常清楚时，才跳过这一步。即使在处理现有 skill 时，它通常仍有价值。

要创建有效的 skill，先清楚理解它会如何被使用。这个理解可以来自用户直接给出的示例，也可以来自生成示例并通过用户反馈验证。

例如，构建 image-editor skill 时，相关问题包括：

- “image-editor skill 应支持哪些功能？编辑、旋转，还有其它吗？”
- “能给几个这个 skill 会如何使用的例子吗？”
- “我能想象用户会说 ‘Remove the red-eye from this image’ 或 ‘Rotate this image’。你还会期待其它用法吗？”
- “用户说什么时应该触发这个 skill？”
- “你希望我在哪里创建这个 skill？如果没有偏好，我会放在 `$CODEX_HOME/skills`（`CODEX_HOME` 未设置时放在 `~/.codex/skills`），让 Codex 能自动发现它。”

为避免让用户负担过重，不要在一条消息里问太多问题。从最重要的问题开始，必要时再追问以提高效果。

当你已经清楚这个 skill 应支持的功能时，结束这一步。

### 步骤 2：规划可复用的 Skill 内容

为了把具体示例转化为有效的 skill，逐个分析示例：

1. 思考如果从零执行该示例，需要怎么做
2. 识别重复执行这些工作流时，哪些 scripts、references 和 assets 会有帮助

示例：构建 `pdf-editor` skill 来处理 “Help me rotate this PDF” 这类请求时，分析会发现：

1. 旋转 PDF 每次都需要重写同一段代码
2. 在 skill 中保存 `scripts/rotate_pdf.py` 会有帮助

示例：设计 `frontend-webapp-builder` skill 来处理 “Build me a todo app” 或 “Build me a dashboard to track my steps” 这类请求时，分析会发现：

1. 编写前端 webapp 每次都需要相同的 HTML/React 样板
2. 保存包含 HTML/React 项目样板文件的 `assets/hello-world/` template 会有帮助

示例：构建 `big-query` skill 来处理“今天有多少用户登录？”这类请求时，分析会发现：

1. 查询 BigQuery 每次都需要重新发现表 schema 和关系
2. 保存记录表 schema 的 `references/schema.md` 文件会有帮助

要确定 skill 内容，分析每个具体示例，形成要包含的可复用资源清单：scripts、references 和 assets。

### 步骤 3：初始化 Skill

到这一步，就可以实际创建 skill。

只有当正在开发的 skill 已经存在时，才跳过这一步。在这种情况下，继续下一步。

运行 `init_skill.py` 之前，询问用户想把 skill 创建在哪里。如果用户没有指定位置，默认使用 `$CODEX_HOME/skills`；当 `CODEX_HOME` 未设置时，回退到 `~/.codex/skills`，以便 skill 能被自动发现。

从零创建新 skill 时，始终运行 `init_skill.py` 脚本。这个脚本会方便地生成新的模板 skill 目录，自动包含 skill 所需的全部基础内容，让创建过程更高效可靠。

用法：

```bash
scripts/init_skill.py <skill-name> --path <output-directory> [--resources scripts,references,assets] [--examples]
```

示例：

```bash
scripts/init_skill.py my-skill --path "${CODEX_HOME:-$HOME/.codex}/skills"
scripts/init_skill.py my-skill --path "${CODEX_HOME:-$HOME/.codex}/skills" --resources scripts,references
scripts/init_skill.py my-skill --path ~/work/skills --resources scripts --examples
```

该脚本会：

- 在指定路径创建 skill 目录
- 生成带有正确 frontmatter 和待填占位内容的 `SKILL.md` 模板
- 使用通过 `--interface key=value` 传入、由 agent 生成的 `display_name`、`short_description` 和 `default_prompt` 创建 `agents/openai.yaml`
- 可选地根据 `--resources` 创建资源目录
- 当设置 `--examples` 时，可选地添加示例文件

初始化后，自定义 `SKILL.md` 并按需添加资源。如果使用了 `--examples`，替换或删除占位文件。

通过阅读 skill 来生成 `display_name`、`short_description` 和 `default_prompt`，然后把它们作为 `--interface key=value` 传给 `init_skill.py`，或用以下命令重新生成：

```bash
scripts/generate_openai_yaml.py <path/to/skill-folder> --interface key=value
```

只有当用户明确提供其它可选 interface 字段时才包含它们。完整字段说明和示例见 `references/openai_yaml.md`。

### 步骤 4：编辑 Skill

编辑新生成或已有的 skill 时，记住这个 skill 是给另一个 Codex 实例使用的。只包含对 Codex 有帮助且非显而易见的信息。思考哪些流程知识、领域细节或可复用资产能帮助另一个 Codex 实例更有效地执行任务。

在大幅修改后，或当 skill 特别复杂时，应使用子 agent 在真实任务或 artifact 上做前向测试。这样做时，传递待验证 artifact，而不是你对问题的诊断；prompt 要足够通用，让成功依赖可迁移的推理，而不是隐藏答案。

#### 从可复用 Skill 内容开始

开始实现时，先处理上面识别出的可复用资源：`scripts/`、`references/` 和 `assets/` 文件。注意，这一步可能需要用户输入。例如，实现 `brand-guidelines` skill 时，用户可能需要提供要存入 `assets/` 的品牌资产或模板，或要存入 `references/` 的文档。

新增脚本必须通过实际运行来测试，确保没有 bug 且输出符合预期。如果有许多类似脚本，只需测试有代表性的样本，以在完成时间和信心之间取得平衡。

如果使用了 `--examples`，删除 skill 不需要的任何占位文件。只创建实际需要的资源目录。

#### 更新 SKILL.md

**写作准则：** 始终使用祈使/不定式形式。

##### Frontmatter 元数据

用 `name` 和 `description` 编写 YAML frontmatter：

- `name`：skill name
- `description`：这是 skill 的主要触发机制，帮助 Codex 理解何时使用该 skill。
  - 同时包含 skill 做什么，以及何种 trigger/context 下使用它。
  - 把所有 “when to use” 信息都写在这里，不要写在正文中。正文只有触发后才会加载，因此正文里的 “When to Use This Skill” 章节对 Codex 触发没有帮助。
  - `docx` skill 的示例 description："全面支持文档创建、编辑和分析，包括修订、批注、格式保留和文本提取。当 Codex 需要处理专业文档（.docx 文件）时使用，例如：(1) 创建新文档，(2) 修改或编辑内容，(3) 处理修订，(4) 添加批注，或其它文档任务"

YAML frontmatter 中不要包含任何其它字段。

##### Body 正文

编写使用 skill 及其打包资源的说明。

### 步骤 5：验证 Skill

skill 开发完成后，验证 skill 文件夹以尽早发现基础问题：

```bash
scripts/quick_validate.py <path/to/skill-folder>
```

验证脚本会检查 YAML frontmatter 格式、必需字段和命名规则。如果验证失败，修复报告的问题并再次运行命令。

### 步骤 6：迭代

测试 skill 后，你可能发现它复杂到需要前向测试；用户也可能请求改进。

用户测试通常发生在刚使用过该 skill 之后，此时仍有 skill 表现如何的新鲜上下文。

**前向测试和迭代工作流：**

1. 在真实任务中使用 skill
2. 观察卡点或低效之处
3. 识别应如何更新 `SKILL.md` 或打包资源
4. 实施修改并再次测试
5. 在合理且合适时做前向测试

## 前向测试

要做前向测试，可以启动子 agent，以最少上下文对 skill 施压测试。
子 agent 不应知道自己是在测试 skill。应把它当作用户请求它执行任务的 agent。给子 agent 的 prompt 应类似：
  `Use $skill-x at /path/to/skill-x to solve problem y`
而不是：
  `Review the skill at /path/to/skill-x; pretend a user asks you to...`

前向测试的决策规则：
  - 倾向于做前向测试
  - 如果你认为前向测试存在以下风险，则先请求批准：
    * 耗时较长
    * 需要用户额外批准
    * 修改线上生产系统

  在这些情况下，向用户展示你建议的 prompt，并请求 (1) yes/no 决策，以及
  (2) 任何建议修改。

前向测试时的注意事项：
   - 使用 fresh threads 做独立检查
   - 以接近用户真实请求的方式传递 skill 和请求
   - 传递原始 artifact，而不是你的结论
   - 避免展示预期答案或预期修复
   - 每次迭代后从源 artifact 重建上下文
   - 审查子 agent 的输出、推理和生成的 artifact
   - 避免在迭代之间留下子 agent 可在磁盘上发现的 artifact；
     清理子 agent 的 artifact，避免额外污染。

如果前向测试只有在子 agent 看到泄漏上下文时才成功，请先收紧 skill 或前向测试设置，再信任结果。
