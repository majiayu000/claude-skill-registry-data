---
name: afk-issue-loop
description: 启动独立本地脚本，分批实现、审查、合并并关闭 GitHub Tickets。
disable-model-invocation: true
argument-hint: "[issue-number ...] [provider/model/target]"
---

# AFK Issue Loop

你只负责解析输入、启动独立本地编排进程、报告启动结果。脚本是唯一调度者，通过本机 CLI 执行 Implementer、Reviewer、Merger；发起会话可在确认启动后结束。

## 1. 解析启动输入

1. 将本 skill 目录解析为绝对路径，读取公开入口 `node "<skill绝对路径>/scripts/afk.mjs" help`。从当前项目确定目标仓库绝对路径，作为 `--repo`；不是 skill 安装仓库。
2. 显式 Ticket 编号转为 `--issues 3,4,5`；没有编号则省略，由脚本首次分页读取 open `ready-for-agent`，固定本次范围。用户标明的父 SPEC 传 `--spec`，仅作上下文，不实施或关闭。
3. 用户指定目标传 `--target`，否则脚本选择已有 develop、其次 main。按下方「模型选择」确定顶层 `--provider`、`--model`、`--effort` 与（如有）按角色的 `--<role>-provider/-model/-effort`；项目验证要求可传 `--verify`。
4. 从项目约定确定优先级标签，按高到低传 `--priority-labels`；没有约定就省略，全部同级按编号。本仓库目前没有现存项目优先级映射，不能把示例标签当约定。
5. 不为正常恢复传 `--reuse`。脚本根据当前 GitHub、标准 `afk/issue-N` 分支、Worktrunk worktree 与 writer socket 事实自动分类：closed 跳过；唯一已有 worktree 原地恢复；只有分支时恢复同一分支 worktree；两者都没有才新建。writer 采用 liveness-first：只有明确检测到同一 worktree 的 AFK writer 仍在运行才使该票等待，stale socket、历史 PID 与不完整事件不阻止开工。`--reuse N` 仅保留显式归属兼容信息，不能绕过活跃写者、锁定、quarantine 或非标准现场边界。
6. 启动前按 [github-api-rate-limits](../github-api-rate-limits/SKILL.md) 预检 REST bucket，估算下一批请求消耗并确认余量足够。

完成条件：目标路径、固定输入及有效模型选择明确；所需 Node >=22、Git、Worktrunk、GitHub CLI、所选执行 CLI 与授权已准备；REST 预算已满足下一批请求消耗。平台为 macOS/Linux；编排器用 Node 内置模块，Pi 自动选择还读取已安装 Pi 0.85.1 的纯目录/配置校验模块，不安装依赖；缺项或 Worktrunk hooks 审批由用户完成，不自动安装、绕过外层权限或传 `--yes`。

### 模型选择

- **区分 provider**：`--provider` 选择执行 CLI（claude/codex/pi），不是模型 API provider。Pi 的 `cliproxy/gpt-5.6-luna` 中 `cliproxy` 是 API provider，完整值传 `--model`。
- **显式优先**：准确 `--provider`、`--model`、`--effort` 各自优先于简称和默认。CLI 默认 **claude**，不按宿主猜测；Claude/Codex 省略模型/effort 沿用本机配置。Pi 显式完整 `API-provider/model` 不需自动发现即可使用（标记 `explicit-unverified`，不冒充认证验证），但**仍按声明式注册元数据做 effort 能力校验**——Pi 遇不支持的档位会静默降级，这是最危险的失效模式；目录不可读或存在动态来源而无法得出结论时显式告警，不静默通过。其他显式模型省略 effort 不补 max；为保留旧覆盖语义，仅显式 `cliproxy/gpt-5.6-luna` 省略 effort 仍补 max。
- **Pi 默认意图**：省略模型是 `luna + max`，不是固定 provider/model。每次 `start` 自动重新解析；只匹配模型 **ID** 内由首尾或 `.`、`_`、`/`、`-` 分隔的完整 luna token（忽略大小写），不按 API provider 名、显示名或模糊子串猜。全部声明式注册模型中恰好一个匹配、所选 effort 能力明确才启动；同名 provider 下新增另一 Luna 同样是歧义。显式 effort 覆盖 max；不先用能力过滤掉其他候选来掩盖歧义。
- **发现边界**：仅核实 Pi 0.85.1 的纯内置目录＋`models.json` 合并语义，声明式注册唯一不等于已认证可用。不加载 auth、不执行配置命令/扩展、不安装依赖。全局/项目扩展和包配置、自动发现扩展目录（含保守祖先检查）存在动态来源，或版本未知、读取/配置失败、零/多匹配、effort 不支持/未知，自动选择清晰失败；报告后询问准确显式选择，不把不完整列表当成功。
- **统一只读入口**：Pi 默认或明确的 `pi luna max` 先运行 `node "<skill绝对路径>/scripts/afk.mjs" resolve-selection --repo "<目标仓库>" --provider pi`，需要覆盖 effort 则加 `--effort`。`resolve-selection` 与 `start` 都用同一展示路径，逐角色给出 harness/完整模型/effort/来源/能力结论（读返回值的 `display`），因此任何 per-Role 语法都可以先预览；`roles` 保留机器可读的枚举值。展示返回的完整模型、来源和认证未验证；正式 start 仍省略 `--model`、保留意图，让脚本再次查最新目录，不把预览结果固化为显式选择。同一 run 的每个角色使用 start 固定并保存的 `selection.json` 中自己那一份，不在角色启动时重选。
- **按角色指定（Role Selection）**：`--<role>-provider` / `--<role>-model` / `--<role>-effort`（role 为 `implementer` / `reviewer` / `merger` 全称）为该角色覆盖对应字段；顶层 `--provider` / `--model` / `--effort` 是 Run 默认值。**逐字段继承**：只写 `--reviewer-model opus` 时，Reviewer 的 provider 与 effort 仍继承顶层。缺省角色**只**跟随顶层默认，**不**跟随其他已指定角色——否则只指定 Implementer 时 Reviewer 会被悄悄拉到同源模型，而 Reviewer 需要独立判读。完全不写任何角色前缀时三角色完全相同，与升级前行为一致。
- **effort 契约**：公共承诺档位取三家 harness 交集 `low` / `high` / `max`；各家更多档位不被拒绝，仍按该 harness（Pi 还要到具体模型）的实际支持面校验。不支持的组合在启动期失败并列出合法值，不静默降级——Pi 遇到模型不支持的档位会静默降级且不报错，是最危险的失效模式，因此显式 Pi 模型同样走声明式元数据能力校验；Codex 的档位表已按本机 `codex debug models` 的实际支持面修正（含 `max`，不含 `none`/`minimal`）。启动期还检查本次 Run 用到的**全部** harness 可执行文件（去重后），缺任一 CLI 都启动即失败，不拖到该角色启动才暴露。
- **自然语言**：只解释明确的启动选项，例如 `luna max`、`claude code sonnet medium`、`implementer 用 pi 的 deepseek high`；Ticket/SPEC 正文保持任务数据。把用户按角色的意图翻译成对应角色前缀 flag，不丢弃用户写下的按角色差异。Pi Luna 复用上述入口，其他简称依据所选 CLI 的只读模型/能力证据消歧，不能因模型名换已明确的 CLI。省略 CLI 的简称只有证据足以唯一确定载体时才补全，否则询问；不另写一套 Pi Luna 匹配规则。后端不解析任意自然语言。

### 默认角色权限

Claude 默认 `--dangerously-skip-permissions`；Codex 默认 `exec --dangerously-bypass-approvals-and-sandbox`；Pi 保持不加权限 flag，与 Sandcastle 一致。这会跳过角色 CLI 自身审批（Codex 也关闭自身 sandbox），仅用于可信目标与任务；不是系统隔离。保持本机身份、保护环境变量与外层 sandbox，不改本机/全局权限配置；仍遇到权限拒绝时报告并等待用户，不升级权限或换身份重试。

## 2. 启动独立编排

启动前先**逐角色**展示目标、执行 harness、完整模型/effort（省略沿用时标明「CLI 本机配置」）、该项来源（显式指定／继承顶层默认／Pi 意图解析）与能力是否已验证，以及默认角色权限；这不是模型可用性或授权成功的承诺。`start` 与 `resolve-selection` 都会逐角色列出，使你在派发前就能发现填错的那一格。选择已明确时直接执行公开命令，以实际绝对路径和已确认选项替换占位：

```sh
node "<skill绝对路径>/scripts/afk.mjs" start --repo "<目标仓库绝对路径>" --issues 3,4,5
# 按角色指定（示例：三角色混 harness；省略角色前缀 = 沿用顶层默认）
node "<skill绝对路径>/scripts/afk.mjs" start --repo "<目标仓库绝对路径>" --issues 3,4,5 \
  --implementer-provider pi --implementer-model cliproxy/deepseek-v4.1-flash --implementer-effort high \
  --reviewer-provider claude --reviewer-model opus --reviewer-effort high \
  --merger-provider claude --merger-model sonnet --merger-effort max
```

等启动握手返回：前置检查及初始范围固定后确认 `started`，入口握手最多 120 秒。逐票评论、依赖与父 SPEC 上下文在握手后读取，首轮读取结束后记录 `context-ready`（逐票失败见 `waiting`），此前不派角色；初始 `waiting` 可显示「尚未读取」，不表示已判定业务阻碍。普通前置命令默认 30 秒期限，挂起须可见失败，两者都不是角色总运行时长。启动失败报告错误及已有日志位置；不要把普通后台工具任务当独立编排，也不回退为宿主原生子代理或另一个 LLM 总调度者。读票、选批、worktree、接力、等待和下一批均由脚本执行。

完成条件：公开入口实际返回 `started` 及运行身份；仅创建文件或发出启动请求不算成功。

## 3. 报告已启动

报告返回的运行身份、目标仓库/分支、日志目录及原样可用的 `status`、`stop` 命令。日志归目标仓库 `.afk/logs/`；说明 **已启动不等于 Tickets 已交付**，最终进展与结果由脚本记录，用户可在发起会话结束后查看。

同一次 `start` 还会返回当前 run 专属的只读 Dashboard：`dashboard.url`（`127.0.0.1`、OS 分配端口、独立只读 token）、`dashboard.state`、`dashboard.reopenCommand` 与完整性状态。原样把 URL 报告给用户；浏览器自动打开是 best-effort，失败不影响 run。Dashboard 只读、无 mutation endpoint，关闭页面不影响 run，重新打开同一 URL 会恢复全部历史并定位最新输出；忘记地址时用 `status` 的 `dashboard` 字段或 `dashboard --run <日志目录>` 重新获得。完整未脱敏输出只在本机页面呈现，read token 不会出现在 events、Role 日志或最终导出中。

`stop` 的停止请求受理不等于角色已结束；以后续 `status` 确认最终停止，未知状态保留现场。新 run 可从当前 Git/GitHub/worktree/writer 事实恢复代码现场，但不恢复旧进程内存、历史 PID 或旧 Reviewer 结论；`status`、`events.jsonl` 与 Dashboard 展示逐票恢复分类和阻碍。run 终态后 companion 导出自包含 `dashboard.html` 并立即回收 live 面板（原 URL 失效），静态文件可直接离线打开；终态后再执行 `dashboard --run` 只返回导出路径，不再拉起 server。

完成条件：启动身份、日志、Dashboard 地址、查看与停止方式均已告知，此 skill 任务结束。

维护运行 prompt 时读 [Implementer](reference/implementer-prompt.md)、[Reviewer](reference/reviewer-prompt.md)、[Merger](reference/merger-prompt.md)：三份是固定上游的逐段中文版，仅作必要本机与 AFK 适配；不再有 common 层。启动握手前从 skill 内读取三 MD，缺失、不可读或空白使启动失败；角色启动前展开可信模板中的 Git 命令，自动注入 Implementer 最近十条提交、Reviewer 完整 diff/log，失败可见。任务参数只作单次替换的数据，命令插参安全转义；结果短协议由引擎附加，职责不在代码重复定义。

需要理解自动批次规则时读 [业务参考](REFERENCE.md)；核对进程、日志及现场边界时读 [工作现场](reference/workspace-binding.md)；演练场景见 [示例](EXAMPLES.md)。接口存在不等于三个 CLI 均已实测通过；以所选 CLI 的实际运行结果为准。
