---
name: "ascend-cluster-compare"
description: "Ascend cluster comparison tool. Invoke when user asks to compare two cluster datasets (DB or TEXT), or to generate cluster_analysis_output from raw profiling data via msprof-analyze and then compare."
---

# 昇腾集群比对分析

本 skill 只做一件事：**比对两个集群的 profiling 数据**，定位性能差异并输出劣化归因 HTML 报告。从 `cluster_analysis_output` 目录（DB 或 TEXT 格式）提取数据；若用户没有现成的 `cluster_analysis_output`，先用 `msprof-analyze cluster` 生成，再执行比对。

## 触发场景

当用户出现以下意图时触发：
- "比对两个集群"、"对比正常和异常集群"、"cluster compare"
- 用户提供两个 `cluster_analysis_output` 目录、`cluster.db` 文件或 `cluster_step_trace_time.csv` 路径
- 用户提供原始 profiling 数据目录（如多张卡的 `*_ascend_pt` 目录），要求生成比对结果

**不适用**：单集群整体分析、单卡分析、专家建议（advisor）、GPU/NPU 性能比对（compare 工具）。这些不属于本 skill 范围。

## 核心工作流（必须严格遵循）

### 阶段 0: 数据准备（仅当用户没有现成的 cluster_analysis_output 时）

#### 步骤 0.1: 判断是否需要生成

检查用户提供的两个集群路径下是否已有可用数据：
- **DB 模式**：`cluster.db`（旧格式，根目录）或 `cluster_analysis_output/cluster_analysis.db`（新格式）
- **TEXT 模式**：`cluster_step_trace_time.csv` + `communication_group.json`（直接位于路径下或 `cluster_analysis_output/` 子目录内）

两类满足其一即可；若路径下只有原始 profiling 数据（如 `*_ascend_pt` 目录），则进入步骤 0.2 生成。

#### 步骤 0.2: 检查并安装 msprof-analyze

1. **检查是否已安装**：执行 `msprof-analyze --version`（或 `msprof-analyze --help`），能正常输出版本/帮助信息即已安装。
2. **未安装则安装**（要求 Python 3.7.5 及以上，建议 3.9+）：
   ```bash
   pip install msprof-analyze
   ```
   - 指定版本：`pip install msprof-analyze==<CANN版本号>`（不明确时用最新版）
3. **验证安装**：再次执行 `msprof-analyze --help`，不报错且能显示帮助即安装成功；若提示命令不存在，确认当前终端使用的是安装了 msprof-analyze 的 Python 环境。

#### 步骤 0.3: 执行 cluster 分析生成 cluster_analysis_output

```bash
msprof-analyze cluster -m all -d <profiling_path> -o <output_path>
```

| 参数 | 说明 |
| --- | --- |
| `-d / --profiling_path` | 必选。集群性能数据根目录，需包含**同一次采集**的多张卡 profiling 子目录（如 `dp0_pp0_tp0_..._rank0_..._ascend_pt/`）。不要混入不同批次或缺失 rank，否则通信矩阵映射可能不准确 |
| `-m / --mode` | 可选。`communication_matrix`（通信矩阵）/ `communication_time`（通信耗时）/ `all`（默认，两者都解析）。比对场景建议 `all` |
| `-o / --output_path` | 可选。自定义输出路径；未指定时在 `-d` 目录下自动创建 `cluster_analysis_output` |
| `--force` | 可选。跳过属主、权限、文件过大（csv>5GB / json>10GB / db>8GB）校验，强制执行 |

生成后的输出文件：
- **TEXT 输入**：`cluster_step_trace_time.csv`（迭代耗时拆解）、`cluster_communication.json`（通信算子耗时）、`cluster_communication_matrix.json`（通信矩阵）、`communication_group.json`（通信域信息）
- **DB 输入**：`cluster_analysis.db`（包含 ClusterBaseInfo、ClusterStepTraceTime、CommunicationGroupMapping、ClusterCommunicationTime、ClusterCommunicationBandwidth、ClusterCommunicationMatrix 表）

对两个集群分别执行生成。注意事项：
- 采集时 `profiler_level` 需为 Level1 及以上，否则无通信小算子数据，仅能汇总 step_trace_time（通信带宽/矩阵缺失）
- 支持仅转存 `analysis.db` + `profiler_info_*.json`（保留目录结构）用于超大集群分析
- 生成后回到阶段 1，使用新产生的 `cluster_analysis_output` 作为数据源

### 阶段 1: 数据识别与全景提取（对集群 A、B 分别执行）

#### 步骤 1.1: 识别数据格式

- **DB 模式**：路径下存在 `cluster.db`（旧格式）或 `cluster_analysis_output/cluster_analysis.db`（新格式）
- **TEXT 模式**：路径下存在 `cluster_step_trace_time.csv` + `communication_group.json`
- **混合模式**：同时存在 DB 和 TEXT 文件（优先使用 DB）

#### 步骤 1.2: 提取全景数据

**DB 模式 SQL 查询**（参考 `references/db_schema.md` 获取完整表结构）：

```sql
-- 1. 集群基础信息
SELECT key, value FROM cluster_base_info;
-- 或新格式: SELECT * FROM CommunicationGroupMapping;

-- 2. Step 时间全景（核心表）
SELECT step_id, AVG(compute_time), AVG(pure_communication_time),
       AVG(overlap_communication_time), AVG(communication_time),
       AVG(free_time), AVG(stage_time), AVG(bubble_time), AVG(preparing)
FROM step_statistic_info GROUP BY step_id;
-- 新格式表名: ClusterStepTraceTime, 字段名略有不同

-- 3. 各 Rank 时间明细
SELECT rank_id, step_id, compute_time, communication_time, free_time, stage_time
FROM step_statistic_info ORDER BY step_id, rank_id;

-- 4. 通信时间汇总（如有数据）
SELECT hccl_op_name, AVG(elapsed_time), AVG(transit_time), AVG(wait_time),
       AVG(synchronization_time), AVG(idle_time)
FROM ClusterCommunicationTime GROUP BY hccl_op_name;

-- 5. 通信带宽汇总（如有数据）
SELECT band_type, AVG(bandwidth), AVG(transit_size), AVG(transit_time)
FROM ClusterCommunicationBandwidth GROUP BY band_type;

-- 6. 通信矩阵（如有数据）
SELECT src_rank, dst_rank, transport_type, AVG(bandwidth), AVG(transit_size)
FROM ClusterCommunicationMatrix GROUP BY src_rank, dst_rank, transport_type;

-- 7. Rank/Host 总数
SELECT COUNT(DISTINCT rankId) FROM RankDeviceMap;
SELECT COUNT(DISTINCT hostUid) FROM HostInfo;
```

**TEXT 模式文件解析**（参考 `references/text_schema.md`）：
- 读取 `cluster_step_trace_time.csv`：解析 Step/Type/Index/Computing/Communication/Free/Stage 等列
- 读取 `communication_group.json`：解析 collective/p2p 通信组信息，提取 rank 列表作为基础信息
- 读取 `cluster_communication.json`（如有）：解析通信算子耗时统计，提取 Top10 算子的 elapsed/transit/wait/sync 时间
- 读取 `cluster_communication_matrix.json`（如有）：解析 4 层嵌套 JSON 通信矩阵，提取 src_rank/dst_rank/transport_type/bandwidth/transit_size，按传输类型（LOCAL/HCCS/RDMA）聚合带宽
- **路径检测**：支持 `data_dir/cluster_step_trace_time.csv` 或 `data_dir/cluster_analysis_output/cluster_step_trace_time.csv` 两种结构
- **单位注意**：TEXT 模式 JSON 中时间单位为 ms（毫秒），DB 模式为 μs（微秒），脚本需自动适配

#### 步骤 1.3: 内嵌进阶分析（提取时同步执行，默认开启）

提取器 `cluster_data_extractor.py` 生成单集群 JSON 时会**同步执行进阶分析**，并把结果嵌入 JSON 的 `advanced_analysis` 字段——进阶分析在比对之前即已完成，比对报告自动携带渲染，无需额外操作。

默认执行的特性（scope=single，记录含 `embedded: true`）：
- **free_analysis**：空闲时间成因聚合（Reason 分布、次数、总时长、占比）
- **communication_bottleneck**：通信瓶颈算子 Top N（慢/快 Rank 耗时差与推断原因）

行为说明：
- 提取器自动探测 msprof-analyze 可用性与数据前置条件；特性不可用时在 `advanced_analysis.features[].status` 标注原因（failed / not_available），不阻塞提取主流程
- 工具输出缓存于 `<data-dir>/advanced_work/`，重复提取时默认复用（status=cached）；用 `--force-advanced` 忽略缓存重跑
- 成功/缓存命中的 feature 会同步生成中文「分析与判断」，写入 `features[].analysis` 字段（由 `scripts/advanced_insights.py` 规则化生成），随单集群 JSON 落盘；HTML/MD 比对报告渲染时直接复用，保证口径一致

内嵌进阶分析可选参数：

| 参数 | 说明 |
| --- | --- |
| `--no-advanced` | 跳过内嵌进阶分析（仅提取基础数据） |
| `--msprof <path>` | 指定 msprof-analyze 可执行文件名/路径 |
| `--advanced-work-dir <path>` | 指定进阶分析工具输出目录（默认 `<data-dir>/advanced_work/`） |
| `--advanced-top-num <n>` | communication_bottleneck 的 Top N 数量（默认 10） |
| `--force-advanced` | 忽略缓存，强制重跑进阶分析 |

> 双集群时间拆解对比（cluster_time_compare_summary）不属于内嵌范围，如需该结果见阶段 2.5。

#### 步骤 1.4: 生成 MD 总结文件

对每个集群，将提取的全部数据组织为结构化 Markdown，保存到该集群的**原始数据文件夹**下（如 `{data_dir}/cluster_data_summary.md`）。

> **双集群比对 MD 报告无需手工编写**：阶段 2 使用 `scripts/generate_cluster_md.py` 自动生成（章节与 HTML 比对报告对应，含进阶分析「分析与判断」与「综合判断」），全部内容中文输出。

MD 文件必须包含以下章节：
1. **集群概览**：Rank 数量、Step 数量、采集时间、并行策略（TP/PP/DP）、算法类型
2. **Step 时间统计**：各 Step 的平均计算/通信/空闲/Stage 时间（μs 和 ms 双单位）
3. **Rank 级明细**：每个 Rank 在各 Step 的时间分解表
4. **负载分布分析**：计算 vs 通信 vs 空闲的占比数据
5. **通信分析**（如有数据）：通信算子耗时 Top10、带宽汇总、通信矩阵
6. **异常 Rank 识别**：偏离均值超过 10% 的 Rank（慢卡/快卡）
7. **数据完整性说明**：哪些表有数据、哪些表为空

**单位换算规则**：原始数据单位为微秒（μs），报告展示时需除以 1000 转换为毫秒（ms）。

### 阶段 2: 计算差异并渲染比对报告（HTML / MD 双格式）

**HTML 使用模板**：`templates/cluster_compare_report.html`；**MD 使用脚本**：`scripts/generate_cluster_md.py`（复用同一套指标计算，与 HTML 结论一致）

1. **计算差异**：
   - 整体差值：ΔStage = Stage_B − Stage_A
   - 一级归因（贡献度，带**显著性门控**）：当 |ΔStage / Stage_A| < 1% 时 ΔStage 趋近 0，各分项变化互相抵消，贡献度比值会爆炸（如 368.5% / −123.4%）且不可解释，此时贡献度降级为 "—" 并在 KPI 卡说明原因；仅 |增幅| ≥ 1% 时计算：
     - 计算贡献度 = (ΔCompute / ΔStage) × 100%
     - 通信贡献度 = (ΔComm / ΔStage) × 100%
     - 空闲贡献度 = (ΔFree / ΔStage) × 100%
     - 贡献度可超 100% 或为负（分项变化方向相反、相互抵消所致），解读时以"占 Stage 变化比例、各分项可相互抵消"口径说明，不得简单当作"占比"
   - 二级算子归因：通信时间差值 Top5 算子
   - 带宽劣化：各 band_type 均值带宽下降百分比 + **有效吞吐**（总传输量/总传输时间，SUM/SUM 或 avg_size/avg_time）对比
2. **渲染比对报告**，报告包含：
   - **核心 KPI 卡片**：Stage 耗时增幅、通信变化贡献度（带显著性门控与配色说明）、计算变化贡献度、带宽变化（均值口径 + 有效吞吐口径）、集群规模对比
   - **Step 核心耗时对比**：并排柱状图（集群A vs 集群B），按 Step 分组
   - **负载类型转换**：双饼图对比（A 的计算/通信/空闲占比 vs B 的占比）
   - **劣化归因瀑布图**：计算/通信/空闲对总劣化的贡献度分解
   - **通信算子差异 Top10**：表格 + 柱状图，展示耗时差最大的算子
   - **带宽对比柱状图**：各 band_type 的 A vs B 带宽对比
   - **Rank 级差异热力图**：每个 Rank 的 Stage 时间差值
   - **劣化根因总结 & 行动建议**：P0/P1/P2 优先级问题列表
   - **进阶分析章节**：`{{ADVANCED_ANALYSIS_HTML}}` 自动合并渲染两路结果——集群 A/B JSON 内嵌的 `advanced_analysis`（阶段 1 提取时已同步执行，同名 feature 按集群归属 A/B 对照展示）与 `--advanced` 外部 JSON（含双集群时间拆解对比）；两者皆无时显示引导卡；每个进阶 feature 卡片尾部渲染中文**「分析与判断」**块，A/B 对照展示时追加**「综合判断（基准 vs 对比）」**块（结论由 `scripts/advanced_insights.py` 规则化生成，优先复用单集群 JSON 内嵌 `analysis` 字段）
3. **生成 MD 比对报告**（与 HTML 同步，结论一致）：
   ```bash
   python scripts/generate_cluster_md.py --data-a <a.json> --data-b <b.json> --output compare.md
   # 可选: 追加 --advanced 外部进阶分析 JSON; --top-ranks 控制 Rank 级差异表行数（默认 20，0=全部）
   python scripts/generate_cluster_md.py --data-a <a.json> --data-b <b.json> --output compare.md --advanced <advanced_analysis.json>
   ```
   MD 报告含八章节：一、综合结论 / 二、核心指标对比 / 三、劣化根因 / 四、行动建议 / 五、Step 级耗时对比 / 六、Rank 级差异 / 七、通信算子差异 / 八、进阶分析（含「分析与判断」与「综合判断（基准 vs 对比）」），全部中文输出。

### 阶段 2.5: 进阶分析补充（msprof-analyze -m，可选）

free_analysis / communication_bottleneck 已在阶段 1 内嵌完成（提取单集群 JSON 时同步执行），比对报告会自动合并渲染，**无需重复执行**。本阶段仅作为可选补充手段，用于获取单集群内嵌不包含的**双集群时间拆解对比**：

1. 运行 `scripts/run_advanced_analysis.py --cluster-a <A数据目录> --cluster-b <B数据目录> --output <advanced_analysis.json>`
2. 脚本自动探测工具可用性、双集群数据格式与前置表，按需补跑 `cluster_time_summary`，再执行进阶特性：
   - **cluster_time_compare_summary**（仅 DB，--bp 指基准）：双集群 rank/step 级时间指标对比，输出总体指标均值差与 Top 差异 Rank
   - **free_analysis / communication_bottleneck**：对集群 A、B **分别执行**，结果标注 `cluster: A/B`，工具输出目录隔离在 `<work-dir>/cluster_A/`、`<work-dir>/cluster_B/`；命中阶段 1 内嵌缓存时直接复用（status=cached），用 `--force` 忽略缓存重跑
3. 输出 JSON 后重新生成报告：`scripts/generate_cluster_report.py ... --advanced <advanced_analysis.json>`（HTML）或 `scripts/generate_cluster_md.py ... --advanced <advanced_analysis.json>`（MD），报告将内嵌结果与外部结果自动合并渲染（time_cmp 取外部结果；单集群 feature 优先取内嵌，缺失时回退外部）
4. 特性不可用时（无 DB、缺表、工具缺失）脚本会标注 reason，报告对应卡片显示原因，不阻塞主报告

### 阶段 3: 输出与交付

1. 单集群 MD 总结文件保存到各集群的原始数据文件夹（每个集群一份）
2. HTML 比对报告保存到用户指定输出路径，未指定时保存到集群 A 的数据目录下（如 `cluster_compare_report.html`）
3. MD 比对报告与 HTML 同步生成（`scripts/generate_cluster_md.py`），输出路径未指定时与 HTML 同目录（如 `cluster_compare_report.md`）
4. 向用户展示报告摘要（关键发现 + 数据链接）

## 数据格式兼容

本 skill 必须同时兼容两种数据格式：

| 维度 | DB 模式（旧格式） | DB 模式（新格式） | TEXT 模式 |
|------|------------------|------------------|-----------|
| **DB 文件名** | `cluster.db`（根目录） | `cluster_analysis.db`（cluster_analysis_output/ 下） | 无 DB 文件 |
| **Step 时间表** | `step_statistic_info` | `ClusterStepTraceTime` | `cluster_step_trace_time.csv` |
| **通信时间表** | `communication_time_info` | `ClusterCommunicationTime` | `cluster_communication.json` |
| **通信带宽表** | `communication_bandwidth_info` | `ClusterCommunicationBandwidth` | `cluster_communication_matrix.json`（按传输类型聚合） |
| **通信矩阵表** | `communication_matrix` | `ClusterCommunicationMatrix` | `cluster_communication_matrix.json`（4 层嵌套 JSON） |
| **基础信息表** | `cluster_base_info` | `CommunicationGroupMapping` | `communication_group.json` |
| **字段名差异** | `compute_time` | `computing` | `Computing` |
| **字段名差异** | `communication_time` | `communication` | `Communication` |
| **字段名差异** | `free_time` | `free` | `Free` |
| **字段名差异** | `stage_time` | `stage` | `Stage` |
| **字段名差异** | `rank_id` | `index`（SQL 保留字，需双引号包裹） | `Index` |
| **时间单位** | μs | μs | μs（CSV）/ ms（JSON 通信数据） |
| **路径检测** | `data_dir/cluster.db` | `data_dir/cluster_analysis_output/cluster_analysis.db` | `data_dir/cluster_step_trace_time.csv` 或 `data_dir/cluster_analysis_output/cluster_step_trace_time.csv` |

**字段映射策略**：提取数据时先检查表存在性和列名，自动适配对应字段名。

## 脚本工具

### 数据提取脚本

`scripts/cluster_data_extractor.py`：自动识别数据格式，执行 SQL/CSV 提取，输出 JSON 格式的结构化数据。**默认在提取时同步执行进阶分析**（free_analysis / communication_bottleneck），结果嵌入 JSON 的 `advanced_analysis` 字段（比对前即已获得）；特性不可用时标注原因，不阻塞提取。

```bash
python scripts/cluster_data_extractor.py --data-dir <path> --output <output.json>
```

内嵌进阶分析可选参数（单行追加执行）：`--no-advanced`（跳过内嵌进阶分析）、`--msprof <path>`（指定工具路径）、`--advanced-work-dir <path>`（工具输出目录，默认 `<data-dir>/advanced_work/`）、`--advanced-top-num <n>`（Top N，默认 10）、`--force-advanced`（忽略缓存重跑）。

### 比对报告生成脚本

`scripts/generate_cluster_report.py`：基于两个集群的提取数据生成 HTML 比对报告（仅支持比对模式）。内置带宽劣化智能解读：均值带宽下降但有效吞吐一致时判定为"统计口径差异"（绿色提示），不作为链路劣化依据；仅有效吞吐下降 ≥5%（轻微）/ ≥15%（严重）才判定为真实劣化。贡献度 KPI 带显著性门控：|ΔStage/Stage_A| < 1% 时展示 "—" 并说明原因，避免 ΔStage 趋近 0 时贡献度爆炸（368.5% / −123.4%）。**进阶分析自动合并渲染**：默认读取 data-a/data-b JSON 内嵌的 `advanced_analysis`（阶段 1 提取时已同步执行），同名 feature 按集群归属在同一卡片内对照展示（集群A · 基准 / 集群B · 对比）；`--advanced` 外部 JSON 作为补充来源合并（time_cmp 仅外部提供；单集群 feature 优先取内嵌，缺失时回退外部）；两者皆无时显示引导卡。**进阶分析自动附带中文分析与判断**：每个进阶 feature 卡片尾部渲染「分析与判断」块，A/B 对照时追加「综合判断（基准 vs 对比）」块，结论由 `scripts/advanced_insights.py` 规则化生成（优先复用单集群 JSON 内嵌 `analysis` 字段），全部中文输出。

```bash
python scripts/generate_cluster_report.py --data-a <a.json> --data-b <b.json> --output compare.html
# 可选: 追加 --advanced 外部进阶分析 JSON（补双集群时间拆解对比; 单集群 feature 缺失时亦作回退）
python scripts/generate_cluster_report.py --data-a <a.json> --data-b <b.json> --output compare.html --advanced <advanced_analysis.json>
```

### 中文分析与判断生成器

`scripts/advanced_insights.py`：规则化中文「分析与判断」生成模块，被提取器（写入单集群 JSON 内嵌 `analysis` 字段）、HTML 报告与 MD 报告三方共享，保证同口径。能力：
- 对 free_analysis / communication_bottleneck / cluster_time_compare_summary 按规则生成中文结论：首要成因与占比阈值（≥50% 高度集中 / ≥30% 主要成因）、Rank 影响面（≤4 局部 / >4 全局）、瓶颈算子集中度、慢卡集合比对（同一卡=硬件嫌疑 / 不重叠=调度负载）等
- `zh_text()` 将工具原始英文原因/指标翻译为中文术语（短语级映射 → 全词映射 → 标识符保留原文）
- `compare_insights()` 生成 A/B 对照的综合判断（双侧数据齐备才输出）
- 单集群 feature 优先复用内嵌 `analysis` 字段（最多 8 条），缺失时按 data 规则即时计算

### MD 比对报告生成脚本

`scripts/generate_cluster_md.py`：基于两个集群的提取数据生成 Markdown 比对报告，**与 HTML 报告共用同一套指标计算与判定逻辑**（直接复用 generate_cluster_report.py 的函数），结论一致。输出八章节：一、综合结论 / 二、核心指标对比 / 三、劣化根因 / 四、行动建议 / 五、Step 级耗时对比 / 六、Rank 级差异 / 七、通信算子差异 / 八、进阶分析（含「分析与判断」与「综合判断（基准 vs 对比）」），全部中文输出。

```bash
python scripts/generate_cluster_md.py --data-a <a.json> --data-b <b.json> --output compare.md
# 可选: --advanced 外部进阶分析 JSON（补双集群时间拆解对比）; --top-ranks 控制 Rank 级差异表行数（默认 20，0=全部）
python scripts/generate_cluster_md.py --data-a <a.json> --data-b <b.json> --output compare.md --advanced <advanced_analysis.json> --top-ranks 20
```

### 进阶分析编排脚本

`scripts/run_advanced_analysis.py`：可选补充脚本——探测 msprof-analyze 与双集群数据格式，编排进阶特性并解析结果为 JSON（供 `generate_cluster_report.py --advanced` 合并渲染）。单集群特性（free_analysis / communication_bottleneck）对集群 A、B **分别执行**，结果标注 `cluster: A/B`，工具输出目录隔离在 `<work-dir>/cluster_A/`、`<work-dir>/cluster_B/`，命中提取器内嵌缓存时直接复用；双集群特性（cluster_time_compare_summary）仅此脚本提供。特性不可用时仅标注原因不阻塞。支持 `--dry-run`（只探测不执行）、`--force`（忽略缓存重跑）、`--msprof`（指定工具路径）、`--top-num`（Top N 数量）、`--work-dir`（工具输出目录，默认 `<output 同目录>/advanced_work`）。

```bash
python scripts/run_advanced_analysis.py --cluster-a <a数据目录> --cluster-b <b数据目录> --output <advanced_analysis.json>
```

### 指标校验脚本

`scripts/verify_extracted_metrics.py`：对提取 JSON 做快速交叉校验，**替代内联 `python -c`**。输出 Step/Rank 均值、Rank 离散度（慢卡线索）、各带宽类型均值带宽与有效吞吐、Total 汇总行残留检查，双文件模式下自动给出带宽口径判定提示。

```bash
python scripts/verify_extracted_metrics.py --data-a <a.json> [--data-b <b.json>]
```

当脚本不可用时，按照上述工作流手动执行 SQL 查询、计算差异、参考 HTML 模板构造报告。

## HTML 报告设计要求

比对报告模板必须满足：
1. **自包含**：单个 HTML 文件，内联 CSS/JS，无外部依赖（ECharts 通过 CDN 引入）
2. **数据驱动**：模板中使用 `{{占位符}}` 标记数据插入点，脚本替换后生成最终报告
3. **交互式图表**：使用 ECharts 渲染所有图表（柱状图/饼图/线图/瀑布图）
4. **响应式**：适配不同屏幕宽度
5. **专业视觉**：深色标题栏、卡片式布局、颜色梯度表格、状态标签（正常/警告/严重）
6. **中文界面**：所有标题、标签、描述使用中文

## 注意事项

- 原始数据单位为微秒（μs），展示时转换为毫秒（ms），保留 2 位小数
- **Windows 下禁止内联 `python -c`**：PowerShell 的引号规则与 bash 不同，嵌套引号极易冲突报错。任何临时校验/计算逻辑必须落盘为独立 `.py` 文件再执行；常规校验优先使用 `scripts/verify_extracted_metrics.py`
- **带宽解读纪律**：均值带宽（AVG(bandwidth)）对算子流量构成（包大小分布）敏感，跨集群比较时必须以**有效吞吐**（总传输量/总传输时间）为准；均值降而吞吐平 → 口径差异，均值与吞吐同降 → 真实劣化
- **Total 汇总行**：DB 模式通信时间/带宽表中可能存在 Total 汇总行（如 `Total Op Info`），提取与算子级对比前必须过滤（提取器已内置过滤，报告生成器含防御性二次过滤）
- **贡献度解读纪律**：贡献度 = ΔX/ΔStage 是"占 Stage 变化量的比例"，可超 100% 或为负（各分项方向相反、相互抵消），不是"占总时间比"；|ΔStage/Stage_A| < 1% 时贡献度无统计意义，报告已降级为 "—"，向用户解读时不得将门控值当作真实占比
- **进阶分析流程**：free_analysis / communication_bottleneck 在提取单集群 JSON 时内嵌执行（默认开启，缓存于 `<data-dir>/advanced_work/`，比对前即已获得结果）；cluster_time_compare_summary 仅 DB 模式可用（需 ClusterTimeSummary 表，缺失时脚本自动补跑 cluster_time_summary），仅通过 run_advanced_analysis.py 提供；free_analysis / communication_bottleneck 走 `--export_type text` 输出 CSV；工具缺失或特性不可用时按 JSON 中的 status/reason 向用户说明，不要自行伪造分析结论
- **全量中文输出**：比对报告（HTML/MD）与进阶分析的所有分析、成因、推断原因均以中文呈现；工具原始英文术语由 `advanced_insights.py` 的 `zh_text()` 映射为中文（短语级 → 全词级 → 标识符保留原文），报告中不得保留未翻译的英文结论
- **分析与判断同口径**：单集群 JSON 内嵌 `features[].analysis`、HTML 报告「分析与判断」块、MD 报告分析判断三者同源（`advanced_insights.py`），报告仅渲染不伪造；结论为规则化输出（占比阈值 / Rank 影响面 / 慢卡集合比对），向用户解读时引用原始依据数据
- 通信表可能为空（如 profiler_level 低于 Level1、单卡场景或未采集通信数据），报告中需标注"无通信数据"
- 并行策略信息从 `cluster_base_info` 的 `algorithm`/`dp_size`/`pp_size`/`tp_size` 字段或 `profiler_metadata.json` 获取
- 慢卡识别阈值：Stage 时间偏离所有 Rank 均值超过 10% 即标记为异常
- 比对报告中，集群 A 为基准（正常），集群 B 为对比（异常），所有差值 = B − A
- Ascend 950PR&950DT系列 CCU 场景不支持采集通信矩阵和通信算子带宽数据，此类数据缺失属正常现象
