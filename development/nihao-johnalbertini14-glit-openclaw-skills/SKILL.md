---
name: nihao
description: Nostr identity setup and health-check CLI. Creates a complete Nostr identity (keypair, profile, relay list, lightning address, Cashu wallet) in one command. Audits existing npub health with a 0–8 score. Single Go binary, non-interactive, agent-friendly.
tags: nostr, bitcoin, lightning, cashu, identity, health-check
---

# nihao 👋

Nostr identity setup and health-check CLI. Single binary, non-interactive, agent-friendly.

Source: https://github.com/dergigi/nihao

## Capabilities Disclosure

This skill installs a single Go binary (`nihao`) that:

- **Generates Nostr keypairs** — random Ed25519 key generation via `crypto/rand`
- **Publishes events** — kind 0 (profile), kind 3 (follows), kind 1 (note), kind 10002 (relay list), kind 10050 (DM relays), kind 17375 (wallet), kind 10019 (nutzap info)
- **Makes HTTP requests** — NIP-05 verification, LNURL resolution, Cashu mint validation, relay NIP-11 probes, image HEAD checks
- **Connects to Nostr relays** — WebSocket connections to publish and query events

It does **not**:
- Store keys on disk (prints nsec to stdout; use `--nsec-file` to write to a file or `--nsec-cmd` to pipe to a command)
- Run as a daemon or background process
- Access local files beyond the binary itself
- Require any accounts, API keys, or KYC

## Prerequisites

- **Go 1.21+** — required to compile the binary from source. Check with `go version`.
  - Install: https://go.dev/dl/ or via your package manager (`brew install go`, `apt install golang`, etc.)

## Install

nihao is distributed as source code compiled locally via Go's standard toolchain. No pre-built binaries are downloaded — the code is fetched from GitHub, compiled on your machine, and placed in your `$GOPATH/bin`.

```bash
go install github.com/dergigi/nihao@latest
```

Verify: `nihao version`

The source is fully auditable at https://github.com/dergigi/nihao.

## On Install

When an agent installs this skill:

### Step 1: Install Binary

```bash
go install github.com/dergigi/nihao@latest
```

### Step 2: Create Identity

```bash
nihao --name "<AGENT_NAME>" --about "<AGENT_BIO>" --nsec-file ./nsec.key --json --quiet
```

This generates a keypair, publishes the identity, and securely writes the nsec to `./nsec.key` with `0600` permissions. Parse the JSON output to extract `npub`, `pubkey`, and `relays`.

**⚠️ The nsec cannot be recovered if lost.** Always use `--nsec-file` or `--nsec-cmd` to persist it securely.

### Step 3: Report to User

Tell the user:
- Their agent's **npub**
- Their agent's **lightning address** (default: `<npub>@npub.cash`)
- Remind them to **back up the nsec**

### Step 4: (Optional) Follow Owner

If the user provides their npub, the agent should follow them. nihao doesn't handle follows of specific npubs — use `nak` or another tool for that.

## Setup — Create a New Identity

```bash
nihao --name "AgentName" --about "I do things" --json
```

What this does:
1. Generates a Nostr keypair (or uses `--sec`/`--stdin`)
2. Publishes profile metadata (kind 0)
3. Publishes relay list (kind 10002) with NIP-65 read/write markers
4. Publishes DM relay list (kind 10050) per NIP-17
5. Publishes follow list (kind 3)
6. Sets up a NIP-60 Cashu wallet (kind 17375 + kind 10019)
7. Sets lightning address to `<npub>@npub.cash`
8. Posts a first note with `#nihao` hashtag

### Setup Flags

| Flag | Purpose |
|---|---|
| `--name <name>` | Display name (default: "nihao-user") |
| `--about <text>` | Bio |
| `--picture <url>` | Profile picture URL |
| `--banner <url>` | Banner image URL |
| `--nip05 <user@domain>` | NIP-05 identifier |
| `--lud16 <user@domain>` | Lightning address (default: `npub@npub.cash`) |
| `--relays <r1,r2,...>` | Override default relay list |
| `--discover` | Discover relays from well-connected npubs |
| `--dm-relays <r1,r2,...>` | Override DM relay list (kind 10050) |
| `--no-dm-relays` | Skip DM relay list publishing |
| `--mint <url>` | Custom Cashu mint (repeatable) |
| `--no-wallet` | Skip wallet setup |
| `--sec, --nsec <nsec\|hex>` | Use existing secret key |
| `--stdin` | Read secret key from stdin |
| `--nsec-file <path>` | Write nsec to file (0600 perms) for secure storage |
| `--nsec-cmd <command>` | Pipe nsec to shell command (alias: `--nsec-exec`) |
| `--json` | JSON output for parsing |
| `--quiet, -q` | Suppress non-JSON, non-error output |

### Key Management

nihao never writes keys to disk by default. Secret keys are handled securely:

- **`--nsec-file <path>`** — writes nsec to a file with `0600` permissions (recommended for automation)
- **`--nsec-cmd <command>`** — pipes nsec to a command's stdin (e.g., a password manager), never as a CLI argument
- **`--stdin`** — reads an existing key from stdin, avoiding shell history and process list exposure
- **`--json` output** — includes nsec in structured output for programmatic parsing

⚠️ **Avoid passing raw nsec values as CLI arguments** (e.g., `--sec nsec1...`) in shared environments, as arguments are visible in process listings. Prefer `--stdin` or `--nsec-cmd` instead.

```bash
# Generate and save securely
nihao --name "Bot" --nsec-file ./bot-nsec.key --json

# Pipe to password manager
nihao --name "Bot" --nsec-cmd "pass insert -m nostr/nsec" --json

# Use existing key via stdin (avoids process list exposure)
echo "$NSEC" | nihao --name "Bot" --stdin
```

## Check — Audit an Existing Identity

```bash
nihao check npub1... --json
```

Checks and scores (0–8):

| Check | What it does |
|---|---|
| `profile` | Kind 0 completeness (name, display_name, about, picture, banner) |
| `nip05` | NIP-05 live HTTP verification, root domain detection |
| `picture` | Image reachability, Blossom hosting detection, file size |
| `banner` | Same as picture |
| `lud16` | Lightning address LNURL resolution |
| `relay_list` | Kind 10002 presence, relay count |
| `relay_markers` | NIP-65 read/write marker analysis |
| `relay_quality` | Per-relay latency, NIP-11 support, reachability |
| `dm_relays` | Kind 10050 DM relay list (NIP-17) |
| `follow_list` | Kind 3 follow count |
| `nip60_wallet` | Kind 17375/37375 wallet presence |
| `nutzap_info` | Kind 10019 nutzap configuration |
| `wallet_mints` | Cashu mint reachability and validation |

### Check Flags

| Flag | Purpose |
|---|---|
| `--json` | Structured JSON output |
| `--quiet, -q` | Suppress non-JSON output |
| `--relays <r1,r2,...>` | Query these relays instead of defaults |

### Exit Codes

| Code | Meaning |
|---|---|
| `0` | All checks pass (score = max) |
| `1` | One or more checks fail |

## Backup — Export Identity Events

```bash
nihao backup <npub|nip05> > identity.json
nihao backup <npub|nip05> --quiet > identity.json
```

Exports all identity-related events as JSON: kind 0 (profile), kind 3 (follows), kind 10002 (relay list), kind 10050 (DM relays), kind 10019 (nutzap info), kind 17375/37375 (wallet). JSON goes to stdout, progress to stderr. Use for snapshots, migration, or archival.

### Backup Flags

| Flag | Purpose |
|---|---|
| `--quiet, -q` | Suppress progress output (JSON always goes to stdout) |
| `--relays <r1,r2,...>` | Query these relays instead of defaults |

## JSON Output

Both setup and check support `--json` for structured, parseable output.

**Setup output:**
```json
{
  "npub": "npub1...",
  "nsec": "nsec1...",
  "pubkey": "hex...",
  "relays": ["wss://..."],
  "profile": { "name": "...", "lud16": "..." },
  "wallet": { "p2pk_pubkey": "02...", "mints": ["https://..."] }
}
```

**Check output:**
```json
{
  "npub": "npub1...",
  "pubkey": "hex...",
  "score": 6,
  "max_score": 8,
  "checks": [
    { "name": "profile", "status": "pass", "detail": "..." },
    { "name": "nip05", "status": "fail", "detail": "not set" }
  ]
}
```

## Integration

### TOOLS.md

After setup, store for quick reference:

```markdown
## Nostr Identity
- npub: npub1...
- Lightning: npub1...@npub.cash
- Relays: relay.damus.io, relay.primal.net, nos.lol
```

### Periodic Health Check

Run `nihao check <npub> --json --quiet` on a schedule to monitor identity health. Parse the JSON and alert if score drops.

## Security

- **No pre-built binaries** — nihao is compiled from source on your machine via `go install`. The source is public and auditable.
- **No key storage** — nihao does not persist keys unless explicitly told to via `--nsec-file` or `--nsec-cmd`.
- **No network exfiltration** — the only network connections are to Nostr relays (WebSocket), NIP-05/LNURL endpoints (HTTPS), and Cashu mints (HTTPS). No telemetry, no analytics, no phoning home.
- **Stdin-first key input** — when using an existing key, prefer `--stdin` over `--sec` to avoid process list exposure.
- **File permissions** — `--nsec-file` writes with `0600` (owner read/write only).

## Defaults

| Setting | Value |
|---------|-------|
| Relays | relay.damus.io, relay.primal.net, nos.lol, purplepag.es |
| DM relays | inbox.nostr.wine, auth.nostr1.com |
| Lightning | `<npub>@npub.cash` |
| Mints | minibits, coinos, macadamia |
| Wallet kind | 17375 (NIP-60) |
