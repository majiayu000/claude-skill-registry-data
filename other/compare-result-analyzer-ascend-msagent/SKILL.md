---
name: compare-result-analyzer
description: "分析 msProbe compare 精度比对结果文件（CSV/XLSX），定位整网精度问题与数值差异。支持统计量模式，输出分析报告。支持辅助信息协助定位：辅助信息（历史结论/已知根因/已排除算子/嫌疑区域等）建议在请求中附带（不依赖交互工具）。若请求中未附带且运行环境无 AskUserQuestion，则跳过辅助信息收集、照常完成分析，报告中省略辅助信息章节并注明原因。"
argument-hint: "提供待分析精度比对结果文件 (compare_result.csv|xlsx)"
---

# msProbe 精度比对分析

## 适用场景
- 分析 `msprobe compare` 的结果文件（CSV/XLSX），定位整网精度问题
- 找"第一个开始变差的位置"，而非全局最大误差
- 输出多个可疑算子候选，不强制收敛为单点结论
- 支持多轮迭代分析：辅助信息帮助跳过已验证项、聚焦未解问题

## 分析流程

### 1. 数据模式检测 + 阈值确定
- 读取 CSV 表头：有 `Max diff` 字段 → **统计量模式**
- **全自动自适应阈值**：脚本内置自适应阈值级联检测算法（序列变点 → 锚定回溯 → Delta-NRE 离群 → 分布间隙 → 统计兜底），自动从数据分布中确定最优 NRE 阈值，无需用户干预。序列变点检测（SICD）支持多窗口变体（滑动窗口 200/500/1000），小窗口独立检测局部跳变，取所有有效检测的最小值作为最终阈值。所有方法结果钳制在 0.1% 下限（被钳制时方法标注 `(clamped to 0.1%)` 且置信度降级）。序列变点检测的 epsilon 基于序列前 100 节点 p25（局部前导基线，对后段污染免疫）。阈值远高于变点前段分布时警惕数据伪影并交叉核对 §7 数据质量告警。
- **Read `references/thresholds.md`** 了解自适应阈值算法详情

### 2. 辅助信息收集
- **Read `references/aux_info.md`**
- 辅助信息获取按以下优先级取首个可用来源，**禁止**因低优先级来源不可用而中断分析：
  1. **请求内附带（最高优先级）**：用户已在本次请求中附带辅助信息 → 直接使用，跳过交互
  2. **交互询问**：请求内无辅助信息且 `AskUserQuestion` 工具可用 → 使用该工具询问（「跳过」或 Type something. 自由输入）
  3. **降级（工具不可用）**：请求内无辅助信息且 `AskUserQuestion` 不可用（当前 agent 运行环境未注册该工具）→ 按标准流程分析，报告省略 §0，并在 §1 元信息标注「辅助信息未收集——当前运行环境无交互工具，如需多轮迭代请在请求中附带辅助信息后重跑」
- 无辅助信息时：禁止自行搜索历史报告
- **多轮迭代支持**：上一轮的单算子验证报告（`*_verify_report_*.md`）可作为辅助信息——验证通过的算子自动归入"已排除算子"，验证失败的归入"已知根因"

### 3. 运行辅助脚本（结构化输出模式）
```bash
python <skill_dir>/scripts/analyze_stat.py <compare_result.csv|xlsx> --format json
```
- 脚本默认启用自适应阈值级联检测（序列变点 → 锚定回溯 → Delta-NRE 离群 → 分布间隙 → 统计兜底），自动确定最优 NRE 阈值。脚本输出的 JSON 中 `auto_threshold` 字段包含检测方法、置信度、统计量，以及 **分段检测信息**（`per_segment_thresholds`、`segment_count`、`low_signal_nodes`）
- JSON 默认写入 `<csv_dir>/.compare_result_analyzer/<csv_stem>_result.json`
- 若过滤比例 >50%，报告中说明
- **脚本自动进行近零噪声过滤**：识别因 bench_l2norm 趋近 dtype 精度下限导致 NRE 虚高的节点，清零其误差指标使其不参与首问题点发现和传播分析。过滤规则：**双向近零判定**——bench 与 npu l2norm 同时低于分界线（数据自适应断层 / dtype 精度边界兜底）且 NRE >= 阈值。仅当两侧都处于精度下限才是分母效应噪声。**单侧近零（bench≈0 而 NPU 有信号）= 发散信号，保留并标记 `divergence_signal`**。实测教训：此规则曾把根因算子的 backward 行整行清除使其在 JSON 隐形。仅作用于浮点 dtype（float32/16/bf16/64），整型和 float8/bool 不参与。噪声节点在 §7 汇总中体现，不在 §E 正文中出现。JSON 输出保留 `noise_filtered_nodes` 明细，计数见 `noise_filter.divergence_signal_nodes`
- **自适应阈值级联顺序**：序列变点检测（SICD）→ 锚定回溯（AnchoredBacktrack）→ Delta-NRE 离群检测（DeltaNREOutlier）→ 分布间隙检测（DistributionGap）→ 统计兜底（StatisticalFallback）。详见 `references/thresholds.md`
- **脚本运行时在 stderr 输出 per-dtype 近零噪声自检日志**：格式 `[noise_filter] dtype=<dtype> cutoff=<value> source=<adaptive_gap|dtype_boundary> total=<count> noise=<count>`。agent 应关注该日志确认各浮点 dtype 均被正确过滤、无遗漏

### 3.5 按需查询（Agent 直接读取 JSON）

Agent SHALL 直接读取 `analyze_stat.py --format json` 输出的 JSON 文件获取所有分析数据。
JSON 已包含 propagation 明细、预计算字段（`amplifier_candidates`、`spike_indicators`、
`fb_association_candidates`、`pool_external_indicators`、`pool_input`）等结构化数据，
无需额外的缓存查询接口。

- **禁止重新运行全量分析**来获取细节——直接读 JSON
- 如需统计摘要，读取 JSON 中的 `summary` 字段
- 如需补充候选，读取 JSON 中的 `pool_external_indicators` 字段并按 C-ANALYSIS-028 筛选

### 3.6 多卡汇总分析（可选）

当用户提供多张卡的比对文件时：

```bash
# 对每张卡独立分析（阈值自动检测）
python <skill_dir>/scripts/analyze_stat.py <card0.csv> --format json
python <skill_dir>/scripts/analyze_stat.py <card1.csv> --format json
```

Agent SHALL 读取每张卡的 per-card JSON，按 **`references/multi_card_rules.md`** 中的规则
（M-001 ~ M-010）执行跨卡聚合分析，包括：
- 跨卡共识根因（M-002）、卡特定根因（M-003）
- 首问题点对齐（M-004）
- 接近阈值告警（M-005）、共识回溯（M-006）
- Backward Amplifier 共识（M-007）
- FB Confidence 分布（M-008）、Scenario Flags 聚合（M-009）
- 最差卡与趋势判定（M-010）

**多卡报告**：使用 `assets/multi_card_report_template.md` 模板生成，包含逐卡对比表、共识指标、
跨卡根因、最差卡、趋势分析，以及 **数据覆盖缺口**（逐卡独立列出 + 跨卡共有缺口优先排查）。

### 3.7 场景定向过滤流程

当 `spike_indicators.spike_condition_met == true` 或 backward 方向存在 NRE>100% 极端节点时，
本聚焦流程为**必选**。流程：
1. **先聚焦**：`python <skill_dir>/scripts/analyze_stat.py <csv> --keep-only parameters_grad --format json`
2. **区域定位**：在聚焦子集中找「首个显著脏参数梯度」
3. **族内首脏成员优先**：执行序首个脏成员 = 根因高优先候选
4. **全量合并呈现**：聚焦与全量分析结论合并呈现
5. **返回空时降级**：改用全量 backward + `fb_association_candidates` 分析
6. **三分类兜底**：Agent SHALL 从 JSON `param_grad_three_category` 字段读取三分类候选（同块成堆 / 孤立大NRE / 执行序靠前），三类并列呈现、不做优先级取舍，各自保留既有传播分类标注

### 4. 数据质量检查 + 定位首差异链（核心分析阶段）
- **数据质量优先检查**：查看 §7 中 shape/dtype 不一致的数量。shape 不一致分级告警：>10% 标注"关键数据异常"（warning），>50% 标注"严重数据异常——建议先修复数据结构对齐"（critical）。shape 不一致节点在传播分类中标注"NRE 可能不可信"
- **首问题点数据质量稀释保护**：当首问题点节点**自身**的 `input→output` 签名清晰（单侧脏输入或明显引入误差）时，即使邻域存在大量 shape 不一致伪象，仍应把该首问题点作为**首要可行动结论**给出；数据质量告警降级为「局限说明」（提示其 NRE 可信度受结构错位影响，标注 "⚠️ 数据质量局限：邻域存在结构伪象，首问题点 NRE 可信度可能受结构错位影响，但其 input→output 签名清晰——仍为首要排查方向"），而非唯一结论。区分「局部结构伪象」与「首点本身仍承载真实载荷」
- **数据覆盖缺口检查**：查看 JSON 中 `meta_errors.data_coverage_gaps`。若存在缺口（干净输出→脏输入之间无可比对节点），报告 §1 增加「数据覆盖缺口」子节
- **Read `references/constraints.md`（重点看分析逻辑约束 C-ANALYSIS-xxx）**
- 按执行顺序和堆栈信息定位，遵循分析逻辑约束（C-ANALYSIS-xxx）
- 首问题点判定：C-ANALYSIS-001（不可忽略标准）+ C-ANALYSIS-002（上下游传播检查，必须经过 INPUT_PROPAGATION 和 DOWNSTREAM_ABSORBED 检查后方可确认）
- 传播跳变分析：C-ANALYSIS-003（四种模式）+ C-ANALYSIS-014（多 input 复合优先级规则，消除 ROOT_CAUSE/PASS_THROUGH 双标签）
- 多 input/output 检查、下游吸收、INPUT_PROPAGATION 溯源（执行顺序链追溯，C-ANALYSIS-015）、反向重计算处理
- 分析范围：上游溯源/下游吸收 ±500 行（C-ANALYSIS-011，报告 §1/§4 须注明）
- 显著放大算子（Jump > 2×）从 ROOT_CAUSE 独立呈现（§5.1a），参数误差节点（weight/bias）自动提升优先级
- 确认首问题点后记录行号范围起始值（C-ANALYSIS-013），作为后续过滤基准
- **低置信首点标注**：首点 NRE ∈ [阈值, 5×阈值] 时标注"低置信首点"，建议结合 `fb_association_candidates` / `spike_indicators` 交叉解读，**不得因量级小直接贬低其指针价值**（曾有根因指针被误判为 bf16 噪声而错过 backward 证据）
- ROOT_CAUSE 分类含 `dirty_inputs` 字段、`input_subtype`（`INPUT_ALL_CLEAN` / `INPUT_PARTIALLY_DIRTY` / `INPUT_ALL_DIRTY`）、`trace_boundary_reason`（上游追溯中断原因）
- C-ANALYSIS-014 **数据输入优先检查**：存在脏数据输入时，仅当 output NRE > max(数据输入 NRE) × 1.1 才判 ROOT_CAUSE（避免干净 weight 覆盖脏 data input）
- **首检点引导标注**：当全局首检点与 §5.1 中最大 NRE 的 ROOT_CAUSE 节点满足以下条件时，agent SHALL 在报告 §4 增加引导性标注：首检点 NRE < 根因区域最大 NRE × 0.1（量级显著差异）且行号距离 > 500 行（无直接因果链）。触发场景：grad_norm_spike 下 forward 首检点 NRE 常仅 ~0.1%，而 backward 根因区域 NRE 可达百万~十亿%，两者行号距离数千行——用户仅看首检点会被引向无关区域。标注文本 SHALL 根据实际数据填入方向信息，**禁止硬编码"参数梯度"**：`"⚠️ 全局首检点（{fp_direction}方向，NRE={fp_nre}%）与最大误差区域（{max_direction}方向，NRE={max_nre}%）相距较远且无直接因果链——首检点的误差量级远小于另一方向，建议优先排查 {max_direction} 方向的根因候选（详见 §5.1），并结合前向/反向根因关联（§4）交叉验证。"` 此标注为增强性引导，**不替换首检点**，首检点仍置顶第一行

### 4.5 方向分池与显著放大算子
- Agent SHALL 直接读取 JSON `top_root_causes`（脚本已按 **C-ANALYSIS-027** 三池合并去重）填充 §5.1，整表总计 ≤15 条（保底 ≤5 + 常规 ≤10，整表统一按行号升序），不再自行合并。三池合并规则（保底 ∪ 执行序 ∪ 量级、去重、保底保证入选、整表按行号升序、≤15）由脚本执行，详见 `references/constraints.md` C-ANALYSIS-027。
- 全量 ROOT_CAUSE 列表保留在 `propagation.root_cause`（执行序、不截断）。需要更多候选时从该列表直接提取，无需重新运行脚本。
- **显著放大算子**（§5.1a）：Agent SHALL 按 **C-ANALYSIS-025** 从 JSON `amplifier_candidates` 字段筛选 `all_inputs_clean == true` 且 `amplification_ratio > 2` 的算子。
  - `output_nre >= threshold` → 保底池候选（纳入 §5.1）
  - `output_nre < threshold` → 显著放大算子（纳入 §5.1a，至多 5 条）
- **Grad Norm Spike 场景**：Agent SHALL 按 **C-ANALYSIS-016** 从 JSON `spike_indicators` 字段判定。若 `spike_condition_met == true`：
  - 清空 `top_root_causes.forward`
  - Backward 参数梯度输出节点置顶
  - `top_root_causes.backward` 顶部已有脚本置顶的 **FB 关联同族 backward**（`fb_associated == true`，与首点同算子族）——Agent SHALL 保留并置为最优先排查项，禁止从 §5.1 剔除
- **参数梯度三分类候选（grad_norm_spike / backward 场景必选）**：Agent SHALL 从 JSON `param_grad_three_category` 字段读取三分类候选，三类**并列呈现、不互斥、不排序压制**，均为"待排查项/候选来源"维度，仅并列呈现、不各自判为根因。是否定位为误差引入点仍需按既有传播判定规则单独确认：
  - **同块成堆**（`same_block_cluster`）：同一子模块块（同一模块路径前缀）内多个参数梯度同时超标——族内集中异常是高置信度信号
  - **孤立大NRE**（`isolated_large_nre`）：单点绝对 NRE 最大的参数梯度——防止绝对值最大的入口被成堆候选淹没
  - **执行序靠前**（`execution_order_first`）：参数梯度中执行序最早出现的超标节点——最接近误差最初扩散点的入口
  - 三类各自 SHALL 保留既有传播分类标注（误差引入/误差放大/误差继承），不得因"三类并列"而全部定性为根因
  - 在报告 §5.1 后增加「参数梯度三分类候选」子节（单卡）或在多卡报告对应位置增加子节，提示"以下候选三类并列、不做优先级取舍，均为待排查项而非根因定性"
- **报告中使用规则**：分析时应区分 forward/backward 方向的根因特征。显著放大算子应在报告 §5.1a 独立展示。参数误差节点（weight/bias，含 backward 参数梯度输出）标注优先级提升。

### 4.6 前向/反向根因关联 + Backward 优先分析路径
- Agent SHALL 按 **C-ANALYSIS-026** 从 JSON `fb_association_candidates` 字段判定
  forward↔backward 关联（含 `confidence` 字段：high/medium/low）。条目多时只列 top 5，
  按 confidence + backward_nre 排序。
- **纯信号判定**：backward 端检查 `pre_filter_root_cause_snapshot`（过滤前原始信号）中
  NRE > 100% 的极端节点；forward 端检查首问题点 Jump > threshold。
- **报告中使用规则**：若 `fb_association_candidates` 非空，在报告 §4 中增加「前向/反向根因关联」节。与首点同族的关联是最高优先排查项。
- **spike 场景置顶**：脚本已把与首点同族的 FB 关联 backward 置顶进 `top_root_causes.backward` 顶部（`fb_associated == true`）——这正是「首点算子的 backward 实现可能有问题」的直接证据，Agent SHALL 在 §5.1 置顶呈现并优先排查，不得降级为普通 §4 参考。
- **Backward 优先分析路径**（grad norm spike 场景）：按 **C-ANALYSIS-021** 三档继承性对照（继承 / 放大 / 实现问题）。族内首脏成员前置（详见 §4.7 和 C-ANALYSIS-028）。

### 4.7 补充候选检查（防漏检）
- Agent SHALL 按 **C-ANALYSIS-028** 从 JSON `pool_external_indicators` 字段筛选补充候选：
  - (a) Family 首脏成员：`is_earliest_in_family == true` 且 NRE ≥ 阈值
  - (b) Output 显著放大：`jump > threshold × 2`
  - (c) 无 input 参数梯度：`is_param_grad_no_input == true`
- 判定指标仅使用 NRE 和 jump，不引入新指标。
- **报告呈现**：取 NRE 最大的至多 5 条 + 族内首脏成员（强制补入），并入 §3 表尾（标注"补充候选"来源）。保留完整 prefix 路径，禁止聚合抹平。纯 forward 场景不触发族内首脏成员逻辑。

### 5. 结合算子类型修正
- **Read `references/thresholds.md`** 了解自适应阈值算法详情
- **Read `references/operator_types.md`** 了解特殊算子处理规则（类别 1 / 类别 2）
- 占位、冗余、无法比对算子仅做说明，不作为根因
- **无计算算子豁免（类别 1）**：`empty*` / `numpy` / `to` 即便 NRE 超阈值也仅做说明、不作为根因，不进入 §3/§5.1/§5.1a 候选
- **集合通信算子输入豁免（类别 2）**：`_reduce_scatter_base` / `_all_gather_base` / `all_to_all_single` / `batch_isend_irecv` 禁止用 input 做传播判定，**仅用 output 判定**——按 output NRE 可作为根因候选/首点（跳过 C-ANALYSIS-002 step2 / 003 / 004 / 014 的 input 侧检查）；上游溯源到此停止（跨 rank），标注边界并引导跨卡共识分析（M-002）交叉确认。细则见 `references/operator_types.md`

### 6. 输出多个候选
- 按条目上限（C-REPORT-009/C-REPORT-013），在报告 §3（内容 = {首问题点} ∪ §5.1 全部条目 ∪ §5.1a 显著放大算子 ∪ §5.2 全部条目 ∪ §5.3 全部条目，上限 31 行 + 补充候选至多 5 条，不含 INPUT_PROPAGATION 和 ABSORBED）、§5.1（常规 ≤10 + 保底 ≤5 = ≤15 条，整表不区分方向）、§5.1a（≤5 条）、§5.2~§5.5（各 ≤5 条）、§5.6（不限制，汇总所有）中列出候选节点
- **§3 补充候选**：Agent SHALL 按 C-ANALYSIS-028 从 JSON `pool_external_indicators` 取 NRE 最大的至多 5 条并入 §3 表尾（标注"补充候选"）。**Backward / grad_norm_spike 场景触发族内首脏成员强制补入时**（窄化条件见 §4.7），补充候选取舍为「NRE-top-5 ∪ 族内首脏成员」——族内首脏成员即使 NRE 不在 top-5 也须补入，标注「族内首脏成员」，保留完整 prefix 路径禁止聚合抹平。纯 forward 场景不触发，零影响
- **§5.1 以 JSON `top_root_causes` 为准**：脚本已按 C-ANALYSIS-027 三池合并去重（保底 ∪ 执行序 ∪ 量级，整表总计 ≤15，整表统一按行号升序、保底保证入选），agent 直接取池内条目填充 §5.1，**禁止用 output 行手工覆盖脚本分类**（grad_norm_spike 下 `top_root_causes.forward` 已清空、backward 参数梯度输出已置顶；含 parameters_grad 的 backward 算子由 C-ANALYSIS-021 独立评估，不受 C-ANALYSIS-007 吸收检查影响）。池外真实量级候选用 `--cache` 下钻补入
- **§5.1 行序前 10 之外必须再按 NRE 降序交叉核对**：无 input 的 parameters_grad 节点无 jump，用 output_nre（同量级池口径）。必须包含「区域入口 + 族内首脏成员」强制项（根因常是量级并非最大的族首成员）。**Backward 场景族内首脏成员**：当同族有 ≥2 成员在 backward root_cause（尤其 impl_only/amplified）或 pool_external_indicators 中出现时，执行序最早/input 最干净的族成员须强制列入候选，标注「族内首脏成员」，不得因 NRE 不在 top-5 而省略（详见 §4.7）
- **§5.2/§5.3 按 jump 交叉核对**：禁止仅按行号截断。Module 族聚合兜底——单条 jump 略低但族内多条不得整体遗漏
- **参数梯度三分类候选**（grad_norm_spike 场景）：在 §5.1 后增加独立子节，从 JSON `param_grad_three_category` 读取三分类候选人（同块成堆 / 孤立大NRE / 执行序靠前），三类并列呈现、不互斥，至多每类 5 条。各条目保留既有传播分类标注（误差引入/误差放大/误差继承），不得因"三类并列"而全部定性为根因。子节抬头提示"以下候选三类并列、不做优先级取舍，均为待排查项而非根因定性"
- 按 `高 / 中 / 低` 三档优先级排列，不强制收敛为单点结论

### 7. 生成报告（报告输出阶段）
- **Read `assets/report_template.md`**，按模板生成完整报告
- **grad_norm_spike 场景**：报告 SHALL 在 §5.1 后增加「参数梯度三分类候选」子节（同块成堆 / 孤立大NRE / 执行序靠前），从 JSON `param_grad_three_category` 读取，三类并列呈现不互斥。多卡报告对应增加子节
- **Read `references/constraints.md`（重点看报告输出约束 C-REPORT-xxx）**
- **报告可读性约束（C-REPORT-xxx，所有报告适用）**：报告正文 SHALL 避免 skill 内部专属名词，尽量使用通用词汇；术语无法避免时必须首次出现给出解释。术语对照表见下：
  | Skill 内部术语 | 报告中的通用表达 |
  |---|---|
  | ROOT CAUSE / PROPAGATION / PASS_THROUGH / INPUT_PROPAGATION / ABSORBED / DOWNSTREAM_ABSORBED | 误差引入点 / 误差放大点 / 误差缩小点 / 误差继承（源自输入）/ 误差被消除 |
  | FB association / fb_association / fb_association_candidates / FB 高置信 | 前向↔反向关联（高置信） |
  | 候选池 / 呈现池 / 三池合并 / 保底维度 / 候选池置顶 / pool_source / top_root_causes | 根因候选（直接列出即可，不描述池机制） |
  | SICD / 序列变点 / 锚定回溯 / DeltaNREOutlier / 分布间隙 / 统计兜底 | 自适应阈值检测（基于数据分布自动确定） |
  | grad_norm_spike / scenario_flags | 梯度范数尖刺（梯度爆炸场景） |
  | 低置信首点 / 首检点引导 | 首点误差偏小、置信度有限 / 首点与最大误差区域差异提示 |
  | divergence_signal / 发散信号 | 发散信号（NPU 有数值而 GPU 接近零） |
  | parameters_grad / param_grad_output | 参数梯度（weight/bias 的梯度） |
  | 继承性三档（继承/放大/实现问题） | 误差继承上游 / 放大上游 / 独立引入 |
  | pool_external_indicators | 补充候选（未被常规候选覆盖、但值得排查） |
  | Module 算子 / API 算子 | 自定义模块算子 / 基础算子（Tensor 级算子） |
  | 无法重建计算图 | 缺少配套前向数据，无法自动验证 |
  | NRE / MeanBias | NRE（归一化相对误差）/ MeanBias（整体均值偏移）——已在核心术语表定义，正文可直接使用 |
  > **禁止**在报告中出现：C-ANALYSIS-xxx / C-REPORT-xxx 约束编号、JSON 字段名（fb_association/top_root_causes/scenario_flags 等）、阈值算法内部名。
- 报告保存为 `<比对文件名>_analysis_report_<YYYYMMDDHHmmss>.md`，保存到比对文件所在目录
- 遵循报告输出约束（C-REPORT-xxx）：§1~§7（§7 含元信息异常 + 近零噪声过滤，为现在必选子节）必选、算子粒度呈现、行号范围标注、条目上限、排序检查
- **禁止使用 memory**，最终输出仅允许 .md 格式文件
- 报告完成后自检：逐一核对 §1~§7 章节编号是否存在且顺序正确

### 8. 单算子验证（API 候选实锤，自动执行）
- **本步骤在分析报告生成后自动执行**，无需用户手动触发
- 单算子验证流程细节（算子注册、构造策略、反向验证、边界情况）详见 `references/verify_op.md`
- 比对分析报告中 §3 的可疑候选分为两类：**API 算子**（如 `Tensor.__truediv__.3`，非 `Module.` 前缀）和 **Module 算子**（如 `Module.xxx.forward.0`）
- **仅 API 算子可进行单算子验证**——Module 算子涉及自定义实现，无法自动验证
- 验证流程：
  1. agent SHALL 自动从报告 §3 表格中提取 API 候选，**保持完整 NPU Name 含方向**（如 `Tensor.__truediv__.3.backward`），与分析报告 §3 格式一致
  2. 去重后**直接传全部 API 候选给 `--op-list`**，由 `verify_op.py` 的自动注册机制（`get_operator_fn(auto_register=True)`）自行处理注册
     ```bash
     python <skill_dir>/scripts/verify_op.py <compare_result.csv> --op-list "<候选1>,<候选2>,..." -o verify.json
     ```
     ❗ **禁止**先调用 `--list-ops` 预过滤——`verify_op.py` 内置了三层递进注册（精确匹配 → 通配匹配 → 自动推断），agent 预过滤会拦截自动注册流程。仅在 `verify_op.py` 返回"自动注册失败"时才在验证报告中标注"未注册"
     ❗ **禁止**传递 `--atol`、`--rtol`、`--construct-*` 参数——使用 verify_op.py 默认值（dtype 自适应容差：float64 atol=1e-9/rtol=1e-7，float32 atol=1e-4/rtol=1e-3，float16 atol=1e-3/rtol=1e-3，bfloat16 atol=5e-3/rtol=5e-3；construct-strategy=auto, construct-l2norm-rtol=5%, construct-clamp-ratio=10%）
  3. 读取 JSON 结果，按 `assets/verify_report_template.md` 生成单算子验证报告
     - 验证报告头部须包含「核心术语」表（NRE/MeanBias/ROOT CAUSE/PROPAGATION 一句话定义），便于用户单独查看验证报告时理解术语
  4. 保存为 `<比对文件名>_verify_report_<YYYYMMDDHHmmss>.md`，与比对分析报告同目录
- 验证结果含义：
  - ✅ 通过：CPU vs NPU 结果一致（dtype 自适应容差下）→ 算子实现无问题，可排除嫌疑
  - ❌ 失败：CPU vs NPU 结果有差异 → 确认问题，标记为已知根因
  - ⚠️ 未注册：`verify_op.py` 自动注册失败（非"不在注册表中"）→ 无法自动验证，需手动排查或在 `_verify_core.py` 中通过 `@register_op` 装饰器手动注册
  - 构造质量差：输入 tensor 构造时 l2norm 偏差或 clamp 比例超标 → 验证结论置信度降低，仅供参考
- 反向验证时，`verify_op.py` 自动使用同调用序号（instance）的前向数据构造计算图。若该 instance 无前向数据，验证失败并报错"未找到同调用序号的前向数据"。
- **Read `assets/verify_report_template.md`** 获取完整报告模板
- ❗ **每个候选实例逐一独立验证，禁止因"同类算子"而跳过**。每个实例的 shape / dtype / 数据分布不同，一个实例通过不能保证同类算子的其他实例也通过
- 验证报告中 SHALL 直接复制分析报告 §3 的完整表格作为"可疑候选来源"章节，让用户无需跨文件对照
- 未注册的 API 候选和所有 Module 候选在验证报告中列出但标注"无法验证"
- 若无 API 候选或全部未注册，仍生成验证报告但标注"无已验证候选"
- **verify 语义边界**：verify 用 NPU 统计值自构造输入，只能证明实现一致性，**无法覆盖「weight/bias 参数值在两侧真实不同」的根因类型**——当根因模式为「参数行脏 + 输出放大」时，验证报告须标注「✅ 通过仅证明实现一致，不排除参数值差异」；verify 通过 ≠ 根因排除
- **验证受限说明**：当验证流程无法正常完成（或结论不可靠）时，agent SHALL 在验证报告中说明原因（标准化模板详见 `references/verify_op.md`「验证未能正常完成的情况」章节），区分以下场景：
  - **NPU 环境不可用**：「⚠️ 验证环境不可用——NPU 设备未授权/不可达，跳过单算子验证」
  - **自动注册失败**：「⚠️ 自动注册失败——算子 `<name>` 三层递进注册均未命中，需在 `_verify_core.py` 中通过 `@register_op` 装饰器手动注册」
  - **混合 dtype 跳过**：「⚠️ 跳过——算子 `<name>` 输入/输出含混合 dtype，verify_op.py 不支持」
  - **构造质量差**：「⚠️ 构造质量差——l2norm 偏差 X%，clamp 比例 Y%，验证结论置信度降低，仅供参考」
  - **无法重建计算图**：「⚠️ 无法重建——未找到同调用序号的前向数据，反向验证不可用」
  - 未正常完成验证的候选 SHALL 在验证报告「未能验证的候选及原因」子节集中呈现

## 输出风格
- 先给结论，再给证据。先给首差异，再给全局最差
- 先给主候选，再给备选候选
- 每个候选写清楚"为什么选中"和"为什么未直接定性"
- 报告里优先说明"命中哪套阈值"，再说"看起来像谁的问题"

### 9. 生成综合分析总结报告（自动执行）
- 在 Step 8 单算子验证报告生成完成后自动执行，无需用户手动触发
- **Read `assets/summary_report_template.md`**，按模板生成总结报告
- **排序自检（C-REPORT-014）**：「待排查节点」表生成后 SHALL 逐档核对高、中、低三档各自起始行号是否递增——常见缺陷是只排了高优先级、漏排中/低优先级，须重点检查中、低档
- 总结报告将分析报告和验证报告的核心结论整合为精简的两章结构：
  1. **结论与建议**：待排查节点（嫌疑候选，按优先级高/中/低分组，**高、中、低每一档优先级内部都必须按起始行号升序排列——不得只对高优先级排序而漏排中、低优先级**）、已排除节点、后续行动建议
  2. **详细发现**：可疑候选列表与验证结果的交叉对照表（Module 算子无法自动验证，原因并入验证结论列）
- **结论性质约束**：总结报告 SHALL NOT 出现「已确认根因」小节——本 skill 仅提供分析与建议，不产出"已确认根因"，所有候选均为嫌疑（按高/中/低优先级分组，**高、中、低每一档优先级内部都必须按起始行号升序排列——禁止只对高优先级排序而漏排中、低优先级，生成后须逐档核对**）；最终根因需人工结合报告、代码与补充验证实锤。唯一可确认的是「已排除」——单算子验证通过可确认某算子实现一致、排除嫌疑
- 头部元信息后须包含「核心术语」表（NRE/MeanBias/误差引入点/误差放大点/首问题点 一句话定义），便于用户单独查看总结报告时理解术语
- 总结报告是独立文件，不替代分析报告和验证报告，后两者作为引用参考
- 无 API 候选或未运行验证流程时：总结报告退化为分析报告的浓缩版，「待排查节点」写"无已验证候选"
- 报告保存为 `<比对文件名>_summary_report_<YYYYMMDDHHmmss>.md`，与比对分析报告同目录
- 整网误差会累积，首差异优先于全局最差值
- 阈值不是一刀切，必须明确使用了哪一套标准
- 如果存在多个合理候选，必须列出备选，不强行收敛成一个答案
