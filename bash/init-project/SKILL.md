---
name: init-project
description: 当用户明确要求初始化项目、创建项目指令文件、生成 AGENTS.md，或为已有项目补齐 AI 协作规范时使用。该 Skill 会分析项目结构，并生成或更新适用于当前项目的标准化协作文档与基础目录。
metadata:
  author: Bensz Conan
  short-description: 完全自动生成 AI 项目指令文档并初始化标准 docs 目录
  keywords:
    - init-project
    - 项目初始化
    - AGENTS.md
    - CLAUDE.md
    - 项目指令
    - 项目规范
    - 自动分析项目
    - 检测项目类型
    - OpenAI Codex
    - Claude Code
    - 跨平台指令
    - "@引用语法"
    - SingleSourceofTruth
---

# Init Project

## 目标

当用户明确要求初始化项目、创建项目指令文件、生成 AGENTS.md，或为已有项目补齐 AI 协作规范时使用。本 Skill 分析项目结构，并生成或更新适用于当前项目的标准化协作文档与基础目录。

## 流程

### 输入

输入为目标项目根目录及用户选择的初始化模式；可选输入包括项目名称/描述、工作流、输出开关、`--overwrite`、`--bac-file` 和 `--disable-bac`。输出路径必须位于当前项目目录内，现有治理文件和用户自定义章节应先识别再合并。

### 执行步骤

#### 目标与边界

为当前项目生成标准 AI 协作文档，让 Claude Code / OpenAI Codex CLI 等工具理解项目目标、工程原则、变更记录规则与协作边界。

只允许在当前工作目录及其子目录内创建或修改文件。禁止写入父目录、其它项目、系统目录或用户级配置。脚本会在写入前校验输出路径，失败时立即停止。

#### 核心约束

- `AGENTS.md` 是唯一需要长期手动维护的通用指令源；`CLAUDE.md` 只做 Claude Code 适配，并通过 `@./AGENTS.md` 自动引用。
- 生成模板统一放在 `init-project/templates/`：`AGENTS.md.template`、`CLAUDE.md.template`、`README.md.template`、`CHANGELOG.md.template`、`gitignore.yaml`。
- 配置统一放在 `init-project/config.yaml`，版本号以 `skill_info.version` 为准；当前 BAC 配置在 `bac_contribution`。
- 完整初始化必须补齐 `docs/`、`docs/plans/` 与 `skills/`；`skills/` 只托管项目专属 Agent Skills。
- `skills/` 中的 Agent Skill 必须遵循 `huangwb8/skills` 仓库的 `AGENTS.md`，并配合该仓库的 `docs/templates` 使用；不得把通用 Skill 或无关项目代码放入其中。
- 代码变化导致 `docs/` 中非 `plans/` 文档过时时，生成的项目指令必须要求同步更新。
- 影响项目行为、结构、工作流、工程原则、指令文件或关键配置的变更，必须写入 `CHANGELOG.md` 的 `[Unreleased]`。

#### BAC 贡献记录

默认基于 `bensz-auto-contribution` / `bac` 记录人类、AI 与工具贡献证据：

- 默认仓库：`https://github.com/huangwb8/bensz-auto-contribution`
- 默认安装源：`git+https://github.com/huangwb8/bensz-auto-contribution.git`
- 默认文件：`docs/contribution.bac`
- Python 要求：`config.yaml:bac_contribution.min_python_version`，当前为 `3.10`
- 默认开启；用户可随时通过 `--disable-bac` 显式关闭。关闭时生成的文档也必须说明当前已关闭且可重新启用。
- 用户通过 `--bac-file` 指定项目内其它路径时，以用户指定为准；禁止把 `.bac` 文件写到项目目录外。

BAC 是过程记录与辅助审计材料，不替代最终署名、责任或合规判断；不得记录敏感密钥、完整私有提示词或无关个人隐私。

#### 推荐执行

在目标项目根目录运行：

```bash
python3 init-project/scripts/generate.py --auto
```

常用参数：

```bash
# 覆盖/强制更新已有文件
python3 init-project/scripts/generate.py --auto --overwrite

# 指定 BAC 文件，必须位于项目目录内
python3 init-project/scripts/generate.py --auto --bac-file docs/audit/contribution.bac

# 显式关闭默认 BAC 初始化
python3 init-project/scripts/generate.py --auto --disable-bac

# 只生成单类文档 / 跳过可选输出
python3 init-project/scripts/generate.py --auto --only-readme
python3 init-project/scripts/generate.py --auto --only-changelog
python3 init-project/scripts/generate.py --auto --skip-readme --skip-gitignore
```

手动模式只在用户明确给出项目信息时使用：

```bash
python3 init-project/scripts/generate.py \
  --project-name "my-project" \
  --project-description "数据科学项目" \
  --workflow "数据获取 → 分析 → 可视化"
```

#### 自动模式流程

`--auto` 会依次完成：

1. 验证输出目录必须位于当前工作目录内。
2. 分析项目：从 README 提取名称/描述，按标志文件识别项目类型，生成最多 2 层目录树。
3. 检测默认语言，失败时回退到简体中文。
4. 完整初始化时创建 `docs/` 与 `docs/plans/`。
5. 按配置决定是否启用 BAC：检查 Python 与 `bac` 包，必要时安装，初始化或验证 `.bac` 文件。
6. 生成或智能合并 `AGENTS.md`、`CLAUDE.md`。
7. 按条件生成 `README.md`、`CHANGELOG.md`、`.gitignore`。
8. 输出生成文件、目录与项目分析摘要。

项目类型识别标志：Python（`pyproject.toml`、`requirements.txt` 等）、Web（`package.json` 等）、Rust（`Cargo.toml`）、Go（`go.mod`）、Java（`pom.xml`/Gradle）、数据科学（`*.ipynb`、`*.R`、`environment.yml`）、文档（`docs/`、`mkdocs.yml`、`docusaurus.config.js`）。

#### 智能合并策略

当 `AGENTS.md` 或 `CLAUDE.md` 已存在时，默认智能合并而非直接覆盖：保留用户自定义的 `## 项目目标`、`## 核心工作流`、`## 变更边界` 及非标准章节；更新工程原则、默认语言、平台适配、`AGENTS.md` 必需章节与 `CLAUDE.md` 的 `@./AGENTS.md` 引用。`AGENTS.md` 中历史遗留的 `## 目录结构` 会被丢弃，避免回填为自定义章节；合并不符合预期时提示用户用 `--overwrite`。

#### .gitignore 策略

从 `templates/gitignore.yaml` 读取规则；缺少 PyYAML 或配置损坏时使用默认规则兜底。安全优先，默认忽略系统文件、IDE 配置、日志、临时文件、环境变量、密钥、凭证目录和常见构建/缓存产物。已有 `.gitignore` 在覆盖模式下会保留用户自定义规则。

### 输出

#### 输出文件

- `AGENTS.md`：跨平台通用项目指令，Single Source of Truth；必生成，智能合并。
- `CLAUDE.md`：Claude Code 适配层，核心为 `@./AGENTS.md`；必生成，智能合并。
- `README.md`、`CHANGELOG.md`、`.gitignore`：按需生成；`--overwrite` 可覆盖/合并。项目变更必须维护 `CHANGELOG.md`。
- `docs/`、`docs/plans/`、`skills/`：完整初始化时自动补齐；计划文档固定放在 `./docs/plans/`，项目专属 Agent Skills 固定放在 `./skills/`。
- `docs/contribution.bac`：默认 BAC 账本；`--bac-file` 可改，`--disable-bac` 可关。

### 输出管理

#### BenszAPI 任务工作区


### 校验

#### 交付前检查

- [ ] `AGENTS.md` 包含必需章节：项目目标、核心工作流、工程原则、默认语言、联网与搜索、贡献记录、Codex CLI 特定说明、变更记录与版本、有机更新原则。
- [ ] `CLAUDE.md` 正确通过 `@./AGENTS.md` 引用通用指令。
- [ ] `docs/`、`docs/plans/`、`skills/` 已存在或无需本模式创建。
- [ ] BAC 已初始化/验证，或用户已显式使用 `--disable-bac`。
- [ ] `.gitignore` 已生成/合并，且包含敏感文件忽略规则。
- [ ] `CHANGELOG.md` 已创建或变更已记录。
- [ ] 未写入当前项目目录之外的文件。

### 失败与恢复

#### 错误处理

- Windows GBK 等非 UTF-8 控制台不会因装饰性 Unicode 状态符号中止；脚本保留宿主编码，仅转义无法编码的字符，业务异常与退出码仍按原逻辑传播。
- 输出目录越界、目标目录不存在或不是目录：停止。
- `docs` / `docs/plans` / `skills` 已存在但不是目录：停止。
- BAC 安装、导入、初始化或验证失败：停止，并提示可用 `--disable-bac` 显式关闭。
- 语言检测失败：回退到简体中文。
- 项目类型无法识别：使用通用项目模板。
- `PyYAML` 缺失：脚本继续运行，配置与 `.gitignore` 使用默认值。


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
