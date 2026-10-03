---
name: analysis-delivery-workflow
description: 严守 9 阶段流程(分析-设计)— 适合新手/复杂项目,按顺序自动调 9 个 user-invoked skill。希望按完整结构化流程、逐步推进且不需每步自行决策时调用本编排。
disable-model-invocation: true
version: 4.0.0

---

# Analysis to Delivery Workflow — 9 阶段流程编排

## Contract

- 输入: 项目目标、领域、技术栈,可选既有 `paths/*.md`
- 输出: 9 阶段交付链,终点为 `HANDOVER.md`
- 门控: 每阶段间 stage-gate 签字;`task-confirm-check.py --strict` 用于 2→3;QA P0=0 才能 8→9
- Required rules: `stage-gate`, `doc-numbering`, `context-pointer`, `goal-boundary`
- Required paths: `knowledge-path`, `tech-stack-path`, `compliance-path`, `doc-naming-path`
- 下一步: 先 `/setup-analysis-delivery`,再按顺序走 9 阶段;阶段 9 之后可选 `/using-superpowers`

## 适用场景

- 复杂项目(中等+)
- 新手第一次用
- 严守流程纪律,避免跳步

## 9 阶段(按顺序触发)

| # | 阶段 | 调用的 skill | 产出 |
|---|---|---|---|
| 1 | 项目配置 | `/setup-analysis-delivery` | 4 个 `*-path.md` |
| 2 | 需求澄清 | `/grill-task` | TASK_CONFIRM + 字段对齐 |
| 3 | BRD | `/to-brd` | 01-BRD + 流程图 |
| 4 | 合规评审 | `/compliance-review` | 04-合规评审 |
| 5 | 测试用例 | `/test-case-design` | 07-测试用例 |
| 6 | PRD | `/to-prd` | 05-PRD(三格式) |
| 7 | 开发设计 | `/dev-design` | AGENTS + FSD + 数据模型 + 开发设计 + 回测 + 复盘 |
| 8 | QA 审计 | `/qa-audit` | 09-QA 审计报告 |
| 9 | 交接 | `/handoff` | HANDOVER.md |

## 衔接 superpowers 实施(阶段 9 之后)

**设计交接完成后,推荐进入 `/using-superpowers` 走 5 步实施**:

```
brainstorming → design-an-interface → domain-modeling → writing-plans → tdd → executing-plans → verification-before-completion
```

| 实施步骤 | 产出 |
|---|---|
| brainstorming | 设计稿 |
| design-an-interface | 接口契约 |
| domain-modeling | 领域模型 |
| writing-plans | ≤ 2h 子任务列表 |
| tdd | RED → GREEN → REFACTOR |
| executing-plans | 逐步开发 + commit |
| verification-before-completion | 完成前验证 |

## 门控(贯穿)

每阶段必签字才能进入下一阶段。详细见 `disciplines/stage-gate` 3 层门控:

- **第 1 层**:9 阶段之间 → 用户签字
- **第 2 层**:实施子流程之间 → 用户 + Claude 双向
- **第 3 层**:每个 writing-plans 子任务 → 测试 + 用户抽查

## 关键纪律

- **严禁自动推进**：本编排"按顺序触发"9 个 skill，但每阶段产物必须经用户显式签字（白名单话术）后才能进入下一阶段。LLM 不得自行解释"OK""继续""好"等模糊回复为签字。
- 严禁跳阶段(从 1 跳 3 / 从 5 跳 7)
- 每阶段产物必须签字
- HARD GATE:阶段 7 设计回测 ❌ 禁入阶段 8
- HARD GATE:阶段 8 QA 审计 P0>0 禁入阶段 9

## 2→3 门控（2026-06-24 强化）

阶段 2 → 阶段 3 之间，必须同时满足：

1. TASK_CONFIRM 状态 = ✅
2. REVIEW 文档中 ❓=0 且 🔴=0
3. 用户白名单话术签字（详见 `skills/disciplines/stage-gate/SKILL.md`）

详见 `scripts/task-confirm-check.py` 自动化校验。

## 状态文件(plan §P1-3,v4.0.0)

每个项目根维护 `.analysis-delivery-state.json`(加入 `.gitignore`),5 个子命令:

```bash
# 初始化(项目级)
python3 scripts/analysis-state.py init --project <name> [--project-root .] [--force]

# 记录 gate 脚本结果(pass/fail 会自动 +1 拦截次数)
python3 scripts/analysis-state.py record-gate --stage N --script <gate> --result pass|fail

# 记录阶段签字(只接受 4 句白名单之一,其他一律 reject)
python3 scripts/analysis-state.py signoff --stage N --text "我已全部确认,可以进入下一步"

# 查看当前状态(9 阶段进度 + last_gate + errors)
python3 scripts/analysis-state.py status

# 5 项度量指标(total_gates / total_signoffs / 拦截次数 / 重试次数 / 阶段用时)
python3 scripts/analysis-state.py metrics [--json]
```

**白名单话术(只 4 句)**:
- "我已全部确认,可以进入下一步"
- "确认通过"
- "全部完成,继续"
- "approved, proceed to next stage"

❌ "OK / 好 / 继续 / 确认" 一律视为非签字。

**中断恢复**:状态文件在 `.gitignore`,存在本地;下次开会话时跑 `status` 即可看到当前阶段、已签字阶段、错误计数。

## 调用的 rule

- `rules/stage-gate` — 3 层门控
- `rules/no-field-guessing` — 字段名
- `rules/doc-numbering` — 文档编号

## 结束条件

- [ ] 9 阶段全部签字
- [ ] HANDOVER.md 已生成
- [ ] 已交接给编码 skill 或开发团队
