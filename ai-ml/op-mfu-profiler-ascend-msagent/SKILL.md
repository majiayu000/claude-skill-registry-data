---
name: op-mfu-profiler
description: 运行程序采集 Profiling 数据，再用 msprof-analyze 分析TFLOPS 与 MFU。
keywords: [MFU, TFLOPS, FLOPs, 利用率]
---

# 算子级 MFU 实测分析

## 这个 Skill 做什么

**MFU（Model FLOPs Utilization）**：算子实际计算吞吐与硬件理论峰值的比值，衡量算力利用效率。

```
MFU = 实际 FLOPS / 硬件理论峰值 FLOPS = 浮点运算次数（FLOPs）/（执行时间 × 芯片理论峰值）
```

其中：

- FLOPs（Floating Point Operations）：浮点运算次数，描述总计算量的单位。
- FLOPS（Floating Point Operations Per Second）：每秒浮点运算次数，衡量硬件性能的指标，FLOPS = FLOPs / 执行耗时
- 执行时间：算子在 device 上的实际运行耗时，可以从 profiling 中拿到。
- 硬件理论峰值算力：由三部分决定——AI Core 数量 × 主频 × 每拍浮点运算次数。以 Cube 单元（FP16）为例，每个时钟周期可完成 16 × 16 × 16 × 2 次浮点运算。AI Core 数量与主频均记录在 device/info.json 中，可以直接读取对应字段计算得到。

整体方案端到端分两段：

采集阶段由torch\_npu.profiler 完成。用户在打开 with\_flops=True 及相关配置后，torch\_npu 在启动时会安装 Python 层的 FLOPs hook，将已注册公式的目标 API 包装起来。当这些算子被调用时，hook 在真正执行前根据当前入参算出 FLOPs，再通过MSTX接口将结果打点到 mfu\_flops 域中，最终落盘到 profile 数据并导出为 ascend\_pytorch\_profiler\_{rank\_id}.db文件，相关信息记录在MSTX\_EVENTS表中。

分析阶段由 msprof-analyze 工具承载。执行 msprof-analyze -m operator\_mfu 后，工具会从 DB 中读取MSTX\_EVENTS，与STRING\_IDS表关联，解析出每条记录对应的 FLOPs 和算子名称。同时，通过框架API到Device Kernel的关联关系，拿到对应的Device kernel 的执行耗时、输入数据类型。芯片理论峰值则从 device 信息中读取 ai\_core\_num 和 aic\_frequency，再结合数据类型估算得出。最后，将 FLOPs range 时间窗内的 kernel 与对应的 FLOPs 关联，逐个计算出 MFU。

本 skill 的任务就是带着用户走完整条链路，或定位到其中任一卡点。

> 提示：流程中任一步出现明显报错或异常，先停下排查、修好再继续，不要硬往下走；典型问题已汇总在文末「常见问题与兜底」，遇到问题先查那里。

## 何时用 / 何时不用

**用本 skill**：

- 想知道某个算子 / kernel 的 MFU、实际 TFLOPS、是否吃满算力
- 要给一个 torch\_npu 未注册的算子扩展 FLOPs 公式（`@register_npu_flop`、改 `_flops_formulas.py`）

**不要用本 skill**（避免重复造轮子）：

- 训练级整模型 MFU 公式估算;
- 纯粹要把 profiler 集成进脚本;
- 已有 profiling 数据想做通用瓶颈/通信/计算/快慢卡分析;

## 前置条件

| 条件                          | 说明                                                            |
| --------------------------- | ------------------------------------------------------------- |
| torch\_npu + msprof-analyze | 在**当前环境**已安装即可，用 `pip show` 确认两者存在                            |
| torch\_npu FLOPs 能力         | `torch_npu.profiler._flops_formulas.py` 必须存在，否则需升级 torch\_npu |

## 工作流：先判断用户处在哪个分支

按用户当前状态选入口，不要无脑从头跑：

- **分支 A**：用户已采集 profiling 数据（目录里能看到 `*_ascend_pt/.../ascend_pytorch_profiler*.db`）→ 直接跳到「第 4 步：解析」。该步开头的「确认 FLOPs 采集成功」会校验 FLOPs 是否落盘。
- **分支 B**：还没采集 → 从「第 1 步」顺序走。若用户没有已集成 `torch_npu.profiler.profile()` 的脚本，仅告知用户自行集成，集成后再回来跑 MFU——本 skill 不替用户写集成代码。

***

## 第 1 步：环境与前置检查

### 1.1 torch\_npu 检查

```bash
pip show torch-npu
python -c "import torch_npu; print(torch_npu.__file__)"
python -c "import torch_npu.profiler._flops_formulas; print(torch_npu.profiler._flops_formulas.__file__)"
```

`pip show` 确认已安装，两条 `python -c` 确认能加载且 FLOPs 公式文件存在；任一不通过见「常见问题与兜底」。

通过后，**读取该文件并列出所有带** **`@register_npu_flop`** **装饰器的 target**（含 target 标识），以表格呈现给用户。要点：

- 这些 target 是 torch\_npu 自带、采集时**能自动算 FLOPs** 的全部算子，仅反映 torch\_npu 支持哪些算子的 FLOPs 采集，与用户程序里实际跑了哪些算子无关。
- 直接告知用户**支持通过扩展注册为新算子补 FLOPs 公式**（流程见 `references/flops_formula_extension.md`）。**不要去翻用户程序里用了哪些算子、也不要逐个比对是否已注册**，只做告知。
### 1.2 msprof-analyze 检查

```bash
pip show msprof-analyze
msprof-analyze cluster --help
```

`--help` 输出里 `-m` 的可选值**包含** `operator_mfu` 才算通过；未安装或不包含见「常见问题与兜底」。

***

## 第 2 步：采集配置检查（分支 B）

这是最常出问题的环节。用户脚本里必须确保以下四项：

| 必须确保 | 配置项                                    | 为什么必须                                                                      |
| ---- | -------------------------------------- | -------------------------------------------------------------------------- |
| ✅    | `with_flops=True`（在 `profile()` 里）     | 没开就根本没有 FLOPs hook，后续一切无从谈起                                                |
| ✅    | `mstx=True`（在 `_ExperimentalConfig` 里） | FLOPs 通过 MSTX 打点，不开打不进 DB                                                  |
| ✅    | `export_type` 含 `Db`                   | 解析侧要读 `MSTX_EVENTS`/`PYTORCH_API`/`COMPUTE_TASK_INFO`/`TASK` 表，只导 Text 读不到 |
| ✅    | `profiler_level ≥ Level1`              | 保证 kernel 信息采全                                                             |

**配置可能以三种形式出现，检查时分别处理**：

1. **硬编码**：直接写在 `torch_npu.profiler._ExperimentalConfig(...)` 或 `profile(...)` 字面量里 —— 直接看字面值。
2. **Python 侧参数化**：通过 `argparse`/环境变量/配置文件传入，如 `profiler_level=args.profiler_level` —— 追到传入的值，必要时改默认值或启动参数。
3. **Bash 脚本驱动**：训练由 bash 拉起，Profiler 参数在命令行传入（如 `--profile-level level1 --profile-export-type db`），Python 用 argparse 接收 —— 既要看 Python 的接收逻辑，也要看 launch 脚本里实际传的值。

**已参数化的配置不用改脚本结构**，只要确保最终传进去的值正确即可。bash 驱动场景还要顺带检查 launch 脚本里的实参。

**额外注意**：如果用户配了 `mstx_domain_include`，要确认 `mfu_flops` 相关 msTX 事件没被过滤掉——否则打点采不到。其余项（`activities`/`schedule`/`aic_metrics` 等）保持用户原设置，不强制改。

完整可参考的采集脚本模板见 `references/collection_template.md`——**仅用于对照，不要要求用户脚本照抄**。

***

## 第 3 步：运行采集

以下事务必提醒，否则容易拿到错的结果：

1. **设置新的输出目录**：`on_trace_ready` 的输出目录里面已有数据，那么本次采集要指向一个**新目录**（如 `./result_<时间戳>`），不要复用残留上次采集 `*_ascend_pt` 子目录或 `cluster_analysis_output` 的旧目录——msprof-analyze 会报错或给出错误结果。**不要清空已有目录**，直接换一个新目录更安全。


module 级 MFU 统计默认不涉及，只要 kernel 级明细即可；确有 module 级需求时再按 `references/collection_template.md` 的「module 级 msTX 打点」段加打点。

***

## 第 4 步：解析（msprof-analyze operator\_mfu）

### 确认 FLOPs 采集成功

解析前先确认 FLOPs 打点真的落盘了，否则解析必空。DB 文件路径通配符：

```
<on_trace_ready输出目录>/*_ascend_pt/ASCEND_PROFILER_OUTPUT/ascend_pytorch_profiler*.db
```

多卡场景任选一个 rank 的 DB 确认即可。文件存在则跑以下 SQL：

```sql
SELECT
    si_msg.value AS message
FROM MSTX_EVENTS me
INNER JOIN STRING_IDS si_domain
    ON me.domainId = si_domain.id
INNER JOIN STRING_IDS si_msg
    ON me.message = si_msg.id
WHERE si_domain.value = 'mfu_flops';
```

期望结果：

- 有记录返回，`message` 格式为 `<正整数FLOPs>-<op_name>`，例如 `137438953472-torch::mm`。
- 没有任何记录：说明 FLOPs 没打进去，回「第 2 步」核对 `with_flops`/`mstx` 等配置后重采，不要继续解析。

### 解析

```bash
msprof-analyze --agent -m operator_mfu -d <profiling_path> -o <output_path>
```

| 参数        | 必/可选 | 说明                                             |
| --------- | ---- | ---------------------------------------------- |
| `--agent` | 必选   | 以 agent 模式运行（为 agent 设计）                       |
| `-m`      | 必选   | 固定 `operator_mfu`                              |
| `-d`      | 必选   | **`on_trace_ready`** **配置的目录路径**（如 `./result`） |
| `-o`      | 可选   | 输出路径，默认在 `-d` 下                                |

输出格式**默认 db**（便于程序读取）。若需要 excel 格式直接解读，也支持导出——加 `--export_type text` 即可生成 `xlsx`。

### ⚠ 最大的坑：`-d` 路径

`-d` **必须**是 `on_trace_ready` 里写的那个目录（如 `./result`），**绝不是**它下面自动生成的 `*_ascend_pt` 子目录。填错会直接报错或给出错误结果。这是本流程最高频的误用点，务必跟用户确认清楚 `on_trace_ready` 的实参值再传 `-d`。

### 输出

msprof-analyze 会在 `-o` 指定路径下生成 `cluster_analysis_output` 文件夹。默认 `--export_type db` 时生成 `cluster_analysis.db`，内含两张表：

- `OperatorMFU`：kernel 级 MFU 明细
- `ModuleMFU`：module 级 MFU 统计（仅当采集数据包含 `Module` domain 的 msTX Range 时写入）

字段含义及 `--export_type text`（Excel）的产物说明见 `references/output_fields.md`，解读时按需查阅。

***

## 第 5 步：结果解读

### MFU 区间评估

| MFU 范围  | 评估                                           |
| ------- | -------------------------------------------- |
| < 20%   | 算子远未吃满算力，可能受内存带宽、launch overhead、shape 不规则拖累 |
| 30%–60% | 中等偏上，许多通用工作负载大致在此区间                          |
| > 70%   | 算子形状、并行度和实现都接近设备上限                           |

### 解读回答要点

解读时按下面组织回答，不要只甩一堆数字：

1. 说明分析基于 msprof-analyze 的 `operator_mfu` 模块。
2. 列出 MFU 最低 / 最高的 Top-N 算子，含关键字段（`op_name`、`kernel_duration`、`actual_tflops`、`mfu`）。
3. **按算子类型、输入 shape 归类**分析：同一算子在不同 shape 下的 MFU 差异、同 shape 下不同算子的利用率对比，定位是 shape 不规则还是算子实现拉低 MFU。
4. 给整体评估：是否存在明显 MFU 瓶颈算子，以及优化方向。
5. 信息不全时，**明确列出还缺哪些信息**（不要硬编）。
6. 列出profiling数据以及分析结果交付件的路径，方便用户查看。

***

## 扩展注册新算子 FLOPs 公式

目标算子不在 `_flops_formulas.py` 已注册列表内时（第 1 步会列出），msprof-analyze 算不出它的 MFU。本 skill 支持通过 `@register_npu_flop` 自行扩展注册。

**核心铁律**：FLOPs 公式不可强行估算——错误的 FLOPs 比「没有」更糟，会让后续 MFU 全失真。推导不出来就直接停，告诉用户推导不出来。

完整流程见 `references/flops_formula_extension.md`，覆盖：确定公式（按优先级，参考已有→要用户代码→推导不出就停）、注册到 `_flops_formulas.py`、改动展示确认、采集验证（SQL 查 `MSTX_EVENTS` 确认打点 + msprof-analyze 验证算子出现且 `flops` 字段与手算一致）。

***

## 常见问题与兜底

### torch\_npu 相关

| 现象                                                | 原因 / 处理                                                       |
| ------------------------------------------------- | ------------------------------------------------------------- |
| `pip show torch-npu` 有该模块，但 `import torch_npu` 报错 | 多半没 source CANN 环境变量。让用户 `source <CANN 安装路径>/set_env.sh` 后重试。 |
| `_flops_formulas.py` 不存在                          | 当前 torch\_npu 版本不支持 FLOPs 注册，升级 torch\_npu 后再继续，到此暂停。         |
| `import torch_npu` 直接 ModuleNotFoundError         | 当前环境未装 torch\_npu，安装后再继续。                                     |

### msprof-analyze 相关

| 现象                                   | 原因 / 处理                                  |
| ------------------------------------ | ---------------------------------------- |
| `pip show msprof-analyze` 无输出        | 未安装，`pip install msprof-analyze`。        |
| `--help` 的 `-m` 可选值不含 `operator_mfu` | 版本过旧，`pip install -U msprof-analyze` 升级。 |

### 解析结果里没有 MFU 数据

`OperatorMFU` 表为空 / 看不到 mfu 结果：先做第 4 步「确认 FLOPs 采集成功」的 SQL 检查定位——`mfu_flops` 域**无记录**属采集配置问题（回第 2 步核对配置重采）；**有记录但 `OperatorMFU` 仍空**属框架 API→kernel 关联失败（多半 `profiler_level` 不够、kernel 信息没采全），同样回第 2 步核对后重采。不要在错数据上硬解。

### `with_modules` 与 `ModuleMFU` 无关

`ModuleMFU` 表的生成条件是采集时打了 `Module` domain 的 msTX Range（`torch_npu.npu.mstx.range_start/range_end`，domain 用 `"Module"`，见 `references/collection_template.md`）。它和 profiler 的 `with_modules` 参数（仅记录 module 调用栈信息）**没有任何关系**——不要建议用户靠开 `with_modules` 来获取 `ModuleMFU`，那是错误建议。没打 `Module` domain msTX 就不会有 `ModuleMFU`，属正常情况（默认即如此）。

***

## references 索引

- `references/output_fields.md` —— `OperatorMFU` / `ModuleMFU` 表字段说明 + MFU 计算逻辑 + 芯片理论峰值算力参考。解读结果时按需查阅。
- `references/collection_template.md` —— 完整采集脚本模板 + module 级 msTX 打点段。仅对照，不要照抄。
- `references/flops_formula_extension.md` —— 扩展注册新算子 FLOPs 公式完整流程（确定公式、注册、展示确认、采集验证）。目标算子未注册时走此流程。

