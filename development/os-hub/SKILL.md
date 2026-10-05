---
name: os-hub
description: SolanaOS Hub — skill registry, gateway management, and control UI. Use when managing skills via ClawHub CLI, connecting to the SolanaOS gateway (TCP bridge on port 18790, WebSocket on port 18793), or working with the Lit-based control UI at ui/.
metadata:
  {
    "solanaos":
      {
        "requires": { "bins": ["clawhub"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "clawhub",
              "bins": ["clawhub"],
              "label": "Install ClawHub CLI (npm)",
            },
          ],
      },
  }
---

# SolanaOS Hub

Central hub for skill management, gateway operations, and the control UI.

## Architecture

```
┌──────────────────┐     ┌────────────────────┐     ┌──────────────────┐
│   Control UI     │────▶│   Gateway Bridge   │────▶│   Headless Nodes │
│  (Lit + Vite)    │ WS  │  (Go TCP Server)   │ TCP │  (Orin/RPi/etc)  │
│  ui/             │     │  pkg/gateway/       │     │                  │
└──────────────────┘     └────────────────────┘     └──────────────────┘
     Port 5173 (dev)        Port 18790 (bridge)
                            Port 18793 (WS/canvas)
```

### Key Codebase Paths

| Component | Path | Description |
| --- | --- | --- |
| **Gateway Bridge** | `pkg/gateway/bridge.go` | TCP server, node auth, JSON-line protocol |
| **Gateway WebSocket** | `pkg/gateway/ws.go` | WebSocket transport for browser clients |
| **Control UI** | `ui/` | Lit web components, Vite build, connects via WS |
| **UI Gateway Client** | `ui/src/ui/gateway.ts` | WebSocket client with device auth |
| **Skills** | `skills/` | All operator skills (this directory) |

## Control UI

The control UI is a Lit web component app at `ui/`.

### Dev Server

```bash
cd /Users/8bit/solanaos/ui && npm run dev
```

### Build

```bash
cd /Users/8bit/solanaos/ui && npm run build
```

### Test

```bash
cd /Users/8bit/solanaos/ui && npm test
```

### UI connects to gateway via WebSocket

The UI uses `solanaos-gateway` subprotocol to communicate with the Go gateway. See `ui/src/ui/gateway.ts` for the client implementation. Protocol frames:

- `hello-ok` — auth handshake with device token
- `event` — server-push events (presence, health, state)
- `res` — request/response pairs

## Gateway

The Go-native gateway at `pkg/gateway/` provides:

- **TCP Bridge** (port 18790): JSON-line protocol for headless nodes
- **WebSocket** (port 18793): Browser/extension connections
- **Auth**: Token-based + device identity signing (Ed25519)
- **Canvas Host**: Serves HTML to connected nodes

### Start Gateway

```bash
cd /Users/8bit/solanaos && go build -ldflags="-s -w" -o build/solanaos . && ./build/solanaos node gateway-spawn
```

### Configuration

In `~/.solanaos/solanaos.json`:

```json
{
  "gateway": {
    "bind": "auto",
    "port": 18790,
    "authToken": "your-token"
  },
  "canvasHost": {
    "enabled": true,
    "port": 18793,
    "root": "~/clawd/canvas"
  }
}
```

## ClawHub CLI (Skill Registry)

Install

```bash
npm i -g clawhub
```

Auth (publish)

```bash
clawhub login
clawhub whoami
```

Search

```bash
clawhub search "postgres backups"
```

Install

```bash
clawhub install my-skill
clawhub install my-skill --version 1.2.3
```

Update (hash-based match + upgrade)

```bash
clawhub update my-skill
clawhub update my-skill --version 1.2.3
clawhub update --all
clawhub update my-skill --force
clawhub update --all --no-input --force
```

List

```bash
clawhub list
```

Publish

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.2.0 --changelog "Fixes + docs"
```

Notes

- Default registry: https://clawhub.com (override with CLAWHUB_REGISTRY or --registry)
- Default workdir: cwd (falls back to SolanaOS workspace); install dir: ./skills (override with --workdir / --dir / CLAWHUB_WORKDIR)
- Update command hashes local files, resolves matching version, and upgrades to latest unless --version is set
