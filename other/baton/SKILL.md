---
name: baton
description: '项目接力协作系统 Baton。用于 Codex、Cursor、Claude Code 跨会话与跨电脑维护同一项目的进度、记忆和 Git。用户说「上班啦」「下班啦」「继续工作」「保存设计规范」「完成」「更新项目文档」「Baton init」「修复 Baton」「看看项目状态」「一键验收」「释放工作区」「记录需求变更」「这个坑记下来」「这个决策记下来」，回复任务编号，或提出 Git 自然语言请求时必须使用。英文触发词语义等价。Slogan: Pass your project, not your context.'
---

# Baton —— 项目接力协作系统

## 定位

Baton 让不同 AI 在同一项目串行接力，保持需求、任务、代码、验证、知识与交接一致。用户说人话。

- **项目真相**：`docs/ai_memory/`（Git 同步）+ `.baton/config.json`/`.baton/manifest.json`（入库，跨机恢复门禁与管理清单）。tracked 记忆/状态和这两个 `.baton` 文件随 Git 移动，Codex/Cursor/Claude Code clone 后可直接上班/继续。`.baton/local/`、扫描/发布配置和 `version.json` 仅在当前设备保存，不进 Git。
- **最高事实**：Git / 真实文件 / 新鲜验证 > `state/*.json` > 交接/日报 > AI 自述。
- **执行方式**：三端直接按本 Skill 操作文件与 Git，不依赖后台服务。

## 核心原则

1. **事实优先级**：AI 说「已完成/已 push」不是证据。
2. **单写入者**：同时只有一个 AI 写入。上班查交接末条所有权；`ownership_conflict: true` 或 dirty 无法归属 → 只读。正常上班只允许 runtime `--clock-in` 以 Git ref CAS 竞争所有权，再事务写入本机 lock、`ownership=holding` 与上班 handoff；禁止手工拼装 ref/state/handoff。普通写动作前必须由 runtime 核对 `ownership=holding` 且 writer 非空，未持有即零写入阻断；唯一例外是官方 updater 在 `released + writer=null` 时通过 `--record-update-event` 写与当前 manifest 版本严格一致的更新事件。同一工作区在下班或释放前不得重新上班；无法确认则只读。
3. **交接最后写**：任务/知识/日报 → 索引 → handoff。
4. **历史只增不改**：只追加或标「已取代/已废弃」。
5. **凭据红线**：API Key/Token 不进 Git、Memory、日志、交接。
6. **完成≠下班**：完成是任务级；下班是工作日级。
7. **假成功是红线**：验证/复核/push/同步必须有命令输出或 SHA，否则 FAIL。
8. **查询历史先查索引**：先读 `state/archive_index.json` 按关键词取得路径与行号，再只读命中片段，禁止全量扫描 `docs/ai_memory`。handoff 超过 10 条 HO 时更早条目自动原文归档并登记；accept 成功后任务从 `tasks.json` 迁出到 `task_finished.md`；Markdown 文档按下文规则自动语义分卷。

## 授权与范围止损

1. **授权不外溢**：只做当前目标所需且已授权的动作。「继续/确认/启用测试」不等于新模块、新环境或额外维护。测试目录只允许本轮测试文件，不是安装依赖、改宿主/profile/权限或复制凭据的许可。
2. **授权证据四要素**：外部变更或越界前必须同时有目标、影响、恢复方式、本轮用户授权；缺一项停止。只接受本轮人工确认，不能声称宿主机械保证。`user:` 与 `lean_exceptions` 只是目标声明，不能单独证明授权。授权不得由执行者自报。
3. **Contract 预锁不得留空**：`contract_level` 必填，只允许 `FROZEN|BOUNDED|OPEN`。FROZEN/BOUNDED 必须非空 `allowed_paths`；未知范围必须显式 `OPEN`，写 `open_reason` 并获得本轮明确确认。历史文档中的「用户原话授权」只表示本轮人工确认，不写入 Git。
4. **外部变更单独确认**：npm/Skill/profile/凭据/真实外部系统变更，必须单独说明并获授权。范围一旦漂到修宿主、搭环境、更新第三方，立即刹车。
5. **最低成本验证**：静态证据 → 已有测试 → 授权目录隔离测试。失败不能自动升级方案：不得自行换成成本更高、权限更大的方式；先报告失败、已知结论、下一步新增耗时/权限，获授权后再继续。
6. **止损**：只删除本轮创建且路径已核实的临时产物；越界立即停止并如实披露；多 AI 共享目录时写入型测试不得派给另一 AI 操作真目录；无新证据的重复调用立即停，汇报已完成／未完成／阻塞点／唯一下一步。

## 口令

> **中英口令对照表（English trigger map）**：中英文语义完全等价。

| 中文口令 | English triggers | 文件/Git 动作 |
|---|---|---|
| 上班啦 | "clock in" / "start work" | 同步 Git、核对所有权、列任务 |
| 下班啦 | "clock out" / "end work" | 更新文档、提交、push、远端 SHA 核验 |
| 继续工作 | "continue work" / "resume" | 只读当前快照 |
| 看看项目状态 | "check project status" / "status" | 只读 Git、任务、交接和索引 |
| 保存设计规范 | "save design spec" | 更新 `ui_spec/` 与索引 |
| 完成 | "complete task" / "mark task complete" | 写完成证据并进入待验收 |
| 更新项目文档 | "update project docs" | 增量写入、自动分卷并更新索引 |
| 这个坑/决策记下来 | "remember this pitfall" / "record this decision" | 写现有 knowledge 与索引 |
| 加个需求 / 需求变更 | "add requirement" / "change requirement" | 更新 overview.md |
| Baton init | "Baton init" | 运行项目级安装并做后验 |
| 一键验收 | "run acceptance check" / "accept" | 按任务 DoD 验收并归档 |
| 拉取/同步/看 git | "pull github" / "sync github" / "check git status" | 执行对应 Git 动作 |
| 回复任务编号 | "reply the number" / task id | 选择任务并冻结 Contract |
| 异常接手释放锁 | "release workspace" / "I confirm the previous agent stopped" | 用户确认后释放所有权 |
| 任务验收通过 | "acceptance passed" / "accept" | 从待验收归档到 finished |
| 检查更新 | "check update" / "check for updates" | 读源码/安装镜像版本 + 实查远端 |
| 更新 Baton | "update baton" / "upgrade baton" | 通过固定公开仓库最新稳定标签更新用户级与当前项目 |
| 修复 Baton | "repair Baton" | 官方更新 → 用户级/项目级重装 → init/Doctor 后验 |

### 上班啦（clock in / start work）——两步

上班不做版本锚预检、不联网查版本、不生成统计或月报，也不搜索聊天历史、外部 Memory 或 rollout；当前 Git 与项目真相足够时禁止旁路查历史。

1. **一次 Git 事实**：`git fetch <remote> --prune`（有 upstream 时必须先成功 fetch）+ 同一次调用读取 branch / HEAD / status / tracking ahead-behind。失败预算一次：解析/网络/SSL/凭据失败即停，报告 `sync_blocked`，不抢锁、不读 tasks/handoff。本地落后无分叉只允许 `git merge --ff-only`；同步完成前不得把任务表当开工依据。禁止覆盖 dirty、reset、rebase、擅自 merge/解 divergence，也禁止先查历史。
2. **一次读取 + 原子上班 + 任务表**：读 `current.md`、handoff 末条、`tasks.json`。若 dirty，先且只调用 `.baton/runtime/baton-closeout.mjs --project <根> --check-update-receipt`：`recognized=true` 且 state/handoff 已释放时，这是 updater 已证明的官方更新待收口，可正常接班，不要求异常接手，也不再定位源码或展开全量 diff；若同时 `event_recorded=false`，立即补一条更新事件后继续。其余 dirty 仍按来源不明只读处理。交接他人持有、state holding、HEAD 非祖先或分支不一致同样只读；用户确认上一代理停止后才异常接手。确认可接班后，把 `{"writer":"Codex","markdown":"### HO-..."}`（writer 按当前执行者取 Cursor / Codex / Claude / workbuddy / 未知）作为 stdin JSON 交给 `node .baton/runtime/baton-closeout.mjs --project <根> --clock-in`；Windows Codex 中该命令会写 Git ref，必须首次就申请主机权限，禁止先在沙箱试跑再重试，权限失败须原样报告 `ownership_ref_write_failed`，不得解释为所有权冲突或要求异常接手。只有 exit 0 才获得写权限，并发失败方必须保持只读。禁止手工拼装 `git update-ref`、`project_state.json` 或上班 handoff。最后直接输出任务表，禁止重复读取或重复门禁。

### 下班啦（clock out / end work）——四阶段

每阶段记录起止耗时；超过 120 秒立即报告当前阶段，不无声等待。

> **标准授权**：“下班啦”口令本身即授权当前项目当前分支的标准 closeout commit、push 与远端 SHA 核验；不得要求第二次确认。该授权不包含发布、tag、npm、跨仓、切分支、force push、历史改写或其他范围扩大，任何非标准目标仍须单独授权。
>
> **审批证据**：需要主机权限时直接发起实际工具授权。只有实际工具拒绝时才能报告拒绝，并必须保留原始错误与审批证据；未调用工具不得声称发生审批拒绝。

1. **增量兜底**：阶段节点、决策和坑点应在发生时落档；下班禁止扫描历史或回放全天。只允许补当前轮最后一小段遗漏，不能首次补写更早阶段；没有则零写入。
2. **文档事务**：持有状态下先运行 `--prepare-closeout-state`，把当前 branch、提交前 HEAD、dirty、tracking SHA 与 `pending_closeout_verification` 写为明确的**提交前快照**；tracked 文件不得把自身所在提交伪装成最终 commit SHA。随后只更新尚未随任务节点落档的 tasks/current，再把单个完整 HO 作为 stdin JSON `{"release":true,"markdown":"### HO-..."}` 交给 `node .baton/runtime/baton-closeout.mjs --project <根> --append-handoff`。CLI 在任何 tracked 写入前核对 state、Git ref 与本机 lock：三者一致才收口匹配锁并释放 ownership/Contract；旧式项目 ref/local lock 同时不存在时保持兼容；只存在一边或归属错配则零写入阻断。随后自动轮转并原子追加，机械保证 **handoff 末条最后写**；相同 HO 在 released 状态重试只读幂等。禁止直接补丁编辑 handoff。该调用必须是本次 tracked 文档的最后写入。执行者只写 Cursor / Codex / Claude / workbuddy / 未知；current.md 修订表最多 3 个日期、每日一行。
3. **一次门禁 + 一次 commit**：用一次组合快照核对远端、凭据、配置、活动 Contract、允许/受保护路径和所有权；成功项禁止重复核验。已由 update receipt 证明的管理面不得再次定位 canonical、重算整套 managed hash 或检查无关历史 Contract；无活动卡时发现旧元数据差异只报告，不在下班顺手修。通过后精确 `git add`，只运行一次 `--check-staged`，再一次 commit。GitHub HTTPS 与 `ssh.github.com:443` 的同 owner/repo 是正常等价，不得渲染为异常。
4. **一次网络收尾**：`git push` + `git ls-remote` 实查远端 SHA == 本地 HEAD；必要时 GitHub 回退 `gh api`。两通道都不可用即 FAIL，不接受声明式通过。通过后把最终本地/远端 SHA 写入 `.baton/local/push-verified.json`，不产生 tracked 改动；Git 与该本机回执才是最终终态，`project_state.repository` 仍是提交前快照，状态查询不得把它当当前 Git 事实。

单分支工作流：在哪个分支上班就在哪个分支收尾，不切分支、不 merge、不建任务分支；多分支并行由用户自行管理。

### 继续工作 / 状态 / 其它口令

- **继续工作**：只读快照（git + current + handoff 末条 + 未完成任务 + 索引最近条）+ 下一步。不写锁、不重跑 clock_in。
- **看看项目状态**：只读六层快照，不写文件。
- **保存设计规范**：已确认设计写入 `ui_spec/`；冲突旧版标已取代。FROZEN UI 必须以它做 Fidelity 比对。
- **完成**：① finish → 待验收（todo/progress 表行移除，DoD 证据「命令 → 结果」）；不 commit。② 用户验收 → `action=accept` 从 `tasks.json` 迁出到 `task_finished.md`。无有效执行证据或证据行占位 → 拒绝，保持待验收。
- **更新项目文档**：增量写入后停止（中途存档，不跑下班）。
- **阶段自动落档**：任务选择、需求/设计变更、阶段节点、里程碑和完成状态在发生时更新现有文档；持有状态下，阶段节点/已确认决策/已验证坑点立即调用 `--record-event`，即时自动写入日报/knowledge/索引。官方 updater 在 released 状态只调用受限的 `--record-update-event`。异常接手成功后必须先记录事件、再写持有中 handoff；禁止拖到下班。存疑先询问，不新建第二套记忆。
- **需求变更**：更新 `overview.md`，历史只增。
- **Baton init**：在业务项目运行 `baton-install.ps1 -Scope Project -ProjectRoot <根>`。只补齐缺失骨架，不覆盖已有项目文档；自动创建/刷新三端 Skill、入口和 `.cursor/rules/baton.mdc`；写配置前剥离远端 URL 中的凭据；不猜配置、不写 version.json。重跑安装必须补回缺失的 Cursor 规则。
- **数字确认**：编号 = 任务表 ID 列，一一对应；支持连写如 `1234` 按顺序全部执行。禁止反问「您指的是任务 1 吗」。手工更新 `tasks.json` 的 `current_task_id` 与契约字段并执行同一门禁。
- **Git 自然语言**：在当前授权范围内执行 status/commit/fetch/push，不额外建立任务 Contract。连接 GitHub 前先从目标远端解析 owner，再执行 `gh auth switch --hostname github.com --user <owner>` 自动切换到对应的本机已登录账号；随后核验当前账号等于 owner，失败即停止。commit 的 author/committer 继续使用目标仓库的 repo-local Git 身份，禁止用全局身份覆盖其他账号的仓库。
- **Git 输出降噪（仅展示过滤）**：执行 Git 命令时必须捕获完整 stdout/stderr 并保留原始退出码。仅当命令 `exit=0` 时，才允许从用户可见输出中过滤单独一行、且精确匹配 `warning: unable to access '<当前用户目录>/.config/git/ignore': Permission denied` 的提示；最终摘要不得复述该行中的本机绝对路径。`exit!=0` 时必须保留完整输出（包括该行）；任何其他 warning、stderr 或 error 始终保留。此规则只改变展示，不得修改 Git 配置、ACL、ignore 文件或用户目录。
- **结果措辞**：只有阻断使用或验证失败才写“FAIL / 缺陷 / 异常”；已自动处理的状态差异写“已处理”，协议等价或普通提示不得包装成问题。
- **检查更新**：源码仓以 `package.json` + HEAD 为准；npm/公开库只在本口令后实查。用户级 Skill 缺失时即使版本号相同也必须恢复（`--restore-user`）。
- **更新 Baton**：当前用户目录 Windows 优先 `USERPROFILE`、其他用 `HOME`，记为 `$HOME`。标准更新先运行当前项目 `.baton/runtime/baton-public-update.mjs --project <根>`；项目引导器缺失时只回退运行 `$HOME/.baton/runtime/baton-public-update.mjs --project <根>`。引导器固定从 `https://github.com/kakadeka/Baton.git` 选择最新稳定语义版本标签，克隆到系统临时目录，核验远端、标签、包名与版本一致后才委托 updater 刷新用户级与当前项目；标准更新不读取 `$HOME/.baton/source.json`、不检查 `$HOME/Baton`、不使用 npm，也不得隐式回退到本地源码。Git 获取或校验失败必须在目标写入前停止并清理临时目录。标准用户更新成功后只核对公开 tag/version、updater 的 `source_preflight`、写后回读、manifest/受管文件哈希与 update receipt；`scripts/check-drift.mjs` 是维护者源码仓开发/发布门禁，公开运行时不包含，禁止在业务项目目录调用或把它作为用户更新成功条件。明确的「更新 Baton」口令本身即授权这一标准范围；说明覆盖面后直接申请必要的主机写权限并执行，不再要求任务编号或第二次确认；非标准目标或范围仍须单独授权。非 dry-run updater 只检查本次精确更新载荷：Git checkout 中载荷必须全部被 HEAD 跟踪且内容干净，任一载荷缺失、未跟踪或 dirty 必须在目标写入前阻断；非 Git 官方包必须通过包名与可信普通文件完整性检查。更新源项目的 Baton ownership、Git ownership ref 与本机 lock 不限制只读消费干净载荷。项目 updater 完成时立即记录更新事件，并在 `.baton/local/update-receipt.json` 写 HEAD、版本、dirty 路径及内容 hash；回执只供下一次上班机械识别官方更新，不进 Git。仅当现有有效回执已按 HEAD、当前 manifest 版本、完整 dirty 路径与内容 hash 精确证明全部修改时，允许在该官方 dirty 上幂等重跑 updater：已成功事件必须复用，最终完整 dirty 集合必须重写回执；任何回执外路径或内容变化都须在写入前阻断，不得覆盖有效回执或误导用户异常接手。
- **更新本地 Baton 开发版**：只在用户明确说出这个口令时，才读取 `$HOME/.baton/source.json` 指向的本地开发 checkout，验证 `package.json.name=@kakadeka/baton` 和精确更新载荷后运行其中的 `scripts/baton-update.mjs --restore-user --project <根>`。定位器缺失或无效即停止，不回退 `$HOME/Baton`、公开下载或 npm；该开发入口永远不是标准更新的隐式回退。
- **修复 Baton**：优先运行上述固定公开仓库标准更新，再执行用户级/项目级重装、init 与 Doctor 后验；公开引导器缺失时按 README 的首次安装步骤恢复引导器后停止并重新开会话，不改业务代码，也不改用本地源码兜底。
- **换电脑恢复**：A 机提交并 push 后，B 机 clone/pull 项目；Codex/Cursor/Claude 直接读取 Git 中的项目 Skill、`config.json` 与 `manifest.json` 后上班。缺用户级 Skill 但项目引导器存在时运行 `.baton/runtime/baton-public-update.mjs --project <根>` 恢复用户级；项目引导器也缺失时按 README 的首次安装步骤恢复。缺 `.baton/config.json`、三端 Skill 或 `.cursor/rules/baton.mdc` 时执行 `Baton init`。
- **释放工作区**：仅用户确认上一代理已停止后 release。

## 任务分类与 Contract 三级

Contract 在开工时固定三要素：①级别 ②范围 ③验收标准。有原型/设计规范/冻结需求必须 **FROZEN**，禁止把明确需求当 OPEN。范围外只能 `user:<路径>` + 当次授权。

| 级别 | 含义 | 例子 |
|---|---|---|
| FROZEN | 用户已确认的需求/原型/设计，禁止自由发挥 | 按冻结稿实现 UI |
| BOUNDED | 明确范围内实现 | 普通功能 |
| OPEN | 真探索，须 open_reason + allowed-once | 未知目录先探路 |

任务体量（与 Contract 正交）：Micro、Bounded、Complex、Architecture、High-risk。High-risk 数据/发布/安全须用户授权；仅高风险、架构或 Contract 明确要求时需独立证据复核。

`select` 另有可选的 Lean 策略 `implementation_policy`（`off|lite|full|strict`，省略时按任务类型自动选）。`full` 只在收尾回执里报告新增文件/依赖/抽象；`strict` 会把它们与预算比对，超限即在收尾阶段阻断——解法是与用户确认后重新 `select` 同一任务并登记 `lean_exceptions`，执行者事后自报无效。判定细则见框架仓 `baton-lean-review`。

## 审查与防跑偏

- 审查者只看真实 diff / 验证输出 / Contract / protected / 未验证项，**不重新开发**。
- 执行前：有原型一律 FROZEN；allowed_paths 限定范围。
- Fidelity 必须对照冻结需求/原型/`ui_spec` 输出差异清单，偏差即 FAIL。
- 高风险、架构或 Contract 要求独立证据复核时，缺少对应证据 = FAIL。
- 精简审查/技术债扫描不在默认安装；需要时显式使用框架仓 `baton-lean-review` / `baton-debt`。

## 任务表格式 + 简报模板

**所有需要用户选择、确认、验收或决定下一步的回复，结尾必须输出任务表**；上班、状态、诊断、阶段结果和完成结果不得退化成只有项目符号。多个独立选项允许连写编号（如 `1234` 按 1、2、3、4 全部执行）。没有可选动作时也输出一行状态表，确认口令写「无需回复」。

| ID | 任务 ID | 任务名称 | 说明 | 建议 | 备注 | 确认口令 |
|---|---|---|---|---|---|---|
| 1 | DC-YYYYMMDD-NNN | 推荐事项 | 当前状态与影响 | 推荐 | 范围、风险或依赖 | 回复 `1` |

简报：

- 任务开始：任务类型｜执行者｜修改范围｜验收标准。
- 任务结束：完成情况｜关键验证｜复核结果｜Git 状态｜是否已同步远端｜下一步。
- 下班结束：验证/复核结果｜文档更新｜commit 数｜push 结果｜**远端 SHA 是否与本地一致**。

## 目录结构 + 文档规范

```
docs/ai_memory/     ← 长期真相（Git 同步）
  index.md  current.md  commands.md  handoff_current.md
  overview.md  constraints.md  validation_matrix.md
  state/{project_state.json, tasks.json, archive_index.json, decisions.jsonl, issues.json}
  tasks/{task_schema, task_todo, task_progress, task_finished}.md
  knowledge/{tech_decision, pit_experience}.md
  ui_spec/*.md  daily_log/  archive/handoff_YYYY-MM.md  plans/
.baton/             ← config.json + manifest.json 入库；local/、private-patterns、publish-identity、version.json 本机私有
```

长期 Markdown 必须含【归档分卷索引】与【修订记录】。每次文档写入后自动检查分卷，无需用户确认：128KB 是软目标，优先在 116–140KB 的完整章节或完整记录边界分卷；不得切断代码围栏、表格、列表完整条目、HO/ADR/任务记录。范围内无安全边界时允许超过 140KB 延伸到下一个完整边界，并在索引记录原因。JSON/JSONL 状态绝不文本分卷。写档顺序：具体文件/分卷 → 文件内索引与 `archive_index.json` → handoff 最后写。

| 文件 | 修订记录 | 写法 |
|---|---|---|
| current.md | ✅ 最多 3 日 | 当前事实简写 |
| handoff_current.md | ✅ | 最近 ≤10 条 HO，更早进 archive |
| tasks.json | 机器 | 无 completed/cancelled 残留 |
| task_finished.md | 追加 | accept 迁出的全文 |
| knowledge/*.md | ✅ 追加 | 已验证决策/坑点 |
| ui_spec/*.md | ✅ | 设计分册，冲突标已取代 |
| daily_log/ | 天然追加 | 标题含动作｜关键词｜东八区时间｜执行者 |

## 红线 + 失败恢复

1. 凭据红线：密钥不进 Git/Memory/日志/交接。
2. 危险 Git 禁止：force push / reset --hard / 危险 clean / 未授权 rebase / 丢弃 dirty。
3. 远端 SHA 核验：`ls-remote` == 本地 HEAD 才报下班完成。
4. FROZEN 不得自由发挥；扩大范围无授权即 FAIL。
5. 顺手工程：擅自改架构、顺手大重构、删除成熟功能、无关格式化、每遇 Bug 就推倒重来。
6. 假成功：无命令输出/SHA 却宣称验证/push/同步。
7. 假 Fidelity / 假 Reviewer。
8. 把项目记忆 push 到公开库 `kakadeka/Baton`。
9. 未授权安装依赖、改宿主/profile。
10. 测试目录授权扩大成环境修改权。
11. 已有结论仍重复调用且不增加新证据。

失败刹车：同一根因两轮有证据尝试失败 → 停止编辑、不擅回滚、标阻塞、给一个诊断动作。汇报固定为「已完成／未完成／阻塞点／唯一下一步」。平台切换、长任务、高风险操作前写检查点（HEAD、修改文件、已验证、未验证、唯一下一步）；检查点不释放工作区。异常接手只读清点，不删不滚不提交。
