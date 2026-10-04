---
name: overlap-analysis
description: 分析两个电话号码之间的关系重叠情况，包括共同对端、共享设备、直接通话、重叠比例和关键证据点。适用于用户询问两个号码有没有共同联系人、共同设备或联系圈重叠；不负责多跳路径解释、单号画像、群体分析或地域对比。
---

# overlap-analysis

## 这个 skill 是做什么的

这是一个 **YiGraph 风格的重叠关系分析 skill**，专门回答“两个号码到底重叠了多少、重叠在哪些地方、这种重叠是否异常”这类问题。

它不重点回答“这两个号码怎么连起来”，那是 `association-path-analysis` 的职责；
它重点回答的是：

- 两个号码有没有 **共同对端**
- 两个号码有没有 **共享设备**
- 两个号码有没有 **直接通话**
- 这些重叠关系的 **数量、比例、强弱等级**
- 哪些共同对端 / 共享设备是最值得优先核查的 **关键证据点**
- 下一步应该优先查什么

它属于一个 **高级分析 skill**，建立在基础算子 `graph-operator` 之上，用于把基础查询结果包装成更像 YiGraph 的业务解释输出。

---

## 和 YiGraph 的关系

这个 skill 主要对齐 YiGraph 里的这几类能力：

1. **Graph Query / common_neighbor**
   - 对应“两个节点的共同邻居是谁”
   - 在电话网络任务里，对应“两个号码的共同对端是谁”

2. **relationship_filter / aggregation_query**
   - 对应“边和关系的筛选、计数、聚合”
   - 在电话网络任务里，对应“共享设备数、共同对端数、重叠率、强弱分级”

3. **YiGraph 风格的解释层**
   - 不只返回原始列表，还返回：
     - 重叠强度判断
     - Top 证据节点
     - 风险提示
     - 下一步调查建议

也就是说，这个 skill 不是直接把 YiGraph 的原始服务搬进来，而是：

**复用 YiGraph 的问题分类方式 + 查询能力映射方式 + 解释风格，结合你当前电话网络数据做适配实现。**

---

## 实际调用脚本

`/mnt/skills/custom/phone-network-analysis/overlap-analysis/scripts/overlap_analysis_wrapper.py`

---

## 推荐调用方式

```bash
cd /mnt/skills/custom/phone-network-analysis/overlap-analysis/scripts && python3 overlap_analysis_wrapper.py \
  --phone-a "<PHONE_A>" \
  --phone-b "<PHONE_B>" \
  --top-k 10 \
  --min-common-counterparty 1
```

---

## 参数说明

- `--phone-a`：号码 A
- `--phone-b`：号码 B
- `--call-graph-path`：通话边文件，默认 `/mnt/datasets/phone-network/processed/unified/call_edges.csv`
- `--device-graph-path`：号码-设备边文件，默认 `/mnt/datasets/phone-network/processed/graph_views/unified/edges_phone_imei.parquet`
- `--graph-format`：通话边文件格式，默认 `csv`
- `--source-col`：通话边起点列，默认 `src_user_id`
- `--target-col`：通话边终点列，默认 `dst_counterparty_id`
- `--device-source-col`：号码-设备边起点列，默认 `user_id`
- `--device-target-col`：号码-设备边终点列，默认 `imei`
- `--top-k`：返回多少个共同对端 / 共享设备证据预览，默认 `10`
- `--min-common-counterparty`：判定“共同对端重叠”时的最低证据数门槛，默认 `1`

---

## 推荐输出结构

前端分析时，建议固定输出下面这几部分：

1. **直接配对信号**
   - A→B 是否直接通话
   - B→A 是否直接通话

2. **共同对端重叠分析**
   - A 的对端数
   - B 的对端数
   - 共同对端数
   - Jaccard 重叠率
   - Top-K 共同对端证据

3. **共享设备重叠分析**
   - A 的设备数
   - B 的设备数
   - 共享设备数
   - Jaccard 重叠率
   - Top-K 共享设备证据

4. **综合重叠强度判断**
   - strong / medium / weak / none

5. **关键证据点排序**
   - 哪些共同对端最值得查
   - 哪些共享设备最值得查

6. **下一步调查建议**

7. **Markdown 报告**

---

## 这个 skill 适合回答哪些问题

- “这两个号码有没有共同联系人？”
- “这两个号码的重叠关系强不强？”
- “它们有没有共享设备？”
- “这两个号码是否属于同一个联系圈？”
- “共同对端多不多？值不值得继续查？”
- “共享设备是不是异常强证据？”

---

## 和 association-path-analysis 的区别

- `association-path-analysis`：回答 **怎么连起来的**
- `overlap-analysis`：回答 **重叠得有多强**

你可以把它理解成：

- 路径 skill 负责“链路”
- overlap skill 负责“重合度”

两者是互补关系，不是重复关系。

---

## 前端首测推荐参数

建议先用：

- `top_k=10`
- `min_common_counterparty=1`

如果结果太泛，再逐步收紧到：

- `top_k=5`
- `min_common_counterparty=2`

---

## 文件输出说明（必须遵守）

脚本会自动生成 Markdown 报告，并保存到：

`/mnt/user-data/outputs/`

### 前端执行时的强制要求

当 `overlap_analysis_wrapper.py` 返回 JSON 后：

1. 必须读取返回结果中的 `report_path`
2. 必须确认该文件存在
3. 最终回复中必须把这个 Markdown 文件作为最终产物交付
4. 不要只打印 `report_path` 这个字符串

### 推荐执行流程

先执行分析脚本，例如：

```bash
cd /mnt/skills/custom/phone-network-analysis/overlap-analysis/scripts && python3 overlap_analysis_wrapper.py \
  --phone-a "<PHONE_A>" \
  --phone-b "<PHONE_B>" \
  --top-k 10 \
  --min-common-counterparty 1
```

如果返回结果里有：

- `report_path`

则继续确认文件存在：

```bash
test -f "<REPORT_PATH>" && echo "REPORT_EXISTS"
```

然后在最终回答中：

- 正常展示分析结果
- 单独列出报告文件路径
- 把该 Markdown 文件作为最终报告产物返回

### 说明

如果前端只显示路径文本而没有下载卡片，这通常不是分析脚本失败，而是文件交付动作没有被明确执行。
因此，调用本 skill 时，必须把“报告文件交付”当成最后一步，而不是只展示路径。
