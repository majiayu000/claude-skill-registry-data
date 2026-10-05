---
name: hermes-runtime-config
description: |-
  Hermes ships FOUR user-facing surfaces (CLI prompt_toolkit, Ink TUI in
  Python, Node ui-tui bundle, Electron desktop, web dashboard, messaging
  gateway). Each has its OWN gate for destructive operations, env var
  inheritance, and config persistence. A `config.yaml` flip in one does NOT
  silence the modal in another. Use when the user says "I turned off X but it
  still pops up", "why doesn't this config take effect", "I set
  HERMES_*_NO_CONFIRM=1 but the dialog is back", or asks to disable/inspect
  any cross-cutting runtime behavior (confirmations, telemetry, key bindings,
  approval gates, resume semantics).
---

# Hermes 多 UI 运行时配置陷阱

Hermes 有 4 套独立 UI,**配置和确认门是分开的**。`config.yaml` 改一处只影响一处;env var 要看是从哪个 shell / 哪个进程启动的;旧的子进程变量不可变。

**Ponetail rule**: 看到用户抱怨"关了 X 还弹" → 第一反应永远是**先问"你用的是哪个 UI"**,不要默认是 CLI。

## 4 套 UI 与它们的配置入口

| UI | 入口 | 启动方式 | 确认门 (destructive 弹框) | 持久化 |
|---|------|---------|-----------------------|-------|
| **CLI** | `hermes` 跑在 prompt_toolkit | 直接执行 `hermes` | `approvals.destructive_slash_confirm: true` in `config.yaml` | `~/.hermes/config.yaml` |
| **TUI (Ink, Python)** | `hermes` 启 `ui-tui` Node bundle | `hermes` → `_launch_tui()` (`hermes_cli/main.py:1985`) | `process.env.HERMES_TUI_NO_CONFIRM` (`ui-tui/src/config/env.ts:52`) | **没有** — 只读 env,不写盘 |
| **Electron desktop** | 桌面 app | `apps/desktop/` | Ink TUI 同一套 (`HERMES_TUI_NO_CONFIRM`) | env only |
| **Web dashboard** | 浏览器内嵌 TUI | `hermes_cli/web_server.py` `/api/pty` 桥 | Ink TUI 同一套,经 env 传入 | env only |
| **Gateway** (Telegram/Discord/Slack) | bot 进程 | `hermes gateway` | native 按钮 + `destructive_slash_confirm` 共享 CLI yaml | yaml |

**关键事实**:
- CLI 和 TUI 走**完全独立**的代码路径。TUI 的 `core.ts:182-208` 有自己的 `commit()` + `patchOverlayState` modal,跟 `cli.py:10578` 的 `_confirm_destructive_slash` 互不通信。
- TUI 的 `NO_CONFIRM_DESTRUCTIVE` 只看 `process.env.HERMES_TUI_NO_CONFIRM` — 不读 `config.yaml`,不读 `~/.hermes/.env`。
- env var 在 `_launch_tui` 时 `os.environ.copy()` 继承,**当前 shell 的 export 必须存在**。`~/.bashrc` 写入后必须开新 shell,旧 TUI 子进程变量已固化。
- "Always Approve" 按钮在 CLI modal 里会**反写 config.yaml**(`cli.py:10657`)。TUI modal 没有这个按钮,所以 TUI 路径**只能靠 env var 永久关**。

## 调试流程: "X 弹框不消失" 怎么排

```
1. 用户看到弹框 → 问"在哪个 UI"(CLI / TUI / desktop / dashboard / gateway)
2. 定位代码:
   - CLI 弹框: cli.py:7663 `_get_slash_confirm_display_fragments` 渲染
                cli.py:10578 `_confirm_destructive_slash` 决策
   - TUI 弹框: ui-tui/src/app/slash/commands/core.ts:199 `patchOverlayState({ confirm: ... })`
3. 找对应 gate:
   - CLI: `config.yaml → approvals.destructive_slash_confirm`
   - TUI: `process.env.HERMES_TUI_NO_CONFIRM`
4. 验证生效:
   - CLI: 改 yaml 立即生效(dispatch 时 `load_cli_config()` 重读)
   - TUI: **必须开新 TUI 窗口** — env 在子进程 spawn 时固化
5. 兜底 inline skip(不改任何配置,一次性):
   - CLI: `/new now`、`/new --yes 标题`、`/new -y`
   - 走 `_split_destructive_skip` (`cli.py:10548` + tokens `{"now", "--yes", "-y"}`)
   - TUI: 无 inline skip — 必须改 env
```

## 其他已知 dual/multi-gate 例子

后续遇到这种"一处改了他处不响应"模式,先列在这里再追代码。

### Slash confirmations (destructive)
- CLI: yaml `approvals.destructive_slash_confirm`
- TUI: env `HERMES_TUI_NO_CONFIRM`
- Gateway: 走 CLI yaml(共享)

### MCP reload confirmation
- CLI: yaml `approvals.mcp_reload_confirm`
- TUI: env `HERMES_TUI_NO_CONFIRM` (TUI 复用同一把 gate)
- 触发点: `cli.py:10565 _confirm_and_reload_mcp`

### Cost guard (expensive model switch)
- 在 CLI / TUI / Gateway 都触发,但 gate 在 `cli.py:2010-2018` 调用 `_request_slash_confirm` 走 slash-confirm 通道
- yaml: `approvals.expensive_model_confirm`

## 如何判定"我的 config 生效了吗"

`hermes config get <key>` 看 yaml 实际值。**TUI 路径不读 yaml**,这一招对 TUI 没用,直接 `echo $HERMES_TUI_NO_CONFIRM` 在启动 TUI 的 shell 里查。

## 验证清单(给"关了 X 还弹"的报告)

- [ ] 确认弹框是哪个 UI 渲染的(看代码:`cli.py:7663` vs `core.ts:199` vs `gateway/...`)
- [ ] 改对了那一侧的配置(yaml for CLI, env for TUI)
- [ ] TUI: env 在启动 TUI 的 shell 里 export,**不是**在另一个 shell
- [ ] 旧 TUI 子进程已 kill,开新窗口
- [ ] `skills_list` 之类不重启就读的配置,yaml 改完即生效,无需重启

## 常见误判

- 改 `config.yaml` 期望 TUI 也生效 → 不行,TUI 不读 yaml
- 在 WSL bash 改 `~/.bashrc` 然后 `/new` → 不行,TUI 子进程早就起来了
- 用 `hermes config set` 想关 TUI 弹框 → 不行,这是 CLI 的 gate
- 改完配置用 `hermes --tui` 启新实例 → 正确;改完用之前开的 TUI 测 → env 没变,无效
