---
name: gang-cluster-analysis
description: 围绕一组电话号码或候选对象识别疑似团伙簇，综合共享设备、共同对端、内部关系、邻居重叠和多跳关联输出候选簇、核心节点、桥接点和证据链。适用于团伙/簇/核心成员/桥接点问题；不用于单号码画像、TopN 排名、地域对比或确认性案件定性。
---

# gang-cluster-analysis

## 这个 skill 是做什么的

这个 skill 用来做**疑似团伙 / 群组识别**。

它不是只看单个号码，也不是只看两个号码，而是：

- 先从输入号码出发扩展候选成员
- 再综合 **共享设备、共同对端、内部号码对关系、邻居重叠** 等证据
- 识别是否存在一个更紧的疑似团伙簇
- 输出：
  - 团伙簇列表
  - 重点簇
  - 核心节点
  - 桥接点 / 或桥接解释
  - 号码对证据链
  - 共享设备证据
  - 共同对端证据
  - Markdown 报告 + 多个 CSV 证据文件

## 它和前面 skill 的关系

这个 skill 本质上是**基础算子 + 现有高级分析 skill 的组合版**：

- 候选扩展：neighbor_query + common_neighbor + relationship_filter
- 号码对关系：common_neighbor + query_shared_device + relationship_filter
- 子群识别：subgraph_by_nodes + aggregation_query
- 核心节点 / 桥接点排序：aggregation_query + 局部图排序
- 后续复核：association-path-analysis + overlap-analysis + single-number-analysis + shared-device-analysis

所以它不是凭空“猜团伙”，而是把前面已经做好的分析能力组合起来，形成一个更高层的团伙识别 skill。

---

## 输入方式

支持三种输入方式，至少给一种：

1. `--phone-ids`
2. `--phone-id-file`
3. `--input-csv + --phone-id-column`

### 常用参数

- `--group-name`：本次分析名字
- `--candidate-scope`：候选扩展方式
  - `input_only`
  - `shared_device`
  - `common_counterparty`
  - `mixed`（推荐）
- `--max-expand-nodes`：最多保留多少候选号码
- `--top-k`：输出前几条重点结果
- `--min-shared-device-count`：最少共享设备数
- `--min-common-counterparty-count`：最少共同对端数
- `--min-neighbor-overlap`：最少邻居重叠比例
- `--min-edge-score`：保留关系边的最低分
- `--focus-min-cluster-size`：重点簇的最小人数

---

## 内置示例文件（这部分非常重要）

### `sample_group_ids.txt` 是什么

`sample_group_ids.txt` 是 **这个 skill 自带的内置示例号码文件**，不是用户上传文件，也不是数据集目录里的原始文件。

它的默认位置是：

```bash
/mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts/sample_group_ids.txt
```

### 当前端或模型看到下面这种说法时，必须这样理解

- “号码文件：sample_group_ids.txt”
- “使用示例号码文件 sample_group_ids.txt”
- “请直接用 sample_group_ids.txt 测试”

都应当理解为：

**优先使用 skill 自带的这个内置示例文件**，也就是：

```bash
/mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts/sample_group_ids.txt
```

### 不要做的事

当文件名是 `sample_group_ids.txt` 时：

- **不要先去** `/mnt/user-data/uploads/` 查找
- **不要先去** `/mnt/datasets/` 查找
- **不要把它当成用户额外上传的输入文件**

除非用户明确说：

- “我自己上传了一个新的 `sample_group_ids.txt`”
- 或者给了别的明确绝对路径

否则默认就是 skill 内置示例文件。

---

## 输出内容

会生成 6 个文件：

1. Markdown 总报告
2. 团伙簇列表 CSV
3. 核心节点 CSV
4. 号码对证据 CSV
5. 共享设备证据 CSV
6. 共同对端证据 CSV

### 这 6 个文件分别是做什么的

- **Markdown 总报告**：给人直接阅读的总结版，适合前端直接展示。
- **团伙簇列表 CSV**：每个 cluster 一行，适合看一共有多少候选团伙簇、各簇规模多大。
- **核心节点 CSV**：每个重点成员一行，适合继续做单号码深挖。
- **号码对证据 CSV**：每对号码一行，适合复核关系链到底是靠共享设备、共同对端还是内部通话。
- **共享设备证据 CSV**：每台重点设备一行，适合继续追设备池。
- **共同对端证据 CSV**：每个重点共同对端一行，适合看群体共同接触目标。

### 能不能合并

不建议把这 6 个文件硬合并成 1 个 CSV。

原因很简单：

- 团伙簇列表是 **cluster 级**
- 核心节点是 **成员级**
- 号码对证据是 **pair 级**
- 共享设备证据是 **device 级**
- 共同对端证据是 **counterparty 级**

它们的粒度不同，强行拼成一个表反而更乱。

更合理的做法是：

- 保留这 6 份分表
- 让 Markdown 报告做“总入口”
- 如果后面确实想做“单文件交付版”，建议额外做一个 `xlsx` 工作簿，而不是强行合并 CSV

---

## 典型命令

### 方式 1：直接给一组号码

```bash
cd /mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts && python3 gang_cluster_analysis_wrapper.py \
  --group-name sample_gang \
  --phone-ids "号码1,号码2,号码3" \
  --candidate-scope mixed \
  --top-k 10
```

### 方式 2：使用 skill 自带示例文件（推荐写法）

**必须优先使用绝对路径，不要只写 `sample_group_ids.txt`。**

```bash
cd /mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts && python3 gang_cluster_analysis_wrapper.py \
  --group-name sample_gang \
  --phone-id-file /mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts/sample_group_ids.txt \
  --candidate-scope mixed \
  --max-expand-nodes 120 \
  --top-k 10 \
  --min-shared-device-count 1 \
  --min-common-counterparty-count 2
```

### 方式 3：从用户自己的 CSV 读号码

```bash
cd /mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts && python3 gang_cluster_analysis_wrapper.py \
  --group-name custom_group \
  --input-csv /mnt/user-data/uploads/你的文件.csv \
  --phone-id-column phone_id \
  --candidate-scope mixed \
  --top-k 10
```

---

## 推荐提示词

### Q1：标准团伙识别

请使用 gang-cluster-analysis skill，围绕这组号码识别是否存在疑似团伙簇。要求：
1. 输出候选扩展规模
2. 输出识别到的团伙簇列表
3. 输出重点簇的核心节点和桥接点
4. 输出共享设备证据、共同对端证据和号码对证据链
5. 生成 markdown 报告和 csv 证据文件并展示下载附件

### Q2：偏共享设备团伙

请使用 gang-cluster-analysis skill，重点围绕共享设备线索识别团伙。参数：candidate_scope=shared_device, top_k=10。

### Q3：偏共同对端耦合团伙

请使用 gang-cluster-analysis skill，重点围绕共同对端和邻居重叠识别团伙。参数：candidate_scope=common_counterparty, min_common_counterparty_count=2, top_k=10。

### Q4：使用内置示例文件测试（非常推荐这样写）

请使用 gang-cluster-analysis skill，围绕这组号码识别是否存在疑似团伙簇。号码文件使用 skill 自带示例文件：
`/mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts/sample_group_ids.txt`
参数：candidate_scope=mixed, top_k=10。

---

## 前端展示规范（很重要）

前端执行完脚本后，**不要只把 JSON 里的路径字符串打印出来**，而要显式展示附件。

必须按下面顺序做：

1. 运行脚本
2. 读取 JSON 输出里的：
   - `report_path`
   - `artifacts`
3. 对每个 artifact 先检查文件是否存在
4. 先读取 Markdown 报告正文
5. 再把 markdown + csv 全部挂成附件卡片

### 特别规则：当用户提到 `sample_group_ids.txt`

如果用户提示词里写的是：

- `sample_group_ids.txt`
- “示例号码文件”
- “skill 自带号码文件”

前端 / 模型应直接使用：

```bash
/mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts/sample_group_ids.txt
```

不要先去 `/mnt/user-data/uploads/` 或 `/mnt/datasets/` 查找。

---

## 结果怎么理解

### 如果识别到“共享设备驱动团伙簇”
说明这批号码主要靠共用设备连起来，通常优先查设备池。

### 如果识别到“共同对端耦合团伙簇”
说明这批号码虽然未必直接互打，但共同接触了同一批对象，可能属于同圈层。

### 如果重点团伙簇密度很高，但桥接中心性全为 0
这通常不表示结果有问题，而是说明这个簇已经非常紧密，内部没有明显“单一桥接点”。此时更应该优先关注：

- 核心节点
- 共享设备证据
- 号码对高分关系

### 如果只得到“候选松散关联群组”
说明有一定关联，但还不足以支撑“紧密团伙簇”的判断，需要继续下钻。

---

## 注意事项

1. 输入号码太少时，更容易得到“候选群组”，不一定形成紧密团伙。
2. `candidate_scope=mixed` 一般效果最好。
3. 如果前端要展示下载附件，必须让模型读取 JSON 输出里的 `artifacts` / `report_path`。
4. 如果号码文件是 `sample_group_ids.txt`，默认就是 skill 内置示例文件，优先使用绝对路径：

```bash
/mnt/skills/custom/phone-network-analysis/gang-cluster-analysis/scripts/sample_group_ids.txt
```

5. 如果要进一步复核关系，建议联动：
   - `shared-device-analysis`
   - `association-path-analysis`
   - `overlap-analysis`
   - `single-number-analysis`
