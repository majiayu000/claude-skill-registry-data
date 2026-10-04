---
name: light-project-structure
description: 规范整洁的项目文件夹整理。当任务涉及新建项目、整理已有项目结构、规整文件命名与版本时使用。规划 data、src、models、results、figures、docs、paper、ppt、patent、software-copyright、experiments、logs、configs、references、assets、notebooks 等目录，保证结构清晰、命名规范、版本可追踪，便于写论文、答辩、申请软著专利与复现实验。
user-invocable: false
---

# 项目文件夹规范整理

## 标准科研项目骨架
```
project-name/
├── data/            原始/中间/处理后数据（大文件走 DVC）
│   ├── raw/ interim/ processed/ external/
├── src/             源代码
├── models/          模型权重与定义
├── results/         实验结果（指标、输出文件）
├── figures/         论文/报告用图
├── docs/            项目文档
├── paper/           论文（LaTeX/Word 工程）
├── ppt/             演示文稿
├── patent/          专利材料
├── software-copyright/  软著材料
├── experiments/     实验脚本与配置（按实验编号）
├── logs/            运行日志（MLflow/W&B 本地）
├── configs/         配置（Hydra yaml）
├── references/      文献库（Zotero 导出/.bib）
├── assets/          图标/模板/素材
├── notebooks/       探索性分析
├── .light/          编排台账 passport.yaml + handoff/ 会话衔接卡（纳入版本控制）
├── README.md  CHANGELOG.md  .gitignore  pyproject.toml
```

数据分层沿用 Cookiecutter Data Science：`raw/`(原始不可变) `interim/`(中间) `processed/`(建模用最终) `external/`(第三方源)。notebooks 用"编号-缩写-描述"命名（如 `1.0-jl-eda.ipynb`）。

## 数据流即 DAG（核心方法）

把整个项目想成一张**有向无环图**：节点是数据/产物，边是确定性变换脚本。沿三条铁律组织目录：

1. **raw 不可变（immutable）**：`data/raw/` 一旦落地永不就地修改、永不被脚本写回。任何清洗/转换都读 raw、写 `interim/` 或 `processed/`。这样原始事实始终可回溯，DAG 有可信源头。
2. **每个产物都能从上游重算**：`processed/`、`models/`、`results/`、`figures/` 都是 DAG 的下游节点，删掉也能由"上游数据 + 代码 + params"重新生成——因此它们进 `.gitignore`/DVC，不进 Git 文本库。能重算的不入库，是 DAG 思路的直接推论。
3. **notebooks 拆探索 vs 报告**：`notebooks/exploratory/`（草稿、可乱、编号命名 `1.0-jl-eda.ipynb`）与 `notebooks/reports/`（干净、可重跑、产出对外图表）分流。探索性 notebook 不进 DAG 关键路径；定稿逻辑要下沉到 `src/`，被 notebook 和管线共同 import，避免"逻辑只活在某个 cell 里"。

用 `dvc.yaml` 把这张 DAG 显式声明出来（stage 的 `deps`→`outs` 就是图的边），`dvc repro` 据此只重跑受影响的下游节点；`dvc dag` 可打印依赖图。

## 命名规范
- 目录/文件用小写+连字符或下划线，不用空格中文。
- 实验/版本带日期或序号：`exp_004_ablation`, `paper_v3`, `fig3_ablation_v2`。
- 数据文件含版本/划分标记；结果文件名映射到实验编号，可追溯。

## 整理动作
1. 盘点已有项目（借 repo-intake-and-plan 思路）：先读 README→扫 setup 脚本与文档化命令→把工作流归类为 推理/训练/评估，再据此给散落文件归位。
2. 新项目骨架：**首选 `scripts/scaffold.py`**——一条命令建全树 + 拷模板 + 可选 `--dvc/--uv|--poetry`：
   `python scripts/scaffold.py ./my-proj --name my-proj --dvc`（生成 data 四分层 + notebooks 探索/报告分流 + src 包 + `.light/`（passport 台账 + handoff/ 衔接卡目录，纳入版本控制）+ 落地 7 模板 + pyproject.toml；目标非空需 `--force`）。pyproject 默认 **uv 后端**（与 a03 推荐一致），加 `--poetry` 切 Poetry 备选。或用 CCDS（`pipx install cookiecutter-data-science` 后 `ccds`）；或按上面骨架手工生成。无论哪种，都要落 README/CHANGELOG/PROJECT_PLAN/.gitignore/.editorconfig/pyproject.toml。
3. 重命名规范化→补 README/CHANGELOG→产出"文件归位说明"（借 handoff 结构：Key Decisions 表 + 失败尝试 + 警告）。

## 版本与依赖
- Git 管文本，DVC 管大文件：`dvc init`→`dvc add data/x.csv`(生成 `.dvc` 小文件并自动写 .gitignore)→`git add *.dvc .gitignore`→`dvc remote add -d storage s3://...`→`dvc push`。拉取：`git pull && dvc pull`。`.dvc`/`dvc.yaml`/`dvc.lock`/`.dvc/config` 入 Git，数据本体进 DVC。
- 多阶段管线用 `dvc.yaml`(stage 字段：`cmd` 必填、`deps`、`params`、`outs`、`metrics`、`plots`)，`dvc repro` 只重跑变更阶段（`frozen:true` 阶段跳过）；实验用 `dvc exp run/show/diff`。
- 依赖锁定**默认 uv**（与 a03 backend-coding 一致，快且 lock 跨平台）：`uv init`→`uv add`→`uv sync`(按 `uv.lock` 精确装)；dev/test 依赖 `uv add --dev` 进 `[dependency-groups]`；应用项目提交 `uv.lock`。**备选 Poetry**：`poetry init`→`poetry add`→`poetry install`，dev/test 放 `[tool.poetry.group.dev.dependencies]`，提交 `poetry.lock`。scaffold 默认出 uv 版 pyproject，`--poetry` 切备选。

## 质量门（配置要点）
四件套——Ruff（替代 flake8+black+isort）、pre-commit（rev 钉死 tag、接 ruff-pre-commit）、EditorConfig（root=true 统一缩进/换行）、.gitignore（GitHub Python 模板 + 科研条目）——的配置已落进 `templates/` 对应模板，逐项 `[tool.*]` 键与命令见 `references.md`；质量门口径与 a03 backend-coding 一致（a03 为代码侧单一真相源）。任务运行器二选一：make 已有则 Makefile；要跨平台+可读用 Taskfile（checksum 跳过、`task -l`）。

## 与项目库对应
目录结构与 db09 project_card 的各 status 字段一一对应（paper_status↔paper/，code_status↔src/，data_status↔data/…），便于 a02 跟踪进度。

## 现成模板（本技能目录 `templates/`，可直接复制使用）
- `scripts/scaffold.py` — **一条命令生成全套骨架**：建目录树 + 拷 7 模板到项目根（去 `.template` 后缀）+ 写 `src/<module>/__init__.py` + 始终落 `pyproject.toml`（默认 **uv** 后端，`--poetry` 切备选，均带 Ruff）；`--dvc` 加写 `dvc.yaml`，`--force` 覆盖非空。已实测两路径 selftest 通过。
- 7 份模板：`PROJECT_STRUCTURE.md`（目录规范+命名+db09 对应）、`README.template.md`、`PROJECT_PLAN.template.md`（可勾选任务+No-Placeholders）、`CHANGELOG.template.md`（Keep a Changelog+SemVer）、`python-research.gitignore`（基线取 GitHub 官方 Python.gitignore，HTTP 200@2026-06-06，补科研条目）、`editorconfig.template`、`pre-commit-config.template.yaml`（rev 钉死 tag，`pre-commit autoupdate --freeze` 维护，仅 git 仓库内 `pre-commit install` 后生效）。各模板用途与配置项细节见 `references.md`。

新建项目时优先 `python scripts/scaffold.py <dir> [--poetry --dvc]` 一步到位；或手工把上述文件复制到项目根（gitignore/editorconfig 去掉模板后缀），填充 README/CHANGELOG/PROJECT_PLAN 中的 `{{占位符}}` 即可。

## 产出
规整后的目录树 + 上面 `templates/` 的 README/CHANGELOG/.gitignore/.editorconfig 落地文件 + 一份"文件归位说明"。

## 衔接
为 m05/a03/a04 提供落地结构；为 m15(软著专利)、m07(论文)、m16(PPT) 预留对应目录；状态同步 a02/db09。
整理任务量大时按"可独立完成+带验收标准+标依赖顺序"拆解（借 to-issues 的垂直切片思路：每个任务是一条端到端可独立认领的路径，而非横向按层切）；复杂整理先出"精确路径+具体动作+验证步骤"的计划再执行，写到无上下文者也能照做的程度（借 writing-plans，任务粒度 2–5 分钟）。复现/审计场景固定 `repro_outputs/` 归档每次跑的结果，落 verified/partial/blocked 三态标记 + 输出 + `PATCHES.md`（改了哪些文件）+ 假设与阻塞清单（借 minimal-run-and-audit）。

> 工具与方法的可核查细节（真实命令/配置/端点/链接）见同目录 `references.md`；现成可复制模板见同目录 `templates/`。
