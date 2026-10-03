---
name: agile-sprint
slug: agile-sprint
displayName: Sprint规划
description: |
  当用户说"开 Sprint""规划迭代""关闭 Sprint"或 using-agile 路由到此，且 PRODUCT-BACKLOG.md 已有条目时触发。
agent_created: true
version: 5.0.0
dependencies:
  - skill: using-agile
    reason: 提供 DOD.md 模板
  - skill: agile-backlog
    reason: PRODUCT-BACKLOG.md 是 Sprint 取条目的来源
---

# Sprint 规划 (Agile Sprint)

## 0. 前置条件（缺失则路由回退）

| 条件 | 缺失时路由 |
|------|-----------|
| `agile-docs/PRODUCT-BACKLOG.md` 存在且 ≥1 条目 | → agile-backlog |
| `agile-docs/DOD.md` 存在 | → using-agile 补 DoD 模板 |

**条目来源硬约束**：Sprint 任务清单必须从 `PRODUCT-BACKLOG.md` 阶段表按 priority 取顶部条目。条目须经 `agile-backlog` 流程产出并写入阶段表；**口头/临时任务清单不能直接进入 Sprint**。若用户跳过 agile-backlog 给临时清单且坚持不回退，按渐进式节奏停下提示风险（`using-agile/references/gate-protocol.md §四`），由用户显式确认是否仍要回 agile-backlog 走正规流程。

## 1. 定位

本技能只做 **Sprint 规划与关闭**，不涉执行态。Sprint 文件是规范层向执行层的单向交付，消费 Agent 拿到后自行细化与追踪。本技能不记录 checkbox 进度、不处理执行中变更。

**产出单一文件**：`sprints/sprint-{序号:03d}-{日期}.md`，含规划信息与闭环检查。

**Sprint 闭环即止**——不做战略层反向回流。若执行中发现需要改愿景/架构/ADR，引用 `using-agile/references/change-matrix.md` 评估影响面后，由用户主动调用对应战略技能。

⚠️ **执行阶段（任务拆解、进度追踪、阻塞处理）归消费 Agent 负责，不在本技能能力范围内。**

## 2. 写前对齐（先问询，再产出；选择题）

姿态遵循 `using-agile/references/probing-protocol.md`（一次一问，含糊必追问）；需要你拍板的决策点用「候选 + 推荐 + 自定义」选择题问。

- 确认取哪些 PRODUCT-BACKLOG.md 阶段表顶部条目（按 priority 排序）
- **Sprint 目标反问**：取完候选条目后，先向用户确认"这 {N} 条能否支撑一个可陈述的 Sprint 目标？用一句话说是什么？"——目标说不出来 → 建议调整取用条目（换入/换出由用户裁决），不开"杂项堆" Sprint
- **技术任务（T-NNN）需关联 ADR 章节编号**；若关联缺失，按 `using-agile/references/gate-protocol.md §二 ①` 拦截，先回 agile-strategic 阶段 B 补 ADR
- **容量参数必问**：团队人数 / Sprint 工作日 / 团队成熟度（决定专注系数）——三者任一未知就问（可先读 `agile-docs/DOD.md` 头部项目画像取团队人数），**禁止静默按 0.6 默认**；专注系数给选项 + 推荐（A 0.5 新团队 / B 0.6 成熟 / C 0.7-0.75 全职专注），确认后使用并在 Sprint 文件中标注"agent 推荐"
- **容量检查**：point 直接读阶段表「点」列（单文件，priority/point 同表），计算承诺点是否 ≤ 可用点。可用点计算见 `references/sprint-rules.md §一`
- 确认本 Sprint 序号：扫描 `sprints/` 目录下已有 `sprint-NNN-*.md`，取最大序号 +1；目录为空则从 001 起（用于命名 `sprint-{序号:03d}-{日期}.md`）
- 确认起始日期（用于命名）
- **交接点识别**：多仓库项目读阶段表「仓库」列取条目的仓库归属；识别跨仓库依赖组（不同仓库 + 先后开发关系，如 `api-server` 后端接口 → `web-app` 前端页面）→ 规划时生成「交接契约」段；无跨仓库依赖 → 跳过（判定与契约段模板见 `references/sprint-template.md` §交接契约，交接文档模板见 `references/handoff-template.md`）
- 确认 DoD（读 `agile-docs/DOD.md`，若缺失回 using-agile 补）

## 3. 产出（按环节，每环节写完即停）

### 环节 A：规划
- 从 `agile-docs/PRODUCT-BACKLOG.md` 阶段表按 priority 取顶部条目（经 §2 Sprint 目标反问确认），point 与仓库归属同表读取
- **生成「交接契约」段**：§2 识别出跨仓库依赖组时，按 `references/sprint-template.md` 交接契约模板生成（交接点 / 上游任务 / 下游任务 / 交接文档位置）；无跨仓库依赖 → 不生成
- 在 `sprints/` 下新建 `sprint-{序号:03d}-{日期}.md`
- 按模板（`references/sprint-template.md`）填写：周期/目标/容量/任务清单（纯列表，多仓库条目标注 `[repo: xxx]`）/**交接契约（如有）**/回填要求（消费 Agent 必读段）/闭环检查清单
- 写完停，按结构化审阅（§4）列出容量假设、取条依据与交接点（如有），确认后问"是否交付消费 Agent 执行？"（执行完毕回填 .done.yaml 后再回来走环节 B 关闭）

### 环节 B：DoD 关闭
- 读取 `sprints/{sprint文件}.done.yaml`：
  - 存在 → 按 completed / moved_next 列表核对 DoD + **读取 feedback**：`reason` 类作 moved_next 依据展示（未完成原因随条目状态建议列出），`issue`/`decision` 类汇总列出，需产品层裁决的停下请用户拍板
  - 不存在 → 提示用户人工确认每条任务的完成情况
- 逐条过 `agile-docs/DOD.md` 的 Sprint 完成标准；**含交接契约的任务**，completed 前须已产出对应交接文档（见「交接契约」段），未产出的归入 moved_next
- 在本 Sprint 文件内追加「条目状态建议」清单（通过 → 已完成；未达标 → 移至下个Sprint），格式见 `references/sprint-template.md §二`
- 写完停，问"是否关闭本 Sprint？"

### 环节 C：关闭
- 在文件头追加行标注执行结果来源（.done.yaml 文件路径 或 "人工确认"）
- 将 Sprint 文件头"状态"改为"已关闭"
- 提示用户完整闭环：入口下次激活时检测到 `.done.yaml` 即**默认执行闭环**（Sprint 已由本环节关闭 → 路由到 agile-backlog 同步 + 反馈处理）→ **同步完成后 `.done.yaml` 改后缀为 `.done.processed.yaml` 留痕（不删除，防重复同步）**。链路 lifecycle 见 `using-agile/references/sprint-schema.yaml`

## 4. 写完即停（结构化审阅）

按 `using-agile/references/probing-protocol.md §四` 输出决策点确认清单（重点列容量参数：人数/工作日/专注系数 / 取条依据 / Sprint 目标 / 交接点（如有） × 来源），问"**继续下一环节**还是**更新**当前产出？"。

## 5. 硬约束
- ✅ 单文件产出 `sprints/sprint-{序号:03d}-{日期}.md`（命名含序号+日期，不用 `current.md`）；❌ **不顺手写** VISION / ARCHITECTURE / ADR / PRODUCT-BACKLOG 业务正文。
- ✅ 写前问询遵循 `using-agile/references/probing-protocol.md`：容量参数（人数/工作日/专注系数）必经用户确认，禁止静默默认；Sprint 目标须可陈述（§2）。
- ✅ 关闭 Sprint 前逐条过 DoD（独立出口门禁 ③）；关闭即标"已关闭"状态并记录执行结果来源（.done.yaml 或人工确认），不删除。
- ❌ 不写 RETRO.md / RELEASE.md / FB-NNN.md，不创建 `sprints/archive/` 子目录。
- ❌ 不在 Sprint 文件中设执行态追踪（任务清单与执行进度不写 checkbox、不记阻塞、不处理执行中变更——归消费 Agent）。
- ✅ 「闭环检查」清单用 `- [ ]` checkbox，关闭前逐项核对（这是关闭核对清单，非执行态追踪）。
- ❌ 不直接修改 PRODUCT-BACKLOG.md 的状态列（所有权属 agile-backlog，由入口检测 .done.yaml 默认闭环时路由同步）。

## 6. 门禁
- **DoD 出口门禁（③）**：有未估算/未过 DoD/未验收条目时要关闭 Sprint → 停下，逐条过 DoD。
- **冲突 / 歧义即停**（见 `using-agile/references/gate-protocol.md`）。
