---
name: openclaw-feishu-multi-bot
description: "Configure multiple Feishu/Lark bot identities within a single OpenClaw instance — each Agent gets its own Feishu App, name, avatar, and message routing. Use when: (1) Setting up multi-bot Feishu integration where each Agent appears as a separate bot, (2) Configuring message routing between Feishu apps and OpenClaw agents, (3) Debugging Feishu bot routing issues (bot not responding, wrong agent receiving messages, gateway startup failures), (4) Designing a multi-Agent architecture with per-role Feishu entry points, (5) Setting up per-project Feishu group isolation. Also trigger for: '飞书多机器人', '一个龙虾多个飞书', '飞书路由', 'Feishu accounts', 'Lark bot routing', or any question about making multiple Agents appear as separate bots in Feishu/Lark. Based on production experience running 10+ Agents with independent Feishu bots (2026-04)."
---



### Helper Behavior Review

`python scripts/_main.py` is an optional helper whose behavior should be compared with this skill's documented purpose before use. Show what the script does, explain any mismatch with the user-facing description, and run it only when the user explicitly wants that diagnostic path.

# OpenClaw Feishu Multi-Bot Configuration

One OpenClaw instance, multiple Feishu bot identities. Each Agent appears as an independent bot in Feishu — own name, own avatar, own group memberships. Users see separate assistants; behind the scenes, a single Gateway dispatches everything.

## Architecture in 30 Seconds

```
OpenClaw Gateway (single instance)
  ├── Agent: orchestrator ←→ Feishu App 1 (总调度 bot)
  ├── Agent: content-writer ←→ Feishu App 2 (写作 bot)
  ├── Agent: code-expert ←→ Feishu App 3 (开发 bot)
  └── Agent: analyst ←→ Feishu App 4 (分析 bot)
```

Three configuration blocks must align:

| Block | Location in openclaw.json | Purpose |
|-------|--------------------------|---------|
| `channels.feishu.accounts` | Feishu credentials per bot | Maps accountId → appId/appSecret |
| `bindings` | Message routing rules | Maps accountId → agentId |
| `agents.list` | Agent definitions | Maps agentId → workspace/model/tools |

The **accountId** is the key that ties them together. Get it wrong in any one place and routing breaks silently.

## Quick Start

### 1. Create Feishu Apps

One enterprise app per Agent at [open.feishu.cn/app](https://open.feishu.cn/app). Enable "Bot" capability. Record each app's `AppID` and `AppSecret`.

### 2. Run the setup helper

```bash
scripts/setup-feishu-bots.sh orchestrator:cli_xxx:secret1 writer:cli_yyy:secret2 coder:cli_zzz:secret3
```

Generates the three JSON blocks ready to paste into openclaw.json.

### 3. Register agents and restart

Add the generated config to openclaw.json, then:
```bash
openclaw doctor && openclaw gateway restart
```

### 4. Test each bot

Send a message to each Feishu bot independently. Verify each responds with the correct Agent identity.

## Reference Files

| File | Read when... |
|------|-------------|
| [references/architecture.md](references/architecture.md) | Understanding the three-block config model, accountId mechanism, and channel layer design |
| [references/build-guide.md](references/build-guide.md) | Setting up from scratch — Feishu developer console through gateway restart, step by step |
| [references/routing-deep-dive.md](references/routing-deep-dive.md) | Debugging routing issues — accountId consistency checks, binding rules, group-based isolation |
| [references/troubleshooting.md](references/troubleshooting.md) | Fixing specific problems — gateway won't start, bot not responding, wrong agent, spawn conflicts |

## Critical Lessons (Save Hours)

**1. accountId must match in 3 places**: `channels.feishu.accounts.{key}`, `bindings[].match.accountId`, and the `agent` field inside the account config. One typo = silent routing failure.

**2. Binding type must be `"route"`**: Using `"delivery"` or any other value causes gateway startup failure with no helpful error message.

**3. Feishu apps must be published**: Draft-state apps cannot receive messages. This is the #1 "bot not responding" cause.

**4. `allowAgents` must be complete**: If your orchestrator spawns sub-agents, every spawnable agent ID must be in `allowAgents`. New agent added but not listed = spawn permission error.

**5. `agentToAgent` must stay OFF**: Enabling `agentToAgent.enabled: true` breaks all sub-agent spawning (known bug #5813). Keep it `false`.

See `references/troubleshooting.md` for the full diagnostic flowchart.

## Scripts

| Script | Usage |
|--------|-------|
| `scripts/setup-feishu-bots.sh` | `./setup-feishu-bots.sh <agentId:appId:appSecret> ...` — Generates channels, bindings, and agents.list JSON blocks |
