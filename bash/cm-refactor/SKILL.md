---
name: cm-refactor
description: 用户明确要求“只整理结构，不改变行为”时使用。执行边界分流、行为判官、分批重构和独立审查；缺陷修复转交 cm-fix，新增或变化的业务行为转交 cm-prd。
---

# cm-refactor — 重构闭环（行为保持）

执行前读取 `../../runtime/project-context.md`、`../../runtime/orchestration.md`、
`../../runtime/review.md`、`../../runtime/model-efficiency.md` 与
`../../runtime/logging.md`。Codex 入口为 `$cm-refactor`；Claude Code 跨平台入口为
`/cm-refactor`，macOS/Linux 另有历史别名 `/cm:refactor`。

用户明确要求外部专家，或为本次重构开启 AUTO 时，按
`../../runtime/external-expert.md` 执行 `../external-expert/SKILL.md` 的任务路由。
重构写入、行为判官与审查保持 LOCAL；复杂方案比较可 CONSULT，权威事实可 VERIFY。
外部结果只进入候选方案和风险清单，不得修改行为基线、代跑判官或满足独立审查。

**用法**:`$cm-refactor {specs路径} {代码项目路径} 重构目标描述(哪块代码/为什么难维护)`

## JS 只读分流

在读取项目内容、解析角色、写 `run_start`、建立行为基线或修改代码前，先确认本轮有非空目标描述，
并按下方“分流门”将意图归为 `defect`、`behavior-change`、`gradual-adoption` 或
`structure-only`；不要把描述正文拼进 shell。随后执行：

```bash
node "{CM_WORKFLOW_ROOT}/scripts/cm-refactor-entry.mjs" \
  --skill-dir "{CM_WORKFLOW_ROOT}/skills/cm-refactor" --project "{CODE_PROJECT}" \
  [--specs "{SPECS_DIR}"] --intent "{四类意图之一}" [--target-present]
```

没有 specs 的裸项目省略 `--specs`；有非空描述才传 `--target-present`。缺描述时入口返回
`blocked / target_required`。`defect`、`behavior-change`、`gradual-adoption` 分别只返回既有
`$cm-fix`、`$cm-prd --change`、普通改动出口并停止本流程，出口不构成执行授权；只有
`structure-only` 才继续校验项目/specs，`ready / g0_feasibility` 才进入 G0，且继续要求行为完全不变
与 G0 人签核。返回的角色、日志和
Learning 均为 `pending`，执行/写入权限为 false；入口不读取项目正文、不跑判官、不调用
provider/browser/外部专家、不写日志/档案/RULEBOOK，也不替代后续轻量道或批量道。

### JS 流程执行

只读分流返回 `ready / g0_feasibility` 后，按 [当前会话 JS 宿主](references/js-host.md)
启动同一轻量/批量控制器；[批量、准备、写回与恢复协议](references/js-batch.md)在需要时读取。
JS 宿主负责日志与状态，不再手工重复写 `run_start`。恢复保留原配置、结果和审查轮次；未知调用先核对。
批量默认串行、worker 只提议文本；真实宿主须保证 bakeoff 隔离和最终独立审查，不能用 header 自证。

不使用 JS 宿主时，两个路径校验通过后立即调用统一写入器记录 `run_start`；暂停/续跑沿用同一
`.cm-run.json`，完成收口人门后写 `run_done`。不得直接拼 JSON。

## 项目角色路由

从代码项目根解析 `coder`、`tester`、`reviewer`，并按
`runtime/workflow-routing.md` 写 `decision`/`phase: route`。角色配置只选择请求的
实现、等价验证和独立审查适配器/模型别名；它不允许子代理提交 Git、改变规则手册、
跳过判官或把 `declared-adapter` 当成已执行。resolver 返回非零或配置错误时立即
`BLOCKED`，不得进入 G0、扇出或修改代码；配置缺失时使用当前默认执行方式。
`managed-adapter` 按 `runtime/model-efficiency.md` 返回文本建议并自动记录真实 usage；
行为基线、代码改动与独立审查仍保持本地。

角色调用按 `runtime/model-efficiency.md` 只传当前批次的行为基线、范围、diff、验证与
审查证据；不得重复发送其他批次或完整历史。精简仅影响模型上下文与输出，不降低
行为判官、独立审查或回归门禁。

结构调整专用闭环。**前提:什么都没坏,行为一丝不变**——设计依据见 `docs/重构流程设计/`(cm 小闭环纪律 × Anthropic 迁移方法论,核心教义:修规则,不修产物)。

**分流门(先于一切,答错门就是错流程)**:

- 有缺陷要修 → `$cm-fix`
- 行为要变(哪怕"变得更合理")→ `$cm-prd --change`
- 渐进式采用(如 JS→TS 逐文件、加类型注解)→ 不用本命令,直接改
- 结构问题且行为保持 → 本命令

**$cm-ai 全局规则同等生效**：灾难级才暂停、多方案自主决策留痕、状态落盘（node 写 `REFACTOR`）、运行日志照记、审查按 `runtime/review.md` 执行。

**续跑检测(先于 G0)**:`{SPECS_DIR}/refactors/` 下存在未收口 slug(档案无收口节 / 运行日志该 slug 无 `run_done` 事件)→ **按磁盘状态定位续跑站点**(RULEBOOK 版本、batch-log 完成集、队列缺口),G0 不重问、判官按 G0.5 重验后继续;无在制状态才走全新 G0。"队列=磁盘"的可恢复性必须有恢复入口才算数(对照系:cm:ai 有 tasks 断点、fix 有 slug 续跑,最长时的批量重构反而没有——本条补齐)。

## G0: 可行性(人门)

1. **动机量化**:动机必须落到可测指标——行数超限 / 重复块 N 处 / 依赖方向违规 / 圈复杂度。"代码不优雅"不构成动机
2. **认领待触发备忘**:扫描 `{SPECS_DIR}/LESSONS.md` 的「待触发备忘」段,结构类条目(标记来源含"重构/拆分/看不惯")与本次目标相关的 → 列入范围并在输出注明认领;收口时销账(改状态为已认领,注档案路径)——备忘的回流出口(实跑教训:备忘只写不读,到期无人认领)
3. 波及面:谁引用这块代码(有业务地图查 03/08,无地图 grep 调用方)
4. 输出可行性摘要:范围清单 / 动机指标现值 / 波及面 / 预估轨道(轻量或批量)/ **预算可见乘法**(批量道必填:文件数 × 单文件估耗 = 总预算,拍脑袋的总数不作数)。**「不重构」是合法结论**——收益盖不住风险就明说,命令到此收口
5. **🛑 人签核后才进下一步**(签核=踢下一阶段;阶段内不再停车)

## G0.5: 判官自验证(无判官不开工)

判官 = 能平等裁决改前改后代码的机械标准,分两层:

- **基线层**:存量测试全量跑绿并记录;无测试资产 → 先写现状快照测试(B3 同款,锁行为不判对错)
- **差分层**:对将被重构的入口函数/接口,构造代表性输入集(含边界值),记录改前输出;**harness 的环境解析照抄项目既有测试的做法**(依赖怎么找、浏览器怎么起)——自造解析必踩环境坑(实跑:playwright 全局安装,裸 import 失败,照抄 smoke.mjs 的 npm root -g 解析才通)(实证方法:12 组输入逐字节对比,json-keeper 拆 core.js 验证过)

**自验证(判官没被验证过,就不配当判官)**:

- 在**原代码**上跑 → 必须全绿
- 在**故意破坏的代码**上跑(手动种 ≥2 处行为变异,如改一个返回值、删一个分支)→ 必须变红;**不红的判官修到红为止**,变异恢复后再开工
- 判官报大面积失败时先怀疑判官(比较器空白处理/序列化陷阱是已知假阳性源),"一个把所有东西都判失败的裁判,通常是它坏了"

## 规模门(客观判据,不是感觉)

- 范围 ≤3 个文件 且 无跨模块搬迁 且 无文件增删 → **轻量道**
- 其余 → **批量道**
- **版本控制 = none → 禁入批量道**(批量改动无 git 回滚是裸奔):只许轻量道并输出强警告,或建议先 git init

## 轻量道(五步,一次跑完)

1. **重构**:只动结构不动行为;**禁止顺手修 bug**(与 N3"禁止顺手重构"互为镜像)——发现缺陷 → 停下记录现象与位置进档案,收口后走 `$cm-fix`。夹带修复会毁掉差分判官:行为变了,是重构失手还是修复生效?无法归因
2. **等价验证**:基线全绿 + 差分逐项一致;**任何行为差异 = 该步失败回滚**——"差异其实更合理"也不例外,那是行为变更,走 prd --change 立项后再做
3. **审查**：执行下方「结构化审查门禁」；重点检查有无夹带行为变更、结构是否真的改善、差分覆盖是否充分
4. **落盘**:档案 `{SPECS_DIR}/refactors/{YYYYMMDD}-{slug}.md`(动机指标改前改后对照 / 等价验证方式与结果 / 发现未修缺陷清单);METRICS 行 Feature 列写 `refactor`;delivery=diff 不提交，branch/draft-mr 才 commit `refactor: {一句话} (档案: refactors/xxx.md)`
5. **规则毕业**:本次收敛出的持久约定(如"路由文件导出形态")→ 写进代码项目 `.claude/rules/` 对应文件——一次重构的规则,变成项目的永久基因;**项目无 `.claude/rules/`(未经 $cm-init)→ 降级记入 LESSONS `[仅记忆]` 并在档案注明,提示补跑 $cm-init 后迁入**(实跑 DEV-003:diff-lens 未 init,毕业规则无处可去)

### 结构化审查门禁（两条轨道共用）

`{slug}` 先规范成跨平台安全的 ASCII kebab；令
`REVIEW_FEATURE=refactor-{slug}`、`REVIEW_TASK=T-REFACTOR-{slug}`。主执行者按真实
diff 和判官证据写
`{SPECS_DIR}/.reviews/refactor-{slug}-T-REFACTOR-{slug}-a{attempt}-handoff.json`，
先按完整 `changed_files` 运行
`cm-task-gate.py hash-implementation --project-root {CODE_PROJECT} --file ...` 并把返回的
`implementation_sha256` 写入 handoff，然后真跑：

```bash
python3 {CM_WORKFLOW_ROOT}/scripts/cm-task-gate.py check-n4 \
  --handoff {HANDOFF_PATH} --reviews-dir {SPECS_DIR}/.reviews \
  --feature refactor-{slug} --task T-REFACTOR-{slug} --project-root {CODE_PROJECT}
```

独立审查投喂全部 diff + RULEBOOK（批量道）+ judge-report/diff-report 摘要；凭证严格落
`{SPECS_DIR}/.reviews/refactor-{slug}-T-REFACTOR-{slug}-r{attempt}.md` 并绑定当前
handoff SHA。审查后必须真跑：

```bash
python3 {CM_WORKFLOW_ROOT}/scripts/cm-task-gate.py check-n5 \
  --handoff {HANDOFF_PATH} --reviews-dir {SPECS_DIR}/.reviews \
  --feature refactor-{slug} --task T-REFACTOR-{slug} --project-root {CODE_PROJECT}
```

只有当前 attempt 的 `verdict: approved` 才能落盘/提交；`changes_requested` 生成
attempt 2 并复审，第 2 轮仍有阻断项写 `blocked`。旧凭证、空壳凭证或文件存在检查
均不得放行。

第一轮要求补判官或测试时，审查返回 `judgeRevision:{paths,reason}`，只列启动时
`testSetup.paths` 内的文件；第二轮由宿主提议文本、控制器登记写入。先在启动时的业务原稿上
重建答案并重做判官自验证，再与第二轮重构稿比较；详见 [判官修订与恢复](references/js-host.md#第二轮判官修订)。

## 批量道(五站 + 三条修上游回环)

> 教义:个别失败交给循环烧掉,**重复失败控诉的是规则**——修规则重新生成,不修产物。

### 站 1: 规则手册

- 建 `{SPECS_DIR}/refactors/{slug}/RULEBOOK.md`,meta 规则:**两个 agent 会答得不同的问题,答案进手册**(目标形态/命名映射/禁用模式/逃生舱标记 `TODO(refactor):`)
- 依赖图定批次顺序(文件粒度 + 模块粒度都查环)
- **手册在循环内只读**:任何批内 diff 碰 RULEBOOK = 自动审查发现;修订排队给人,批间应用

### 站 2: 压力测试(人门)

- **双译对比(bakeoff)**:同 2-3 个最难的文件派两个隔离 agent——一个严格守 RULEBOOK,一个**从不知道手册存在**;第三个 agent 逐处 diff,每处差异裁决为「规则正确 / 规则缺失 / 规则错误」——差异清单就是规则修订清单(比"跑一遍看看"锐利:每个 diff 都是对某条规则的判决)
- 只要有一项裁决为规则缺失或规则错误，返回的手册在忽略行尾空白、换行符风格及首尾空行后就必须不同于对比前的手册，否则以 `refactor_rule_revision_required` 停机、不发布对比报告也不启动试点，修订是否解决问题仍由后续独立审查判断。
- 试点:按批量道管线原样跑通(含站 3 禁令与站 4 裁决);**试点产物可弃,唯一留下的是规则修订**
- 采样规模:批量 ≥10 单元 → 取 2-3 个最难文件;<10 单元 → 取 ⌈20%⌉ 且至少 1 个;偏离记偏差日志(实跑 DEV-001:5 单元取 1,规程数字对小批不成比例)
- 🛑 规则定稿人签核后才扇出

### 站 3: 批量执行

- **队列 = 磁盘**:完成的客观定义是"该文件的重构产物存在且通过站 4"——可恢复、可并行、不靠记忆
- **配置禁令**：开跑前读取 `{CM_WORKFLOW_ROOT}/templates/refactor/cm-refactor-denies.json`，将其约束注入每个 Codex 子代理：循环内禁 git 变更操作、禁重型测试命令。当前运行时无法保证这些边界时**不扇出**
- 扇出时按 `runtime/orchestration.md` 为 Codex 子代理注入对应工种 skill 与 RULEBOOK 摘录；子代理只做指定文件、不碰界外、不自行标记或提交
- 当前 Codex 运行时支持模型分层时，机械实现可用成本较低的模型，独立审查与规则修订保留高能力模型；不支持则使用当前模型，不将分层作为硬依赖
- 每个完成文件末尾带状态尾注 `// REFACTOR STATUS: confidence={high|medium|low} todos={N}`;审查者对账实际 `TODO(refactor)` 数,**尾注少报即为审查发现**
- 提交在批次边界由主流程执行,循环 agent 不 commit

### 站 3.5: 装配(主流程职责,不派 agent)

- 按各单元 delta 清单执行**编排层改写**与**加载登记类波及物**(HTML script 注册 / 打包白名单 / 构建清单);agent 汇报的「需其他工种配合」在本站**强制逐条消费**,漏项即偏差记 DEV
- 装配产物(编排层 + 登记文件)与模块产物**同等过站 4-5 判官链**——装配是全程唯一无规则手册护航的手写高危区(实跑:全程唯一真 bug 出自装配期,root 缺绑定,站 5 拦截)

### 站 4: 机械裁决

- **裁判有价格,价格决定位置**:typecheck/lint 便宜 → 进每文件循环;整体构建/重型测试贵 → 批末跑一次,错误清单按模块切片成下一批队列
- **同类错误第 3 次出现 = 规则 bug**:停止修实例 → 修订 RULEBOOK(排队人批)→ **重新生成该批**,不手工补丁(手工补丁让第 500 个文件和第 5 个文件长得不一样)
- **批间的一切规则驱动重生成/规范化变换视同新产物,必须重过站 4-5 判官链**——机械变换是上下文盲的(实跑:挂载行统一变换把 `root.` 写进无 root 绑定的 IIFE,启动即挂,站 5 金样前的 smoke 拦截)

### 站 5: 行为等价

- 判官上场:基线全量绿 + 差分全组一致;差异 = 回滚该批重做
- 判官报异常先按 G0.5 自验证复查判官本身,再信判决

### 收口(同轻量道 3-5 + 追加)

- 先通过「结构化审查门禁」，再写档案(落 `refactors/{slug}/` 目录,与 RULEBOOK 同处)、METRICS、规则毕业
- **偏差日志**:跳过的环节、放宽的检查,一行一条记入档案 `DEV-{序号} | 日期 | 跳过了什么 | 谁批准`——没人记录的偏差就是没人批准的偏差
- **结构同步**:重构天然改变文件结构——按 cm-doc-syncer 口径同步项目 README / CLAUDE.md 的目录与模块描述(调用 skill,不动其命令文件);收口清单含**波及物核对**:批内全部「需配合事项」逐条销账(实跑失误:U1 汇报的 README 同步在收口被漏,靠事后审计才发现)

## 收口人门(轻量道与批量道共用,全流程第三处签核)

🛑 **双计数呈签核后本命令才算闭环**:基线 {N} 项全绿 + 差分 {M} 组一致,连同档案、动机指标改前改后对照、**预算对账**(G0 预估 vs 实耗:agent 调用次数/时长,写入 METRICS 备注)一并打给人——不对账的预算永远是拍脑袋。与 G0、站 2 构成全流程恰好三处人门——门在阶段之间,签核=踢下一阶段,阶段内零停车(与 `docs/重构流程设计/` 的图一致,图与实现不得漂移)。

## 运行日志必记事件(node 写 `REFACTOR`,格式同 cm:ai 全局规则)

- `node_enter`:进入每道门/每站(G0、G0.5、规模门、各站、收口)
- `pause` / `resume`:**三处人门各一对**(G0 签核、站 2 规则定稿、收口 done-gate)——人门无 pause 记录 = 门没停,审计可查
- `decision`:规则修订采纳(修了哪条/为什么)、轨道选择、判官修复
- `task_start` / `task_done`:轻量道按次;批量道按**批次**记,detail 必带数字(完成 N/总数 M · 差分通过率 · 动机指标现值)——单文件粒度不灌主日志,进明细层 batch-log(见下节)
- `error`:判官假阳性排查、批次重生成(记明"第几次重复触发规则修订")、行为差异回滚
- `run_done`:收口(双计数与 slug 写进 detail/data)

## 重构专属明细日志(事件层之下的第二层,轻量道不豁免只减薄)

> 为什么比 feature 开发厚:新开发的失败是"没做出来",看得见;重构的失败是"**悄悄改了行为**",事后归因全靠明细。事件级日志答得了"发生过什么",答不了"这个行为差异是哪个文件、哪版规则、哪次批次引入的"。

- **judge-report.md**(`refactors/{slug}/`):判官档案——基线清单与结果、自验证变异清单(**种了什么变异 / 抓到没有**,漏抓的怎么修到抓到)、假阳性排查记录。判官的可信度证据,不是口头的"验证过了"
- **diff-report.md**:差分明细——每组输入 / 改前输出 / 改后输出 / 结论,逐组落盘(不是一句"全部一致");出现差异时该组全文保留,回滚后补记处置
- **batch-log.jsonl**(批量道):单文件粒度一行一条:`{file, agent, model, rulebook_rev, diff_pass, todos, confidence, duration}`——**归因链的关键是 `rulebook_rev`**:每个产物记录由哪版规则生成,行为差异出现时可精确定位"这批是坏规则的产物"而不是逐文件猜
- **RULEBOOK 修订史**(手册内置表):`版本 | 日期 | 触发实例(哪个失败) | 旧条文 → 新条文 | 裁决人`——规则演进必须可追溯,否则"修规则不修产物"就成了无账本的改法
- **回滚记录**:每次回滚在档案记一节(回滚了哪批 / 回到哪个 commit / 触发差异的输入组 / 归因结论),并与主日志 `error` 事件双写互指

## 落盘物清单(审计链)

| 落盘物 | 位置 |
| ---- | ---- |
| 运行日志 + 状态 | `{SPECS_DIR}/运行日志.jsonl` 追加 · `.cm-status.json`(状态条自动显示 REFACTOR 进度) |
| 明细层(判官/差分/批次/回滚) | `refactors/{slug}/` 下 judge-report.md · diff-report.md · batch-log.jsonl(批量道) |
| 可行性摘要 + 档案 | `{SPECS_DIR}/refactors/{日期}-{slug}.md`(批量道为同名目录) |
| RULEBOOK(批量道) | `refactors/{slug}/RULEBOOK.md` |
| 审查凭证 | `{SPECS_DIR}/.reviews/refactor-{slug}-T-REFACTOR-{slug}-r{N}.md` |
| 度量 | METRICS.md 追加行,Feature 列 `refactor` |
| 毕业规则 | 代码项目 `.claude/rules/` 对应文件 |
| 备忘销账 | LESSONS.md 待触发备忘状态更新 |

## 边界

- **不承接**:缺陷(→ $cm-fix)、行为变更(→ $cm-prd --change)、架构级重设计(升级出口:交人经 $cm-prd 立项——重设计下规则手册变设计文档、试点对比失效,是另一种流程)
- **不触发 cm-qa-engineer**:行为等价验证就是重构的 QA,行为没变就没有新 AC
- 没有 specs 目录的裸项目:档案落代码项目 `docs/refactors/`,凭证落 `docs/refactors/.reviews/`,METRICS 跳过(同 $cm-fix 惯例)

**对上游方法论的三处有意改编**(是取舍不是遗漏,放弃了什么留痕):

- kit 的重设计模式(规则手册变设计文档)→ 整体分流给 `$cm-prd` 立项——cm 已有方案对抗审查链,不重复造
- kit 的双对抗审查+第三方仲裁 → 用 cm 既有 N4 纪律(≤2 轮+分歧记录)——全框架审查纪律保持单一来源
- kit 的缺口清单(gap inventory)→ 不设——那是跨语言迁移特有物(目标语言强制要求表),同语言行为保持重构由波及面清单承担残余职能
