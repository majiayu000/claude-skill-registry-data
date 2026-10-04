---
name: light-data-engineering
description: 数据处理、数据质量分析与数据集构建。当用户需要清洗数据、处理缺失/异常值、特征工程、数据增强、划分数据集、评估数据质量，或需自建数据集（采集、标注规范、格式、说明文档、隐私合规、发布）时使用。在提 idea 前优先判断现有数据是否足以支撑研究。
---

# 数据处理、质量分析与数据集构建

## 核心原则
**数据先行**：在 m03 提 idea 之前，先回答四问——数据是否足以支撑研究？质量是否可靠？规模是否足够？特征是否有挖掘价值？避免脱离数据基础的空想。**"规模是否足够"可先跑 `scripts/sample_size_check.py` 拿经验预警**（分类每类最小样本/回归样本特征比 EPV/检测每类实例数），它给 ok/warn/insufficient 粗筛——但**不是 power analysis**，主结论样本量仍须正式功效论证。

## 输入 / 触发
- **上游（idea 前，主线）**：用户原始数据 / 现成数据集 / 自建需求 → 出四问结论喂给 m03/m04。
- **回边（实验阶段，来自 m05）**：可接收 research-plan 实验矩阵「派生数据规格」区块的派生数据需求（基础数据集 + 变换类型 + 关键参数 + 划分策略），据此产出对应的**加噪/缺失/跨域/扫参**评测集与 dataset_card，回填 db04 供 ROB/GEN/SEN 实验使用。派生集构建沿用下文「处理流程」「划分」「自建数据集规划」的方法与防泄漏铁律。

## 数据体检（先做）
1. 概览：行列、类型、内存、样例。
   - 中小数据 pandas：读入即定 `dtype`/`parse_dates`，`df.info(memory_usage='deep')` 看真实内存，`df.isna().mean()` 一行得缺失率，`df.describe(include='all')`。object 列转 `category` 省内存。
   - 大数据按场景选引擎：单机想要快+查询优化用 Polars 惰性管线 `pl.scan_csv(...).filter(...).group_by(...).collect()`，超大开 `collect(streaming=True)`；想用 SQL 直查 parquet/csv 且 out-of-core 用 DuckDB（`duckdb.sql("SELECT ... FROM 'data/*.parquet'")`，超内存自动 spill）；想保持 pandas 写法又超内存用 Dask `dd.read_csv("*.csv")...compute()`。（引擎选型矩阵以 a09 tool-selection `decision_matrix.md` 为单一口径；旧推荐的 Vaex 2023 后已停维护、勿新用。）
2. 质量画像：按需各取所长，别只跑一个。
   - ydata-profiling 出整体 EDA 报告：`ProfileReport(df, title=...).to_file("r.html")`；列多/行多务必 `minimal=True`，时序 `tsmode=True`；对比清洗前后/train-test 用 `r1.compare(r2)`。看报告 Alerts（高相关、高基数、常量、缺失）。
   - Deepchecks 跑结构化校验套件：`Dataset(df, label=, cat_features=[...])` 后 `data_integrity().run(ds)`（重复/混合类型/特征-标签泄漏/异常值）、`train_test_validation().run(train_ds, test_ds)`（漂移/新类别/train-test 样本重叠泄漏）。
   - Great Expectations 做可复现质量门禁：`gx.get_context()` → Data Source/Asset/Batch → Expectation Suite（`ExpectColumnValuesToNotBeNull`/`ToBeBetween`/`ToBeInSet`/`ToBeUnique`/`ToMatchRegex`）→ Validation Definition → Checkpoint，产出 Data Docs。注意 GX 1.x 与 0.x API 断层，认版本。
   - 标准化交换/发布元数据用 Frictionless：`frictionless describe` 推断 Table Schema，`frictionless validate datapackage.json` 出 cell/row 级错误报告。
3. 质量结论：给出“可直接用 / 需清洗 / 不足以支撑 / 需补采”的明确判断与理由。

## EDA 与统计分析流程
- EDA 七步：结构概览→缺失分析（missingno matrix/heatmap 看缺失模式）→单变量（数值直方图+箱线、类别频次）→双变量（散点+相关、分组箱线、交叉表/卡方）→多变量（相关热力图、pairplot、PCA）→目标关系（特征 vs 目标，初判预测力与泄漏）→质量小结。EDA 结论只是假设，别用同一份数据既探索又下统计定论。
- 统计检验决策：先查前提——正态性（Shapiro-Wilk，大样本改看 QQ 图，因其过敏感）、方差齐性（Levene）。两组数值正态→t 检验（方差不齐用 Welch）；非正态→Mann-Whitney U；配对→配对 t/Wilcoxon；多组→ANOVA/Kruskal-Wallis；类别关联→卡方/Fisher。必报效应量（Cohen's d、Cramér's V、r/ρ）与置信区间，不只报 p。多检验必校正：FDR(Benjamini-Hochberg) 优先，Bonferroni 更保守。警惕 p-hacking 与 HARKing。

## 处理流程
- 清洗：去重、类型修正、统一编码/单位、文本规范化。
- 缺失值：分机制(MCAR/MAR/MNAR)选策略——删除/均值中位数/模型插补/标记位。
- 异常值：IQR/z-score/孤立森林/业务规则，区分错误 vs 真实极端。
- 特征工程：编码、缩放、构造、选择(过滤/包裹/嵌入)、降维。
- 数据增强：按模态选工具，**先划分再增强、只增训练折**（验证/测试保持原始分布，否则指标虚高）——图像 albumentations（bbox/mask 同步变换）、文本 nlpaug（同义词/上下文/回译，注意别翻转标签语义）、时序 tsaug（TimeWarp/Drift/加噪，注意别破坏因果引入泄漏）、表格 SMOTE 等只在训练折拟合。各模态用法与红线见 references「数据增强」节。
- 划分（scikit-learn）——**命名方法论锚点**(db04 卡 recommended_splits/preprocessing_steps 指针引用，跨数据集单点维护)：`train_test_split(..., stratify=y, random_state=)` 分类必分层；交叉验证按数据性质选——**`SPLIT-01`(time-forward 防未来穿越)** 时序用 `TimeSeriesSplit`、**`SPLIT-02`(按组/患者/牧场/地点分域防泄漏)** 重复个体用 `GroupKFold`/`StratifiedGroupKFold`、一般分类用 `StratifiedKFold`。**`LEAK-01`(只在训练折 fit)**：缩放/插补/编码/特征选择全部放进 `Pipeline`+`ColumnTransformer`，只在训练折 fit，绝不在划分前对全量 fit_transform。记录随机种子。（`safe_split.py` 已对 LEAK-01 做折内 refit 断言。）

## 自建数据集规划
采集方式、标注规范、数据格式、数据说明文档(datasheet)、隐私合规(脱敏/授权/许可)、发布方式(Zenodo/HF/Figshare + DOI + license)。产出 dataset_card（见 db04 字段）。
- **标注规范用模板 [templates/annotation_guide.md](templates/annotation_guide.md)**：类目定义 / 边界案例判定规则 / LLM 辅助标注+人工审核闭环 / 质检抽样率 / IAA 一致性指标。一致性指标**复用 `code_assets/agreement.py`**（Cohen's κ / 二次加权 κ 用于有序评分 / Fleiss' κ ≥3 标注者 / ICC(2,1) 连续值，已对齐 sklearn），不重写；κ<0.6 不达标要回补边界规则重标。
- **LLM 预标注不可直接当真值**：会放大模型偏差，必须人工审核闭环，留痕 `pred_label/human_label/是否修正/仲裁`。

## 找现成数据集（自建前先查）
- OpenML：轻量取数 `fetch_openml(name=, version=, as_frame=True)` 或 `fetch_openml(data_id=)`；完整能力 `openml.datasets.get_dataset(id).get_data(target=)`、`list_datasets(...)`、标准化 `tasks`/`runs` 可复现。锁 version/data_id 保证复现。
- Hugging Face Datasets：`load_dataset(name, split=)`，本地 `load_dataset("csv"/"parquet", data_files=)`，超大 `streaming=True`（IterableDataset）。处理用 `.map(batched=True)`/`.filter`/`.train_test_split`。
- Kaggle：`kaggle.json` 放 `~/.kaggle/`（权限 600），`kaggle datasets list -s 关键词`、`kaggle datasets download -d owner/name --unzip`。需先接受数据集条款，注意各数据集 license。

## 质量评估指标
完整性、一致性、准确性、时效性、唯一性、代表性、偏差(bias_risk)、隐私(privacy_risk)、标注质量。漂移监控用 Evidently 新版 API：`Dataset.from_pandas(df, data_definition=DataDefinition(...))` 包装 current/reference，`Report(metrics=[DataDriftPreset()]).run(current_data=, reference_data=)`，`.save_html()`。漂移按列选检验（KS/PSI/卡方/Wasserstein）；注意 Evidently 近年 API 大改，认版本，且“检出漂移≠有害”需结合业务判断。
- **标注质量有指标更要有检测手段**：用 **cleanlab** 置信学习定位疑似标错样本——交叉验证 out-of-sample 预测概率 → `find_label_issues` 出按可疑度排序清单（用法见 references「cleanlab」节）。pred_probs 必须 out-of-sample，找出候选后**人工裁定 top-K，不全自动删**。cleanlab（定位具体可疑样本）与 IAA（评标注流程整体可靠度，`code_assets/agreement.py`）互补，两者都做。

## 产出
1. 数据质量报告（含四问结论）。**标准工件：`quality_report.md`**（命名见 CONVENTIONS §6.1）。
2. 可复现处理流水线（脚本 + 参数 + 种子，交 a03 落地）。
3. 划分方案与说明。
4. dataset_card（自建时）。**项目级数据卡标准工件：`data_card.md`**（交 m05/a03/m06）。
5. **四问结论卡 `data_feasibility.md`**（交 m03/m04）：把"数据是否足以支撑/质量是否可靠/规模是否足够/特征是否有价值"四问收敛成 ok/warn/insufficient + 依据的轻量落盘工件，**给 m03 判 idea 该不该立项、m04 复核数据声明用**——区别于给做实验用的重工件 data_card/quality_report。由 `scripts/data_feasibility.py` 生成；insufficient 即退出码 1，可当"不进 m03"的闸门。**这是 m02→m03/m04 的标准交接工件，补此前靠聊天传的单向挂载（CONVENTIONS §6.1 双向声明）。**

> 工件落位：用 `scripts/emit_artifacts.py --check` 核三件套（quality_report.md / data_card.md / data_feasibility.md）是否落到 §6.1 标准名，`--register` 打印 passport 登记命令（委托 a01 orchestrator 的 passport.py），保证 orchestrator 台账与 a07 一致性回扫扫得到。

## 衔接
结论喂给 m03/m04；流水线交 a03 实现；数据集登记 db04 与项目库 db09。隐私/许可问题上报 a10。

## 随技能脚本（可直接运行，纯 python + 合成自测，无网络依赖）
所有脚本带 `--selftest`（无需数据，内置合成数据 + 断言验证检测器真的触发）。
- `scripts/data_doctor.py`：CSV → Markdown 数据体检报告（形状/类型/真实内存/缺失/重复/常量列/全空列/高基数/IQR 异常值/强相关/**目标泄漏提示/ID-like 列/inf 无穷值/混合类型列/类不均衡/强偏态/稀有类别**，按 HIGH/MED/LOW 给问题摘要）。**泄漏检测覆盖数值目标（|corr|≥0.98）与分类目标（数值特征 η² 相关比、类别特征条件纯度，纯 numpy/pandas 算单特征近乎可分）；低基数整数目标自动当分类处理；ID-like 列（近乎逐行唯一）单列提示；高基数阈值随行数自适应。**
  - 自测：`python scripts/data_doctor.py --selftest`
  - 用法：`python scripts/data_doctor.py --csv data.csv --target y --out report.md`（`--sample N` 先抽样防大表卡死）。
- `scripts/safe_split.py`：按 `--task clf/reg/timeseries/group` 构建 `Pipeline`+`ColumnTransformer`（数值 median 插补+标准化、类别 most_frequent 插补+OneHot）并自动选 CV——StratifiedKFold/KFold/TimeSeriesSplit/GroupKFold/StratifiedGroupKFold。内置泄漏断言：证明预处理在每折单独 refit（折内 mean ≠ 全量 mean），杜绝划分前 fit_transform。**时序正确性护栏**：timeseries 任务用 `--time-col` 按时间升序重排并校验单调（不给则显式警告，不静默用乱序数据跑出穿越结果）。**group 分类/回归显式声明** `--group-clf`/`--group-reg`（不再靠 `nunique<=20` 猜，避免 20+ 类分类误退化丢分层）。
  - 自测：`python scripts/safe_split.py --selftest`（四种任务全跑 + 时序排序护栏 + 显式 group 判定）。
  - 用法：`python scripts/safe_split.py --csv data.csv --target y --task group --group-col user_id --group-clf`；时序 `--task timeseries --time-col date`。
- `scripts/sample_size_check.py`：数据规模充足性**经验预警**（四问之"规模"）。按经验阈值给 ok/warn/insufficient——分类每类最小样本（50/100 档）、回归样本/特征比 EPV（10/20 档）、检测每类实例数、二分类正例 EPV（Peduzzi 1996）。**明确非 power analysis**，只做"低于经验下限就预警"的粗筛，主结论样本量仍须正式功效论证（statsmodels / code_assets stats_tests power 函数）。阈值可调。
  - 自测：`python scripts/sample_size_check.py --selftest`
  - 用法：`python scripts/sample_size_check.py --task clf --n 1200 --classes 3 --features 20`（`--per-class 960,20,20` 按最小类更严谨）。
- `scripts/quality_gate.py`：拿 YAML 规则校验 CSV，出 PASS/FAIL 报告（dataset: min/max_rows、no_duplicate_rows；columns: dtype/required/non_null/unique/min/max/enum/regex）。纯 pandas+PyYAML，无 GX/Frictionless 硬依赖，退出码 0/1 可直接做 CI 数据门禁。
  - 自测：`python scripts/quality_gate.py --selftest`；规则示例见 `examples/rules.example.yaml`。
  - 用法：`python scripts/quality_gate.py --csv data.csv --rules rules.yaml --out gate.md`。
- `assets/data_card_template.md`：datasheet 模板（字段对齐 db04），含质量评估、偏差/隐私风险、访问分级、推荐划分、溯源核实区。
- `scripts/croissant_export.py`：把数据卡关键字段导出为 **Croissant JSON-LD**（MLCommons 机器可读数据卡标准，HF/Kaggle/OpenML 已采用），发布数据集时附上便于被自动索引——人读 Markdown(data_card) + 机读 JSON-LD(croissant) 双产物。**最小骨架**（name/license/url/citation + 字段字典），完整 distribution 校验和/hash 须用 mlcommons/croissant 官方库补全。`python scripts/croissant_export.py --in card_fields.json --out ds.croissant.json`（缺核心字段会 warn 不臆造）。
- `scripts/check_access_level.py`：数据访问分级守门。每份数据/派生集在数据卡声明 `access_level`（`raw`/`redacted`/`verified_only`），脚本校验它能否流向某下游 sink——raw 数据流向 paper/figure/public-repo 等公开环节会被**阻断**（退出码非零，可当 pipeline 闸门）。三态 pass/blocked/unknown，只按声明判定，真实脱敏是否到位仍需 a10 复核。
  - 自测：`python scripts/check_access_level.py --selftest`
  - 用法：`python scripts/check_access_level.py --level raw --sink paper`，或 `--manifest flows.json` 批量校验流向清单。
- `scripts/data_feasibility.py`：**数据先行四问 → `data_feasibility.md`**（交 m03/m04 的标准工件）。四问各给 ok/warn/insufficient + 依据，整体取最差档(usable/usable_with_caveats/insufficient)。可手填(`--q1 ok:理由`)或吃 `sample_size_check.py --json` 自动填 Q3(`--scale-json`)。insufficient → 退出码 1，可当"不进 m03"闸门。补 m02→m03/m04 的单向挂载。
  - 自测：`python scripts/data_feasibility.py --selftest`
  - 用法：`python scripts/data_feasibility.py --project X --q1 ok:... --q2 warn:... --q3 insufficient:... --q4 ok:... --out data_feasibility.md`。
- `scripts/drift_check.py`：两数据集分布漂移检验(reference vs current)，补 data_doctor 单数据集体检之外的 train/test 同分布 / 上线漂移 / 清洗前后对比。数值列 KS+PSI、类别列卡方+PSI；纯 numpy 实现(p 值渐近近似，无 scipy 硬依赖)。PSI 档 <0.1 稳定/0.1~0.25 轻微/>0.25 显著。**以 PSI 效应量为主、p 为辅**(大样本 p 过敏)，检出漂移≠有害。
  - 自测：`python scripts/drift_check.py --selftest`
  - 用法：`python scripts/drift_check.py --ref train.csv --cur test.csv --out drift.md`。
- `scripts/derive_eval_set.py`：**m05 派生数据回边的可执行实现**。据派生规格 JSON(基础集 + 变换 + 参数)生成鲁棒性/泛化/敏感性评测集 + 对齐 db04 的 dataset_card 字段。变换：noise(加噪)/missing(MCAR缺失)/subset(跨域子集)/scale(扫参)。**铁律：默认只动特征不碰标签(target_safe)、固定 seed 记入卡、仅作评测不回流训练折**。规格示例见 `examples/derive_spec.example.json`，产出 card_fields 可喂 `croissant_export.py` 回填 db04。
  - 自测：`python scripts/derive_eval_set.py --selftest`
  - 用法：`python scripts/derive_eval_set.py --base data.csv --spec derive_spec.json --outdir derived/`。
- `scripts/emit_artifacts.py`：m02 标准工件落位守门——`--check` 核 quality_report.md/data_card.md/data_feasibility.md 是否落到 §6.1 标准名，`--register` 打印委托 orchestrator passport.py 的登记命令(artifacts 路径是 a07 回扫权威清单)。纯标准库。
  - 自测：`python scripts/emit_artifacts.py --selftest`
  - 用法：`python scripts/emit_artifacts.py --check --dir .`。
- 统计检验/效应量/多重校正请复用仓库根的 `code_assets/stats_tests.py`（相对本技能为 `../../code_assets/`，含 welch_t、benjamini_hochberg、wilson_ci 等），标注一致性复用 `agreement.py`，长尾重采样复用 `longtail_resample.py`，不要重造。

---
工具的真实端点/API/参数与已知坑详见 `references.md`（逐工具核查笔记）。
