---
name: ge-fusion-pass-skill
description: 触发：用户需要开发、实现、验证或诊断 GE/CANN 自定义融合 pass，或提出融合/拆分子图、GE pass、PatternFusionPass、DecomposePass、graph_base_pass、CANN/GE dump、ATC/pyatc 自定义 pass 时使用；支持端到端流程，也支持明确限定的需求分析、源码实现、功能验证/融合诊断或真实证据后的知识沉淀。默认按 G1→G2→G3 执行，环境或证据不足时如实降级。
---

# GE/CANN 自定义融合 pass

本文件负责阶段路由、门禁、产物交接和操作边界。接口签名、GE 样例、输入 schema、诊断细节和性能口径都在同级 `references/`，按需读取，不在这里复制第二份规则。

> `references/` 各文档中提到的“统一 skill”均指本 skill。

## 阶段路由

| 用户意图 | 执行范围 | 前置条件 | 结束条件 |
|---|---|---|---|
| 未限定阶段的开发任务 | 阶段一 → 阶段二 → 阶段三 | 自然语言需求或输入包 | G3 报告与交付清单 |
| 只分析需求、选 pass 路线或生成需求文档 | 阶段一 | 自然语言需求或输入包 | G1 后停止，不写源码 |
| 已有需求文档，只实现 pass | 阶段二 | `requirements-analysis.md`（路径、摘要文件、完整内容） | G2 后停止，不自动验证 |
| 已有源码/构建命令，只验证或诊断 | 阶段三 | `requirements-analysis.md` 与开发产物 | G3 后停止 |
| 明确要求沉淀新知识 | 阶段四 | 本轮真实验证/诊断证据 | 维护操作结束，不重跑 G1–G3 |

除阶段四外，用户可以一次指定连续的若干阶段，但不能跳过其中一段所需的输入契约。未限定阶段时，按阶段一 → 二 → 三执行。

## 门禁和共用规则

```text
阶段一：需求分析                → G1：gate_status + result_status
  PASS / DEGRADED：传 requirements-analysis.md 路径、摘要文件、完整内容
阶段二：开发                    → G2：gate_status + api_gate_status + implementation_status
  PASS / DEGRADED：传源码、API 签名表、日志点、构建/加载/运行命令
阶段三：功能验证与融合诊断      → G3：gate_status + result_status
  保留每一步 PASSED / FAILED / NOT_RUN、实际命令和证据路径
```

- 每个阶段自行判定门禁；调用方只传递结果，不能重算或编造证据。
- `gate_status` 只描述阶段产物是否足以交给下一阶段或形成报告；它不表示功能成功。`result_status` 描述该阶段的实质结果，取 `PASSED` / `FAILED` / `NOT_RUN`，不得被 `gate_status` 覆盖或省略。
- `DEGRADED` 可以继续，但必须传递假设、未运行原因和未覆盖范围；仅 `BLOCKED` 状态会停止主流程。
- 无法探测的环境记录为“未运行 / 未确认”。不要补写 dump、日志、API 签名或融合成功结论。
- CANN 根只能从 `ASCEND_HOME_PATH`、`ASCEND_OPP_PATH`、`ASCEND_TOOLKIT_HOME` 解析；本 skill 的脚本只能从显式确定的 `$SKILL_ROOT`（包含本 `SKILL.md` 和 `scripts/` 的目录）调用，不能猜测安装路径或把 case 当前目录当作 skill 根。
- 所有随包脚本均通过 `"$SKILL_ROOT/scripts/..."` 调用；`SKILL_ROOT` 为空或目录不完整时，记录相应步骤 `NOT_RUN`，不改用裸 `scripts/...` 路径。
- `CASE_ROOT` 表示从用户输入或开发产物明确解析出的**case 的绝对工作根目录**；`artifacts/` 均位于 `$CASE_ROOT/artifacts/`，它不是 skill 根，也不能由当前目录猜测。
- 源码直接调用的 API 先经 G2 签名核对；验证步骤留下真实状态、命令和证据路径。
- 阶段四不属于默认流水线。不能因为“可能有新知识”自动修改 `references/`；只有用户明确要求知识沉淀时才执行。

### 按需读取 references

| 需要解决的问题 | 先读 |
|---|---|
| pass 选型、语言、注册阶段、开发顺序 | `references/pass-development-paradigm.md` §3–§7 |
| 需求文档的 12 节结构 | `references/requirements-analysis-template.md` |
| 输入包、ONNX/AIR/pbtxt 或最小复现 | `references/input-adaptation.md`、`references/normalized-graph-schema.md` |
| 接口签名、基类、V1/V2 和构图 API | `references/interface-catalog.md` |
| GE 文档、样例和 options 的确切路径 | `references/ge-repo-map.md` §1 |
| 目标片段、边界和 optional 输入 | `references/fragment-spec.md` |
| 验证证据、dump、失败诊断和性能 | `references/validation-evidence.md`、`references/fusion-troubleshooting.md`、`references/performance-analysis.md` |

## 阶段一：需求分析（G1）

输入是一段自然语言需求、一个输入包（如 `data/`、`CMakeLists.txt`、模型、dump、参考路径、交付物），或两者都有。只产出 `requirements-analysis.md`（含摘要文件）；本阶段不创建 `src/*.cpp`、`src/*.py`，不改 `data/`，也不为 API 签名给出未经 G2 核对的最终结论。

### 纯文本请求：直接返回分析

当用户明确要求“只返回文本 / 只做分析 / 不调用工具”，且没有提供 `data/`、模型、dump 或其他输入包时，直接返回结构化需求分析，不进入文件或环境流程：

1. 不调用 `bash`、`read`、`write`、`edit`、`glob`、`grep`、`web` 或其他工具。
2. 不创建 `requirements-analysis.md` 或其他文件；回复包含该文档的结构化摘要、G1 `gate_status`、假设和证据边界。
3. 不启动阶段二或三，不等待用户确认。完成一次文本回复后结束。

用户要求落盘，或提供输入包并允许检查文件时，才进入下面的正常流程。

### 门禁 G1：由本 skill 判定需求分析文档是否可交付

在 `requirements-analysis.md` §12 写入：

```text
gate_status: PASS | DEGRADED | BLOCKED
result_status: PASSED | FAILED | NOT_RUN
missing_fields: []
assumptions_or_limitations: []
evidence: []
artifacts: [requirements-analysis.md, artifacts/handoff/requirements-analysis.sha256]
revision:
  handoff_digest: artifacts/handoff/requirements-analysis.sha256
  produced_at: <产出时间>
```

- 文档定稿后，用 `python3 "$SKILL_ROOT/scripts/write_handoff_digest.py" --input "$CASE_ROOT/requirements-analysis.md" --out "$CASE_ROOT/artifacts/handoff/requirements-analysis.sha256"` 生成摘要文件；它保存**文档字节**的 SHA256，不写回文档本身。文档改动后必须重新生成，阶段二先用同一脚本的 `--check` 核验。
- `PASS`：文档与可核验摘要文件已产出，且 `base 家族 / 具体接口 / 语言` 都有已核实结论，`result_status: PASSED`。
- `DEGRADED`：文档已产出，三个关键字段均有明确取值或“未确认”占位；所有未核实项标为假设、写入 §10，并说明确认方式。摘要文件或部分证据不可获得时相应标 `NOT_RUN`，下游只能按限制继续，不能把假设当事实。
- `BLOCKED`：文档未产出，或任一关键字段既无取值/占位，也无降级说明。仅此状态停止，不进入开发。

调用方只读取 `gate_status`，不重新实现 G1 判定。

### 证据核实、联网与澄清

先查 GE 仓文档和样例，再查用户输入包，最后才提问。输入只给模型或 dump 时，先运行 `python3 "$SKILL_ROOT/scripts/adapt_input.py" detect` 或 `inventory`，取得 `input-inventory.json` 和 `normalized-graph.json`；pbtxt 只能声明结构复现（`structural`），不能声称恢复缺失权重或属性。skill 根未解析时，这一步记 `NOT_RUN`，不从当前目录猜脚本位置。

默认解析 GE 仓根时只读、不联网：

```bash
if [[ -n "${SKILL_ROOT:-}" && -f "$SKILL_ROOT/scripts/sync_ge_repo.sh" ]]; then
  GE_REPO_PATH="$(bash "$SKILL_ROOT/scripts/sync_ge_repo.sh")" || echo "GE 仓不可达 → 按降级规则标注"
else
  echo "skill 根未显式提供 → GE 仓同步未运行，按降级规则标注"
fi
```

只给自然语言且未禁止工具时，最多执行一次上面的离线解析；失败后使用 skill 内 `references/` 并按 G1 降级，不重复调用 `sync_ge_repo.sh`。需要查具体文件或章节时，先读 `references/ge-repo-map.md` §1；接口与枚举以 `references/interface-catalog.md` 为准。

#### 联网授权协议（需要最新 master 证据时）

只有既有 `GE_REPO_PATH` 或缓存不足、且确实需要最新 `master` 时才申请联网。先在一轮回复中交代：刷新还是克隆、远端 URL（默认 `https://gitcode.com/cann/ge.git`，可由 `GE_REPO_URL` 覆盖）、所需证据、目标缓存目录 `$GE_REPO_CACHE_DIR`、用户自行 `git pull` 后设置 `GE_REPO_PATH` 的只读替代方案，以及拒绝授权后的降级范围。得到明确授权后才运行：

```bash
GE_REPO_PATH="$(bash "$SKILL_ROOT/scripts/sync_ge_repo.sh" --allow-network)" \
  || echo "联网刷新/克隆失败 → 回退旧缓存或按降级规则标注"
```

将 stderr 中的 `GE_REPO_ACCESS: ...` 行或 `$GE_REPO_ACCESS_LOG` 日志作为证据记录。用户拒绝或未响应时，不执行 `clone` / `fetch`，将限制写入文档 §10 并标 `【假设，待确认】`。复用用户本地仓时只读，不执行 `fetch`、`reset` 或清理，也不改其工作树、分支或 revision。

只问会改变关键字段、且无法从证据推断的问题。一次最多问 3 个；每个问题说明影响的字段、候选答案和不回答时的默认假设。用户无法回答时按默认假设继续，并在 §10 记录原因、确认方式和暂行处理。

### 目标片段与路线选择

在文档 §3 写清六项：导入后真实 GE op type、可选定位、输入/输出边界、守卫、可选算子和目标形态。op type 以 dump 为准，不以框架算子名猜测；替换后仍被外部使用的 Tensor 要声明为 pattern 输出。大网络的定位方式和 S1/S2/S3 optional 输入策略见 `references/fragment-spec.md`。

选型先受可表达性约束，再看对外接口、参考路径和交付物。三者冲突时以对外接口为准，并在 §5.3 记录被否决方案；对外接口缺失且证据不足时标“接口未确认”，按默认假设继续。

| 条件 | 路线与需要记录的结论 |
|---|---|
| 控制边、嵌套子图、动态输入/输出、边界不能表达、运行期节点数 N 可变，或只做全图属性/边修改 | `graph_base_pass`；选择函数式 graph pass 或 `FusionBasePass`，说明原因 |
| 固定数据拓扑的一段子图 → 另一结构 | `PatternFusionPass`；记录 pattern 数量、输出、捕获和守卫 |
| 单个算子按属性展开为多个算子 | `DecomposePass`；记录 `op_types` |
| optional 输入形态有限 | S1 只支持一种并显式拒绝，或 S2 每种形态一个 pattern；组合过多则 S3 回到 graph 路线 |
| 钩子内需要读 option 或写 error msg | pattern/decompose 用 V2（`PatternFusionPassV2` / `DecomposePassV2`，CANN ≥ 9.1.0）；V1 钩子没有 `CustomPassContext` |

语言由交付物和加载方式决定：`src/*.cpp` + CMake + `.so` + `REG_*` 宏用 C++，经已验证的 `<OPP_ROOT>/vendors/<vendor>/custom_fusion_passes/` 加载，`atc` 触发；`src/*.py` + `ASCEND_GE_PY_PASS_PATH` + 注册装饰器用 Python，必须用同进程的 `pyatc`。注册阶段是 `.Stage(...)` / `stage=...` 参数，不是编译 option：不依赖 shape 时优先 `kBeforeInferShape`；依赖真实 shape、通道、`groups` 或 `data_format` 时用 `kAfterInferShape` 并保证 replacement 的 shape 连续性；`kAfterOriginGraphOptimize` 需 CANN ≥ 9.0.0；普通融合 pass 不用 `kAfterAssignLogicStream`。开关读取 `GetOptionValue` / `get_option_value` 需 CANN ≥ 9.0.0，并写明 key 缺失时的默认行为。

### 写入需求文档并交接

按 `references/requirements-analysis-template.md` 生成 12 节文档：§3 放片段六要素，§4 放预期图变换，§5.1 放 pattern 可表达性，§5.2/§6/§7 放路线、接口、语言、阶段、边界和 optional 输入，§8 放开关、加载和环境，§9 放验证方案，§10 放假设和限制，§12 放 G1、证据和 revision。`gate_status` 为 `PASS` 或 `DEGRADED` 时，将文档路径、摘要文件路径和完整内容交给阶段二；`BLOCKED` 时报告缺失项并停止。

## 阶段二：开发（G2）

输入是阶段一传来的 `requirements-analysis.md`（路径、摘要文件和完整内容）。先运行 `python3 "$SKILL_ROOT/scripts/write_handoff_digest.py" --input "$CASE_ROOT/requirements-analysis.md" --out "$CASE_ROOT/artifacts/handoff/requirements-analysis.sha256" --check`；摘要不匹配时记录证据并回到阶段一，不能按旧文档继续写代码。输出为 `src/*.cpp` 或 `src/*.py`，以及构建、加载、运行命令说明。

### 门禁 G2：先核对 API 签名，再写代码

创建或修改任何 `src/*.cpp|*.py` 前，列出本 case 直接调用的全部 GE/ES API，并完成签名核对表。字段和降级条款见 `references/tips/api-signature-gate.md`。签名证据优先来自 `$GE_REPO_PATH/docs` 和现场 ES API 清单；文档缺失、冲突或需确认重载时才查 CANN 头文件。此阶段不自行联网；需要刷新仓证据时回到阶段一的「联网授权协议」。

```text
gate_status: PASS | DEGRADED | BLOCKED
api_gate_status: PASS | DEGRADED | BLOCKED
implementation_status: PASSED | FAILED | NOT_RUN
result_status: PASSED | FAILED | NOT_RUN  # 必须与 implementation_status 一致
missing_fields: []
assumptions_or_limitations: []
evidence: []
artifacts: [API 签名核对表, src/ 下新增源文件]
```

- `api_gate_status: PASS`：每个直接调用的 API 都有核对表行和文档、头文件或现场 probe 证据；`DEGRADED`：每个 API 都有核对表行，但至少一项明确标为 `【签名未核实，假设 X，待确认】`；`BLOCKED`：任一直接调用的 API 缺核对表行，或签名不确定却未标假设，此时不能创建或修改源码。
- `implementation_status: PASSED`：新增源码存在，并逐项覆盖需求文档中承诺的匹配、边界、守卫、replacement、注册和日志；`FAILED`：源码存在但已知不完整、与需求冲突或只能提供占位实现，必须列明缺口；`NOT_RUN`：因 API 门禁 `BLOCKED` 或无写码授权而没有源码。
- `gate_status: PASS`：摘要文件已核验、API 门禁为 `PASS`、源码和交接信息齐全且实现为 `PASSED`；`DEGRADED`：源码可交给阶段三诊断，但 API 或实现有显式限制/失败；`BLOCKED`：摘要不匹配、API 门禁阻断，或没有足以制定验证计划的源码产物。

调用方只读取 `gate_status`，不重新判定 G2。

### 实现规则

先查 `references/example-map.md`，用最接近的真实 GE 样例确定骨架、日志点和注册阶段；匹配对象换成本 case dump 中的真实 op type，不沿用样例节点名。严格按需求文档 §3 实现匹配、边界、守卫、optional 输入和 replacement。只在 `src/` 新增源文件；除非 §11 明确要求，不改顶层 `CMakeLists.txt`、`data/` 或 `gen_es_api/`。需要最小复现时使用 `artifacts/repro/`，不覆盖用户已有 `data/`。

| 已选路线 | 实现边界 |
|---|---|
| 函数式 graph pass | `REGISTER_CUSTOM_PASS(...).CustomPassFn(...)`，回调为 `Status(GraphPtr &, CustomPassContext &)`；遍历 `Graph/GNode`，不实现 `Patterns()` / `Replacement()` / `MeetRequirements()` |
| `FusionBasePass` | 先用 `Graph/GNode` 扫图、ES API 构 replacement graph、`SubgraphBoundary` / `SubgraphRewriter::Replace`；只有文档和编译/ATC 证据表明不可行时才直接改边删点 |
| `PatternFusionPass` / `DecomposePass` | 按文档 §5.2 的接口实现，不能混用其他 base 家族的回调模型 |

pattern 代码要满足：外部输入都用占位符声明；所有被外部使用的输出都声明为 pattern 输出；每个普通算子的输入个数与真实图一致；多 op type 变体或 optional 输入形态建多个 pattern；控制边、嵌套子图和动态 I/O 出现时回到 graph 路线。Python 的 `@pattern` 与 `patterns()` 互斥；需要读取中间 Tensor 时用 `create_pattern(...)` + `capture_tensor(...)`，不要用 `@pattern`；`PatternFusionPass` / `DecomposePass` 不得重写 `run()`。对于 Python `FusionBasePass`，`run()` 成功应返回 `True` 或 `None`，不能照搬 C++ 的 `return 0`。

新节点默认使用 `es_all` wrapper，不预换版本名；只有真实出现 `Failed to select engine` 才回退等价实现。format-sensitive 的 Conv/Pool 输入显式设置 NCHW/NHWC；C++ 推 shape 只用 `InferShapeUtil::InferShape`；框架类使用 `ge::fusion`；其余命名、IR 顺序、Python 节点生命周期和失败归因按 `references/pass-development-paradigm.md` §7 与对应 `references/tips/` 执行。

关键分支用 `std::cout << ... << std::endl;`（C++）或 `print(...)`（Python）写 stdout，而非只依赖 GE 日志宏。每个 pass 至少记录 begin/end、pattern/capture、守卫命中或跳过原因、replacement、InferShape 和 skip reason；日志带 pass 名和阶段，便于阶段三从 `run.log` 检索。

### 输出

输出 G2 门禁块、API 签名核对表、新增源文件路径、日志点，以及构建、加载和运行命令。即使 `gate_status: PASS`，也必须显式交接 `implementation_status`；阶段三据此区分“可诊断的失败实现”和“已实现”。`PASS` 或 `DEGRADED` 时，将这些内容和需求文档路径交给阶段三；`BLOCKED` 时不写源码并停止。

## 阶段三：功能验证与融合诊断（G3）

输入是开发产物和 `requirements-analysis.md`。输出为验证报告和交付检查清单。性能默认只做图层收益核对，不把 ATC/pyatc 编译成功误作融合命中、功能正确或端到端性能结论。

### 门禁 G3：环境不可用时如实降级

先探测 CANN 根和 `atc` / `pyatc`、skill 根、完整 soc version、ES API、只读 `$GE_REPO_PATH`、Python bridge / TorchAir / TensorFlow / custom-op runtime。skill 根和 case 根均解析成功时，先运行 `mkdir -p "$CASE_ROOT/artifacts"`、`bash "$SKILL_ROOT/scripts/check_env.sh" | tee "$CASE_ROOT/artifacts/check-env.log"`，再按 case 路线运行 `python3 "$SKILL_ROOT/scripts/check_runtime.py" --mode <python-pass|tf1|custom-op> --out-json "$CASE_ROOT/artifacts/runtime-probe.json"`；两份产物是 G3 第一步的环境证据。skill 根或 case 根缺失时，依赖 skill 脚本的步骤标“未运行”，不把当前目录当作任一根目录。soc version 通过 `bash "$SKILL_ROOT/scripts/detect_soc_version.sh"` 取得完整值；例如 `Ascend910_93` 只是 short family，ATC 需要 `Ascend910_9362` 这样的完整值。缺失项逐条写成“缺 X → 跳过 Y 步”，其余可执行步骤继续运行。

每个适用步骤记录 `status: PASSED | FAILED | NOT_RUN`、实际命令、证据路径和原因；语言或路径不适用的步骤可记 `N/A`，不计作 `NOT_RUN`。阶段末尾输出：

```text
gate_status: PASS | DEGRADED | BLOCKED
result_status: PASSED | FAILED | NOT_RUN
missing_fields: []
assumptions_or_limitations: []
evidence: []
artifacts: [验证报告, 交付检查清单, artifacts/case-matrix.json]
```

- `result_status: PASSED`：全部适用步骤为 `PASSED`；`FAILED`：至少一个适用步骤为 `FAILED`；`NOT_RUN`：没有 `FAILED`，但至少一个适用步骤为 `NOT_RUN`。`N/A` 不计入聚合。
- `PASS`：输入足以制定计划，所有适用步骤均已实际执行；此时 `result_status` 可以为 `PASSED` 或 `FAILED`，但失败必须有真实日志。
- `DEGRADED`：输入完整，但至少一个适用步骤因环境缺失或前置失败而 `NOT_RUN`；仍交付报告和清单，并明确未覆盖范围。
- `BLOCKED`：需求文档或开发产物缺失到无法制定验证计划。环境缺失本身属于 `DEGRADED`，不是 `BLOCKED`。

编排 agent 只读取 `gate_status`，不改写步骤状态或证据。

### 验证顺序与证据

1. 构建、加载前隔离本轮产物：只清理当前 case 根的本轮 `build/` 产物；共享 C++ vendor 目录默认只读。安装、覆盖或移除 case 根外的一项前，记录精确源/目标路径并取得用户确认。无法证明加载集合隔离时，报告“加载基线未确认”。
2. 运行 `cmake -S . -B build`；C++ case 再按可用并行度运行 `cmake --build build -j<N>`。无 CANN run 包造成的失败如实记录。
3. 按需检查 ES API：内置算子检查 `es_all` 的头、库和 Python `import ge.es`；缺失时先运行 `bash "$SKILL_ROOT/scripts/gen_es_all.sh"`。只有自定义算子 case 才运行 `bash "$SKILL_ROOT/scripts/gen_es_api.sh" "$CASE_ROOT"` 构建 `es_custom`，随后用步骤 1 的 `check_runtime.py --require-es-custom` 核验真实加载能力。
4. Python pass 将 `ASCEND_GE_PY_PASS_PATH` 精确指向本次 `.py`，在 GE 初始化前设置；内置 ES API 再设置 `PYTHONPATH=$GE_ES_API_PYTHONPATH` 和 `LD_LIBRARY_PATH=$GE_ES_API_LIB_DIR`。
5. 环境可用时触发 GE 编译：设 `DUMP_GE_GRAPH=1`，必要时设 `DUMP_GRAPH_LEVEL=1`；C++ 用 `atc`，Python 用 `pyatc`，并用 `<atc/pyatc/在线脚本> 2>&1 | tee run.log` 保存 stdout。按 `references/input-adaptation.md` 分流：ONNX 用 `atc --framework=5`；AIR 的 C++ 用 `atc --mode=0 --framework=1`，Python 用 `pyatc`；pbtxt 先 `repro`，仅结构同构 `PASSED` 后再编译。
6. 真实 baseline/optimized 产物齐备时，用 `python3 "$SKILL_ROOT/scripts/validate_evidence.py"` 运行 `events`、`normalize`、`graph`、`outputs`、可选 `performance` 和 `report`。需要整网输出/性能时，按 `references/validation-evidence.md` 先用 `python3 "$SKILL_ROOT/scripts/run_om.py"` 为 baseline 和 optimized 各生成 manifest。每个用户 case 只生成一条 `artifacts/case-matrix.json`，记录 case id、适用步骤及其 `PASSED` / `FAILED` / `NOT_RUN`、命令和证据路径。缺输入时保留 `NOT_RUN`，不能用 fixture 或编译成功替代真实图、输出或性能结论。

单个 case 的 matrix 的最小结构见 `references/validation-evidence.md` §一：`cases` 必须恰有一个元素，逐步骤保留状态、实际命令、证据路径和失败/未运行原因。它是 G3 `result_status` 的唯一聚合输入。

先根据注册阶段找正确 dump 文件：

| 注册阶段 | 优化前 | 自定义 pass 后 |
|---|---|---|
| `kBeforeInferShape`（含 CANN ≥ 8.3.RC1 的函数式 graph pass） | `ge_onnx_*_PreRunBegin.pbtxt` | `ge_onnx_*_RunCustomPassBeforeInferShape.pbtxt` |
| `kAfterInferShape` | 同上 | `ge_onnx_*_RunCustomPass_AfterInferShape.pbtxt` |
| `kAfterOriginGraphOptimize` | 同上 | `*_RunCustomPassAfterOriginGraphOptimize*` |
| CANN < 8.3.RC1 的函数式 graph pass | `ge_onnx_*_RunCustomPassBegin.pbtxt` | `ge_onnx_*_RunCustomPassEnd.pbtxt` |

使用 `ls | grep -i runcustompass` 查找大小写和 `.txt` 变体；自定义阶段 dump 缺失时检查 `DUMP_GRAPH_LEVEL`。`run.log` 应能找到阶段二约定的 stdout 日志；完全没有 pass 日志通常说明没有加载或触发。

### 诊断、性能与交付

诊断按“是否加载 → 是否执行 → 是否命中”排序，避免把未加载误判为 pattern 写错：

| 现象 | 优先检查 |
|---|---|
| 无 pass 日志 | C++ `.so` 是否位于已验证加载根、注册宏/阶段；Python 的 `ASCEND_GE_PY_PASS_PATH`、`.py` 后缀、初始化时机和 `pyatc` |
| Python 已 import 但不执行 | 注册装饰器、`stage`、全局唯一 `name` |
| 静默不命中或 skip | dump 的真实 op type、optional 输入的实际个数、pattern 输入/输出边界、`MeetRequirements` 日志 |
| Python `run()` 失败 | 是否返回 `0` 或 `False`；成功应为 `True` / `None` |
| `Failed to select engine` | 按报错算子走 `es-all-no-version-rename.md` 的等价实现回退，不预换版本名 |
| `Not_Supported_Format` / `E50002` | format 是否显式设置；见 `format-sensitive-nchw.md` |
| IR 顺序、replacement 或 shape 失败 | `REG_OP` 顺序、`InferShapeUtil::InferShape`、`fusion-troubleshooting.md` 对应节点 |

失败时先按报错读对应 tip 的“自查”清单。确认环境缺失后才标“未运行”，不要把漏设 format、使用框架名或残留旧 pass 归因给环境或文档。

默认 L0：对照需求文档 §4，核对替换前后的算子数、中间 tensor、`TransData` / `Transpose` / `Cast` 等变化。decompose 的节点数上升可能是预期；L0 不需要 NPU。用户明确要求“详细性能分析 / profiling / msprof”时才运行 L1：在同一输入、同一 soc 下比较 baseline（pass 未生效）和 optimized（pass 生效）的 `msprof` 数据；NPU 或 msprof 不可用时标“未运行”，保留 L0。

交付清单至少包含 G3 门禁和逐步骤状态、覆盖的优化意图、新增源文件、构建/ES/Python 加载结果、ATC/pyatc 或在线脚本结果、dump 与日志结论、不命中/失败日志、所用 `es_all` wrapper 或等价回退、format 证据，以及 `PreRunBegin` 中确认的真实 op type。真实 case 结束后，用户明确要求时才进入阶段四。

## 阶段四：知识沉淀（显式维护操作）

仅在 case 结束后、用户明确要求时执行。输入是本轮验证报告、融合诊断、报错和日志关键字、最终修法，以及文档或头文件证据路径。目标是记录 `references/` 尚未覆盖、且已经核实的新知识；它不改变本次开发交付物。

### 触发和证据规则

适合沉淀的内容包括：新失败现象及已验证修法、经真实文档或头文件确认的 API 签名要点、尚未记录的场景↔GE 样例映射。先检索 `references/tips/*`、`interface-catalog.md`、`example-map.md` 和 `knowledge-base.md`；已覆盖的不重复创建，既有 tip 的补充优先追加到原 tip。

每条结论先核实：枚举、继承、函数签名和 `@since` 以 `$GE_REPO_PATH/inc/**` 头文件为准；行为和返回值以 `docs/zh/` 与 `examples/fusion_pass/` 为准；dump 图名和日志文案以样例 README 加实测为准。证据写到文档路径+章节、头文件+行号、dump 片段或复现命令。取不到证时标“假设+待确认”并写入当前 case 的 `requirements-analysis.md` §10；不能把未证实内容沉淀进 `references/`，更不能伪造 dump、日志或结论。

### 工作步骤

1. 用 `rg` 判重。
2. 按内容归类：开发流程导航更新 `pass-development-paradigm.md`；诊断树更新 `fusion-troubleshooting.md`；签名/枚举更新 `interface-catalog.md`；场景↔样例更新 `example-map.md`；仅在现有主题均不覆盖时新建 `references/tips/<kebab-slug>.md`。
3. 新 tip 保持现有骨架：`# tip: 标题`、导航落点、`**读者**`、`症状`、`根因`、`硬性做法`、`自查`；一条 tip 只处理一个关注点。新导航落点同步更新 `references/tips/MIGRATION.md`。需要新增 skill 索引行或宿主校验规则时，先作为提议交给用户确认。
4. 不改写既有正文；可添加交叉链接。只有既有正文与 GE 一手资料发生事实冲突时，核实后直接修正，并在输出中单列“事实性修正”。保持宿主中立，不写评测协议、绝对路径或环境注入假设。
5. 运行宿主仓库提供的 skill 结构校验，并报告实际命令与结果。

输出判重结论、新增或改动文件、每条证据来源，以及尚待用户确认的提议。未经确认的提议不落地。
