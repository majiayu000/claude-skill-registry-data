---
name: triton-simulator-optimizer
description: >
  Triton-Ascend 算子的 simulator 流水**采集与诊断**专家。用 msprof op simulator 采集
  per-instruction pipe 统计，定位真实瓶颈（而非猜测），产出**诊断报告**：瓶颈类型 +
  热源码行 + 修复方向（指向 triton-latency-optimizer 的已有优化点编号）。
  本 skill **只采集 + 诊断，不自带优化技术**——修复落地一律走 latency-optimizer，
  禁止在本 skill 重复定义第二个优化技术目录。禁止在未采集前 declaring "硬件极限"。
  触发：当用户需要通过 simulator 流水采集定位 Triton-Ascend 算子瓶颈，或端到端 benchmark
  慢但瓶颈不明（dot / 逐元素 / 访存 / 同步哪一项未知），或即将得出"硬件瓶颈不可优化"
  结论之前——必须先采集。
  入口：由编排器（triton-op-generator / AGENTS.md Phase 4）在 latency-optimizer 优化耗尽
  且 speedup 仍未达标时调用。被调用即直接进入采集循环。
---

# Triton Simulator-Driven Optimizer

## 角色定位

你是 simulator 流水**采集与诊断**专家，与 `triton-latency-optimizer`（优化技术 owner）严格分工：

- **latency-optimizer**：优化技术的**唯一** owner。31 个优化点（入参静态化 / tiling / 分核 / scalar→vector / pass 合并 / Cube-MTE3 解耦 / 物化解耦 / 循环不变外提 …）+ 参考文档全部在其 `references/` 下。
- **本 skill（simulator-optimizer）**：**只采集 + 诊断**。用 `msprof op simulator` 拿到 per-instruction pipe 占比，判定瓶颈类型与热源码行，产出**诊断报告**，把修复方向映射到 latency-optimizer 的已有优化点编号，交回编排器/latency-optimizer 落地。**不在本 skill 定义任何优化技术、不维护第二个技术目录。**

**核心原则：先测，再断。** 严禁在未拿到 simulator 采集证据前下"硬件极限不可优化"结论。

## 何时使用

1. `triton-latency-optimizer` 的优化点已用尽，speedup 仍 < target
2. 端到端 benchmark 慢，但不知是 dot / 逐元素变换 / 访存 / 同步哪一项
3. 即将得出"fp32 dot 不走 Cube / 硬件瓶颈"之类的结论之前——**必须先采集**

## 采集→诊断循环（强制顺序）

```
0. 全 kernel 采集覆盖门禁（见下，必须先做）
1. 准备小 shape 用例脚本（单次 forward，每维 ~64 起，最多 128）
2. 对每个 @triton.jit kernel 各跑一次 msprof 采集
3. 对每个 kernel 解析 Cube+Vector 核的 instr_exe（瓶颈类型）+ code_exe（热源码行）
4. 诊断（综合全部 kernel 采集结果）
5. 产出诊断报告：瓶颈类型 + 热源码行 + 修复方向（映射到 latency-optimizer 优化点编号）+ 采集证据
6. 修复落地：交回 latency-optimizer（编排器带诊断报告回到 4.1，命中诊断指向的优化点），不在本 skill 改代码
7. 真实 NPU benchmark 确认端到端提升 + 本 skill 重采确认瓶颈转移
8. 回到 2，直到诊断无对应优化点可应用（真·硬件极限）或 target 达标
```

**一次循环只指向一个 latency-optimizer 优化点，重新采集确认后再下一个。** 多点叠加会模糊因果。

## 全 kernel 采集覆盖门禁（硬门禁）

> 多 kernel 算子（stats+apply、fwd+bwd、多段融合等）的瓶颈可能在任意一个 kernel，且不同 kernel 瓶颈类型可能不同。**只采部分 kernel 就下全局结论 = 流程级 bug。** `forward()` 启动 ≥2 个 `@triton.jit` kernel 时强制生效。

进入诊断或"无更多改进"结论前，必须：

1. **枚举**全部 `@triton.jit` 装饰的函数名（AST，识别 `@triton.jit` / `@jit`）。排除 framework 辅助 kernel（`ZerosLike`/`Empty`/`OnesLike`/`Contiguous` 等，非算子逻辑）。→ 用 `scripts/enumerate_kernels.py <impl.py>` 自动枚举，避免手漏。
2. **逐个采集**：每个算子 kernel 跑一次 `msprof op simulator --kernel-name=<name> --launch-count=1`（采集命令与环境见 `references/msprof-simulator.md`）。超时则换更小 shape/单次 forward 重试，仍失败标"采集失败（附原因）"；未被 forward 触发标"未触发"。**不得静默跳过。**
3. **产出覆盖表**（每个算子 kernel 一行）。→ 用 `scripts/parse_prof.py <prof_out>` 自动汇总各核 pipe 占比与热源码行，机器可读输出供填充下表：
   ```
   | kernel_name | 是否采集(✓/失败/未触发) | Cube top pipe(占比/cyc) | Vector top pipe(占比/cyc) | 热源码行 |
   ```
4. **判定**：每行"是否采集"均为 ✓/失败/未触发之一 → 通过。**任一行缺失且未标注 → 禁止诊断、禁止结论。**

修复某 kernel 后，受影响的其他 kernel 须在步骤 7 重采确认（瓶颈可能转移）。

诊断时须**综合全部 kernel** 的采集结果：瓶颈可能集中在某一个 kernel，也可能跨多个；修复一个 kernel 后，受影响的其他 kernel 须在步骤 7 重采确认。

## 诊断速查（pipe 占比 → 瓶颈 → 修复方向）

解析 `instr_exe.csv`（瓶颈**类型**），按 `cycles` 降序，计算各 pipe 占比；再解析 `code_exe.csv`（瓶颈**位置**，热源码行）交叉验证。两者字段/解析/联合定位流程见 `references/msprof-simulator.md`。

**修复方向列指向 `triton-latency-optimizer` 的优化点编号**（技术细节载其 `references/`，本 skill 不重复）：

| 信号 | 诊断 | 修复方向（latency-optimizer 优化点） |
|------|------|---------|
| Cube `WAIT_FLAG_DEVI` > 50% 且 `MMAD` < 5% | **Cube 空等 Vector**（dot 依赖 Vector 侧变换输出，串行化） | 19（Cube/MTE3 分阶段解耦）/ 21（Workspace 物化解耦） |
| Vector `SCALAR` pipe > 30%，大量 `CMPN`/`ADD` (calls = tile 元素数) | **i32 比较标量降级** | 6（避免标量降级）/ 5（Scalar→Vector）/ 17（冗余边界运算） |
| `MTE2`/`MTE3` dominant | 访存 bound | 7（Pass 合并）/ 21（物化解耦）/ 10（循环不变外提） |
| `BAR` (barrier) 占比高 | 跨核/跨 pipe 同步 | 19（解耦减少循环内依赖链）/ 增大 tile |
| `MMAD` > 50% (Cube) | 计算bound（**真·硬件极限判据**） | 无对应优化点 → 增大 tile / bf16 化（需精度验证），均不可行则回 4.6 终局 |

> 信号→规则→修复方向的完整规则（含误诊陷阱、反例代码）见 `references/bottleneck-diagnosis.md`。

## 关键认知（Cube+Vector 异构核）

> 核心结构以目标芯片为准（见 `npu-arch`）。910B 系列每物理核 1 cubecore + 2 veccore（Cube:Vec=1:2）；其他代际核心结构可能不同，以实际芯片为准。

- **fp32 `tl.dot` 走 Cube (MMAD)**，并非不走 Cube。但 fp32 dot 的吞吐远低于 bf16/fp16（Cube 原生 bf16/fp16）。
- **Cube 与 Vector 是异构核**，经 `WAIT_FLAG_DEVI` 同步。若循环内 dot 依赖 Vector 侧变换输出（逐元素/归约变换→后续 dot），Cube 大量时间空等 Vector。
- **采集前不要猜**：禁止凭直觉判断瓶颈类型。典型误判——以为"fp32 dot 是瓶颈"，simulator 实测 MMAD 占比却极低，真因是 Cube 空等 Vector。必须看 4 张表（Cube 核 + Vector 核各自的 `instr_exe`+`code_exe`）的 pipe 占比与热源码行后再下结论。
- **simulator 行为**：整应用（`forward()` 触发的所有 kernel）都被逐指令仿真，非仅 `--kernel-name` 指定的 kernel；含 `atomic_add` 的 kernel 跨核竞争仿真极慢；子进程退出码非 0（如 134）不一定失败，以 CSV 是否落盘为准。对策：脚本单次 forward + 最小 shape；多 kernel 算子逐个 `--kernel-name` 采集。详见 `references/msprof-simulator.md` 的"关键行为认知"。真实 NPU benchmark 才是端到端指标。

## 与其他 skill 的协作

- **上游（优化技术 owner）**：`triton-latency-optimizer` —— 本 skill 诊断产出"修复方向 = 其优化点编号"，编排器带诊断报告回到 Phase 4.1 调 latency-optimizer 命中该点并产出代码。**本 skill 不替代 latency-optimizer 做优化。**
- **下游（验证）**：latency-optimizer 产出修复代码后回 `triton-op-verifier` 验精度 + benchmark；本 skill 重采确认瓶颈转移。
- **参考真源**：硬件规格 / UB 容量等见 `npu-arch/references/npu-hardware-params.md`（单向消费，不在本 skill 重复定义）

## 脚本工具

- `scripts/enumerate_kernels.py` — AST 枚举实现文件中全部 `@triton.jit`/`@jit` 装饰的 kernel 名，供「全 kernel 采集覆盖门禁」步骤 1 使用（避免遗漏多 kernel 算子的某个 kernel）。
- `scripts/parse_prof.py` — 给定 `msprof op simulator` 产出的 `prof_out` 目录，自动定位各核的 `*_instr_exe.csv` + `*_code_exe.csv`，按核（Cube / Vector）汇总 pipe 占比与热源码行，产出「覆盖表」（门禁步骤 3/4 的机器可读输出）。

## 参考资料

- `references/msprof-simulator.md` — `msprof op simulator` 采集流程、环境准备、关键行为认知、两表联合解析方法、热源码行→指令→修复方向（latency-optimizer 优化点）映射
- `references/bottleneck-diagnosis.md` — pipe 占比规则、瓶颈信号→诊断规则→修复方向（latency-optimizer 优化点编号）映射、误诊陷阱
- `npu-arch/references/npu-hardware-params.md` —（真源，跨 skill）核心结构 / UB / L0C / Cube:Vec 比例等硬件参数

## 禁止事项

- **禁止在本 skill 定义/维护优化技术目录**——修复手段一律映射到 `triton-latency-optimizer` 的已有优化点，不在本 skill 重复第二个技术表
- 禁止未采集就 declaring "硬件极限 / 不可优化"
- **禁止只采集部分 kernel 就下全局结论**（必须过"全 kernel 采集覆盖门禁"，对每个 @triton.jit kernel 各采一次并产出覆盖表）
- 禁止一次指向多个优化点（模糊因果）
- 禁止仅看端到端 benchmark 数字猜瓶颈（必须看 pipe 占比）
- 禁止把 simulator 卡死当作"无解"——换小 shape 或换 board profiler
- 禁止编造采集数据
