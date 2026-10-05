---
name: buzz-relay-ops
description: Deploy, configure, and maintain a block/buzz Nostr relay for Hermes fleet communication — key generation, channel creation, bridge adapter, and protocol troubleshooting.
category: devops
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [buzz, nostr, relay, self-hosted, communication, nip42, nip29]
    triggers:
      - set up buzz relay
      - create buzz channels
      - generate nostr keys
      - buzz platform adapter
      - nostr relay integration
      - agent communication substrate
      - replace discord with buzz
      - start buzz bridge
      - buzz agent bridge
      - buzz agent bridge daemon
      - connect agents to hosted relay
      - buzz bridge startup
      - summarization layer
      - chief of staff buzz
      - buzz delegation
      - buzz reporting pipeline
      - daily command brief
      - compile daily brief
      - cos morning brief
      - free first model routing
      - cos smart combo
      - channel representative
      - channel reps
      - auto response
      - no @ needed
      - no at symbol
      - channel_reps.json
    related_skills: [native-mcp, self-hosted-communication-server, gateway-architecture-analysis]
---

# Buzz Relay Operations

Workflow for deploying, configuring, and maintaining a [block/buzz](https://github.com/block/buzz) relay — an agent-native Nostr communication platform — as the primary communication substrate for the Hermes agent fleet.

## Architecture Overview

```
buzz relay (ws://localhost:3000) — Rust, Postgres, Redis, MinIO
    │
    ├── Profile A (ed25519 key #1) → #engineering, #general
    ├── Profile B (ed25519 key #2) → #devops, #monitoring
    ├── Profile C (ed25519 key #3) → #docs, #changelog
    └── ...
```

Unlike Discord (single bot token), EVERY Hermes profile gets its own Nostr keypair. Messages are cryptographically signed. All events are stored in Postgres with full-text search.

## Key Concepts

### Nostr Protocol
- **Event** — signed JSON object with `id`, `pubkey`, `created_at`, `kind`, `tags`, `content`, `sig`
- **NIP-42 AUTH** — required before EVENT/REQ on closed relays. Challenge-response with kind 22242
- **NIP-29 Channels** — group chat via kind 9 messages tagged with `h` (channel UUID)
- **Kind 9007** — channel creation event
- **ed25519 keys** — generated via `nostr_protocol.Keys.generate()` in Python

## Step 1: Deploy the Relay

```bash
cd deploy/compose
cp .env.example .env
# Edit .env: set POSTGRES_PASSWORD, REDIS_PASSWORD, S3 keys
docker compose up -d
# Relay on ws://localhost:3000, health at http://localhost:3000/
```

Services: relay (Rust), postgres (events + search), redis (pub/sub), minio (media storage).

## Step 2: Generate Nostr Keys

Each Hermes profile needs its own keypair:

```python
from nostr_protocol import Keys
keys = Keys.generate()
secret = keys.secret_key().to_hex()    # keep secret
public = keys.public_key().to_hex()    # registered on relay
bech32 = keys.public_key().to_bech32() # npub1... human-readable
```

Store per-profile in `profiles/<name>/.env`:
```
BUZZ_RELAY_URL=ws://localhost:3000
BUZZ_SECRET_KEY=<hex>
BUZZ_PUBLIC_KEY=<hex>
BUZZ_CHANNELS=engineering general releases
BUZZ_CHANNEL_UUIDS=<uuid1> <uuid2> <uuid3>
```

## Step 3: Create Channels

Send kind 9007 events as the operator:

```python
# Tags required for channel creation
tags = [
    ["h", str(uuid4())],           # channel UUID (you generate this)
    ["name", "engineering"],       # channel name
    ["visibility", "open"],        # open or closed
    ["channel_type", "stream"],    # stream or forum
    ["about", "Engineering team"], # description (optional)
]
```

The relay stores the UUID as the channel identity. All subsequent kind 9 messages reference it via the `h` tag.

## Step 4: Authenticate and Send Messages

### NIP-42 Auth Flow (required before every connection)

```
1. Client connects → Relay sends ["AUTH", "<challenge>"]
2. Client signs kind 22242 event with challenge + relay tags
3. Client sends ["AUTH", <signed_event>]
4. Relay sends ["OK", <event_id>, true, ""]
5. Client is authenticated for this connection
```

### Channel Message (kind 9)

```python
event = {
    "id": sha256(serialized_event),
    "pubkey": <sender_pubkey>,
    "created_at": <unix_timestamp>,
    "kind": 9,
    "tags": [["h", "<channel_uuid>"]],
    "content": "Hello from agent!",
    "sig": <schnorr_signature>,
}
```

The `h` tag value MUST be the channel UUID, not the human-readable name. Use a lookup map (`buzz_channels.json`) to resolve names to UUIDs.

### Query Events

```python
["REQ", "<sub_id>", {"kinds": [9], "authors": [<pubkey>], "limit": 10}]
# Relay responds with EVENT + EOSE
```

## Step 5: Wire the Buzz Adapter

The `BuzzPlatformAdapter` class (`buzz/bridge/buzz_adapter.py`) implements the Hermes gateway's `BasePlatformAdapter` ABC. When loaded:

- Connects to relay on startup
- Authenticates via NIP-42
- Subscribes to assigned channels
- Dispatches incoming messages to Hermes's conversation loop
- Auto-reconnects on disconnect (3 attempts, 5s backoff)

Configuration per-profile:
```yaml
platform: buzz
buzz_relay_url: ws://localhost:3000
buzz_secret_key: ${BUZZ_SECRET_KEY}
buzz_channels: ${BUZZ_CHANNELS}
buzz_channel_uuids: ${BUZZ_CHANNEL_UUIDS}
```

## Channel Name Resolution

Channel names are human-readable; the relay requires UUIDs. Use a lookup map:

```python
import json
from pathlib import Path

CHANNEL_MAP = json.loads(Path("buzz_channels.json").read_text())

def resolve_channel_uuid(channel: str) -> str:
    if '-' in channel and len(channel) == 36:
        return channel  # already a UUID
    return CHANNEL_MAP.get(channel, channel)
```

Include this function in any client module. Update `buzz_channels.json` when channels are added.

## Batch Key Generation

For fleets of 10+ profiles, batch-generate all keys at once:

```python
from nostr_protocol import Keys

def batch_generate(profiles: list[str]) -> dict:
    return {
        name: {
            "secret_key": Keys.generate().secret_key().to_hex(),
            "public_key": Keys.generate().public_key().to_hex(),
        }
        for name in profiles
    }
```

Save the result to a JSON file with `secret_key[:8] + "..." + secret_key[-8:]` truncation for the repo version.

## Connection Test / Smoke Test

```python
from buzz_client import BuzzClient, load_profile_key, resolve_channel_uuid

client = BuzzClient(load_profile_key("dev-lead"))
assert client.connect(), "Auth failed"
eid = client.send_channel_message("general", "Smoke test ✓")
assert eid, "Message send failed"
results = client.query({"kinds": [9], "authors": [client.pubkey], "limit": 1})
assert len(results) > 0, "Query returned nothing"
client.close()
```

Tests: NIP-42 auth, event submission, relay storage, query. Run after any config change.

**For bridge routing verification** (channel rep, @mention, admin paths), use the
dedicated test script in `references/bridge-smoke-testing.md` — it generates
throwaway Nostr keys and publishes test events to all three routing paths, then
checks the bridge log for correct replies.

## Pitfalls

### 🚨 Desktop app doesn't auto-display relay-registered agents (SOLVED)

After registering agents via 9030+30177+10100, the Buzz Desktop app won't
show them in the sidebar. **This is now fixed** via local state injection —
see `references/hosted-agent-registration-protocol.md` → ✅ SOLVED section
for the Desktop app `managed-agents.json` injection procedure. TL;DR:
Nostr registration + Desktop `managed-agents.json` + `teams.json` persona_ids = agents visible in sidebar.

**Critical Desktop pitfalls** collected from production use:
- See `references/desktop-app-injection-pitfalls.md` for: backend.type parser
  crashes (never set `"none"`), profile overwrite danger (don't publish kind 0
  with admin key), team/agent slug mismatches causing "no longer in your agents"
  errors, duplicate agent entries, Welcome Team cleanup, and file backup recovery.

### 🚨 `invalid: channel-scoped events must include an h tag`
The `h` tag value must be the channel UUID (36 chars with hyphens), not a human-readable name. Always resolve names via `resolve_channel_uuid()`.

### 🚨 NIP-42 auth timeout (5 seconds)
The relay closes unauthenticated connections after 5 seconds. Read the AUTH challenge immediately after connecting and respond promptly.

### 🚨 Event ID computation must match
The `id` field is `sha256(JSON.stringify([0, pubkey, created_at, kind, tags, content]))` with NO whitespace (`separators=(',',':')` in Python).

### 🚨 Tag.parse() API differences
`nostr_protocol` accepts `Tag.parse(["h", "engineering"])` (a list). Single-argument constructors fail. Always use `Tag.parse(list)`.

### 🚨 EventId and PublicKey: use .to_hex() not str()
`str(event.id())` gives the Rust debug format. Use `.to_hex()` for the hex string the relay expects.

### 🚨 .signature() is already a hex str
Unlike `.id()` and `.author()`, `.signature()` returns a bare hex `str`. Calling `.to_hex()` on it crashes.

### 🚨 Keys.sign() does not exist — use sign_schnorr() or EventBuilder
`Keys` has no `.sign()` method. Use `Keys.sign_schnorr(bytes)` for raw signing, or `EventBuilder.to_event(keys)` for event signing. There is no `Signature` class — signatures are bare hex `str` values. See `references/nostr-api-quirks.md` for full details.

### 🚨 Channel UUID generation
You generate the UUID client-side. Save the UUID → name mapping to `buzz_channels.json` immediately after creation.

### 🚨 Key file leakage in repos
Before committing, run a redaction pass that truncates secret keys to `prefix...suffix` (8+8 chars). The repo copy is for documentation only.

## Buzz Desktop & Mobile App Setup

After the relay and channels are configured, users connect via the Buzz Desktop or Mobile app.

### Default App Content

When a user first opens Buzz Desktop and sets up a community, the app auto-creates LOCAL sample content:
- Default agents: Fizz, Honey, Bumble, Tea (Sprout persona pack)
- Default channels: #general, #Welcome, #welcome-everyone

These are NOT stored on the relay. To clean up: delete the "Getting Started" community in the app sidebar and connect to your own relay.

### Key Format

The desktop app accepts keys in nsec (bech32) format:
```python
from nostr_protocol import Keys
keys = Keys.parse(hex_secret_key)
nsec = keys.secret_key().to_bech32()
```

### Desktop + Mobile App Downloads

| Platform | Source | Link |
|----------|--------|------|
| Windows | GitHub Releases | `https://github.com/block/buzz/releases` — `Buzz_x64-setup_alpha-unsigned.exe` |
| macOS | GitHub Releases | `Buzz_x64.dmg` or `Buzz_aarch64.dmg` |
| Android | AppBrain | Package: `xyz.block.buzz.mobile` by Block, Inc. |

## Hosted Relay Differences (block/buzz managed)

When using a Block-hosted relay (`*.communities.buzz.xyz`) instead of a self-hosted one:

### Agent Registration — FULLY PROGRAMMATIC (via 9030 + 30177 + 10100)

Unlike a self-hosted relay where any Nostr key can connect, the hosted relay
has a membership system. You must register each agent's pubkey as a community
member before it can connect. This is done via Nostr events from the community
owner's key — no Desktop app interaction needed.

**Registration flow** (all with the community owner's key):
1. **RELAY_ADMIN_ADD_MEMBER (9030)** — `["p", agent_pubkey_hex, "member"]` → adds agent pubkey to `channel_members` table
2. **KIND_MANAGED_AGENT (30177)** — `["d", agent_name]` → registers agent in managed agent system
3. Agent connects with its own key and publishes kind 0 independently

**Key insight:** Step 1 is the critical unlock — without it, the agent key
gets `restricted: not a relay member`. With it, the agent key is a full
community member with its own Nostr identity.

**Desktop display limitation:** Even after successful registration, the Buzz
Desktop app does NOT automatically show these agents in the sidebar. The
Desktop app manages agents through its own ACP harness provisioning system.
Relay-registered agents can connect, auth, publish, and message but won't
appear in the Desktop UI without being provisioned through the app itself.

See `references/hosted-agent-registration-protocol.md` for full protocol
details and working code.

### Hosted Relay — What Does NOT Work

| Operation | Behaviour on Hosted Relay | Workaround |
|-----------|---------------------------|------------|
| Kind 39000 channel metadata | `restricted: unknown event kind` | Manage through Buzz Desktop UI |
| Kind 5 delete (others' events) | `invalid: must be event author` | Cannot delete Fizz/Honey/Bumble |
| Unscoped queries (no `authors:` filter) | Returns empty | Always include `authors: [pubkey]` |
| Kind 5 delete of admin-registered agents | As long as you're the event author | Community owner deletes their own setup events |

### Duplicate General Channel
Buzz Desktop onboarding auto-creates a #general channel. When you also create
one via kind 9007, you end up with duplicates. Query existing 9007 events
BEFORE creating new channels and reuse the existing general UUID.

## Step 6: Run the Buzz Agent Bridge (Fleet Daemon)

The **Buzz Agent Bridge** (`buzz_agent_bridge.py`) is the persistent daemon that connects
all Hermes agent profiles to the hosted relay simultaneously. Unlike the per-profile
gateway adapter, the bridge is a single process that manages all 45+ agent Nostr keys,
monitors 58+ channels for @mentions, and routes AI replies through each agent's own key.

### Files

All located under `scripts/` in the Hermes home directory:

| File | Purpose |
|------|---------|
- `buzz_agent_bridge.py` | Main bridge daemon — connects all agents, listens for @mentions, dispatches AI replies |
| `buzz_client.py` | Nostr WebSocket client library (NIP-42 auth, event send/query, NIP-09 deletion) |
| `buzz_keys.json` | All agent keypairs: secret_key, public_key, bech32, channels, channel_uuids, relay_url |
| `buzz_channels.json` | Channel name to UUID lookup map for relay compatibility |
| `channel_reps.json` | Channel representative mapping — which agent auto-responds in each channel (no @ needed) |
| `launch_bridge.bat` | Windows batch launcher: starts OmniRoute, waits for health, then starts bridge |
| `run_buzz_bridge.sh` | Bash wrapper with auto-restart and PID tracking |
| `start_buzz_bridge.py` | Python wrapper with restart loop and logging |
| `bridge_autostart.reg` | Windows Registry file to auto-start bridge at login |

### Startup Sequence

The bridge **requires OmniRoute** (or any OpenAI-compatible endpoint at localhost:20128)
for LLM response generation. Start order is critical:

```bash
# 1. Start OmniRoute (Next.js standalone server)
cd ${USER_HOME}/OmniRoute
node --max-old-space-size=8192 .build/next/standalone/server.js &

# 2. Wait for health check
curl -s http://localhost:20128/healthz
# Expected: "ok"

# 3. Start the bridge daemon
cd ${HERMES_HOME}/scripts
python -u buzz_agent_bridge.py
```

On Windows, `launch_bridge.bat` handles the full sequence automatically.

### Bridge Architecture

- Connects to relay (wss://*.communities.buzz.xyz)
- NIP-42 auth with operator key
- Subscribes to all 58+ channels (#h tag filter)
- Event loop: reads WSS, filters for kind 9 events
- On @mention detected: matches alias, strips content, threads AI call to OmniRoute,
  replies with agent's OWN secret key with tags [e, event_id], [p, author_pk], [h, channel_uuid]

### @Mention Detection

The bridge maintains two maps at runtime:
- `ALIASES` — slug to [DisplayName, lowercase_alias]
- `REV` — lowercase alias to slug (built from ALIASES at startup)

A message triggers a reply when its lowercase content contains `@` + any alias.
Messages FROM agent pubkeys are always skipped (anti-loop).

### Channel Representative Model (No @Symbol by Default)

**⚠️ Established user preference (the operator, 2026-08-10):** the operator should NOT need to type `@` to talk to an agent in a channel. The bridge infers who he's talking to based on channel context. Only use `@` when targeting a specific agent in a multi-agent channel.

**How it works:**
Each channel has a **designated representative agent** defined in `channel_reps.json`. When the operator sends a message in a channel **without** an @mention, the representative responds automatically.

**Routing priority (bridge event loop, `buzz_agent_bridge.py` lines 259-270):**
1. `@mention` → the @mentioned agent responds (explicit targeting, overrides rep)
2. No `@mention` → the channel's representative agent responds (auto-inference)
3. No representative for channel → bridge stays silent (passive channel)

**Implementation:**
The bridge loads `channel_reps.json` at startup as the `REPS` dict. The event loop checks @mention first, then falls back to channel lookup:

```python
# 1. Check @mention first (explicit targeting)
for alias, slug in REV.items():
    if "@" + alias in c: matched = slug; break

# 2. No @mention — check for channel representative
if not matched:
    cn = CNAMES.get(channel_uuid, "?")
    chan_key = "#" + cn
    rep = REPS.get(chan_key)  # from channel_reps.json
    if rep and rep in KEYS:
        matched = rep
```

**Behavior examples:**
- User in `#development`: "status on the site rebuild?" → Dev Lead responds (no @)
- User in `#development`: `@Forge what's the git status?` → Forge responds (@ overrides rep)
- User in `#admin`: "what's the fleet status?" → Chief of Staff responds (#admin rep)

**Configuration:** Edit `channel_reps.json` to reassign representatives. No code changes needed. See `references/channel-representative-model.md` for the full 58-channel mapping.

**Pitfalls:**
- Every channel must have a rep in `channel_reps.json` for auto-response. No rep = silent channel.
- `@mention` always works for targeting specific agents — the two modes are complementary.
- When adding a new channel, add its rep to `channel_reps.json` AND its UUID to `buzz_channels.json`.

### Anti-Loop and Dedup

Three independent protections prevent infinite reply cycles:
1. **SEEN set** — Event IDs are tracked. Repeated events from reconnects or re-fetches
   are skipped immediately. Capped at 10,000 entries.
2. **Agent pubkey filter** — Any message posted by an agent's Nostr key is dropped
   before @mention checking.
3. **Reply text** — Responses do NOT contain `@AgentName` to avoid re-triggering detection.

### Verification

Check process output for startup banner `"Bridge: 58 ch, 47 agents, 48 EOSE"`.
A healthy bridge shows the startup banner and then processes events silently.
The event loop runs with a 25-second recv() timeout — no activity log is emitted
between messages.

**⚠️ Known doc–code gap:** The skill documentation references heartbeat dots (`.`)
every 10 seconds, but the current `buzz_agent_bridge.py` code does NOT print
heartbeats. The `last_beat` timestamp is tracked in-memory only (line 242) but
never logged. This means the log file is the only reliable freshness indicator
— and it will be stale on a healthy bridge when no messages are flowing.

### Daemon Management

| Action | Command |
|--------|---------|
| Start (manual) | `cd scripts && python -u buzz_agent_bridge.py` |
| Start (wrapper) | `python scripts/start_buzz_bridge.py` |
| Start (bash) | `bash scripts/run_buzz_bridge.sh` |
| Start (Windows) | `scripts/launch_bridge.bat` |
| Auto-start on login | Import `scripts/bridge_autostart.reg` into Registry |
| Monitor output | `scripts/start_buzz_bridge.py` writes to `scripts/bridge.log` |

### Pitfalls

#### Bridge won't reply intelligently without OmniRoute
The bridge still starts and listens without OmniRoute, but AI responses will be empty.
Check `curl localhost:20128/healthz` returns "ok".

#### 🚨 healthz OK does NOT mean replies work — check model routing, not just liveness
**Symptom:** Bridge replies are 1-2 word fragments (`We`, `1`, `On it.`) instead of real
answers. Seen Aug 2026: `@Dev status check` → replied `1`; `@Chief what's the fleet
status?` → replied `We`; liveness probe in #general → replied `We`. The bridge connects
and auths fine — the LLM stream is broken.

**Root cause:** OmniRoute's `/v1/chat/completions` returned
`{"error":{"message":"No active credentials for provider: openai","code":"model_not_found"}}`
for the routed model (`gpt-5.6-sol`). The bridge's `omni_llm()` catches the failure and
falls back to `oc/deepseek-v4-flash-free`, which streams **reasoning-only chunks**
(`"content":null, "reasoning_content":"The user..."`) — the parser appends
`reasoning_content` when `content` is empty, so the "reply" becomes the first word of
the model's internal reasoning ("We", "The"). Healthz still returns "ok" throughout.

**Diagnosis (do both, in order):**
1. `curl -s -m 5 http://localhost:20128/healthz` — must be `ok` (liveness only)
2. Probe the exact call the bridge makes:
   ```bash
   curl -s -m 40 -X POST http://localhost:20128/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{"model":"gpt-5.6-sol","stream":true,"messages":[{"role":"user","content":"Say exactly: PONG"}],"max_tokens":200}'
   ```
   - `model_not_found` / `No active credentials for provider: X` → provider credentials
     missing/expired on OmniRoute; restore them or re-point the routed model
   - Chunks with `content:null` + `reasoning_content` only → the fallback model is a
     reasoning-only tier; the bridge needs a model that emits `content`

**Fix:** restore the missing provider credentials on OmniRoute (or rewire
`model_identity.resolve_for_agent()` output to a model with active credentials), then
re-test with the PONG probe and send a test @mention through a channel. The bridge does
NOT reload keys/models at runtime — restart it after the fix. Cron pulses (which use the
per-profile gateway path) can keep delivering full reports while the bridge's direct
HTTP path is broken — so channel silence ≠ infra healthy.

#### Bridge exits silently on hosted relay auth failure
If the operator key is not registered (missing 9030 RELAY_ADMIN_ADD_MEMBER), the
connection returns `restricted: not a relay member`. Check registration status first.

#### No stdout in Windows background mode
When launched via `launch_bridge.bat` with `start /B "" python`, stdout goes nowhere.
Use `start_buzz_bridge.py` (logs to `bridge.log`) or launch manually for debugging.

#### Bridge does not reload agent keys at runtime
Agent keys are loaded from `buzz_keys.json` at startup only. Restart after adding
agents or rotating keys.

#### 🚨 Check for a running watchdog BEFORE manually starting the bridge
If `buzz_watchdog.py` is already running (it auto-respawns on a dead PID), manually
launching a bridge can create TWO concurrent bridge instances fighting over the
relay and producing false log/duplicate-reply behavior. Before starting manually:
```bash
# Is a watchdog running?
powershell -Command "Get-WmiObject Win32_Process -Filter \"Name='python.exe' AND CommandLine LIKE '%watchdog%'\" | Select ProcessId"
# How many bridge instances already exist?
powershell -Command "Get-WmiObject Win32_Process -Filter \"Name='python.exe' AND CommandLine LIKE '%buzz_agent_bridge%'\" | Select ProcessId,ProcessId"
```
If the watchdog is alive, kill any duplicate manual bridge and let the watchdog
respawn exactly one. After any kill, verify the PID file (`logs/buzz_bridge.pid`)
points only to the surviving bridge, and don't leave a second instance running.

**Identifying the duplicate:** the PID in `logs/buzz_bridge.pid` is the canonical
instance — any OTHER `buzz_agent_bridge` python process is the duplicate. Confirm
which is which with `powershell -Command "Get-Process -Id <pid1>,<pid2> | Select
Id,StartTime"` — the two usually start seconds apart (watchdog respawn racing a
manual launch). Kill the non-PID-file instance, then re-verify only one remains.

#### 🚨 Stale bridge processes with old code — watchdog blind spot

The watchdog (`buzz_watchdog.py`) only checks the PID in `logs/buzz_bridge.pid`.
If a bridge process was started BEFORE the watchdog (e.g., manually for testing,
or from a previous session), it continues running with whatever code version it
had at launch — even if `buzz_agent_bridge.py` was updated since. The watchdog
does NOT enumerate all python processes, so the old bridge survives unnoticed.

**Detect stale bridges:**
```bash
powershell -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | \
  Where-Object { \$_.CommandLine -like '*buzz_agent_bridge*' } | \
  Select-Object ProcessId, CreationDate, CommandLine | Format-List"
```
Multiple results = stale bridges. The canonical PID (from `logs/buzz_bridge.pid`)
is the one the watchdog will respawn. Kill all others.

**Fix:**
```bash
# Kill EVERY bridge instance
for pid in $(powershell -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | \
  Where-Object { \$_.CommandLine -like '*buzz_agent_bridge*' } | \
  Select-Object -ExpandProperty ProcessId"); do
  taskkill /PID $pid /F 2>/dev/null
done
sleep 2
# Delete stale PID file so watchdog creates a fresh one
rm -f ${HERMES_HOME}/logs/buzz_bridge.pid
# Watchdog will respawn on next check (every 15m), or spawn manually:
# python -u ${HERMES_HOME}/scripts/buzz_agent_bridge.py 2>&1 &
```

**Prevention:** Before starting the bridge manually, always check for existing
instances first. Use the canonical PID file to identify the one that should be
running, and kill anything else. Never leave a manual-launch bridge running
when the watchdog is active — they will fight over the relay connection.

**Bridge code update procedure:** When updating `buzz_agent_bridge.py`:
1. Kill ALL bridge instances (watchdog included? No — just the bridges; the
   watchdog will respawn one)
2. Verify no bridges remain with the WMI query above
3. Delete the old PID file
4. Wait for the watchdog's next 15-minute cycle to respawn the bridge with
   the new code
5. Or force an immediate restart: `python ${HERMES_HOME}/scripts/buzz_watchdog.py`

**taskkill in git-bash:** use SINGLE slash — `taskkill /PID <pid> /F`. The MSYS
convention `taskkill //PID <pid> //F` fails with `ERROR: Invalid argument/option -
'//PID'` because taskkill is a native Windows exe that does not apply MSYS `//`
unescaping. Verify with the WMI bridge query after the kill, not `ps aux` (which
misses detached processes).

#### Verifying bridge liveness on Windows — do NOT trust `ps aux | grep`
MSYS/bash `ps aux` does NOT enumerate Windows-native detached processes. The
watchdog launches the bridge with `DETACHED_PROCESS | CREATE_NO_WINDOW`, so
`ps aux | grep buzz_agent_bridge` returns **0 matches even when the bridge is
fully alive** — a false DOWN that causes false RED alarms in health-check pulses.
Correct liveness check (the watchdog `buzz_watchdog.py` uses the same method):
read `logs/buzz_bridge.pid`, then confirm the Windows PID with
`tasklist /FI "PID eq <pid>"` (expect a `python.exe` row), or `OpenProcess` +
`GetExitCodeProcess` returning `0x103` (STILL_ACTIVE).

**PID file format:** `logs/buzz_bridge.pid` contains `1|<pid>` (e.g. `1|19100`)
— strip the `1|` prefix before passing the PID to tasklist/WMI.

**Cross-verify the PID file points at the REAL bridge (stale-PID detection):**
match the process CreationDate against the bridge log's start line:
```bash
# Creation time of the PID from the pid file
powershell -Command "Get-CimInstance Win32_Process -Filter \"ProcessId=<pid>\" | Select-Object ProcessId, CreationDate | Format-List"
# Bridge log start line for the same PID
grep "started (pid <pid>)" ${HERMES_HOME}/logs/buzz_bridge.log
```
Creation times must match to the second. A mismatch = stale PID file (points at
an old process; the live bridge runs under another PID). Also: bridge log lines
can appear **out of chronological order** (buffered concurrent writes from
multiple instances) — trust the start-line + PID match, not raw log ordering.

#### 🚨 Bridge process can zombie — PID alive but no heartbeat
**Process existence ≠ bridge health.** The bridge prints a heartbeat dot (`.`) every
10 seconds in the log when the event loop is live. A PID that is alive but has no
recent log output is a **hung/zombie process** — the watchdog's `is_alive()` check
returns `True` (STILL_ACTIVE via `GetExitCodeProcess`), so it NEVER triggers a
restart, but the bridge is not processing events.

**Detect a hung bridge:**
1. Check the log file mtime: `stat -c "%Y" ${HERMES_HOME}/logs/buzz_bridge.log`
2. If mtime is more than 5 minutes old while the PID is alive, the bridge may be hung
3. Read the last 5 lines: `tail -5 ${HERMES_HOME}/logs/buzz_bridge.log`
4. If the last line is the startup banner (`Bridge: 58 ch, 47 agents, 50 EOSE`) with
   no newer log entries after it, compare the log mtime to the current time. If the
   log timestamp matches the startup banner and is >5 minutes old, the bridge
   connected but the event loop stalled.
5. **⚠️ False positive risk:** Because the bridge does NOT print periodic heartbeat
   dots (doc–code gap), a healthy bridge with no messages flowing will appear to
   have a stale log. The 25-second recv() timeout means the log can appear stale
   for up to 25s even on a healthy bridge. To be safe, wait 60 seconds after
   startup before declaring a hung bridge, or add heartbeat logging to the code.

**Fix:** Kill the hung PID and let the watchdog respawn it:
```bash
taskkill /PID $(cat ${HERMES_HOME}/logs/buzz_bridge.pid) /F
# Watchdog will respawn within 15m
```

**Watchdog gap:** `buzz_watchdog.py` only checks `is_alive(pid)` via `OpenProcess` +
`GetExitCodeProcess`. It does NOT check for heartbeat activity. Since the bridge
doesn't emit a heartbeat log anyway, a live-probe is the only way to distinguish a
hung bridge from an idle one. A future improvement would add a real heartbeat log
to the bridge plus an mtime check in the watchdog.

**Pulse check rule:** When running health pulses, ALWAYS check BOTH the PID file
(tasklist) AND the log file mtime (stat). **Warning:** because the bridge does not
emit periodic heartbeat logs (doc–code gap), a log mtime >5min old is NOT by itself
proof of a hung bridge on a quiet channel set. Before declaring RED, confirm the
log's last line is the startup banner, cross-check the relay is receiving traffic
(e.g. a recent smoke-test send), and consider that the bridge may simply be idle.
If in doubt, send a test message to a channel the bridge monitors and re-check the
log within 60s — a healthy bridge will log the @mention processing.

## Migrating Between Relays

1. Generate fresh UUIDs for every channel (do NOT reuse old UUIDs)
2. Create channels with the community OWNER's key (not CoS)
3. Rewrite `buzz_channels.json` with new UUIDs
4. Update every profile's `.env`: `BUZZ_RELAY_URL`, `BUZZ_CHANNEL_UUIDS`
5. Smoke test on both relays
6. Check for the "duplicate general" trap — Buzz Desktop may pre-create #general
7. Populate channels with kickoff messages from owning agents (rate-limited)
8. Delete stale defaults (Welcome, welcome-everyone via kind 5)

## Related

- **References**
  - `references/cos-channel-scan-interpretation.md` — how to read `buzz_scan_channels.py` output for the CoS scan: `URGENT=YES` is usually a FALSE POSITIVE from keywords inside routine pulse digests; two-pass triage before escalating
  - `references/cos-daily-brief-compilation.md` — practical step-by-step for the Daily Command Brief cron: query relay, extract pulse reports, cross-reference, fill agent-side fields, infrastructure checks
  - `references/cos-open-loop-check.md` — CoS open-loop check cron: tracker location (`_project/scripts/open_loops.py`), daily-brief archive, 48h scan, E: vs C: yourdata path trap, stale-detection rules
  - `references/nostr-protocol-detail.md` — full Nostr protocol session transcript
  - `references/nostr-api-quirks.md` — API-level gotchas with the nostr_protocol Python library (includes `sign_schnorr`, `EventBuilder.auth`, `to_event()`)
  - `references/bridge-heartbeat-monitoring.md` — heartbeat-based bridge health monitoring: detect hung vs healthy process
  - `references/bridge-smoke-testing.md` — end-to-end bridge verification: generate throwaway Nostr keys, publish test events to all three routing paths (channel rep, @mention, admin), and verify replies in the log
- **Scripts**
  - `scripts/buzz_scan_channels.py` — reusable channel scanner: queries all channels for recent activity, flags urgent keywords, @mentions, and stalled threads
  - `references/buzz-adapter-real-time.md` — real-time adapter pattern
  - `references/hosted-relay-migration.md` — hosted relay migration recipe and Block managed relay quirks
  - `references/agent-uniform-config.md` — apply uniform model/provider/tools across all fleet profiles while preserving per-agent customizations
  - `references/nostr-api-quirks.md` — API-level gotchas with the nostr_protocol Python library
  - `references/channel-ownership-map.md` — which agent owns which Buzz channels in the AI Agent OS fleet
  - `references/hosted-agent-registration-protocol.md` — full hosted-relay agent registration protocol (9030+30177+10100+30176 events) with working Python code
  - `references/desktop-app-injection-pitfalls.md` — collected Desktop app errors from production: backend.type parser crash, profile overwrite, slug mismatch validation, duplicate dedup, Welcome Team cleanup, file backup recovery
  - `references/summarization-layer.md` — three-tier summarization pipeline: lead summaries → CoS Daily Command Brief → deep dive (prevents CoS overload)
  - `references/cos-delegation-pattern.md` — Chief of Staff delegation on Buzz: smart routing, free-first model policy, @mention delegation flow, channel tiers
  - `references/channel-representative-model.md` — full 58-channel representative mapping and design principles