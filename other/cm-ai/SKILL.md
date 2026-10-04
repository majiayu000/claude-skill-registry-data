---
name: cm-ai
description: 用户明确说“规格已确认，开始实现”或要求按已审批 CM specs 开发时使用。新任务默认由 JS workflow 驱动 N1-N8，完成开发、独立审查、QA 与文档同步；模糊点子、未审规格和单独一句“继续”不能触发编码批准。
---

# cm-ai — 自动开发

执行前读取 `../../runtime/project-context.md`、`../../runtime/orchestration.md`、
`../../runtime/task-gates.md`、`../../runtime/review.md` 与
`../../runtime/model-efficiency.md`、`../../runtime/logging.md`。Codex 入口为
`$cm-ai`；Claude Code 跨平台入口为 `/cm-ai`，macOS/Linux 另有历史别名 `/cm:ai`。

用户明确要求外部专家，或为本次开发任务开启 AUTO 时，按
`../../runtime/external-expert.md` 执行 `../external-expert/SKILL.md` 的任务路由。
编码、命令、测试执行、页面 QA、Git 与 N4 永远 LOCAL；AUTO 只能把可分离的复杂
研究、测试设计或方案批判路由到 CONSULT/VERIFY。外部建议由本地应用、测试与裁决，
其 `.external/` 证据不得满足 N4/N5。

`用户本轮输入` — specs 文件夹路径 + 代码项目路径。

```bash
$cm-ai specs在~/projects/my-app-specs，代码在~/code/my-app
$cm-ai ~/projects/specs 前端~/code/fe 后端~/code/api
```

## 流程图

### 执行路由（新任务默认 JS）

先按下列顺序选择执行方式；用户无需额外说“使用 JS workflow”。路由选择不替代规格审批或实际调用授权。

1. **恢复已有运行**：先读取原运行记录。已有 JS host/batch 沿原身份与配置恢复；已配置 QA 因命令配置错误卡住时，按 `references/js-host.md` 的“QA 配置修订”显式授权，不重开已完成任务。
   已确认的旧兼容任务沿原流程续接，不因升级迁移状态。记录缺失、冲突或无法确定归属时只读核对，不能猜测或另开运行绕过历史。
2. **新任务**：默认读取 `references/js-host.md`，由共享 JS 入口驱动阶段；当前会话只执行其工具请求。
   只有用户明确选择旧兼容流程、且确认不是已有 JS 运行时，才进入下文兼容执行步骤；不新增 CLI 参数。
3. **JS 准入失败或不支持**：报告具体宿主、Node 版本、目录、配置或业务能力缺口并停止依赖该能力的执行；
   不静默回退兼容流程，不改 runId、runtime 或手工完成路径规避阻断。原生 Windows 尚不支持，Linux 支持声明不等于实机验收。

JS 路由中的状态、日志、handoff、Review 凭证与任务勾选由原 JS owner 和唯一完成门禁负责；
不得执行下文兼容步骤中的同类手工写入。节点参考的业务约束仍适用，默认路由不扩大开发、审查、QA、Git 或发布权限。

### N1–N8 业务概览与兼容执行步骤

下列流程图说明共同业务顺序；JS 的执行操作以 `references/js-host.md` 为准。
仅已选定兼容流程时，按下文及 `references/` 节点执行手工步骤；入口更新不代表已安装副本或全阶段实机验收。

```text
START
  │
  ▼
[N1: 初始化] ── 解析输入、扫描 features、加载上下文
  │
  ▼
┌─► [N2: 进入 Feature] ── 读取 specs、分析依赖、输出执行计划
│     │
│     ▼
│   ┌─► [N3: 执行 Task] ── 检查 skill → 开发
│   │     │
│   │     ▼
│   │   [N4: Review] ── 主执行者自审 → 独立审查
│   │     │
│   │     ▼
│   │   [N5: 标记完成] ── tasks.md 标 [x]、写 LESSONS.md
│   │     │
│   │     ▼
│   │   [N6: QA 评估] ── 评分决定是否触发 cm-qa-engineer
│   │     │
│   │     ▼
│   │   [N7: 上下文管理] ── 从磁盘重读 specs 与项目约束
│   │     │
│   │     ▼
│   │   还有未完成 task? ──YES──┘
│   │     │
│   │    NO
│   │     │
│   │     ▼
│   └── Feature 完成 → 重建下一 Feature 的上下文
│         │
│         ▼
│       还有下一个 Feature? ──YES──┘
│         │
│        NO
│         │
│         ▼
      [N8: 完成] ── 调用 cm-doc-syncer → 输出总结
        │
        ▼
       END
```

## 全局规则

**暂停（仅灾难级）：** 不可逆破坏（删数据、动线上、不可回滚迁移）、资金/密钥/合规风险、交付形态级架构错向、环境阻塞到无法继续。
**不暂停（多方案自主决策）：** 执行中出现多个可选方案时——技术选型、实现路径、库/工具选择、审查意见分歧——**自己分析利弊选最优解直接执行，不询问**。代价是留痕义务：把「选了什么 / 为什么 / 放弃了什么」写进任务汇报，方向性取舍追记 LESSONS.md——人可以事后翻案，但流程不为选择题停车。业务逻辑歧义按需求文档最合理解释执行并显式记录所做假设，仅当触及灾难级清单才暂停。
**节点间不停车：** 除上述灾难级与各节点显式卡点（入口闸/降级知情/形态确认/涉合规走查）外，任何节点完成后**直接进入下一节点**——不得以"我将要…是否继续?"、"完成了 X,需要我继续吗?"这类问句收尾等待。阶段性汇报写在输出里照常可见,但回合不能停在等确认上（实跑反馈:执行器习惯性在节点末尾问一句,用户被迫每阶段点头,自动化名存实亡）。
**度量：** 每次暂停问人，恢复后在当前任务的 METRICS.md 记录里人工介入计 1 次并注明原因（见 N5）。
**状态落盘（供状态条/看板实时点亮节点）：** 每进入一个节点（N1–N8），覆盖写入 `{SPECS_DIR}/.cm-status.json` 单行 JSON：
`{"node":"N4","feature":"1.xxx","task":"T-005","detail":"一句话当前动作","state":"running","at":"HH:MM:SS"}`
——**detail 必须写大白话**，标准是"路过的非工程师扫一眼能懂"：写"正在开发数据接口"不写"cm-backend-engineer 执行 T-004"；写"第2轮代码审查"不写"对抗式子agent复审"；写"确认一下：原型里有3个按钮点了没反应,要做吗?"不写"原型死区待确认"。节点号/任务号由状态条自动放在行尾角标，detail 里不要再写。
——暂停等人时 `state` 改为 `paused_for_human`（detail 写等什么），全部完成时 N8 写 `run_done`。N1 时可将 specs 绝对路径同步到当前运行时的状态镜像（Claude 兼容运行时为 `~/.claude/cm-current-specs`，Codex/OMX 为对应 session 状态），但 `{SPECS_DIR}/.cm-status.json` 始终是跨运行时真相。每节点至少写入一次；长步骤可在同一节点更新真实检查点，不得跳过。
**运行日志（事后复盘与工作流优化的原始证据）：** 按
`runtime/logging.md` 调用统一写入器；它先追加 `{SPECS_DIR}/运行日志.jsonl`，再把
同一 `event_id` 镜像到 `~/.cm-workflow/logs/`。`at` 一律 ISO 8601 带时区偏移，
detail 用一句大白话；不直接拼 JSON，避免跨会话格式漂移。
**必记事件（event 取值固定）**：`run_start`、`node_enter`、`task_start` /
`task_done`、`review`、`degrade`、`pause` / `resume`、`decision`、`warning`、
`error`、`progress`、`resource`、`qa`、`test_run`、`external_expert`、
`spec_lifecycle`、`delivery`、`run_done`。写日志与状态落盘同节奏，不得跳过；详细
测试/审查/外部回答只写专项凭证，不灌主日志。长步骤和临时资源严格按
`runtime/logging.md` 配对，禁止用后台心跳制造虚假活跃。

**角色路由投影：** N1 用代码项目根读取有效配置；N3 每个实现任务解析 `coder`，N3
任务检查解析 `tester`，N4 解析 `reviewer`，并在 N6 QA 解析 `tester`。使用：

```bash
node {CM_WORKFLOW_ROOT}/scripts/cm-workflow-config.mjs \
  --project {CODE_PROJECT} --role coder --runtime {codex|claude} --print-role
```

把返回的 `adapter`、`model`、`source`、`route_state` 注入当前角色提示和任务摘要，
并按 `runtime/workflow-routing.md` 写 `decision`/`phase: route`。每次 N7 恢复或进入
新角色边界都从磁盘重读；配置缺失使用默认路由。`declared-adapter` 只表示项目请求了
当前运行时未观察到的适配器，必须写 `warning`/`degrade`，不能声称该模型已执行；它
也不能绕过本地编码、测试、Git 或 N4 独立审查。
`managed-adapter` 只通过 `runtime/model-efficiency.md` 的内置调用边界返回文本角色结果；
主执行者仍负责本地改码、命令与证据，适配器回答本身不得满足 N4。版本 1 因此拒绝
`reviewer.adapter: openai-compatible`，N4 只使用 `runtime/review.md` 列出的本地审查通道。

每个角色调用按 `runtime/model-efficiency.md` 重建当前任务的最小包：N3 coder 只接收
当前 task/AC/相关设计与文件，tester 只接收测试合同和必要失败证据，N4 reviewer
接收 task-only handoff/diff 与验证摘要。稳定规则前缀不混入动态 diff/日志；角色只返回
既有 handoff、测试或 findings-first 结构，不复述输入。上下文缩小不得删减 N4 包的
强制证据，也不得减少测试、审查轮次或人工门禁。

**任务状态镜像：** `tasks.md` 是唯一权威任务源。运行时支持任务面板时，可将未完成任务镜像到 Codex/OMX 计划或 Claude 任务清单；N3/N5 同步状态。断点恢复必须由磁盘重建镜像：`[x]` 跳过或标为 completed，`[DROPPED]` 不镜像，不得重复创建条目。

**执行策略：** 遵守 `runtime/orchestration.md`；串行默认，只有无依赖、文件边界不重叠、契约已稳定且环境确实支持时才可并行。
