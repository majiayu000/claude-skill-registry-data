---
name: single-number-analysis
description: 对单个电话号码进行完整综合画像和下钻分析，输出基础属性、通话行为、联系人广度、共享设备、关系圈规模、Top 可疑节点、桥接/枢纽角色、风险解释和 Markdown 报告。适用于完整分析一个号码；若用户要求正式证据包，应使用 risk-evidence-pack。
---

# single-number-analysis

## 这个 skill 是做什么的

这个 skill 不是“子图抽取子技能”，而是一个 **完整的单号码综合分析 skill**。

它面向 **单个号码** 做下面几类事情：

1. 输出号码画像摘要
2. 从通话 / 设备 / 混合关系三个视角分析该号码
3. 评估关系圈规模，并区分“截断前 / 截断后”
4. 输出 Top 可疑节点排序
5. 输出共享设备主线索
6. 识别局部 Hub 和桥接点
7. 推荐下一步最值得下钻的节点
8. 自动生成 Markdown 报告并提供附件

---

## 什么时候优先使用它

当用户的问题属于下面这些类型时，应该优先使用本 skill：

- “帮我完整分析这个号码”
- “这个号码值不值得重点查”
- “围绕这个号码，谁最可疑”
- “这个号码的共享设备线索强不强”
- “输出这个号码的画像、关系圈规模、可疑节点和调查建议”
- “请生成 markdown 报告并给我下载”

### 不要误用成 subgraph-extraction-analysis 的情况

如果用户明确要求的是 **完整单号码综合分析**，就不要只调用子图技能。

也就是说：

- 要完整分析一个号码 → 用 `single-number-analysis`
- 只想抽 1 跳 / 2 跳局部图 → 用 `subgraph-extraction-analysis`

---

## 输入参数

### 必填参数

- `--phone-id`：目标号码 ID

### 可选参数

- `--hops`：关系圈跳数，默认 `2`
- `--max-nodes`：最多保留多少个关键节点，默认 `200`
- `--top-k`：输出多少个 Top 可疑节点，默认 `10`
- `--analysis-mode`：分析模式，可选 `mixed` / `call_only` / `device_only`，默认 `mixed`
- `--directed-call`：是否按有向通话图分析
- `--user-node-path`：号码画像表路径
- `--call-graph-path`：通话边表路径
- `--device-graph-path`：号码-设备边表路径
- `--source-col`：通话边源列名，默认 `src_user_id`
- `--target-col`：通话边目标列名，默认 `dst_counterparty_id`
- `--device-source-col`：设备边号码列名，默认 `user_id`
- `--device-target-col`：设备列名，默认 `imei`
- `--output-dir`：报告输出目录，默认 `/mnt/user-data/outputs`

---

## 输出内容

脚本输出 JSON，重点字段包括：

- `phone_profile`：号码画像摘要
- `analysis_view`：当前分析模式和参数
- `call_relation_analysis`：通话关系统计
- `shared_device_analysis`：共享设备统计与线索
- `subgraph_analysis`：关系圈规模、截断状态、结构边数统计
- `top_suspicious_nodes`：Top 可疑节点
- `key_roles`：局部 Hub / 局部桥接点
- `drilldown_seeds`：推荐二次下钻节点
- `human_summary`：一句话结论
- `investigation_next_steps`：下一步调查建议
- `report_path`：Markdown 报告路径
- `report_exists`：报告文件是否存在
- `artifacts`：前端可展示附件信息

---

## 特别说明：边数统计口径

本 skill 里会明确区分三类数字：

1. **原始通话记录数**
   - 按原始通话表逐条统计
   - 重复通话会重复计数

2. **设备关系投影次数**
   - 一台设备关联多个号码时，会被投影成多个号码对
   - 不同设备可重复贡献多次

3. **图去重边数**
   - 用于关系图展示和结构规模描述
   - 同一对号码只算一条结构边

所以如果你看到“原始记录数”和“图边数”不一样，属于正常现象，不是 bug。

---

## 命令行使用示例

### 示例 1：完整混合分析

```bash
cd /mnt/skills/custom/phone-network-analysis/single-number-analysis/scripts && python3 single_number_analysis_wrapper.py \
  --phone-id "<PHONE_ID>" \
  --hops 2 \
  --max-nodes 200 \
  --top-k 10 \
  --analysis-mode mixed
```

### 示例 2：仅通话 + 有向模式

```bash
cd /mnt/skills/custom/phone-network-analysis/single-number-analysis/scripts && python3 single_number_analysis_wrapper.py \
  --phone-id "<PHONE_ID>" \
  --hops 2 \
  --max-nodes 200 \
  --top-k 10 \
  --analysis-mode call_only \
  --directed-call
```

### 示例 3：仅共享设备模式

```bash
cd /mnt/skills/custom/phone-network-analysis/single-number-analysis/scripts && python3 single_number_analysis_wrapper.py \
  --phone-id "<PHONE_ID>" \
  --hops 2 \
  --max-nodes 200 \
  --top-k 10 \
  --analysis-mode device_only
```

---

## 前端提示词建议

### 提示词 1：完整单号码分析

```text
请使用 phone-network-analysis/single-number-analysis skill 对下面这个号码做完整分析：
1. 输出号码画像
2. 输出通话关系分析
3. 输出共享设备分析
4. 输出关系圈规模（截断前 / 截断后）
5. 输出 Top 可疑节点
6. 输出桥接点/枢纽点
7. 输出推荐二次下钻节点
8. 生成 markdown 报告并展示下载附件

号码ID：<PHONE_ID>
参数：hops=2, max_nodes=200, top_k=10, analysis_mode=mixed
```

### 提示词 2：只看通话视角

```text
请使用 phone-network-analysis/single-number-analysis skill 只从通话关系视角分析这个号码，按有向图处理，并生成 markdown 报告。
号码ID：<PHONE_ID>
参数：analysis_mode=call_only, directed_call=true, hops=2, max_nodes=200, top_k=10
```

### 提示词 3：只看共享设备视角

```text
请使用 phone-network-analysis/single-number-analysis skill 只从共享设备视角分析这个号码，并给出最值得继续调查的 3 个节点。
号码ID：<PHONE_ID>
参数：analysis_mode=device_only, hops=2, max_nodes=200, top_k=10
```

---

## 前端执行要求

脚本运行后，如果返回了 `report_path` / `report_exists` / `artifacts`：

1. 必须先检查 `report_exists` 或直接检查文件存在
2. 再读取完整 Markdown 报告
3. 最终把 Markdown 作为附件展示给用户
4. 不要只显示路径字符串

---

## 和其他 skill 的关系

- `graph-operator`：底层基础算子层
- `subgraph-extraction-analysis`：只负责局部子图抽取
- `single-number-analysis`：面向业务的完整单号码分析主 skill
- `association-path-analysis`：继续做路径型联合核查
- `overlap-analysis`：继续做重叠关系核查

也就是说：

**single-number-analysis 不是替代基础算子，而是把基础算子组合起来，形成真正可直接使用的电话网络业务 skill。**
