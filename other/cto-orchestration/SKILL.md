---
name: cto-orchestration
version: 1.7.12
description: "CTO/orchestrator 模式管理多 agent 软件交付：agentctl 统一派工（一条 duplex lane、三引擎原生协议，轮内 steer）、goal 合同驱动、typed watcher、异构评审、真路径验收与主理人减负。适用于用户要求'你做 CTO/编排者'、'派 omp/codex 去做'、'goal 模式派发'、管理多会话开发或把这套工作流接入新项目；用户说'复盘 / 收口 / retro / retrospective'时也必须触发（七步仪式 + retro-check 硬门），说'工作盘点 / 盘点候选 / stocktake'时同样触发（盘点仪式，只提案不动工）。新项目先用 repo-governance-bootstrap 建治理骨架。不要用于单 agent 小任务、无需评审循环的局部改动或纯文档初始化。"
metadata:
  requires:
    bins: ["tmux", "omp", "codex"]
---

# CTO Orchestration — 多 agent 软件交付

> 主干只留每次派工都要用的判据与路由；命令细节、故障矩阵和模板按需读 `references/`。
> **能电不文，电后即减**：能下沉 hook / gate 的规则不写散文；电上之后原正文收成一行指针（判据 `references/shock-in-the-loop.md` §1）——约束类散文的价值随门增多而递减，复盘 §3 同轮淘汰。

三条铁律：

1. **编排者不写产品代码**：只产出契约、调度、裁决和状态；实现与长 E2E 交给 worker（guard E1 + bash ⑳ 强制：编排位对源码/测试面的写入 → WARN 留痕，复盘按次数审；通道拼写与未覆盖面见 agentctl README §强制层）。
2. **不可逆先核事实与授权**：push / merge / 部署 / 删除 / 对外消息只认主理人真实新 turn；一次批准不外延。
3. **主理人持判断，不持状态**：可逆事项自驱，非紧急决策攒批；风险带证据、影响边界和下一步及时冒泡。

## 0. 角色与 lane

| 角色 | 责任 | 默认实现（可换） |
|---|---|---|
| 编排者 | 写 goal、派工、监控、裁决、落盘；不写产品代码；提示词 / 教义文本自己改（要派出则准最强模型），改完的测试再派 | 任意 shell + 文件 agent |
| 执行 agent | 按 goal 实现、自测、E2E、交付；不扩 scope；须可观测且可轮间 resume | omp / Claude Code |
| 评审 agent | 冷上下文只读挑刺，给 evidence + severity + verdict；不改码 | codex / 不同 lineage 模型 |
| 运维 agent | 对不可达环境只读取证与部署后验证；不顺手修复 | 用户转交只读取证提示词 |
| watcher | 返回 typed 状态；不把 idle 或沉默解释成完成 | `references/agentctl/` |

默认用 omp 执行、codex 评审，但**工具名不证明异构**；派工前看实际 model/backend，避免执行席与评审席落到同一 lineage 或 quota 池。

派工统一走 `agentctl start|steer|status|watch|stop`——**一条 lane、三引擎**各跑原生 duplex 协议，
能力差异不分叉车道（接口 typed 拒绝 + 指正路）。谁支持什么问 runtime（`agentctl capabilities`，状态词表 `agentctl states`），本文不留第二份能力表。

另有 **Agent subagent**（浏览器 / MCP / 隔离主上下文的读密集工作：独立上下文、只回蒸馏结论、显式按任务分档 model）。
需要人工现场时直接 `tmux attach` 旁观，worker 控制始终走协议。

原生工具与 lane 的边界（选错一次就是一晚，2026-09-02 一席自锁 2h03m）：

| 需求 | 用什么 | 不用什么 |
|---|---|---|
| worker 会话终态 / 交付物 freshness | `agentctl watch`（typed exit） | Monitor 之类文件/进程观察器——不产 typed 终态 |
| 等长外部作业（CI / 部署 / 远端队列） | 宿主长间隔 wakeup（如 ScheduleWakeup / loop） | 反复重挂 watch |
| 席位间即时提醒（同机在线） | 宿主 SendMessage 类即时通道 | agent-mail（它管跨机 / 跨 harness / 需归档的信） |
| 读密集、结论小的取证 | Agent subagent（显式 model 档）；多来源 / 多镜头 → 宿主 Workflow 工具扇出 | 主上下文亲读 |

文件任务必须声明 `--deliverable <glob>`（相对 glob 按会话 cwd 解析），让 runtime 做 freshness gate；非文件结果不带。lane 的完整限制、状态与命令见 `references/agentctl/README.md`。

## 1. 每次派工闭环

1. **校准基线**：fetch 远端，确认目标 base 与 worktree；base 未动不仪式性 rebase。只读 scout 也显式指定 cwd/base，防静默继承过期 checkout。命令与核证见 `references/dispatch-baseline.md`。
2. **写自包含 goal**：一个 goal = 一个可独立交付的单元 + 一个清晰交付物；每条 Done-when 绑定证明命令，写清 scope、out-of-scope、stop-and-report。高不确定方向进入昂贵设计/实现前，先跑最便宜证伪；取证 / 机械 / 纯研究类 goal 用 `--no-preflight` 显式豁免，其余 goal 默认过 preflight 门（start 校验 Preflight 声明已解）。单行合同、Premises 与 Value gate 直接用 `references/goal-template.md`；场景条款按需读 `references/goal-clauses.md`。
3. **派发并挂 watcher**：`agentctl start …`——goal 帧被接受即返回、**不会自动 watch**，紧接着用宿主
   受控后台跑 `agentctl watch`；先接线 `references/agentctl/guard-hooks.json`（高频机械失误归 guard，
   主干不复制其规则表）。理解门与 BLOCKED 协议由 runtime footer 固定追加（`agentctl` `append_footer` 为真源，本文不复述）。
4. **只消费 typed status**：`agentctl status`（一次性）或 `agentctl watch`（阻塞终态）。不直接读私有 rc/events，也不把 watcher/agent 自报当完成。任何沉默、超时、外部停滞或缺交付物都按对应 typed 分支处理；词表跑 `agentctl states`，处置见 agentctl README。
5. **steering 走 `agentctl steer`**：默认**尽快送达**（turn 进行中原生 mid-turn：omp/codex；claude
   降级 turn 边界并明说；空闲即刻开新 turn）、`--interrupt` 打断当前 turn 以本条重开；
   引擎能力差异查 `agentctl capabilities`。投递成功 ≠ 模型照做，验收仍看交付物。每个后续 turn 都重挂 `agentctl watch`（stop guard S1：本仓有 RUNNING 席位且无活 watcher 时拦收工）。
6. **Implemented → Verified**：fresh 正向交付证据 + 独立评审 + 真实用户路径 E2E 三件齐，**深度按 §2 档位**（轻档 = 1 轮冷评审或编排位抽查 + 子集门；部署与部署环境 E2E 仅当交付物真有部署面）。先本机真路径，再部署，最后才关单；git 集成与 push 门禁归 Git workflow 标准。

## 2. 对抗式评审循环

- 按风险定深度：低风险走轻量 review；鉴权、迁移、基建、大重构走 `references/review-dispatch.md` 的完整循环。
- **goal 评审：白名单免评，其余必评**——命中免评白名单（唯一清单在 `references/review-dispatch.md` §goal-review，共同硬门=不新增任何决策面）→ 跳过；未命中或拿不准 → 派发前 1 轮冷上下文 goal-review（仪器六问 + 契约三问，同节）。
- **档位只有两档，按派工前能看见的事实判，不按行数、不按文件类型**：**深档** = goal 新增判断面（判据 / 门 / 状态 / 接口 / 解析面）→ goal-review 1 轮 + 冷评审 blocking 驱动；跨模块 / 新状态机的深档批派工前方案预审给主理人（goal 抬头 `Tier:` 行声明档位，deep 带 `Goal-Review:` 回执，preflight 缺则 WARN）。**轻档** = 其余（纯删、纯搬迁、有参考实现、本地文档）→ 不做 goal-review，1 轮冷评审或编排位抽查闭合；轻改车道（下文）是轻档的子集。**档位同时决定执行席模型**：轻档 = 基础变量、深档 = `_DEEP`（README §start 默认模型），派工不手打 `--model`。规模由评审看真实 diff 事后判；goal 里不写行数预估、上限或比值（写了 = finding）。写深档合同、裁大批阻断 findings 时建议高推理档（`xhigh` 或者 `max`）。
- **直写也要合同**：编排位自己直写 shipped 面（教义 / 门 / guard）动手前，同样先写最小合同——
  Done-when + 坏样本来源 + scope 三行即可，评审 brief 随附；无合同的直写单元评审者当 finding 报。
- brief 冷上下文，不喂实现者结论；只审主路径 + 零变异 + 已知阳性（边界口径归 review-brief-preamble，brief 点名边界词 guard ⑬ WARN），出口用 file:line、confidence 与失败探针过滤。
- 先枚举执行分叉；轴装配先查 path→轴映射表（表命中必进 brief，判断只增补），再点名 `缺失消费者`、
  under-fire、并发 / 恢复等高风险轴；完整轴表与映射表留在 reference。
- **非深档默认恒一轮**：findings 回编排位裁 fix / accept-documented，修复轮不自动回评审——编排位
  复现抽查闭合；任何续派评审须在 brief 写 `SHIP-BLOCKING: <依据>`（runtime 从第 3 次投递起强制：start = 第 1 轮、首次 steer = 第 2 轮）。深档（门禁/
  量具/状态机/安全面）保留 blocking 驱动续轮；同一 finding 的修复连续 2 轮只新增 finding，则止损走三选项之一：换机制 / accept-documented / **向主理人请示需求降级**——两轮催生的是**更大机制**（本轮 remedy 比上轮新增更多防御面/配置/状态，diff 面数在涨）
  而非更小需求 ⇒ 强制走第三选项，请示时附上原需求与两轮 remedy 的净增面（止损空间含需求层）。
- **提效是显式目标**：批 overhead（评审轮数 × 门分钟数 × 保姆轮）计入杠杆账，收口在台账记
  wall/avoidable 两个数（retro-check 第 9 检缺记即 FAIL）。仪器（自证 / 变异 / 矩阵）墙钟超过实现墙钟 = 倒挂，下批该仪器降档（binding → advisory → 删；不降 §3 三态门底线）。**轻改车道**（教义/注释/指针，零产品代码）：不派席、不派评审席——
  编排位直改，子集门 + CI 兜底，单 commit 落。非深档迭代只跑**改动面子集门**（选择机械推导；
  同名歧义 / rename / 量具坏一律回退全量），全量留合并前一次 + CI 兜底。**证据到层即停**：
  拒绝/回退类行为证到**决策行**为止，全量只在运行本身是验收对象时跑——合同写明证到哪层，
  不写则席位会用最贵的方式证。
- **杠杆账（简单干脆优先）**：用户可见小病 → 先找交互/配置层一刀关整类的最小解；机制自明（关掉即该类物理不可发生）且可逆 → 直做，机制存疑 → 仍过 §3 先量再改；取证仅在最小解不明时派。修复轮 ≥2 或对外协定往返 ≥2 → 主动算杠杆账（残余 = 概率×血量×复杂度）提降级案，不等主理人纠偏；单 seat 不堆叠多份合同——交付时点会被最慢件绑架。
- **配比轴（真路径优先）**：开批前判面，**以落地物路径为准**——外部使用者装得到 / 读得到 /
  跑得到 = 业务面（工具型项目 shipped 工具即产品本体，判「装得到吗」不判「是不是工具」）；
  测试 / 门 / 自用工具 / 本地台账 = 工程面；覆写留一行理由。**闸咬结果停滞不咬投入计数**：
  距上次「真实用户路径被走通」超阈值 → STOP-and-report，报告必答「下一条要验的真路径是什么」。
  三个词各有确定来源，缺一即闸不成立：「被走通」= 存在过本节回执判据的交付回执；
  **阈值与单位**由项目 AGENTS.md 编排节声明（无声明 = 闸未装）；
  **尚无合格回执 = 闸已触发**（fail-closed）。权威记录 = 复盘写进台账那一行，故此闸**复盘时判、
  不连续计时**；比值旋钮（默认 8:2，惯例非发现）只在复盘呈现、归主理人调。
- 多轮 headless review 显式传 `--workflow review-loop --max-rounds N`（三引擎通用：每次 goal/steer 投递计一轮）；轮数与 stop-loss 只认 runtime meta，主干不复制状态机。
- 评审期间执行 agent 不写同一 worktree。

## 3. 实现与验证判据

- **先量再改**：先证 bug 当前可复现、怀疑机制真是绑定约束、执行真到该路径；未证先补观测，不发投机修复。
- **病类确认后枚举同模式点**：逐一分类，一轮收敛，别等评审逐个显形。
- **高风险 checker 先自证判别力（三态门：判不了 ≠ 通过）**：坏样本红、好样本绿、量具坏时报 `ERROR`；缺一不消费 `PASS`。
  验证深度按**门的严重度**分档（DENY 全套 / WARN 减项），表在 implementation-discipline。
- **golden 参照物先过已知阳性**：收编好结果 run 里的组件（SQL / 配方 / 模板）前，行级复现它真能产出期望阳性——run 得高分不是证据（功劳可能记错组件），byte-fidelity 只证抄得像。
- **代验不冒充真验**：不 mock 正在验证的边界；交付明确写已验证、未验证与剩余风险。
- **回执要答「谁走的」不是「跑了多少」**：必须能答**谁 / 在真实模式下 / 走到第几步 / 看到了什么**；
  只答得出条数与 exit code = 没人走过，按未完成收。**缺口要与成绩同形态**——「N passed」是数字而
  「真实依赖未验」是散文时，散文进不了决策：把缺口也变成数字或门（推论见 implementation-discipline）。
- **绿而路没走时先走那条路，别先加门**：机制测试增长与用户路径覆盖增长互不产生因果。
- **多主体轴**：可见性/授权/内容随 actor 变化（本人 / 同租户他人 / 跨租户 / 角色）的功能，验收须
  列 actor 矩阵、至少覆盖 owner + 一个非 owner 视角；单视角验收结论标 `UNKNOWN`——这类盲区
  当事人提不出问题，只有清单覆盖得住。

具体旗标、stale-edit、验证顺序与失败模式按需读 `references/implementation-discipline.md`。

## 4. 不可达环境

够不着 prod / 独立 dev DB 时不猜、不直接改：写一份自包含只读取证提示词交用户转交。现场证据优先于 HEAD 推断；矛盾时先核部署 SHA / 构建漂移。

## 5. 状态、收口与主理人注意力

- `docs/orchestration/` 是共享 SoT：live 只留在跑/在等事项，完结物归档；memory 只存编排者私有教训和入口，不替代共享 docs。
- runtime evidence 推翻 audit/scout 时，同轮回写源文档 `REFUTED CLAIMS`（claim / evidence / pointer），不只记在摘要。
- 外部任务系统存在时，它是状态 SoT；roadmap 只做映射，不养第二套账。
- **复盘仪式**（触发词：复盘 / 收口 / retro；事件点：收口 / 压缩前 / ReOpen 后）：读
  `references/retrospective.md` 七步逐条勾，再跑 `references/retro-check.sh`；不即兴发挥。
  压缩点自动提醒 wiring 真源 = `references/retro-hooks.json`（可选接入）。
- **盘点仪式**（触发词：盘点 / 接下来做什么 / 规划下一批）：读 `references/stocktake.md`
  四步逐条勾；选题取舍判据单源在该文件，不即兴。
- 主理人只决战略、不可逆、钱与价值。决策队列、T0/T1/T2 语义和静默默认见 `references/decision-queue.md`。

## 6. 专项路由（用到才读）

| 场景 | Reference |
|---|---|
| 新项目接入 | `references/onboarding-checklist.md` |
| 前端真实验证、状态形状矩阵、浏览器委派 | `references/frontend-verify.md` |
| 评审 brief、ledger、收敛 | `references/review-dispatch.md` |
| 基线与收工四件套 | `references/dispatch-baseline.md` |
| 测量/评测类 goal 的测量协议 | `references/measurement-protocol.md` |
| agentctl 命令面、duplex 机制、steering、guard wiring | `references/agentctl/README.md` |
| 电在回路：承重规则下沉强制层、DENY 三件套、下沉判据 | `references/shock-in-the-loop.md` |
| 主理人决策队列 | `references/decision-queue.md` |
| 项目 AGENTS.md 编排增量 | `references/agents-md-orchestration-section.md` |

多个编排者并行时，用可选伴随 skill `agent-mail` 做跨席位异步通信。
