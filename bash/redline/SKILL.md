---
name: redline
description: Live rate-limit awareness for Claude.ai (Max/Pro) and OpenAI (Plus/Pro/Codex). Never hit the red line again — your agent checks remaining budget every heartbeat and automatically throttles from full-send to conservation mode. Two CLI scripts + a 4-tier pacing strategy (GREEN/YELLOW/ORANGE/RED) that keeps you running at maximum token efficiency 24/7.
metadata:
  openclaw:
    requires:
      bins: [python3]
---

# Usage Pacing

Check live rate-limit usage for **Claude.ai** and **OpenAI/Codex** plans, then apply pacing tiers to avoid hitting limits.

## Scripts

### `claude-usage`

Reads the Claude Code OAuth token from macOS Keychain and calls the Anthropic usage API.

```bash
# Human-readable output with color bars
scripts/claude-usage

# JSON output (for programmatic use)
scripts/claude-usage --json
```

**Requirements:**
- macOS with `security` CLI (Keychain access)
- Claude Code OAuth token in Keychain (run `claude login` to set up)
- Token needs `user:profile` scope (standard Claude Code login provides this)

**Token location:** macOS Keychain, service `Claude Code-credentials`, account = your macOS username.

### `openai-usage`

Reads the OpenAI OAuth token from OpenClaw's auth-profiles and calls the ChatGPT usage API.

```bash
# Human-readable output with color bars
scripts/openai-usage

# JSON output
scripts/openai-usage --json
```

**Requirements:**
- OpenClaw with an authenticated `openai-codex` profile (run `openclaw auth openai-codex`)
- Auth profiles at `~/.openclaw/agents/main/agent/auth-profiles.json`

## Pacing Tiers

Wire both scripts into your heartbeat to automatically pace work based on remaining budget:

| Tier | Remaining | Behavior |
|------|-----------|----------|
| 🟢 GREEN | >50% | Normal operations |
| 🟡 YELLOW | 25-50% | Skip sub-agents, defer non-urgent research |
| 🟠 ORANGE | 10-25% | Essential replies only, no proactive checks |
| 🔴 RED | <10% | Critical only, warn user |

### Heartbeat integration

Add to your `HEARTBEAT.md`:

```markdown
## Usage pacing (every heartbeat)
- Run `scripts/claude-usage --json` and `scripts/openai-usage --json` to check rate limits.
- Store readings in memory/heartbeat-state.json under "usage.claude" and "usage.openai".
- Apply pacing tiers:
  - GREEN (>50% left): normal ops
  - YELLOW (25-50%): skip sub-agents, defer non-urgent research
  - ORANGE (10-25%): essential replies only, no proactive checks
  - RED (<10%): critical only, warn user
- If entering YELLOW or worse, mention it briefly when next messaging.
```

### JSON output format

**Claude (`--json`):**
```json
{
  "five_hour": {"utilization": 39.0, "resets_at": "2026-02-18T04:00:00Z"},
  "seven_day": {"utilization": 12.0, "resets_at": "2026-02-24T03:00:00Z"},
  "extra_usage": {"is_enabled": true, "used_credits": 5044, "monthly_limit": 5000}
}
```

**OpenAI (`--json`):**
```json
{
  "plan_type": "plus",
  "rate_limit": {
    "primary_window": {"used_percent": 0, "limit_window_seconds": 10800, "reset_at": 1771556400},
    "secondary_window": {"used_percent": 34, "limit_window_seconds": 86400, "reset_at": 1771556400}
  },
  "credits": {"balance": "882.99"}
}
```
