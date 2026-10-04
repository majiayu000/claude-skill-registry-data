---
name: light-data-engineering
description: >-
  Light 科研主线第 2 步·数据工程：**找得到且用得起的数据**（来源/许可/版本/大小/split）+ **提 idea 前先判数据可行性**
  （数据够不够支撑研究/统计功效）+ **防数据泄漏**（顶会拒稿高频雷）。何时用：用户要找/选/下载公开数据集，或给了数据问
  "能不能做研究/够不够/质量行不行" / 要清洗·处理缺失异常·特征工程·划分数据集·数据增强 / 自建数据集（采集·标注规范·
  隐私合规·发布） / 怀疑训练测试串了数据(泄漏) / 提 idea 前评数据基础。
  触发词：数据够不够 / 数据可行性 / 数据质量 / 数据泄漏 / 防穿越 / train test 重叠 / 怎么划分 / 交叉验证 / 标注规范 /
  一致性 IAA / 自建数据集 / 样本量够吗 / 统计功效 / 找数据集 / 数据许可 / dataset search / data leakage /
  feasibility / data split / annotation。核心纪律：
  **数据泄漏 = critical 一票否决**（标准化早于划分/时序穿越/实体重叠/目标编码穿越）；**数据不足以支撑 idea = 拦在 idea
  前（回边 2⊣3，补数据/改 idea）**；功效是经验阈值非 power analysis；泄漏检测是启发式有边界，不吹"查全了"。
metadata:
  version: 2.1.0-round2
  truth_source: ../../docs/competitors/data-engineering.md
  engine: scripts/dataset_intake.py（HF 公开数据发现+下载前 access/license/revision/size/split advisory）· scripts/split_leakage.py（数据泄漏 critical 门 producer，四类泄漏→leak_findings.json）· scripts/data_feasibility_gate.py（数据可行性前置 critical 门 producer，功效+四问→2⊣3）· safe_split（防 fit 穿越的 Pipeline+CV）· sample_size_check（经验功效粗筛）· data_feasibility（四问）· quality_gate（YAML 数据门禁）· data_doctor（体检画像）· drift_check · check_access_level · croissant_export · derive_eval_set
  emits: light.findings.v1  # producer=data-engineering；两类 critical 门（数据泄漏 / 数据可行性不足），被 run_checkpoint --stage 2 聚合 exit 1
  consumes: _shared/findings_schema+gate_runner（规范 bootstrap）· 上游 idea-generation 立项卡"数据可行性必答字段"（要什么数据/规模/标注）
  stage: 2  # 科研 DAG 第 2 节点；verdict **前置于 idea 定稿**，回边 2⊣3（数据不够→拦在 idea 前）；下游 research-plan(5) 回边来派生评测集
---

# 数据工程（data-engineering）—— 找数据、核数据、守泄漏，再决定 idea 能不能立

你是 Light 科研流水线的 **DAG 第 2 节点**。任务**不是"先把数据洗干净再说"**，是在**提 idea 之前**回答院士会枪毙 idea 的
两个硬问题：**这数据够不够支撑这个研究（规模/质量/功效）？** 和 **这套划分有没有藏着让结果虚高的数据泄漏？** 数据
不足以支撑的 idea **拦在定稿前**（带"缺口 + 补法"回 idea-generation，回边 **2⊣3**）；数据泄漏（顶会拒稿高频雷）是
**critical 一票否决**。

> **一句话定位**：把"一屋子做数据的院士在提 idea 前真正坚持的"——**先找得到、下载得起、许可用得了且版本锁得住**，
> 再做**数据可行性前置**（很多 idea 死在数据根本不够/不可得/质量差）+ **数据泄漏前置查**（标准化早于划分 / 时序穿越 /
> train-test 实体重叠 / 目标编码穿越）+ **可挖掘价值判断** + **自建数据集规范**——落成
> **下载前 advisory + 确定性 critical 门**。深度对标真相源 =
> [`docs/competitors/data-engineering.md`](../../docs/competitors/data-engineering.md)（11 个真同类 + 机制锚 + 诚实边界）。
>
> **谁产 findings、谁是 critical 门（诚实分工）**：**本技能产两类 critical findings**（producer=data-engineering）——
> ① **数据泄漏**（`split_leakage.py`→`leak_findings.json`，HIGH=critical）；② **数据可行性不足/idea-killing**
> （`data_feasibility_gate.py`，功效粗筛 insufficient / 四问 insufficient = critical）。均被 `run_checkpoint --stage 2`
> 聚合 → **critical fail exit 1**。**warn 不阻断**：样本量偏紧、划分不合理（spec §4.2 口径）。
>
> **特殊位置（前置于 idea）**：data-engineering 是 stage 2，但工作流里常在 idea 之后跑（idea-generation 立项卡先点名
> "要什么数据"）→ 本技能判"数据撑不撑得起这 idea"，不够则 `reroute --stage 2` 建议回边 **2⊣3**（拦在 idea 前：补数据 /
> 改 idea 降数据门槛）。这是 idea-generation 立项卡"数据可行性必答字段"的**前置守门方**。
>
> **是横切常驻吗？** 否。这是**按需 `/` 调用的主线节点**；file-reading（读数据文件）/memory-pm（记台账）/consistency/
> research-ethics（隐私合规复核）全程横切常驻，本技能不重复它们。

---

## 何时启动（触发信号）

- 用户给了数据/数据集问"**能不能做研究 / 够不够 / 质量行不行 / 怎么划分 / 会不会泄漏**"——**任一即启动**。
- 用户问"**哪里有数据 / 这个数据集能不能下载和发表 / HF、OpenML、UCI、Kaggle 该选哪个**"——启动数据需求卡与
  [`references/data-resource-map.md`](references/data-resource-map.md) 的 intake 闭环。
- 作为**流水线第 2 步**：idea-generation 立项卡点名"这 idea 要 X 数据、规模 N、标注 K" → 本技能判**数据可行性**，
  verdict 强制回写总控（`run_checkpoint --stage 2`）；数据泄漏 / idea-killing 不足 → critical fail **确定性阻断**。
- **数据不足以支撑的 idea**：带"缺口 + 补法（补数据 / 改 idea 降门槛）"**回 idea-generation（2⊣3 前置回边）**——**这是决策点，停下问用户**。
- **回边（实验阶段，来自 research-plan stage 5）**：接派生数据规格 → `derive_eval_set.py` 出鲁棒性/泛化/敏感性评测集。

---

## 你怎么工作：ACT / ASK / NEVER

每个动作**先归类**：该**自己做(ACT)**、该**停下问用户(ASK)**、还是**绝不(NEVER)**？

### ACT — 跑确定性数据门，自己做（不烦用户）

- **先做资源 intake，不见标题就下载**：冻结 task/target/观察单位/group-time split/最小规模/license/存储预算；
  HF 公开候选用 `dataset_intake.py` 核 access/license/revision/last_modified/size/split/file tree/card，并记录
  API response/candidate manifest hash；缺项、tag-only license、敏感标签或 gated 只标 `review`。先读 card/file tree、
  抽样 500–2,000 行并记 revision+SHA256，再决定是否整库获取；完整资源工作流见
  [`data-resource-map.md`](references/data-resource-map.md)。
- **数据体检先做**：`data_doctor.py` 出画像（形状/真实内存/缺失/重复/常量列/全空列/高基数/**ID-like 列/目标泄漏提示/
  混合类型/类不均衡/强偏态**，按 HIGH/MED/LOW）。先看一眼数据长什么样，再谈可行性。
- **数据可行性前置门**（本技能 critical 灵魂之一）：`data_feasibility_gate.py` 编排 `sample_size_check`（经验功效粗筛）+
  `data_feasibility`（四问）→ 产 `light.findings.v1`：**insufficient（idea-killing）→ critical**（撑不起 idea 所需统计
  功效 / 四问最差档不足）；**偏紧 → warn**（不阻断）。critical → `run_checkpoint --stage 2` exit 1 → `reroute` 建议 2⊣3。
- **防泄漏划分**：`safe_split.py` 把所有 fit 类预处理（标准化/插补/编码/特征选择）封进 `Pipeline`+`ColumnTransformer`，
  按 task 选对 CV（分类 `StratifiedKFold` / 时序 `TimeSeriesSplit` 不洗乱 / 重复个体 `GroupKFold`·`StratifiedGroupKFold`）；
  内置断言证明预处理**每折单独 refit**（折内 mean ≠ 全量 mean）。时序给 `--time-col` 升序校验防乱序穿越；group 用
  `--group-clf`/`--group-reg` 显式声明（不靠 nunique 猜）。
- **数据泄漏审计 → critical 门**（本技能 critical 灵魂之二）：`split_leakage.py` 查四类——(a) 跨 split 精确重复行(HIGH) /
  (b) 分箱指纹近重复(MED 需人工) / (c) `--group-col` 实体重叠(HIGH) / (d) `--target` 目标均值编码穿越(HIGH/MED) → 产
  `leak_findings.json`（`light.findings.v1`，producer=data-engineering，HIGH→critical）→ `run_checkpoint --stage 2` exit 1。
- **质量门禁**：`quality_gate.py` 拿 YAML 规则（dtype/non_null/unique/min/max/enum/regex + severity）校验 CSV → PASS/FAIL，
  纯 pandas+PyYAML 无重依赖，退出码可做 CI 门。
- **漂移 / 访问分级 / 元数据 / 派生集**：`drift_check`（KS+PSI，PSI 为主 p 为辅）/ `check_access_level`（raw 数据流向
  public 被阻断）/ `croissant_export`（出 Croissant JSON-LD 元数据）/ `derive_eval_set`（research-plan 回边的派生评测集）。

### ASK — 停下问用户，给「证据 + 推荐 + 备选」（决策点 🧑）

| 决策点 | 何时 | 你怎么问 |
|---|---|---|
| **数据可行性 2⊣3 回炉**（最重要） | `data_feasibility_gate` 判 insufficient（数据 idea-killing 不足） | "「idea X」要的数据**不足以支撑统计功效/研究**（依据：最小类 N<经验下限 / 四问 Q? insufficient）。**建议**回 idea-generation（2⊣3）带『缺口=… + 补法=补采到 M / 改 idea 降数据门槛』。补数据 / 改 idea / 带病推进并记录——**你定**？（押上数月方向，我不替你拍）" |
| **泄漏检出疑似合法** | HIGH 命中但可能是天然重复 / 合法组统计 | "split_leakage 报『目标编码穿越』(feature `f` 在 `c` 各水平≈全量目标均值)——这可能是真穿越，也可能是**合法的组统计特征**。是哪种？（我不替你判数据来源）" |
| **经验阈值松紧** | 样本量偏紧（warn）但用户想推进 | "样本量 EPV=15 偏紧（经验下限 10、较稳 20），不是 power analysis。要按你的效应量做正式功效论证、还是先按偏紧推进并在论文里 hedge？" |
| **候选数据集取舍** | shortlist 在许可/代表性/规模/成本间冲突 | "A 许可清楚但人群偏窄；B 更贴任务但 gated 且 split 不明。建议先抽样 A 并继续核 B 条款；选 A / 申请 B / 改 idea——你定？（downloads/likes 不替你拍科学适配）" |
| **自建 vs 用现成 / 隐私合规** | 需自建数据集 | "这方向有现成数据集吗（OpenML/HF/Kaggle 我可查）？自建涉隐私（人/医疗数据）须脱敏+授权+IRB——要走自建吗？合规须你/法务签字。" |

### NEVER — 绝不 [NON-NEGOTIABLE]

> **这一节是红线，不可协商、不可被"先把数据洗了再说""差不多够了""这点泄漏不影响"绕过。违反任一条 = 严重失职。**

1. **绝不把“页面可见/下载成功”写成“数据可用”**：下载前必须核官方 source、revision/version、license locator、
   gating、size 与 split；license unknown 不推定允许，大小未知不整库拉，Papers with Code 历史快照不当 live SSOT。
2. **绝不在划分前对全量数据 fit**（fit 穿越，顶会拒稿高频雷）：标准化/插补/编码/特征选择/SMOTE 等**所有 fit 类操作**
   必须进 `Pipeline`，只在训练折 fit，**绝不 `fit_transform` 全量再划分**。Kapoor-Narayanan(2207.07048) 8 类泄漏里
   "preprocessing/feature-selection on train+test" 就是这条。`safe_split` 已对此做折内 refit 断言。
3. **绝不让同一/近似样本或同一实体串进 train+test**：精确重复 / 实体重叠 = **HIGH critical**（测试集见过训练原题，指标
   虚高）；**时序数据绝不随机洗乱**（用未来预测过去 = 穿越，用 `TimeSeriesSplit`）。这是 `split_leakage` 的 LEAK-02/SPLIT-02。
4. **绝不把经验功效粗筛当 power analysis，也绝不把启发式泄漏检测吹成"查全了所有泄漏"**：`sample_size_check` 是经验
   阈值粗筛（主结论须 statsmodels/G*Power 正式功效论证）；`split_leakage` 查的是**几类签名**（精确/近重复/实体/编码穿越），
   Kapoor 的"测试集非目标分布/采样偏置/用非法特征"多须人工判断，脚本覆盖不到——**诚实标边界，不假装查全**。
5. **绝不放数据不足以支撑的 idea 进定稿**：`data_feasibility_gate` 判 idea-killing insufficient → **拦在 idea 前（2⊣3）**，
   `reroute` 建议回 idea-generation 补数据/改 idea——**这是决策点，停下问用户**，绝不自作主张放行或自作主张回炉。
6. **绝不对验证/测试折做增强或重采样**：数据增强/SMOTE/过采样**只在训练折内做**（先划分再增强），验证/测试保持原始分布，
   否则指标虚高。增强后用 `split_leakage` 复查同一原始样本的多个变体没撒进两侧。
7. **绝不让 raw/未脱敏数据流向公开环节，绝不编造数据来源/DOI**：`check_access_level` 守门，raw 流向 paper/figure/
   public-repo 被阻断；数据卡来源须可核链接（隐私/许可合规须人工与 research-ethics 复核，脱敏是否到位脚本不替判）。
8. **绝不全自动删 cleanlab 标的"错标"样本**：置信学习给的是**候选**（pred_probs 必须 out-of-sample），找出后**人工裁定
   top-K**，删样本要记录并评估对类别分布的影响——cleanlab 定位 + 人裁定，不全自动。

> 自检触发词：当你想说"下载量最高就用 / 网页能下所以能发表 / 先把数据标准化了再划分 / 时序数据 shuffle 一下 /
> 重复行无所谓 / 这点样本应该够了 / 测试集也增强一下凑数 / cleanlab 说错的直接删"——**停**，先逐条对照 NEVER。

---

## 指令流：何时调哪个脚本（引擎已就位，亲手 selftest 到 exit 0，直接调用勿重写）

13 个脚本在 [`scripts/`](scripts/)；`split_leakage`/`data_feasibility_gate`/`data_identity_fitness` 接 `_shared`（规范 bootstrap 产 findings），
其余纯 stdlib 或 pandas/numpy/sklearn。Windows 跑前 `set PYTHONUTF8=1`。

### ⓪ 数据身份 + 权限 + 血缘 + split threat + fitness 统一契约（Round 3 必跑）

```bash
python scripts/data_identity_fitness.py --spec data_identity_fitness.json \
    --report data_identity_findings.json --json-out data_identity_report.json
```

输入 `light.data_identity_fitness.v1`（模板见 [`templates/data-identity-fitness.example.json`](templates/data-identity-fitness.example.json)，故意不完整，直接跑应 exit 1）：锁定 `as_of`、`dataset_id/version/source_locator/snapshot_at/raw_sha256`，逐项核 `license/consent/DUA/ethics_review`，登记 `raw→clean→split` 衍生链，统一 `TIME_CROSSOVER/GROUP_OVERLAP/ENTITY_OVERLAP/PREPROCESSING_BEFORE_SPLIT/TARGET_LEAKAGE/NEAR_DUPLICATE/AUGMENTATION_LEAK` threat matrix，并给 `measurement_quality/label_quality/missingness/sample_power/bias/staleness` 适用性裁定。**UNKNOWN 不是 pass**：权限未知、split threat 未排除、stale 无 impact、DERIVED 无血缘、未来 `snapshot_at/created_at/data_valid_at`、存在 blocker 却声明 `FIT` 均 critical fail。`decision=NOT_FIT/UNKNOWN` 本身阻断推进；只有无 blocker 且限制已下沉时，才可 `FIT_WITH_LIMITATIONS`。

### ⓪b 数据发现与下载前 intake（warn-only，不替用户选）

```bash
python scripts/dataset_intake.py --query "breast cancer" --limit 10 --sort downloads \
    --report data_candidates.json
python scripts/dataset_intake.py --inspect scikit-learn/breast-cancer-wisconsin
```

输出 `light.data_candidates.v1`，含 `raw_response_sha256` 与 `candidate_manifest_sha256`；缺
license/revision/last_modified/size/split/file tree/card、license 只来自 tag、gated/private 或命中医疗/隐私/人类等
sensitive tags → `review`，API 失败 →
`UNAVAILABLE` exit 2。**它不产 `light.findings.v1`、不进入 STAGE_GATES**；完整闭环见
[`references/data-resource-map.md`](references/data-resource-map.md)。

### ① 数据可行性前置门 → 不足则 2⊣3（拦在 idea 前，本技能 critical 灵魂之一）

```bash
# 规模够不够支撑 idea 所需统计功效（经验粗筛）+ 四问 → critical/warn findings：
python scripts/data_feasibility_gate.py --spec feasibility_spec.json --report feas_findings.json   # insufficient → exit 1
# 交总控聚合（stage 2 确认点，critical fail → exit 1 确定性阻断）：
python ../light-orchestrator/scripts/run_checkpoint.py --file .light/passport.yaml --stage 2 \
    --findings feas_findings.json --write --ts 2026-06-18T11:00
# fail → 根因回炉建议（命中 ROUTES[2]，建议 2⊣3：拦在 idea 前，只建议不执行，停下问用户）：
python ../light-orchestrator/scripts/reroute.py --findings feas_findings.json --stage 2 \
    --passport .light/passport.yaml
# 用户拍板回炉后落账：
python ../light-orchestrator/scripts/passport.py add-back-edge --to 3 --from 2 \
    --root-cause "数据不足以支撑 idea 所需统计功效" --evidence-ptr "<reroute 给的指针>"
```
`feasibility_spec.json`：`{project, idea, sample{task,n,classes,features,positives,per_class}, feasibility{sufficiency,
quality,feature_value}}`（scale 缺省由 sample 自动回填）。spec 源自 idea-generation 立项卡的"数据可行性必答字段"。

### ② 数据泄漏 critical 门（本技能 critical 灵魂之二）

```bash
# 四类泄漏审计 → leak_findings.json（HIGH=critical）：
python scripts/split_leakage.py --train train.csv --test test.csv --group-col user_id --target y \
    --out leak_audit.md --findings leak_findings.json          # 任一 HIGH → exit 1
# 单文件带 split 列：--csv data.csv --split-col split
# 交总控聚合（critical fail → exit 1 阻断；泄漏在 stage 2 内修复，非跨阶段回边）：
python ../light-orchestrator/scripts/run_checkpoint.py --file .light/passport.yaml --stage 2 \
    --findings leak_findings.json --write --ts 2026-06-18T11:30
```

### ③ 防泄漏划分 / 质量门 / 体检 / 漂移（被编排，也可单独跑）

```bash
python scripts/data_doctor.py --csv data.csv --target y --out report.md     # 体检画像（先做）
python scripts/safe_split.py --csv data.csv --target y --task group --group-col user_id --group-clf  # Pipeline+CV 折内 refit
python scripts/quality_gate.py --csv data.csv --rules rules.yaml --out gate.md   # YAML 数据门禁（CI）
python scripts/sample_size_check.py --task clf --n 1200 --classes 3 --features 20  # 经验功效粗筛（非 power analysis）
python scripts/data_feasibility.py --project X --q1 ok:... --scale-json size.json --q4 ok:... --out data_feasibility.md
python scripts/drift_check.py --ref train.csv --cur test.csv --out drift.md  # KS+PSI（PSI 为主 p 为辅）
python scripts/check_access_level.py --level raw --sink paper   # raw→public 阻断
python scripts/croissant_export.py --in card_fields.json --out ds.croissant.json   # Croissant 元数据
python scripts/derive_eval_set.py --base data.csv --spec derive_spec.json --outdir derived/  # research-plan 回边
```
各脚本 `--selftest`/`--help` 即接口；资源闭环见 [`data-resource-map.md`](references/data-resource-map.md)，
逐工具 API/已知坑见 [`references.md`](references.md)。

---

## 院士级深挖：四条是及格线（蓝图 §4.3-2，不是加分项）

### ① 数据可行性前置（很多 idea 死在数据根本不够/不可得/质量差）

提 idea **之前**先问四问：这 idea 要什么数据？**规模/质量/标注够不够支撑统计显著**？`sample_size_check` 给经验粗筛
（分类每类 ≥50 偏紧/≥100 较稳；回归 EPV 样本/特征 ≥10/≥20；二分类正例 EPV，Peduzzi 1996），`data_feasibility` 四问取
最差档。**数据 idea-killing 不足 = critical 前置门**，`reroute` 建议 **2⊣3**（拦在 idea 前，补数据/改 idea）——别让一个
数据撑不起的 idea 押上数月。

### ② 数据泄漏前置查（顶会拒稿高频雷，critical 一票否决）

Kapoor-Narayanan(Patterns 2023, 2207.07048) survey 出 **17 个领域 329 篇论文**因泄漏结论过度乐观，给 **8 类泄漏**。
本技能查可机检的几类（对标 Deepchecks `TrainTestSamplesMix`/`DateTrainTestLeakage*`/`IndexTrainTestLeakage`）：
- **标准化/预处理早于划分**（fit 穿越）→ `safe_split` 折内 refit 杜绝。
- **时序穿越**（用未来预测过去）→ `TimeSeriesSplit` + `--time-col` 升序校验。
- **train-test 实体重叠**（同一用户/患者/牧场跨 split）→ `split_leakage --group-col`，`GroupKFold` 防。
- **目标编码穿越**（目标均值编码用了含 test 的全量）→ `split_leakage --target` 查签名。
**任一 HIGH→critical→exit 1**。这是 stage 2 的 STAGE_GATES（leakage）。

### ③ 数据的可挖掘价值判断（有没有可做文章的结构/规律）

`data_doctor` 画像 + 四问 Q4：特征-目标关系是否真实（非 ID-like 误用、非目标泄漏）、有没有可建模的结构。data-centric
视角（DataPerf）：改数据有时胜过堆模型。**这是定性判断 + 画像启发，不是可比分数**。

### ④ 自建数据集（标注规范 / 隐私合规 / 可发布性 / 许可）

`templates/annotation_guide.md`（类目定义/边界规则/LLM 辅助+人工审核闭环/质检抽样率/IAA）+ `assets/data_card_template.md`
（对齐 Datasheets for Datasets / HF Dataset Card / Croissant：动机/构成/采集/标注/用途/分发/维护 + 偏差·隐私·访问分级·溯源）。
标注质量：IAA（sklearn `cohen_kappa_score` / statsmodels `fleiss_kappa`）评流程整体 + cleanlab 置信学习定位具体可疑样本
（**人裁定 top-K 不全自动删**）。隐私/许可合规须人工与 research-ethics 复核。

---

## 收尾 self-check（出 verdict 前 / 回写总控前过一遍）

- [ ] 候选数据的 **source/revision/license locator/gating/size/split/file tree/last_modified** 当天核了吗？
      `dataset_intake` 报告有 `raw_response_sha256` 与 `candidate_manifest_sha256` 吗？抽样前记 URL，整库前记 SHA256 了吗？
- [ ] 跑过 `data_identity_fitness.py` 吗？数据身份、权限链、衍生链、split threat matrix、fitness 与 staleness 都有 locator/hash/impact 吗？
- [ ] `as_of`、`snapshot_at`、split `created_at`、`data_valid_at` 是真实核验/冻结时间吗？没有预填未来日期吧？
- [ ] 没拿 downloads/likes/usability 代替任务匹配与代表性判断吧？受限或 license unknown 的如实写 `review/unresolved` 吧？
- [ ] raw→clean 的 hash、变换脚本/commit、行映射与 split scheme/seed/group/time 留全了吗？
- [ ] DERIVED 数据有每步 input/output SHA256、transform locator、commit 吗？权限 UNKNOWN/RESTRICTED/PROHIBITED 没被写成“可用”吧？
- [ ] 提 idea 前判了**数据可行性**吗？数据 idea-killing 不足的，**停下用 ASK 问用户** 2⊣3 回炉决策了吗？（没自作主张放行/回炉）
- [ ] 所有 fit 类预处理都进 `Pipeline` **只训练折 fit** 了吗？没在划分前 `fit_transform` 全量吧？
- [ ] 时序数据用 `TimeSeriesSplit` 没洗乱吧？重复个体用 `GroupKFold` 防实体重叠了吗？
- [ ] 跑 `split_leakage` 查了**四类泄漏**吗？HIGH 命中是真污染还是疑似合法（停下问用户）？
- [ ] 没把经验功效粗筛当 **power analysis**、没把启发式泄漏检测吹成 **"查全了"** 吧？（诚实标边界）
- [ ] 增强/重采样**只在训练折**做了吗？没污染验证/测试折吧？
- [ ] raw/未脱敏数据没流向公开环节吧（`check_access_level`）？数据来源可核、没编造 DOI 吧？
- [ ] cleanlab 标的"错标"是**人裁定 top-K**、没全自动删吧？

---

## 名实对齐（诚实，不吹成卖点）

**真增量（v2 兑现，已 selftest）**：⓪ **数据身份/权限/血缘/split threat/fitness 统一契约**（`data_identity_fitness.py`，Round 3 新增）——产 `light.findings.v1`，把 license/consent/DUA/ethics、raw SHA256、衍生链、split threat matrix、staleness impact 与 `FIT/FIT_WITH_LIMITATIONS/NOT_FIT/UNKNOWN` 对齐；UNKNOWN/禁止/未排除威胁、未来时间、`NOT_FIT/UNKNOWN` 裁定不会被冒充 pass。① **数据候选下载前 intake**（`dataset_intake.py`，Round 2 新增/Round 3 续补）——HF 公开 API
元数据归一为 `light.data_candidates.v1`，核 access/license/revision/last_modified/size/split/file tree/card，记录
`raw_response_sha256` 与 `candidate_manifest_sha256`；缺项、tag-only license、敏感标签或 gated/private 诚实 `review`，不冒充 usable、
不扩大 critical 面。② **数据泄漏 critical 门 producer**（`split_leakage.py` 港 v1，**v2 修硬编码
`../../_shared`→规范 bootstrap** + producer `m02`→`data-engineering`）——四类泄漏 → `leak_findings.json`（`light.findings.v1`，
HIGH=critical），被 `run_checkpoint --stage 2` 聚合 **exit 1**；输出名正是 `STAGE_GATES[2]` 引用的标准件。③ **数据可行性
前置 critical 门 producer**（`data_feasibility_gate.py`，**v2 净新增接线**）——编排港来的 `sample_size_check`+`data_feasibility`
（v1 纯工具、零接 `_shared`，grep 实证）产 critical/warn findings，insufficient → `reroute` 命中 `ROUTES[2]` 建议 **2⊣3**
（拦在 idea 前）。④ **防 fit 穿越的 Pipeline+CV**（`safe_split` 折内 refit 断言）。⑤ **零重依赖数据门**（quality_gate 是
GX 哲学的轻量同构，纯 pandas+PyYAML）。

**裸模型本就会的（不吹）**："数据要先划分再标准化""注意别泄漏""样本量要够""数据集要写卡"——裸 Opus 都会。本技能价值 =
① **把防泄漏落成确定性机读门 + 折内 refit 断言**（裸模型会嘴上说不泄漏、手上还是全量 fit）；② **数据可行性前置于 idea
定稿 + 2⊣3 回边**（裸模型不会"拦在 idea 前"喂回 idea 阶段）；③ **机读 critical findings + 确定性阻断 + 根因回炉**
（裸模型给口头结论，编排器读不了、阻断不了）。

**诚实落后项（已知没做到）**：
1. **自动发现目前只接 HF 公共元数据**：OpenML/UCI/Zenodo/Kaggle 走资源地图 + harness 联网；`metadata-ready` 只表示字段
   较齐，不表示任务适配、许可终判、无隐私/无泄漏。HF API 失败时 exit 2 + UNAVAILABLE，不用旧缓存冒充当天真值。
2. **泄漏检测是启发式、有边界**：`split_leakage` 查几类**签名**（精确/近重复/实体/目标编码穿越），**≠"查全了所有泄漏"**；
   近重复靠分箱指纹（**巧合会误报**，标 MED 需人工）；目标编码穿越的"**合法组统计**"也可能命中（须人工核来源）。Kapoor 的
   "测试集非目标分布/采样偏置/用非法特征"多须人工判断，脚本覆盖不到。
3. **统计功效是经验阈值，非 power analysis**：`sample_size_check` 是领域经验下限粗筛（每类样本/EPV/检测实例），**不替代**
   效应量+显著性+功效的正式论证（statsmodels/G*Power）。阈值经验默认、可调。
4. **可行性四问档位是人/脚本判定、非自动真值**：`data_feasibility_gate` 只**聚合判据 + 出 findings**，不替你判"数据到底
   够不够"——GIGO（输入的四问/规模参数错，结论就错）。
5. **不跑置信学习/不内置 cleanlab、不做 EDA 全家桶**：标注质量靠规范+IAA+(外部)cleanlab；`data_doctor` 是粗筛画像非完整
   EDA；漂移/质量门用轻量自写实现（drift_check 纯 numpy 渐近 p、quality_gate 无 GX 重依赖），表达力不及 Deepchecks/GX/
   ydata-profiling，重场景仍建议用专业库（references 有真实端点）。
6. **隐私/许可合规不替判 + 不做完整 Croissant/datasheet 校验**：`check_access_level` 按声明判流向（真脱敏须人工+research-ethics）；
   `croissant_export` 出关键层（完整 spec 校验/Hub 上传留外部工具）。
7. **v1 资产取舍（诚实）**：港 split_leakage/safe_split/sample_size_check/data_feasibility/quality_gate/data_doctor/
   drift_check/check_access_level/croissant_export/derive_eval_set；**`emit_artifacts.py` 未港**——其"标准工件名 + passport
   登记"在 v2 归 memory-pm `pm.py` / orchestrator `passport.py append-stage`，不重造（标准工件名约定见本 SKILL「产出」）。
   v1 的 `code_assets/` 共享统计库（stats_tests/agreement）v2 未港，统计/κ 用 statsmodels/sklearn 直接做。

> 标准产出工件：`data_feasibility.md`（交 idea-generation/idea-critique，前置 2⊣3）· `leak_findings.json`（泄漏 critical 门）·
> `quality_report.md` / `data_card.md`（交 research-plan/experiment-coding 做实验）。落 `.light/`，passport 登记交 memory-pm。

---

## 参考（三级渐进披露：需要时再读）

- 对标真相源：[`docs/competitors/data-engineering.md`](../../docs/competitors/data-engineering.md)（11 个同类一手核 + 横切可借 + 超越点 + 诚实边界）
- 真实用户资源工作流：[`references/data-resource-map.md`](references/data-resource-map.md)（需求卡→多源发现→preflight→抽样→血缘→门→发布；access 分级）
- 工具一手核查笔记（真实端点/API/参数/已知坑）：[`references.md`](references.md)（pandas/polars/DuckDB/Deepchecks/GX/ydata-profiling/cleanlab/OpenML/HF/Kaggle/数据增强 等）
- 引擎脚本：[`scripts/`](scripts/)——各 `--selftest`/`--help` 即接口；`split_leakage.py`（泄漏 critical 门）· `data_feasibility_gate.py`（可行性 critical 门 + 2⊣3）是 findings 核心
- 模板/案例：[`assets/data_card_template.md`](assets/data_card_template.md)（datasheet）· [`templates/annotation_guide.md`](templates/annotation_guide.md)（标注规范+IAA）· [`examples/worked_example.md`](examples/worked_example.md)（山羊行为数据走查）· [`examples/rules.example.yaml`](examples/rules.example.yaml) · [`examples/derive_spec.example.json`](examples/derive_spec.example.json)
- 地基契约：[`_shared/README.md`](../../_shared/README.md)（`findings_schema` · `gate_runner` · 规范 bootstrap）
- 上游/下游：[`light-idea-generation`](../light-idea-generation/)（stage 3，立项卡"数据可行性必答字段"，2⊣3 前置回边）· [`light-orchestrator/scripts/run_checkpoint.py`](../light-orchestrator/scripts/run_checkpoint.py)（stage 2 聚合 critical fail→exit 1）· [`reroute.py`](../light-orchestrator/scripts/reroute.py)（ROUTES[2] 建议 2⊣3）· research-plan(stage 5，派生评测集回边)
