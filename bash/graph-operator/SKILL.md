---
name: graph-operator
description: 提供电话网络图数据的基础图分析算子，包括节点查询、邻居展开、共享设备、共同对端、共同设备、路径追踪、子图抽取和基础图统计。该 skill 更适合作为上层业务 skill 的底层积木；普通用户问业务结论时应优先路由到对应业务分析 skill。
---

# graph-operator

## 这个 skill 是做什么的

这个 skill 用于对**图结构数据**进行最基础的分析与处理，聚焦于轻量、可直接运行的基础算子，不依赖大型图数据库或完整图分析平台。

当前阶段重点是：
1. 先把基础图分析能力统一收口为 DeerFlow 可调用 skill
2. 再在其上组合形成单号码研判、双号码关联分析、局部团伙图分析等业务型 skill

当前 skill 支持两类 operator：

### 一、8 个核心基础图分析算子
1. `query_phone_node`：查询单个号码节点的基础属性、通话情况和设备情况
2. `expand_neighbors`：展开某个节点的一跳邻居
3. `query_shared_device`：查询某个号码关联的设备，以及这些设备是否还被其他号码共同使用
4. `common_counterparty`：计算两个号码共同联系过的对端
5. `common_device`：计算两个号码共同使用过的设备
6. `path_trace`：追踪两个号码在图中的路径关系
7. `subgraph_extract`：抽取某个号码周围的局部关系图
8. `basic_graph_metrics`：计算图的基础统计信息

### 二、2 个工程辅助 operator
9. `load_graph`：从 edge list / CSV / Parquet 文件加载图或关系表
10. `export_graph`：把图导出为 edgelist / graphml / json

兼容保留的旧名称：
- `shortest_path`：当前对应 `path_trace` 的基础版
- `extract_subgraph`：当前对应 `subgraph_extract` 的旧接口

## 什么时候使用这个 skill

当用户的问题属于下面这些类型时，应该优先使用本 skill：

- “帮我加载这份边表/边列表数据，看看图里有多少节点和边”
- “帮我展开节点 A 的邻居”
- “帮我找 A 到 B 的最短路径”
- “帮我统计这张图的基础指标”
- “帮我抽取一批节点对应的局部子图”
- “帮我把图导出成 GraphML / JSON / edgelist”
- “帮我分析两个号码有没有共同联系过的对端”
- “帮我分析两个号码有没有共同使用过的设备”
- “帮我看这个号码本身的节点信息和基础画像”
- “帮我看这个号码关联了哪些设备，这些设备还被谁共用”
- “帮我看两个号码在图里有没有路径关系，中间经过了谁”
- “帮我围绕某个号码抽取 1 跳或 2 跳的局部关系图”

## 什么时候不要使用这个 skill

下面这些情况不是当前第一版 skill 的目标：

- 大规模分布式图计算
- 需要 GPU 图分析的任务
- 复杂社区发现、动态图、图神经网络训练
- 强依赖图数据库的 Cypher 查询

## 输入约定

本 skill 当前建议通过脚本 `scripts/graph_operator_wrapper.py` 执行，统一输入参数如下：

- `--operator`：算子名称，必填
- `--graph-path`：图数据文件路径，`load_graph` 及其它需要图输入的操作必填
- `--graph-format`：图格式，可选值 `csv` / `edgelist` / `graphml` / `json`，默认 `csv`
- `--source-col`：CSV 源节点列名，默认 `src`
- `--target-col`：CSV 目标节点列名，默认 `dst`
- `--node`：邻居展开时的目标节点
- `--source`：最短路径起点
- `--target`：最短路径终点
- `--nodes`：子图抽取时的节点列表，逗号分隔，如 `A,B,C`
- `--output-path`：导出图时的输出文件路径
- `--export-format`：导出格式，可选值 `edgelist` / `graphml` / `json`
- `--directed`：是否按有向图加载，传入该参数即表示有向图

## 输出约定

所有 operator 都返回统一 JSON，格式如下：

```json
{
  "ok": true,
  "operator": "shortest_path",
  "input_summary": {
    "source": "A",
    "target": "C"
  },
  "result": {
    "path": ["A", "B", "C"],
    "length": 2
  },
  "notes": []
}
```

## 数据路径规则

电话网络图数据优先使用以下候选路径，并在执行前先检查文件是否存在：

1. `/mnt/datasets/phone-network/processed/unified/call_edges.csv`
2. `/mnt/user-data/workspace/imiss-deer-flow-main/datasets/phone-network/processed/unified/call_edges.csv`

执行 graph operator 前，必须先确认实际可用路径。
若候选路径 1 存在，则优先使用候选路径 1。
若候选路径 1 不存在但候选路径 2 存在，则使用候选路径 2。
不要在未检查完上述候选路径前要求用户上传文件。
不要重复安装 `networkx`、`pandas`，因为 sandbox 镜像中已提供这些依赖。

---
name: graph-operator
summary: 基于 NetworkX 的通用图结构基础分析 skill，支持图加载、邻居展开、最短路径、基础图统计和子图抽取。
---


## 内部实现方式

本 skill 当前第一版使用 Python + NetworkX 实现基础算子，执行入口为：

```bash
python scripts/graph_operator_wrapper.py ...
```

## 推荐工作流

### 1. 图加载与检查
先用 `load_graph` 看图是否成功读入，以及节点数、边数是否正常。

### 2. 基础查询
对目标节点做 `expand_neighbors`，快速看其局部结构。

### 3. 路径分析
对两个节点做 `shortest_path`，验证连通关系。

### 4. 统计汇总
对整张图做 `basic_graph_metrics`。

### 5. 局部抽取或导出
按需要做 `extract_subgraph` 或 `export_graph`。

## 参考资料

本 skill 附带的 `references/` 目录用于提供 NetworkX 的基础知识与代码模板：

- `graph-basics.md`：基础建图与常用操作
- `algorithms.md`：路径、连通性、中心性等算法示例
- `io.md`：图输入输出、格式转换、pandas 互转
- `README_SHORT.md`：当前 skill 最小可运行版说明

本 skill 运行在定制 sandbox 中，`networkx`、`pandas`、`duckdb`、`pyarrow` 已预装。
执行时不要主动安装依赖，除非明确检测到 import 失败。

## 使用注意事项

1. 对电话网络通话边文件来说，通常：
   - `src_user_id` 表示主叫 / 用户号码
   - `dst_counterparty_id` 表示被叫或对端号码

2. `path_trace` 当前第一版基于单张关系图上的最短路径搜索。
   - 如果使用 `call_edges.csv`，表示沿“号码 -> 对端号码”的关系寻找路径
   - 若不加 `--directed`，默认按无向图分析
   - 若加 `--directed`，则按有向路径分析

3. `subgraph_extract` 当前第一版基于 ego graph（局部邻域子图）。
   - 推荐使用 `--center-node` 指定中心号码
   - 推荐配合 `--hops` 控制抽取范围（1 跳 / 2 跳）
   - 推荐配合 `--max-nodes` 控制返回规模
   - 当局部子图过大时，会进行截断，但会优先保留中心节点和距离更近的节点

4. `query_phone_node` 适合做单号码基础画像；
   `query_shared_device`、`common_device`、`common_counterparty` 适合做号码关联分析；
   `path_trace`、`subgraph_extract` 适合做局部结构分析。

5. `load_graph` 和 `export_graph` 属于工程辅助 operator，
   不属于“8 个核心基础图分析算子”，但用于读图和导图很重要。
