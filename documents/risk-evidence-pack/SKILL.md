---
name: risk-evidence-pack
description: 为单个电话号码生成结构化风险证据包，汇总号码画像、风险结论、通话证据、共享设备证据、共同对端证据、证据评分和后续下钻建议。适用于“为什么高风险”“整理证据包”“生成可交付材料”等问题；不用于全局 TopN 发现或群体团伙识别。
---

# risk-evidence-pack

## 这个 skill 是干什么的

这个 skill 用来回答这类问题：

- “这个号码为什么值得重点关注？”
- “请把这个号码的风险证据整理成一套证据包。”
- “请输出这个号码的共享设备、同圈重叠、共同对端证据。”
- “请生成 markdown 报告和附件，方便下载和后续研判。”

它和 `topn-high-risk-discovery` 的分工不同：

- `topn-high-risk-discovery` 负责 **找出谁最值得优先看**
- `risk-evidence-pack` 负责 **解释为什么这个对象值得看**

所以这个 skill 的重点是：

1. 给出风险证据分和证据强度
2. 拆开证据来源
3. 形成结构化附件
4. 帮助继续下钻到别的 skill

---

## 它依赖什么数据

这个 skill **优先使用已经预处理好的电话网络图数据**，默认分析 `unified` 数据集。

默认会优先寻找下面这些数据根目录：

1. `PHONE_NETWORK_DATASET_ROOT` 环境变量
2. `/mnt/datasets/phone-network`
3. `/workspace/imiss-deer-flow-main/datasets/phone-network`
4. skill 自带的测试数据目录

它期望数据已经整理成这种结构：

- `processed/unified/user_nodes.csv`
- `processed/unified/call_edges.csv`
- `processed/graph_views/unified/edges_phone_imei.parquet` 或 `edges_phone_imei.csv`

### 统一数据集选择规则

- **如果用户明确给了 `--dataset-root`，就用用户指定的数据集根目录。**
- **如果用户没有明确给数据根目录，就优先用现成的 `unified` 预处理图数据。**
- **如果用户只是上传了原始 Excel / CSV，而没有先整理成图结构，这个 skill 不能直接对原始数据开箱即用。**
- **只有真实数据集根目录确实找不到时，才允许退回测试样例。**

也就是说：

- 它能处理 **新的图数据**，前提是新数据已经被预处理成和 `unified` 一样的图结构。
- 它**不能直接把任意原始上传文件自动变成图**，这一层需要单独的数据接入 / 预处理流程。

---

## 它是怎么实现的

这个 skill 是由基础图分析算子组合出来的，不是孤立写死的逻辑。

对应关系如下：

- 号码画像 = `node_lookup`
- 直接联系对端 / 通话广度 = `neighbor_query + aggregation_query`
- 共享设备证据 = `query_shared_device + aggregation_query`
- 同圈重叠证据 = `common_neighbor + aggregation_query`
- 风险证据评分与解释打包 = `aggregation_query + scoring_layer`

所以它本质上是一个 **证据组织与解释层 skill**。

---

## 输入参数

### 必填

- `--phone-id`：目标号码 ID

### 可选

- `--dataset-root`：明确指定数据根目录
- `--dataset`：默认 `unified`
- `--top-k`：控制 markdown 报告中展示多少条主要证据，默认 `10`
- `--evidence-limit`：控制 csv / xlsx 附件保留多少行证据，默认 `50`

---

## 标准命令

### 命令行 / 前端统一推荐写法

```bash
cd /mnt/skills/custom/phone-network-analysis/risk-evidence-pack/scripts && python3 risk_evidence_pack_wrapper.py \
  --phone-id "<PHONE_ID>" \
  --dataset unified \
  --top-k 10
```

### 如果你明确知道数据根目录

```bash
cd /mnt/skills/custom/phone-network-analysis/risk-evidence-pack/scripts && python3 risk_evidence_pack_wrapper.py \
  --phone-id "<PHONE_ID>" \
  --dataset-root "/workspace/imiss-deer-flow-main/datasets/phone-network" \
  --dataset unified \
  --top-k 10
```

---

## 前端提问模板

### 模板 1：标准风险证据包

请使用 `risk-evidence-pack` skill，对这个号码生成完整风险证据包。要求：

1. 输出号码画像
2. 输出风险证据强度和证据分
3. 输出 Top 直接联系对端
4. 输出 Top 共享设备证据
5. 输出 Top 共享设备关联号码
6. 输出 Top 共同对端证据
7. 输出 Top 同圈重叠号码
8. 生成 markdown 报告和 csv/xlsx/json 附件并展示下载入口

号码ID：`<PHONE_ID>`
参数：`dataset=unified, top_k=10`

### 模板 2：解释为什么值得看

请使用 `risk-evidence-pack` skill，解释这个号码为什么值得重点关注，并把关键证据整理成完整证据包。

号码ID：`<PHONE_ID>`
参数：`dataset=unified`

### 模板 3：如果号码不存在，也要明确说明

请使用 `risk-evidence-pack` skill，核查这个号码是否能生成风险证据包；如果当前数据集中不存在该号码，请明确说明原因，不要输出空洞结论。

号码ID：`<PHONE_ID>`
参数：`dataset=unified`

---

## 预期输出

这个 skill 正常会产出：

1. `markdown` 完整报告
2. `direct_counterparties.csv`：直接联系对端明细
3. `devices.csv`：共享设备证据
4. `shared_peers.csv`：共享设备关联号码证据
5. `counterparties.csv`：共同对端证据
6. `overlap_peers.csv`：同圈号码证据
7. `summary.json`：结构化摘要
8. `evidence.xlsx`：证据工作簿

前端应优先展示 markdown 报告，同时把附件挂出来供下载。

---

## 当前版本专门修了什么问题

这个版本重点修了下面几类问题：

1. **DuckDB 的 DISTINCT + ORDER BY 聚合报错问题**
2. **`top_k` 参数之前没有真正影响 markdown 展示的问题**
3. **共同对端和设备预览过长，导致 markdown 报告非常臃肿的问题**
4. **号码不存在时，之前会生成“看起来成功、但实际空洞”的低质量证据包问题**
5. **测试脚本里“未标注号码”样例可能根本不存在，导致测试没意义的问题**

---

## 测试方法

### 一键回归

```bash
cd /mnt/skills/custom/phone-network-analysis/risk-evidence-pack/scripts && bash test_risk_evidence_pack.sh
```

这个测试脚本会：

- 自动跑 1 个经典高风险号码
- 自动找 1 个真实存在的非风险号码
- 自动跑 1 个故意不存在的号码，验证“找不到目标时是否能正确解释”
- 自动把日志写入 `logs/` 目录

### 单独跑一个真实号码

```bash
cd /mnt/skills/custom/phone-network-analysis/risk-evidence-pack/scripts && python3 risk_evidence_pack_wrapper.py \
  --phone-id "141ab86b0a1277138c664368f30bfd93878754a968ca4f0f6f9f4d1b2279328985781d0740742e523f43e705753c5b9fd2bec9752624c1b79cf2b1132f1915be" \
  --dataset-root "/workspace/imiss-deer-flow-main/datasets/phone-network" \
  --dataset unified \
  --top-k 10
```

---

## 适用边界

### 适合

- 给单个重点号码做结构化证据说明
- 给高风险发现结果补“为什么”的解释层
- 给后续 `single-number-analysis` / `shared-device-analysis` / `overlap-analysis` / `association-path-analysis` 提供入口

### 不适合

- 直接处理未预处理的原始上传表格
- 直接替代法律结论或人工终审
- 直接做整群体筛选（那是 `group-risk-analysis` / `condition-based-screening` 的任务）

---

## 后面还能继续扩展什么

后续还可以继续加：

- 时间维异常证据（昼夜切换、突增突降）
- 跟 Top 高风险对象的路径证据自动补充
- 设备池 / 团伙簇归属判断
- “简版证据包”和“完整版证据包”两种输出模板

### 特别说明：目标不存在时

如果当前数据集中不存在该号码：

- 应明确返回 `status=target_not_found`
- markdown 报告里要直接写清楚“当前数据集中未找到该号码”
- 附件只保留：
  - `markdown_report`
  - `summary.json`
- 不应继续把空的 csv/xlsx 当成有效证据附件挂出来
