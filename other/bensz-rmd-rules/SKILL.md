---
name: bensz-rmd-rules
description: 当主要交付物是基于 R 的数据分析流程、科学结果、可复现数据产品、R Markdown/HTML 报告或论文级图表与解读时使用；即使流程中包含 `.R` 脚本和仅服务当前分析的辅助函数，也由本 Skill 主导。⚠️ 不适用：主要交付物是可独立复用的 R 函数、稳定公共 API、类或 R Package；这些任务使用 bensz-r-developer。也不用于仅渲染既有 Rmd 或其它语言的数据分析。
metadata:
  author: Bensz Conan
  short-description: R/Rmd 多阶段分析、可恢复数据产品与论文级报告规范
  keywords:
    - bensz-rmd-rules
    - R Markdown
    - Rmd
    - 数据分析
    - 断点续算
    - 可复现报告
---

# bensz-rmd-rules

## 目标

把研究目标和数据组织为可审查、可复现的 R 分析流程。新项目必须用 `renv`，并在真实 R/Rmd 入口完成轻量测试：线性低成本流程用 `simple`；有非线性依赖、昂贵步骤、复用、局部失效、恢复、血缘或并行需求时用 **targets-first complex/pipeline**（`_targets.R` 唯一 DAG，计算函数在 `R/`，Rmd 只消费 target）。`_targets/` 是机器状态，`products/`/`reports/` 是科学产物。已有项目不自动补齐或迁移：有 `_targets.R` 按 complex，无 targets（含历史编号脚本）按 simple；需要复杂能力时由人类显式迁移。本 Skill 不维护编号 runner。

主要交付物决定触发，而不是扩展名：

| 交付物 | 主导 Skill |
| --- | --- |
| 分析数据流、统计结果、可恢复产品、Rmd/HTML、图表与解读 | `bensz-rmd-rules` |
| 可复用、版本化或跨项目的函数、类、API、Package | `bensz-r-developer` |
| 分析需要可复用组件 | 本 Skill 定义需求/集成证据，`bensz-r-developer` 实现，本 Skill 接回验证 |

可创建只服务当前分析的 `R/` 函数和 helper，但不扩展为公共 Package。`luckyBase` 是唯一固定 Bensz 依赖；其它包由项目写入 `renv.lock`。`crew`、`autometric`、集群插件只是项目级可选依赖；不自制调度器、日志协议、worker 状态机或资源采样器。本 Skill 不自动接入 State、Verifier、Pack 或 Gate。

## 流程

### 输入

收集：研究问题、用途、交付物、统计边界和完成判据；主要/次要估计对象、目标人群、观察单位、对比与效应尺度、研究设计、缺失/依赖结构、预注册方案及推断目的；原始输入/数据字典/隐私授权及 `raw/` 只读边界；重算成本、依赖、外部请求、随机性、关键参数和恢复需求；现有 R/Rmd、`00.Environment.R`、产品路径、`tmp/`、`_targets.R`、`renv.lock`/`renv/`；可用测试数据与边缘条件；函数复用范围。缺失信息只有在改变行为或安全边界时才询问。

先读 `config.yaml`，再按任务读取最少 references：
- 模式/目录：[`workflow_modes.md`](references/workflow_modes.md)、[`hybrid_architecture_guide.md`](references/hybrid_architecture_guide.md)；测试：[`lightweight_testing.md`](references/lightweight_testing.md)。
- 缓存/示例：[`analysis_workflow_cache.md`](references/analysis_workflow_cache.md)、[`hybrid_architecture_examples.md`](references/hybrid_architecture_examples.md)；审查：[`serial_review_protocol.md`](references/serial_review_protocol.md)。
- R 实现：[`code_style_guide.md`](references/code_style_guide.md)、[`no_overdefensive_code.md`](references/no_overdefensive_code.md)、[`cross_platform.md`](references/cross_platform.md)。
- 指标/解读：[`metric_explanation_protocol.md`](references/metric_explanation_protocol.md)、[`four_tier_interpretation_framework.md`](references/four_tier_interpretation_framework.md)、[`interpretation_templates.md`](references/interpretation_templates.md)、[`interpretation_narrative_examples.md`](references/interpretation_narrative_examples.md)、[`expert_discussion_template.md`](references/expert_discussion_template.md)。
- 论文级估计与检验：[`statistical_inference_protocol.md`](references/statistical_inference_protocol.md)；计算前逐项确定可估计性与方法，报告时逐项核对。
- 图表/HTML：[`plot_quality_standards.md`](references/plot_quality_standards.md)、[`plot_language.md`](references/plot_language.md)、[`htmlwidget_visibility_rules.md`](references/htmlwidget_visibility_rules.md)、[`liquid_glass_theme_guide.md`](references/liquid_glass_theme_guide.md)；ID/函数：[`gene_id_guidelines.md`](references/gene_id_guidelines.md)、[`candidate_r.md`](references/candidate_r.md)。

对 `raw/` 仅做规划和选样所需的轻量只读盘点，不启动完整计算。

### 执行步骤

1. **映射交付与推断**：若只要公共函数/API/类/Package，转交 `bensz-r-developer`；否则建立 target—输入—科学产品—报告—完成判据映射，确保依赖无环。计算前列出影响论文结论的主要与次要估计对象，逐项判断是否需要且能够给出区间/检验，记录设计、方法理由和结果去向；预注册方案优先，不为显著性事后更换主终点或检验。纯描述、固定常数或不可估计项明确标状态与原因，不伪造 CI/p。新 pipeline 的计算函数放 `R/`，由 `_targets.R` 的 `tar_source("R")` 发现；`00.Environment.R` 默认唯一，只负责包、项目根、产品路径和全局配置。
2. **判状态和模式**：先运行
   ```bash
   python3 <skill-root>/scripts/check_targets_renv.py <项目根> --project-state auto --workflow-mode auto
   ```
   优先级为人类要求 → existing 边界 → 复杂度。新项目默认 simple；复杂信号（非线性、昂贵/高失败代价、多下游复用、局部失效、恢复、血缘、并行）选 complex。`existing` 不是第三种模式：有 `_targets.R` 按 complex，否则按 simple；不创建缺失 targets/renv，不隐式迁移。详见 [`workflow_modes.md`](references/workflow_modes.md)。
3. **固定路径**：按需使用 `00.Environment.R`、`R/`、`_targets.R`、`raw/`、`products/`、`reports/`、`templates/`、`scripts/tests/`、`tmp/tests/<run-id>/`、`tmp/scratch/`、`renv.lock` 和 `renv/activate.R`，不预建空目录。`products/` 只存需审阅/复用/交付的科学产物；路径优先级为人类指定 → 已有路径 → 项目统一设置 → `products/`，必须在项目内且不得与 `raw/`、`reports/`、`tmp/`、`_targets/`、`.bensz-api/` 重叠。
4. **设计缓存边界**：只导出昂贵、可复用、高风险/有损、需人工审查、依赖可变外部请求或中断代价高的结果。targets 管理 `_targets/` metadata、失效和增量重建；禁止 `SUCCESS`、identity hash、force-step/resume runner 或 checkpoint helper。详见 [`analysis_workflow_cache.md`](references/analysis_workflow_cache.md)。
5. **计算推断并实现报告**：`00.Environment.R` 用 `luckyBase::Plus.library()`；分析代码优先 `pkg::fn()`，基因 ID 用 `luckyBase::convert()`。分析层对关键参数计算估计值、适当的默认 95% CI（方案另有水平时从其规定），并仅在有明确检验问题时给 p 值；多重检验记录校正方法与 q/调整后 p。保留未经显著性筛选的完整结果，含参数身份、尺度/单位、有效 N/事件数、方法、CI 界限/水平、适用的 p/q、来源及不适用/不可估计/未运行状态与理由。complex 的 `R/` 函数读取 `raw/`/上游 target；Rmd 用 `tar_read()`/`tar_load()` 消费真实结果，不在正文臆算。Top N/阈值/配色放 YAML `params`。target 语义化命名并按阶段注释；交付摘要附 `targets::tar_manifest()`。静态图写 `reports/`，HTML 留根目录；默认不在图内重复标题。只在 I/O 边界和硬前提检查，不用占位/静默降级掩盖失败。
6. **真实轻量测试**：新建或实质修改流程选择 `synthetic_fixture`（保 schema、类型、主键、分组、缺失和边缘条件，固定种子）或有授权时的 `project_subset`（覆盖关键分组/结局/缺失/异常，不能仅 `head(n)`）。测试在 `scripts/tests/`，每次使用唯一 `tmp/tests/<run-id>/`；只改输入规模和路径，不加业务 `analysis_mode`/`test_mode`。simple 调正式入口；complex 执行同一 DAG，store 放 `<run-id>/_targets`。至少断言输入契约、类型/主键、数值不变量、产品/报告生成和 `raw/` 未写入。checker/语法/`--dry-run` 仅为 `preflight`；真实链为 `lightweight_execution`；未跑全量记 `full_data_execution=NOT_RUN`。按环境依赖、fixture/子集、路径隔离、分析代码、科学断言、渲染、外部服务分类失败。
7. **串行审查**：初稿和轻量测试后，按 [`serial_review_protocol.md`](references/serial_review_protocol.md) 完成结构/数据流、R/恢复、科学/统计三项只读审查；每项读取前项修正后的最新版本。影响执行、输出或断言的修正会使旧证据失效，须在最新 identity 上重跑受影响链；不能提供独立 Agent 时须记录降级。
8. **正式运行与报告**：simple 用明确 R/Rmd 入口；complex 先检查契约，再 `targets::tar_make()`，store 为 `_targets/`。中断后用 `tar_meta()`、outdated 集合和执行记录证明有效 target 被跳过，不手工写 `SUCCESS`。图表默认英文，中文场景用 `params.plot_language`；静态图保存 PDF，并在任务工作区生成 JPG 预览。每个关键结论给出与计算产品对应的估计值、CI、有明确假设时的 p/q、实际意义与局限；无法推断时写清状态和理由。图/表附近给对象、方向/对比与可追溯证据，不为装饰性数字逐个检验。

### 输出

交付需求—target—报告映射、唯一 `00.Environment.R`、`R/` 函数、Rmd/HTML、`renv.lock`、`renv/activate.R`、`scripts/tests/`、`reports/` 和验证摘要。complex 另交 `_targets.R` 与 `tar_manifest()` 快照，按需交分析计划和科学产品；simple 不创建 targets。测试记录绑定最新 identity，分别报告三层执行状态，不能以轻量通过暗示全量通过。

### 输出管理

正式代码、测试、Rmd/HTML、产品和报告留在用户项目约定位置；草稿、审查、JPG 和日志进入当前 `.bensz-api/task-*`；测试现场进入 `tmp/tests/<run-id>/`。不写 `raw/`；`products/` 不放草稿；`reports/` 不放源码、缓存或审查日志；`tmp/scratch/` 的重要发现须晋升并补 renv/轻量测试证据。

### 校验

```bash
# 新 simple
python3 <skill-root>/scripts/check_targets_renv.py <项目根> --project-state new --workflow-mode simple
Rscript -e 'renv::status()'
Rscript <项目根>/scripts/tests/smoke_test.R

# 新 complex
python3 <skill-root>/scripts/check_targets_renv.py <项目根> --project-state new --workflow-mode complex
Rscript -e 'renv::status()'
Rscript <项目根>/scripts/tests/smoke_test.R
Rscript -e 'targets::tar_make()'
Rscript -e 'targets::tar_meta()'

# 已有项目
python3 <skill-root>/scripts/check_targets_renv.py <项目根> --project-state existing --workflow-mode auto
```

所有 Rmd 还要检查解读覆盖/质量、widget 可见性、图表可读性和数字追溯，并按实际情况做 R 语法/运行、Rmd 渲染；逐项复核主要估计对象的结果或不可估计理由、CI/p 方法与设计的一致性。现有文本检查器只作启发式预检，词语命中不证明推断已计算或方法正确。检查清单见 [`workflow_checklist.md`](references/workflow_checklist.md)，证据格式见 [`delivery_verification.md`](references/delivery_verification.md)。最低验收：模式理由可复述、renv 可信、测试未污染正式路径、Rmd 未绕过 DAG、恢复可证明、已有项目未隐式迁移、跳过项不写成通过。

### 失败与恢复

- 缺 `luckyBase` 或新项目无 renv：停止补齐前提，不更换包管理逻辑。
- simple 出现复杂信号：评估升级 complex，不扩展调度器或无理由降级。
- 测试失败：按失败类别最小修正并重跑；权限/网络/授权/依赖不足时记录阻塞，不伪造成功。
- complex 测试写正式 `_targets/`、products、reports 或 raw：停止、隔离并确认正式路径后重跑。
- targets 失效/失败按 outdated/error 重算必要节点；不伪造 `SUCCESS`。Rmd 渲染失败只从报告层恢复。
- existing 冲突不覆盖/迁移；沿现有 targets 或顺序入口做授权增量修改，需复杂能力时显式迁移。

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

- 只在授权范围内只读盘点 `raw/`；不得修改、覆盖或向其写入，也不在日志中记录绝对私有路径、凭据或不必要原始值。
- 不因模板存在就创建全部文件；模式、缓存边界和目录由真实需求决定。
- 新 pipeline 不引入 checkpoint helper、SUCCESS 或自定义 identity runner；该自制缓存机制已移除，不得在任何项目中新引入或修复。
