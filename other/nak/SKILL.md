---
name: nak
description: The Nostr Army Knife (nak) CLI. Use this skill to interact with the Nostr network, publish events, query relays, manage keys, and perform advanced Nostr operations like NIP-46 signing, NIP-60 wallet management, and Blossom file uploads.
compatibility: Requires `nak` CLI (v0.15.3+ recommended).
---

# `nak` - Nostr Army Knife

`nak` is a powerful CLI for interacting with the Nostr protocol. It handles event creation, signing, publishing, querying, key management, and more.

## Usage

### 1. Events (`nak event`)

Generate, sign, and publish events.

```bash
# Publish a simple text note (Kind 1) to specific relays
nak event -c "Hello Nostr" wss://relay.damus.io wss://nos.lol

# Publish using a specific secret key (hex or nsec)
nak event -c "Authenticated message" --sec <nsec/hex> wss://relay.damus.io

# Reply to an event (Kind 1)
nak event -c "I agree!" -e <event_id> --sec <nsec/hex> wss://relay.damus.io

# Create a profile metadata event (Kind 0)
echo '{"name":"bob","about":"builder"}' | nak event -k 0 --sec <nsec/hex> wss://relay.damus.io

# Generate an event JSON without publishing (dry run)
nak event -c "Just checking" -k 1 --sec <nsec/hex>
```

### 2. Querying (`nak req`)

Subscribe to relays and filter events.

```bash
# Listen for all Kind 1 notes on a relay
nak req -k 1 wss://relay.damus.io

# Listen for a specific author
nak req -a <pubkey_hex> wss://relay.damus.io

# Listen for replies to a specific event (E-tag)
nak req -e <event_id> wss://relay.damus.io

# Fetch with a limit
nak req -k 1 --limit 10 wss://relay.damus.io

# Output is stream of ["EVENT", ...] JSON arrays.
# Pipe to jq for readability:
nak req -k 1 wss://relay.damus.io | jq
```

### 3. Fetching (`nak fetch`)

Fetch specific events by reference (NIP-19/NIP-05).

```bash
# Fetch an event by nevent
nak fetch nevent1...

# Fetch a profile
nak fetch npub1...

# Fetch from specific relays
nak fetch npub1... --relay wss://relay.nostr.band
```

### 4. Keys & Encoding (`nak key`, `nak encode`, `nak decode`)

Manage keys and NIP-19 entities.

```bash
# Generate a new keypair
nak key generate

# Convert nsec to hex (or vice versa - automated detection)
nak decode nsec1...

# Encode a hex pubkey to npub
nak encode npub <hex_pubkey>

# Encode an event ID to nevent with relay hints
nak encode nevent <event_id> --relay wss://relay.damus.io
```

### 5. Encryption (NIP-44)

Encrypt and decrypt messages.

```bash
# Encrypt a message for a recipient
nak encrypt --sec <sender_nsec> --target <recipient_pubkey> "Secret message"

# Decrypt a message
nak decrypt --sec <recipient_nsec> --source <sender_pubkey> <base64_ciphertext>
```

### 6. Wallet (NIP-60)

Manage a Cashu wallet backed by Nostr relays.

```bash
# Show balance (reloads from relays)
nak wallet --sec <nsec>

# Pay a Lightning invoice
nak wallet pay --sec <nsec> lnbc1...
```

### 7. Blossom (File Storage)

Interact with Blossom media servers.

```bash
# Upload a file
nak blossom upload --server https://cdn.example.com --sec <nsec> ./image.png
```

## Agentic/MCP Mode

`nak` has an `mcp` command that starts a Model Context Protocol server.
```bash
nak mcp
```
This is useful if you want to integrate `nak` directly as an MCP tool source, but usually, you will invoke the CLI commands directly via `exec`.

## Tips

*   **Piping:** `nak` is designed for piping. You can pipe JSON into `nak event` to sign it, or pipe `nak req` output into other tools.
*   **Environment Variables:**
    *   `NOSTR_SECRET_KEY`: Set this to avoid passing `--sec` every time.
