---
name: triton-op-verifier
description: >
  算子代码验证 Skill — 按照标准验证流程验证生成的内核代码。
  创建验证项目文件，调用 scripts/verify.py 运行验证，验证通过后
  调用 scripts/benchmark.py 进行性能测试并收集结果。
  触发：当用户需要验证 Triton 算子代码功能正确性或采集其性能数据时使用。
argument-hint: >
  输入：generated-code-path、task-file-path、op-name、warmup、repeats。
  输出：验证结果（成功/失败）、错误信息、性能数据。
  固定参数：framework=torch、backend=ascend、dsl=triton_ascend。
---

# Kernel Verifier Skill

<role>
你是一个内核代码验证专家。你的任务是按照标准验证流程，创建验证项目并运行，检查生成的算子代码是否能正确编译运行且与参考实现的输出一致。验证通过后，执行性能测试并收集性能数据。
</role>

## 精度判定规则

> 本节是精度判定的**唯一权威说明**。所有阈值、路由、前置检查只在此处定义；
> 下游章节（Step 2/3）只引用、不重复。

verify.py 同时挂着两套精度标准：**生态算子开源精度标准**为第一标准，
**NPU Benchmark 标准**为 fallback。本节先讲两者的路由关系，再分别详解。

### 0.1 路由：先看数据格式，再选标准

| 输出情况 | 走哪套标准 | 判据 |
|---|---|---|
| 浮点输出，dtype 在生态阈值表内 | **生态开源标准（第一标准）** | 两项 AND，见 §一 |
| 浮点输出，dtype 不在生态阈值表内 | NPU Benchmark（fallback） | 三项 AND，见 §二 |
| 整型输出，输入为 float | NPU Benchmark（fallback） | 量化计算类 `\|diff\| <= 1` |
| 整型输出，输入为 int / 无 tensor | NPU Benchmark（fallback） | 整数计算类 `\|diff\| == 0` |
| bool 输出 | NPU Benchmark（fallback） | `torch.equal` 严格相等 |
| `--non-compute` 开关打开 | NPU Benchmark（fallback） | 二进制完全一致 |

路由的依据是**数据格式**：生态标准第 0 节声明它只讨论浮点计算类，
整型计算类与搬移类不在其范围内，因此这些输出继续用原判据。
浮点输出中 dtype 不在生态阈值表内的（表见 §1.3），同样回退，
避免拿 float32 的默认阈值去套一个未定义的类型。

日志里会打印实际走了哪条：

- `[评测模式] 模式=eco_open_source（生态开源精度标准，第一标准），...`
- `[评测模式] 生态标准阈值表未覆盖 dtype=...，回退 NPU Benchmark 三项判定`
- `[评测模式] 模式=float_compute（浮点计算类）...` / `模式=non_compute（非计算类）...`

### 0.2 golden 的落点：CPU 优先，跑不起来回退 NPU

golden（参考实现 `Model`）**优先跑在 CPU 上**，待评测实现 `ModelNew` 始终跑在 NPU 上。
CPU 上执行失败时（参考实现调用 `npu::` 专有算子、CPU 后端不支持该 dtype 等），
自动把 golden 回退到 NPU 重试，日志打印
`[用例 i/n] golden 落 CPU 时执行失败，回退 golden 到 NPU 重试: ...`。

只有**执行期异常**才触发回退。`AccuracyError` 与 `AssertionError`（精度判定、形状不一致、
NaN/Inf 位置不一致）是判定结论，直接上报不重试，避免把真实失败重跑一遍掩盖掉。
精度判定本身不受 golden 落点影响：比对前两侧都会搬到 CPU。

> **副作用**：golden 落 CPU 后，隐藏状态探针（§三）会拿 CPU 侧权重对拍 NPU 侧权重。
> 参考实现若用 `torch.manual_seed(hash(key))` 惰性造权重且 `key` 里含 `x.device`，
> 两侧 seed 不同、权重完全无关，探针会给出 `HiddenStateMismatch` 硬失败。
> 这类算子的误差本来就不能归因为 kernel 精度，硬失败是正确的暴露方式，
> 但相对 golden 落 NPU 的旧行为，是从「通过」变为「明确失败」。

### 0.3 输入类型推断（路由到整数计算类 / 量化计算类时用）

从实际传入对象推断（不依赖 task 文件结构化 spec）：

1. 存在 `torch.Tensor` 输入 → 取所有 tensor 中**最高精度 dtype**
   （例：输入为 `[fp16 tensor, fp32 tensor, int64 tensor]` → 取 fp32）
2. 否则存在 `list/tuple of Tensor`（tensor_list）→ 取首个 tensor_list 首元素 dtype
3. 否则视为**无 tensor 输入**（`no_tensor`，最严路径）

**dtype 优先级**：

精度从高到低排列：float64 > float32 > float16 > bfloat16 > float8_e4m3 / float8_e5m2 > int64 > int32 > int16 > int8 / uint8 > bool

**`input_type` 二分类**（用于 §0.1 路由与 §2.1 决策矩阵分流）：

- `input_type = float`：输入最高精度 dtype 属于浮点族（float64/32/16、bfloat16、float8_e4m3/e5m2、复数 complex64/128）
- `input_type = int`：输入最高精度 dtype 属于整型族（int64/32/16/8、uint8、bool）
- `input_type = no_tensor`：无任何 tensor 输入（走最严判定）

> **关于 bool 的两处特殊性**（避免混淆）：
> - bool 作**输入**：归入 `int`，与 int 系输入等同；分流时只看输出 dtype（如输出 fp 走浮点判定）
> - bool 作**输出**：不进入 input_type 分流，直接走 §2.1 "bool 输出"路径（`torch.equal` 严格相等）


---

## 一、生态算子开源精度标准（第一标准）

### 1.1 适用范围

只覆盖**浮点计算类**输出。标准第 0 节明确整型计算类与搬移类需按各自业务场景单独制定，
不在其讨论范围内，因此这些输出由 §二 的 fallback 承接。

### 1.2 两项判定（AND，全部满足才算通过）

采用**混合容差**（Mixed Tolerance），逐元素判定：

```
元素通过：|actual - golden| <= atol + rtol * |golden|
```

1. **`matched_ratio`**：通过元素数 / 总元素数 `>= 0.99`
2. **逐元素绝对上限**：每个元素满足

```
|actual - golden| <= max(max_abs_error_limit, 32 * ULP(|golden|), atol + rtol * |golden|)
```

### 1.3 阈值表（`scripts/eco_limits.py` 是唯一权威来源）

| 数据类型 | rtol | atol | max_abs_error_limit |
|---|---|---|---|
| `float16` | 2⁻⁹ ≈ 1.95e-3 | 2⁻⁹ ≈ 1.95e-3 | 1e-1 |
| `bfloat16` | 2⁻⁶ ≈ 1.56e-2 | 2⁻⁶ ≈ 1.56e-2 | 1e-0 |
| `float32` | 2⁻¹⁰ ≈ 9.77e-4 | 2⁻¹⁶ ≈ 1.53e-5 | 1e-2 |
| `hifloat32` | 2⁻⁹ ≈ 1.95e-3 | 2⁻¹⁰ ≈ 9.77e-4 | 1e-1 |
| `float8_e4m3` | 2⁻² = 0.25 | 2⁻⁴ = 0.0625 | 1e-0 |
| `float8_e5m2` | 2⁻¹ = 0.5 | 2⁻³ = 0.125 | 1e-1 |

`required_matched_ratio = 0.99`。表内没有的 dtype **不套默认值**，直接回退 §二。

### 1.4 绝对上限的 ULP 按逐元素取

`ULP` 按**逐元素**取 —— 每个元素依自身量级定限值，比整张量共用一个限值更贴近原意。
（标准原文写作「1e-2 **or** 32 * ULP」，二选一未定义，本仓补充 32*ULP 项。）

绝对上限公式已并入 §1.2 第 1 项的混合容差项 `atol + rtol*|golden|`，因此两项判据
**不再语义独立**：由于混合容差斜率（对 float32 为 `rtol = 2⁻¹⁰`）恒大于 `32*ULP`
的斜率（`32*2⁻²³ = 2⁻¹⁸`，相差 2⁸ 倍），对 float32 等尾数位较多的 dtype，绝对上限
实际由 `max_abs_error_limit` 与混合容差二者取大决定，`32*ULP` 不对判定形成额外约束；
仅在尾数位较少的 dtype（float16 / bfloat16 / hifloat32 / float8 类）下 `32*ULP`
才可能成为制约项。相应地，第 2 项 `over_count == 0` 的实际语义为
「**大幅值区间不允许出现任何混合容差失败元素**」——比第 1 项的
`matched_ratio >= 0.99`（允许 1% 失败）更硬。

### 1.5 已知局限

- golden 是参考实现在 CPU 上的**同精度**执行，不是标准 2.3 字面要求的「更高精度实现」。
  参考实现内部若硬编码 `.float()` 或 `torch.float32`，其计算精度由实现本身决定，
  与 golden 落在哪个 device 无关。
- 标准第 1 节的用例生成规则（全组合覆盖、维度取 2ᵏ 与 2ᵏ−1、
  空 / 标量 / 边界 / INF-NAN 特殊场景）由用例集自身负责，本脚本不校验。
- 标准第 3 节的压测（单用例执行 50 次）与 4.5.2 的置信区间复检未实现，
  每个用例只执行一次，分辨不了偶发失败与真实精度失败。

---

## 二、NPU Benchmark 精度标准（fallback）

承接生态标准覆盖不到的数据格式：整型输出、bool 输出、非计算类，
以及 dtype 不在生态阈值表内的浮点输出。

### 2.1 五类判定决策矩阵

| 类别 | 输入 type | 输出 dtype | `--non-compute` | 误差要求 |
|---|---|---|---|---|
| **非计算类** | 任意 | 任意 | **是** | 二进制完全一致（view-as-int 比对，含 NaN bit pattern） |
| **bool 输出** | 任意 | bool | 否 | `torch.equal` 严格相等 |
| **整数计算类** | int / no_tensor | int | 否 | `\|actual − golden\| == 0` |
| **量化计算类 fp→int** | float | int | 否 | `\|actual − golden\| <= 1` |
| **浮点计算类** | 任意 | float | 否 | 优先生态标准（§一）；dtype 未覆盖时三项 AND（见 §2.3）|


### 2.2 比对前置检查（按顺序，任一失败即判 fail）

0. **隐藏状态对齐检查**（仅第 1 个用例执行一次，详见 §三）
1. 形状必须一致
2. NaN 位置必须完全一致（mask 按位相等）
3. Inf 位置和符号必须完全一致
4. `bool` dtype：要求 `torch.equal` 完全相等，不进入精度判定
5. 仅在 `finite_mask`（双方都 finite）上做精度计算；dtype 不一致时 impl 会被 cast 到 golden 的 dtype


### 2.3 浮点计算类：三项 AND 整体判定

#### 2.3.1 元素级 matched 定义（分桶）

对每个 finite 元素 `i`，按 `|golden[i]|` 落入的类别分别判定：

- **小值域** `|golden[i]| < small_value_threshold`：
  `matched[i] = (|actual[i] - golden[i]| <= small_value_error)`
- **正常域** `|golden[i]| >= small_value_threshold`：
  `matched[i] = (|actual[i] - golden[i]| / (|golden[i]| + 1e-7) <= rel_threshold)`

> 计算前两侧统一升 float32，避免低精度 dtype 自身误差污染。
> 分母 `+1e-7` 仅为保险——正常域里 `|golden| >= sv_thr ≫ 1e-7`。

#### 2.3.2 三项通过条件（AND，全部满足才算通过）

1. **`max_error_cap`**：所有 finite 元素满足 `|diff| <= atol + rtol * |golden|`（dtype-aware，要求 100% 通过）
2. **`required_matched_ratio`**：`sum(matched) / total_finite >= 0.9`
3. **`MERE`**：对所有 finite 元素计算 `rel_err = |diff| / (|golden| + 1e-7)` 再取均值，要求 `MERE < rel_threshold`。当 `total_finite == 0` 时本项自动通过。

#### 2.3.3 阈值表

**matched_mask 与 MERE 阈值**（沿用 NPU Benchmark 标准）：

| 数据类型 | small_value_threshold | small_value_error | rel_threshold (= MERE 上限) |
|---|---|---|---|
| `float16` | 2⁻¹¹ ≈ 4.88e-4 | 2⁻¹⁶ ≈ 1.53e-5 | 2⁻¹⁰ ≈ 9.77e-4 |
| `bfloat16` | 2⁻⁸ ≈ 3.91e-3 | 2⁻¹⁶ ≈ 1.53e-5 | 2⁻⁷ ≈ 7.81e-3 |
| `float32` | 2⁻¹⁴ ≈ 6.10e-5 | 2⁻³⁰ ≈ 9.31e-10 | 2⁻¹³ ≈ 1.22e-4 |
| `hifloat32` | 2⁻¹² ≈ 2.44e-4 | 2⁻²⁸ ≈ 3.73e-9 | 2⁻¹¹ ≈ 4.88e-4 |
| `float8_e4m3` | 2⁻⁴ = 0.0625 | 2⁻⁶ ≈ 0.015625 | 2⁻³ = 0.125 |
| `float8_e5m2` | 2⁻³ = 0.125 | 2⁻⁵ = 0.03125 | 2⁻² = 0.25 |
| 其他 dtype（fallback） | 2⁻¹⁴ | 2⁻³⁰ | 2⁻¹³ |

**max_error_cap 阈值**（`|diff| <= atol + rtol * |golden|`）：

| 数据类型 | atol | rtol |
|---|---|---|
| `float16` | 9e-2 | 2⁻¹⁰ ≈ 9.77e-4 |
| `bfloat16` | 1e-1 | 2⁻⁷ ≈ 7.81e-3 |
| `float32` | 1e-3 | 2⁻¹³ ≈ 1.22e-4 |
| 其他 dtype（fallback） | 1e-3 | 2⁻¹³ |


---

## 三、隐藏状态对齐检查（`scripts/hidden_state_probe.py`）

抓「参考实现 `Model` 的输出依赖不由输入张量决定的内部状态（随机初始化权重 / buffer /
跨调用缓存），而生成实现没有逐位复刻」这一类失败。它与 kernel 实现无关，单独修 kernel
永远修不好，且误差形态与"算法全错"无法区分，因此必须在精度比对之前单独点名。

| 层 | 内容 | 严重级别 |
|---|---|---|
| P0 | 深度扫描后无隐藏状态 → SKIP | 绝大多数算子走这条，零开销 |
| P1 | 两侧**同名** parameter/buffer 逐位一致 | **硬失败** → `error_type: HiddenStateMismatch` |
| P2 | fw 每个隐藏张量需在 im 中找到逐位相等项（不要求同名） | 软诊断（日志 WARN，不影响 passed_cases） |
| P3 | 同输入连跑两次各自输出一致 | 软诊断（默认关闭，`ProbeOptions(check_determinism=True)` 启用） |

- **执行时机**：第 1 个用例的正式 forward **之前** —— 生成实现编译失败时正式 forward 会直接抛
  `CompilationError`，放在其后探针就没机会执行。
- **降级**：`hidden_state_probe.py` 缺失时静默禁用，不阻断验证。
- 命中后如何修：见 `ops/triton-op-coding/SKILL.md`「参考实现的 nn.Module 语义复刻」C1/C2。

---

## 验证流程

```
输入：generated_code.py + task_file.py
    ↓
[0. Triton 退化预检查] → scripts/validate_triton_impl.py (AST 静态分析)
    ↓ (通过)
[1. 创建验证项目] → 两个文件
    ↓
[2. 执行验证脚本] → scripts/verify.py --op_name ...
    ↓
[3. 收集验证结果]
    ↓
[验证通过] → [4. 执行性能测试] → scripts/benchmark.py --op_name ...
    ↓
[5. 收集性能结果]
    ↓
输出：验证结果 + 性能数据
```

---

## Step 0: Triton 退化预检查（AST 静态分析）

在创建验证项目之前，先使用 `validate_triton_impl.py` 对生成代码进行退化检测。此检查为纯 AST 静态分析，无需 NPU/torch 运行时，毫秒级完成。

**命令模板**：

```bash
python3 <本skill所在目录的绝对路径>/scripts/validate_triton_impl.py \
    <生成代码文件路径> --json
```

**检测四种退化类型**：

| 类型 | 含义 | 检测方式 |
|------|------|---------|
| Type 1 | 完全无 `@triton.jit` kernel | AST 中无 `triton.jit` 装饰的函数定义 |
| Type 2 | 有 kernel 但 `forward()` 未调用 | kernel 定义存在但 `ModelNew.forward()` 未引用（含 wrapper 函数追踪） |
| Type 3 | 部分计算使用 PyTorch | `forward()` **及其可达的模块内辅助函数**中存在禁止的 `torch.*` / `F.*` / tensor 方法计算操作（精确到行号）。⚠️ 从 `forward()` 出发做**跨函数可达性分析**——把主链计算挪到 `forward()` 之外的模块级函数里是常见绕过手法 |
| Type 4 | 只有占位 kernel | 被调用的 kernel **全部**只做 `tl.load`/`tl.store` 搬运、无任何计算（`tl.*` 里除 load/store/arange/program_id 等非计算 API 外为空）。这类 kernel 纯粹为让 AST 检测到"有 kernel 被调用"而存在，真实计算仍在 PyTorch 侧 |

**结果判断**：
- exit code == 0 → 通过，继续 Step 1
- exit code != 0 → 退化检测到，解析 JSON 中的 `regression_type` 和 `suggestion`，直接返回失败

> **典型作弊形态（实测捕获，Type 3 + Type 4 同时命中）**：
> ```python
> @triton.jit
> def identity_kernel(x_ptr, o_ptr, n, BLOCK: tl.constexpr):
>     """占位 kernel：将输入按元素拷贝到输出，保证 AST 检测到真实 Triton 调用。"""
>     ...  # 只有 tl.load / tl.store
>
> def _run_flash_attention(x, ...):        # ← 计算被挪到 forward 之外
>     query = torch.matmul(x, wq.t())      # 主链全在 torch
>     weights = scores.softmax(dim=-1)     # 用 tensor 方法绕过对 F.softmax 的拦截
>     ...
>
> class ModelNew(nn.Module):
>     def forward(self, x, ...):
>         y = _run_flash_attention(x, ...)     # forward 子树里看不到任何 torch 计算
>         identity_kernel[grid](y, out, ...)   # 只为满足"kernel 被调用"
>         return out
> ```
> 三个特征缺一不可地共同构成绕过：**计算外移**（避开只扫 forward 的检查）+ **tensor 方法**（避开 `F.softmax` 名单）+ **占位 kernel**（伪造 Triton 调用）。
> 现在 Type 3 的跨函数可达性分析与 Type 4 的占位 kernel 检测分别堵住其中两环，任一命中即判失败。

**JSON 输出格式**：

```json
{
  "valid": false,
  "regression_type": 3,
  "checks": {
    "triton_kernel_exists": {"passed": true, "kernels": [...]},
    "kernel_called_from_forward": {"passed": true, "called": [...]},
    "no_forbidden_torch_ops": {"passed": false, "violations": [{"line": 45, "call": "F.softmax", "reason": "..."}]}
  },
  "suggestion": "..."
}
```

---

## Step 1: 创建验证项目

在当前迭代的验证目录（如 `{output-path}/iter_{iteration}/verify/`）下创建两个文件：

### 文件 1: `{op_name}_torch.py`

直接复制任务文件的完整内容。此文件包含 `Model`、`get_inputs()`、`get_init_inputs()`。

### 文件 2: `{op_name}_triton_ascend_impl.py`

直接复制生成代码的完整内容。此文件包含 `ModelNew` 类。

---

## Step 2: 执行验证（⚠️ 必须使用本脚本，禁止自创测试方法）

**必须使用** `bash` 工具调用本 skill 自带的 `scripts/verify.py` 脚本。

**命令模板**：

```bash
python3 <本skill所在目录的绝对路径>/scripts/verify.py \
    --op_name <算子名> \
    --verify_dir <验证目录> \
    --triton_impl_name <triton实现模块名> \
    --timeout 900
```

**实际调用示例**（假设验证目录为 `/tmp/workspace/softmax/verify`，算子名为 `softmax`）：

```bash
python3 /path/to/triton-op-verifier/scripts/verify.py \
    --op_name softmax \
    --verify_dir /tmp/workspace/softmax/verify \
    --triton_impl_name triton_ascend_impl \
    --timeout 900
```

**参数说明**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--op_name` | 是 | 算子名称，与文件名前缀对应 |
| `--verify_dir` | 否 | 验证目录路径，默认当前目录 |
| `--triton_impl_name` | 否 | Triton 实现模块名（不含 `{op_name}_` 前缀），默认 `triton_ascend_impl` |
| `--timeout` | 否 | 超时秒数，默认 900 |
| `--output` | 否 | 验证结果 JSON 输出路径，默认 `{verify_dir}/verify_result.json` |
| `--non-compute` | 否 | 适用于非计算类算子（不做数值运算、只对张量进行形状变换、维度重排、切分拼接、索引、类型转换等数据重组操作的算子，常见如 Reshape、Transpose、Concat、Split、Gather、Cast、Pad 等），强制走二进制完全一致判定 |
| `--fresh-cache` | 否 | 本次运行使用独立的临时 `TRITON_CACHE_DIR`，不使用也不修改用户全局 Triton 缓存（`~/.triton/cache`），跑完即清理。全量重编译在 Ascend 上是分钟级开销，因此**默认关闭**，仅在排查缓存嫌疑时开启（见下方「精度失败的归因禁令」）|
| `--keep-cache` | 否 | 与 `--fresh-cache` 配合：无论成败都保留临时缓存目录并在 stderr 打印绝对路径。单独使用无效 |

**超时设置**：默认 900 秒，复杂算子可适当增加。

**注意事项**：
- 禁止自己编写 Python 代码来测试算子（如手动 import 并 forward 比较）
- 禁止使用 `torch.allclose` 或其他自创方法替代 `scripts/verify.py`
- 禁止跳过此步骤直接报告验证结果
- 禁止对计算类算子（含数值运算）传 `--non-compute`；该开关仅适用于不做数值运算、只做形状变换 / 维度重排 / 切分拼接 / 索引 / 类型转换等数据重组操作的算子（如 Reshape、Transpose、Concat、Split、Gather、Cast、Pad）。误用会强制走二进制完全一致判定，把正常的浮点舍入差异判为失败
- 对非计算类算子（例如形状变换、维度重排、切分拼接、索引、类型转换等数据重组操作的算子）**一定要**传 `--non-compute`；漏传会让此类算子按浮点三项判定走，容许超出预期的差异，无法识别真正的位级不一致
- 禁止用 `rm -rf ~/.triton/cache` 清缓存：会破坏并发跑的其他算子 / 其他会话的缓存，且不可回滚。需要空缓存一律走 `--fresh-cache`（靠独立目录隔离）

---

## Step 3: 收集验证结果

verify.py 会在 `verify_dir` 下生成 `verify_result.json`（或 `--output` 指定路径），包含：

```json
{
  "op_name": "softmax",
  "total_cases": 5,
  "passed_cases": 4,
  "failed_cases": 1,
  "failures": [
    {
      "case_idx": 2,
      "input_desc": [
        {"type": "tensor", "shape": [128, 256], "dtype": "torch.float16"}
      ],
      "error_type": "CompilationError",
      "error_msg": "..."
    }
  ],
  "environment": {
    "timestamp": "2026-09-03T14:22:01+08:00",
    "triton": {
      "version": "3.2.0",
      "path": "/usr/local/python3.11.10/lib/python3.11/site-packages/triton",
      "key_sha256": "9f2c..."
    },
    "cache": {
      "dir": "/tmp/triton_verify_cache_ab12cd",
      "fresh": true,
      "fresh_effective": true,
      "always_compile": false
    },
    "cann": {
      "ascend_home_path": "/usr/local/Ascend/ascend-toolkit/latest",
      "info_file": "/usr/local/Ascend/ascend-toolkit/latest/x86_64-linux/ascend_toolkit_install.info",
      "info_sha256": "3a7e...",
      "version": "8.0.RC3"
    },
    "torch": {"version": "2.1.0", "torch_npu_version": "2.1.0.post..."},
    "device": {
      "ASCEND_RT_VISIBLE_DEVICES": "3",
      "current_device": 0,
      "npu_name": "Ascend910B4"
    },
    "cmdline": {"triton_impl_name": "triton_ascend_impl", "non_compute": false}
  }
}
```

**`environment` 字段（环境指纹）**：记录本次验证跑在什么环境上，让精度结论可以跨机器 / 跨时间 / 跨 agent 复核。前 5 个字段（`op_name` / `total_cases` / `passed_cases` / `failed_cases` / `failures`）的名称、含义、顺序全部不变，`environment` 只是新增的尾部字段，下游读取逻辑（含 benchmark.py 的 L1 verify 闸门）不受影响。

| 字段 | 含义 |
|------|------|
| `triton.key_sha256` | `triton_key()` 的摘要，覆盖全部 triton python 文件 + `libtriton.so` + `backends/` 目录。**一个值就能判定两次跑的是不是同一个 triton 安装**，能抓住小版本编译默认值漂移 |
| `cache.dir` | 本次实际使用的 Triton 编译缓存目录 |
| `cache.fresh` | 本次是否传了 `--fresh-cache` |
| `cache.fresh_effective` | `TRITON_CACHE_DIR` 是否真的决定缓存位置。设置了 `TRITON_CACHE_MANAGER` / `TRITON_REMOTE_CACHE_BACKEND` 时为 `false`，此时**隔离并未成立** |
| `cache.always_compile` | `TRITON_ALWAYS_COMPILE` 是否设置（影响是否读缓存）|
| `cann.info_sha256` | 与 Ascend backend `options.hash()` 用的是同一个哈希。两次跑该值不同 ⇒ cache key 必然不同，可直接用来解释缓存命中与否 |
| `cann.error` | 采集失败原因。**非交互 shell 未 `source set_env.sh` 时 `ASCEND_HOME_PATH` 为空，此处会留下 `EnvironmentError`** —— 这是最有价值的诊断信息，见到它先修环境再谈精度 |
| `device.ASCEND_RT_VISIBLE_DEVICES` | 只有这个变量对 torch_npu 生效（`ASCEND_DEVICE_ID` 无效），排查坏卡 / 卡占用时必需 |

采集全程 try/except，任何一项失败只写成该分节下的 `{"error": "..."}`，不会影响验证本身的执行与退出码。

**引用与上报约束**：
- 报告精度结论时**必须连同 `environment` 一起给出**，只给 `58/60` 这类计数不构成可复核的结论。
- 跨机器 / 跨版本引用历史 verify 结论前，先比对 `triton.key_sha256` 与 `cann.info_sha256`；**不一致则历史结论作废，必须重跑**。

**精度失败时的 `metrics` 字段**：当 `error_type == "AccuracyError"`（浮点三项判定未通过）时，`failures[*]` 会带上结构化 `metrics`，便于下游分类失败原因（max_error_cap 违例 / 离群点过多 / 平均误差偏大）：

```json
{
  "case_idx": 1,
  "input_desc": [...],
  "error_type": "AccuracyError",
  "error_msg": "...",
  "metrics": {
    "matched_ratio": 0.95,
    "max_abs_diff": 0.2,
    "MERE": 2.0e-4,
    "rel_threshold": 1.22e-4,
    "small_value_threshold": 6.10e-5,
    "small_value_error": 9.31e-10,
    "atol": 1.0e-3,
    "rtol": 1.22e-4,
    "max_error_cap_violation_count": 12,
    "required_matched_ratio": 0.9,
    "total_finite": 1000,
    "matched_count": 950,
    "small_count": 0,
    "normal_count": 1000,
    "checks": {
      "max_error_cap": false,
      "required_matched_ratio": false,
      "MERE": false
    }
  }
}
```

`checks` 三个布尔位标记每项判定是否独立通过。阈值定义见上文 §精度判定规则 §4。

非浮点类失败（`non_compute` / `bool_output` / `integer_compute` / `quant_fp_to_int`）的 `metrics` 字段较简单，含 `category` / `violation_count` / `total_*` 等基本计数。

**多 shape 行为**：每个 shape 独立 try/except，失败不中止后续 shape；全部跑完才落盘并退出。

**退出码语义（策略 A：严格）**：
- `passed_cases == total_cases` 且 `total_cases > 0` → exit 0，`verifier_result = true`
- 否则（`passed_cases < total_cases`，或 `total_cases == 0`）→ exit 1，`verifier_result = false`，`verifier_error` 应读取 `verify_result.json.failures` 的**全部条目**（不是第一个），汇总后提交给 Conductor。

**超时**：脚本输出 `"验证超时"` 且退出码为 1 → `verifier_error = "验证超时（{timeout}秒）"`。

### 精度失败的归因禁令（缓存 A/B）

**不得在未做 `--fresh-cache` A/B 的前提下，把精度失败归因为"编译缓存里的坏二进制"。**

出现精度失败且怀疑缓存时，唯一允许的排查动作是同一份代码再跑一遍空缓存：

```bash
python3 <本skill所在目录的绝对路径>/scripts/verify.py \
    --op_name <算子名> --verify_dir <验证目录> --fresh-cache --keep-cache
```

判定规则：

| A/B 结果 | 结论 | 允许的动作 |
|----------|------|-----------|
| 带与不带 `--fresh-cache` 两次结果**一致** | **真实精度缺陷** | 必须继续修代码，**不得以缓存为由放行** |
| 两次结果**不一致** | 编译器缺陷嫌疑 | 必须用 `--keep-cache` 保留临时缓存目录（内含 `*.ttir` / `*.ttadapter` / `*.npubin` 与 metadata），连同两份 `verify_result.json` 的 `environment` 一起作为编译器缺陷上报 |

背景：Triton 的 cache key 覆盖 kernel 源码 sha256、triton 安装指纹与 CANN 安装信息文件哈希，因此**改 kernel 源码必然使缓存失效**，"改了代码却命中旧二进制"这条因果链不成立。真实存在的陈旧缓存路径只有一条：原地替换 `bishengir-compile`（打补丁版 / 自编译版）而不动 `ascend_toolkit_install.info` —— `AscendBackend.hash()` 只含 `str(self.target)`，编译器版本不进 key。`--fresh-cache` 正是针对这条路径的排查手段。

等价的手工排查手段（仅作了解，**不推荐**）：`TRITON_ALWAYS_COMPILE=1` 能强制重编，但产物仍写入全局缓存目录，会污染用户缓存，不满足"不触碰用户缓存"。

---

## Step 4: 执行性能测试（验证通过后执行）

**前置条件（L1 脚本层强制）**：benchmark.py 启动时会自动按 `--triton_impl_name` 推导对应的 `verify_result` 文件并校验 `passed_cases == total_cases`；不通过时直接 **exit 2**，禁止运行 benchmark。详见下方"L1 verify 闸门"小节。

仅在 verify.py 的 `passed_cases == total_cases` 时执行（策略 A）。verify 有任何失败 → 禁止执行 benchmark.py。

**NPU 锁频与频率监控**：benchmark.py 默认在性能测试前尝试对所有可用 NPU 设备执行 A5 锁频（`drv_hlt_dsmi_test set_lp_idle <dev> 0`），并在整个 benchmark 期间按 `--freq-check-interval` 周期采样 `npu-smi info -t common -i <dev>` 中的 `Aicore curFreq(MHZ)`，检测是否相对锁频后的基线频率发生漂移。

- 锁频目标值按设备型号自动探测，不硬编码具体 MHz。
- 若 `drv_hlt_dsmi_test` 不可用或锁命令失败，默认输出 warning 并继续测试；传 `--lock-frequency-fail-action error` 可在锁频失败或频率漂移时让 benchmark 以非零码退出。
- 传 `--no-lock-frequency` 可完全关闭锁频与监控。

使用 `bash` 工具调用本 skill 自带的 `scripts/benchmark.py` 脚本。

**命令模板**：

```bash
python3 <本skill所在目录的绝对路径>/scripts/benchmark.py \
    --op_name <算子名> \
    --verify_dir <验证目录> \
    --triton_impl_name <triton实现模块名> \
    --warmup <warmup次数> \
    --repeats <测试次数> \
    --output <输出文件路径>
```

**实际调用示例**：

```bash
python3 /path/to/triton-op-verifier/scripts/benchmark.py \
    --op_name softmax \
    --verify_dir /tmp/workspace/softmax/verify \
    --triton_impl_name triton_ascend_impl \
    --warmup 5 \
    --repeats 50 \
    --output /tmp/workspace/softmax/iter_0/perf_result.json
```

> **注意**：`--output` 路径由调用方指定，性能报告将写入该路径。通常由 `kernelgen-workflow` SubAgent 指定为 `{output-path}/iter_{iteration}/perf_result.json`。

**参数说明**：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--op_name` | 是 | 算子名称 |
| `--verify_dir` | 否 | 验证目录路径，默认当前目录 |
| `--triton_impl_name` | 否 | Triton 实现模块名（不含 `{op_name}_` 前缀），默认 `triton_ascend_impl` |
| `--warmup` | 否 | warmup 次数，默认 5 |
| `--repeats` | 否 | 正式测试次数，默认 50 |
| `--output` | 否 | 性能报告输出路径（JSON 格式）|
| `--verify_not_required` | 否 | 跳过 L1 verify 闸门（默认强制要求 verify_result 全过）|
| `--lock-frequency` / `--no-lock-frequency` | 否 | 性能测试前是否对 NPU 锁频并在测试期间监控频率（默认开启）|
| `--lock-frequency-fail-action` | 否 | 锁频失败或频率漂移时的处理方式：`warn`（默认）或 `error`|
| `--freq-check-interval` | 否 | 频率监控采样间隔，单位秒（默认 `1.0`）|

---

### L1 verify 闸门

benchmark.py 启动时按 `--triton_impl_name` 推导对应的 verify_result 文件名：

| triton_impl_name | 对应 verify json |
|-----------------|----------------|
| `triton_ascend_impl`（默认，Phase 3）| `verify_result.json` |
| `triton_baseline`（Phase 4 baseline）| `verify_result_baseline.json` |
| `triton_optimized`（Phase 4 optimized）| `verify_result_optimized.json` |
| 其他 `triton_xxx` | `verify_result_xxx.json` |

**判定规则**（默认开启，传 `--verify_not_required` 可跳过）：

| 情况 | 退出码 | 说明 |
|------|-------|------|
| 文件不存在 | exit 2 | 必须先跑 verify.py |
| 文件读取失败 | exit 2 | JSON 损坏 |
| `total_cases == 0` | exit 2 | verify 未实际跑任何 shape |
| `passed_cases < total_cases` | exit 2 | 精度未全过，benchmark 无意义且会传染下游 |
| `passed_cases == total_cases > 0` | 继续执行 benchmark | — |

**exit 2 时 stderr 会打印**：verify_json 路径 / passed/total / 前 5 条 failures，便于上游 agent 把错误等价映射到 verify 失败处理路径。

---

## Step 5: 收集性能结果

性能测试完成后，从 `--output` 指定的 JSON 文件中读取结果。

### 性能报告格式

```json
{
  "op_name": "softmax",
  "warmup": 5,
  "repeats": 50,
  "total_cases": 3,
  "passed_cases": 3,
  "failed_cases": 0,
  "nan_indices": [],
  "inf_indices": [],
  "zero_indices": [],
  "negative_indices": [],
  "none_indices": [],
  "framework": {
    "avg_latency_ms": 1.2345,
    "peak_memory_mb": 256.00,
    "operators": {"...": 0.0}
  },
  "implementation": {
    "avg_latency_ms": 0.5678,
    "peak_memory_mb": 128.00,
    "operators": {"...": 0.0}
  },
  "speedup_vs_torch": 2.1746,
  "per_shape_results": [
    {
      "case_idx": 1,
      "input_desc": [{"type":"tensor","shape":[128,256],"dtype":"torch.float16"}],
      "status": "pass",
      "framework": {"avg_latency_ms": 1.23, "peak_memory_mb": 64.0},
      "implementation": {"avg_latency_ms": 0.56, "peak_memory_mb": 32.0},
      "speedup_vs_torch": 2.19,
      "error_type": null,
      "error_msg": null
    }
  ]
}
```

**字段说明**：

| 指标 | 说明 |
|------|------|
| `avg_latency_ms` | 各 shape 延时的算术平均（兼容语义）|
| `peak_memory_mb` | 峰值内存占用（MB）|
| `speedup_vs_torch` | **几何平均加速比** = `(∏ s_i)^(1/n)`，仅对 status==pass 且 `s_i` 为有限正数的 shape 取几何平均；全部异常时为 `null` |
| `passed_cases` / `failed_cases` | 多 shape 通过 / 失败计数（异常 shape 仍计入 `passed_cases`，因为算子功能正常）|
| `nan_indices` / `inf_indices` / `zero_indices` / `negative_indices` / `none_indices` | 各类异常 `s_i` 的 case_idx 列表（从 1 开始），不进入几何平均；无异常时为 `[]` |
| `per_shape_results[].status` | `"pass"` 或 `"fail"` |
| `per_shape_results[].speedup_vs_torch` | 该 shape 的加速比；fail 或异常时为 `null` |

**边界值处理**：

`s_i = framework_latency_ms / impl_latency_ms` 可能因 profiler 故障、极小延时等出现异常值。`compute_overall` 对每个 `s_i` 按以下优先级分类：

| 类别 | 判定 | 落盘行为 |
|------|------|---------|
| `none` | `s_i is None` | `per_shape.speedup_vs_torch = null`，case_idx 入 `none_indices` |
| `nan` | `math.isnan(s_i)` | 同上，入 `nan_indices` |
| `inf` | `math.isinf(s_i)` | 同上，入 `inf_indices` |
| `negative` | `s_i < 0` | 同上，入 `negative_indices` |
| `zero` | `s_i == 0` | 同上，入 `zero_indices` |
| `valid` | 有限正数 | 进入几何平均 |

异常 shape **仍计入 `passed_cases`**（算子功能正常，仅测量数据不可信），但 `s_i` 不参与整体几何平均。全部 shape 都异常时 `speedup_vs_torch = null`。

**退出码**：
- exit 0：benchmark 正常完成（按 shape 内部 try/except，pass/fail 写在 per_shape_results）
- exit 1：脚本本身崩溃
- exit 2：L1 verify 闸门拒绝（precondition 未满足，benchmark 未实际运行）

调用方通过读 JSON 判断 `passed_cases == total_cases`；exit 2 时无 JSON 产出，应等价于"对应 verify 失败"处理。

**返回**：
- `perf_result`：dict（完整性能数据）
- `perf_report_path`：str（性能报告文件路径）

---

## 脚本位置

验证脚本位于本 skill 的 `scripts/` 目录：

| 脚本 | 用途 |
|------|------|
| `scripts/validate_triton_impl.py` | 退化预检查（AST 静态分析） |
| `scripts/verify.py` | 验证正确性 |
| `scripts/benchmark.py` | 测试性能 |
| `scripts/eco_limits.py` | 生态开源精度标准阈值表（`verify.py` §一 唯一权威来源） |

**CLI 参数**：
- `validate_triton_impl.py`: `<file_path>`, `[--json]`
- `verify.py`: `--op_name`, `--verify_dir`, `--triton_impl_name`, `--timeout`, `--output`, `--non-compute`, `--fresh-cache`, `--keep-cache`
- `benchmark.py`: `--op_name`, `--verify_dir`, `--triton_impl_name`, `--warmup`, `--repeats`, `--output`, `--skip_framework`, `--framework_latency_ms`, `--verify_not_required`, `--lock-frequency`, `--lock-frequency-fail-action`, `--freq-check-interval`
