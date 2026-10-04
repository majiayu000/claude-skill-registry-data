---
name: supersim
description: Local Multi-L2 Development Environment for simulating the Superchain. Use when testing cross-chain applications, OP Stack deployments, or L1/L2 message passing locally.
---

# Supersim

Supersim is a local multi-L2 development environment that simulates the Superchain with a single L1 and multiple OP-Stack L2s.

## Quick Start

```bash
# Install
brew install ethereum-optimism/tap/supersim

# Start vanilla mode (3 chains: L1=900, L2s=901,902)
supersim
```

## Core Concepts

- **Vanilla Mode**: Local dev chains with predeployed OP Stack contracts
- **Fork Mode**: Fork real networks (mainnet, testnet) locally
- **Interop**: L2-to-L2 message passing and SuperchainERC20 tokens

## Chain Configuration (Vanilla)

| Chain | ChainID | RPC Port |
|-------|---------|----------|
| L1    | 900     | 8545     |
| OPChainA | 901  | 9545     |
| OPChainB | 902  | 9546     |

## Common Commands

```bash
# Vanilla mode with auto-relay for L2->L2 transfers
supersim --interop.autorelay

# Fork mode - specify chains to fork
supersim fork --chains=op,base,zora

# Fork with interop contracts
supersim fork --chains=op,base,zora --interop.enabled
```

## Example: L1 to L2 Deposit

```bash
# 1. Check L2 balance
cast balance 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 --rpc-url http://127.0.0.1:9545

# 2. Bridge ETH (use L1StandardBridge address from supersim output)
cast send <L1StandardBridgeAddress> "bridgeETH(uint32,bytes)" 50000 0x \
  --value 0.1ether --rpc-url http://127.0.0.1:8545 \
  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

# 3. Verify L2 balance increased
cast balance 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 --rpc-url http://127.0.0.1:9545
```

## Example: L2 to L2 Transfer

```bash
# Requires --interop.autorelay flag on supersim

# 1. Mint tokens on source chain (901)
cast send 0x420beeF000000000000000000000000000000001 \
  "mint(address,uint256)" 0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 1000 \
  --rpc-url http://127.0.0.1:9545 \
  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

# 2. Send to destination chain (902)
cast send 0x4200000000000000000000000000000000000028 \
  "sendERC20(address,address,uint256,uint256)" \
  0x420beeF000000000000000000000000000000001 \
  0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 1000 902 \
  --rpc-url http://127.0.0.1:9545 \
  --private-key 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80

# 3. Check balance on destination chain
cast balance --erc20 0x420beeF000000000000000000000000000000001 \
  0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266 --rpc-url http://127.0.0.1:9546
```

## Key Predeploy Addresses (Vanilla)

| Contract | Address |
|----------|---------|
| L2NativeSuperchainERC20 | 0x420beeF000000000000000000000000000000001 |
| SuperchainTokenBridge | 0x4200000000000000000000000000000000000028 |

## Docker Usage

```bash
# Build
docker build -t supersim .

# Run
docker run --rm -it --network host supersim:latest
```

## Resources

- [Full Documentation](https://supersim.pages.dev)
- [Training Video](https://www.youtube.com/live/Kh4fNshcl5Y?t=30s)
- [SuperchainERC20 Starter Kit](https://github.com/ethereum-optimism/superchainerc20-starter)
