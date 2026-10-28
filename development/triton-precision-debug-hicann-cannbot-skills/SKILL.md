---
name: triton-precision-debug
description: >
  Triton-Ascend 算子精度对齐调试专家。当算子精度校验（MERE/MARE）不通过时，
  按照系统化的五阶隔离法定位 ULP 级差异根因，并提供修复方案。
  尤其擅长处理编译器 scalar/vector 浮点行为差异、常量除法精度偏差等隐蔽问题。
argument-hint: >
  输入：算子代码路径、任务描述、verify_result.json 失败摘要、迭代历史。
  输出：根因定位报告、修复后的代码、验证建议。
  固定参数：framework=torch、backend=ascend、dsl=triton_ascend。
---

# Precision Debugger Skill

<role>
你是 Triton-Ascend 算子精度对齐调试专家。当算子与 torch 参考实现存在 ULP 级精度差异、
MERE/MARE 校验不通过时，按照系统化的五阶隔离法逐层排查，定位编译器行为差异或代码逻辑缺陷，
并提供可验证的修复方案。
</role>

## 适用场景

- Triton-Ascend 算子精度校验失败（MERE/MARE 不通过）
- 42 case 多 shape 场景下大面积精度偏差
- 已排除明显算法错误（shape mismatch、NaN/Inf 不一致），需定位隐蔽的编译器行为差异
- 尤其适用于涉及常量除法、标量/向量浮点操作混合的量化类算子
- GEMM 融合类算子 epilogue 精度偏差（round-trip cast 被编译器消除，逐 op 舍入链丢失，见模式 4）

## 排查方法论：五阶隔离法

遇到 ULP 级精度差异时，按以下五个阶段系统排查，禁止跳步。

### Stage 0：前置检查（排除低级错误）

在怀疑编译器之前，先确认以下基础项：

```
□ 输出 shape 与参考完全一致
□ NaN 位置完全一致（mask 按位相等）
□ Inf 位置和符号完全一致
□ dtype 转换逻辑正确（如 bfloat16 -> float32 后再计算）
□ 未使用未初始化的 memory（tl.load 的 other=0.0 是否合适）
```

### Stage 1：端到端差异定位

先用最小 reproduction 找到差异最大的 case，缩小排查范围。

```python
# 在失败 case 上对比 Triton 输出与 torch 输出
triton_out, triton_scale = model_new(x, smooth)
torch_out, torch_scale = model_ref(x, smooth)

diff = (triton_out.float() - torch_out.float()).abs()
print(f"max_diff={diff.max().item():.2e}")
print(f"diff>0 count={(diff > 0).sum().item()}")

# 如果 diff 存在，打印前几处差异的原始值和量化值
indices = torch.where(diff > 0)
for i in range(min(10, len(indices[0]))):
    idx = tuple(t[i].item() for t in indices)
    print(f"idx={idx}: triton={triton_out[idx].item()}, torch={torch_out[idx].item()}")
```

**判定**：若 diff 存在且原始输入值差异为 0（即差异纯由量化引入），则进入 Stage 2。

### Stage 2：逐操作隔离微基准测试

将算子拆分为独立原子操作，每个操作写一个最小 Triton kernel，与 torch 一对一比对。

**检查清单（DynamicQuant 为例）**：

| # | 操作 | Triton 代码 | Torch 参考 | 预期结果 |
|---|------|------------|-----------|---------|
| 1 | `abs` | `tl.abs(x)` | `x.abs()` | 0 diff |
| 2 | `max` | `tl.max(abs_x, axis=0)` | `x.abs().max(dim=1)[0]` | 0 diff |
| 3 | 常量除法 | `max_val / 127.0` | `max_val / 127.0` | **需重点检查** |
| 4 | clamp scale | `tl.maximum(scale, 1e-10)` | `scale.clamp(min=1e-10)` | 0 diff |
| 5 | 变量除法 | `x / scale` | `x / scale` | 0 diff |
| 6 | round | `nearbyint(x)` | `torch.round(x)` | 0 diff |
| 7 | clamp quant | `max(min(val,127),-128)` | `val.clamp(-128,127)` | 0 diff |
| 8 | cast to int8 | `.to(tl.int8)` | `.to(torch.int8)` | 0 diff |

**微基准 kernel 模板（以 scale 除法为例）**：

```python
import torch
import torch_npu
import triton
import triton.language as tl

@triton.jit
def scale_kernel(max_ptr, scale_ptr, M, BLOCK_SIZE: tl.constexpr):
    pid = tl.program_id(0)
    offsets = pid * BLOCK_SIZE + tl.arange(0, BLOCK_SIZE)
    mask = offsets < M
    max_vals = tl.load(max_ptr + offsets, mask=mask, other=0.0)
    scales = max_vals / 127.0
    scales = tl.maximum(scales, 1e-10)
    tl.store(scale_ptr + offsets, scales, mask=mask)

# 测试数据
torch.manual_seed(0)
x = torch.randn((512, 512), dtype=torch.bfloat16, device="npu")
max_abs = x.float().abs().max(dim=1)[0]

# Torch 参考
scale_torch = max_abs / 127.0
scale_torch = scale_torch.clamp(min=1e-10)

# Triton 测试
scale_triton = torch.empty_like(max_abs)
grid = ((M + BLOCK_SIZE - 1) // BLOCK_SIZE,)
scale_kernel[grid](max_abs, scale_triton, M, BLOCK_SIZE=BLOCK_SIZE)
torch.npu.synchronize()

# 比对
diff = (scale_torch.cpu() - scale_triton.cpu()).abs()
print(f"BLOCK_SIZE={BLOCK_SIZE}: max_diff={diff.max().item():.2e}, count={(diff > 0).sum().item()}")
```

### Stage 3：Scalar vs Vector 路径判定

当 Stage 2 发现某个操作存在差异时，用以下矩阵测试确定是否为 scalar/vector 编译器行为差异：

| 测试 | BLOCK_SIZE | Grid | 预期 |
|------|-----------|------|------|
| A | 1 | (M,) | **可能失败**（scalar 优化） |
| B | 2 | (M/2,) | 应通过（vector） |
| C | 4 | (M/4,) | 应通过（vector） |
| D | 2048 | (1,) | 应通过（vector loop） |
| E | scalar loop in kernel | (1,) | **可能失败**（显式 scalar） |

**测试 E 的代码形式**：
```python
@triton.jit
def scalar_loop_kernel(max_ptr, scale_ptr, M):
    for i in range(M):
        val = tl.load(max_ptr + i)
        scale = val / 127.0          # 显式标量除法
        tl.store(scale_ptr + i, scale)
```

**判定规则**：
- 若 A/E 失败但 B/C/D 通过 → **确诊 scalar/vector 编译器差异**
- 若全部失败 → 差异来源不是 scalar/vector，需继续排查（如 `127.0` 字面量精度、div 指令选型等）

### Stage 4：验证修复方案

确诊后，将算子中对应操作改为 vector 路径，然后做**两级验证**：

**Level 1 — 单操作验证**：仅修改目标操作，其余仍用 torch，确认该操作单独通过。

**Level 2 — 全链路验证**：将修改后的操作放回完整 pipeline，跑全量 case 验证。

---

## 核心根因与修复模式

### 模式 1：Scalar/Vector 浮点除法精度差异（最隐蔽）

**根因**：Triton-Ascend 编译器对 scalar 浮点除法和 vector 浮点除法走不同代码生成路径：

| 路径 | 触发条件 | 精度行为 |
|------|---------|---------|
| Scalar | 标量变量直接运算；或 BLOCK_SIZE=1 被编译器优化回标量 | 与 torch `aclnnDiv` 存在 1-2 ULP 偏差 |
| Vector | `tl.load(vector_offsets) / 127.0`，且 BLOCK_SIZE >= 2 | 与 torch `aclnnDiv` 完全一致 |

**关键陷阱**：即使代码形式上使用了 `tl.arange(0, BLOCK_SIZE)`，若 `BLOCK_SIZE=1`，编译器仍可能将其优化为标量操作。

**修复方案**：
```python
@triton.jit
def compute_scale_kernel(max_ptr, scale_ptr, M, BLOCK_SIZE: tl.constexpr):
    for start in range(0, M, BLOCK_SIZE):
        offsets = start + tl.arange(0, BLOCK_SIZE)
        mask = offsets < M
        max_vals = tl.load(max_ptr + offsets, mask=mask, other=0.0)
        scales = max_vals / 127.0        # vector 除法，强制编译器走向量路径
        scales = tl.maximum(scales, 1e-10)
        tl.store(scale_ptr + offsets, scales, mask=mask)
```

调用时确保 `BLOCK_SIZE >= 2`：
```python
compute_scale_kernel[(1,)](max_temp, scale, M, BLOCK_SIZE=2048)
```

**底线**：`BLOCK_SIZE` 绝不能为 1。

### 模式 2：AST 结构适配（多 kernel 场景）

`validate_triton_impl.py` 要求 `forward()` 只能直接启动一次 kernel。多 kernel 场景下，使用 `_route()` 包装器：

```python
def _route(self, x, smooth_scales, dst_type):
    # ... 根据维度选择 2D/3D/1D 分支，启动 kernel ...

def forward(self, x, smooth_scales=None, group_index=None, dst_type=None):
    # ... 参数准备
    return self._route(x, smooth_scales, dst_type)
```

AST 校验器明确允许 `self._route()` 作为合法的 kernel dispatch 包装器。

### 模式 3：NPU 浮点除法 scale 校正（坐标/权重查找表法）

**根因**：CPU 与 NPU（CANN `vdiv`）的浮点除法在某些 shape 上会相差 1 ulp。对
`float16`/`bfloat16` 算子，这个差异会通过坐标/权重放大为大量像素超阈值。

**典型场景**：
- `interpolate` 的 `(in-1)/(out-1)`、`in/out`
- `grid_sample` 的 `2.0/(W-1)`
- `avg_pool` / `adaptive_avg_pool` 的 `1.0/count`
- `normalize` 的 `1.0/sqrt(var+eps)`

**修复方案**：

1. 在模块级别定义 `_npu_scale(num, den)`，用 NPU `float32` 除法得到 scale：
   ```python
   def _npu_scale(num, den):
       a = torch.tensor([num], dtype=torch.float32, device='npu')
       b = torch.tensor([den], dtype=torch.float32, device='npu')
       return (a / b).cpu().item()
   ```
2. 在 `forward()` 中用 `_npu_scale(...)` 计算所有影响坐标的 scale。
3. 基于 NPU scale 在 host 侧生成坐标/权重/索引查找表，上传为 `float32` tensor。
4. kernel 内部只查表和做 fp32 累加，最后按输入 dtype 输出。

完整细节见 `references/divide-scale-calibration.md`。

> **同根因的另一形态**：attention 类算子里，参考实现的 `aclnnDivs` 与设备 fp32 除法（Newton 迭代、非正确舍入）会让 `scores` 差 1 ulp，经 `exp` 放大成 ~0.8% 权重误差。解法不是查找表而是**整条算术路径逐位复刻**（host 侧 fp32 倒数乘法 + 三条配套契约），见 `references/attention-lowprec-contract.md`。

### 模式 4：Epilogue cast 消除导致舍入语义丢失（GEMM 融合类算子）

**根因**：`tl.dot` 的 fp32 累加器若在 epilogue 中紧跟 round-trip cast
（`acc.to(f16).to(f32)`），Triton-Ascend 编译器判定其为 no-op 直接消除，
"每步运算前舍入到输入 dtype"的逐 op 舍入链不复存在，epilogue 后续
运算实际作用在未舍入的 fp32 上。

**无效拦截**（均被编译器消除，勿再尝试）：bitcast、`tl.where` 强制依赖、
`tl.debug_barrier`。

**修复方案**：GM 物化（store-reload）——将舍入后的累加器先落 GM 再读回：

```python
tl.store(h_ptr + ..., acc.to(DT), mask=msk)      # round 后的值强制落 GM
g = tl.load(h_ptr + ..., mask=msk_e, other=0.0)  # 读回的已是 DT 舍入值
# 此后 bias/激活链的逐 op 舍入语义成立
```

---

## 扩展检查清单

以下是在其他算子中排查 ULP 级差异时的通用检查项：

### 运算类

- [ ] **常量除法**：`a / 127.0`、`a * 0.5` 等是否走了 scalar 路径？尝试改为 vector load 后再运算
- [ ] **常量乘法**：与除法同理，`a * inv_127` 和 `a / 127.0` 可能生成不同指令序列，需分别测试
- [ ] **整数除法 vs 浮点除法**：确认分子分母均为浮点类型，无隐式整数除法
- [ ] **减法顺序**：`a - b` 与 `b - a` 在浮点中不等价，确认与参考实现顺序一致
- [ ] **累加顺序**：reduce/scan 操作的累加顺序是否与参考一致？

### 类型转换类

- [ ] **中间精度**：是否在运算前统一升精度到 float32？低精度中间结果会引入差异
- [ ] **隐式类型提升**：`tl.int8` 和 `tl.float32` 混合运算时的隐式转换行为是否与 torch 一致
- [ ] **rounding 模式**：`nearbyint`、`rint`、`round` 在边界值（如 x.5）的行为是否一致

### 内存类

- [ ] **mask 处理**：`tl.load(..., mask=mask, other=0.0)` 中的 `other` 值是否会影响后续运算？
- [ ] **越界读**：mask 未正确覆盖时是否读取了脏数据？
- [ ] **内存对齐**：stride 是否为预期值？可用 `tensor.stride()` 打印确认

### 编译器行为类

- [ ] **BLOCK_SIZE=1 陷阱**：任何使用 `tl.arange(0, BLOCK_SIZE)` 的地方，若 BLOCK_SIZE=1，检查编译器日志确认未被优化为标量
- [ ] **循环展开**：显式 `for` 循环中的标量操作 vs 向量化操作，对比结果
- [ ] **grid=1 行为**：grid 数为 1 时是否触发了不同的调度或指令选择？
- [ ] **cast 消除**：dot 累加器后的 `f32 -> f16 -> f32` round-trip cast 可能被编译器当 no-op 消除，舍入语义丢失；用 GM 物化（store-reload）强制落盘（模式 4）

---

## 参考文档

| 文档 | 路径 |
|------|------|
| 完整调试案例（DynamicQuant） | `references/precision-alignment-guide.md` |
| NPU 除法 scale 校正（坐标/权重查找表法） | `references/divide-scale-calibration.md` |
| **Attention 低精度逐位契约**（FA/MHA/SDPA） | `references/attention-lowprec-contract.md` |

## 关键经验总结

1. **微基准隔离是定位 ULP 差异的唯一可靠手段**，不要依赖端到端的猜测
2. **标量/向量浮点操作在 Ascend 后端可能有不同精度**，这是容易被忽视的编译器行为差异
3. **BLOCK_SIZE=1 在 Triton 中不等于向量操作**，编译器可能优化回标量；保守选择 BLOCK_SIZE >= 2
4. **常量除法是量化类算子的高风险点**，`scale = max / constant` 这类操作应优先放入独立 kernel 并强制 vector 路径
5. **多 kernel 场景用 `_route()` 包装**，既满足 AST 校验，又保持代码结构清晰
6. **编译器会消除"看似有副作用"的 round-trip cast**，逐 op 舍入链必须通过 GM 物化（store-reload）强制生效
