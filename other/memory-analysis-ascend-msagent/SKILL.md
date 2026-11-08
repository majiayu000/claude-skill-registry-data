---
name: memory-analysis
description: 对 msMemScope 显存数据做全链路处理：根据用户的显存问题诉求（OOM、显存泄漏、显存占比拆解、Step 间对比等），指导并帮助用户以最合适的 msMemScope 采集配置完成显存数据采集（支持命令行、Python 接口、mstx 打点三种采集方式，覆盖训练、推理 vLLM-Ascend、FSDP、强化学习 verl 等场景）；对已采集的 memscope_dump_*.csv/db 数据做系统性解读与问题诊断（整体显存曲线趋势分析、显存使用大头按模块/组件拆解分析、显存峰值点各模块与流程占比分析，以及对显存泄漏、OOM 等典型问题的根因定位与原因分析）。
keywords: [显存, 内存, memscope, 采集, collect, dump, 解读, 分析, OOM, 泄漏, leak, 拆解, decompose, 峰值, 占比, 曲线, check_leaks, 快照, snapshot, vllm, fsdp, verl]
---

# msMemScope 显存数据采集与解读

## 技能目标

本 Skill 覆盖显存数据全链路：**采集指导 → 数据解读 → 问题诊断**。根据用户的实际诉求，选择正确的采集方式与参数组合，生成可直接执行的命令或代码，指导用户完成采集并确认产物完整可用；随后对采集产物做系统性解读（曲线趋势、显存大头、峰值占比），并对典型显存问题（泄漏、OOM）做根因定位与原因分析。

整体链路：

```
用户诉求 → 采集方案 → 执行采集 → 产物确认 → 数据解读 → 问题诊断
```

> 提示：流程中任一步出现明显报错或异常，先停下排查、修好再继续，不要硬往下走；典型问题已汇总在 Part A 文末「常见问题与兜底」，遇到问题先查那里。

解读是**证据驱动**的：所有结论必须引用 dump 数据中的具体证据（数值、占比、事件、调用栈），以「问题 → 证据 → 建议」的结构组织输出，而不是描述你做了哪些操作；**证据不足时不下结论**，明确列出还缺哪些信息（缺调用栈、缺拆解数据等）。

## 流程入口：先判断数据是否已有

| 用户状态 | 走哪个分支 |
| --- | --- |
| 尚无采集数据（先明确诉求，见 Part A 决策树） | → **[Part A 采集](#part-a-显存数据采集)** |
| 已有 dump 数据（`memscope_dump_*.csv/db`、`memory_compare_*.csv` 或产物目录） | → **[Part B 解读与诊断](#part-b-数据解读与问题诊断)** |

## 何时用 / 何时不用

**用本 Skill**：

- 用户提出显存问题（OOM、显存泄漏、显存占用过高、Step 间显存差异）且**尚无采集数据**，需要采集数据用于分析
- 用户需要采集显存快照、显存拆解（权重/梯度/优化器/kv_cache 等）数据
- 用户要求"帮我采集显存数据""帮我看下内存都花在哪了""帮我采个数分析 OOM"
- 用户提供 msMemScope 采集产物（`memscope_dump_*.csv` / `*.db` / `memory_compare_*.csv` 或产物目录），要求解读或诊断
- 用户询问显存曲线趋势、显存大头、峰值占比，或询问是否存在显存泄漏、OOM 根因

**不要用本 Skill**：

- 非显存维度问题（计算/通信/调度等性能瓶颈）→ 使用 `ascend-*` 系列性能技能
- 需要排查内存踩踏→ 本 Skill 当前不覆盖
- 需要可视化展示数据 → 可引导用户使用 MindStudio Insight 可视化（csv 数据先用 `scripts/convert_dump.py --to-db` 转 db 再导入；本 Skill 只做数据解读）

---

# Part A 显存数据采集

> 本部分适用于**尚无采集数据**的场景。若用户已有 dump 数据，直接跳到 [Part B](#part-b-数据解读与问题诊断)。

## A1 前置条件检查

1. **确认工具已安装**：

   ```bash
   msmemscope --version
   ```

   命令不存在或版本过低时，先安装/升级 msMemScope 工具，再进行后续步骤。

2. **确认运行环境**：采集需要目标训练/推理脚本可运行的环境（CANN 环境变量已 source、Ascend NPU 可用）。

3. **（Python 接口方式）注入环境变量**：使用 Python 接口采集前必须执行：

   ```bash
   source msmemscope --load-api-env
   ```

   > ⚠️ **硬性要求**：使用完毕后，必须执行 `source msmemscope --unload-api-env` 清除环境变量，避免与后续操作产生冲突。若未及时清除，后续执行 set_env 类操作或手动设置 `LD_PRELOAD`、`LD_LIBRARY_PATH` 等 LD 类环境变量时，可能产生不可预知的错误。详见 `references/msmemscope_usage.md`（§5 环境变量管理）。

## A2 采集决策树（核心）

根据用户诉求选择采集方案，**必须先明确诉求再决定配置，不要默认使用同一套参数**：

```
用户诉求
   │
   ├─ OOM / 显存不足 ─────────────► analysis=oom[:K]（联动 alloc/free）+ call_stack
   ├─ 怀疑显存泄漏 ───────────────► 在线：analysis=leaks；离线：mstx mark A/B/C + check_leaks
   ├─ 显存大头 / 占比拆解 ─────────► analysis=decompose（自动使能钩子）+ describe 自定义标签
   ├─ Step 间差异 / 显存增长 ──────► 先分次采集两个 Step 数据，再 --compare 对比
   ├─ 整体曲线 / 趋势 ────────────► events=alloc,free（曲线由 used/device_used 事件驱动）
   └─ 推理 / 强化学习场景 ─────────► 一键分析 init_framework_hooks（vLLM/verl 快照）
        │
        ▼
   场景适配（训练/推理/FSDP/verl 约束检查，见「场景适配表」）
        │
        ▼
   格式：默认 csv（采集快、可直接脚本分析）——仅当用户明确要 MindStudio Insight 可视化时才用 db，见 A5 第 10 条
        │
        ▼
   生成可执行命令 / Python API 代码 → 执行 → 确认产物（见「产物确认」）
```

### 诉求 → 采集方案映射表

| 用户诉求 | 推荐方案 | 关键配置 | 采集方式 |
| --- | --- | --- | --- |
| OOM / 显存不足 | `--analysis=oom[:K]` | 自动联动 alloc/free；建议加 `--call-stack` 便于归因；K∈[1,1000] 默认 10 | 命令行或 Python 接口 |
| 怀疑显存泄漏（在线） | `--analysis=leaks` | `--events` 含 alloc,free | 命令行 |
| 怀疑显存泄漏（离线） | mstx mark A/B/C 打点 + 事后 `check_leaks` | mark 打点标记 A→B→C 范围；采集时 `--events` 含 alloc,free | mstx 打点 + Python 接口 |
| 显存大头 / 占比拆解 | `--analysis=decompose` | 自动使能框架钩子；必要时用 `describe` 自定义标签 | 命令行或 Python 接口 |
| 显存快照（单点） | `take_snapshot()` | `device_mask`、`name` 可选 | Python 接口（独立调用） |
| Step 间差异 / 显存增长 | 分次采集两个 Step + `--compare` | 采集时 `--steps=N`（一次一个 Step）；对比时 `TASK_QUEUE_ENABLE=0`、`--compare --input-path=p1,p2` | 命令行 |
| 整体曲线 / 趋势 | `events=alloc,free`（+可选 launch） | 建议加 `--call-stack` 辅助定位 | 命令行或 Python 接口 |
| 推理（vLLM-Ascend）快照/拆解 | 一键分析 `init_framework_hooks` | 框架 vllm_ascend 11.0 / worker / decompose 或 snapshot | Python 接口 |
| 强化学习（verl）快照 | 一键分析 `init_framework_hooks` | 框架 verl 0.7.0 / TaskRunner / snapshot | Python 接口 |

> 若用户诉求不明确（如"帮我采集数据看看"），**先追问用户想解决什么问题**（是否 OOM、是否怀疑泄漏、是否想知道内存花在哪），再按上表选择方案，不要替用户猜测。

## A3 采集方式与参数详解

msMemScope 支持三种采集方式，各有适用场景：

| 采集方式 | 适用场景 | 说明 |
| --- | --- | --- |
| 命令行采集 | 非 Python 场景（bash 脚本拉起训练等） | `msmemscope [options] bash user.sh` 或 `msmemscope [options] -- <prog> [args]`；**VLLM-Ascend 不支持** |
| Python 接口采集 | Python 训练/推理脚本，需精细控制采集范围 | `config/start/stop/step/take_snapshot` 组合；推荐方式 |
| mstx 打点采集 | 结合 mstx 标记 Step 边界/泄漏分析范围；C 脚本 | `mstx.range_start("step start")` / `mstx.mark`；仅支持单卡局部数据 |

### 采集范围评估：局部 vs 全局（生成采集方案前先评估）

**原则**：先分析用户任务，从理论上评估 **Python 接口局部采集**（`start()/stop()` 包裹目标代码段）能否支撑当前分析诉求；能支撑就用局部采集（数据量小、时间轴聚焦、分析快、资源占用低），**不足以支撑时才用全局采集**。避免"全量采集再分析"——全量数据往往数十万~百万行，后续分析引入不必要的困难。

**诉求 → 采集范围决策表**：

| 用户诉求 | 局部采集可支撑？ | 理由与推荐做法 |
| --- | --- | --- |
| OOM 定位 | ✅ 常可 | OOM 通常发生在特定阶段（profile 段、某 batch、图捕获等），`start()/stop()` 包住触发段即可；需要调用栈时补 `--call-stack` |
| 单阶段拆解 / 大头占比 | ✅ 常可 | 包住目标阶段（如权重加载段、训练循环内一个 Step），数据量小且拆解归因完整 |
| 局部泄漏验证（段内申请段内释放） | ✅ 可 | 包住"申请逻辑 + 释放逻辑"相互独立的一段代码，验证段内块能否全部释放 |
| 泄漏趋势判断（在线/离线） | ❌ 常不足 | 算法 A/B 需要多个周期（Step）的 `used` 曲线对比"是否回基线"，局部单段无法判断周期性增长——至少覆盖多个 Step 或全局采集 |
| 整条曲线全貌 / 进程生命周期 | ❌ 不足 | 需要启动→稳态→退出全过程事件 |
| 未知阶段的排查 | ❌ 不足（第一轮） | 不知道问题出在哪个阶段时，先全局采集看轮廓，再用局部采集聚焦复验 |
| Step 间对比 | ✅ 可 | 分次局部采集两个 Step 数据（`--steps=N`），再 `--compare` |

**局部采集的注意点**：

- **存量显存只统计不分析**：`start()` 前已分配未释放的块只参与总量统计，**不参与泄漏/拆解分析**——若怀疑对象可能在 start 前申请、start 后持续持有，局部采集会漏，需要将 start 提前或全局采集。
- **幽灵机制不变**：局部窗口内的 shadow 判别规则与 Part B 泄漏诊断一致（见 `references/leak_diagnosis_guide.md` §1/§4）。
- 局部采集期间若需要跨 stop 继续观察，用多段 `start()/stop()`，注意 shadow 块在每段 start 时转正参与统计。

### 命令行采集模板

```bash
# 方式一（推荐）：user.sh 为用户脚本
msmemscope [options] bash user.sh

# 方式二：直接指定程序
msmemscope [options] -- <prog_name> [prog_options]
```

常用示例（**格式默认 csv，无需写 `--format`；仅用户明确要 MindStudio Insight 可视化时追加 `--format=db`**）：

```bash
# OOM 分析（K=50，含调用栈）
msmemscope --analysis=oom:50 --call-stack=python:10,c:20 --events=alloc,free bash train.sh

# 显存泄漏检测
msmemscope --analysis=leaks --events=alloc,free --call-stack=python:10 bash train.sh

# 显存拆解（训练场景，自动使能框架钩子）
msmemscope --analysis=decompose --events=alloc,free --output-path=/home/user/output bash train.sh

# 采集指定 Step（供后续 Step 间对比，一次一个 Step）
msmemscope --steps=5 --level=kernel --events=alloc,free bash train.sh

# Step 间对比（采集两个 Step 后执行，与 --input-path 必须成对）
msmemscope --compare --input-path=/home/user/step1,/home/user/step2 --level=kernel
```

### 采集模板（Python 接口 / mstx 打点）

Python 接口模板（`config/start/stop` 组合）、mstx 打点模板（`range_start/range_end` + mark 离线泄漏打点）与 config 参数对应关系见 `references/msmemscope_usage.md`（§2 Python 接口速查）；`assets/collection_template.py` 为可运行参考模板。局部采集（包住目标代码段）见上方「采集范围评估」小节。

### 关键参数速查

| 参数 | 可选值 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--events` | alloc,free,launch,access,traceback,none | alloc,free,launch | alloc/free 不成对配置会导致配对信息缺失；traceback 仅 API 方式可用 |
| `--analysis` | leaks,decompose,oom[:K],none | leaks | 分析功能；none 表示不启用 |
| `--level` | op,kernel | op | 采集算子 or kernel 粒度（旧值 0/1 已废弃） |
| `--call-stack` | python[:N],c[:N] | 深度默认 50 | 采集调用栈，N∈[0,1000]；泄漏归因必需 |
| `--steps` | 1~5 个整数 | 全部 | 指定 Step 采集；与分析功能互斥 |
| `--device` | npu、npu:{id}、cpu | npu | cpu 仅锁页内存 |
| `--collect-mode` | immediate,deferred | immediate | deferred 需配合 start()/stop()；deferred 模式分析功能不可用 |
| `--format` | db,csv | csv | **默认 csv，推荐**：采集快、体积小、便于脚本分析；仅需要在 MindStudio Insight 做可视化时才选 db（采集慢且不利于脚本分析，需转 csv 才能用本 Skill 脚本） |
| `--output-path` | 路径 | memscopeDumpResults | 输出目录 |
| `--compare` / `--input-path` | 成对使用 | - | Step 间内存对比 |
| `--log-level` | debug,info,warning,error | info | 日志级别 |

> 完整参数说明（含废弃参数对照）见 `references/msmemscope_usage.md`（§1 命令行参数全表）。

## A4 场景适配表

不同场景支持的采集/分析能力不同，**必须按用户实际场景核对**；下表为重点约束，完整矩阵与一键分析框架/版本/组件功能表见 `references/msmemscope_usage.md`（§4 场景与采集配置矩阵）。

| 场景 | 支持的采集/分析能力 | 关键注意 |
| --- | --- | --- |
| 训练（Ascend for PyTorch 原生） | 全量：泄漏/拆解/OOM/快照/对比 | 拆解细分类需调用过 `optimizer.step()`；aten 细分类需 PyTorch ≥ 2.3.1 且 `--level=op` |
| 训练（pytorch fsdp1/fsdp2） | 拆解（对应版本区间） | 拆解内容：激活值、分片权重、all-gather 缓冲、梯度等 |
| 推理（vLLM-Ascend 11.0） | 拆解（decompose）、快照（snapshot） | **仅 Python 接口（一键分析）**；命令行采集、泄漏分析不支持 |
| 强化学习（verl）/ 训练（mindspeed_llm） | 快照（snapshot） | 一键分析开启；verl 拆解暂不支持 |

> 完整矩阵与一键分析框架/版本/组件表见 `references/msmemscope_usage.md`（§4 场景与采集配置矩阵）。

### 一键分析（推理/RL 场景专用）

vLLM/verl/mindspeed_llm 场景需通过一键分析接口开启快照或拆解：

```python
import msmemscope
msmemscope.config(events="alloc,free", data_format="csv", output="/home/user/output")  # csv 默认；仅需可视化时改 db
msmemscope.cleanup_framework_hooks()                                       # 清空历史注册
msmemscope.init_framework_hooks("vllm_ascend", "11.0", "worker", "snapshot")  # 框架/版本/组件/功能
msmemscope.start()
# ... 训练或推理逻辑 ...
msmemscope.stop()
```

## A5 硬性约束（MUST DO）

1. **环境变量用后必清**：使用 `--load-api-env` 注入环境变量后，结束采集必须执行 `source msmemscope --unload-api-env`。
2. **分析功能必须含 alloc/free**：使用 `--analysis` 时，`--events` 必须包含 alloc 和 free，否则泄漏分析结果不准确、时间线展示不完整。
3. **`--steps` 与分析功能互斥**：使用内存分析功能时**不要**设置 `--steps`。
4. **VLLM-Ascend 限制**：不支持命令行采集、不支持泄漏分析；请使用 Python 接口 + 一键分析。
5. **deferred 模式限制**：`--collect-mode=deferred` 时内存分析功能不可用；内存块监测、拆解只对采集范围内数据可用。
6. **离线泄漏分析需 mstx mark**：离线 `check_leaks` 必须先用 mark 打点标记 A/B/C 三个点。
7. **对比功能必须成对**：`--compare` 和 `--input-path` 必须一起使用，单个使用无效；对比前需设置 `TASK_QUEUE_ENABLE=0`。
8. **根因优先采集调用栈**：需要做泄漏/OOM 归因分析时，务必配置 `--call-stack`，否则后续无法定位代码位置。
9. **不替用户改脚本**：Python 接口采集需用户脚本配合（加入 start/stop），如用户脚本未集成，告知用户自行集成后重采，不要替用户修改训练代码。
10. **默认用 csv 格式采集**：默认全部使用 csv（`--format` 缺省即 csv；Python 接口 `data_format="csv"`）。仅当用户**明确需要 MindStudio Insight 可视化**时才改用 db；**禁止**"先采 db 再转 csv 分析"的绕路做法——csv 采集更快、体积小，可直接用本 Skill 脚本分析；db 采集慢且无法直接分析，转 csv 是纯浪费。生成采集方案时：无可视化诉求 → csv（不出现 `--format=db`）；有可视化诉求 → 采集 db，分析侧另转 csv（或让用户同时产出 csv）。

## A6 产物确认

采集完成后，确认产物结构与预期一致（默认输出目录 `memscopeDumpResults`）：

```text
memscopeDumpResults/
├── memscope_{PID}_{timestamp}_ascend/          # Python 接口采集的输出目录
│   ├── config.json                             # 采集配置信息
│   └── device_{device_id}/dump/
│       ├── memscope_dump_{timestamp}.csv       # 内存事件数据（--format=csv）
│       ├── memscope_dump_{timestamp}.db        # 内存事件数据（--format=db）
│       └── python_trace_{TID}_{timestamp}.csv  # Python Trace（可选）
└── compare/
    └── memory_compare_{timestamp}.csv          # Step 间对比结果（仅对比场景）
```

确认要点：

- **文件存在且非空**：`memscope_dump_*.csv/db` 已生成。
- **含预期事件类型**：OOM 场景检查是否存在 `Event=OOM_DETAIL` 的记录；泄漏场景检查是否有泄漏回显。
- **OOM 快照**：OOM 通常发生在采集区间内，OOM 前后快照会落盘（`Event=SNAPSHOT`，查看 Attr 与 Call Stack 字段）。
- 采集数据确认无误后，继续本 Skill **Part B** 进行解读与诊断（解读前的数据完整性校验、按时间戳排序及 csv/db 格式转换在 Part B 开头一次性完成，采集侧无需处理）。

## A7 常见问题与兜底

| 现象 | 原因 / 处理 |
| --- | --- |
| `source msmemscope --load-api-env` 后其他工具异常 | LD_PRELOAD/LD_LIBRARY_PATH 被注入，使用完毕后必须 `source msmemscope --unload-api-env` 清理；详情见 `references/msmemscope_usage.md`（§5 环境变量管理） |
| 运行报错但无具体日志 | 加 `--log-level=debug` 重跑定位 |
| OOM 场景下 dump 中无 OOM_DETAIL 记录 | 确认 `--analysis=oom` 已配置；OOM 需发生在采集区间内（immediate 模式为整个运行期） |
| 泄漏分析结果不准确/时间线不完整 | 检查 `--events` 是否同时含 alloc 和 free |
| 使用 `--level=kernel` 且用 HuggingFace tokenizers 时出现"fork 并行被禁用"告警 | 属已知告警，可忽略；或设置 `export TOKENIZERS_PARALLELISM=false` |
| workspace 内存未采集到 | 配置 `TASK_QUEUE_ENABLE=2` 可采集 task_queue 算子下发队列 Level 2 优化的 workspace 内存 |
| mstx 打点采集不到数据 | 确认单卡局部场景；可配置 `PYTHONMALLOC=malloc`（对小内存申请有一定影响） |
| 采集产物目录与预期不符 | 检查 `--output-path`（默认 `memscopeDumpResults`）；Python 接口以 `config` 中 `output` 为准 |

---

# Part B 数据解读与问题诊断

> 本部分适用于**已有采集数据**的场景。若用户尚无数据，先按 [Part A](#part-a-显存数据采集) 完成采集。

## B1 数据产物确认

解读前先确认数据，**不要在没有数据或数据不完整时强行分析**。

1. **定位 dump 文件**：用户提供路径，或查找默认输出目录：

   ```text
   memscopeDumpResults/                                     # 命令行采集
   memscopeDumpResults/memscope_{PID}_{ts}_ascend/device_{id}/dump/   # Python 接口采集
   ```

   涉及的文件：`memscope_dump_{ts}.csv`（事件数据）、`memscope_dump_{ts}.db`（db 格式）、`memory_compare_{ts}.csv`（对比数据）、`config.json`（采集配置）。

2. **核对采集配置**（`config.json` 或询问用户）：确认数据是否满足解读前提：

   | 解读目标 | 前提配置 | 不满足时 |
   | --- | --- | --- |
   | 显存大头 / 占比拆解 | `analysis=decompose`（Attr 含 `owner` 字段） | 无法按模块拆解，只能按事件类型/内存池维度看 |
   | 泄漏归因（代码位置） | `call_stack` 已配置 | 只能定位到分配行为，无法给出代码位置 |
   | 曲线趋势 | `events` 含 alloc/free | 曲线不完整 |

3. **数据预处理（一次性）**：每个数据文件在解读前执行一次格式适配与完整性校验（幂等——已处理过的文件会提示已就绪，不会重复处理）：

   a) **格式适配（按需）**：本 Skill 分析脚本基于 csv（本 Skill 指导采集的产物按 A5 第 10 条应为 csv，无需转换；仅当用户已提供 db 格式时才做 db→csv；需将 csv 导入 MindStudio Insight 可视化时才转 db）。命令见「scripts 使用」格式转换段，双向均流式处理、百万行级可用。⚠️ **转换输出默认在输入文件同目录**（如 `device_0/dump/`），且多卡各 device 的同名 db 可安全逐卡转换；若在 dump 外执行并显式 `--output` 到同一路径，多卡之间会互相覆盖——转换后核对每个 `device_{id}/dump/` 下 CSV 均存在。

   b) **完整性校验与排序**：

   ```bash
   # ① 完整性校验：表头、行数、列数一致性、最后一行是否完整、时间戳是否已有序
   python3 scripts/aggregate_dump.py <dump.csv> --check

   # ② 按时间戳升序排序并覆写原文件（校验提示"未排序"时执行；已有序时自动跳过）
   python3 scripts/aggregate_dump.py <dump.csv> --sort --overwrite
   ```

   校验不通过（如最后一行不完整、列数不一致）时，**先重采或修复数据，不要带病解读**；校验通过且有序后，再进入后续分析步骤。

4. **优先用脚本做数值计算**：涉及聚合、占比、峰值的计算，使用 `scripts/aggregate_dump.py` 执行（见「scripts 使用」），不要手工估算。

5. **数据规模评估**：先判断事件行数落在哪个档位，再选择可行的分析动作（新旧脚本均流式/增量处理，但部分动作在大数据量下不可行或在输出侧受限）：

   | 规模（事件行数） | 曲线 / 聚合 / 时刻快照 | `--check` | `--sort` | csv↔db 转换 | 直接查看 dump / GUI 导入 |
   | --- | --- | --- | --- | --- | --- |
   | < 10 万行 | ✅ | ✅（流式） | ✅ 全量排序，内存可接受 | ✅（流式） | ✅ 正常 |
   | 10 万 ~ 100 万行 | ✅（输出侧用 `--limit` / `--bins` 控制） | ✅ | ✅ 全量排序（内存 O(行数)，百 MB 级） | ✅（百万行实测 ~30s / 峰值 ~8MB） | ⚠️ 导入耗时明显；不要 Read 大文件 |
   | > 100 万行 | ✅（先 `--ascii --bins N` 看宏观，`--limit` 采样） | ✅ | ⚠️ 内存大；mmemosope 产物通常已有序，`--check` 通过即跳过 | ✅ 可用但耗时长 | ❌ 不可行 |

   **大数据量降维策略**（先宏观后微观）：
   - 曲线看宏观：`--curve --ascii --bins N`（分桶绘制）或 `--limit N`（采样数据点）——`--bins` 把数据点聚合成 N 个统计桶（每桶含首/末/最小/最大），是天然的数据拟合；再按需对时间窗放大。
   - 峰值/异常段定位后切片：`--peak [--key used|device_used|process_used]` 自动定位峰值时间戳（直接衔接下一步）→ `--at-timestamp <ts>`（流式维护活跃块集合，内存 O(活跃块)；默认拆**驱动层全集（HAL 事件）**：一级归口表 + 层级分配树，`--pool <池>` 下钻池内）、`--group-by owner --metric peak/total --pool <池>`（O(1) 内存，单维度拆解）。
   - 需要 db 时用 `convert_dump.py`（流式，内存 O(活跃块)，不整文件载入）。
   - ⚠️ **禁止动作**：直接 `Read` 打开大 dump 文件、全量 grep 后人工浏览、大数据量导入 MindStudio Insight——一律改为"脚本提取 + TOP/时段归纳"后再解读。

## B2 系统性解读三件套

### ① 整体曲线趋势

**目的**：判断显存使用整体形态，识别异常增长。

**方法**：

1. 用脚本提取显存曲线数据点：

   ```bash
   python3 scripts/aggregate_dump.py <dump.csv> --curve
   ```

   曲线由事件 Attr 中四个统计键驱动（`used` 进程内用量 / `device_used` 整卡用量 / `process_used` 本进程用量 / `total` 池预留水位），**事件驱动**：仅事件时刻有点，两事件之间为阶梯保持。各键口径构成（device_used 与 npu-smi HBM-Usage 同源、used 与 process_used 差值为 HCCP 占用、total 变大 = 池扩容）与 npu-smi 对照方法见 `references/msmemscope_data.md` §3（统计键口径）/§4（曲线解读）。

2. **曲线形态识别**（对照 `references/msmemscope_data.md` §4 决策树）：

   | 形态 | 可能含义 | 后续动作 |
   | --- | --- | --- |
   | 持续攀升、无回落 | 显存泄漏 / 缓存累积 | 进入「泄漏诊断」 |
   | 阶梯上升 | 内存池按需预留（total 同步增长） | 观察是否超限；评估池预留策略 |
   | 平台期稳定 | 正常运行 | 无需处理 |
   | 峰值后回落 | 瞬时峰值（如大 batch 中间量） | 进入「峰值占比」分析 |

   > 阶梯上升/平台期的**一次性固定大段**还需考虑通信内存：HCCL 每通信域默认申请 ~401MB CCL Buffer（in 200MB + out 200MB + winExp 1MB），通信域创建时一次性出现、不随数据量变化；AIV 模式另 +40MB、MC2 场景另 +16MB。**当用户需要对 HCCL 通信内存展开分析时**，各类通信算子 scratch 大小计算、CCL/AIV/MC2 Buffer 行为与 msmemscope 观测对接详见 `references/hccl_memory_detail.md`。

3. **与 npu-smi 对照**：若用户环境可用 `npu-smi info`，将 `device_used` 曲线与其对照，确认工具数据与整卡实际一致；不一致时说明工具可见范围（host 侧申请）与整卡（含片上/其他进程）的差异。

**报告要点**：曲线形态结论 + 关键转折点（时间戳、对应事件） + 趋势判断（是否异常）。

### ② 显存使用大头（模块/组件维度）

**目的**：回答"显存花在哪了"。

**方法**：

1. 确认数据开启过 decompose（Attr 含 `owner`），否则降级分析（见「B1 数据产物确认」第 2 步）。
2. **用级联模型拆解（单维度操作）**：显存拆解是**级联**的——**HAL 事件是驱动层全集**（其大小 ≈ 进程驱动显存 process_used，**包含 PTA/ATB/MindSpore 框架池向驱动申请的大段，owner=`CANN@APP`**），池事件是同一物理内存的**池内子视图**，两类数值**嵌套、不可相加**。正确路径：默认从驱动层全集（HAL）拆出组件（HCCL/APP/GE/RUNTIME…）→ `CANN@APP` 即框架池段 → 再 `--pool PTA` 下钻池内用途（weight/optimizer/fsdp2…）。HOST（锁页/主机侧）暂不分析。按场景选池后按 owner 聚合：

   ```bash
   # 驱动层全集拆解（默认；含框架池段，owner=CANN@APP）
   python3 scripts/aggregate_dump.py <dump.csv> --group-by owner --metric peak --pool HAL
   # HAL 之下第二层：框架池内用途拆解
   python3 scripts/aggregate_dump.py <dump.csv> --group-by owner --metric peak --pool PTA
   ```

3. 解读 owner 多级分类（`@` 分隔，如 `PTA@fsdp2@all_gather_output@ops`）：**首段是分配器来源（FRAMEWORK 级）**——PTA 池为 `PTA`，**HAL 池为 `CANN@<组件>`（CANN@HCCL/CANN@APP/CANN@GE/CANN@RUNTIME）**；丢弃首段后才是该维度的下一级（PTA 池 → weight/optimizer/fsdp2…，HAL 池 → HCCL/APP/GE…）。各段是独立级别槽位（框架@组件@流程@细化），空段跳过，**同一维度内深度天然不一致**，细分标签见 `references/msmemscope_data.md` §6.2。
4. **优先从框架内存池入手**：框架内存池是显存分析的重点对象（pytorch 用户优先 PTA），先判断框架池是否异常再联动其他池；内存池语义（HAL 为各框架池总量的父集、池扩容失败触发 OOM）见 `references/msmemscope_data.md` §5（内存池模型）。
5. 通信场景（HCCL 集合通信多的训练/推理任务）：HAL owner 中出现的**一次性固定大段**多为 CCL Buffer（默认每通信域 ~401MB，AIV/MC2 场景另加）或算子 scratch——用 `--hal-segments` 直接列出 HAL 池大段清单（含 `alloc_type`/`page_type`，`alloc_type=create` 即 expandable 生效），按通信类型与运行模式核对应然大小（详见 `references/hccl_memory_detail.md`）。
6. 输出大头排名（Top-N，含占比），说明每项的来源与合理性。

> 需要深入组件/框架行为时按需读取：PTA 池行为 → `references/pta_memory_management.md`；vLLM-Ascend 显存管理 → `references/vllm_ascend_memory_management.md`（MindSpore/ATB 独立文件后续补充）。

### ③ 显存峰值点占比

**目的**：回答"峰值时刻各模块/流程占比多少"。

**方法**：

1. 定位峰值时间点：`--peak [--key used|device_used|process_used] [--pool <池>]` 自动定位（输出峰值时间戳，可直接衔接 `--at-timestamp`）；或使用 SNAPSHOT 记录的 `peak_allocated`/`peak_reserved` 字段。
2. 默认从驱动层全集拆解（HAL 事件，含框架池段 owner=`CANN@APP`）；按场景下钻——`--pool PTA`（框架池内用途，weight/optimizer_state/fsdp2…）。命令筛选生命周期包含该时间点的内存块，输出**池内一级归口表**（丢弃框架段，含各子级）+ **层级分配树**（按 组件→流程→细化 下钻，每节点含占用/占比/块数）：

   ```bash
   # 驱动层全集拆解（默认；含框架池段；≈ process_used）
   python3 scripts/aggregate_dump.py <dump.csv> --at-timestamp <ns>
   # 显式 HAL / 第二层池内
   python3 scripts/aggregate_dump.py <dump.csv> --at-timestamp <ns> --pool HAL
   python3 scripts/aggregate_dump.py <dump.csv> --at-timestamp <ns> --pool PTA
   ```

   ⚠️ 级联口径：HAL 是驱动层全集，**框架池的物理段已计入 HAL 事件**（CANN@APP），池事件是同一物理内存的池内子视图——**HAL 与池两类数值嵌套、不可相加**，不存在"池并列汇总"；HOST 暂不分析。
3. 峰值成因：结合峰值时间戳前的 OP_LAUNCH/KERNEL_LAUNCH 事件、Call Stack 与 python_trace（若采集）识别关键算子/代码段；结合 SNAPSHOT 字段（`allocated`/`reserved`/`device_utilization`/`pt_utilization`）补充整卡水位（判定方法与成因分析详见 `references/msmemscope_data.md` §7）。

## B3 典型问题诊断

### ④ 显存泄漏诊断

**入口一：在线泄漏分析（采集时已运行 `--analysis=leaks`）**：采集结束工具回显逐卡泄漏汇总（泄漏 Step 数、关联 kernel、地址、泄漏大小）+ 内存波动（单 Step 最小/最大占用比）。**第一 Step 波动可忽略**（内存尚未稳定），从第二 Step 起分析。

**入口二：离线泄漏分析（mstx mark A/B/C + check_leaks）**：A→B 范围申请、C 点前未释放即判定泄漏；用户未执行时指导执行 `msmemscope.check_leaks(input_path=..., mstx_info=..., start_index=0)`。

**核心原则（幽灵机制）**：进程退出时未释放的块会被工具**补发 shadow FREE**，因此 **dump 中 MALLOC/FREE 必然配对——"有配对"不是无泄漏的证据**；泄漏判定的正确口径是"该 Ptr 的 FREE 是否全部为 `shadow:true`"（机制与操作见 `references/leak_diagnosis_guide.md` §1~§2）。

**检测方法速览**（算法细节、风险分级、shadow 来源判别、常驻内存区分见 `references/leak_diagnosis_guide.md` §3~§4）：
**0）脚本先筛候选块**（算法 C 的块级筛选自动化）——优先分析**长生命周期内存**与**随进程退出补齐释放（shadow FREE，无真实释放动作）** 的块：

```bash
python3 scripts/aggregate_dump.py <dump.csv> --leak-candidates [--detail N] [--pool PTA]
```

输出：候选块汇总（块数/大小/占全部申请量比/含 shadow FREE vs 无任何 FREE 分类）、按 owner 与**维度内一级归口**（丢弃框架段）聚合、申请时间跨度（早-常驻 vs 晚-新增）、调用栈首帧 TOP、候选块明细（`--detail` 控制条数，0=不输出）。`--pool <池>` 按单维度扫描（默认 HAL 驱动层全集；池事件是嵌套子视图，两类不可相加）；筛出的候选块再逐一判别 shadow 来源（换栈/退出补齐/真泄漏）与常驻内存；随后按序走算法 **A（used 跨周期不回基线，强信号）** → **B（预留增长，弱信号，须与 A 联动）** → **C（长生命周期块 shadow 判别）** → **D（堆栈归因 TOP3）**。

**原因分析**：对照 `references/leak_diagnosis_guide.md` §5 常见泄漏模式（缓存未清理、梯度/优化器状态累积、KV cache 增长、循环内重复申请、Python 引用残留等），给出"现象特征 → 证据 → 假设 → 验证路径"。

### ⑤ OOM 诊断

OOM 数据在 dump 的 `Event=OOM_DETAIL` 中，三类记录（Attr 中 Event Type 区分）：

| Event Type | 内容 | 解读要点 |
| --- | --- | --- |
| `OOM_TRIGGER` | 触发操作：`func`、`req_size`、`flag`、`ret` | 谁在申请、申请多大触发 OOM |
| `OOM_RECENT_ALLOC` | 最近 K 条未释放记录（`pool`/`ptr`/`size`/`timestamp`/`step`/`kernel` + Call Stack） | 识别"压死骆驼的最后一根稻草" |
| `OOM_TOP_ALLOC` | 最大 K 条未释放记录 | OOM 时的大头占用者 |

**诊断步骤**：脚本一键汇总 `--oom [--detail N]`（OOM_TRIGGER/TOP_ALLOC/RECENT_ALLOC 三表 + 量化推断提示自动判定）→ ① 看 `OOM_TRIGGER`（req_size 巨大 = 单次巨量申请；不大 = 总量已耗尽）→ ② 看 `OOM_TOP_ALLOC` 大头归属（权重/kv_cache/激活/中间量）→ ③ 看 `OOM_RECENT_ALLOC` 分配序列 → ④ 结合 Call Stack 与 owner 归因到代码位置 → ⑤ 区分**框架池扩容失败 OOM**（`func` 指向池扩容路径时，根因是池内占用过高、可回收不足，而非单次大申请）。

> 字段明细、量化推断规则（req_size ≥80% 剩余空间、同栈重复 ≥3 次、RECENT 累积型判定等）与典型场景示例见 `references/oom_diagnosis_guide.md`。

### ⑥ 显存碎片分析

**目的**：回答"池预留（`total`）高但实际使用（`used`）低，是否碎片导致、能否通过配置回收"。

**方法概要**：

1. **算碎片率**：`--fragmentation [--pool <池>]` 一键输出池扩容清单（时间戳/前后 total/增量/扩容前 used/total/伴随 HAL 段）+ 碎片率统计（当前/峰值/均值/最差时刻）+ 有效使用率最低 TOP5；或 SNAPSHOT `1 − pt_utilization`；峰值时刻与稳定期各算一次；分级 <5% 正常 / 5~15% 偏高 / >15% 严重。
2. **量化池预留行为**：扩容频率按运行时长/Step 数归一化；HAL 段"申请后从未归还"是池缓存正常行为（释放≠归还）；扩容前 `used/total` 为池有效使用率。
3. **观测盲区**：msmemscope 无段级/块级存量视图，逐段碎片率、块状态分布、假性碎片判定需引用 **ascend-npu-snapshot-analyzer** skill 补采 snapshot；⚠️ 多流场景碎片率高有三种候选解释（真碎片/流池残留/跨流延迟假性碎片），无法区分。

**建议速查**（配置杠杆详见 `references/pta_memory_management.md` §4.1 与 §7.3）：
- 碎片严重且频繁扩容 → `expandable_segments`（与 `max_split_size_mb`、`garbage_collection_threshold` 互斥）
- 碎片集中大块段 → `max_split_size_mb`；池缓存长期占位、可接受间歇回收 → `garbage_collection_threshold` 或定期 `empty_cache()`
- 多流场景 → 检查流复用设计（每流池 total 只增不减，见 `pta_memory_management.md` §3.2）

> 口径明细与观测边界见 `references/msmemscope_data.md` §9（碎片分析口径）。

4. **建议**（配置杠杆详见 `references/pta_memory_management.md` §4）：
   - 碎片严重且频繁扩容 → `expandable_segments`（注意与 `max_split_size_mb`、`garbage_collection_threshold` 互斥）
   - 碎片集中于大块段 → `max_split_size_mb`
   - 池缓存长期占位、可接受间歇回收 → `garbage_collection_threshold` 或定期 `empty_cache()`
   - 多流场景 → 检查流复用设计（每流池 total 只增不减，见 §3.2 流池残留）

## B4 输出报告结构

最终回复按以下结构组织（数据缺失时在对应位置显式说明）：

1. **分析概要**：数据来源路径、采集配置（事件/分析功能/调用栈是否开启）、分析范围。
2. **证据**：表格形式呈现关键数据——曲线形态与关键转折点、大头 Top-N 与占比、峰值时刻占比、泄漏/OOM 关键记录（引用具体数值）。
3. **结论**：是否存在问题、问题类型（泄漏/OOM/显存增长/正常）、严重程度。
4. **建议**：针对性优化建议与验证路径（复采验证、修改方向）。
5. **交付件路径**：dump 数据与分析产物路径，方便用户查看。

## B5 常见解读误区

| 误区 | 正确做法 |
| --- | --- |
| 把第一 Step 的内存波动当作泄漏证据 | 第一 Step 内存尚未稳定，从第二 Step 起分析（在线泄漏分析本身即如此） |
| 认为 `device_used` 等于本进程使用量 | `device_used` 是整卡用量（含片上/其他进程）；本进程用量看 `used`/`process_used` |
| `device_used` 为 `-1`（或键省略）时仍引用该值 | 说明环境不支持整卡用量查询，改用 `used`/`process_used` 分析 |
| 没开 decompose 却按 owner 拆解 | 无 `owner` 字段时只能按事件类型/内存池维度分析，明确告知用户信息缺失 |
| 用曲线点当轮询采样 | 曲线是事件驱动的（仅 HAL/池事件时刻有点），两事件之间是线性填充/阶梯，不代表中间态采样 |
| 把历史显存块计入泄漏 | start 前的存量显存只参与统计（总量准确），不参与泄漏/拆解分析 |
| 证据不足强行下结论 | 列出缺失信息（缺调用栈、缺拆解、缺对比数据），按 Part A 补采对应配置的数据 |
| 把"MALLOC/FREE 一一配对"当作无泄漏证据 | 幽灵机制保证必然配对（未释放块在进程退出时被工具补发 shadow FREE）——配对不是无泄漏证据；泄漏判别看该 Ptr 的 FREE 是否全部为 `shadow:true`、及跨周期增长性 |
| 把幽灵释放（attr `shadow:true`）一概当作未释放内存 | shadow 有两种来源：非采集期正常释放（真实释放行为）与进程退出时统一释放（未释放内存）；前者挂在中间 stop 点之后、后者挂在最后一次 stop/退出时刻，按采集状态与时间戳判别 |
| 把常驻内存误判为泄漏 | 常驻内存一般在程序前期申请、总量稳定；泄漏常见周期性增长，按增长性判别（见泄漏诊断） |
| 数值计算手算 | 聚合、占比、峰值计算用 `scripts/aggregate_dump.py`，保证准确可复现 |

---

# scripts 使用

`scripts/aggregate_dump.py` 对 `memscope_dump_*.csv` 做数据预处理、确定性聚合统计与本地可视化（仅依赖 Python 标准库）；`scripts/convert_dump.py` 做 csv ↔ db 格式转换（与官方 db 格式一致，字段口径详见 `references/msmemscope_data.md`）：

> **运行前提**：仅依赖 Python 3 标准库（3.7+，输出编码自适应）。**Linux 使用 `python3`，Windows 使用 `py -3`（或 `python`）**执行；脚本无平台相关调用，两者输出一致。输出统一为 UTF-8（Windows 控制台为 GBK 时自动替换，不报错）。

```bash
# ---- 格式转换（csv ↔ db）----
# 两个方向均流式处理（内存 O(活跃块数)，不整文件载入），百万行级可用
# db → csv（供分析脚本使用；默认输出到**输入文件同目录**（如 device_0/dump/），文件名 memscope_dump_{时间戳}.csv；⚠️ 多卡各 device 的同名 db 默认互不覆盖，但显式 --output 到同一路径仍会覆盖，多卡批量转换建议逐卡转换或按卡指定 --output）
python3 scripts/convert_dump.py <dump.db> --to-csv
# csv → db（导入 MindStudio Insight 可视化；默认输出 memscope_dump_{时间戳}.db；建议输入先 --sort 保证时间序）
python3 scripts/convert_dump.py <dump.csv> --to-db
# 旧版工具链表名为 leaks_dump 时用 --table 指定
python3 scripts/convert_dump.py <dump.csv> --to-db --table leaks_dump

# ---- 数据预处理（每个文件一次，幂等）----
# 完整性校验（表头/列数/行关键字段/是否已有序；流式，O(1) 内存）
python3 scripts/aggregate_dump.py <dump.csv> --check
# 按时间戳排序（--overwrite 覆写原文件；已有序时自动跳过；排序需全量载入，大数据量且有序时跳过此步）
python3 scripts/aggregate_dump.py <dump.csv> --sort --overwrite

# ---- 聚合统计与可视化 ----
# 级联单维度拆解：HAL=驱动层全集（含框架池段 CANN@APP，≈process_used）；PTA 为第二层池内视图（与 HAL 嵌套不可相加）
python3 scripts/aggregate_dump.py <dump.csv> --group-by owner --metric peak --pool HAL
python3 scripts/aggregate_dump.py <dump.csv> --group-by owner --metric peak --pool PTA
# 未开 decompose 的降级分析：按事件类型（HAL/PTA/...）聚合（仅作层次参考，不并列相加）
python3 scripts/aggregate_dump.py <dump.csv> --group-by event_type --metric peak

# 统计指定时间点（如峰值时刻）活跃块分布：默认拆 HAL 驱动层全集（一级归口表 + 层级分配树，占比默认输出）；--pool 下钻池内
python3 scripts/aggregate_dump.py <dump.csv> --at-timestamp <ns>
python3 scripts/aggregate_dump.py <dump.csv> --at-timestamp <ns> --pool PTA

# 扫描泄漏候选块（FREE 全部为 shadow:true 或无任何 FREE 事件的块；默认 HAL 驱动层全集，--pool 指定维度；按 owner/维度内一级归口/申请时间跨度/调用栈聚合，--detail N 控制候选明细条数，0=不输出）
python3 scripts/aggregate_dump.py <dump.csv> --leak-candidates [--detail N] [--pool PTA]

# 输出整卡/进程显存曲线数据点（ts, device_used, used）
python3 scripts/aggregate_dump.py <dump.csv> --curve

# 输出文本化曲线（ASCII，无外部依赖）
python3 scripts/aggregate_dump.py <dump.csv> --curve --ascii

# 峰值定位（--key 选择 used/device_used/process_used，默认 used；--pool 指定维度）；
# 输出的峰值时间戳可直接衔接 --at-timestamp <ts> 做时刻拆解
python3 scripts/aggregate_dump.py <dump.csv> --peak [--key used] [--pool HAL]

# OOM 诊断汇总（OOM_TRIGGER/TOP_ALLOC/RECENT_ALLOC 三表 + 量化推断提示，--detail 控制条数，0=不输出明细）
python3 scripts/aggregate_dump.py <dump.csv> --oom [--detail 10]

# 池碎片率与扩容画像：扩容清单（时间戳/前后 total/增量/扩容前 used/total/伴随 HAL 段）+
# 碎片率统计（当前/峰值/均值/最差时刻）+ 有效使用率最低 TOP5（--pool 指定池，默认全部池事件）
python3 scripts/aggregate_dump.py <dump.csv> --fragmentation [--pool PTA]

# HAL 池大段清单（供应然值核对：CCL Buffer ~401MB/域、MC2 16MB、AIV 40MB、池扩容段 20MB 等；
# alloc_type=create 出现即 expandable_segments 生效判定）；--min-size 过滤（支持 KB/MB/GB 后缀，
# 默认 100MB，段数过少可调小）
python3 scripts/aggregate_dump.py <dump.csv> --hal-segments [--min-size 100MB]

# 跨周期趋势（泄漏算法 A/B 自动化）：等宽桶输出 used/total 末值 + 单调/不回基线判定；
# 默认拆 HAL + PTA 双视图（PTA 存在时；HAL 段级仅参考，PTA 块级 used=算法 A），--pool 指定单一池
python3 scripts/aggregate_dump.py <dump.csv> --trend [--buckets 20]

# 数据画像：事件分布/时间范围/解析能力提示（owner/SNAPSHOT/OOM/Call Stack 可用性，分析前体检）
python3 scripts/aggregate_dump.py <dump.csv> --stats

# 时间窗切片：起点/终点活跃块、窗口内申请/释放/净变化、TOP 归口（纳秒，含端点）
python3 scripts/aggregate_dump.py <dump.csv> --window <START> <END> [--pool HAL]
```

# references 索引

按知识层次分类：**工具使用**（msmemscope 工具怎么用）→ **数据理解**（数据是什么、怎么通用解读）→ **问题诊断**（具体场景的诊断指南）→ **框架/组件机制**（跨场景的底座知识）。新增知识按此分类落位，命名规则：`{scenario}_diagnosis_guide.md` / `{framework}_memory_management.md` / `{component}_memory_detail.md`。

**工具使用**：
- `references/msmemscope_usage.md` —— msMemScope 工具本身的用法：CLI/Python 接口参数全表（含废弃参数对照）、采集模板、输出文件位置、场景 × 采集配置矩阵（分析能力总览/场景能力矩阵/一键分析组合/自动拆解范围/配置速查/限制）、环境变量管理与常见风险（§5）。

**数据理解**：
- `references/msmemscope_data.md` —— 采集数据字段口径与通用解读：输出文件列结构、Attr 各键（SNAPSHOT/OOM_DETAIL/Call Stack 等）、统计键口径（§3）、曲线形态决策树（§4）、内存池模型（§5）、owner 聚合（§6）、峰值定位与占比（§7）、常见口径陷阱（§8）、碎片分析口径（§9）。

**问题诊断**：
- `references/leak_diagnosis_guide.md` —— **显存泄漏诊断**（幽灵机制与配对误区、泄漏点识别、算法 A/B/C/D、风险分级、shadow 来源判别、常见泄漏模式对照 §5、与 snapshot-analyzer 差异）。
- `references/oom_diagnosis_guide.md` —— OOM 诊断步骤与典型场景解读示例。

**框架机制**：
- `references/pta_memory_management.md` —— PTA（TorchNPU）显存管理行为模式（五条显存通道、池分配/释放/扩容决策、流池模型、配置调优杠杆、SNAPSHOT 统计语义、分析与调优速查——预期曲线形态/异常点定位/优化杠杆对照表）。**其他会管理显存的框架（MindSpore/ATB 等后续逐个补充为独立文件）**。
- `references/vllm_ascend_memory_management.md` —— vLLM-Ascend 推理框架显存管理行为模式（显存全景与 PTA 池载体、KV cache 容量 profile 计算、块结构与 Ascend 特有 cache spec、MC2 通信预留、图捕获内存、swap/offload、分析与调优速查）。**当用户的分析对象是 vLLM-Ascend 框架时读取本文件细化分析**。

**组件机制**：
- `references/hccl_memory_detail.md` —— HCCL/HCOMM 通信显存行为模式（CCL Buffer 与 Scratch Buffer 两类管理机制、各通信算子 scratch 大小计算公式、AIV/MC2 特殊 Buffer、Buffer 共享、分析与调优速查）。**当用户需要对 HCCL 通信内存展开分析时优先读取本文件细化分析**。

### 各维度速查定位总表

> 各组件/框架的"分析与调优速查"**结构按自身特性设计，不强求对齐**，分析过程中**按需翻表**，不必从头读正文。每个实体文档的速查章节都以「预期曲线/信号形态 → 异常点定位 → 优化杠杆」为主干，但切入方式因组件而异（例如：PTA 侧重池曲线形态判别与实验验证、HCCL 侧重应然值正向核对、vLLM 侧重启动序列阶段核对）——具体切入方式以对应文档为准。后续新增组件/框架文档时，在本表追加一行即可，无需改动其他条目。

| 分析目标 | 速查入口 |
| --- | --- |
| 曲线形态通用识别（阶梯/锯齿/平台/陡降） | SKILL B2① 形态表 → `msmemscope_data.md` §4 曲线形态决策树 |
| PTA 池行为：释放≠归还、扩容、碎片、池配置、expandable 生效判定 | `pta_memory_management.md` §7（7.1 曲线 → 7.2 异常 → 7.3 杠杆） |
| 通信内存：HAL 大段归属、scratch 应然值核对、AIV/MC2、共享 | `hccl_memory_detail.md` §6（6.1 曲线 → 6.2 应然值核对 → 6.3 异常 → 6.4 杠杆） |
| vLLM-Ascend 推理：KV 容量、启动序列、推理期异常 | `vllm_ascend_memory_management.md` §9（9.1 曲线 → 9.2 异常 → 9.3 杠杆） |
| OOM 归因与处置 | `oom_diagnosis_guide.md`（先于 §7.2/§9.2 的 OOM 行进入） |
| 泄漏判定与模式 | SKILL B3④ → `leak_diagnosis_guide.md`（判定方法 §1~§4 → 模式对照 §5） |
| 碎片量化与深层核对 | `msmemscope_data.md` §9 → ascend-npu-snapshot-analyzer |
| 字段/事件口径疑问 | `msmemscope_data.md` §1~§3 |

# assets

- `assets/collection_template.py` —— Python 接口采集参考模板（仅对照，不要求照抄）。
