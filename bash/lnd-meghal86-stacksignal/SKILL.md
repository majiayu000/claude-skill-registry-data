---
name: lnd
description: Install and run Lightning Terminal (litd) which bundles lnd, loop, pool, tapd, and faraday in a single Docker container. Defaults to neutrino backend with SQLite storage on testnet. Supports watch-only mode with remote signer, standalone mode, and regtest development. Use when setting up a Lightning node for payments, channel management, liquidity management (loop), channel marketplace (pool), taproot assets (tapd), or enabling agent L402 commerce.
---

# Lightning Terminal (litd) — Lightning Network Node

Install and operate a Lightning Terminal (litd) node for agent-driven payments.
litd bundles lnd with loop, pool, tapd, and faraday — giving agents access to
liquidity management, channel marketplace, and taproot assets in a single
container.

**Default:** Docker container, neutrino backend, SQLite storage, testnet. No full
Bitcoin node required. Use `--network mainnet` for real coins.

**Default mode: watch-only with remote signer.** Private keys stay on a separate
signer container — the agent never touches key material. For quick testing, use
`--mode standalone` (keys on disk, less secure).

## Quick Start (Container — Recommended)

### Watch-Only with Remote Signer (Production)

```bash
# 1. Install litd image
skills/lnd/scripts/install.sh

# 2. Start litd + signer containers
skills/lnd/scripts/start-lnd.sh --watchonly

# 3. Set up signer wallet (first run only)
skills/lightning-security-module/scripts/setup-signer.sh --container litd-signer

# 4. Import credentials and create watch-only wallet
skills/lnd/scripts/import-credentials.sh --bundle ~/.lnget/signer/credentials-bundle
skills/lnd/scripts/create-wallet.sh

# 5. Check status
skills/lnd/scripts/lncli.sh getinfo
```

### Standalone (Testing Only)

```bash
# 1. Install litd image
skills/lnd/scripts/install.sh

# 2. Start litd container
skills/lnd/scripts/start-lnd.sh

# 3. Create standalone wallet (generates seed — keys on disk)
skills/lnd/scripts/create-wallet.sh --mode standalone

# 4. Check status
skills/lnd/scripts/lncli.sh getinfo
```

> **Warning:** Standalone mode stores the seed mnemonic and wallet passphrase on
> disk. Do not use for mainnet funds you cannot afford to lose.

### Regtest Development

```bash
# Start litd + bitcoind for local development
skills/lnd/scripts/start-lnd.sh --regtest

# Create wallet and mine some blocks
skills/lnd/scripts/create-wallet.sh --container litd --mode standalone
docker exec litd-bitcoind bitcoin-cli -regtest -generate 101
```

## Container Modes

| Mode | Command | Containers | Use Case |
|------|---------|-----------|----------|
| Standalone | `start-lnd.sh` | litd | Testing, development |
| Watch-only | `start-lnd.sh --watchonly` | litd + litd-signer | Production |
| Regtest | `start-lnd.sh --regtest` | litd + litd-bitcoind | Local dev |

## Profiles

Profiles customize litd behavior without editing compose files:

```bash
# List available profiles
skills/lnd/scripts/docker-start.sh --list-profiles

# Start with a profile
skills/lnd/scripts/start-lnd.sh --profile taproot
skills/lnd/scripts/start-lnd.sh --profile debug
```

| Profile | Purpose |
|---------|---------|
| `default` | Standard operation (info logging) |
| `debug` | Trace logging, verbose subsystems |
| `taproot` | Simple taproot channels enabled |
| `wumbo` | Large channels up to 10 BTC |
| `regtest` | Regtest network preset |

## Network Selection

Default is testnet. Override with `--network`:

```bash
# Testnet (default — no real coins)
skills/lnd/scripts/start-lnd.sh

# Mainnet (real coins — use with remote signer)
skills/lnd/scripts/start-lnd.sh --network mainnet --watchonly

# Signet (testing network)
skills/lnd/scripts/start-lnd.sh --network signet
```

## litd Sub-Daemons

litd integrates multiple daemons. Access them via the `--cli` flag:

```bash
# lnd CLI (default)
skills/lnd/scripts/lncli.sh getinfo

# Loop — liquidity management (submarine swaps)
skills/lnd/scripts/lncli.sh --cli loop quote out 100000

# Pool — channel marketplace
skills/lnd/scripts/lncli.sh --cli pool accounts list

# Taproot Assets (tapd)
skills/lnd/scripts/lncli.sh --cli tapcli assets list

# Lightning Terminal (litd)
skills/lnd/scripts/lncli.sh --cli litcli getinfo

# Faraday — channel analytics
skills/lnd/scripts/lncli.sh --cli frcli revenue
```

## Installation

Default: pulls the litd Docker image.

```bash
skills/lnd/scripts/install.sh
```

This pulls `lightninglabs/lightning-terminal:v0.16.0-alpha` from Docker Hub and
verifies the image. The litd image includes lncli, litcli, loop, pool, tapcli,
and frcli.

### Build from Source (Fallback)

```bash
skills/lnd/scripts/install.sh --source
```

Requires Go toolchain. Builds lnd and lncli with all build tags.

## Native Mode

For running without Docker, use `--native`:

```bash
# Start natively
skills/lnd/scripts/start-lnd.sh --native --mode standalone

# Stop natively
skills/lnd/scripts/stop-lnd.sh --native
```

Native mode uses the config template at `skills/lnd/templates/lnd.conf.template`
and runs lnd as a background process.

## Remote Nodes

Connect to a remote lnd node with connection credentials:

```bash
skills/lnd/scripts/lncli.sh \
    --rpcserver remote-host:10009 \
    --tlscertpath ~/remote-tls.cert \
    --macaroonpath ~/remote-admin.macaroon \
    getinfo
```

## MCP / Lightning Node Connect

For read-only access without direct gRPC connectivity, use the
`lightning-mcp-server` skill with Lightning Node Connect (LNC). LNC uses
encrypted WebSocket tunnels — no TLS certs, macaroons, or open ports needed.
Just a pairing phrase from Lightning Terminal.

```bash
skills/lightning-mcp-server/scripts/install.sh
skills/lightning-mcp-server/scripts/configure.sh
skills/lightning-mcp-server/scripts/setup-claude-config.sh
```

## Wallet Setup

### Watch-Only Wallet (Default)

Imports account xpubs from the remote signer — no seed or private keys on this
machine.

```bash
# Import credentials bundle from signer
skills/lnd/scripts/import-credentials.sh --bundle <credentials-bundle>

# Create watch-only wallet (auto-detects litd container)
skills/lnd/scripts/create-wallet.sh
```

### Standalone Wallet

Generates a seed locally. Use only for testing.

```bash
skills/lnd/scripts/create-wallet.sh --mode standalone
```

Handles the full wallet creation flow via REST API:
1. Generates a secure random wallet passphrase
2. Calls `/v1/genseed` to generate a 24-word seed mnemonic
3. Calls `/v1/initwallet` with the passphrase and seed
4. Stores credentials securely:
   - `~/.lnget/lnd/wallet-password.txt` (mode 0600)
   - `~/.lnget/lnd/seed.txt` (mode 0600)

### Unlock Wallet

```bash
skills/lnd/scripts/unlock-wallet.sh
```

Auto-unlock is enabled by default in the container via
`--wallet-unlock-password-file`. Manual unlock is only needed if auto-unlock
is disabled.

### Recover Wallet from Seed (Standalone Only)

```bash
skills/lnd/scripts/create-wallet.sh --mode standalone --recover --seed-file ~/.lnget/lnd/seed.txt
```

## Starting and Stopping

### Start

```bash
# Docker standalone (default)
skills/lnd/scripts/start-lnd.sh

# Docker watch-only (production)
skills/lnd/scripts/start-lnd.sh --watchonly

# Docker with profile
skills/lnd/scripts/start-lnd.sh --profile taproot

# Mainnet
skills/lnd/scripts/start-lnd.sh --network mainnet
```

### Stop

```bash
# Stop (preserve data)
skills/lnd/scripts/stop-lnd.sh

# Stop and clean (remove volumes)
skills/lnd/scripts/stop-lnd.sh --clean

# Stop all litd containers
skills/lnd/scripts/stop-lnd.sh --all
```

## Node Operations

All commands auto-detect the litd container:

### Node Info

```bash
skills/lnd/scripts/lncli.sh getinfo
skills/lnd/scripts/lncli.sh walletbalance
skills/lnd/scripts/lncli.sh channelbalance
```

### Funding

```bash
skills/lnd/scripts/lncli.sh newaddress p2tr
skills/lnd/scripts/lncli.sh walletbalance
```

### Channel Management

```bash
skills/lnd/scripts/lncli.sh connect <pubkey>@<host>:9735
skills/lnd/scripts/lncli.sh openchannel --node_key=<pubkey> --local_amt=1000000
skills/lnd/scripts/lncli.sh listchannels
skills/lnd/scripts/lncli.sh closechannel --funding_txid=<txid> --output_index=<n>
```

### Payments

```bash
skills/lnd/scripts/lncli.sh addinvoice --amt=1000 --memo="test payment"
skills/lnd/scripts/lncli.sh decodepayreq <bolt11_invoice>
skills/lnd/scripts/lncli.sh sendpayment --pay_req=<bolt11_invoice>
skills/lnd/scripts/lncli.sh listpayments
```

### Macaroon Bakery

Use the `macaroon-bakery` skill for least-privilege agent credentials:

```bash
skills/macaroon-bakery/scripts/bake.sh --role pay-only
skills/macaroon-bakery/scripts/bake.sh --role invoice-only
skills/macaroon-bakery/scripts/bake.sh --inspect <path-to-macaroon>
```

## Configuration

### Container Config

The Docker compose templates pass configuration via command-line arguments. For
advanced customization, mount a custom `litd.conf`:

- **litd template:** `skills/lnd/templates/litd.conf.template`
- **lnd template (native):** `skills/lnd/templates/lnd.conf.template`

Note: litd requires `lnd.` prefix for lnd flags (e.g., `lnd.bitcoin.active`).
Standalone lnd does not use the prefix.

### Key Defaults

- **Backend:** neutrino (BIP 157/158 light client)
- **Database:** SQLite
- **Network:** testnet (override with `--network mainnet`)
- **Auto-unlock:** enabled via password file

## Container Naming & Ports

| Container | Purpose | Ports |
|-----------|---------|-------|
| `litd` | Main Lightning Terminal | 8443, 10009, 9735, 8080 |
| `litd-signer` | Remote signer (lnd) | 10012, 10013 |
| `litd-bitcoind` | Bitcoin Core (regtest only) | 18443, 28332, 28333 |

### Port Reference

| Port  | Service   | Description                    |
|-------|-----------|--------------------------------|
| 8443  | litd UI   | Lightning Terminal web UI      |
| 9735  | Lightning | Peer-to-peer Lightning Network |
| 10009 | gRPC      | lncli and programmatic access  |
| 8080  | REST      | REST API (wallet, etc.)        |
| 10012 | Signer gRPC | Remote signer RPC            |
| 10013 | Signer REST | Signer REST API              |

## File Locations

| Path | Purpose |
|------|---------|
| `~/.lnget/lnd/wallet-password.txt` | Wallet unlock passphrase (0600) |
| `~/.lnget/lnd/seed.txt` | 24-word mnemonic backup (0600, standalone only) |
| `~/.lnget/lnd/signer-credentials/` | Imported signer credentials (watch-only) |
| `versions.env` | Pinned container image versions |
| `skills/lnd/templates/` | Docker compose and config templates |
| `skills/lnd/profiles/` | Profile .env files |

## Version Pinning

Container image versions are pinned in `versions.env` at the repo root:

```bash
LITD_VERSION=v0.16.0-alpha
LND_VERSION=v0.20.0-beta
```

Override at runtime:

```bash
LITD_VERSION=v0.17.0-alpha skills/lnd/scripts/start-lnd.sh
```

## Integration with lnget

Once litd is running with a funded wallet and open channels:

```bash
lnget config init
lnget ln status
lnget --max-cost 1000 https://api.example.com/paid-data
```

## Security Considerations

See [references/security.md](references/security.md) for detailed guidance.

**Default model (watch-only with remote signer):**
- No seed or private keys on the agent machine
- Signing delegated to signer container via gRPC
- Set up with the `lightning-security-module` skill

**Standalone model (testing only):**
- Wallet passphrase and seed stored on disk (0600)
- Suitable for testnet and quick testing

**Macaroon security:**
- Never give agents the admin macaroon in production
- Bake scoped macaroons with the `macaroon-bakery` skill

## Troubleshooting

### "wallet not found"
Run `skills/lnd/scripts/create-wallet.sh` to create the wallet.

### "wallet locked"
Run `skills/lnd/scripts/unlock-wallet.sh`. Auto-unlock is enabled by default.

### "chain backend is still syncing"
Neutrino needs time to sync headers:
```bash
skills/lnd/scripts/lncli.sh getinfo | jq '{synced_to_chain, block_height}'
```

### Container not starting
```bash
docker logs litd
docker logs litd-signer
```

### "remote signer not reachable"
```bash
docker ps | grep litd-signer
docker logs litd-signer
```
