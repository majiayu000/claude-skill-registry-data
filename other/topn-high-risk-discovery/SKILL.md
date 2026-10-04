---
name: topn-high-risk-discovery
description: 在用户没有指定硬性筛选条件时，基于预设综合风险评分模型对电话网络全量号码进行自动打分、排序和候选发现，输出 TopN 高风险排行榜、风险分、排名驱动因素和证据摘要。核心任务是自动发现“最值得优先核查”的对象，不是按用户规则过滤；适用于“找 Top10 高风险号码/生成风险排行榜/哪些号码最可疑/自动发现重点对象/综合评分排序”等开放式发现问题。不用于按省份、标签、夜间阈值、联系人阈值、共享设备阈值等明确条件筛选号码，不解释单个号码，不生成单号码证据包，不做原始数据建图或地域对比。
---

# topn-high-risk-discovery

## 这个 skill 是做什么的

`topn-high-risk-discovery` 是电话网络数据中的**自动发现与综合排名型** skill。

它的核心不是按用户给出的条件做过滤，而是：

> 用户没有给出硬性筛选规则时，系统基于预设综合风险评分模型，对全量号码或候选集合进行自动打分和排序，找出最值得优先核查的 TopN 对象。

它直接生成：

- TopN 高风险候选榜；
- 未标注高可疑榜；
- 设备驱动高可疑榜；
- 风险分和排名；
- 排名驱动因素；
- Top 证据摘要；
- Markdown 报告；
- CSV 风险名单。

它回答的是：

1. 全量号码里谁最值得优先核查；
2. 哪些号码综合风险分最高；
3. 哪些未标注号码虽然没有风险标签，但结构特征很可疑；
4. 哪些对象主要由共享设备或联系人广度等因素驱动上榜；
5. 每个上榜对象的主要排名驱动因素是什么。

## 与 condition-based-screening 的强边界

必须严格区分本 skill 和 `condition-based-screening`。

| 维度 | topn-high-risk-discovery | condition-based-screening |
|---|---|---|
| 用户意图 | 用户希望系统自动发现重点对象 | 用户已经给出明确筛选规则 |
| 核心动作 | 自动打分、排序、生成榜单 | 筛选、过滤、命中解释 |
| 典型词 | TopN、Top10、排行榜、最可疑、自动发现、优先核查、综合评分 | 筛选、过滤、满足条件、阈值、同时满足、按省份、按标签 |
| 输出重点 | 排名、风险分、驱动因素 | 命中对象、筛选链路、命中条件 |
| 是否按用户规则过滤 | 不作为核心任务 | 是核心任务 |

如果用户说：

- “找 Top10 高风险号码”；
- “生成高风险排行榜”；
- “哪些号码最可疑”；
- “自动发现重点对象”；
- “综合风险评分排序”；

应使用本 skill。

如果用户说：

- “筛选夜间通话占比超过阈值的号码”；
- “过滤出四川省风险标签对象”；
- “找同时满足联系人广度高和共享设备多的号码”；
- “按省份、标签或阈值筛选对象”；

应使用 `condition-based-screening`，不是本 skill。

## 适合使用的场景

本 skill 适合开放式发现、自动评分、优先级排序类问题，例如：

- 现在这批电话网络数据中最值得优先核查的 TopN 号码是谁；
- 哪些号码综合风险分最高；
- 请生成一份高风险号码排行榜；
- 请自动发现未标注但结构特征可疑的号码；
- 请找出设备关系特别异常、值得优先关注的号码；
- 请输出重点对象名单、风险分、驱动因素和证据摘要。

## 不适合使用的场景

以下情况不要使用本 skill：

- 用户已经给出明确条件，要求按条件筛选；
- 用户要求按省份、标签、夜间阈值、联系人阈值、共享设备阈值过滤号码；
- 用户要求找“同时满足某几个条件”的对象；
- 用户要求解释某一个号码为什么可疑；
- 用户要求生成单号码风险证据包；
- 用户上传原始 CSV，要求先建图；
- 用户要求四川和陕西做地域对比；
- 用户要求跨省同实体联动识别。

对应应转向：

- 条件筛选：`condition-based-screening`；
- 单号码画像：`single-number-analysis`；
- 单号码证据包：`risk-evidence-pack`；
- 原始数据建图：`dataset-onboarding-graph-preprocess`；
- 四川陕西地域对比：`sichuan-shaanxi-comparison`；
- 跨省可联动性判断：`dataset-quality-and-linkability-diagnostic`。

---

## 一、数据集使用规则

### 规则 1：用户明确指定数据集时，优先使用用户指定的数据集

如果用户问题或命令中明确给出：

- `--dataset-root /workspace/imiss-deer-flow-main/datasets/phone-network`
- `--dataset unified`
- “使用 unified / sichuan / shaanxi 数据”

则直接按用户指定执行。

### 规则 2：用户没有指定数据集根目录时，优先使用真实 unified 预处理数据

脚本优先自动查找以下真实数据位置：

1. `PHONE_NETWORK_DATASETS_ROOT`
2. `<repo_root>/datasets/phone-network`
3. `/workspace/imiss-deer-flow-main/datasets/phone-network`
4. `/mnt/datasets/phone-network`
5. `~/imiss-deer-flow-main/datasets/phone-network`

### 规则 3：用户没有指定 dataset 时，默认使用 `unified`

前端问题中出现：

- “在现有电话网络数据里找高风险号码”；
- “对 unified 数据生成风险榜”；
- “自动找最可疑对象”；

都应默认理解为：

```text
dataset-root = datasets/phone-network
dataset = unified
```

---

## 二、输入数据

本 skill 默认依赖标准图结构三件套：

```text
datasets/phone-network/processed/unified/user_nodes.csv
datasets/phone-network/processed/unified/call_edges.csv
datasets/phone-network/processed/unified/edges_phone_imei.parquet
```

各文件作用：

| 文件 | 用途 |
|---|---|
| `user_nodes.csv` | 号码节点画像、标签、省份、sub_label |
| `call_edges.csv` | 通话活跃度、对端数量、联系人广度、夜间行为 |
| `edges_phone_imei.parquet` | 设备关联、共享设备、设备驱动风险 |

---

## 三、它是怎么基于基础算子实现的

本 skill 通过基础图分析算子组合完成自动风险发现：

- `node_lookup`：读取号码画像、标签、省份等节点属性；
- `aggregation_query + neighbor_query`：聚合通话记录、联系人广度、对端数量；
- `neighbor_query + subgraph_by_nodes`：扩展共享设备关系，得到共享设备数、牵出号码数、最强共享设备；
- `relationship_filter + aggregation_query`：做候选范围预过滤和多视角特征聚合；
- `scoring_layer`：对多维特征进行综合风险评分；
- `ranking_layer`：输出 TopN 榜单和不同视角的发现结果。

因此它本质上是：

```text
基础图分析算子 -> 多维特征聚合 -> 综合评分 -> 自动排序 -> TopN 重点对象发现
```

---

## 四、核心输入参数

### 排名与发现参数

- `--top-n`：综合总榜 TopN，默认 `20`；
- `--discovery-top-n`：未标注榜 / 设备榜 TopN，默认 `10`；
- `--analysis-mode`：`mixed` / `call_only` / `device_only`；
- `--ranking-view`：
  - `all_views`
  - `overall`
  - `unlabeled_only`
  - `device_priority`
- `--candidate-scope`：
  - `all`
  - `labeled_only`
  - `unlabeled_only`
- `--province`：候选范围省份限制，例如 `sichuan`。

### 候选范围预过滤参数

- `--min-call-records`
- `--min-counterparties`
- `--min-shared-device-count`
- `--min-device-count`
- `--min-shared-peer-total`
- `--include-sub-labels`
- `--exclude-sub-labels`

重要说明：

> 这些参数在本 skill 中只用于限制自动评分的候选范围，不改变本 skill 的性质。只要用户的核心诉求是“生成风险榜单、自动发现最可疑号码、综合评分排序”，就仍然属于本 skill。若用户的核心诉求是“按这些条件筛出满足规则的对象”，则应使用 `condition-based-screening`。

---

## 五、输出内容

JSON 输出里最关键的字段包括：

- `top_overall_numbers`：综合风险总榜；
- `top_unlabeled_numbers`：未标注高可疑榜；
- `top_device_driven_numbers`：设备驱动高可疑榜；
- `top3_evidence_pack`：Top 对象证据摘要；
- `view_summaries`：不同榜单视角的摘要；
- `discovery_insights`：自动发现结论；
- `report_context_flags`：报告上下文控制信息；
- `report_path`：Markdown 报告路径；
- `risk_list_csv_path`：风险名单 CSV 路径；
- `artifacts`：前端附件列表。

输出报告应明确说明：

- 排名依据；
- 风险分；
- 主要驱动因素；
- Top 证据摘要；
- 是否是未标注但高可疑线索；
- 建议下一步下钻的 skill。

---

## 六、命令行示例

进入脚本目录：

```bash
cd /mnt/skills/custom/phone-network-analysis/topn-high-risk-discovery/scripts
```

### 示例 1：完整自动重点对象发现

```bash
python3 topn_high_risk_discovery_wrapper.py \
  --top-n 20 \
  --discovery-top-n 10 \
  --analysis-mode mixed \
  --ranking-view all_views \
  --candidate-scope all
```

### 示例 2：只看未标注高可疑对象榜

```bash
python3 topn_high_risk_discovery_wrapper.py \
  --top-n 10 \
  --discovery-top-n 10 \
  --analysis-mode mixed \
  --ranking-view unlabeled_only \
  --candidate-scope unlabeled_only
```

### 示例 3：设备驱动重点对象榜

```bash
python3 topn_high_risk_discovery_wrapper.py \
  --top-n 10 \
  --discovery-top-n 10 \
  --analysis-mode device_only \
  --ranking-view device_priority \
  --candidate-scope all \
  --min-shared-device-count 1
```

### 示例 4：四川省候选范围内自动排序

```bash
python3 topn_high_risk_discovery_wrapper.py \
  --top-n 20 \
  --discovery-top-n 10 \
  --analysis-mode mixed \
  --ranking-view all_views \
  --candidate-scope all \
  --province sichuan \
  --exclude-sub-labels whitelist
```

注意：示例 4 的 `--province` 和 `--exclude-sub-labels` 只是限定自动评分的候选范围，不是规则筛选任务。

---

## 七、前端推荐提问模板

### 模板 1：自动 TopN 风险发现

```text
请自动发现 unified 电话网络数据中 Top10 最值得优先核查的高风险号码，输出风险分、排名驱动因素和证据摘要。
```

### 模板 2：未标注高可疑发现

```text
请自动找出尚未标注为风险、但结构特征已经明显可疑的号码，并生成未标注高可疑榜单。
```

### 模板 3：设备驱动重点对象发现

```text
请自动生成设备关系异常驱动的高风险号码排行榜，说明哪些号码主要因为共享设备或设备牵出关系异常而上榜。
```

### 模板 4：开放式重点对象名单

```text
请综合电话网络中的通话行为、联系人广度、设备关联和标签信息，自动生成一份最值得优先核查的重点对象名单。
```

---

## 八、快速测试

建议运行脚本目录下的：

```bash
bash test_topn_high_risk_discovery_fast.sh
```

该测试脚本会：

1. 自动创建项目根目录下的 `logs/topn-high-risk-discovery/`；
2. 保存每次测试的完整终端输出；
3. 列出生成的 Markdown 和 CSV 文件。

---

## 九、什么时候该用这个 skill

当问题是开放式发现和排序时，优先用本 skill：

- “一批号码里谁最值得先查？”
- “帮我自动发现重点对象并生成名单。”
- “帮我找 Top10 高风险号码。”
- “哪些号码最可疑？”
- “帮我生成风险排行榜。”
- “帮我找未标注但很可疑的号码。”
- “帮我找设备关系特别异常、值得优先关注的号码。”

## 十、什么时候不要用这个 skill

当问题是规则过滤或对象下钻时，不要用本 skill：

- “筛选夜间通话占比超过 0.35 的号码。”
- “筛选四川省中共享设备数量不少于 1 的号码。”
- “筛选同时满足联系人广度高和共享设备多的号码。”
- “这个号码为什么可疑？”
- “请给这个号码生成风险证据包。”
- “请比较四川和陕西差异。”

对应转向：

- 条件筛选：`condition-based-screening`；
- 单号码画像：`single-number-analysis`；
- 单号码证据包：`risk-evidence-pack`；
- 两号码路径：`association-path-analysis`；
- 两号码关系重叠：`overlap-analysis`；
- 四川陕西地域对比：`sichuan-shaanxi-comparison`。

---

## 十一、结果解读原则

本 skill 的结果表示“系统自动综合评分后认为最值得优先核查的对象”，不是最终风险定性。

解读时应说明：

- 当前榜单的候选范围；
- 使用的 ranking view；
- 风险分和排名；
- 每个对象的主要驱动因素；
- Top 证据摘要；
- 是否属于未标注高可疑线索；
- 建议下一步调用哪个下钻 skill。

推荐后续链路：

- 解释 Top1 号码：`single-number-analysis`；
- 生成 Top1 证据包：`risk-evidence-pack`；
- 共享设备下钻：`shared-device-analysis`；
- 团伙簇扩展：`gang-cluster-analysis`；
- 时间变化分析：`time-series-anomaly-analysis`。
