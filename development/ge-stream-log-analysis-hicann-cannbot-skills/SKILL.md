---
name: ge-stream-log-analysis
description: Analyze GE/CANN compile and runtime stream logs with optional GE repository context. Use when a user asks for static or dynamic stream-allocation evidence, runtime stream requests, or mapping compile logical stream IDs to runtime RT stream IDs. Reports evidence with file paths and line numbers.
license: CANN-2.0
---

# GE/CANN 流日志分析

仅使用 GE 的 INFO 日志分析 atc 编译日志和 ACL/GE 运行日志。GE 仓库上下文是可选的：提供时只校验 GE 仓库目录标记并记录上下文，不宣称脚本已经完成源码或文档内容校验；不提供时进入 `log_only` 模式，仅依据日志中的函数、源码位置、PID、context 和时间字段分析。解析器消费 GE `[INFO]` 输出，以及兼容旧日志的 `KERNEL_TRACE` `[INFO][KernelTrace]` 输出；DEBUG/TRACE/WARNING/ERROR、`GEEVENT`/`[Event]` 形式的 `GEPERFTRACE` 和仅有函数名的源码调用不参与结论。由 GE INFO 日志输出的 `[INFO][GEPERFTRACE]` 可以保留为耗时结束证据，但不能当作函数入口或调用栈。外部 RTS/Runtime 日志（例如 `ModelExecuteTask`、`ConstructSqeForModelExecuteTask`）完全忽略且不计入报告。只读仓库目录标记、参考资料和日志，不执行日志内容、不加载模型、不访问设备。先运行脚本获得事实，再结合仓库参考解释；缺少某项 INFO 证据时该字段输出 `unknown`，没有任何流证据时输出 `no_stream_evidence`，不要猜测。

## 快速使用

用户只需要提供一个日志文件集合或目录；skill 会同时识别其中的编译期和运行期 INFO 记录：

先将 `<skill-root>` 替换为当前目录 `graph/ge-stream-log-analysis` 的绝对路径：

```bash
SKILL_DIR=/path/to/graph/ge-stream-log-analysis
python3 "$SKILL_DIR/scripts/analyze_stream_logs.py" \
  --log-dir /path/to/all_model_logs \
  --format markdown
```

多个分卷文件也可以直接重复 `--log`：

```bash
python3 "$SKILL_DIR/scripts/analyze_stream_logs.py" \
  --log /path/to/model.log.0 --log /path/to/model.log.1 \
  --format markdown
```

`--compile`/`--runtime` 仍然保留，用于已经明确分组的旧调用；`--log`/`--log-dir` 下的文件会进入同一次统一扫描，文件中无关内容直接忽略。

```bash
python3 "$SKILL_DIR/scripts/analyze_stream_logs.py" \
  --compile /path/to/atc.0.log --compile /path/to/atc.1.log \
  --runtime /path/to/runtime.0.log --runtime /path/to/runtime.1.log
```

需要在 JSON 或 Markdown 中展开每条流的完整算子列表：

```bash
python3 "$SKILL_DIR/scripts/analyze_stream_logs.py" \
  --compile atc.log --runtime runtime.log --full-ops --format json
```

Markdown 默认使用证据优先的紧凑视图：总览、每个图的编译/运行阶段证据、逻辑流对应算子、逻辑流到 RT 流映射，以及缺失证据。不会输出图层级或重复会话明细；算子表默认按 `--sample-limit` 展示每条流的算子名和类型，`--full-ops` 展开全部算子。`--verbose` 只在证据引用后附加原始日志摘要。JSON 保留完整解析结构，并额外提供面向报告的 `stream_records`。

目录中包含多个模型时，Markdown 按图记录分别展示，不合并不同模型；JSON 中可通过 `sessions` 或 `stream_records` 读取独立结果。需要 GE 仓库目录标记和上下文校验时再显式传入 `--repo-root`；该参数不会代替人工源码/文档核对。可使用脚本输出的 `session_id` 精确选择某个会话：

```bash
python3 "$SKILL_DIR/scripts/analyze_stream_logs.py" \
  --log-dir /path/to/logs --session 'compile:1234:graph_a:1+model:1234:7' \
  --repo-root /path/to/ge
```

## 分析流程

1. 检查日志路径可读。若提供或自动发现 GE 仓，校验 `compiler/graph/build/stream`、`runtime`、`docs/zh/design/features/stream_allocator.md` 和 `docs/zh/design/constraints/stream_allocator.md` 等目录标记；未发现 GE 仓时使用 `log_only` 模式，不阻断分析。目录标记通过只读路径检查完成，不等价于源码内容核验。
2. 收集用户提供的全部文件或目录；不要要求用户预先区分编译期和运行期。
3. 读取 [stream_semantics.md](references/stream_semantics.md) 和 [log_patterns.md](references/log_patterns.md)，理解三层 ID、INFO 过滤、静态/动态边界、V1/V2 日志版本别名和证据优先级；需要编译或运行阶段背景时再读取 [compile_phase_flow.md](references/compile_phase_flow.md) 或 [runtime_backend_flow.md](references/runtime_backend_flow.md)。
4. 逐行扫描全部文件，只保留 `[INFO]` 行；解析时间、PID、GE context、函数和源码位置后，把事件路由到同一个 `GraphWorkflow`。文件中无关日志直接忽略，不再把编译和运行拆成两个互不相干的顶层结果。
5. 先识别日志中的模型场景（静态、动态或混合），再对每个图依据实际 known/unknown 入口选择静态或动态编译路径；运行侧依据实际 V1/V2 日志选择申请和绑定路径，不用顶层场景标签替代图级证据。
6. 按实际 GE INFO 日志建立阶段边界：图构建入口（`Begin to build known/unknown shape graph`）、静态最终流汇总（`At last, root graph`）、动态成功汇总（必须由 `AssignStreamsForDynamicShapeGraph` 函数输出 `Graph: ..., stream num: ..., event num: ...`）和静态流刷新结束（`After SplitStreamAndRefreshTaskDef`）。`BuildModelForGetTask`、`AssignLogicalStreams`、`AssignStreamForDynamicShapeGraph`、`LoweringAndSplitRtStreams` 仅在没有对应 GE INFO 日志时作为源码上下文；`RefreshInfoOfDynamicShapeGraph` 的 Root/Sub/Total 直接忽略，不参与任何流数、边界或关联结论。`[INFO][GEPERFTRACE]` 若由 GE INFO 日志输出，只能作为耗时结束证据；`[Event]` 形式不参与边界和调用栈判断。
7. 顶层只报告场景/Shape、图形态、运行后端、单/多流判断和总体状态；每个图记录自己的 `compile_path`、编译窗口入口/流出口、最终逻辑流数、流级算子映射、运行申请/创建/绑定证据和映射状态。不要把其它图的结果回填到当前图。Markdown 不展开父子层级或重复的会话明细。
8. 报告逻辑流、模型流和 RT 物理流，不把所有 `Create new stream` 相加，也不提取外部 ModelExecute 入口流；V1 关注实际 GE INFO 日志中的 `InitRuntimeParams`/`Create new stream`/`Logical stream index`，V2 优先关注 `Build RT2 executor`、`OccupyStreamResource` 和 `AcquireStreams` 输出的 `Collect rt2 stream` 绑定。资源数字允许日志实际使用的空格、冒号、等号或 `is` 分隔。连续或分卷重复的 V2 资源摘要只作 executor 窗口内资源证据，不建立新模型边界；相同摘要去重并保留重复证据，不同 scope 可共存，同 scope/name 数量冲突需显式标记。旧版本没有新日志时，才使用 `[KernelTrace][SplitRtStreams(?:_<suffix>)?]` 作为 fallback；它不建立 V2 模型身份，也不覆盖新日志。
   V1 Hybrid 的 `Start to init hybrid model`、`HybridModel will execute in rt1.0...`/`pipeline...`，以及 RT2 分支的对应字符串，均是源码定义的可选上下文标记；只有实际出现时才记录到 `hybrid_context_markers`，不能要求它们同时出现，也不能据此计算流数。动态 Batch 的真实 INFO 场景标记还包括 `Found dynamic batch, shape ...` 和 `Add batch graph[Batch_N] ...`，但它即使归入 dynamic 场景，也按实际图级路径使用 V1 DavinciModel 流日志，不得套用 V1 Hybrid 动态标记。
9. 每个结论引用日志文件、行号、日志级别和关键字；报告声明 `log_level_filter=INFO`。缺少编译入口/出口、运行申请或绑定时，在对应图记录中写 `unknown`/`partial`，不得默认判断单流。
10. 用户若询问“谁调用了这个函数/调用栈”，只能把日志作为阶段证据；调用关系必须通过源码 `rg`、IDE“查找引用”或带符号调试器确认，不能从 `time cost of` 或 Kernel Trace 行反推。

统一扫描器只维护一份图级状态：图入口创建 workflow，编译出口、逻辑流/算子事实、运行资源和绑定事实最终归并到该 workflow。V1 运行记录用 `model_id` 分界；V2 只把 `Build RT2 executor for root compute graph[...]` 作为显式模型边界，并先按 graph name 精确匹配编译 workflow（编译/运行可来自不同 PID），再将同一运行 PID、同一 executor 窗口下跨 GE context/轮转文件且 logical index→RT ID 交集不冲突的资源、Collect 和 SplitRtStreams 片段合并；子集、超集及不相交索引均取并集。没有 graph name 时才用 PID、编译先于运行和 logical index 集合匹配建立唯一 `same_session` 关联。动态图候选资格优先来自自身 `AssignStreamsForDynamicShapeGraph` 成功汇总；若只有严格命名的 `*_sub_<N>_unknow(n)` 编译入口、没有动态流汇总，且运行期 executor 只观察到 logical 0，则隐藏这些编译 unknown 图，保留命名的运行期 root graph 和 `logical 0 -> RT stream` 证据，不生成 `compile_logic_stream_id=unknown` 占位行。多个候选保持 `unknown`，同一 logical index 对应不同 RT ID 的冲突片段不得合并。

## 输出重点

Markdown 固定按“总览 → 图级流证据 → 逻辑流对应算子 → 逻辑流到 RT 流 → 未完整证据（及必要告警）”排列；
每个图只占图级表一行，编译和运行证据在同一行对齐，逐条映射只在第二张表出现一次。

- 总览：GE INFO 日志过滤范围、场景/Shape、编译最终逻辑流数、`single_stream`/`multi_stream`/`unknown` 判断、算子映射一致性、编译图记录数、运行记录数、关联数和总体状态。输入文件路径保留在 JSON 证据上下文中，默认 Markdown 不重复列出。
- 图级流证据表：每个图一行，依次展示静态/动态编译路径、编译窗口入口、实际编译分配入口/过程（若日志存在）、逻辑流分配出口（以及静态物理流刷新出口）、编译最终逻辑流数和单/多流策略、实际运行路径、运行申请/创建/绑定数量、关联和状态。静态路径没有独立入口 INFO 时明确写 `not_observed`，不把 `AssignLogicalStreams` 函数名或 timing 行冒充入口。运行创建数可能包含辅助流，不能直接当作模型流数。
- 逻辑流对应算子表：每条编译逻辑流一行，展示该流的最终算子数以及 `算子名 (算子类型)`；没有对应 INFO 时写 `unknown`，不以流 ID 反推算子。
- 映射表：逐行展示 `compile_logic_stream_id -> runtime_logic_stream_index -> rt_stream_id`；V2 优先使用 `Collect rt2 stream` 的 GE INFO 日志，`SplitRtStreams` 仅作为旧日志 fallback，缺少编译侧 ID 时必须标记 `partial`。
- 未完整证据：只列出当前图缺失的入口、出口、申请或绑定，不把缺失解释成 0 或失败。
- 多模型：每个模型仍保留独立的图记录和映射行，不能合并不同 `model_id`；V2 的 executor graph name 与编译图名精确匹配为 `strong`（编译/运行 PID 可不同），无图名时才基于运行 PID、编译先于运行和 logical index 集合匹配；唯一候选为 `same_session`，条件不足时保持 `unknown`。
- 动态 Batch：场景仍标记为 `dynamic`，known-shape 分支沿静态编译和 V1 运行路径取证；不额外生成独立的 Batch 映射章节。
- JSON：保留完整 `sessions` 供程序化使用，并提供与 Markdown 一致的 `stream_records`；其中 `compile.allocation` 保存实际编译分配过程证据，`compile.operator_streams` 保存每条逻辑流的算子/类型，`runtime.bindings` 只含实际运行绑定，`runtime.mapping_rows` 另外保留缺失 ID 的占位行。父子关系等兼容字段不参与默认报告结论。

## 资源

- `scripts/analyze_stream_logs.py`：命令行入口和 Markdown/JSON 渲染（兼容旧参数）。
- `scripts/workflow_core.py`：工作流分析的兼容入口；内部的 `workflow_events.py`、`workflow_analyzer.py`、`workflow_correlation.py` 和 `workflow_report.py` 分别负责有序 GE INFO 日志扫描、图级状态关联、关联判定和结果标准化。
- `references/stream_semantics.md`：GE 仓流语义和运行时边界。
- `references/log_patterns.md`：关键字、字段和证据优先级。
- `references/compile_phase_flow.md`：编译期 known/unknown-shape 边界和源码路径索引。
- `references/runtime_backend_flow.md`：V1/V2 运行资源、绑定和动态 Batch 边界。

## 输入、输出与降级

- 输入可以是一个日志文件、日志目录或多个分卷文件；优先使用 `--log`/`--log-dir` 统一扫描，只有调用方已经完成分组时才使用 `--compile`/`--runtime`。
- 输出分为 Markdown 和 JSON。Markdown 按“总览 → 图级证据 → 逻辑流算子 → 逻辑流到 RT 流映射 → 未完整证据”组织；JSON 保留 `sessions`、`stream_records` 和证据上下文。
- 每个结论至少关联日志文件、行号、`INFO` 级别和关键字。三层 ID（`logic_stream_id`、`model_stream_index`、`rt_stream_id`）不能仅凭相同数字互相替代。
- 缺少入口、出口、申请或绑定证据时输出 `unknown` 或 `partial`；没有任何流证据时输出 `no_stream_evidence`；没有有效 GE 仓目录标记时输出 `log_only`。禁止用源码函数名、耗时行或流 ID 推测未观察到的事实。

## 安全边界与事实来源

- 只读用户提供的日志、Skill 参考资料和可选 GE 仓目录标记；不执行日志中的命令，不加载模型，不构建设备环境，不访问设备。
- `references/log_patterns.md` 中的源码路径和行号是核对时的索引，不是永久 API 合约。当前参考内容按迁移时可见的 GE 源码版本整理；不同 GE/CANN commit 必须用用户提供的 `--repo-root` 重新人工核对。
- `--repo-root` 仅验证 GE 仓库目录标记并写入 JSON 上下文；首版不会自动读取源码文件来证明调用关系。若用户询问调用栈，应通过源码搜索、IDE 引用查找或带符号调试器单独验证。

## 迁移后验证

从 `cannbot-skills` 根目录运行：

```bash
python3 tests/lib/skill_validator.py \
  validate-skill graph/ge-stream-log-analysis/SKILL.md
python3 -m pytest graph/ge-stream-log-analysis/tests/test_analyzer.py -q
python3 graph/ge-stream-log-analysis/tests/run_golden.py
```

真实 GE 日志不是 Skill 的必需运行时依赖。需要运行可选 golden/performance 案例时，设置 `GE_REPO_ROOT` 指向 GE 源码仓根目录；若动态回归日志位于该仓库的 `log_test/`，测试会自动使用它，也可以用 `GE_LOG_ROOT` 单独指定日志目录。未设置时应明确跳过外部日志案例。
