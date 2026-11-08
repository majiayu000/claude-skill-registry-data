---
name: spike-root-cause-analysis
description: >
  分布式训练梯度尖刺 (Gradient Spike) 根因定位。基于梯度监控数据 (trend.db/CSV)、
  msprobe dump 统计数据，三阶段渐进式从异常坐标定位逐层深入到算子级根因。
  当用户明确指明分析梯度尖刺问题时使用此 skill。 即便用户提供以上数据，但未指明分析梯度尖刺问题时，不可使用此skill。
keywords: [spike, 梯度尖刺, gradient spike, 梯度异常, 根因定位, root cause, dump_statistic,
  trend.db, parameters_grad, 参数梯度, 前反向, 激活追溯]
---

# Spike 根因定位分析

**目标:** 不断往「最先」定位——找到异常最早产生的位置，不是异常最大的位置。

```text
Phase 1+2 — 梯度监控数据 → 最先的根因前反向
    定位最早出现异常梯度的前反向（单点尖刺源头，而非传导后的爆发点）

Phase 3 — Dump 统计数据 → 对照正常数据，最早的分叉点
    以正常样本为对照组，找激活过程最先分叉的层/算子
```

**判定铁律:**
- 找「最先」不是「最大」——最早出现的异常才是根因，最大异常往往是传导/放大结果
- 不按绝对差异大小判断——以对照组（C/D）定义正常噪声水平，A/B 相对对照组的偏离才是异常
- 有对照组时必须参考对照组

**核心原则:** 数据够就分析，不够就输出当前结论，不强行推进。每个阶段输出必须包含表格展示。

**数据路径:** trend.db / monitor CSV → Phase 1-2；dump_statistic → Phase 1、3。
仅有 dump 时直接 `--dump` 模式走 Phase 1→2→3。

---

## Phase 1: 候选 spike 三维坐标

### 脚本

```bash
python scripts/trend_db_spike_detector.py <data.db> [-o p1.json]     # trend.db
python scripts/trend_db_spike_detector.py <csv_or_dir> --csv [-o p1.json]  # CSV 文件或目录
python scripts/trend_db_spike_detector.py <dump_dir> --dump [-o p1.json]   # dump_statistic
```

CSV 直接传目录（自动批量加载多 rank × 多 step），不需要自写合并脚本。

### 分析流程

**Step 0: 切分分析** — 脚本自动完成:
- PP 检测（`vpp_stage` 多值）
- 累积窗口检测: norm 周期性重置 → `step` 实为 micro_step → 派生 `optimizer_step`/`micro_step`。
  CSV 与 trend.db 同源，走相同检测；短序列（5-9 step）用多 rank 共同重置点判窗口边界
- dump 自动检测单/多 step 结构

**Step 1: 异常检测** — 按数据粒度分支:
- **step 级**: 每 step 独立完整梯度 → 全局基线 (MAD/IQR) 动态阈值
- **micro_step 累积**: 每 opt_step 最终态 top-3 suspect → 展开累积曲线 → delta 突变检测。
  短序列（CSV 切片）全量展开 + median 倍数阈值 + top-N 收敛
- **dump**: 单 step 绝对值 top-N；多 step 跨 step 基线检测

### 输出 JSON 关键字段

- `sharding_analysis`: `accumulation_window`（0=step级/dump）, `pass_unit`, `reset_boundary`（短序列窗口边界）
- `target_rank_norms`: 每 opt_step top target 的全 rank 最终 norm（micro_step 数据，供 Phase 2）
- `anomalies[]`: `rank`, `step`, `micro_step`, `optimizer_step`, `target_name`, `norm`, `delta`,
  `deviation_ratio`, `suspect_final_norm`, `trigger`

---

## Phase 2: 根因坐标选定

### 脚本

```bash
python scripts/phase2_root_cause_selector.py --phase1 p1.json [-o p2.json]                    # 单设备
python scripts/phase2_root_cause_selector.py --npu <p1.json> --gpu <p1.json> [-o p2.json]     # 跨设备
#   --npu 异常侧, --gpu 标杆侧; 标杆不限于 GPU
```

### 分析流程

**Step 2.1: 确定关注 target** — 每 opt_step 取 `suspect_final_norm` 最大者；dump 直接取 top-1 norm 最大 rank。

**Step 2.2: 跨 step 根因判定** (仅 micro_step 数据):

```text
IF 相邻 opt_step 间，大多数 rank（>=60%）的最终 norm 增长 >= 2x
THEN 根因在前一个 opt_step（异常梯度 → 权重更新污染 → 后续爆炸）
ELSE 取异常偏离最大的 opt_step
```

多个相邻对同时满足时取**时间最早**的转折点——最早异常是源头，后续增长是传导。

**跨 step 判定只依据异常侧自身的增长率**——标杆侧同转折也有增长（双端共有）不否定根因 step：
异常侧增长就是前一步梯度污染的结果，不管标杆侧涨不涨。标杆对比只用于标注「双端共有/设备特异」，不用于推翻根因 step。

**Step 2.3: 选定坐标**
- 无标杆: 根因 opt_step 内取 delta/norm 最大者
- 有标杆: 从最异常坐标开始逐个对比标杆侧同位置，比值 >= 2x 或标杆无 → 设备特异性；接近则跳过

### 输出 JSON

`root_cause_coordinate`(opt_step/rank/micro_step/target_name/delta/norm), `reasoning`,
`cross_device_verification`

---

## Phase 3: 激活过程差异追溯

### 前置条件
Phase 2 已输出根因坐标；有 dump_statistic（至少异常侧）。

### 脚本

```bash
python scripts/phase3_trace_analyzer.py \
  --dump-a <异常dump> --dump-b <异常标杆> [--dump-c <邻近正常> --dump-d <邻近标杆>] [-o p3.json]
```

脚本输出四组对照逐层表格（前向+反向 Max/Min/Norm），LLM 基于表格判定方向并下钻。

### 分析流程

**Step 3.1: 组装对照组** — 建立四组: A=异常坐标（Phase 2 输出）, B=A 的标杆, C=邻近正常坐标, D=C 的标杆。
异常度 = (A/B)/(C/D)，C/D 消除设备系统偏差并验证标杆对齐（应 ≈1.0x，明显偏离先确认数据）。

C/D 通常可以从已有数据中获得:
- 异常侧 dump 目录的其他 rank（如 rank59 异常 → rank60 即 C）
- 异常侧其他 step（正常 step 的 dump）
- 标杆侧对应位置（同 rank/同 step 的标杆设备 dump 即 D）

用户只提供 A/B 两个 dump 时，先在数据目录中找同设备的其他 rank/step dump 补成 C/D。
自动补选 C 必须过滤: 该坐标不在 Phase 1 异常列表中，且梯度 Norm 处于同目录正常水平（如低于 P75 百分位）；
若目录内所有候选都有尖刺（尖刺持续多步的场景）或无法判定「正常」，禁止自动选取，改为询问用户提供正常样本。
确实只有两个 dump 时才降级为 A/B 直接对比，并注明「无对照组，A/B 比值可能混入设备系统偏差」。

**Step 3.2: 选锚点 module** — 至少三个在 A/B/C/D 中命名可对齐的 module（锚点不足 3 个时脚本输出 `anchor_warning`，结论必须标注判定不完整）。
每层代表算子取 module **输出算子**（如 self_attention.MLASelfAttention / mlp.MoELayer——输出携带 module 计算结果；
分叉常在 module 内部计算产生，只比 Norm 最大的中间算子会漏掉，如 qkv 投影一致但 attention 输出已分叉）；输出算子不可对齐时回退 Norm 最大可对齐算子。
锚点算子必须 A/B 两侧**同一算子**（key 或归一化后同 key；脚本自动归一设备命名差异: TE 前缀、Flash vs Fused、forward/backward 序号）**且两侧都有有效数值**。
一侧 NaN/None/缺 key/元素总数不一致 → 该层标「未对齐」: 不算比值、不参与判定、不当作「一致/正常」。
**代表算子一致 ≠ 该层无分叉**——分叉可能产生在 module 内部算子，起点层必须按 Step 3.5 展开内部 sub-module 算子对比。

**Step 3.3: 逐层对比** — 打印表格，每锚点前向+反向各列 Norm:

```text
anchor: <module>  四组: A(异常) B(标杆) C(正常) D(标杆)  异常度=(A/B)/(C/D)
  L |  F_A  F_B  F_C  F_D | F_A/B F_C/D F异常 |  B_A  B_B  B_C  B_D | B_A/B B_C/D B异常
```

逐层遍历全部层；Max/Min/Norm 三指标都看。异常标注 `F!`/`B!` 用**对照组自适应阈值**（median(C/D) + max(3*IQR, 0.03)）——
对照组定义正常噪声水平，C/D≈1.0x 时任何 A/B 偏离（哪怕 1.2x）都是真实分叉。

**Step 3.4: 判断方向** — 汇总前向/反向异常层（与表格标注完全一致）。
判定某方向「正常」需该方向**无未对齐层**（脚本结论 `uncompared_layers` 为空）——未对齐层≠正常，禁止以「异常层列表为空」断言方向一致（NA 往往是比对不了，不是没有异常）:
- 异常判定只看**对照组自适应阈值标注**（`F!`/`B!` 层），禁止用 A/B 绝对值大小重判（1.2x 是「弱」还是「强」不由幅度决定，由 C/D 噪声水平决定）
- 前向有 `F!` 层 → 前向存在分叉，[P0] 追溯前向分叉点。前向分叉是反向异常的潜在源头（计算顺序前向在前）；禁止用「轻微/基本正常/仅一层」消解，禁止用另一锚点干净来宣称「前向没问题」
- 仅反向有 `B!` → 反向自身产生异常
- 前向分叉幅度 << 反向 → 反向放大了前向差异，仍以追溯前向为 [P0]
- 某方向「正常」需所有层 A/B ≈ C/D；否则表述「大部分层正常，Lx-Ly 有弱分叉」

**Step 3.5: 找分叉起点，不是找最大分叉** — 从传播起始端开始逐层检查:
- 前向: 浅层 → 深层，第一个出现 `F!` 的层是起点
- 反向: 深层 → 浅层，第一个出现 `B!` 的层是起点
- 定位起点后，在该层展开所有 sub-module 算子对比，找差异最大的算子；再查该算子的上游是否已有分叉，直到差异不可分辨
- 禁止跳过起点直接下钻「分叉幅度最大的层」——最大分叉往往是传导/放大结果，起点才是根因位置

**Step 3.6: 多指标交叉验证（迭代往前探）** — 单指标找到的分叉起点可能不是真起点。
**每用一个指标确认一个分叉点后，必须用其余指标再探是否有更早的分叉点，直到所有指标都指向同一个最前分叉点为止。**

流程:
1. 先用一个指标（如 Norm）找到分叉起点 Lx
2. 检查 Max/Min/Mean 是否显示更早的分叉层（脚本输出各指标主分叉段起点）
3. 若有更早的（如 Min 起点 L2 < Norm 起点 L4）→ 以更早者为准，**继续用其余指标再探**（L2 之前是否还有更早分叉）
4. 重复直到所有指标的起点都不再更早 → 收敛的最前分叉点即最终分叉点
5. 各指标阈值从其对照组 C/D 分布独立学习，不共用阈值
6. 收敛保证与分歧裁决: 每轮只向**更早层**移动，层数有限故迭代必然终止，无需固定迭代上限；若不同指标给出互不包含的分歧起点（均不早于当前起点），以**当前最前分叉点**为准，并在结论中注明「各指标分歧: <指标>→<层>」；若多个指标的起点都早于当前且互不一致，以**最先开始偏离（起点最浅）的指标**为准

**结论必须引用脚本输出的「各指标主分叉段起点」、「最早分叉点」和「未对齐层 uncompared_layers」行，并说明是否做过其他指标的往前再探。**

**数据特征一致性检查:** 组间存在数据特征差异（seq_len/batch）时，先验证标杆侧同 rank 是否也有；
标杆侧数据相同但梯度不同 → 数据差异不是根因；标杆侧未知 → 标注「待验证」。

---

## 报告输出格式

遵循 msagent 标准 **问题/证据/影响/建议**。表格由 agent 根据脚本 JSON 输出渲染（脚本只输出 JSON，不打印表格）。

### Phase 1: 候选根因表格

**表 1 — 数据总览:**

| 项目 | 值 |
|------|-----|
| 数据 | `<路径>` / `<格式>` |
| 参数 | `<N>` |
| Step/Rank | `<范围>` / `<N>` |
| 前反向单位 | `<pass_unit>` |

**表 2 — 候选根因坐标**（按时间最早排序: opt_step 升序，同 opt_step 按 ms 升序）:

| Opt Step | Rank | 参数 | ms | delta | 偏离 | 最终 Norm |
|----------|------|------|-----|-------|------|----------|
| `<N>` | `<N>` | `<target>` | `<N>` | `<v>` | `<v>x` | `<v>` |

表格后跟结论: 问题（最早异常坐标及偏离）、证据（跨 step 趋势）、建议（进入 Phase 2）。

### Phase 2: 候选根因坐标模式表格

**表 1 — 跨 step 判定**（micro_step 数据，**只看异常侧，标杆侧增长不推翻根因**）:

| 转折 | 增长阈值 | 达标 rank | 判定 |
|------|----------|-----------|------|
| opt_step N-1 → N | `<threshold>x` | `<X>/<Y> (<P>%)` | 根因在 opt_step N-1 / 无明显转折 |

跨 step 判定只依据异常侧自身的增长率。标杆侧同转折也有增长时，标注「双端共有」但不改变根因位置——异常侧增长就是前一步异常的结果，前一步即根因。

**表 2 — 候选根因坐标**（按时间最早排序，跨设备时含标杆对比）:

| Opt Step | Rank | 参数 | ms | delta | 标杆 delta | 比值 | 判定 |
|----------|------|------|-----|-------|-----------|------|------|
| `<N>` | `<N>` | `<target>` | `<N>` | `<v>` | `<v>` | `<v>x` | 设备特异性/双端共有 |

表格后跟结论: 根因坐标 + 选定理由（跨 step 判定 + 跨设备验证）。

### Phase 3: 四组对照表格

**表 1 — 四组对照逐层对比**（每锚点一表，主列 Norm；Max/Min 有异常层时附注）:

| L | F_A | F_B | F_C | F_D | F_A/B | F_C/D | F异常 | B_A | B_B | B_C | B_D | B_A/B | B_C/D | B异常 |
|---|-----|-----|-----|-----|-------|-------|-------|-----|-----|-----|-----|-------|-------|-------|
| 0 | `<v>` | `<v>` | `<v>` | `<v>` | `<v>x` | `<v>x` | 1.0x | `<v>` | `<v>` | `<v>` | `<v>` | `<v>x` | `<v>x` | 29.6x `B!` |
| 7 | `<v>` | `<v>` | `<v>` | `<v>` | `<v>x` | `<v>x` | 1.95x `F!` | `<v>` | `<v>` | `<v>` | `<v>` | `<v>x` | `<v>x` | 8.3x `B!` |

异常标注用对照组自适应阈值（`F!`/`B!`），未对齐层标「-」（引用 `uncompared_layers`）。

**表 2 — 方向判定汇总:**

| 方向 | 判定 | 起点 | 最大点 | 证据 |
|------|------|------|--------|------|
| 前向 | 存在分叉 / 一致 | L4（浅→深第一个 `F!`） | L7 (`<峰值>x`) | `<异常层列表>` |
| 反向 | 存在分叉 / 一致 | L0（深→浅第一个 `B!`） | L0-L3 (`<峰值>x`) | `<异常层列表>` |

表格后跟结论: 方向判定 + 分叉起点 + 未对齐层核对（uncompared 非空时方向判定不可下）→ 对照组验证（C/D≈1.0x）→ [P0] 追溯方向。

---

## 用户交互

- 数据类型/step 对应关系/标杆归属不明确 → 向用户确认
- Phase 1 候选过多 → 用户可手动指定坐标跳过 Phase 2
- 数据不足: 无标杆 → Phase 2 单设备；无 dump → 以 Phase 2 为终；分析到头输出结论+缺失项
