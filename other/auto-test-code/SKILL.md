---
name: auto-test-code
category: normal
description: 当用户明确要求测试代码、代码审查或代码自检时使用。系统化发现并验证代码问题。⚠️ 不适用：用户只是想实现或优化功能、询问代码问题，或没有明确测试意图。
metadata:
  author: Bensz Conan
  short-description: 批判性思维驱动的代码自审查与优化流水线（多轮 A 轮静态/动态/安全分析 + B 轮代码质量原则检查）
  keywords:
    - auto-test-code
    - 代码审查
    - code review
    - 静态分析
    - 安全漏洞审查
    - 代码自检
---

# auto-test-code（批判性思维驱动的代码自审查技能）

## 目标

当用户明确要求"测试代码"、"运行代码审查"或"进行代码自检"时使用。通过多轮 A 轮批判性代码审查 + B 轮代码质量原则检查，系统化发现、记录、修复程序代码中的问题，并将计划/过程/结果统一沉淀到目标代码根目录的 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/` 隔离工作区。⚠️ 不适用：用户只是想优化功能（应直接修改）、只是询问代码问题（应直接回答）、没有明确"测试代码"意图。

## 流程

### 输入

输入为待审查的代码项目根目录；可选输入包括用户指定的 A 轮次数、运行 ID、测试/审查参数、配置文件和排除目录。必须覆盖核心源代码、配置/构建脚本及测试代码，并排除 `tmp/`、依赖和缓存目录；触发与不适用边界以本 Skill 的 `## 目标` 为准。

### 执行步骤

#### 工作流程

##### 隔离工作区硬规则

- 每次 skill 执行开始时，必须先在目标项目根目录创建当次专用工作区：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/`。
- 所有由 skill 生成的计划、报告、日志、辅助脚本与中间产物，**只能**写入当前 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/` 工作区内。
- 运行可能产生缓存或临时文件的命令时，优先将工作目录、`TMPDIR`、`XDG_CACHE_HOME`、`PYTHONPYCACHEPREFIX` 等重定向到当前 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/` 工作区。
- 除了用户明确要求的源码修复外，不得把 skill 相关文件写到 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/` 之外的位置，以免污染源软件项目。

##### 概览

```
用户输入（目标代码路径）
  ↓
[A轮 × N]：静态分析 → 动态推理 → 安全分类审查 → 计划 → 优化 → 轻量测试
  ↓
B轮：代码质量原则检查 → 针对性优化 → 轻量验证
  ↓
完成（文档齐全 + 问题闭环）
```

##### A 轮代码审查（可重复 N 次）

###### A.1 初始化会话（生成测试 ID + 目录）

目标：创建本轮的 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/` 会话骨架（计划/过程/结果都在同一目录）。

推荐使用确定性脚本：

```bash
# 在目标代码根目录内执行（选择你实际的安装路径）
RUN_ID=YYYY-MM-DD-HH-MM
python3 ~/.codex/skills/auto-test-code/scripts/create_session.py --code-root . --run-id "$RUN_ID" --kind a --id vYYYYMMDDHHMM
# 或
RUN_ID=YYYY-MM-DD-HH-MM
python3 ~/.claude/skills/auto-test-code/scripts/create_session.py --code-root . --run-id "$RUN_ID" --kind a --id vYYYYMMDDHHMM
```

最低要求：
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/` 存在
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/vYYYYMMDDHHMM/REVIEW.md`、`TEST_PLAN.md`、`TEST_RUN.md`、`TEST_REPORT.md` 和 `_artifacts/` 存在

###### A.2 批判性分析与计划生成（写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/` 会话目录）

目标：使用**批判性思维**发现代码中的系统性问题，写成可执行计划，按 P0/P1/P2 排序。

输出：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/vYYYYMMDDHHMM/REVIEW.md`

⚠️ **批判性思维是核心要求**：
- **必须使用「刁钻角度」思考**（详见 `references/CRITICAL_THINKING_FOR_CODE.md`）
- **必须发现至少 3 个系统性问题**（算法设计/边界条件/并发安全/内存安全/安全漏洞/设计质量）
- **禁止列出"不痛不痒"的表面问题**（如"缺少注释"等 P2 级别问题不应占多数）

**质量要求**（强制）：
- 每轮至少发现 10 个问题（P0 + P1 + P2 总和）
- 鼓励达到 15-20 个问题
- **P0 + P1 占比必须 ≥ 60%**
- **系统性问题 ≥ 3 个**（算法/边界/并发/内存/安全/架构/设计）

**核心要求**：
- **独立评估原则**（强制）：
  - 每轮 A 轮必须基于目标代码的**当前工作状态**独立分析
  - **不查看**历史 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/` 工作区中的审查文件
  - 每轮都是一次完整的、无偏见的系统性审查
- **审查范围**（强制）：
  - 必须审查：核心源代码文件（以 `config.yaml:a_round_check.independent_review.scan_patterns` 为准）
  - 必须审查：配置文件、构建脚本、测试代码
- 排除范围：`tmp/` 等 skill 产物目录，以及 `node_modules/`、`venv/`、`__pycache__/` 等依赖/缓存目录；目标项目的测试代码仍属于必须审查范围
- **全维度覆盖**（强制）：每轮必须覆盖所有审查维度（以 `config.yaml:a_round_check.dimensions` 为准）；不得以“本轮不聚焦”为由跳过任何维度
- **深挖维度**（可选）：可在全覆盖基础上额外指定 1-2 个**深挖维度**，对该维度使用刁钻角度做更细致分析；多轮时建议轮换深挖点
- **刁钻角度**：在深挖维度上必须使用至少一个刁钻角度（空输入/超大输入/恶意输入/竞态条件/资源耗尽/权限绕过/供应链污染）
- **优先级依据**：P0/P1/P2 必须有明确的判定标准
  - P0: 崩溃风险、可利用安全漏洞、未授权访问、敏感信息泄露、数据损坏、死锁/活锁、内存泄漏
  - P1: 性能问题、边界条件缺陷、逻辑错误、资源泄漏、需要前置条件或组合利用的安全风险
  - P2: 代码风格、可读性、冗余代码
- **可追溯性**：每个问题必须包含位置、现象、影响、修复建议、验证方法

**批判性思维框架**（必读）：
- `references/CRITICAL_THINKING_FOR_CODE.md` ⚠️ **核心文档，必须使用**
  - 框架 1: 静态分析视角（算法设计/数据结构/代码复杂度/设计质量）
  - 框架 2: 动态推理视角（边界条件/异常处理/资源管理）
  - 框架 3: 问题质量标准（黄金公式 + 质量检查清单）
  - 框架 4: 设计质量视角（架构/扩展性/API/状态/建模/耦合/模式）
  - 框架 5: 安全漏洞分类视角（CWE/OWASP/STRIDE/七大王国/CVSS）
- `references/A_ROUND_REVIEW_TEMPLATE.md` ⚠️ 代码审查计划模板
- `references/CODE_SMELLS.md` 代码异味识别指南
- `references/SECURITY_PATTERNS.md` 安全漏洞模式库
- `references/SECURITY_TAXONOMY.md` 安全漏洞分类审查体系（必须用于安全维度）
- `references/DESIGN_ANTI_PATTERNS.md` 设计反模式识别指南

###### A.3 执行优化与轻量测试（写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/`）

目标：按计划逐项修复，并用轻量测试验证。

输出：
- 过程：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/vYYYYMMDDHHMM/TEST_RUN.md`
- 结果：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/vYYYYMMDDHHMM/TEST_REPORT.md`

轻量测试原则：
- 只验证"核心路径"与"本轮变更点"
- 每条结论必须有可复现证据（命令输出、日志、对比结果）
- 中间产物放入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/vYYYYMMDDHHMM/_artifacts/`

可选增强：

```bash
python3 ~/.codex/skills/auto-test-code/scripts/verify_session.py --require-review .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/vYYYYMMDDHHMM
# 或
python3 ~/.claude/skills/auto-test-code/scripts/verify_session.py --require-review .bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/vYYYYMMDDHHMM
```

说明：`verify_session.py --strict` 仅用于你已将会话文档中的模板占位符全部替换后的最终自检；新建骨架默认会失败（属于预期行为）。

###### A.4 是否进入下一轮

⚠️ **强制检查**：
- [ ] 本轮已提出至少 10 个问题（P0 + P1 + P2 总和）

**进入下一轮 A 轮的条件**：
- [ ] 用户指定的轮次数未完成
- [ ] 本轮问题（P0/P1/P2）已全部闭环

**重要**：A 轮结束后，必须进入 B 轮代码质量检查。

##### B 轮代码质量检查

⚠️ **强制执行**：B 轮代码质量检查是自动测试流程的强制性环节。

###### B.1 产出质量检查报告（写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/` 会话目录）

目标：对 A 轮后的最新代码做系统性质量检查。

输出：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/b-vYYYYMMDDHHMM/REVIEW.md`

推荐使用确定性脚本创建 B 轮会话目录：

```bash
# 在目标代码根目录内执行（选择你实际的安装路径）
RUN_ID=YYYY-MM-DD-HH-MM
python3 ~/.codex/skills/auto-test-code/scripts/create_session.py --code-root . --run-id "$RUN_ID" --kind b --id vYYYYMMDDHHMM --a-test-id vYYYYMMDDHHMM
# 或
RUN_ID=YYYY-MM-DD-HH-MM
python3 ~/.claude/skills/auto-test-code/scripts/create_session.py --code-root . --run-id "$RUN_ID" --kind b --id vYYYYMMDDHHMM --a-test-id vYYYYMMDDHHMM
```

检查维度（以 `config.yaml` 的 `b_round_check.dimensions` 为准）：
- 算法复杂度分析
- 边界条件覆盖
- 异常处理完整性
- 资源管理（内存/文件/连接）
- 并发安全性
- 安全漏洞分类审查（CWE/OWASP/STRIDE/七大王国/CVSS）
- 代码可读性与可维护性
- 测试覆盖充分性
- 设计质量（可扩展性/架构/API/状态/建模/耦合/模式）

模板：`templates/B_ROUND_CODE_QUALITY_TEMPLATE.md`

###### B.2 B 轮优化与验证（写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/`）

⚠️ **强制修复要求**：
- B 轮发现的 **所有 P0-P2 问题都必须处理**
- P0 问题必须修复
- P1 问题必须修复（除非有合理理由）
- 每个修复必须有验证证据

**完成条件**：
- [ ] P0 问题修复率 = 100%
- [ ] P1 问题修复率 ≥ 80%
- [ ] 所有修复都有可复现证据

#### 可复用资源

- 配置：`config.yaml`
- 模板：`templates/`
  - A 轮审查：`templates/CODE_REVIEW_TEMPLATE.md`
  - B 轮质量检查：`templates/B_ROUND_CODE_QUALITY_TEMPLATE.md`
  - 测试计划：`templates/SESSION_TEST_PLAN_TEMPLATE.md`
  - 测试过程：`templates/SESSION_TEST_RUN_TEMPLATE.md`
  - 测试报告：`templates/SESSION_TEST_REPORT_TEMPLATE.md`
- 参考：`references/`
  - **批判性思维指南**：`references/CRITICAL_THINKING_FOR_CODE.md` ⚠️
  - A 轮审查结构：`references/A_ROUND_REVIEW_TEMPLATE.md` ⚠️
  - 代码异味识别：`references/CODE_SMELLS.md`
  - 安全漏洞模式：`references/SECURITY_PATTERNS.md`
  - 安全漏洞分类审查体系：`references/SECURITY_TAXONOMY.md` ⚠️
  - 边界条件检查清单：`references/BOUNDARY_CHECKLIST.md`
  - 设计反模式识别：`references/DESIGN_ANTI_PATTERNS.md`
- 辅助脚本：`scripts/create_session.py`
- 辅助脚本：`scripts/verify_session.py`

### 输出

#### 交付物

本技能的审查结论和验证证据必须落盘到目标代码项目的隔离工作区中，形成可追溯、可复核、后续可接续的会话文件。

默认交付根目录为 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/`；实际目录以 `config.yaml` 中的 `directories.tmp` 和 `directories.tests` 为准。

每个 A 轮或 B 轮会话目录都必须包含同一组文件：

- `REVIEW.md`：审查报告。A 轮记录批判性代码审查的问题清单与改进计划；B 轮记录代码质量原则检查结果。
- `TEST_PLAN.md`：测试计划，说明本轮要验证的修复点、核心路径和预期证据。
- `TEST_RUN.md`：测试过程记录，包含实际执行的命令、关键输出摘录和关键决策。
- `TEST_REPORT.md`：测试结果报告，包含结论、证据、遗留问题和后续建议。
- `_artifacts/`：中间产物目录，用于保存命令输出、日志、截图、对比结果等证据。

### 输出管理

#### BenszAPI 任务工作区


#### 目录与命名规范

- 运行工作区：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/`，同一次技能执行的所有 A/B 轮必须复用同一个 `run_id`。
- 会话 ID：`vYYYYMMDDHHMM`，使用分钟级时间戳。
- A 轮会话目录：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/vYYYYMMDDHHMM/`。
- B 轮会话目录：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/b-vYYYYMMDDHHMM/`，即在同类会话 ID 前增加 `b-` 前缀。
- 兼容旧目录：`verify_session.py` 可识别历史目录名 `tests/B轮-vYYYYMMDDHHMM/`；新建目录必须使用 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/b-vYYYYMMDDHHMM/`。
- 废弃目录：`reviews/` 不再创建、不再写入；如目标项目中存在旧的 `reviews/`，只视为历史遗留并在审查时排除。

### 校验

#### 完成条件（验收）

- [ ] 用户指定的 A 轮次数已完成
- [ ] B 轮代码质量检查已完成
- [ ] 每轮 A 轮平均问题数量 ≥ 10 个
- [ ] **每轮 P0 + P1 占比 ≥ 60%**
- [ ] **每轮系统性问题 ≥ 3 个**（算法/边界/并发/内存/安全/设计）
- [ ] 关键问题（P0/P1）已闭环
- [ ] `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-code/{yyyy-mm-dd-hh-mm}/output/tests/` 会话结构完整且可追溯（每轮都有 `REVIEW.md`、`TEST_PLAN.md`、`TEST_RUN.md`、`TEST_REPORT.md` 和 `_artifacts/`）

### 失败与恢复

会话脚本、测试命令或依赖失败时，保留 `TEST_RUN.md`、日志和 `_artifacts/` 中的命令输出，标记当前轮次未完成并报告可复现命令；修复后可在同一 `run_id` 的会话目录重试。目标路径越界、输入缺失或无法安全判断时停止，不把失败或不确定结果写成通过。


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
