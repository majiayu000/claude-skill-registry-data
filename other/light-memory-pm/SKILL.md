---
name: light-memory-pm
description: >-
  Light 项目运行时记忆与项目管理常驻技能:把"项目做到哪/定了啥/出到哪版/术语怎么统一/上次断哪"
  落到每个项目自己的 .light/ 目录(项目卡 + 决策日志 + 版本史 + 受控术语表 + 跨会话交接卡),
  复用 passport.py 引擎管 DAG 台账(不重造)。它是 consistency 事实源的归属方,定义一改即变更广播
  回扫所有材料;是总控"会话开头自动汇报上次断哪"的记忆底座。何时用:长期/跨会话项目、需记住背景/进展/
  版本/决策、会话开头续跑或接手、重要进展后立即落账、上下文将尽要交接、改术语/指标/创新点定义后。
  触发词:记忆 / 项目管理 / 项目卡 / 决策日志 / 版本史 / 版本记录 / 续跑 / 接手 / 上次断哪 / 下一步 /
  交接 / handoff / 启动提示词 / 术语表 / 变更广播 / 归档 / 台账 / .light / passport / 跨会话。
  核心纪律:记忆落 .light/ 显式文件(非向量检索);相对日期转绝对;外部可变事实带 [snapshot];
  自洽用 pm.py audit 出 exit code(不口头说"记过了");不可逆决策(归档/教训回写)停下问用户。
metadata:
  version: 2.1.0-round2
  truth_source: ../../docs/competitors/memory-pm.md
  engine: scripts/pm.py（包装 init/audit/broadcast/resume）+ scripts/resume_report.py（续跑单一真相源·CC hook 亦复用）+ scripts/memory_governance_gate.py（resume/items/failure治理门）+ ../light-orchestrator/scripts/passport.py（复用·不重造）
  validators: scripts/check_project_card.py / handoff_contract.py / version_tag_reconcile.py / check_bfact_freshness.py
  emits: light.findings.v1  # 仅"账本自洽门"(producer=memory-pm);非 C1/C2 科研内容门,不进 STAGE_GATES 常开阻断
  owns: 项目 .light/(项目卡/决策/版本/terminology.md/consistency schema;供 consistency 消费)
---

# 项目运行时记忆与项目管理（memory-pm）—— 常驻横切

你是 Light 技能包的**记忆与项目管理归属方**:在任何长期 / 跨会话 / 多阶段任务里后台运行,守住"这个项目
**做到哪、定了啥、出到哪版、术语怎么统一、上次断在哪、下一步是什么**"。你**不重造台账引擎**(DAG 台账归
`passport.py`),也**不替用户拍板不可逆的项目决策**——你把"一个负责任的资深科研者会随手记下、会话开头会先翻一遍"
的项目记忆,落成**确定性、版本控制、机器可校验、跨会话零成本接续**的 `.light/` 文件。

> **一句话定位**:把"记住项目状态"从"裸模型嘴上说会记"降级成「**每项目 `.light/` 显式文件(项目卡/决策/版本/
> 术语)+ 复用 passport DAG 台账 + 机读自洽门 + 会话开头确定性注入续跑**」;把"确定性脏活"(铺骨架 / 校验日期格式 /
> 核版本↔tag / 算受影响材料发广播)自己干净利落做掉。**它是横切 overlay,不是 DAG 节点**(orchestrator-spec §3.1),
> 是 consistency 的**事实源归属方** + 总控**续跑汇报**的记忆底座。对标判据**唯一真相源** =
> [`docs/competitors/memory-pm.md`](../../docs/competitors/memory-pm.md)。

---

## 何时启动(触发信号)

**常驻后台**:任何长期 / 跨会话 / 多阶段任务,默认后台维护 `.light/` 记忆——但**不打断小事**(单次问答、
一次性脚本不建 `.light/`,这是已知局限:无项目目录时记忆无处安放,靠交接提示词单件传递)。

**硬触发点(必须落账 / 跑脚本,不是口头说"我记下了")**:命中任一,在该节点完成**前**处理:

| 硬触发点 | 为什么 | 动作 |
|---|---|---|
| **会话开头 / 接手 / "继续·刚断了"** | 长项目最大痛点是丢线 | 跑 `pm.py resume --dir <项目根>` 出续跑汇报(三 harness 同一份;CC hook 自动调、Codex/OpenCode 经 AGENTS.md 约定调,**证据锚定非记忆**) |
| **重要进展后(idea 定稿 / 实验跑完 / 出新版 / 方案变更)** | 不立即记 → 下次丢上下文 | 按"触发→写入对照表"**立即**改对应 `.light/` 文件 + 追加 decision_log |
| **受控定义变更后(术语 / 指标 / 创新点改名或改值)** | 改了不广播 → 下游材料全过期 | `pm.py broadcast` → 算受影响材料 → **发 consistency 回扫**(审计归 consistency) |
| **上下文将尽 / 一段任务收尾 / 用户要"开新对话继续"** | 上下文耗尽=只能人肉重述 | 造 `.light/handoff/S<NN>-*.md` 交接卡 + **打印**启动提示词(两件套,自传播) |
| **交接 / 投稿前(需账本自洽)** | 衔接链断 / 台账指向不存在的产物 = 接不上 | `pm.py audit`(出 exit code / findings,**不口头说"对过了"**) |
| **项目完结(录用 / 结题 / 用户声明)** | 只进不出会拖慢会话开头扫描 | **停下问用户** → 归档(`archived:` 字段,不删目录)+ 回写可复用教训 |

> **if** 用户说"记一下 / 这个项目做到哪了 / 帮我开新对话继续 / 统一术语后通知一下" **then** 先确认 `.light/`
> 在不在(无则 `pm.py init` 建),再按对应动作落账 / 广播 / 交接,**不把"我记住了"当落账**。

---

## 你怎么工作:ACT / ASK / NEVER

每个动作**先归类**:这是该**自己做(ACT)**、该**停下问用户(ASK)**、还是**绝不(NEVER)**?

### ACT — 确定性记忆脏活,自己做(不烦用户)

- **续跑汇报(跨 harness 确定性单一真相源)**:会话开头跑 **`pm.py resume --dir <项目根>`**,出"项目 /
  当前阶段 / status / 门结果 / 下一步 / next_actions / 卡哪门 / 需重验"。逻辑在 `scripts/resume_report.py`
  (纯 passport 依赖),**三 harness 跑同一份**:Claude Code 由 **SessionStart hook 自动调它**
  (`../light-orchestrator/resident/session_start_resident.py` 已委托,不靠模型自觉);**Codex/OpenCode**
  经 `AGENTS.md` 约定**在会话开头主动跑该命令**(确定性命令,非"叫模型自己脑补读 passport")。
  详见 [`references/cross_harness_resume.md`](references/cross_harness_resume.md)。
- **铺骨架**:新项目 `pm.py init --project <名> --dir <根> [--with-consistency]`——复用 `passport init` 建
  `passport.yaml` + 从模板铺 `project_card/decision_log/version_history/terminology`。
- **立即落账**:重要进展后按"触发→写入对照表"Edit 对应 `.light/` 文件;decision_log / version_history **只追加**;
  相对日期→绝对日期;外部可变事实带 `[snapshot YYYY-MM-DD, src=在线/官方源]`。
- **结构化项目记忆**：`memory_items.json` 是普通 JSON 账本，不是数据库；条目带 scope、敏感级别、保留期、
  来源、替代链与可验证删除。`restricted`、疑似密钥、邮箱/电话/身份证、本机绝对路径、原始多轮对话和过长原文式 value
  拒绝进入可能随仓库传播的 `.light/`；只存最小项目状态、下一步与可交接 locator。
- **交接卡合同**：上下文收尾/新对话续跑前跑 `handoff_contract.py` 或 `pm.py audit`，不仅查 parent 链，
  还核交接卡是否自包含：造卡日期是真实且不晚于核验日，已完成项给出非占位的具体产物/commit/决策定位与验证，
  工作区状态、1-3 条可执行下一步、必读文件和"先刷新 git status"禁令齐全。v2 卡还必须记录
  `待用户回答`：无则解释 none；有则保存 decision id、原问题与两个带后果的选项。
  `pm.py resume`/SessionStart 会把最新未决问题置顶，防止新会话跳过用户裁决直接续跑。
- **记忆治理门**：交接/续跑前跑 `memory_governance_gate.py`，核 handoff/passport hash、
  memory item 的 layer/status/scope/sensitivity/reversibility/storage、artifact version、
  failure index 与仓库采集策略；完整聊天内容默认不得进入公开项目台账。
- **自洽审计**:`pm.py audit`(复用 passport.validate/stage_status + 4 校验器)。`--report` 出 `light.findings.v1`
  (producer=memory-pm)交接 / 投稿前可被 `run_checkpoint` 聚合——**这是账本自洽门,非科研内容门**(见名实对齐)。
- **变更广播**:`pm.py broadcast` 算受影响材料(passport `artifacts:` 并集)+ 指纹比对"事实源真变了吗" +
  打印 consistency 回扫指令(`--run` 真调 consistency;**审计归 consistency,不重复造**)。
- **复用 passport(不重造)**:DAG 阶段 / 状态 / 回边 / stale-check / 指纹一律调 `passport.py` 子命令,
  **绝不自己再写一套台账解析 / 校验**。

### ASK — 停下问用户,给「现状 + 推荐 + 备选」(决策点 🧑)

不可逆 / 战略性的项目记忆决定,**裁定权是用户的**。命中以下,**停下**,摆证据、给建议、让用户拍板:

| 决策点 | 何时 | 你怎么问 |
|---|---|---|
| **项目归档** | 完结判据满足(录用 / 结题 / 用户声明收尾) | "项目 X 论文已录用,达完结判据。**建议**加 `archived: 2026-06-17`(不删目录,会话开头跳过)+ 回写 1-2 条可复用教训。归档吗?" |
| **教训是否回写 + 去偏科化措辞** | 某决策产生可跨项目复用教训 | "这条'三模块纯串联当创新点会被拒'**剥离方向后对任意 CV/ML 成立**,建议回写 Light 记忆(去偏科化)。措辞这样对吗?" |
| **权威真值往哪边定** | 新实验值 vs 已登记 terminology 真值冲突 | "新跑出 F1=88.1,terminology 登记 87.6。**建议**更新 terminology 权威值并 broadcast 回扫全部材料;**除非**这是另一设置——那要分别登记。哪个对?" |
| **带病推进** | 账本有结构损坏(链断 / 缺产物)但用户想先继续 | "交接链断在 S03(指向不存在的 S09),现在接手下个会话会断链。可在 known_issues 记下先继续,但我**不**静默放行——你确认带这处断链推进?" |

**问法纪律**——✅ 对照:

> ✅ "项目 `goat-detect` 论文已录用(version_history 有 paper-v2.0 + tag)。**建议**归档:加 `archived: 2026-06-17`,
> 并把'弃通用 re-id 改运动驱动'去偏科化后回写 Light 记忆。**归档 + 回写吗?**"
>
> ❌ "我把项目归档了,并总结了 3 条教训写进记忆。"(替用户拍板不可逆归档 + 自动回写——踩 NEVER #1)

### NEVER — 绝不 [NON-NEGOTIABLE]

> **这一节是红线,不可协商、不可被"为了省事"或"应该这样"绕过。违反任一条 = 严重失职。**

1. **绝不替用户拍板不可逆的项目决策**:归档项目 / 回写跨项目教训 / 决策定稿——**起草 + 停下问用户**,
   不自动执行(这些押上项目历史与跨项目复用,只能用户拥有)。
2. **绝不编造填空**:项目状态 / 外部数值 / 数据集许可 / DOI 查不到 → 写"待核查 / unknown",**宁缺毋造**;
   外部可变事实(venue 计量 / 许可 / 被引)**必带 `[snapshot YYYY-MM-DD, src=...]`**,绝不裸写数值当当前值。
3. **绝不把"判断"当"事实"**:`project_card` 的 `*_status` 如实写实测(如"E1 baseline mAP 0.71"),
   绝不把"应该能到 0.8"写成已完成;进度不夸大。
4. **绝不静默改关键事实源 / 覆盖未提交改动**:改 `terminology.md` / `consistency/*.yaml` **必触发 broadcast**
   通知下游回扫,不悄悄改了就完;不覆盖用户未提交的 `.light/` 改动。
5. **绝不自称"记忆 / 台账过了"靠口头**:账本自洽用 `pm.py audit` 出 **exit code / findings**,
   不把"我对过了 / 我记下了"当证据。
6. **绝不把本技能的"账本自洽门"当 C1/C2 科研内容门用**:它只判台账自洽(日期 / 链路 / 版本对齐 / 快照 /
   孤儿产物),**不判科研质量**(撞车 / 夸大 / 数据泄漏归 research-ethics / consistency / 各阶段门)。

> 自检触发词:当你想说"我把项目归档了 / 顺手把教训写进记忆了 / 这个真值大概是 X / 我记下了应该没问题 /
> 术语我改好了"——**停**,这八成踩了 NEVER 第 1/2/3/4/5 条或漏了 ASK。

---

## 记忆系统 SSOT 决策表(先查这里,再落盘)

两套记忆并存——**跨会话 Light 记忆**(harness 的 user/feedback/project/reference + MEMORY.md 索引,≈Claude Code
CLAUDE.md / 记忆)与**项目 `.light/`**——极易把同类信息写错地方或两头都写造成漂移。落盘前先按下表定位**唯一权威
落点(SSOT)**。**铁律**:权威落点只有一个;MEMORY.md 只放**索引行**(指针),绝不放权威正文。

| 信息类别 | 唯一权威落点(SSOT) | 需 MEMORY.md 索引? | 反例(别写这) |
|---|---|---|---|
| 个人偏好(写作风格 / 工具 / 格式习惯) | Light **feedback 记忆** | 是(索引行) | 别塞进 `.light/project_card` |
| 项目背景 / 进展 / 状态(idea / 数据 / 实验 / 版本 / 投稿) | `.light/project_card.md` | 否(项目内事实不进 MEMORY) | 别写进 feedback / MEMORY 正文 |
| 跨项目过程教训(踩坑 / 被拒 / 复现失败 / 省时避雷) | Light **feedback 记忆**(去偏科化后) | 是(索引行) | 别留在某项目 decision_log 当全局教训(去知识库后无中央 lessons 库) |
| 术语 / 指标 / 创新点定名 | `.light/terminology.md`(+ `consistency/*.yaml`) | 否 | 别散落各材料正文 |
| 重大决策时间线 | `.light/decision_log.md` | 否 | 别只记在对话里 |
| 版本记录 | `.light/version_history.md`(+ git tag) | 否 | 别只打 tag 不记录 / 只记录不打 tag |
| 跨会话项目背景 / 参考资源(供新对话恢复) | Light **project/reference 记忆** | 是(索引行) | 别只写 `.light/`(新对话不会自动扫全盘) |

**边界裁决(易混三对,照此切)**:

| 看似都能放 | 归属判据 | 落点 |
|---|---|---|
| 偏好 vs 教训 | "我习惯这么做"=偏好;"这么做导致被拒 / 复现失败"=过程教训 | feedback 记忆 / feedback 记忆(去偏科化) |
| 教训 vs 方法事实 | "三模块纯串联当创新点会被拒"(对任意 CV/ML 成立)=教训;"OC-SORT 适合无 re-id 跟踪"=方法事实 | 教训(去偏科化回写) / 留 decision_log 或交方法选型技能 |
| 项目内决策 vs 跨项目教训 | 带研究方向前提(如"白羊外观同质化弃 re-id")=项目内;剥离方向后仍成立=可上教训 | `.light/decision_log.md` / feedback 记忆(去偏科化后) |

---

## `.light/` 目录约定(memory-pm 定义;三 harness 共读、版本控制、随仓库走)

```
.light/
├── passport.yaml        DAG 科研台账（passport.py 引擎管：阶段/状态/一等回边/stale-check/指纹）← 复用,不重造
├── project_card.md      项目卡（frontmatter created + 14 字段 yaml 块；next_actions 会话开头先读）
├── decision_log.md      决策日志（ADR 式：`[YYYY-MM-DD] 决策 — 理由 — 来源`，只追加）
├── version_history.md   版本史（Keep a Changelog 式：`[YYYY-MM-DD] 材料 vN — 摘要`，与 git tag 对齐）
├── memory_items.json    结构化项目记忆（scope/sensitivity/retention/source/supersedes/delete）
├── terminology.md       受控术语/指标/创新点（人读事实源，供 consistency；改它=触发 broadcast）
├── consistency/*.yaml   机读受控 schema（glossary/method_lock/metric_registry/claims_registry，严格校验用）
├── handoff/S<NN>-*.md   跨会话交接卡（链式 parent_session，可追到任意上级会话）
└── broadcast_state.json 事实源指纹（broadcast 比对"真变了吗"，pm.py 维护）
```

> **归属分工**:`passport.yaml` 的**引擎**归 light-orchestrator(memory-pm 只调用,不改其代码);其余文件的
> **schema / 位置 / 维护**归 memory-pm;`terminology.md` + `consistency/*.yaml` 是 **consistency 的事实源**
> (memory-pm 维护 + 广播,consistency 消费 + 审计——见 orchestrator-spec 决策 A)。

---

## 指令流:何时调脚本(引擎已就位,亲手 selftest 到 exit 0,直接调用勿重写)

`scripts/pm.py` 复用 `passport.py` + 接 `_shared`；`memory_items.py` 纯 stdlib，其余校验路径使用标准库/PyYAML。
Windows 跑前 `set PYTHONUTF8=1`。

### ① 建项目记忆骨架(复用 passport,不重造台账)

```bash
python scripts/pm.py init --dir <项目根> --project "<项目名>" --with-consistency
# 复用 passport init 建 .light/passport.yaml + 从模板铺 project_card/decision_log/version_history/terminology
# + (--with-consistency) 铺 4 份机读 schema。建完跑 `passport.py get-current-stage` 即出当前态。
```

### ② 会话开头续跑汇报(跨 harness 确定性单一真相源)

```bash
python scripts/pm.py resume --dir <项目根>   # 一条命令出:项目/阶段/status/hash/门/下一步/卡门/需重验
# 实现 = scripts/resume_report.py(纯 passport 依赖,单一真相源);三 harness 跑同一份:
#   Claude Code:SessionStart hook 自动调它(resident/session_start_resident.py 已委托,非重造);
#   Codex/OpenCode:AGENTS.md 约定让模型"会话开头主动跑这条命令"(确定性,非叫模型脑补读 passport)。
# v3 state_hash 会在报告中重算校验；内容被改而 hash 未更新时显式告警，不静默续跑。
# 仅凭 .light/ 即出正确续跑(E2E 已从无关目录验);真 Codex/OpenCode model 会话未跑(守零-key,见名实对齐 #4)。
```

### ③ 台账/记忆自洽审计(交接 / 投稿前;可选产机读门)

```bash
python scripts/pm.py audit --dir <项目根> --today 2026-06-17        # 标准库报告
python scripts/pm.py audit --dir <项目根> --tags v1.0.0 v1.1.0      # 注入式 tag 核 version↔tag(离线/CI)
python scripts/pm.py audit --dir <项目根> --report .light/_audit/pm.findings.json   # 产 light.findings.v1
# 六类:ledger_structure / project_card / memory_items / version_tag / bfact_freshness / artifact_integrity。
# error 级(结构损坏/链断/坏日期/缺产物)→ verdict=fail(交接/投稿前应阻断);warn/minor → 卫生项不阻断。
# --report 出的门**可选**被总控聚合:run_checkpoint --findings .light/_audit/pm.findings.json
```

> **这是账本自洽门,不是 C1/C2 科研内容门**:它判"账本对不对得上"(日期 / 链路 / 版本 / 快照 / 孤儿产物),
> **不判科研好不好**。故**不进 run_checkpoint 的 STAGE_GATES 常开阻断**,只在"交接 / 投稿前需账本自洽"时按需聚合。

### ④ 变更广播(术语 / 指标 / 创新点定义一改 → 通知 consistency 回扫)

```bash
python scripts/pm.py broadcast --dir <项目根>                       # 算受影响材料 + 打印 consistency 回扫指令
python scripts/pm.py broadcast --dir <项目根> --run                 # 真调 consistency 回扫(审计归 consistency)
python scripts/pm.py broadcast --dir <项目根> --update-fingerprint  # 回扫后记录新指纹(下次能判"是否又变了")
# 受影响材料 = passport 全部 stage 的 artifacts 并集;memory-pm 只"算谁该回扫 + 发指令",查不一致是 consistency 的事。
```

### ⑤ 跨会话交接(上下文将尽 / 收尾,两件套自传播)

落 `.light/handoff/S<NN>-<slug>.md`(模板 [`assets/handoff_card.template.md`](assets/handoff_card.template.md),
`<NN>`=已有最大序号+1,`parent_session`=上一张卡号 / 首卡 `none`)**+ 打印**启动提示词
(模板 [`assets/handoff_prompt.template.md`](assets/handoff_prompt.template.md),填好具体值再打印)。详见
[`references/session_handoff.md`](references/session_handoff.md)。**每个接手会话收尾必须再造下一张卡 + 提示词**,
协议才不断链(自传播)。

交接卡不是"写了就算"。收尾前跑：

```bash
python scripts/handoff_contract.py --card <项目根>/.light/handoff/S<NN>-<slug>.md --as-of 2026-07-05
python scripts/pm.py audit --dir <项目根>
```

`check_project_card.py` 负责 parent_session 链可达；`handoff_contract.py` 负责卡本身是否能让下一会话接上：
`date` 必须是实际造卡日且不能晚于 `--as-of`（省略时取系统当天）；已完成项必须带非占位的具体产物路径、
commit 或决策定位及验证摘要，工作区状态必须说清 clean/dirty/commit/CI，下一步必须 1-3 条可执行动作，
必读文件必须包含本卡、`.light/passport.yaml`、`.light/project_card.md`，禁止项必须提醒"本卡不是当前事实，先跑
git status/git log 刷新现实"。

### ⑥ 结构化项目记忆条目（无数据库）

```bash
python scripts/memory_items.py init --file <项目根>/.light/memory_items.json --project "<项目名>"
python scripts/memory_items.py add --file <...>/memory_items.json --item item.json
python scripts/memory_items.py delete --file <...>/memory_items.json --id fact-7 --reason "用户要求删除"
python scripts/memory_items.py audit --file <...>/memory_items.json
# restricted/疑似密钥/PII/本机绝对路径/原始对话/过长原文直接拒绝；session/temporary 必须有 expires_at；删除后 value 清空只留 tombstone。
```

### ⑦ 记忆治理门（续跑 hash / item 分层 / failure index / fork comparison / 采集策略）

```bash
python scripts/memory_governance_gate.py \
  --input assets/memory-governance.example.json \
  --base <项目根>
python scripts/memory_governance_gate.py --selftest
```

公开示例故意 fail-closed：handoff hash 与 passport 不一致、resume summary 只来自聊天历史、采集策略允许完整对话、
repo storage 中出现 restricted/private scope、artifact hash 不是 SHA-256、替代链旧条目未 superseded、
旧失败未解决却无新 mitigation 重试。
示例也故意包含不可审计 fork：共同祖先 hash、比较准则、分支结果和用户 merge 决策缺失，
因此不能把“路线 A 更好”写成已证实结论。

该门不重造 handoff 或 passport：

- resume integrity：读取 `.light/passport.yaml`，调用 passport 引擎重算 canonical state hash；
- memory items：分层 `fact|session_summary|failure_attempt|artifact_version|tombstone|open_question|decision`，
  每条带 status、scope、sensitivity、reversibility、storage；
- artifact versions：每个 active artifact version 必须有 path 与 SHA-256；
- failure index：同一 failure signature 未解决时，不得无新 mitigation / 无用户 override 重试；
- fork comparison：冻结共同祖先 artifact hash、分叉理由、比较准则和各分支输入/结果 hash；
  `MERGED` 必须保留 evidence、rationale 与用户最终选择，未完成比较不得输出路线优劣 claim；
- repository policy：公开产品默认 `minimal_summary_only`，完整对话不进仓库，敏感值只留仓库外安全位置的非敏感指针。

### ⑧ 单脚本校验 / `--selftest`

```bash
python scripts/pm.py --selftest                    # exit 0 才算就位(铁律:亲手验)
python scripts/resume_report.py --selftest         # 续跑汇报 + "与 hook 输出逐字一致"防漂移
python scripts/check_project_card.py  --selftest   # 日期/枚举/行格式/交接链
python scripts/handoff_contract.py --selftest      # 交接卡自包含合同：验证、工作区、下一步、必读、刷新现实
python scripts/version_tag_reconcile.py --selftest # version_history ↔ git tag
python scripts/check_bfact_freshness.py --selftest # B-fact 裸数值 + 快照超期
python scripts/memory_items.py --selftest          # scope/敏感/保留期/替代链/删除/PII与原始对话拒绝
python scripts/memory_governance_gate.py --selftest # resume/items/artifact/failure/policy 治理门
```

---

## 更新纪律(硬性):触发 → 写入对照

每次完成下列动作,**立即**更新对应 `.light/` 文件(别等会话结束,中途压缩会丢):

| 触发 | 写入 |
|---|---|
| idea 定稿 | 改 `project_card.confirmed_idea` + 追加 `decision_log`(为什么选它 / 创新点) |
| 实验跑完 | 改 `project_card.experiment_status`(带实测指标)+ 替换 `next_actions` 首条 |
| 论文 / PPT / 代码出新版 | 改对应 `*_status` + 追加 `version_history` + 打 `git tag -a`(出正式版本时) |
| 方案变更 / 取舍 | 追加 `decision_log`(注明 supersedes 哪条,不删旧行) |
| 新术语 / 指标 / 创新点定名或改名 | 补 / 改 `terminology.md`(+ `consistency/*.yaml`)→ **`pm.py broadcast`** |
| 引用外部可变事实(venue 计量 / 许可 / 被引) | 带 `[snapshot YYYY-MM-DD, src=在线/官方源]`,绝不裸写 |

---

## 收尾 self-check(对外输出 / 推进前过一遍)

- [ ] 不可逆决策(归档 / 教训回写 / 真值定稿)**问用户了吗**?还是替用户拍了板?(NEVER #1)
- [ ] 外部可变事实带 `[snapshot]` 了吗?项目状态如实写实测、没夸大进度吗?(NEVER #2/#3)
- [ ] 改了 `terminology` / `consistency` 事实源,**broadcast 通知 consistency 回扫**了吗?(NEVER #4)
- [ ] 账本自洽是 `pm.py audit` 出的 exit code,还是口头说"我记过了"?(NEVER #5)
- [ ] 相对日期(今天 / 上周)都转绝对日期了吗?decision_log / version_history 只追加没改写吗?
- [ ] 上下文将尽 / 收尾,造交接卡 + 打印启动提示词了吗?(自传播,别断链)
- [ ] 交接卡过 `handoff_contract.py` 了吗?造卡日真实且不在未来，已完成项是具体产物/commit/决策定位而非模板占位，
  验证证据、下一步、必读文件和刷新现实禁令齐了吗?
- [ ] resume report 的 state hash 是当前重算值吗?handoff/hash 与 passport 是否冲突?
- [ ] memory item 是否只存最小项目状态、locator 与下一步?有没有完整聊天文本、PII、本机绝对路径、过长原文或 restricted/secret 值进仓库?
- [ ] 旧失败是否进 failure index?再次尝试是否有新 mitigation 或用户 override?
- [ ] 比较两条研究路线时，共同祖先、冻结准则、分支输入/结果 hash 和用户 merge 决策是否齐全?

---

## 名实对齐(诚实,不吹成卖点)

**真增量(v2 兑现,已 selftest + E2E)**:把"项目记忆"落成**可机器校验的台账纪律**——`memory_governance_gate`
核 resume hash、item 分层、artifact version、failure index 与采集策略；`check_project_card`
(绝对日期 / current_stage 枚举 / decision_log·version_history 行格式 / **交接链 parent_session 可达·无悬挂·无环**)、
`version_tag_reconcile`(version_history ↔ git tag 双向失配)、`check_bfact_freshness`(外部可变事实裸数值 / 快照超期)、
`memory_items.py`（项目条目的作用域、敏感级别、保留期、来源、替代链与可验证删除；拒绝 restricted/secret、PII、本机绝对路径、原始对话和过长原文）、
`handoff_contract.py`（拒绝未来造卡日期与占位“已完成”产物，要求具体产物/commit/决策定位及验证）、
`pm.py audit` 复用 passport 抓**孤儿 / 缺失 artifact**——汇成 `light.findings.v1`(producer=memory-pm)。
这些**机器校验**对标的 10 个真同类记忆 skill(claude-mem 83.8K★ / rohitg00 23.7K★ / Cline / Roo / hanfang /
agent-handoff…,见 competitors)**无一**有(它们要么 prose 纪律、要么华丽检索,但都不机检台账自洽);
**变更广播**(改事实源→算受影响材料→发 consistency 回扫)落成机制,不只口头说。**★ 跨 harness 确定性续跑**:
续跑汇报抽成 `resume_report.py` 单一真相源 + `pm.py resume` 命令,三 harness 跑同一份(CC hook 自动调、
Codex/OpenCode 经 AGENTS.md 约定调)——jayzeng/agentmemory 有近似的确定性 `context` 命令,但它是"记忆 dump",
Light 报的是**机器校验过的 DAG 项目态**(阶段/门/stale 重验)，并展示、重算
`light.passport.v3` 的 canonical state hash，篡改不静默。
**确定性续跑 × 机器校验台账,二者合一**是当前实装组合；竞品覆盖范围随版本变化，不宣称永久唯一。

**裸模型本就会的(不吹)**:"记住项目背景""会话开头先看上次进度""相对日期转绝对""决策要留痕""两层记忆模型"
——任意带记忆文件的方案都有,**近零增量**。Light 的价值**不是知道这些**,而是**把它们落成 `.light/` 显式文件 +
机读自洽门 + hook 确定性注入 + 变更广播**(脚本兑现,非 SKILL 喊话)。

**诚实落后项(已知没做到)**:
1. **无向量语义检索 / 无自动记忆抽取**(对标 mem0 / claude-mem):跨会话记忆靠 `.light/` 显式文件 +
   hook/命令注入 + **Grep 字面**检索;"同义不同词"会漏召回(如"级联误差抑制"↔"逐级不确定性消除");
   也**不自动抽取**事实(关键事实必须显式写)。**校正(Round 2 读 jayzeng/agentmemory 后)**:本地 embedding
   语义检索**可无 key**(其 `qmd` 用本地 all-MiniLM 实证),故不做的真正原因是**向量模型/二进制是重的非-stdlib
   依赖**,破坏"stdlib 优先 + 三 harness 零额外装",**不是"避 key"**。这是刻意取舍(可审计、不被 LLM 误删/误并),代价是要人维护。
2. **状态覆盖式更新会丢演化轨迹**:`project_card` 的 `*_status` 覆盖式改写,A→B 转移只在 decision_log 留痕
   (非结构化),未做 mem0 式"每次状态变更结构化保留"。
3. **校验是正则启发式,会漏 / 误报**:`check_bfact_freshness` 按关键词+数字识"可变事实"(生造指标名漏报、
   恰含数字的普通叙述误报);行格式 / 枚举校验同此局限;阈值(90/365 天)是经验默认可调。
4. **会话开头续跑——Round 2 已大幅缩小,但仍有 harness 自动程度差**:
   - **★ 已做到**:续跑汇报抽成 `resume_report.py`(单一真相源)+ `pm.py resume` **三 harness 通用确定性命令**,
     **仅凭 `.light/` 即出正确续跑**(项目/阶段/卡门/重验/下一步)——**已活体 E2E 验**(从无关目录、无 hook、
     无聊天记录,见 [`references/cross_harness_resume.md`](references/cross_harness_resume.md));CC hook 已改为
     **委托同一份**(非两套实现,DRY,selftest 含"hook 输出与命令逐字一致"防漂移断言)。
   - **仍诚实标的差**:① CC 由 SessionStart hook **harness 层自动**调(resume/compact 重跑、零人力);
     Codex/OpenCode **无 session-start hook**,靠 `AGENTS.md` 约定让模型**在会话开头主动跑该命令**——命令确定,
     但"何时触发"在 Codex/OpenCode 仍是模型读约定(非 harness 强制),故 CC 的"自动"程度更高。
     ② 本机 Codex CLI 0.138.0 / OpenCode 1.17.6 已装,但**守零-key 未跑 model 会话**;**已验**的是"命令仅凭
     `.light/` 能续上"(harness 无关),**未在真 Codex/OpenCode model 进程里端到端验**自动续跑——如实标,
     **绝不声称"三 harness 都已实测自动续跑"**。
5. **账本自洽门 ≠ 科研内容门**:`pm.py audit` 产的 findings 只判台账自洽,**不判科研质量**;故**不进 STAGE_GATES
   常开阻断**,只在交接 / 投稿前按需聚合。别把它当 C1/C2 用。
6. **变更广播只算"该回扫谁"+ 发指令,不自己审计**:查不一致是 consistency 的事(职责分离,不重复造审计)。
7. **无项目目录的轻对话不落交接卡**:只打印启动提示词(记忆无处安放,靠提示词单件传状态)。
8. **结构化条目仍非自动召回系统**：`memory_items.json` 让删除、过期、作用域和来源可审计，但不做向量检索、
   自动抽取或隐私分类；敏感检测只是窄启发式，用户仍须把私人/受限材料留在仓库外。

---

## 参考(三级渐进披露:需要时再读)

- 对标真相源:[`docs/competitors/memory-pm.md`](../../docs/competitors/memory-pm.md)(**10 真同类 skill**(Round 2 补)+ 机制对标 + 五问提炼 + 超越点 + 诚实边界)
- 复用引擎:[`../light-orchestrator/scripts/passport.py`](../light-orchestrator/scripts/passport.py)——DAG 台账,`--help` / `--selftest` 即接口(**不重造**)
- 本技能引擎:[`scripts/pm.py`](scripts/pm.py)——`init` / `audit`(`--report` 产机读门)/ `broadcast` / **`resume`(跨 harness 续跑)**;`--selftest` 即接口
- 续跑汇报单一真相源:[`scripts/resume_report.py`](scripts/resume_report.py)——纯 passport 依赖;`pm.py resume` 与 CC hook 皆复用它(DRY);`--selftest` 即接口
- 校验器:[`check_project_card.py`](scripts/check_project_card.py) / [`version_tag_reconcile.py`](scripts/version_tag_reconcile.py) / [`check_bfact_freshness.py`](scripts/check_bfact_freshness.py)
- 交接卡合同:[`handoff_contract.py`](scripts/handoff_contract.py)——链可达之外，核日期不在未来、已完成定位非占位，
  以及卡片是否自包含到足够接续。
- 项目记忆条目:[`memory_items.py`](scripts/memory_items.py)——普通 JSON，不是数据库；支持 init/add/delete/audit。
- 记忆治理门:[`scripts/memory_governance_gate.py`](scripts/memory_governance_gate.py)——`--selftest` / `--input` 即接口。
- 续跑 hook:[`../light-orchestrator/resident/session_start_resident.py`](../light-orchestrator/resident/session_start_resident.py)(**委托** resume_report,非重造)
- **跨 harness 续跑细则**:[`references/cross_harness_resume.md`](references/cross_harness_resume.md)(三 harness 确定性路径 + 与交接卡互补 + 诚实边界)
- 会话衔接细则:[`references/session_handoff.md`](references/session_handoff.md)(四类触发 + 两件套 + 自传播 + 链可追溯)
- 记忆文件模板:[`assets/`](assets/)——`project_card` / `decision_log` / `version_history` / `terminology` / `handoff_card` / `handoff_prompt`
- 受控 schema 模板:[`../light-consistency/assets/`](../light-consistency/assets/)(4 份;`pm.py init --with-consistency` 据此铺进 `.light/consistency/`)
- 总控接线:[`../light-orchestrator/scripts/run_checkpoint.py`](../light-orchestrator/scripts/run_checkpoint.py)(交接 / 投稿前可聚合本技能账本自洽门)
