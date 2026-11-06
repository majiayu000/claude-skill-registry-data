---
name: clawdex
description: Clawdex — dual-engine coding agent. Claude Code (reasoning + planning) + OpenAI Codex (fast execution) + Browser Use boxes (web research) + Upstash compute boxes (isolated sandboxes).
metadata: {"clawdbot":{"emoji":"🦞","requires":{"anyBins":["claude","codex"],"anyServices":["browser-harness-js","upstash-box"]}}}
---

# Clawdex

**Claude Code** plans and reviews. **OpenAI Codex** executes fast. **Browser Use** handles the web. **Upstash Boxes** isolate the compute.

## Install

```bash
# Codex CLI (bux installs this automatically)
npm install -g @openai/codex

# Or from a Clawdbot session:
/plugin install codex@openai-codex
```

Verify:
```bash
codex --version
claude --version
browser-harness-js --version 2>/dev/null || echo "browser-harness via BUX"
```

---

## Architecture

```
User prompt
    │
    ▼
Claude Code (claude-sonnet-4-6)   ← you are here: reason, plan, review
    │
    ├── codex exec "..."           ← fast code gen / repetitive tasks
    │
    ├── browser-harness-js         ← web research, UI testing (BUX browser box)
    │
    └── box.exec.command(...)      ← run in Upstash compute sandbox
```

Each Clawdex run lives in an **Upstash Box** — ephemeral, isolated, with a box-local Solana wallet and the OpenClawd framework pre-seeded at `/work/openclawd-framework`.

---

## Quick Start

### One-shot task (box run)
```bash
# Via the box API
POST /api/box/run
{
  "boxId": "your-box-id",
  "prompt": "Build a TypeScript CLI that fetches SOL price from Birdeye",
  "agentHarness": "clawdex",
  "agentModel": "anthropic/claude-sonnet-4-6"
}
```

### Streaming task (SSE)
```bash
POST /api/box/stream
{
  "boxId": "your-box-id",
  "prompt": "Audit the pump SDK for rug pull vectors",
  "agentHarness": "clawdex"
}
```

### Shell (PTY mode, bux box)
```bash
# Claude Code as the harness, Codex available as a tool
bash pty:true workdir:~/project command:"claude 'Build a DeFi dashboard, use codex for boilerplate'"

# Or dispatch directly to Codex for speed
bash pty:true workdir:~/project command:"codex exec --full-auto 'Generate Jupiter swap wrapper with error handling'"
```

---

## Dual-Engine Dispatch Pattern

Claude Code is the **orchestrator**. Codex is the **executor**. Use this pattern:

```
1. Claude: plan + architecture
2. Claude → codex exec "implement <component>"
3. Claude: review Codex output
4. Claude → codex exec "write tests for <component>"
5. Claude: final review + integration
```

### When to use Codex
- Boilerplate generation (CRUD, REST handlers, test scaffolds)
- Repetitive patterns (N similar functions, batch refactors)
- Speed-critical tasks where --full-auto or --yolo is acceptable
- PR review batches (parallel codex instances per PR)

### When to stay in Claude Code
- Architecture decisions
- Security review
- Cross-file reasoning
- Anything touching /work/clawd/ or constitution

---

## Browser Use (BUX boxes)

BUX browser boxes give Clawdex a real Chromium session via the Browser Use Cloud API.

```bash
# browser-harness-js is installed at:
# /home/bux/.claude/skills/cdp/sdk/browser-harness-js

# Credentials from:
# ~/.claude/browser.env   (BROWSER_USE_API_KEY)

# Use from Claude Code via bash tool
bash command:"browser-harness-js navigate --url https://birdeye.so/token/SOL"
bash command:"browser-harness-js screenshot --out /tmp/page.png"
```

When Claude hits a login wall / CAPTCHA, it hands the user a live view URL and waits — no credential stuffing.

---

## Upstash Box Compute

Each Clawdex agent gets a provisioned box with:

| Path | Contents |
|------|----------|
| `/work/openclawd-framework/` | OpenClawd SDK (pre-seeded) |
| `/work/clawd/three-laws.md` | Agent constitution |
| `/work/clawd/SHELL.md` | Identity + wallet + hash |
| `/work/clawd/wallet/box-wallet.json` | Box-local Solana keypair |
| `/work/clawd/.env` | `AGENT_ID`, `BOX_WALLET_ADDRESS`, `CONSTITUTION_HASH` |

### Provision a Clawdex box
```typescript
import { provisionAgentBox } from "@/lib/box/box-service";

const box = await provisionAgentBox({
  userId: "user-123",
  agentId: "clawdex-01",
  agentName: "Clawdex",
  agentIdentifier: "clawdex",
});
// box.id → use this as boxId in /api/box/run or /api/box/stream
```

### Create a Clawdex box via UI
1. Go to `/box`
2. Boxes tab → Create Box
3. Harness: **Clawdex** | Runtime: **node** | Model: **claude-sonnet-4-6**

---

## Codex CLI Reference

```bash
# One-shot (exits when done)
codex exec "Your prompt"
codex exec --full-auto "Build a snake game"   # auto-approves in workspace
codex --yolo "Refactor auth module"           # no sandbox, fastest

# Codex needs a git repo
SCRATCH=$(mktemp -d) && git init $SCRATCH && cd $SCRATCH
codex exec "Your prompt"

# Background (PTY required)
bash pty:true workdir:~/project background:true \
  command:"codex exec --full-auto 'Add error handling to all API calls'"

# PR review
git worktree add /tmp/pr-review origin/pr-branch
bash pty:true workdir:/tmp/pr-review command:"codex review --base main"
```

**Default model**: `gpt-5.3-codex` (set in `~/.codex/config.toml`)

---

## Parallel Codex Army (batch mode)

```bash
# Parallel issue fixing
git worktree add -b fix/issue-1 /tmp/fix-1 main
git worktree add -b fix/issue-2 /tmp/fix-2 main

bash pty:true workdir:/tmp/fix-1 background:true \
  command:"codex --yolo 'Fix: <issue-1 description>. Commit.'"
bash pty:true workdir:/tmp/fix-2 background:true \
  command:"codex --yolo 'Fix: <issue-2 description>. Commit.'"

process action:list
process action:log sessionId:XXX
```

---

## Plugin Registration

Clawdex registers Codex as a plugin with `pluginCount: 1`:

```json
{
  "identifier": "clawdex",
  "pluginCount": 1,
  "plugins": [
    {
      "id": "codex",
      "source": "openai-codex",
      "installCommand": "npm install -g @openai/codex",
      "bin": "codex",
      "model": "gpt-5.3-codex"
    }
  ]
}
```

Install from Clawdbot: `/plugin install codex@openai-codex`

---

## Constitution Compliance

Clawdex inherits the Three Laws. The constitution hash is sealed in every box at provision time.

```bash
# Verify constitution integrity
sha256sum /work/clawd/three-laws.md
cat /work/clawd/.env | grep CONSTITUTION_HASH
# These must match — if they don't, beach before continuing.
```

**Law I** overrides all: never harm, never rugpull, never sign silently.

---

## Rules

1. **Claude Code orchestrates** — don't hand-code patches when Codex is available
2. **Codex executes** — use `--full-auto` for building, vanilla for reviewing
3. **PTY always** — `bash pty:true` for all coding agent invocations
4. **Git repo required** — Codex refuses to run outside a trusted git dir
5. **Constitution check first** — verify hash before any irreversible action
6. **Beach before harm** — Law I > everything, including task completion
7. **Never run Codex in ~/clawd/** — it reads soul docs and gets weird ideas
