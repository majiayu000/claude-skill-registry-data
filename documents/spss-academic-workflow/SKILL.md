---
name: spss-academic-workflow
description: "Use when the user wants a complete SPSS or SPSS-MCP empirical research workflow: organize source data, prepare datasets, design variables and models, run SPSS analyses, export Chinese result paragraphs and tables, write a Chinese LaTeX paper, and compile the final PDF."
metadata:
  short-description: "Run SPSS empirical analysis and draft a Chinese LaTeX paper"
---

# SPSS Academic Workflow

本 skill 用于把原始数据推进为完整的中文实证研究交付物：数据整理、研究设计、SPSS 统计分析、结果表格、中文论文正文、LaTeX 源码和 PDF。它的核心主题始终是“基于 SPSS 的实证分析”，写作与排版服务于分析结论，而不是反过来主导流程。

## 适用任务

当用户提出以下需求时使用本 skill：

- 使用 `SPSS`、`SPSS-MCP` 或 `SPSS syntax` 完成实证分析
- 从 Excel、CSV、SAV 等原始数据生成描述性统计、相关、回归、方差分析或其他统计结果
- 将统计结果整理成中文“结果”段落、表格和 LaTeX 论文
- 在指定项目目录内完成从原始数据到 `.tex`、PDF 的完整交付

## 执行模式

本 skill 按两种模式工作：

- 显式分析模式：用户明确说明分析类型，例如回归、t 检验、方差分析、相关、聚类、因子、信度、逻辑回归、生存分析等。此时优先执行用户指定分析，同时补齐必要的数据读取、描述统计、结果解释与成果整理。
- 自动路由模式：用户只说“使用 spss skills 分析这份数据”或“看看这份数据适合做什么分析”。此时先读取数据结构，再根据变量类型、研究问题和样本条件自动选择保守且合理的分析路径。

除非用户明确要求只做单一检验，否则不要只输出一张软件结果表；至少要补齐数据概览、变量说明和中文结果解释。

## 核心流程

1. 侦察项目：确认项目根目录、原始数据文件、已有产物和潜在旧分析。
2. 建立目录：创建标准目录树，必要时复制原始数据到 `01_source_data/raw/`。
3. 读取数据：检查变量名、样本量、缺失情况、变量类型和取值范围。
4. 研究设计：在 `03_research_design/` 中明确研究问题、假设、变量设计、模型设计和样本规则。
5. 数据准备：在 `02_data_prep/` 完成重命名、编码转换、缺失处理、异常值处理、变量标签和样本筛选。
6. 运行 SPSS：在 `04_spss_syntax/` 中用 SPSS-MCP 或 SPSS syntax 执行描述统计、相关、回归和补充检验。
7. 解析结果：把 SPSS 输出整理成 `05_analysis_output/` 下的表格、图形、说明笔记、日志和论文输入接口。
8. 完善设计：根据数据条件补充诊断检验、稳健性、异质性、机制或替代模型。
9. 写作论文：在 `06_paper_draft/` 中生成中文实证论文，包括摘要、引言、文献与假设、数据变量、模型、结果、讨论、结论和局限。
10. 排版与编译：按普通中文论文版式组织主稿，检查表格接口、引用流和编译链，输出 PDF。
11. 汇报交付：说明文件路径、调用工具、主要结论、研究限制和验证状态。

## 项目结构

用户给定项目根目录后，所有新产物默认写入该目录。标准结构如下：

```text
project-name/
├── 01_source_data/
│   ├── raw/
│   ├── external/
│   └── documentation/
├── 02_data_prep/
│   ├── mapping/
│   ├── interim/
│   ├── final/
│   └── audit/
├── 03_research_design/
│   ├── question.md
│   ├── hypotheses.md
│   ├── variable_design.md
│   ├── model_design.md
│   └── sample_rules.md
├── 04_spss_syntax/
│   ├── data_cleaning/
│   ├── variable_construction/
│   ├── descriptive/
│   ├── main_models/
│   ├── robustness/
│   └── appendix_models/
├── 05_analysis_output/
│   ├── tables/
│   ├── figures/
│   ├── notes/
│   ├── logs/
│   └── export_for_paper/
├── 06_paper_draft/
│   ├── sections/
│   ├── references/
│   ├── tables_inputs/
│   ├── figures_inputs/
│   └── paper.tex
├── 07_submission_package/
│   ├── draft/
│   ├── final/
│   └── archive/
└── 08_project_admin/
    ├── README.md
    ├── changelog.md
    └── reproducibility_checklist.md
```

如需快速建立目录，可运行：

```powershell
$codexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$skillDir = Join-Path $codexHome "skills\spss-academic-workflow"
python (Join-Path $skillDir "scripts\scaffold_spss_academic.py") --project-root "<项目根目录>"
```

在 macOS、Linux 或服务器环境可使用：

```bash
SKILL_DIR="${CODEX_HOME:-$HOME/.codex}/skills/spss-academic-workflow"
python "$SKILL_DIR/scripts/scaffold_spss_academic.py" --project-root "<项目根目录>"
```

原始数据不得删除、覆盖或原地修改。清洗后的数据写入 `02_data_prep/interim/` 或 `02_data_prep/final/`。若中文路径会导致 SPSS 不稳定，可使用英文临时子目录或盘符映射，并优先使用英文变量名进入 SPSS。

## 分析标准

默认分析标准如下：

- 探索性任务：默认做到最低交付，重点是数据概览、描述统计、频数、相关和初步模型建议。
- 验证性任务：默认做到推荐交付，重点是主模型、递进模型、诊断和至少一种合理补充检验。
- 只有在研究问题、变量定义和样本条件充分时，才推进完整交付中的稳健性、异质性、机制或调节分析。

最低交付：

- 描述性统计
- 缺失值和样本筛选说明
- 主模型或核心统计检验
- 中文结果段落
- 一份结果表和复现日志

推荐交付：

- 描述统计表、相关系数表和主回归表
- 多模型递进设定
- 合理的变量转换与说明
- 至少一种稳健性或替代检验

完整交付：

- 数据质量审计、主模型、诊断、稳健性、异质性或机制分析
- 所有结果进入统一结果接口，供论文通过表格片段和结果摘要调用

## SPSS 调用原则

优先使用 SPSS-MCP。若当前 Codex 会话没有直接暴露 `mcp__spss__*` 工具，可在 Python 脚本中调用本机 `spss_mcp.server` 中的同名函数回退执行。

分析阶段至少沉淀以下成果物：

```text
02_data_prep/audit/codebook_<study_slug>.md
02_data_prep/audit/desc_<study_slug>.csv
05_analysis_output/notes/note_01_data_profile.md
05_analysis_output/notes/note_03_baseline_model.md
05_analysis_output/logs/run_03_baseline_model.md
05_analysis_output/tables/table_01_descriptive_statistics.md
05_analysis_output/tables/table_01_descriptive_statistics.tex
05_analysis_output/tables/table_02_correlation_matrix.md
05_analysis_output/tables/table_02_correlation_matrix.tex
05_analysis_output/tables/table_03_baseline_model.md
05_analysis_output/tables/table_03_baseline_model.tex
05_analysis_output/export_for_paper/paper_table_03_baseline_model.tex
06_paper_draft/paper.tex
06_paper_draft/output/paper.pdf
```

命名采用“阶段编号 + 内容说明”的小写 `snake_case` 规则，避免使用 `tab1<ScriptName>`、驼峰命名或依赖脚本名的结果文件名。表格编号应按论文展示顺序稳定排列，而不是按脚本运行顺序临时生成。

## 写作与排版原则

- 写作必须服务于论证，不得把论文写成软件输出说明书。
- 摘要、引言、结果、讨论和结论都必须与实际分析结果一致。
- 所有数字都以 `05_analysis_output/` 中的结果接口或结果表为准，不手工凭记忆改数。
- 普通中文论文默认使用 `ctexart`，除非已有项目另有 `class`。
- 结果表优先通过 `05_analysis_output/export_for_paper/` 接入主稿，不在主稿中手工重做表格。
- `06_paper_draft/tables_inputs/` 和 `06_paper_draft/figures_inputs/` 用于需要本地适配的稿件级输入，不是统计结果的唯一真源。

如需更稳定的主稿或段落骨架，优先复用 `assets/` 中的模板文件。

## 交付与验证

交付前至少检查：

- 清洗脚本可重复运行。
- 最终分析数据存在，样本量与 codebook、结果表一致。
- 主要结果表中的数字来自 SPSS 输出或解析结果。
- 主稿中的 `\input{}` 路径有效。
- PDF 编译成功，或已明确记录失败原因。
- 最终答复说明调用了哪些 SPSS-MCP 工具或回退函数。

## 参考地图

按任务需要读取，不要一次性加载所有内容：

- `references/workflow.md`：项目结构、阶段产物、清理规则和验证门禁
- `references/analysis-routing.md`：显式分析触发、自动分析路由、止损规则和汇报方式
- `references/empirical-design.md`：变量构造、模型选择、诊断、稳健性、异质性和机制分析
- `references/spss-mcp.md`：SPSS-MCP 环境发现、兼容处理、回退调用和结果记录
- `references/tool-matrix.md`：已注册工具、类别、用途和调用可见性
- `references/paper-writing.md`：中文实证论文结构、写作逻辑、结果叙述和修订检查
- `references/latex-layout.md`：普通中文论文的 LaTeX 版式规划、表格接口、编译链和排版 QA

## 最终答复格式

最终答复使用简体中文，简洁说明：

- 已完成哪些阶段
- 关键输出文件在哪里
- 调用了哪些 SPSS-MCP 工具或函数
- 主要实证结论是什么
- 是否成功生成 PDF；若失败，说明原因和可恢复路径
