---
name: write-readme
description: 为 GitHub 项目创建或改写高质量、可执行、证据驱动的双语 README；当用户要求写 README、项目说明或整理项目首页时使用。优先依据项目事实核验功能、命令和链接。
metadata:
  author: Bensz Conan
  short-description: 为任意项目生成中英文对齐的 GitHub README
  keywords:
    - write-readme
    - README
    - README.md
    - README_EN.md
    - GitHub documentation
    - project documentation
    - bilingual README
    - write-skill-readme
---

# write-readme

## 目标

为任意 GitHub 项目创建或改写高质量、可执行、证据驱动的双语 README；当用户说“写 README / README.md / 项目说明 / 文档首页 / GitHub 项目介绍”，或需要把 Agent Skill、库、CLI、Web 应用、服务、数据/机器学习项目整理成中文 README.md 与英文 README_EN.md 时使用。优先读取项目事实并验证命令、链接和功能，不凭空编造。

为项目写 README 的通用 Skill。它只负责项目说明文档，不改业务代码、配置或测试；默认写入项目根目录的 `README.md`（中文）和 `README_EN.md`（英文）。

## 流程

### 输入

#### 触发边界

适用：创建、重写、补齐或双语化项目 README；为 Agent Skill 写用户指南；根据仓库现状补 Quick Start、示例、架构、贡献或安全说明。

不适用：只改代码注释、写 API 参考手册、生成发布说明、翻译与项目无关的文章，或用户只要求审查而不允许写 README。若用户只指定一个语言，仍先确认是否应保持双语契约；本仓库默认保持两份对齐文件。

### 执行步骤

#### 核心原则

1. **先回答“这是什么、为何有用、如何开始”**：首屏给出项目名、具体价值主张和最短成功路径。
2. **事实优先**：功能、版本、命令、徽章、性能数字、兼容性和链接必须来自仓库或明确来源；无法确认就标为待确认/不写。
3. **任务优先而非文件优先**：按用户要完成的任务组织 Quick Start、示例和导航，架构细节后置。
4. **最小可运行示例**：安装、配置、运行、预期结果形成闭环；复杂用法链接到更深文档。
5. **渐进披露**：首屏短而有用；高级部署、内部设计、故障排查和贡献流程分层展开。
6. **双语等价**：英文不是逐词直译，而是自然表达同一事实；两份文件的标题树、代码块、链接目标、版本和示例保持同步。
7. **完整 GitHub Hero**：除非项目确实是极短的索引或用户明确要求极简排版，首屏默认采用“居中标题/标识 → 事实徽章 → 导航 → 价值主张 → 解释段 → 证据或 Quick Start”的完整 Hero；视觉不可用时保留信息顺序并退化为纯 Markdown。
8. **克制装饰**：只添加能帮助判断的徽章、截图、GIF 或图表；视觉材料必须有替代文本和真实路径。
9. **诚实边界**：明确支持范围、限制、风险、数据来源、许可证和未验证事项，不用营销语气掩盖缺口。

#### 工作流

##### 1. 建立事实清单

读取并交叉核对：

- 项目元数据：`pyproject.toml`、`package.json`、`Cargo.toml`、`go.mod`、`LICENSE`、版本文件。
- 入口与安装：CLI 入口、服务启动脚本、Docker/Compose、Makefile、CI workflow、示例配置。
- 能力证据：源码目录、测试、演示资源、发布包和现有文档。
- 约束：运行时版本、平台、外部服务、凭据需求、数据/模型许可和安全注意事项。

把“已证实”“用户明确提供”“推断/待确认”分开。不要为了填满章节而创造功能。

##### 2. 识别项目类型并选模板

优先选择一个主模板，必要时组合一个部署附录；不要把所有模板拼成超长手册。详细章节骨架见 `references/templates/`；首屏 Hero 的组成、项目类型变体、可访问性门槛和反模式见 `references/github-hero-patterns.md`。

| 类型 | 识别信号 | 首要读者 | 首屏重点 |
|---|---|---|---|
| 通用库/SDK | 可导入包、API、版本发布 | 开发者 | 安装、最小 API、支持版本 |
| CLI/服务 | 命令入口、HTTP/Worker、Docker | 使用者/运维 | 一条命令运行、配置、健康检查 |
| Web/桌面应用 | 前端入口、截图、在线 Demo | 终端用户/部署者 | 视觉预览、体验路径、部署选项 |
| 数据/ML | 数据集、训练/推理、模型权重 | 研究者/工程师 | 数据与许可、复现实验、资源需求 |
| Agent Skill/插件 | `SKILL.md`、manifest、宿主安装 | Skill 使用者/维护者 | 触发方式、输入输出、宿主安装 |

通用章节规则与反例见 `references/readme-principles.md`；Hero 模式和社区调研摘要见 `references/github-hero-patterns.md` 与 `references/research-notes.md`。

##### 3. 设计信息架构

按项目事实取舍以下顺序（不要生成空章节）：

1. 完整 GitHub Hero：居中标题/真实标识、已验证徽章、语言/文档/演示导航、价值主张、2–4 句解释和真实证据或最短行动入口。
2. 一句话概览、核心能力或视觉预览（如果已在 Hero 中表达则不要重复堆砌）。
3. Quick Start：前置条件 → 安装 → 配置 → 运行 → 预期结果；Hero 中的命令必须与此处一致。
4. 按任务编排的 1–3 个最小示例；复杂示例链接到 `docs/`。
5. 选择性章节：功能/用例、架构、配置、部署、性能/复现、限制与安全、故障排查。
6. 帮助渠道、贡献指南、路线图（只有仓库有依据时）、许可证与致谢/引用。

标题使用 GitHub 可生成锚点的 Markdown 标题；目录仅在长文档或用户明确要求时添加（GitHub 已提供 Outline）。外部链接说明用途；相对链接和图片路径必须可解析。

##### 4. 先写中文，再生成英文

先固定中文事实和结构，再逐节生成英文。保留命令、代码、环境变量、路径、版本号、URL、表格列数和示例输出；品牌、API、许可证不翻译。中文客套话和夸大形容词不硬译。

##### 5. 校验与交付

运行：

```bash
python3 scripts/check_readme_pair.py README.md README_EN.md
```

脚本只做确定性检查：文件存在、标题树一致、代码围栏平衡、相对链接目标存在、两份文档中的命令/环境变量/版本 token 集合无明显漂移。语义准确性仍需 AI/人工复核。若目标项目无现成脚本，可从 Skill 目录运行：

```bash
python3 /path/to/write-readme/scripts/check_readme_pair.py /path/to/project/README.md /path/to/project/README_EN.md
```

交付摘要须说明：采用的模板、事实来源、实际运行过的命令、未运行或未确认的命令、生成文件和剩余风险。

#### Agent Skill 专用规则（继承 legacy 能力）

当项目包含 `SKILL.md` 时，读取其 frontmatter、`config.yaml`、`scripts/`、`references/` 和 `assets/`，把 README 写成使用者指南，而不是重复内部执行协议。至少包含：触发条件、最小 Prompt、进阶 Prompt、输入输出、推荐/备选用法、与相邻 Skill 的区别、配置/脚本入口、FAQ 和更多文档链接。只读这些文件作为事实来源，绝不修改它们。

Agent Skill README 仍遵守本 Skill 的双语约定：中文 `README.md` 与英文 `README_EN.md` 完全对齐。旧的 `write-skill-readme` 仅作为 legacy 名称保留，不应再被默认安装；安装器负责清理系统级旧目录。

#### 与其他 Skill 的协作

- `write-skill-readme`：legacy 能力已吸收；新任务统一使用 `write-readme`。
- `validate-md-ref`：可在交付前检查 Markdown 链接和锚点。
- `which-model`：若 README 需要模型选择建议，可单独生成并人工核对来源。
- `auto-test-skill`：测试本 Skill 的触发与文档契约，不替代 README 的事实校验。

### 输出

#### 输入与输出

输入：项目路径（默认当前目录）、写作目标和可选受众/定位。读取 README、许可证、包配置、入口、CI、示例、文档、测试命令等公开事实。

输出：中文 `README.md`、英文 `README_EN.md`（章节、示例、链接、命令和事实一一对应），以及可选的检查摘要（模板、已验证命令、待确认项）。

仅在用户授权的项目范围内写入上述 README 文件；不覆盖其它文档，不把密钥、令牌、个人信息或完整私有提示词写入 README。

### 输出管理

正式交付物、临时产物和日志继续遵循原有路径及覆盖边界；任务级中间文件使用当前会话声明的 `.bensz-api` 工作区。

### 校验

#### 质量门槛

- 首屏在 30 秒内说明项目用途和最短成功路径。
- Quick Start 不依赖未声明的前置步骤；命令来自仓库并尽量实际运行。
- 没有无法定位的徽章、图片、链接、功能数字或版本声明。
- 中文和英文标题树、代码块数量、命令、环境变量、相对链接与许可证事实一致。
- README 不包含凭据、隐私、内部 Prompt 或不必要的大段原始数据。
- 高级细节有明确的下一步链接；失败场景给出恢复建议或指向支持渠道。

### 失败与恢复

#### 安全与失败处理

路径仅限用户授权的项目范围；不读取或记录 `.env`、密钥文件、Cookie、SSH 凭据和私有提示词。遇到缺少入口、命令需要凭据、网络不可用或事实冲突时，保留可验证部分并在交付摘要列出阻塞点，不猜测、不静默跳过。

若发现是本 Skill 的设计缺陷（而非用户数据错误、第三方服务抖动、用户改源码或模型偶发波动），按 `bensz-collect-bugs` 规则先脱敏记录到 `~/.bensz-skills/bugs/`，当前任务继续；不得就地修改系统级已安装 Skill，也不得在未获明确授权时公开上报。


## 控制

### Runtime Contract Pack（可选）

运行时由 `bensz-skill-kernel` 按 `config.yaml.runtime` 管理 State、Verifier 与 Gate；事实收集、双语草稿和交付阶段必须绑定可引用 Evidence，未实现的写作判断仍由 Agent 完成。

当宿主提供 `bensz-skill-kernel` 时，使用 `config.yaml.runtime` 声明的
State/Verifier 子集记录阶段和验证证据；没有 Kernel 时仍按本文普通流程执行，
不得声称已自动完成验证。领域阶段按以下稳定节点推进：

`input-ready` → `facts-collected` → `bilingual-draft-ready` →
`delivery-ready` → `reported`。

运行身份必须绑定 `run_id` 与 `attempt_id`。Pair Verifier
`bensz.document.readme-pair-alignment@1.0.0` 复用确定性结构检查；路径范围、文件存在、
Markdown 链接、敏感信息脱敏和证据来源优先复用 Kernel 原子 Verifier。结构错误、越界或
敏感信息命中应 fail-closed；token 漂移、网络不可观测或事实语义不足只能标为
`uncertain`/`unchecked` 并转人工复核，不能把模型自评当作通过。

事实清单和交付摘要遵循最小 Evidence Contract：项目/双语产物使用授权的相对路径，
每条关键事实保留来源、内容哈希、来源类型和 `verified`/`user-provided`/`inferred`/
`unresolved` 状态；日志不得保存凭据、完整 Prompt 或无关原始上下文。交付前 required
Verifier 结果及 Kernel Gate 必须覆盖当前运行，否则停在检查/等待阶段或失败，不写入最终
README。

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
