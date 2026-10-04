---
name: aisbench-dataset-compression-herding
description: |
  当用户直接要求进行数据集压缩测评，或在量化调优过程中需要使用 AISBench 评测工具输出数据集精度等场景时使用。
  本 Skill 负责：使用 AISBench 数据集压缩代码、用 RBF Kernel Herding 算法生成压缩后的数据子集（coreset），并按用户目标交付两种产物之一：
  ① 接入量化调优主流程：产出独立的 coreset 数据集配置（不覆盖原始数据），回传「全集 config_name + coreset config_name」给编排层，供 evaluation.yaml 切换；
  ② 仅数据集压缩测评（不做量化调优）：基于 example 模板生成「全集测试脚本」和「子集测试脚本」两份 shell 脚本。
  暂时支持 AIME 2025 和 GPQA，其他数据集需要再结合 aisbench tools目录下 herding_coreset_selector 源码进行分析。
---

# AISBench 数据集压缩

适用于以下场景：用户直接要求进行数据集压缩测评，或在量化调优过程中需要使用 AISBench 评测工具输出数据集精度。当用户提出"数据集压缩""评测集压缩""生成 coreset""压缩后的评测集"等需求时，优先使用本 Skill。

AISBench 参考链接：<https://github.com/AISBench/benchmark>

使用现有 herding 算法，根据模型 hidden state 和 RBF Kernel Herding 从评测数据集中选择子集。暂时支持：

- `aime2025`
- `gpqa`

其他数据集需要结合 aisbench 源码进行分析。不要复制或修改 herding 算法，也不要把此 Skill 用于尚未支持的数据集。

## 整体流程

```text
环境检查（路径 / 安装 / 压缩代码可用）
    │
    ▼
测评准备（vllm_api_general_chat 服务拉起方式）
    │
    ▼
压缩准备
    ├── 第 1 步 询问是否自备已压缩数据集（是 → 直接跳第 4 步）
    ├── 第 2 步 压缩耗时与风险提示（约 30 分钟）
    ├── 第 3 步 执行压缩（用户提供原始数据集 + 本地模型 → 生成压缩集合路径）
    └── 第 4 步 交付压缩结果（场景 A 生成测试脚本 / 场景 B 产出 coreset 配置与 config_name）
```

---

## 一、环境检查部分

### 步骤 1：确认 AISBench 代码路径

1. 优先使用用户提供的 AISBench 代码路径。
2. 用户未提供时，**必须与用户确认是否下载 AISBench 代码**，未经确认不得自动下载。

### 步骤 2：确认 AISBench 是否已安装

先确认当前环境是否已安装 `aisbench`，例如在对应 Python 环境中执行 `pip list` 查找包：

```shell
pip list
```

- 若 `pip list` 中已包含 `aisbench`：进入步骤 3。
- 若 `pip list` 中不包含 `aisbench`：**要求用户先安装 AISBench**，可参考官方安装文档 <https://yh-ais-bench-benchmark.readthedocs.io/zh-cn/latest/get_started/install.html>，并参考使用如下命令安装。安装前必须先征得用户确认，不自动安装：

```shell
git clone https://github.com/AISBench/benchmark.git
cd benchmark/
pip3 install -e ./ --use-pep517
```

安装完成后返回步骤 2 重新检查；确认已安装后再进入步骤 3。

### 步骤 3：确认压缩代码可用

数据集压缩代码应位于 AISBench 工程的 `tools/herding_coreset_selector` 目录下：

```text
<aisbench-code-path>/tools/herding_coreset_selector/
```

- 若该目录存在并包含 `herding/` 包（含 `herding/eval_datasets/` 适配器等结构，可通过 `python -m herding` 调用）：进入「二、测评准备部分」。
- 若该目录不存在或结构不完整：**明确提示用户该功能暂未支持**，并建议用户改用已压缩的数据集；若用户无可用压缩数据集，则退回到按照数据集全集进行测试。

---

## 二、测评准备部分

测评默认使用 AISBench 的 `vllm_api_general_chat` 模型包装文件（对应 example 脚本中的 `--models vllm_api_general_chat`）。

按以下规则处理服务拉起方式：

1. **用户提供了服务拉起脚本**：Agent 自动将拉起方式修改/写入 `vllm_api_general_chat` 文件，使测评命令按用户提供的拉起方式启动服务。其余字段（`stream=False`、`max_out_len=512`、`temperature=0.01`、`retry=2`）保持默认，与 GPQA 选择题评测场景匹配——**此处需要提示用户自行更改**这些字段，Agent 不得替用户决定。
2. **用户未提供服务拉起脚本**：Agent 根据 `vllm_api_general_chat` 文件所需的字段，对缺失的字段逐一询问用户，待用户补齐后再写入/修改 `vllm_api_general_chat` 文件。

---

## 三、压缩准备部分

### 第 1 步：询问用户是否自备已压缩数据集

优先询问用户是否自己提供已压缩的数据集。

- **用户自备已压缩数据集**：直接跳过第 2、3 步，进入第 4 步生成测试脚本。
- **用户不自备**：继续第 2 步。

### 第 2 步：压缩耗时与风险提示（必做）

在用户正式使用本地压缩前，必须先提示成本与风险，由用户自行决定，不得替用户做决定：

- 现有实现压缩时间可能在 **约 30 分钟**（AIME/GPQA）。
- 当前版本大量使用 CPU 上的 numpy 算法，存在性能瓶颈，后续版本预计会优化。
- **优先建议用户自己提供已压缩的数据集**，可显著节省等待时间。

用户确认后，才继续第 3 步。

### 第 3 步：执行压缩

执行压缩前需要用户提供：

1. **原始数据集**（对应 `--dataset-path`，AIME 为 jsonl，GPQA 为 csv）。
2. **本地模型**（对应 `--model-path`，用于提取 hidden state，如 Qwen 系列模型）。

Agent 据此通过 `python -m herding` 的显式命令行参数执行压缩，生成最终的压缩集合路径（见「四、压缩执行细节」中的输出结构）。

### 第 4 步：交付压缩结果（两种用途，二选一）

压缩完成后（或用户自备压缩数据集后），**先向用户确认压缩结果的用途**，据此选择一种交付方式，不要同时产出两种：

- **场景 A：仅数据集压缩测评（不接入量化调优）** → 生成两份测试脚本（见下方「场景 A」）。
- **场景 B：接入量化调优主流程** → 产出可被 evaluation.yaml 引用的 coreset 数据集配置与 config_name（见「四、产出 coreset 数据集配置（场景 B）」）。

#### 场景 A：生成测试脚本

适用于用户只想用 AISBench 分别评测全集与子集精度、**不做量化调优**的情况。参考本 Skill 的 example 模板进行替换，给用户生成**两份**最终测试脚本。注意：example 模板以 GPQA 数据集为例，需根据实际数据集和评测场景进行修改：

1. **全集测试脚本**：数据集路径指向原始数据集目录。
2. **子集测试脚本**：数据集路径指向压缩后的 coreset 数据集目录。

模板位于 `example/` 目录：

```text
example/run_gpqa_fullset.sh   ← 全集测试脚本模板（path 指向原始 gpqa 全集）
example/run_gpqa_subset.sh    ← 子集测试脚本模板（path 指向压缩子集）
```

> **注意**：example 中的两个脚本以 GPQA 数据集为例，仅作参考模板。若目标数据集为 AIME（aime2025），需自行将脚本中的数据集名、数据文件（`gpqa_diamond.csv` → `aime2025.jsonl`）、配置文件路径（`gpqa_gen_*` / `gpqa_ppl_*` → AIME 对应配置）以及 `--datasets` 参数替换为 AIME 对应内容，不能直接照搬 GPQA 配置。

生成时按实际环境替换模板中的关键变量：

| 模板变量 | 替换为 |
|---------|--------|
| `BASE_DIR` | ais_bench 源码根目录（配置文件所在目录） |
| `TARGET_PATH` | 全集脚本用原始数据集绝对路径；子集脚本用 coreset 数据集绝对路径 |
| `WORK_DIR` | 本次 `--work-dir` 输出目录 |
| `FILES` 中的配置路径 | 目标数据集实际涉及的配置文件路径 |

执行 `ais_bench` 命令时使用 `--num-warmups 0` 跳过 warmup（预热）阶段，直接进入推理（AISBench 默认 `1`，设为 `0` 不预热）。

执行全集或子集测试脚本**之前**，推荐先用 `curl` 访问服务端口（如 `curl http://127.0.0.1:<port>/health` 或发起一个简单对话请求）进行健康检查：若服务端回复正常，再执行测评脚本；若回复异常，先排查服务拉起情况，不要盲目执行测评脚本。

生成后向用户回显两份脚本路径，并确认脚本内的数据集路径与全集/子集一致。


---

## 四、压缩执行细节

### 执行入口

现有 herding 实现位于 AISBench 工程的 `tools/herding_coreset_selector` 目录。**执行前必须 `cd` 到该目录**，然后通过 `python -m herding` 的显式命令行参数执行。工具运行时配置全部通过命令行传入，不依赖环境变量，也不使用本 Skill 自带脚本。

### 模型要求（重要）

数据集压缩需要加载一个本地 LLM 来计算样本的 hidden state 特征，**必须提供一个可被 Transformers 加载的本地模型目录**（通过 `--model-path` 指定），压缩过程不会自动下载模型。

- **推荐参考模型**为 `Qwen3-4B-Instruct-2507`，但**不限于此模型**——任何可被 Transformers 加载的本地模型都可作为 `--model-path` 使用。推荐使用 Qwen3 / Qwen2.5 系列的小模型，**模型参数量最好不超过 7B**，以避免特征提取阶段占用过多显存/内存资源。
- **若用户已提供某个本地模型路径**：直接使用该模型。
- **若用户没有可用本地模型**：必须提示用户需要先单独下载一个模型（例如优先下载推荐的 `Qwen3-4B-Instruct-2507`），准备好本地模型目录后再继续。不得在不告知用户的情况下直接拉取或拼接在线模型路径。
- **提醒事项**：不同模型的分词器/权重特征不同，会导致选出的 coreset 不同，需向用户说明这一点。

### 必须确认的参数（命令行参数）

缺少以下参数时先向用户询问，不要猜测：

- `--eval-dataset`：数据集适配器名称，当前为 `aime2025` 或 `gpqa`（必选）。
- `--dataset-path`：包含当前数据集文件的具体目录（AIME 为 jsonl，GPQA 为 csv）（必选）。
- `--model-path`：可被 Transformers 加载的本地模型目录（必选）。若用户未提供且本地不存在该模型，则按上文「模型要求」先提示下载。
- `--coreset-ratio`：保留比例，例如 `0.1` 表示保留约 10%，不是删除 10%。范围 `(0, 1]`，默认 `0.2`（可选）。
- `--output-dir`：结果输出根目录，默认 `./datasets`（可选）。

Coreset 方法固定为 RBF Kernel Herding，输出目录中的 `herding` 为固定标识，不通过参数切换算法。

### 输入数据

由 `--dataset-path` 指定数据集目录。数据文件约定如下：

```text
<dataset-path>/aime2025.jsonl
<dataset-path>/gpqa_diamond.csv
```

AIME 文件必须是 JSONL。GPQA CSV 必须包含 `question`、`A`、`B`、`C`、`D` 列。

### 执行命令示例

采用命令行参数 + `python -m herding` 的标准流程。

#### 第一步：搭建环境

```shell
pip install numpy torch transformers tqdm
cd <aisbench-code-path>
pip install -e .
```

> AISBench 在这里主要用于提供数据集和 Prompt 相关组件；执行 Coreset 时不会启动 AISBench 模型评测流程。

#### 第二步：运行压缩（示例为 GPQA）

```shell
cd <aisbench-code-path>/tools/herding_coreset_selector

python -m herding \
  --eval-dataset gpqa \
  --dataset-path <aisbench-code-path>/ais_bench/datasets/gpqa \
  --model-path /path/to/Qwen2.5-7B-Instruct \
  --coreset-ratio 0.2
```

AIME 时改为 `--eval-dataset aime2025`，并指定 AIME 数据目录。

如目标输出已经存在，请先与用户确认是否覆盖；只有用户明确要求覆盖时才进行处理，不要默认覆盖现有结果。

### 输出

输出默认位于 `<output-dir>/`（未指定时为 `tools/herding_coreset_selector/datasets/`）下，结构为：

```text
<output-dir>/<eval-dataset>/herding/<model-name>/
├── origin/
│   ├── <dataset_file>
│   └── indices.json
└── coreset/
    ├── <dataset_file>
    └── indices.json
```

其中 `<eval-dataset>` 为 `--eval-dataset` 的取值，`<model-name>` 自动取自 `--model-path` 的最后一级目录名，`herding` 为固定方法目录。

每个目录包含：

- AIME：`aime2025.jsonl` 和 `indices.json`
- GPQA：`gpqa_diamond.csv` 和 `indices.json`

`origin` 保存本批筛选对应的完整数据集，`coreset` 保存选择后的子集（即最终的压缩集合路径）。`indices.json` 记录样本在完整数据中的原始索引，便于复现与追溯。实际需要保留的压缩数据位于 `coreset/<dataset_file>`。

### 保存压缩结果到 AISBench

推荐不在 AISBench 数据目录覆盖原始数据，而是在 `ais_bench/datasets/` 下为 Coreset 单独建立 `_coreset` 目录，与原始数据集并存：

```text
<aisbench-code-path>/ais_bench/datasets/
├── <dataset_name>/
│   └── <original_dataset_file>
└── <dataset_name>_coreset/
    ├── <dataset_file>
    └── indices.json
```

例如 GPQA（模型目录名为 `Qwen2.5-7B-Instruct`）：

```shell
mkdir -p <aisbench-code-path>/ais_bench/datasets/gpqa_coreset
cp <aisbench-code-path>/tools/herding_coreset_selector/datasets/gpqa/herding/Qwen2.5-7B-Instruct/coreset/gpqa_diamond.csv <aisbench-code-path>/ais_bench/datasets/gpqa_coreset/
cp <aisbench-code-path>/tools/herding_coreset_selector/datasets/gpqa/herding/Qwen2.5-7B-Instruct/coreset/indices.json <aisbench-code-path>/ais_bench/datasets/gpqa_coreset/
```

这样原始数据和压缩后的 Coreset 分别保存，互不覆盖。

- 场景 A（仅压缩测评）：第 4 步生成的「子集测试脚本」应指向该 `_coreset` 目录，「全集测试脚本」指向原始 `<dataset_name>/` 目录。
- 场景 B（接入量化调优）：见下方小节，产出 coreset 数据集配置与 config_name。

### 产出 coreset 数据集配置（场景 B：接入量化调优主流程）

当压缩结果用于量化调优的快速迭代时，交付物不是 shell 脚本，而是**一套可被 evaluation.yaml 直接引用的 coreset 数据集配置**。编排层（`quantization-accuracy-tuning-orchestrator`）通过切换 evaluation.yaml 中 `datasets.<key>.config_name` 在「全集 / coreset」之间切换，全程复用 msmodelslim 内建评测服务（`run_evaluation.py` → `ServiceOrientedEvaluateService`），不新增任何服务拉起脚本。

#### 步骤

1. **保存 coreset 数据到独立目录**：按上文「保存压缩结果到 AISBench」，把 `coreset/<dataset_file>` 与 `indices.json` 复制到 `ais_bench/datasets/<dataset>_coreset/`，不覆盖原数据。

2. **新建独立 dataset 配置（不修改原配置）**：在 `benchmark/configs/datasets/<dataset>/` 下复制原数据集对应的 `.py` 配置，仅把 `path='...'` 改为 coreset 目录，其余字段（mode、prompt、metric 等）保持与原配置一致；配置名（config_name）默认约定为 `<原 config_name>_coreset`（如 `gpqa_gen_0_shot_str` → `gpqa_gen_0_shot_str_coreset`），实际以新建配置文件的注册名称为准。

3. **回传两套 config_name 给编排层**：
   - 全集 config_name：原数据集配置名（最终全量验收用）；
   - coreset config_name：新建配置名（调优迭代快速反馈用）。

4. **切换规则（由编排层执行，本 Skill 只回传 config_name）**：
   - 迭代期：evaluation.yaml 中对应 `datasets.<key>.config_name` 用 coreset config_name；
   - 最终全集验收：切回全集 config_name；
   - accuracy 缓存自动隔离：编排层精度缓存键为 `md5(evaluation_config) + md5(quant_config)`，而 `evaluation_config` 含 `config_name`，全集与 coreset 自然形成不同缓存键，无需额外处理。

#### 注意

- **不改 msmodelslim 评测层**：`run_evaluation.py` / `ServiceOrientedEvaluateService` 只认 `config_name`，不认数据路径；切子集只能在 ais_bench 数据集配置层做，不要尝试改评测脚本。
- **达标口径由编排层负责**：本 Skill 只回传「全集 config_name + coreset config_name」两套配置，供编排层切换。编排层 `quantization_tuning.md` 采用「**子集调优 → 全集验证 → 不通过改全集调优**」的闭环：子集出口标准与全集出口标准是**两个**独立标准（先询问用户，不给出的一方由当前环境跑浮点模型测 FP 基线，且浮点基线评测会额外占用卡数）；子集达标只代表可进入全集验证，全集不达标时**直接切全集重跑调优**，保证与全集一致（不再采用固定步长逐步收紧子集出口标准的做法）。本 Skill 仅提供 config_name，不参与达标/调优决策。

---

## 五、接入新的数据集

如果需要处理新的数据格式，可在 `herding/eval_datasets/` 中增加数据集适配器。适配器继承 `EvalDatasetBase` 并实现 `dataset_size()`、`dataset_prompts()`、`save_data_by_indices()`，并使用 `reg_eval_dataset("名称")` 注册，同时在 `herding/eval_datasets/__init__.py` 中导入对应模块。之后即可通过 `--eval-dataset <新名称>` 加载。建议 `save_data_by_indices()` 保持原始数据格式不变，以便压缩结果可直接保存到 AISBench 对应数据目录。

**注意**：接入新数据集前仍应坚持本 Skill 的边界，未经要求不要把压缩扩展到超出当前已支持的数据集范围；其他数据集需要结合 aisbench 源码进行分析。

---

## 约束

- 删除文件或目录时**永远不要使用 `rm -rf`**，一律使用 `rm -r`，并且在删除前必须先征求用户确认。
- 不自动下载数据集或模型。
- 不自动下载 AISBench 代码；用户未提供 AISBench 代码路径时，必须先征得用户确认才能下载。
- 不自动安装依赖。
- 不修改原始数据集、AISBench 源码或 herding 源码。
- 不接受任意 shell 命令参数。
- 依赖缺失、输入文件不存在、比例无效或数据集不受支持时，应直接报告错误。
- 输出目录中的模型名来自 `--model-path` 的最后一级目录名，不能自定义为其他路径标签。