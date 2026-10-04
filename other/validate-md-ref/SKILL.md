---
name: validate-md-ref
description: 检查 Markdown 文档中的引用是否可定位、URL 或锚点是否可访问，并整理供后续判断引用真实性与适切性的结构化证据。当用户要求核查引用、检查文档链接，或确认引用是否支持正文论断时使用。
metadata:
  author: Bensz Conan
  short-description: 检查 Markdown 引用是否可定位、可访问
  keywords:
    - validate-md-ref
---

# validate-md-ref

## 目标

检查 Markdown 文档中的引用是否可定位、URL 或锚点是否可访问，并整理供后续判断引用真实性与适切性的结构化证据。当用户要求核查引用、检查文档链接，或确认引用是否支持正文论断时使用。

## 流程

### 输入

#### 范围与边界

- 输入：一个 Markdown 文件，可选一个 YAML 配置文件。
- 检查：Markdown 行内链接、HTML `<a href>` 链接、当前文档内的 `#anchor`，以及外部 HTTP(S) 链接的可达性。
- 输出：结构化 JSON，逐条保留引用位置、验证状态和失败或跳过原因。
- 不做：不修改原文；URL 可达性不等于来源支持论断；不代替用户决定修复方式。
- 运行时能力：使用 `bensz.document.markdown-link-integrity` 检查链接事实，并保留 `bensz.evidence.citation-truth-fit` 的语义复核状态；两者版本独立记录，旧 ID 仅作兼容 alias。

### 执行步骤

#### 强制运行门禁

每次执行必须经过 Bensz Skill Kernel 状态机并调用指定版本的链接完整性 Verifier。任一环节不可用或失败，任务即未完成并须说明原因；不得降级为普通脚本或手工检查。

状态机使用 `bensz.workspace.ready` 作为系统入口，并依次进入 `bensz.validate-md-ref.input-ready`、`bensz.validate-md-ref.checking` 和 `bensz.validate-md-ref.reported`；旧 State ID 仅作兼容 alias。

AI 应使用本 Skill 的执行器或封装入口，不得手工模拟状态转移、拼接事件账本或复制 Verifier 规则。命令、上下文和事件契约见：

- [`references/state-machine.md`](references/state-machine.md)
- [`references/verifiers.md`](references/verifiers.md)

#### 流程

1. 确认 Markdown 存在并只读处理；需限制网络请求时加载默认或指定 YAML。
2. 提取并分类检查：站内锚点在当前文档定位；HTTP(S) 按安全策略验证可达性；白/黑名单命中则跳过。
3. 保留链接 Verifier 标准结果；真实性或适切性仅保留语义 Verifier 的 `unchecked`/`manual_review`，无证据不得判通过。
4. 汇总总数、有效、无效、跳过项，逐条披露位置、状态、失败原因和语义边界。

网络 DNS、连接失败和超时属于 `unresolved`/`timed_out` 观测不确定性，不得当作确定性链接失效；只有 HTTP 明确错误、本地 anchor 缺失或越界文件才计入 `invalid`。

命令行入口以 kernel `bensz.document.markdown-link-integrity` Pack 返回的
`facts.summary` 与 `facts.references` 为唯一链接事实来源；不要将旧兼容函数的本地
探测结果与 Verifier 结果合并或互相覆盖。

#### 工具

- `scripts/validate_links.py`：读取 Markdown 及可选 YAML，输出结构化结果。
- `config.yaml`：提供默认超时、域名白名单和黑名单，并在 `runtime` 节声明状态包与 Verifier 选择。

从 Skill 目录调用脚本；工作目录不同则使用绝对路径或先切换目录。运行入口负责状态机和 Verifier 门禁，不得绕过门禁解释脚本结果。

常用业务调用形式：

```bash
python3 scripts/validate_links.py DOCUMENT.md
python3 scripts/validate_links.py DOCUMENT.md CONFIG.yaml
```

输出字段和配置字段的完整说明见 [`references/formats.md`](references/formats.md) 与 [`references/tools.md`](references/tools.md)。

### 输出

输出结构化引用检查结果、可定位证据和报告：记录每条引用的来源、URL/锚点状态、错误或不确定原因，以及供后续真实性/适切性判断使用的 Evidence 快照；不修改源 Markdown。

### 输出管理

#### 文件边界

需落盘时，将本 Skill 的输入、临时结果和日志写入当前会话声明的 `./.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/validate-md-ref/{input,output,log}/`；多 Skill 共享材料放任务根目录 `shared/`。正式交付物、用户指定文件和源 Markdown 留在项目约定位置。不得写入密钥、令牌、Cookie、私有指令、隐私或不必要的大体积原始数据；纯文本答复无需建目录。

### 校验

校验输入路径位于允许的 `base_dir`、拒绝越界/symlink 逃逸和敏感路径，按配置检查 URL/锚点、重定向、域名白黑名单和超时；required 链接完整性通过后才可放行，advisory 真实性判断仅作提示并保留人工复核。

### 失败与恢复

文件不可读、路径越界、URL/锚点检查超时或外部站点不可用时，保留已收集的 Evidence、错误分类和日志，按 required/advisory 规则阻断或标记 `uncertain/unchecked`；修复输入或网络后可在同一任务工作区重试，不把缺失证据视为通过。


## 控制

运行时由 `bensz-skill-kernel` 按 `config.yaml.runtime` 管理 State、Verifier 与 Gate；链接完整性为 required，语义真实性为 advisory，失败或不确定时保留证据并转人工复核。

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

### Skill 专属约束

#### 疑似 Skill 设计问题

- **适用范围**：仅记录流程漏判、输入约定不完整、环境假设错误等 Skill 设计缺陷；用户数据错误、第三方波动和偶发模型输出除外。
- **隐私保护**：不得记录密钥、密码、身份信息、邮箱、私密路径、用户名、主机名或工作目录；公开前须脱敏。
- **本地优先**：先写入 `~/.bensz-skills/bugs/`，不打断任务；仅用户明确要求时用本机 `gh api` 上报。
- **禁止就地修 bug**：不要直接修改用户本地已安装 Skill 源码；先记录，再继续任务。
