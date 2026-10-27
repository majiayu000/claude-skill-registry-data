---
name: triton-mfu-analyzer
description: >
  在昇腾 NPU 上测量单算子的 MFU（Model FLOPs Utilization，官方 operator_mfu 等价口径），
  并按 kernel 拆解瓶颈，回答"低是低在哪一段、还有没有得优化"。
  覆盖目录适配、极限 MFU 的 (case,倍率) 二维搜索、flops.py 编写与自检、按 dtype 修正峰值、kernel 级 MFU 拆解。
  触发：当用户提到"测 MFU"、"算力利用率"、"离硬件极限多远"、"峰值算力利用率验收"、
  "MFU 偏低为什么"、"极限 MFU"、"放大 shape 测上界"等场景时使用。
argument-hint: >
  输入：算子参考实现 .py（含 class Model）、被测实现 .py（含 class ModelNew）、
  用例 .json/.jsonl。
  输出：各 case 的 MFU（标称口径 / dtype 修正口径）、kernel 级耗时与 MFU 拆解、
  瓶颈判定结论（mfu_decompose.json）。
  若目标是"极限 MFU"，需在 (case, 倍率) 二维网格上逐点采集取最大值，
  而不是只测最大 shape——MFU 对 shape 不单调，且不同 case 可能走不同代码路径。
---

# 单算子 MFU 测量与瓶颈拆解

在真实 NPU 上测出算子的 MFU，并回答"低是低在哪一段、还有没有得优化"。

```
mfu = 理论 FLOPs / kernel 实际耗时 / 芯片峰值算力
```

口径来自昇腾 msprof-analyze 的 `operator_mfu`
（`docs/zh/advanced_features/operator_mfu_instruct.md`）：

```
actual_tflops = FLOPs / (kernelDuration(ns) × 1e-9) / 1e12
mfu           = FLOPs / (kernelDuration(ns) × 1e-9) / chipPeakFLOPS
```

官方那套要走 torch profiler（`with_flops=True` + mstx + Db 导出），由框架按注册公式
自动算 FLOPs。**单算子 benchmark 场景没有这些**，所以本 skill 用 ops-profiling 的
`--quick --mfu` 重建同一个公式：分子来自你写的 `flops.py`，分母来自 msprof 的
`task_time.csv`，峰值从 cube 规格推。

> **与 `ops-profiling` 的关系（重要）**
>
> 本 skill 的采集脚本 `scripts/ops_profiling/msprof_perf_summary.py` 是
> `ops/ops-profiling/scripts/msprof_perf_summary.py` 的**扩展副本**，在其基础上增加了
> `--mfu` / `--mfu-top-k` / `--mfu-peak` / `--impl` 等参数与 MFU 统计逻辑。
> 上游那份目前**不支持 `--mfu`**（典型报错：`unrecognized arguments: --mfu --impl`），
> 因此本 skill 暂时自带副本以保证可独立运行。
>
> 后续计划：待 `--mfu` 能力在 `ops-profiling` 侧稳定后，将该副本合入上游，
> 本 skill 改为直接引用，避免长期维护分叉。修改采集逻辑时请同步评估两处影响。
>
> 下文用 `$SKILL_DIR` 指代本 skill 目录（`ops/triton-mfu-analyzer`）。

---

## 六步流程

> 只要目标是**极限 MFU / 算力上界**，第 2 步不能跳过：
> 数据集自带的是正确性用例（常见 `[2,3,7,16]`），在那种 shape 上测出的是 kernel 启动开销，
> 且数据全在 cache 里，访存墙根本不显形。

### 1. 适配目录布局

三个输入有两种布局，**先判断当前是哪一种**，这是最容易搞错的一步。

判据不要靠文件名，靠内容：
**参考实现 = 含 `class Model` 的 .py**，**被测实现 = 含 `class ModelNew` 的 .py**，
**用例 = 每行含 `inputs` 列表的 .json/.jsonl**。两种布局用同一套判据都能定位。

#### 布局 A（默认）：三个文件在同一个 verify 目录

批跑流程的 verify 目录是最常见的形态：

```
<算子目录>/op_<Op>_<时间戳>/                 # 一次生成任务的产物根目录
    <Op>.py                                ← torch 参考实现（class Model + get_input_groups）
    <Op>.json                              ← 用例
    <Op>_generated.py                      ← 生成的 triton 实现
    output/iter_<n>/verify/
        <Op>_torch.py                      ← torch 参考实现（与外层 <Op>.py 同）
        <Op>_torch.json                    ← 用例
        <Op>_triton_ascend_impl.py         ← triton 实现
        （也可能是 <Op>_triton_baseline.py / <Op>_triton_optimized.py 两份）
        verify_result*.json                ← 精度校验产物，不是用例
```

**torch 实现在两处都有**（外层 `<Op>.py` 与 verify 里的 `<Op>_torch.py`），内容相同，
取任一份即可；用例同理。**triton 实现的后缀不固定**：`_triton_ascend_impl`、
`_generated`、`_triton_baseline`/`_triton_optimized` 都出现过。

```bash
V=<算子目录>/output/<iter>/verify

python3 $SKILL_DIR/scripts/prepare_op_dir.py \
    --ref   $V/<Op>_torch.py \
    --cases $V/<Op>_torch.json \
    --impl  $V/<Op>_triton_optimized.py \
    --dst   <工作目录>/<Op>
```

**同一目录常有多份 `_triton*.py`，都含 `class ModelNew`**（如 `_baseline` 与 `_optimized`）。

> **默认取 `_optimized` 那一份。** 这是被测的目标实现，`_baseline` 只是对照。
> 只有一份时（`_triton_ascend_impl`、`_generated` 等其它后缀）直接用那一份。
> 需要出优化前后对比时才两份各跑一遍，且**分别记录成两行**，不要混在一起。

选择顺序：`*_triton_optimized.py` > `*_triton*.py`（唯一时）> 其它 `*_generated*.py` 等变体。

#### 布局 B：参考实现与生成代码分属两个仓

有的批次把参考实现留在 benchmark 仓、只把生成代码归档到另一个目录：

```bash
BENCH=<benchmark仓>/npu_benchmark/level4      # <N>_<Op>.py + <N>_<Op>.json
GEN=<生成代码归档目录>/Level4                  # <N>_<Op>_<后缀>.py

python3 $SKILL_DIR/scripts/prepare_op_dir.py \
    --ref   $BENCH/<N>_<Op>.py \
    --cases $BENCH/<N>_<Op>.json \
    --impl  $GEN/<N>_<Op>_<后缀>.py \
    --dst   <工作目录>/<N>_<Op>
```

**配对规则**（按编号前缀 `<N>_` 匹配，某次 Level4 全量统计）：

- **生成侧后缀不固定**，实测 6 种：`_generated`(53)、`_triton_optimized`(35)、
  `_generated_code`(8)、`_triton_ascend_impl`(2)、`_optimized_code`(2)、`_code`(1)。
  用 glob `<N>_*.py` 取即可——该批次同一编号只有一份实现。
- **参考侧同一编号可能有多份**（`_old`、`_<hash>` 等变体）。
  **取有同名 `.json` 的那一份**，这条规则能唯一确定。
- **两侧编号不是全集**：benchmark 有而生成侧没有实现的编号需跳过。
- 生成代码仓按批次滚动，同一算子在不同批次下后缀可能不同。**路径要跟当前批次走。**

> **同级目录里的 `.json` 不都是用例**：`verify_result*.json`（精度校验）、
> `perf_result*.json`（性能结果）都是流程产物。
> `max_shape_probe.py` 放大 shape 时会**写入所有用例文件**（见坑 7），
> 判错会直接覆盖掉这些结果。
> 判定用**两道**：先按文件名排除产物（`EXCLUDE_PATTERNS`），
> 再按内容确认（每行是含 `inputs` 列表的对象）。
> 只靠内容不稳——产物结构会变；只靠文件名也不够——下个批次多出新产物就漏了。

#### 落地布局：源文件名 → 采集脚本要求的文件名

采集脚本 `msprof_perf_summary.py` 硬编码了三个文件名，`prepare_op_dir.py` 负责搬运改名。
**对应关系按源文件名记**：

| 源文件（verify 目录 / benchmark 仓） | 落地为 | 里面必须有 |
|---|---|---|
| `<Op>_torch.py` | `model.py` | `class Model` + `get_input_groups()` |
| `<Op>_triton_optimized.py`（多份时取 optimized） | `model_new.py` | `class ModelNew` |
| `<Op>_torch.json` | `<Op>_perf_cases.jsonl` **和** `model.json` | 每行一个含 `inputs` 的 case |

用例要落两份是因为：采集脚本优先读 `*_perf_cases.jsonl`，而参考实现改名成 `model.py` 之后，
它内部 `os.path.splitext(__file__)[0] + ".json"` 派生出的路径会变成 `model.json`。
少写任何一份都会**静默**拿到错数据（见 pitfalls 坑 3 与坑 7）。

`prepare_op_dir.py` 还会校验类名、补齐硬编码的用例路径。原目录不动。

### 2. 测定极限 MFU 的 (case, 倍率) 点（求极限 MFU 时必做）

```bash
python3 $SKILL_DIR/scripts/max_shape_probe.py \
    --dir <工作目录>/<Op> \
    --flops-tool $SKILL_DIR/scripts/check_flops.py \
    --max-bytes 10e9 --max-ms 4000
```

把原始 case 放大后选出**同时通过五道闸**的配置，写回目录供后续采集直接使用。

> **放大哪些维度需要逐算子判断，不要交给脚本写死。**
> 主要放大 **seq_len 和 batch**：seq 让 attention 的 FLOPs 二次增长而显存只线性增长，
> 是提 MFU 的主要杠杆；batch 提并行度。
> 等比放大所有维度则会让体积按 `s^ndim` 爆炸（4D 张量 s=2 即 16 倍显存）。
>
> 判断依据：同一符号的 `(张量名, 轴)` 位置在所有 case 上取值必然相同，
> 按此分组可还原出 batch / seq_q / seq_k / heads / head_dim 的语义结构。
> **注意排除"每个张量的末轴"**（多为 head_dim），它的取值范围常比 seq 还大。
> 具体分组实例与档位建议见 `$KB_ROOT/ops/triton/guides/tooling/mfu_max_shape_search.md`。

> **极限 MFU ≠ 最大 shape 下的 MFU。** MFU 对 shape 不单调——小 shape 时数据在 cache 里，
> 放大后被打回 HBM，实测约 2/3 的算子放大后 MFU 反而**下降**。
> 极限 MFU 必须在 **(case, 倍率)** 二维候选空间里取最大值：
> 倍率维要含 `s=1`，case 维要含原始 top-3（不同 case 可能走不同代码路径，
> 实测 55_OutlookAttention 的 case11 只跑一个 kernel、MFU 高出 8 倍）。
>
> 成本控制分两级：**初筛**用墙钟遍历候选池（按 FLOPs 降序取前 8 个原始 case
> + 它们的合法放大变体，不开 msprof，只用于排序），**精测**只对前 3 名采 PMU。
> 最终数字一律取自精测的 kernel 时间。
> 取前 8 的依据、墙钟开销的实测标定见 `$KB_ROOT/ops/triton/guides/tooling/mfu_max_shape_search.md`。

五道闸（按代价从低到高，缺一不可）：

| 闸 | 判据 | 漏掉的后果 |
|---|---|---|
| 1 输入预算 | 总字节 ≤ `--max-bytes` | OOM |
| 2 **参考实现接受** | `class Model` 可追踪且 FLOPs>0 | shape 非法、分子算不出（实测 26/94 踩中） |
| 3 被测实现跑通 | `ModelNew` 在卡上不报错 | — |
| 4 单次耗时 | ≤ `--max-ms` | PMU 采集不现实 |
| 5 **有效带宽 ≤ HBM** | 输入字节/耗时 ≤ 1.3TB/s | 缩放静默未生效（实测 55/89 踩中） |

闸 2 和闸 5 是重点。**"被测实现能跑"不是合法性判据**——参考实现拒绝的 shape
语义上就不成立；闸 5 则是兜底，能挡住所有没预料到的失效方式。

放大不必然让 MFU 变高：实测 62 个算子里约 2/3 **下降**，因为小 shape 时数据在 cache 里，
放大后被打回 HBM，`aic_mte2` 成为主要的墙（多个达 0.9+）。这恰恰是真实负载下的样子。

完整方法（二维搜索、五道闸、两阶段、6 个坑）见 `$KB_ROOT/ops/triton/guides/tooling/mfu_max_shape_search.md`。

> **分子取语义值**：`min(参考实现追踪值, 硬件实测值)`。
> 两个可测分子的偏差方向相反——参考实现用稠密表达稀疏语义时偏大，
> kernel 有 tiling 补齐 / mask 丢弃时偏大——取较小者才接近 Model FLOPs。
> `mfu_grid_search.py` 已自动执行该规则并在结果里记录 `num_src` 与两种口径的值。
> 详见 `$KB_ROOT/ops/triton/guides/tooling/mfu_pitfalls.md`「分子该取哪个」。

### 3. 写 flops.py

放进工作目录，暴露 `flops(case) -> float`。**这是整条链路上唯一没有硬件校验的环节**：
写错不会报错，只会得到一个看起来很合理的数字。

> **分子来自 torch 参考实现，不是 triton 实现。** FLOPs 追踪的对象始终是含
> `class Model` 的 **torch** 文件（源目录里是 `<Op>_torch.py` 或 `<Op>.py`），
> 它定义了算子的语义；triton 实现（`<Op>_triton*.py` / `<Op>_generated.py`）
> 只提供分母（kernel 耗时），不参与分子计算。
>
> **源目录里没有 `model.py`** —— 那是 `prepare_op_dir.py` 落地后的改名结果。
> 下文凡出现 `model.py` 处，指的都是工作目录里已落地的那份，对应源文件是 `<Op>_torch.py`。

**动手前先读 torch 参考实现的 forward**——算子名字经常只描述最显眼的一段
（实测例：`20_FlashAttentionV2` 里 4 个投影占 94.7% 的 FLOPs，只算 attention
会让分子小 18 倍）。

想做 kernel 级拆解就再加 `flops_parts(case) -> dict` 和 `KERNEL_PARTS`。

**可选：先生成初稿再改。** 生成器按 AST 特征把算子分到 attention / GQA /
sparse / paged / window / FFN / matmul 等类别，套用对应模板：

```bash
python3 $SKILL_DIR/scripts/flops_generator.py \
    --model <工作目录>/model.py \
    --cases <工作目录>/<OpName>.json \
    -o      <工作目录>/flops.py
```

生成结果**必须人工 review**——模板只覆盖常见形态，稀疏/变长/rope 的边界要自己核对。

**写完必须自检：**

```bash
python3 $SKILL_DIR/scripts/check_flops.py --op-dir <工作目录>
```

校验 `flops_parts` 之和、FLOPs 是否为 0 或超峰值、`actual_seq_lengths` 与 shape
是否自洽，并 monkey-patch `torch.matmul`/`F.linear` 跑一遍参考实现做**独立对拍**。
tracer 比值 ≈1.0 说明分子写对了；≈2.0 通常是漏了 causal 缩减；<0.5 多半漏算了投影。

→ 口径、模板、自检办法见 `$KB_ROOT/ops/triton/guides/tooling/mfu_flops_guide.md`
→ 完整实例见 [`examples/flops_mha_block.py`](examples/flops_mha_block.py)

### 4. 采集

```bash
cd <工作目录>
python3 $SKILL_DIR/scripts/ops_profiling/msprof_perf_summary.py \
    --quick --mfu --impl asc --output-dir . \
    --warmup 5 --repeats 5 --keep-prof .
```

**不指定 case 时自动按理论 FLOPs 降序只测 top-3 大 shape**，这是默认也是推荐做法：
MFU 随规模饱和，最大几个 shape 就代表峰值水平，小 case 只是白花采集时间。

50 case 全量实测验证过这条：尾部 10 个小 shape（S≤23）MFU 全部 ≤0.2%，
而自动选出的 top-3 在标称和 dtype 修正两种口径下**都命中了全局最大值**。

- `--impl asc` 只跑被测实现，省掉参考实现的采集时间（不需要加速比时用）
- `--keep-prof` **必须加**，否则第 5 步没有数据可拆
- `--warmup/--repeats` 是**被采集进程内**的迭代数，解析时丢弃 warmup 份
- `--mfu-top-k N` 改数量；`--cases 3,7,9` 显式指定；
  `--max-cases <N≥用例数>` 跑全量（50 case 约 1 小时，仅在需要完整分布时才做）

耗时参考：top-3 × (warmup 5 + repeats 5) 约 4 分钟。

### 5. 标定各 dtype 的算力上限

```bash
python3 $SKILL_DIR/scripts/peak_calib.py -o peak.json
```

ops-profiling 推的峰值**与 dtype 无关**，实际是 fp16/bf16 峰值。fp32 case 直接用它
会低估约 4 倍（实测 910B2C：fp16/bf16 ~314-320，fp32 ~85 TFLOPS）。

> 该脚本运行时会打印大量 CANN HCCL 的 `tiling struct ... is conflict` 警告，
> 与 GEMM 峰值测量无关，可忽略；最终结果表格在输出末尾。

### 6. 拆解与修正

```bash
python3 $SKILL_DIR/scripts/mfu_decompose.py --op-dir . --peak-json peak.json
```

不需要重复指定 case、warmup/repeats 或 PROF 路径——这些全部从第 3 步产出的
`performance.json` 里读：**采集测了哪三个 case，这里就拆哪三个**。

输出每个 case 的：总 MFU（标称口径 / dtype 修正口径）、每个 kernel 段的耗时与
各自的 MFU，并给出最大值。明细落到 `mfu_decompose.json`。

`--cases 46` 可以只看其中几个；`--report <另一份.json>` 可以拆历史轮次。

---

## 输出怎么读

拿到一张这样的表（实测 `20_FlashAttentionV2`）：

```
case dtype      total us  TFLOPS  MFU@nom  MFU@ach   attn us  attn MFU   proj us  proj MFU
46   float16       271.8    58.6   16.57%    18.7%     166.9      1.6%     104.9     45.8%
48   float32       588.7    36.0   10.18%    42.5%     197.7      7.7%     391.0     60.1%
```

三步判断：

1. **先看 dtype 与 `MFU@ach`。** `MFU@nom` 只在同 dtype 内可比。
   case 48 从 10.18% 变 42.5%，结论完全反转。
2. **再看哪一段拖后腿。** case 46 的投影 45.8%（正常 GEMM 水平），
   attention 1.6%——差距全在 attention。同时注意**理论 FLOPs 占比与耗时占比的错配**：
   attention 只占 5.3% 的 FLOPs 却吃掉 61% 的时间。
3. **最后判断瓶颈类型。** 比同一 kernel 在 fp32 与 fp16 下的**绝对吞吐**：
   若 fp32 没有掉到 fp16 的 ~1/4，说明 cube 在空等，优化 cube 利用率不会有收益。

→ 完整解读手法与全部已知坑见 `$KB_ROOT/ops/triton/guides/tooling/mfu_pitfalls.md`

---

## 与 PMU 口径的分工

| | 本 skill（官方 MFU 口径） | PMU（ops-profiling `--compare` 的 ArithmeticUtilization） |
|---|---|---|
| 分子 | 理论 FLOPs（语义必需） | 实际执行 MAC（含冗余、tile padding） |
| 归一 | 全部 cube 核 × 峰值 | **活跃核 × 运行时频率** |
| 小 shape | 正确反映核铺不满 | 按活跃核归一会**严重虚高** |
| 回答 | 离硬件极限多远、还能优化多少 | 瓶颈在哪条流水线 |

两者差距揭示冗余计算量（实际执行 FLOPs / 理论 FLOPs）。横向对比一律以官方口径为准。

---

## 文件

```
scripts/prepare_op_dir.py                目录适配 + 用例路径补齐 + 类名校验
scripts/max_shape_probe.py               测定可承载的最大 shape（五道闸 + 二分细化）
scripts/mfu_grid_search.py               (case,倍率) 二维搜索极限 MFU（阶段一，墙钟计时）
scripts/flops_generator.py               按算子类别生成 flops.py 初稿（需人工 review）
scripts/check_flops.py                   flops.py 自检 + tracer 独立对拍
scripts/peak_calib.py                    各 dtype 实测算力上限 → peak.json
scripts/mfu_decompose.py                 按 kernel 拆 MFU + 按 dtype 修正峰值
scripts/ops_profiling/msprof_perf_summary.py   采集脚本（ops-profiling 扩展副本，支持 --mfu）
$KB_ROOT/ops/triton/guides/tooling/mfu_flops_guide.md        flops.py 口径、模板、自检
$KB_ROOT/ops/triton/guides/tooling/mfu_pitfalls.md           坑清单 + 瓶颈判别手法 + 经验水位
$KB_ROOT/ops/triton/guides/tooling/mfu_max_shape_search.md   极限 MFU 的二维搜索、缩放规则、五道闸、6 个坑
$KB_ROOT/ops/triton/guides/tooling/mfu_pmu_guide.md          PMU 是什么、各流水计数器含义、bound 判据、常见误读
$KB_ROOT/ops/triton/guides/tooling/mfu_profiling_guide.md    --mfu 参数与产出字段说明
examples/flops_mha_block.py              实测用过的完整 flops.py（MHA block，含 causal）
examples/flops_sparse_flash_attention.py 实测用过的完整 flops.py（稀疏 + 变长 + rope）
```

## 依赖

- 真实昇腾 NPU 环境（`npu-smi` 可用）、CANN 环境变量已 source
- `torch` + `torch_npu`
- 采集前确认 `echo $ASCEND_HOME_PATH` 与 `which msprof` 指向预期的 CANN，
  非交互 shell 可能读不到 `set_env.sh`，会静默跑在旧 CANN 上（见 pitfalls 坑 6）
