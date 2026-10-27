---
name: ascendc-sync-audit
description: Ascend C 信号同步问题检验与修正。检测核内流水线同步（SetFlag/WaitFlag、SyncFunc、PipeBarrier、EnQue/DeQue）、核间同步（CrossCoreSetFlag/WaitFlag、SyncAll、ScalarBar）以及 producer/consumer/sync 数据流图中的 buffer 索引一致性问题。触发关键词：同步、同步问题、SetFlag、WaitFlag、CrossCore、SyncFunc、PipeBarrier、死锁、死等、卡死、hang、数据错乱、半成品、flagId、buffer 索引、output buffer id、producer consumer、核间同步、流水线同步、信号同步、检视同步、检查同步、修正同步、sync。
license: CANN-2.0
permission:
  external_directory: allow
---

# Ascend C 信号同步检验与修正

系统化检验 Ascend C 算子的**信号同步正确性**，并给出修正方案。同步是 Ascend C 算子最高频且「编译期不报错」的隐患来源——异步搬运（MTE2/MTE3）、Cube 计算（M）、Vector 计算（V）之间若无同步，会读到未完成或半成品数据；核间（Cube↔Vec）同步缺失/错序会导致死锁或死等。

## 分析职责

优先使用 analyzer 生成证据，再由 LLM 复核和补跨文件链路：

| 组件 | 职责 | 不该做 |
|------|------|--------|
| `scripts/sync_audit.py` | 生成 Set/Wait 配对、方向、缺同步、下溢、Atomic 等结构性候选 | 不证明复杂数据流等价 |
| `scripts/ascendc_flow_analyzer.py` | 以正则构建数据流图：buffer region 表达式摘要、按行索引别名、buffer access 生命周期、函数内 def-use dependency、producer 输出地址、sync edge、sync coverage；自动补查 SYNC-14； | 不替代完整 C++ 编译器，不证明模板/宏展开后的所有路径 |
| LLM | 发现关联文件、合并脚本候选、复核图证据、追踪被调函数、给出逐行 diff | 不凭直觉否决脚本红线，不用“看起来一致”跳过数据流表 |

## 工作流路由

根据用户意图选择 workflow。无显式意图时默认走 `full-audit`。

| 触发条件 | 工作流 |
|---------|---------|
| 检视同步、检查同步、同步有没有问题、全面检查同步、sync audit | [full-audit](workflows/full-audit.md) |
| 只查 set/wait 配对、set 和 wait 个数是否一致 | [pair-check](workflows/pair-check.md) |
| 卡死/hang/死锁/死等，怀疑是同步导致 | [deadlock-triage](workflows/deadlock-triage.md) |
| 迁移/重构后怀疑残留了多余的同步、单核场景核间同步是否都取消了 | [stale-sync](workflows/stale-sync.md) |

## 执行规则

1. Read 对应 workflow 文件，获取编排定义
2. 发现目标文件的关联头文件/同族文件，按 workflow 要求一并纳入扫描；找不到时在报告中标注能力边界
3. 运行 `scripts/sync_audit.py <目标文件+关联文件> --format json`，保留红线和高级别候选
4. 运行 `scripts/ascendc_flow_analyzer.py <目标文件+关联文件> --format json`，保留图 analyzer 的 `findings` 和关键 `evidence`
5. 若 analyzer 运行失败，不要静默跳过；报告失败原因，并按 workflow 手工执行对应数据流表补查
6. **禁止否决脚本候选**（本规则唯一权威表述，各 workflow 引用以此为准；操作细则见 [full-audit 1b](workflows/full-audit.md)）：脚本输出的红线和高级别候选必须原样呈报给用户，不得以任何理由（包括"同流水保序""框架自动同步""SetFlag 天然等待"等）否决为误报。实测 LLM 在同步判定上会误排除正确候选，造成漏报。脚本不查的标注为能力边界，不自行补充。
7. 对红线+高级别候选给出逐行修改方案（编号展示，等用户选择后执行）
8. **仅在以下情况按需查阅 references**：
   - 同步机制原理不清楚 → [sync-mechanisms.md](references/sync-mechanisms.md)
   - 需要修正代码模板 → [fix-patterns.md](references/fix-patterns.md)
   - 条例细节有疑问 → [sync-checklist.md](references/sync-checklist.md)
9. 涉及具体 API 参数/版本差异时，用 `ascendc-docs-search` skill 核实

## 失败、降级与人工检查点

1. analyzer 全程使用正则 frontend，无需安装任何额外依赖。
3. 关联文件缺失、include 无法定位、宏展开无法还原或模板实例化不完整：在报告中标注“能力边界”，并把相关 SYNC-02/SYNC-05/SYNC-14 结论降级为候选。
4. 脚本红线与 LLM 复核意见冲突：保留脚本红线，追加人工复核说明，不得用主观判断否决脚本候选。
5. 写操作检查点：给出所有修正方案后必须暂停，等待用户确认编号；未经用户确认，不修改目标源码。
6. 范围扩大检查点：需要跨目录扫描、引入新关联文件、或从报告进入修复时，必须在输出中说明范围变化并要求人工确认。
7. 修复后复核检查点：每次写操作完成后运行自测；若验证不通过，报告不通过的命令、错误摘要、降级路径和残余风险。

> **输出要求（重要）**：
> 1. 最终报告必须给出**逐行修改方案**——每个问题编号（(1)(2)(3)...）、标明文件名+精确行号、用 diff 格式（`-`删 `+`增）展示修改前/修改后对比。
> 2. SYNC-14 必须给出 producer→consumer→sync 对比表；若来自 `ascendc_flow_analyzer.py`，同时列出 `expected_root`、`actual_root`、producer operation 或 buffer access、sync edge、sync coverage。
> 3. **列出所有修改方案后不立即执行修改**，向用户提问"要执行哪几号？"，等用户明确选择后只执行选中的修改。增加一层人工判断。
> 4. 修正 diff 出手前必须通过 **API 签名自检**（细则见 [fix-patterns.md「修正 diff API 签名自检」](references/fix-patterns.md)）：`PipeBarrier` 模板参数是 `PIPE_*` 顶层枚举而非 `HardEvent` 成员，diff 中出现 `HardEvent::PIPE_` 即必错；`SetFlag/WaitFlag` 模板参数必须是 `HardEvent::方向`。机制选择优先级 = case_retriever 提示 > 场景规则（一次性初始化用 PipeBarrier、双缓冲重叠用 Flag）> 同族表面风格（同族风格不得推翻机制选择）。

## 检查条例索引

完整条例见 [references/sync-checklist.md](references/sync-checklist.md)。共 14 条，覆盖用户提出的问题 + 补充场景：

| 条例 | 名称 | 严重级别 | 对应关注点 |
|------|------|---------|--------------|
| SYNC-01 | Wait 先于 Set / 先 wait 后 set | 红线 | (1) 先 wait 后 set |
| SYNC-02 | 跨流水数据依赖缺同步（MTE2→V / V→MTE3 / L0C 变化 / 下一轮等 MTE3） | 红线 | (2) 缺少同步（含 L0C、搬入→计算、搬出 GM、下一轮 vector 等 MTE3） |
| SYNC-03 | 核间同步对称性 + 残留同步该取消未取消 | 红线 | (3) 核间同步验证，所有同步是否都取消 |
| SYNC-04 | Set/Wait 个数一致、EVENT_ID/flag 匹配 | 红线 | (4) set 和 wait 个数是否一致 |
| SYNC-05 | HardEvent 方向与数据流匹配 | 红线 | 补充 |
| SYNC-06 | 跨 PIPE 依赖误用 PipeBarrier<PIPE_V> 替代 SetFlag/WaitFlag | 红线 | 补充 |
| SYNC-07 | flagId 复用 ≤15、禁止与 Matmul 高阶 API 混用 | 红线 | 补充 |
| SYNC-08 | 提前 return/break 跳过 SetFlag | 红线 | 补充 |
| SYNC-09 | PipeBarrier 粒度（PIPE_ALL 过粗 / 连续 >3） | 性能 | 补充 |
| SYNC-10 | 双缓冲 loop 下溢（(loop-1)%N, loop=0） | 高 | 补充 |
| SYNC-11 | 同步冗余/混用（EnQue/DeQue 隐式同步处又加 Flag） | 性能 | 补充 |
| SYNC-12 | SyncAll 全核同步必要性与 `<false>` 语义 | 高 | 补充 |
| SYNC-13 | AtomicAdd 乱序：同流水内原子操作语义顺序需 PipeBarrier 保证 | 红线 | 补充 |
| SYNC-14 | 同步信号与 buffer 索引一致性（图 analyzer + LLM 补查） | 红线 | 补充 |

## 资源索引

| 资源 | 路径 | 说明 |
|------|------|------|
| 同步机制全景 | [references/sync-mechanisms.md](references/sync-mechanisms.md) | 6 类同步机制原理、HardEvent 对照表、数据流方向 |
| 检查条例 | [references/sync-checklist.md](references/sync-checklist.md) | SYNC-01~14 逐条：问题、检测、判定、示例 |
| 修正模式 | [references/fix-patterns.md](references/fix-patterns.md) | 每类问题的修正代码模板 |
| 检测范围 | [references/detection-scope.md](references/detection-scope.md) | 能识别的 API、覆盖的数据流场景、已知精度限制、不覆盖场景 |
| 静态分析脚本 | [scripts/sync_audit.py](scripts/sync_audit.py) | 自动扫描 set/wait 配对、方向、缺失同步等 |
| 数据流图 analyzer | [scripts/ascendc_flow_analyzer.py](scripts/ascendc_flow_analyzer.py) | 以正则抽取语句，提取 buffer region 表达式摘要、按行索引别名、buffer access 生命周期、函数内 def-use dependency、producer 地址、同步边、sync coverage，补查 SYNC-14 |
| 历史 case 检索器 | [scripts/case_retriever.py](scripts/case_retriever.py) | 从 333 个真实同步修复 PR 中检索相似 case，为候选自动配对修复模式+diff 证据（sync_audit.py 运行时自动调用） |
| case 数据 | [data/README.md](data/README.md) | `sync_cases.jsonl`（明文 source of truth）+ `sync_cases.db`（build_db.py 重建）+ 来源/schema/修改流程 |

| 示例样例 | [references/examples/](references/examples/) | bad/good/cube/vec kernel 样例；含 SYNC-14 output producer 地址索引与同步索引不同源、SYNC-05 条件分支 PIPE 不匹配（fixpipe+enableRelu）最小坏例 |
| 量化评测（submodule） | tests/eval_recall.py + tests/labels.json | 571 文件 ground truth 量化召回/误报/配对判别，口径固化在脚本 docstring；tests/ 为独立仓 [ascendc-sync-audit-tests](https://gitcode.com/XieQianyi/ascendc-sync-audit-tests) 的子模块（`git submodule update --init --recursive` 拉取），量化基线按需本地记录 |

## 快速使用

```bash
# 全量扫描
python3 scripts/sync_audit.py path/to/kernel.cpp


# 仅 Set/Wait 配对检查（cube+vec 同传以做跨核配对）
python3 scripts/sync_audit.py cube_kernel.cpp vec_kernel.cpp --check pair

# 数据流缺同步启发式
python3 scripts/sync_audit.py path/to/kernel.cpp --check flow

# 数据流图 + SYNC-14 producer/consumer/sync 索引一致性
python3 scripts/ascendc_flow_analyzer.py path/to/kernel.cpp --format text

# JSON 图证据（便于 Agent 合并 findings/evidence）
python3 scripts/ascendc_flow_analyzer.py path/to/kernel.cpp --format json --pretty

# 列出所有同步点
python3 scripts/sync_audit.py path/to/kernel.cpp --list-only

# JSON 输出（便于 Agent 解析）
python3 scripts/sync_audit.py path/to/kernel.cpp --format json
```

退出码：`0`=无红线问题，`1`=存在红线候选，`2`=参数错误。

## 维护自检

修改脚本、workflow 或检查条例后，至少运行：

```bash
# 在 ops/ascendc-sync-audit 下运行
python3 -m py_compile scripts/sync_audit.py scripts/ascendc_flow_analyzer.py scripts/case_retriever.py
python3 scripts/ascendc_flow_analyzer.py references/examples/sync14_output_bundle_index.cpp --format text
python3 scripts/ascendc_flow_analyzer.py references/examples/sync14_same_name_index_rebind.cpp --format text
python3 scripts/ascendc_flow_analyzer.py references/examples/sync14_same_root_different_region.cpp --format text
python3 scripts/ascendc_flow_analyzer.py references/examples/sync14_equivalent_modulo_region.cpp --format text
python3 scripts/sync_audit.py references/examples/bad_sync_kernel.cpp --format json
python3 scripts/sync_audit.py references/examples/sync05_conditional_pipe_wait.cpp --format json  # SYNC-05 跨函数 PIPE 匹配回归锁
python3 tests/eval_recall.py   # 量化基线不应回退（对照 tests/issues.md 表）
# 注：tests/ 语料为独立仓 ascendc-sync-audit-tests 的 git submodule，
#     先执行 git submodule update --init --recursive 拉取，再跑评测；未拉取时可跳过（不影响 Skill 运行）。
python3 data/build_db.py --verify                                    # case 数据 jsonl 与 db 一致

# 在 cannbot-skills 仓库根目录下运行
python3 infra/cannbot-skill-reviewer/scripts/review_skill.py ops/ascendc-sync-audit --json
git diff --check
```

预期：SYNC-14 示例返回非零、`frontends` 显示 `regex` 并包含 `expected_root`/`actual_root`；`sync14_same_name_index_rebind.cpp` 应通过 buffer 生命周期追踪命中同名 `idx` 重新赋义问题；`sync14_same_root_different_region.cpp` 应命中同 root 但不同 buffer region 表达式的高危候选并输出 `buffer_dependencies`；`sync14_equivalent_modulo_region.cpp` 应识别 `idx & 3` 与 `idx % 4` 等价并保持 `findings: 0`；基础 bad 示例至少产生红线候选；`sync05_conditional_pipe_wait.cpp` 应报 1 条 SYNC-05（解析链「变量类型→模板形参→前缀匹配」+ if constexpr 条件双 PIPE wait 修法建议，该检查曾在 v8 因函数体括号双重计数整体失效）。若有真实修复前/后文件，应分别记录 analyzer 命中与修复后清零结果。

### 验证证据记录

- `py_compile` 验证脚本语法；Expected：退出码 0。
- `ascendc_flow_analyzer.py ... --format text` 验证数据流图；Expected：坏例返回 SYNC-14，输出包含 `buffer_accesses`、`buffer_dependencies` 和 `sync_coverages`，修复后真实文件 `findings: 0`。
- `sync_audit.py ... --format json` 验证基础同步规则；Expected：bad 示例至少包含红线候选。
- `review_skill.py ... --json` 验证仓库规范；Expected：无 blocking findings，`verdict` 不为 `REJECT`。
- `git diff --check` 验证补丁格式；Expected：无输出、退出码 0。
- 未执行 `pytest`、`run-tests`、`eval`、`dry_run` 或 `NPU实测` 时，最终报告必须明确说明未验证项和原因。

## 能力边界

- 脚本为**候选生成器**，**禁止否决脚本候选**——红线和高级别候选必须原样呈报，不得以任何理由排除为误报。`ascendc_flow_analyzer.py` 是正则驱动的函数内 buffer 生命周期图，不是完整 C++/AscendC 编译器；暂不覆盖复杂跨文件调用图、模板实例化、宏展开后的真实控制流、完整循环回边证明。
- analyzer 找不到问题不等于证明无问题；报告必须说明已扫描文件、关联文件是否齐全、是否存在未解析宏/模板/跨文件调用。
- **不覆盖**：Tiling 侧、纯 EnQue/DeQue 内存配对（属 `ascendc-api-best-practices` API-6）、HCCL 集合通信时序（属 `mc2-specific`）。

## 信息来源

基于本仓既有可信文档 + CANN 官方文档 + ops-nn/ops-tensor/ops-blas 真实代码全集。涉及 API 参数/版本差异时以 `ascendc-docs-search` 获取的最新官方文档为准。
