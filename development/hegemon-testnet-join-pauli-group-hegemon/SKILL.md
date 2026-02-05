---
name: hegemon-testnet-join
description: Join the Hegemon testnet using the shared chainspec, verify genesis, sync to the tip, and enable mining safely.
compatibility: Requires ./target/release/hegemon-node, ./target/release/walletd, network access to hegemon.pauli.group:30333, and a shared chainspec at config/dev-chainspec.json.
metadata:
  repo: Reflexivity/Hegemon
  version: "1.0"
---

# Goal
Connect a new node to the Hegemon testnet, verify it is on the canonical chain, and mine only after sync completes.

# Defaults
- Boot node: hegemon.pauli.group:30333
- Chain spec: config/dev-chainspec.json
- Genesis hash: 0xcaa718106d1530705c53a99628d929cd78d47a0bf06b177aa4853962b47c637d
- RPC port: 9944
- P2P listen: /ip4/0.0.0.0/tcp/30333

# Steps
1. Ensure binaries exist (fresh clones must run make setup and make node):
   - make setup
   - make node
   - cargo build --release -p walletd
2. Verify the shared chainspec matches the boot node. Do not use --chain dev.
   - shasum -a 256 config/dev-chainspec.json
3. Create or open a wallet and export the shielded mining address:
   - export HEGEMON_MINER_ADDRESS=$(printf '%s\n{"id":1,"method":"status.get","params":{}}\n' "YOUR_PASSPHRASE" \
     | ./target/release/walletd --store ~/.hegemon-wallet --mode open \
     | jq -r '.result.primaryAddress')
4. Start the node with the shared chainspec and seed:
   - HEGEMON_MINE=1 \
     HEGEMON_SEEDS="hegemon.pauli.group:30333" \
     HEGEMON_MINER_ADDRESS="$HEGEMON_MINER_ADDRESS" \
     ./target/release/hegemon-node \
       --dev \
       --base-path ~/.hegemon-node \
       --chain config/dev-chainspec.json \
       --listen-addr /ip4/0.0.0.0/tcp/30333 \
       --rpc-port 9944 \
       --rpc-external \
       --rpc-methods safe \
       --name "TestnetNode"
5. Monitor sync status and height. Mining pauses while syncing and resumes once caught up.
   - curl -s -H "Content-Type: application/json" \
     -d '{"id":1,"jsonrpc":"2.0","method":"system_health"}' \
     http://127.0.0.1:9944 | jq
   - curl -s -H "Content-Type: application/json" \
     -d '{"id":1,"jsonrpc":"2.0","method":"hegemon_consensusStatus"}' \
     http://127.0.0.1:9944 | jq
   - curl -s -H "Content-Type: application/json" \
     -d '{"id":1,"jsonrpc":"2.0","method":"chain_getHeader"}' \
     http://127.0.0.1:9944 | jq
6. If height stalls, check peers and genesis hash:
   - curl -s -H "Content-Type: application/json" \
     -d '{"id":1,"jsonrpc":"2.0","method":"chain_getBlockHash","params":[0]}' \
     http://127.0.0.1:9944 | jq

# Notes
- If the genesis hash or chainspec differ, stop the node and wipe the base path before restarting.
- Keep RPC access locked down if you expose it beyond localhost.
