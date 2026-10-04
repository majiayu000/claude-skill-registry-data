---
name: auto-test-project
category: normal
description: 当用户明确要求“测试项目”、 “运行 auto-test-project”或“进行项目级测试”时使用。对完整项目执行多轮 A 轮批判性测试与 B 轮质量检查，发现、记录、修复并验证问题。⚠️ 不适用：用户只是想优化功能、询问项目问题，或没有明确测试意图。
metadata:
  author: Bensz Conan
  short-description: 多轮 A 轮测试 + B 轮质量检查的项目级测试驱动优化流水线
  keywords:
    - auto-test-project
    - 项目级测试
    - project QA
---

# auto-test-project（项目级自动化测试驱动优化）

## 目标

为具备明确目录和可执行入口的完整项目提供可追溯的项目级测试与优化流水线：项目初始化、A 轮问题发现与修复、B 轮质量原则检查、验证和交付总结。仅在用户明确要求项目级测试时触发；单个 Agent Skill 使用 `auto-test-skill`。

本 Skill 将“项目”定义为具有指令文件或等价入口、明确目录结构和功能模块，并包含可执行代码、脚本或流程定义的项目，包括 Agent Skills、工作流项目、脚本工具集和结构化文档项目。本 Skill 不替代领域业务判断，不默认修改远程系统，不把报告模式误当作发布阻断，也不负责单 Skill 测试。

## 流程

### 输入

- 项目根目录、用户指定的测试范围、优化目标或 A 轮次数。
- 项目指令文件、配置文件、模块目录、可执行代码/脚本和已有测试入口。
- 需要关注的历史问题、已知约束和可接受的修改边界。

排除历史任务产物、缓存、依赖目录和敏感信息。先验证项目结构与可执行入口，再确定项目类型、核心模块和跨模块测试边界；配置中的 `project_testing`、`a_round` 和 `b_round_check` 是规划口径的单一来源。

### 执行步骤

1. **初始化会话**：使用宿主已经公开并锁定的任务根；调用 `scripts/create_test_session.py` 创建 A/B 会话及模板文件。缺省 `--task-root` 时才分配新任务；A/B 轮和 continuation 必须显式复用同一 task root，不猜测最近任务。
2. **识别项目**：检查指令文件、目录结构、功能模块、入口和测试边界，排除 `node_modules/`、`__pycache__/`、`.git/`、`tests/`、`plans/` 和 `_artifacts/` 等配置的排除路径。
3. **执行 A 轮（可重复 N 次）**：结合 `references/CRITICAL_THINKING_GUIDE.md` 与配置的审查范围独立发现问题；为每个问题记录证据、影响、优先级、修复建议和验收标准，形成可引用的 `P0-1` 等编号。
4. **修复并轻量测试**：按计划优先修复 P0/P1，再处理其它问题；只做最小必要修改，补充 `TEST_PLAN.md` 和 `TEST_REPORT.md` 中的可复现命令、结果和证据。项目已有测试时优先运行受影响范围，再按风险扩大验证。
5. **判断下一轮**：检查计划中的问题是否均有报告对应项、成功标准是否有验证结论，以及 P0/P1 是否闭环；达到用户指定轮数或明确的停止条件后进入 B 轮。
6. **执行 B 轮质量检查**：依据 `config.yaml:b_round_check.dimensions` 检查硬编码与 AI 功能规划、冗余残留、安全性、过度设计、通用性、一致性、项目指令文件瘦身和配置集中化；对发现的 P0/P1 做针对性修复与轻量验证。
7. **收尾验证**：每个会话运行 `scripts/verify_test_session.py`，最终运行 `scripts/verify_all_sessions.py --require-plan`；更新目标项目的 `CHANGELOG.md`，并保留失败证据与提前结束原因。

### 输出

交付以下可追溯产物，具体模板由 `config.yaml:templates` 指定：

- A 轮计划：`<task-root>/auto-test-project/output/plans/vYYYYMMDDHHMM.md`。
- A 轮会话：`<task-root>/auto-test-project/output/tests/vYYYYMMDDHHMM/`，包含 `TEST_PLAN.md` 和 `TEST_REPORT.md`。
- B 轮计划：`<task-root>/auto-test-project/output/plans/B轮-vYYYYMMDDHHMM.md`。
- B 轮会话：`<task-root>/auto-test-project/output/tests/B轮-vYYYYMMDDHHMM/`，包含 `TEST_PLAN.md` 和 `TEST_REPORT.md`。
- 正式代码、文档和项目 `CHANGELOG.md`：按目标项目原有目录约定保存。

报告必须区分已修复、未修复、无法验证和不确定问题，并提供复现命令或后续人工动作；不得用空报告或口头结论代替证据。

### 输出管理

所有计划草案、测试报告、会话元数据、命令输出和验证证据写入当前任务根下的 `auto-test-project/`，不得写入旧的 `.bensz-api/skills/auto-test-project/`。规划文档放在 `output/plans/`，会话放在 `output/tests/`，B 轮会话名统一使用 `B轮-` 前缀。

旧目录仅允许验证脚本通过 `--legacy-root` 显式只读检查；创建脚本不得写入。不得覆盖用户已有文件，不得把缓存、依赖或测试运行产物写入源码目录。

### 校验

使用分钟级会话 ID `vYYYYMMDDHHMM`。典型 A 轮初始化与验证命令如下：

```bash
TASK_ROOT=".bensz-api/task-{yyyymmdd-hhmm}-{简短描述}"
python3 auto-test-project/scripts/create_test_session.py \
  --project-root . --task-root "$TASK_ROOT" --kind a --create-plan
python3 auto-test-project/scripts/verify_test_session.py \
  --project-root . --task-root "$TASK_ROOT" --require-plan \
  "$TASK_ROOT/auto-test-project/output/tests/vYYYYMMDDHHMM"
```

B 轮创建时显式关联 A 轮：

```bash
python3 auto-test-project/scripts/create_test_session.py \
  --project-root . --task-root "$TASK_ROOT" --kind b \
  --id vYYYYMMDDHHMM --a-test-id vYYYYMMDDHHMM
```

最终验证：

```bash
python3 auto-test-project/scripts/verify_all_sessions.py \
  --project-root . --task-root "$TASK_ROOT" --require-plan
```

通过标准：每轮会话均有非空计划和报告，模板占位符已替换，计划与报告的问题编号和成功标准可对应，验证脚本通过，P0 修复率为 100%，P1 修复率达到配置门槛，且 B 轮强制完成或明确记录无法完成的原因。仓库级 Skill 结构和公共约束由仓库治理检查器负责，不由本 Skill 的会话验证脚本替代。

### 失败与恢复

将失败分类为输入缺失、项目结构无效、脚本错误、测试失败、外部依赖不可用和结果不确定；保存命令、输出、错误和已生成证据，不伪造通过、不删除失败记录。

可在同一任务根重试未完成阶段；A/B continuation 必须复用原 task root 和关联 ID。输入或环境问题先停止并给出补充项/复现命令；测试失败保留失败报告并允许针对性修复后重跑；无法取得可靠证据时标记为不确定并转人工复核。达到用户指定轮数后不得擅自扩展范围。

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

- A 轮至少按配置完成用户指定次数；若提前结束，必须说明原因和未完成范围。
- B 轮质量检查为强制阶段，维度以 `config.yaml:b_round_check.dimensions` 为准，不得在正文另设易漂移的默认清单。
- 计划、修复、测试、证据和结论必须形成闭环；P0/P1 不得仅以建议或口头判断结案。
- 与 `auto-test-skill` 的边界固定为：本 Skill 面向完整项目及跨模块关系，`auto-test-skill` 面向单个 Skill 目录。
- 可复用的 FAQ（`references/FAQ.md`）、最佳实践、问题挖掘技巧、反例、严格示例（`references/EXAMPLE_STRICT_MINIMAL.md`）和报告示例放在 `references/`；会话创建、单会话验证、批量验证和 Skill 自检使用 `scripts/`，不得把这些详细材料重新堆回正文。
