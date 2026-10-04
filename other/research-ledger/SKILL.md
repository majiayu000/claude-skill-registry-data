---
name: research-ledger
description: 研究台账与知识图谱。按当前项目自动定位记忆：维护 projects/<id>/.research/ 下的假设、实验、结果、结论、引用记录；实验矩阵状态机（设计→待跑→运行中→完成→统计）；跨课题共享元记忆在 .research/meta/；跨会话长期迭代的记忆层。触发词：研究台账、实验矩阵、research ledger、更新台账、记录实验、跨会话、项目记忆、共享经验。
metadata:
  short-description: 研究台账/知识图谱与实验矩阵状态机，跨会话记忆。
---

# 研究台账（research-ledger）

维护课题科研记忆，保证跨会话连续性与可追溯性。记忆分两层：

- **项目记忆**：`<workspace>/projects/<id>/.research/`，只属于当前课题；
- **共享元记忆**：`<workspace>/.research/meta/`，跨课题可复用的经验与技巧。

路径一律用 `scripts/project_context.py` 解析，禁止硬编码绝对路径。用户在工作区根目录操作即可：点名课题后用 `--project <id>` 锁定；未点名时按共享模式处理。

## 目录与文件约定

以下文件均位于 `project_memory`（项目 `.research/`）：

- `hypotheses.jsonl`：每行一条假设/idea。字段：`id, created, status(active|tested|rejected|superseded), claim, evidence, links, source`。
- `matrix.md`：实验矩阵（方法 × 数据集 × 指标），每格记录状态；基线格标注策略 `reproduce` / `cite_published` / `excluded`，已有已发表数字的基线默认 `cite_published`（直接采用原文数字、注明来源，不要求同协议、不复现），只有无已发表数字或必须本地跑的方法才 `reproduce`，`excluded` 记录排除原因。
- `experiments/<id>.md`：单个实验记录（目标、配置、命令、结果、复现说明、失败原因）。
- `claims.md`：论文结论级声明，每条链接到实验与引用证据。
- `citations.tsv`：引用清单（key, source, verified, note）。
- `graph/`：记忆图谱（结构化索引，见下方"记忆图谱"节）。`nodes.jsonl` / `edges.jsonl` /
  `candidates.jsonl` / `events.jsonl` 为机器可读本体，`kg.md` 由脚本自动重生成（**勿手改**）。
- `narrative/`：narrative-engine 产出。
- `reviews/`：三轮审查记录。
- `acceptance/`：S6 验收报告（逐条 PASS/FAIL + 证据 + 剩余风险）；全 PASS 前矩阵不得进入 S7。
- `.workflow/state.json`：阶段门禁状态（`gate_pending`、阶段、返工轮数），由 `gate_check.py` 维护；属私有记忆，不提交。

共享元记忆位于 `shared_memory`（`<workspace>/.research/meta/`）：候选经验写 `inbox/`，
确认后转 `lessons/<domain>/`，规范见 `schema.md`；`graph/` 为共享记忆图谱
（经验节点、用户画像、期刊画像、工具/方法规则）；**禁止写入课题私有数据**。

## 实验矩阵状态机

状态流转：`design → pending → running → done → stats`，失败态 `failed`（记录原因后回到 design 或 pending）。

- `design`：S6 冻结矩阵规格；`pending`：S6 验收报告全 PASS 后进入；`running`：S7 的 pilot/调参/配置锁定/canonical 均属此态，只有锁定配置后的 canonical 结果可回写 `done`/`stats`；`failed` 记录原因后回 `design` 或 `pending`。
- 实验协议（数据划分、随机/分层策略、指标、早停、统计口径）由项目定义，S6 冻结时登记在 `matrix.md` 头部（或 `protocol.md`）；S7 运行期间禁止修改协议。
- 调参只在 pilot 折/子集上进行并记录；正式结果只认锁定配置后的 canonical 运行。

- 新建实验：先登记到 `matrix.md`（design），再执行；
- 执行中：experiment-agent / 用户运行实验后更新为 running，并在 `experiments/<id>.md` 记录命令与日志位置；
- 完成：回写结果数值与复现命令（done），随后用 nature-statistics / statistical-analysis 完成统计（stats）；
- 每次会话结束：检查所有 running 状态，未完成的标记进度并留下下一步指令。

## 记忆图谱（graph）

图谱是台账之上的**派生结构化关联索引**：文档仍存全文与事实，图谱只存节点/边/候选/事件，
每条记录带来源指针（provenance）可回溯。记忆分两层：

- 项目图谱：`projects/<id>/.research/graph/`（工作记忆：假设/实验/结论/协议/论文/评审）；
- 共享图谱：`.research/meta/graph/`（经验记忆：lesson / profile_rule / venue /
  tool_fact / method_fact / workflow_rule）。

边类型：`evidence_for`（机械）、`derived_from`（机械）、`complements`（判断）、
`contradicts`（判断）、`supersedes`（判断）、`applies_to` / `informs` / `conflicts_with` /
`refuted_by` / `generated_by` / `decided_in` / `relates_to`。

**确认策略（强制）**：机械边（`evidence_for`、`derived_from`、`generated_by`、
`decided_in`、`relates_to`）由 scan 自动入图；判断边（`contradicts`、`supersedes`、
`complements` 等）只允许生成候选，**必须用户确认**后才入图。任何 LLM 自认为的
`contradicts/supersedes` 都不得直接写 edges.jsonl。

### 常用命令（工作区根目录运行即可，无需切目录）

```bash
# 初始化 / 查看状态
python3 .codex/scripts/graph_evolve.py init --project ser
python3 .codex/scripts/graph_evolve.py status --project ser

# 台账变化后：扫描生成自动节点/机械边 + 候选
python3 .codex/scripts/graph_evolve.py scan --project ser

# 人工确认候选（判断边）
python3 .codex/scripts/graph_evolve.py review --project ser
python3 .codex/scripts/graph_evolve.py review --project ser --accept C-0001,C-0002

# 论文回应矛盾边后标记位置（S9 门禁消费）
python3 .codex/scripts/graph_evolve.py edge respond --project ser \
  --src H-SER-004 --dst 2026H2-2027 --where papers/paperA/main.tex

# 查询
python3 .codex/scripts/graph_evolve.py query --project ser neighbors --node A-E1
python3 .codex/scripts/graph_evolve.py query --project ser contradictions
python3 .codex/scripts/graph_evolve.py query --project ser orphans

# 共享层
python3 .codex/scripts/graph_evolve.py promote --project ser --domain methods \
  --title "..." --scope "..." --body "..."
python3 .codex/scripts/graph_evolve.py feedback add --rule "..." --domain workflow
python3 .codex/scripts/graph_evolve.py profile add --rule "..." --domain workflow
python3 .codex/scripts/graph_evolve.py venue add --name KBS --tier "SCI 1区" --style "..."
python3 .codex/scripts/graph_evolve.py review --shared

# 会话摘要（UserPromptSubmit 钩子自动注入；可手动看）
python3 .codex/scripts/graph_evolve.py digest --project ser
```

### 演化规则

- 新结论与旧假设冲突 → 生成 `contradicts` 候选，保留双方记录（不删除）；
- 新结论补充旧结论 → `complements` 候选；
- 新结论取代旧结论 → `supersedes` 候选，确认后旧节点自动置 `superseded` 并记录
  `meta.superseded_by`（A-MEM 式反向刷新，不是只加新边）；
- 项目收尾/阶段完成 → `promote` 把可复用经验抽象为共享候选（禁止带课题私有数据），
  确认后同时更新 `lessons/<domain>/` 与共享图谱；
- 用户纠正同一规则达到 3 次（N=3，`MTC_FEEDBACK_THRESHOLD` 可调）→ 自动生成画像候选，
  仍须用户确认才生效；与旧规则冲突时旧规则置 retired 并互相引用；
- 定期 `consolidate`：合并重复节点、标记长期未更新节点、重建 `kg.md`，历史一律保留不硬删。

## 会话协议

1. **确定项目**：用户点名课题后运行 `scripts/project_context.py --project <id>`（如“看 ser”→ `--project ser`）；`mode=project` 时只读写该项目 `.research/` + 共享层。用户未点名时运行不带参数的脚本，`mode=shared` 只读写共享层；`mode=outside` 时提示工作区未找到。**不要求用户切换目录。**
2. 会话开始时：读取当前项目图谱摘要（`graph_evolve.py digest --project <id>`，UserPromptSubmit
   钩子已自动注入；未注入时手动读取）+ `matrix.md` + `hypotheses.jsonl`（project 模式），
   或共享 `meta/index.md` + `graph_evolve.py digest --shared`（shared 模式），
   在回复中简要复述当前状态与待确认候选。
3. 会话结束时（或每完成一个实验/结论）：更新对应文件。
   台账被修改后运行 `graph_evolve.py scan --project <id>`；有新矛盾/取代关系时
   生成候选并提醒用户 `review`（判断边不得绕过确认）。
4. 跨项目读取必须由用户显式点名（如“参考 projects/ser 的结论”），只读并标注来源，不并入当前项目记忆。
5. 共享经验沉淀：项目收尾或阶段完成时，运行 `graph_evolve.py promote` 写候选到
   `shared_memory/inbox/`（frontmatter 见 `schema.md`）并生成共享图谱候选；用户确认后
   `review --shared` 转 `lessons/<domain>/` 并置 accepted。
6. 用户询问"我们之前研究到哪了"时，用台账回答，不凭记忆。
7. 新建课题：用户说“新建课题 xxx”时，运行 `scripts/project_context.py --create <id> --title <描述>`，脚本自动创建 `projects/<id>/AGENTS.md`、`.research/` 并注册到 `.codex/projects.json`。

### 用户画像与自进化

- 用户纠正（“不要跑 CNN 基线”“人家报多少就用多少”等）→ `feedback add` 记录；
  同一规则累计 3 次自动生成 `profile_rule` 候选 → 用户确认后成为 active 画像规则，
  每次会话经 digest 注入，直接约束后续行为。
- 投稿期刊 → `venue add` 建期刊画像（层级/风格/模板/审稿口味/经验），确认后入共享图谱。
- 画像规则冲突：新规则确认时旧规则置 `retired`，并在事件日志留痕。

## 阶段门禁（hooks，推荐启用）

- 完成 S2/S3/S4/S5/S5S6/S6/S7/S9/S11/S12/S13 时，先布防门禁：
  `python3 .codex/hooks/gate_check.py --pending --stage <阶段> --project <id>`，
  状态写入 `.research/.workflow/state.json`。
- 项目 `.codex` 层被信任后，Stop 钩子会在每回合结束时自动复检：不合格自动返工（默认最多 3 轮），全部 PASS 才放行；超限停止并请用户决策。
- 手动验收/查看/取消：
  - `--check --stage S6 --project ser`：立即运行门禁并输出报告；
  - `--status --project ser`：查看当前门禁状态；
  - `--reset --project ser`：取消门禁（逃生口，仅在人工判断后使用）。
- 钩子不可用（未信任/桌面端异常）时门禁降级为强流程：进入下一阶段前必须手动 `--check` 拿到 PASS，禁止跳过。
- 门禁只检查流程产物与一致性（如矩阵必须挂到叙事、结论必须可追溯），科学判断仍由用户决定。
