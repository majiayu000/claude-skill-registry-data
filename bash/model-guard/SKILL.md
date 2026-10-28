---
name: model-guard
description: |
  Budget guard for top-tier expensive models (Claude Code Fable, Codex astra): keeps one session from burning the whole plan quota and stalling every other session. Below the reserve line it is a soft CLAUDE.md/AGENTS.md rule (expensive model only thinks, plans and reviews; heavy work goes to cheap subagents); once 5h/7d remaining quota drops under a time-decaying reserve, a PreToolUse hook enforces the split. Triggers: install model guard, fable guard, 装模型预算闸, 贵模型保护, 更新贵模型列表, 改保留额, 卸载模型预算闸.
trigger: /model-guard
compatibility: Claude Code 2.1.301+（套餐用户）, Codex CLI 0.163+（hook 需用户信任一次）
license: MIT
---

# model-guard：贵模型预算闸

使用方式始终一套：贵模型只做思考、方案、审阅，重活派便宜 subagent。套餐余量充足时这是 CLAUDE.md 里的软提示；余量越过保留线后，PreToolUse hook 把它变成硬约束（强制分工，不是禁用贵模型）。

## 机制

| 组件 | 作用 |
| --- | --- |
| `scripts/statusline-tap.sh` | 包在原 statusLine 外层：把 stdin 里的 `rate_limits` 落盘到 `~/.claude/model-guard/rate-limits.json`，再把原 stdin 交给原命令 |
| `scripts/guard.sh` | PreToolUse hook（matcher `*`），Claude Code 与 Codex 共用：当前模型是贵模型且越线时，只放行派便宜 subagent、提问、计划类工具（Claude Code 另放行 limit≤200 的 `Read`） |
| `scripts/install.sh` | 安装、更新、现状、自检、卸载；幂等，改 settings.json 前备份 |
| `~/.claude/model-guard.json` | 贵模型/便宜模型列表、保留额、Codex 便宜模型与工具名清单、被包住的原 statusLine |

触发线随时间走：对 5h、7d 窗口各算 `remaining = clamp(距重置秒数 / 窗口秒数, 0, 1)`，余量 `100 - 已用%` 小于 `保留额 × remaining` 即越线，任一窗口越线就进入强制分工。

Claude Code 越线后 `Read` 只放行带 limit≤200 且不带 pages 的读取；用 offset 分段连续读仍可读完整文件，这是有意保留的小口子，大段阅读应派 subagent。模型判定取 transcript 最后一条 assistant 消息（实测首个工具调用时本条消息已写入）；`/model` 切换后的第一次调用可能仍按上一条消息的模型判定。

宿主按 hook 输入自动识别：带 `model` 字段的是 Codex，模型直接取该字段，用量取本 session rollout 里最后一条 `token_count` 的 `rate_limits`（`window_minutes`≤360 按 5h 口径，否则按 7d）；否则是 Claude Code，模型取 transcript 末尾 assistant 消息，用量取状态栏落盘文件。Codex 没有状态栏命令，不需要旁路。

用量数据缺失、超过 6 小时未更新、或非套餐用户（`rate_limits` 为 null）时一律放行。subagent 内的工具调用按 subagent 自己的模型判定，便宜 subagent 不受影响。

## 执行步骤

### 1. 展示现状

```bash
bash scripts/install.sh --status
```

把输出的现状表原样给用户：是否已装、模型列表、保留额、hook / 状态栏旁路 / 软提示是否就位、Codex 状态、当前用量是否已触发。`python3` 缺失时脚本直接报错，停止并提示安装。

### 2. 用 AskUserQuestion 一次问两件事

- **保留额**：推荐默认 5h 40% / 7d 50%（给其它 session 留的余量）；可自定 0-100。已安装时以现有值为推荐项。
- **贵模型列表**：默认 `fable`、`astra`（模型名子串，大小写不敏感）；可增删。

用户只是"更新贵模型列表"或"改保留额"时，只问对应的一项。

### 3. 一次性请求授权

列出将改动的文件，等用户确认：

- `~/.claude/settings.json`：注册 PreToolUse hook、包一层状态栏（改前自动备份为 `settings.json.bak-<时间戳>`）
- `~/.claude/CLAUDE.md`：写入 `<!-- model-guard:start -->` 标记块
- `~/.codex/hooks.json`：仅当 `~/.codex` 存在时，注册同一个 guard.sh（改前备份）
- `~/.codex/AGENTS.md`：仅当 `~/.codex` 存在时；若 CLAUDE.md 软链到它，只写一次

### 4. 执行安装

```bash
bash scripts/install.sh --models fable,astra --reserve-5h 40 --reserve-7d 50
```

未传的参数沿用已有配置。重跑即更新：hook 与状态栏不会重复注册，标记块按块替换。

### 5. 自检

```bash
bash scripts/install.sh --selftest
```

确认 settings.json（及 Codex hooks.json）已注册可执行的 guard.sh，并在临时目录伪造贵模型 transcript 与越线用量，验证两种宿主下 Bash 被拒（exit 2）、派便宜子 agent 放行。任一项失败即如实报告，不得说已完成。

Codex 只执行用户信任过的 hook。`--status` 显示"已注册，✗ 未信任"时，告诉用户：下次启动交互式 Codex 会提示 Hooks need review，选 Review hooks 或 Trust all and continue；`codex exec` 不提示，未信任的 hook 静默不执行。不要替用户写信任登记。

### 6. 汇报

给出：改动的文件（绝对路径）、备份文件路径、最终模型列表与保留额、自检结果、Codex 信任状态。提醒用户 Claude Code 要等状态栏下次刷新才有用量数据，Codex 要等每个 session 跑完第一轮，此前 hook 放行。

## 卸载

```bash
bash scripts/install.sh --uninstall
```

移除 settings.json 与 Codex hooks.json 中的 hook、还原原 statusLine、删除软提示标记块，保留 `~/.claude/model-guard.json` 供重装沿用。执行前同样列出改动文件请求确认。

## 被拦时怎么办

拒绝原因会回灌给模型，含当前模型、5h/7d 用量与剩余时间、越过了哪条线。按提示三选一：

- Claude Code：派 subagent，Agent 工具显式传 `model=opus|sonnet|haiku`，禁止 `subagent_type=fork`
- Codex：spawn_agent 显式传便宜模型（默认 sol/luna/terra/reserve），不传会继承贵模型
- `/model` 切到便宜模型继续
- `/compact` 减小上下文，降低每轮消耗

## 错误处理

| 情况 | 处理 |
| --- | --- |
| settings.json 不是合法 JSON | 安装拒绝修改并退出，请用户手工修复后重跑 |
| 保留额超出 0-100 或模型列表为空 | 安装拒绝，配置不变 |
| `--status` 显示"用量数据无或已过期" | 正常：等状态栏刷新；API key 用户永远没有数据，只有软提示生效 |
| 用户之后自己换了 statusLine | 重跑安装会把新命令当作原命令重新包住 |
| Codex hook 不生效 | `--status` 查信任状态；未信任时按上文在交互式 Codex 里信任一次 |
| Codex 工具名随版本变化 | 改 `model-guard.json` 的 `codex_allowed_tools` / `codex_agent_tools`；默认值按 codex-cli 0.163.0 实测（如 `collaborationspawn_agent`） |

## 测试

```bash
bash tests/test_guard.sh      # 规则矩阵：两种宿主的越线、窗口首尾、子 agent 规则、subagent 判定、fail open
bash tests/test_install.sh    # 临时 HOME：幂等、软链、状态栏旁路、Codex 注册与信任检测、更新、卸载还原
```
