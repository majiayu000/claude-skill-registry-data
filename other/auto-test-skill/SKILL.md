---
name: auto-test-skill
category: normal
description: 当用户明确要求测试 Skill、运行 auto-test 或对 Skill 进行批判性测试时使用。系统化发现、记录并验证 Skill 问题。⚠️ 不适用：用户只是想开发或优化 Skill，或没有明确测试意图。
metadata:
  author: Bensz Conan
  short-description: 批判性思维驱动的测试驱动优化流水线（多轮 A 轮 + B 轮质量原则检查）
  keywords:
    - auto-test-skill
    - 批判性测试
    - QA review
---

# auto-test-skill（批判性思维驱动的测试优化技能）

## 目标

当用户明确要求"测试技能"、"运行 auto-test"或"进行批判性测试"时使用。通过多轮 A 轮批判性测试 + B 轮质量原则检查，系统化发现、记录、修复问题，并将中间产物写入调用方锁定的 `.bensz-api/task-*/auto-test-skill/` 工作区。⚠️ 不适用：用户只是想优化功能（应直接修改）、只是询问技能问题（应直接回答）、没有明确"测试"意图。

## 流程

### 输入

输入为待测试的 Agent Skill 根目录；可选输入包括测试提示、A/B 轮次数、运行 ID、`config.yaml` 参数和输出路径。测试前确认目标 `SKILL.md`、配置、脚本、模板与必要 references 可读，且不把测试产物写回被测 Skill 源目录。

### 执行步骤

#### 你要产出的东西

本 skill 的交付不是“口头建议”，而是一组可追溯的文件：

（目录位置以 `config.yaml:directories` 为准；默认 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/` + `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/`）

- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/vYYYYMMDDHHMM.md`：A 轮问题分析与改进计划（每轮 1 份）
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/vYYYYMMDDHHMM/`：A 轮测试会话目录（包含 `TEST_PLAN.md` + `TEST_REPORT.md`）
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/B轮-vYYYYMMDDHHMM.md`：B 轮质量原则检查报告（维度以 `config.yaml:b_round_check.dimensions` 为准）
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/B轮-vYYYYMMDDHHMM/`：B 轮验证会话目录（包含 `TEST_PLAN.md` + `TEST_REPORT.md`）

#### 工作流程

##### 概览

```
用户输入
  ↓
[A轮 × N]：分析 → 计划 → 优化 → 轻量测试
  ↓
B轮：质量原则检查 → 针对性优化 → 轻量验证
  ↓
完成（文档齐全 + 问题闭环）
```

##### A 轮测试（可重复 N 次）

###### A.1 初始化会话（生成测试 ID + 目录）

目标：在已锁定的 `--task-root` 下创建本轮 `auto-test-skill/output/plans/` 与 `auto-test-skill/output/tests/` 骨架，不向被测 Skill 源目录写入产物。

推荐使用确定性脚本（避免 AI 每次手动拼目录/文件名）：

```bash
# 复用已锁定的项目任务目录
python3 /path/to/auto-test-skill/scripts/create_test_session.py --skill-root /path/to/target-skill --task-root /path/to/project/.bensz-api/task-YYYYMMDD-HHMM-description --kind a --id vYYYYMMDDHHMM --create-plan

# 方式2：在任意位置执行（--skill-root 指向目标 skill 根目录）
python3 auto-test-skill/scripts/create_test_session.py --skill-root /path/to/target-skill --task-root /path/to/project/.bensz-api/task-YYYYMMDD-HHMM-description --kind a --id vYYYYMMDDHHMM --create-plan
```

说明：
- 脚本会优先使用目标 skill 的 `templates/`（如存在）；否则回退到 auto-test-skill 自带的 `templates/`，确保对任意 skill 都可用。
- `--id` 可省略（脚本自动生成 `vYYYYMMDDHHMM`）；如显式指定，必须为 `vYYYYMMDDHHMM` 格式。

最低要求：
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/` 与 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/` 存在
- `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/vYYYYMMDDHHMM/TEST_PLAN.md` 与 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/vYYYYMMDDHHMM/TEST_REPORT.md` 存在
可选增强（推荐）：
- 使用 `--create-plan` 自动生成 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/vYYYYMMDDHHMM.md` 的骨架（默认不覆盖）

###### A.2 批判性分析与计划生成（写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/`）

目标：使用**批判性思维**发现系统性问题，写成可执行计划，按 P0/P1/P2 排序。

输出：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/vYYYYMMDDHHMM.md`

⚠️ **批判性思维是核心要求**（不是可选项）：
- **必须使用「刁钻角度」思考**（详见 `references/CRITICAL_THINKING_GUIDE.md`）
- **必须发现至少 3 个系统性问题**（架构/过度设计/一致/安全）
- **禁止列出"不痛不痒"的表面问题**（如"缺少注释"等 P2 级别问题不应占多数）

**质量要求**（强制）：
- 每轮至少发现 10 个问题（P0 + P1 + P2 总和）
- 鼓励达到 15-20 个问题（深入挖掘）
- **P0 + P1 占比必须 ≥ 60%**（确保问题有价值）
- **系统性问题 ≥ 3 个**（架构设计/过度设计/一致性/安全性）

**核心要求**：
- **独立评估原则**（强制）：
  - 每轮 A 轮必须基于目标 skill 的**当前工作状态**独立分析
  - **不查看**上轮的 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/` 和 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/` 文件，避免"确认偏差"与"路径依赖"
  - 每轮都是一次完整的、无偏见的系统性审查
- **审查范围**（强制）：
  - 必须审查：`SKILL.md`、`config.yaml`（核心工作文件）
  - 必须审查目录：`scripts/`、`references/`、`templates/`、`assets/`（如不存在可在计划中说明）
  - 排除范围：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/`、`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/`、`CHANGELOG.md`、`README.md`（测试产物、变更记录和用户文档，不属于 skill 的工作代码），以及 `config.yaml` 中 `a_round_check.independent_review.exclude_patterns` 命中的文件
  - 审查方法：使用 Glob/Read/Grep（如 `rg`/`find`）对工作文件做全量扫描，确保不遗漏
- **批判性聚焦**：每轮选择 1-2 个聚焦维度（系统架构/过度设计/一致性/安全性/边缘情况/用户体验）
- **刁钻角度**：必须使用至少一个刁钻角度（边缘情况/恶意输入/隐式假设/自我质疑/跨文件矛盾）
- **优先级依据**：P0/P1/P2 必须有明确的判定标准
  - P0: 阻塞性问题、安全风险、核心功能缺失、架构设计缺陷
  - P1: 重要优化（过度设计/冗余/不一致）、功能增强、测试覆盖不足
  - P2: 锦上添花、文档改进、后续迭代项
- **可追溯性**：每个问题必须包含位置、现象、影响、修复建议、验证方法
- **建设性**：每条建议必须可执行、有证据、有价值、可验证（详见 `references/CONSTRUCTIVE_SUGGESTION_GUIDELINES.md`）

**批判性思维框架**（必读）：
- `references/CRITICAL_THINKING_GUIDE.md` ⚠️ **核心文档，必须使用**
  - 框架 1: 系统视角思考（架构设计/过度设计/一致性）
  - 框架 2: 刁钻角度思考（边缘情况/恶意输入/隐式假设/自我质疑）
  - 框架 3: 问题质量标准（黄金公式 + 质量检查清单）
- `references/A_ROUND_PLAN_TEMPLATE.md` ⚠️ **已简化，突出批判性思维要求**
- `references/ISSUE_DISCOVERY_TECHNIQUES.md` 问题挖掘技巧（辅助工具）
- `references/CONSTRUCTIVE_SUGGESTION_GUIDELINES.md` 建设性建议标准
- `references/ANTI_PATTERNS_LIBRARY.md` 反例库（快速识别常见问题）

###### A.3 执行优化与轻量测试（写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/`）

目标：按计划逐项修复，并用轻量测试验证。

输出：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/vYYYYMMDDHHMM/TEST_REPORT.md`

轻量测试原则：
- 只验证“核心路径”与“本轮变更点”
- 每条结论必须有可复现证据（命令输出、文件、对比结果）
- 中间产物放入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/vYYYYMMDDHHMM/_artifacts/`，不污染主目录

可选增强（推荐，确定性自检）：

```bash
python3 auto-test-skill/scripts/verify_test_session.py --skill-root /path/to/target-skill --task-root /path/to/project/.bensz-api/task-YYYYMMDD-HHMM-description --require-plan /path/to/project/.bensz-api/task-YYYYMMDD-HHMM-description/auto-test-skill/output/tests/vYYYYMMDDHHMM
```

###### A.4 是否进入下一轮

⚠️ **强制检查**（必须满足才能进入下一轮）：
- [ ] 本轮已提出至少 10 个问题（P0 + P1 + P2 总和）
- 如未达到，必须继续挖掘问题（使用 `references/ISSUE_DISCOVERY_TECHNIQUES.md` 中的技巧）

**进入下一轮 A 轮的条件**（在满足强制检查的前提下）：
- [ ] 用户指定的轮次数未完成
- [ ] 本轮问题（P0/P1/P2）已全部闭环：修复完成，并在 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/` 会话的 `TEST_REPORT.md` 中给出验证证据

注意：每轮 A 轮都是独立评估，不因“问题已解决”而提前终止；如用户指定 N 轮，则按 N 轮执行。

**重要**：A 轮结束后（无论多少轮），必须进入 B 轮质量检查，不得跳过。

##### B 轮质量原则检查（当前 8 项）

⚠️ **强制执行**：B 轮质量检查是自动测试流程的强制性环节，除非用户明确要求跳过，否则不得省略。

###### B.1 产出质量检查报告（写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/`）

目标：对 A 轮后的最新状态做系统性质量检查。

输出：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/B轮-vYYYYMMDDHHMM.md`

检查维度（以 `config.yaml` 的 `b_round_check.dimensions` 为准）：
- 硬编码/AI 功能规划
- 冗余残留错误检查
- 安全性检查
- 过度设计检查
- 通用性检查
- 一致性检查
- 配置集中化检查：检查精确端（config.yaml）与模糊端（工作文档）是否完全分离，确保所有可配置参数集中在 config.yaml 作为单一真相来源
- SKILL.md 瘦身检查：检查 SKILL.md 是否过于冗长，应将详细内容模块化到 `references/`

模板：`templates/B_ROUND_CHECK_TEMPLATE.md`

###### B.2 B 轮优化与验证（写入 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/`）

⚠️ **强制修复要求**：
- B 轮发现的 **所有 P0-P2 问题都必须处理**（修复或明确说明不修复理由）
- P0 问题必须修复
- P1 问题必须修复（除非有合理理由）
- P2 问题应尽可能修复
- 每个修复必须有验证证据（命令输出、文件对比、测试结果）
- 修复后必须更新 `CHANGELOG.md`

**验证报告必须包含**：
1. 修复清单：每个 P0-P2 问题的修复方案和证据
2. 遗留问题：未修复问题及原因（无论优先级）
3. 变更记录：更新目标 skill 的 CHANGELOG.md

可选增强（推荐，确定性自检）：

```bash
python3 auto-test-skill/scripts/verify_test_session.py --skill-root /path/to/target-skill --task-root /path/to/project/.bensz-api/task-YYYYMMDD-HHMM-description --require-plan /path/to/project/.bensz-api/task-YYYYMMDD-HHMM-description/auto-test-skill/output/tests/B轮-vYYYYMMDDHHMM
```

**完成条件**：
- [ ] P0 问题修复率 = 100%
- [ ] P1 问题修复率 = 100%（除非有合理的不修复理由）
- [ ] P2 问题修复率 ≥ 60%（鼓励全部修复）
- [ ] 所有修复都有可复现证据

目标：对 B 轮发现的所有问题（P0-P2）进行系统性修复并验证。

推荐创建独立会话目录：

```bash
python3 /path/to/auto-test-skill/scripts/create_test_session.py --skill-root /path/to/target-skill --task-root /path/to/project/.bensz-api/task-YYYYMMDD-HHMM-description --kind b --id vYYYYMMDDHHMM --a-test-id vYYYYMMDDHHMM --create-plan
```

输出：`.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/B轮-vYYYYMMDDHHMM/TEST_REPORT.md`

#### 可复用资源

- 配置：`config.yaml`
- 模板：`templates/`
  - A 轮计划：`templates/OPTIMIZATION_PLAN_TEMPLATE.md`
  - B 轮质量检查：`templates/B_ROUND_CHECK_TEMPLATE.md`
  - Bug 报告：`templates/BUG_REPORT_TEMPLATE.md`
  - 最终总结：`templates/FINAL_SUMMARY_TEMPLATE.md`
  - 测试计划：`templates/TEST_PLAN_TEMPLATE.md`
  - 测试报告：`templates/TEST_REPORT_TEMPLATE.md`
- 参考：`references/`
  - **批判性思维指南**：`references/CRITICAL_THINKING_GUIDE.md` ⚠️ **核心文档，必须使用**
  - A 轮计划结构：`references/A_ROUND_PLAN_TEMPLATE.md` ⚠️ **已简化，突出批判性思维**
  - 测试最佳实践：`references/TESTING_BEST_PRACTICES.md`
  - 建设性建议标准：`references/CONSTRUCTIVE_SUGGESTION_GUIDELINES.md`
  - 问题挖掘技巧：`references/ISSUE_DISCOVERY_TECHNIQUES.md`
  - 反例库：`references/ANTI_PATTERNS_LIBRARY.md`
- 辅助脚本：`scripts/create_test_session.py`
- 辅助脚本：`scripts/verify_test_session.py`

### 输出

每轮必须交付可追溯文件：A 轮计划 `output/plans/vYYYYMMDDHHMM.md`、A 轮会话 `output/tests/vYYYYMMDDHHMM/`，B 轮报告 `output/plans/B轮-vYYYYMMDDHHMM.md` 和 B 轮会话 `output/tests/B轮-vYYYYMMDDHHMM/`；各会话至少包含 `TEST_PLAN.md` 与 `TEST_REPORT.md`，具体目录以 `config.yaml:directories` 为准。

### 输出管理

#### BenszAPI 任务工作区


#### 目录与命名规范

- 测试会话 ID：`vYYYYMMDDHHMM`（分钟级时间戳）
- 规划文档：默认放在 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/`（以 `config.yaml:directories.plans` 为准）
- 测试会话：默认放在 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/`（以 `config.yaml:directories.tests` 为准）
- B 轮统一加前缀：`B轮-`

### 校验

#### 完成条件（验收）

- [ ] 用户指定的 A 轮次数已完成（或明确说明提前结束原因）
- [ ] B 轮质量检查已完成并形成报告（⚠️ 强制要求，参考 `config.yaml` 的 `b_round_check.mandatory`）
- [ ] 每轮 A 轮平均问题数量 ≥ 10 个（P0 + P1 + P2 总和）
- [ ] **每轮 P0 + P1 占比 ≥ 60%**（确保问题有价值）
- [ ] **每轮系统性问题 ≥ 3 个**（架构/过度设计/一致/安全）
- [ ] 关键问题（P0/P1）已闭环：计划 → 修复 → 证据 → 结论
- [ ] B 轮 P0 问题修复率 = 100%，P1 问题修复率 = 100%（或在报告中逐条说明不修复理由）
- [ ] `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/plans/` 与 `.bensz-api/task-{yyyymmdd-hhmm}-{简短描述}/auto-test-skill/output/tests/` 结构完整且可追溯
- [ ] 目标 skill 的 `CHANGELOG.md` 已更新

### 失败与恢复

脚本、目标 Skill 读取或测试执行失败时，保留当前会话的计划、日志和测试报告，明确区分输入缺失、环境错误与行为失败，并给出复现命令；可在同一任务工作区重试未完成阶段。证据不足时不得臆测通过，A 轮与 B 轮的强制环节不得静默跳过。


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
