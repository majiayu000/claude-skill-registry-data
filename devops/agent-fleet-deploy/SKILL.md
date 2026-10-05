---
name: agent-fleet-deploy
description: Deploy teams of Hermes AI agents to Discord using ClawFleet. Generic + customizable workflow.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [fleet, clawfleet, deployment, discord, agents]
    triggers: [fleet-deploy, clawfleet, multi-agent, discord-bot, agent-team]
    related_skills: [self-hosted-communication-server]
---

# Agent Fleet Deploy

Deploy multiple Hermes agents to Discord in one flow. Uses **ClawFleet** (web dashboard, Docker-based) or **Hermes profiles** (cross-platform).

---

## ⚠️ IMPORTANT: DESIGN BEFORE DEPLOY

This skill covers the **deploy and ops** phase. The **design and scaffolding phase** — researching existing fleet structure, defining agent roles, writing SOUL.md personalities, creating profile configs, wiring the fleet YAML, updating the ecosystem map — is documented in:

📄 **[references/team-design-workflow.md](references/team-design-workflow.md)**

**Always check:** Has the team been designed? If not, load `references/team-design-workflow.md` and complete the design phase first. Deploying without a design produces agents with overlapping roles, inconsistent SOUL.md quality, and no ecosystem documentation.

---

## Quick Flow

```
0. DESIGN PHASE (if needed)  → see references/team-design-workflow.md
1. Clone repo               → git clone https://github.com/pmb2/agent-fleet.git
2. Configure fleet           → cp config/agent-fleet.yaml.example config/my-fleet.yaml
3. Set Discord bot tokens    → replace *** with tokens from Discord Developer Portal
4. Deploy (ClawFleet/WSL2)   → bash scripts/wsl-deploy.sh config/my-fleet.yaml
   Deploy (Hermes profiles)  → ./agent-fleet deploy config/my-fleet.yaml
5. Customize personalities   → edit ~/.hermes/profiles/<name>/SOUL.md
6. Agents live on Discord    → talk to them in their channels
```

## Creating Discord Bot Tokens

### Option A: Manual (Discord Developer Portal)

1. Go to https://discord.com/developers/applications
2. New Application → name it after the agent (e.g. "people")
3. Bot → Add Bot → Copy Token
4. Enable: Message Content Intent, Server Members Intent
5. Invite: OAuth2 → URL Generator → Scopes: bot, applications.commands → Permissions: Send Messages, Read Messages, Read Message History
6. Use the generated URL to invite bot to your server

### Option B: API-Based (Programmatic — blocked by hCaptcha)

**⚠️ Discord now REQUIRES hCaptcha for programmatic application creation.** Attempting `POST /applications` with a user token returns:

```json
{"captcha_key":["captcha-required"],"captcha_service":"hcaptcha","captcha_sitekey":"a9b5fb07-92ff-493f-86fe-352a2803b3df",...}
```

This cannot be bypassed via API. For batch/bulk creation, each bot must be created manually through the Developer Portal (Option A). The API code below is preserved as reference but **WILL return 400 captcha-required** on fresh attempts.

**Discord user token format:** `MTU3...XXXX.XXXX` (base64-encoded snowflake + 2-part secret, ~72 chars). NOT the same as a Spacebar JWT (`eyJhbG...` format). You can extract the user token from Discord web app → DevTools → Application → Local Storage → `https://discord.com` → `token` key.

**API flow (reference only — blocked by captcha):**
```python
BASE = "https://discord.com/api/v10"
HEADERS = {"Authorization": USER_TOKEN, "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 ..."}

# 1. Create Application
app = requests.post(f"{BASE}/applications", json={"name": agent_name})

# 2. Create Bot
bot = requests.post(f"{BASE}/applications/{app_id}/bot")

# 3. Get Bot Token
bot_token = bot.json()["token"]

# 4. Enable privileged intents
requests.put(f"{BASE}/applications/{app_id}/bot", json={"intents": 32768, "bot_public": True})

# 5. Invite to guild
requests.post(f"{BASE}/oauth2/authorize", json={
    "client_id": app_id, "scope": "bot",
    "permissions": 3072, "guild_id": GUILD_ID,
    "response_type": "code", "authorize": True,
})
```

**Manual OAuth2 invite URL format:**
```
https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions=412672252992&scope=bot
```
Permissions `412672252992` = Send Messages, Read Message History, Add Reactions, Embed Links, Attach Files, Mention Everyone.

### Pitfalls

- **Rate limit:** 5 POST/min for application creation on free accounts. Add `time.sleep(3)` between creates.
- **Python urllib vs curl:** When making Discord API calls from Python, you MUST set a `User-Agent` header. Without it, Discord returns 403 Forbidden. Use `"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"` — `curl` includes a default UA, but Python's `urllib` does not.
- **Browser automation login fails:** Chrome DevTools MCP's `evaluate_script` cannot access `localStorage` — the function runs in a context where `window.localStorage` is `undefined`. This prevents injecting Discord user tokens into the browser session programmatically. The Developer Portal login must be done manually by the user once; after that, the browser tab can be used normally for bot creation.
- **Token types:** Discord bot tokens start with `MTUw...` (base64 snowflake). Spacebar bot tokens start with `eyJhb...` (JWT). If your `.env` has `eyJhb...`, it's a Spacebar token and won't work on real Discord.

## Spacebar → Discord Profile Migration

When moving existing Hermes agent profiles from a self-hosted Spacebar server to real Discord, the migration steps differ from a fresh deployment because profiles already exist with Spacebar-specific configuration.

### Prerequisites

- Hermes profiles exist at `~/AppData/Local/hermes/profiles/<name>/`
- Spacebar server is running (for reference/tokens while migrating)
- A Discord server with `Manage Server` permission (for creating channels)
- A Discord bot in the server with `Manage Channels` permission for API-based channel creation (or manual creation)

### Step 1: Check Existing Profile State

```bash
# Check which profiles have config.yaml:
for p in profile-name1 profile-name2; do
  f=~/AppData/Local/hermes/profiles/$p/config.yaml
  echo "$p: $([ -f \"$f\" ] && echo 'HAS config' || echo 'MISSING config')"
done

# Check .env for Spacebar-specific vars:
cat ~/AppData/Local/hermes/profiles/<name>/.env
```

**Common Spacebar-specific vars that MUST be removed for Discord:**
```
GATEWAY_ALLOW_ALL_USERS=true
DISCORD_AUTO_THREAD=false
DISCORD_REQUIRE_MENTION=false
DISCORD_ALLOWED_USERS=*
```

These are safe to delete — Discord ignores unknown env vars, but they can interfere with gateway startup logic that checks for Spacebar vs Discord.

### Step 2: Create config.yaml (if missing)

For Discord, each profile needs a `config.yaml` with the `discord:` section:

```yaml
model:
  api_mode: chat_completions
  base_url: https://opencode.ai/zen/go/v1
  default: deepseek-v4-flash
  provider: opencode-go
fallback_model:
  provider: openrouter
  model: google/gemma-4-31b-it:free
agent:
  max_turns: 120
  tool_use_enforcement: true
memory:
  memory_enabled: true
  user_profile_enabled: true
  provider: mempalace
tools:
  - web
  - terminal
  - file
  - memory
  - session_search
  - delegation
  - cronjob
  - clarify
  - skills
  - todo
  - send_message
skills: []
discord:
  require_mention: false
  auto_thread: false
mcp_servers:
  - MemPalace
  - Postgres
```

Key differences from Spacebar config:
- No need for `GATEWAY_ALLOW_ALL_USERS` — Discord has its own permission system
- `discord:` section with `require_mention` controls whether the bot responds without @-mention
- `auto_thread: false` is optional for Discord (Spacebar requires it; Discord works with either)

### Step 3: Replace Token in .env

The existing `DISCORD_BOT_TOKEN` in the profile's `.env` is a Spacebar JWT (`eyJhb...`). Replace it with a real Discord bot token from the Developer Portal. Keep the same env var name.

### Step 4: Create Discord Channels

Channels can be created via the Discord API using a bot with `Manage Channels` permission:

```bash
TOKEN=*** -s -X POST "https://discord.com/api/v10/guilds/$GUILD_ID/channels" \
  -H "Authorization: Bot $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"channel-name","type":0,"parent_id":"<category-id>"}'
```

### Step 5: Launch Gateway (No Monkey-Patching Needed)

Unlike Spacebar (which requires heavy monkey-patching of discord.py), Discord bots use Hermes' native gateway support. The launcher is a simple subprocess:

```python
import os, subprocess
env = os.environ.copy()
env["HERMES_HOME"] = "~/AppData/Local/hermes"
env["HERMES_PROFILE"] = "profile-name"
env["DISCORD_BOT_TOKEN"] = "<token>"
subprocess.Popen(["hermes", "gateway", "run", "--accept-hooks"], env=env)
```

Full launcher script at `references/discord-gateway-launcher.md`.

### Step 6: Invite Bot to Server

```
https://discord.com/api/oauth2/authorize?client_id={app_id}&permissions=412672252992&scope=bot
```

### Token Format Quick Reference

| Platform | Token Prefix | Format | Length |
|----------|-------------|--------|--------|
| Discord Bot | `MTUw...` | base64 snowflake + 2-part secret | ~72 chars |
| Discord User | `MTU3...` or `mfa.` | base64 snowflake + 2-part secret | ~72 chars |
| Spacebar | `eyJh...` | JWT | ~400 chars |

### Channel Mapping for Council Deployment

| Channel | Assigned Bot(s) |
|---------|----------------|
| `#command` | Chief of Staff |
| `#dev` | Technology Lead |
| `#revenue` | Revenue Lead |
| `#intel` | Intelligence Lead |
| `#finance` | Finance Lead, Tax Lead, Investment Lead |
| `#legal` | Legal Lead |
| `#ops` | Operations Lead |
| `#content` | Content Media |

## Repo Structure (generic)

```
agent-fleet/
├── README.md                 # Generic docs
├── AGENTS.md                 # Template for defining agent personalities
├── config/agent-fleet.yaml.example
├── scripts/
│   ├── wsl-deploy.sh         # ClawFleet in WSL2
│   ├── agent-fleet           # Hermes profiles CLI
│   └── install.sh
├── templates/
│   ├── profiles/             # SOUL.md, env, config templates
│   └── examples/             # Ready-to-use SOUL.md examples
└── LICENSE
```

## Customization Approach (Open-Source Pattern)

```
agent-fleet/
├── main branch ── generic, open-source
│   ├── templates/examples/     ← generic SOUL.md examples
│   ├── config/*.yaml.example   ← generic config template
│   ├── scripts/                ← deploy scripts (generic)
│   └── LICENSE (MIT)
│
└── pmb2-custom branch ── our specific agents
    ├── templates/agents/       ← our team dirs with SOUL.md files
    └── config/financial-fleet.yaml  ← our fleet config
```

**How to maintain this pattern:**

1. **Main branch stays clean** — generic examples, no specific agent names or team definitions. Anyone can clone and use. All documentation references example agents (scout, analyst).

2. **Custom branch adds specific agents** — create a `pmb2-custom` (or org name) branch. Add `templates/agents/<team>/` with SOUL.md files and a custom fleet config under `config/`. The branch inherits all scripts, CI, and templates from main.

3. **Work in custom branch for daily use** — agents live here. Sync from main periodically (`git merge main`) to pick up script improvements and CI updates.

4. **Open-source contributions go in main** — PRs, bug fixes, example improvements all target main. The custom branch stays private unless explicitly published.

This keeps the project shareable without exposing internal team structures or Discord bot tokens.

## Deploy Paths

### Path A: ClawFleet in WSL2 (Recommended — web dashboard + Docker isolation)

```bash
# Windows + Docker Desktop with WSL2 integration
cp config/agent-fleet.yaml.example config/my-fleet.yaml
# Edit: add Discord bot tokens
bash scripts/wsl-deploy.sh config/my-fleet.yaml
# → Dashboard at http://localhost:8080
```

### Path B: Hermes Profiles (Cross-platform, no Docker)

```bash
# Works anywhere Hermes is installed
./agent-fleet deploy config/my-fleet.yaml  # Create profiles + start gateways
./agent-fleet status config/my-fleet.yaml  # Dashboard via terminal
```

ClawFleet creates Docker containers per agent (Hermes `--runtime hermes`). The profile approach creates a Hermes profile per agent and runs gateways as background processes.

### Path C: Manual profile setup (recommended for teams with custom SOUL.md files)

The deploy script (Path B) only copies a generic SOUL.md from `templates/profiles/SOUL.md`. For teams with **per-agent personalities** in `templates/agents/<team-name>/`, the workflow is:

```bash
# 1. Create profiles with the deploy script (generic template)
./agent-fleet deploy config/full-fleet.yaml

# 2. Overwrite SOUL.md with team-specific versions
cp templates/agents/hermes-dev/dev-lead-soul.md ~/.hermes/profiles/dev-lead/SOUL.md
cp templates/agents/hermes-dev/skills-lead-soul.md ~/.hermes/profiles/skills-lead/SOUL.md
# ...repeat for each agent

# 3. Set tokens & start gateways individually
for name in dev-lead skills-lead integration-lead qa-lead docs-lead; do
  hermes -p "$name" gateway run &
done
```

### Path E: Spacebar (Self-Hosted Discord) — Custom Gateway Bridge

**Fleet scale:** After adding the Pulse Team (4 agents), the Spacebar fleet grows from **35 agents (5 teams)** to **39 agents (6 teams):**
- Council (9) + Specialists (8) + Hermes-Dev (5) + **Pulse Team (4)** + Trading (8) + Social Media (5)

The Pulse Team is a reusable deployment block for any large agent ecosystem that needs self-healing infrastructure monitoring.

For deployments to a **self-hosted Spacebar instance** (discord-compatible API) instead of Discord. Uses a custom gateway script to bridge Hermes ↔ Spacebar.

**Architecture:**
```
Hermes Agent (local machine)
  └─ spacebar-gateway.py ── WebSocket ──► Spacebar API (localhost:3001 or via SSH tunnel)
       ├─ Listens as a bot
       ├─ Routes messages to Hermes session
       └─ Registers slash commands
```

**Setup steps:**

1. **Create the gateway script** — see `references/spacebar-gateway-pattern.md` for the full template. Key requirements:
   - discord.py API version must be **v9** (Spacebar caps at v9, not v10+)
   - Monkey-patch `msvcrt.locking` → noop (circumvents Windows file lock from gateway.lock)
   - Set `PYTHONPATH` to the hermes-agent source directory for imports
   - Read bot token from profile `.env` file

2. **Profile config** — each agent needs a Hermes profile:
   - `hermes profile create <name>` or copy config into `~/.hermes/profiles/<name>/`
   - Set `source_token: SPACEBAR_BOT_<NAME>` in `.env`
   - Disable the default gateway plugin: the custom script replaces it

3. **Bot account** — register bots via Spacebar API:
   ```bash
   curl -X POST "http://localhost:3100/api/v9/auth/register" \
     -H "Content-Type: application/json" \
     -d '{"username":"<agent-name>","password":"...","consent":true,"bot":true}'

   # Get bot token:
   curl -X POST "http://localhost:3100/api/v9/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"login":"<agent-name>","password":"..."}'
   ```

4. **Start the gateway**:
   ```bash
   cd ${MY_REPOS}/hermes-agent
   PYTHONPATH=${MY_REPOS}/hermes-agent/src \
     python scripts/spacebar-gateway.py \
     --token "$SPACEBAR_TOKEN" \
     --guild "$GUILD_ID" \
     --api-url "http://localhost:3001/api/v9" \
     --profile <profile-name>
   ```

5. **Public access via SSH tunnel** (if Spacebar is local):
   ```
   VPS (Caddy in Docker) → SSH tunnel → localhost:3001 → Spacebar API
   VPS (Caddy in Docker) → SSH tunnel → localhost:PORT → Fermi/Gateway
   ```
   See `MCP tunnel setup` → `references/expose-local-service-via-ssh-tunnel.md`.

**Spacebar-specific pitfalls:**
- discord.py v10+ **will not work** — Spacebar hasn't implemented v10 API changes. Must use v9-compatible behavior.
- `msvcrt.locking` on Windows — the gateway lock file triggers it. Patch: `import msvcrt; msvcrt.locking = lambda *a: None`.
- Bot tokens in `.env` — source them before gateway start to keep tokens out of command history.
- Spacebar config must have `autoCreateBotUsers: true` for bot account creation via API.
- **Bot token source** — Some Spacebar builds return `token` as a top-level login field, not nested under `bot.token`. The gateway must handle both response shapes.
- **Spacebar config must be at production path** — use `config.production.json` and `NODE_ENV=production`. The default `config.json` is for dev; production settings (port, domain) go in `config.production.json`.
- **Port mismatch kills the tunnel** — if Spacebar runs on port 3100 but the SSH tunnel forwards 3001, the Caddy proxy returns 502. The tunnel port and Spacebar PORT env var must match.

#### Pulse Team Deployment on Spacebar (4 Agents)

When adding the Pulse Team (Vigil, Chronicle, Helix, Muse) to an existing Spacebar fleet, the deployment pattern is:

**Step 1 — Create bot accounts:**
Bots are registered as regular users (Spacebar rejects `"bot": true`). Use a registration script pattern:

```python
bots = [
    ("security-lead", "vigilPulse789!", "vigil_pulse@local.dev"),
    ("history-lead", "chroniclePulse789!", "chronicle_pulse@local.dev"),
    ("automation-lead", "helixPulse789!", "helix_pulse@local.dev"),
    ("creative-lead", "musePulse789!", "muse_pulse@local.dev"),
]
for uname, pwd, email in bots:
    data = {"username": uname, "password": pwd, "consent": True, "date_of_birth": "1990-01-01", "email": email}
    requests.post("http://localhost:3001/api/v9/auth/register", json=data)
```

After registration, login to get the bot token, then save to `.env.spacebar` as `SPACEBAR_BOT_VIGIL`, etc. Each bot account must join the guild (via `PUT /guilds/{guild_id}/members/@me` or admin-add).

**Step 2 — Create channel structure:**
Create a category + 5 text channels under it:

```
#pulse-ops (category/type=4)
├── #pulse-alerts     (🔴 Vigil → Helix, alerts only)
├── #pulse-status     (🟢 every 15m heartbeat)
├── #pulse-report     (📋 Chronicle project reports every 4h)
├── #pulse-intel      (🧠 Muse intelligence briefs every 6h)
└── #pulse-internal   (🔄 team coordination)
```

API: `POST /guilds/{gid}/channels` with `{"name": "pulse-alerts", "type": 0, "parent_id": "{cat_id}", "topic": "..."}`

**Step 3 — Create Hermes profiles:**
Each agent profile needs constrained tools (no browser, no delegation for Vigil/Helix — they're probes not builders) and specific skills:

| Agent | Tools | Skills | MemPalace Wing |
|-------|-------|--------|----------------|
| **Vigil** | terminal, file, memory | `systematic-debugging`, `web-app-qa` | pulse-infra, pulse-state |
| **Chronicle** | terminal, file, web, delegation | `codebase-inspection`, `project-inventory`, `writing-plans` | pulse-progress, pulse-state |
| **Helix** | terminal, file, memory | `systematic-debugging`, `token-optimization-rtk` | pulse-playbooks, pulse-infra |
| **Muse** | web, terminal, file, memory | `blogwatcher`, `intelligence-pulse`, `youtube` | pulse-intel, pulse-state |

**Step 4 — Wire into council SOULs:**
The Technology Lead SOUL gets a Pulse Team Integration section describing their oversight of Vigil/Helix, and the Chief of Staff SOUL gets a reference to Chronicle as their direct report for project tracking. The Intelligence Lead SOUL references Muse for the intel pipeline.

**Step 5 — Save tokens and deploy:**
```bash
source .env.spacebar
bash scripts/spacebar-fleet-deploy.sh config/spacebar-fleet.yaml
```

The deploy script auto-populates `DISCORD_BOT_TOKEN` in each profile's `.env` from the corresponding `SPACEBAR_BOT_*` env var.

**Pulse Team prompts for cron jobs** (each agent runs on its own cron schedule):

| Agent | Schedule | Prompt Pattern |
|-------|----------|----------------|
| Vigil | Every 15m | Probe all services, write to security-lead-PULSE.md, alert #pulse-alerts if 🔴 |
| Chronicle | Every 4h | Scan all git repos, cross-reference priorities, write to history-lead-PULSE.md |
| Helix | Every 4h | Read security-lead-PULSE.md, apply playbooks, write to automation-lead-PULSE.md |
| Muse | Every 6h | Scan blogwatcher/PIM/YouTube, curate top 5 signals, write to creative-lead-PULSE.md |

See `teams/pulse/cron-config.md` in the agent-fleet repo for exact cron creation commands.

**Profile config templates live at:** `agent-fleet/config/profiles/security-lead.yaml`, `history-lead.yaml`, `automation-lead.yaml`, `creative-lead.yaml` — copy these to `~/.hermes/profiles/<name>/config.yaml`.

**Complete example implementation:** See `agent-fleet/teams/pulse/` for all 4 SOUL.md files, PULSE.md heartbeat templates, ORG_INTEGRATION.md with the approval tier system, and DEPLOYMENT.md checklist.

#### Pulse Team Registration + Channel Script Pattern

For any new specialized team addition to a Spacebar fleet, use this reusable two-script pattern:

**Script 1: `register-<team>-bots.py`** — Register bot accounts, login, join guild, save tokens to `.env.spacebar`
**Script 2: `create-<team>-channels.py`** — Create category + text channels under it, configure topics

Both scripts follow the same template: Spacebar API calls at `http://localhost:3001/api/v9`, admin token from `.env.spacebar`, bot registration as regular users with 1-second delay between registrations.

### Path D: Post-Deploy — Pulse System Setup (Agent-Powered)

Every agent needs a recurring pulse — where the AGENT ITSELF runs its domain work on schedule and appends findings to PULSE.md. This is modeled on ChatGPT's Scheduled Tasks feature.

After profiles are created, set up each agent's pulse cron job:

```bash
cronjob action=create \
  name="<agent>-pulse" \
  schedule="every 4h" \
  profile="<agent-name>" \
  skills="[skill1, skill2, ...]" \
  prompt="<role-specific domain work>"
```

Key properties:
- `profile: <name>` — runs under the agent's own profile (their model, persona, SOUL.md)
- `skills: [...]` — role-specific skills loaded for each pulse
- `prompt:` — tells the agent to investigate its domain and write to PULSE.md
- Delivery goes to the origin channel so you see results

See the `agent-provisioning` skill **Phase 5** for the full pattern: prompt design, PULSE.md format standards, frequency guidance, and the pulse-vs-heartbeat distinction table.

**DO NOT** use `no_agent=true` shell scripts for pulse monitoring — that produces sysadmin heartbeats ("PID: 12345, Uptime: 2h"), not value-producing agent pulses ("Found 3 stale skills in the library").

### Path F: Command OS Council Profile Structure (Executive + Specialist Teams)

For the operator's Command OS architecture, use a structured profile format with YAML frontmatter in AGENTS.md:

**Council lead profile** (per lead — 4 files):
- `SOUL.md` — identity, mission, codename, values, boundaries
- `AGENTS.md` — YAML frontmatter (name, codename, team, reports_to, supervisor, model, provider, tools, mcp_servers, authority_level) + agent definition with core duties, escalation triggers, reporting cadence
- `SKILLS.md` — 5 key workflows with trigger, steps, output format
- `config.yaml` — profile config with system prompt, tools list, MCP servers

**Specialist team profile** (per team — 3 files):
- `SOUL.md` — identity, mission, reporting line
- `AGENTS.md` — same YAML frontmatter + role definition
- `SKILLS.md` — 3-5 domain workflows

All profiles live at: `agent-fleet/teams/council/<lead-name>/` or `agent-fleet/teams/<specialist-name>/`

For the **Spacebar-specific** profile wiring — `.env`, `.env.spacebar`, `config.yaml` template, DOX-framework `AGENTS.md`, `SOUL.md` pattern, fleet manager maintenance, batch URL migration, and deployment flow — see **[references/spacebar-profile-wiring.md](references/spacebar-profile-wiring.md)**. That reference is the canonical guide for what was built in the 43-agent fleet on gc.your-domain.example.

**CAUTION:** The deploy script (Path B) only copies generic templates. For Command OS profiles with custom YAML frontmatter in AGENTS.md, deploy manually:
1. Create the directory under `agent-fleet/teams/`
2. Write SOUL.md, AGENTS.md, SKILLS.md, config.yaml directly
3. Register the Hermes profile: `hermes profile create <name> --description "..."` or copy config.yaml into `~/.hermes/profiles/<name>/`

Unlike basic profiles that use Discord deployment (Path A/B), Command OS council profiles are designed to run as the `default` Hermes session with X-Team-ID headers routing through the Intent Firewall.

## Population Pattern: Census-First Deployment

For the operator's ecosystem, ALL 9 council leads + 8 specialist teams were deployed in a single sprint using this pattern:
1. 3 parallel discovery subagents → ecosystem census
2. 2 parallel subagent waves (3 × 5 leads each) → 40 council profile files
3. 2 parallel subagent waves (4 × 3 teams each) → 24 specialist profile files
4. Direct file creation → shared memory + MCP registry + operational scripts
5. 61 files committed to `agent-fleet` repo in one commit

Total: ~144 files, ~20K lines, ~8 hours wall time, ~2 hours in subagent parallel waves.

Before deploying, assign a model to each agent based on role:
- Reasoning-heavy (dev-lead, qa-lead) → `deepseek/deepseek-chat`
- Instruction-following (skills-lead, docs-lead) → `google/gemma-4-31b-it:free`
- Code-heavy (integration-lead) → `qwen/qwen3-coder:free`

Set in `model:` in profile's config.yaml. See `agent-provisioning` skill Phase 2b for full mapping.

### Windows Detached Process Launch

On Windows, `subprocess.Popen` children **do not survive parent exit** — even with `CREATE_NO_WINDOW`. The only reliable detach is VBScript's `WshShell.Run`:

```vbscript
Set WshShell = CreateObject("WScript.Shell")
cmd = """" & pythonExe & """ """ & script & """ " & arg
WshShell.Run cmd, 0, False
```

Or PowerShell:
```powershell
Start-Process -WindowStyle Hidden -FilePath $pythonExe -ArgumentList @($script, $arg) -WorkingDirectory $cwd
```

**Critical:** Detached processes **lose environment variables** from the parent. The gateway script must fall back to reading config from the profile's `.env` or `.env.spacebar` file directly (not from env vars). See `self-hosted-communication-server` Patch #16 for the token file fallback pattern.

## Pitfalls

- Discord bot tokens **must** have Message Content Intent enabled
- Discord now **blocks** programmatic bot creation with hCaptcha — always use the manual Developer Portal for creating bot applications. The API method returns `captcha_key: captcha-required`.
- ClawFleet dashboard starts on port 8080
- Each agent needs its OWN Discord bot application (different tokens)
- The WSL2 deploy script assumes Docker Desktop with WSL2 integration
- Hermes profiles approach works on Windows/Mac/Linux without Docker
- **Per-agent SOUL.md files** — The deploy script only copies `templates/profiles/SOUL.md` (generic template). For team-specific personalities (in `templates/agents/<team>/`), copy them manually after deploy: `cp templates/agents/<team>/<agent>-soul.md ~/.hermes/profiles/<name>/SOUL.md`
- **Gateway start** — `hermes -p <name> gateway run` for individual agents. May need `nohup ... &` for background persistence.
- **Spacebar: discord.py API v9 pinned** — Spacebar caps at API v9. Use `discord.VoiceRegion.us_west` or explicitly set API version in client construction. v10+ calls will 404.
- **Spacebar: msvcrt.locking on Windows** — The gateway.lock file triggers `msvcrt.locking()` which throws in MSYS. Add `import msvcrt; msvcrt.locking = lambda *a: None` before any lock-file code.
- **Spacebar: SSH tunnel port must match server port** — If Spacebar runs on PORT=3001 but ssh tunnel forwards 3100 (or vice versa), the proxy returns 502. Set PORT env var to match the tunnel target port.
- **Discord bot tokens CAN be created programmatically** via the Discord REST API with a user token. Use the API approach (Option B above) for bulk creation. Manual creation (Option A) is still fine for 1-2 bots.
- **Data pipeline agents vs Discord agents** — If you have a Python data pipeline (scouts, APScheduler, SQLite) and want Discord agents that read from it, use the **MCP bridge pattern**: create a lightweight MCP server that wraps the DB with query tools, wire it into Hermes config, and write SOUL.md that tells agents to query it. The pipeline runs independently.
- **One agent per channel, multiple channels per team** — All agents on a team share one Discord channel. They @-mention each other for cross-reference. The SOUL.md should define which other agents each agent coordinates with.

## Customization via Fork/Branch

Keep the main repo open-source generic. Create a branch or fork for your specific agents:

```
main (generic)        →  templates/examples/  (ready-to-use archetypes)
pmb2-custom (yours)   →  templates/agents/<your-team>/  + config/<your-fleet>.yaml
```

The main branch stays publishable. The custom branch adds:
- Your agent SOUL.md files
- Your fleet config with real Discord tokens
- Team-specific skills

## Team Structure Template

When adding your own teams, organize as:

```
templates/agents/
├── financial/           ← Team name
│   ├── people.md        ← Agent SOUL.md
│   ├── product-lead.md          ← Agent SOUL.md
│   └── skills/          ← Team-specific skills (optional)
├── security/
│   └── ...
└── ...
```

Each agent maps to:
- One Discord bot (different token)
- One channel (shared per team)
- One SOUL.md (personality + role)
- Access to ALL MCP servers (shared pool)
- Shared MemPalace + Kanban

## Ecosystem Reference

Full ecosystem map at `ECOSYSTEM.md` on the custom branch:
- When adding a new agent to an existing fleet, just add its entry to the fleet config YAML and re-deploy — the CLI skips existing profiles and updates tokens
- The `agent-fleet deploy` CLI copies SOUL.md from templates/profiles/SOUL.md — customize each agent's personality in `~/.hermes/profiles/<name>/SOUL.md` after deploy
- **Existing Hermes profiles get updated, not overwritten** — when deploying an agent that already has a Hermes profile, the CLI skips profile creation and only updates .env (token) and SOUL.md. Pre-existing config.yaml stays intact.
- **To reset an agent's personality after changing its template, run deploy again** — the CLI overwrites SOUL.md from the template. For fine-grained edits, edit `~/.hermes/profiles/<name>/SOUL.md` directly.
