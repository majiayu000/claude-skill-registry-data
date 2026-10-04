---
name: association-path-analysis
description: 分析两个电话号码之间是否存在直接通话路径、间接多跳路径、共享设备路径、共同对端路径或复合桥接链路。适用于用户询问两个号码如何关联、是否存在中间节点或关系链路的场景；不用于数据概览、TopN 风险发现、单号码画像、群体团伙识别或跨省同实体联动判断。
---

# association-path-analysis

## 这个 skill 是做什么的

这个 skill 用于分析**两个号码之间的关联路径**，支持两层分析：

1. **direct_call_analysis**  
   基于电话网络原始通话边图，按**有向图**分析号码 A 是否能沿着通话方向到达号码 B。

2. **composite_analysis**  
   把三类关系联合起来做复合路径分析：
   - `call`（通话关系）
   - `shared_device`（共享设备关系）
   - `common_counterparty`（共同对端关系）

它不只是看“有没有通话路径”，而是分析两个号码在当前标准图数据内是否存在**多关系混合连接**。它不负责判断跨省同一真实实体，也不应替代 `dataset-quality-and-linkability-diagnostic` 的跨省可联动性诊断。

---

## 实际调用脚本

脚本位置：

`/mnt/skills/custom/phone-network-analysis/association-path-analysis/scripts/association_path_wrapper.py`

---

## 适合回答什么问题

当用户的问题属于下面这些类型时，优先使用本 skill：

- 帮我看这两个号码有没有关系
- 这两个号码之间怎么连起来的
- 这两个号码有没有间接联系
- 中间桥接号码是谁
- 除了通话关系以外，它们有没有设备共用或者共同对端
- 请做复合路径分析
- 两个号码是否通过共同设备或共同对端连起来
- 给我 Top-K 候选路径
- 给我桥接点排序和下一步调查建议

---

## 默认数据源

### 通话边图
- `/mnt/datasets/phone-network/processed/unified/call_edges.csv`

字段：
- `src_user_id`
- `dst_counterparty_id`

### 号码-设备图
- `/mnt/datasets/phone-network/processed/graph_views/unified/edges_phone_imei.parquet`

字段：
- `user_id`
- `imei`

---

## 默认行为

### 通话路径
默认按**有向图**分析，也就是优先保留真实通话方向：
- `src_user_id -> dst_counterparty_id`

### 复合路径
默认联合启用三类关系：
- `call`
- `shared_device`
- `common_counterparty`

---

## 参数说明

- `--phone-a`：号码 A
- `--phone-b`：号码 B
- `--analysis-mode`：
  - `direct_call`：只做有向通话路径分析
  - `composite`：只做复合关系路径分析
  - `both`：同时做直接配对信号 + 有向通话路径 + 复合路径分析
- `--max-hops`：复合路径搜索最大跳数
- `--top-k`：返回候选路径数量
- `--per-relation-limit`：每类关系最大扩展数
- `--max-expand-nodes`：复合搜索最大扩展节点数
- `--min-common-counterparty`：建立共同对端关系边的最低共同对端数
- `--directed-call`：是否按有向通话图分析（默认开启）

---

## 前端首测推荐参数

首次测试建议优先使用：

- `analysis_mode=both`
- `max_hops=3`
- `top_k=1`
- `per_relation_limit=20`
- `max_expand_nodes=500`
- `min_common_counterparty=2`

如果第一轮稳定返回，再逐步放宽到：

- `top_k=3`
- `per_relation_limit=30`
- `max_expand_nodes=800`

不建议首次直接请求 Top-3 候选路径、桥接点全量排序和超大范围复合搜索。

---

## 推荐输出内容

前端分析建议固定输出以下结构：

1. 直接配对信号
   - A 是否直接打给 B
   - B 是否直接打给 A
   - 共享设备数
   - 共同对端数
2. 有向通话路径分析
3. 最优复合路径分析
4. Top-K 候选路径
5. 桥接点 / 关键证据节点排序
6. 下一步调查建议
7. `report_path`

---

## 文件交付要求（必须遵守）

当脚本返回 `report_path` 后：

1. 必须检查该文件是否存在
2. 必须把该 Markdown 文件作为最终报告产物交付
3. 不要只输出路径字符串
4. 若前端支持文件展示卡片，应优先展示报告文件
5. 若脚本返回 `artifacts`，应把其中的 markdown 报告作为最终附件展示

推荐检查方式：

```bash
REPORT_PATH="/mnt/user-data/outputs/association_path_report_xxxxxxxx_yyyyyyyy_both.md"
test -f "$REPORT_PATH" && echo "REPORT_EXISTS"
```

若文件存在，再组织最终回答。

---

## 执行方式

```bash
cd /mnt/skills/custom/phone-network-analysis/association-path-analysis/scripts && python3 association_path_wrapper.py \
  --phone-a "<PHONE_A>" \
  --phone-b "<PHONE_B>" \
  --analysis-mode both \
  --max-hops 3 \
  --top-k 1 \
  --per-relation-limit 20 \
  --max-expand-nodes 500 \
  --min-common-counterparty 2
```

---

## 与 YiGraph 的关系

这个 skill 不是直接把 YiGraph 整套系统部署到 DeerFlow 中，而是：

- 复用了 YiGraph 的查询能力分类思路
- 复用了 YiGraph 风格的路径分析与解释逻辑
- 结合 DeerFlow 当前电话网络数据结构，做了适配后的高级分析实现

所以它属于：

**YiGraph 风格 + DeerFlow 可运行版的高级分析 skill**
