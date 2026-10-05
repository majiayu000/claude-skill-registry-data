---
name: decision-gates
description: 在 DSH 长程任务中为决策层加装五道防偏闸门：原始证据锚、对抗式对齐审计、跨包一致性校验、成本比对、防御自检，防止目标漂移、验收失真与摘要偏差。用于跨会话长任务、多 worker 并行、审计类任务、成本敏感任务的 checkpoint 记录与恢复，以及任何需要"决策层不跑偏"保障的执行场景。
version: 0.2.0
triggers:
  - "长程任务 checkpoint / 断点恢复"
  - "多 worker 并行结果验收"
  - "审计类任务成果汇总"
  - "成本敏感派工单"
  - "防御系统自检"
not_for:
  - "单轮小修改"
  - "无需持久化的临时问答"
depends_on:
  - task-mode-router
  - minimal-implementation
---

# 决策闸门（Decision Gates）

## 核心规则

决策层跑偏的根因不是提示词不够强，而是**状态没有物化**：目标只存在于对话里、验收只依赖自述、恢复只信任摘要。决策闸门把防偏从"意志"变成"硬门禁"：

1. **闸门 0 原始证据锚**：checkpoint 必须同时落盘摘要与原始证据锚 JSON；恢复时先读锚、后读摘要，锚里有 SKIP/WARN/PENDING 则"PASS"自动降级为"PARTIAL"。
2. **闸门 1 对抗式对齐审计**：**事件驱动**触发一个**不读摘要**的独立审计 subagent，只给 objective + 原始证据锚 + 产出物，防"自检即跑偏"。触发事件：objective 变更 / 关键假设被证伪 / 不可逆或高风险边界 / 多 worker 结果集成 / 证据相互冲突 / 连续无 Progress Delta / 重大架构决策 / **最终验收（必跑）**。若连续 ≥5 个 checkpoint 无任何触发事件，补一次低成本自检兜底。固定周期计数不再是主要触发方式（防止无行动价值的重复审计）。
3. **闸门 2 跨包一致性校验**：≥2 个 worker 并行时，验收前先跑算法脚本核对文件覆盖重叠/空白/哈希冲突，0 token。
4. **闸门 3 成本比对**：每个派工单记录授权档位与预算，worker 返回时核对实际档位与消耗，0 token。
5. **闸门 4 防御自检**：每 5 个 checkpoint 扫描历史锚，统计摘要比证据乐观的次数（summary_bias），≥2 次判定 DEFENSE_DRIFT 并回退，0 token。
6. **闸门 5 物理范围锁（Scope Lock）**：验收或交付前用 `gate_scope_lock.py` 严格校验变更文件集，任何触碰 Non-Goals 或越界文件直接判 `SCOPE_VIOLATION`，0 token。
7. **闸门 6 轨迹死循环熔断（Deadband Loop Interceptor）**：连续 2 次相同报错/失败模式时通过 `gate_deadband.py` 自动触发 `DEADBAND_TRIPPED`，强制推翻假设并回退，0 token。

**零 token 原则**：闸门 2/3/4/5/6 是纯数据算法逻辑，必须用 `scripts/` 下的 Python 脚本执行，禁止用 LLM 调用替代；这些机械 scope/cost/integrity 检查保持低成本执行，不因事件化而删除。唯一消耗 token 的闸门 1 用最便宜档位的独立 subagent，按上方事件驱动触发。

**验证预算（VERIFICATION_PURPOSE）**：任何验证/审计动作执行前必须能回答：

```text
hypothesis:            要验证什么假设
uncertainty_removed:   通过后消除了什么不确定性
pass_action:           验证通过后的下一动作
fail_action:           验证失败后的下一动作
```

若 `pass_action == fail_action` 且没有新的风险证据，通常**跳过**该验证。验证必须产出 Progress Delta（改变 next action 或 done state），否则视为无进展动作（见 execution-discipline「Progress Delta」）。

## 适用范围与触发边界

**触发**（满足任一即启用本技能）：
- 任务进入长程（预计 >30 分钟或 >50 步），开始建 checkpoint；
- 同一阶段有 ≥2 个 worker 并行产出待验收；
- 审计类任务需要汇总多个 worker 成果；
- 派工单涉及成本预算（授权档位 + token 预算）；
- 会话从 work_memory/checkpoint 恢复，准备继续推进。

**不适用**：
- 单轮小修改、无需持久化的临时问答：不要为它们建 checkpoint 或跑闸门，避免流程过度（经 task-mode-router 判级）。

## 工作流程

### 阶段 1：初始化（首个 checkpoint 前）

1. 用 `create_goal` 锁定原始 objective，逐字拷贝保存。
2. 建立 `checkpoints/` 目录（或沿用 `.agent-broker/topics/<topic>/checkpoints/`）。
3. 从 `templates/raw_evidence_anchors.json` 复制锚模板到 `checkpoints/raw_evidence_anchors.json` 并填写 objective。

### 阶段 2：每个 checkpoint（里程碑完成时）

1. **更新 Todo → 沉淀 work_memory → 校验 Goal**（三位一体同步纪律）。
2. **写原始证据锚**：按 `templates/raw_evidence_anchors.json` 结构记录本阶段的：
   - 执行命令 + 退出码 + 最后 20~30 行日志摘要（物理证据，拒绝口头汇报）；
   - 修改文件 + SHA-256；
   - worker 的 SKIP/WARN/PENDING 登记；
   - alignment_decision（PASS / PARTIAL / FAIL）+ decider_notes。
3. **如果本阶段有多 worker 并行**：先跑闸门 2，结果写入锚，❌ 冲突不得进入验收。
4. **写摘要到 work_memory**：一句话结论 + 指向锚的路径。摘要必须与锚一致，禁止比锚乐观。

### 阶段 3：对抗式对齐审计（事件驱动）

触发事件（满足任一即启动）：objective 变更 / 关键假设被证伪 / 不可逆或高风险边界 / 多 worker 结果集成 / 证据相互冲突 / 连续无 Progress Delta / 重大架构决策 / 最终验收（必跑）。连续 ≥5 个 checkpoint 无事件时补一次低成本自检兜底。

1. 用 `templates/adversarial-audit-brief.md` 生成派工单。
2. 启动独立 subagent（`run_in_background: true`），**只传** objective + 原始证据锚路径 + 产出物列表；**禁止**传任何摘要或 work_memory。
3. 用 `job_output(job_id, wait=true, timeout_ms=60000)` 长轮询收取。
4. 审计结论 ⚠️/❌ 时必须先逐项 resolve 才能推进下一个 checkpoint。

### 阶段 4：成本比对（每个派工单返回时）

1. 派发时在派工单里记 `authorized_tier`、`authorized_model`、`budget_tokens`。
2. 返回时用闸门 3 脚本比对实际档位与消耗。
3. 连续 3 次 COST_DEVIATION → 暂停并审查路由配置（见"安全边界"）。

### 阶段 5：防御自检（每 5 个 checkpoint）

1. 用闸门 4 脚本扫描 `checkpoints/` 下全部锚。
2. bias ≥ 2 → DEFENSE_DRIFT：暂停推进、修正摘要生成规则、回退到最近无 bias 的 checkpoint。

### 阶段 6：恢复（跨会话续接）

1. **先读原始证据锚，后读摘要**（硬顺序）。
2. 锚中有未解决的 SKIP/WARN/PENDING → 摘要里的 PASS 按 PARTIAL 处理，先补完再推进。
3. 恢复完成后沉淀 work_memory："已从 checkpoint cp-N 恢复，未决项：...，下一步：..."。

## 输出契约

- **checkpoint 目录**：`checkpoints/` 下每个阶段一个锚 JSON（`cp-001.json`、`cp-002.json`…）+ 一个工作摘要文件（`summary.md`，可选）。
- **锚 JSON 结构**：严格遵循 `templates/raw_evidence_anchors.json` 的字段：`checkpoint_id`、`objective`、`evidence[]`（type/cmd/exit_code/last_lines | path/sha256 | skipped）、`alignment_decision`、`decider_notes`、`gates_run[]`（gate 名 + 结果）。
- **验收报告**（闸门 1/2/3/4/5/6 输出）必须含：结论（PASS/PARTIAL/FAIL/COST_DEVIATION/DEFENSE_DRIFT/SCOPE_VIOLATION/DEADBAND_TRIPPED）、依据（脚本输出或审计结论）、未决项清单、下一步。

## 验证

1. 运行包内回归：`python scripts/run_tests.py`（标准库，无第三方依赖），覆盖闸门 2/3/4/5/6 脚本的 PASS/FAIL 分支。
2. 校验锚模板可解析：`python -c "import json; json.load(open('templates/raw_evidence_anchors.json', encoding='utf-8'))"`。
3. 对照本技能"工作流程"检查：每个 checkpoint 是否同时落盘摘要 + 锚；恢复顺序是否"先锚后摘要"；闸门 2/3/4 是否由脚本执行而非 LLM。

## 安全边界与非目标

- **不替代 task-mode-router 的规模判级**：小型任务不得因本技能加装流程。
- **不替代人工审批**：对抗审计是独立判定通道，不是绕过 approval 的借口。
- **认证失败时停止并上报**：闸门 3 连续 3 次偏差只触发"审查路由配置"，不自动升级权限、不自动重试绕过。
- **审计 agent 不读摘要**是硬约束：向闸门 1 传摘要等于让审计失效，属于违反本技能。
- **本技能不写任何运行态数据**到发布集；checkpoint 目录属于本地运行态，不纳入 `skills.json` 发布。
