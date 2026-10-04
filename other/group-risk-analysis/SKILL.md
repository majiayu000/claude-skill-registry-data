---
name: group-risk-analysis
description: 对一组电话号码开展群体级风险分析，统计群体规模、行为模式、夜间异常、联系人广度、共享设备、共同对端、核心成员和证据完整度。适用于群体画像和群体风险归纳；若用户强调团伙簇、核心节点和桥接点，应优先使用 gang-cluster-analysis。
---

# group-risk-analysis

## 能力定位

`group-risk-analysis` 是面向**号码集合**的群体级风险分析技能。

它不是单号码画像，也不是简单的 TopN 排序，而是把一组号码当成一个整体来做：

- 群体级统计
- 风险模式归纳
- 关系证据链整合
- 共享设备池识别
- 子群结构与群体形态判断
- 后续下钻建议

它面向电话网络数据场景，重点支持识别以下主要群体特征：

1. **高通话量型**
2. **夜间异常型**
3. **联系人广度异常型**
4. **共享设备型**

在基础能力之外，这个最终版还额外支持：

- **号码对关系证据链**：把共享设备、内部通话、共同对端三类证据并到一张关系矩阵里
- **群体形态判断**：输出更像“设备池型紧密群组”“联系人扩张型群组”等结论
- **过滤影响解释**：当 `risk_only`、`province`、`min_shared_device_count` 等过滤没有改变样本时，自动说明“样本同质性”
- **证据完整度与置信度**：告诉你当前群体分析链路是否完整，结论有多稳
- **更完整的附件导出**：markdown 报告 + 成员 CSV + 号码对 CSV + 设备证据 CSV + 共同对端 CSV

---

## 它解决什么问题

适合回答这类问题：

- 这批号码是不是一个明显的高风险群体？
- 这批号码主要是哪种风险特征更突出？
- 群体内部是否形成共享设备池？
- 群体内部是“设备驱动”还是“共同对端驱动”？
- 群体内部是否已经形成多个子群/小团体？
- 哪些号码最值得优先下钻？
- 当前过滤条件是否真的改变了群体分析对象？

---

## 输入方式

支持三种输入方式，至少提供一种：

### 方式 1：直接传号码列表
```bash
--phone-ids "号码1,号码2,号码3"
```

### 方式 2：传文本文件
```bash
--phone-id-file /path/to/group_ids.txt
```

文本文件要求：每行一个号码 ID。

### 方式 3：传 CSV 文件
```bash
--input-csv /path/to/input.csv --phone-id-column phone_id
```

---

## 主要参数

### 基础参数
- `--group-name`：群体名称，默认 `group`
- `--top-k`：报告里展示前多少个重点成员/设备/号码对/共同对端，默认 `10`
- `--pattern-min-members`：某类模式至少命中多少成员才算群体特征，默认 `2`

### 群体过滤参数
- `--risk-only`：只保留风险标签号码
- `--province sichuan`：只保留指定省份号码
- `--include-sub-labels risk,purefraud`：只保留这些 sub_label
- `--exclude-sub-labels whitelist,normal`：剔除这些 sub_label
- `--min-call-records 100`
- `--min-counterparties 50`
- `--min-shared-device-count 1`
- `--min-shared-peer-total 20`
- `--min-device-pool-count 2`

### 模式阈值参数
- `--high-call-threshold`：高通话量阈值（默认自动）
- `--broad-contact-threshold`：联系人广度阈值（默认自动）
- `--shared-peer-threshold`：共享设备牵出号码阈值（默认自动）
- `--shared-device-threshold`：共享设备数阈值，默认 `1`
- `--min-common-counterparty-members`：至少多少个群体成员共同接触某个对端才纳入“共同对端证据”，默认 `2`

### 夜间分析参数
- `--night-start-hour 22`
- `--night-end-hour 6`
- `--night-ratio-threshold 0.30`
- `--night-count-threshold 10`

---

## 输出内容

技能会输出：

### 1. 群体总体结论
- 群体规模
- 重点信号
- 群体形态判断
- 已识别主要群体特征
- 省份分布
- 标签分布
- 证据完整度与分析置信度

### 2. 过滤与样本影响说明
- 初始输入成员数
- 标签过滤后成员数
- sub_label 过滤后成员数
- 省份过滤后成员数
- 指标阈值过滤后成员数
- 如果过滤没有改变样本，会自动说明“样本同质性”

### 3. 群体级统计
- 总通话记录数
- 平均通话量
- 平均联系人广度
- 总共享设备数与共享设备牵出号码总量
- 群体内部关系边数量与密度
- 共同对端数量
- 夜间通话统计

### 4. 四类主要群体特征识别
- 高通话量型
- 夜间异常型
- 联系人广度异常型
- 共享设备型

每一类都会输出：
- 是否触发
- 命中成员数
- 参考阈值
- 未触发原因（如适用）
- 代表成员

### 5. 群体核心成员排序
输出最值得优先下钻的号码，并说明：
- 命中多少类群体信号
- 主要驱动类型
- 综合群体核心分
- 简要证据摘要

### 6. 号码对关系证据链
把三类证据统一整合进一张关系矩阵：
- 共用设备数
- 内部通话记录数
- 共同对端数
- 综合 relation_score

### 7. 共享设备证据链
输出：
- 群体内重点共享设备
- 每台设备在群体内挂了多少成员
- 设备总挂载号码数
- 风险号码数
- 省份数
- 标签种类数

### 8. 内部关系结构与子群
输出：
- 基于“共享设备 + 群体内部通话 + 共同对端”联合关系识别的子群
- 子群规模与成员预览

### 9. 共同对端证据
输出：
- 被多个成员共同接触的重点对端
- 共同接触成员数
- 累计通话量

### 10. 导出附件
会生成：
- markdown 报告
- 成员指标 csv
- 号码对证据 csv
- 设备证据 csv
- 共同对端证据 csv

---

## 输出文件说明

通常会生成：

- `group_risk_report_<group_name>_<N>members.md`
- `group_risk_report_<group_name>_<N>members_members.csv`
- `group_risk_report_<group_name>_<N>members_pairs.csv`
- `group_risk_report_<group_name>_<N>members_devices.csv`
- `group_risk_report_<group_name>_<N>members_counterparts.csv`

---

## 和基础算子的关系

这个技能不是独立底层图系统，而是通过基础能力组合实现。

### 对齐关系
- `group_profile_summary = node_lookup + aggregation_query`
- `high_call_volume_pattern = aggregation_query + relationship_filter`
- `night_abnormal_pattern = relationship_filter`
- `broad_contact_pattern = neighbor_query + aggregation_query`
- `shared_device_pattern = query_shared_device + common_device + subgraph_by_nodes`
- `internal_link_pattern = relationship_filter + subgraph_by_nodes`
- `common_counterparty_pattern = common_neighbor + aggregation_query`

---

## 典型命令示例

### 示例 1：直接分析一组号码
```bash
python3 group_risk_analysis_wrapper.py \
  --group-name classic_group \
  --phone-ids "号码1,号码2,号码3,号码4,号码5" \
  --top-k 10
```

### 示例 2：从文本文件读入群体号码，并只保留共享设备迹象明显的成员
```bash
python3 group_risk_analysis_wrapper.py \
  --group-name device_focus_group \
  --phone-id-file ./sample_group_ids.txt \
  --min-shared-device-count 5 \
  --min-shared-peer-total 50 \
  --top-k 10
```

### 示例 3：只分析风险标签号码
```bash
python3 group_risk_analysis_wrapper.py \
  --group-name risk_only_group \
  --phone-id-file ./sample_group_ids.txt \
  --risk-only \
  --top-k 10
```

### 示例 4：排除 whitelist / normal
```bash
python3 group_risk_analysis_wrapper.py \
  --group-name focused_group \
  --phone-id-file ./sample_group_ids.txt \
  --exclude-sub-labels whitelist,normal \
  --top-k 10
```

---

## 前端提示词建议

### 提示词 1：完整群体分析
请使用 `group-risk-analysis` skill 对下面这组号码做群体级风险分析，并完成：

1. 输出群体规模和总体结论
2. 判断是否存在高通话量型、夜间异常型、联系人广度异常型、共享设备型等主要特征
3. 输出群体核心成员 Top10
4. 输出号码对关系证据链、共享设备证据链与内部子群
5. 生成 markdown 报告和 csv 证据附件

### 提示词 2：更聚焦的设备池群体
请使用 `group-risk-analysis` skill 只保留共享设备迹象明显的成员，并判断该群体是否更像设备池驱动群组。

### 提示词 3：只分析风险成员
请使用 `group-risk-analysis` skill 只分析风险标签成员，并判断当前过滤是否真正改变了群体对象；如果没有改变，请在结果中明确解释原因。
