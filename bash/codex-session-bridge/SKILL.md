---
name: codex-session-bridge
description: Keep Codex Desktop conversation history visible when bridging between a ChatGPT personal account and an API proxy. This is a session-continuity skill, not an API manager. Includes an interactive API setup wizard where users only paste a base URL and choose a model; never ask users to paste API keys into chat. Trigger phrases:「codex 会话桥 / codex 会话不见了 / 历史会话不显示 / 切 api / 桥接到 api / 切回个人账号 / 配置 API 代理 / 设置 API 地址」「codex session bridge / missing codex conversations / bridge codex sessions to api / switch codex to api / switch codex to chatgpt」.
---

# Codex Session Bridge

This skill is for users who want Codex Desktop **conversation history to stay visible** when moving between:

- ChatGPT personal account
- API proxy

It is **not** primarily an API/provider manager. The core problem is session continuity: after changing Codex profile/provider, old conversations can disappear from the session list even though the jsonl files still exist.

Main promise: the user runs one beginner command or local `start.sh`, pastes an OpenAI-compatible API base URL, and can then bridge Codex between ChatGPT and API modes while keeping the full conversation history visible.

Important safety rule: **do not ask the user to paste an API key into chat.** `setup-api.sh` only asks for `base_url` and model. Codex Desktop prompts for the key in its GUI on first API use and stores it in macOS Keychain.

## Positioning

If a user asks how this differs from cc-switch / ccswitch:

- cc-switch-like tools solve API/provider configuration management.
- Codex Session Bridge solves Codex Desktop session continuity.
- The differentiator is migrating Codex's local session ownership (`model_provider`) in both jsonl session files and sqlite index.

Suggested short answer:

> ccswitch helps you switch API/provider configs. This skill helps Codex keep showing the same conversation history after the provider/account changes.

## When to trigger this skill

Any of:

- "codex 会话桥" / "会话桥" / "会话不中断"
- "codex 会话不见了" / "历史会话不显示" / "切完历史没了"
- "切 api" / "切到 api" / "桥接到 api" / "换 api" / "switch to api"
- "切 chatgpt" / "切回个人" / "切回个人账号" / "switch to chatgpt"
- "codex 切档案" / "codex 切配置" / "codex profile" / "codex switch account"

## Execution

### 1. Verify Codex is not running

Just call the script — it self-checks. Only the GUI main process (`Codex.app/Contents/MacOS/Codex`) and `codex app-server` block; crashpad / helper services are ignored.

If blocked, tell the user: **"Cmd+Q to fully quit Codex (closing the window is not enough), then retry."**

### 2. First-time API setup when needed

If the user is a beginner, asks to configure API proxy, says they only have an API URL, or `~/.codex/config.toml.profile.api` is missing, prefer the one-stop beginner entrypoint:

```bash
~/.claude/skills/codex-session-bridge/start.sh
```

Installed skill path:

```bash
~/.claude/skills/codex-session-bridge/start.sh
```

If the repo is not installed locally, share the remote one-line command instead:

```bash
bash <(curl -fsSL https://raw.githubusercontent.com/LXR110-bit/codex-session-bridge/main/start.sh)
```

If they only want to regenerate the API profile, use the smaller wizard:

```bash
~/.claude/skills/codex-session-bridge/setup-api.sh
```

The setup wizard asks for:

1. API proxy base URL, e.g. `https://api.deepseek.com/v1`.
2. Default model; pressing Enter uses the default.

Do not ask for the API key in chat. Tell the user Codex Desktop will prompt for it after switching to API mode and reopening Codex.

### 3. Diagnose or preview when appropriate

If setup looks suspicious, run doctor first:

```bash
~/.claude/skills/codex-session-bridge/switch.sh --doctor
```

If the user wants to preview changes before writing files, run dry-run:

```bash
~/.claude/skills/codex-session-bridge/switch.sh --dry-run chatgpt
~/.claude/skills/codex-session-bridge/switch.sh --dry-run api
```

If the user needs rollback support, list backups first:

```bash
~/.claude/skills/codex-session-bridge/switch.sh --list-backups
~/.claude/skills/codex-session-bridge/switch.sh --rollback <backup-dir>
```

For non-default API provider names, use explicit migration providers:

```bash
~/.claude/skills/codex-session-bridge/switch.sh api --provider my-proxy --from openai
```

### 4. Run the bridge/switch

```bash
~/.claude/skills/codex-session-bridge/switch.sh chatgpt   # to ChatGPT account
~/.claude/skills/codex-session-bridge/switch.sh api       # to API proxy
```

The script:
1. Backs up `config.toml`, `state_5.sqlite`, and every jsonl it touches into `~/.codex/jsonl_backup_<timestamp>/`.
2. Copies `config.toml.profile.<target>` to `config.toml`.
3. Uses `find` to recursively rewrite `"model_provider"` in every jsonl under `sessions/YYYY/MM/DD/` and `archived_sessions/`. (Do not use `**` glob — macOS bash 3.2 doesn't expand it.)
4. Updates the `threads.model_provider` column in `state_5.sqlite`.

### 5. Verify (mandatory)

```bash
~/.claude/skills/codex-session-bridge/switch.sh --verify
```

Both sqlite and jsonl must show **only one** `model_provider` value. If two appear, the rewrite missed something — investigate before letting the user reopen Codex (Codex will re-sync sqlite from jsonl at launch and bake the inconsistency in).

### 6. Tell the user to restart Codex

After verification passes: "Restart Codex — all history conversations will be visible."

## Core invariants

- ChatGPT mode uses `model_provider = "openai"` (Codex built-in, cannot be redefined in `[model_providers]` in recent versions).
- API mode uses `model_provider = "openai-custom"` (any non-built-in name works; this one is hard-coded across script + examples for consistency).
- Both jsonl and sqlite must be migrated together. Patching one and not the other gets reverted at the next Codex launch.

## Profile files (must exist before first use)

- `~/.codex/config.toml.profile.chatgpt`
- `~/.codex/config.toml.profile.api`

If the API profile is missing and the user is non-technical, prefer `start.sh`; if they only want API config regeneration, prefer `setup-api.sh`; avoid manual template editing unless they ask for advanced control. If the ChatGPT profile is missing and Codex is currently logged into ChatGPT, tell the user they can seed it with `cp ~/.codex/config.toml ~/.codex/config.toml.profile.chatgpt`.

## API 中转站和密钥说明 / Credentials and API proxy setup

不要要求用户把 API key 直接粘贴到对话里。

这个 skill 不保存、不托管、不管理用户的 API key。切换到 API profile 之前，用户必须先在本机准备好这个文件：

```text
~/.codex/config.toml.profile.api
```

普通用户不要手写这个文件，优先运行 `setup-api.sh`。这个文件里会包含 API provider 配置，例如 OpenAI 兼容接口的 `base_url`。API key 不写入该文件。

如果用户问：

> 我是不是把 API 中转站地址或者 API key 发给你，以后就能直接切了？

应该解释：

> 不是。第一次使用 API profile 前，需要你先在本机配置好 `~/.codex/config.toml.profile.api`。这个 skill 不会保存你的 API key，也不建议你把密钥发到聊天里。配置好之后，我才能帮你执行“桥接到 api / 切回个人账号”。

当用户要求桥接到 API 时，按这个流程处理：

1. 先检查 `~/.codex/config.toml.profile.api` 是否存在；
2. 如果不存在，告诉用户需要先在本机创建这个 profile；
3. 不要要求用户把真实 API key 发到聊天里；
4. 如果需要，可以给用户一个本地配置模板，让用户自己在本机编辑；
5. profile 文件存在后，再执行切换命令；
6. 切换后必须执行 `--verify`；
7. 最后提醒用户重启 Codex Desktop。

## Backups and rollback

Every run leaves a timestamped folder in `~/.codex/jsonl_backup_<TS>/` containing `config.toml.bak`, `state_5.sqlite.bak`, `manifest.tsv`, and every rewritten jsonl. To roll back: stop Codex and run `switch.sh --rollback <backup-dir>`. Backups created before v1.0.2 do not have `manifest.tsv`, so automated rollback restores config/sqlite only for those older backups.

## When the user changes config inside Codex GUI

GUI changes land in `~/.codex/config.toml` only — neither profile file is updated. After helping the user change something via GUI, ask: **"Should this change be saved into the chatgpt profile, the api profile, or both? Otherwise the next bridge/switch will lose it."**

Sync command:

```bash
cp ~/.codex/config.toml ~/.codex/config.toml.profile.chatgpt    # or .api
```

## Further reading

- [docs/HOW_IT_WORKS.md](docs/HOW_IT_WORKS.md) — internal mechanics
- [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) — war stories worth reading before debugging
