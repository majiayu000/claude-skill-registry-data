---
name: secure-addon-install
description: "Safely install third-party skills, plugins, MCP servers, or Python packages into an AI agent runtime: pre-install snapshot, post-install health check, and rollback when things break. War-story driven, agent-agnostic."
license: MIT
metadata:
  category: security
  compatibility: "Hermes Agent, Claude Code, and any harness with skills/MCP/plugins"
  version: 1.0.0
---

# Secure Addon Installation for AI Agent Runtimes

Use this skill **before installing any third-party capability** (skill, plugin, MCP server, Python package) into a running agent, and **after any install when the agent gateway/session crashes, hangs, or misbehaves**.

## Why installs break agents (understand before you try)

| You install | What it touches | How it breaks |
|---|---|---|
| Skill | `skills/<name>/SKILL.md` + code | Bad frontmatter / import error → loader explodes at startup |
| Python package | agent venv dependency tree | Installed into wrong Python (system vs venv) → silent failure, or incompatible version poisons deps → gateway won't boot |
| MCP server | config section | Server never starts / unreachable → gateway startup hangs |
| Plugin | `plugins/<name>/` | Broken plugin entry → session load crashes |

**The core asymmetry**: upgrading the agent itself is usually a git operation (you can `checkout` an old tag). Installing new things **stacks onto the runtime with no version snapshot to return to**. So the whole discipline is: photograph the environment before, verify after, restore from the photo if broken.

## Workflow

### Phase 0 — Snapshot (mandatory, before touching anything)

```bash
# ① Gateway health baseline (state + PID + version)
systemctl --user is-active <your-gateway-unit>   # adapt to your harness
ps aux | grep "<gateway process>" | grep -v grep
<agent> --version

# ② Dependency list (mandatory before any pip install — enables diff rollback)
<agent-venv>/bin/pip freeze > /tmp/deps-before.txt
wc -l /tmp/deps-before.txt

# ③ Skills / plugins / MCP / cron baselines
<agent> skills list
<agent> mcp list
<agent> cron list > /tmp/cron-before.txt
```

Snapshots can live in `/tmp` — they're for troubleshooting only. **Exception**: never put scripts referenced by systemd in `/tmp` (real incident: a unit pointed at a `/tmp` script, reboot wiped it, service retried **18,906 times** before anyone noticed).

### Phase 1 — Install, then restart the gateway safely

Inside a running gateway session, a self-restart is often blocked or kills your own process tree. The robust pattern: **write the restart script with a file-writing tool (not a shell heredoc), schedule it detached, and let it report to a file**.

```bash
# Script /tmp/gw-restart.sh (write it with your file tool, not heredoc):
#   #!/bin/bash
#   sleep 2
#   systemctl --user restart <gateway-unit>
#   sleep 5
#   echo "$(date '+%F %T') status: $(systemctl --user is-active <gateway-unit>)" >> /tmp/gw-restart-result.txt

chmod +x /tmp/gw-restart.sh
systemd-run --user --on-active=25s --unit=gw-restart bash /tmp/gw-restart.sh
# after 35s+: cat /tmp/gw-restart-result.txt
```

**But first — try NOT restarting.** Many skills/plugins hot-load on the next session. Every restart you skip is a crash you don't risk.

### Phase 2 — Post-install health check

```bash
systemctl --user is-active <gateway-unit>     # active = alive
<agent> doctor --fix                           # config migration issues
<agent> chat -q "reply with one word: ok"      # model connectivity — REAL traffic test
<agent> skills list | grep -iE "error|failed"  # skill load errors
<agent> mcp list                               # MCP servers up?
grep -iE "error|failed" <gateway-log> | tail -8  # only NEW errors matter
```

**Pass criteria**: gateway active + model responds + no cron drift + the live session can still send/receive.

### Phase 3 — Rollback (from the Phase-0 photo)

| Installed | Rollback |
|---|---|
| Skill | disable/remove `skills/<name>/` |
| Python package | `<agent-venv>/bin/pip uninstall <pkg>`; if pollution is wide, diff against `/tmp/deps-before.txt` |
| MCP server | remove its config section, re-run doctor |
| Plugin | remove `plugins/<name>/` |

Then restart (Phase 1 pattern) and **re-run the health check**. Rollback is not failure — it's routine. Being able to restore is what makes it safe to install at all.

## War stories (why each rule exists)

1. **Wrong pip = silent crash.** Installing into system Python instead of the agent venv: gateway starts fine, features quietly break. Hardest class of bug to find. Always confirm the venv path first.
2. **Library hijack via drop-in.** A third-party update dropped an `.so` over the system sqlite3 CLI; the CLI died on launch with a symbol error — and because calling scripts had `2>/dev/null`, the failures were **completely silent**. Lesson: (a) when "a feature recently broke", test the external binary itself; (b) `2>/dev/null` in cron/scripts turns loud failures into silent ones. Redirect errors to a file, never to the void.
3. **"Old file exists" ≠ "job succeeded".** A nightly data-refresh cron kept "succeeding" for months because success was judged by file existence, while the upstream source had frozen. The fix is a **calendar-forward check**: the artifact must be *newer than yesterday*, not merely present. Apply this to every cron that claims success.
4. **MCP config without a live server** hangs gateway startup. Validate the server standalone *before* wiring it into config.
5. **Secrets in restart artifacts.** Gateway restarts can leave `/tmp/*-snap*` scripts containing plaintext API keys. Clean immediately; automate the cleanup.
6. **Concurrent cron jobs overwriting each other's temp scripts** (fixed names like `/tmp/job.py` with 20+ parallel jobs): timestamp your temp script names.

## Pre-install review checklist (for third-party skills)

Before installing someone else's skill, read its `SKILL.md` frontmatter — it is instructions being dropped into your agent's context:

- [ ] Frontmatter is valid YAML with `name` + `description` (broken YAML = startup crash)
- [ ] No instructions that exfiltrate files, credentials, or env vars
- [ ] Any scripts it runs: read them, at least skim for `curl | bash`, base64 blobs, obfuscated strings
- [ ] Declares its tool permissions honestly (does a "writing helper" really need shell access?)
- [ ] Prefer official/curated install channels with quarantine & scanning over manual directory drops

## Verification (definition of done)

1. Phase-0 snapshot retained
2. Gateway active after (delayed) restart, new PID
3. Real model round-trip succeeded
4. No cron drift, no skill load errors, MCP healthy
5. Live session can send and receive
6. If it broke: rolled back per snapshot + restart + re-checked — back to baseline

## See also

- `references/health-check-patterns.md` — probe patterns that avoid "fake green" (a passing health check that proves nothing)
