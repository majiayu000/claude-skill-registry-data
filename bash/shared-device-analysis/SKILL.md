---
name: shared-device-analysis
description: 分析电话号码与设备之间的共享关系，支持单号码共享设备扩散、两个号码是否共用设备、单设备挂载号码和设备池线索分析。适用于共享设备/同设备池问题；输出仅作为风险线索，不等同于最终团伙认定或可靠跨省同实体联动判断。
---

# shared-device-analysis

## 作用
用于分析号码之间是否存在共享设备关系，识别同一设备下关联的号码对象，并辅助发现可疑群组、高风险关联线索和重点设备池。

这是一个**电话网络业务层 skill**，不是底层算子本身。它主要通过组合以下基础能力实现：

- `query_shared_device`
- `common_device`
- `query_phone_node`
- `relationship_filter`
- `subgraph_by_nodes`

分析风格对齐 YiGraph 中“关系过滤 + 共同邻居 + 证据节点继续下钻”的思路。

---

## 支持的分析模式

### 1. pair
分析两个号码是否存在共用设备关系。

输出重点：
- 共用设备数量
- 关系强度（none / medium / strong）
- 共用设备明细
- 额外同设备关联号码
- 共享设备证据包
- 下一步联动建议

### 2. phone
分析一个号码的共享设备扩散关系。

输出重点：
- 设备总数
- 共享设备数
- Top 共享设备
- Top 同设备关联号码
- 团伙/设备池信号
- 省份分布 / 跨省表面信号（仅作为数据线索，不等同于可靠跨省同实体联动判断）
- 混合标签共享设备信号
- 下一步联动建议

### 3. device
把设备本身当成分析对象，查看其挂载的号码对象。

输出重点：
- 挂载号码数
- 风险号码数与占比
- 聚集强度
- 重点设备池信号
- Top 关联号码
- 省份分布 / 标签分布
- 下一步联动建议

---

## 参数说明

### 通用参数
- `--mode pair|phone|device`
- `--top-k 10`
- `--min-shared-phone 1`：相关号码至少共用多少台设备才保留
- `--min-device-phone-count 2`：设备至少挂载多少号码才算“共享设备”
- `--risk-only`：只保留风险标签号码

### pair 模式
- `--phone-a <PHONE_A>`
- `--phone-b <PHONE_B>`

### phone 模式
- `--phone-id <PHONE_ID>`

### device 模式
- `--device-id <DEVICE_ID>`

---

## 标准调用示例

### pair
```bash
cd /mnt/skills/custom/phone-network-analysis/shared-device-analysis/scripts && python3 shared_device_analysis_wrapper.py \
  --mode pair \
  --phone-a "<PHONE_A>" \
  --phone-b "<PHONE_B>" \
  --top-k 10 \
  --min-shared-phone 1 \
  --min-device-phone-count 2
```

### phone
```bash
cd /mnt/skills/custom/phone-network-analysis/shared-device-analysis/scripts && python3 shared_device_analysis_wrapper.py \
  --mode phone \
  --phone-id "<PHONE_ID>" \
  --top-k 10 \
  --min-shared-phone 1 \
  --min-device-phone-count 2
```

### device
```bash
cd /mnt/skills/custom/phone-network-analysis/shared-device-analysis/scripts && python3 shared_device_analysis_wrapper.py \
  --mode device \
  --device-id "<DEVICE_ID>" \
  --top-k 20 \
  --min-device-phone-count 2
```

---

## 前端测试推荐提问

### Q1：两个号码是否共用设备
请使用 shared-device-analysis skill 分析这两个号码是否存在共用设备关系，输出共用设备数、关系强度、Top 共用设备、额外同设备号码，并生成 markdown 报告和 csv 明细。

### Q2：单号码共享设备扩散
请使用 shared-device-analysis skill 对这个号码做共享设备扩散分析，输出设备总数、共享设备数、Top 共享设备、Top 同设备关联号码、团伙/设备池信号，并生成 markdown 报告和 csv 明细。

### Q3：单设备挂载号码分析
请使用 shared-device-analysis skill 分析这台设备关联了哪些号码，输出挂载号码数、风险号码数、聚集强度、Top 关联号码，并生成 markdown 报告和 csv 明细。

---

## 输出文件
脚本会在 `/mnt/user-data/outputs/` 或兼容输出目录下自动生成：

- Markdown 报告
- CSV 明细

返回 JSON 中会包含：
- `report_path`
- `csv_path`
- `artifacts`

---

## 结果解释注意事项
1. “高可疑/重点设备池”表示分析线索，不等于最终风险认定；若数据集是当前 unified，任何跨省共享设备类表述都只能作为表面统计或数据线索，不能说成可靠跨省同实体联动结论。
2. `risk_only` 只影响输出对象范围，不改变底层原始设备关系。
3. `min-device-phone-count` 可以过滤掉“一机一号”这类弱信号设备，让结果更聚焦。
4. 如果 pair 模式没有共用设备，不代表两号码没有关系，只说明“共享设备证据不存在”，此时应联动：
   - `overlap-analysis`
   - `association-path-analysis`
   - `single-number-analysis`
